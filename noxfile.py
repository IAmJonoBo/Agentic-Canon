"""Automation sessions for Agentic Canon."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, Iterable, Iterator, Mapping, Sequence

import nox

SANITY_SECTIONS = (
    "core",
    "templates",
    "examples",
    "dashboards",
    "videos",
    "cloud",
    "cli",
    "tests",
)

RENDER_ROOT = Path("build/template-renders")
RENDER_INDEX = RENDER_ROOT / "index.json"
REPO_ROOT = Path(__file__).parent.resolve()
TRUNK_SCRIPT = REPO_ROOT / ".dev" / "trunk-with-progress.sh"

nox.options.error_on_missing_interpreters = False
nox.options.reuse_existing_virtualenvs = True


def _run_sanity(session: nox.Session, *sections: str) -> None:
    command = ["./.dev/sanity-check.sh"]
    for section in sections:
        command.extend(["--section", section])
    session.run(*command, external=True)


def _load_manifest_templates() -> Dict[str, Mapping[str, object]]:
    from templates._shared.manifest import load_manifest  # pylint: disable=import-outside-toplevel

    manifest = load_manifest()
    return manifest.get("templates", {})


def _arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--template", action="append", dest="templates")
    parser.add_argument("--context", action="append", dest="contexts")
    parser.add_argument("--feature", action="append", dest="features")
    parser.add_argument("--force", action="store_true")
    return parser


def _parse_feature_filters(feature_args: Iterable[str] | None) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for clause in feature_args or []:
        if "=" not in clause:
            raise ValueError(f"Feature filter must be NAME=value, got '{clause}'")
        name, value = clause.split("=", 1)
        result[name.strip()] = value.strip()
    return result


def _iter_render_targets(
    templates: Mapping[str, Mapping[str, object]],
    args: argparse.Namespace,
) -> Iterator[tuple[str, str, Dict[str, str], Mapping[str, object]]]:
    template_filter = set(args.templates or [])
    context_filter = set(args.contexts or [])
    feature_filter = _parse_feature_filters(args.features)

    for template_name, template_cfg in templates.items():
        if template_filter and template_name not in template_filter:
            continue

        sample_contexts = template_cfg.get("sample_contexts", {})
        if not isinstance(sample_contexts, Mapping):
            continue

        for context_name, context in sample_contexts.items():
            if context_filter and context_name not in context_filter:
                continue
            if not isinstance(context, Mapping):
                continue

            # Feature filters require the context value to match the desired value.
            if feature_filter:
                context_dict = {str(k): str(v) for k, v in context.items()}
                if not all(context_dict.get(name) == value for name, value in feature_filter.items()):
                    continue
            yield template_name, context_name, dict(context), template_cfg


def _ensure_clean_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


@nox.session
def render_templates(session: nox.Session) -> None:
    """Render all template/context combinations into build/template-renders."""
    parser = _arg_parser()
    args = parser.parse_args(session.posargs)

    session.install("cookiecutter==2.6.0")

    from cookiecutter.main import cookiecutter  # pylint: disable=import-outside-toplevel
    from templates._shared import cache as cache_utils  # pylint: disable=import-outside-toplevel

    templates = _load_manifest_templates()
    targets = list(_iter_render_targets(templates, args))
    if not targets:
        session.log("No template contexts matched the provided filters.")
        return

    _ensure_clean_directory(RENDER_ROOT)
    index: list[dict[str, str]] = []

    session.env.setdefault("AGENTIC_CANON_SKIP_GIT_INIT", "1")
    session.env.setdefault("AGENTIC_CANON_SKIP_MESSAGES", "1")

    for template_name, context_name, extra_context, template_cfg in targets:
        template_root = Path(template_cfg["root"])  # type: ignore[index]
        session.log(f"Rendering template '{template_name}' context '{context_name}'")

        def _produce(destination: Path) -> None:
            cookiecutter(
                str(template_root),
                no_input=True,
                extra_context=extra_context,
                output_dir=str(destination),
            )
            slug = extra_context.get("project_slug") or extra_context.get("project_slug", template_name)
            generated = destination / str(slug)
            if generated.exists():
                for item in generated.iterdir():
                    shutil.move(str(item), destination)
                shutil.rmtree(generated)

        cache_dir = cache_utils.prime_template_cache(
            template_name,
            extra_context,
            _produce,
            force=args.force,
        )

        render_path = RENDER_ROOT / template_name / context_name
        cache_utils.copy_from_cache(cache_dir, render_path)

        index.append(
            {
                "template": template_name,
                "context": context_name,
                "path": str(render_path),
                "cache_dir": str(cache_dir),
            }
        )

    with RENDER_INDEX.open("w", encoding="utf-8") as handle:
        json.dump({"entries": index}, handle, indent=2)


def _load_render_index() -> Sequence[Mapping[str, str]]:
    if not RENDER_INDEX.exists():
        raise FileNotFoundError(
            "Template render index not found. Run `nox -s render_templates` first."
        )
    data = json.loads(RENDER_INDEX.read_text(encoding="utf-8"))
    return data.get("entries", [])


def _copy_trunk_configuration(project_path: Path, template_cfg: Mapping[str, object]) -> None:
    trunk_cfg = template_cfg.get("trunk", {})
    inherit = True
    if isinstance(trunk_cfg, Mapping):
        inherit = bool(trunk_cfg.get("inherit_from_root", True))

    if not inherit:
        return

    trunk_root = REPO_ROOT / ".trunk"
    if not trunk_root.exists():
        return

    target_trunk = project_path / ".trunk"
    if target_trunk.exists():
        shutil.rmtree(target_trunk)
    shutil.copytree(trunk_root, target_trunk, dirs_exist_ok=True)


@nox.session
def lint_templates(session: nox.Session) -> None:
    """Run Trunk checks across rendered template variants."""
    parser = _arg_parser()
    args = parser.parse_args(session.posargs)

    templates = _load_manifest_templates()
    entries = _load_render_index()
    if not entries:
        session.error("No rendered templates found. Run `nox -s render_templates` first.")

    for entry in entries:
        template_name = entry["template"]
        context_name = entry["context"]
        if args.templates and template_name not in args.templates:
            continue
        if args.contexts and context_name not in args.contexts:
            continue

        project_path = Path(entry["path"])
        if not project_path.exists():
            session.warn(f"Rendered project missing at {project_path}; skipping.")
            continue

        template_cfg = templates.get(template_name, {})
        _copy_trunk_configuration(project_path, template_cfg)

        session.log(f"[lint] {template_name} :: {context_name}")
        with session.chdir(str(project_path)):
            session.run(
                str(TRUNK_SCRIPT),
                "check",
                "--all",
                external=True,
            )


@nox.session
def format_templates(session: nox.Session) -> None:
    """Format rendered templates and fail if formatting introduces changes."""
    parser = _arg_parser()
    args = parser.parse_args(session.posargs)

    templates = _load_manifest_templates()
    entries = _load_render_index()
    if not entries:
        session.error("No rendered templates found. Run `nox -s render_templates` first.")

    for entry in entries:
        template_name = entry["template"]
        context_name = entry["context"]
        if args.templates and template_name not in args.templates:
            continue
        if args.contexts and context_name not in args.contexts:
            continue

        project_path = Path(entry["path"])
        if not project_path.exists():
            session.warn(f"Rendered project missing at {project_path}; skipping.")
            continue

        template_cfg = templates.get(template_name, {})
        _copy_trunk_configuration(project_path, template_cfg)

        session.log(f"[format] {template_name} :: {context_name}")
        with session.chdir(str(project_path)):
            session.run(
                str(TRUNK_SCRIPT),
                "fmt",
                "--all",
                external=True,
            )
            result = session.run("git", "status", "--porcelain", external=True, silent=True)
            if result.stdout.strip():
                session.error(f"Formatting produced changes in {project_path}")


@nox.session
def upgrade_tools(session: nox.Session) -> None:
    """Upgrade shared tooling (Trunk, linters, template dependencies)."""
    parser = _arg_parser()
    args = parser.parse_args(session.posargs)

    session.log("Upgrading Trunk CLI and pinned plugins.")
    session.run(".dev/trunk-with-progress.sh", "upgrade", external=True)

    session.log("Template-specific dependency upgrade hooks not yet implemented.")
    if args.templates:
        session.log(f"Templates requested for upgrade: {', '.join(args.templates)}")


@nox.session
def sanity(session: nox.Session) -> None:
    """Run the full sanity check."""
    _run_sanity(session)


def _register_section_session(section: str) -> None:
    @nox.session(name=f"sanity_{section}")
    def sanity_section(session: nox.Session, section: str = section) -> None:
        """Run a single sanity-check section."""
        _run_sanity(session, section)

    globals()[f"sanity_{section}"] = sanity_section


for _section in SANITY_SECTIONS:
    _register_section_session(_section)


@nox.session
def tests(session: nox.Session) -> None:
    """Execute the pytest suite with xdist parallelism."""
    session.install("-r", "requirements.txt")
    session.run("pytest", "-n", "auto")

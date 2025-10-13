"""Automation sessions for Agentic Canon."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import sys
import time
from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, cast

import nox  # type: ignore[import]

from agentic_canon_cli import pip_support

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
TRUNK_BIN = Path.home() / ".cache" / "trunk" / "bin" / "trunk"
SYNC_MANIFEST_SCRIPT = REPO_ROOT / ".dev" / "scripts" / "sync-manifest.py"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
TEMPLATES_DIR = REPO_ROOT / "templates"
if str(TEMPLATES_DIR) not in sys.path:
    sys.path.insert(0, str(TEMPLATES_DIR))

if "PYTHONPATH" not in os.environ:
    os.environ["PYTHONPATH"] = f"{REPO_ROOT}{os.pathsep}{TEMPLATES_DIR}"
else:
    existing_paths = os.environ["PYTHONPATH"].split(os.pathsep)
    if str(REPO_ROOT) not in existing_paths:
        existing_paths.insert(0, str(REPO_ROOT))
    if str(TEMPLATES_DIR) not in existing_paths:
        existing_paths.insert(0, str(TEMPLATES_DIR))
    os.environ["PYTHONPATH"] = os.pathsep.join(existing_paths)

nox.options.error_on_missing_interpreters = False
nox.options.reuse_existing_virtualenvs = True


def _run_sanity(session: nox.Session, *sections: str) -> None:
    command = ["./.dev/sanity-check.sh"]
    for section in sections:
        command.extend(["--section", section])
    session.run(*command, external=True)


def _load_manifest_templates() -> dict[str, Mapping[str, Any]]:
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


def _parse_feature_filters(feature_args: Iterable[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for clause in feature_args or []:
        if "=" not in clause:
            raise ValueError(f"Feature filter must be NAME=value, got '{clause}'")
        name, value = clause.split("=", 1)
        result[name.strip()] = value.strip()
    return result


def _iter_render_targets(
    templates: Mapping[str, Mapping[str, Any]],
    args: argparse.Namespace,
) -> Iterator[tuple[str, str, dict[str, str], Mapping[str, Any]]]:
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
                matches = all(
                    context_dict.get(name) == value for name, value in feature_filter.items()
                )
                if not matches:
                    continue
            yield template_name, context_name, dict(context), template_cfg


def _ensure_clean_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _ensure_trunk(session: nox.Session) -> None:
    """Install the Trunk CLI if it is not already present."""
    existing = shutil.which("trunk")
    if existing:
        return

    install_path = TRUNK_BIN.parent
    session.log("Installing Trunk CLI")
    session.run(
        "bash",
        "-c",
        "curl https://get.trunk.io -fsSL | bash -s -- -y",
        external=True,
    )

    session.env["PATH"] = f"{install_path}:{session.env.get('PATH', os.environ.get('PATH', ''))}"
    if not shutil.which("trunk"):
        session.error("Trunk installation failed")


@contextmanager
def _session_timer(session: nox.Session, label: str):
    start = time.perf_counter()
    session.log(f"[timer] {label} started")
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        session.log(f"[timer] {label} finished in {duration:.2f}s")


def _collect_key_material(project_path: Path, candidates: Iterable[str]) -> list[bytes]:
    material: list[bytes] = []
    for relative in candidates:
        candidate_path = project_path / relative
        if candidate_path.exists():
            material.append(candidate_path.read_bytes())
    if not material:
        material.append(str(project_path).encode("utf-8"))
    return material


def _resolve_env(project_path: Path, env_cfg: Mapping[str, Any] | None) -> dict[str, str]:
    resolved: dict[str, str] = {}
    for key, value in (env_cfg or {}).items():
        if not isinstance(value, str):
            continue
        if value.startswith("$") or value.startswith("${"):
            resolved[str(key)] = value
            continue
        candidate = Path(value)
        if candidate.is_absolute():
            resolved[str(key)] = str(candidate)
        else:
            resolved[str(key)] = str((project_path / candidate).resolve())
    return resolved


def _run_installers(
    session: nox.Session,
    project_path: Path,
    cache_cfg: Mapping[str, Any] | None,
    *,
    force: bool,
) -> None:
    if not cache_cfg:
        return

    from templates._shared import cache as cache_utils  # pylint: disable=import-outside-toplevel

    installers = cache_cfg.get("installers", {})
    if not isinstance(installers, Mapping):
        return

    def _command_list(default: Sequence[str], cfg: Mapping[str, Any]) -> list[str]:
        command = cfg.get("command")
        if isinstance(command, Sequence) and not isinstance(command, str):
            return [str(part) for part in command]
        return list(default)

    # Node.js dependencies
    node_cfg = installers.get("node")
    if isinstance(node_cfg, Mapping) and node_cfg.get("enabled"):
        key_files = node_cfg.get("key_files") or ["package-lock.json", "package.json"]
        key_material = _collect_key_material(project_path, [str(f) for f in key_files])
        command = _command_list(["npm", "install", "--no-fund", "--no-audit"], node_cfg)

        def _node_installer(path: Path) -> None:
            with session.chdir(str(path)):
                session.run(*command, external=True)

        cache_utils.cache_node_modules(project_path, key_material, _node_installer, force=force)

    # Python / pip dependencies
    pip_cfg = installers.get("pip")
    if isinstance(pip_cfg, Mapping) and pip_cfg.get("enabled"):
        key_files = pip_cfg.get("key_files") or ["requirements.txt", "pyproject.toml"]
        key_material = _collect_key_material(project_path, [str(f) for f in key_files])
        command = _command_list(
            ["python", "-m", "pip", "install", "-r", "requirements.txt"], pip_cfg
        )

        def _pip_installer(path: Path) -> None:
            with session.chdir(str(path)):
                session.run(*command, external=True)

        cache_utils.cache_pip_install(project_path, key_material, _pip_installer, force=force)

    # Go module downloads
    go_cfg = installers.get("go")
    if isinstance(go_cfg, Mapping) and go_cfg.get("enabled"):
        key_files = go_cfg.get("key_files") or ["go.sum", "go.mod"]
        key_material = _collect_key_material(project_path, [str(f) for f in key_files])
        command = _command_list(["go", "mod", "download"], go_cfg)
        env_cfg = go_cfg.get("env")
        env = _resolve_env(project_path, env_cfg) if isinstance(env_cfg, Mapping) else {}

        def _go_installer(path: Path) -> None:
            with session.chdir(str(path)):
                session.run(*command, external=True, env=env)

        cache_utils.cache_go_modules(project_path, key_material, _go_installer, force=force)


@nox.session
def render_templates(session: nox.Session) -> None:
    """Render all template/context combinations into build/template-renders."""
    with _session_timer(session, "render_templates"):
        parser = _arg_parser()
        args = parser.parse_args(session.posargs)

        session.install("PyYAML>=6.0")  # manifest sync depends on PyYAML
        session.run(
            "python3",
            str(REPO_ROOT / ".dev" / "scripts" / "sync-manifest.py"),
            "--check",
            external=True,
        )

        session.install("cookiecutter==2.6.0")
        existing_pythonpath = session.env.get("PYTHONPATH")
        extra_paths = [str(REPO_ROOT), str(TEMPLATES_DIR)]
        if existing_pythonpath:
            session.env["PYTHONPATH"] = os.pathsep.join(extra_paths + [existing_pythonpath])
        else:
            session.env["PYTHONPATH"] = os.pathsep.join(extra_paths)

        python_env_script = (
            "import json, sys; print(json.dumps({'prefix': sys.prefix, "
            "'version': sys.version_info[:2]}))"
        )
        python_env_info = session.run(
            "python",
            "-c",
            python_env_script,
            silent=True,
        )
        python_env_stdout = ""
        if isinstance(python_env_info, str):
            python_env_stdout = python_env_info.strip()
        elif python_env_info:
            python_env_stdout = getattr(python_env_info, "stdout", "").strip()
        if python_env_stdout:
            try:
                payload = json.loads(python_env_stdout.splitlines()[-1])
            except json.JSONDecodeError:
                payload = {}
            else:
                prefix = payload.get("prefix")
                version = payload.get("version") or []
                if isinstance(prefix, str) and isinstance(version, list) and len(version) >= 2:
                    major, minor = version[:2]
                    site_packages_path = (
                        Path(prefix) / "lib" / f"python{major}.{minor}" / "site-packages"
                    )
                    if site_packages_path.exists():
                        candidate = str(site_packages_path)
                        if candidate not in sys.path:
                            sys.path.insert(0, candidate)

        cookiecutter = importlib.import_module("cookiecutter.main").cookiecutter
        cache_utils = importlib.import_module("templates._shared.cache")

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
            root_value_obj = template_cfg.get("root")  # type: ignore[call-overload]
            if not isinstance(root_value_obj, str):
                session.error(f"Template '{template_name}' is missing a valid 'root' path")
            template_root = Path(cast(str, root_value_obj))
            session.log(f"Rendering template '{template_name}' context '{context_name}'")

            context_payload = dict(extra_context)
            slug_value = str(context_payload.get("project_slug") or template_name)

            def _produce(
                destination: Path,
                *,
                cookiecutter_func=cookiecutter,
                template_root_path=template_root,
                payload=context_payload,
                slug=slug_value,
            ) -> None:
                cookiecutter(
                    str(template_root_path),
                    no_input=True,
                    extra_context=payload,
                    output_dir=str(destination),
                )
                generated = destination / slug
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
            cache_cfg = template_cfg.get("cache", {}) if isinstance(template_cfg, Mapping) else {}
            if isinstance(cache_cfg, Mapping):
                _run_installers(session, render_path, cache_cfg, force=args.force)

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


def _copy_trunk_configuration(project_path: Path, template_cfg: Mapping[str, Any]) -> None:
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
        if target_trunk.is_symlink():
            target_trunk.unlink()
        else:
            shutil.rmtree(target_trunk)
    try:
        os.symlink(trunk_root, target_trunk, target_is_directory=True)
    except OSError:
        shutil.copytree(trunk_root, target_trunk, dirs_exist_ok=True)


def _ensure_git_repo(
    session: nox.Session, project_path: Path, default_branch: str = "main"
) -> None:
    with session.chdir(str(project_path)):
        session.run("git", "init", "-q", external=True)
        session.run(
            "git",
            "symbolic-ref",
            "HEAD",
            f"refs/heads/{default_branch}",
            external=True,
        )
        head_ref = project_path / ".git" / "refs" / "heads" / default_branch
        if not head_ref.exists():
            session.run("git", "config", "user.name", "Template Bot", external=True)
            session.run("git", "config", "user.email", "template@example.com", external=True)
            session.run(
                "git",
                "commit",
                "--allow-empty",
                "-m",
                "Initial commit",
                external=True,
            )


def _quality_commands(template_cfg: Mapping[str, Any], category: str) -> list[dict[str, Any]]:
    quality_cfg = template_cfg.get("quality")
    if not isinstance(quality_cfg, Mapping):
        return []

    category_entries = quality_cfg.get(category)
    if not isinstance(category_entries, Sequence):
        return []

    commands: list[dict[str, Any]] = []
    for entry in category_entries:
        if not isinstance(entry, Mapping):
            continue
        run = entry.get("run")
        if not isinstance(run, Sequence) or isinstance(run, str):
            continue
        env_cfg = entry.get("env")
        env: dict[str, str] = {}
        if isinstance(env_cfg, Mapping):
            env = {str(key): str(value) for key, value in env_cfg.items() if isinstance(value, str)}
        workdir = str(entry.get("workdir") or ".")
        commands.append(
            {
                "name": str(entry.get("name") or " ".join(str(part) for part in run)),
                "command": [str(part) for part in run],
                "env": env,
                "workdir": workdir,
            }
        )
    return commands


@nox.session
def lint_templates(session: nox.Session) -> None:
    """Run Trunk checks across rendered template variants."""
    with _session_timer(session, "lint_templates"):
        parser = _arg_parser()
        args = parser.parse_args(session.posargs)

        templates = _load_manifest_templates()
        entries = _load_render_index()
        if not entries:
            session.error("No rendered templates found. Run `nox -s render_templates` first.")

        _ensure_trunk(session)

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
            _ensure_git_repo(session, project_path)

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
    with _session_timer(session, "format_templates"):
        parser = _arg_parser()
        args = parser.parse_args(session.posargs)

        templates = _load_manifest_templates()
        entries = _load_render_index()
        if not entries:
            session.error("No rendered templates found. Run `nox -s render_templates` first.")

        _ensure_trunk(session)

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
            _ensure_git_repo(session, project_path)

            session.log(f"[format] {template_name} :: {context_name}")
            with session.chdir(str(project_path)):
                session.run(
                    str(TRUNK_SCRIPT),
                    "fmt",
                    "--all",
                    external=True,
                )
                git_status = session.run(
                    "git",
                    "status",
                    "--porcelain",
                    external=True,
                    silent=True,
                )
                stdout = getattr(git_status, "stdout", "")
                if isinstance(stdout, str) and stdout.strip():
                    session.error(f"Formatting produced changes in {project_path}")


@nox.session
def type_templates(session: nox.Session) -> None:
    """Execute template-configured type-check commands across render variants."""
    with _session_timer(session, "type_templates"):
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
            commands = _quality_commands(template_cfg, "type")
            if not commands:
                session.log(f"[type] {template_name} :: {context_name} (no commands configured)")
                continue

            for command in commands:
                workdir = project_path / command["workdir"]
                if not workdir.exists():
                    session.warn(
                        f"[{command['name']}] Working directory {workdir} missing; skipping."
                    )
                    continue
                env = session.env.copy()
                env.update(command["env"])
                session.log(f"[type] {template_name} :: {context_name} :: {command['name']}")
                with session.chdir(str(workdir)):
                    session.run(*command["command"], external=True, env=env)


@nox.session
def security_templates(session: nox.Session) -> None:
    """Run template-configured and Trunk security checks across render variants."""
    with _session_timer(session, "security_templates"):
        parser = _arg_parser()
        args = parser.parse_args(session.posargs)

        templates = _load_manifest_templates()
        entries = _load_render_index()
        if not entries:
            session.error("No rendered templates found. Run `nox -s render_templates` first.")

        success, detail = pip_support.ensure_safe_pip(Path(sys.executable), quiet=True)
        if not success:
            session.error(f"Failed to upgrade pip: {detail}")

        _ensure_trunk(session)

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

            manifest_commands = _quality_commands(template_cfg, "security")
            for command in manifest_commands:
                workdir = project_path / command["workdir"]
                if not workdir.exists():
                    session.warn(
                        f"[{command['name']}] Working directory {workdir} missing; skipping."
                    )
                    continue
                env = session.env.copy()
                env.update(command["env"])
                session.log(f"[security] {template_name} :: {context_name} :: {command['name']}")
                with session.chdir(str(workdir)):
                    session.run(*command["command"], external=True, env=env)

            template_cfg = templates.get(template_name, {})
            _copy_trunk_configuration(project_path, template_cfg)
            _ensure_git_repo(session, project_path)

            session.log(f"[security] {template_name} :: {context_name} :: trunk")
            with session.chdir(str(project_path)):
                session.run(
                    str(TRUNK_SCRIPT),
                    "check",
                    "--all",
                    "--scope",
                    "security",
                    external=True,
                )


@nox.session
def upgrade_tools(session: nox.Session) -> None:
    """Upgrade shared tooling (Trunk, linters, template dependencies)."""
    with _session_timer(session, "upgrade_tools"):
        parser = _arg_parser()
        args = parser.parse_args(session.posargs)

        _ensure_trunk(session)

        session.log("Upgrading Trunk CLI and pinned plugins.")
        session.run(".dev/trunk-with-progress.sh", "upgrade", external=True)

        session.log("Template-specific dependency upgrade hooks not yet implemented.")
        if args.templates:
            session.log(f"Templates requested for upgrade: {', '.join(args.templates)}")


@nox.session
def validate_templates_all(session: nox.Session) -> None:
    """Run manifest sync, render, lint, and format in sequence for templates."""
    with _session_timer(session, "validate_templates_all"):
        session.log("Starting unified template validation pipeline.")
        notify_args = list(session.posargs)
        session.notify("sync_manifest", [])
        session.notify("render_templates", notify_args)
        session.notify("lint_templates", notify_args)
        session.notify("type_templates", notify_args)
        session.notify("security_templates", notify_args)
        session.notify("format_templates", notify_args)


@nox.session
def sync_manifest(session: nox.Session) -> None:
    """Synchronise manifest.json from manifest.yaml."""
    session.install("PyYAML==6.0.2")
    command = [str(SYNC_MANIFEST_SCRIPT)]
    command.extend(session.posargs)
    session.run(*command, external=True)


@nox.session
def sanity(session: nox.Session) -> None:
    """Run the full sanity check."""
    session.install(
        "pip-audit==2.9.0",
        "pip-licenses==5.0.0",
    )
    success, detail = pip_support.ensure_safe_pip(Path(sys.executable), quiet=True)
    if not success:
        session.error(f"Failed to upgrade pip: {detail}")
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


@nox.session
def typecheck(session: nox.Session) -> None:
    """Run static type checks with mypy."""
    session.install("-r", "requirements.txt")
    session.run("mypy", "--config-file", "mypy.ini")

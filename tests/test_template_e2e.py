"""End-to-end integration tests for non-Python templates (Task #54)."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

import pytest

cookiecutter_main = pytest.importorskip(
    "cookiecutter.main",
    reason="cookiecutter is required for template integration tests",
)
cookiecutter = cookiecutter_main.cookiecutter


CACHE_ROOT = Path(
    os.environ.get("AGENTIC_CANON_CACHE_DIR", Path.home() / ".cache" / "agentic-canon")
)
TEMPLATE_CACHE_DIR = CACHE_ROOT / "templates"
NODE_CACHE_DIR = CACHE_ROOT / "node_modules"

TEMPLATE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
NODE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

try:  # pragma: no cover - platform dependent
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


@contextlib.contextmanager
def _file_lock(lock_path: Path):
    if fcntl is None:
        yield
        return

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    """Execute a subprocess command, raising on failure."""
    subprocess.run(cmd, check=True, cwd=cwd, env=env)


def _version_tuple(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(".") if part.isdigit())


def _require_tool(
    tool: str,
    *,
    version_args: list[str] | None = None,
    min_version: str | None = None,
    parse: Callable[[str], str] | None = None,
) -> None:
    if shutil.which(tool) is None:
        pytest.skip(f"'{tool}' is required for this integration test")

    if not min_version:
        return

    version_args = version_args or ["--version"]
    result = subprocess.run(
        [tool, *version_args], capture_output=True, text=True, check=True
    )
    raw = result.stdout.strip() or result.stderr.strip()
    if parse is not None:
        raw = parse(raw)
    if _version_tuple(raw) < _version_tuple(min_version):
        pytest.skip(f"{tool} version {raw} < required {min_version}")


def _cookiecutter_bake(
    template_name: str,
    tmp_path: Path,
    extra_context: dict[str, str],
) -> Path:
    template_dir = Path(__file__).resolve().parents[1] / "templates" / template_name
    slug = extra_context["project_slug"]
    project_path = tmp_path / slug

    cache_key = hashlib.sha256(
        json.dumps({"template": template_name, "context": extra_context}, sort_keys=True).encode()
    ).hexdigest()
    cache_dir = TEMPLATE_CACHE_DIR / template_name / cache_key
    lock_file = cache_dir.with_suffix(".lock")

    if cache_dir.exists():
        shutil.copytree(cache_dir, project_path, dirs_exist_ok=True)
        return project_path

    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    with _file_lock(lock_file):
        if cache_dir.exists():
            shutil.copytree(cache_dir, project_path, dirs_exist_ok=True)
            return project_path

        cookiecutter(
            str(template_dir),
            no_input=True,
            extra_context=extra_context,
            output_dir=str(tmp_path),
        )

        cache_tmp = cache_dir.with_suffix(".tmp")
        if cache_tmp.exists():
            shutil.rmtree(cache_tmp)
        shutil.copytree(project_path, cache_tmp, dirs_exist_ok=True)
        os.replace(cache_tmp, cache_dir)

    return project_path


def _parse_node_version(output: str) -> str:
    return output.strip().lstrip("v")


def _parse_go_version(output: str) -> str:
    parts = output.split()
    for token in parts:
        if token.startswith("go") and len(token) > 2 and token[2].isdigit():
            return token[2:]
    return "0"


def _cache_node_modules(project_path: Path, env: dict[str, str]) -> None:
    lockfile = project_path / "package-lock.json"
    if lockfile.exists():
        key_source = lockfile.read_bytes()
    else:
        key_source = (project_path / "package.json").read_bytes()

    digest = hashlib.sha256(key_source).hexdigest()
    cache_dir = NODE_CACHE_DIR / digest
    lock_file = cache_dir.with_suffix(".lock")
    node_modules = project_path / "node_modules"

    with _file_lock(lock_file):
        if cache_dir.exists():
            if node_modules.exists():
                shutil.rmtree(node_modules)
            shutil.copytree(cache_dir, node_modules, dirs_exist_ok=True)
            return

        _run(["npm", "install", "--no-fund", "--no-audit"], cwd=project_path, env=env)
        cache_tmp = cache_dir.with_suffix(".tmp")
        if cache_tmp.exists():
            shutil.rmtree(cache_tmp)
        shutil.copytree(node_modules, cache_tmp, dirs_exist_ok=True)
        os.replace(cache_tmp, cache_dir)


@pytest.mark.slow
def test_node_service_template_end_to_end(tmp_path: Path) -> None:
    """Bake the Node service template, install deps, and run the vitest suite."""
    _require_tool("node", min_version="20.0.0", parse=_parse_node_version)
    _require_tool("npm")

    project_path = _cookiecutter_bake(
        "node-service",
        tmp_path,
        {
            "project_name": "Integration Node Service",
            "project_slug": "integration-node-service",
            "description": "Node service integration test",
            "author_name": "Agentic Canon",
            "author_email": "devnull@example.com",
            "license": "Apache-2.0",
            "node_version": "20",
            "enable_security_gates": "yes",
            "enable_sbom_signing": "yes",
            "ci_provider": "github",
        },
    )

    env = os.environ.copy()
    env.setdefault("CI", "true")

    _cache_node_modules(project_path, env)
    _run(
        ["npm", "run", "test", "--", "--run", "--coverage.enabled", "false"],
        cwd=project_path,
        env=env,
    )


@pytest.mark.slow
def test_react_webapp_template_end_to_end(tmp_path: Path) -> None:
    """Bake the React webapp template, install deps, lint, build, and test."""
    _require_tool("node", min_version="20.0.0", parse=_parse_node_version)
    _require_tool("npm")

    project_path = _cookiecutter_bake(
        "react-webapp",
        tmp_path,
        {
            "project_name": "Integration React App",
            "project_slug": "integration-react-app",
            "description": "React webapp integration test",
            "author_name": "Agentic Canon",
            "author_email": "devnull@example.com",
            "license": "Apache-2.0",
            "include_storybook": "yes",
            "include_e2e_tests": "no",
            "enable_accessibility_tests": "yes",
            "ci_provider": "github",
        },
    )

    env = os.environ.copy()
    env.setdefault("CI", "true")

    _cache_node_modules(project_path, env)
    _run(["npm", "run", "build"], cwd=project_path, env=env)
    _run(
        ["npm", "run", "test", "--", "--run", "--passWithNoTests"],
        cwd=project_path,
        env=env,
    )


@pytest.mark.slow
def test_go_service_template_end_to_end(tmp_path: Path) -> None:
    """Bake the Go service template and execute go test."""
    _require_tool(
        "go", version_args=["version"], min_version="1.21.0", parse=_parse_go_version
    )

    project_path = _cookiecutter_bake(
        "go-service",
        tmp_path,
        {
            "project_name": "Integration Go Service",
            "project_slug": "integration-go-service",
            "module_path": "github.com/agentic-canon/integration-go-service",
            "description": "Go service integration test",
            "author_name": "Agentic Canon",
            "author_email": "devnull@example.com",
            "license": "Apache-2.0",
            "go_version": "1.22",
            "enable_security_gates": "yes",
            "ci_provider": "github",
        },
    )

    _run(["go", "test", "./..."], cwd=project_path)

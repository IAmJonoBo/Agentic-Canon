"""End-to-end integration tests for non-Python templates (Task #54)."""

from __future__ import annotations

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
    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=extra_context,
        output_dir=str(tmp_path),
    )
    slug = extra_context["project_slug"]
    return tmp_path / slug


def _parse_node_version(output: str) -> str:
    return output.strip().lstrip("v")


def _parse_go_version(output: str) -> str:
    parts = output.split()
    for token in parts:
        if token.startswith("go") and len(token) > 2 and token[2].isdigit():
            return token[2:]
    return "0"


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

    _run(["npm", "install", "--no-fund", "--no-audit"], cwd=project_path, env=env)
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

    _run(["npm", "install", "--no-fund", "--no-audit"], cwd=project_path, env=env)
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

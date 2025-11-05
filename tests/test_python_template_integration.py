"""Integration test for the Python service template (Task #52).

This simulates a real project workflow:
1. Generate the template with common options enabled.
2. Create an isolated virtual environment.
3. Install the project in editable mode with dev dependencies.
4. Run the project's pytest suite to ensure everything passes.

The test is marked as "slow" because it performs package installs.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = REPO_ROOT / "applications" / "scaffolder" / "templates"

cookiecutter_main = pytest.importorskip(
    "cookiecutter.main",
    reason="cookiecutter is required for the Python template integration test",
)
cookiecutter = cookiecutter_main.cookiecutter


def _venv_python(venv_path: Path) -> Path:
    """Return the Python executable inside the virtual environment."""
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def _venv_pip(venv_path: Path) -> Path:
    """Return the pip executable inside the virtual environment."""
    if os.name == "nt":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a subprocess command, showing output on failure."""
    subprocess.run(cmd, check=True, cwd=cwd)


@pytest.mark.slow
def test_python_template_real_world_flow(tmp_path: Path) -> None:
    """Bake the template, install deps, and run pytest (Task #52)."""
    template_dir = TEMPLATES_ROOT / "python-service"
    output_dir = tmp_path

    cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context={
            "project_name": "Integration Service",
            "project_slug": "integration-service",
            "pkg_name": "integration_service",
            "project_description": "Integration test for the python template",
            "author_name": "Agentic Canon",
            "author_email": "devnull@example.com",
            "license": "Apache-2.0",
            "include_jupyter_book": "no",
            "enable_security_gates": "yes",
            "enable_sbom_signing": "yes",
            "enable_contract_tests": "yes",
            "ci_provider": "github",
        },
        output_dir=str(output_dir),
    )

    project_path = output_dir / "integration-service"
    venv_path = project_path / ".venv"

    # 1. Create a virtual environment for isolation.
    _run([sys.executable, "-m", "venv", str(venv_path)])

    python = _venv_python(venv_path)
    pip = _venv_pip(venv_path)

    # 2. Upgrade pip/setuptools to latest to avoid install issues.
    _run([str(pip), "install", "--upgrade", "pip", "setuptools", "wheel"])

    # 3. Install the generated project in editable mode with dev extras.
    _run([str(pip), "install", "-e", ".[dev]"], cwd=project_path)

    # 4. Execute the project's pytest suite to validate the stack.
    _run([str(python), "-m", "pytest"], cwd=project_path)

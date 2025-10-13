"""Regression tests for the ``agentic-canon fix`` workflow."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path


def _write_executable_script(path: Path, content: str) -> None:
    """Write ``content`` to ``path`` and mark it executable."""

    path.write_text(content)
    current_mode = path.stat().st_mode
    path.chmod(current_mode | stat.S_IEXEC)


def test_fix_command_runs_template_pipeline(tmp_path: Path) -> None:
    """The fixer should surface template pipeline activity by default."""

    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Minimal repo structure expected by ``cmd_validate``.
    for filename in [
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "LICENSE",
        ".gitignore",
    ]:
        (workspace / filename).write_text("")

    (workspace / ".git").mkdir()
    workflows_dir = workspace / ".github" / "workflows"
    workflows_dir.mkdir(parents=True)
    (workflows_dir / "ci.yml").write_text("name: CI\n")

    dev_dir = workspace / ".dev"
    dev_dir.mkdir()

    # Provide stubbed scripts that mimic the interface used by the fixer.
    _write_executable_script(
        dev_dir / "validate-templates.sh",
        """#!/usr/bin/env bash
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all|--quiet)
      shift
      ;;
    *)
      shift
      ;;
  esac
done
echo "Template validation pipeline complete"
exit 0
""",
    )

    _write_executable_script(
        dev_dir / "sanity-check.sh",
        """#!/usr/bin/env bash
echo "Sanity Check Summary"
echo "Passed: 1"
echo "Warnings: 0"
echo "Failed: 0"
exit 0
""",
    )

    env = os.environ.copy()
    repo_root = Path(__file__).resolve().parent.parent
    existing_pythonpath = env.get("PYTHONPATH", "")
    components = [str(repo_root)]
    if existing_pythonpath:
        components.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(components)
    env["AGENTIC_CANON_SANITY_MODE"] = "full"

    result = subprocess.run(
        [sys.executable, "-m", "agentic_canon_cli.cli", "fix"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Template validation pipeline" in result.stdout

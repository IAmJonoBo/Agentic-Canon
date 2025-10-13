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


def _bootstrap_workspace(tmp_path: Path) -> Path:
    """Create a minimal repository structure expected by ``cmd_fix``."""

    workspace = tmp_path / "workspace"
    workspace.mkdir()

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

    (workspace / ".dev").mkdir()
    return workspace


def _cli_environment() -> dict[str, str]:
    """Prepare environment variables so the CLI can import itself."""

    env = os.environ.copy()
    repo_root = Path(__file__).resolve().parent.parent
    existing_pythonpath = env.get("PYTHONPATH", "")
    components = [str(repo_root)]
    if existing_pythonpath:
        components.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(components)
    env["AGENTIC_CANON_SANITY_MODE"] = "full"
    return env


def test_fix_command_runs_template_pipeline(tmp_path: Path) -> None:
    """The fixer should surface template pipeline activity by default."""

    workspace = _bootstrap_workspace(tmp_path)
    dev_dir = workspace / ".dev"

    pipeline_log = workspace / "pipeline.log"
    _write_executable_script(
        dev_dir / "validate-templates.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
echo \"$@\" > "{pipeline_log}"
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

    result = subprocess.run(
        [sys.executable, "-m", "agentic_canon_cli.cli", "fix"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=120,
        env=_cli_environment(),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert pipeline_log.exists(), "Pipeline script should have recorded invocation"
    assert "--all --quiet" in pipeline_log.read_text().strip()
    assert "Template validation pipeline" in result.stdout


def test_fix_command_can_skip_template_pipeline(tmp_path: Path) -> None:
    """The fixer should tolerate skipping template checks when requested."""

    workspace = _bootstrap_workspace(tmp_path)
    dev_dir = workspace / ".dev"

    # If the pipeline ran this script the fixer would fail, ensuring the skip flag is honoured.
    _write_executable_script(
        dev_dir / "validate-templates.sh",
        """#!/usr/bin/env bash
exit 99
""",
    )

    sanity_args = workspace / "sanity-args.txt"
    _write_executable_script(
        dev_dir / "sanity-check.sh",
        f"""#!/usr/bin/env bash
set -euo pipefail
echo \"$@\" > "{sanity_args}"
echo "Sanity Check Summary"
echo "Passed: 1"
echo "Warnings: 0"
echo "Failed: 0"
exit 0
""",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "agentic_canon_cli.cli",
            "fix",
            "--skip-template-checks",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=120,
        env=_cli_environment(),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert sanity_args.exists(), "Sanity check should have run with skip flag"
    recorded_args = sanity_args.read_text().strip()
    assert recorded_args == "--quiet --skip-templates"
    assert "template checks skipped" in result.stdout

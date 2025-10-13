"""Regression tests for the template validation shell wrapper."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_executable(path: Path, content: str) -> None:
    """Persist ``content`` to ``path`` and mark it executable."""

    path.write_text(content)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def _script_environment(tmp_path: Path) -> tuple[dict[str, str], Path]:
    """Return an environment and log directory wired with stub binaries."""

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True)

    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    nox_log = log_dir / "nox.log"
    python_log = log_dir / "python.log"

    _write_executable(
        bin_dir / "nox",
        """#!/usr/bin/env bash
set -euo pipefail
log="${VALIDATE_TEMPLATES_TEST_LOG:?missing log path}"
{
        printf 'ARGS:%s\n' "$*"
        printf 'PYTHONPATH:%s\n' "${PYTHONPATH-}"
        printf '\n'
} >>"${log}"
exit 0
""",
    )

    _write_executable(
        bin_dir / "python",
        f"""#!/usr/bin/env bash
set -euo pipefail
log="${{VALIDATE_TEMPLATES_TEST_PYTHON_LOG:?missing python log}}"
printf '%s\n' "$@" >>"${{log}}"
exec "{sys.executable}" "$@"
""",
    )

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    env["VALIDATE_TEMPLATES_TEST_LOG"] = str(nox_log)
    env["VALIDATE_TEMPLATES_TEST_PYTHON_LOG"] = str(python_log)

    return env, log_dir


def test_validate_templates_all_injects_pythonpath(tmp_path: Path) -> None:
    """The wrapper should seed PYTHONPATH so hooks import reliably."""

    env, log_dir = _script_environment(tmp_path)
    script = REPO_ROOT / ".dev" / "validate-templates.sh"

    result = subprocess.run(
        [
            "bash",
            str(script),
            "--all",
            "--template",
            "python-service",
            "--skip-safe-pip",
            "--quiet",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )

    assert result.returncode == 0

    log_contents = (log_dir / "nox.log").read_text().strip().splitlines()
    args_line = next(line for line in log_contents if line.startswith("ARGS:"))
    path_line = next(line for line in log_contents if line.startswith("PYTHONPATH:"))

    assert "validate_templates_all" in args_line
    assert "--template python-service" in args_line

    pythonpath = path_line.removeprefix("PYTHONPATH:")
    assert str(REPO_ROOT) in pythonpath.split(os.pathsep)
    assert str(REPO_ROOT / "templates") in pythonpath.split(os.pathsep)


def test_skip_safe_pip_bypasses_upgrade(tmp_path: Path) -> None:
    """Passing --skip-safe-pip should avoid invoking pip hardening."""

    env, log_dir = _script_environment(tmp_path)
    script = REPO_ROOT / ".dev" / "validate-templates.sh"

    result = subprocess.run(
        [
            "bash",
            str(script),
            "--linters",
            "--skip-safe-pip",
            "--quiet",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )

    assert result.returncode == 0

    log_lines = [line for line in (log_dir / "nox.log").read_text().splitlines() if line.strip()]
    args_lines = [line for line in log_lines if line.startswith("ARGS:")]

    assert args_lines == ["ARGS:-s render_templates", "ARGS:-s lint_templates"]

    python_log = log_dir / "python.log"
    if python_log.exists():
        assert python_log.read_text() == ""

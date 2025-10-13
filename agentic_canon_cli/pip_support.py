"""Utilities to harden pip against GHSA-4xh5-x5gv-qwph."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

SAFE_PIP_SPEC = "pip @ git+https://github.com/pypa/pip@f2b92314da012b9fffa36b3f3e67748a37ef464a"
"""Patched pip build that includes the GHSA-4xh5-x5gv-qwph fix."""

SAFE_PIP_SPEC_ENV = "AGENTIC_CANON_SAFE_PIP_SPEC"
SKIP_SAFE_PIP_ENV = "AGENTIC_CANON_SKIP_SAFE_PIP"
_TRUE_VALUES = {"1", "true", "yes", "y", "on"}


class _CompletedProcess:
    """Lightweight view of subprocess output for testing."""

    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _run(cmd: Sequence[str]) -> _CompletedProcess:
    """Run a command and capture output."""

    result = subprocess.run(
        list(cmd),
        check=False,
        capture_output=True,
        text=True,
    )
    return _CompletedProcess(result.returncode, result.stdout, result.stderr)


def _should_skip_safe_pip() -> bool:
    """Return ``True`` when the skip environment variable is opt-in."""

    value = os.getenv(SKIP_SAFE_PIP_ENV)
    if value is None:
        return False
    return value.strip().lower() in _TRUE_VALUES


def _resolve_safe_pip_spec() -> str:
    """Return the pip specifier, honoring any environment override."""

    override = os.getenv(SAFE_PIP_SPEC_ENV)
    if override is None:
        return SAFE_PIP_SPEC

    override = override.strip()
    return override or SAFE_PIP_SPEC


def ensure_safe_pip(python_executable: Path | None = None, quiet: bool = False) -> tuple[bool, str]:
    """Upgrade pip to a patched build that includes the GHSA fix.

    Args:
        python_executable: Interpreter whose pip should be upgraded. Defaults to
            ``sys.executable``.
        quiet: When ``True`` suppresses detailed command output.

    Returns:
        Tuple of ``(success, detail_message)`` suitable for user-facing logs.
    """

    python_path = Path(python_executable or sys.executable)
    if not python_path.exists():
        return False, f"Python executable not found: {python_path}"

    if _should_skip_safe_pip():
        return True, f"pip upgrade skipped via {SKIP_SAFE_PIP_ENV}"

    command = [
        str(python_path),
        "-m",
        "pip",
        "install",
        "--upgrade",
        _resolve_safe_pip_spec(),
    ]
    result = _run(command)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "pip upgrade failed"
        return False, detail

    if quiet:
        return True, "pip upgraded to patched build"

    output = result.stdout.strip() or result.stderr.strip()
    if not output:
        return True, "pip upgraded to patched build"

    lines = [line for line in output.splitlines() if line.strip()]
    return True, lines[-1] if lines else "pip upgraded to patched build"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ensure pip is patched against GHSA-4xh5-x5gv-qwph",
    )
    parser.add_argument(
        "--python",
        type=Path,
        default=None,
        help="Interpreter whose pip should be upgraded (defaults to sys.executable)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the upgrade command without executing it",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational output",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint so scripts can reuse the upgrade helper."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    python_path = args.python or Path(sys.executable)
    command_preview = [
        str(python_path),
        "-m",
        "pip",
        "install",
        "--upgrade",
        _resolve_safe_pip_spec(),
    ]

    if args.dry_run:
        if not args.quiet:
            print(" ".join(command_preview))
        return 0

    success, detail = ensure_safe_pip(python_path, quiet=args.quiet)
    if not success:
        if not args.quiet:
            print(detail, file=sys.stderr)
        return 1

    if not args.quiet:
        print(detail)
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised via CLI integration tests
    raise SystemExit(main())

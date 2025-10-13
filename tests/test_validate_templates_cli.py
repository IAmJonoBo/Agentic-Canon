"""Smoke tests for the template validation wrapper."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_validate_templates_help() -> None:
    """Ensure the wrapper script is present and shows help."""
    script = Path(".dev/validate-templates.sh")
    assert script.exists(), "Validation script missing"

    result = subprocess.run(
        ["bash", str(script), "--help"],
        check=False,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    assert result.returncode == 0
    assert "Usage" in result.stdout

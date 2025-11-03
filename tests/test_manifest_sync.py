"""Ensure manifest.json mirrors manifest.yaml."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    import yaml  # type: ignore[import]
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


MANIFEST_DIR = Path(__file__).resolve().parents[1] / "templates"
YAML_PATH = MANIFEST_DIR / "manifest.yaml"
JSON_PATH = MANIFEST_DIR / "manifest.json"


@pytest.mark.skipif(yaml is None, reason="PyYAML not available")
def test_manifest_json_is_in_sync() -> None:
    """Compare YAML source to JSON mirror."""
    yaml_data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))  # type: ignore[arg-type]
    json_data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert json_data == yaml_data
"""Manifest helpers for n00-frontiers templates."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

try:  # Optional dependency; hooks must continue to work without PyYAML.
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fall back to JSON representation
    yaml = None  # type: ignore


MANIFEST_DIR = Path(__file__).resolve().parent.parent
MANIFEST_YAML = MANIFEST_DIR / "manifest.yaml"
MANIFEST_JSON = MANIFEST_DIR / "manifest.json"


def _load_from_yaml() -> Dict[str, Any]:
    if yaml is None or not MANIFEST_YAML.exists():
        raise RuntimeError("YAML manifest unavailable")
    with MANIFEST_YAML.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_from_json() -> Dict[str, Any]:
    if not MANIFEST_JSON.exists():
        raise FileNotFoundError("manifest.json is missing")
    with MANIFEST_JSON.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def load_manifest() -> Dict[str, Any]:
    """
    Load the template manifest.

    We prefer the YAML representation for readability, but fall back to the
    JSON mirror when PyYAML is unavailable (e.g., inside Cookiecutter hooks).
    """
    if MANIFEST_YAML.exists() and yaml is not None:
        return _load_from_yaml()
    return _load_from_json()


def get_template_config(template_name: str) -> Dict[str, Any]:
    manifest = load_manifest()
    templates = manifest.get("templates", {})
    config = templates.get(template_name)
    if config is None:
        raise KeyError(f"Unknown template '{template_name}' in manifest")
    return config


def list_templates() -> Dict[str, Dict[str, Any]]:
    return load_manifest().get("templates", {})

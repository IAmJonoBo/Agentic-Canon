"""Manifest helpers for n00-frontiers templates."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

try:  # Optional dependency; hooks must continue to work without PyYAML.
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fall back to JSON representation
    yaml = None  # type: ignore


MANIFEST_DIR = Path(__file__).resolve().parent.parent
MANIFEST_YAML = MANIFEST_DIR / "manifest.yaml"
MANIFEST_JSON = MANIFEST_DIR / "manifest.json"
TOOLCHAIN_ENV_VAR = "N00_TOOLCHAIN_MANIFEST_PATH"
TOOLCHAIN_DEFAULT = MANIFEST_DIR.parents[2] / "n00-cortex" / "data" / "toolchain-manifest.json"


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


def _toolchain_manifest_path() -> Optional[Path]:
    override = os.environ.get(TOOLCHAIN_ENV_VAR)
    if override:
        candidate = Path(override).expanduser()
        if candidate.exists():
            return candidate
    if TOOLCHAIN_DEFAULT.exists():
        return TOOLCHAIN_DEFAULT
    return None


@lru_cache(maxsize=None)
def load_toolchain_manifest() -> Optional[Dict[str, Any]]:
    """Load the shared toolchain manifest if it is available locally."""
    path = _toolchain_manifest_path()
    if path is None:
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None


def get_toolchain_version(tool_name: str) -> Optional[str]:
    manifest = load_toolchain_manifest()
    if not manifest:
        return None
    toolchains = manifest.get("toolchains", {})
    tool_info = toolchains.get(tool_name, {})
    if isinstance(tool_info, dict):
        value = tool_info.get("version")
        if isinstance(value, str):
            return value
    return None

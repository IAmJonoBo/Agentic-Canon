"""Pytest configuration for project-wide fixtures and plugins."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
APPLICATIONS_ROOT = REPO_ROOT / "applications" / "scaffolder"
TEMPLATES_ROOT = APPLICATIONS_ROOT / "templates"

_BAKE_CACHE: Dict[str, Any] = {}


@pytest.fixture(autouse=True)
def _patch_hook_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGENTIC_CANON_SKIP_GIT_INIT", "1")
    monkeypatch.setenv("AGENTIC_CANON_SKIP_MESSAGES", "1")


def pytest_configure(config):
    """Ensure pytest-cookies is registered exactly once."""
    if not (
        config.pluginmanager.hasplugin("pytest_cookies")
        or config.pluginmanager.hasplugin("cookies")
    ):
        plugin = importlib.import_module("pytest_cookies.plugin")
        config.pluginmanager.register(plugin, "pytest_cookies")


@pytest.fixture
def bake_template(cookies):
    """Bake templates with an in-memory cache to avoid re-rendering."""

    def _bake(template: str, extra_context: dict[str, Any]):
        candidate = Path(template)
        if not candidate.is_absolute():
            repo_candidate = REPO_ROOT / template
            if repo_candidate.exists():
                candidate = repo_candidate
            else:
                template_rel = template.split("/", 1)[1] if template.startswith("templates/") else template
                candidate = TEMPLATES_ROOT / template_rel

        if not candidate.exists():
            raise FileNotFoundError(f"Template path does not exist: {candidate}")

        cache_key = json.dumps(
            {"template": str(candidate), "context": extra_context}, sort_keys=True
        )
        cached = _BAKE_CACHE.get(cache_key)
        if cached is not None:
            return cached

        result = cookies.bake(template=str(candidate), extra_context=extra_context)
        if result.exception is None and result.exit_code == 0:
            _BAKE_CACHE[cache_key] = result
        return result

    return _bake

"""Pytest configuration for project-wide fixtures and plugins."""

from __future__ import annotations

import importlib
import json
from typing import Any, Dict

import pytest

_BAKE_CACHE: Dict[str, Any] = {}


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
        cache_key = json.dumps(
            {"template": template, "context": extra_context}, sort_keys=True
        )
        cached = _BAKE_CACHE.get(cache_key)
        if cached is not None:
            return cached

        result = cookies.bake(template=template, extra_context=extra_context)
        if result.exception is None and result.exit_code == 0:
            _BAKE_CACHE[cache_key] = result
        return result

    return _bake

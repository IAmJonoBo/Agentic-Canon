"""Pytest configuration for project-wide fixtures and plugins."""

import importlib


def pytest_configure(config):
    """Ensure pytest-cookies is registered exactly once."""
    if not (
        config.pluginmanager.hasplugin("pytest_cookies")
        or config.pluginmanager.hasplugin("cookies")
    ):
        plugin = importlib.import_module("pytest_cookies.plugin")
        config.pluginmanager.register(plugin, "pytest_cookies")

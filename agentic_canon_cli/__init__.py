"""Compatibility wrapper for the relocated scaffolder CLI package."""

from importlib import import_module as _import_module

_scaffolder = _import_module("applications.scaffolder.agentic_canon_cli")

__all__ = getattr(_scaffolder, "__all__", [])

globals().update(
    {name: value for name, value in _scaffolder.__dict__.items() if not name.startswith("_")}
)

#!/usr/bin/env python3
"""Post-generation hook for docs-only template."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType


def _load_hooks() -> ModuleType:
    template_root = Path("{{ cookiecutter._template }}").resolve()
    if template_root.exists():
        repo_root = template_root.parent.parent
        for candidate in (repo_root, template_root.parent):
            candidate_str = str(candidate)
            if candidate_str and candidate_str not in sys.path:
                sys.path.insert(0, candidate_str)

    return importlib.import_module("templates._shared.hooks")


hooks = _load_hooks()

PROJECT_ROOT = Path(".").resolve()
CONTEXT = {"ci_provider": "{{ cookiecutter.ci_provider }}"}

hooks.run_post_gen("docs-only", PROJECT_ROOT, CONTEXT)

if not hooks.should_suppress_messages():
    print("\n" + "=" * 60)
    print("✓ Documentation project created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. cd {{cookiecutter.project_slug}}")
    print("  2. pip install jupyter-book")
    print("  3. jupyter-book build docs")
    print("\nTo deploy to GitHub Pages:")
    print("  - Push to GitHub")
    print("  - GitHub Actions will build and deploy automatically")
    print("=" * 60)

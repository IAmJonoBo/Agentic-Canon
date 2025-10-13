#!/usr/bin/env python3
"""Post-generation hook for docs-only template."""
from __future__ import annotations

import sys
from pathlib import Path

TEMPLATE_ROOT = Path("{{ cookiecutter._template }}").resolve()
if TEMPLATE_ROOT.exists():
    sys.path.insert(0, str(TEMPLATE_ROOT.parent))

from _shared import hooks  # type: ignore  # pylint: disable=wrong-import-position

PROJECT_ROOT = Path(".").resolve()
CONTEXT = {
    "ci_provider": "{{ cookiecutter.ci_provider }}"
}

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

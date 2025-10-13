#!/usr/bin/env python3
"""Post-generation hook for node-service template."""

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
CONTEXT = {
    "enable_security_gates": "{{ cookiecutter.enable_security_gates }}",
    "enable_sbom_signing": "{{ cookiecutter.enable_sbom_signing }}",
    "ci_provider": "{{ cookiecutter.ci_provider }}",
}

hooks.run_post_gen("node-service", PROJECT_ROOT, CONTEXT)

if not hooks.should_suppress_messages():
    print("\n" + "=" * 60)
    print("✓ Node.js service project created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. cd {{ cookiecutter.project_slug }}")
    print("  2. npm install")
    print("  3. npm test")
    print("  4. npm run dev")
    print("\nFor CI/CD:")
    print("  - Push to GitHub to trigger workflows")
    print("  - Review .github/workflows/ for pipeline configuration")
    print("=" * 60)

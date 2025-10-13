#!/usr/bin/env python3
"""Post-generation hook for python-service template."""

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
    "include_jupyter_book": "{{ cookiecutter.include_jupyter_book }}",
    "enable_security_gates": "{{ cookiecutter.enable_security_gates }}",
    "enable_sbom_signing": "{{ cookiecutter.enable_sbom_signing }}",
    "enable_contract_tests": "{{ cookiecutter.enable_contract_tests }}",
    "ci_provider": "{{ cookiecutter.ci_provider }}",
}

hooks.run_post_gen("python-service", PROJECT_ROOT, CONTEXT)

if not hooks.should_suppress_messages():
    print("\n" + "=" * 60)
    print("✓ Python service project created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. cd {{ cookiecutter.project_slug }}")
    print("  2. python -m venv venv")
    print("  3. source venv/bin/activate")
    print("  4. pip install -e .[dev]")
    print("  5. pre-commit install")
    print("  6. git add . && git commit -m 'Initial commit'")
    print("  7. Create GitHub repo and push")
    print("=" * 60)

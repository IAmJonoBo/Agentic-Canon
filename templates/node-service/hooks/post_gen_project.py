#!/usr/bin/env python3
"""Post-generation hook for node-service template."""
from __future__ import annotations

import os
import sys
from pathlib import Path

TEMPLATE_ROOT = Path("{{ cookiecutter._template }}").resolve()
if TEMPLATE_ROOT.exists():
    sys.path.insert(0, str(TEMPLATE_ROOT.parent))

from _shared import hooks  # type: ignore  # pylint: disable=wrong-import-position

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

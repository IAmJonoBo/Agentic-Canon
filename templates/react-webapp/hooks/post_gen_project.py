#!/usr/bin/env python3
"""Post-generation hook for react-webapp template."""
from __future__ import annotations

import importlib
import json
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
    "include_storybook": "{{ cookiecutter.include_storybook }}",
    "include_e2e_tests": "{{ cookiecutter.include_e2e_tests }}",
    "enable_accessibility_tests": "{{ cookiecutter.enable_accessibility_tests }}",
    "ci_provider": "{{ cookiecutter.ci_provider }}",
}

hooks.run_post_gen("react-webapp", PROJECT_ROOT, CONTEXT)


def _update_package_json() -> None:
    package_path = PROJECT_ROOT / "package.json"
    if not package_path.exists():
        return

    data = json.loads(package_path.read_text(encoding="utf-8"))

    def pop_script(*keys: str) -> None:
        scripts = data.get("scripts", {})
        for key in keys:
            scripts.pop(key, None)

    def pop_dev_dependency(*keys: str) -> None:
        dev_deps = data.get("devDependencies", {})
        for key in keys:
            dev_deps.pop(key, None)

    if CONTEXT["include_e2e_tests"].lower() == "no":
        pop_script("test:e2e", "test:e2e:ui")
        pop_dev_dependency("@playwright/test")

    if CONTEXT["include_storybook"].lower() == "no":
        pop_script("storybook", "build-storybook")
        pop_dev_dependency(
            "@storybook/react-vite",
            "@storybook/addon-essentials",
            "@storybook/addon-a11y",
        )
    elif CONTEXT["enable_accessibility_tests"].lower() == "no":
        pop_dev_dependency("@storybook/addon-a11y")

    package_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


_update_package_json()

if not hooks.should_suppress_messages():
    print("\n" + "=" * 60)
    print("✓ React webapp project created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. cd {{ cookiecutter.project_slug }}")
    print("  2. npm install")
    print("  3. npm run dev")
    print("  4. Open http://localhost:5173")
    print("\nFor development:")
    if CONTEXT["include_storybook"].lower() == "yes":
        print("  - npm run storybook (Component development)")
    if CONTEXT["include_e2e_tests"].lower() == "yes":
        print("  - npm run test:e2e (End-to-end tests)")
    print("\nFor CI/CD:")
    print("  - Push to GitHub to trigger workflows")
    print("=" * 60)

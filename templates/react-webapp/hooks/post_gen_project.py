#!/usr/bin/env python3
"""Post-generation hook for react-webapp template."""
import os
import pathlib
import shutil
import subprocess
import sys

# Get cookiecutter variables
include_storybook = "{{ cookiecutter.include_storybook }}"
include_e2e = "{{ cookiecutter.include_e2e_tests }}"
include_a11y = "{{ cookiecutter.enable_accessibility_tests }}"

root = pathlib.Path(".")

def remove_file(*paths):
    """Remove files or directories."""
    for path in paths:
        target = root / path
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            print(f"  Removed: {path}")

# Remove optional files based on configuration
if include_storybook == "no":
    remove_file(".storybook", "src/components/Button.stories.tsx", ".github/workflows/storybook-pages.yml")

if include_e2e == "no":
    remove_file("tests/e2e", "playwright.config.ts")

if include_a11y == "no":
    remove_file(".github/workflows/accessibility.yml")

# Initialize git repository
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    print("✓ Initialized git repository")
except Exception as e:
    print(f"⚠ Could not initialize git: {e}")

print("\n" + "="*60)
print("✓ React webapp project created successfully!")
print("="*60)
print("\nNext steps:")
print("  1. cd {{cookiecutter.project_slug}}")
print("  2. npm install")
print("  3. npm run dev")
print("  4. Open http://localhost:5173")
print("\nFor development:")
if include_storybook == "yes":
    print("  - npm run storybook (Component development)")
if include_e2e == "yes":
    print("  - npm run test:e2e (End-to-end tests)")
print("\nFor CI/CD:")
print("  - Push to GitHub to trigger workflows")
print("="*60)

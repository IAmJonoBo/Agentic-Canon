#!/usr/bin/env python3
"""Post-generation hook for docs-only template."""
import pathlib
import subprocess

root = pathlib.Path(".")

# Initialize git repository
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    print("✓ Initialized git repository")
except Exception as e:
    print(f"⚠ Could not initialize git: {e}")

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

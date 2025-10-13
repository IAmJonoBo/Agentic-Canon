#!/usr/bin/env python3
"""Post-generation hook for go-service template."""
import pathlib
import shutil
import subprocess

enable_security = "{{ cookiecutter.enable_security_gates }}"
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


# Remove optional files
if enable_security == "no":
    remove_file(".github/workflows/security.yml")

# Initialize git and Go module
try:
    subprocess.run(["git", "init", "-q"], check=False, cwd=root)
    subprocess.run(["go", "mod", "tidy"], check=False, cwd=root)
    print("✓ Initialized git repository and Go module")
except Exception as e:
    print(f"⚠ Could not initialize: {e}")

print("\n" + "=" * 60)
print("✓ Go service project created successfully!")
print("=" * 60)
print("\nNext steps:")
print("  1. cd {{cookiecutter.project_slug}}")
print("  2. make test")
print("  3. make run")
print("\nFor development:")
print("  - make build  # Compile the service")
print("  - make lint   # Run linters")
print("  - make test   # Run tests")
print("=" * 60)

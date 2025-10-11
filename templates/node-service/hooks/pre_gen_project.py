#!/usr/bin/env python3
"""Pre-generation hook for node-service template."""
import re
import sys

project_slug = "{{ cookiecutter.project_slug }}"

# Validate project slug (kebab-case)
if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", project_slug):
    print(f"ERROR: project_slug '{project_slug}' must be kebab-case (lowercase with hyphens)")
    print("Example: my-node-service")
    sys.exit(1)

print(f"✓ Project slug '{project_slug}' is valid")

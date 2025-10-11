#!/usr/bin/env python3
"""Pre-generation hook for go-service template."""
import re
import sys

project_slug = "{{ cookiecutter.project_slug }}"
module_path = "{{ cookiecutter.module_path }}"

# Validate project slug (kebab-case)
if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", project_slug):
    print(f"ERROR: project_slug '{project_slug}' must be kebab-case")
    sys.exit(1)

# Validate module path
if not re.match(r"^[a-z0-9]+(?:[./][a-z0-9-]+)+$", module_path, re.IGNORECASE):
    print(f"ERROR: module_path '{module_path}' is not a valid Go module path")
    print("Example: github.com/username/project-name")
    sys.exit(1)

print(f"✓ Project slug '{project_slug}' is valid")
print(f"✓ Module path '{module_path}' is valid")

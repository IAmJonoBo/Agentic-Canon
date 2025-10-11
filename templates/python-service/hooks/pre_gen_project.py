import re
import sys

slug = "{{ cookiecutter.project_slug }}"
pkg  = "{{ cookiecutter.pkg_name }}"

if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
    sys.exit("ERROR: project_slug must be kebab-case: [a-z0-9-].")

if not re.match(r"^[a-z_][a-z0-9_]*$", pkg):
    sys.exit("ERROR: pkg_name must be a valid Python identifier (snake_case).")

print(f"✓ Validated project_slug: {slug}")
print(f"✓ Validated pkg_name: {pkg}")

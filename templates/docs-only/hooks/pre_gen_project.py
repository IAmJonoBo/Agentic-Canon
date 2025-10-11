import re
import sys

slug = "{{ cookiecutter.project_slug }}"

if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
    sys.exit("ERROR: project_slug must be kebab-case: [a-z0-9-].")

print(f"✓ Project slug '{slug}' is valid")

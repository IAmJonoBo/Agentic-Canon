#!/usr/bin/env python3
"""Pre-generation validation for docs-only template.

Validates all user inputs before generating the project to ensure
consistency, security, and standards compliance.
"""
import re
import sys

# Approved licenses (including Creative Commons for docs)
APPROVED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "GPL-3.0", "LGPL-3.0", "MPL-2.0", "ISC", "Unlicense", "CC-BY-4.0"}

def validate_project_slug(slug):
    if not slug or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
        print(f"ERROR: project_slug must be kebab-case: [a-z0-9-]")
        print("Examples: my-docs, api-documentation, user-guide")
        sys.exit(1)
    print(f"✓ Validated project_slug: {slug}")

def validate_email(email, field_name="email"):
    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        print(f"ERROR: {field_name} must be a valid email address")
        sys.exit(1)
    print(f"✓ Validated {field_name}: {email}")

def validate_author_name(name):
    if not name or not name.strip() or len(name.strip()) < 2 or not re.search(r'[a-zA-Z]', name):
        print(f"ERROR: author_name must be a valid name (at least 2 characters with letters)")
        sys.exit(1)
    print(f"✓ Validated author_name: {name}")

def validate_license(license_id):
    if license_id not in APPROVED_LICENSES:
        print(f"ERROR: {license_id} is not an approved license")
        print(f"  Approved: {', '.join(sorted(APPROVED_LICENSES))}")
        sys.exit(1)
    print(f"✓ Validated license: {license_id}")

def validate_description(description, field_name="description"):
    if not description or len(description.strip()) < 10:
        print(f"ERROR: {field_name} must be at least 10 characters")
        sys.exit(1)
    print(f"✓ Validated {field_name}: {description[:50]}...")

# Extract and validate
project_slug = "{{ cookiecutter.project_slug }}"
author_name = "{{ cookiecutter.author_name }}"
author_email = "{{ cookiecutter.author_email }}"
license_id = "{{ cookiecutter.license }}"
description = "{{ cookiecutter.description }}"

validate_project_slug(project_slug)
validate_author_name(author_name)
validate_email(author_email, "author_email")
validate_license(license_id)
validate_description(description)

print("\n" + "="*60)
print("✅ All validations passed!")
print("="*60 + "\n")

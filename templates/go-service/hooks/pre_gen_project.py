#!/usr/bin/env python3
"""Pre-generation validation for go-service template.

Validates all user inputs before generating the project to ensure
consistency, security, and standards compliance.
"""

import re
import sys

# Approved licenses
APPROVED_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "GPL-3.0",
    "LGPL-3.0",
    "MPL-2.0",
    "ISC",
    "Unlicense",
}


def validate_project_slug(slug):
    if not slug or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
        print("ERROR: project_slug must be kebab-case")
        print("Examples: my-go-service, grpc-api, microservice")
        sys.exit(1)
    print(f"✓ Validated project_slug: {slug}")


def validate_go_module_path(module_path):
    if not module_path or not re.match(
        r"^[a-zA-Z0-9.-]+(?:[./][a-zA-Z0-9._-]+)+$",
        module_path,
    ):
        print("ERROR: module_path is not a valid Go module path")
        print("Format: domain.com/path/to/module")
        print("Examples: github.com/user/project, example.com/my/module")
        sys.exit(1)
    parts = re.split(r"[./]", module_path)
    if len(parts) < 2:
        print("ERROR: module_path must have at least domain and path")
        sys.exit(1)
    print(f"✓ Validated module_path: {module_path}")


def validate_email(email, field_name="email"):
    if not email or not re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        email,
    ):
        print(f"ERROR: {field_name} must be a valid email address")
        sys.exit(1)
    print(f"✓ Validated {field_name}: {email}")


def validate_author_name(name):
    if (
        not name
        or not name.strip()
        or len(name.strip()) < 2
        or not re.search(r"[a-zA-Z]", name)
    ):
        print(
            "ERROR: author_name must be a valid name "
            "(at least 2 characters with letters)"
        )
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
module_path = "{{ cookiecutter.module_path }}"
author_name = "{{ cookiecutter.author_name }}"
author_email = "{{ cookiecutter.author_email }}"
license_id = "{{ cookiecutter.license }}"
description = "{{ cookiecutter.description }}"

validate_project_slug(project_slug)
validate_go_module_path(module_path)
validate_author_name(author_name)
validate_email(author_email, "author_email")
validate_license(license_id)
validate_description(description)

print("\n" + "=" * 60)
print("✅ All validations passed!")
print("=" * 60 + "\n")

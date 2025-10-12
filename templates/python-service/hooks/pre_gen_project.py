#!/usr/bin/env python3
"""Pre-generation validation for python-service template.

Validates all user inputs before generating the project to ensure
consistency, security, and standards compliance.
"""
import re
import sys
import os

# Try to import shared validation, fallback to inline if not available
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
    from validation import (
        validate_project_slug,
        validate_python_package_name,
        validate_email,
        validate_author_name,
        validate_license,
        validate_description,
        APPROVED_LICENSES
    )
    using_shared = True
except (ImportError, FileNotFoundError):
    # Fallback to inline validation
    using_shared = False
    APPROVED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "GPL-3.0", "LGPL-3.0", "MPL-2.0", "ISC", "Unlicense"}
    
    def validate_project_slug(slug, field_name="project_slug"):
        if not slug or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
            print(f"ERROR: {field_name} must be kebab-case: [a-z0-9-]")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {slug}")
        return True
    
    def validate_python_package_name(name, field_name="pkg_name"):
        reserved = {"and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", 
                   "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "not", "or", "pass",
                   "raise", "return", "try", "while", "with", "yield", "True", "False", "None"}
        if not name or not re.match(r"^[a-z_][a-z0-9_]*$", name) or name in reserved:
            print(f"ERROR: {field_name} must be a valid Python identifier (snake_case)")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {name}")
        return True
    
    def validate_email(email, field_name="email"):
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print(f"ERROR: {field_name} must be a valid email address")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {email}")
        return True
    
    def validate_author_name(name, field_name="author_name"):
        if not name or not name.strip() or len(name.strip()) < 2 or not re.search(r'[a-zA-Z]', name):
            print(f"ERROR: {field_name} must be a valid name (at least 2 characters with letters)")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {name}")
        return True
    
    def validate_license(license_id, field_name="license"):
        if license_id not in APPROVED_LICENSES:
            print(f"ERROR: {license_id} is not an approved license")
            print(f"  Approved: {', '.join(sorted(APPROVED_LICENSES))}")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {license_id}")
        return True
    
    def validate_description(description, field_name="description", min_length=10, max_length=500):
        if not description or len(description.strip()) < min_length:
            print(f"ERROR: {field_name} must be at least {min_length} characters")
            sys.exit(1)
        print(f"✓ Validated {field_name}: {description[:50]}...")
        return True

# Extract cookiecutter variables
project_slug = "{{ cookiecutter.project_slug }}"
pkg_name = "{{ cookiecutter.pkg_name }}"
author_name = "{{ cookiecutter.author_name }}"
author_email = "{{ cookiecutter.author_email }}"
license_id = "{{ cookiecutter.license }}"
description = "{{ cookiecutter.project_description }}"

# Run all validations
validate_project_slug(project_slug)
validate_python_package_name(pkg_name)
validate_author_name(author_name)
validate_email(author_email, "author_email")
validate_license(license_id)
validate_description(description, "project_description")

print("\n" + "="*60)
print("✅ All validations passed!")
print("="*60 + "\n")

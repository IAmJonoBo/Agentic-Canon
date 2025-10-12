#!/usr/bin/env python3
"""Shared validation utilities for Cookiecutter templates.

This module provides common validation functions used across all templates
to ensure consistent input validation and error messaging.

Standards Compliance:
- NIST SSDF: PO.3 (Security requirements)
- OWASP SAMM: Security by default
- ISO/IEC 25010: Quality characteristics
"""
import re
import sys
from typing import List, Optional


# Approved open source licenses (SPDX identifiers)
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


def validate_project_slug(slug: str, field_name: str = "project_slug") -> bool:
    """Validate project slug is in kebab-case format.
    
    Args:
        slug: The project slug to validate
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
        
    Examples:
        Valid: my-project, service-123, api-v2
        Invalid: MyProject, my_project, -project, project-
    """
    if not slug:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
        print(f"ERROR: {field_name} '{slug}' must be in kebab-case format")
        print("  Requirements:")
        print("    - Must start with a lowercase letter or digit")
        print("    - Can contain lowercase letters, digits, and hyphens")
        print("    - Cannot start or end with a hyphen")
        print("    - Cannot have consecutive hyphens")
        print("  Examples: my-project, api-service, web-app-v2")
        sys.exit(1)
        
    if len(slug) > 64:
        print(f"ERROR: {field_name} '{slug}' is too long (max 64 characters)")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {slug}")
    return True


def validate_python_package_name(name: str, field_name: str = "pkg_name") -> bool:
    """Validate Python package name is a valid identifier.
    
    Args:
        name: The package name to validate
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
        
    Examples:
        Valid: my_package, service_api, webapp
        Invalid: my-package, 123package, package-name
    """
    if not name:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    if not re.match(r"^[a-z_][a-z0-9_]*$", name):
        print(f"ERROR: {field_name} '{name}' must be a valid Python identifier")
        print("  Requirements:")
        print("    - Must start with a lowercase letter or underscore")
        print("    - Can contain lowercase letters, digits, and underscores")
        print("    - Must use snake_case format")
        print("  Examples: my_package, api_service, web_app")
        sys.exit(1)
        
    # Check for Python reserved keywords
    reserved = {
        "and", "as", "assert", "break", "class", "continue", "def", "del",
        "elif", "else", "except", "finally", "for", "from", "global", "if",
        "import", "in", "is", "lambda", "not", "or", "pass", "raise",
        "return", "try", "while", "with", "yield", "True", "False", "None"
    }
    if name in reserved:
        print(f"ERROR: {field_name} '{name}' is a Python reserved keyword")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {name}")
    return True


def validate_email(email: str, field_name: str = "email") -> bool:
    """Validate email address format.
    
    Args:
        email: The email address to validate
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
    """
    if not email:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    # RFC 5322 simplified pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print(f"ERROR: {field_name} '{email}' is not a valid email address")
        print("  Examples: user@example.com, dev.team@company.io")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {email}")
    return True


def validate_author_name(name: str, field_name: str = "author_name") -> bool:
    """Validate author name is not empty and has reasonable format.
    
    Args:
        name: The author name to validate
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
    """
    if not name or not name.strip():
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    # Check for minimum length
    if len(name.strip()) < 2:
        print(f"ERROR: {field_name} '{name}' is too short (minimum 2 characters)")
        sys.exit(1)
        
    # Check for maximum length
    if len(name) > 100:
        print(f"ERROR: {field_name} '{name}' is too long (max 100 characters)")
        sys.exit(1)
        
    # Check for suspicious patterns (all special characters, etc.)
    if not re.search(r'[a-zA-Z]', name):
        print(f"ERROR: {field_name} '{name}' must contain at least one letter")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {name}")
    return True


def validate_license(license_id: str, field_name: str = "license") -> bool:
    """Validate license is an approved open source license.
    
    Args:
        license_id: The license identifier (SPDX format)
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
    """
    if not license_id:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    if license_id not in APPROVED_LICENSES:
        print(f"ERROR: {license_id} is not an approved license")
        print(f"  Approved licenses: {', '.join(sorted(APPROVED_LICENSES))}")
        print("  See: https://spdx.org/licenses/")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {license_id}")
    return True


def validate_version(version: str, field_name: str = "version") -> bool:
    """Validate semantic version format.
    
    Args:
        version: The version string to validate (e.g., "1.0.0")
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
    """
    if not version:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    # Semantic versioning pattern (simplified)
    pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?$'
    if not re.match(pattern, version):
        print(f"ERROR: {field_name} '{version}' is not a valid semantic version")
        print("  Format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]")
        print("  Examples: 1.0.0, 2.1.3, 1.0.0-beta.1, 1.0.0+20130313")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {version}")
    return True


def validate_go_module_path(module_path: str, field_name: str = "module_path") -> bool:
    """Validate Go module path format.
    
    Args:
        module_path: The Go module path to validate
        field_name: The name of the field (for error messages)
        
    Returns:
        True if valid, exits with error if invalid
        
    Examples:
        Valid: github.com/user/project, example.com/my/module
        Invalid: github.com, not-a-url
    """
    if not module_path:
        print(f"ERROR: {field_name} cannot be empty")
        sys.exit(1)
        
    # Go module path should have at least domain/path
    pattern = r'^[a-zA-Z0-9.-]+(?:[./][a-zA-Z0-9._-]+)+$'
    if not re.match(pattern, module_path):
        print(f"ERROR: {field_name} '{module_path}' is not a valid Go module path")
        print("  Format: domain.com/path/to/module")
        print("  Examples: github.com/user/project, example.com/my/module")
        sys.exit(1)
        
    # Check for minimum components (at least 2 parts)
    parts = re.split(r'[./]', module_path)
    if len(parts) < 2:
        print(f"ERROR: {field_name} '{module_path}' must have at least domain and path")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {module_path}")
    return True


def validate_description(description: str, field_name: str = "description", 
                        min_length: int = 10, max_length: int = 500) -> bool:
    """Validate project description has reasonable content.
    
    Args:
        description: The description to validate
        field_name: The name of the field (for error messages)
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        True if valid, exits with error if invalid
    """
    if not description or not description.strip():
        print(f"ERROR: {field_name} cannot be empty")
        print(f"  Please provide a brief description (at least {min_length} characters)")
        sys.exit(1)
        
    desc_length = len(description.strip())
    
    if desc_length < min_length:
        print(f"ERROR: {field_name} is too short ({desc_length} chars, minimum {min_length})")
        print("  Please provide a more detailed description")
        sys.exit(1)
        
    if desc_length > max_length:
        print(f"ERROR: {field_name} is too long ({desc_length} chars, maximum {max_length})")
        print("  Please provide a more concise description")
        sys.exit(1)
        
    print(f"✓ Validated {field_name}: {description[:50]}{'...' if len(description) > 50 else ''}")
    return True


def print_validation_summary(validations: List[str]) -> None:
    """Print a summary of completed validations.
    
    Args:
        validations: List of validation descriptions
    """
    print("\n" + "="*60)
    print("✅ All validations passed!")
    print("="*60)
    for validation in validations:
        print(f"  ✓ {validation}")
    print("="*60 + "\n")


def main():
    """Run self-tests for validation functions."""
    print("Running validation module self-tests...\n")
    
    # These should pass
    try:
        validate_project_slug("my-project")
        validate_python_package_name("my_package")
        validate_email("user@example.com")
        validate_author_name("John Doe")
        validate_license("MIT")
        validate_version("1.0.0")
        validate_go_module_path("github.com/user/project")
        validate_description("This is a test description for validation")
        print("\n✅ All self-tests passed!")
    except SystemExit:
        print("\n❌ Self-tests failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Template Validation Guide

This guide documents all input validation rules and requirements for Agentic Canon Cookiecutter templates.

## Overview

All templates implement comprehensive input validation to ensure:

- **Security**: Prevent injection attacks and invalid inputs
- **Consistency**: Uniform naming and structure across projects
- **Standards Compliance**: Follow industry best practices
- **User Experience**: Clear, actionable error messages

## Validation Rules

### Project Slug

**Field**: `project_slug`  
**Format**: kebab-case  
**Pattern**: `^[a-z0-9]+(?:-[a-z0-9]+)*$`

**Requirements**:

- Must start with a lowercase letter or digit
- Can contain lowercase letters, digits, and hyphens
- Cannot start or end with a hyphen
- Cannot have consecutive hyphens
- Maximum 64 characters

**Valid Examples**:

```
my-project
api-service-v2
web-app
microservice-123
```

**Invalid Examples**:

```
MyProject         # Uppercase not allowed
my_project        # Underscores not allowed
-project          # Cannot start with hyphen
project-          # Cannot end with hyphen
my--project       # Consecutive hyphens not allowed
```

**Error Message**:

```
ERROR: project_slug must be in kebab-case format
  Requirements:
    - Must start with a lowercase letter or digit
    - Can contain lowercase letters, digits, and hyphens
    - Cannot start or end with a hyphen
    - Cannot have consecutive hyphens
  Examples: my-project, api-service, web-app-v2
```

---

### Python Package Name

**Field**: `pkg_name` (Python templates only)  
**Format**: snake*case  
**Pattern**: `^[a-z*][a-z0-9_]\*$`

**Requirements**:

- Must start with a lowercase letter or underscore
- Can contain lowercase letters, digits, and underscores
- Must be a valid Python identifier
- Cannot be a Python reserved keyword

**Python Reserved Keywords**:

```python
and, as, assert, break, class, continue, def, del, elif, else, except,
finally, for, from, global, if, import, in, is, lambda, not, or, pass,
raise, return, try, while, with, yield, True, False, None
```

**Valid Examples**:

```
my_package
api_service
webapp
service_v2
```

**Invalid Examples**:

```
my-package        # Hyphens not allowed
123package        # Cannot start with digit
import            # Reserved keyword
```

---

### Go Module Path

**Field**: `module_path` (Go templates only)  
**Format**: domain.com/path/to/module  
**Pattern**: `^[a-zA-Z0-9.-]+(?:[./][a-zA-Z0-9._-]+)+$`

**Requirements**:

- Must have at least a domain and path component
- Uses periods or slashes as separators
- Follows Go module path conventions

**Valid Examples**:

```
github.com/user/project
example.com/my/module
gitlab.com/org/team/service
```

**Invalid Examples**:

```
github.com              # Missing path component
not-a-url               # Missing domain
my-local-project        # Not a valid module path
```

---

### Email Address

**Field**: `author_email`  
**Format**: RFC 5322 (simplified)  
**Pattern**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

**Requirements**:

- Must be a valid email address format
- Contains @ symbol
- Has domain with TLD

**Valid Examples**:

```
user@example.com
dev.team@company.io
john.doe+tag@enterprise.org
```

**Invalid Examples**:

```
not-an-email            # Missing @
user@                   # Missing domain
@example.com            # Missing local part
user@invalid            # Missing TLD
```

---

### Author Name

**Field**: `author_name`  
**Requirements**:

- Cannot be empty
- Minimum 2 characters
- Maximum 100 characters
- Must contain at least one letter

**Valid Examples**:

```
John Doe
Jane Smith
李明
Development Team
Dr. Sarah Johnson
```

**Invalid Examples**:

```
X                       # Too short (1 character)
123                     # No letters
(empty string)          # Cannot be empty
```

---

### License

**Field**: `license`  
**Format**: SPDX identifier  
**Whitelist**: Approved open source licenses

**Approved Licenses**:

- `MIT` - MIT License
- `Apache-2.0` - Apache License 2.0
- `BSD-3-Clause` - BSD 3-Clause License
- `BSD-2-Clause` - BSD 2-Clause License
- `GPL-3.0` - GNU General Public License v3.0
- `LGPL-3.0` - GNU Lesser General Public License v3.0
- `MPL-2.0` - Mozilla Public License 2.0
- `ISC` - ISC License
- `Unlicense` - The Unlicense
- `CC-BY-4.0` - Creative Commons Attribution 4.0 (docs-only)

**Valid Examples**:

```
MIT
Apache-2.0
BSD-3-Clause
```

**Invalid Examples**:

```
MIT License             # Use SPDX identifier, not full name
Apache 2.0              # Incorrect format
Proprietary             # Not in approved list
```

**Reference**: https://spdx.org/licenses/

---

### Description

**Field**: `description` or `project_description`  
**Requirements**:

- Cannot be empty
- Minimum 10 characters
- Maximum 500 characters
- Should be meaningful and descriptive

**Valid Examples**:

```
A modern REST API service for user management
React dashboard for monitoring system metrics
Documentation for the Acme project API
```

**Invalid Examples**:

```
Test                    # Too short (less than 10 characters)
A                       # Way too short
(500+ characters)       # Exceeds maximum length
```

---

### Semantic Version

**Field**: `version` (where applicable)  
**Format**: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]  
**Pattern**: `^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?$`

**Valid Examples**:

```
1.0.0
2.1.3
1.0.0-beta.1
1.0.0+20130313
3.0.0-rc.1+build.123
```

**Invalid Examples**:

```
1.0                     # Missing patch version
v1.0.0                  # Should not include 'v' prefix
1.0.0-SNAPSHOT          # Use lowercase for prerelease
```

**Reference**: https://semver.org/

---

## Error Messages

All validation errors include:

1. **Clear error description** - What went wrong
2. **Requirements** - What the input should be
3. **Examples** - Valid formats to follow

### Example Error Output

```
ERROR: project_slug 'My_Project' must be in kebab-case format
  Requirements:
    - Must start with a lowercase letter or digit
    - Can contain lowercase letters, digits, and hyphens
    - Cannot start or end with a hyphen
    - Cannot have consecutive hyphens
  Examples: my-project, api-service, web-app-v2
```

## Implementation

### Validation Hooks

Each template has a `hooks/pre_gen_project.py` file that validates inputs before generation.

**Example**:

```python
#!/usr/bin/env python3
"""Pre-generation validation for template."""
import re
import sys

# Approved licenses
APPROVED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", ...}

def validate_project_slug(slug):
    if not slug or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
        print(f"ERROR: project_slug must be kebab-case")
        print("Examples: my-project, api-service")
        sys.exit(1)
    print(f"✓ Validated project_slug: {slug}")

# Extract and validate
project_slug = "{{ cookiecutter.project_slug }}"
validate_project_slug(project_slug)
```

### Shared Validation Module

The `templates/_shared/validation.py` module provides reusable validation functions:

```python
from validation import validate_project_slug, validate_email, validate_license

validate_project_slug("my-project")
validate_email("user@example.com")
validate_license("MIT")
```

See `templates/_shared/README.md` for full documentation.

## Testing

Validation is tested comprehensively in `tests/test_cookiecutters.py`:

```python
def test_python_invalid_email(cookies):
    """Test that invalid email is rejected."""
    result = cookies.bake(
        extra_context={"author_email": "not-an-email"},
        template="templates/python-service"
    )
    assert result.exit_code != 0  # Should fail
```

**Test Coverage**:

- Valid inputs for all fields
- Invalid formats (wrong patterns)
- Edge cases (empty strings, too short/long)
- Special cases (reserved keywords, etc.)

Run tests:

```bash
pytest tests/test_cookiecutters.py -v
```

## Standards Compliance

Validation supports multiple compliance frameworks:

### NIST SSDF v1.1

- **PO.3**: Security requirements defined at project creation
- Input validation prevents common security issues

### OWASP SAMM

- **Security by default**: Validated inputs reduce attack surface
- Consistent naming prevents injection attacks

### ISO/IEC 25010

- **Functional Suitability**: Inputs meet quality requirements
- **Reliability**: Validation prevents configuration errors

### SLSA Level 3

- **Build Integrity**: Validated inputs ensure reproducible builds
- **Provenance**: Consistent metadata for attestation

## Troubleshooting

### Common Issues

#### "ERROR: project_slug must be kebab-case"

**Problem**: Using incorrect characters or format  
**Solution**: Use lowercase letters, digits, and hyphens only

#### "ERROR: pkg_name is a Python reserved keyword"

**Problem**: Package name conflicts with Python keywords  
**Solution**: Choose a different name (e.g., `my_import` instead of `import`)

#### "ERROR: license is not an approved license"

**Problem**: Using a non-standard or proprietary license  
**Solution**: Choose from approved SPDX licenses (MIT, Apache-2.0, etc.)

#### "ERROR: description must be at least 10 characters"

**Problem**: Description is too short  
**Solution**: Provide a meaningful description (at least 10 characters)

#### "ERROR: author_email must be a valid email address"

**Problem**: Email format is incorrect  
**Solution**: Use format: name@domain.tld

### Validation Bypass (Not Recommended)

To skip validation for testing:

```bash
# Temporarily rename the hook
mv templates/python-service/hooks/pre_gen_project.py \
   templates/python-service/hooks/pre_gen_project.py.bak

# Generate project (no validation)
cookiecutter templates/python-service

# Restore hook
mv templates/python-service/hooks/pre_gen_project.py.bak \
   templates/python-service/hooks/pre_gen_project.py
```

**⚠️ Warning**: Bypassing validation may create invalid projects that fail CI/CD pipelines.

## Contributing

When adding new validation rules:

1. **Update validation functions** in `templates/_shared/validation.py`
2. **Update all template hooks** to use new validation
3. **Add tests** in `tests/test_cookiecutters.py`
4. **Document** validation rules in this guide
5. **Update examples** with valid/invalid cases

## References

- [SPDX License List](https://spdx.org/licenses/)
- [Semantic Versioning](https://semver.org/)
- [RFC 5322](https://tools.ietf.org/html/rfc5322) - Email format
- [PEP 8](https://pep8.org/) - Python naming conventions
- [Go Module Path](https://go.dev/ref/mod#module-path)

---

**Last Updated**: 2025-10-12  
**Version**: 1.0  
**Maintained By**: Agentic Canon Team

# Shared Template Utilities

This directory contains shared utilities used across all Cookiecutter templates in the n00-frontiers framework.

## Files

### `validation.py`

Common validation functions for template input validation. Provides consistent error messaging and input validation across all templates.

**Usage in pre_gen_project.py hooks:**

```python
import sys
import os

# Add shared utilities to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_shared'))
from validation import validate_project_slug, validate_email, validate_license

# Validate inputs
project_slug = "{{ cookiecutter.project_slug }}"
author_email = "{{ cookiecutter.author_email }}"
license_id = "{{ cookiecutter.license }}"

validate_project_slug(project_slug)
validate_email(author_email, "author_email")
validate_license(license_id)
```

**Available validation functions:**

- `validate_project_slug(slug)` - Validate kebab-case project names
- `validate_python_package_name(name)` - Validate Python package identifiers
- `validate_email(email)` - Validate email addresses (RFC 5322)
- `validate_author_name(name)` - Validate author names
- `validate_license(license_id)` - Validate against approved licenses
- `validate_version(version)` - Validate semantic versioning
- `validate_go_module_path(module_path)` - Validate Go module paths
- `validate_description(description)` - Validate project descriptions
- `print_validation_summary(validations)` - Print validation summary

**Approved Licenses:**

- MIT
- Apache-2.0
- BSD-3-Clause
- BSD-2-Clause
- GPL-3.0
- LGPL-3.0
- MPL-2.0
- ISC
- Unlicense

## Standards Compliance

All validation functions support:

- **NIST SSDF v1.1**: PO.3 (Security requirements defined)
- **OWASP SAMM**: Security by default practices
- **ISO/IEC 25010**: Software quality characteristics
- **SLSA Level 3**: Build integrity and provenance

## Testing

Run self-tests:

```bash
python templates/_shared/validation.py
```

All functions include comprehensive error messages with examples to guide users.

## Design Principles

1. **Fail Fast**: Invalid inputs cause immediate, clear errors
2. **Helpful Messages**: Every error includes examples and requirements
3. **Consistency**: Same validation rules across all templates
4. **Security**: Prevent injection attacks and invalid characters
5. **Standards**: Follow industry best practices (SPDX, RFC, semver)

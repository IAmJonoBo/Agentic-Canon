{% if cookiecutter.include_jupyter_book == "yes" -%}

# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Overview

This documentation is built with Jupyter Book and includes executable notebooks demonstrating how to use {{ cookiecutter.pkg_name }}.

## Quick Start

```python
import {{ cookiecutter.pkg_name }}

# Get started with {{ cookiecutter.project_name }}
result = {{ cookiecutter.pkg_name }}.hello()
print(result)
```

## Features

- Clean, tested codebase
- Type-safe with mypy
- Formatted with black
- Linted with ruff
- Comprehensive test coverage
  {% if cookiecutter.enable_security_gates == "yes" %}
- Security scanning with CodeQL
  {% endif %}
  {% if cookiecutter.enable_sbom_signing == "yes" %}
- SBOM generation
  {% endif %}

## Notebooks

See the notebooks section for interactive examples and tutorials.
{% endif -%}

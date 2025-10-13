# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- 🚀 Modern Python {{ cookiecutter.python_version }}+ with type hints
- 📦 Managed with setuptools and pyproject.toml
- ✅ Testing with pytest and coverage
- 🔍 Code quality with black, ruff, and mypy
- 🔒 Pre-commit hooks for consistent code style
  {% if cookiecutter.enable_security_gates == "yes" -%}
- 🛡️ Security scanning with CodeQL and Gitleaks
  {% endif -%}
  {% if cookiecutter.enable_sbom_signing == "yes" -%}
- 📋 SBOM generation with CycloneDX
- ✍️ Artifact signing with Sigstore/Cosign
  {% endif -%}
  {% if cookiecutter.include_jupyter_book == "yes" -%}
- 📚 Documentation with Jupyter Book
  {% endif -%}

## Quick Start

### Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Usage

```python
import {{ cookiecutter.pkg_name }}

print({{ cookiecutter.pkg_name }}.hello())
```

### Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov

# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

{% if cookiecutter.include_jupyter_book == "yes" -%}

### Documentation

Build the documentation:

```bash
jupyter-book build docs
```

View locally: Open `docs/_build/html/index.html` in your browser.
{% endif -%}

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   └── {{ cookiecutter.pkg_name }}/
│       └── __init__.py
├── tests/
│   └── test_smoke.py
├── .github/
│   └── workflows/
│       └── ci.yml
{% if cookiecutter.include_jupyter_book == "yes" -%}
├── docs/
│   ├── _config.yml
│   ├── _toc.yml
│   └── intro.md
├── notebooks/
│   └── 01_bootstrap.ipynb
{% endif -%}
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## License

{{ cookiecutter.license }}

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:

- Tests pass (`pytest`)
- Code is formatted (`black`, `ruff`)
- Type checks pass (`mypy`)
- Pre-commit hooks pass

## Authors

- {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

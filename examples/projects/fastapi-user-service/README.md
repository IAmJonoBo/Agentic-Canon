# FastAPI User Service

A Python service with best practices

## Features

- 🚀 Modern Python 3.11+ with type hints
- 📦 Managed with setuptools and pyproject.toml
- ✅ Testing with pytest and coverage
- 🔍 Code quality with black, ruff, and mypy
- 🔒 Pre-commit hooks for consistent code style
- 🛡️ Security scanning with CodeQL and Gitleaks
- 📋 SBOM generation with CycloneDX
- ✍️ Artifact signing with Sigstore/Cosign
- 📚 Documentation with Jupyter Book
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
import acme_service

print(acme_service.hello())
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

### Documentation

Build the documentation:

```bash
jupyter-book build docs
```

View locally: Open `docs/_build/html/index.html` in your browser.
## Project Structure

```
fastapi-user-service/
├── src/
│   └── acme_service/
│       └── __init__.py
├── tests/
│   └── test_smoke.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── _config.yml
│   ├── _toc.yml
│   └── intro.md
├── notebooks/
│   └── 01_bootstrap.ipynb
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## License

MIT

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

- Agentic Canon Team <team@agenticcanon.dev>

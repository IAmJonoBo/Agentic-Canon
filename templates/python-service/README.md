# Python Service Cookiecutter Template

Production-ready Python service template with comprehensive CI/CD, security, and quality tooling.

## Quick Start

```bash
# Using Cookiecutter
cookiecutter templates/python-service

# Or using Agentic Canon CLI
agentic-canon init
# Select "Python Service" when prompted
```

## Features

### Core Capabilities

- ✅ **Modern Python** - Python 3.11+ with type hints
- ✅ **Project Structure** - `src/` layout following best practices
- ✅ **Dependency Management** - `pyproject.toml` with modern packaging
- ✅ **Testing** - pytest with coverage ≥80% target
- ✅ **Type Checking** - mypy for static type analysis
- ✅ **Linting** - Ruff for fast, comprehensive linting
- ✅ **Formatting** - Black for consistent code style
- ✅ **Pre-commit Hooks** - Automated quality checks

### CI/CD

- ✅ **GitHub Actions** workflows for linting, testing, documentation, and security scanning
- ✅ **Multi-version Testing** - Python 3.11, 3.12
- ✅ **Coverage Reporting** - Codecov integration on the Python 3.11 job
- ✅ **Notebook Validation** - Conditional nbmake run when notebooks are present

### Security

- ✅ **CodeQL Analysis** - Semantic code analysis
- ✅ **Semgrep** - Pattern-based security scanning
- ✅ **Secret Scanning** - Gitleaks + TruffleHog
- ✅ **Dependency Review** - Automated vulnerability checks
- ✅ **SBOM Generation** - CycloneDX format
- 🛠️ **Artifact Signing (planned)** - Sigstore/Cosign integration to be scoped

### Documentation

- ✅ **Jupyter Book** - Beautiful documentation (optional)
- ✅ **Auto-generated Docs** - From docstrings
- ✅ **GitHub Pages** - Automated deployment
- ✅ **Notebooks** - Interactive examples (optional)

## Template Configuration

### Required Parameters

| Parameter             | Description                    | Example                                |
| --------------------- | ------------------------------ | -------------------------------------- |
| `project_name`        | Human-readable project name    | "Acme Service"                         |
| `project_slug`        | URL-friendly name (kebab-case) | "acme-service"                         |
| `project_description` | Short description              | "A Python service with best practices" |
| `author_name`         | Your name                      | "Jane Doe"                             |
| `author_email`        | Your email                     | "jane@example.com"                     |

### Optional Parameters

| Parameter               | Options                      | Default    | Description                |
| ----------------------- | ---------------------------- | ---------- | -------------------------- |
| `license`               | Apache-2.0, MIT, Proprietary | Apache-2.0 | License type               |
| `python_version`        | 3.11, 3.12                   | 3.11       | Minimum Python version     |
| `include_jupyter_book`  | yes, no                      | yes        | Include documentation site |
| `enable_security_gates` | yes, no                      | yes        | Enable security scanning   |
| `enable_sbom_signing`   | yes, no                      | yes        | Enable SBOM generation     |
| `enable_contract_tests` | yes, no                      | no         | Enable API contract tests  |
| `ci_provider`           | github, gitlab               | github     | Select CI provider (GitLab scaffolding pending)

## Generated Project Structure

```
acme-service/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Linting, tests, coverage, optional notebook checks
│       ├── security.yml        # CodeQL, Semgrep, secrets, optional SBOM
│       └── docs.yml            # Conditional documentation build & deploy
├── docs/                        # Jupyter Book documentation
│   ├── _config.yml
│   ├── _toc.yml
│   └── intro.md
├── notebooks/                   # Interactive notebooks
│   └── 01_bootstrap.ipynb
├── src/
│   └── acme_service/           # Source code
│       └── __init__.py
├── tests/                       # Test files
│   └── test_smoke.py
├── .editorconfig               # Editor configuration
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks
├── pyproject.toml              # Project configuration
└── README.md                   # Project documentation
```

## Usage

### Interactive Generation

```bash
# Install Cookiecutter
pip install cookiecutter

# Generate from template
cookiecutter templates/python-service

# Follow the prompts
project_name [Acme Service]: My API Service
project_slug [acme-service]: my-api-service
project_description [A Python service with best practices]: RESTful API service
author_name [Your Name]: Jane Doe
author_email [your.email@example.com]: jane@example.com
license [1]: 1  # Apache-2.0
python_version [3.11]: 3.11
include_jupyter_book [1]: 1  # yes
enable_security_gates [1]: 1  # yes
enable_sbom_signing [1]: 1  # yes
enable_contract_tests [1]: 2  # no
ci_provider [1]: 1  # github
```

### Non-Interactive Generation

```bash
# Using --no-input with defaults file
cookiecutter templates/python-service --no-input \
  project_name="My API Service" \
  project_slug="my-api-service" \
  project_description="RESTful API service" \
  author_name="Jane Doe" \
  author_email="jane@example.com"
```

### Post-Generation Setup

```bash
# Navigate to generated project
cd my-api-service

# Install dependencies
pip install -e .[dev]

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest

# Build documentation (if Jupyter Book enabled)
jupyter-book build docs/

# Start development
code .
```

## CI/CD Workflows

### GitHub Actions

**ci.yml** - Main CI/CD Pipeline:

- Lint and format checks
- Unit tests with coverage
- Type checking with mypy
- Multi-version testing (Python 3.11, 3.12)
- Conditional notebook validation (nbmake) when notebooks are present
- Coverage upload via Codecov on Python 3.11 job

**security.yml** - Security Scanning:

- CodeQL (SAST)
- Semgrep (pattern-based)
- Gitleaks (secrets)
- TruffleHog (secrets)
- Dependency review
- SBOM generation (optional)

**docs.yml** - Documentation:

- Jupyter Book build
- GitHub Pages deployment
- Automated on commits to main

> ℹ️ GitLab CI scaffolding is planned; see `Next_Steps.md` for the release/signing roadmap.

## Development

### Local Setup

```bash
# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run all pre-commit hooks
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_smoke.py::test_example

# With verbose output
pytest -v

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# All quality checks
black src/ tests/ && \
  ruff check src/ tests/ && \
  mypy src/ && \
  pytest --cov=src
```

### Documentation

```bash
# Build documentation
jupyter-book build docs/

# Clean and rebuild
jupyter-book clean docs/
jupyter-book build docs/

# View locally
open docs/_build/html/index.html

# Or serve with live reload
jupyter-book serve docs/
```

## Best Practices

### Project Structure

1. **Use `src/` layout** - Avoids import issues
2. **Type hints everywhere** - Enable mypy checking
3. **Comprehensive tests** - ≥80% coverage
4. **Clear documentation** - README, docstrings, Jupyter Book
5. **Pre-commit hooks** - Catch issues before commit

### Testing

1. **Unit tests** - Test individual functions/classes
2. **Integration tests** - Test component interactions
3. **Contract tests** - Validate API contracts (if enabled)
4. **Coverage** - Aim for ≥80% coverage
5. **Fixtures** - Use pytest fixtures for setup

### Security

1. **No secrets** - Never commit credentials
2. **Dependency scanning** - Keep dependencies updated
3. **SBOM** - Generate for supply chain transparency
4. **Signing** - Plan release signing once automation is available
5. **Security scanning** - Run on every commit

## Customization

### Adding Dependencies

```toml
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.11.0",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
]
```

### Modifying CI/CD

Edit `.github/workflows/ci.yml`:

```yaml
# Add environment variables
env:
  CUSTOM_VAR: "value"

# Add steps
steps:
  - name: Custom Step
    run: |
      echo "Custom command"
```

### Adding Workflows

```bash
# Create new workflow
cat > .github/workflows/performance.yml <<EOF
name: Performance Tests
on: [push]
jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install locust
      - run: locust --headless -f tests/performance/locustfile.py
EOF
```

## Troubleshooting

### Common Issues

**Import errors:**

```bash
# Ensure package is installed in editable mode
pip install -e .
```

**Pre-commit hooks failing:**

```bash
# Update hooks
pre-commit autoupdate

# Run manually
pre-commit run --all-files
```

**Coverage below threshold:**

```bash
# Check coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Find untested code
pytest --cov=src --cov-report=term-missing
```

**Documentation build fails:**

```bash
# Clean and rebuild
jupyter-book clean docs/
pip install -e .[docs]
jupyter-book build docs/
```

## Standards Compliance

This template implements:

- ✅ **PEP 517/518** - Modern Python packaging
- ✅ **PEP 8** - Code style (via Black)
- ✅ **NIST SSDF** - Secure development framework
- ✅ **OWASP SAMM** - Software assurance maturity
- ✅ **SLSA Level 3** - Supply chain security (optional)

## Related Resources

- [Template Creation Runbook](../../runbooks/template-creation-runbook.md)
- [Video Tutorial: Creating Services](../../examples/video-tutorials/02-creating-services.md)
- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)

## Contributing

To improve this template:

1. Test with real projects
2. Report issues or edge cases
3. Suggest new features
4. Submit PRs with improvements
5. Share your generated projects

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

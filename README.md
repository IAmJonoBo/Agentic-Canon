# Agentic Canon

**The machine-readable, agent-friendly guide and templates for fast, correct software scaffolding and delivery.**

[![Notebooks Test](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Notebooks%20•%20test/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)
[![Cookiecutters Test](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Cookiecutters%20•%20render%20test/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)
[![Book Deploy](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Jupyter%20Book%20•%20deploy/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)

## What is Agentic Canon?

Agentic Canon is a comprehensive framework for building software projects with industry best practices baked in from day one. It provides:

- 📓 **Executable Notebooks**: Interactive guides for bootstrapping, security, testing, observability, and documentation
- 🎨 **Cookiecutter Templates**: Production-ready project templates for Python, Node.js, React, Go, and documentation
- 🔄 **CI/CD Pipelines**: Pre-configured GitHub Actions workflows with security gates, SBOM generation, and automated deployments
- ✅ **Quality Gates**: Automated testing, linting, security scanning, and compliance checks
- 📊 **Observability**: OpenTelemetry integration with SLO tracking and dashboards
- 📚 **Documentation**: Jupyter Book integration for beautiful, searchable documentation

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/IAmJonoBo/Agentic-Canon.git
cd Agentic-Canon
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a New Project

Choose a template and generate your project:

```bash
# Python service
cookiecutter templates/python-service

# Answer the prompts interactively, or use --no-input with defaults
```

### 4. Explore the Notebooks

The `notebooks/` directory contains executable guides:

```bash
jupyter notebook notebooks/
```

Or view the published Jupyter Book at: [https://IAmJonoBo.github.io/Agentic-Canon/](https://IAmJonoBo.github.io/Agentic-Canon/)

## Available Templates

### Python Service (`templates/python-service`)

Modern Python service with:
- Type hints and mypy
- Black formatting, Ruff linting
- Pytest with coverage
- Optional Jupyter Book documentation
- Optional security scanning (CodeQL, Gitleaks)
- Optional SBOM generation

**Generate:**
```bash
cookiecutter templates/python-service
```

### More Templates Coming Soon

- Node.js Service
- React WebApp (Vite + TypeScript + Playwright + Storybook)
- Go Service
- Docs-Only (Jupyter Book)

## Notebooks

Each notebook is executable and parameterizable with Papermill:

1. **01_bootstrap.ipynb**: Scaffold repositories, enable quality gates, generate SBOM/signing demos
2. **02_security_supply_chain.ipynb**: SAST/secret scanning, SBOM & provenance walkthrough
3. **03_contracts_and_tests.ipynb**: Generate OpenAPI/AsyncAPI specs, run contract + mutation tests
4. **04_observability_slos.ipynb**: OpenTelemetry quickstart & SLO probe examples
5. **05_docs_to_book.ipynb**: Jupytext synchronization and Jupyter Book build automation

## Standards Compliance

This framework aligns with industry standards and best practices:

- **NIST SSDF v1.1**: Secure Software Development Framework
- **OWASP SAMM**: Software Assurance Maturity Model
- **OWASP ASVS**: Application Security Verification Standard (L2/L3 for web/API)
- **SLSA**: Supply-chain Levels for Software Artifacts (targeting Level 3)
- **OpenSSF Scorecard**: Open Source Security Foundation metrics
- **ISO/IEC 25010**: Software quality characteristics
- **ISO/IEC 5055**: Structural quality
- **WCAG 2.2 AA**: Web accessibility standards

## Features

### Security First

- 🔒 Secret scanning with Gitleaks
- 🛡️ SAST with CodeQL and Semgrep
- 📋 SBOM generation (CycloneDX format)
- ✍️ Artifact signing with Sigstore/Cosign
- 🔍 Dependency scanning and updates
- 🎯 SLSA provenance attestation

### Quality Gates

- ✅ Automated testing (unit, integration, E2E)
- 📊 Code coverage tracking (≥80% target)
- 🎨 Code formatting (Black, Prettier)
- 🔍 Linting (Ruff, ESLint, golangci-lint)
- 🧬 Mutation testing
- 📝 Contract testing (Pact)

### Observability

- 📡 OpenTelemetry instrumentation
- 📊 Metrics, traces, and logs
- 🎯 SLI/SLO definitions
- 💰 Error budget tracking
- 📈 Grafana dashboards
- 🚨 Prometheus alerting

### Developer Experience

- 🚀 Fast feedback loops
- 🔄 Pre-commit hooks
- 📝 Git-friendly notebooks (Jupytext)
- 🎨 Beautiful documentation (Jupyter Book)
- 🤖 GitHub Actions automation
- 📦 Binder integration for reproducibility

## Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Create notebook pairs (if editing .ipynb files)
jupytext --set-formats ipynb,md:myst notebooks/*.ipynb
```

### Testing

```bash
# Test notebooks
pytest --nbmake notebooks/**/*.ipynb

# Test cookiecutter templates
pytest tests/test_cookiecutters.py -v

# Run all tests
pytest
```

### Documentation

```bash
# Build Jupyter Book
jupyter-book build docs

# View locally
open docs/_build/html/index.html

# Deploy to GitHub Pages (done automatically by CI)
ghp-import -n -p -f docs/_build/html
```

## Roadmap

### v1.0 (Current)
- ✅ Core notebooks
- ✅ Python service template
- ✅ GitHub Actions workflows
- ✅ Jupyter Book documentation
- 🚧 Additional templates (Node, React, Go, Docs)

### v1.1.0 (Next)
- Azure Pipelines support
- Enhanced dashboards (DORA, SPACE, Security, Quality metrics)
- Additional examples (FastAPI, Express, React apps)
- Video tutorials
- Interactive CLI wizard

### v2.0.0 (Future)
- Multi-cloud support (AWS, Azure, GCP)
- Advanced fitness functions
- ML-powered insights (anomaly detection, predictive analysis)
- Full automation (auto-remediation, self-healing)
- Community template marketplace

See [TASKS.md](TASKS.md) for detailed implementation tracking.

## Contributing

Contributions are welcome! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache-2.0

## Authors

- Jonathan Boardman (@IAmJonoBo)

## Acknowledgments

This project is inspired by and builds upon:
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- [Jupyter Book](https://jupyterbook.org/)
- [OpenTelemetry](https://opentelemetry.io/)
- [SLSA](https://slsa.dev/)
- [OWASP](https://owasp.org/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf)

## Links

- 📖 [Documentation](https://IAmJonoBo.github.io/Agentic-Canon/)
- 🐛 [Issue Tracker](https://github.com/IAmJonoBo/Agentic-Canon/issues)
- 💬 [Discussions](https://github.com/IAmJonoBo/Agentic-Canon/discussions)

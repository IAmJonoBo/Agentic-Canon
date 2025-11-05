# Agentic Canon Bible

This book is the machine-readable, agent-friendly guide and templates for fast, correct scaffolding and delivery. See `notebooks/` for executable playbooks.

## What is Agentic Canon?

Agentic Canon is a comprehensive framework for building software projects with best practices baked in from day one. It provides:

- **Executable Notebooks**: Interactive guides for bootstrapping, security, testing, observability, and documentation
- **Cookiecutter Templates**: Production-ready project templates for Python, Node.js, React, Go, and documentation
- **CI/CD Pipelines**: Pre-configured GitHub Actions workflows with security gates, SBOM generation, and automated deployments
- **Quality Gates**: Automated testing, linting, security scanning, and compliance checks
- **Observability**: OpenTelemetry integration with SLO tracking and dashboards
- **Documentation**: Jupyter Book integration for beautiful, searchable documentation

## Getting Started

1. **Explore the Notebooks**: Start with the bootstrap notebook to understand the core concepts
2. **Choose a Template**: Select from Python, Node.js, React, or Go service templates
3. **Generate Your Project**: Use Cookiecutter to create a new project from a template
4. **Customize and Deploy**: Follow the generated CI/CD pipelines to deploy your service

## Notebooks

Each notebook is executable and parameterizable with Papermill:

1. **01_bootstrap**: Scaffold repositories, enable quality gates, generate SBOM/signing demos
2. **02_security_supply_chain**: SAST/secret scanning, SBOM & provenance walkthrough
3. **03_contracts_and_tests**: Generate OpenAPI/AsyncAPI specs, run contract + mutation tests
4. **04_observability_slos**: OpenTelemetry quickstart & SLO probe examples
5. **05_docs_to_book**: Jupytext synchronization and Jupyter Book build automation

## Standards Compliance

This framework aligns with industry standards:

- **NIST SSDF v1.1**: Secure Software Development Framework
- **OWASP SAMM**: Software Assurance Maturity Model
- **OWASP ASVS**: Application Security Verification Standard
- **SLSA**: Supply-chain Levels for Software Artifacts
- **OpenSSF Scorecard**: Open Source Security Foundation metrics
- **ISO/IEC 25010**: Software quality characteristics
- **WCAG 2.2 AA**: Web accessibility standards

## Contributing

Contributions are welcome! See our templates and notebooks for examples, and submit PRs to enhance the framework.

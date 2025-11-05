# Agentic Canon

**The machine-readable, agent-friendly guide and templates for fast, correct software scaffolding and delivery.**

[![Notebooks Test](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Notebooks%20•%20test/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)
[![Cookiecutters Test](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Cookiecutters%20•%20render%20test/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)
[![Book Deploy](https://github.com/IAmJonoBo/Agentic-Canon/workflows/Jupyter%20Book%20•%20deploy/badge.svg)](https://github.com/IAmJonoBo/Agentic-Canon/actions)

> **🎉 Project Status:** v1.0 ✅ Complete | v1.1.0 ✅ ~98% Complete | v2.0.0 🚧 ~40% Complete  
> **📍 Progress Tracker:** See [TASKS.md](TASKS.md) for detailed status (single source of truth)  
> **✅ Verified:** 2025-10-12 via comprehensive sanity check (121 passed, 2 warnings, 0 failed)

> 🔧 **Toolchain alignment:** Template runtimes are pinned via `n00-cortex/data/toolchain-manifest.json`. Update that manifest first, then rerun `.dev/validate-templates.sh --all` to pick up new versions.

## What is Agentic Canon?

Agentic Canon is a **comprehensive framework for frontier software excellence** that combines industry best practices, standards compliance, and automation to enable fast, secure, and reliable software delivery. It provides everything needed to build production-ready projects with security, quality, and observability baked in from day one.

### Core Components

- 📓 **Executable Notebooks**: Interactive guides for bootstrapping, security, testing, observability, and documentation
- 🎨 **Cookiecutter Templates**: Production-ready project templates for Python, Node.js, React, Go, and documentation
- 🔄 **CI/CD Pipelines**: Pre-configured GitHub Actions workflows with security gates, SBOM generation, and automated deployments
- ✅ **Quality Gates**: Automated testing, linting, security scanning, and compliance checks (80%+ coverage, mutation testing)
- 📊 **Observability**: OpenTelemetry integration with SLO tracking, error budgets, and dashboards
- 📚 **Documentation**: Jupyter Book integration for beautiful, searchable, version-controlled documentation
- 🎯 **Standards Compliance**: NIST SSDF, OWASP SAMM/ASVS, SLSA, OpenSSF Scorecard, ISO/IEC 25010, WCAG 2.2 AA
- 🤖 **Agent-Friendly**: Machine-readable formats optimized for AI/agent automation and autonomous execution

### Key Documents

#### Framework Core

- **[FRAMEWORK.md](FRAMEWORK.md)** - 🎯 **Unified framework defining OUR approach to software excellence**
- **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - ⭐ **Comprehensive quality standards for all disciplines**
- **[CONVENTIONS.md](CONVENTIONS.md)** - 📋 **Development conventions and best practices**

#### Implementation Guides

- **[TASKS.md](TASKS.md)** - 📍 **SINGLE SOURCE OF TRUTH** - Complete implementation roadmap tracking all features and priorities
- **[SUMMARY.md](SUMMARY.md)** - Executive summary derived from TASKS.md
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Technical decisions, architecture, testing strategy, and handover guide
- **[V110-V200-SUMMARY.md](V110-V200-SUMMARY.md)** - Detailed v1.1.0 and v2.0.0 status

#### Standards References

- **[BIBLE.md](BIBLE.md)** - AI-friendly reference with implementation checklists, quality gates, and quick-start commands
- **[INDEX.md](INDEX.md)** - Complete navigation guide for all templates, standards, and usage patterns
- **[TEMPLATE_STANDARDS.md](TEMPLATE_STANDARDS.md)** - 📐 **Standards requirements for templates** - What must be met vs. what can be omitted
- **[Red Team + Software Excellence.md](Red%20Team%20+%20Software%20Excellence.md)** - Comprehensive playbook for frontier software excellence with detailed controls
- **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Technical implementation details for notebooks, templates, and CI/CD setup
- **[control-traceability-matrix.json](control-traceability-matrix.json)** - Machine-readable standards → implementation → evidence mapping

#### Process & Management

- **[docs/adr/](docs/adr/)** - Architecture Decision Records with [lifecycle guide](docs/adr/ADR-LIFECYCLE.md)
- **[docs/ISSUE_MANAGEMENT.md](docs/ISSUE_MANAGEMENT.md)** - Comprehensive issue and sprint management guide
- **[docs/TASKS-ADR-SYNC.md](docs/TASKS-ADR-SYNC.md)** - Automated TASKS.md and ADR synchronization system
- **[PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md)** - Automated project management setup

## Quick Start

### For Developers

```bash
# 1. Clone the repository
git clone https://github.com/IAmJonoBo/Agentic-Canon.git
cd Agentic-Canon

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a new project from template
cookiecutter templates/python-service
# Or: templates/node-service, templates/react-webapp, templates/go-service, templates/docs-only

# 4. Explore executable notebooks
jupyter notebook notebooks/
```

### For AI Agents

1. **Discover**: [catalog.json](catalog.json) - Machine-readable catalog of all templates, assets, and resources ([docs](docs/CATALOG.md))
2. **Read**: [BIBLE.md](BIBLE.md) for comprehensive guidance and quality gates
3. **Check**: [control-traceability-matrix.json](control-traceability-matrix.json) for compliance requirements
4. **Execute**: [runbooks/agent-runbook.json](runbooks/agent-runbook.json) for step-by-step automation
5. **Use**: Templates from [templates/](templates/) directory with machine-readable configurations

### For Platform Teams

1. **Assess**: Current state against [control-traceability-matrix.json](control-traceability-matrix.json)
2. **Plan**: Use [BIBLE.md](BIBLE.md) implementation checklist (7-phase approach)
3. **Deploy**: Backstage template from [templates/platform/backstage/](templates/platform/backstage/)
4. **Monitor**: Set up SLOs from [templates/observability/slo/](templates/observability/slo/)

**Published Documentation**: [https://IAmJonoBo.github.io/Agentic-Canon/](https://IAmJonoBo.github.io/Agentic-Canon/)

## Available Templates

**All 6 primary templates are complete and tested (21 cookiecutter tests passing ✅):**

All templates include security scanning, quality gates, SBOM generation, and CI/CD pipelines (where applicable).

### Python Service (`templates/python-service`) ✅

Modern Python service with type hints, Black formatting, Ruff linting, pytest with coverage, optional Jupyter Book documentation, optional security scanning (CodeQL, Gitleaks), and optional SBOM generation.

**Generate:**

```bash
cookiecutter templates/python-service
# Or: agentic-canon init
```

### Node.js Service (`templates/node-service`) ✅

TypeScript service with ESLint, Prettier, Vitest testing, security scanning, and CI/CD pipeline.

**Generate:**

```bash
cookiecutter templates/node-service
# Or: agentic-canon init
```

### React WebApp (`templates/react-webapp`) ✅

Vite + TypeScript + React with Playwright E2E tests, Storybook component library, accessibility testing (WCAG 2.2 AA), and GitHub Pages deployment.

**Generate:**

```bash
cookiecutter templates/react-webapp
# Or: agentic-canon init
```

### Go Service (`templates/go-service`) ✅

Go service with golangci-lint, testing, Makefile build automation, security scanning, and CI/CD pipeline.

**Generate:**

```bash
cookiecutter templates/go-service
# Or: agentic-canon init
```

### Docs-Only (`templates/docs-only`) ✅

Jupyter Book documentation site with MyST Markdown, version control via Jupytext, and automated GitHub Pages deployment.

**Generate:**

```bash
cookiecutter templates/docs-only
# Or: agentic-canon init
```

### Project Management (`templates/project-management`) ✅ **NEW**

Automated project management setup with GitHub Actions workflows for task tracking and issue management.

**Features:**

- 🔄 TODO/FIXME → GitHub Issues automation
- 📋 Markdown tasklist → GitHub Issues automation
- 💬 PR review follow-ups → Issues automation
- 🏷️ Auto-triage and label new issues
- 🧹 Stale issue management
- 👥 CODEOWNERS and PR templates
- 📝 Issue templates (bug, feature, task)

**Generate:**

```bash
cookiecutter templates/project-management
# Or: agentic-canon repo-init  # Add to existing repo
```

**Use Case:** Add automated task tracking and project management to any repository, eliminating manual overhead while maintaining visibility.

### Additional Template Categories ✅

8 specialized template categories covering:

- **Architecture** - ADRs, C4 diagrams, fitness functions
- **Automation** - Hooks, bots, workflows
- **CI/CD** - GitHub Actions, GitLab CI, Azure Pipelines
- **Contracts** - OpenAPI, AsyncAPI specifications
- **Observability** - OpenTelemetry, SLO definitions
- **Platform** - Backstage, policy enforcement
- **Repository** - Common files, configurations
- **Security** - Scanning tools, SBOM, compliance

## Machine-Readable Catalog

**[catalog.json](catalog.json)** - Complete machine-readable catalog of all templates, assets, and resources ([Documentation](docs/CATALOG.md))

The catalog enables:

- 🔍 **Discovery**: Find templates by language, framework, or features
- 🤖 **Automation**: Power CLI tools, agents, and MCP servers
- 📊 **Validation**: Check requirements and compliance
- 🔗 **Integration**: Seamless integration with external tools

**Example queries:**

```bash
# List all templates
cat catalog.json | jq '.templates.cookiecutter[] | {id, name, language}'

# Find Python templates
cat catalog.json | jq '.templates.cookiecutter[] | select(.language == "python")'

# Get template usage commands
cat catalog.json | jq '.templates.cookiecutter[] | select(.id == "python-service") | .usage'

# Check compliance standards
cat catalog.json | jq '.compliance.standards'
```

**What's cataloged:**

- 6 Cookiecutter templates with full metadata
- 4 Grafana dashboards (DORA, SPACE, Quality, Security)
- 5 GitHub Actions workflows + 2 Azure Pipelines
- 3 Fitness function templates
- Framework documentation and ADRs
- CLI commands and distribution methods
- 7 compliance standards

## Dependency Governance

- Renovate extends the shared preset published in `n00-cortex/renovate-presets/workspace.json`; repo-specific rules live in [renovate.json](renovate.json).
- `nox -s validate_templates_all` fails fast if template runtimes drift from `n00-cortex/data/toolchain-manifest.json`.

See [docs/CATALOG.md](docs/CATALOG.md) for usage examples, integration patterns, and API reference.

## Notebooks

Each notebook is executable, parameterizable with Papermill, and version-controlled with Jupytext:

1. **01_bootstrap.ipynb**: Scaffold repositories, enable quality gates, generate SBOM/signing demos
2. **02_security_supply_chain.ipynb**: SAST/secret scanning, SBOM & provenance walkthrough
3. **03_contracts_and_tests.ipynb**: Generate OpenAPI/AsyncAPI specs, run contract + mutation tests
4. **04_observability_slos.ipynb**: OpenTelemetry quickstart & SLO probe examples
5. **05_docs_to_book.ipynb**: Jupytext synchronization and Jupyter Book build automation

**Key Features:**

- Git-friendly via Jupytext pairing (ipynb ↔ md:myst)
- Automated execution in CI with nbmake/pytest
- Scheduled runs with Papermill for continuous validation
- Published as searchable documentation via Jupyter Book

## Standards Compliance

This framework embeds industry-leading standards and best practices directly into templates and workflows:

### Security & Supply Chain

- **NIST SSDF v1.1**: Complete Secure Software Development Framework compliance
- **OWASP SAMM 2.0**: Software Assurance Maturity Model (Level 2 maturity)
- **OWASP ASVS 4.0**: Application Security Verification Standard (L2/L3 for web/API)
- **SLSA Level 3**: Build provenance, signed artifacts, isolated builds
- **OpenSSF Scorecard**: Security health metrics with automated checks
- **OWASP LLM Top 10**: AI/LLM security controls for Copilot/agent usage
- **CWE Top 25**: Complete coverage of most dangerous software weaknesses

### Quality & Architecture

- **ISO/IEC 25010**: Software quality characteristics (maintainability, reliability, performance, usability)
- **ISO/IEC 5055**: Structural quality metrics and automated weakness detection
- **ISO 9241-210**: User-centered design process compliance

### Accessibility

- **WCAG 2.2 AA**: Web Content Accessibility Guidelines (automated testing integrated)

### Governance & Compliance

- **Control Traceability Matrix**: Machine-readable mapping of standards → controls → implementation → evidence
- **Audit-Ready Evidence**: Automated collection of SBOMs, provenance, test results, scan results, and logs
- **Policy-as-Code**: OPA/Kyverno for admission control and drift prevention

See [control-traceability-matrix.json](control-traceability-matrix.json) for complete standards mapping.

## Features

### Security by Construction (Deep Dive)

- 🔒 **Secret Scanning**: Gitleaks/TruffleHog on every commit
- 🛡️ **SAST/DAST**: CodeQL, Semgrep for code analysis; OWASP ZAP for runtime testing
- 📋 **SBOM Generation**: CycloneDX/SPDX format with license and provenance metadata
- ✍️ **Artifact Signing**: Sigstore/Cosign with keyless signing
- 🔍 **Dependency Management**: Automated scanning and updates via Dependabot/Renovate
- 🎯 **SLSA Provenance**: in-toto attestations for build integrity
- 🚨 **VEX Documents**: Vulnerability Exploitability eXchange for triage
- 🛡️ **Zero-Trust**: Workload identities (SPIFFE/SPIRE) and signed IaC/templates

### Quality Gates (Non-Negotiable)

- ✅ **Automated Testing**: Unit, integration, contract, E2E testing pyramid
- 📊 **Code Coverage**: ≥80% target enforced in CI
- 🧬 **Mutation Testing**: 40-60% initial thresholds with quarterly ratchets
- 🎨 **Code Formatting**: Black, Prettier, gofmt (language-specific)
- 🔍 **Linting**: Ruff, ESLint, golangci-lint with strict rules
- 📝 **Contract Testing**: Pact for HTTP, AsyncAPI for event-driven
- 🏗️ **SonarQube Integration**: Zero new code smells, ≤3% duplication
- ⚡ **Performance Budgets**: Core Web Vitals, API latency thresholds enforced in CI
- ♿ **Accessibility**: WCAG 2.2 AA compliance with axe-core testing

### Observability & Reliability

- 📡 **OpenTelemetry**: Auto-instrumentation for traces, metrics, and logs
- 🎯 **SLI/SLO Definitions**: User-journey-based service level objectives
- 💰 **Error Budget Tracking**: Automated budget consumption with deployment blocks
- 📈 **Dashboards**: Grafana templates for DORA, SPACE, security, and quality metrics
- 🚨 **Alerting**: Prometheus rules with intelligent routing
- 🔄 **Progressive Delivery**: Canary, blue-green deployments with automated rollback
- 🎪 **Chaos Engineering**: Fault injection and game days integrated
- 🔮 **Predictive Analysis**: ML-powered anomaly detection (v2.0.0)

### Developer Experience & Platform

- 🚀 **Trunk-Based Development**: Small PRs, fast feedback loops
- 🔄 **Pre-commit Hooks**: Automated formatting, linting, and security checks
- 📝 **Git-Friendly Notebooks**: Jupytext pairing for version control
- 🎨 **Beautiful Documentation**: Jupyter Book with MyST Markdown
- 🤖 **GitHub Actions**: Complete automation with workflow reuse
- 📦 **Binder Integration**: One-click reproducible environments
- 🎯 **Backstage Integration**: Self-service golden paths and TechDocs
- 📊 **DORA Metrics**: Automated tracking of deployment frequency, lead time, MTTR, change failure rate
- 🧠 **SPACE Signals**: Developer flow, cognitive load, and interruption monitoring
- 🔧 **Auto-Remediation**: Dependency updates, security patches, drift correction

## Repository Organization

**Separation of Concerns:** The repository is organized with clear boundaries between development tools, distribution assets, and boilerplates:

### 📁 Development Tools (`.dev/`)

**Internal use - for maintaining this repository:**

- `.dev/validate-templates.sh` - Unified template validation orchestrator (runs sync → render → lint → format)
- `.dev/sanity-check.sh` - Repository health checks
- `.dev/scripts/` - Maintenance scripts (labels, etc.)

### 📦 Distribution Assets (External use)

**For end users and AI generators:**

- `agentic_canon_cli/` - CLI wizard for project generation
- `templates/` - Cookiecutter templates and supporting files
- `notebooks/` - Executable guides for bootstrapping, security, testing, observability
- `docs/` - Jupyter Book documentation
- `examples/` - Reference implementations and dashboards

### 🎯 Boilerplates (`templates/`)

**Ready-to-use project templates:**

- `python-service/` - Modern Python with pytest, mypy, Black
- `node-service/` - TypeScript with Vitest, ESLint
- `react-webapp/` - React + Vite + Storybook + Playwright
- `go-service/` - Go with golangci-lint
- `docs-only/` - Jupyter Book documentation site
- Supporting templates for CI/CD, security, observability, and more

See [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) for complete details.

## Development

### Setup for Contributors

```bash
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Create notebook pairs (if editing .ipynb files)
jupytext --set-formats ipynb,md:myst notebooks/*.ipynb
jupytext --sync notebooks/*.ipynb
```

### Testing

```bash
# Test notebooks (execution validation)
pytest --nbmake notebooks/**/*.ipynb

# Test cookiecutter templates (rendering validation)
pytest tests/test_cookiecutters.py -v

# Run all tests
pytest -v
```

### Documentation

```bash
# Build Jupyter Book locally
jupyter-book build docs

# View locally
open docs/_build/html/index.html  # macOS
# or: xdg-open docs/_build/html/index.html  # Linux

# Deploy to GitHub Pages (automated by CI on main branch)
ghp-import -n -p -f docs/_build/html
```

### Validation

```bash
# Validate GitHub Actions workflows
actionlint .github/workflows/*.yml

# Validate templates (sync + render + lint + format)
.dev/validate-templates.sh
# or run directly with Nox
nox -s validate_templates_all

# Check notebook output is stripped
git status  # Should show no changes to .ipynb files after execution
```

## Roadmap

### v1.0 (Current - Foundation)

- ✅ Core notebooks (01-05) with Jupytext pairing
- ✅ Python service template with complete CI/CD
- ✅ GitHub Actions workflows (notebooks-test, book-deploy, cookiecutters-test, notebooks-schedule)
- ✅ Jupyter Book documentation site
- ✅ BIBLE.md and INDEX.md reference guides
- ✅ Control traceability matrix
- 🚧 Additional templates (Node, React, Go, Docs-only)
- 🚧 Template directory structure (`templates/cicd/`, `templates/security/`, etc.)
- 🚧 Validation scripts and testing infrastructure

### v1.1.0 (Next - Enhanced Capabilities)

- **Azure Pipelines**: Complete Azure DevOps CI/CD templates
- **Enhanced Dashboards**: Grafana templates for DORA, SPACE, security, and quality metrics
- **Additional Examples**: FastAPI microservice, Express API, React dashboard, gRPC service
- **Video Tutorials**: Getting started, service creation, CI/CD setup, security gates, observability
- **Interactive CLI Wizard**: `agentic-canon init` with guided setup and template selection
- **GitOps Templates**: ArgoCD and Flux configurations for each cloud provider
- **Performance Budgets**: Automated Core Web Vitals and API latency enforcement

### v2.0.0 (Future - Advanced Automation)

- **Multi-Cloud Support**: AWS, Azure, GCP templates with cloud-agnostic abstractions
- **Advanced Fitness Functions**: Automated architecture quality gates (coupling, cyclic dependencies, attack surface)
- **ML-Powered Insights**: Anomaly detection, predictive failure analysis, intelligent alerting
- **Full Automation**: Auto-remediation, self-healing infrastructure, intelligent deployment scheduling
- **Community Template Marketplace**: Contribution framework, gallery, ratings, and automated updates via Cruft
- **AI/ML Governance**: ISO/IEC 42001 compliance, model cards, evaluation artifacts
- **Continuous Chaos**: Automated fault injection, game days, and resilience testing

See [TASKS.md](TASKS.md) for detailed implementation tracking and priority matrix.

## Architecture & Key Concepts

### Security by Construction

Security is embedded from the start, not bolted on later. Every template includes:

- **Shift-Left Security**: SAST/DAST in CI before deployment
- **Supply Chain Integrity**: SLSA L3 provenance, signed artifacts, SBOMs
- **Zero-Trust Architecture**: Workload identities, admission controllers, policy-as-code
- **Continuous Verification**: Automated scanning, drift detection, compliance checks

### Quality Gates

Non-negotiable gates enforce quality standards:

```yaml
gates:
  build:
    - compiles: true
    - unit_tests: green
    - coverage: ">= 80%"
    - mutation_score: ">= 40%"
  security:
    - secrets_scan: clean
    - sast_critical: 0
    - sbom_generated: true
    - provenance_signed: true
  quality:
    - code_smells: 0
    - duplicates: "<= 3%"
    - sonar_quality_gate: passed
  performance:
    - core_web_vitals: within_budget
    - p95_latency: "<= threshold"
  accessibility:
    - wcag_aa_violations: 0
```

### Observability & SLOs

Instrumentation and monitoring built-in:

- **OpenTelemetry**: Unified traces, metrics, and logs
- **SLI/SLO Framework**: User-journey-based service level objectives
- **Error Budgets**: Automated tracking with deployment blocks when exhausted
- **Progressive Delivery**: Canary analysis with automated rollback on SLO violations

### Developer Platform

Self-service infrastructure reduces friction:

- **Backstage Integration**: Software templates, TechDocs, service catalog
- **Golden Paths**: Pre-validated patterns for common use cases
- **GitOps**: Declarative infrastructure with drift detection
- **Auto-Remediation**: Dependency updates, security patches, configuration fixes

### Agent-Friendly Design

Optimized for AI/agent automation:

- **Machine-Readable Formats**: JSON, YAML, structured Markdown
- **Task Graphs**: Explicit dependencies, predicates, rollback paths
- **Control Traceability**: Standards → Implementation → Evidence mapping
- **Agent Runbooks**: Step-by-step execution guides with decision predicates

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- New Cookiecutter templates for additional languages/frameworks
- Enhanced dashboards and observability configurations
- Additional examples and tutorials
- Documentation improvements
- Bug fixes and optimizations
- Cloud provider integrations (AWS, Azure, GCP)

### Contribution Process

1. Review [Red Team + Software Excellence.md](Red%20Team%20+%20Software%20Excellence.md) for standards
2. Check [TASKS.md](TASKS.md) for current priorities
3. Open an issue to discuss major changes
4. Submit PRs with tests and documentation
5. All contributions must pass quality gates (coverage, linting, security scans)

## License

Apache-2.0

## Authors

- Jonathan Boardman (@IAmJonoBo)

## Acknowledgments

This project is inspired by and builds upon:

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - Project templating
- [Jupyter Book](https://jupyterbook.org/) - Beautiful documentation from notebooks
- [Jupytext](https://jupytext.readthedocs.io/) - Version control for notebooks
- [OpenTelemetry](https://opentelemetry.io/) - Unified observability
- [SLSA](https://slsa.dev/) - Supply chain security framework
- [OWASP](https://owasp.org/) - Application security standards (SAMM, ASVS, LLM Top 10)
- [NIST SSDF](https://csrc.nist.gov/Projects/ssdf) - Secure software development practices
- [OpenSSF](https://openssf.org/) - Open source security best practices
- [Backstage](https://backstage.io/) - Developer platform and golden paths
- [Sigstore](https://www.sigstore.dev/) - Artifact signing and transparency

## Related Resources

### Standards & Frameworks

- [NIST SSDF v1.1](https://csrc.nist.gov/publications/detail/sp/800-218/final) - Secure Software Development Framework
- [OWASP SAMM 2.0](https://owaspsamm.org/) - Software Assurance Maturity Model
- [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/) - Application Security Verification Standard
- [SLSA Framework](https://slsa.dev/spec/v1.0/) - Supply-chain Levels for Software Artifacts
- [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) - Software quality model
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) - Web Content Accessibility Guidelines

### Tools & Projects

- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - Security health metrics
- [in-toto](https://in-toto.io/) - Supply chain integrity framework
- [CycloneDX](https://cyclonedx.org/) - SBOM standard
- [Cosign](https://github.com/sigstore/cosign) - Container signing
- [Renovate](https://github.com/renovatebot/renovate) - Automated dependency updates
- [Cruft](https://cruft.github.io/cruft/) - Template synchronization

## Links

- 📖 [Documentation](https://IAmJonoBo.github.io/Agentic-Canon/) - Published Jupyter Book
- 🗂️ [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) - Complete guide to repository organization
- 🐛 [Issue Tracker](https://github.com/IAmJonoBo/Agentic-Canon/issues) - Report bugs or request features
- 💬 [Discussions](https://github.com/IAmJonoBo/Agentic-Canon/discussions) - Ask questions and share ideas
- 📋 [BIBLE.md](BIBLE.md) - AI-friendly implementation reference
- 📑 [INDEX.md](INDEX.md) - Complete template navigation
- 🎯 [Red Team + Software Excellence.md](Red%20Team%20+%20Software%20Excellence.md) - Comprehensive playbook

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-11  
**Maintained By:** Jonathan Boardman (@IAmJonoBo)

Built with ❤️ for developers, platform teams, and AI agents

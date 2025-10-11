# Agentic Canon - Directory Structure

**Purpose:** Complete guide to repository organization and file locations

**Last Updated:** 2025-10-11

---

## 📁 Repository Overview

This repository is organized for maximum clarity, ease of access, and maintainability. Each top-level directory serves a specific purpose in the Agentic Canon ecosystem.

```
Agentic-Canon/
├── 📄 Root Documentation          # Core project documents
├── 📁 agentic_canon_cli/          # Interactive CLI wizard
├── 📁 binder/                     # Binder environment config
├── 📁 docs/                       # Jupyter Book documentation
├── 📁 examples/                   # Reference implementations
├── 📁 notebooks/                  # Executable Jupyter notebooks
├── 📁 runbooks/                   # Operational procedures
├── 📁 templates/                  # Cookiecutter templates
└── 📁 tests/                      # Test suite
```

---

## 📄 Root Documentation

Core project documentation files located at repository root for easy discovery:

### Essential Project Documents
- **`README.md`** - Project overview, quick start, features, installation
- **`TASKS.md`** - Complete task tracking (v1.0, v1.1.0, v2.0.0)
- **`CHANGELOG.md`** - Version history and release notes
- **`LICENSE`** - Apache 2.0 license

### Contribution & Community
- **`CONTRIBUTING.md`** - Contribution guidelines and workflow
- **`CODE_OF_CONDUCT.md`** - Community standards and expectations
- **`CODEOWNERS`** - Code ownership and review assignments
- **`SECURITY.md`** - Security policy, reporting, and controls

### Planning & Status Documents
- **`SUMMARY.md`** - Project completion summary and next steps
- **`V110-V200-SUMMARY.md`** - v1.1.0 to v2.0.0 implementation status

### Comprehensive Guides
- **`Agentic_Canon.md`** - Unified playbook and implementation blueprint
- **`BIBLE.md`** - Detailed implementation guide
- **`Red Team + Software Excellence.md`** - Security and quality playbook
- **`INDEX.md`** - Complete repository index
- **`INSTRUCTIONS.md`** - User instructions and getting started

### Configuration Files
- **`.gitignore`** - Git ignore rules
- **`.gitattributes`** - Git attributes (nbstripout filters)
- **`.pre-commit-config.yaml`** - Pre-commit hooks configuration
- **`jupytext.toml`** - Jupytext notebook pairing settings
- **`renovate.json`** - Renovate dependency update config
- **`requirements.txt`** - Python dependencies
- **`validate-templates.sh`** - Template validation script
- **`control-traceability-matrix.json`** - Compliance control mapping

---

## 📁 agentic_canon_cli/

Interactive CLI wizard for project generation

```
agentic_canon_cli/
├── __init__.py                    # Package initialization
├── __main__.py                    # CLI entry point
├── cli.py                         # CLI implementation with Click
└── README.md                      # CLI documentation and usage
```

**Purpose:** Provides `agentic-canon` command for interactive project scaffolding

**Features:**
- Interactive template selection
- Configuration wizard
- Feature toggles (security, SBOM, Jupyter Book)
- CI/CD provider selection
- Post-generation setup automation

**Usage:**
```bash
pip install -e .
agentic-canon init
```

---

## 📁 binder/

Binder environment configuration for interactive notebooks

```
binder/
└── requirements.txt               # Binder dependencies
```

**Purpose:** Enables running notebooks in cloud via [MyBinder.org](https://mybinder.org)

**Features:**
- Zero-install notebook execution
- Shareable interactive documentation
- Automatic environment setup

**Usage:** Click "Launch Binder" badge in README

---

## 📁 docs/

Jupyter Book documentation sources

```
docs/
├── _config.yml                    # Jupyter Book configuration
├── _toc.yml                       # Table of contents
├── intro.md                       # Documentation landing page
├── adr/                           # Architecture Decision Records
│   ├── README.md                  # ADR index
│   ├── template.md                # ADR template
│   ├── ADR-001-cookiecutter-multi-template.md
│   ├── ADR-002-jupytext-pairing.md
│   └── ADR-003-github-actions-ci.md
└── notebooks/                     # MyST markdown notebooks
    ├── 01_bootstrap.md
    ├── 02_security_supply_chain.md
    ├── 03_contracts_and_tests.md
    ├── 04_observability_slos.md
    └── 05_docs_to_book.md
```

**Purpose:** Source files for beautiful, interactive documentation built with Jupyter Book

**Key Features:**
- Executable documentation
- MyST markdown format
- Synced with Jupytext
- Auto-deployed to GitHub Pages
- Built-in search and navigation

**Build Commands:**
```bash
jupyter-book build docs/
jupyter-book clean docs/  # Clean build artifacts
```

### Architecture Decision Records (ADRs)

Documented architecture decisions with context, rationale, and consequences:

- **ADR-001:** Cookiecutter multi-template approach
- **ADR-002:** Jupytext for notebook version control
- **ADR-003:** GitHub Actions for CI/CD
- **Planned:** ADR-004 (OpenTelemetry), ADR-005 (SLSA)

---

## 📁 examples/

Reference implementations and practical examples

```
examples/
├── azure-pipelines/               # Azure DevOps pipeline examples
│   ├── README.md                  # Setup guide
│   ├── python-service/
│   │   └── azure-pipelines.yml
│   └── node-service/
│       └── azure-pipelines.yml
├── community/                     # Community contribution framework
│   ├── README.md                  # Community guide
│   └── CONTRIBUTING-TEMPLATES.md  # Template contribution guide
├── dashboards/                    # Monitoring & observability dashboards
│   ├── README.md                  # Dashboard documentation
│   ├── dora-metrics.json          # DORA metrics Grafana dashboard
│   ├── space-devex-metrics.json   # SPACE/DevEx metrics dashboard
│   ├── security-metrics.json      # Security metrics dashboard
│   ├── quality-metrics.json       # Code quality metrics dashboard
│   ├── otel-collector-config.yaml # OpenTelemetry Collector config
│   ├── prometheus-alerts.yaml     # Prometheus alerting rules
│   └── grafana/                   # Additional Grafana resources
│       └── README.md
├── fitness-functions/             # Architecture fitness functions
│   └── README.md                  # Framework and examples
├── ml-insights/                   # ML-powered insights framework
│   └── README.md                  # ML framework documentation
├── multi-cloud/                   # Multi-cloud deployment examples
│   ├── README.md                  # Multi-cloud guide
│   └── aws/                       # AWS-specific examples
│       └── README.md
├── projects/                      # Example project implementations
│   └── fastapi-microservice-README.md
└── video-tutorials/               # Video tutorial scripts
    ├── 01-getting-started.md      # Getting started (5-7 min)
    ├── 02-creating-services.md    # Creating services (8-10 min)
    ├── 03-cicd-setup.md           # CI/CD setup (10-12 min)
    ├── 04-security-gates.md       # Security gates (12-15 min)
    ├── 05-observability-setup.md  # Observability (10-12 min)
    └── 06-jupyter-book.md         # Jupyter Book (8-10 min)
```

**Purpose:** Production-ready examples demonstrating Agentic Canon capabilities

### Examples Categories

#### 1. Azure Pipelines (`azure-pipelines/`)
Multi-stage Azure DevOps pipelines for Python and Node.js services
- Build, test, security scanning, deployment stages
- Comparison with GitHub Actions
- Variable configuration examples

#### 2. Community (`community/`)
Framework for community template contributions
- Contribution guidelines
- Template standards and quality requirements
- Review process
- PR templates

#### 3. Dashboards (`dashboards/`)
Production-ready Grafana dashboards and monitoring configs
- **DORA Metrics:** Deployment frequency, lead time, MTTR, change failure rate
- **SPACE/DevEx:** Developer satisfaction, flow time, cognitive load
- **Security:** Vulnerability tracking, SBOM coverage, remediation time
- **Quality:** Test coverage, mutation score, technical debt
- **OpenTelemetry Collector:** Complete configuration
- **Prometheus Alerts:** 20+ alerting rules

#### 4. Fitness Functions (`fitness-functions/`)
Architecture fitness function framework and examples
- Performance checks (latency, throughput)
- Architecture validation (dependencies, coupling)
- Security validation (secrets, attack surface)
- Quality metrics (complexity, duplication)

#### 5. ML Insights (`ml-insights/`)
Machine learning-powered insights framework
- Anomaly detection (Isolation Forest)
- Predictive failure analysis (Random Forest)
- Test flakiness detection
- Code quality prediction
- Docker and Kubernetes deployment

#### 6. Multi-Cloud (`multi-cloud/`)
Cloud deployment examples and patterns
- AWS, Azure, GCP examples
- Cloud-agnostic patterns
- Multi-region deployments

#### 7. Projects (`projects/`)
Complete example project implementations
- FastAPI microservice example
- Additional examples planned

#### 8. Video Tutorials (`video-tutorials/`)
Complete scripts for video tutorial series (60+ minutes total)
- Getting started (complete)
- Creating services (complete)
- CI/CD setup (complete)
- Security gates (complete)
- Observability setup (complete)
- Jupyter Book usage (complete)

---

## 📁 notebooks/

Executable Jupyter notebooks (source of truth)

```
notebooks/
├── 01_bootstrap.ipynb             # Repo scaffolding and gates
├── 02_security_supply_chain.ipynb # Security scanning and SBOM
├── 03_contracts_and_tests.ipynb   # Contracts and mutation testing
├── 04_observability_slos.ipynb    # OpenTelemetry and SLOs
└── 05_docs_to_book.ipynb          # Jupytext and Jupyter Book
```

**Purpose:** Source notebooks synced to `docs/notebooks/*.md` via Jupytext

**Key Features:**
- Executable code with outputs
- Can be run locally or in Binder
- Tested in CI with nbmake
- Scheduled execution with Papermill
- Git-friendly via Jupytext pairing

**Important:** `.ipynb` files are in `.gitignore`. Only MyST markdown versions are committed.

---

## 📁 runbooks/

Operational procedures and automation guides

```
runbooks/
└── README.md                      # Runbook index and overview
```

**Purpose:** Step-by-step operational procedures

**Planned Runbooks:**
- Template creation runbook
- Deployment procedures
- Incident response runbook
- Agent-oriented automation runbook

---

## 📁 templates/

Cookiecutter templates and supporting templates

```
templates/
├── python-service/                # Python service template
│   ├── cookiecutter.json
│   ├── hooks/
│   │   ├── pre_gen_project.py
│   │   └── post_gen_project.py
│   └── {{cookiecutter.project_slug}}/
├── node-service/                  # Node.js service template
├── react-webapp/                  # React webapp template
├── go-service/                    # Go service template
├── docs-only/                     # Documentation-only template
├── architecture/                  # Architecture templates
│   ├── adr/                       # ADR templates
│   ├── c4/                        # C4 diagram templates
│   └── fitness-functions/         # Fitness function templates
├── automation/                    # Automation templates
│   ├── bots/                      # Bot configurations
│   └── hooks/                     # Git hooks
├── cicd/                          # CI/CD pipeline templates
│   ├── github-actions/
│   └── gitlab-ci/
├── contracts/                     # API contract templates
│   ├── asyncapi/
│   └── openapi/
├── observability/                 # Observability templates
│   ├── otel/                      # OpenTelemetry configs
│   └── slo/                       # SLO definitions
├── platform/                      # Platform templates
│   ├── backstage/                 # Backstage software templates
│   └── policy/                    # Policy-as-code
├── repository/                    # Repository templates
│   └── common/                    # Common repo files
└── security/                      # Security templates
    └── sbom/                      # SBOM generation
```

**Purpose:** Cookiecutter templates for project scaffolding and supporting template files

### Cookiecutter Templates

Production-ready templates with complete CI/CD, security, and quality tooling:

#### 1. Python Service (`python-service/`)
- Modern Python packaging (pyproject.toml)
- Type hints and mypy
- Black, Ruff, pytest
- GitHub Actions CI/CD
- Security scanning (CodeQL, Gitleaks)
- Optional: Jupyter Book docs, SBOM generation

#### 2. Node.js Service (`node-service/`)
- TypeScript configuration
- ESLint, Prettier
- Jest testing
- GitHub Actions CI/CD
- Security scanning

#### 3. React WebApp (`react-webapp/`)
- Vite + React + TypeScript
- Playwright E2E testing
- Storybook component library
- GitHub Actions CI/CD

#### 4. Go Service (`go-service/`)
- Standard Go project layout
- golangci-lint
- Testing and benchmarks
- GitHub Actions CI/CD

#### 5. Docs-Only (`docs-only/`)
- Jupyter Book setup
- MyST markdown
- GitHub Pages deployment

### Supporting Templates

Non-Cookiecutter template files for various purposes:

- **Architecture:** ADRs, C4 diagrams, fitness functions
- **Automation:** Git hooks, bot configs
- **CI/CD:** GitHub Actions, GitLab CI workflows
- **Contracts:** OpenAPI, AsyncAPI specs
- **Observability:** OpenTelemetry, SLO definitions
- **Platform:** Backstage, policy-as-code
- **Repository:** Common files (SECURITY.md, CONTRIBUTING.md)
- **Security:** SBOM generation, scanning configs

---

## 📁 tests/

Test suite for templates and infrastructure

```
tests/
├── README.md                      # Testing documentation
└── test_cookiecutters.py          # Template rendering tests
```

**Purpose:** Automated testing with pytest-cookies

**Test Coverage:**
- Template rendering validation
- Required file generation
- Optional feature toggles
- Invalid input rejection
- Generated project structure

**Run Tests:**
```bash
pytest tests/ -v
```

---

## 🔄 Workflow: How Directories Work Together

### 1. Creating a New Project

```
User runs CLI
    ↓
agentic_canon_cli/ → Interactive wizard
    ↓
templates/ → Cookiecutter renders template
    ↓
Generated project with CI/CD, security, docs
```

### 2. Documentation Workflow

```
Edit notebooks/*.ipynb
    ↓
Save (Jupytext syncs to docs/notebooks/*.md)
    ↓
Commit only .md files
    ↓
CI builds Jupyter Book
    ↓
Deploy to GitHub Pages
```

### 3. Examples and Reference

```
Need example? → examples/
Need template? → templates/
Need procedure? → runbooks/
Need documentation? → docs/
```

---

## 📊 Directory Statistics

| Directory | Files | Purpose | Status |
|-----------|-------|---------|--------|
| Root | ~20 | Core documentation | ✅ Complete |
| agentic_canon_cli | 4 | CLI wizard | ✅ Complete |
| binder | 1 | Cloud notebooks | ✅ Complete |
| docs | ~15 | Jupyter Book | ✅ Complete |
| examples | ~20 | Reference examples | 🚧 ~75% |
| notebooks | 5 | Source notebooks | ✅ Complete |
| runbooks | 1 | Procedures | 📋 Planned |
| templates | ~50+ | Scaffolding | ✅ Complete |
| tests | 2 | Test suite | ✅ Complete |

---

## 🎯 Finding What You Need

### "I want to..."

**...generate a new project**
→ `agentic_canon_cli/` or `templates/`

**...see examples of X**
→ `examples/` (dashboards, pipelines, fitness functions, etc.)

**...understand architecture decisions**
→ `docs/adr/`

**...learn how to use Agentic Canon**
→ `examples/video-tutorials/` or `docs/notebooks/`

**...contribute a template**
→ `examples/community/CONTRIBUTING-TEMPLATES.md`

**...check project status**
→ `TASKS.md`, `SUMMARY.md`, `V110-V200-SUMMARY.md`

**...understand security controls**
→ `SECURITY.md`, `templates/security/`

**...set up monitoring**
→ `examples/dashboards/`

**...implement fitness functions**
→ `examples/fitness-functions/`

**...add ML insights**
→ `examples/ml-insights/`

---

## 🔧 Maintenance Guidelines

### Adding New Content

1. **New Template:** Add to `templates/` with cookiecutter.json and tests
2. **New Example:** Add to appropriate `examples/` subdirectory with README
3. **New Documentation:** Add to `docs/` and update `_toc.yml`
4. **New ADR:** Add to `docs/adr/` following template
5. **New Runbook:** Add to `runbooks/` with step-by-step procedures

### Updating Documentation

- Always update `TASKS.md` when completing tasks
- Update `CHANGELOG.md` for significant changes
- Keep README.md badges and links current
- Maintain consistency across summary documents

### File Naming Conventions

- **Markdown:** `kebab-case.md`
- **Python:** `snake_case.py`
- **Config:** `kebab-case.yaml` or `snake_case.toml`
- **Templates:** `{{cookiecutter.project_slug}}/`

---

## 📚 Related Documentation

- [README.md](README.md) - Project overview and quick start
- [TASKS.md](TASKS.md) - Complete task tracking
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [INDEX.md](INDEX.md) - Complete repository index

---

**Last Updated:** 2025-10-11  
**Maintained By:** Agentic Canon Team  
**Questions?** Open an issue or discussion on GitHub

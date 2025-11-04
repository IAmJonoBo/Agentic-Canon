# Templates Index

## Purpose

This directory contains comprehensive templates for building production-ready software with frontier excellence practices baked in. Templates are organized into two categories:

1. **Cookiecutter Templates** - Complete project scaffolding for new services
2. **Supporting Templates** - Drag-and-drop files for specific capabilities

**📋 Standards Compliance:** See [TEMPLATE_STANDARDS.md](../TEMPLATE_STANDARDS.md) for details on what standards templates must meet versus what can be reasonably omitted. Templates serve as **starting points** and are designed to be customized.

## Navigation

### 📦 Cookiecutter Templates (Full Project Generation)

Generate complete, production-ready projects with all tooling configured:

- **[Python Service](python-service/README.md)** - Modern Python with pytest, type hints, security scanning
- **[Node.js Service](node-service/README.md)** - TypeScript, Vitest, ESLint, comprehensive testing
- **[React WebApp](react-webapp/README.md)** - Vite, TypeScript, Storybook, Playwright E2E
- **[Go Service](go-service/README.md)** - Clean architecture, golangci-lint, table-driven tests
- **[Documentation Site](docs-only/README.md)** - Jupyter Book for beautiful documentation

### 🎯 Supporting Templates (Individual Files)

Pick and choose templates for specific needs:

- **[Architecture](architecture/README.md)** - ADRs, C4 diagrams, fitness functions
- **[Automation](automation/README.md)** - Git hooks, Renovate dependency management
- **[CI/CD](cicd/README.md)** - GitHub Actions, GitLab CI pipelines
- **[Contracts](contracts/README.md)** - OpenAPI, AsyncAPI specifications
- **[Observability](observability/README.md)** - OpenTelemetry, SLO definitions
- **[Platform](platform/README.md)** - Backstage templates, OPA policies
- **[Repository](repository/README.md)** - SECURITY.md, CONTRIBUTING.md, CODEOWNERS
- **[Security](security/README.md)** - SBOM, signing, accessibility, performance budgets

## Quick Start

### Option 1: Generate Complete Project (Recommended)

```bash
# Install Cookiecutter
pip install cookiecutter

# Generate a new project
cookiecutter templates/python-service
# or
cookiecutter templates/node-service
# or
cookiecutter templates/react-webapp
# or
cookiecutter templates/go-service
# or
cookiecutter templates/docs-only

# Or use the n00-frontiers CLI
pip install -e .
agentic-canon init
```

### Option 2: Add Individual Templates

```bash
# Add architecture documentation
cp -r templates/architecture/adr/ docs/adr/
cp -r templates/architecture/c4/ docs/architecture/

# Add automation
cp templates/automation/hooks/pre-commit .git/hooks/
cp templates/automation/bots/renovate.json .

# Add CI/CD
cp templates/cicd/github-actions/complete-pipeline.yml .github/workflows/ci.yml

# Add observability
cp templates/observability/otel/collector-config.yaml otel-config.yaml
cp templates/observability/slo/slo-definition.yaml slo-config.yaml

# Add repository governance
cp templates/repository/common/SECURITY.md .
cp templates/repository/common/CONTRIBUTING.md .
cp templates/repository/common/CODEOWNERS .github/
```

## Template Categories

### CI/CD Pipelines (`cicd/`)

Stack-agnostic CI/CD configurations implementing comprehensive quality gates.

- **GitHub Actions** (`cicd/github-actions/`)
  - Complete workflow with all gates
  - Modular job examples
  - Reusable workflows
- **GitLab CI** (`cicd/gitlab-ci/`)
  - Pipeline configuration
  - Stage templates
  - Policy examples

- **Azure Pipelines** (`cicd/azure-pipelines/`)
  - YAML pipeline templates
  - Stage definitions
  - Variable groups

### Security (`security/`)

Security scanning and supply chain hardening templates.

- **SAST** (`security/sast/`)
  - CodeQL configuration
  - Semgrep rules
  - Custom rule examples

- **DAST** (`security/dast/`)
  - OWASP ZAP baseline
  - Dynamic scanning configs
  - API security tests

- **Secrets** (`security/secrets/`)
  - Gitleaks configuration
  - TruffleHog setup
  - Secret rotation policies

- **SBOM** (`security/sbom/`)
  - CycloneDX generation
  - SPDX generation
  - SBOM diffing

- **SLSA** (`security/slsa/`)
  - Provenance generation
  - in-toto attestations
  - Verification policies

- **Signing** (`security/signing/`)
  - Cosign configuration
  - Keyless signing
  - Verification policies

### Contracts (`contracts/`)

API contract definitions and testing.

- **OpenAPI** (`contracts/openapi/`)
  - OpenAPI 3.1 templates
  - Specification examples
  - Generator configs

- **AsyncAPI** (`contracts/asyncapi/`)
  - AsyncAPI templates
  - Event schemas
  - Message examples

- **Tests** (`contracts/tests/`)
  - Pact contract tests
  - Provider verification
  - Consumer tests

### Architecture (`architecture/`)

Architecture documentation and governance.

- **ADR** (`architecture/adr/`)
  - ADR templates
  - Example decisions
  - Status tracking

- **C4** (`architecture/c4/`)
  - Context diagrams
  - Container diagrams
  - Component diagrams
  - Code diagrams

- **Fitness Functions** (`architecture/fitness-functions/`)
  - Coupling checks
  - Performance assertions
  - Dependency rules

### Platform (`platform/`)

Internal developer platform templates.

- **Backstage** (`platform/backstage/`)
  - Catalog entities
  - Software templates
  - TechDocs configs

- **GitOps** (`platform/gitops/`)
  - Argo CD applications
  - Flux configs
  - Progressive delivery

- **Policy** (`platform/policy/`)
  - OPA policies
  - Kyverno policies
  - Admission controls

### Observability (`observability/`)

Monitoring, logging, and SLO definitions.

- **OpenTelemetry** (`observability/otel/`)
  - SDK configuration
  - Collector config
  - Auto-instrumentation

- **SLO** (`observability/slo/`)
  - SLO definitions
  - Error budgets
  - Alert rules

- **Dashboards** (`observability/dashboards/`)
  - Grafana dashboards
  - Prometheus rules
  - Log queries

### Repository (`repository/`)

Repository setup and governance files.

- **GitHub** (`repository/github/`)
  - Issue templates
  - PR templates
  - Branch protection

- **GitLab** (`repository/gitlab/`)
  - Merge request templates
  - Issue templates
  - Pipeline configs

- **Common** (`repository/common/`)
  - SECURITY.md
  - CONTRIBUTING.md
  - CODEOWNERS
  - .gitignore

### Automation (`automation/`)

Automation hooks and remediation scripts.

- **Hooks** (`automation/hooks/`)
  - Pre-commit hooks
  - Pre-push hooks
  - Commit message validation

- **Autofix** (`automation/autofix/`)
  - Dependency update scripts
  - Linting auto-fixes
  - Test quarantine

- **Bots** (`automation/bots/`)
  - Renovate config
  - Dependabot config
  - Custom bot rules

## Quick Start

### For New Projects

```bash
# Copy all essential templates
cp -r templates/repository/common/* .
cp -r templates/cicd/github-actions/.github .
cp -r templates/security/secrets/gitleaks.toml .
```

### For Existing Projects

```bash
# Add security scanning
cp templates/cicd/github-actions/security-scan.yml .github/workflows/

# Add SBOM generation
cp templates/security/sbom/cyclonedx-action.yml .github/workflows/
```

## Quick Reference

### For New Projects

**Generate a complete project:**

```bash
cookiecutter templates/python-service    # Python API service
cookiecutter templates/node-service      # Node.js/TypeScript service
cookiecutter templates/react-webapp      # React web application
cookiecutter templates/go-service        # Go microservice
cookiecutter templates/docs-only         # Documentation site
```

**Or use the interactive CLI:**

```bash
agentic-canon init
```

### For Existing Projects

**Add quality gates:**

```bash
# CI/CD pipeline
cp templates/cicd/github-actions/complete-pipeline.yml .github/workflows/ci.yml

# Pre-commit hooks
cp templates/automation/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Security scanning
cp templates/security/sbom/cyclonedx-workflow.yml .github/workflows/
cp templates/security/signing/cosign-workflow.yml .github/workflows/
```

**Add documentation:**

```bash
# Repository governance
cp templates/repository/common/SECURITY.md .
cp templates/repository/common/CONTRIBUTING.md .
cp templates/repository/common/CODEOWNERS .github/

# Architecture decisions
cp -r templates/architecture/adr/ docs/adr/
cp -r templates/architecture/c4/ docs/architecture/
```

**Add observability:**

```bash
# OpenTelemetry
cp templates/observability/otel/collector-config.yaml otel-config.yaml

# SLO definitions
cp templates/observability/slo/slo-definition.yaml slo-config.yaml
```

### Common Workflows

**Setting up a new Python service:**

```bash
cookiecutter templates/python-service
cd my-service
pip install -e .[dev]
pre-commit install
pytest
```

**Setting up a new React app:**

```bash
cookiecutter templates/react-webapp
cd my-app
npm install
npm run dev
```

**Adding security scanning to existing project:**

```bash
mkdir -p .github/workflows
cp templates/cicd/github-actions/security-scan.yml .github/workflows/
git add .github/workflows/security-scan.yml
git commit -m "ci: add security scanning"
git push
```

## Directory Structure

```
templates/
├── README.md (this file)
│
├── Cookiecutter Templates (Full Projects)
├── python-service/          # Python service with pytest, mypy, black
├── node-service/            # Node.js/TypeScript with Vitest, ESLint
├── react-webapp/            # React + Vite + Storybook + Playwright
├── go-service/              # Go service with golangci-lint
├── docs-only/               # Jupyter Book documentation
│
└── Supporting Templates (Individual Files)
    ├── architecture/        # ADR, C4, fitness functions
    ├── automation/          # Git hooks, Renovate bot
    ├── cicd/               # GitHub Actions, GitLab CI
    │   ├── github-actions/
    │   └── gitlab-ci/
    ├── contracts/          # OpenAPI, AsyncAPI
    ├── observability/      # OpenTelemetry, SLOs
    ├── platform/           # Backstage, OPA policies
    ├── repository/         # SECURITY.md, CONTRIBUTING.md
    └── security/           # SBOM, signing, accessibility
```

## Template Features Matrix

| Template       | Testing               | Security  | Docs            | CI/CD         | Observability |
| -------------- | --------------------- | --------- | --------------- | ------------- | ------------- |
| Python Service | ✅ pytest             | ✅ CodeQL | ✅ Jupyter Book | ✅ GH Actions | ✅ OTel       |
| Node Service   | ✅ Vitest             | ✅ CodeQL | ✅ JSDoc        | ✅ GH Actions | ✅ OTel       |
| React WebApp   | ✅ Vitest, Playwright | ✅ CodeQL | ✅ Storybook    | ✅ GH Actions | ✅ Lighthouse |
| Go Service     | ✅ table-driven       | ✅ CodeQL | ✅ godoc        | ✅ GH Actions | ✅ OTel       |
| Docs-Only      | ✅ link check         | N/A       | ✅ Jupyter Book | ✅ GH Actions | N/A           |

## Validation

Each template includes:

- Inline comments explaining configuration
- Validation commands to verify setup
- Links to relevant standards/documentation
- Example outputs

## Standards Compliance

All templates implement:

- ✅ NIST SSDF v1.1
- ✅ OWASP SAMM Level 2
- ✅ SLSA Level 3
- ✅ ISO/IEC 25010
- ✅ WCAG 2.2 AA (where applicable)

## Customization Guide

### Placeholders

Templates use `{{ VARIABLE }}` syntax for customization:

```yaml
name: { { PROJECT_NAME } }
owner: { { TEAM_NAME } }
threshold: { { COVERAGE_THRESHOLD } }
```

### Environment Variables

Reference environment-specific values:

```yaml
url: ${{ secrets.API_URL }}
token: ${{ secrets.API_TOKEN }}
```

## Support

For questions or issues:

1. Check BIBLE.md for conceptual guidance
2. Review template comments
3. Consult referenced standards
4. Open an issue with specific questions

## Contributing

To add new templates:

1. Follow existing structure and naming
2. Include comprehensive comments
3. Add validation commands
4. Update this index
5. Reference relevant standards

---

_Part of Frontier Software Excellence Copilot_

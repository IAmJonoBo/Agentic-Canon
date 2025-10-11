# Templates Index

## Purpose
This directory contains drag-and-drop, stack-agnostic templates for implementing frontier software excellence practices.

## Usage
1. Copy the relevant template(s) to your project
2. Customize placeholders (marked with `{{ }}`)
3. Validate with provided verification commands
4. Commit and enable in your CI/CD

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
name: {{ PROJECT_NAME }}
owner: {{ TEAM_NAME }}
threshold: {{ COVERAGE_THRESHOLD }}
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

*Part of Frontier Software Excellence Copilot*

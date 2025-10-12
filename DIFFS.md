# Agentic Canon - Version Differences

This document tracks major differences and improvements between versions of the Agentic Canon framework.

## Version 1.1.0 vs 1.0.0

### New Features

#### Azure Pipelines Support
- Complete Azure DevOps pipeline templates for all service types
- Azure-specific security scanning and SBOM generation
- Documentation and migration guides

#### Enhanced Dashboards
- **DORA Metrics Dashboard** (`dora-metrics.json`) - Production-ready Grafana dashboard
- **SPACE/DevEx Metrics Dashboard** (`space-devex-metrics.json`) - Developer experience tracking
- **Quality Metrics Dashboard** (`quality-metrics.json`) - Code quality and testing metrics
- **Security Metrics Dashboard** (`security-metrics.json`) - Security posture visualization

#### Interactive CLI Wizard
- `agentic-canon init` command for guided project creation
- Template selection with feature toggles
- CI/CD provider selection (GitHub Actions, Azure Pipelines, GitLab CI)
- Cloud provider configuration
- License selection

#### Additional Security Workflows
- **License Compliance** - SPDX validation and license compatibility checks
- **Container Scanning** - Trivy and Grype for container image security
- **IaC Security** - Checkov and tfsec for infrastructure-as-code
- **Performance Budgets** - Lighthouse CI and bundle size enforcement
- **Accessibility Testing** - WCAG 2.2 AA compliance with axe-core and pa11y

#### Documentation Improvements
- Video tutorial scripts (6 tutorials, ~65 minutes of content)
- Architecture Decision Records (ADRs) for security, dependencies, and secrets
- Comprehensive example project documentation
- Troubleshooting guides

### Improvements

#### Template Quality
- Comprehensive input validation with detailed error messages
- Consistent validation across all templates
- Enhanced sanity checking in hooks

#### Security Hardening
- Expanded SAST coverage (CodeQL + Semgrep)
- Multiple secret scanning tools (Gitleaks + TruffleHog)
- Artifact signing with Sigstore/Cosign
- SLSA Level 3 provenance attestation

#### Standards Compliance
- **NIST SSDF v1.1** - Complete framework coverage
- **OWASP SAMM/ASVS** - Level 2 compliance
- **SLSA Level 3** - Supply chain security
- **WCAG 2.2 AA** - Web accessibility
- **ISO/IEC 25010** - Quality model

### Breaking Changes

**None** - Version 1.1.0 is fully backward compatible with 1.0.0

### Migration Path

Existing projects can adopt 1.1.0 features incrementally:

1. **Update workflows** - Copy new CI/CD workflows from templates
2. **Add dashboards** - Import Grafana dashboards from `examples/dashboards/`
3. **Enhanced validation** - Update cookiecutter hooks with new validation logic
4. **Security workflows** - Add optional security scanning workflows

## Version 2.0.0 (Planned) vs 1.1.0

### Planned Features

#### Multi-Cloud Support
- AWS, Azure, and GCP-specific templates
- Terraform/OpenTofu modules
- Cloud-agnostic patterns with Pulumi
- Multi-region deployment examples

#### Advanced Fitness Functions
- Automated architecture quality checks
- Performance regression detection
- Security posture monitoring
- Technical debt tracking

#### ML-Powered Insights
- Anomaly detection in metrics
- Predictive failure analysis
- Test flakiness detection
- Code quality prediction

#### Community Templates
- Template marketplace/gallery
- Rating and review system
- Template certification program
- Automated updates via Cruft

#### Full Automation
- Auto-remediation workflows
- Self-healing infrastructure
- Intelligent deployment scheduling
- Chaos engineering automation

### Breaking Changes (Planned)

**None currently planned** - Maintaining backward compatibility is a priority

## Version History Summary

| Version | Release Date | Status | Templates | Workflows | Standards |
|---------|-------------|--------|-----------|-----------|-----------|
| 1.0.0 | 2025-10-01 | ✅ Complete | 5 primary | 15+ | 4 major |
| 1.1.0 | 2025-10-12 | ✅ ~98% | 5 primary + 8 categories | 25+ | 7 major |
| 2.0.0 | TBD | 🚧 Planning | TBD | TBD | 7+ major |

## Feature Comparison Matrix

| Feature | v1.0.0 | v1.1.0 | v2.0.0 (Planned) |
|---------|--------|--------|------------------|
| Python Service | ✅ | ✅ | ✅ |
| Node.js Service | ✅ | ✅ | ✅ |
| React WebApp | ✅ | ✅ | ✅ |
| Go Service | ✅ | ✅ | ✅ |
| Docs-Only | ✅ | ✅ | ✅ |
| GitHub Actions | ✅ | ✅ | ✅ |
| Azure Pipelines | ❌ | ✅ | ✅ |
| GitLab CI | ❌ | ✅ | ✅ |
| CLI Wizard | ❌ | ✅ | ✅ |
| Grafana Dashboards | ❌ | ✅ | ✅ |
| License Compliance | ❌ | ✅ | ✅ |
| Container Scanning | ❌ | ✅ | ✅ |
| IaC Security | ❌ | ✅ | ✅ |
| Accessibility Tests | ❌ | ✅ | ✅ |
| Performance Budgets | ❌ | ✅ | ✅ |
| Multi-Cloud | ❌ | 🚧 30% | ✅ |
| Fitness Functions | ❌ | 🚧 70% | ✅ |
| ML Insights | ❌ | 🚧 60% | ✅ |
| Community Templates | ❌ | 🚧 50% | ✅ |

## Standards Coverage Evolution

| Standard | v1.0.0 | v1.1.0 | v2.0.0 (Planned) |
|----------|--------|--------|------------------|
| NIST SSDF v1.1 | 🟡 Partial | ✅ Complete | ✅ Complete |
| OWASP SAMM | 🟡 Level 1 | ✅ Level 2 | ✅ Level 3 |
| OWASP ASVS | 🟡 L1 | ✅ L2 | ✅ L3 |
| SLSA | 🟡 Level 1 | ✅ Level 3 | ✅ Level 3+ |
| WCAG 2.2 | ❌ None | ✅ AA | ✅ AAA |
| ISO/IEC 25010 | 🟡 Partial | ✅ Complete | ✅ Complete |
| OpenSSF Scorecard | 🟡 5/10 | ✅ 8/10 | ✅ 10/10 |

## Upgrade Recommendations

### From 1.0.0 to 1.1.0

**Immediate (High Impact)**:
1. Add enhanced validation to template hooks
2. Implement license compliance checks
3. Add container and IaC security scanning
4. Configure performance budgets

**Near-term (Medium Impact)**:
5. Import Grafana dashboards for metrics
6. Add accessibility testing for web apps
7. Update CI/CD workflows with new gates
8. Configure artifact signing

**Optional (Lower Priority)**:
9. Switch to CLI wizard for new projects
10. Add Azure Pipelines support
11. Implement video tutorials
12. Add ADRs for decisions

### Preparing for 2.0.0

**Infrastructure**:
- Review cloud provider strategy
- Plan multi-cloud deployment approach
- Evaluate IaC tools (Terraform vs Pulumi)

**Automation**:
- Identify candidates for fitness functions
- Collect metrics for ML training
- Define auto-remediation policies

**Community**:
- Contribute domain-specific templates
- Participate in template reviews
- Share success stories and patterns

## Deprecation Notices

**None** - No features are deprecated in current versions.

Future deprecations will be announced at least 6 months in advance with migration guides provided.

## Support Policy

- **v1.0.0**: Security fixes only (until v2.0.0 release)
- **v1.1.0**: Full support (current)
- **v2.0.0**: Planning phase

---

**Last Updated**: 2025-10-12  
**Document Version**: 1.0  
**Maintained By**: Agentic Canon Team

# ADR-006: Security Scanning Strategy

## Status

Accepted

## Context

Modern software development requires comprehensive security scanning to detect vulnerabilities early in the development lifecycle. We need a strategy that provides:

1. **Comprehensive Coverage**: Multiple types of security issues (code vulnerabilities, secrets, dependencies, containers, IaC)
2. **Defense in Depth**: Multiple tools for each category to reduce false negatives
3. **Developer Experience**: Fast feedback without overwhelming developers
4. **Compliance**: Meet industry standards (NIST SSDF, OWASP SAMM, SLSA)
5. **Automation**: Integrated into CI/CD without manual intervention
6. **Actionability**: Clear, prioritized findings with remediation guidance

Several approaches were considered:

- Single comprehensive tool (e.g., Snyk, Veracode)
- Open-source only approach
- Manual security reviews only
- Minimal scanning (just dependency checks)
- Multi-layered approach with specialized tools

## Decision

We will implement a **multi-layered security scanning strategy** using specialized open-source tools for each security domain, integrated into GitHub Actions workflows.

### Security Scanning Layers

#### 1. Static Application Security Testing (SAST)

- **Primary**: GitHub CodeQL (semantic analysis)
- **Secondary**: Semgrep (pattern-based rules)
- **Rationale**: CodeQL provides deep semantic understanding; Semgrep adds fast pattern-matching and custom rules

#### 2. Secret Scanning

- **Primary**: TruffleHog (entropy-based detection)
- **Secondary**: Gitleaks (pattern-based detection)
- **Rationale**: Dual approach catches both high-entropy secrets and known patterns

#### 3. Dependency Scanning

- **Language-Specific Tools**:
  - Python: `pip audit`, CodeQL
  - Node.js: `npm audit`, GitHub Dependency Review
  - Go: `govulncheck`
- **Rationale**: Native tools understand ecosystem-specific nuances

#### 4. Container Security

- **Primary**: Trivy (comprehensive vulnerability database)
- **Secondary**: Grype (Anchore's scanner)
- **Rationale**: Different vulnerability databases provide complementary coverage

#### 5. Infrastructure as Code (IaC)

- **Multi-Tool Approach**: Checkov, tfsec, Terrascan, KICS
- **Rationale**: Each tool has unique policy sets; combined coverage is comprehensive

#### 6. Supply Chain Security

- **SBOM Generation**: CycloneDX
- **Artifact Signing**: Sigstore/Cosign
- **Provenance**: SLSA attestation
- **Rationale**: Transparency and verification for the software supply chain

#### 7. License Compliance

- **Tools**: pip-licenses, license-checker, go-licenses, FOSSA
- **Rationale**: Automated license compliance reduces legal risk

## Implementation

### Workflow Integration

All security scans are implemented as GitHub Actions workflows:

```
.github/workflows/
├── security.yml          # Core security (SAST, secrets, dependencies)
├── container-scan.yml    # Container vulnerability scanning
├── iac-security.yml      # IaC policy enforcement
├── license-check.yml     # License compliance
└── sign-artifacts.yml    # Artifact signing and provenance
```

### Execution Strategy

1. **On Every PR**:
   - SAST (CodeQL, Semgrep)
   - Secret scanning (TruffleHog, Gitleaks)
   - Dependency review

2. **On Main Branch Push**:
   - All PR checks
   - SBOM generation
   - Container scanning (if applicable)

3. **Weekly Schedule**:
   - Full security scan suite
   - License compliance check
   - IaC security scan

4. **On Release**:
   - Artifact signing with Cosign
   - SLSA provenance generation
   - Final security validation

### Branch Protection

Required status checks before merge:

- `codeql` (SAST)
- `semgrep` (SAST)
- `secret-scan` (Secret detection)
- `dependency-review` (Dependency vulnerabilities)

### Performance Optimization

- **Conditional Execution**: Run IaC scans only when IaC files change
- **Caching**: Cache dependencies to speed up scans
- **Parallelization**: Run independent scans concurrently
- **Smart Scheduling**: Space out heavy scans to avoid resource contention

## Consequences

### Positive

- **Comprehensive Security**: Multiple layers of defense catch different issue types
- **Early Detection**: Issues found in PRs, not production
- **Compliance**: Meets NIST SSDF, OWASP SAMM Level 2, SLSA Level 3
- **Open Source**: No vendor lock-in, transparent scanning logic
- **GitHub Integration**: Native integration with GitHub Security tab
- **Developer Friendly**: Clear findings with remediation guidance
- **Supply Chain Security**: SBOM and signing provide transparency

### Negative

- **Multiple Tools**: Requires maintaining multiple tool configurations
- **False Positives**: Some tools generate noise that needs triaging
- **CI Time**: Security scans add time to CI/CD pipeline
- **Learning Curve**: Developers need to understand different tools
- **Alert Fatigue**: Too many findings can overwhelm teams

### Mitigation

- **Tuning**: Regularly tune scanners to reduce false positives
- **Suppressions**: Document and suppress known false positives
- **Prioritization**: Focus on high/critical findings first
- **Documentation**: Clear guidelines on interpreting and remediating findings
- **Gradual Rollout**: Introduce tools incrementally, not all at once
- **Training**: Provide security training for development teams

## Compliance Mapping

### NIST SSDF v1.1

- **PO.3**: Security requirements defined
- **PS.1**: Secure design practices
- **PS.2**: Code review
- **PS.3**: Automated security testing
- **PW.1**: Secure build process
- **PW.4**: Software supply chain security
- **RV.1**: Vulnerability identification

### OWASP SAMM Level 2

- **Security Testing**: Automated security scanning
- **Security Architecture**: Defense in depth
- **Secure Build**: Integrity verification

### SLSA Level 3

- **Build as Code**: Reproducible builds
- **Provenance**: Build metadata attestation
- **Isolation**: Build environment integrity

## Alternatives Considered

### Single Commercial Tool (e.g., Snyk, Veracode)

- **Pros**: Unified interface, enterprise support
- **Cons**: Vendor lock-in, cost, limited customization
- **Rejected**: Cost and flexibility concerns

### Minimal Scanning

- **Pros**: Fast CI, simple setup
- **Cons**: Misses many vulnerability types
- **Rejected**: Insufficient security coverage

### Manual Security Reviews Only

- **Pros**: Human expertise, context-aware
- **Cons**: Slow, doesn't scale, inconsistent
- **Rejected**: Cannot scale to all commits

## Related Decisions

- [ADR-007: Secret Management Approach](ADR-007-secret-management.md)
- [ADR-008: Dependency Management and Updates](ADR-008-dependency-management.md)

## References

- [NIST SSDF v1.1](https://csrc.nist.gov/Projects/ssdf)
- [OWASP SAMM](https://owaspsamm.org/)
- [SLSA Framework](https://slsa.dev/)
- [GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning)
- [Sigstore Documentation](https://docs.sigstore.dev/)

---

**Date**: 2025-10-11  
**Author**: Agentic Canon Security Team  
**Status**: Accepted  
**Version**: 1.0

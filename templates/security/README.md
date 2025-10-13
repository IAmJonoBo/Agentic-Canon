# Security Templates

This directory contains comprehensive security scanning and compliance workflows for the Agentic Canon framework.

## Overview

These templates implement a defense-in-depth security approach with multiple layers:

1. **Static Application Security Testing (SAST)**
2. **Secret Scanning**
3. **Dependency Scanning**
4. **Container Security**
5. **Infrastructure as Code (IaC) Security**
6. **License Compliance**
7. **Artifact Signing and Provenance**

## Directory Structure

```
security/
├── README.md                           # This file
├── sbom/
│   └── cyclonedx-workflow.yml         # SBOM generation workflow
├── signing/
│   └── cosign-workflow.yml            # Artifact signing with Sigstore/Cosign
├── container-scanning/
│   └── trivy-workflow.yml             # Container vulnerability scanning
├── iac-scanning/
│   └── iac-security-workflow.yml      # IaC security scanning
├── license-compliance/
│   └── license-check-workflow.yml     # License compliance checking
├── performance-budgets/
│   ├── performance-budget-workflow.yml # Performance budget enforcement
│   ├── lighthouse-budget.example.json # Lighthouse budget configuration
│   └── size-limit.example.js          # Bundle size limits
└── accessibility/
    ├── accessibility-workflow.yml      # Accessibility testing
    ├── lighthouserc.example.json      # Lighthouse config for a11y
    └── pa11yci.example.json           # pa11y-ci configuration
```

## Security Workflows

### 1. SAST Scanning

All service templates include comprehensive SAST scanning:

- **CodeQL**: GitHub's semantic code analysis
- **Semgrep**: Pattern-based security scanning

Configuration in each service template's `.github/workflows/security.yml`

### 2. Secret Scanning

Multiple tools for comprehensive secret detection:

- **TruffleHog**: Entropy-based secret scanning
- **Gitleaks**: Pattern-based secret detection

Both tools run on every commit to prevent credential leaks.

### 3. Dependency Scanning

Language-specific dependency vulnerability scanning:

- **Python**: `pip audit`, CodeQL
- **Node.js**: `npm audit`, dependency-review-action
- **Go**: `govulncheck`

### 4. Container Security

Comprehensive container image scanning with multiple tools:

- **Trivy**: Aqua Security's vulnerability scanner
- **Grype**: Anchore's vulnerability scanner

Features:

- Image vulnerability scanning
- Filesystem scanning
- SARIF output for GitHub Security tab integration
- Configurable severity levels

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/container-scanning/trivy-workflow.yml .github/workflows/
```

### 5. Infrastructure as Code Security

Multi-tool IaC security scanning:

- **Checkov**: Bridgecrew's policy-as-code scanner
- **tfsec**: Terraform security scanner
- **Terrascan**: Tenable's IaC scanner
- **KICS**: Checkmarx's infrastructure scanner

Supports:

- Terraform
- CloudFormation
- Kubernetes manifests
- Docker files
- Helm charts
- Azure ARM templates

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/iac-scanning/iac-security-workflow.yml .github/workflows/
```

### 6. License Compliance

Automated license compliance checking:

- **Python**: `pip-licenses`
- **Node.js**: `license-checker`
- **Go**: `go-licenses`
- **FOSSA**: Universal license scanning (requires API key)

Features:

- License report generation (JSON, Markdown, CSV)
- Forbidden license detection
- License header validation
- Third-party license collection

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/license-compliance/license-check-workflow.yml .github/workflows/
```

### 7. Artifact Signing and SLSA Provenance

Supply chain security with Sigstore/Cosign:

- **Cosign**: Keyless artifact signing
- **SLSA Provenance**: Build provenance attestation

Features:

- Keyless signing with Sigstore
- Automatic signature verification
- SLSA Level 3 provenance generation
- SHA256 checksums

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/signing/cosign-workflow.yml .github/workflows/
```

**Verification:**

```bash
# Verify a signed artifact
cosign verify-blob \
  --bundle artifact.tar.gz.cosign.bundle \
  artifact.tar.gz
```

### 8. Performance Budget Enforcement

Automated performance monitoring and budget enforcement:

- **Lighthouse CI**: Core Web Vitals and performance scores
- **Bundle size**: JavaScript/CSS bundle size limits
- **API performance**: Response time budgets
- **Memory budgets**: Memory usage limits

Features:

- Core Web Vitals tracking (LCP, FID, CLS, FCP, TTFB)
- Bundle size limits enforcement
- API response time monitoring
- Database query performance tracking
- Memory usage monitoring

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/performance-budgets/performance-budget-workflow.yml .github/workflows/

# Configure budgets
cp templates/security/performance-budgets/lighthouse-budget.example.json lighthouse-budget.json
cp templates/security/performance-budgets/size-limit.example.js .size-limit.js
```

**Budget Example:**

```json
{
  "timings": [
    {
      "metric": "first-contentful-paint",
      "budget": 1500
    },
    {
      "metric": "largest-contentful-paint",
      "budget": 2500
    }
  ]
}
```

### 9. Accessibility Testing

Comprehensive accessibility testing to ensure WCAG 2.2 compliance:

- **axe-core**: Automated accessibility testing
- **pa11y**: Accessibility testing framework
- **Lighthouse**: Accessibility audit
- **WAVE**: WebAIM's accessibility checker

Features:

- WCAG 2.2 Level AA/AAA compliance
- Color contrast validation
- Keyboard navigation testing
- Screen reader compatibility
- HTML validation
- ARIA attribute verification

**Usage:**

```yaml
# Add to .github/workflows/
cp templates/security/accessibility/accessibility-workflow.yml .github/workflows/

# Configure tools
cp templates/security/accessibility/lighthouserc.example.json .lighthouserc.json
cp templates/security/accessibility/pa11yci.example.json .pa11yci.json
```

**Standards:**

- WCAG 2.2 Level AA (minimum)
- WCAG 2.2 Level AAA (recommended)
- Section 508 compliance
- ADA compliance

## Service Template Integration

Each service template includes a comprehensive `security.yml` workflow:

### Python Service

```yaml
jobs:
  - codeql # GitHub CodeQL SAST
  - semgrep # Semgrep SAST
  - secrets # TruffleHog + Gitleaks
  - dependency-review
  - sbom # CycloneDX SBOM generation
```

### Node.js Service

```yaml
jobs:
  - dependency-scan # npm audit
  - codeql # JavaScript/TypeScript SAST
  - semgrep # JavaScript/TypeScript patterns
  - secret-scan # TruffleHog + Gitleaks
```

### React WebApp

```yaml
jobs:
  - dependency-scan # npm audit
  - codeql # JavaScript/TypeScript SAST
  - semgrep # React-specific patterns
  - secret-scan # TruffleHog + Gitleaks
```

### Go Service

```yaml
jobs:
  - dependency-scan # govulncheck
  - codeql # Go SAST
  - semgrep # Go patterns
  - secret-scan # TruffleHog + Gitleaks
```

## Security Standards Compliance

These templates help achieve compliance with:

- ✅ **NIST SSDF v1.1**: Secure Software Development Framework
- ✅ **OWASP SAMM Level 2**: Software Assurance Maturity Model
- ✅ **SLSA Level 3**: Supply-chain Levels for Software Artifacts
- ✅ **OWASP ASVS**: Application Security Verification Standard
- ✅ **CWE Top 25**: Common Weakness Enumeration

## GitHub Security Features Integration

All workflows integrate with GitHub's security features:

- **Security Tab**: View all findings in one place
- **Code Scanning Alerts**: Track and remediate vulnerabilities
- **Secret Scanning**: Automatic secret detection
- **Dependabot**: Automated dependency updates
- **SARIF Upload**: Unified security reporting format

## Configuration

### Branch Protection Rules

Require security checks to pass before merging:

1. Go to **Settings** → **Branches**
2. Add branch protection rule for `main`
3. Enable "Require status checks to pass"
4. Select security jobs:
   - `codeql`
   - `semgrep`
   - `secret-scan`
   - `dependency-review`

### Secret Management

Required secrets for enhanced features:

- `FOSSA_API_KEY` - For FOSSA license scanning (optional)
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

## Best Practices

1. **Run security scans on every PR** - Catch issues early
2. **Schedule weekly scans** - Detect new vulnerabilities in dependencies
3. **Review security alerts promptly** - Keep your security tab clean
4. **Enable Dependabot** - Automated dependency updates
5. **Sign your releases** - Build trust with users
6. **Generate SBOMs** - Track your software supply chain
7. **Monitor false positives** - Tune scanners to reduce noise

## Performance Considerations

Security scans can be resource-intensive. Optimize with:

- **Conditional execution**: Only run IaC scans when IaC files change
- **Matrix strategies**: Run language-specific scans only for relevant projects
- **Caching**: Cache dependencies to speed up scans
- **Soft failures**: Use `continue-on-error: true` for non-critical scans

## Troubleshooting

### False Positives

1. Review the finding in GitHub Security tab
2. If confirmed false positive, dismiss with explanation
3. Consider adding suppressions:
   - CodeQL: `.github/codeql/codeql-config.yml`
   - Semgrep: `.semgrepignore`
   - Trivy: `.trivyignore`

### Rate Limits

If you hit GitHub API rate limits:

- Use `GITHUB_TOKEN` for authenticated requests
- Space out scheduled scans
- Consider GitHub Enterprise for higher limits

### Slow Scans

Optimize scan performance:

- Use `--skip-dirs` to exclude large directories
- Enable caching for dependencies
- Run heavyweight scans only on schedule, not on PR

## Additional Resources

- [GitHub Code Scanning](https://docs.github.com/en/code-security/code-scanning)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [SLSA Framework](https://slsa.dev/)
- [OWASP SAMM](https://owaspsamm.org/)
- [NIST SSDF](https://csrc.nist.gov/Projects/ssdf)

## Related Documentation

- [Security Policy](../../templates/repository/common/SECURITY.md)
- [Video Tutorial: Security Gates](../../examples/video-tutorials/04-security-gates.md)
- [Notebook: Security & Supply Chain](../../docs/notebooks/02_security_supply_chain.md)

---

**Last Updated**: 2025-10-11  
**Version**: 2.0.0  
**Maintained by**: Agentic Canon Security Team

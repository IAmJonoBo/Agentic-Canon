# Security Policy

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Agentic Canon, please follow these steps:

### 1. DO NOT create a public issue

Security vulnerabilities should be reported privately to maintain security for all users.

### 2. Contact Information

- **Email**: security@jonathanboardman.com
- **Response Time**: Within 48 hours
- **GitHub Security Advisories**: [Report a vulnerability](https://github.com/IAmJonoBo/Agentic-Canon/security/advisories/new) (preferred)

### 3. What to Include

Please provide:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact and severity assessment
- Affected versions or components
- Suggested fix (if any)
- Your contact information for follow-up

### 4. Response Process

1. **Acknowledgment** (within 48 hours): We'll confirm receipt of your report
2. **Investigation** (5-10 days): We'll assess the issue and verify the vulnerability
3. **Resolution** (varies by severity): We'll develop, test, and validate a fix
4. **Disclosure** (coordinated): Public disclosure after patch release and user notification

## Security Standards

Agentic Canon follows frontier software excellence practices:

### Supply Chain Security
- **SLSA Level 3**: Templates include signed provenance generation
- **SBOM**: Software Bill of Materials generation in all templates
- **Signing**: Artifact signing with Sigstore/Cosign examples
- **Verification**: Automated signature verification workflows

### Development Security
- **SAST**: Static analysis with CodeQL and Semgrep configurations
- **Secret Scanning**: Gitleaks and TruffleHog in all templates
- **Dependency Scanning**: Automated vulnerability detection via Dependabot and Renovate
- **License Scanning**: Compliance checking in CI/CD pipelines

### Template Security
- **Security by Default**: All templates include security scanning
- **Least Privilege**: RBAC and principle of least privilege in examples
- **Secure Defaults**: Templates use secure configuration defaults
- **Security Gates**: Quality gates prevent insecure code from merging

## Compliance

### Standards Compliance
- ✅ **NIST SSDF v1.1**: Secure Software Development Framework
- ✅ **OWASP SAMM Level 2**: Software Assurance Maturity Model
- ✅ **OWASP ASVS Level 2/3**: Application Security Verification Standard
- ✅ **CWE Top 25**: Coverage for most dangerous software weaknesses
- ✅ **SLSA Level 3**: Supply-chain Levels for Software Artifacts

### Security Controls in Templates

#### Authentication & Authorization
- Multi-factor authentication examples
- Role-based access control (RBAC) configurations
- Principle of least privilege
- Token-based authentication patterns

#### Data Protection
- Encryption at rest examples (AES-256)
- Encryption in transit (TLS 1.3 minimum)
- Secret management patterns
- Privacy by design principles

#### Secure Development
- Mandatory code review workflows
- Security-focused pre-commit hooks
- Threat modeling templates
- Secure coding guidelines in documentation

#### Supply Chain
- Dependency pinning in all templates
- SBOM generation workflows
- Provenance attestation
- Vulnerability scanning

## Vulnerability Disclosure Timeline

| Day | Activity |
|-----|----------|
| 0 | Report received |
| 1-2 | Initial triage and acknowledgment |
| 3-10 | Investigation and impact assessment |
| 11-30 | Fix development and testing |
| 31-45 | Patch release and coordinated disclosure |
| 46+ | Public disclosure details published |

## Security Features in Templates

### Implemented Controls

#### Code Security
- Static analysis on every commit (CodeQL, Semgrep)
- Dependency vulnerability scanning (Trivy, Snyk)
- Secret detection and prevention (Gitleaks, TruffleHog)
- Code quality gates (SonarQube patterns)

#### Build Security
- Reproducible builds
- Signed artifacts (Cosign/Sigstore)
- Provenance generation (SLSA)
- SBOM included (CycloneDX, SPDX)

#### Deployment Security
- Policy enforcement examples (OPA/Kyverno)
- Container image scanning
- Network policies
- Runtime security monitoring patterns

#### Monitoring
- Security event logging
- Anomaly detection patterns
- Audit trail examples
- Incident alerting configurations

## Security Updates

### Patch Management Priority
- **Critical**: Address within 24 hours
- **High**: Address within 7 days
- **Medium**: Address within 30 days
- **Low**: Address in next regular release

### Communication Channels
- Security advisories published on GitHub
- CHANGELOG.md updates for security fixes
- GitHub Discussions for security topics
- Repository notifications for critical updates

## Security Testing

### Automated Testing
- **SAST**: Included in all template CI/CD pipelines
- **Secret Scanning**: Pre-commit hooks and CI checks
- **Dependency Scanning**: Daily automated scans
- **Container Scanning**: On every image build

### Manual Review
- Code reviews for all changes
- Security-focused PR reviews
- Template validation before release
- Community security audits welcome

## Security Best Practices in Generated Projects

When using Agentic Canon templates, follow these practices:

### 1. Secrets Management
- Never commit secrets to Git
- Use environment variables or secret management services
- Rotate secrets regularly
- Use the included .gitignore patterns

### 2. Dependencies
- Keep dependencies up to date
- Use Dependabot/Renovate configurations included
- Review dependency updates before merging
- Monitor for known vulnerabilities

### 3. CI/CD Security
- Enable required checks on branches
- Use CODEOWNERS for sensitive files
- Implement security scanning in pipelines
- Sign and verify artifacts

### 4. Access Control
- Follow principle of least privilege
- Use short-lived tokens
- Implement MFA where possible
- Regular access reviews

## Security Resources

### For Contributors
- [Secure Coding Guidelines](templates/repository/common/SECURITY.md)
- [Security Scanning Setup](docs/security/)
- [SBOM Generation](templates/security/sbom/)

### For Users
- [Security Best Practices](BIBLE.md)
- [Template Security Features](INDEX.md)
- [CI/CD Security Gates](templates/cicd/)

### Tools Included in Templates
- **CodeQL**: Static analysis for security vulnerabilities
- **Semgrep**: Pattern-based security scanning
- **Trivy**: Vulnerability and misconfiguration scanning
- **Gitleaks**: Secret scanning
- **TruffleHog**: Secret detection
- **Cosign**: Container image signing
- **OWASP Dependency-Check**: Dependency vulnerability scanning

## Scope

This security policy applies to:
- Agentic Canon repository and documentation
- All Cookiecutter templates
- Example implementations
- Generated projects (for template-included security features)
- CI/CD workflows and configurations

## Out of Scope

The following are out of scope:
- Third-party dependencies (report to respective maintainers)
- Projects generated from templates (user's responsibility to maintain)
- Theoretical vulnerabilities without proof of concept
- Social engineering attacks

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities.

### Recognition
Contributors who report valid security issues will be:
- Acknowledged in CHANGELOG.md (with permission)
- Listed in security advisories
- Recognized in the GitHub Security tab

## Contact

- **Security Team**: security@jonathanboardman.com
- **Project Maintainer**: Jonathan Boardman (@IAmJonoBo)
- **Security Advisories**: https://github.com/IAmJonoBo/Agentic-Canon/security/advisories
- **General Issues**: https://github.com/IAmJonoBo/Agentic-Canon/issues

## Policy Updates

This security policy is reviewed and updated regularly to reflect:
- New security standards and best practices
- Community feedback
- Emerging threats and vulnerabilities
- Changes in tooling and processes

**Last Updated**: 2025-10-11  
**Version**: 1.0.0  
**Next Review**: 2026-01-11

---

*This security policy is part of our commitment to frontier software excellence and follows NIST SSDF, OWASP SAMM, and SLSA best practices.*

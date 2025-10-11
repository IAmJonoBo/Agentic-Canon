# ADR-007: Secret Management Approach

## Status

Accepted

## Context

Applications require secrets (API keys, passwords, tokens, certificates) to function. Managing these secrets securely throughout the development lifecycle is critical to prevent:

1. **Secret Leakage**: Accidental commits to version control
2. **Unauthorized Access**: Secrets exposed in logs, error messages, or artifacts
3. **Compliance Violations**: Failure to meet security standards
4. **Production Incidents**: Revoked or rotated secrets causing outages

We need a comprehensive secret management strategy that:
- Prevents secrets from entering version control
- Detects leaked secrets quickly
- Provides secure secret storage and access
- Works seamlessly with CI/CD
- Supports multiple environments (dev, staging, prod)
- Enables secret rotation without downtime

Several approaches were considered:
- Environment variables only
- Encrypted secrets in repository
- External secret management services
- No secrets policy (service-to-service auth only)
- Multi-layered approach with prevention, detection, and remediation

## Decision

We will implement a **multi-layered secret management approach** with prevention, detection, and secure storage.

## Implementation Strategy

### Layer 1: Prevention (Pre-commit)

**Goal**: Stop secrets before they enter version control

**Tools**:
- Pre-commit hooks with Gitleaks
- IDE integrations (GitHub Copilot, GitGuardian)
- Developer training and guidelines

**Configuration** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

**Guidelines**:
- Never hardcode secrets in source code
- Use placeholder values in example configs
- Document required secrets in README
- Use `.env.example` templates

### Layer 2: Detection (CI/CD)

**Goal**: Detect secrets that bypass pre-commit hooks

**Tools**:
- **TruffleHog**: Entropy-based secret detection
- **Gitleaks**: Pattern-based secret detection
- **GitHub Secret Scanning**: Native GitHub feature

**Workflow** (`.github/workflows/security.yml`):
```yaml
secret-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v5
      with:
        fetch-depth: 0
    
    - name: TruffleHog Secret Scan
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: ${{ github.event.repository.default_branch }}
        head: HEAD
    
    - name: Run Gitleaks
      uses: gitleaks/gitleaks-action@v2
```

**Response Process**:
1. **Immediate**: Block PR merge if secrets detected
2. **Notify**: Alert security team and committer
3. **Revoke**: Immediately rotate compromised secrets
4. **Remediate**: Remove from git history (BFG Repo-Cleaner)
5. **Learn**: Update detection patterns if needed

### Layer 3: Secure Storage

**Goal**: Provide secure secret storage and retrieval

**Per Environment**:

#### Development
- **Local**: `.env` files (gitignored)
- **Team**: Encrypted 1Password/LastPass vaults
- **Fallback**: Dummy/mock values for development

#### CI/CD
- **GitHub Actions**: Repository/Environment secrets
- **Azure Pipelines**: Variable groups
- **GitLab CI**: CI/CD variables

#### Production
- **Cloud-Native**:
  - AWS: Secrets Manager, Parameter Store
  - Azure: Key Vault
  - GCP: Secret Manager
- **Self-Hosted**: HashiCorp Vault, Conjur
- **Kubernetes**: Sealed Secrets, External Secrets Operator

### Secret Access Patterns

#### Application Runtime
```python
# ✅ Correct: Load from environment
import os
api_key = os.environ["API_KEY"]

# ❌ Wrong: Hardcoded
api_key = "sk_live_abc123"
```

#### GitHub Actions
```yaml
# ✅ Correct: Use secrets context
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh

# ❌ Wrong: Expose in logs
- run: echo "Key: ${{ secrets.API_KEY }}"
```

#### Docker
```dockerfile
# ✅ Correct: Build-time ARG, runtime ENV
ARG BUILD_SECRET
RUN --mount=type=secret,id=build_secret \
    ./build.sh

# ❌ Wrong: Bake into image
ENV API_KEY=sk_live_abc123
```

### Secret Types and Handling

#### API Keys
- Store in secret manager
- Rotate quarterly or on compromise
- Use scoped/limited permissions

#### Database Passwords
- Store in secret manager
- Rotate monthly via automation
- Use connection pooling to minimize exposure

#### TLS Certificates
- Store private keys in secret manager
- Automate renewal (Let's Encrypt, cert-manager)
- Never commit to repository

#### SSH Keys
- Use ephemeral keys when possible
- Store in secret manager if persistent
- Rotate after team changes

#### JWT Signing Keys
- Store in secret manager
- Use asymmetric keys (RS256, ES256)
- Rotate signing keys regularly

### Secret Rotation Strategy

**Automated Rotation**:
- Database credentials: Monthly
- API keys: Quarterly
- Certificates: 90 days (automated)
- SSH keys: On personnel changes

**Rotation Process**:
1. Generate new secret
2. Deploy new secret to all environments
3. Update applications to use new secret
4. Verify new secret works
5. Revoke old secret
6. Confirm no breakage

**Zero-Downtime Rotation**:
- Support multiple valid secrets simultaneously
- Phase out old secret gradually
- Monitor for usage of old secret

### Compliance and Auditing

**Audit Trail**:
- Who accessed which secrets when
- Secret creation and rotation events
- Failed access attempts

**Compliance Requirements**:
- **SOC 2**: Encrypt secrets at rest and in transit
- **PCI DSS**: Rotate secrets, restrict access
- **HIPAA**: Audit all secret access
- **GDPR**: Document data encryption keys

**Monitoring**:
- Alert on unusual secret access patterns
- Track secret age and rotation status
- Monitor failed authentication attempts

## Consequences

### Positive

- **Leak Prevention**: Multi-layer defense prevents most leaks
- **Quick Detection**: Automated scanning finds leaks within minutes
- **Secure Storage**: Secrets stored in purpose-built systems
- **Compliance**: Meets SOC 2, PCI DSS, HIPAA requirements
- **Developer Experience**: Clear patterns and tooling
- **Auditable**: Complete audit trail of secret access

### Negative

- **Complexity**: Multiple systems to manage secrets
- **Onboarding**: New developers need training
- **CI/CD Integration**: Requires configuration for each pipeline
- **Cost**: Secret managers have licensing costs
- **Rotation Overhead**: Regular rotation requires coordination

### Mitigation

- **Documentation**: Clear guides for each secret type
- **Automation**: Automated rotation where possible
- **Templates**: Pre-configured secret management in templates
- **Training**: Security training for all developers
- **Tooling**: CLI tools to simplify secret operations

## Security Best Practices

### Do's ✅

1. **Use secret managers** for production secrets
2. **Rotate secrets regularly** on a schedule
3. **Limit secret scope** to minimum necessary permissions
4. **Encrypt secrets** at rest and in transit
5. **Audit secret access** and review logs regularly
6. **Use pre-commit hooks** to prevent leaks
7. **Document secret requirements** in README
8. **Test secret rotation** in staging first
9. **Monitor for leaked secrets** with scanning tools
10. **Revoke compromised secrets** immediately

### Don'ts ❌

1. **Don't commit secrets** to version control (even in private repos)
2. **Don't log secrets** in application logs
3. **Don't expose secrets** in error messages
4. **Don't share secrets** via email or chat
5. **Don't reuse secrets** across environments
6. **Don't embed secrets** in container images
7. **Don't store secrets** in config management (Chef, Ansible)
8. **Don't use weak secrets** (short, guessable)
9. **Don't leave secrets** in memory dumps or core files
10. **Don't skip rotation** after team changes

## Example Configurations

### .env.example Template
```bash
# API Keys
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379

# Third-party Services
STRIPE_API_KEY=sk_test_...
SENDGRID_API_KEY=SG....
```

### Gitleaks Configuration (.gitleaksrc)
```toml
[extend]
useDefault = true

[[rules]]
description = "Custom API Key Pattern"
id = "custom-api-key"
regex = '''(?i)(api[_-]?key|apikey)['":\s]*[=:\s]*['"]([a-zA-Z0-9_\-]{20,})['"]'''
keywords = ["api_key", "apikey"]
```

### GitHub Actions Secret Usage
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v5
      
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy
        run: |
          ./deploy.sh
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
```

## Incident Response

### Secret Leak Detected

1. **Immediate Actions** (within 1 hour):
   - Revoke/rotate compromised secret
   - Block PR merge (if in PR)
   - Notify security team
   - Assess scope of exposure

2. **Short-term Actions** (within 24 hours):
   - Remove secret from git history
   - Update all applications using secret
   - Review access logs for unauthorized use
   - Document incident

3. **Long-term Actions** (within 1 week):
   - Review and improve detection rules
   - Additional developer training
   - Update documentation
   - Post-mortem review

## Related Decisions

- [ADR-006: Security Scanning Strategy](ADR-006-security-scanning-strategy.md)
- [ADR-008: Dependency Management and Updates](ADR-008-dependency-management.md)

## References

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [HashiCorp Vault](https://www.vaultproject.io/)

---

**Date**: 2025-10-11  
**Author**: Agentic Canon Security Team  
**Status**: Accepted  
**Version**: 1.0

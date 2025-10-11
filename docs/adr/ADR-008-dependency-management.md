# ADR-008: Dependency Management and Updates

## Status

Accepted

## Context

Modern applications depend on hundreds of third-party libraries and packages. Managing these dependencies securely and efficiently is critical for:

1. **Security**: Vulnerabilities in dependencies are a primary attack vector
2. **Stability**: Breaking changes can cause production incidents
3. **Maintenance**: Outdated dependencies accumulate technical debt
4. **Compliance**: License compatibility and audit requirements
5. **Performance**: Newer versions often include performance improvements

Challenges include:
- Keeping dependencies up-to-date without breaking changes
- Detecting and patching security vulnerabilities quickly
- Managing transitive dependencies
- Handling breaking changes across major versions
- Ensuring license compliance
- Balancing update frequency with stability

Several approaches were considered:
- Manual dependency updates
- Automated updates without testing
- Conservative approach (update only on CVE)
- Aggressive approach (update immediately)
- Balanced approach with automation and safety checks

## Decision

We will implement a **balanced, automated dependency management strategy** using multiple tools and processes to ensure security, stability, and maintainability.

## Implementation Strategy

### Core Tools

#### 1. Renovate Bot (Primary)
- **Purpose**: Automated dependency updates
- **Configuration**: `renovate.json` in repository root
- **Frequency**: Daily checks, weekly batch updates

#### 2. Dependabot (Secondary)
- **Purpose**: Security vulnerability alerts and PRs
- **Configuration**: `.github/dependabot.yml`
- **Frequency**: Daily for security, weekly for everything else

#### 3. Dependency Review Action
- **Purpose**: PR-level dependency vulnerability scanning
- **Integration**: GitHub Actions workflow
- **Trigger**: On every pull request

#### 4. Language-Specific Scanners
- **Python**: `pip-audit`, Safety
- **Node.js**: `npm audit`, Snyk
- **Go**: `govulncheck`
- **Rust**: `cargo audit`

### Update Strategy

#### Security Updates (High Priority)
- **Trigger**: CVE published with CVSS ≥ 7.0
- **Response Time**: Within 24 hours
- **Process**:
  1. Automated PR created by Renovate/Dependabot
  2. CI tests run automatically
  3. If tests pass → Auto-merge (for patch versions)
  4. If tests fail → Notify team for manual review
  5. Deploy to production within 24 hours

#### Non-Security Updates (Regular Cadence)

**Patch Versions (x.x.X)**:
- **Frequency**: Weekly batch
- **Auto-merge**: Yes, if tests pass
- **Risk**: Low (bug fixes only)

**Minor Versions (x.X.0)**:
- **Frequency**: Weekly batch
- **Auto-merge**: No
- **Review Required**: Quick review + manual merge
- **Risk**: Medium (new features, possible behavior changes)

**Major Versions (X.0.0)**:
- **Frequency**: Quarterly review
- **Auto-merge**: Never
- **Review Required**: Thorough review + testing
- **Risk**: High (breaking changes expected)

### Renovate Configuration

**File**: `renovate.json`
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base", "schedule:weekly"],
  "rangeStrategy": "bump",
  "semanticCommits": "enabled",
  "dependencyDashboard": true,
  "packageRules": [
    {
      "groupName": "Security updates",
      "matchUpdateTypes": ["patch"],
      "matchDatasources": ["npm", "pypi", "go"],
      "matchDepTypes": ["dependencies"],
      "automerge": true,
      "automergeType": "pr",
      "schedule": ["at any time"],
      "vulnerabilityAlerts": {
        "enabled": true
      }
    },
    {
      "groupName": "Patch updates",
      "matchUpdateTypes": ["patch"],
      "schedule": ["before 6am on Monday"],
      "automerge": true
    },
    {
      "groupName": "Minor updates",
      "matchUpdateTypes": ["minor"],
      "schedule": ["before 6am on Monday"],
      "automerge": false
    },
    {
      "groupName": "Major updates",
      "matchUpdateTypes": ["major"],
      "schedule": ["before 6am on the first day of the month"],
      "automerge": false,
      "dependencyDashboardApproval": true
    }
  ],
  "vulnerabilityAlerts": {
    "labels": ["security", "high-priority"],
    "assignees": ["@security-team"],
    "enabled": true
  }
}
```

### Dependabot Configuration

**File**: `.github/dependabot.yml`
```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "python"

  # Node.js dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "javascript"

  # Go dependencies
  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "go"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "ci-cd"
```

### Dependency Review Workflow

**File**: `.github/workflows/dependency-review.yml`
```yaml
name: Dependency Review
on: [pull_request]

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
          deny-licenses: GPL-2.0, GPL-3.0, AGPL-3.0
          comment-summary-in-pr: always
```

### Lock Files and Version Pinning

#### Python
```python
# pyproject.toml - Flexible ranges
[project]
dependencies = [
    "fastapi>=0.100.0,<1.0.0",
    "uvicorn[standard]>=0.23.0",
]

# requirements.txt - Exact pins (generated by pip-compile)
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

#### Node.js
```json
// package.json - Flexible ranges
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21"
  }
}

// package-lock.json - Exact versions (auto-generated)
```

#### Go
```go
// go.mod - Minimum versions
module github.com/org/service

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/stretchr/testify v1.8.4
)

// go.sum - Checksums for verification
```

### Testing Strategy

**Before Merging Updates**:

1. **Unit Tests**: All existing tests must pass
2. **Integration Tests**: Service-to-service communication verified
3. **E2E Tests**: Critical user flows validated
4. **Performance Tests**: No regression in latency/throughput
5. **Security Scans**: No new vulnerabilities introduced

**Post-Update Monitoring**:
- Error rate monitoring (30 minutes)
- Performance metrics (1 hour)
- User feedback (24 hours)
- Rollback plan ready

### Handling Breaking Changes

#### Assessment Phase
1. Review changelog and breaking changes
2. Estimate migration effort
3. Check for available codemods/migration tools
4. Assess business value of update

#### Migration Phase
1. Create feature branch for update
2. Update dependency version
3. Fix breaking changes
4. Update tests
5. Update documentation
6. Test thoroughly in staging

#### Rollout Phase
1. Deploy to canary environment (5% traffic)
2. Monitor for 24 hours
3. Gradual rollout: 25% → 50% → 100%
4. Keep previous version ready for rollback

### License Compliance

**Allowed Licenses** (permissive):
- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause
- ISC, CC0-1.0, Unlicense

**Review Required** (weak copyleft):
- MPL-2.0, EPL-2.0, LGPL-3.0

**Forbidden** (strong copyleft):
- GPL-2.0, GPL-3.0, AGPL-3.0

**Enforcement**:
- Automated license checking in CI
- PR blocked if forbidden license detected
- Legal review for uncertain cases

### Vulnerability Response

#### Severity Levels

**Critical (CVSS 9.0-10.0)**:
- Response: Within 4 hours
- Process: Emergency patch, immediate deployment
- Communication: Incident notification

**High (CVSS 7.0-8.9)**:
- Response: Within 24 hours
- Process: Hotfix PR, expedited review
- Communication: Team notification

**Medium (CVSS 4.0-6.9)**:
- Response: Within 7 days
- Process: Regular update cycle
- Communication: Weekly security report

**Low (CVSS 0.1-3.9)**:
- Response: Within 30 days
- Process: Batch with other updates
- Communication: Monthly summary

#### False Positive Handling

If vulnerability is not applicable:
1. Document reason (different code path, environment, etc.)
2. Add suppression with justification
3. Review suppression quarterly
4. Track in security dashboard

### Transitive Dependencies

**Strategy**:
- Monitor transitive dependencies for vulnerabilities
- Update direct dependencies to pull in patched transitives
- If direct update unavailable, consider dependency override
- Document all overrides with reason and expiry date

**Override Example (package.json)**:
```json
{
  "overrides": {
    "minimist": "^1.2.8"
  }
}
```

### Metrics and Monitoring

**Key Metrics**:
- Dependency age (time since latest version)
- Vulnerability count by severity
- Update lag (time from release to deployment)
- Update success rate
- Rollback rate

**Dashboard**:
- Dependency health score per service
- Open security vulnerabilities
- Pending updates by priority
- License compliance status

**Alerts**:
- Critical vulnerability detected
- Dependency > 6 months outdated
- Update failed > 3 times
- License violation detected

## Consequences

### Positive

- **Security**: Fast response to vulnerabilities
- **Automation**: Minimal manual work for updates
- **Stability**: Graduated rollout prevents widespread issues
- **Visibility**: Clear view of dependency health
- **Compliance**: Automated license checking
- **Freshness**: Dependencies stay reasonably up-to-date

### Negative

- **Update Churn**: Frequent dependency PRs
- **Test Load**: More CI/CD runs from updates
- **False Positives**: Some vulnerability alerts not applicable
- **Breaking Changes**: Major updates require manual work
- **Tool Overlap**: Renovate and Dependabot have some overlap

### Mitigation

- **Batching**: Group related updates together
- **Scheduling**: Run updates during off-peak hours
- **Filtering**: Suppress non-applicable vulnerabilities
- **Planning**: Schedule major updates during sprint planning
- **Coordination**: Use Renovate as primary, Dependabot for security alerts only

## Best Practices

### Do's ✅

1. **Pin exact versions** in lock files
2. **Test updates** before merging
3. **Monitor post-deployment** for issues
4. **Document breaking changes** in CHANGELOG
5. **Review major updates** carefully
6. **Keep dependencies fresh** (< 6 months old)
7. **Use SBOM** to track dependencies
8. **Audit licenses** regularly
9. **Have rollback plan** for updates
10. **Communicate impact** to team

### Don'ts ❌

1. **Don't ignore security updates**
2. **Don't update everything at once**
3. **Don't skip testing**
4. **Don't use wildcards** in version ranges (e.g., `*`, `latest`)
5. **Don't merge failing updates**
6. **Don't let dependencies get stale** (> 1 year)
7. **Don't forget transitive dependencies**
8. **Don't commit lock files to .gitignore**
9. **Don't override security policies** without approval
10. **Don't ignore license violations**

## Related Decisions

- [ADR-006: Security Scanning Strategy](ADR-006-security-scanning-strategy.md)
- [ADR-007: Secret Management Approach](ADR-007-secret-management.md)

## References

- [Renovate Documentation](https://docs.renovatebot.com/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [Snyk Vulnerability Database](https://snyk.io/vuln/)
- [CVE Database](https://cve.mitre.org/)

---

**Date**: 2025-10-11  
**Author**: Agentic Canon Security Team  
**Status**: Accepted  
**Version**: 1.0

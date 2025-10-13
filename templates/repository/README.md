# Repository Templates

Common repository files for governance, security, and contribution guidelines.

## Purpose

These templates provide standardized repository files that ensure consistent governance, clear contribution processes, and security best practices across all projects.

## Contents

### 📋 Common Files (`common/`)

Essential repository files for all projects.

**Files:**

- [`SECURITY.md`](common/SECURITY.md) - Security policy and vulnerability reporting
- [`CONTRIBUTING.md`](common/CONTRIBUTING.md) - Contribution guidelines and development process
- [`CODEOWNERS`](common/CODEOWNERS) - Code ownership and review requirements

### 🔒 SECURITY.md

Comprehensive security policy template.

**Sections:**

1. **Vulnerability Reporting**
   - Private reporting instructions
   - Response timeline (48 hours acknowledgment)
   - Disclosure process

2. **Security Standards**
   - Supply chain security (SLSA Level 3, SBOM, Sigstore)
   - Development security (SAST, secret scanning, dependency scanning)
   - Runtime security (DAST, penetration testing, monitoring)

3. **Compliance**
   - NIST SSDF v1.1
   - OWASP SAMM Level 2
   - OWASP ASVS Level 2/3
   - CWE Top 25 coverage

4. **Security Controls**
   - Authentication & authorization
   - Data protection (encryption at rest/transit)
   - Secure development practices
   - Incident response

**Usage:**

```bash
# Copy to repository root
cp templates/repository/common/SECURITY.md .

# Customize placeholders
sed -i 's/{{ DOMAIN }}/example.com/g' SECURITY.md
sed -i 's/{{ ORGANIZATION }}/MyOrg/g' SECURITY.md

# Commit
git add SECURITY.md
git commit -m "docs: add security policy"
```

**Key Features:**

- GitHub Security Advisories integration
- Clear reporting process
- Standards compliance documentation
- Security control mapping
- Incident response procedures

### 🤝 CONTRIBUTING.md

Detailed contribution guidelines.

**Sections:**

1. **Getting Started**
   - Prerequisites and setup
   - Development environment configuration
   - Repository structure

2. **Development Process**
   - Branch strategy (trunk-based development)
   - Commit message conventions (Conventional Commits)
   - Code style and linting

3. **Quality Standards**
   - Code coverage requirements (≥80%)
   - Testing requirements (unit, integration, E2E)
   - Documentation standards
   - Security checks

4. **Submitting Changes**
   - Pull request process
   - PR template requirements
   - Required checks

5. **Review Process**
   - Review timeline (48-72 hours)
   - Approval requirements
   - Merge criteria

**Usage:**

```bash
# Copy to repository root
cp templates/repository/common/CONTRIBUTING.md .

# Customize for your project
sed -i 's/{{ PROJECT_NAME }}/My Project/g' CONTRIBUTING.md
sed -i 's/{{ LANGUAGE }}/Python/g' CONTRIBUTING.md
sed -i 's/{{ MIN_VERSION }}/3.11/g' CONTRIBUTING.md
sed -i 's/{{ PACKAGE_MANAGER }}/pip/g' CONTRIBUTING.md
sed -i 's/{{ INSTALL_COMMAND }}/pip install -e .[dev]/g' CONTRIBUTING.md
sed -i 's/{{ TEST_COMMAND }}/pytest/g' CONTRIBUTING.md

# Commit
git add CONTRIBUTING.md
git commit -m "docs: add contribution guidelines"
```

**Commit Convention:**

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 👥 CODEOWNERS

Code ownership and automatic review assignment.

**Features:**

- Path-based ownership rules
- Team-based assignments
- Required reviewers for specific paths
- Escalation paths

**Format:**

```
# Global owners
* @org/team-leads

# Component owners
/src/auth/ @org/auth-team
/src/payments/ @org/payments-team
/src/api/ @org/api-team

# Infrastructure
/infrastructure/ @org/platform-team @org/sre-team
/.github/ @org/devops-team

# Documentation
/docs/ @org/tech-writers
README.md @org/tech-writers

# Security-sensitive
/src/auth/ @org/security-team
/src/crypto/ @org/security-team
SECURITY.md @org/security-team

# Configuration
*.yml @org/platform-team
*.yaml @org/platform-team
Dockerfile @org/platform-team
```

**Usage:**

```bash
# Copy to repository root
cp templates/repository/common/CODEOWNERS .github/CODEOWNERS

# Customize teams
vim .github/CODEOWNERS

# Commit
git add .github/CODEOWNERS
git commit -m "chore: add code owners"

# Enable in branch protection
# Settings → Branches → Require review from Code Owners
```

**Best Practices:**

- Start general, get more specific
- Use teams instead of individuals
- Document ownership rationale
- Review and update quarterly
- Consider bus factor

### 📝 Additional Repository Files (Planned)

Future templates to be added:

- **CODE_OF_CONDUCT.md** - Community guidelines
- **SUPPORT.md** - Support channels and resources
- **CHANGELOG.md** - Version history
- **.gitignore** - Language-specific ignore patterns
- **.editorconfig** - Editor configuration
- **LICENSE** - Open source license
- **README.md** - Project overview and quick start

## Quick Start

### Complete Repository Setup

```bash
# 1. Create .github directory
mkdir -p .github/{ISSUE_TEMPLATE,PULL_REQUEST_TEMPLATE,workflows}

# 2. Copy common files
cp templates/repository/common/SECURITY.md .
cp templates/repository/common/CONTRIBUTING.md .
cp templates/repository/common/CODEOWNERS .github/

# 3. Customize placeholders
find . -type f \( -name "SECURITY.md" -o -name "CONTRIBUTING.md" \) \
  -exec sed -i 's/{{ PROJECT_NAME }}/My Project/g' {} +

# 4. Add issue templates
cat > .github/ISSUE_TEMPLATE/bug_report.md <<'EOF'
---
name: Bug Report
about: Report a bug
---

## Description
A clear description of the bug.

## Steps to Reproduce
1.
2.
3.

## Expected Behavior


## Actual Behavior


## Environment
- OS:
- Version:
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md <<'EOF'
---
name: Feature Request
about: Suggest an idea
---

## Problem
What problem does this solve?

## Proposed Solution


## Alternatives Considered


## Additional Context

EOF

# 5. Add PR template
cat > .github/PULL_REQUEST_TEMPLATE.md <<'EOF'
## Description
What does this PR do?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] All tests passing
- [ ] No security vulnerabilities

## Related Issues
Closes #
EOF

# 6. Commit all files
git add .github/ SECURITY.md CONTRIBUTING.md
git commit -m "docs: add repository governance files"
git push
```

### Branch Protection Setup

```bash
# GitHub CLI setup
gh repo edit --enable-issues \
  --enable-wiki=false \
  --enable-projects=false

# Add branch protection
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=ci \
  --field required_status_checks[contexts][]=security \
  --field enforce_admins=true \
  --field required_pull_request_reviews[dismiss_stale_reviews]=true \
  --field required_pull_request_reviews[require_code_owner_reviews]=true \
  --field required_pull_request_reviews[required_approving_review_count]=2 \
  --field required_linear_history=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## Best Practices

### Repository Governance

1. **Clear documentation** - README, CONTRIBUTING, SECURITY
2. **Issue templates** - Standardize bug reports and feature requests
3. **PR templates** - Consistent pull request format
4. **Code owners** - Automatic reviewer assignment
5. **Branch protection** - Prevent direct pushes to main
6. **Status checks** - Require CI/CD to pass
7. **Security policy** - Clear vulnerability reporting
8. **License** - Choose appropriate open source license

### Code Review

1. **Timely reviews** - Review within 48-72 hours
2. **Constructive feedback** - Focus on improvement
3. **Two reviewers** - Require at least two approvals
4. **Code owner approval** - Require owner approval for their code
5. **Automated checks** - Let CI do the mechanical checks
6. **Small PRs** - Keep PRs focused and reviewable (<500 lines)
7. **Documentation** - Update docs with code changes

### Security

1. **Private reporting** - Use GitHub Security Advisories
2. **Quick response** - Acknowledge within 48 hours
3. **Coordinated disclosure** - Patch before public disclosure
4. **Security scanning** - Automated SAST, dependency, secret scanning
5. **SBOM** - Generate Software Bill of Materials
6. **Signing** - Sign releases with Cosign
7. **Audit logs** - Review repository activity

## Integration Examples

### GitHub Branch Protection

```yaml
# .github/settings.yml (with probot/settings)
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - ci
          - security
          - test
      enforce_admins: true
      required_linear_history: true
      restrictions: null
```

### Auto-assign Reviewers

```yaml
# .github/auto_assign.yml
addReviewers: true
addAssignees: author
reviewers:
  - org/team-leads
numberOfReviewers: 2
```

### Issue Triage

```yaml
# .github/workflows/issue-triage.yml
name: Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.addLabels({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: ['needs-triage']
            })
```

## Standards Compliance

These templates help achieve compliance with:

- ✅ **Open Source Best Practices** - Standard governance files
- ✅ **GitHub Community Standards** - 100% community profile
- ✅ **Security Best Practices** - Vulnerability disclosure
- ✅ **Contribution Guidelines** - Clear process for contributors
- ✅ **ISO/IEC 25010** - Maintainability through documentation

## Additional Resources

### GitHub Documentation

- [Community Profile](https://docs.github.com/en/communities)
- [Code Owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Security Advisories](https://docs.github.com/en/code-security/security-advisories)

### Best Practices

- [Open Source Guides](https://opensource.guide/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

### Related Templates

- [CI/CD Templates](../cicd/README.md) - Automated checks
- [Security Templates](../security/README.md) - Security scanning
- [Automation Templates](../automation/README.md) - Pre-commit hooks

## Contributing

To improve these templates:

1. Share your repository configurations
2. Add language-specific examples
3. Contribute issue/PR templates
4. Document governance patterns
5. Submit PRs with improvements

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

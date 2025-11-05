# Automation Templates

Automation hooks, bot configurations, and remediation scripts for continuous quality and security.

## Purpose

These templates automate quality gates, dependency management, and remediation workflows to maintain code quality and security without manual intervention.

## Contents

### 🪝 Git Hooks (`hooks/`)

Pre-commit and pre-push hooks that enforce quality gates before code enters the repository.

**File:** [`pre-commit`](hooks/pre-commit)

**Features:**

- Secret scanning (Gitleaks)
- Linting enforcement
- Code formatting validation
- Unit test execution
- Commit message format validation (Conventional Commits)
- TODO/FIXME detection
- File size limits (5MB)
- Colored output for clear feedback

**Installation:**

```bash
# Copy to your project
cp templates/automation/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Or use pre-commit framework (recommended)
pip install pre-commit
# Add .pre-commit-config.yaml, then:
pre-commit install
```

**Requirements:**

- Git 2.9+
- Gitleaks (optional but recommended)
- Node.js (for npm projects)

**Customization:**

```bash
# Edit the hook file to add/remove checks
vim .git/hooks/pre-commit

# Adjust MAX_SIZE for file size limits
# Add project-specific validations
# Configure tool paths if needed
```

**Bypass (use sparingly):**

```bash
# Skip pre-commit hooks (NOT recommended)
git commit --no-verify -m "emergency hotfix"
```

### 🤖 Bot Configurations (`bots/`)

Automated dependency management and maintenance bot configurations.

**File:** [`renovate.json`](bots/renovate.json)

**Features:**

- Automated dependency updates
- Security vulnerability alerts (OSV, GitHub)
- Smart automerge for patches
- Grouped updates (minor/patch together)
- Major updates with stability period (7 days)
- Docker image pinning with digest
- GitHub Actions auto-updates
- Lock file maintenance
- Merge confidence metrics
- PR rate limiting (5 concurrent, 2/hour)

**Setup:**

```bash
# Copy to project root
cp templates/automation/bots/renovate.json .

# Customize team names
sed -i 's/{{ TEAM_NAME }}/your-team/g' renovate.json

# Enable Renovate in GitHub:
# 1. Install Renovate GitHub App
# 2. Grant repository access
# 3. Renovate will automatically detect renovate.json
```

**Configuration Highlights:**

**Security-First:**

- Immediate updates for security patches
- Auto-merge enabled for patch versions
- Vulnerability alerts with labels
- OSV database integration

**Smart Scheduling:**

- Weekly schedule (Monday before 6am UTC)
- Minimizes disruption
- Batched updates

**Update Strategy:**

- Patches: Auto-merge after tests pass
- Minor: Group and auto-merge (3-day stabilization)
- Major: Manual review required (7-day stabilization)
- DevDependencies: More permissive auto-merge

**Rate Limiting:**

- Max 5 concurrent PRs
- Max 2 PRs per hour
- Prevents PR spam

**Validation:**

```bash
# Validate configuration
npx renovate-config-validator

# Dry run (test without creating PRs)
npx renovate --dry-run=full

# Check available updates
npx renovate --schedule="" --require-config=ignored
```

### 🔧 Autofix Scripts (Planned)

Automated remediation scripts for common issues.

**Planned Features:**

- Automatic dependency updates
- Linting auto-fixes
- Test quarantine for flaky tests
- Security issue remediation
- Code smell cleanup

## Quick Start

### Complete Setup

```bash
# Set up all automation
mkdir -p .git/hooks scripts

# Copy and configure hooks
cp templates/automation/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Configure Renovate
cp templates/automation/bots/renovate.json .
# Edit {{ TEAM_NAME }} placeholders

# Install dependencies
pip install pre-commit gitleaks
npm install -g renovate

# Test configuration
pre-commit run --all-files
npx renovate-config-validator
```

### Pre-commit Framework Setup (Recommended)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ["--maxkb=5000"]
      - id: check-merge-conflict
      - id: check-json
      - id: pretty-format-json
        args: ["--autofix"]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

  - repo: local
    hooks:
      - id: lint
        name: Run linter
        entry: npm run lint
        language: system
        pass_filenames: false

      - id: test
        name: Run tests
        entry: npm test
        language: system
        pass_filenames: false
```

```bash
# Install and use
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Integration Examples

### GitHub Actions Integration

```yaml
# .github/workflows/pre-commit.yml
name: Pre-commit

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: pre-commit/action@v3.0.1
```

### Renovate Dashboard

Enable Renovate Dashboard to track all dependency updates:

```json
{
  "extends": [":dependencyDashboard"]
}
```

Creates a GitHub Issue with:

- Pending updates
- Ignored dependencies
- Rate-limited PRs
- Configuration errors

### Branch Protection Integration

```yaml
# Require pre-commit checks to pass
# Settings → Branches → Branch protection rules

Required status checks: ✅ pre-commit
  ✅ lint
  ✅ test
  ✅ security-scan
```

## Best Practices

### Git Hooks

1. **Keep hooks fast** - Run only essential checks (<30s)
2. **Use pre-commit framework** - Easier to maintain and share
3. **Fail fast** - Exit on first failure
4. **Provide clear feedback** - Use colors and messages
5. **Allow bypass for emergencies** - Document when appropriate

### Dependency Management

1. **Enable Renovate** - Automate routine updates
2. **Review major updates** - Breaking changes need attention
3. **Auto-merge patches** - Low-risk, high-value
4. **Monitor security alerts** - Respond within 24 hours
5. **Pin Docker digests** - Reproducible builds
6. **Test updates** - CI must pass before merge

### Automation Philosophy

1. **Automate the boring** - Repetitive tasks should be automated
2. **Fail loudly** - Issues should be obvious
3. **Self-service** - Developers fix issues locally
4. **Continuous improvement** - Adjust thresholds based on team experience
5. **Security first** - Vulnerability patches take priority

## Troubleshooting

### Pre-commit Hook Issues

**Hook not running:**

```bash
# Check if hook is installed
ls -la .git/hooks/pre-commit

# Ensure it's executable
chmod +x .git/hooks/pre-commit

# Test manually
.git/hooks/pre-commit
```

**Hook failing:**

```bash
# Run verbose
bash -x .git/hooks/pre-commit

# Check tool installation
which gitleaks
which npm

# Bypass for emergency (use sparingly)
git commit --no-verify
```

### Renovate Issues

**No PRs created:**

```bash
# Check Renovate logs in GitHub
# Settings → Installed GitHub Apps → Renovate → Configure

# Validate config
npx renovate-config-validator

# Check Dependency Dashboard issue
# Look for "Renovate Dashboard" issue in repo
```

**Too many PRs:**

```json
// Adjust rate limits in renovate.json
{
  "prConcurrentLimit": 3, // Reduce from 5
  "prHourlyLimit": 1 // Reduce from 2
}
```

**Auto-merge not working:**

```bash
# Ensure branch protection allows auto-merge
# Settings → Branches → Enable "Allow auto-merge"

# Check PR labels
# Auto-merge PRs should have "automerge" label

# Verify CI status checks pass
```

## Standards Compliance

These templates help achieve compliance with:

- ✅ **NIST SSDF v1.1**: Secure Software Development Framework
  - PW.1: Validate code before commit
  - PW.4: Update dependencies regularly
- ✅ **OWASP SAMM**: Software Assurance Maturity Model
  - Implementation: Automated security testing
- ✅ **CIS Controls**: Critical Security Controls
  - Control 4: Secure configuration management
  - Control 16: Application software security

## Additional Resources

### Pre-commit

- [Pre-commit Framework](https://pre-commit.com/)
- [Pre-commit Hooks](https://github.com/pre-commit/pre-commit-hooks)
- [Gitleaks](https://github.com/gitleaks/gitleaks)

### Renovate

- [Renovate Documentation](https://docs.renovatebot.com/)
- [Renovate Configuration Options](https://docs.renovatebot.com/configuration-options/)
- [Merge Confidence](https://docs.renovatebot.com/merge-confidence/)

### Related Templates

- [Security Templates](../security/README.md) - Secret scanning, SBOM
- [CI/CD Templates](../cicd/README.md) - Pipeline integration
- [Repository Templates](../repository/README.md) - Branch protection

## Contributing

To improve these templates:

1. Test with real projects
2. Share your configurations
3. Report issues or edge cases
4. Suggest new automation opportunities
5. Submit PRs with examples

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

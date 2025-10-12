# CI/CD Templates

Continuous Integration and Continuous Delivery pipeline templates for multiple platforms.

## Purpose

These templates provide production-ready CI/CD pipelines implementing comprehensive quality gates, security scanning, and deployment automation across GitHub Actions, GitLab CI, and Azure Pipelines.

## Contents

### 🚀 GitHub Actions (`github-actions/`)

Complete CI/CD workflows for GitHub Actions with all quality gates.

**File:** [`complete-pipeline.yml`](github-actions/complete-pipeline.yml)

**Pipeline Stages:**

1. **Lint & Format** - Code style enforcement
2. **Build & Unit Tests** - Compilation and unit testing with coverage
3. **Security Scanning** - SAST, secret scanning, dependency checks
4. **Integration Tests** - API and integration testing
5. **Contract Tests** - API contract validation
6. **E2E Tests** - End-to-end testing
7. **Performance Tests** - Load testing and budgets
8. **Accessibility Tests** - WCAG compliance
9. **Mutation Testing** - Test quality validation
10. **SBOM Generation** - Software Bill of Materials
11. **Artifact Signing** - Cosign/Sigstore signing
12. **Container Build** - Multi-arch container images
13. **Deploy** - Environment-specific deployment

**Features:**
- Comprehensive quality gates
- Security-first approach (SAST, secrets, dependencies)
- SLSA Level 3 build provenance
- Performance and accessibility budgets
- Matrix testing (multiple Node/Python versions)
- Conditional job execution
- Artifact management
- Deployment strategies (blue-green, canary)

**Usage:**
```bash
# Copy to your project
cp templates/cicd/github-actions/complete-pipeline.yml .github/workflows/ci.yml

# Customize placeholders
sed -i 's/{{ PROJECT_NAME }}/my-service/g' .github/workflows/ci.yml
sed -i 's/{{ COVERAGE_THRESHOLD }}/80/g' .github/workflows/ci.yml

# Commit and push
git add .github/workflows/ci.yml
git commit -m "ci: add complete CI/CD pipeline"
git push
```

**Customization:**
- Adjust `COVERAGE_THRESHOLD` for your project (default: 80%)
- Set `MUTATION_THRESHOLD` for mutation testing (default: 40%)
- Configure `SONAR_ORGANIZATION` if using SonarCloud
- Add project-specific environment variables
- Modify deployment targets and strategies

### 🦊 GitLab CI (`gitlab-ci/`)

GitLab CI/CD pipelines with parallel job execution and caching.

**File:** [`.gitlab-ci.yml`](gitlab-ci/.gitlab-ci.yml)

**Pipeline Stages:**

1. **Validate** - Linting and formatting
2. **Build** - Compilation
3. **Test** - Unit and integration tests
4. **Security** - Security scanning
5. **Package** - Artifact creation
6. **Deploy** - Environment deployment

**Features:**
- Parallel job execution
- Docker-in-Docker support
- GitLab Container Registry integration
- Review apps for MRs
- Manual deployment gates
- Dependency caching
- Environment-specific variables

**Usage:**
```bash
# Copy to project root
cp templates/cicd/gitlab-ci/.gitlab-ci.yml .

# Customize for your project
# Edit stages, jobs, and variables

# Commit and push
git add .gitlab-ci.yml
git commit -m "ci: add GitLab CI pipeline"
git push
```

**Variables:**
```yaml
variables:
  NODE_VERSION: "20"
  COVERAGE_THRESHOLD: "80"
  DOCKER_DRIVER: overlay2
  FF_USE_FASTZIP: "true"
```

### ☁️ Azure Pipelines (Planned)

Azure DevOps pipeline templates (planned).

**Status:** Templates planned for future release

**Planned Features:**
- Multi-stage YAML pipelines
- Template libraries
- Azure DevOps integration
- Azure services deployment
- Variable groups
- Pipeline artifacts

## Quick Start

### GitHub Actions Setup

```bash
# 1. Create workflows directory
mkdir -p .github/workflows

# 2. Copy complete pipeline
cp templates/cicd/github-actions/complete-pipeline.yml \
   .github/workflows/ci.yml

# 3. Customize variables
vim .github/workflows/ci.yml
# Update: PROJECT_NAME, COVERAGE_THRESHOLD, etc.

# 4. Add secrets (if needed)
# GitHub UI: Settings → Secrets and variables → Actions
# Add: SONAR_TOKEN, CODECOV_TOKEN, etc.

# 5. Commit and test
git add .github/workflows/
git commit -m "ci: add CI/CD pipeline"
git push origin main
```

### GitLab CI Setup

```bash
# 1. Copy pipeline to root
cp templates/cicd/gitlab-ci/.gitlab-ci.yml .

# 2. Customize for your project
vim .gitlab-ci.yml

# 3. Configure CI/CD variables
# GitLab UI: Settings → CI/CD → Variables
# Add: DOCKER_REGISTRY_USER, SONAR_TOKEN, etc.

# 4. Commit and test
git add .gitlab-ci.yml
git commit -m "ci: add GitLab CI pipeline"
git push origin main
```

## Integration Examples

### Branch Protection with Required Checks

**GitHub:**
```yaml
# Settings → Branches → Branch protection rules
Required status checks:
  ✅ lint
  ✅ build
  ✅ security / codeql
  ✅ security / secrets
  ✅ test / unit
  ✅ test / integration
```

**GitLab:**
```yaml
# Settings → Repository → Protected branches
Allowed to merge: Maintainers
Allowed to push: No one
Require approval: Yes
```

### Multi-Environment Deployment

```yaml
# GitHub Actions
jobs:
  deploy-dev:
    environment:
      name: development
      url: https://dev.example.com
    # ... deployment steps

  deploy-staging:
    needs: deploy-dev
    environment:
      name: staging
      url: https://staging.example.com
    # ... deployment steps

  deploy-prod:
    needs: deploy-staging
    environment:
      name: production
      url: https://example.com
    # ... deployment steps
```

### Conditional Job Execution

```yaml
# Run security scans only on main branch
security:
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  # ... security steps

# Run E2E tests only if backend changes
e2e-tests:
  if: contains(github.event.head_commit.modified, 'backend/')
  runs-on: ubuntu-latest
  # ... E2E test steps
```

### Matrix Testing

```yaml
# Test across multiple versions
test:
  strategy:
    matrix:
      node-version: [18, 20, 22]
      os: [ubuntu-latest, windows-latest, macos-latest]
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

## Best Practices

### General CI/CD

1. **Fail fast** - Run quick checks (lint, format) first
2. **Parallel execution** - Run independent jobs concurrently
3. **Cache dependencies** - Speed up builds with caching
4. **Artifact reuse** - Build once, deploy many times
5. **Environment parity** - Production-like CI environment
6. **Immutable artifacts** - Tag/version all artifacts
7. **Secure secrets** - Use secret management, not hardcoded values
8. **Status badges** - Show build status in README
9. **Notifications** - Alert team on failures
10. **Pipeline as code** - Version control all pipeline configs

### Security

1. **Scan early** - Security checks in every PR
2. **Block on vulnerabilities** - Fail builds on critical issues
3. **Dependency scanning** - Automated vulnerability checks
4. **Secret scanning** - Prevent credential leaks
5. **SBOM generation** - Track software supply chain
6. **Artifact signing** - Sign releases with Cosign
7. **Least privilege** - Minimal permissions for jobs
8. **Audit logs** - Enable and review CI/CD logs

### Performance

1. **Optimize build times** - Target <10 minutes
2. **Use caching** - Dependencies, build outputs
3. **Parallel jobs** - Split test suites
4. **Conditional execution** - Skip unnecessary jobs
5. **Resource limits** - Set appropriate timeouts
6. **Artifact pruning** - Clean up old artifacts
7. **Performance budgets** - Enforce build/bundle limits

### Quality

1. **Coverage thresholds** - Enforce minimum coverage
2. **Mutation testing** - Validate test quality
3. **Code analysis** - SonarQube, CodeClimate
4. **Contract testing** - Validate API contracts
5. **Accessibility checks** - WCAG compliance
6. **Visual regression** - Catch UI changes
7. **Performance testing** - Load and stress tests

## Tools and Integrations

### Code Quality
- **SonarQube/SonarCloud** - Code quality and security
- **Codecov** - Coverage reporting
- **CodeClimate** - Maintainability metrics
- **Stryker** - Mutation testing

### Security
- **CodeQL** - Semantic code analysis
- **Semgrep** - Pattern-based scanning
- **Snyk** - Dependency vulnerabilities
- **Trivy** - Container scanning
- **Gitleaks** - Secret detection

### Testing
- **Jest/Vitest** - Unit testing
- **Playwright/Cypress** - E2E testing
- **K6/Artillery** - Load testing
- **Pact** - Contract testing
- **Pa11y/axe** - Accessibility testing

### Deployment
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Helm** - Package management
- **ArgoCD/Flux** - GitOps
- **Terraform** - Infrastructure as Code

## Monitoring and Observability

### Pipeline Metrics

Track these key metrics:

- **Build success rate** - Target: >95%
- **Build duration** - Target: <10 minutes
- **Time to feedback** - Target: <5 minutes
- **Flaky test rate** - Target: <2%
- **Deployment frequency** - DORA metric
- **Lead time for changes** - DORA metric
- **Change failure rate** - DORA metric
- **Mean time to recovery** - DORA metric

### Dashboards

```yaml
# Example Grafana dashboard for CI/CD metrics
dashboards:
  - Build Success Rate (30d)
  - Average Build Duration
  - Test Failure Trends
  - Security Scan Results
  - Deployment Frequency
  - DORA Metrics
```

## Troubleshooting

### Common Issues

**Build Timeout:**
```yaml
# Increase timeout
jobs:
  build:
    timeout-minutes: 30  # Default is 360
```

**Cache Not Working:**
```yaml
# Verify cache key is correct
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Secrets Not Available:**
```bash
# Check secret is set in repository settings
# Verify secret name matches exactly (case-sensitive)
# Ensure workflow has correct permissions
```

**Flaky Tests:**
```yaml
# Run tests with retry
- run: npm test -- --retries=2

# Or use test retry action
- uses: nick-fields/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test
```

## Standards Compliance

These templates help achieve compliance with:

- ✅ **NIST SSDF v1.1** - Secure Software Development Framework
- ✅ **OWASP SAMM** - Software Assurance Maturity Model
- ✅ **SLSA Level 3** - Supply-chain Levels for Software Artifacts
- ✅ **ISO/IEC 25010** - Software quality characteristics
- ✅ **DORA Metrics** - DevOps Research and Assessment

## Additional Resources

### Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [Azure Pipelines Docs](https://learn.microsoft.com/en-us/azure/devops/pipelines/)

### Best Practices
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitLab CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [Continuous Delivery](https://continuousdelivery.com/)

### Related Templates
- [Security Templates](../security/README.md) - Security scanning
- [Contracts Templates](../contracts/README.md) - API contract testing
- [Video Tutorial: CI/CD Setup](../../examples/video-tutorials/03-cicd-setup.md)

## Contributing

To improve these templates:
1. Share your production pipeline configurations
2. Add platform-specific examples
3. Document common patterns
4. Report issues or edge cases
5. Submit PRs with improvements

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

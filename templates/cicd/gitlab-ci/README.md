# GitLab CI Templates

Complete GitLab CI/CD pipeline templates with comprehensive quality gates and security scanning.

## Overview

This directory contains production-ready GitLab CI/CD pipeline configurations implementing the same quality standards as the GitHub Actions templates but tailored for GitLab's CI/CD platform.

## File

**[.gitlab-ci.yml](.gitlab-ci.yml)** - Complete CI/CD pipeline with:
- Parallel job execution
- Multi-stage pipeline (lint, build, test, security, quality, package, deploy)
- Docker-in-Docker support
- Comprehensive caching
- Security scanning
- Code quality checks
- Artifact management
- Environment-specific deployments

## Pipeline Stages

### 1. Lint (lint)
- Code linting
- Format checking
- Fast feedback (runs in parallel)

### 2. Build (build)
- Dependency installation
- Application build
- Artifact generation

### 3. Test (test)
- Unit tests with coverage
- Integration tests
- Mutation testing (optional)
- E2E tests (optional)

### 4. Security (security)
- SAST scanning
- Secret detection
- Dependency scanning
- Container scanning
- License compliance

### 5. Quality (quality)
- Code quality analysis
- Coverage reporting
- Technical debt tracking

### 6. Package (package)
- Docker image build
- Multi-arch support
- Registry push

### 7. Deploy (deploy)
- Environment-specific deployment
- Review apps for merge requests
- Production deployment (manual)

## Quick Start

```bash
# Copy to project root
cp templates/cicd/gitlab-ci/.gitlab-ci.yml .

# Customize variables
vim .gitlab-ci.yml
# Update: PROJECT_NAME, coverage thresholds, etc.

# Commit and push
git add .gitlab-ci.yml
git commit -m "ci: add GitLab CI pipeline"
git push origin main
```

## Configuration

### Variables

```yaml
variables:
  PROJECT_NAME: "my-project"
  COVERAGE_THRESHOLD: 80        # Minimum code coverage %
  MUTATION_THRESHOLD: 40        # Minimum mutation score
  DOCKER_DRIVER: overlay2       # Docker driver
  DOCKER_TLS_CERTDIR: "/certs"  # Docker TLS configuration
```

### CI/CD Settings

Configure in GitLab UI:
- **Settings → CI/CD → Variables**
  - `DOCKER_REGISTRY_USER`
  - `DOCKER_REGISTRY_PASSWORD`
  - `SONAR_TOKEN` (if using SonarQube)

### Runners

Works with:
- **Shared runners** - GitLab.com free tier
- **Specific runners** - Self-hosted
- **Docker executor** - Recommended

## Features

### Caching

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .npm/
```

### Artifacts

```yaml
artifacts:
  paths:
    - dist/
    - coverage/
  reports:
    coverage_report:
      coverage_format: cobertura
      path: coverage/cobertura-coverage.xml
  expire_in: 1 week
```

### Rules

```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'  # Run on MRs
  - if: '$CI_COMMIT_BRANCH == "main"'                   # Run on main
  - when: manual                                        # Manual trigger
```

### Review Apps

```yaml
review-app:
  stage: deploy
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

## Language-Specific Examples

### Python

```yaml
# Python-specific jobs
python-test:
  image: python:3.11
  script:
    - pip install -e .[dev]
    - pytest --cov=src
    - coverage report --fail-under=80
```

### Node.js

```yaml
# Node.js jobs (default in template)
node-test:
  image: node:20
  script:
    - npm ci
    - npm test -- --coverage
```

### Go

```yaml
# Go-specific jobs
go-test:
  image: golang:1.22
  script:
    - go mod download
    - go test -v -cover ./...
    - go test -race ./...
```

## Security Scanning

### SAST (Static Application Security Testing)

```yaml
sast:
  stage: security
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker run --rm -v $PWD:/src ghcr.io/returntocorp/semgrep semgrep --config=auto /src
```

### Secret Detection

```yaml
secret-detection:
  stage: security
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --report-format json --report-path gitleaks-report.json
  artifacts:
    reports:
      secret_detection: gitleaks-report.json
```

### Dependency Scanning

```yaml
dependency-scanning:
  stage: security
  script:
    - npm audit --production --audit-level=moderate
    - npm audit fix --dry-run
  allow_failure: true
```

## Best Practices

### Performance

1. **Use caching** - Cache dependencies to speed up builds
2. **Parallel jobs** - Run independent jobs in parallel
3. **Docker layer caching** - Enable for faster Docker builds
4. **Artifacts** - Only store what's needed

### Security

1. **Protected variables** - Mark secrets as protected and masked
2. **Runner tags** - Use specific runners for sensitive jobs
3. **Artifact expiry** - Set appropriate expiration times
4. **Branch protection** - Require pipeline success before merge

### Maintenance

1. **Include templates** - Use `include:` for reusable configs
2. **YAML anchors** - DRY with YAML anchors and aliases
3. **Job templates** - Create templates for common patterns
4. **Documentation** - Comment complex configurations

## Advanced Features

### Matrix Builds

```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
  script:
    - docker run --rm node:${NODE_VERSION} npm test
```

### Child Pipelines

```yaml
trigger-child:
  trigger:
    include: .gitlab-ci-child.yml
    strategy: depend
```

### Dynamic Pipelines

```yaml
generate-pipeline:
  stage: .pre
  script:
    - ./scripts/generate-pipeline.sh > generated.yml
  artifacts:
    paths:
      - generated.yml

run-generated:
  trigger:
    include:
      - artifact: generated.yml
        job: generate-pipeline
```

## Monitoring

### Pipeline Metrics

Track in GitLab Analytics:
- Pipeline success rate
- Average duration
- Job failure rates
- Coverage trends

### Dashboards

```yaml
# Export metrics to Prometheus
metrics:
  stage: .post
  script:
    - echo "pipeline_duration_seconds{status=\"${CI_JOB_STATUS}\"} ${CI_PIPELINE_DURATION}" > metrics.txt
  artifacts:
    reports:
      metrics: metrics.txt
```

## Troubleshooting

### Common Issues

**Cache not working:**
```yaml
# Ensure cache key is consistent
cache:
  key: ${CI_COMMIT_REF_SLUG}
  policy: pull-push  # Default behavior
```

**Jobs timing out:**
```yaml
# Increase timeout
job-name:
  timeout: 2h  # Default is 1h
```

**Artifacts too large:**
```yaml
# Compress or exclude files
artifacts:
  paths:
    - dist/*.min.js  # Only minified
  exclude:
    - dist/**/*.map  # Exclude source maps
```

**Docker connection issues:**
```yaml
# Use proper Docker configuration
services:
  - docker:dind
variables:
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_VERIFY: 1
```

## Comparison with GitHub Actions

| Feature | GitLab CI | GitHub Actions |
|---------|-----------|----------------|
| Configuration | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| Runners | Shared/Specific | GitHub-hosted/Self-hosted |
| Caching | Built-in | actions/cache |
| Artifacts | Native | actions/upload-artifact |
| Environments | First-class | environments |
| Review Apps | Built-in | Manual setup |
| Cost (Free Tier) | 400 min/month | 2000 min/month |

## Related Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Pipeline Configuration Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [Security Scanning](https://docs.gitlab.com/ee/user/application_security/)

## Contributing

To improve this template:
1. Test with real projects
2. Add language-specific examples
3. Share optimization tips
4. Report issues
5. Submit merge requests

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

# ADR-003: GitHub Actions for CI/CD

## Status

Accepted

## Context

We need a CI/CD platform for:

1. Running tests on notebooks and templates
2. Building and deploying Jupyter Book documentation
3. Scheduled notebook execution
4. Template validation
5. Security scanning (future)
6. Artifact generation and signing (future)

Several CI/CD platforms were considered:

- GitHub Actions
- GitLab CI
- Azure Pipelines
- Jenkins
- CircleCI
- Travis CI

Requirements:

- Native GitHub integration
- Free tier for open source
- YAML configuration
- Matrix builds
- Secrets management
- Good marketplace/ecosystem
- Multi-platform support

## Decision

We will use **GitHub Actions** as the primary CI/CD platform for Agentic Canon, while providing examples for Azure Pipelines to support multi-platform strategies.

## Rationale

### Why GitHub Actions?

1. **Native Integration**: Seamless integration with GitHub
   - No external service setup required
   - Direct access to GitHub APIs
   - Native support for GitHub features

2. **Cost**: Free for public repositories
   - Generous free tier
   - Cost-effective for our use case
   - No credit card required for public repos

3. **Ecosystem**: Rich marketplace of actions
   - Reusable actions from community
   - Official actions from vendors
   - Easy to create custom actions

4. **Developer Experience**:
   - YAML-based configuration
   - Matrix builds for multiple versions
   - Workflow visualization
   - Debugging capabilities
   - Good documentation

5. **Features**:
   - Container support
   - Service containers
   - Secrets management
   - Environment protection rules
   - Reusable workflows

6. **Performance**:
   - Fast startup times
   - Concurrent jobs
   - Good runner performance
   - GitHub-hosted and self-hosted runners

### Workflow Organization

```
.github/workflows/
├── notebooks-test.yml         # Test notebook execution
├── cookiecutters-test.yml    # Validate template rendering
├── book-deploy.yml           # Build and deploy Jupyter Book
├── notebooks-schedule.yml    # Scheduled notebook runs
└── repo-guardrails.yml       # Repository quality checks
```

Each workflow is:

- **Focused**: One responsibility per workflow
- **Testable**: Can be triggered manually
- **Documented**: Inline comments explain steps
- **Efficient**: Uses caching and parallel jobs

## Consequences

### Positive

- Zero setup cost for contributors
- Excellent GitHub integration
- Large ecosystem of actions
- Good documentation and community
- Free for open source projects
- Easy to test workflows
- YAML configuration is version-controlled
- Workflow logs are accessible
- Can use matrix builds for multiple versions

### Negative

- GitHub-specific (vendor lock-in)
- Runner limitations (time, resources)
- Requires internet connection
- Some features require paid tier
- Learning curve for advanced features
- YAML can become complex

### Mitigations

- Provide Azure Pipelines examples for organizations using Azure DevOps
- Document common patterns and best practices
- Use reusable workflows to reduce duplication
- Keep workflows simple and focused
- Add comments explaining complex steps
- Test workflows thoroughly

## Implementation

### Workflows Created

1. **notebooks-test.yml**
   - Runs on: PR, push to main
   - Purpose: Test notebook execution
   - Tools: pytest, nbmake
   - Duration: ~5 minutes

2. **cookiecutters-test.yml**
   - Runs on: PR, push to main
   - Purpose: Validate templates render
   - Tools: pytest-cookies
   - Duration: ~2 minutes

3. **book-deploy.yml**
   - Runs on: push to main
   - Purpose: Deploy Jupyter Book
   - Target: GitHub Pages
   - Duration: ~3 minutes

4. **notebooks-schedule.yml**
   - Runs on: schedule (weekly)
   - Purpose: Automated notebook execution
   - Tools: papermill
   - Duration: ~10 minutes

5. **repo-guardrails.yml**
   - Runs on: PR, push
   - Purpose: Repository quality checks
   - Tools: various linters
   - Duration: ~2 minutes

### Best Practices Implemented

1. **Caching**: Cache pip dependencies

   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
   ```

2. **Matrix Builds**: Test multiple Python versions

   ```yaml
   strategy:
     matrix:
       python-version: ["3.11", "3.12", "3.13"]
   ```

3. **Concurrency**: Prevent duplicate runs

   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```

4. **Secrets**: Use GitHub Secrets for sensitive data
   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   ```

## Multi-Platform Support

While GitHub Actions is primary, we provide examples for:

### Azure Pipelines

Located in `examples/azure-pipelines/`:

- Python service pipeline
- Node.js service pipeline
- Documentation on usage
- Migration guide from GitHub Actions

Benefits:

- Organizations using Azure DevOps
- Integration with Azure services
- Enterprise features

### Future Platforms

Planned examples:

- GitLab CI (for GitLab users)
- CircleCI (for specific use cases)
- Jenkins (for on-premise)

## Alternatives Considered

### 1. GitLab CI

**Pros**:

- Integrated with GitLab
- Good feature set
- Free for open source

**Cons**:

- Requires GitLab account
- Less relevant for GitHub projects
- Smaller ecosystem

### 2. Azure Pipelines

**Pros**:

- Enterprise features
- Azure integration
- Free for open source

**Cons**:

- External service
- Setup complexity
- Less GitHub integration

### 3. CircleCI

**Pros**:

- Good performance
- Nice UI
- Good caching

**Cons**:

- Cost for private repos
- External service
- Setup required

### 4. Jenkins

**Pros**:

- Self-hosted
- Very flexible
- Large ecosystem

**Cons**:

- Maintenance burden
- Complex setup
- Resource intensive

### 5. Travis CI

**Pros**:

- Simple setup
- Good for open source

**Cons**:

- Pricing changes
- Less feature-rich
- Declining popularity

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Azure Pipelines](https://azure.microsoft.com/en-us/services/devops/pipelines/)

## Notes

- Aligns with Version 1.0 goals in TASKS.md
- Workflows follow security best practices
- Can be extended with custom actions
- Consider self-hosted runners for resource-intensive jobs
- GitHub Actions is the standard for GitHub-hosted projects

## Future Enhancements

Planned additions:

- Security scanning workflows (CodeQL, Semgrep)
- SBOM generation workflows
- Artifact signing with Sigstore
- Performance testing workflows
- Multi-cloud deployment workflows

---

**Date**: 2025-10-11  
**Author**: Jonathan Boardman (@IAmJonoBo)  
**Status**: Accepted

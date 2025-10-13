# Setting Up CI/CD Pipelines

**Duration:** 10-12 minutes  
**Target Audience:** Developers ready to automate their workflow  
**Prerequisites:** Generated project from Agentic Canon

---

## Script Outline

### Introduction (30 seconds)

"In this tutorial, we'll explore the CI/CD pipelines that come with Agentic Canon projects. You'll learn how they work, how to customize them, and how to leverage them for maximum automation."

---

### Understanding the CI/CD Architecture (2 minutes)

**[Screen: Diagram showing pipeline flow]**

"Agentic Canon projects include three main workflows:"

1. **CI Pipeline (ci.yml)**
   - Runs on every push and pull request
   - Multi-version Python testing (3.11, 3.12)
   - Code coverage with Codecov
   - Quality gates enforcement

2. **Security Pipeline (security.yml)**
   - CodeQL analysis
   - Secret scanning with Gitleaks
   - Dependency vulnerability checks
   - SBOM generation
   - Runs on push and schedule

3. **Documentation Pipeline (docs.yml)**
   - Builds Jupyter Book
   - Deploys to GitHub Pages
   - Runs on pushes to main

**[Screen: Show .github/workflows/ directory]**

---

### The CI Pipeline Deep Dive (3 minutes)

**[Screen: Code editor showing ci.yml]**

"Let's examine the CI pipeline in detail:"

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Explain:**

- Trigger conditions
- Matrix testing strategy
- Checkout and setup steps
- Dependency installation
- Test execution
- Coverage reporting

**[Screen: Show pipeline running in GitHub Actions]**

---

### Security Pipeline Configuration (2 minutes)

**[Screen: Code editor showing security.yml]**

"The security pipeline has multiple jobs:"

```yaml
jobs:
  codeql:
    # Static code analysis

  gitleaks:
    # Secret scanning

  dependency-review:
    # Check for vulnerable dependencies

  sbom:
    # Generate Software Bill of Materials
```

**Demo:**

- CodeQL security findings
- Gitleaks secret detection
- Dependency vulnerability report
- Generated SBOM artifact

**[Screen: GitHub Security tab]**

---

### Customizing Workflows (2 minutes)

**[Screen: Code editor]**

"Common customizations:"

1. **Add new test steps**

   ```yaml
   - name: Run integration tests
     run: pytest tests/integration/
   ```

2. **Change Python versions**

   ```yaml
   matrix:
     python-version: ["3.10", "3.11", "3.12"]
   ```

3. **Add deployment**

   ```yaml
   deploy:
     needs: test
     if: github.ref == 'refs/heads/main'
     steps:
       - name: Deploy to production
         run: ./deploy.sh
   ```

4. **Conditional jobs**
   ```yaml
   if: github.event_name == 'push'
   ```

---

### Setting Up GitHub Actions Secrets (1 minute)

**[Screen: GitHub Settings > Secrets]**

"Configure secrets for external services:"

```bash
# Required secrets:
- CODECOV_TOKEN          # Coverage reporting
- DOCKER_USERNAME        # Container registry
- DOCKER_PASSWORD
- DEPLOYMENT_TOKEN       # Deployment credentials
```

**Show:**

- Adding secrets in GitHub UI
- Using secrets in workflows
- Secret scope (repo vs org)

---

### Monitoring Pipeline Health (1 minute)

**[Screen: GitHub Actions dashboard]**

"Monitor your pipelines:"

- View workflow runs
- Check job status
- Review logs
- Download artifacts
- Re-run failed jobs

**Demo:**

- Successful run
- Failed run with logs
- Artifact download

---

### Azure Pipelines Alternative (1 minute)

**[Screen: Azure DevOps]**

"Agentic Canon also supports Azure Pipelines:"

```bash
# Copy Azure pipeline config
cp examples/azure-pipelines/python-service-pipeline.yml azure-pipelines.yml
```

**Show:**

- Azure pipeline structure
- Differences from GitHub Actions
- Setup in Azure DevOps

---

### Best Practices (1 minute)

1. **Always test locally first**

   ```bash
   act  # Test GitHub Actions locally
   ```

2. **Use caching for dependencies**

   ```yaml
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
   ```

3. **Fail fast for quick feedback**

   ```yaml
   strategy:
     fail-fast: true
   ```

4. **Use reusable workflows**
5. **Set up branch protection rules**
6. **Monitor workflow costs**

---

### Troubleshooting Common Issues (1 minute)

**[Screen: Terminal and GitHub Actions logs]**

Common problems and solutions:

1. **Tests pass locally but fail in CI**
   - Check Python version
   - Verify dependencies
   - Check environment variables

2. **Slow pipelines**
   - Use caching
   - Parallelize jobs
   - Optimize test suite

3. **Flaky tests**
   - Use pytest-retry
   - Add timeouts
   - Fix timing issues

---

### Conclusion (30 seconds)

"You now know how to:

- Understand CI/CD pipeline structure
- Customize workflows
- Set up secrets
- Monitor pipeline health
- Troubleshoot issues

Next: Learn about implementing security gates!"

---

## Key Files Reference

```
.github/workflows/
├── ci.yml          # Main CI pipeline
├── security.yml    # Security scanning
├── docs.yml        # Documentation build
└── notebooks-test.yml  # Notebook validation
```

---

## Useful Commands

```bash
# Test workflows locally with act
act -l                    # List workflows
act push                  # Test push event
act pull_request         # Test PR event

# GitHub CLI
gh workflow list         # List workflows
gh run list             # List recent runs
gh run watch            # Watch current run
gh run view <run-id>    # View specific run

# Validate workflow syntax
actionlint .github/workflows/*.yml
```

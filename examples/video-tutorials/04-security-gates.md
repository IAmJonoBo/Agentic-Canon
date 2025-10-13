# Video Tutorial Script: Implementing Security Gates

**Duration:** 12-15 minutes  
**Target Audience:** Developers, DevSecOps Engineers, Security Champions  
**Prerequisites:** Basic understanding of CI/CD, familiarity with GitHub Actions

---

## Introduction (1 minute)

### Opening (15 seconds)

"Welcome back to the Agentic Canon tutorial series! In this video, we'll explore how to implement comprehensive security gates in your development workflow. Security isn't just a final check—it's baked into every step of your process."

### What You'll Learn (45 seconds)

By the end of this tutorial, you'll be able to:

- Implement SAST (Static Application Security Testing)
- Set up secret scanning to prevent credential leaks
- Generate Software Bills of Materials (SBOM)
- Configure dependency vulnerability scanning
- Create security-focused CI/CD pipelines

"Let's dive in and make security an automated, integral part of your workflow!"

---

## Section 1: Understanding Security Gates (2 minutes)

### Security Gate Overview (1 minute)

"Security gates are automated checkpoints in your CI/CD pipeline that prevent insecure code from reaching production. Think of them as guardrails that catch issues before they become vulnerabilities."

**Key Security Gates:**

1. **SAST** - Analyzes source code for security vulnerabilities
2. **Secret Scanning** - Detects hardcoded secrets and credentials
3. **Dependency Scanning** - Identifies vulnerable dependencies
4. **SBOM Generation** - Creates inventory of software components
5. **Container Scanning** - Checks container images for vulnerabilities

### The Security Workflow (1 minute)

"In Agentic Canon, security gates are implemented at multiple stages:"

```
Developer commits code
    ↓
Pre-commit hooks (local)
    ↓
SAST scanning (PR)
    ↓
Secret scanning (PR)
    ↓
Dependency review (PR)
    ↓
Build & SBOM generation
    ↓
Container scanning
    ↓
Deployment (with provenance)
```

---

## Section 2: SAST with CodeQL (3 minutes)

### Setting Up CodeQL (1.5 minutes)

"Let's start with CodeQL, GitHub's semantic code analysis engine."

**Show on screen: `.github/workflows/security.yml`**

```yaml
name: Security Scanning

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1" # Weekly Monday scan

jobs:
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    strategy:
      matrix:
        language: ["python", "javascript"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: security-extended

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

"CodeQL runs on every PR, push to main, and weekly. It uses semantic analysis to find vulnerabilities like SQL injection, XSS, and path traversal."

### Understanding CodeQL Results (1.5 minutes)

**Show on screen: GitHub Security tab**

"CodeQL findings appear in the Security tab. Each finding includes:"

- Severity level (Critical, High, Medium, Low)
- Detailed explanation of the vulnerability
- Example code path showing data flow
- Recommended fixes

**Demo: Click through a sample finding**

"You can configure CodeQL to block PRs with critical/high severity findings. This ensures vulnerabilities never make it to main."

---

## Section 3: Secret Scanning (2.5 minutes)

### Why Secret Scanning Matters (30 seconds)

"Hardcoded secrets are one of the most common security mistakes. API keys, passwords, and tokens accidentally committed to repositories can be exploited within minutes."

### Setting Up Gitleaks (1.5 minutes)

**Show on screen: `.github/workflows/security.yml` (continued)**

```yaml
secrets:
  name: Secret Scanning
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Run Gitleaks
      uses: gitleaks/gitleaks-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

"Gitleaks scans your entire repository history for over 140 types of secrets including:"

- AWS credentials
- GitHub tokens
- Private keys
- Database passwords
- API keys

### Pre-commit Hook Protection (30 seconds)

**Show on screen: `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

"Pre-commit hooks catch secrets before they're committed. This is your first line of defense."

---

## Section 4: Dependency Scanning (2 minutes)

### Dependency Vulnerabilities (30 seconds)

"Third-party dependencies are essential but can introduce vulnerabilities. Dependency scanning identifies known CVEs in your packages."

### Configuring Dependency Review (1.5 minutes)

**Show on screen: `.github/workflows/dependency-review.yml`**

```yaml
name: Dependency Review

on: [pull_request]

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
```

**Show on screen: `renovate.json`**

```json
{
  "extends": ["config:recommended"],
  "schedule": ["before 3am on Monday"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "schedule": ["at any time"]
  }
}
```

"Renovate automatically creates PRs for dependency updates, with a focus on security patches."

---

## Section 5: SBOM Generation (2 minutes)

### Understanding SBOMs (45 seconds)

"An SBOM—Software Bill of Materials—is an inventory of all components in your software. It's essential for:"

- Compliance and auditing
- Vulnerability tracking
- Supply chain security
- License compliance

### Generating SBOMs (1 minute 15 seconds)

**Show on screen: SBOM workflow**

```yaml
sbom:
  name: Generate SBOM
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Generate SBOM
      uses: anchore/sbom-action@v0.20.6
      with:
        path: .
        format: spdx-json
        output-file: sbom.spdx.json
        artifact-name: sbom-spdx-json
        upload-artifact: true
        upload-release-asset: false

    - name: Scan SBOM for vulnerabilities
      uses: anchore/scan-action@v7.0.0
      with:
        sbom: sbom.spdx.json
        fail-build: false
        severity-cutoff: medium
        output-format: json
        output-file: scan-results.json
        cache-results: true

    - name: Summarise results
      run: |
        {
          echo "Generated SBOM: sbom.spdx.json"
          echo
          echo "| Severity | Findings |"
          echo "| --- | --- |"
          if [ -f scan-results.json ] && jq -e '.matches | length > 0' scan-results.json >/dev/null 2>&1; then
            jq -r '.matches[].vulnerability.severity' scan-results.json \
              | tr '[:lower:]' '[:upper:]' \
              | sort \
              | uniq -c \
              | awk '{printf("| %s | %s |\n", $2, $1)}'
          else
            echo "| NONE | 0 |"
          fi
        } >> "$GITHUB_STEP_SUMMARY"
```

"This generates an SPDX SBOM, scans it with the latest Grype engine, and writes a severity summary to the job log."

---

## Section 6: Putting It All Together (3 minutes)

### Complete Security Pipeline (1.5 minutes)

**Show on screen: Full security.yml workflow**

"Here's how all the pieces work together:"

1. **Pre-commit** - Catches secrets locally
2. **PR Checks** - CodeQL + Gitleaks + Dependency Review
3. **Build** - SBOM generation
4. **Post-build** - Container scanning
5. **Deployment** - Sign artifacts with provenance

**Demo: Show PR with all security checks**

### Configuring Security Policies (1 minute)

**Show on screen: Branch protection rules**

"You can require all security checks to pass before merging:"

- Go to Settings → Branches → Branch protection rules
- Check "Require status checks to pass"
- Select: CodeQL, Secret Scanning, Dependency Review

### Monitoring Security Metrics (30 seconds)

**Show on screen: Security dashboard**

"Agentic Canon includes Grafana dashboards for security metrics:"

- Vulnerability trends over time
- Mean time to remediate
- SBOM coverage
- Security scan results

---

## Section 7: Best Practices & Tips (2 minutes)

### Security Best Practices (1 minute)

1. **Run security scans on every PR** - Don't wait for main branch
2. **Fix critical/high findings immediately** - Use security SLAs
3. **Keep dependencies updated** - Enable automated updates
4. **Rotate secrets regularly** - Use secret management services
5. **Monitor security metrics** - Track MTTR for vulnerabilities
6. **Educate your team** - Security is everyone's responsibility

### Common Pitfalls (45 seconds)

❌ **Don't:**

- Skip security scans to speed up deployment
- Ignore low/medium findings indefinitely
- Hardcode secrets even for development
- Disable security checks without review

✅ **Do:**

- Fail builds on critical/high vulnerabilities
- Review and triage all findings
- Use environment variables or secret managers
- Document security exceptions

### Troubleshooting (15 seconds)

"Common issues and solutions are documented in our Security Policy at SECURITY.md"

---

## Conclusion (1 minute)

### Recap (30 seconds)

"Today we covered:"

- ✅ Setting up SAST with CodeQL
- ✅ Implementing secret scanning with Gitleaks
- ✅ Configuring dependency scanning
- ✅ Generating SBOMs for supply chain security
- ✅ Building a complete security pipeline

### Next Steps (30 seconds)

"In the next video, we'll explore observability—how to instrument your services with OpenTelemetry and set up SLOs."

**Show on screen:**

- 📚 Read the Security Policy: SECURITY.md
- 🔗 Example workflows: examples/dashboards/security-metrics.json
- 📖 Full documentation: docs/notebooks/02_security_supply_chain.md
- 💬 Join the discussion on GitHub

"Thanks for watching, and remember: security is a journey, not a destination. Happy securing!"

---

## YouTube Description Template

```
🔒 Implementing Security Gates with Agentic Canon

Learn how to build comprehensive security into your CI/CD pipeline with automated security gates. This tutorial covers SAST, secret scanning, dependency scanning, and SBOM generation.

⏱️ Timestamps:
0:00 - Introduction
1:00 - Understanding Security Gates
3:00 - SAST with CodeQL
6:00 - Secret Scanning with Gitleaks
8:30 - Dependency Scanning
10:30 - SBOM Generation
12:30 - Complete Security Pipeline
15:30 - Best Practices & Tips
16:30 - Conclusion

🔗 Resources:
- Repository: https://github.com/IAmJonoBo/Agentic-Canon
- Security Policy: SECURITY.md
- Security Dashboards: examples/dashboards/security-metrics.json
- Documentation: docs/notebooks/02_security_supply_chain.md

📚 Related Videos:
- Getting Started with Agentic Canon
- Creating Services with Cookiecutter
- Setting up CI/CD Pipelines

#DevSecOps #Security #CICD #GitHub #CodeQL #SAST #SecretScanning
```

---

## Social Media Snippets

**Twitter/X:**
"🔒 New tutorial: Implementing Security Gates with Agentic Canon! Learn how to automate SAST, secret scanning, dependency scanning, and SBOM generation in your CI/CD pipeline. #DevSecOps #Security"

**LinkedIn:**
"Excited to share our latest tutorial on implementing comprehensive security gates in CI/CD pipelines! Learn how to use CodeQL, Gitleaks, and automated dependency scanning to build security into your development workflow. Check it out!"

**Reddit (r/devops, r/netsec):**
"Tutorial: Implementing Security Gates in CI/CD - Covers SAST with CodeQL, secret scanning with Gitleaks, dependency scanning, and SBOM generation. All integrated into GitHub Actions workflows."

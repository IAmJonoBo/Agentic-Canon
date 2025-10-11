---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 02 Security & Supply Chain

This notebook covers:
- SAST (Static Application Security Testing)
- Secret scanning
- SBOM generation and validation
- Provenance attestation with in-toto
- SLSA compliance

```{code-cell} ipython3
:tags: [parameters]

# Parameters cell for Papermill
run_mode = "interactive"
```

## SAST - Static Application Security Testing

Use tools like CodeQL, Semgrep, or language-specific analyzers to find security vulnerabilities in code.

```{code-cell} ipython3
sast_tools = {
    "CodeQL": "GitHub's semantic code analysis engine",
    "Semgrep": "Fast, open-source SAST tool",
    "Bandit": "Python security linter",
    "ESLint": "JavaScript/TypeScript linter with security rules",
    "gosec": "Go security checker"
}

print("Recommended SAST Tools:")
for tool, desc in sast_tools.items():
    print(f"  • {tool}: {desc}")
```

## Secret Scanning

Detect leaked credentials, API keys, and tokens before they reach production.

```{code-cell} ipython3
secret_scanners = {
    "Gitleaks": "Fast secret scanner for git repositories",
    "TruffleHog": "Find secrets in git history",
    "detect-secrets": "Baseline secrets detection"
}

print("Secret Scanning Tools:")
for tool, desc in secret_scanners.items():
    print(f"  • {tool}: {desc}")
```

## SBOM - Software Bill of Materials

Generate SBOM in CycloneDX or SPDX format to track all dependencies.

```{code-cell} ipython3
import json

# CycloneDX SBOM example
sbom = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "metadata": {
        "timestamp": "2024-01-01T00:00:00Z",
        "tools": [{"name": "cyclonedx-python", "version": "3.11.0"}]
    },
    "components": [
        {
            "type": "library",
            "name": "requests",
            "version": "2.31.0",
            "purl": "pkg:pypi/requests@2.31.0",
            "licenses": [{"license": {"id": "Apache-2.0"}}]
        }
    ]
}

print("CycloneDX SBOM Structure:")
print(json.dumps(sbom, indent=2))
```

## Provenance with in-toto

Generate provenance attestations to track the build process and ensure integrity.

```{code-cell} ipython3
provenance_example = {
    "_type": "https://in-toto.io/Statement/v0.1",
    "subject": [{"name": "artifact.tar.gz", "digest": {"sha256": "abc123..."}}],
    "predicateType": "https://slsa.dev/provenance/v0.2",
    "predicate": {
        "builder": {"id": "https://github.com/actions"},
        "buildType": "https://github.com/actions/workflow@v1",
        "materials": [{"uri": "git+https://github.com/repo", "digest": {"sha1": "def456..."}}]
    }
}

print("in-toto Provenance Structure:")
print(json.dumps(provenance_example, indent=2))
```

## SLSA Compliance

Supply-chain Levels for Software Artifacts (SLSA) framework for supply chain security.

```{code-cell} ipython3
slsa_levels = {
    "SLSA 1": "Documentation of build process",
    "SLSA 2": "Tamper-resistant build platform + signed provenance",
    "SLSA 3": "Hardened builds + non-falsifiable provenance",
    "SLSA 4": "Two-party review + hermetic, reproducible builds"
}

print("SLSA Levels:")
for level, desc in slsa_levels.items():
    print(f"  • {level}: {desc}")

print("\nTarget: Achieve SLSA Level 3 for production builds")
```

## GitHub Actions Security Workflows

Example workflows for security scanning:

```{code-cell} ipython3
workflow_example = """
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
      - name: Run CodeQL
        uses: github/codeql-action/init@v2
      - name: Build
        run: make build
      - name: CodeQL Analysis
        uses: github/codeql-action/analyze@v2
"""

print("Example Security Workflow:")
print(workflow_example)
```

```{code-cell} ipython3
print(f"Security & Supply Chain notebook complete! (mode: {run_mode})")
```

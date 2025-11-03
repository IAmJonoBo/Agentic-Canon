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

# 01 Bootstrap: Repository Scaffolding & Quality Gates

This notebook demonstrates how to:

- Scaffold a new repository with best practices
- Enable quality gates (linting, testing, security)
- Generate SBOM (Software Bill of Materials)
- Demonstrate artifact signing with Sigstore/Cosign

## Parameters

This notebook is parameterized for Papermill execution.

```{code-cell} ipython3
:tags: [parameters]

# Parameters cell for Papermill
run_mode = "interactive"  # Options: interactive, ci, demo
```

## Repository Scaffolding

Use Cookiecutter to scaffold a new project with all best practices included:

```{code-cell} ipython3
import subprocess
import json
from pathlib import Path

print(f"Running in {run_mode} mode")

# Example: List available templates
templates_dir = Path("../templates")
if templates_dir.exists():
    templates = [t.name for t in templates_dir.iterdir() if t.is_dir()]
    print(f"Available templates: {templates}")
else:
    print("Templates directory not found. Run this from the repository root.")
```

## Quality Gates

Essential quality gates for every project:

1. **Linting**: Enforce code style (pylint, eslint, golangci-lint)
2. **Testing**: Unit tests, integration tests, coverage ≥ 80%
3. **Security Scanning**: SAST, secret scanning, dependency checks
4. **SBOM Generation**: Track all dependencies
5. **Artifact Signing**: Sign releases for supply chain security

```{code-cell} ipython3
# Example quality gate checks
quality_gates = {
    "linting": "Format and style compliance",
    "unit_tests": "Test coverage ≥ 80%",
    "sast": "No high/critical security issues",
    "secrets": "No leaked credentials",
    "sbom": "CycloneDX SBOM generated",
    "signing": "Artifacts signed with cosign"
}

for gate, description in quality_gates.items():
    print(f"✓ {gate}: {description}")
```

## SBOM Generation

Generate Software Bill of Materials using CycloneDX format:

```{code-cell} ipython3
# Example SBOM structure
sbom_example = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "version": 1,
    "metadata": {
        "component": {
            "type": "application",
            "name": "example-service",
            "version": "1.0.0"
        }
    },
    "components": [
        {
            "type": "library",
            "name": "requests",
            "version": "2.31.0",
            "purl": "pkg:pypi/requests@2.31.0"
        }
    ]
}

print("SBOM Example:")
print(json.dumps(sbom_example, indent=2))
```

## Artifact Signing

Sign artifacts using Sigstore/Cosign for supply chain security:

```{code-cell} ipython3
# Example signing workflow
signing_steps = [
    "1. Install cosign: curl -O -L https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64",
    "2. Generate key pair: cosign generate-key-pair",
    "3. Sign artifact: cosign sign --key cosign.key artifact.tar.gz",
    "4. Verify signature: cosign verify --key cosign.pub artifact.tar.gz"
]

for step in signing_steps:
    print(step)
```

## Next Steps

1. Choose a template from `templates/`
2. Run `cookiecutter` to generate your project
3. Initialize git and push to GitHub
4. Enable GitHub Actions for automated quality gates
5. Configure GitHub Pages for documentation

See the next notebooks for security, testing, and observability setup.

```{code-cell} ipython3
print("Bootstrap notebook complete!")
print(f"Mode: {run_mode}")
```

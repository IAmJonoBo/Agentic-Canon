# SBOM & Vulnerability Scanning Workflow

Task #132 delivers a reusable GitHub Actions workflow that generates SBOMs using
Syft and scans them with Grype.

## Workflow Location

`/.github/workflows/sbom-scan.yml`

The workflow can be consumed in two ways:

```yaml
name: SBOM Scan

on:
  push:
    branches: [main]

jobs:
  call-sbom:
    uses: ./.github/workflows/sbom-scan.yml
```

Or run manually:

```text
GitHub UI → Actions → “Security • SBOM Scan” → Run workflow
```

### Inputs

- `target` (optional) – defaults to the repository contents. Supply an OCI
  image reference or a subdirectory path if needed.

### Outputs

- `sbom.spdx.json` uploaded as an artifact directly by `anchore/sbom-action@v0.20.6`.
- Severity counts (medium and above) written to the job summary by parsing the `anchore/scan-action@v7.0.0` JSON report.

## Local Reuse

Install the tooling:

```bash
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

syft . -o spdx-json=sbom.spdx.json
grype sbom.spdx.json
```

## Best Practices

- Trigger the workflow nightly or on push to critical branches.
- Store SBOM artifacts to trace dependency drift.
- Pair with the CLI `agentic-canon fix` routine (which runs the sanity check)
  for comprehensive guardrails.

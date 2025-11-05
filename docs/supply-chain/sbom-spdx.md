---
title: "SPDX SBOM Policy"
summary: "Defines how to generate, validate, and consume SPDX 3.x Software Bills of Materials as part of the release process."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - supply-chain
  - sbom
  - spdx
sources:
  - "https://spdx.dev/use/specifications/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/docs_legacy/sbom-workflow.md"
decision_records:
  - id: "DR-2025-11-05-SBOM"
    title: "Mandated SPDX 3.x SBOM generation and validation"
    link: "docs/supply-chain/sbom-spdx.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SPDX Specifications"
      url: "https://spdx.dev/use/specifications/"
      type: "primary"
    - name: "Legacy SBOM workflow"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/docs_legacy/sbom-workflow.md"
      type: "secondary"
    - name: "frontiers/policy/slsa-policy.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml"
      type: "secondary"
  methods:
    - "Integrated legacy SBOM guidance with updated SLSA policy requirements."
    - "Extended workflow to support SPDX 3.x fields and attestation."
  key_results:
    - "Step-by-step SBOM generation and validation instructions."
    - "Template snippet for SPDX 3.x JSON entries."
  uncertainty: "SPDX 3.0 tooling still emerging; some generators may lag the specification."
  safer_alternative: "Fallback to SPDX 2.3 while ensuring compatibility until tooling stabilises."
---

# SPDX SBOM Policy

## Summary

1. Requires SPDX 3.x SBOMs for all release artefacts, generated via Syft and stored with provenance.
2. Validates SBOMs against schema and ensures digest alignment with artefacts.
3. Integrates SBOM publishing into release notes and vulnerability scanning workflows.

## Generation Workflow

1. Run Syft via `frontiers/quality-gate.yml` or locally:
   ```bash
   syft . -o spdx-json=sbom.spdx.json --file sbom.spdx.json
   ```
2. For container images:
   ```bash
   syft ghcr.io/example/image:1.2.3 -o spdx-json=sbom.spdx.json
   ```
3. Upload SBOM to build artefacts, and attach cosign attestation (see signing guide).

## SPDX 3.x Snippet

```json
{
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "example-service",
  "spdxVersion": "SPDX-3.0",
  "creationInfo": {
    "created": "2025-11-05T08:00:00Z",
    "creators": ["Tool: syft@0.105.0", "Organization: n00-frontiers"]
  },
  "packages": [
    {
      "name": "fastapi",
      "versionInfo": "0.115.0",
      "supplier": "Organization: FastAPI",
      "downloadLocation": "pkg:pypi/fastapi@0.115.0",
      "checksums": [{ "algorithm": "SHA256", "checksumValue": "<digest>" }]
    }
  ]
}
```

## Validation

```bash
pip install spdx-tools
python -m spdx_tools.spdx.spdx_json_parser --file sbom.spdx.json
```

Or use `spdx-sbom-tool verify --input sbom.spdx.json --artifact ghcr.io/example/image:1.2.3`.

## Consumption

1. Submit SBOM to vulnerability scanners (Grype, Trivy).
2. Publish SBOM link in release notes.
3. Provide SBOM to downstream consumers via secure artefact repository.

## Retention & Access

- Store under `artifacts/sbom/<release-id>/sbom.spdx.json` (retain 3 years).
- Access controlled through release engineering group; log downloads.

## Decision Records

- **DR-2025-11-05-SBOM** — Supply-chain guild enforced SPDX 3.x requirement.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://spdx.dev/use/specifications/">SPDX specifications</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/docs_legacy/sbom-workflow.md">Legacy SBOM workflow</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml">SLSA policy</a><br>
<strong>Methods:</strong> Updated legacy workflow to align with SPDX 3.x schema and SLSA policy; added validation commands.<br>
<strong>Key results:</strong> Generation steps, JSON snippet, validation guidance, retention policy.<br>
<strong>Uncertainty:</strong> Tooling for SPDX 3.x still maturing.<br>
<strong>Safer alternative:</strong> Use SPDX 2.3 fallback while ensuring compatibility until tooling stabilises.
</div>

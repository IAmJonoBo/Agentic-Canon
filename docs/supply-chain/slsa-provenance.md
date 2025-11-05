---
title: "SLSA Provenance"
summary: "Explains how n00-frontiers meets SLSA v1.0 Level 3 requirements using provenance attestations and secure build pipelines."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - supply-chain
  - slsa
  - provenance
sources:
  - "https://slsa.dev/spec/v1.0/provenance"
  - "https://docs.sigstore.dev/cosign/"
decision_records:
  - id: "DR-2025-11-05-SLSA"
    title: "Committed to SLSA Level 3 for release artefacts"
    link: "docs/supply-chain/slsa-provenance.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SLSA v1.0 provenance specification"
      url: "https://slsa.dev/spec/v1.0/provenance"
      type: "primary"
    - name: "frontiers/policy/slsa-policy.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml"
      type: "secondary"
  methods:
    - "Translated policy YAML requirements into actionable steps for pipeline teams."
    - "Validated against cosign/in-toto documentation."
  key_results:
    - "Level 3 control checklist, pipeline architecture, and verification commands."
  uncertainty: "Cosign keyless workflow availability may vary by environment; plan fallback with KMS keys."
  safer_alternative: "Use dedicated hardware-backed keys if Fulcio unavailability is a risk."
---

# SLSA Provenance

## Summary

1. Requires SLSA Level 3 provenance for all build artefacts, including container images, packages, and model artefacts.
2. Uses cosign with OIDC identity to generate in-toto provenance attestations stored under `artifacts/provenance/`.
3. Documents verification steps to run before deployment, ensuring artefact integrity and supply-chain trust.

## Level 3 Checklist

| Control        | Requirement                                    | Implementation                                                    |
| -------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| Source control | Verified, versioned source with review         | GitHub protected branches, CODEOWNERS enforcement                 |
| Build service  | Isolated, ephemeral runners                    | GitHub Actions hosted runners with ephemeral environment          |
| Provenance     | In-toto SLSA predicate, signed                 | `frontiers/quality-gate.yml#provenance` with cosign attest        |
| Access control | No manual changes to build outputs             | Build outputs stored in artifact store; manual changes prohibited |
| Verification   | Verify signatures and provenance before deploy | Deployment pipeline runs `cosign verify-attestation`              |

## Pipeline Overview

1. Workflow triggered on tag or release branch.
2. Build jobs produce artefacts (container image, wheel, etc.).
3. SBOM generated with Syft; stored as `sbom.spdx.json`.
4. Cosign signs both artefact and provenance predicate (OIDC identity).
5. Artefacts uploaded to registry along with attestations.

## Verification Commands

```bash
# Verify image signature
cosign verify --certificate-identity $OIDC_ID --certificate-oidc-issuer $OIDC_ISSUER $IMAGE_REF

# Verify SLSA provenance attestation
cosign verify-attestation --type slsa-provenance --certificate-oidc-issuer $OIDC_ISSUER $IMAGE_REF

# Validate SBOM matches digest
spdx-sbom-tool verify --input sbom.spdx.json --artifact $IMAGE_REF
```

## Evidence & Storage

- `artifacts/provenance/` — Attestations, predicate JSON, verification logs (retain 3 years).
- `artifacts/sbom/` — SPDX SBOMs (retain 3 years).
- Deployment pipeline attaches verification output to release notes.

## Decision Records

- **DR-2025-11-05-SLSA** — Platform and security teams mandated SLSA Level 3 compliance.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://slsa.dev/spec/v1.0/provenance">SLSA v1.0 specification</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml">SLSA policy</a>; <a href="https://docs.sigstore.dev/cosign/">Cosign documentation</a><br>
<strong>Methods:</strong> Converted policy YAML into pipeline steps and verification commands; aligned with cosign guidance.<br>
<strong>Key results:</strong> Level 3 checklist, pipeline overview, verification commands, evidence retention guidance.<br>
<strong>Uncertainty:</strong> Keyless signing availability may fluctuate.<br>
<strong>Safer alternative:</strong> Use hardware-backed keys if OIDC-based signing is unavailable.
</div>

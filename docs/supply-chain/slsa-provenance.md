---
title: "SLSA Provenance"
summary: "Explains how n00-frontiers meets SLSA v1.1 Level 3 requirements using provenance attestations and secure build pipelines."
version: "1.1.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - supply-chain
  - slsa
  - provenance
sources:
  - "https://slsa.dev/spec/v1.1/provenance"
  - "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
  - "https://docs.sigstore.dev/cosign/"
decision_records:
  - id: "DR-2025-11-05-SLSA"
    title: "Committed to SLSA Level 3 for release artefacts"
    link: "docs/supply-chain/slsa-provenance.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SLSA v1.1 provenance specification"
      url: "https://slsa.dev/spec/v1.1/provenance"
      type: "primary"
    - name: "SLSA 1.1 release announcement"
      url: "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
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

1. Requires SLSA Level 3 provenance for all build artefacts, including container images, packages, model weights, and benchmark datasets.citeturn7view0
2. Uses cosign with OIDC identity to generate in-toto provenance attestations stored under `artifacts/provenance/`, aligning with SLSA 1.1’s tightened builder identity and metadata requirements.citeturn6view0
3. Documents verification steps to run before deployment, ensuring artefact integrity and providing a migration path toward forthcoming SLSA 1.2 policy profiles.citeturn3search0

SLSA 1.1 emphasises explicit builder identity, richer metadata, and optional verification summaries; these changes are reflected in the policy and pipeline guidance here.citeturn6view0

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
5. Artefacts uploaded to registry along with provenance and optional SLSA verification-summary attestations.citeturn6view0

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

## Migration Notes

- Track the SLSA 1.2 release candidate effort and be prepared to adopt policy profiles that formalise organisational requirements.citeturn3search0
- Review downstream tooling compatibility (e.g., deployment platforms, artifact repositories) for the new verification-summary predicate published with SLSA 1.1.citeturn6view0

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://slsa.dev/spec/v1.1/provenance">SLSA v1.1 specification</a>; <a href="https://slsa.dev/blog/2025/04/slsa-1.1-is-here">SLSA 1.1 release</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml">SLSA policy</a>; <a href="https://docs.sigstore.dev/cosign/">Cosign documentation</a><br>
<strong>Methods:</strong> Converted policy YAML into pipeline steps and verification commands; aligned with SLSA 1.1 guidance and cosign documentation.<br>
<strong>Key results:</strong> Level 3 checklist, pipeline overview, verification commands, evidence retention guidance.<br>
<strong>Uncertainty:</strong> Keyless signing availability may fluctuate and SLSA 1.2 policy profiles are still stabilising.<br>
<strong>Safer alternative:</strong> Use hardware-backed keys if OIDC-based signing is unavailable.
</div>

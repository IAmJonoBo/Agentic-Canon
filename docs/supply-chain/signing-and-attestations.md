---
title: "Signing & Attestations"
summary: "Provides step-by-step guidance for signing artefacts with Sigstore cosign and generating in-toto attestations for builds, SBOMs, and tests."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - supply-chain
  - signing
  - attestations
sources:
  - "https://docs.sigstore.dev/cosign/"
  - "https://in-toto.io/"
decision_records:
  - id: "DR-2025-11-05-Signing"
    title: "Standardised signing and attestation workflow"
    link: "docs/supply-chain/signing-and-attestations.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Sigstore cosign documentation"
      url: "https://docs.sigstore.dev/cosign/"
      type: "primary"
    - name: "in-toto framework"
      url: "https://in-toto.io/"
      type: "primary"
    - name: "frontiers/policy/slsa-policy.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml"
      type: "secondary"
  methods:
    - "Combined cosign and in-toto guidance with SLSA policy requirements."
    - "Defined CLI snippets and CI integration steps for developers."
  key_results:
    - "Manual signing instructions, CI integration, and verification checklist."
  uncertainty: "Key rotation policy requires additional automation (backlog)."
  safer_alternative: "Until rotation automation exists, rotate keys manually every 90 days."
---

# Signing & Attestations

## Summary

1. Uses Sigstore cosign for signing container images, packages, and provenance statements.
2. Generates in-toto attestations for build, test, and SBOM steps to satisfy SLSA requirements.
3. Documents manual and automated verification workflows for developers and release engineers.

## Prerequisites

1. Install cosign: `brew install cosign` or follow platform-specific instructions.
2. Ensure access to signing key: keyless (OIDC) or key pair stored in secure vault.
3. For in-toto, install pipeline tooling or use `slsa-framework/slsa-github-generator` actions.

## Signing Workflow (Manual)

```bash
# Authenticate with keyless (GitHub Actions OIDC) or set COSIGN_PASSWORD for key-based signing
cosign login ghcr.io

# Sign container image
cosign sign --identity-token "$OIDC_TOKEN" ghcr.io/example/image:1.2.3

# Attach SBOM attestation
cosign attest --predicate sbom.spdx.json --type spdx --identity-token "$OIDC_TOKEN" ghcr.io/example/image:1.2.3
```

## In-toto Attestation Structure

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "subject": [
    { "name": "ghcr.io/example/image", "digest": { "sha256": "<digest>" } }
  ],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "https://github.com/Attestations/GitHubHostedActions@v1",
      "externalParameters": { "ref": "${{ github.ref }}" },
      "internalParameters": { "runner": "${{ runner.name }}" }
    },
    "runDetails": { "builder": { "id": "${{ github.workflow }}" } }
  }
}
```

## CI Integration

1. Add steps in `frontiers/quality-gate.yml#provenance` (copy to service-specific workflow).
2. Store signing secrets (`COSIGN_KEY`, `COSIGN_PASSWORD`) in GitHub Actions secrets.
3. Upload attestations and logs to `artifacts/provenance/`.
4. Gate deployment pipeline on successful verification.

## Verification Checklist

1. Verify signature identity and transparency log inclusion.
2. Confirm predicate references correct commit SHA and workflow path.
3. Ensure SBOM digest matches artefact digest.
4. Archive logs and verification report.

## Key Management

- Keyless: Use OIDC tokens (preferred). Ensure Fulcio and Rekor availability.
- Key pair: Store private key in managed secret vault; rotate every 90 days; audit via change management.
- Record public key fingerprint in `frontiers/policy/slsa-policy.yml`.

## Decision Records

- **DR-2025-11-05-Signing** — Release engineering approved unified signing and attestation workflow.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://docs.sigstore.dev/cosign/">Sigstore cosign documentation</a>; <a href="https://in-toto.io/">in-toto framework</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/slsa-policy.yml">SLSA policy</a><br>
<strong>Methods:</strong> Synthesised cosign and in-toto instructions with policy requirements to create actionable workflow.<br>
<strong>Key results:</strong> Manual and CI signing steps, attestation schema, verification checklist, key management guidance.<br>
<strong>Uncertainty:</strong> Key rotation automation pending.<br>
<strong>Safer alternative:</strong> Manual key rotation every 90 days until automation is built.
</div>

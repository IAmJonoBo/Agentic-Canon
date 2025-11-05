---
title: "Compliance Manifest"
summary: "Provides the machine-readable manifest format downstream teams use to declare alignment with the n00-frontiers documentation and policy set."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - governance
  - compliance
  - automation
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
decision_records:
  - id: "DR-2025-11-05-ComplianceManifest"
    title: "Adopted compliance manifest template and automation hooks"
    link: "docs/workflows/compliance-manifest.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SLSA 1.1 release"
      url: "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
      type: "primary"
    - name: "Compliance manifest template"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/compliance/manifest-template.yml"
      type: "secondary"
  methods:
    - "Modelled manifest entries after SSDF/SLSA policy references and new waiver automation."
  key_results:
    - "Documented required fields and lifecycle for compliance manifests."
  uncertainty: "Manifest schema may expand with new policy classes."
  safer_alternative: "Regenerate manifest per release when unsure."
---

# Compliance Manifest

## Summary

1. Each downstream repository publishes a `frontiers-compliance.yml` manifest derived from `frontiers/compliance/manifest-template.yml`.
2. Manifests pin documentation and policy hashes, list waiver files, and surface key contacts for audits.
3. Waiver automation (`tools/check_waivers.py`) and doc validation workflows consume the manifest to ensure nothing drifts.

## Required Fields

| Field              | Description                                                               |
| ------------------ | ------------------------------------------------------------------------- |
| `docs_version`     | Tag of the documentation release the repo complies with (e.g., `v1.1.0`). |
| `policies[]`       | List of policy IDs with source paths and SHA-256 hashes.                  |
| `tooling_versions` | Language and platform versions required to honour the policy set.         |
| `quality_gates`    | Reference to workflow definitions and dashboards enforcing compliance.    |
| `waivers[]`        | Link each active waiver with ID, control, and expiry (omit if none).      |
| `contacts`         | Named owner emails for platform, security, and compliance alignment.      |

## Workflow

1. Copy `frontiers/compliance/manifest-template.yml` into the downstream repo as `frontiers-compliance.yml`.
2. Run `python tools/check_waivers.py --manifest frontiers-compliance.yml` (coming soon) or manually update hashes:
   ```bash
   yq '.manifest.policies[].source' frontiers/compliance/manifest-template.yml \
     | xargs -I{} sh -c "printf \"  - id: %s\n    source: %s\n    hash: %s\n\" \"\${1}\" \"{}\" \"$(shasum -a 256 {})\"" _
   ```
3. Commit the manifest in the downstream repo and reference the docs version tag in release notes.
4. CI pipelines should verify the manifest on every build (future automation will provide a GitHub Action).

## Integration Hooks

- `.github/workflows/waiver-reminder.yml` uses the manifest + waiver directory to alert owners 7 days before expiry.
- Downstream repos can import `frontiers/policy/code-quality-tooling.yml` to configure their static/dynamic tooling.
- Platform dashboards link to `frontiers/compliance/manifest-template.yml` fields to surface compliance posture.

## Decision Records

- **DR-2025-11-05-ComplianceManifest** — Governance council approved the manifest template and automation bindings.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://slsa.dev/blog/2025/04/slsa-1.1-is-here">SLSA 1.1 release</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/compliance/manifest-template.yml">Compliance manifest template</a><br>
<strong>Methods:</strong> Mapped policy references and waiver automation to manifest fields.<br>
<strong>Key results:</strong> Manifest field definition, workflow guidance, integration hooks.<br>
<strong>Uncertainty:</strong> Schema will evolve with new policy classes.<br>
<strong>Safer alternative:</strong> Regenerate manifest when new policy versions publish.
</div>

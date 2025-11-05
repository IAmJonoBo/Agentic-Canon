---
title: "Evidence-Gated Protocol"
summary: "How to capture data, methods, and verification evidence so every page, workflow, and benchmark decision is auditable."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - evidence
  - governance
  - audit
sources:
  - "https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf"
  - "https://diataxis.fr/"
decision_records:
  - id: "DR-2025-11-05-Evidence"
    title: "Adopted Evidence-Gated Protocol for documentation and automation"
    link: "docs/overview/evidence-protocol.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "NIST AI RMF 1.0"
      url: "https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf"
      type: "primary"
    - name: "Diátaxis guide"
      url: "https://diataxis.fr/"
      type: "secondary"
    - name: "control-traceability-matrix.json"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
      type: "secondary"
  methods:
    - "Reconciled NIST AI RMF MAP/MEASURE/MANAGE/ GOVERN functions with AGENT-docs-job provenance requirements."
    - "Reviewed existing traceability matrix to ensure protocol covers evidence collection across disciplines."
  key_results:
    - "Defined five-step workflow for evidence capture tied to CI and documentation updates."
    - "Specified artefact retention expectations aligned with repository policies."
  uncertainty: "Automation scripts for schema validation and evidence attachments are planned but not yet implemented."
  safer_alternative: "Until automation lands, require manual review of provenance sections before merge."
---

# Evidence-Gated Protocol

## Summary

1. Every material change must surface verifiable evidence (data, methods, results) alongside written guidance.
2. Evidence capture integrates with CI outputs and policy YAML so auditors and agents can trace controls end-to-end.
3. Exceptions require recorded risk acceptance, owner approval, and retrospective remediation plans.

## Five-Step Workflow

1. **Plan** — Identify the control or decision affected. Log the intended change in `TASKS.md` with a link to the issue/DR.
2. **Collect** — Gather at least two independent data sources (official + secondary). Store raw artefacts under `artifacts/` with retention that matches `frontiers/policy/*.yml`.
3. **Analyse** — Document methods (scripts, queries, interviews). When scripts exist, commit them or link to reproducible notebooks.
4. **Decide** — Update the relevant Markdown page. Refresh front matter (`summary`, `version`, `last_verified`) and add bullet points to `key_results`.
5. **Verify** — Run `mkdocs build --strict` and the relevant CI jobs (quality gate, benchmarks). Attach run IDs or logs in the PR description.

## Required Artefacts

| Control Type       | Minimum Evidence                                   | Storage Location        | Retention |
| ------------------ | -------------------------------------------------- | ----------------------- | --------- |
| Secure SDLC (SSDF) | CI run logs, updated policy mapping                | `artifacts/security/`   | 3 years   |
| Supply-chain       | SPDX SBOM, in-toto attestations, cosign bundle     | `artifacts/provenance/` | 3 years   |
| Quality & Testing  | Coverage report, mutation score, benchmark summary | `artifacts/quality/`    | 12 months |
| AI Safety          | Benchmark outputs, guardrail configuration         | `artifacts/ai-safety/`  | 12 months |

## Templates

Use the following snippet when updating Markdown:

```markdown
## Provenance

<div class="provenance-block">
<strong>Data:</strong> [Primary Source], [Secondary Source]<br>
<strong>Methods:</strong> Method description...<br>
<strong>Key results:</strong> Outcome 1; Outcome 2.<br>
<strong>Uncertainty:</strong> Known gap.<br>
<strong>Safer alternative:</strong> Recommended fallback.
</div>
```

For machine-readable parity, update the front matter `provenance` object to mirror the same information.

## Exception Handling

1. Record the request in `docs/workflows/triage-and-exceptions.md`.
2. Tag the waiver with expiry date, owner, and residual risk.
3. Schedule a follow-up task in `TASKS.md` to revisit the waiver before expiry.
4. If evidence cannot be produced within SLA, escalate to the platform governance forum.

## Tooling Backlog

- `tools/validate_frontmatter.py` — Validate metadata against `frontiers.schema.json`.
- `tools/link_provenance_artifacts.py` — Cross-check that each data entry links to an artefact in `artifacts/`.
- `mkdocs serve --dirtyreload` integration to auto-highlight missing provenance blocks.

## Decision Records

- **DR-2025-11-05-Evidence** — Programme leadership mandated Evidence-Gated Protocol across all doc and policy updates.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf">NIST AI RMF 1.0</a>; <a href="https://diataxis.fr/">Diátaxis framework</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json">Control traceability matrix</a><br>
<strong>Methods:</strong> Mapped RMF functions to existing control-traceability entries; mirrored requirements into schema fields.<br>
<strong>Key results:</strong> Five-step evidence workflow; artefact storage table; automation backlog.<br>
<strong>Uncertainty:</strong> Automation enforcement scripts pending.<br>
<strong>Safer alternative:</strong> Require manual provenance review by Documentation Engineering before merging any page that lacks tooling support.
</div>

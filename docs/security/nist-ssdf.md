---
title: "NIST SSDF Implementation"
summary: "Maps NIST SP 800-218 v1.1 practice families to n00-frontiers processes, policies, and automation."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - security
  - ssdf
  - compliance
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
decision_records:
  - id: "DR-2025-11-05-SSDF"
    title: "Ratified SSDF alignment for n00-frontiers"
    link: "docs/security/nist-ssdf.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "NIST SP 800-218 Rev.1 (v1.1)"
      url: "https://csrc.nist.gov/pubs/sp/800/218/final"
      type: "primary"
    - name: "Control Traceability Matrix"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
      type: "secondary"
    - name: "frontiers/policy/ssdf-mapping.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/ssdf-mapping.yml"
      type: "secondary"
  methods:
    - "Reviewed SSDF practice families and mapped to the policy YAML plus automation steps."
    - "Cross-checked with control-traceability-matrix to ensure no gaps."
  key_results:
    - "Practice family table linking policy, automation, and evidence."
    - "Defined verification cadence and exception process."
  uncertainty: "Pending evaluation of new SSDF supplemental guidance for AI/GenAI workloads."
  safer_alternative: "Default to stricter controls where ambiguity exists (e.g., require manual review plus automated checks)."
---

# NIST SSDF Implementation

## Summary

1. Implements NIST SP 800-218 v1.1 across Plan (PO), Protect (PS), Produce (PW), and Respond (RV) practice families.
2. Uses `/frontiers/policy/ssdf-mapping.yml` as the authoritative machine-readable source for controls.
3. Couples policy with `/frontiers/quality-gate.yml` to automate verification and evidence capture.

## Practice Family Overview

| Family                              | Outcome                                                 | Implementation                                               | Evidence                                           | Automation                                     |
| ----------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- | ---------------------------------------------- |
| **PO** (Prepare the Organisation)   | Security requirements documented and communicated       | `FRAMEWORK.md`, this page, onboarding tutorials              | Signed Decision Records, onboarding checklist      | Linkcheck + schema validation in planned CI    |
| **PS** (Protect the Software)       | Access control, change management, integrity protection | Branch protection, signing policy, pre-commit hooks          | Cosign logs, GitHub branch protection exports      | `frontiers/quality-gate.yml#provenance`        |
| **PW** (Produce Secure Software)    | Secure design, coding, testing                          | Templates enforce lint, test, SAST, DAST, dependency hygiene | CI logs (CodeQL, Semgrep, Trivy), coverage reports | `frontiers/quality-gate.yml#sast`              |
| **RV** (Respond to Vulnerabilities) | Monitor, assess, respond                                | Incident response runbook, vulnerability triage workflow     | Incident postmortems, remediation issues           | Tasklist automation + security triage workflow |

## Control Highlights

1. **PO.1** — Security requirements defined in this page and `frontiers/policy/ssdf-mapping.yml`; training tracked quarterly.
2. **PS.2** — Repositories protected via admins-only force push, cosign-signed artefacts, and automation verifying provenance per release.
3. **PW.4** — Code review and analysis enforced via CodeQL + Semgrep; manual review uses ISO 25010 rubric.
4. **RV.1** — Security bulletins triaged within 24 hours; release verification uses in-toto and SBOM gating.

## Verification Cadence

- **Every PR**: Quality gate run, SARIF scan, coverage + mutation metrics.
- **Nightly**: Dependency updates (Renovate) and vulnerability scans (Trivy, Grype).
- **Quarterly**: Control effectiveness review documented in `docs/workflows/triage-and-exceptions.md`.

## Exceptions

- Request via `docs/workflows/triage-and-exceptions.md#security-waivers`.
- Minimum fields: control ID, risk rating, mitigation, expiry ≤ 30 days.
- Auto-reminder workflow (backlog) will comment on PR when waiver nearing expiry.

## Decision Records

- **DR-2025-11-05-SSDF** — Security leadership confirmed mapping and automation coverage for SSDF v1.1.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://csrc.nist.gov/pubs/sp/800/218/final">NIST SP 800-218 v1.1</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json">Control traceability matrix</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/ssdf-mapping.yml">SSDF machine mapping</a><br>
<strong>Methods:</strong> Mapped practice families to existing automation and machine-readable policy; validated coverage with traceability matrix.<br>
<strong>Key results:</strong> Practice overview, control highlights, verification cadence, waiver process.<br>
<strong>Uncertainty:</strong> Awaiting AI supplement finalisation.<br>
<strong>Safer alternative:</strong> Apply stricter controls until supplement clarifies expectations.
</div>

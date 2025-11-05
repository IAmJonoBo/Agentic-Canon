---
title: "OWASP ASVS Adoption"
summary: "Describes how the repository applies OWASP ASVS 4.0.3 controls, level selection, and verification cadence."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - security
  - asvs
  - compliance
sources:
  - "https://owasp.org/www-project-application-security-verification-standard/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/asvs-checklist.yml"
decision_records:
  - id: "DR-2025-11-05-ASVS"
    title: "Set ASVS level targets and controls"
    link: "docs/security/owasp-asvs.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "OWASP ASVS 4.0.3"
      url: "https://owasp.org/www-project-application-security-verification-standard/"
      type: "primary"
    - name: "ASVS checklist policy"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/asvs-checklist.yml"
      type: "secondary"
  methods:
    - "Mapped ASVS control families to repository workflows and templates."
    - "Classified systems into base vs internet-facing profiles with level expectations."
  key_results:
    - "Level selection guidance and verification cadence."
    - "Evidence expectations tied to automation outputs."
  uncertainty: "Future ASVS versions may adjust control numbering or severity."
  safer_alternative: "Default to L3 requirements when in doubt."
---

# OWASP ASVS Adoption

## Summary

1. Applies ASVS 4.0.3 Level 2 baseline for internal services and Level 3 for internet-facing workloads.
2. Captures machine-readable checklist requirements in `frontiers/policy/asvs-checklist.yml`.
3. Integrates ASVS evidence into PR review and security automation workflows.

## Level Selection

- **Base profile (L2)**: Services with authenticated internal usage only.
- **Internet-facing (L3)**: Public APIs, web applications, or services processing customer data.
- Level is recorded in service metadata (backlog: extend `catalog.json`).

## Control Coverage

| Section                      | Control Focus             | Implementation                                     | Evidence                               |
| ---------------------------- | ------------------------- | -------------------------------------------------- | -------------------------------------- |
| V1: Architecture             | SDLC and threat modelling | `FRAMEWORK.md`, threat modelling runbook           | Threat model artefacts, DR references  |
| V2: Authentication           | MFA, session management   | Template security modules, IdP integration guides  | Auth test suite, IdP config screenshot |
| V5: Validation, Sanitisation | Input/output validation   | Shared validation libs, property-based tests       | Test logs, schema definitions          |
| V7: Error handling           | Logging, redaction        | Observability stack, structured logging guidelines | Log redaction proof, runbook link      |
| V11: Business Logic          | Abuse cases               | ISO 25010 rubric, mutation testing                 | Mutation reports, abuse-case tests     |
| V14: Config                  | Secure defaults, secrets  | Vault integration, Terraform modules               | Terraform plan, secrets audit log      |

## Verification Cadence

- **Per PR**: Reviewers confirm relevant checklist items satisfied.
- **Weekly**: Security team samples 10% of merged PRs for spot checks.
- **Quarterly**: Full ASVS self-assessment with results stored in `artifacts/security/asvs/`.

## Evidence Checklist

1. Attach CodeQL/Semgrep summaries for V5 and V11.
2. Provide authentication test results or automation screenshot for V2.
3. Link to Terraform plan or configuration diff for V14.
4. Document threat model updates for significant architectural shifts.

## Decision Records

- **DR-2025-11-05-ASVS** — Security guild mandated L2 baseline, L3 for internet-facing, and machine-readable checklist.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS 4.0.3</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/asvs-checklist.yml">ASVS checklist policy</a><br>
<strong>Methods:</strong> Mapped ASVS sections to repo automation and evidence expectations; codified verification cadence.<br>
<strong>Key results:</strong> Level selection guidance, coverage table, evidence checklist.<br>
<strong>Uncertainty:</strong> Next ASVS revision may shift numbering.<br>
<strong>Safer alternative:</strong> Apply Level 3 requirements when uncertain.
</div>

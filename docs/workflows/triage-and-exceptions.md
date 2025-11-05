---
title: "Triage & Exceptions"
summary: "Explains how to triage issues, manage waivers, and enforce SLAs for risk acceptance across security, supply-chain, quality, and AI benchmarks."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - workflow
  - governance
  - exceptions
sources:
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/PROJECT_MANAGEMENT_QUICKREF.md"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/VERIFICATION_GUIDE.md"
decision_records:
  - id: "DR-2025-11-05-Triage"
    title: "Formalised triage and exception management flow"
    link: "docs/workflows/triage-and-exceptions.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Project management quick reference"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/PROJECT_MANAGEMENT_QUICKREF.md"
      type: "secondary"
    - name: "Verification guide"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/VERIFICATION_GUIDE.md"
      type: "secondary"
    - name: "frontiers/policy/*.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/tree/main/frontiers/policy"
      type: "secondary"
  methods:
    - "Consolidated automation behaviours with policy waiver requirements."
    - "Defined SLAs and escalation paths based on governance needs."
  key_results:
    - "Exception workflow, SLA table, and automation integration."
  uncertainty: "Automation for waiver reminders is planned but not yet implemented."
  safer_alternative: "Manually audit waivers weekly until automation is live."
---

# Triage & Exceptions

## Summary

1. Automates task and issue creation via TODO/tasklist/PR follow-up workflows.
2. Establishes standard waiver templates and SLAs for security, supply-chain, quality, and AI benchmark exceptions.
3. Defines escalation paths when risks remain unresolved beyond tolerated windows.

## Issue Triage Flow

1. **Capture** — TODO comments, `TASKS.md` checkboxes, and PR follow-ups automatically create issues via GitHub Actions.
2. **Label** — Automation applies labels (`from:todo`, `from:tasklist`, severity). Review and adjust if needed.
3. **Prioritise** — Assign owner, due date, and severity. Link to relevant documentation section.
4. **Verify** — Use steps in `VERIFICATION_GUIDE.md` to ensure automation is functioning.

## Waiver Template

```
### Risk Summary
- Control: e.g., SSDF PO.3.2 / Benchmark pass@1
- Reason: <explain constraint>
- Impact: <likelihood x impact>

### Mitigation
- Compensating control(s):
- Monitoring:

### Approval
- Owner:
- Approver:
- Expiry (YYYY-MM-DD):
- Follow-up issue:
```

Store waivers under relevant heading below; link to issue for traceability.
All active waivers must be represented by a YAML file in `frontiers/waivers/` so automation can monitor expirations.

## SLA Table

| Area                 | SLA     | Escalation                         | Tracking Location       |
| -------------------- | ------- | ---------------------------------- | ----------------------- |
| Security waivers     | 7 days  | Security steering committee        | `#security-waivers`     |
| Supply-chain waivers | 7 days  | Platform security lead             | `#supply-chain-waivers` |
| Benchmark waivers    | 14 days | AI safety guild                    | `#benchmark-waivers`    |
| LLM safety waivers   | 3 days  | Chief Information Security Officer | `#llm-waivers`          |

## Sections

### Security Waivers {#security-waivers}

- Document SSDF or ASVS exceptions. Reference `frontiers/policy/ssdf-mapping.yml` or `frontiers/policy/asvs-checklist.yml`.

### Supply-chain Waivers {#supply-chain-waivers}

- Capture SBOM, SLSA, signing, or Scorecard deviations.

### Quality Waivers {#quality-waivers}

- Record lint/formatting overrides, static or dynamic analysis suppressions, and documentation validation skips. Reference `frontiers/policy/code-quality-tooling.yml` and specify compensating controls (manual review, expanded testing) plus expiry.

### Benchmark Waivers {#benchmark-waivers}

- Track HumanEval+/MBPP+, SWE-bench, LiveCodeBench, AgentBench waivers with metrics.

### LLM Waivers {#llm-waivers}

- Use when guardrail controls temporarily disabled or benchmark regressions knowingly accepted.

## Automation Backlog

- `.github/workflows/waiver-reminder.yml` runs daily to surface waivers within seven days of expiry and re-opens the reminder issue if required.
- Compliance manifests (`frontiers/compliance/manifest-template.yml`) reference waiver IDs to keep downstream consumers aligned.
- Dashboard summarising open waivers, SLA status, and affected controls.
- Link-check step ensuring waiver anchors remain present in this document.

## Decision Records

- **DR-2025-11-05-Triage** — Governance forum approved triage automation and waiver SLAs.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/PROJECT_MANAGEMENT_QUICKREF.md">Project management quick reference</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/VERIFICATION_GUIDE.md">Automation verification guide</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/tree/main/frontiers/policy">Policy directory</a><br>
<strong>Methods:</strong> Combined automation guidance with waiver requirements; defined SLA table and escalation paths.<br>
<strong>Key results:</strong> Triage flow, waiver template, SLA table, automation backlog.<br>
<strong>Uncertainty:</strong> Reminder automation pending implementation.<br>
<strong>Safer alternative:</strong> Perform manual weekly audits until automation is ready.
</div>

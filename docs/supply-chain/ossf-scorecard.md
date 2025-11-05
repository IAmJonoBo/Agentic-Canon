---
title: "OpenSSF Scorecard"
summary: "Outlines required checks, thresholds, and escalation paths using the OpenSSF Scorecard action."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - supply-chain
  - ossf
  - governance
sources:
  - "https://github.com/ossf/scorecard-action"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml"
decision_records:
  - id: "DR-2025-11-05-Scorecard"
    title: "Adopted OpenSSF Scorecard thresholds"
    link: "docs/supply-chain/ossf-scorecard.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "OpenSSF Scorecard action"
      url: "https://github.com/ossf/scorecard-action"
      type: "primary"
    - name: "frontiers/quality-gate.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml"
      type: "secondary"
  methods:
    - "Configured Scorecard step in the quality gate and documented threshold review."
    - "Defined escalation workflow for degraded scores."
  key_results:
    - "Set score thresholds, evidence requirements, and remediation flow."
  uncertainty: "Future Scorecard versions may adjust checks or scoring."
  safer_alternative: "Treat new checks as mandatory upon release."
---

# OpenSSF Scorecard

## Summary

1. Runs OpenSSF Scorecard via `/frontiers/quality-gate.yml#ossf-scorecard` on every pull request.
2. Requires minimum overall score of 7.0; critical checks (Branch-Protection, Token-Permissions) must pass.
3. Uses results to trigger remediation tasks and escalate supply-chain risks.

## Configuration

```yaml
ossf-scorecard:
  needs: lint-and-format
  uses: ossf/scorecard-action@v2.3.1
  with:
    results_file: results.json
```

## Thresholds

| Check                  | Minimum | Action if Below                          |
| ---------------------- | ------- | ---------------------------------------- |
| Overall Score          | ≥ 7.0   | Block merge; open remediation issue      |
| Branch-Protection      | PASS    | Escalate to repo admins                  |
| Token-Permissions      | PASS    | Restrict workflow tokens; review secrets |
| Dependency-Update-Tool | PASS    | Ensure Dependabot/Renovate enabled       |
| Signed-Releases        | PASS    | Enforce cosign signing before release    |

## Remediation Workflow

1. CI posts Scorecard summary in PR (automation backlog).
2. If any critical check fails, label PR `risk:supply-chain` and block merge.
3. Create issue with remediation tasks; assign owner and due date (<14 days).
4. Track improvement progress in SAMM roadmap and `TASKS.md`.

## Evidence

- Store `results.json` under `artifacts/supply-chain/scorecard/`.
- Document exceptions in `docs/workflows/triage-and-exceptions.md#supply-chain-waivers`.
- Provide screenshot of Scorecard dashboard when required for audits.

## Decision Records

- **DR-2025-11-05-Scorecard** — Platform and security leads mandated Scorecard thresholds.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/ossf/scorecard-action">OpenSSF Scorecard action</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml">Quality gate workflow</a><br>
<strong>Methods:</strong> Integrated Scorecard action into quality gate; defined thresholds and remediation workflow.<br>
<strong>Key results:</strong> Configuration snippet, thresholds table, remediation flow, evidence expectations.<br>
<strong>Uncertainty:</strong> Future Scorecard versions may modify checks.<br>
<strong>Safer alternative:</strong> Treat new Scorecard checks as mandatory upon release.
</div>

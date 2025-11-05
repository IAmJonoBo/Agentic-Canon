---
title: "OWASP SAMM Roadmap"
summary: "Sets maturity targets, measurement cadence, and improvement backlog using OWASP SAMM 2.0 domains."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "explanation"
tags:
  - security
  - samm
  - maturity
sources:
  - "https://owasp.org/www-project-samm/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
decision_records:
  - id: "DR-2025-11-05-SAMM"
    title: "Defined SAMM maturity targets and cadence"
    link: "docs/security/owasp-samm.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "OWASP SAMM 2.0"
      url: "https://owasp.org/www-project-samm/"
      type: "primary"
    - name: "Control Traceability Matrix"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
      type: "secondary"
  methods:
    - "Used traceability matrix to identify existing SAMM-aligned practices."
    - "Set maturity targets with incremental quarterly goals."
  key_results:
    - "Maturity target table across Governance, Design, Implementation, Verification, Operations."
    - "Cadence for measurement and reporting."
  uncertainty: "Detailed SAMM scoring worksheets to be created (backlog)."
  safer_alternative: "Adopt SAMM provided worksheets until tailored spreadsheets exist."
---

# OWASP SAMM Roadmap

## Summary

1. Establishes OWASP SAMM 2.0 maturity targets for each domain and stream.
2. Defines measurement cadence and owners to track progress.
3. Feeds improvement actions into the programme backlog and decision records.

## Maturity Targets

| Domain         | Stream                  | Current | Target | Owner               | Notes                                              |
| -------------- | ----------------------- | ------- | ------ | ------------------- | -------------------------------------------------- |
| Governance     | Strategy & Metrics      | 1.5     | 2.5    | Security Leadership | Expand metrics to include AI safety KPIs           |
| Governance     | Policy & Compliance     | 2.0     | 3.0    | Compliance Lead     | Automate policy attestations via schema validation |
| Design         | Threat Assessment       | 1.5     | 2.5    | Architecture Guild  | Integrate STRIDE + LLM threats into PR template    |
| Design         | Security Requirements   | 2.0     | 3.0    | Product Security    | Keep SSDF mapping current with standards           |
| Implementation | Secure Build            | 2.0     | 3.0    | Platform            | Enforce `/frontiers/quality-gate.yml` in all repos |
| Implementation | Secure Deployment       | 1.5     | 2.5    | SRE                 | Expand Terraform policy-as-code coverage           |
| Verification   | Architecture Assessment | 1.0     | 2.0    | Security Guild      | Run semi-annual architecture reviews               |
| Verification   | Security Testing        | 2.0     | 3.0    | QA                  | Codify DAST smoke tests in CI                      |
| Operations     | Incident Management     | 2.0     | 3.0    | SRE                 | Include AI incidents and SBOM response in runbooks |
| Operations     | Environment Management  | 1.5     | 2.5    | Platform            | Harden sandbox isolation for agent workflows       |

## Measurement Cadence

1. **Quarterly** — Run SAMM self-assessment workshop; update maturity scores; document actions in `TASKS.md`.
2. **Monthly** — Review progress on active improvement actions.
3. **Per PR** — Tag changes affecting maturity actions with label `samm:improvement`.

## Reporting

- Summaries reside in `artifacts/security/samm/quarterly-<YYYY-MM>.md`.
- Dashboard backlog: Build Grafana view combining maturity scores, open risks, and waiver count.
- Escalate gaps ≥0.5 points below target to the governance meeting; raise issue with owner and due date.

## Decision Records

- **DR-2025-11-05-SAMM** — Programme office ratified maturity targets and cadence.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://owasp.org/www-project-samm/">OWASP SAMM 2.0</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json">Control traceability matrix</a><br>
<strong>Methods:</strong> Cross-referenced existing controls with SAMM domains; set maturity targets with quarterly cadence.<br>
<strong>Key results:</strong> Target table, measurement cadence, reporting plan.<br>
<strong>Uncertainty:</strong> Custom scoring worksheets pending.<br>
<strong>Safer alternative:</strong> Use SAMM-provided spreadsheets until custom tooling is ready.
</div>

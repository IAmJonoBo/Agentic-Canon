---
title: "Developer Experience Framework"
summary: "Codifies golden-path practices, tooling expectations, and metrics so n00tropic engineering teams deliver consistently exceptional developer experiences."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - experience
  - developer-experience
  - platform-engineering
sources:
  - "https://www.atlassian.com/software/compass/resources/state-of-developer-2024"
  - "https://www.devopsdigest.com/state-of-cicd-2024"
  - "https://www.infoq.com/news/2024/11/2024-dora-report/"
decision_records:
  - id: "DR-2025-11-05-DevEx"
    title: "Established developer experience framework and metrics"
    link: "docs/experience/developer-experience.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Atlassian State of Developer Experience 2024"
      url: "https://www.atlassian.com/software/compass/resources/state-of-developer-2024"
      type: "primary"
    - name: "State of CI/CD 2024 (CD Foundation)"
      url: "https://www.devopsdigest.com/state-of-cicd-2024"
      type: "secondary"
    - name: "2024 DORA Accelerate report coverage"
      url: "https://www.infoq.com/news/2024/11/2024-dora-report/"
      type: "secondary"
  methods:
    - "Synthesised developer experience research with existing platform and automation capabilities."
    - "Aligned metrics with DORA, SPACE, and local golden-path requirements."
  key_results:
    - "Defined DevEx pillars, golden-path workflow, and measurement cadence."
    - "Established feedback loops and downstream contracts for platform teams."
  uncertainty: "Full DORA 2025 dataset pending; review metrics when published."
  safer_alternative: "Default to conservative performance targets until new benchmarks validated."
---

# Developer Experience Framework

## Summary

1. Developer experience (DevEx) is treated as a first-class quality attribute, with platform teams owning golden paths and teams accountable for feedback loops.citeturn0search1
2. High-performing teams standardise on well-integrated CI/CD, security scanning, and self-service tooling to sustain top-tier DORA outcomes.citeturn0search0turn0search3
3. DevEx health is measured continuously (SPACE + DORA + sentiment) and tied to business outcomes such as deployment throughput, retention, and satisfaction.

## DevEx Pillars

| Pillar      | Description                               | Key Practices                                                              | Metrics                                                       |
| ----------- | ----------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Flow        | Minimise friction from idea to production | Trunk-based development, automated quality gate, self-service environments | Lead time, deployment frequency, WIP age                      |
| Feedback    | Provide actionable insights quickly       | Observability dashboards, feature experiments, post-incident reviews       | Feedback latency, MTTR, experiment win rate                   |
| Empowerment | Give teams autonomy with guardrails       | Internal developer platform, docs-as-code, playbooks                       | Self-service adoption %, time-to-value, golden-path adherence |
| Learning    | Institutionalise improvement              | Communities of practice, blameless retros, platform OKRs                   | L&D hours, retrop action closure, platform NPS                |

## Golden Path Expectations

1. **Bootstrap** — Use platform generator/CLI to scaffold services with standards baked in (policy YAML, pipelines, docs).
2. **Develop** — Branch from `main`, run `pre-commit`, execute unit + property tests, ensure mutation score ≥ 40%.
3. **Review** — Submit PR with automated checks, include DevEx metadata (impact, risk, testing).
4. **Release** — Merge via protected branch, prove health via CI/CD dashboards, log release in change calendar.
5. **Observe** — Monitor SLOs, feature metrics, and guardrail alerts; capture learnings in retros and docs.

## Tooling Baseline

- Source control: GitHub with CODEOWNERS + branch protection.
- CI/CD: GitHub Actions with `frontiers/quality-gate.yml`.
- Security: CodeQL, Semgrep, Trivy, Scorecard (enforced).
- Productivity: Internal developer portal surfacing golden paths, runbooks, and compliance manifests.
- Knowledge: MkDocs + policy YAML; incident retros stored with timeline + follow-up tasks.

## Measurement & Feedback

- **SPACE scorecards** quarterly (Satisfaction, Performance, Activity, Communication, Efficiency).
- **DORA metrics** streamed to dashboards; outliers trigger improvement reviews.
- **Survey cadence** bi-annually referencing Atlassian/Wakefield benchmarks for alignment.citeturn0search1
- **Platform KPIs**: golden-path adoption %, self-service success rate, time-to-environment.

## Continuous Improvement Loop

1. Collect metrics + qualitative feedback (surveys, retros, platform telemetry).
2. Prioritise DevEx backlog via platform council.
3. Implement improvements; document in `docs/experience/developer-experience.md`.
4. Communicate changes through release notes and training.

## Decision Records

- **DR-2025-11-05-DevEx** — Platform guild ratified DevEx pillars, measurement cadence, and golden path.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://www.atlassian.com/software/compass/resources/state-of-developer-2024">Atlassian State of Developer Experience 2024</a>; <a href="https://www.devopsdigest.com/state-of-cicd-2024">State of CI/CD 2024</a>; <a href="https://www.infoq.com/news/2024/11/2024-dora-report/">InfoQ coverage of the 2024 DORA report</a><br>
<strong>Methods:</strong> Merged industry research with platform capabilities; defined pillars, metrics, and golden path.<br>
<strong>Key results:</strong> DevEx framework, tooling baseline, measurement loop.<br>
<strong>Uncertainty:</strong> Awaiting DORA 2025 data.<br>
<strong>Safer alternative:</strong> Set conservative targets until new benchmarks verified.
</div>

---
title: "Code Health Metrics"
summary: "Defines the quantitative metrics—coverage, mutation score, flake rate, latency budgets—that govern merge readiness."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - metrics
  - quality
  - observability
sources:
  - "https://stryker-mutator.io/docs/stryker-js/introduction/"
  - "https://pitest.org/"
decision_records:
  - id: "DR-2025-11-05-CodeHealth"
    title: "Standardised code health metrics and thresholds"
    link: "docs/quality/code-health-metrics.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Stryker mutation testing docs"
      url: "https://stryker-mutator.io/docs/stryker-js/introduction/"
      type: "primary"
    - name: "PIT mutation testing docs"
      url: "https://pitest.org/"
      type: "primary"
    - name: "QUALITY_STANDARDS.md"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
      type: "secondary"
  methods:
    - "Aggregated thresholds from QUALITY_STANDARDS.md and benchmark policy."
    - "Aligned metrics with data captured in GitHub Actions and Grafana dashboards."
  key_results:
    - "Metric table with definitions, thresholds, and data sources."
    - "Alerting guidance for sustained degradations."
  uncertainty: "Latency budgets will vary per service; defaults provided as starting point."
  safer_alternative: "Use environment-specific budgets (dev/staging/prod) until SLOs mature."
---

# Code Health Metrics

## Summary

1. Defines the quantitative metrics that determine whether a change can merge.
2. Specifies target and warning thresholds plus monitoring locations.
3. Ensures regression detection feeds into SLO/SLI dashboards for continuous improvement.

## Metric Catalogue

| Metric               | Definition                                                     | Target                 | Warning                      | Data Source                              | Notes                        |
| -------------------- | -------------------------------------------------------------- | ---------------------- | ---------------------------- | ---------------------------------------- | ---------------------------- |
| Line Coverage        | Percentage of executed statements under unit/integration tests | ≥ 80%                  | < 85% trend down two sprints | `coverage.xml`, Codecov                  | Hard gate < 80%              |
| Branch Coverage      | Percentage of branches executed                                | ≥ 70%                  | < 75%                        | `coverage.xml` (branch)                  | Encourage targeted tests     |
| Mutation Score       | Survived mutants / total mutants inverted                      | ≥ 40%                  | < 45%                        | `mutmut.json`, `stryker-report.json`     | Aspirational 60%             |
| Test Flake Rate      | % of retries required in CI                                    | ≤ 2%                   | > 5%                         | GitHub Actions re-run analytics          | >5% triggers investigation   |
| Mean Merge Lead Time | PR open to merge                                               | ≤ 24h                  | > 48h                        | DORA metrics dashboard                   | Monitor tooling friction     |
| P95 Latency Budget   | 95th percentile latency for key SLO                            | Within declared budget | > budget for 2 hours         | Grafana dashboard `quality-metrics.json` | Align with SLO doc           |
| Error Rate           | % requests failing                                             | ≤ 0.1%                 | > 0.2%                       | Observability pipeline                   | Connect to incident response |

## Monitoring

- Grafana dashboards under `dashboards/quality-metrics.json` ingest coverage and mutation outputs nightly.
- Alerts route to `#frontier-quality` Slack when any metric enters warning for two consecutive runs.
- Weekly review summarises trending metrics; create improvement tasks if threshold breached for >1 week.

## Reporting Workflow

1. CI uploads coverage, mutation, and benchmark artefacts to `artifacts/quality/`.
2. `tools/report_quality.py` (backlog) will aggregate results and comment on PRs.
3. Use PR template checklist to confirm metric review; note if exception filed.

## Decision Records

- **DR-2025-11-05-CodeHealth** — Approved metric thresholds and monitoring cadence.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://stryker-mutator.io/docs/stryker-js/introduction/">Stryker mutation documentation</a>; <a href="https://pitest.org/">PIT mutation testing</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md">Quality standards</a><br>
<strong>Methods:</strong> Cross-referenced existing thresholds with mutation tooling guidelines; integrated DORA metrics for lead time.<br>
<strong>Key results:</strong> Metrics table, monitoring instructions, reporting workflow.<br>
<strong>Uncertainty:</strong> Latency budgets vary by service; final numbers require SLO review.<br>
<strong>Safer alternative:</strong> Use dynamic budgets per environment until SLO data stabilises.
</div>

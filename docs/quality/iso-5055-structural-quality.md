---
title: "ISO/IEC 5055 Structural Quality"
summary: "Explains how automated structural quality measures drive gates for reliability, security, performance efficiency, and maintainability."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - quality
  - iso5055
  - automation
sources:
  - "https://www.it-cisq.org/standards/code-quality-standards/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
decision_records:
  - id: "DR-2025-11-05-ISO5055"
    title: "Aligned structural quality measures with ISO/IEC 5055"
    link: "docs/quality/iso-5055-structural-quality.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "ISO/IEC 5055:2021 overview"
      url: "https://www.it-cisq.org/standards/code-quality-standards/"
      type: "primary"
    - name: "Quality Standards document"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
      type: "secondary"
  methods:
    - "Mapped CISQ categories to metrics available in templates (SonarQube, mutation, coverage)."
    - "Defined thresholds consistent with AGENT-docs-job non-negotiable gates."
  key_results:
    - "Four-category metric table with thresholds and tooling."
    - "Documented remediation workflow for deviations."
  uncertainty: "SonarQube project keys and baseline thresholds still require calibration for each service."
  safer_alternative: "Tie thresholds to moving averages until baselines stabilise."
---

# ISO/IEC 5055 Structural Quality

## Summary

1. Uses ISO/IEC 5055 to quantify structural quality through automated analysis pipelines.
2. Sets minimum thresholds for reliability, security, performance efficiency, and maintainability across all services.
3. Defines escalation workflows when quality debt exceeds tolerances.

## Metric Overview

| Category (CISQ)        | Target Metric             | Threshold                   | Tooling                                          | Notes                                                      |
| ---------------------- | ------------------------- | --------------------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Reliability            | Structural defect density | ≤ 0.1 per KLOC              | SonarQube Reliability Rating, chaos smoke tests  | Failing tests trigger hotfix procedure                     |
| Security               | Vulnerability index       | No new critical/high issues | SonarQube Security Hotspots, CodeQL results      | Must document mitigation plan for medium issues            |
| Performance Efficiency | Efficiency score          | Maintain ≥ B grade          | SonarQube Performance, k6/Locust baselines       | Track regressions >10%                                     |
| Maintainability        | Maintainability rating    | Technical debt ratio ≤ 5%   | SonarQube Maintainability, mutation score ≥ 0.40 | Enforce refactor tasks when ratio exceeds 5% for 2 sprints |

## Automation Pipeline

1. `frontiers/quality-gate.yml#sast` seeds SARIF data for security metrics.
2. `frontiers/quality-gate.yml#mutation-tests` ensures maintainability proxies stay above threshold.
3. SonarQube analysis (self-hosted or cloud) ingests coverage and lint reports to compute ISO 5055-aligned scores.
4. `docs/workflows/quality-gate.md` describes how the pipeline fails the PR when thresholds drop below target.

## Remediation Workflow

1. Open issue with label `debt:structural` and attach SonarQube screenshot or SARIF snippet.
2. Reference the issue in `TASKS.md` with an expected fix sprint.
3. If risk is high (critical vulnerabilities or debt ratio >10%), escalate via `docs/workflows/triage-and-exceptions.md`.
4. Once remediated, rerun quality gate and attach updated metrics.

## Decision Records

- **DR-2025-11-05-ISO5055** — Quality guild approved thresholds; mandates SonarQube integration per service.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://www.it-cisq.org/standards/code-quality-standards/">ISO/IEC 5055 overview</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md">Quality standards document</a><br>
<strong>Methods:</strong> Translated CISQ measures into SonarQube metrics; aligned with mutation and coverage thresholds.<br>
<strong>Key results:</strong> Metric table with thresholds; automation pipeline and remediation workflow.<br>
<strong>Uncertainty:</strong> Service-specific baselines still to be calibrated.<br>
<strong>Safer alternative:</strong> Apply moving-average thresholds until SonarQube baselines are stable.
</div>

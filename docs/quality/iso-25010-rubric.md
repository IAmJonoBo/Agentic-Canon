---
title: "ISO/IEC 25010 Review Rubric"
summary: "Provides a pull-request review rubric tied to ISO/IEC 25010 quality characteristics with evidence expectations and automation hooks."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - quality
  - iso25010
  - review
sources:
  - "https://www.iso.org/standard/78176.html"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
decision_records:
  - id: "DR-2025-11-05-ISO25010"
    title: "Adopted ISO/IEC 25010 rubric for PR reviews"
    link: "docs/quality/iso-25010-rubric.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "ISO/IEC 25010:2023 (Product quality)"
      url: "https://www.iso.org/standard/78176.html"
      type: "primary"
    - name: "Quality Standards baseline"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
      type: "secondary"
  methods:
    - "Parsed ISO quality characteristics, aligned review questions with existing automation from QUALITY_STANDARDS.md."
    - "Validated mapping with template repositories to ensure each characteristic has at least one guardrail."
  key_results:
    - "Eight characteristic rubric with acceptance criteria and automated evidence pointers."
    - "Defined reviewer checklist and gating metrics for each characteristic."
  uncertainty: "Awaiting paid access to ISO text for verbatim wording; placeholders summarise publicly available descriptions."
  safer_alternative: "Use ISO-sanctioned wording when sharing externally; keep this rubric internal if licensing concerns arise."
---

# ISO/IEC 25010 Review Rubric

## Summary

1. Normalises review expectations using ISO/IEC 25010 characteristics and sub-characteristics.
2. Connects reviewer questions to automated signals from `/frontiers/quality-gate.yml` and template scaffolding.
3. Captures evidence links so reviewers can attest to compliance without manual guesswork.

## Applying the Rubric

1. Identify the characteristic most affected by the change.
2. Run through the corresponding reviewer prompts in the table below.
3. Attach evidence (test results, logs, screenshots) directly in the PR or link to artefacts in `artifacts/quality/`.
4. Record outcomes in the PR checklist; escalate gaps via `docs/workflows/triage-and-exceptions.md`.

## Characteristic Matrix

| Characteristic         | Reviewer Prompts                                                        | Automated Signals                                         | Evidence Expectations                             |
| ---------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------- |
| Functional Suitability | Do acceptance tests cover new behaviour? Are contracts updated?         | Contract tests, API schema diff (`templates/*/contracts`) | Link to test run, updated OpenAPI or AsyncAPI     |
| Reliability            | Are error budgets respected? Does change alter recovery logic?          | Unit/integration tests, chaos experiments backlog         | Attach test results, note SLO impact              |
| Performance Efficiency | Does change affect latency, throughput, or resource budgets?            | Performance budgets in `package.json`/`Makefile`          | Provide benchmark output or profiling summary     |
| Compatibility          | Are interfaces/backwards compatibility preserved?                       | Contract test job, schema versioning                      | Document version bump and migration guidance      |
| Security               | Are new inputs validated? Secrets or tokens handled safely?             | CodeQL/Semgrep results, secret scan step                  | Reference SARIF findings or security review notes |
| Maintainability        | Is code modular, readable, and tested? Tech debt recorded?              | Mutation score, coverage reports                          | Link to coverage xml, tech debt tracker entry     |
| Portability            | Are container images, infrastructure modules, or build scripts updated? | Build pipeline results, infrastructure tests              | Provide Dockerfile diff, Terraform plan output    |
| Accessibility          | Do UI changes respect WCAG 2.2 AA? Are assistive tests updated?         | Axe tests, Playwright accessibility suite                 | Include screenshot/gif + test run link            |

## Reviewer Checklist

1. Confirm metrics in the PR description include impact on coverage, mutation score, and relevant benchmarks.
2. Ensure new dependencies have licence compatibility (refer to `docs/supply-chain/sbom-spdx.md`).
3. Verify documentation updates accompany code changes (tutorial/how-to/reference/explanation as needed).
4. Log residual risk or follow-up tasks in `TASKS.md` or as issues tagged `from:review`.

## Decision Records

- **DR-2025-11-05-ISO25010** — Review leads approved the rubric, superseding ad-hoc checklists in `QUALITY_STANDARDS.md`.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://www.iso.org/standard/78176.html">ISO/IEC 25010:2023 overview</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md">Internal quality standards</a><br>
<strong>Methods:</strong> Cross-referenced ISO characteristics against automation steps and template defaults.<br>
<strong>Key results:</strong> Eight-characteristic rubric; reviewer checklist; evidence expectations.<br>
<strong>Uncertainty:</strong> ISO text not publicly accessible; summarised characteristics may require refinement once licensed copy reviewed.<br>
<strong>Safer alternative:</strong> Use ISO-authorised descriptions in regulated contexts.
</div>

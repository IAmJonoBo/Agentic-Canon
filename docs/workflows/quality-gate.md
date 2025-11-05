---
title: "Quality Gate Workflow"
summary: "Describes the reusable quality gate workflow that orchestrates linting, testing, security scans, SBOMs, provenance, and benchmarks."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "explanation"
tags:
  - workflow
  - ci
  - quality
sources:
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
decision_records:
  - id: "DR-2025-11-05-QualityGate"
    title: "Approved reusable quality gate workflow contents"
    link: "docs/workflows/quality-gate.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "frontiers/quality-gate.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml"
      type: "primary"
    - name: "QUALITY_STANDARDS.md"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
      type: "secondary"
  methods:
    - "Documented each job within the workflow and mapped it to standards and metrics."
    - "Ensured alignment with non-negotiable gates from QUALITY_STANDARDS.md."
  key_results:
    - "Detailed job breakdown with commands, ownership, and evidence expectations."
  uncertainty: "Workflow assumes availability of toolchain (Python, Node, Go); service-specific overrides may be required."
  safer_alternative: "Split per-language jobs if runtime conflicts occur."
---

# Quality Gate Workflow

## Summary

1. `/frontiers/quality-gate.yml` provides a reusable GitHub Actions workflow that enforces linting, testing, security, and supply-chain gates.
2. Jobs map directly to non-negotiable controls set out in `QUALITY_STANDARDS.md`, the code-quality tooling policy (`frontiers/policy/code-quality-tooling.yml`), and SSDF requirements.
3. Benchmarks run optionally through an input toggle to avoid blocking docs-only changes.

## Invocation

Add to repository workflow:

```yaml
jobs:
  quality-gate:
    uses: IAmJonoBo/n00-frontiers/frontiers/quality-gate.yml@docs/frontiers-v1
    with:
      run-benchmarks: false
```

## Job Breakdown

| Job                     | Purpose                                              | Key Tools                       | Evidence                          |
| ----------------------- | ---------------------------------------------------- | ------------------------------- | --------------------------------- |
| `lint-and-format`       | Enforce style, static typing across Python, Node, Go | Ruff, mypy, ESLint, gofmt       | Lint logs, mypy report            |
| `unit-tests`            | Run tests with coverage                              | pytest                          | `coverage.xml` artefact           |
| `property-based`        | Hypothesis tests + fuzz smoke                        | Hypothesis, libFuzzer           | Hypothesis log, fuzz crash corpus |
| `mutation-tests`        | Mutation testing threshold (≥40%)                    | mutmut                          | `mutmut.json`                     |
| `sast`                  | CodeQL + Semgrep scanning                            | CodeQL, Semgrep                 | SARIF results                     |
| `dependency-security`   | Trivy, SBOM generation                               | Trivy, Syft                     | `sbom.spdx.json`, scan summary    |
| `provenance`            | Generate and sign SLSA provenance                    | cosign                          | Attestation bundle                |
| `ossf-scorecard`        | Assess OSS supply-chain posture                      | Scorecard                       | `results.json`                    |
| `benchmarks` (optional) | Smoke runs for code/agent benchmarks                 | EvalPlus, SWE-bench, AgentBench | Benchmark outputs                 |

## Evidence Storage

- Coverage & mutation: `artifacts/quality/`
- Security scans: `artifacts/security/`
- SBOM & provenance: `artifacts/provenance/`
- Benchmarks: `artifacts/benchmarks/`

## Failure Handling

1. Hard failures block merge until resolved or waiver approved.
2. Soft failures (benchmark toggled) require reviewer acknowledgement and follow-up issue.
3. Secrets absent for cosign? Skip with explicit comment and create remediation issue.

## Tips for Adoption

- Override versions (Python/Node/Go) via workflow inputs if project uses different runtime.
- Extend with language-specific jobs (e.g., Java, Rust) by forking workflow.
- Use run-name conventions to tie results to PR or release.

## Decision Records

- **DR-2025-11-05-QualityGate** — Platform guild approved workflow jobs and thresholds.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml">Quality gate workflow</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md">Quality standards</a><br>
<strong>Methods:</strong> Documented workflow jobs and alignment with quality standards; defined invocation guidance.<br>
<strong>Key results:</strong> Job breakdown table, evidence storage guidance, failure handling, adoption tips.<br>
<strong>Uncertainty:</strong> Language runtime differences may require overrides.<br>
<strong>Safer alternative:</strong> Split workflow per stack if shared runner approach causes conflicts.
</div>

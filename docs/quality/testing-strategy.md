---
title: "Testing Strategy"
summary: "Details the multi-layer testing strategy covering unit, property-based, fuzz, mutation, contract, and end-to-end checks."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "how-to"
tags:
  - testing
  - quality
  - strategy
sources:
  - "https://hypothesis.readthedocs.io/"
  - "https://llvm.org/docs/LibFuzzer.html"
decision_records:
  - id: "DR-2025-11-05-Testing"
    title: "Adopted layered testing strategy with property-based and fuzzing requirements"
    link: "docs/quality/testing-strategy.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Hypothesis documentation"
      url: "https://hypothesis.readthedocs.io/"
      type: "primary"
    - name: "LLVM libFuzzer guide"
      url: "https://llvm.org/docs/LibFuzzer.html"
      type: "primary"
    - name: "QUALITY_STANDARDS.md"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md"
      type: "secondary"
  methods:
    - "Consolidated requirements from QUALITY_STANDARDS.md with benchmark policy thresholds."
    - "Mapped each testing layer to CI jobs inside `frontiers/quality-gate.yml`."
  key_results:
    - "Defined minimal expectations and commands for each testing layer."
    - "Clarified ownership and evidence for reviews."
  uncertainty: "Service-specific test suites may require adjustments for language ecosystems beyond Python/Node/Go."
  safer_alternative: "Start with core unit and property-based tests before introducing fuzzing for legacy codebases."
---

# Testing Strategy

## Summary

1. Testing follows a layered approach: unit → property-based → fuzz → mutation → contract/E2E.
2. Quality gates enforce thresholds for coverage (≥80%), mutation score (≥40%), and benchmark guardrails.
3. Exceptions require explicit waivers and remediation plans tracked in `docs/workflows/triage-and-exceptions.md`.

## Layered Approach

### 1. Unit Tests

- Target scope: Pure functions, components, modules.
- Command: `pytest --cov=src --cov-report=xml`.
- Evidence: Attach coverage XML summary to PR.

### 2. Property-Based Tests

- Target scope: Invariants, edge cases, parser/serializer symmetry.
- Framework: Hypothesis (Python), fast-check (TypeScript), quickcheck (Go/Rust).
- Command: `pytest tests/property -q` (Python), `npm run test:property`.

### 3. Fuzz Tests

- Target scope: Parsers, interpreters, protocol handlers.
- Tools: libFuzzer, Jazzer, go-fuzz.
- Command: `./build/fuzz/target -max_total_time=60` or `go test ./fuzz -fuzz=Fuzz`.
- Evidence: Attach crash corpus, minimised cases to PR.

### 4. Mutation Testing

- Purpose: Ensure tests detect behavioural regressions.
- Tools: `mutmut`, `stryker`, `pitest`.
- Threshold: Mutation score ≥ 40% (hard gate), 60% aspirational.
- Command: `mutmut run --paths-to-mutate src`.

### 5. Contract & End-to-End

- Contract checks: Ensure API compatibility (`schemathesis`, `pact`, `buf`).
- E2E: Playwright/Cypress for web; k6 for performance; Postman or Tavern for API flows.
- Evidence: Provide failing scenario reproduction or attach sanitized recordings.

## Ownership Matrix

| Layer           | Primary Owner        | Secondary Owner | Automation Hook                             |
| --------------- | -------------------- | --------------- | ------------------------------------------- |
| Unit / Property | Feature team         | QA              | `frontiers/quality-gate.yml#unit-tests`     |
| Fuzz            | Security engineering | Feature team    | `frontiers/quality-gate.yml#property-based` |
| Mutation        | QA                   | Feature team    | `frontiers/quality-gate.yml#mutation-tests` |
| Contract        | Platform             | Feature team    | Template-specific workflows                 |
| End-to-End      | QA                   | SRE             | Scheduled nightly pipeline                  |

## Evidence Checklist

1. Fuzzing logs stored under `artifacts/quality/fuzz/`.
2. Mutation reports stored under `artifacts/quality/mutation/`.
3. Contract test results annotated in PR with dataset versions.
4. E2E video or screenshot attachments stored for 30 days.

## Decision Records

- **DR-2025-11-05-Testing** — Quality guild ratified layering approach and thresholds.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://hypothesis.readthedocs.io/">Hypothesis documentation</a>; <a href="https://llvm.org/docs/LibFuzzer.html">LLVM libFuzzer guide</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/QUALITY_STANDARDS.md">Quality standards baseline</a><br>
<strong>Methods:</strong> Synthesised layering requirements with existing CI workflow steps and benchmark policy.<br>
<strong>Key results:</strong> Layer definitions, commands, ownership matrix, evidence checklist.<br>
<strong>Uncertainty:</strong> Additional language ecosystems may require alternative tooling.<br>
<strong>Safer alternative:</strong> Introduce fuzzing gradually with guided smoke runs for legacy systems.
</div>

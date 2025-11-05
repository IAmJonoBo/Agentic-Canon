---
title: "HumanEval+ & MBPP+ Policy"
summary: "Defines how HumanEval+ and MBPP+ benchmarks are executed, recorded, and enforced for code generation quality."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - benchmarks
  - humaneval
  - mbpp
sources:
  - "https://github.com/evalplus/evalplus"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
decision_records:
  - id: "DR-2025-11-05-HumanEval"
    title: "Adopted EvalPlus benchmarks and thresholds"
    link: "docs/benchmarks/humaneval-plus.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "EvalPlus project"
      url: "https://github.com/evalplus/evalplus"
      type: "primary"
    - name: "Benchmark policy"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
      type: "secondary"
  methods:
    - "Referenced policy thresholds; added operational commands and evidence requirements."
    - "Confirmed dataset pinning to avoid contamination."
  key_results:
    - "Execution cadence, pass thresholds, and reporting steps for HumanEval+ and MBPP+."
  uncertainty: "EvalPlus dataset revisions may change problem counts; monitor releases."
  safer_alternative: "Lock to known-good commit hash when running in CI."
---

# HumanEval+ & MBPP+ Policy

## Summary

1. Uses EvalPlus HumanEval+ and MBPP+ to measure code synthesis quality.
2. Enforces pass@1 ≥ 0.82 (HumanEval+) and pass@10 ≥ 0.94 (MBPP+) as defined in `frontiers/policy/benchmark-policy.yml`.
3. Requires reproducible runs with pinned versions, recorded seeds, and stored artefacts.

## Setup

```bash
pip install evalplus==0.3.2
poetry install  # if using poetry-managed env
```

## Execution

```bash
# HumanEval+
poetry run evalplus.humaneval --max-problems 164 --post-process --samples 1 --log-dir artifacts/benchmarks/humaneval

# MBPP+
poetry run evalplus.mbpp --max-problems 500 --samples 10 --log-dir artifacts/benchmarks/mbpp
```

Set environment variables:

- `EVALPLUS_SEED`: deterministic sampling (store in artefact metadata).
- `EVALPLUS_STRICT`: set to `1` to enforce hidden tests.

## Cadence & Thresholds

- **Per PR (optional toggle)**: Run smoke subset (`--max-problems 20`) when code generation modules change.
- **Nightly**: Full HumanEval+ on latest main branch.
- **Weekly**: Full MBPP+ run.
- Hard fail when pass@1 < 0.70 (HumanEval+) or regression > 5 points.

## Reporting

1. Store raw JSON results in `artifacts/benchmarks/humaneval/` and `.../mbpp/`.
2. Summarise key metrics in PR comment or release notes.
3. Update benchmark trends dashboard (backlog) with pass rates.

## Contamination Control

- Pin evalplus version and commit hash.
- Reset caches between runs; run inside clean container.
- Record problem IDs excluded due to known contamination (maintain list in repo).

## Decision Records

- **DR-2025-11-05-HumanEval** — AI guild approved thresholds and cadence for EvalPlus benchmarks.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/evalplus/evalplus">EvalPlus benchmarks</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml">Benchmark policy</a><br>
<strong>Methods:</strong> Applied policy thresholds and dataset pinning guidance to create reproducible workflow.<br>
<strong>Key results:</strong> Execution commands, cadence, reporting, contamination controls.<br>
<strong>Uncertainty:</strong> Dataset revisions may adjust counts.<br>
<strong>Safer alternative:</strong> Lock runs to specific commit hash and container digest.
</div>

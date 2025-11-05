---
title: "LiveCodeBench Policy"
summary: "Defines how LiveCodeBench evaluations are executed, how contamination is prevented, and how regressions are handled."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - benchmarks
  - livecodebench
  - ai
sources:
  - "https://github.com/LiveCodeBench/LiveCodeBench"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
decision_records:
  - id: "DR-2025-11-05-LiveCodeBench"
    title: "Adopted LiveCodeBench cadence and thresholds"
    link: "docs/benchmarks/livecodebench.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "LiveCodeBench repository"
      url: "https://github.com/LiveCodeBench/LiveCodeBench"
      type: "primary"
    - name: "Benchmark policy"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
      type: "secondary"
  methods:
    - "Referenced policy thresholds; added contamination controls and reporting requirements."
  key_results:
    - "Execution commands, cadence, and escalation for LiveCodeBench."
  uncertainty: "Dataset snapshots update regularly; ensure locking when gating."
  safer_alternative: "Freeze dataset tarball per release and verify checksums."
---

# LiveCodeBench Policy

## Summary

1. Runs LiveCodeBench weekly (full) and daily smoke (20 prompts) to monitor agent coding performance.
2. Enforces exact-match ≥ 0.55 as per benchmark policy; soft alerts at 0.60 trending downward.
3. Implements contamination controls by verifying dataset checksums and isolating evaluation environments.

## Setup

```bash
pip install livecodebench==0.2.1
python -m livecodebench.bootstrap --dataset latest --output datasets/livecodebench-2025-10.tar.gz
```

Verify checksum:

```bash
shasum -a 256 datasets/livecodebench-2025-10.tar.gz
```

Record checksum in artefact metadata.

## Execution

```bash
python -m livecodebench.runner \
  --config configs/livecodebench.yml \
  --dataset datasets/livecodebench-2025-10.tar.gz \
  --output artifacts/benchmarks/livecodebench/results.json \
  --max-prompts 200
```

### Smoke Run

```bash
python -m livecodebench.runner \
  --config configs/livecodebench.yml \
  --dataset datasets/livecodebench-2025-10.tar.gz \
  --output artifacts/benchmarks/livecodebench/smoke.json \
  --max-prompts 20 \
  --seed 1337
```

## Cadence & Thresholds

- Weekly full run (200 prompts) — target ≥ 0.55 exact-match.
- Daily smoke run (20 prompts) — track deltas; alert if drop >10 points from baseline.
- Document dataset version and hash in run summary.

## Contamination Controls

1. Keep dataset tarball read-only; do not merge evaluation prompts into training sets.
2. Run evaluations inside isolated container; clear caches.
3. Rotate seeds monthly to detect overfitting.

## Reporting

- Publish summary (exact-match, partial credit, compile rate) in `artifacts/benchmarks/livecodebench/summary.md`.
- Link results in weekly AI capability report (backlog).
- Escalate persistent regressions to AI safety guild; track remediation in `TASKS.md`.

## Decision Records

- **DR-2025-11-05-LiveCodeBench** — AI guild approved thresholds and cadence for LiveCodeBench.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/LiveCodeBench/LiveCodeBench">LiveCodeBench repository</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml">Benchmark policy</a><br>
<strong>Methods:</strong> Applied policy thresholds to LiveCodeBench runs; defined contamination controls and reporting steps.<br>
<strong>Key results:</strong> Setup instructions, execution commands, cadence, reporting, controls.<br>
<strong>Uncertainty:</strong> Dataset updates may change prompt composition.<br>
<strong>Safer alternative:</strong> Freeze dataset tarball per release and verify checksums.
</div>

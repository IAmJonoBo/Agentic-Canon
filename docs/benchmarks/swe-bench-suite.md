---
title: "SWE-bench Suite"
summary: "Describes how to run SWE-bench Verified, Lite, and Live benchmarks, including cadence, gating, and contamination controls."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - benchmarks
  - swe-bench
  - agents
sources:
  - "https://www.swebench.com/"
  - "https://github.com/SWE-bench/SWE-bench"
decision_records:
  - id: "DR-2025-11-05-SWEbench"
    title: "Adopted SWE-bench benchmarking cadence and gating"
    link: "docs/benchmarks/swe-bench-suite.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SWE-bench official site"
      url: "https://www.swebench.com/"
      type: "primary"
    - name: "SWE-bench GitHub repository"
      url: "https://github.com/SWE-bench/SWE-bench"
      type: "primary"
    - name: "frontiers/policy/benchmark-policy.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
      type: "secondary"
  methods:
    - "Aligned suite cadence and thresholds with policy YAML."
    - "Documented dataset pinning and smoke run configuration."
  key_results:
    - "Guidance for Verified, Lite, Live runs with commands and gating rules."
  uncertainty: "SWE-bench Live tasks change daily; sampling strategy may require tuning."
  safer_alternative: "Use Verified snapshot for gating while Live tasks inform trend analysis."
---

# SWE-bench Suite

## Summary

1. Uses SWE-bench Verified for reproducible regression gating, Lite for quick feedback, and Live for real-time capability tracking.
2. Requires minimum resolved rate of 0.38 (Verified) and 0.20 (Live) per `frontiers/policy/benchmark-policy.yml`.
3. Implements contamination controls by pinning dataset commit hashes and archiving patched repos.

## Environment Setup

```bash
pip install -r benchmarks/requirements.txt
python -m pip install -e git+https://github.com/SWE-bench/SWE-bench.git@9f23c13#egg=swebench
```

## Running Benchmarks

### SWE-bench Verified

```bash
python tools/swebench_runner.py \
  --dataset verified \
  --config configs/swebench.yml \
  --limit 50 \
  --output artifacts/benchmarks/swebench-verified.json
```

### SWE-bench Lite

```bash
python tools/swebench_runner.py \
  --dataset lite \
  --limit 20 \
  --output artifacts/benchmarks/swebench-lite.json
```

### SWE-bench Live

```bash
python tools/swebench_runner.py \
  --dataset live \
  --limit 30 \
  --sampling stratified \
  --output artifacts/benchmarks/swebench-live.json
```

## Cadence

- Verified: Weekly full run; PR shard run when touching agent or automation logic.
- Lite: Daily smoke run (20 tasks) for rapid feedback.
- Live: Daily sample (5 tasks) + weekly larger sample (30 tasks) for trend monitoring.

## Thresholds & Escalation

- Verified resolved ≥ 0.38; drop below triggers remediation issue.
- Lite < 0.40 triggers focused investigation.
- Live two consecutive runs < 0.10 triggers escalation to AI safety guild.

## Contamination Control

1. Pin dataset commit `9f23c13` for Verified.
2. Store patched repo snapshots to avoid cross-run leakage.
3. Reset environment between runs; use containerised executor.

## Reporting

1. Store results JSON and summary in `artifacts/benchmarks/swebench/`.
2. Publish weekly summary (pass rate, failure taxonomy, regression cases).
3. Link to summary in PRs affecting agent automation.

## Decision Records

- **DR-2025-11-05-SWEbench** — AI guild approved cadence and gating for SWE-bench suite.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://www.swebench.com/">SWE-bench official site</a>; <a href="https://github.com/SWE-bench/SWE-bench">SWE-bench repository</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml">Benchmark policy</a><br>
<strong>Methods:</strong> Applied policy thresholds to Verified/Lite/Live runs; documented commands and contamination controls.<br>
<strong>Key results:</strong> Environment setup, commands, cadence, thresholds, reporting instructions.<br>
<strong>Uncertainty:</strong> Live dataset volatility may require sampling adjustments.<br>
<strong>Safer alternative:</strong> Use Verified snapshot for gating while Live informs monitoring.
</div>

---
title: "AgentBench Smoke Tests"
summary: "Describes smoke-level AgentBench evaluations, failure taxonomy, and escalation rules for agentic capability safety."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - benchmarks
  - agentbench
  - ai-safety
sources:
  - "https://arxiv.org/abs/2308.03688"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
decision_records:
  - id: "DR-2025-11-05-AgentBench"
    title: "Approved AgentBench smoke coverage and thresholds"
    link: "docs/benchmarks/agentbench-smoke.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "AgentBench paper"
      url: "https://arxiv.org/abs/2308.03688"
      type: "primary"
    - name: "Benchmark policy"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml"
      type: "secondary"
  methods:
    - "Derived smoke task subset from AgentBench taxonomy."
    - "Aligned pass thresholds with policy and guardrail requirements."
  key_results:
    - "Smoke test configuration, failure taxonomy, and escalation flow."
  uncertainty: "AgentBench datasets evolve; keep config synced with upstream releases."
  safer_alternative: "Lock smoke subset to known-good release before gating production."
---

# AgentBench Smoke Tests

## Summary

1. Runs AgentBench smoke suite to validate agentic orchestration behaviours before deployment.
2. Requires pass rate ≥ 0.70; hard fail at <0.65 per benchmark policy.
3. Captures failure taxonomy to inform guardrail enhancements and incident response.

## Setup

```bash
pip install agentbench==1.1.0
python -m agentbench.bootstrap --tasks smoke --output datasets/agentbench-smoke.jsonl
```

## Execution

```bash
python -m agentbench.run \
  --tasks smoke \
  --config configs/agentbench-smoke.yml \
  --limit 10 \
  --output artifacts/benchmarks/agentbench/smoke.json
```

Set environment:

- `AGENTBENCH_API_KEY` for third-party APIs (stored in vault).
- `AGENTBENCH_SEED` to ensure reproducibility.

## Failure Taxonomy

| Category          | Description                            | Example Signal                      | Mitigation                                    |
| ----------------- | -------------------------------------- | ----------------------------------- | --------------------------------------------- |
| Tool misuse       | Agent calls unauthorised tool          | Telemetry event `unauthorised_tool` | Tighten allowlist, update guardrail tests     |
| Hallucinated plan | Agent asserts success without evidence | `result_confidence < threshold`     | Add verification step, require human approval |
| Safety violation  | Agent attempts restricted action       | Policy violation event              | Update policy, escalate to AI safety guild    |
| Timeout           | Agent fails within SLA                 | `latency > budget`                  | Optimise planner, adjust concurrency          |

## Cadence & Escalation

- Execute smoke suite on every production deploy and nightly on main.
- Soft alert when pass rate <0.75 (investigation required).
- Hard fail (<0.65) blocks deployment until mitigations implemented.

## Reporting

1. Store logs and transcripts in `artifacts/benchmarks/agentbench/`.
2. Summarise failure taxonomy counts in weekly AI safety report.
3. File follow-up issues for recurring failures; tag `ai-safety`.

## Decision Records

- **DR-2025-11-05-AgentBench** — AI guild approved smoke suite coverage and thresholds.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://arxiv.org/abs/2308.03688">AgentBench paper</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/benchmark-policy.yml">Benchmark policy</a><br>
<strong>Methods:</strong> Selected smoke subset based on AgentBench taxonomy; aligned pass thresholds with guardrail requirements.<br>
<strong>Key results:</strong> Setup instructions, execution commands, failure taxonomy, cadence, reporting.<br>
<strong>Uncertainty:</strong> AgentBench datasets evolve; ensure configs remain current.<br>
<strong>Safer alternative:</strong> Lock smoke set to known-good release for gating until automation verifies updates.
</div>

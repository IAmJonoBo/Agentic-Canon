---
title: "Dynamic & Runtime Analysis"
summary: "Establishes policies for dynamic testing, fuzzing, observability-driven validation, and runtime enforcement across services and AI workloads."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - quality
  - security
  - dast
sources:
  - "https://snyk.io/blog/dynamic-application-security-testing-guide/"
  - "https://owasp.org/www-community/OWASP_Dynamic_Application_Security_Testing_(DAST)_Tools"
decision_records:
  - id: "DR-2025-11-05-DynamicAnalysis"
    title: "Standardised dynamic testing and runtime assurance policies"
    link: "docs/quality/dynamic-analysis.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Snyk 2025 DAST guide"
      url: "https://snyk.io/blog/dynamic-application-security-testing-guide/"
      type: "secondary"
    - name: "OWASP DAST tooling overview"
      url: "https://owasp.org/www-community/OWASP_Dynamic_Application_Security_Testing_(DAST)_Tools"
      type: "primary"
    - name: "n00-frontiers quality gate workflow"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml"
      type: "secondary"
  methods:
    - "Benchmarked OWASP and industry guidance against existing fuzzing, benchmarking, and observability assets."
    - "Defined dynamic testing cadences aligned with benchmark policy and incident response playbooks."
  key_results:
    - "Unified guidance for DAST, fuzzing, chaos, and observability-based checks."
    - "Runtime enforcement and rollback expectations tied to experience outcomes."
  uncertainty: "Tooling coverage may differ per language; maintain compatibility matrix quarterly."
  safer_alternative: "Use managed services or manual penetration tests when automation is insufficient."
---

# Dynamic & Runtime Analysis

## Summary

1. Dynamic testing complements SAST by exercising deployed services, APIs, and agents under realistic conditions.
2. Fuzzing, chaos, and observability pipelines provide continuous assurance that regression budgets stay within defined thresholds.
3. Runtime guardrails enforce safe defaults (feature flags, circuit breakers, policy engines) and trigger automated containment.

## Testing Portfolio

| Layer            | Goal                                        | Tooling                               | Cadence                           | Evidence               |
| ---------------- | ------------------------------------------- | ------------------------------------- | --------------------------------- | ---------------------- |
| DAST/API         | Detect runtime vulnerabilities, auth issues | OWASP ZAP, Snyk DAST, Schemathesis    | Nightly + pre-release             | DAST reports, SARIF    |
| Fuzzing          | Stress parsers, protocol handlers           | libFuzzer, Jazzer, go-fuzz            | Per PR (smoke) + nightly long-run | Corpus + crash reports |
| Performance      | Validate latency & budgets                  | k6, Locust, Lighthouse CI             | Per sprint + release candidate    | Metrics dashboards     |
| Chaos/Resilience | Verify failure handling & SLOs              | Gremlin, Litmus, custom chaos scripts | Monthly                           | Chaos runbook entries  |
| AI Guardrails    | Detect hallucination/toxicity               | AgentBench smoke, LiveCodeBench delta | Per deploy + weekly full          | Benchmark artefacts    |

## Policies

1. **Gatekeeping** — Production deploys require latest DAST + fuzz smoke + benchmark status green (or approved waiver).
2. **Observability-first** — Instrument structured traces/metrics; set alerts for p95 latency, error rate, hallucination rate.
3. **Automated rollback** — Define automated rollback criteria (SLO budget depletion, guardrail violation, spike in critical logs).

## Runtime Enforcement

- **Policies**: Use OPA/Kyverno for Kubernetes, AWS SCPs for cloud guardrails.
- **Circuit breakers**: Deploy `bulkhead`, `retry`, and `timeout` patterns; document thresholds.
- **Feature flags**: Wrap risky functionality; require dark launches with telemetry gating.
- **AI-specific**: Enforce kill switches; integrate red-team prompts for post-deploy sampling.

## Reporting & Metrics

- Track DAST coverage (% endpoints scanned), mean time to remediate dynamic findings, frequency of guardrail trips.
- Maintain run history in `artifacts/runtime/` and visualise trends in Grafana (quality and security dashboards).
- Include runtime quality summary in release notes (latency, availability, safety metrics).

## Waivers

- Allowed for limited time with compensating controls (e.g., WAF rule, feature disabled).
- Must include monitoring plan and expiry; track in `docs/workflows/triage-and-exceptions.md#benchmark-waivers`.

## Decision Records

- **DR-2025-11-05-DynamicAnalysis** — Approved dynamic testing and runtime enforcement policy stack.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://snyk.io/blog/dynamic-application-security-testing-guide/">Snyk DAST guide</a>; <a href="https://owasp.org/www-community/OWASP_Dynamic_Application_Security_Testing_(DAST)_Tools">OWASP DAST tooling overview</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/quality-gate.yml">Quality gate workflow</a><br>
<strong>Methods:</strong> Synthesised OWASP/Snyk guidance with existing automation to produce layered dynamic testing policy.<br>
<strong>Key results:</strong> Testing portfolio, runtime enforcement expectations, reporting metrics.<br>
<strong>Uncertainty:</strong> Tool coverage varies; maintain compatibility matrix.<br>
<strong>Safer alternative:</strong> Engage manual testing when automation coverage is insufficient.
</div>

---
title: "LLM Top 10 Guardrails"
summary: "Maps the OWASP LLM Top 10 risks to preventative, detective, and responsive controls implemented in n00-frontiers."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - ai
  - security
  - guardrails
sources:
  - "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml"
decision_records:
  - id: "DR-2025-11-05-LLMGuardrails"
    title: "Formalised LLM guardrail controls and testing cadence"
    link: "docs/security/llm-top10-guardrails.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "OWASP Top 10 for LLM Applications (v1.1)"
      url: "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
      type: "primary"
    - name: "LLM guardrail policy"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml"
      type: "secondary"
  methods:
    - "Converted policy YAML entries into developer-facing guardrail guidance."
    - "Linked each risk to specific automation and observability signals."
  key_results:
    - "Risk-to-control matrix with verification steps."
    - "Incident triggers and escalation workflow."
  uncertainty: "Runtime telemetry for hallucination detection still being tuned."
  safer_alternative: "Disable high-risk autonomous actions until telemetry stabilises."
---

# LLM Top 10 Guardrails

## Summary

1. Implements OWASP LLM Top 10 controls across prompt handling, output sanitisation, supply-chain, and monitoring.
2. Uses `/frontiers/policy/llm-top10-controls.yml` for machine-readable test hooks and escalation rules.
3. Integrates guardrail verification with benchmark suites and runtime observability.

## Risk Matrix

| Risk ID                        | Threat                               | Preventive Controls                                              | Detective Controls                                    | Tests                                                    |
| ------------------------------ | ------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| LLM01 Prompt Injection         | Malicious user instruction overrides | Immutable system prompts, prompt sanitisation, context scrubbing | Prompt trace logs, anomaly detection on refusal rates | `pytest tests/llm/test_prompt_filters.py`; prompt fuzzer |
| LLM02 Insecure Output Handling | Execution of untrusted output        | JSON Schema validation, HTML sanitisation                        | Runtime allowlist, SSRF/DOS filters                   | Quality gate secret scan & contract tests                |
| LLM03 Training Data Poisoning  | Compromised training corpora         | Dataset provenance manifests, hashed snapshots                   | Drift detection, dataset diff alerts                  | Dataset checksum job (backlog)                           |
| LLM05 Data Leakage             | Sensitive data exfiltration          | Secrets scanning, context redaction                              | DLP classifiers, audit logging                        | Quality gate secret scan, manual review                  |
| LLM07 Supply Chain             | Compromised models/dependencies      | Sigstore signatures, SLSA provenance, vendor attestation         | Scorecard monitoring, vulnerability scanning          | `frontiers/quality-gate.yml#provenance`                  |
| LLM09 Monitoring               | Lack of observability                | OTel spans, structured prompt/response logging                   | Outlier detection dashboards                          | Benchmarks + runtime anomaly alerts                      |

## Runtime Safeguards

1. **Content Filtering** — Use policy-based filters (e.g., Azure OpenAI safety filters or open-source equivalent) with fallback responses.
2. **Scope Limitation** — Constrain tool access and environment variables; use capability allowlists with explicit approval.
3. **Human-in-the-loop** — Require reviewer approval for critical operations (deployments, production data access).
4. **Kill Switches** — Provide runbook for disabling AI endpoints and revoking credentials upon incident detection.

## Testing & Monitoring

- Benchmarks: Run AgentBench smoke, LiveCodeBench delta, and targeted evaluation tasks referenced in `frontiers/policy/benchmark-policy.yml`.
- Logging: Enrich each prompt/response with metadata (user, session, classification tags) and ship to central SIEM.
- Alerts: Trigger on classification risk score > threshold, repeated refusal/hallucination rates, or anomaly in prompt volume.

## Incident Response

1. Detect unusual activity via alerts or customer reports.
2. Initiate AI-specific incident playbook (to be appended to `runbooks/incident-response-runbook.md`).
3. Suspend affected models or behaviours, revoke tokens, rotate secrets, and notify stakeholders.
4. Post-incident review: update guardrail tests, adjust benchmarks, document residual risks.

## Decision Records

- **DR-2025-11-05-LLMGuardrails** — AI safety guild accepted guardrail set and benchmark integration.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/">OWASP LLM Top 10 (v1.1)</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml">LLM guardrail policy</a><br>
<strong>Methods:</strong> Expanded machine-readable policy into developer guidance; mapped risks to tests and telemetry.<br>
<strong>Key results:</strong> Risk matrix, runtime safeguards, incident workflow.<br>
<strong>Uncertainty:</strong> Telemetry thresholds require tuning.<br>
<strong>Safer alternative:</strong> Disable autonomous actions until telemetry and guardrail tuning complete.
</div>

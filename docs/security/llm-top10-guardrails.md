---
title: "LLM Top 10 Guardrails"
summary: "Maps the 2025 OWASP LLM Top 10 risks to preventative, detective, and responsive controls implemented in n00-frontiers."
version: "1.1.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - ai
  - security
  - guardrails
sources:
  - "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
  - "https://www.invicti.com/blog/application-security/owasp-llm-top-10-2025/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml"
decision_records:
  - id: "DR-2025-11-05-LLMGuardrails"
    title: "Formalised LLM guardrail controls and testing cadence"
    link: "docs/security/llm-top10-guardrails.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "OWASP Top 10 for LLM Applications (2025 whitepaper)"
      url: "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
      type: "primary"
    - name: "Invicti analysis of OWASP LLM Top 10 2025"
      url: "https://www.invicti.com/blog/application-security/owasp-llm-top-10-2025/"
      type: "secondary"
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

1. Implements the 2025 OWASP LLM Top 10 controls across prompt handling, disclosure prevention, supply-chain, and runtime monitoring.citeturn5view0
2. Uses `/frontiers/policy/llm-top10-controls.yml` for machine-readable guardrail tests and escalation rules.
3. Integrates guardrail verification with benchmark suites and runtime observability to detect regressions early.citeturn1search8

## Risk Matrix

| Risk ID                                | Threat                                             | Preventive Controls                                     | Detective Controls                             | Tests                                                    |
| -------------------------------------- | -------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| LLM01 Prompt Injection                 | Adversarial prompts override safeguards            | Immutable system prompts, layered sanitisation          | Prompt tracing, refusal-rate anomaly detection | `pytest tests/llm/test_prompt_filters.py`; prompt fuzzer |
| LLM02 Sensitive Information Disclosure | PII, secrets, or regulated data leak via responses | JSON Schema validation, PII redaction, policy filters   | Content classifiers, audit logging             | Quality gate content-safety step                         |
| LLM03 Supply-chain Vulnerabilities     | Compromised models, APIs, tooling                  | Model provenance attestations, allowlisted dependencies | Scorecard, Trivy/SBOM diff                     | `frontiers/quality-gate.yml#dependency-security`         |
| LLM04 Data & Model Poisoning           | Malicious data corrupts training or retrieval      | Dataset manifests, contributor vetting, canary prompts  | Drift detection, poisoning probes              | `pytest tests/llm/test_poisoning_guards.py`              |
| LLM05 Improper Output Handling         | Unsafe execution of generated code/markup          | Sandbox execution, output sanitisation                  | Runtime policy allowlists, SSRF monitors       | `pytest tests/llm/test_execution_sandbox.py`             |
| LLM06 Excessive Agency                 | Agents exceed intended authority                   | Capability allowlists, human approvals, rate limits     | Budget monitoring dashboards                   | `python tools/check_agent_capabilities.py --policy ...`  |
| LLM07 System Prompt Leakage            | System/developer prompts exposed                   | Response scrubbing, segregated storage                  | Prompt leakage detectors                       | `pytest tests/llm/test_prompt_leakage.py`                |
| LLM08 Vector & Embedding Weaknesses    | Embedding stores allow injection or leakage        | ACLs/encryption, multi-tenant segmentation              | Embedding drift monitors                       | `pytest tests/llm/test_vector_acl.py`                    |
| LLM09 Misinformation & Deception       | Harmful or deceptive content published             | Fact-checking pipelines, human escalation               | Runtime classifiers, editorial review          | `pytest tests/llm/test_fact_check_pipeline.py`           |
| LLM10 Unbounded Resource Consumption   | Runaway spend/compute/tokens                       | Budget enforcement, circuit breakers                    | Usage anomaly dashboards                       | `pytest tests/llm/test_circuit_breakers.py`              |

## Runtime Safeguards

1. **Content Filtering** — Apply layered classifiers and policy filters before response delivery to limit sensitive disclosures.citeturn1search8
2. **Scope Limitation** — Enforce capability allowlists, sandbox execution, and secret-free runtime environments for agents.
3. **Human-in-the-loop** — Require approval steps for privileged actions such as deployments, production data access, or financial transactions.citeturn1search8
4. **Kill Switches** — Maintain documented kill switches and credential revocation runbooks for rapid containment.citeturn1search8

## Testing & Monitoring

- Benchmarks: Run AgentBench smoke, LiveCodeBench delta, and targeted evaluation tasks referenced in `frontiers/policy/benchmark-policy.yml`.
- Logging: Enrich prompts/responses with metadata (user, session, classification tags) and forward to central SIEM for correlation.citeturn1search8
- Alerts: Trigger on content safety scores, refusal anomalies, embedding drift, and budget overages; escalate when thresholds breach configured SLAs.citeturn1search8

## Incident Response

1. Detect unusual activity via alerts or customer reports.
2. Initiate AI-specific incident playbook (to be appended to `runbooks/incident-response-runbook.md`).
3. Suspend affected models or behaviours, revoke tokens, rotate secrets, and notify stakeholders.
4. Post-incident review: update guardrail tests, adjust benchmarks, document residual risks.

## Decision Records

- **DR-2025-11-05-LLMGuardrails** — AI safety guild accepted guardrail set and benchmark integration.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/">OWASP LLM Top 10 (2025)</a>; <a href="https://www.invicti.com/blog/application-security/owasp-llm-top-10-2025/">Invicti LLM Top 10 2025 analysis</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml">LLM guardrail policy</a><br>
<strong>Methods:</strong> Cross-referenced official OWASP whitepaper and industry analysis, then reflected updates in machine-readable policy and guardrail guidance.<br>
<strong>Key results:</strong> Updated risk matrix, runtime safeguards, monitoring guidance aligned to 2025 list.<br>
<strong>Uncertainty:</strong> Telemetry thresholds require tuning for new detectors.<br>
<strong>Safer alternative:</strong> Limit autonomous actions until telemetry and guardrail tuning complete.
</div>

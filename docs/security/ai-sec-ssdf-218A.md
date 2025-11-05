---
title: "NIST SP 800-218A AI Profile"
summary: "Extends SSDF controls to generative AI and foundation model workflows using the interim SP 800-218A profile and NIST AI RMF guidance."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - ai
  - security
  - ssdf
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/a/ipd"
  - "https://www.nist.gov/itl/ai-risk-management-framework"
decision_records:
  - id: "DR-2025-11-05-SSDF-AI"
    title: "Adopted interim AI profile mapping for SSDF"
    link: "docs/security/ai-sec-ssdf-218A.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "NIST SP 800-218A (Initial Public Draft)"
      url: "https://csrc.nist.gov/pubs/sp/800/218/a/ipd"
      type: "primary"
    - name: "NIST AI RMF 1.0"
      url: "https://www.nist.gov/itl/ai-risk-management-framework"
      type: "primary"
    - name: "frontiers/policy/llm-top10-controls.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml"
      type: "secondary"
  methods:
    - "Overlayed AI-specific recommendations from SP 800-218A on existing SSDF mapping."
    - "Aligned MAP-MEASURE-MANAGE functions from AI RMF with guardrails and benchmarks."
  key_results:
    - "AI risk control table incorporating prompt, model, data, and operations safeguards."
    - "Verification workflow connecting benchmarks to AI risk ratings."
  uncertainty: "SP 800-218A is an interim public draft; requirements may change before final release."
  safer_alternative: "Treat draft controls as mandatory pending final publication to avoid under-hardening."
---

# NIST SP 800-218A AI Profile

## Summary

1. Extends SSDF to cover AI system lifecycle risks (data, model, deployment) using NIST SP 800-218A IPD.
2. Aligns AI RMF functions (Govern, Map, Measure, Manage) with OWASP LLM Top 10 guardrails and benchmark policy.
3. Documents verification steps tying model evaluations and runtime monitoring to compliance.

## Control Overlay

| SSDF Practice  | AI Profile Augmentation                             | Implementation Artefact                                                    | Verification                                          |
| -------------- | --------------------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| PO.1 / GOV     | Define AI risk taxonomy, roles, and accountability  | `docs/overview/frontiers-principles.md`, this page                         | Quarterly AI risk review                              |
| PS.2 / MAP     | Secure model supply chain, document lineage         | `docs/supply-chain/slsa-provenance.md`, `frontiers/policy/slsa-policy.yml` | Provenance & SBOM checks                              |
| PW.4 / MEASURE | Evaluate model behaviour (hallucinations, toxicity) | Benchmark docs + `frontiers/policy/benchmark-policy.yml`                   | HumanEval+, SWE-bench, LiveCodeBench, AgentBench runs |
| RV.1 / MANAGE  | Monitor runtime outputs, respond to incidents       | `docs/security/llm-top10-guardrails.md`, incident runbook                  | Runtime telemetry, guardrail alerts                   |

## Risk Controls

1. **Model Inventory** — Register every model (internal/external) with metadata: version, training data, evaluation scores. Stored in `catalog.json` extension (backlog).
2. **Data Governance** — Ensure training/evaluation datasets carry provenance, consent, and usage restrictions; track via SBOM-like dataset manifest (planned).
3. **Evaluation Cadence** — Per benchmark policy: run smoke tests per PR when toggled; full runs weekly; track regressions >5%.
4. **Runtime Guardrails** — Deploy content filters, prompt sanitisation, and output validation (JSON Schema, signature checks). Document in `docs/security/llm-top10-guardrails.md`.
5. **Incident Response** — Add AI-specific playbooks (prompt injection, data leakage, hallucination) to incident response runbook; ensure page references once updated.

## Verification Workflow

1. PR merges require latest benchmark summary appended to PR comment (automation backlog).
2. CI ensures guardrail tests run (`frontiers/quality-gate.yml#benchmarks` when enabled).
3. Weekly evaluation meeting reviews benchmark trends, incident metrics, and guardrail effectiveness.
4. Exceptions documented under `docs/workflows/triage-and-exceptions.md#llm-waivers`.

## Decision Records

- **DR-2025-11-05-SSDF-AI** — AI safety guild agreed to treat SP 800-218A IPD controls as mandatory until final release.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://csrc.nist.gov/pubs/sp/800/218/a/ipd">NIST SP 800-218A IPD</a>; <a href="https://www.nist.gov/itl/ai-risk-management-framework">NIST AI RMF 1.0</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/llm-top10-controls.yml">LLM guardrail policy</a><br>
<strong>Methods:</strong> Aligned SSDF practice families with AI RMF functions and internal guardrail policy; recorded verification workflow.<br>
<strong>Key results:</strong> AI-specific control overlay, risk controls list, verification workflow.<br>
<strong>Uncertainty:</strong> Draft status of SP 800-218A.<br>
<strong>Safer alternative:</strong> Enforce all draft controls immediately to avoid under-hardening.
</div>

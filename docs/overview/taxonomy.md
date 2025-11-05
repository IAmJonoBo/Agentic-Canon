---
title: "Taxonomy & Glossary"
summary: "Defines shared terminology and maps industry standards to n00-frontiers controls so humans and agents can navigate consistently."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - glossary
  - taxonomy
  - mapping
sources:
  - "https://slsa.dev/spec/v1.0/provenance"
  - "https://owasp.org/www-project-samm/"
decision_records:
  - id: "DR-2025-11-05-Taxonomy"
    title: "Published shared taxonomy for standards and controls"
    link: "docs/overview/taxonomy.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "SLSA v1.0"
      url: "https://slsa.dev/spec/v1.0/provenance"
      type: "primary"
    - name: "OWASP SAMM 2.0"
      url: "https://owasp.org/www-project-samm/"
      type: "primary"
    - name: "control-traceability-matrix.json"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json"
      type: "secondary"
  methods:
    - "Normalised abbreviation list, ensuring each term maps to a Markdown page and policy YAML."
    - "Cross-checked matrix entries with new navigation to avoid orphaned controls."
  key_results:
    - "Glossary of 18 core terms with canonical definitions."
    - "Standards-to-controls matrix aligning documentation, policies, and automation."
  uncertainty: "Some glossary entries will need updating when AI-specific SSDF supplement is finalised."
  safer_alternative: "Link to authoritative standard text whenever ambiguity exists rather than paraphrasing."
---

# Taxonomy & Glossary

## Summary

1. Establishes a canonical vocabulary for frontier security, quality, and AI safety controls.
2. Maps each standard to the documentation section, machine policy, and automated gate that enforces it.
3. Reduces duplication by pointing contributors to single-source artefacts for each control.

## Glossary

| Term / Abbreviation      | Definition                                                                                               | Source                     | Primary Artefact                                |
| ------------------------ | -------------------------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------------------- |
| **SSDF**                 | NIST Secure Software Development Framework practice families PO/PS/PW/RV                                 | NIST SP 800-218 v1.1       | `docs/security/nist-ssdf.md`                    |
| **SLSA**                 | Supply-chain Levels for Software Artifacts, provenance and build integrity requirements                  | SLSA v1.0                  | `docs/supply-chain/slsa-provenance.md`          |
| **ASVS**                 | OWASP Application Security Verification Standard level-based requirements                                | OWASP ASVS 4.0.3           | `docs/security/owasp-asvs.md`                   |
| **SAMM**                 | OWASP Software Assurance Maturity Model for governance, design, implementation, verification, operations | OWASP SAMM 2.0             | `docs/security/owasp-samm.md`                   |
| **LLM Top 10**           | OWASP Top 10 for Large Language Model Applications risk catalogue                                        | OWASP LLM Top 10 1.1       | `docs/security/llm-top10-guardrails.md`         |
| **ISO 25010**            | Product quality model covering eight characteristics such as security, maintainability, portability      | ISO/IEC 25010:2023         | `docs/quality/iso-25010-rubric.md`              |
| **ISO 5055**             | Automated structural quality measures (reliability, performance efficiency, security, maintainability)   | ISO/IEC 5055:2021          | `docs/quality/iso-5055-structural-quality.md`   |
| **EvalPlus**             | Benchmark harness for HumanEval+ and MBPP+ tasks with hidden tests                                       | EvalPlus v0.3.2            | `docs/benchmarks/humaneval-plus.md`             |
| **SWE-bench**            | Real-world software maintenance benchmark (Verified/Lite/Live)                                           | SWE-bench (2025 snapshots) | `docs/benchmarks/swe-bench-suite.md`            |
| **LiveCodeBench**        | Rolling coding benchmark resistant to contamination                                                      | LiveCodeBench 2025         | `docs/benchmarks/livecodebench.md`              |
| **AgentBench**           | Multitask agent capability benchmark with smoke subset                                                   | AgentBench v1.1            | `docs/benchmarks/agentbench-smoke.md`           |
| **Provenance**           | Verified chain of custody for build artefacts                                                            | SLSA v1.0                  | `docs/supply-chain/slsa-provenance.md`          |
| **Attestation**          | Signed statement about software artefact properties (build, SBOM, test)                                  | in-toto spec               | `docs/supply-chain/signing-and-attestations.md` |
| **SBOM**                 | Software Bill of Materials enumerating components and licences                                           | SPDX 3.0                   | `docs/supply-chain/sbom-spdx.md`                |
| **Quality Gate**         | Consolidated CI workflow enforcing lint, tests, security scans                                           | Repository workflow        | `docs/workflows/quality-gate.md`                |
| **Decision Record (DR)** | Concise note capturing context, decision, and consequences                                               | Internal standard          | Each page `## Decision Records`                 |
| **Waiver**               | Temporary exception to a control, tracked with owner, expiry, mitigation                                 | Governance policy          | `docs/workflows/triage-and-exceptions.md`       |
| **AI RMF**               | NIST AI Risk Management Framework (Govern, Map, Measure, Manage)                                         | NIST AI RMF 1.0            | `docs/security/ai-sec-ssdf-218A.md`             |

## Standards Mapping

| Standard            | Documentation                     | Machine Policy                            | Automation Check                            |
| ------------------- | --------------------------------- | ----------------------------------------- | ------------------------------------------- |
| NIST SSDF v1.1      | `security/nist-ssdf.md`           | `frontiers/policy/ssdf-mapping.yml`       | `frontiers/quality-gate.yml#sast`           |
| SP 800-218A (IPD)   | `security/ai-sec-ssdf-218A.md`    | `frontiers/policy/llm-top10-controls.yml` | Benchmarks + LLM guardrails tests           |
| OWASP ASVS 4.0.3    | `security/owasp-asvs.md`          | `frontiers/policy/asvs-checklist.yml`     | Quality gate security review step           |
| OWASP SAMM 2.0      | `security/owasp-samm.md`          | n/a (tracking via SSDF map)               | Quarterly governance review                 |
| SLSA v1.0           | `supply-chain/slsa-provenance.md` | `frontiers/policy/slsa-policy.yml`        | `frontiers/quality-gate.yml#provenance`     |
| SPDX 3.0 / SBOM     | `supply-chain/sbom-spdx.md`       | `frontiers/policy/slsa-policy.yml`        | SBOM step in quality gate                   |
| OpenSSF Scorecard   | `supply-chain/ossf-scorecard.md`  | n/a                                       | `frontiers/quality-gate.yml#ossf-scorecard` |
| EvalPlus Benchmarks | `benchmarks/humaneval-plus.md`    | `frontiers/policy/benchmark-policy.yml`   | Optional benchmark job                      |
| SWE-bench           | `benchmarks/swe-bench-suite.md`   | `frontiers/policy/benchmark-policy.yml`   | Benchmark pipeline                          |

## Decision Records

- **DR-2025-11-05-Taxonomy** — Established canonical glossary and mapping across security, quality, supply-chain, and AI benchmarking standards.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://slsa.dev/spec/v1.0/provenance">SLSA v1.0</a>; <a href="https://owasp.org/www-project-samm/">OWASP SAMM 2.0</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/control-traceability-matrix.json">Control traceability matrix</a><br>
<strong>Methods:</strong> Surveyed existing controls and ensured each term has a single owning document plus optional machine-readable mapping.<br>
<strong>Key results:</strong> Glossary of 18 terms; standards-to-controls table; pointers for automation teams.<br>
<strong>Uncertainty:</strong> SP 800-218A still in draft; terms may evolve.<br>
<strong>Safer alternative:</strong> Default to the definitions inside official standards when conflicts occur.
</div>

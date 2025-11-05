---
title: "Frontiers Principles"
summary: "Defines the goals, non-goals, and foundational principles that anchor the n00-frontiers programme across security, quality, and AI governance."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "explanation"
tags:
  - principles
  - governance
  - overview
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://www.iso.org/standard/78176.html"
decision_records:
  - id: "DR-2025-11-05-Principles"
    title: "Codified frontiers goals and non-goals"
    link: "docs/overview/frontiers-principles.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "NIST SSDF v1.1"
      url: "https://csrc.nist.gov/pubs/sp/800/218/final"
      type: "primary"
    - name: "ISO/IEC 25010:2023 Overview"
      url: "https://www.iso.org/standard/78176.html"
      type: "primary"
    - name: "Agentic Canon core documents"
      url: "https://github.com/IAmJonoBo/n00-frontiers"
      type: "secondary"
  methods:
    - "Extracted shared statements from FRAMEWORK.md, BIBLE.md, and QUALITY_STANDARDS.md and reconciled wording."
    - "Aligned principle wording with SSDF practice families and ISO quality characteristics."
  key_results:
    - "Documented six primary frontiers goals tied to measurable outcomes."
    - "Listed explicit non-goals to prevent scope creep in automation and AI augmentation."
  uncertainty: "Awaiting publication of ISO/IEC 25010:2023 full text to refine quality characteristic descriptors."
  safer_alternative: "Default to ISO/IEC 25010:2011 language until procurement grants access to 2023 text."
---

# Frontiers Principles

## Summary

1. Secure-by-construction, evidence-backed delivery is mandatory for every change, regardless of size.
2. Frontier software excellence requires balanced investment across quality, resilience, safety, and supply-chain integrity.
3. AI augmentation amplifies both capability and risk, so controls must treat agents as privileged collaborators, not infallible oracles.

## Goals

1. **Assurance** — Deliver verifiable compliance with NIST SSDF v1.1 practice families (PO, PS, PW, RV) through automation-first workflows.
2. **Product Quality** — Optimise for ISO/IEC 25010:2023 characteristics (functional suitability, reliability, security, maintainability, portability) across templates and services.
3. **Supply-Chain Trust** — Achieve SLSA Level 3 for all release artefacts, including model weights and prompt libraries.
4. **Agentic Safety** — Embed OWASP LLM Top 10 mitigations into development and runtime guardrails, measured through policy controls and benchmark regressions.
5. **Usability** — Ensure documentation and tooling remain accessible to humans and machine agents through structured metadata, consistent APIs, and AI-friendly formats.
6. **Continuous Improvement** — Track and publish KPIs (coverage, mutation score, benchmark pass@k, SBOM completeness) with trend analysis and action plans.
7. **Canonical Authority** — Keep documentation and policy assets independent from implementation repos and require downstream consumers to declare alignment with the published version.

## Non-Goals

1. Acting as a replacement for formal legal, regulatory, or privacy counsel.
2. Serving as a generic developer handbook divorced from the n00-frontiers automation stack.
3. Maintaining forks of external standards; instead we link to authoritative sources and document our implementation specifics.
4. Supporting uncontrolled experimental AI agents in production environments without risk assessment and defensive controls.

## Principles in Practice

| Principle               | Implementation Example                                   | Measurement                       |
| ----------------------- | -------------------------------------------------------- | --------------------------------- |
| Evidence over intuition | Provenance block on each page; CI stores evaluation logs | Decision Records + CI artefacts   |
| Automation-first        | `/frontiers/quality-gate.yml` orchestrates checks        | All merges require successful run |
| Defence-in-depth        | Combine CodeQL, Semgrep, Trivy, and mutation testing     | Hard gate on blocking findings    |
| Human + AI pairing      | AgentBench smoke tests gate AI copilots                  | Benchmarks policy thresholds      |
| Transparency            | `frontiers/policy/*.yml` available for machine ingestion | Schema validation via JSON Schema |
| Canonical-first         | Downstream generators track doc version tags             | Compliance manifests + waiver log |

## Contribution Expectations

1. Propose changes via `docs/frontiers-v1` branches and include updated provenance and decision records.
2. Update affected policy YAML and cross-reference it in the Markdown under “Integration” or “Controls” sections.
3. Run `mkdocs serve` locally or `mkdocs build --strict` in CI to verify navigation, links, and schema compliance.

## Decision Records

- **DR-2025-11-05-Principles** — Steering committee approved the six goals and four non-goals, with quarterly review cadenced to NIST SSDF updates.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://csrc.nist.gov/pubs/sp/800/218/final">NIST SSDF v1.1</a>; <a href="https://www.iso.org/standard/78176.html">ISO/IEC 25010:2023 overview</a>; Repository strategy documents.<br>
<strong>Methods:</strong> Normalised shared language between FRAMEWORK.md and QUALITY_STANDARDS.md, mapped to SSDF and ISO characteristic tables.<br>
<strong>Key results:</strong> Six goals and four non-goals anchored to measurable controls; matrix connecting principles to automation.<br>
<strong>Uncertainty:</strong> Full ISO/IEC 25010:2023 text pending procurement; descriptions may need adjustment.<br>
<strong>Safer alternative:</strong> Follow ISO/IEC 25010:2011 characteristics verbatim when formal compliance is required.
</div>

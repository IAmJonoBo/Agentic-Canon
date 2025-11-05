---
title: "Information Architecture"
summary: "Provides navigation, tagging, and versioning guidance for the MkDocs site and machine-readable artefacts."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "explanation"
tags:
  - documentation
  - information-architecture
  - mkdocs
sources:
  - "https://squidfunk.github.io/mkdocs-material/"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/mkdocs.yml"
decision_records:
  - id: "DR-2025-11-05-IA"
    title: "Defined documentation information architecture"
    link: "docs/docs/information-architecture.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "MkDocs Material documentation"
      url: "https://squidfunk.github.io/mkdocs-material/"
      type: "primary"
    - name: "mkdocs.yml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/mkdocs.yml"
      type: "secondary"
  methods:
    - "Mapped navigation tree from mkdocs.yml to Diátaxis expectations."
    - "Documented tagging, search metadata, and versioning approach."
  key_results:
    - "Navigation overview, tagging scheme, and versioning guidance."
  uncertainty: "Versioning via mike pending integration; update when configured."
  safer_alternative: "Manual release notes until versioning automation complete."
---

# Information Architecture

## Summary

1. Organises content by domain (overview, quality, security, supply-chain, benchmarks, workflows, docs) with Diátaxis signal in front matter.
2. Uses MkDocs Material features (tabs, search, tags) to support human and agent navigation.
3. Synchronises documentation and machine-readable policies through consistent naming and tagging.

## Navigation Overview

- **Home**: Landing page with scope and integration map.
- **Overview**: Principles, evidence protocol, taxonomy.
- **Quality**: ISO rubrics, testing, metrics.
- **Security**: SSDF, ASVS, SAMM, LLM guardrails.
- **Supply Chain**: SLSA, signing, SBOM, Scorecard.
- **Benchmarks**: HumanEval+, SWE-bench, LiveCodeBench, AgentBench.
- **Workflows**: Quality gate, pre-commit, triage/waivers.
- **Docs-as-Code**: Style guide, information architecture, AI accessibility.

Maintain parity between nav labels and file headings to simplify agent retrieval.

## Tagging

- Use concise lowercase tags (`security`, `benchmarks`, `workflow`, `docs`).
- Minimum one, recommended three tags per page.
- Tags power site search facets and upcoming taxonomy visualisations.

## Metadata

- `summary` field acts as search excerpt.
- `sources` list appear in provenance; ensures at least one official reference.
- `decision_records` anchor cross-links for governance review.

## Versioning Strategy

- MkDocs Material `extra.version` reserved for mike integration.
- Release steps:
  1. Update `version` fields in affected pages.
  2. Tag repo (e.g., `docs/v1.0.0`).
  3. Once mike integrated, run `mike deploy 1.0 latest`.
  4. Update `extra.version.name` in `mkdocs.yml`.

## Search & Discoverability

- Search plugin indexes summary, headings, body, and tags.
- For agent interoperability, expose JSON index (backlog) or query `mkdocs build` outputs.
- Provide consistent anchor IDs (e.g., `{#security-waivers}`) for machine linking.

## Machine-readable Alignment

- Mirror doc filenames with policy equivalents (e.g., `security/nist-ssdf.md` ↔ `policy/ssdf-mapping.yml`).
- Use same IDs in `decision_records` and policy entries when referencing controls.
- Document cross-links in `index.md` integration map.

## Decision Records

- **DR-2025-11-05-IA** — Documentation guild approved navigation and metadata scheme.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://squidfunk.github.io/mkdocs-material/">MkDocs Material docs</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/mkdocs.yml">Site configuration</a><br>
<strong>Methods:</strong> Mapped navigation structure to Diátaxis and tagging requirements; documented versioning plans.<br>
<strong>Key results:</strong> Navigation overview, tagging guidance, metadata standards, versioning workflow.<br>
<strong>Uncertainty:</strong> Mike versioning pending integration.<br>
<strong>Safer alternative:</strong> Maintain manual release notes until versioning is automated.
</div>

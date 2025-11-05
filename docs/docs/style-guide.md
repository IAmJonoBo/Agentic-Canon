---
title: "Style Guide"
summary: "Defines writing conventions, tone, formatting, and citation requirements for n00-frontiers documentation."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - documentation
  - style
  - diataxis
sources:
  - "https://diataxis.fr/"
  - "https://www.writethedocs.org/guide/docs-as-code.html"
decision_records:
  - id: "DR-2025-11-05-Style"
    title: "Approved documentation style guide"
    link: "docs/docs/style-guide.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Diátaxis documentation framework"
      url: "https://diataxis.fr/"
      type: "primary"
    - name: "Write the Docs - Docs as Code"
      url: "https://www.writethedocs.org/guide/docs-as-code.html"
      type: "secondary"
    - name: "frontiers/policy/frontiers.schema.json"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/frontiers.schema.json"
      type: "secondary"
  methods:
    - "Harmonised Diátaxis principles with docs-as-code practices and schema requirements."
    - "Codified tone, structure, and citation rules to support provenance."
  key_results:
    - "Authoring checklist, formatting rules, and citation guidance."
  uncertainty: "Schema may evolve; update guidance accordingly."
  safer_alternative: "Validate against schema before finalising new conventions."
---

# Style Guide

## Summary

1. Enforces Oxford English, concise sentences, and active voice across all documentation.
2. Requires Diátaxis alignment (tutorial, how-to, reference, explanation) with clear audience intent.
3. Mandates provenance metadata, citations, and decision record updates for every change.

## Voice & Tone

- Prefer active voice, short sentences, and precise terminology.
- Use inclusive language; avoid idioms and sarcasm.
- Write for practitioners and agent assistants; assume technical literacy.

## Structure

1. Include `## Summary`, `## Decision Records`, and `## Provenance` sections in every page.
2. Break content into numbered or bulleted lists for scanning.
3. Keep paragraphs ≤ 4 sentences; highlight commands with fenced code blocks.

## Diátaxis Mapping

| Type        | Purpose                | Example Sections                        |
| ----------- | ---------------------- | --------------------------------------- |
| Tutorial    | Guided learning path   | `docs/workflows/pre-commit.md`          |
| How-to      | Task-based steps       | `docs/supply-chain/sbom-spdx.md`        |
| Reference   | Facts and APIs         | `docs/security/nist-ssdf.md`            |
| Explanation | Concepts and rationale | `docs/overview/frontiers-principles.md` |

Indicate type via front matter `diataxis` field.

## Formatting Rules

- Headings use Title Case.
- Use fenced code blocks with language hints (e.g., ` ```bash `).
- Tables require headers and consistent alignment.
- Inline code for commands (`git status`), file paths (`docs/index.md`), environment variables (`COSIGN_KEY`).

## Citations & Provenance

- At least two sources per page (one primary).
- Cite inline with Markdown links; summarise evidence in `## Provenance`.
- Mirror data in front matter `provenance` object.

## Author Checklist

1. Update front matter: `version`, `last_verified`, `tags`, `sources`, `decision_records`.
2. Validate with `python tools/validate_frontmatter.py` (backlog; manual review meanwhile).
3. Run `mkdocs build --strict`.
4. Update relevant policy YAML if controls changed.

## Decision Records

- **DR-2025-11-05-Style** — Documentation guild approved style rules and checklist.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://diataxis.fr/">Diátaxis framework</a>; <a href="https://www.writethedocs.org/guide/docs-as-code.html">Write the Docs guide</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/frontiers/policy/frontiers.schema.json">Front matter schema</a><br>
<strong>Methods:</strong> Combined Diátaxis and docs-as-code practices with schema requirements to produce actionable rules.<br>
<strong>Key results:</strong> Voice & tone guidance, structure rules, checklist, citation expectations.<br>
<strong>Uncertainty:</strong> Schema updates may require revisions.<br>
<strong>Safer alternative:</strong> Validate against schema before finalising new conventions.
</div>

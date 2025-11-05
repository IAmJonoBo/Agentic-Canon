---
title: "n00-frontiers Documentation System"
summary: "Defines the scope, operating principles, and governance for the frontier-grade documentation that supports secure, high-quality, AI-enabled delivery."
version: "1.1.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "explanation"
tags:
  - overview
  - governance
  - quality
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://owasp.org/www-project-application-security-verification-standard/"
  - "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
  - "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
decision_records:
  - id: "DR-2025-11-05-Index"
    title: "Baseline governance for n00-frontiers Docs"
    link: "docs/index.md#governance-model"
    status: "accepted"
provenance:
  data:
    - name: "NIST SP 800-218 Rev.1 (v1.1)"
      url: "https://csrc.nist.gov/pubs/sp/800/218/final"
      type: "primary"
    - name: "OWASP ASVS 4.0.3"
      url: "https://owasp.org/www-project-application-security-verification-standard/"
      type: "primary"
    - name: "SLSA 1.1 release announcement"
      url: "https://slsa.dev/blog/2025/04/slsa-1.1-is-here"
      type: "primary"
    - name: "Agentic Canon framework repository analysis"
      url: "https://github.com/IAmJonoBo/n00-frontiers"
      type: "secondary"
  methods:
    - "Mapped canonical standards to repository assets via control-traceability-matrix.json review."
    - "Validated Diátaxis coverage and machine-readable policy requirements against AGENT-docs-job.md directives."
  key_results:
    - "Established MkDocs-based documentation system with Material theme and structured metadata."
    - "Recorded mandatory provenance workflow for all pages to support agentic validation."
  uncertainty: "Final publication workflow not yet connected to GitHub Pages; legacy Jupyter Book content remains in docs_legacy awaiting archival plan."
  safer_alternative: "Serve docs behind staging site until automated link-check and schema validation are wired into CI."
owner: "Documentation Engineering"
---

# n00-frontiers Documentation System

## Summary

1. Centralises secure SDLC, quality, supply-chain, and AI safety guidance into a single MkDocs site for humans and agents.
2. Enforces machine-readable front matter validated by `frontiers.schema.json` to keep metadata consistent and auditable.
3. Aligns documentation maintenance with NIST SSDF v1.1, OWASP ASVS 4.0.3, SLSA v1.1, and the 2025 OWASP LLM Top 10 updates for evidence-backed controls.

## Scope

The n00-frontiers documentation system covers the whole lifecycle of frontier software delivery: product quality models, secure engineering, supply-chain integrity, benchmarking, contributor workflows, and docs-as-code practices. Each section follows the Diátaxis framework so contributors can locate tutorials, task guides, references, and explanations with minimal translation effort.

## Canonical Authority & Separation of Concerns

1. **Docs-first governance** — This library is the canonical specification for secure SDLC, AI safety, quality, and experience requirements. Implementations (templates, generators, internal platforms) consume these standards and must not diverge without a documented waiver.
2. **Implementation sandboxes** — Application scaffolding, sample services, and automation tooling live outside the documentation tree (or in separate repositories) so the standards remain stack-agnostic and reusable across n00tropic business units.
3. **Downstream contracts** — Every generator, template, or platform must declare which documentation release it targets (e.g., docs `v1.1.0`) and publish a compliance manifest referencing the relevant policy YAML. Deviations are tracked via `docs/workflows/triage-and-exceptions.md`.

## Operating Principles

1. **Evidence-gated guidance** — Each page declares sources, methods, and uncertainties so that auditors and agents can trace recommendations back to authoritative standards.
2. **Single source of truth** — Machine-readable YAML policies in `frontiers/policy/` mirror the Markdown guidance, enabling automated checks in CI and external governance platforms.
3. **Iterative hardening** — Updates must bump the page version, refresh the `last_verified` date in Africa/Johannesburg time, and document decision records for major structural changes.

## Governance Model

- **Ownership**: The Documentation Engineering group stewards schema updates and MkDocs navigation; domain leads own their sections (security, quality, supply-chain, benchmarks).
- **Change control**: Significant modifications require a Decision Record entry (DR) referencing the approval meeting or issue, recorded both in front matter and the `## Decision Records` section.
- **Validation**: Before merge, run `npm run lint-docs` (to be defined) and `python tools/validate_frontmatter.py` (backlog) to verify schema compliance. Link checking must pass via `mkdocs build --strict` or an equivalent CI gate.

## Versioning & Branching

- Primary branch: `main`
- Documentation working branch: `docs/frontiers-v1`
- Release cadence: Monthly for incremental updates; quarterly for major version revision aligning with standard refreshes.
- Version tags reflect the doc system release, not the product codebase. For example, `v1.1.0` will coincide with the next SSDF or ASVS refresh.

## Integration Map

| Capability             | Source Markdown                    | Machine Policy                               | Automation hook                         |
| ---------------------- | ---------------------------------- | -------------------------------------------- | --------------------------------------- |
| Secure SDLC            | `security/nist-ssdf.md`            | `frontiers/policy/ssdf-mapping.yml`          | `frontiers/quality-gate.yml#sast`       |
| Supply-chain integrity | `supply-chain/slsa-provenance.md`  | `frontiers/policy/slsa-policy.yml`           | `frontiers/quality-gate.yml#provenance` |
| Product quality        | `quality/iso-25010-rubric.md`      | n/a                                          | `frontiers/quality-gate.yml#unit-tests` |
| Agent safety           | `security/llm-top10-guardrails.md` | `frontiers/policy/llm-top10-controls.yml`    | Benchmarks policy + smoke suites        |
| Benchmark governance   | `benchmarks/*.md`                  | `frontiers/policy/benchmark-policy.yml`      | Benchmark jobs (optional toggle)        |
| Compliance manifest    | `workflows/compliance-manifest.md` | `frontiers/compliance/manifest-template.yml` | Waiver reminder + downstream validation |

## Decision Records

- **DR-2025-11-05-Index** — Ratified MkDocs migration and machine-readable metadata gatekeepers.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://csrc.nist.gov/pubs/sp/800/218/final">NIST SP 800-218 Rev.1 (v1.1)</a>; <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS 4.0.3</a>; <a href="https://slsa.dev/blog/2025/04/slsa-1.1-is-here">SLSA 1.1 release</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers">Repository inventory</a><br>
<strong>Methods:</strong> Reviewed control-traceability-matrix.json, FRAMEWORK.md, and AGENT-docs-job.md directives to align nav and metadata schema.<br>
<strong>Key results:</strong> MkDocs scaffolding with Material theme; YAML schema enforcing provenance; nav mapping published.<br>
<strong>Uncertainty:</strong> Legacy Jupyter Book content pending archival decision; CI hook for schema validation under development.<br>
<strong>Safer alternative:</strong> Deploy documentation behind staging gateway until linkcheck and schema validation are automated.
</div>

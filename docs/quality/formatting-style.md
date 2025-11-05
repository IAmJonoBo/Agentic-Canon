---
title: "Formatting & Style Harmonisation"
summary: "Defines unified formatting, naming, and documentation standards so teams ship consistent, review-friendly code across languages."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - quality
  - formatting
  - developer-experience
sources:
  - "https://peps.python.org/pep-0008/"
  - "https://google.github.io/styleguide/jsguide.html"
decision_records:
  - id: "DR-2025-11-05-Formatting"
    title: "Adopted cross-language formatting and documentation policy"
    link: "docs/quality/formatting-style.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "PEP 8 — Style Guide for Python Code"
      url: "https://peps.python.org/pep-0008/"
      type: "primary"
    - name: "Google JavaScript Style Guide"
      url: "https://google.github.io/styleguide/jsguide.html"
      type: "primary"
    - name: "Repository conventions inventory"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/CONVENTIONS.md"
      type: "secondary"
  methods:
    - "Unified existing language-specific style guides and automation hooks into a single policy."
    - "Mapped formatting expectations to tooling (pre-commit, quality gate) to guarantee enforcement."
  key_results:
    - "Standardised formatting matrix, naming conventions, and docstring requirements."
    - "Defined automated enforcement and exceptions process."
  uncertainty: "Future language additions require extension of the matrix; track via CONVENTIONS.md."
  safer_alternative: "Adopt stricter community style guides when conflict arises."
---

# Formatting & Style Harmonisation

## Summary

1. Consistent formatting reduces review friction and accelerates onboarding, while reinforcing automated tooling discipline.citeturn15search0
2. Every repository must adopt pre-configured formatters and style guides; deviations require formal approval.
3. Documentation (README, ADRs, API docs) observes the same clarity and structure standards to streamline human and agent consumption.

## Formatting Matrix

| Language / Domain | Formatter              | Linter            | Style Guide          | Notes                                  |
| ----------------- | ---------------------- | ----------------- | -------------------- | -------------------------------------- |
| Python            | Black (line length 88) | Ruff              | PEP 8                | Enforce docstrings for public APIs     |
| TypeScript/JS     | Prettier (tabWidth 2)  | ESLint (strict)   | Google JS Style      | Require TypeScript strict mode         |
| Go                | gofmt + goimports      | golangci-lint     | Effective Go         | Add module documentation comments      |
| Terraform         | terraform fmt          | tflint, checkov   | HashiCorp style      | Enforce module README format           |
| Markdown/Docs     | markdownlint           | custom link check | Diátaxis conventions | Validate front matter + Oxford English |

## Automation

1. `pre-commit` enforces formatters locally; run `pre-commit run --all-files` before committing.
2. CI verifies formatting via `frontiers/quality-gate.yml#lint-and-format`; failures block merge.
3. Documentation formatting validated by `doc-sanity-check.yml` plus `mkdocs build --strict`.

## Naming & Structure

- Use descriptive names (`verbNoun` for functions, `PascalCase` for types).
- Keep files ≤ 500 lines; break modules logically by domain.
- Ensure tests mirror source tree structure (`tests/<module>/<feature>_test.py`).
- Document public APIs with docstrings or JSDoc; include examples and edge cases.

## Exceptions

- Temporary deviations (e.g., upstream generated code) must include `fmt: off` annotations with justification and expiry.
- Track exceptions in `docs/workflows/triage-and-exceptions.md#quality-waivers` (add section).
- Revisit exceptions quarterly; automation backlog monitors outstanding overrides.

## Decision Records

- **DR-2025-11-05-Formatting** — Approved cross-language formatting policy tied to automated enforcement.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://peps.python.org/pep-0008/">PEP 8</a>; <a href="https://google.github.io/styleguide/jsguide.html">Google JavaScript Style Guide</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/CONVENTIONS.md">Repository conventions</a><br>
<strong>Methods:</strong> Harmonised language-specific guides with existing conventions and automation steps.<br>
<strong>Key results:</strong> Formatting matrix, automation expectations, exception handling.<br>
<strong>Uncertainty:</strong> New languages require matrix updates.<br>
<strong>Safer alternative:</strong> Default to stricter community style guides when conflicts arise.
</div>

---
title: "Static Analysis & Code Review"
summary: "Defines unified policies for static application security testing (SAST), linters, and automated code review across the n00-frontiers ecosystem."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "reference"
tags:
  - quality
  - security
  - sast
sources:
  - "https://csrc.nist.gov/pubs/sp/800/218/final"
  - "https://www.synopsys.com/blogs/software-security/whats-next-static-analysis/"
decision_records:
  - id: "DR-2025-11-05-StaticAnalysis"
    title: "Standardised static analysis and linting policies"
    link: "docs/quality/static-analysis.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "NIST SSDF SP 800-218 Rev.1"
      url: "https://csrc.nist.gov/pubs/sp/800/218/final"
      type: "primary"
    - name: "Synopsys static analysis best practices (2025)"
      url: "https://www.synopsys.com/blogs/software-security/whats-next-static-analysis/"
      type: "secondary"
    - name: "Repository automation inventory"
      url: "https://github.com/IAmJonoBo/n00-frontiers"
      type: "secondary"
  methods:
    - "Mapped SSDF PW.4 and OWASP SAMM verification practices to the current automation surface."
    - "Benchmarked tool capabilities against 2025 static analysis trend report."
  key_results:
    - "Defined policy tiers for SAST, linters, and review automation with measurable thresholds."
    - "Documented enforcement hooks and issue management expectations."
  uncertainty: "Language-specific rule packs may require tuning; monitor false-positive rates quarterly."
  safer_alternative: "Escalate to manual review when static tooling confidence drops below target precision."
---

# Static Analysis & Code Review

## Summary

1. Static analysis underpins SSDF PW.4 expectations and remains mandatory for every merge, with enforcement tuned per language.
2. Unified linting and formatting policies reduce cognitive load and enforce baseline quality before code review.
3. Automated review bots complement human reviewers by triaging findings, tracking metrics, and escalating regressions.

## Policy Tiers

| Tier   | Scope                             | Required Tools                                                     | Thresholds                                | Evidence                               |
| ------ | --------------------------------- | ------------------------------------------------------------------ | ----------------------------------------- | -------------------------------------- |
| Bronze | Documentation-only or prototypes  | Markdown lint (`markdownlint`), schema validation                  | 0 blocking lint errors                    | `doc-sanity-check.yml` logs            |
| Silver | Services without critical data    | SAST (language-specific), lint/format, dependency license scan     | 0 critical/high SAST findings; lint clean | `frontiers/quality-gate.yml` artefacts |
| Gold   | Production services, AI pipelines | SAST + secret scan + IaC scan, custom rulesets, AI prompt scanning | Block on medium+ issues without waiver    | SARIF + waiver record                  |

## Toolchain Requirements

- **Python**: Ruff (lint), mypy (strict types), Bandit (security), Semgrep (policy rules).
- **JavaScript/TypeScript**: ESLint (strict), TypeScript `--strict`, Semgrep or SonarJS for SAST.
- **Go**: `golangci-lint`, `gosec`, baseline `go vet`.
- **Infrastructure**: Checkov or Terrafirma for Terraform; `tflint` for style.
- **AI artefacts**: Prompt/flow validation via custom Semgrep/AST rules; dataset manifest linting.

## Automation Hooks

1. `frontiers/quality-gate.yml#sast` runs CodeQL and Semgrep on every PR.
2. Project-specific linters run via `pre-commit` and fail fast locally.
3. SARIF uploads surface findings in GitHub Security tab; CodeQL auto-triage rules route noise to backlog.

## Metrics & Reporting

- Track SAST coverage (% of repos with enforced runs), mean time to remediate, and recurring finding volume.
- Mutation score and coverage metrics provide secondary validation for code quality gates.
- Quarterly analysis identifies rule packs needing calibration; log adjustments in `docs/workflows/triage-and-exceptions.md`.

## Waivers

- Allowed only with documented mitigation, expiry ≤ 30 days, and owner sign-off.
- Store waiver IDs in compliance manifest and cross-reference in PR body.
- Automation reminder (backlog) will ping owners five days before expiry.

## Decision Records

- **DR-2025-11-05-StaticAnalysis** — Approved three-tier SAST policy and toolchain requirements.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://csrc.nist.gov/pubs/sp/800/218/final">NIST SSDF SP 800-218 Rev.1</a>; <a href="https://www.synopsys.com/blogs/software-security/whats-next-static-analysis/">Synopsys 2025 SAST best practices</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers">Automation inventory</a><br>
<strong>Methods:</strong> Aligned SSDF PW.4 with industry SAST guidance and existing workflow automation; defined tiered policy and reporting expectations.<br>
<strong>Key results:</strong> Policy tiers, toolchain requirements, metrics, waiver governance.<br>
<strong>Uncertainty:</strong> Rule packs may require tuning; monitor false positives.<br>
<strong>Safer alternative:</strong> Escalate critical code paths to manual review when automated confidence is low.
</div>

# n00-frontiers — Unified Playbook and Implementation Guide

Version: 1.0.0 (Last updated: 2025-10-11)

- Next: v1.1.0 — Azure Pipelines, more dashboards, additional examples, video tutorials, interactive wizard
- Future: v2.0.0 — Multi-cloud support, advanced fitness functions, ML-powered insights, full automation, community templates

---

## Overview

This single document unifies two parts of the canon:

- Strategy and guardrails: Frontier Software Excellence & Red-Team Copilot Playbook (principles, standards, risk posture).
- Concrete implementation: Repository layout, CI/CD, docs, notebooks, and Cookiecutter templates you can drop in and run.

Use this when you want one source of truth that explains what to do (playbook) and exactly how to do it (implementation), with agent- and Copilot-friendly notes.

---

## Table of Contents

1. Mission, Scope, and Outcomes
2. Excellence Playbook (Red-Team + Software Excellence)
3. Implementation Blueprint (Drop-in files and workflows)
   - Repo layout
   - Configuration files
   - Jupyter Book source
   - GitHub Actions workflows
   - One-time setup
   - Minimal notebooks and intents
   - Cookiecutter multi-template repository
   - Hooks, tests, CI for templates
   - Optional extras (Storybook, golangci-lint, Pages)
4. Copilot Notes on Implementation (Do not delete)
5. Paths to Adoption (Greenfield/Brownfield/Platform)
6. Standards Coverage and Traceability
7. References and Appendices

---

## 1) Mission, Scope, and Outcomes

Operate as a Frontier Software Excellence & Red-Team Copilot to raise security, delivery speed, developer experience, product quality, and long-term evolvability to frontier practice. Deliver:

- Evidence-backed findings mapped to standards with severity, confidence, and remediation.
- PR-ready artefacts (files/diffs), pipelines, and policies.
- A 30/60/90-day plan with dependencies, owners, and measurable outcomes.
- An agent-oriented runbook and a control traceability matrix for auditability.

---

## 2) Excellence Playbook (Red-Team + Software Excellence)

Below is the merged and slightly reorganized content from “Red Team + Software Excellence.md”. The original sections are preserved and can be navigated by headings. Use this as the governing strategy and guardrails.

### 2.0 Mission & Operating Mode

- Multi-expert ensemble (Platform/DevEx, Security/Supply-chain, SRE/Observability, Architecture, Product/UX, QA/Testing). Capture rationale → alternatives → trade-offs.
- Evidence, standards mapping, and prioritisation by Risk = Likelihood × Impact and Delivery Leverage.
- Deliver a single Markdown report, PR artefacts, and a 30/60/90-day plan with a dependency/tooling matrix.

### 2.1 Project Context Inputs

Define project, paths to scan, stack, priorities, standards, and constraints. See matrix fields in the original playbook.

### 2.2 Discovery → Objectives → Measures

- Clarify mission, constraints, personas, risks.
- Instrument DORA and SPACE metrics from the start.

### 2.3–2.13 Core Analyses and Guardrails

Perform: rapid system model, threat modeling (STRIDE, MITRE ATT&CK), supply-chain posture, SSDF/SAMM/ASVS/SLSA gap analysis, DX/SPACE & IDP review, UX/WCAG, quality gates (SAST/DAST, contracts, mutation testing), architecture future-proofing (C4, ADRs, OTel, SLOs), automation/GitOps, tool-chain radar, concrete improvements codified as PRs, roadmap, critical-reasoning checks, and governance guardrails.

### 2.14 Output Format (Exactly)

Provide: Executive Summary, Findings (Title • Severity • Confidence • Evidence • Affected assets) with standards mapping and residual risk; Supply-Chain Posture; Delivery, DX & UX; PR-ready diffs; 30/60/90 plan; Assumptions & Unknowns; Appendix; Dependency & Tooling Matrix; Research Log; Control Traceability Matrix; Agent Runbook & Handover Docs.

### 2.15 Guardrails & Governance

- Mark inferences; prefer reversible changes with flags; treat LLM code like human code (tests, scans, contracts, review).
- Verify cross-tool compatibility, licenses, and vendor/community support horizons.
- Prevent scope creep; require stakeholder approvals for expansions.

### 2.16 Copilot & Agent Reality Checks

Apply SSDF, OWASP LLM Top-10, ASVS-aligned gates; identity-scoped retrieval; DLP; sandboxed tools; forbid hallucinated dependencies; SBOM + attestations; immutable lockfiles.

### 2.17 Frontier Control Set (Embed in Scaffolding)

Security gates, supply chain hardening (SLSA 2→3), testing pyramid with mutation testing, DX guardrails, UX excellence, and post-incident learning requirements.

### 2.18–2.22 Blueprint Highlights

Architecture and future-proofing (C4, ADRs, fitness functions); tech stack and contracts; first-run bootstrap; layered quality and testing; security & supply-chain depth; reliability with SLOs and incident workflow; DevEx enablement; UX & product excellence; AI/ML governance; automation and autoremediation; continuous improvement; non-negotiable gates; expected agent outputs; performance & simplicity principles; and a minimal “Run Now” checklist.

> Full, unabridged text of the playbook is incorporated from the source file. For any section not quoted verbatim above, see “Red Team + Software Excellence.md” in this repository; this unified guide keeps the same intent and structure while aligning it to the implementation below.

---

## 3) Implementation Blueprint (Drop-in files and workflows)

This section merges the concrete scaffolding and examples from “INSTRUCTIONS.md” into a coherent, step-by-step implementation guide. Each subsection can be applied independently; combine them for full coverage.

### 3.1 Repo layout

Recommended top-level structure for notebooks, docs, CI, and environment files, enabling Jupyter Book publishing and CI notebook execution:

```text
notebooks/
  01_bootstrap.ipynb
  02_security_supply_chain.ipynb
  03_contracts_and_tests.ipynb
  04_observability_slos.ipynb
  05_docs_to_book.ipynb

docs/
  _config.yml
  _toc.yml
  intro.md
  notebooks/           # MyST mirrors of ipynb via Jupytext pairing

binder/
  requirements.txt

.pre-commit-config.yaml
jupytext.toml
.gitattributes
requirements.txt

.github/workflows/
  notebooks-test.yml
  book-deploy.yml
  notebooks-schedule.yml
```

Why this: Jupytext pairs ipynb↔MyST, nbmake executes notebooks in CI, nbstripout removes outputs, GitHub Actions deploys Jupyter Book, and Binder gives a reproducible environment.

### 3.2 Configuration files

- `jupytext.toml`: pair `notebooks/` ipynb → `docs/notebooks/` MyST.
- `.gitattributes`: nbstripout filters for notebooks to keep Git diffs clean.
- `.pre-commit-config.yaml`: enable nbstripout and jupytext sync hooks.
- `requirements.txt`: jupyter, jupytext, nbstripout, pytest, nbmake, papermill, jupyter-book.
- `binder/requirements.txt`: `-r ../requirements.txt` for repo2docker/Binder.

### 3.3 Jupyter Book source

Minimal `docs/_config.yml`, `docs/_toc.yml`, and `docs/intro.md` to publish the book and include MyST-rendered notebook mirrors.

### 3.4 GitHub Actions workflows

Provide three workflows:

- `notebooks-test.yml`: run nbmake over notebooks on PR/push.
- `book-deploy.yml`: build and publish Jupyter Book to gh-pages.
- `notebooks-schedule.yml`: scheduled Papermill execution for parameterized runs.

### 3.5 One-time setup

- `pip install -r requirements.txt`
- `pre-commit install`
- Pair existing notebooks: `jupytext --set-formats ipynb,md:myst notebooks/*.ipynb && jupytext --sync notebooks/*.ipynb`

### 3.6 Minimal notebook intents (agent-friendly)

1. Bootstrap: scaffold repo, enable gates, SBOM/signing demo (param `run_mode`).
2. Security & supply chain: SAST/secrets scan, SBOM & provenance.
3. Contracts & tests: OpenAPI/AsyncAPI; contract + mutation tests.
4. Observability & SLOs: OTel quickstart & SLO probes.
5. Docs-to-book: Jupytext sync and Jupyter Book build driver.

### 3.7 Cookiecutter multi-template repository

Support multiple templates under `templates/` with a Python-service baseline and optional Node/React/Go/Docs templates. Use `cookiecutter --directory` to select a sub-template. Include validation hooks and tests (`pytest-cookies`) to ensure templates render and are usable out-of-the-box.

Key elements:

- `cookiecutter.json` with options (include_jupyter_book, enable_security_gates, sbom_signing, contracts, ci_provider).
- Hooks: input validation (`pre_gen_project.py`) and post-render bootstrap/cleanup (`post_gen_project.py`).
- Tests: `tests/test_cookiecutters.py` to bake and validate a project.
- CI: `cookiecutters-test.yml` to run pytest in CI on push/PR.
- Cruft: recommend to keep generated projects in sync with templates over time.

### 3.8 Template CI examples

- Python service CI: build, test, coverage, nbmake notebook checks.
- Node service CI: build and test on Node 20 with caching via `actions/setup-node`.
- Webapp E2E CI: Playwright with webServer and multi-browser projects.

### 3.9 Optional extras

- React webapp Storybook (Vite builder) with accessibility addon and CI to build/upload artifact, plus a GitHub Pages deployment workflow.
- Go service `golangci-lint` config and CI using `golangci-lint-action`.

---

## 4) Copilot Notes on Implementation (Do not delete)

These instruction blocks are preserved verbatim for automation. Paste them into Copilot/agent chats to scaffold and wire everything quickly. Treat them as implementation notes; they do not replace human review or standards gates.

### 4.1 Repo Scaffolder Copilot — Notebooks and Book

You are Repo Scaffolder Copilot for "n00-frontiers".

1. Create folders/files exactly as in the provided tree.
2. Write `jupytext.toml` that pairs `notebooks/` (ipynb) → `docs/notebooks/` (md:myst).
3. Add `.gitattributes` and `.pre-commit-config.yaml` to strip outputs and sync pairs.
4. Add `requirements.txt` with jupyter, jupytext, nbstripout, pytest, nbmake, papermill, jupyter-book.
5. Create `docs/_config.yml`, `docs/_toc.yml`, `docs/intro.md` per Jupyter Book.
6. Add three workflows: `notebooks-test.yml` (pytest --nbmake), `book-deploy.yml` (jupyter-book build + ghp-import), `notebooks-schedule.yml` (papermill).
7. Generate 5 small, parameterised notebooks matching the names; include a top “Parameters” cell for papermill.
8. Run pre-commit install and output the commands I must execute locally.
   Abide by Jupytext/Jupyter Book conventions; no outputs checked in; fail on CI errors.

### 4.2 Tiny Copilot brief — Cookiecutter multi-templates

Repo task: Add Cookiecutter multi-templates under /templates (python-service, node-service, react-webapp, go-service, docs-only). Each has cookiecutter.json, hooks, and CI workflows. Add tests/test_cookiecutters.py using pytest-cookies; add cookiecutters-test.yml to render on PRs. Document usage with cookiecutter --directory and Cruft sync. No outputs in Git, hooks validate slugs.

### 4.3 Copilot task — Node/React/Go templates and CI seeds

Repo task: add Cookiecutter sub-templates for node-service, react-webapp (Vite+TS+Playwright), and go-service. Use files shown in the canon. Ensure Node uses `@tsconfig/node20` and `tsx`; React uses `@vitejs/plugin-react-swc` and Playwright config with `webServer`; Go has `go.mod 1.22` and `Makefile`. Add CI seeds (`node-ci.yml`, `webapp-e2e.yml`). Output the exact changes as diffs.

### 4.4 Copilot task — React Storybook and Go golangci-lint

React webapp: add Storybook (React+Vite). Update package.json (storybook scripts, devDeps), add .storybook/{main.ts,preview.ts}, add Button.tsx + Button.stories.tsx, and .github/workflows/storybook-build.yml that builds and uploads artifact.

Go service: add .golangci.yml and .github/workflows/go-lint.yml using golangci-lint-action (v8 action, tool v2.1). Keep diffs small; no breaking changes.

### 4.5 Copilot task — Storybook deploy to Pages

Add .github/workflows/storybook-pages.yml to the react-webapp template. Build with `npm run build-storybook`, upload via `actions/upload-pages-artifact@v3`, deploy with `actions/deploy-pages@v4`. Remind to set Settings → Pages → Source: GitHub Actions and surface the public URL from job output.

---

## 5) Paths to Adoption

Choose the path that matches your context. Commands are examples; adapt build/test tools by language.

### 5.1 New Project (Greenfield)

1. Use Backstage service template (golden path) or copy from `templates/`.
2. Initialize CI/CD using `templates/cicd/github-actions/complete-pipeline.yml` and SBOM workflow.
3. Replace placeholders and validate with `actionlint`.
4. Commit and push; PRs should trigger all gates.

### 5.2 Existing Project (Brownfield)

1. Assess current state using `control-traceability-matrix.json`.
2. Add security scanning and SBOM generation workflows.
3. Add repository files like `SECURITY.md` and `CONTRIBUTING.md`.
4. Validate, commit, and push; address gate failures.

### 5.3 Platform Setup

1. Deploy Backstage and publish service templates.
2. Configure SLOs and policies (OPA/Kyverno) and enable GitOps.
3. Onboard teams via golden paths with guardrails baked in.

---

## 6) Standards Coverage and Traceability

This canon targets NIST SSDF v1.1, OWASP SAMM, SLSA (≥ L3 for builds), OWASP ASVS 4.0 (L2/L3), OpenSSF Scorecard, ISO/IEC 25010 & 5055, and WCAG 2.2 AA. See:

- `control-traceability-matrix.json` for machine-readable control → implementation → evidence mappings.
- `runbooks/agent-runbook.json` for machine-executable steps and rollback paths.

---

## 7) References and Appendices

- Notebooks: `notebooks/01_bootstrap.ipynb` … `05_docs_to_book.ipynb` (pair with MyST and run in CI).
- Docs: Jupyter Book sources in `docs/` with gh-pages deployment workflow.
- Templates: see `templates/` for Cookiecutter baselines and CI examples.
- Examples: see `examples/` for Azure Pipelines, dashboards, and multi-cloud notes.
- Original Sources: `INSTRUCTIONS.md`, `Red Team + Software Excellence.md` (merged here).

---

Notes

- Treat AI/Copilot output as untrusted until gated by tests, scans, contracts, and reviews.
- Prefer reversible, small PRs guarded by feature flags and progressive delivery.
- Keep generated artefacts and controls auditable; update the control matrix as you evolve.

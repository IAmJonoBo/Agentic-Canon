---
title: "Pre-commit Workflow"
summary: "Guides contributors through installing and using pre-commit hooks that enforce formatting, notebook hygiene, and sanity checks."
version: "1.0.0"
last_verified: "2025-11-05"
last_verified_tz: "Africa/Johannesburg"
diataxis: "tutorial"
tags:
  - workflow
  - pre-commit
  - developer-experience
sources:
  - "https://github.com/pre-commit/pre-commit"
  - "https://github.com/IAmJonoBo/n00-frontiers/blob/main/CONTRIBUTING.md"
decision_records:
  - id: "DR-2025-11-05-PreCommit"
    title: "Established standard pre-commit workflow for contributors"
    link: "docs/workflows/pre-commit.md#decision-records"
    status: "accepted"
provenance:
  data:
    - name: "Pre-commit documentation"
      url: "https://github.com/pre-commit/pre-commit"
      type: "primary"
    - name: "CONTRIBUTING.md"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/CONTRIBUTING.md"
      type: "secondary"
    - name: ".pre-commit-config.yaml"
      url: "https://github.com/IAmJonoBo/n00-frontiers/blob/main/.pre-commit-config.yaml"
      type: "secondary"
  methods:
    - "Condensed CONTRIBUTING setup steps into tutorial-style workflow."
    - "Documented repo-specific hooks and troubleshooting tips."
  key_results:
    - "Step-by-step installation instructions, hook breakdown, and automation integration."
  uncertainty: "Local tool availability (Python, pip) may vary; provide alternatives as backlog."
  safer_alternative: "Use Docker-based dev container if local setup diverges."
---

# Pre-commit Workflow

## Summary

1. Pre-commit hooks ensure notebooks stay clean, Jupytext pairs sync, and sanity checks run before CI.
2. Contributors install hooks once, then run `pre-commit run --all-files` to validate before pushing.
3. Hooks align with guidance in `CONTRIBUTING.md` and integrate with quality gate expectations.

## Install Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

For Poetry:

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## Hook Breakdown

| Hook              | Purpose                                     | When it runs                                     |
| ----------------- | ------------------------------------------- | ------------------------------------------------ |
| `nbstripout`      | Remove notebook outputs to keep diffs clean | Every commit touching `.ipynb`                   |
| `jupytext --sync` | Sync `.ipynb` with `.md` MyST mirrors       | Every commit touching notebooks                  |
| `sanity-check`    | Runs `.dev/sanity-check.sh --quiet`         | Every commit; fails fast on repo inconsistencies |

Template repositories add additional hooks (lint, formatting) automatically—run `pre-commit autoupdate` quarterly.

## Recommended Workflow

1. Create branch: `git checkout -b feat/<topic>`.
2. Make changes; run `pre-commit run --all-files` before committing.
3. Resolve any hook failures (e.g., re-run `jupytext --sync` if notebooks changed).
4. Commit with Conventional Commit message.
5. Push branch; quality gate will re-run hooks as part of lint job.

## Troubleshooting

- **Missing nbstripout**: reinstall via `pip install nbstripout`.
- **Large notebook diffs**: ensure Jupyter saves without outputs, or run `nbstripout notebook.ipynb`.
- **Sanity-check issues**: run `.dev/sanity-check.sh` manually to view section-specific failures.

## Decision Records

- **DR-2025-11-05-PreCommit** — Developer experience guild standardised pre-commit workflow steps.

## Provenance

<div class="provenance-block">
<strong>Data:</strong> <a href="https://github.com/pre-commit/pre-commit">Pre-commit documentation</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/CONTRIBUTING.md">Repository contributing guide</a>; <a href="https://github.com/IAmJonoBo/n00-frontiers/blob/main/.pre-commit-config.yaml">Pre-commit configuration</a><br>
<strong>Methods:</strong> Combined CONTRIBUTING steps with hook configuration to produce workflow-specific tutorial.<br>
<strong>Key results:</strong> Installation steps, hook breakdown, troubleshooting guidance.<br>
<strong>Uncertainty:</strong> Local tooling may differ.<br>
<strong>Safer alternative:</strong> Use dev container if local environment differs significantly.
</div>

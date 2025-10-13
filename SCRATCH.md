# Implementation Instructions for the Next Agent

## Objective

Solidify template validation so every run performs manifest sync, template rendering, linting, and formatting in one automated flow while fixing import errors and updating CI/docs.

## Preparation

- Use repo root `Agentic-Canon`
- Activate the virtualenv: `source .venv/bin/activate`
- Ensure core deps installed: `pip install -r requirements.txt`
- Most tasks rely on `noxfile.py`, `validate-templates.sh`, and `README.md`; check for user edits before touching them

## Implementation Steps

### Current Progress

- Added deterministic `PYTHONPATH` bootstrapping in `tests/conftest.py`, `.dev/validate-templates.sh`, and every template hook so pytest, Nox, and cookiecutter executions all discover `templates._shared` without ad-hoc path tweaks.
- Modernized Ruff configuration to the `[tool.ruff.lint]` schema, added template-specific ignores for jinja placeholders, and cleaned up outstanding lint violations (unused imports, outdated typing aliases, and f-string warnings).
- Wrapped the project-management `tasklist-scan.yml` workflow in a conditional block so disabling tasklist automation now yields an empty artifact, matching the pytest expectation.
- Project-management cookiecutter test now passes in isolation, confirming the workflow gating fix. 【ea3314†L1-L3】
- Repository-level `ruff check` now completes cleanly after the config migration. 【6e0b69†L1-L2】
- Baseline reruns show Node and React end-to-end template tests still failing due to npm install/test conflicts (Storybook peer dependency and Vitest exit), blocking full suite success. 【3078d5†L1-L161】

### 1. Add Unified Validation Session

In `noxfile.py`, create a new session (e.g., `@nox.session` named `validate_templates_all`) that executes, in order:

1. `sync_manifest`
2. `render_templates`
3. `lint_templates`
4. `format_templates`

**Requirements:**

- Session should forward `session.posargs` to `render_templates`, `lint_templates`, and `format_templates` so feature filters still work
- Use `session.notify("other_session", posargs=session.posargs)` to run the chained sessions
- Document timing with the existing `_session_timer`

### 2. Fix PYTHONPATH for Template Imports

Update `render_templates` session in `noxfile.py`:

- Before importing from `templates._shared`, ensure `session.env["PYTHONPATH"]` includes repo templates directory
- This prevents `ModuleNotFoundError` when Nox runs outside repo root

**Example:**

```python
session.env["PYTHONPATH"] = str(Path.cwd() / "templates")
```

### 3. Enhance validate-templates.sh

- Add a CLI flag (e.g., `--all`) that invokes `nox -s validate_templates_all` by default when no other flags are provided
- Keep existing behaviors (`--linters`, `--format`) intact
- Ensure the script gracefully handles pre-existing caches and passes through template filters

### 4. Update Documentation

In `README.md`, document:

- New Nox session name and purpose
- Updated instructions showing `validate-templates.sh` default flow includes sync + render + lint + format
- Mention the PYTHONPATH fix only if user-facing (optional)
- If `DIRECTORY_STRUCTURE.md` or `README.md` reference validation tooling, adjust summaries (one sentence) to note the unified session

### 5. CI Integration

Modify workflows as needed (likely `ci.yml` or lint-focused workflow) so the unified session replaces individual lint/format steps.

**Example job step:**

```yaml
- name: Validate templates
  run: nox -s validate_templates_all
```

Make sure the workflow installs nox and dependencies before calling the session.

### 6. Validation

- Run `nox -s validate_templates_all` locally; expect it to regenerate manifests, render templates, run Trunk lint, and confirm formatting without errors
- Follow up with targeted tests:

  ```bash
  pytest tests/test_manifest_sync.py
  pytest tests/test_template_e2e.py
  ```

- Fix any Trunk lint failures encountered during the run

### 7. Final Checks

- Review `git status`; ensure only intended files changed (noxfile, shell script, docs, workflow)
- Avoid touching user modifications unless coordinated
- Provide a concise summary with validation commands executed

### YAML Formatting Guardrails

- Confirm `.trunk/trunk.yaml` keeps both `prettier` and `yamllint` enabled for `**/*.yml` and `**/*.yaml` so indentation and style stay consistent across the repo.
- After modifying or generating YAML, run `.dev/validate-templates.sh` (or `nox -s format_templates`) to let Trunk apply formatting before committing changes.
- For generated YAML (e.g., manifest sync, cookiecutter hooks), rely on Trunk’s formatter rather than manual whitespace tweaks; re-run the formatter after generation.
- Optionally wire up the pre-commit helper (`.dev/install-precommit.sh`) to call `trunk fmt --staged`, ensuring staged YAML is auto-formatted.

## Pipeline Remediation Plan

### Baseline Findings

- `pytest` now completes the project-management cookiecutter path but still fails for Node (`npm run test`) and React (`npm install` Storybook conflict); both require dependency remediation before the unified suite can pass. 【3078d5†L1-L161】
- `ruff check` previously reported 41 issues and configuration deprecation warnings; the migration to `[tool.ruff.lint]` and lint clean-up brings the command to a clean pass. 【c61c7e†L1-L83】【6e0b69†L1-L2】
- `mypy` has no configured targets; running the command exits with an error because no modules are specified. 【2458de†L1-L4】
- Security scanning tooling (e.g., TruffleHog/Gitleaks) is referenced in docs and workflows, but local command coverage has not been verified during the baseline run. `pip-audit` currently passes with pinned dependencies. 【695db8†L1-L2】

### Remediation Strategy

1. **Stabilize Environment Bootstrapping**
   - Update Nox sessions (`render_templates`, `validate_templates_all`) to prepend both repo root and `templates/` paths to `PYTHONPATH`, matching documented expectations for template hooks. This should eliminate the `_shared` import failures during pytest runs.
   - Extend `.dev/validate-templates.sh` to export equivalent environment variables so CLI usage mirrors CI behavior.

2. **Harden Template Hooks and Shared Utilities**
   - Audit `templates/_shared` to confirm it exposes importable hook utilities without relying on implicit relative paths.
   - Refactor hook scripts to avoid top-level sys.path manipulations where possible; encapsulate shared behaviors in a dedicated module within `_shared` and ensure packaging metadata (e.g., `__init__.py`) supports module discovery.
   - Add targeted unit tests under `tests/` to exercise hook modules directly, guarding against regressions.

3. **Consolidate Linting/Formatting Workflow**
   - Refactor root and template-level Ruff configurations to the modern `[tool.ruff.lint]` layout and tighten rule coverage called out in `QUALITY_STANDARDS.md`. *(Status: Completed; configs migrated and legacy warnings resolved.)*
   - Update rendered project scaffolds (e.g., `pyproject.toml`, `.ruff.toml`) so `ruff check` and `ruff format` run cleanly across all template variants. *(Status: FastAPI example + Python template updated; confirm other templates after full render pass.)*
   - Extend `validate_templates_all` to invoke `ruff check` after rendering (mirroring CI) and gate merges on a lint-clean workspace.
   - Ensure formatting tools (Black, Prettier, gofmt, rustfmt) run as part of the session, per automation guardrails.

4. **Define Type-Checking Coverage**
   - Document intended type-check targets (core CLI, shared template utilities) in `SCRATCH.md` and configure `mypy.ini`/`pyproject.toml` with explicit module lists and strictness levels.
   - Introduce a dedicated `typecheck` Nox session (wrapping `mypy`) and have `validate_templates_all` notify it after linting unless explicitly skipped via CLI flag.
   - Cache `.mypy_cache` per-rendered project when feasible to keep the unified flow performant.

5. **Verify Security and Compliance Hooks**
   - Wire `.dev/validate-templates.sh` to call TruffleHog/Gitleaks via an opt-in flag that also runs inside `validate_templates_all` for CI gating.
   - Update pipeline documentation to clarify local vs. CI security coverage, including remediation SLAs and evidence capture expectations.

6. **CI/CD Alignment**
   - Review GitHub Actions workflows to ensure they call the updated unified session and propagate environment fixes. Capture the order of operations in the plan to avoid downstream race conditions.
   - Add workflow assertions (e.g., `PYTHONPATH` echo) to aid troubleshooting if imports regress.

7. **Documentation & Change Management**
   - Cross-reference updates in README, TASKS.md, and relevant ADRs to maintain traceability.
   - Record baseline deltas and remediation status in `Next_Steps.md`, updating checkboxes as work progresses.
   - Prepare rollback guidance for each change set (e.g., toggling environment variables, disabling new lint rules) to minimize downstream disruption.

8. **Validation Gates**
   - Once fixes are implemented, re-run baseline commands (`pytest`, `ruff check`, `mypy`, secret scans, builds) and capture outputs.
   - Block release until all gates pass or documented exceptions are approved per governance docs.

### Detailed Gate Integration Blueprint

#### Lint Modernization & Enforcement

- Inventory every Ruff configuration (`pyproject.toml`, `.ruff.toml`, `.trunk/configs/ruff.toml`) and migrate deprecated `[tool.ruff]` keys to the modern `[tool.ruff.lint]` / `[tool.ruff.format]` structure to eliminate warnings surfaced in the latest baseline run.
- Harmonize rule sets: define a shared include/exclude matrix for repository roots and rendered templates, then update cookiecutter scaffolds so downstream projects inherit the same lint posture.
- Extend `validate_templates_all` with a post-render Ruff stage that shells out to `ruff check --output-format text build/template-renders/*` (respecting template filters) and fails fast on violations; plumb a `--skip-lint` switch through `.dev/validate-templates.sh` for emergency bypass.
- Capture autofix guidance—when safe—in documentation so contributors can run `ruff check --fix` locally without breaking template determinism.

#### Type-Check Orchestration

- Author a `mypy.ini` (or update `pyproject.toml`) that explicitly targets `agentic_canon_cli`, `templates._shared`, and new shared utilities, starting with `strict = False` but enabling incremental caches.
- Implement a dedicated `@nox.session(name="typecheck")` that installs `mypy`, respects the configured cache directory, and accepts the same template filter arguments for per-render checks.
- Have `validate_templates_all` notify `typecheck` once linting succeeds; surface skip controls via `--skip-typecheck` flags in both the Nox session and wrapper script.
- Record minimum type coverage expectations in `Next_Steps.md` Quality Gates and cross-link to the governance docs for sign-off criteria.

#### Security Scan Integration

- Keep `pip-audit` in the default validation stack now that it is manifest-pinned; add retries/timeouts to mitigate transient index hangs observed locally.
- Evaluate lightweight secret scanning (`trufflehog filesystem`, `gitleaks detect`) for inclusion under a new `.dev/validate-templates.sh --security` flag that toggles corresponding Nox sessions.
- Document external binary prerequisites (TruffleHog, Gitleaks) in README/TASKS and ensure CI installs pinned versions via cacheable scripts.
- For rendered templates, emit SBOM stubs (CycloneDX JSON) and store them under `build/` so subsequent validation steps can assert their presence.

### Assumptions & Unknowns

- Precise scope of CLI integration for template validation (need to confirm whether additional commands beyond `.dev/validate-templates.sh` require updates).
- Availability of TruffleHog/Gitleaks binaries in contributor environments; may need to document installation prerequisites.
- Potential need for Dockerized execution to mimic CI runner for certain hooks—requires validation.

### Immediate Next Steps

- Confirm ownership of existing `noxfile.py` sessions and gather historical context from ADRs before modifying behavior.
- Draft ADR or update existing records if significant workflow changes are introduced.
- Schedule follow-up baseline run after environment path adjustments to verify import fixes before broader refactors.

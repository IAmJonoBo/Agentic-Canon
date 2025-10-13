# Implementation Instructions for the Next Agent

## Objective

Solidify template validation so every run performs manifest sync, template rendering, linting, and formatting in one automated flow while fixing import errors and updating CI/docs.

## Preparation

- Use repo root `Agentic-Canon`
- Activate the virtualenv: `source .venv/bin/activate`
- Ensure core deps installed: `pip install -r requirements.txt` and `pip install nox`
- Most tasks rely on `noxfile.py`, `validate-templates.sh`, and `README.md`; check for user edits before touching them

## Implementation Steps

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

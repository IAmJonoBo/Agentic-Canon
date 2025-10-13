# Next Steps

## Tasks

- [x] Establish pipeline remediation plan (Owner: Agent, Due: 2025-02-05)
- [x] Harden local/CLI PYTHONPATH bootstrapping so template hooks import cleanly (Owner: Agent, Due: 2025-02-05)
- [x] Re-run baseline validation to confirm import fixes and capture fresh results (Owner: Agent, Due: 2025-02-05) _(pytest manifest test passes; `ruff check` now clean — latest pass chunk 5390e6; `mypy` and remaining gates still outstanding; `pip-audit` vulnerable package noted in chunk 0f9f62)_
- [x] Produce lint/type/security integration design updates for unified validation flow (Owner: Agent, Due: 2025-02-06) _(blueprint recorded in SCRATCH.md §Detailed Gate Integration Blueprint)_
- [x] Migrate Ruff configs to `[tool.ruff.lint]` schema and clear existing lint violations (Owner: Agent, Due: 2025-02-06)
- [x] Resolve React template npm peer dependency conflict so e2e test can pass (Owner: Agent, Due: 2025-02-07) _(storybook/tooling pinned to 8.6 with Node 22 shims; validated via `pytest` chunk 48e64d)_
- [x] Resolve Node template npm/vitest failures uncovered during e2e run (Owner: Agent, Due: 2025-02-07) _(Vitest scripts now bypass shim; `pytest` chunk 48e64d)_
- [x] Configure mypy targets and add a dedicated Nox/typecheck gate (Owner: Agent, Due: 2025-02-07) _(tracked by `mypy.ini` + nox session; clean run chunk 7679c3)_
- [x] Wire CLI auto-fix through template validation flag and quiet pipeline (Owner: Agent, Due: 2025-02-08) _(implemented this pass; regression covered by `pytest tests/test_cli_fix.py` chunk 82e19d)_
- [x] Expand `.dev/validate-templates.sh` / Nox to run lint + type + security stages post-render (Owner: Agent, Due: 2025-02-08) _(sessions wired + passing via `nox -s type_templates` chunk 72b969 and `nox -s security_templates` chunks 58e2e8/077e58)_
- [x] Align cookiecutter/boilerplate quality requirements with unified lint/format CLI updates (Owner: Agent, Due: 2025-02-09) _(React + Node workflows updated; manifest-driven commands exercised via chunks 72b969, 58e2e8, 7ff00d, ceb73c)_
- [x] Investigate `pip-audit` invalid requirements failure and capture remediation plan (Owner: Agent, Due: 2025-02-08) _(`pip-audit -r requirements.txt` now succeeds; see chunk db9029)_
- [x] Diagnose template formatting drift reported by `ruff format --check` before enabling enforcement (Owner: Agent, Due: 2025-02-08) _(`ruff format --check` clean in chunk 56fb10)_
- [x] Ship pip hardening helper and quiet security audits (Owner: Agent, Due: 2025-02-09) _(pip patched via `agentic_canon_cli.pip_support`; spinner disabled; `pip-audit` passes in chunks 3d121b/a0943a)_
- [x] Document safe-pip override controls across CLI + validation flows (Owner: Agent, Due: 2025-02-10) _(AGENTIC_CANON_SKIP_SAFE_PIP and AGENTIC_CANON_SAFE_PIP_SPEC documented + wired into `.dev/validate-templates.sh`)_
- [x] Add validate-templates orchestrator regression coverage (Owner: Agent, Due: 2025-02-11) _(new shell wrapper tests confirm PYTHONPATH seeding and skip controls; see `tests/test_validate_templates_script.py` + pytest chunk 5cd380)_

## Steps

- [x] Document current pipeline baseline results
- [x] Identify root causes for template validation failures (missing PYTHONPATH wiring)
- [x] Propose remediation actions aligned with standards
- [x] Validate PYTHONPATH remediation via pytest + CLI smoke runs (manifest sync test passes; CLI help executes cleanly)
- [x] Finalize lint/type/security extension approach for `validate_templates_all` (blueprint captured; awaiting implementation)
- [x] Capture detailed lint/type/security integration blueprint in SCRATCH.md
- [x] Normalize template hook imports to rely on shared PYTHONPATH helper
- [x] Remove legacy Ruff issues across examples/tests/templates to confirm clean baseline
- [x] Address React npm peer dependency blocker or document mitigation strategy
- [x] Address Node npm/vitest failure highlighted in e2e suite
- [x] Define mypy coverage scope and codify invocation in automation
- [x] Re-ran baseline validation commands to refresh evidence (`pytest` chunk 385380; `ruff check` chunk 5390e6; `mypy` chunk 6ba6e3; `ruff format --check` chunk 56fb10; `pip-audit` chunks 0f9f62/db9029)
- [x] Added CLI regression coverage to confirm template pipeline visibility and skip controls (chunks 5951f9 & 5d3429)
- [x] Captured environment escape hatch for hardened pip tooling so offline runs stay unblocked
- [x] Added regression coverage ensuring `.dev/validate-templates.sh` seeds PYTHONPATH and respects skip flags (`tests/test_validate_templates_script.py`, chunk 5cd380)
- [x] Added Ruff config regression coverage for the Python template to guard against deprecated settings (chunk e8dedd)
- [x] Reviewed template standards/docs to extract cookiecutter + boilerplate quality expectations for upcoming CLI alignment (see TEMPLATE_STANDARDS.md)
- [x] Ensured quick-mode sanity summary stays synchronized with recorded passes and captured regression coverage (`tests/test_sanity_check.py`, pytest chunk cd2c27)
- [x] Added quick-mode HTML report regression coverage so rendered artifacts track recorded passes (`tests/test_sanity_check.py::test_sanity_check_quick_mode_html_report`, pytest chunk 59ba8a)
- [x] Documented the React Storybook 8 upgrade path and added regression coverage for scripts/dependencies (`tests/test_cookiecutters.py::test_react_cookiecutter_storybook_scripts`, pytest chunk 3d7b60)

## Deliverables

- [x] Updated SCRATCH.md with detailed remediation plan
- [x] Baseline command results logged
- [x] Add-on design notes covering lint/type/security flow adjustments
- [x] Conditionalize tasklist workflow output when automation disabled
- [x] Document React/npm resolution plan once validated _(captured via Tasks/Steps updates)_

## Quality Gates

- [x] Tests: pytest (passing end-to-end, including React build fix) _(chunk 895d86)_
- [x] Lint: ruff check (passing; monitor for regressions) _(chunk 511a4c)_
- [x] Type-check: mypy (configured and passing) _(chunk e76474)_
- [x] Security: secret scan (pip patched via helper; `pip-audit` clean) _(chunks d8ebd1/351c8b)_
- [x] Build: applicable build commands succeed _(template renders + audits passing; see chunks f33a16, 8f1475, 58e2e8, 077e58)_

## Links

- [x] SCRATCH.md §Current Progress, Remediation Strategy
- [x] `.dev/validate-templates.sh` PYTHONPATH bootstrapping
- [x] `tests/conftest.py` environment preparation helpers
- [x] Test + lint failure logs (`pytest` chunks d35d86 & c8cb83, `ruff check` chunk c61c7e, `mypy` chunk 3f2957, `pip-audit` chunk 695db8)
- [x] Latest baseline runs (`pytest` chunk 385380; `ruff check` chunk 5390e6; `mypy` chunk 6ba6e3; `ruff format --check` chunk 56fb10; `pip-audit` chunks 0f9f62/db9029)
- [x] Updated failure snapshots for Node/React e2e (`pytest` chunk 3078d5)
- [x] Ruff clean pass reference (`ruff check` chunk 0254a4)
- [x] Project-management targeted test confirmation (`pytest` chunk ea3314)
- [x] Latest validation evidence (`pytest` chunks 59ba8a/895d86; `ruff check` chunk 511a4c; `mypy` chunk e76474; `pip-audit` chunks d8ebd1/351c8b)
- [x] Template hook updates ensuring shared import discovery (e.g., `templates/python-service/hooks/post_gen_project.py`)

## Risks/Notes

- [x] Validate template hook imports across other entry points (nox sessions, pytest-cookies) _(shell wrapper tests guard PYTHONPATH + skip flows; chunk 5cd380)_
- [x] Ruff config deprecation warnings from generated projects _(validated via new regression in `tests/test_cookiecutters.py`; pytest chunk e8dedd)_
- [ ] Monitor baseline command health; security gate now green after safe pip upgrade (chunk aa754c)
- [x] React Storybook 8 upgrade: confirm docs/changelog guidance added for template consumers _(React template README refreshed; coverage added via `tests/test_cookiecutters.py::test_react_cookiecutter_storybook_scripts`, pytest chunk 3d7b60)_
- [ ] Replace temporary SAFE_PIP_SPEC pin once upstream pip publishes a patched release
- [x] Quick-mode sanity summary now derives from recorded passes (guarded by `tests/test_sanity_check.py::test_sanity_check_quick_mode_summary_matches_passes`, pytest chunk cd2c27)
- [x] Evaluate adding targeted tests for `.dev/sanity-check.sh` quick-mode output to prevent regressions _(HTML report parity locked by pytest chunk 59ba8a)_
- [ ] `pip-audit` virtualenv bootstrap occasionally hangs; investigate caching/timeout strategy before gating CI
- [ ] Template formatting drift (`ruff format --check`) spans shared hooks/notebooks; monitor templated placeholders ahead of strict enforcement (chunk 56fb10)

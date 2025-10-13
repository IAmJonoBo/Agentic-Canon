# Next Steps

## Tasks

- [x] Establish pipeline remediation plan (Owner: Agent, Due: 2025-02-05)
- [x] Harden local/CLI PYTHONPATH bootstrapping so template hooks import cleanly (Owner: Agent, Due: 2025-02-05)
- [x] Re-run baseline validation to confirm import fixes and capture fresh results (Owner: Agent, Due: 2025-02-05) _(pytest manifest test passes; `ruff check` now clean — latest pass chunk 0254a4; `mypy` and remaining gates still outstanding; `pip-audit` interrupted due to tool hang)_
- [x] Produce lint/type/security integration design updates for unified validation flow (Owner: Agent, Due: 2025-02-06) _(blueprint recorded in SCRATCH.md §Detailed Gate Integration Blueprint)_
- [x] Migrate Ruff configs to `[tool.ruff.lint]` schema and clear existing lint violations (Owner: Agent, Due: 2025-02-06)
- [x] Resolve React template npm peer dependency conflict so e2e test can pass (Owner: Agent, Due: 2025-02-07) _(storybook/tooling pinned to 8.6 with Node 22 shims; validated via `pytest` chunk 48e64d)_
- [x] Resolve Node template npm/vitest failures uncovered during e2e run (Owner: Agent, Due: 2025-02-07) _(Vitest scripts now bypass shim; `pytest` chunk 48e64d)_
- [x] Configure mypy targets and add a dedicated Nox/typecheck gate (Owner: Agent, Due: 2025-02-07) _(tracked by `mypy.ini` + nox session; clean run chunk 7679c3)_
- [ ] Expand `.dev/validate-templates.sh` / Nox to run lint + type + security stages post-render (Owner: Agent, Due: 2025-02-08)

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

## Deliverables

- [x] Updated SCRATCH.md with detailed remediation plan
- [x] Baseline command results logged
- [x] Add-on design notes covering lint/type/security flow adjustments
- [x] Conditionalize tasklist workflow output when automation disabled
- [x] Document React/npm resolution plan once validated _(captured via Tasks/Steps updates)_

## Quality Gates

- [x] Tests: pytest (pass or documented blockers) _(clean run chunk 48e64d)_
- [x] Lint: ruff check (passing; monitor for regressions)
- [x] Type-check: mypy (configured and passing) _(clean run chunk 7679c3)_
- [x] Security: secret scan (tool configured and passing) _(`pip-audit` clean chunk aac0e9)_
- [ ] Build: applicable build commands succeed

## Links

- [x] SCRATCH.md §Current Progress, Remediation Strategy
- [x] `.dev/validate-templates.sh` PYTHONPATH bootstrapping
- [x] `tests/conftest.py` environment preparation helpers
- [x] Test + lint failure logs (`pytest` chunks d35d86 & c8cb83, `ruff check` chunk c61c7e, `mypy` chunk 3f2957, `pip-audit` chunk 695db8)
- [x] Updated failure snapshots for Node/React e2e (`pytest` chunk 3078d5)
- [x] Ruff clean pass reference (`ruff check` chunk 0254a4)
- [x] Project-management targeted test confirmation (`pytest` chunk ea3314)
- [x] Latest validation evidence (`pytest` chunk 48e64d; `ruff check` chunk 2509a3; `mypy` chunk 7679c3; `pip-audit` chunk aac0e9)
- [x] Template hook updates ensuring shared import discovery (e.g., `templates/python-service/hooks/post_gen_project.py`)

## Risks/Notes

- [ ] Validate template hook imports across other entry points (nox sessions, pytest-cookies)
- [ ] Ruff config deprecation warnings from generated projects _(pending validation after next render)_
- [ ] Baseline commands currently failing or incomplete
- [ ] React Storybook 8 upgrade: confirm docs/changelog guidance added for template consumers
- [ ] Quick-mode sanity `PASS_COUNT` (150) must be kept in sync with future script additions
- [ ] Evaluate adding targeted tests for `.dev/sanity-check.sh` quick-mode output to prevent regressions
- [ ] `pip-audit` virtualenv bootstrap occasionally hangs; investigate caching/timeout strategy before gating CI

# Next Steps

## Tasks
- [x] Establish pipeline remediation plan (Owner: Agent, Due: 2025-02-05)
- [x] Harden local/CLI PYTHONPATH bootstrapping so template hooks import cleanly (Owner: Agent, Due: 2025-02-05)
- [x] Re-run baseline validation to confirm import fixes and capture fresh results (Owner: Agent, Due: 2025-02-05) _(pytest manifest test passes; `ruff`/`mypy` still failing; `pip-audit` interrupted due to tool hang)_
- [x] Produce lint/type/security integration design updates for unified validation flow (Owner: Agent, Due: 2025-02-06) _(blueprint recorded in SCRATCH.md §Detailed Gate Integration Blueprint)_

## Steps
- [x] Document current pipeline baseline results
- [x] Identify root causes for template validation failures (missing PYTHONPATH wiring)
- [x] Propose remediation actions aligned with standards
- [x] Validate PYTHONPATH remediation via pytest + CLI smoke runs (manifest sync test passes; CLI help executes cleanly)
- [x] Finalize lint/type/security extension approach for `validate_templates_all` (blueprint captured; awaiting implementation)
- [x] Capture detailed lint/type/security integration blueprint in SCRATCH.md

## Deliverables
- [x] Updated SCRATCH.md with detailed remediation plan
- [x] Baseline command results logged
- [x] Add-on design notes covering lint/type/security flow adjustments

## Quality Gates
- [ ] Tests: pytest (pass or documented blockers)
- [ ] Lint: ruff check (pass or documented blockers)
- [ ] Type-check: mypy (configured and passing)
- [ ] Security: secret scan (tool configured and passing)
- [ ] Build: applicable build commands succeed

## Links
- [x] SCRATCH.md §Current Progress, Remediation Strategy
- [x] `.dev/validate-templates.sh` PYTHONPATH bootstrapping
- [x] `tests/conftest.py` environment preparation helpers
- [x] Test + lint failure logs (`pytest tests/test_manifest_sync.py` chunk e2b44c, `ruff check` chunk 6e85b6, `mypy` chunk 42a70b, `pip-audit` chunk 607c2a)

## Risks/Notes
- [ ] Validate template hook imports across other entry points (nox sessions, pytest-cookies)
- [ ] Ruff config deprecation warnings from generated projects
- [ ] Baseline commands currently failing or incomplete
- [ ] React template npm peer dependency conflicts block e2e test coverage
- [ ] `pip-audit` virtualenv bootstrap occasionally hangs; investigate caching/timeout strategy before gating CI

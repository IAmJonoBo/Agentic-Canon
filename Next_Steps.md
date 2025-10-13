# Next Steps

## Tasks
- [x] Establish pipeline remediation plan (Owner: Agent, Due: 2025-02-05)
- [x] Harden local/CLI PYTHONPATH bootstrapping so template hooks import cleanly (Owner: Agent, Due: 2025-02-05)
- [ ] Re-run baseline validation to confirm import fixes and capture fresh results (Owner: Agent, Due: 2025-02-05)
- [ ] Produce lint/type/security integration design updates for unified validation flow (Owner: Agent, Due: 2025-02-06)

## Steps
- [x] Document current pipeline baseline results
- [x] Identify root causes for template validation failures (missing PYTHONPATH wiring)
- [x] Propose remediation actions aligned with standards
- [ ] Validate PYTHONPATH remediation via pytest + CLI smoke runs
- [ ] Finalize lint/type/security extension approach for `validate_templates_all`

## Deliverables
- [x] Updated SCRATCH.md with detailed remediation plan
- [x] Baseline command results logged
- [ ] Add-on design notes covering lint/type/security flow adjustments

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
- [ ] Test + lint failure logs (pytest chunk a85a8e, ruff chunk 0d8c2b)

## Risks/Notes
- [ ] Validate template hook imports across other entry points (nox sessions, pytest-cookies)
- [ ] Ruff config deprecation warnings from generated projects
- [ ] Baseline commands currently failing or incomplete
- [ ] React template npm peer dependency conflicts block e2e test coverage

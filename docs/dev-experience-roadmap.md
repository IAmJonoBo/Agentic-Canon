# Developer Experience Roadmap

The initiatives below outline upcoming DX-focused enhancements for Agentic Canon.
Each effort has a corresponding task in `TASKS.md` so that execution can be
tracked alongside the rest of the backlog.

## Backstage Portal Integration (#130)

- ✅ Backstage Software Template published at
  `templates/platform/backstage/service-template.yaml`, accompanied by a
  usage guide (`templates/platform/backstage/README.md`).
- ✅ Provides self-service scaffolding plus catalog annotations while keeping
  cookiecutter templates untouched.
- ⏳ Future iterations: surface sanity-check and template E2E telemetry inside
  Backstage dashboards.

## OpenFeature / flagd Starter Kit (#131)

- ✅ Shared helpers published under `templates/_shared/feature_flags/`
  (Python, TypeScript, Go).
- ✅ Documentation added (`docs/feature-flags.md`) with install instructions
  and quick-start examples.
- ⏳ Next step: wire proactive lint/CI guidance into the CLI `fix` routine once
  flag usage becomes widespread.

## Syft + Grype Workflow (#132)

- Add reusable GitHub Actions workflow(s) that generate SBOMs via Syft and run
  Grype vulnerability scanning.
- Update CI docs so teams can layer the workflow on top of their generated
  projects with minimal effort.

## Remote Development Environments (#133)

- Ship reference `.gitpod.yml` and `.devcontainer/` definitions aligned with the
  repository toolchain.
- Explain how to copy these configs post-cookiecutter to enable instant cloud or
  container-based development environments.

## Semgrep Guardrails (#134)

- Centralize a Semgrep ruleset covering secure defaults across languages.
- Deliver helper workflows / pre-commit examples so teams can opt-in without
  editing template payloads.

### Contributing Feedback

Have suggestions or discover friction? Open an issue tagged `dx` so we can fold
improvements into future sprints.

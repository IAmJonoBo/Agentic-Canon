# Developer Experience Roadmap

The initiatives below outline upcoming DX-focused enhancements for Agentic Canon.
Each effort has a corresponding task in `TASKS.md` so that execution can be
tracked alongside the rest of the backlog.

## Backstage Portal Integration (#130)

- Deliver a Backstage module exposing Agentic Canon templates, sanity check
  status, and documentation entry points.
- Provide scripts + guidance for organizations to import the module into their
  existing Backstage instances without altering template payloads.

## OpenFeature / flagd Starter Kit (#131)

- Publish language-specific shims (Python/TypeScript/Go) under a shared tooling
  directory to accelerate feature flag adoption.
- Document how to wire the shims into projects generated from any template.

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

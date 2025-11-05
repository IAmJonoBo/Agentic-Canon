# Backstage Integration Module

This directory hosts reusable Backstage assets that expose Agentic Canon
capabilities inside a platform portal. The goal is to empower developers to
self‑service the same golden paths that our cookiecutter templates provide,
without requiring direct edits to the templates themselves.

## Included Assets

- `service-template.yaml` – opinionated Software Template that provisions a new
  repository using Agentic Canon scaffolds, sets up CI/CD workflows, and registers
  the component/catalog metadata automatically.
- `catalog-info` fragments (inline within the template) – ensure generated
  services surfaced in Backstage inherit the same compliance annotations, SLO
  dashboards, and automation hooks.

## Usage

1. Copy `service-template.yaml` (or clone this folder) into your Backstage portal
   repository under `templates/`.
2. Update the template metadata (owners, example URLs, secrets) to match your
   organization’s standards.
3. Register the template via Backstage:
   ```bash
   yarn backstage-cli repo schema openapi verify --schema templates/service-template.yaml
   yarn backstage-cli create --from templates/service-template.yaml
   ```
4. Surface the template inside the Backstage catalog (typically using
   `catalog-info.yaml` for your templates repo).
5. Optionally extend the steps in the template to call `.dev/sanity-check.sh`,
   the `Templates • e2e` workflow, or other automation described in `docs/`.

## Extending the Portal

- Add additional templates (e.g., docs-only or project-management variants) by
  following the same pattern and pointing to the relevant cookiecutter directories.
- Leverage the shared scripts in `.dev/` to expose sanity check health or template
  E2E status through Backstage dashboards.

For background, see the Developer Experience roadmap entry in
[`docs/dev-experience-roadmap.md`](../../../docs/dev-experience-roadmap.md) and task
tracking in `TASKS.md` (#130).

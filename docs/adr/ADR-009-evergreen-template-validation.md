# ADR-009: Evergreen Template Validation Pipeline

## Status

Accepted – 2025-10-12

## Context

Template validation relied on ad-hoc shell scripts that:

- Embedded template-specific logic in Bash, making it difficult to keep pace with new features.
- Duplicated manifest data across hooks, tests, and sync tooling.
- Required manual cache management for expensive `npm`/`go` installs.
- Lacked a single entry point usable by developers, automation, and sanity checks.
- Offered no Renovate coverage for Trunk CLI/runtime/tool versions, increasing drift risk.

## Decision

Standardise validation around a manifest-driven, cached Nox pipeline:

1. **Manifest** – Authoritative `templates/manifest.yaml` with per-template hooks, options, caches, and trunk overrides. A sync helper mirrors it to JSON for environments without PyYAML.
2. **Shared hooks** – `templates/_shared/hooks.py` exposes helpers (`run_post_gen`, `replace_workflow_placeholders`, cache utilities) that every `post_gen_project.py` imports.
3. **Caching** – `templates/_shared/cache.py` writes baked templates to `~/.cache/agentic-canon/templates/<template>/<sha>` and installer caches under `<cache>/installers/{node,pip,go}` with `.installed` sentinels. `--force` wipes caches.
4. **Nox orchestration** – New sessions:
   - `render_templates` renders manifest contexts and hydrates caches.
   - `lint_templates` copies `.trunk/` then runs `trunk check --all`.
   - `format_templates` runs `trunk fmt --all` and fails if dirty.
   - `upgrade_tools` reuses `.dev/trunk-with-progress.sh upgrade`.
5. **CLI wrapper** – `.dev/validate-templates.sh` delegates to the sessions with `--linters`, `--format`, `--upgrade`, `--template`, and `--force-rebuild` flags. Sanity checks call `--linters`.
6. **CI workflows** – Matrixed jobs invoke the wrapper for lint/format; end-to-end tests reuse caches via `AGENTIC_CANON_CACHE_DIR`; nightly upgrades call `nox -s upgrade_tools`.
7. **Renovate** – Regex managers cover `.trunk/trunk.yaml` (cli, runtimes, lint tool versions) with a shared `type:tools` label and grouped upgrades.

## Consequences

- Template changes require updating `manifest.yaml`; hooks/tests consume it automatically.
- CI can add new templates by editing the manifest only; workflows pick them up via the matrix.
- Rendered templates live under `build/template-renders/`, so local tooling and spa editors need to ignore that directory.
- Trunk CLI must be available (Nox installs it automatically when missing).
- Renovate PRs touching Trunk/tooling are labelled `type:tools` and grouped.

## Alternatives considered

- **Keep Bash scripts:** Low effort but brittle, no caching, fragmented knowledge.
- **Invoke `trunk` directly from CI:** Hard to share between local workflows and automation, no manifest context or caching.
- **Custom Python orchestration outside Nox:** Possible, but we already standardise on Nox for repo automation.

## Follow-up

- Extend manifest installers for future ecosystems (e.g., `pnpm`, `uv`).
- Refine Renovate coverage as new linters or runtimes are added.
- Monitor cache size and add pruning if necessary.

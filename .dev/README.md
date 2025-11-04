# Development Tools

**Purpose:** Internal tools for maintaining and upgrading the n00-frontiers repository itself.

**⚠️ Important:** These tools are for **repository maintenance only**, not for end users.

## Directory Structure

```text
.dev/
├── README.md                   # This file
├── scripts/                    # Development scripts
│   └── setup-labels.sh        # GitHub labels setup
├── validate-templates.sh       # Template validation orchestrator
└── sanity-check.sh            # Repository sanity checks
```

## Tools

### validate-templates.sh

Front-end for the Nox template sessions. Provides a single command that local
developers, CI, and sanity-check tooling can share.

- `--linters` runs `nox -s render_templates` followed by `lint_templates`
- `--format` runs `nox -s render_templates` followed by `format_templates`
- `--upgrade` runs `nox -s upgrade_tools`
- `--template NAME` filters to matching templates (repeatable)
- `--force-rebuild` invalidates render and installer caches

**Usage examples:**

```bash
# Render + lint + format every template (default behaviour)
.dev/validate-templates.sh

# Lint a single template/context combination
.dev/validate-templates.sh --linters --template python-service

# Rebuild caches and run formatting checks
.dev/validate-templates.sh --format --force-rebuild
```

### scripts/sync-manifest.py

Synchronises the JSON manifest mirror from the YAML source so hooks continue to
function in environments without PyYAML.

- Reads `templates/manifest.yaml`
- Writes `templates/manifest.json` with sorted keys and stable formatting
- Supports a `--check` mode for CI enforcement

**Usage:**

```bash
.dev/scripts/sync-manifest.py           # updates manifest.json
.dev/scripts/sync-manifest.py --check   # exits 1 if sync required
```

### sanity-check.sh

Runs comprehensive repository health checks:

- Verifies directory structure
- Checks documentation completeness
- Validates configuration files
- Tests CI/CD workflows

**Usage:**

```bash
.dev/sanity-check.sh

# Quiet summary only
.dev/sanity-check.sh --quiet

# Skip template-heavy checks (useful when running with older Bash versions)
.dev/sanity-check.sh --skip-templates --quiet
```

### trunk-with-progress.sh

Wrapper for trunk commands with visual progress feedback:

- Adaptive spinner that only renders when running in an interactive terminal
- Automatic cursor hide/show with guaranteed cleanup on exit (even when interrupted)
- Colored status messages with graceful fallbacks for non-TTY environments (CI logs stay clean)
- Preserves trunk exit codes and full command output while providing progress feedback
- Works with every trunk sub-command

**Usage:**

```bash
# Check all files with progress indicator
.dev/trunk-with-progress.sh check --all

# Format all files with progress indicator
.dev/trunk-with-progress.sh fmt --all

# Any trunk command works
.dev/trunk-with-progress.sh upgrade
```

**Why This Tool:** Trunk operations can take a long time, especially when checking the entire repository. This wrapper provides feedback so you know the operation is still running.

> 💡 Tip: When running in CI or any non-interactive session, the script automatically disables the spinner and color codes, so log output remains readable.

### scripts/setup-labels.sh

Sets up GitHub issue labels for the repository:

- Creates standard label set
- Configures colors and descriptions
- Requires GitHub CLI (gh) authentication

**Usage:**

```bash
.dev/scripts/setup-labels.sh
```

## Separation of Concerns

### Development Tools (.dev/)

**Internal use - for maintaining this repository:**

- Repository validation scripts
- CI/CD maintenance tools
- Label and issue management
- Health checks and diagnostics

### Distribution Assets (root level)

**External use - for end users:**

- `agentic_canon_cli/` - CLI wizard for project generation
- `templates/` - Cookiecutter templates and supporting files
- `notebooks/` - Executable guides
- `docs/` - Documentation
- `examples/` - Reference implementations

## Contributing

When adding new development tools:

1. Place them in `.dev/` or `.dev/scripts/`
2. Make scripts executable: `chmod +x script-name.sh`
3. Add documentation to this README
4. Update DIRECTORY_STRUCTURE.md if structure changes

## Related Documentation

- [DIRECTORY_STRUCTURE.md](../DIRECTORY_STRUCTURE.md) - Complete repository structure
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [FRAMEWORK.md](../FRAMEWORK.md) - Framework and philosophy

## Template Linting & Formatting

n00-frontiers standardises on Trunk, orchestrated through dedicated Nox sessions. Configuration
lives in [`.trunk/trunk.yaml`](../.trunk/trunk.yaml) and mirrors the versions baked into each
template.

### Session overview

- `render_templates` – renders every template/context combination into `build/template-renders/`
  using the manifest cache. Installer caches (`node_modules`, `.venv`, Go modules) are populated
  when enabled in the manifest.
- `lint_templates` – copies or symlinks `.trunk/` into the rendered project and runs
  `trunk check --all` via `.dev/trunk-with-progress.sh`.
- `format_templates` – runs `trunk fmt --all` and fails if any files change afterwards.
- `upgrade_tools` – upgrades Trunk itself and refreshes pinned tool versions.

`.dev/validate-templates.sh` wraps these sessions so you rarely need to remember individual Nox
invocations.

### Runtime baselines (from `.trunk/trunk.yaml`)

- **Python 3.10.8** keeps `ruff`, `bandit`, and the Python hook tooling aligned with the templates.
- **Go 1.22.6** matches the Go service template and example projects, ensuring `gofmt` parity.
- **Node.js 22.16.0** matches the Vite/React stacks used across templates and examples.

When bumping any runtime or tool version in `.trunk/trunk.yaml`, run:

```bash
nox -s upgrade_tools
```

### Enabled linters & formatters

Trunk drives `prettier`, `eslint`, `ruff`, `yamllint`, `shellcheck`, `taplo`, and the rest. To add
or update tooling:

1. Edit `.trunk/trunk.yaml` (often under `lint.enabled`).
2. Execute `.dev/validate-templates.sh --linters` locally to confirm the change.
3. Commit both the config change and any resulting file updates.

### Recommended commands

| Command                                                   | Purpose                                                   |
| --------------------------------------------------------- | --------------------------------------------------------- |
| `.dev/validate-templates.sh`                              | Render, lint, and format every template (default flow)    |
| `.dev/validate-templates.sh --linters --template react`   | Lint only the React template contexts                     |
| `.dev/validate-templates.sh --format --force-rebuild`     | Re-render from scratch and verify formatting consistency  |
| `nox -s lint_templates -- --feature include_storybook=no` | Ad-hoc lint run with manifest-driven feature filters      |
| `.dev/sanity-check.sh --section templates`                | Structural checks + lint smoke through the sanity harness |
| `nox -s typecheck`                                        | Run mypy across CLI tooling and automation scripts        |

### Reproducibility Tips

- Always create or refresh the virtual environment before running the checks:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Reuse template installer caches by exporting `N00_FRONTIERS_CACHE_DIR` (CI points this to
  `$RUNNER_TEMP/n00-frontiers-cache`).

- After pulling changes, re-run the sanity check:

  ```bash
  .dev/sanity-check.sh --quiet
  ```

  Add `--format` if you want the script to invoke `trunk fmt --all` automatically when it detects
  unformatted files.

- End-to-end template tests cache rendered projects and `node_modules` under
  `~/.cache/n00-frontiers` (override with `N00_FRONTIERS_CACHE_DIR`). Delete that directory if you
  ever need a completely clean run.

### Nox Sessions

We provide dedicated Nox sessions for each major sanity-check section. Examples:

```bash
pip install nox             # one-time setup (if not already installed)
nox -s sanity                  # full run
nox -s sanity_core             # docs/config checks only
nox -s sanity_templates        # cookiecutter structure checks
nox -s sanity_tests            # template/unit test coverage
nox -s tests                   # pytest -n auto (xdist)
```

Sections currently supported: `core`, `templates`, `examples`, `dashboards`, `videos`, `cloud`,
`cli`, and `tests`.

### Make Targets

For quick local orchestration (and simple parallel execution) there is also a lightweight
`Makefile`:

```bash
make sanity-all            # run every section sequentially
make -j4 sanity-all        # run sections in parallel where safe
make sanity-core           # run a specific section
make sanity-fast           # core + templates + tests
```

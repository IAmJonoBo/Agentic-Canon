# Development Tools

**Purpose:** Internal tools for maintaining and upgrading the Agentic Canon repository itself.

**⚠️ Important:** These tools are for **repository maintenance only**, not for end users.

## Directory Structure

```text
.dev/
├── README.md                   # This file
├── scripts/                    # Development scripts
│   └── setup-labels.sh        # GitHub labels setup
├── validate-templates.sh       # Template validation
└── sanity-check.sh            # Repository sanity checks
```

## Tools

### validate-templates.sh

Validates all Cookiecutter templates for correctness:

- Checks cookiecutter.json syntax
- Validates hooks (pre_gen_project.py, post_gen_project.py)
- Verifies template structure

**Usage:**

```bash
.dev/validate-templates.sh
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

## Linting & Formatting Workflow

Agentic Canon standardises on the Trunk CLI for linting, formatting, and security scans. The
configuration lives in [`.trunk/trunk.yaml`](../.trunk/trunk.yaml) and is intentionally aligned with
the versions used by our templates and example projects.

### Runtime Baselines

- **Python 3.10.8** — matches the interpreter baked into the templates and keeps `ruff`, `bandit`,
  and other Python linters on a supported version.
- **Go 1.22.6** — mirrors the sample gRPC/Go services so `gofmt` output is identical in CI and
  locally.
- **Node.js 22.16.0** — supports the React, Vite, and Vitest stacks used across the repo.

If you change runtime versions, update them in `.trunk/trunk.yaml` and run:

```bash
.dev/trunk-with-progress.sh upgrade
```

### Enabled Linters

Trunk drives all tooling—`prettier`, `eslint`, `ruff`, `gofmt`, `yamllint`, `shellcheck`, and more.
Refer to `lint.enabled` in `.trunk/trunk.yaml` for the complete list. To add or upgrade a tool:

1. Update the entry in `.trunk/trunk.yaml` (or add a new one under `lint.enabled`).
2. Run `.dev/trunk-with-progress.sh upgrade` to download the new tool version.
3. Commit both the YAML change and any resulting formatting edits.

### Import Sorting / Python Formatting

Python projects rely on `ruff` for linting and `black`-style formatting. Import ordering is handled
by `isort` with the configuration in the repository root (`.isort.cfg`), set to mirror Black’s
style (`line_length = 100`, trailing commas, etc.). This means the following will yield identical
results:

```bash
trunk fmt --all          # preferred – runs every formatter
trunk check --all        # preferred – runs linters + security scanners
```

### When to Run What

| Command                                   | Purpose                                                        |
| ----------------------------------------- | -------------------------------------------------------------- |
| `.dev/trunk-with-progress.sh fmt --all`   | Format everything with progress feedback                       |
| `.dev/trunk-with-progress.sh check --all` | Run the full lint + security suite                             |
| `.dev/sanity-check.sh --format`           | Run Trunk via the sanity check helper (auto-formats if needed) |

The sanity check script now prefers the repository’s virtual environment (`.venv/bin/python`), so
all JSON/YAML/validation steps use the same interpreter as our tooling. This keeps local runs,
cookiecutter hooks, and CI pipelines fully aligned.

### Reproducibility Tips

- Always create or refresh the virtual environment before running the checks:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- After pulling changes, re-run the sanity check:

  ```bash
  .dev/sanity-check.sh --quiet
  ```

  Add `--format` if you want the script to invoke `trunk fmt --all` automatically when it detects
  unformatted files.

- End-to-end template tests cache rendered projects and `node_modules` under
  `~/.cache/agentic-canon` (override with `AGENTIC_CANON_CACHE_DIR`). Delete that directory if you
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

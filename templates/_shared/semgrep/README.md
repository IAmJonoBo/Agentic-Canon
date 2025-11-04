# Semgrep Shared Ruleset

Task #134 introduces a baseline Semgrep policy that teams can opt into without
modifying template payloads. Copy the relevant files from this directory into
your project and reference the CI workflow snippets below.

## Files

- `rules.yml` – curated collection of security and code-quality rules covering
  Python, TypeScript/JavaScript, and Go.
- `semgrep-ci.yml` – reusable GitHub Actions workflow (see below) that runs the
  ruleset on push/PR.
- `pre-commit-config.yaml` snippet – optional entry teams can merge into their
  local pre-commit setup.

### GitHub Actions

Add the reusable workflow by dropping `semgrep-ci.yml` into your project’s
`.github/workflows/` folder:

```yaml
name: Security • Semgrep

on:
  pull_request:
  push:
    branches: [main]

jobs:
  semgrep:
    uses: ./.github/workflows/semgrep-ci.yml
```

### Pre-commit

Merge the snippet into your `.pre-commit-config.yaml` to run Semgrep locally:

```yaml
- repo: local
  hooks:
    - id: semgrep
      name: semgrep
      entry: semgrep --config templates/_shared/semgrep/rules.yml
      language: system
      types: [python, javascript, typescript, go]
```

### Running Manually

```bash
semgrep --config templates/_shared/semgrep/rules.yml
```

## Rule Selection Philosophy

- Focus on **high-signal security and correctness rules** to avoid alert fatigue.
- Cover the primary languages shipped in n00-frontiers templates.
- Expose a single config that teams can extend with their local exceptions.

You can extend `rules.yml` with organisation-specific policies as needed.

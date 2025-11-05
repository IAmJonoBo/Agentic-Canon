# Semgrep Shared Ruleset

Task #134 delivers a baseline Semgrep ruleset and automation options.

## Files

- `templates/_shared/semgrep/rules.yml` – curated security and correctness rules covering Python, TypeScript/JavaScript, and Go.
- `templates/_shared/semgrep/semgrep-ci.yml` – reusable GitHub Actions workflow that runs the ruleset.
- `templates/_shared/semgrep/pre-commit-snippet.yml` – drop-in pre-commit configuration.

## Usage

### GitHub Actions

```yaml
name: Security • Semgrep

on: [push, pull_request]

jobs:
  semgrep:
    uses: ./.github/workflows/semgrep-ci.yml
```

### Pre-commit

Merge the snippet into `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: semgrep
      name: semgrep
      entry: semgrep --config templates/_shared/semgrep/rules.yml
      language: system
      types: [python, javascript, typescript, go]
```

### Manual Execution

```bash
semgrep --config templates/_shared/semgrep/rules.yml
```

## Philosophy

- High-signal rules only to minimise noise.
- Coverage for all major Agentic Canon templates.
- Extensible—teams can append organisation-specific policies.

See `docs/dev-experience-roadmap.md` for roadmap context.

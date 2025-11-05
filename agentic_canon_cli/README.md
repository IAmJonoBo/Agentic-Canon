# Agentic Canon CLI (Compatibility Wrapper)

The CLI source moved to `applications/scaffolder/agentic_canon_cli/`. This shim keeps import paths
and entry points working until downstream consumers migrate to the new location.

Use the relocated package for development:

```bash
cd applications/scaffolder
python -m agentic_canon_cli.cli
```

When the scaffolder is extracted into its own repository, this wrapper can be removed.

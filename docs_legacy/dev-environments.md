# Remote Development Environments

Task #133 introduces ready-to-use configurations for Gitpod and VS Code Dev Containers so contributors can start hacking within minutes.

## Gitpod

- Config file: `.gitpod.yml`
- Base image: `.gitpod.Dockerfile`
- Pre-installs project `requirements.txt`, upgrades npm, and runs the fast pytest suite.

Launch:

```
https://gitpod.io/#https://github.com/IAmJonoBo/Agentic-Canon
```

You can edit the `tasks` section to run additional checks (e.g., `pytest -m slow`).

## Dev Containers

- Config file: `.devcontainer/devcontainer.json`
- Bundles Python 3.11, Node 20, and Go 1.22 via devcontainer features.
- Automatically bootstraps a local `.venv` with repository requirements.
- Installs useful VS Code extensions (Python, Pylance, Prettier, Go).

Usage:

1. Open the repository in VS Code.
2. Run “Dev Containers: Reopen in Container”.
3. When the container starts the post-create script provisions dependencies.

### Tips

- Combine with `agentic-canon fix` inside the container to run validation, pre-commit setup, and the sanity check in one go.
- Forwarded ports (8000, 5173) support local FastAPI/Vite development by default.

For roadmap context see `docs/dev-experience-roadmap.md` (#133).

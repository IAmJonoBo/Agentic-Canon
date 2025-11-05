# Applications Workspace

The `applications/` directory isolates implementation assets from the canonical documentation and policy stack. This separation makes it easy to extract productised tooling into a dedicated repository while keeping the n00-frontiers docs as the single source of truth.

## Layout

```
applications/
└── scaffolder/
    ├── agentic_canon_cli/      # CLI source
    ├── binder/                 # Binder environment (symlinked at repo root)
    ├── build/                  # Render caches and artefacts
    ├── examples/               # Reference implementations and walkthroughs
    ├── notebooks/              # Executable notebooks (Jupytext pairs)
    └── templates/              # Cookiecutter templates and shared tooling
```

Root-level symlinks (`templates/`, `examples/`, `binder/`, `build/`, `notebooks/`) are retained to avoid breaking existing tooling. New consumers should target `applications/scaffolder/...` directly and declare the docs/policy version they align with via the compliance manifest.

## Planned Extraction

1. Clone this repository and create a new bare repo (e.g., `n00-frontiers-scaffolder`).
2. Move `applications/scaffolder/` into the new repo history (e.g., using `git filter-repo` or `git subtree split`).
3. Add the new repo as a submodule or GitHub dependency so the canonical docs can pin a specific scaffolder release.
4. Remove the compatibility symlinks once all consumers reference the new location.
5. Update compliance manifests to record the scaffolder release version alongside docs/policy versions.

Until the extraction is complete, maintain parity by:

- Keeping pull requests that modify scaffolder assets scoped to `applications/scaffolder/` (plus compatibility symlinks when necessary).
- Updating the compliance manifest template whenever the scaffolder requires new tooling or policy hashes.
- Using waiver automation to track temporary deviations while refactoring.

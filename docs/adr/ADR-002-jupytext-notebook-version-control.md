# ADR-002: Jupytext for Notebook Version Control

## Status

Accepted

## Context

Jupyter notebooks (`.ipynb` files) are JSON files that contain code, outputs, and metadata. This creates several challenges for version control:

1. **Diff Noise**: JSON structure and outputs create noisy diffs
2. **Merge Conflicts**: Difficult to resolve conflicts in JSON
3. **Code Review**: Hard to review notebook changes in PRs
4. **Output Management**: Outputs and metadata pollute version control
5. **Collaboration**: Multiple people editing notebooks leads to conflicts

We need a solution that allows us to:

- Version control notebook code effectively
- Enable meaningful code reviews
- Avoid output pollution in git
- Support collaboration
- Maintain executable notebooks

## Decision

We will use **Jupytext** to pair `.ipynb` notebooks with MyST Markdown (`.md`) files, storing only the Markdown files in git for documentation while maintaining `.ipynb` files for execution.

## Rationale

### Why Jupytext?

1. **Two-Way Sync**: Automatically syncs between `.ipynb` and `.md` formats
2. **Clean Diffs**: Markdown files produce clean, readable diffs
3. **Code Review**: Easy to review code changes in Markdown
4. **Format Choice**: Supports multiple text formats (Markdown, Python, R, etc.)
5. **Jupyter Integration**: Works seamlessly with Jupyter Lab/Notebook
6. **Automation**: Can be automated with pre-commit hooks
7. **MyST Support**: Integrates with Jupyter Book's MyST Markdown

### Configuration

```toml
# jupytext.toml
[formats]
"notebooks/" = "ipynb"
"docs/notebooks/" = "md:myst"
```

This configuration:

- Keeps executable `.ipynb` files in `notebooks/`
- Stores version-controlled `.md` files in `docs/notebooks/`
- Uses MyST Markdown format for Jupyter Book compatibility

### Workflow

1. Developers edit `.ipynb` files in Jupyter
2. Jupytext syncs changes to `.md` files
3. Only `.md` files are committed to git
4. `.ipynb` files are in `.gitignore` (except outputs can be stripped)
5. MyST Markdown files are used by Jupyter Book for documentation

## Consequences

### Positive

- Clean git diffs for notebook changes
- Easy code reviews of notebooks
- No output pollution in version control
- Merge conflicts are manageable in Markdown
- Works seamlessly with Jupyter Book
- Can edit either `.ipynb` or `.md` and changes sync
- Pre-commit hooks ensure synchronization

### Negative

- Requires setup and configuration
- Learning curve for contributors
- Notebooks must be paired initially
- Synchronization must be maintained
- Both formats exist locally (though only one in git)

### Mitigations

- Document Jupytext setup in CONTRIBUTING.md
- Provide setup scripts for contributors
- Use pre-commit hooks to automate syncing
- Add CI checks to verify synchronization
- Provide clear error messages when out of sync

## Implementation Details

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/mwouts/jupytext
    rev: v1.17.3
    hooks:
      - id: jupytext
        args: [--sync, --pipe, black]
        additional_dependencies:
          - black==24.10.0
```

### Initial Pairing

```bash
# Pair all notebooks
jupytext --set-formats ipynb,md:myst notebooks/*.ipynb

# Sync paired notebooks
jupytext --sync notebooks/*.ipynb
```

### Git Configuration

```gitattributes
# .gitattributes
*.ipynb filter=nbstripout diff=ipynb
```

```gitignore
# .gitignore
# Jupyter notebook checkpoints
.ipynb_checkpoints/
```

## Consequences for CI/CD

### Notebook Testing

- Tests run against `.ipynb` files in `notebooks/`
- CI uses `pytest --nbmake` to execute notebooks
- Ensures notebooks remain executable

### Documentation Building

- Jupyter Book uses `.md` files from `docs/notebooks/`
- MyST Markdown provides rich formatting
- Documentation stays in sync with code

### Version Control

- Only `.md` files committed to git
- Clean history and diffs
- Easy to track changes

## Alternatives Considered

### 1. nbstripout Only

**Pros**:

- Simpler setup
- Keeps `.ipynb` format

**Cons**:

- Still noisy diffs
- JSON merge conflicts
- Harder code reviews

### 2. Jupyter Book MyST Notebooks

**Pros**:

- Pure Markdown
- Clean diffs

**Cons**:

- No `.ipynb` for local execution
- Requires different editing workflow

### 3. ReviewNB or Similar Tools

**Pros**:

- Better notebook PR reviews

**Cons**:

- External service dependency
- Doesn't solve git diff issues
- Additional cost

### 4. No Pairing (`.ipynb` only)

**Pros**:

- Simplest approach

**Cons**:

- All the original problems remain
- Poor version control experience

## References

- [Jupytext Documentation](https://jupytext.readthedocs.io/)
- [MyST Markdown](https://myst-parser.readthedocs.io/)
- [Jupyter Book](https://jupyterbook.org/)
- [nbstripout](https://github.com/kynan/nbstripout)

## Notes

- This decision supports the documentation-as-code approach
- Aligns with Jupyter Book usage in Version 1.0
- Notebooks are parameterized with Papermill for automated execution
- MyST Markdown supports rich features like admonitions, tabs, and more
- Works well with AI/Copilot code generation

## Migration Path

For existing notebooks:

```bash
# 1. Pair existing notebooks
jupytext --set-formats ipynb,md:myst notebooks/*.ipynb

# 2. Generate initial MyST files
jupytext --sync notebooks/*.ipynb

# 3. Commit MyST files
git add docs/notebooks/*.md
git commit -m "docs: add MyST markdown mirrors for notebooks"

# 4. Update .gitignore if needed
echo "*.ipynb" >> notebooks/.gitignore  # Optional
```

---

**Date**: 2025-10-11  
**Author**: Jonathan Boardman (@IAmJonoBo)  
**Status**: Accepted

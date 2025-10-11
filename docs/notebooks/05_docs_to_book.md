---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 05 Documentation with Jupyter Book

This notebook demonstrates:
- Jupytext synchronization
- Jupyter Book build process
- Documentation best practices
- Publishing to GitHub Pages

```{code-cell} ipython3
:tags: [parameters]

# Parameters cell for Papermill
run_mode = "interactive"
```

## Jupytext: Notebooks as Markdown

Jupytext enables version control-friendly notebooks by pairing .ipynb with MyST markdown.

```{code-cell} ipython3
jupytext_benefits = [
    "Git-friendly diffs (no JSON noise)",
    "Easier code review",
    "Merge conflict resolution",
    "Direct markdown editing",
    "Automatic synchronization"
]

print("Jupytext Benefits:")
for benefit in jupytext_benefits:
    print(f"  ✓ {benefit}")
```

## Configuration

Set up Jupytext pairing in `jupytext.toml`:

```{code-cell} ipython3
jupytext_config = """
# jupytext.toml
[formats]
"notebooks/" = "ipynb"
"docs/notebooks/" = "md:myst"
"""

print("Jupytext Configuration:")
print(jupytext_config)

print("\nSetup Commands:")
print("  1. Create pairs: jupytext --set-formats ipynb,md:myst notebooks/*.ipynb")
print("  2. Sync changes: jupytext --sync notebooks/*.ipynb")
print("  3. Pre-commit hook: Automatically syncs on commit")
```

## Jupyter Book

Build beautiful, publication-quality documentation from Jupyter notebooks.

```{code-cell} ipython3
jupyter_book_features = {
    "MyST Markdown": "Extended markdown with roles and directives",
    "Executable Content": "Run notebooks during build",
    "Interactive Widgets": "Binder integration for live notebooks",
    "PDF Export": "Generate PDF from your book",
    "Search": "Full-text search out of the box",
    "Theming": "Customizable themes and branding"
}

print("Jupyter Book Features:")
for feature, desc in jupyter_book_features.items():
    print(f"  • {feature}: {desc}")
```

## Book Structure

Organize content with `_config.yml` and `_toc.yml`:

```{code-cell} ipython3
config_yml = """
# docs/_config.yml
title: Agentic Canon Bible
author: Agentic Canon
repository:
  url: https://github.com/IAmJonoBo/Agentic-Canon
  path_to_book: docs
execute:
  execute_notebooks: "off"  # CI runs notebooks
"""

toc_yml = """
# docs/_toc.yml
format: jb-book
root: intro
chapters:
  - file: notebooks/01_bootstrap
  - file: notebooks/02_security_supply_chain
  - file: notebooks/03_contracts_and_tests
  - file: notebooks/04_observability_slos
  - file: notebooks/05_docs_to_book
"""

print("Configuration Files:")
print(config_yml)
print(toc_yml)
```

## Build Process

Build and deploy your Jupyter Book:

```{code-cell} ipython3
build_commands = """
Build & Deploy Commands:

1. Local build:
   jupyter-book build docs

2. View locally:
   open docs/_build/html/index.html

3. Deploy to GitHub Pages:
   ghp-import -n -p -f docs/_build/html

4. Clean build:
   jupyter-book clean docs
"""

print(build_commands)
```

## GitHub Actions Automation

Automatically build and deploy on every push to main:

```{code-cell} ipython3
github_workflow = """
# .github/workflows/book-deploy.yml
name: Jupyter Book • deploy
on:
  push:
    branches: [main]
permissions:
  contents: write
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install jupyter-book ghp-import
      - run: jupyter-book build docs
      - name: Publish to gh-pages
        run: ghp-import -n -p -f docs/_build/html
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

print("GitHub Actions Workflow:")
print(github_workflow)

print("\nSetup:")
print("  1. Go to Settings → Pages")
print("  2. Set Source to 'gh-pages' branch")
print("  3. Your book will be at: https://<username>.github.io/<repo>/")
```

## Documentation Best Practices

```{code-cell} ipython3
best_practices = [
    "Write for your audience (users, developers, operators)",
    "Keep notebooks focused on one topic",
    "Include runnable examples",
    "Use MyST markdown for rich formatting",
    "Add diagrams and visualizations",
    "Link to API documentation",
    "Version your documentation",
    "Test notebooks in CI",
    "Keep outputs out of git (use nbstripout)",
    "Use Papermill for parameterized notebooks"
]

print("Documentation Best Practices:")
for i, practice in enumerate(best_practices, 1):
    print(f"  {i}. {practice}")
```

## Documentation Structure

Recommended organization for technical documentation:

```{code-cell} ipython3
doc_structure = """
Documentation Structure:

docs/
├── intro.md              # Overview and getting started
├── tutorials/            # Step-by-step guides
│   ├── quickstart.md
│   └── advanced.md
├── how-to/              # Task-oriented guides
│   ├── setup.md
│   └── deployment.md
├── reference/           # API documentation
│   ├── api.md
│   └── configuration.md
├── explanation/         # Conceptual information
│   ├── architecture.md
│   └── decisions.md
└── notebooks/           # Executable notebooks
    └── *.md (MyST)

Follow the Diátaxis framework:
- Tutorials: Learning-oriented
- How-to guides: Task-oriented
- Reference: Information-oriented
- Explanation: Understanding-oriented
"""

print(doc_structure)
```

```{code-cell} ipython3
print(f"Documentation notebook complete! (mode: {run_mode})")
print("\nAll notebooks ready for Jupyter Book!")
```

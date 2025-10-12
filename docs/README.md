# Documentation

This directory contains the source files for the Agentic Canon documentation, built with Jupyter Book.

## Overview

The documentation is organized as:

- Configuration files for Jupyter Book
- MyST Markdown versions of notebooks
- Architecture Decision Records (ADRs)
- Additional documentation pages

## Structure

```text
docs/
├── _config.yml          # Jupyter Book configuration
├── _toc.yml            # Table of contents
├── intro.md            # Introduction page
├── notebooks/          # MyST Markdown notebook mirrors
└── adr/                # Architecture Decision Records
```

## Jupyter Book

This documentation is built using [Jupyter Book](https://jupyterbook.org/), which provides:

- Beautiful, book-like documentation
- Integration with Jupyter notebooks
- MyST Markdown support
- Interactive content
- Multiple output formats (HTML, PDF)

### Configuration

#### \_config.yml

Main Jupyter Book configuration including:

- Book metadata (title, author, logo)
- Repository information
- Execution settings
- Build options
- Theme customization

#### \_toc.yml

Table of contents defining:

- Page order
- Chapter structure
- Section hierarchy
- Navigation

## Building the Documentation

### Local Build

```bash
# Install requirements
pip install -r ../requirements.txt

# Build the book
jupyter-book build .

# View in browser
open _build/html/index.html
```

### Clean Build

```bash
# Clean previous builds
jupyter-book clean .

# Rebuild
jupyter-book build .
```

## MyST Markdown

Documentation uses MyST (Markedly Structured Text) Markdown, an enhanced version of Markdown that supports:

### Features

- **Directives**: Special blocks for notes, warnings, code, etc.

  ```markdown
  :::{note}
  This is a note!
  :::
  ```

- **Roles**: Inline markup for cross-references, math, etc.

  ```markdown
  See {ref}`section-label` for details.
  ```

- **Math**: LaTeX math equations

  ```markdown
  $$
  E = mc^2
  $$
  ```

- **Citations**: Bibliography and citations

  ```markdown
  {cite}`reference-key`
  ```

### Notebooks

Jupyter notebooks in `notebooks/` are paired with MyST Markdown files in `docs/notebooks/` using Jupytext:

- Edit `.ipynb` files in Jupyter
- Changes sync automatically to `.md` files
- MyST files are version-controlled
- Jupyter Book uses MyST files for rendering

See [ADR-002](adr/ADR-002-jupytext-notebook-version-control.md) for details.

## Architecture Decision Records

ADRs documenting significant architectural decisions are in `adr/`:

- ADR-001: Cookiecutter for multi-template approach
- ADR-002: Jupytext for notebook version control
- [More ADRs...](adr/README.md)

## Deployment

### GitHub Pages

Documentation is automatically deployed to GitHub Pages on every push to main:

1. GitHub Actions builds the book
2. HTML is pushed to `gh-pages` branch
3. GitHub Pages serves the site

See `.github/workflows/book-deploy.yml`

### URL

Published documentation: `https://IAmJonoBo.github.io/Agentic-Canon/`

### Verifying the Build Locally

Before pushing, you can confirm the book builds the same way the CI workflow does:

```bash
# Run the pytest helper (marked as slow) to execute the full Jupyter Book build
pytest tests/test_docs_build.py -k builds_successfully -v

# Or call jupyter-book directly if you prefer
jupyter-book build docs --path-output /tmp/book-output
```

The GitHub workflow uses Python 3.12 and installs dependencies from `requirements.txt`, so local verification mirrors production as closely as possible.

### Template Integration CI

The `Templates • e2e` workflow (`.github/workflows/template-e2e.yml`) runs weekly and on-demand to ensure every template still boots, installs dependencies, and executes its smoke tests. Locally you can mirror the check with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/test_template_e2e.py -m slow -v
```

### Developer Experience Roadmap

See [`dev-experience-roadmap.md`](dev-experience-roadmap.md) for planned DX initiatives (Backstage integration, feature flags, SBOM workflows, remote dev environments, Semgrep guardrails) tracked in `TASKS.md`.

### Feature Flags

Refer to [`feature-flags.md`](feature-flags.md) for guidance on adopting OpenFeature/flagd using the shared helpers in `templates/_shared/feature_flags/`.

## Adding Content

### New Page

1. Create a Markdown file in `docs/`
2. Add to `_toc.yml`:

   ```yaml
   - file: your-page
   ```

3. Rebuild the book

### New Section

1. Create directory with pages
2. Add to `_toc.yml`:

   ```yaml
   - file: section/index
     sections:
       - file: section/page1
       - file: section/page2
   ```

### New Notebook

1. Create notebook in `../notebooks/`
2. Pair with MyST:

   ```bash
   jupytext --set-formats ../notebooks/notebook.ipynb,notebooks/notebook.md:myst
   ```

3. Sync:

   ```bash
   jupytext --sync ../notebooks/notebook.ipynb
   ```

4. Add to `_toc.yml`:

   ```yaml
   - file: notebooks/notebook
   ```

## Customization

### Theme

Customize theme in `_config.yml`:

```yaml
sphinx:
  config:
    html_theme: sphinx_book_theme
    html_theme_options:
      repository_url: https://github.com/IAmJonoBo/Agentic-Canon
      use_repository_button: true
```

### Extensions

Add Sphinx extensions in `_config.yml`:

```yaml
sphinx:
  extra_extensions:
    - sphinx_design
    - sphinx_copybutton
```

## Troubleshooting

### Build Errors

```bash
# Clean and rebuild
jupyter-book clean .
jupyter-book build . --all

# Check with verbose output
jupyter-book build . -v
```

### Missing Files

Ensure all files in `_toc.yml` exist:

```bash
# Check for broken links
jupyter-book build . --builder linkcheck
```

### MyST Syntax Errors

Use MyST parser to validate:

```bash
# Install myst-parser
pip install myst-parser

# Validate file
python -m myst_parser your-file.md
```

## References

- [Jupyter Book Documentation](https://jupyterbook.org/)
- [MyST Markdown Guide](https://myst-parser.readthedocs.io/)
- [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/)

## Related

- [Notebooks](../notebooks/) - Source notebooks
- [Jupytext Config](../jupytext.toml) - Pairing configuration
- [Book Deploy Workflow](../.github/workflows/book-deploy.yml) - Deployment automation

---

For questions about documentation, see [CONTRIBUTING.md](../CONTRIBUTING.md) or open a discussion.

# Notebooks

This directory contains executable Jupyter notebooks that serve as interactive guides for implementing best practices in software development.

## Overview

The notebooks in this directory provide hands-on, executable documentation for:
- Bootstrapping new projects
- Implementing security and supply chain best practices
- Setting up contracts and testing
- Implementing observability and SLOs
- Building and publishing documentation

## Available Notebooks

### 01_bootstrap.ipynb
**Repository Scaffolding & Quality Gates**

Demonstrates how to:
- Scaffold a new repository using Cookiecutter templates
- Enable quality gates (linting, testing, security)
- Generate SBOM (Software Bill of Materials)
- Demonstrate artifact signing with Sigstore/Cosign

**Topics**: Cookiecutter, Quality Gates, SBOM, Signing

### 02_security_supply_chain.ipynb
**Security & Supply Chain Best Practices**

Covers:
- SAST (Static Application Security Testing)
- Secret scanning
- SBOM generation and management
- Build provenance and attestation
- SLSA compliance

**Topics**: SAST, Secrets, SBOM, Provenance, SLSA

### 03_contracts_and_tests.ipynb
**OpenAPI/AsyncAPI & Testing Strategies**

Includes:
- API contract definition with OpenAPI
- Event contract definition with AsyncAPI
- Contract testing
- Mutation testing
- Property-based testing

**Topics**: OpenAPI, AsyncAPI, Contract Testing, Mutation Testing

### 04_observability_slos.ipynb
**OpenTelemetry & SLO Implementation**

Demonstrates:
- OpenTelemetry instrumentation
- Traces, metrics, and logs
- SLO (Service Level Objective) definition
- Error budgets
- SLO monitoring and alerting

**Topics**: OpenTelemetry, Observability, SLOs, Error Budgets

### 05_docs_to_book.ipynb
**Jupyter Book & Documentation Publishing**

Shows:
- Jupytext for notebook version control
- MyST Markdown features
- Jupyter Book configuration
- Building and publishing documentation
- GitHub Pages deployment

**Topics**: Jupytext, MyST Markdown, Jupyter Book, GitHub Pages

## Using the Notebooks

### Prerequisites

```bash
# Install requirements
pip install -r ../requirements.txt

# Or use the Binder environment (online)
# Click the "launch binder" badge in the main README
```

### Running Locally

```bash
# Start Jupyter
jupyter notebook

# Or Jupyter Lab
jupyter lab
```

Then open any notebook from the file browser.

### Running in CI

Notebooks are automatically executed in CI using nbmake:

```bash
pytest --nbmake notebooks/*.ipynb
```

### Parameterized Execution

Notebooks are parameterized with Papermill for automation:

```bash
papermill notebooks/01_bootstrap.ipynb output.ipynb \
  -p run_mode ci
```

## Notebook Features

### Parameterization

Each notebook has a parameters cell tagged with `parameters`:

```python
# Parameters cell
run_mode = "interactive"  # Options: interactive, ci, demo
```

You can override these with Papermill:

```bash
papermill notebook.ipynb output.ipynb -p run_mode ci
```

### MyST Markdown Mirrors

Notebooks are paired with MyST Markdown files in `docs/notebooks/` using Jupytext:

- Edit `.ipynb` files in Jupyter
- Changes automatically sync to `.md` files
- MyST files are version-controlled and used by Jupyter Book
- Clean diffs and easy code review

See [ADR-002](../docs/adr/ADR-002-jupytext-notebook-version-control.md) for details.

## Development

### Creating a New Notebook

1. Create the notebook in this directory
2. Add a parameters cell at the top
3. Pair it with MyST Markdown:
   ```bash
   jupytext --set-formats ipynb,../docs/notebooks//md:myst your_notebook.ipynb
   ```
4. Write your content
5. Test execution:
   ```bash
   pytest --nbmake your_notebook.ipynb
   ```
6. Commit only the MyST file to git

### Best Practices

- Keep notebooks focused on one topic
- Use clear section headings
- Include runnable code examples
- Add explanatory markdown cells
- Keep execution time reasonable (< 5 minutes)
- Use parameters for flexibility
- Test in CI before merging

## Testing

### Local Testing

```bash
# Test all notebooks
pytest --nbmake notebooks/*.ipynb

# Test specific notebook
pytest --nbmake notebooks/01_bootstrap.ipynb
```

### CI Testing

Notebooks are automatically tested on:
- Every pull request
- Every push to main
- Scheduled runs (weekly)

See `.github/workflows/notebooks-test.yml`

## Troubleshooting

### Notebook Won't Execute

1. Check Python version (requires 3.11+)
2. Verify all dependencies installed
3. Look for missing environment variables
4. Check for path issues

### Sync Issues with MyST

```bash
# Force sync
jupytext --sync notebooks/*.ipynb

# Re-pair if needed
jupytext --set-formats ipynb,../docs/notebooks//md:myst notebooks/*.ipynb
```

### Import Errors

```bash
# Reinstall requirements
pip install -r ../requirements.txt --force-reinstall
```

## Contributing

To contribute a new notebook or improve existing ones:

1. Follow the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
2. Ensure the notebook executes cleanly
3. Pair with MyST Markdown
4. Add tests if needed
5. Update this README
6. Submit a pull request

## References

- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [Papermill Documentation](https://papermill.readthedocs.io/)
- [nbmake Documentation](https://github.com/treebeardtech/nbmake)
- [Jupytext Documentation](https://jupytext.readthedocs.io/)
- [MyST Markdown](https://myst-parser.readthedocs.io/)

## Related

- [Jupyter Book Configuration](../docs/_config.yml)
- [MyST Markdown Mirrors](../docs/notebooks/)
- [Jupytext Configuration](../jupytext.toml)
- [CI Workflows](../.github/workflows/)

---

For questions, open an issue or discussion in the repository.

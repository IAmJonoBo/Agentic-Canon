# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Building the Documentation

### Prerequisites

- Python 3.8 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build Locally

```bash
jupyter-book build docs
```

The built documentation will be in `docs/_build/html/`.

### Serve Locally

```bash
jupyter-book build docs --path-output .
python -m http.server -d _build/html 8000
```

Then visit http://localhost:8000 in your browser.

## Structure

```
docs/
├── _config.yml        # Jupyter Book configuration
├── _toc.yml           # Table of contents
├── index.md           # Home page
├── getting-started.md # Getting started guide
├── user-guide.md      # User guide
├── api-reference.md   # API documentation
└── contributing.md    # Contributing guidelines
```

## Deployment

This documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch.

To enable GitHub Pages:

1. Go to repository Settings → Pages
2. Set Source to "gh-pages" branch
3. The documentation will be available at `https://username.github.io/{{cookiecutter.project_slug}}`

## License

{{cookiecutter.license}}

## Author

{{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

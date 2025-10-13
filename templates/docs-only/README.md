# Documentation-Only Cookiecutter Template

Jupyter Book documentation site template for creating beautiful, publication-quality documentation.

## Quick Start

```bash
# Using Cookiecutter
cookiecutter templates/docs-only

# Or using Agentic Canon CLI
agentic-canon init
# Select "Documentation Only" when prompted
```

## Features

### Core Capabilities

- ✅ **Jupyter Book** - Publication-quality documentation
- ✅ **MyST Markdown** - Enhanced markdown with roles and directives
- ✅ **Executable Content** - Notebooks and code blocks
- ✅ **Search** - Full-text search built-in
- ✅ **Navigation** - Multi-level table of contents
- ✅ **Theming** - Beautiful default theme

### Documentation Features

- ✅ **API Documentation** - Auto-generated from code
- ✅ **User Guides** - Step-by-step tutorials
- ✅ **Getting Started** - Quick start guide
- ✅ **Contributing Guidelines** - Contribution process
- ✅ **Cross-references** - Internal linking
- ✅ **Admonitions** - Notes, warnings, tips

### CI/CD

- ✅ **GitHub Actions** - Automated builds
- ✅ **GitHub Pages** - Free hosting
- ✅ **GitLab CI** - Alternative support
- ✅ **GitLab Pages** - Alternative hosting
- ✅ **Build Validation** - Check for broken links

## Template Configuration

### Required Parameters

| Parameter      | Description         | Example                          |
| -------------- | ------------------- | -------------------------------- |
| `project_name` | Documentation title | "Acme Documentation"             |
| `project_slug` | URL-friendly name   | "acme-docs"                      |
| `description`  | Short description   | "Documentation for Acme Project" |
| `author_name`  | Your name           | "Jane Doe"                       |
| `author_email` | Your email          | "jane@example.com"               |

### Optional Parameters

| Parameter     | Options                    | Default   | Description    |
| ------------- | -------------------------- | --------- | -------------- |
| `license`     | Apache-2.0, MIT, CC-BY-4.0 | CC-BY-4.0 | License type   |
| `ci_provider` | github, gitlab             | github    | CI/CD platform |

## Generated Project Structure

```
acme-docs/
├── .github/
│   └── workflows/
│       └── book-deploy.yml     # Build and deploy
├── docs/
│   ├── _config.yml             # Jupyter Book config
│   ├── _toc.yml                # Table of contents
│   ├── index.md                # Homepage
│   ├── getting-started.md      # Getting started guide
│   ├── user-guide.md           # User documentation
│   ├── api-reference.md        # API documentation
│   └── contributing.md         # Contributing guide
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Build documentation
jupyter-book build docs/

# View locally
open docs/_build/html/index.html

# Or serve with live reload
jupyter-book serve docs/

# Clean and rebuild
jupyter-book clean docs/
jupyter-book build docs/
```

## Documentation Structure

### index.md - Homepage

````markdown
# Welcome to Acme Documentation

This is the main landing page for your documentation.

```{tableofcontents}

```
````

## Quick Links

- {doc}`getting-started` - Get up and running
- {doc}`user-guide` - Learn how to use the project
- {doc}`api-reference` - API documentation

````

### getting-started.md

```markdown
# Getting Started

Quick start guide to get you up and running.

## Installation

```bash
pip install acme
````

## Basic Usage

```python
import acme

# Your first example
result = acme.do_something()
```

## Next Steps

Continue to the {doc}`user-guide` for more details.

````

### MyST Markdown Features

```markdown
# MyST Enhanced Markdown

## Admonitions

```{note}
This is a note admonition.
````

```{warning}
This is a warning.
```

```{tip}
This is a helpful tip!
```

## Cross-references

Link to other pages: {doc}`getting-started`
Link to sections: {ref}`section-label`

## Code blocks with execution

```{code-cell} python
print("This code will execute during build!")
```

## Tables

| Feature | Status |
| ------- | ------ |
| Search  | ✅     |
| PDF     | ✅     |
| Mobile  | ✅     |

## Images

```{figure} path/to/image.png
---
alt: Alt text
width: 500px
---
Caption for the figure
```

````

## Configuration

### _config.yml

```yaml
title: Acme Documentation
author: Jane Doe
logo: _static/logo.png

# Execution settings
execute:
  execute_notebooks: auto
  timeout: 60

# HTML settings
html:
  favicon: _static/favicon.ico
  use_edit_page_button: true
  use_repository_button: true
  use_issues_button: true

# Repository settings
repository:
  url: https://github.com/example/acme-docs
  path_to_book: docs/
  branch: main

# Launch buttons
launch_buttons:
  binderhub_url: ""
  colab_url: ""
  notebook_interface: jupyterlab

# Sphinx extensions
sphinx:
  extra_extensions:
    - sphinx.ext.autodoc
    - sphinx.ext.napoleon
    - sphinx_copybutton
````

### \_toc.yml

```yaml
format: jb-book
root: index
chapters:
  - file: getting-started
  - file: user-guide
    sections:
      - file: user-guide/installation
      - file: user-guide/configuration
      - file: user-guide/advanced
  - file: api-reference
    sections:
      - file: api-reference/module1
      - file: api-reference/module2
  - file: contributing
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/book-deploy.yml
name: Deploy Jupyter Book

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build book
        run: jupyter-book build docs/

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/_build/html
```

## Best Practices

### Documentation Writing

1. **Start with why** - Explain the purpose
2. **Show, don't tell** - Use examples
3. **Progressive disclosure** - Basic to advanced
4. **Keep it updated** - Review quarterly
5. **Search optimization** - Use clear headings

### Content Organization

```
docs/
├── index.md              # Welcome and overview
├── getting-started.md    # Quick start (15 min)
├── tutorials/            # Step-by-step guides
├── how-to/               # Task-oriented recipes
├── reference/            # API documentation
├── explanation/          # Conceptual topics
└── contributing.md       # How to contribute
```

### Writing Tips

- Use clear, concise language
- Break up long paragraphs
- Add visual elements (diagrams, screenshots)
- Include code examples
- Provide context and explanations
- Link to related content

## Advanced Features

### Auto-generated API Docs

````markdown
# API Reference

```{eval-rst}
.. automodule:: acme
   :members:
   :undoc-members:
   :show-inheritance:
```
````

````

### Executable Code

```markdown
# Interactive Example

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
````

````

### Custom CSS

```css
/* docs/_static/custom.css */
.admonition {
    border-left: 4px solid #007bff;
}

code {
    background-color: #f5f5f5;
}
````

## Standards Compliance

This template implements:

- ✅ **Documentation Best Practices** - Clear, concise, comprehensive
- ✅ **Accessibility (WCAG 2.1)** - Keyboard navigation, screen readers
- ✅ **Mobile-Responsive** - Works on all devices
- ✅ **Search Engine Optimization** - Discoverable content

## Related Resources

- [Jupyter Book Documentation](https://jupyterbook.org/)
- [MyST Markdown Guide](https://myst-parser.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Write the Docs](https://www.writethedocs.org/)

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Version**: 1.0.0

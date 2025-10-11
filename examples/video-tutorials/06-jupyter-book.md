# Video Tutorial Script: Using Jupyter Book for Documentation

**Duration:** 8-10 minutes  
**Target Audience:** Technical Writers, Developers, Documentation Engineers  
**Prerequisites:** Basic understanding of Markdown, familiarity with documentation

---

## Introduction (45 seconds)

### Opening (15 seconds)

"Welcome to the final video in our Agentic Canon tutorial series! Today we're exploring Jupyter Book—a powerful tool for creating beautiful, interactive documentation from computational notebooks and markdown files."

### What You'll Learn (30 seconds)

In this tutorial, you'll discover how to:
- Create interactive documentation with Jupyter Book
- Sync notebooks with Jupytext for version control
- Build and deploy documentation to GitHub Pages
- Write executable documentation
- Integrate code, narrative, and outputs seamlessly

"Let's turn your documentation from static text into a living, executable resource!"

---

## Section 1: Why Jupyter Book? (1.5 minutes)

### The Documentation Challenge (45 seconds)

"Traditional documentation has problems:"
- 📄 **Outdated** - Code examples drift from reality
- 📄 **Static** - No interactivity or exploration
- 📄 **Disconnected** - Documentation separate from code
- 📄 **Untested** - Examples may not even work

"Jupyter Book solves these by making documentation executable and testable."

### Jupyter Book Benefits (45 seconds)

**Show on screen: Jupyter Book features**

✅ **Executable Content**
- Run code directly in documentation
- Verify examples work with every build
- Show actual outputs, not screenshots

✅ **Beautiful Presentation**
- Professional book-like appearance
- Built-in search and navigation
- Mobile-responsive design

✅ **Developer-Friendly**
- Write in Markdown or Jupyter notebooks
- Version control with Git
- Automated deployment to GitHub Pages

✅ **Interactive Elements**
- Collapsible code cells
- Live code execution with Binder
- Embedded visualizations

---

## Section 2: Setting Up Jupyter Book (2 minutes)

### Project Structure (1 minute)

**Show on screen: Directory structure**

```
your-project/
├── docs/
│   ├── _config.yml          # Jupyter Book configuration
│   ├── _toc.yml             # Table of contents
│   ├── intro.md             # Landing page
│   ├── getting-started.md   # Getting started guide
│   ├── user-guide.md        # User guide
│   ├── api-reference.md     # API documentation
│   └── notebooks/           # Executable notebooks
│       ├── 01_tutorial.md   # MyST markdown notebooks
│       ├── 02_examples.md
│       └── 03_advanced.md
├── notebooks/               # Source notebooks
│   ├── 01_tutorial.ipynb
│   ├── 02_examples.ipynb
│   └── 03_advanced.ipynb
└── requirements.txt
```

"Notebooks live in `notebooks/` and are mirrored as MyST markdown in `docs/notebooks/` using Jupytext."

### Configuration (1 minute)

**Show on screen: docs/_config.yml**

```yaml
title: My Project Documentation
author: Your Name
logo: _static/logo.png

execute:
  execute_notebooks: force  # Always execute notebooks
  timeout: 300              # 5 minute timeout
  allow_errors: false       # Fail on errors

parse:
  myst_enable_extensions:
    - colon_fence      # ::: blocks
    - deflist          # Definition lists
    - dollarmath       # $...$ math
    - html_image       # HTML images
    - linkify          # Auto-link URLs
    - substitution     # Variable substitution
    - tasklist         # - [ ] task lists

sphinx:
  config:
    html_theme: sphinx_book_theme
    html_theme_options:
      repository_url: https://github.com/yourusername/yourproject
      use_repository_button: true
      use_issues_button: true
      use_edit_page_button: true

repository:
  url: https://github.com/yourusername/yourproject
  branch: main
```

**Show on screen: docs/_toc.yml**

```yaml
format: jb-book
root: intro
chapters:
  - file: getting-started
  - file: user-guide
  - file: api-reference
  - file: notebooks/01_tutorial
  - file: notebooks/02_examples
  - file: notebooks/03_advanced
```

---

## Section 3: Writing with MyST Markdown (2 minutes)

### MyST Markdown Basics (1 minute)

"MyST (Markedly Structured Text) extends Markdown with powerful features."

**Show on screen: Example MyST markdown**

````markdown
# Tutorial: Getting Started

## Installation

Install the package using pip:

```bash
pip install mypackage
```

## Quick Example

```{code-cell} python
import mypackage

# Create a client
client = mypackage.Client(api_key="demo")

# Fetch data
data = client.get_data()
print(f"Retrieved {len(data)} items")
```

:::{note}
This example uses a demo API key. Replace with your own key for production use.
:::

## Advanced Usage

```{code-cell} python
# Process data
processed = [item for item in data if item.status == "active"]

# Visualize
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(range(len(processed)), [item.value for item in processed])
plt.title("Active Items")
plt.show()
```
````

### Interactive Elements (1 minute)

**Show on screen: Advanced MyST features**

````markdown
:::{admonition} Pro Tip
:class: tip
Use environment variables for sensitive data like API keys!
:::

:::{dropdown} Show detailed explanation
This is additional information that users can expand if they want more details.
:::

```{margin}
This note appears in the margin, great for side comments!
```

::::{tab-set}
:::{tab-item} Python
```python
print("Hello from Python")
```
:::
:::{tab-item} JavaScript
```javascript
console.log("Hello from JavaScript")
```
:::
::::
````

---

## Section 4: Jupytext for Version Control (1.5 minutes)

### The Problem with Notebooks (30 seconds)

"Jupyter notebooks contain JSON with outputs and metadata, making them:"
- 😕 Difficult to review in PRs
- 😕 Prone to merge conflicts
- 😕 Full of noise in git diffs
- 😕 Hard to collaborate on

### Jupytext to the Rescue (1 minute)

**Show on screen: jupytext.toml**

```toml
[tool.jupytext]
formats = "notebooks///ipynb,docs/notebooks///md:myst"
```

"This syncs every `.ipynb` file with a MyST markdown mirror."

**Demo: Show sync in action**

```bash
# Edit notebook/01_tutorial.ipynb in Jupyter
# Save it

# Jupytext automatically updates docs/notebooks/01_tutorial.md
# Commit only the .md file to git!

git add docs/notebooks/01_tutorial.md
git commit -m "Update tutorial"
```

"The `.ipynb` files stay in `.gitignore`. Only clean markdown gets committed!"

---

## Section 5: Building and Deploying (2 minutes)

### Local Build (45 seconds)

**Show on screen: Terminal**

```bash
# Install dependencies
pip install -r requirements.txt

# Build the book
jupyter-book build docs/

# Open in browser
open docs/_build/html/index.html
```

**Demo: Show built documentation in browser**

"The book is a static website you can host anywhere!"

### GitHub Actions Deployment (1 minute 15 seconds)

**Show on screen: .github/workflows/book-deploy.yml**

```yaml
name: Deploy Jupyter Book

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Build book
      run: |
        jupyter-book build docs/
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: docs/_build/html
```

"Every push to main automatically builds and deploys your documentation!"

**Show on screen: GitHub Pages settings**

"Enable Pages in Settings → Pages → Source: gh-pages branch"

---

## Section 6: Advanced Features (1.5 minutes)

### Executable Books with Binder (45 seconds)

"Make your documentation interactive with Binder!"

**Show on screen: Add to _config.yml**

```yaml
launch_buttons:
  notebook_interface: jupyterlab
  binderhub_url: https://mybinder.org
```

**Demo: Click "Launch Binder" button**

"Readers can run your notebooks in the cloud without installing anything!"

### Cross-Referencing (45 seconds)

**Show on screen: Cross-reference examples**

````markdown
## Installation {#installation}

Install the package...

## Usage

Before using the package, make sure you've completed the [installation](#installation).

See {doc}`api-reference` for the complete API.

Check {ref}`advanced-usage` for advanced topics.
````

"Jupyter Book automatically creates navigation between pages and sections."

---

## Conclusion (1 minute)

### Recap (30 seconds)

"Today we covered:"
- ✅ Setting up Jupyter Book for your project
- ✅ Writing with MyST Markdown
- ✅ Using Jupytext for version control
- ✅ Building and deploying to GitHub Pages
- ✅ Adding interactive features

### Next Steps (30 seconds)

"You've now completed the Agentic Canon tutorial series!"

**Show on screen:**
- 📚 Full example: docs/notebooks/05_docs_to_book.md
- 🔧 Configuration: docs/_config.yml
- 📖 Jupyter Book docs: https://jupyterbook.org
- 💬 Community: Join our GitHub Discussions

"Thanks for watching the entire series! Now go build amazing, well-documented, observable, and secure software. Happy coding!"

---

## YouTube Description Template

```
📚 Using Jupyter Book for Documentation

Learn how to create beautiful, executable documentation with Jupyter Book. This tutorial covers setup, MyST Markdown, Jupytext for version control, and automated deployment to GitHub Pages.

⏱️ Timestamps:
0:00 - Introduction
0:45 - Why Jupyter Book?
2:15 - Setting Up Jupyter Book
4:15 - Writing with MyST Markdown
6:15 - Jupytext for Version Control
7:45 - Building and Deploying
9:45 - Advanced Features
11:15 - Conclusion

🔗 Resources:
- Repository: https://github.com/IAmJonoBo/Agentic-Canon
- Full Guide: docs/notebooks/05_docs_to_book.md
- Jupyter Book: https://jupyterbook.org
- MyST Markdown: https://myst-parser.readthedocs.io

📚 Complete Tutorial Series:
1. Getting Started with Agentic Canon
2. Creating Services with Cookiecutter
3. Setting up CI/CD Pipelines
4. Implementing Security Gates
5. Adding Observability
6. Using Jupyter Book (this video)

#Documentation #JupyterBook #TechnicalWriting #Python #DevOps
```

---

## Social Media Snippets

**Twitter/X:**
"📚 Final tutorial in our series: Using Jupyter Book for Documentation! Learn to create beautiful, executable docs that sync with version control and deploy automatically to GitHub Pages. #Documentation #JupyterBook"

**LinkedIn:**
"Wrapping up our Agentic Canon tutorial series with Jupyter Book! Learn how to transform your documentation from static text into executable, interactive, and always-up-to-date resources. Perfect for technical writers and documentation engineers!"

**Reddit (r/python, r/programming):**
"Tutorial: Using Jupyter Book for Documentation - Create beautiful, executable documentation with automated deployment. Covers MyST Markdown, Jupytext for version control, and integration with GitHub Pages. Final video in the Agentic Canon series!"

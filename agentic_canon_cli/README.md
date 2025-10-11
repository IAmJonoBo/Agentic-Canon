# Agentic Canon CLI

Interactive command-line wizard for creating new projects with the Agentic Canon framework.

## Installation

```bash
# From the repository root
pip install -e .
```

Or for development:

```bash
pip install -e ".[cli]"
```

## Usage

### Interactive Wizard

Run the interactive wizard to create a new project:

```bash
agentic-canon init
```

or

```bash
python -m agentic_canon_cli
```

The wizard will guide you through:

1. **Template Selection**: Choose from Python, Node.js, React, Go, or Docs-only
2. **Project Configuration**: Name, description, author information
3. **Feature Selection**: Enable/disable optional features
   - Jupyter Book documentation
   - Security gates (CodeQL, secret scanning)
   - SBOM generation and signing
   - Contract testing
4. **CI/CD Provider**: GitHub Actions, GitLab CI, or Azure Pipelines
5. **License**: Apache-2.0, MIT, or Proprietary
6. **Generation**: Creates your project with all selected features

### Example Session

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              🚀 Agentic Canon CLI 🚀                     ║
║                                                           ║
║   Machine-readable, agent-friendly project scaffolding   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

📦 Select a project template:

  1. Python Service (FastAPI/Flask)
  2. Node.js Service (TypeScript)
  3. React WebApp (Vite + TypeScript)
  4. Go Service
  5. Documentation Only (Jupyter Book)

👉 Enter your choice (1-5): 1

✅ Selected: Python Service (FastAPI/Flask)

📝 Project Configuration:

  Project name (e.g., 'My Awesome Service'): My API
  Project slug [my-api]: 
  Package name [my_api]: 
  Description: A modern REST API
  Author name: John Doe
  Author email: john@example.com

⚙️  Optional Features:

  Include Jupyter Book documentation? (Y/n): y
  Enable security gates (CodeQL, secret scanning)? (Y/n): y
  Enable SBOM generation and signing? (Y/n): y
  Enable contract testing? (Y/n): n

  CI/CD Provider:
    1. GitHub Actions
    2. GitLab CI
    3. Azure Pipelines
  Select (1-3) [1]: 1

  License:
    1. Apache-2.0
    2. MIT
    3. Proprietary
  Select (1-3) [1]: 1

📊 Project Summary:
  Template: python-service
  Name: My API
  Slug: my-api
  Features: include_jupyter_book, enable_security_gates, enable_sbom_signing

✅ Generate project? (Y/n): y

🔨 Generating project...

✅ Project generated successfully!

📋 Next Steps:

  1. cd my-api
  2. python -m venv venv
  3. source venv/bin/activate
  4. pip install -e .[dev]
  5. pre-commit install
  6. git add . && git commit -m 'Initial commit'
  7. Create a GitHub repository and push your code
  8. Enable GitHub Actions in repository settings
  9. Configure GitHub Pages (Settings → Pages → Source: gh-pages)

🎉 Happy coding!
```

## Features

- 🎨 **Interactive UI**: Beautiful terminal interface with emoji indicators
- ⚡ **Fast**: Leverages Cookiecutter for quick project generation
- 🔧 **Customizable**: Toggle features on/off based on your needs
- 📚 **Guided**: Clear explanations and sensible defaults
- 🚀 **Production-Ready**: Generates projects with best practices built-in

## Requirements

- Python 3.11+
- cookiecutter
- Terminal with emoji support (optional but recommended)

## Development

To work on the CLI:

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest tests/test_cli.py -v

# Test interactively
python -m agentic_canon_cli
```

## Command Reference

### `agentic-canon init`

Launch the interactive wizard to create a new project.

**Features:**
- Template selection
- Project configuration
- Feature toggles
- Summary and confirmation
- Automatic project generation

### Future Commands (Planned)

- `agentic-canon update` - Update existing project from template
- `agentic-canon check` - Validate project structure
- `agentic-canon doctor` - Diagnose common issues
- `agentic-canon list` - List available templates

## Template Variables

The CLI automatically configures these Cookiecutter variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `project_name` | Human-readable name | "My Awesome API" |
| `project_slug` | Kebab-case slug | "my-awesome-api" |
| `pkg_name` | Python package name | "my_awesome_api" |
| `project_description` | Brief description | "A modern REST API" |
| `author_name` | Author's name | "John Doe" |
| `author_email` | Author's email | "john@example.com" |
| `license` | License type | "Apache-2.0" |
| `include_jupyter_book` | Enable docs | "yes"/"no" |
| `enable_security_gates` | Enable security | "yes"/"no" |
| `enable_sbom_signing` | Enable SBOM | "yes"/"no" |
| `enable_contract_tests` | Enable contracts | "yes"/"no" |
| `ci_provider` | CI/CD platform | "github"/"gitlab"/"azure" |

## Troubleshooting

### "Cookiecutter not found"

Install cookiecutter:
```bash
pip install cookiecutter
```

### "Template not found"

Make sure you're running the CLI from the Agentic Canon repository root or have it properly installed.

### "Permission denied"

On Unix systems, you may need to make the script executable:
```bash
chmod +x agentic_canon_cli/cli.py
```

## Contributing

Contributions welcome! To add a new template to the CLI:

1. Create the template in `templates/`
2. Add it to `select_template()` in `cli.py`
3. Update this README
4. Test the generation process

## License

Apache-2.0

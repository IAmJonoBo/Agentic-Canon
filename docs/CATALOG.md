# Agentic Canon Catalog

## Overview

The `catalog.json` file is a machine-readable catalog of all templates, assets, and resources provided by Agentic Canon. It enables automated discovery and integration with tools, agents, and services.

## Purpose

The catalog serves multiple purposes:

1. **Discovery**: Enables automated discovery of available templates and assets
2. **Integration**: Facilitates integration with MCP servers, CLI tools, and agents
3. **Documentation**: Provides structured metadata about all resources
4. **Validation**: Enables validation of template usage and requirements
5. **Automation**: Powers automated workflows and tooling

## Structure

The catalog is organized into several top-level sections:

### Templates

The `templates` section catalogs all Cookiecutter templates:

```json
{
  "templates": {
    "cookiecutter": [
      {
        "id": "python-service",
        "name": "Python Service Template",
        "description": "...",
        "path": "templates/python-service",
        "language": "python",
        "framework": "fastapi",
        "features": [...],
        "requirements": {...},
        "usage": {...},
        "compliance": {...}
      }
    ]
  }
}
```

**Available Templates:**
- `python-service` - Python/FastAPI microservice
- `node-service` - Node.js/Express API service
- `react-webapp` - React web application with Vite and Storybook
- `go-service` - Go microservice
- `docs-only` - Jupyter Book documentation site
- `project-management` - GitHub Actions automation workflows

### Assets

The `assets` section catalogs reusable components:

- **Dashboards**: Grafana dashboards for metrics visualization
  - DORA metrics
  - SPACE/DevEx metrics
  - Quality metrics
  - Security metrics

- **Workflows**: GitHub Actions and Azure Pipelines workflows
  - License compliance
  - Container scanning
  - IaC security
  - Accessibility testing
  - Performance budgets

- **Fitness Functions**: Automated architecture and quality checks
  - Performance fitness
  - Architecture fitness
  - Security fitness

### Documentation

The `documentation` section catalogs framework documentation and guides:

- Framework documents (FRAMEWORK.md, QUALITY_STANDARDS.md, CONVENTIONS.md)
- Architecture Decision Records (ADRs)
- Runbooks
- Guides

### CLI

Information about the `agentic-canon` CLI tool and its commands.

### Distribution

Methods for accessing and using templates:
- Cookiecutter
- tiged
- Git sparse-checkout
- GitHub Releases

### Compliance

Standards compliance information and validation details.

## Usage

### For Humans

Browse the catalog to discover available templates and assets:

```bash
# View the catalog
cat catalog.json | jq '.templates.cookiecutter[] | {id, name, description}'

# List all template IDs
cat catalog.json | jq -r '.templates.cookiecutter[].id'

# Get details for a specific template
cat catalog.json | jq '.templates.cookiecutter[] | select(.id == "python-service")'

# List all available dashboards
cat catalog.json | jq '.assets.dashboards.grafana[] | {id, name}'

# Check compliance standards
cat catalog.json | jq '.compliance.standards'
```

### For Agents and Tools

The catalog is designed for programmatic consumption:

**Python Example:**
```python
import json
import requests

# Load catalog
with open('catalog.json') as f:
    catalog = json.load(f)

# Find a template
def find_template(template_id):
    templates = catalog['templates']['cookiecutter']
    return next((t for t in templates if t['id'] == template_id), None)

# Get usage command
template = find_template('python-service')
cookiecutter_cmd = template['usage']['cookiecutter']
print(f"Generate with: cookiecutter {cookiecutter_cmd}")

# Check requirements
print(f"Requirements: {template['requirements']}")

# List features
print(f"Features: {', '.join(template['features'])}")
```

**JavaScript Example:**
```javascript
const fs = require('fs');

// Load catalog
const catalog = JSON.parse(fs.readFileSync('catalog.json', 'utf8'));

// Find templates by language
function findTemplatesByLanguage(language) {
  return catalog.templates.cookiecutter.filter(
    t => t.language === language
  );
}

// Get Python templates
const pythonTemplates = findTemplatesByLanguage('python');
console.log(`Found ${pythonTemplates.length} Python templates`);

// Get all available workflows
const workflows = catalog.assets.workflows['github-actions'];
console.log(`Available workflows: ${workflows.map(w => w.id).join(', ')}`);
```

### For MCP Servers

The catalog powers MCP resource endpoints:

```python
# MCP resource: ac://catalog
@server.resource("ac://catalog")
async def get_catalog():
    with open('catalog.json') as f:
        return json.load(f)

# MCP resource: ac://templates
@server.resource("ac://templates")
async def list_templates():
    catalog = get_catalog()
    return catalog['templates']['cookiecutter']

# MCP resource: ac://template/{id}
@server.resource("ac://template/{template_id}")
async def get_template(template_id: str):
    catalog = get_catalog()
    templates = catalog['templates']['cookiecutter']
    return next((t for t in templates if t['id'] == template_id), None)
```

## Schema

The catalog follows a JSON schema for validation. Key fields:

### Template Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique template identifier |
| `name` | string | Human-readable name |
| `description` | string | Template description |
| `path` | string | Path to template in repository |
| `language` | string | Primary programming language |
| `framework` | string | Main framework used |
| `version` | string | Template version |
| `tags` | array | Tags for discovery |
| `features` | array | List of features |
| `requirements` | object | System requirements |
| `example` | string | Path to example project |
| `usage` | object | Usage commands for different methods |
| `documentation` | array | Paths to documentation |
| `compliance` | object | Standards compliance info |

### Asset Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique asset identifier |
| `name` | string | Human-readable name |
| `description` | string | Asset description |
| `path` | string | Path to asset in repository |
| `tags` | array | Tags for discovery |

## Maintenance

### Updating the Catalog

When adding new templates or assets:

1. Add entry to appropriate section in `catalog.json`
2. Ensure all required fields are populated
3. Validate JSON syntax: `python -c "import json; json.load(open('catalog.json'))"`
4. Update version number if making breaking changes
5. Update `updated` date field

### Validation

Validate the catalog structure:

```bash
# Check JSON syntax
python -c "import json; json.load(open('catalog.json')); print('✓ Valid JSON')"

# Verify template count
python -c "import json; cat = json.load(open('catalog.json')); print(f'Templates: {len(cat[\"templates\"][\"cookiecutter\"])}')"

# Check for required fields
python -c "
import json
cat = json.load(open('catalog.json'))
for t in cat['templates']['cookiecutter']:
    assert all(k in t for k in ['id', 'name', 'path', 'description'])
print('✓ All templates have required fields')
"
```

## Integration Examples

### CLI Integration

```python
# agentic_canon/cli.py
import json
from pathlib import Path

def load_catalog():
    catalog_path = Path(__file__).parent.parent / 'catalog.json'
    with open(catalog_path) as f:
        return json.load(f)

def list_templates():
    catalog = load_catalog()
    templates = catalog['templates']['cookiecutter']
    
    print("Available templates:\n")
    for template in templates:
        print(f"  {template['id']}: {template['name']}")
        print(f"    {template['description']}")
        print(f"    Language: {template.get('language', 'N/A')}")
        print()

def get_template_info(template_id):
    catalog = load_catalog()
    templates = catalog['templates']['cookiecutter']
    template = next((t for t in templates if t['id'] == template_id), None)
    
    if template:
        return template
    else:
        raise ValueError(f"Template '{template_id}' not found")
```

### Web UI Integration

```javascript
// Fetch and display catalog
async function loadCatalog() {
  const response = await fetch('/catalog.json');
  const catalog = await response.json();
  return catalog;
}

async function renderTemplates() {
  const catalog = await loadCatalog();
  const templates = catalog.templates.cookiecutter;
  
  const container = document.getElementById('templates');
  templates.forEach(template => {
    const card = document.createElement('div');
    card.className = 'template-card';
    card.innerHTML = `
      <h3>${template.name}</h3>
      <p>${template.description}</p>
      <div class="tags">
        ${template.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
      </div>
      <button onclick="generateFromTemplate('${template.id}')">
        Use Template
      </button>
    `;
    container.appendChild(card);
  });
}
```

### GitHub Actions Integration

```yaml
name: List Available Templates
on: [workflow_dispatch]
jobs:
  list-templates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Parse catalog
        run: |
          echo "## Available Templates" >> $GITHUB_STEP_SUMMARY
          cat catalog.json | jq -r '.templates.cookiecutter[] | "- **\(.name)** (\(.id)): \(.description)"' >> $GITHUB_STEP_SUMMARY
```

## Future Enhancements

Planned improvements to the catalog:

1. **JSON Schema**: Add formal JSON Schema for validation
2. **Versioning**: Support multiple template versions
3. **Dependencies**: Track dependencies between templates
4. **Metrics**: Usage statistics and popularity
5. **Search API**: Full-text search across catalog
6. **Tags API**: Browse by tags and categories
7. **Validation**: Automated validation in CI/CD
8. **Documentation**: Auto-generate documentation from catalog

## References

- [MCP (Model Context Protocol)](https://spec.modelcontextprotocol.io/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [JSON Schema](https://json-schema.org/)

---

**Last Updated**: 2025-10-12  
**Version**: 1.0.0  
**Status**: Active

# Creating a New Service with Cookiecutter

**Duration:** 8-10 minutes  
**Target Audience:** Developers familiar with Agentic Canon basics  
**Prerequisites:** Agentic Canon installed, basic Cookiecutter knowledge

---

## Script Outline

### Introduction (30 seconds)

"Welcome back! In this tutorial, we'll dive deeper into creating services using Cookiecutter templates. We'll explore different template types, customization options, and best practices."

---

### Understanding Cookiecutter Templates (1 minute)

**[Screen: File explorer showing templates/ directory]**

"Agentic Canon uses Cookiecutter for multi-template support. Let's look at what templates are available:"

```bash
# List available templates
ls -la templates/

# Templates:
# - python-service/    Production Python API service
# - node-service/      TypeScript Node.js service
# - react-webapp/      React + Vite web application  
# - go-service/        Go microservice
# - docs-only/         Documentation-only project
```

---

### Method 1: Using the CLI Wizard (2 minutes)

**[Screen: Terminal]**

"The easiest way is using our interactive CLI:"

```bash
agentic-canon init
```

**Walk through:**
- Template selection with descriptions
- Project configuration
- Feature toggles
- Real-time validation
- Summary and confirmation

---

### Method 2: Direct Cookiecutter (3 minutes)

**[Screen: Terminal]**

"For advanced users, you can use Cookiecutter directly:"

```bash
# Using local template
cookiecutter templates/python-service

# From GitHub (once published)
cookiecutter gh:IAmJonoBo/Agentic-Canon --directory templates/python-service

# Interactive prompts
# - project_name
# - project_slug  
# - author_name
# - description
# - features
```

**Show:**
- Different prompt types
- Validation rules
- Default values
- Conditional prompts

---

### Customizing Templates (2 minutes)

**[Screen: Code editor showing template structure]**

"Let's explore template anatomy:"

```
templates/python-service/
├── cookiecutter.json       # Template variables
├── hooks/                  
│   ├── pre_gen_project.py  # Validation
│   └── post_gen_project.py # Post-generation setup
└── {{cookiecutter.project_slug}}/
    ├── src/
    ├── tests/
    └── ...
```

**Explain:**
- Template variables with Jinja2
- Conditional file inclusion
- Pre/post generation hooks
- Hook capabilities

---

### Testing Generated Projects (1-2 minutes)

**[Screen: Terminal split view]**

```bash
# Generate project
cookiecutter templates/python-service

# Enter project
cd my-new-service

# Run tests
pytest

# Check pre-commit
pre-commit run --all-files

# Local development
pip install -e ".[dev]"
python -m my_new_service
```

---

### Advanced Features (1 minute)

**[Screen: Code editor]**

"Advanced template features:"

1. **Conditional Features**
   ```jinja
   {% if cookiecutter.use_jupyter_book == 'yes' %}
   docs/
   {% endif %}
   ```

2. **Dynamic Content**
   ```jinja
   # {{cookiecutter.project_name}}
   Author: {{cookiecutter.author_name}}
   ```

3. **Multiple CI/CD Options**
   - GitHub Actions
   - Azure Pipelines
   - GitLab CI

---

### Template Updates with Cruft (1 minute)

**[Screen: Terminal]**

"Keep your project in sync with template updates:"

```bash
# Install cruft
pip install cruft

# Link to template
cruft link https://github.com/IAmJonoBo/Agentic-Canon --directory templates/python-service

# Check for updates
cruft check

# Apply updates
cruft update
```

---

### Best Practices (1 minute)

1. **Always use semantic versioning**
2. **Test templates with pytest-cookies**
3. **Document template variables**
4. **Use hooks for validation**
5. **Keep templates minimal**
6. **Version control generated projects**

---

### Conclusion (30 seconds)

"You now know how to:
- Choose the right template
- Generate projects with CLI or Cookiecutter
- Customize templates
- Keep projects updated

Next: Learn about setting up CI/CD pipelines!"

---

## Key Commands Reference

```bash
# CLI wizard
agentic-canon init

# Direct Cookiecutter
cookiecutter templates/python-service

# From GitHub
cookiecutter gh:IAmJonoBo/Agentic-Canon --directory templates/python-service

# Template updates
cruft link <template-url> --directory <path>
cruft check
cruft update

# Testing
pytest templates/python-service
```

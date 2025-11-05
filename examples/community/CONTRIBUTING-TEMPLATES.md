# Community Template Contribution Guide

Welcome to the Agentic Canon community! This guide will help you contribute new templates to the project.

## Overview

The Agentic Canon community template system allows developers to:

- Submit new project templates
- Share best practices
- Build on existing templates
- Help others get started faster

## Template Types

We accept templates for:

1. **Programming Languages**
   - Python, JavaScript/TypeScript, Go, Rust, Java, C#, Ruby, etc.

2. **Frameworks**
   - Web: FastAPI, Django, Express, NestJS, React, Vue, Angular, Svelte
   - Mobile: React Native, Flutter, Swift, Kotlin
   - Desktop: Electron, Tauri, Qt

3. **Architectures**
   - Microservices
   - Serverless
   - Monoliths
   - Event-driven
   - CQRS/Event Sourcing

4. **Domains**
   - ML/AI projects
   - Data pipelines
   - IoT applications
   - Blockchain/Web3
   - Game development

## Contribution Process

### 1. Check Existing Templates

Before creating a new template, check if similar templates exist:

```bash
ls templates/
```

Review the [template catalog](../templates/README.md) to avoid duplicates.

### 2. Create Your Template

#### Directory Structure

```
templates/your-template/
├── cookiecutter.json           # Template variables
├── README.md                   # Template documentation
├── hooks/
│   ├── pre_gen_project.py     # Pre-generation validation
│   └── post_gen_project.py    # Post-generation setup
├── {{cookiecutter.project_slug}}/
│   ├── README.md
│   ├── src/
│   ├── tests/
│   ├── .github/workflows/
│   └── ... (your template files)
└── tests/
    └── test_template.py       # Template tests
```

#### cookiecutter.json

Define your template variables:

```json
{
  "project_name": "My Awesome Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-').replace('_', '-') }}",
  "project_description": "A brief description",
  "author_name": "Your Name",
  "author_email": "your.email@example.com",
  "version": "0.1.0",
  "license": ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause"],

  "_copy_without_render": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg"]
}
```

#### Template README

Document your template thoroughly:

```markdown
# Template Name

Brief description of what this template creates.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Tool 1
- Tool 2

## Quick Start

\`\`\`bash
cookiecutter gh:IAmJonoBo/Agentic-Canon --directory templates/your-template
\`\`\`

## Configuration

Explain template variables and options.

## Generated Project Structure

Show the directory structure.

## Next Steps

What users should do after generating the project.

## License

License information.
```

### 3. Add Validation Hooks

#### Pre-generation Hook

```python
# hooks/pre_gen_project.py
import re
import sys

project_slug = "{{ cookiecutter.project_slug }}"

# Validate project slug
if not re.match(r'^[a-z][a-z0-9-]+$', project_slug):
    print(f"ERROR: '{project_slug}' is not a valid project slug!")
    print("Project slug must:")
    print("  - Start with a lowercase letter")
    print("  - Contain only lowercase letters, numbers, and hyphens")
    sys.exit(1)

# Validate email
email = "{{ cookiecutter.author_email }}"
if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
    print(f"ERROR: '{email}' is not a valid email address!")
    sys.exit(1)

print("✅ Template validation passed")
```

#### Post-generation Hook

```python
# hooks/post_gen_project.py
import os
import subprocess
import shutil

def remove_optional_files():
    """Remove files based on user choices."""
    use_docker = "{{ cookiecutter.use_docker }}"

    if use_docker == "no":
        os.remove("Dockerfile")
        os.remove("docker-compose.yml")
        print("Removed Docker files")

def initialize_git():
    """Initialize git repository."""
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from Agentic Canon"],
            check=True
        )
        print("✅ Git repository initialized")
    except subprocess.CalledProcessError:
        print("⚠️  Could not initialize git repository")

def install_pre_commit_hooks():
    """Install pre-commit hooks."""
    try:
        subprocess.run(["pre-commit", "install"], check=True)
        print("✅ Pre-commit hooks installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Could not install pre-commit hooks")

def show_next_steps():
    """Display next steps to user."""
    project_name = "{{ cookiecutter.project_slug }}"

    print("\n" + "="*60)
    print(f"🎉 Successfully created {project_name}!")
    print("="*60)
    print("\n📝 Next steps:")
    print(f"  1. cd {project_name}")
    print("  2. Install dependencies (see README.md)")
    print("  3. Run tests")
    print("  4. Start developing!")
    print("\n📚 Documentation: ./README.md")
    print("🐛 Issues: https://github.com/IAmJonoBo/Agentic-Canon/issues")
    print("="*60 + "\n")

if __name__ == "__main__":
    remove_optional_files()
    initialize_git()
    install_pre_commit_hooks()
    show_next_steps()
```

### 4. Write Tests

```python
# tests/test_template.py
import pytest
from pathlib import Path

def test_template_generation(cookies):
    """Test basic template generation."""
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()

def test_required_files_exist(cookies):
    """Test that required files are generated."""
    result = cookies.bake()

    required_files = [
        "README.md",
        ".gitignore",
        "pyproject.toml",  # or package.json, etc.
        "src",
        "tests",
    ]

    for file_name in required_files:
        file_path = result.project_path / file_name
        assert file_path.exists(), f"{file_name} should exist"

def test_optional_files(cookies):
    """Test conditional file generation."""
    result = cookies.bake(extra_context={"use_docker": "yes"})

    assert (result.project_path / "Dockerfile").exists()
    assert (result.project_path / "docker-compose.yml").exists()

    result = cookies.bake(extra_context={"use_docker": "no"})

    assert not (result.project_path / "Dockerfile").exists()
    assert not (result.project_path / "docker-compose.yml").exists()

def test_generated_project_valid(cookies):
    """Test that generated project is valid."""
    result = cookies.bake()

    # For Python projects
    assert (result.project_path / "pyproject.toml").exists()

    # Check that tests can run
    # This depends on your project type
```

### 5. Submit Pull Request

1. **Fork the repository**

   ```bash
   # Fork on GitHub, then clone
   git clone https://github.com/YOUR-USERNAME/Agentic-Canon.git
   cd Agentic-Canon
   ```

2. **Create a branch**

   ```bash
   git checkout -b add-your-template-name
   ```

3. **Add your template**

   ```bash
   # Add your template files
   git add templates/your-template/

   # Commit with descriptive message
   git commit -m "Add [Framework] template for [use case]"
   ```

4. **Push and create PR**

   ```bash
   git push origin add-your-template-name
   ```

5. **Fill out PR template** (see below)

## Pull Request Template

```markdown
## Template Description

Brief description of what this template creates.

## Template Type

- [ ] Programming Language
- [ ] Framework
- [ ] Architecture Pattern
- [ ] Domain-Specific

## Checklist

- [ ] Template follows directory structure guidelines
- [ ] cookiecutter.json has all required fields
- [ ] README.md is comprehensive
- [ ] Pre/post generation hooks are included
- [ ] Tests are included and passing
- [ ] Template has been tested locally
- [ ] Documentation is clear and complete
- [ ] License is specified

## Testing

Describe how you tested the template:

\`\`\`bash
cookiecutter templates/your-template
cd generated-project

# Commands to verify it works

\`\`\`

## Screenshots (if applicable)

Add screenshots of the generated project.

## Additional Notes

Any additional context or notes for reviewers.
```

## Quality Standards

All templates must meet these standards:

### Required Features

1. **Documentation**
   - Comprehensive README
   - Clear quick start guide
   - Documented variables
   - Usage examples

2. **Testing**
   - Template generation tests
   - Generated project tests
   - CI/CD configuration

3. **Best Practices**
   - Security best practices
   - Code quality tools
   - Pre-commit hooks
   - License file

4. **CI/CD**
   - GitHub Actions workflow
   - Linting and formatting
   - Test automation
   - (Optional) Deployment examples

### Code Quality

- Follow language-specific conventions
- Include linting configuration
- Use type hints/annotations where applicable
- Include formatter configuration (Black, Prettier, etc.)

### Security

- No hardcoded secrets
- Security scanning configuration
- Dependency vulnerability checks
- SBOM generation (for production templates)

## Review Process

1. **Automated Checks** (5-10 minutes)
   - Template validation
   - Tests pass
   - Linting checks
   - Security scan

2. **Community Review** (1-3 days)
   - Code review by maintainers
   - Template quality check
   - Documentation review
   - Testing by reviewers

3. **Approval & Merge** (1-2 days)
   - Final approval by maintainer
   - Merge to main branch
   - Template published

## Template Versioning

Templates follow Semantic Versioning:

- **Major**: Breaking changes to template variables or structure
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, documentation updates

Use Cruft to help users update their projects:

```bash
cruft link https://github.com/IAmJonoBo/Agentic-Canon \
  --directory templates/your-template

cruft check  # Check for updates
cruft update # Apply updates
```

## Template Marketplace (Coming Soon)

We're building a template marketplace where:

- Templates can be rated and reviewed
- Usage statistics are tracked
- Popular templates are featured
- Templates can be searched and filtered

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
- **Bugs**: Open an [Issue](https://github.com/IAmJonoBo/Agentic-Canon/issues)
- **Ideas**: Open a [Discussion](https://github.com/IAmJonoBo/Agentic-Canon/discussions)

## Examples of Good Templates

Check out these existing templates for inspiration:

- [Python Service](../templates/python-service/)
- More coming soon!

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Credited in template documentation
- Featured in release notes
- Showcased on project website (coming soon)

## Code of Conduct

Please read and follow our [Code of Conduct](../../CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Thank you for contributing to Agentic Canon and helping the community! 🎉

Your contributions help developers worldwide build better software faster.

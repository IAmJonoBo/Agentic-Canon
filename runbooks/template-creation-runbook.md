# Runbook: Template Creation

## Purpose

This runbook provides step-by-step instructions for creating new Cookiecutter templates in the Agentic Canon framework. Use this guide to add support for new languages, frameworks, or project types.

## Prerequisites

- Git and GitHub CLI installed
- Python 3.11+ with `cookiecutter` and `pytest-cookies` installed
- Text editor or IDE
- Basic understanding of Jinja2 templating
- Familiarity with target technology stack

## Steps

### 1. Plan Your Template

**Duration**: 30-60 minutes

**Actions**:

1. Identify the target technology (language, framework, tools)
2. Research best practices and common patterns
3. List required features:
   - Build system (e.g., npm, pip, go modules, make)
   - Testing framework
   - Linting/formatting tools
   - CI/CD requirements
   - Security scanning needs
4. Review existing templates for patterns to reuse

**Validation**: Create a design document or checklist of features

### 2. Create Template Directory Structure

**Duration**: 15 minutes

**Commands**:

```bash
# Navigate to templates directory
cd /path/to/Agentic-Canon/templates

# Create template directory
mkdir -p my-template/hooks
mkdir -p my-template/{{cookiecutter.project_slug}}

# Create initial files
touch my-template/cookiecutter.json
touch my-template/hooks/pre_gen_project.py
touch my-template/hooks/post_gen_project.py
```

**Expected Structure**:

```
templates/my-template/
├── cookiecutter.json              # Template variables
├── hooks/
│   ├── pre_gen_project.py        # Pre-generation validation
│   └── post_gen_project.py       # Post-generation setup
└── {{cookiecutter.project_slug}}/
    └── [template files]
```

**Validation**: Verify directory structure matches pattern

### 3. Define Template Variables

**Duration**: 15-30 minutes

**Actions**:

Create `cookiecutter.json` with all template variables:

```json
{
  "project_name": "My Project",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-').replace('_', '-') }}",
  "description": "A short description of the project",
  "author_name": "Your Name",
  "author_email": "you@example.com",
  "license": ["MIT", "Apache-2.0", "BSD-3-Clause", "GPL-3.0", "CC-BY-4.0"],
  "version": "0.1.0",

  "_comment_features": "Optional features (yes/no)",
  "enable_security_gates": ["yes", "no"],
  "enable_sbom_signing": ["yes", "no"],
  "ci_provider": ["github", "gitlab", "azure", "none"],

  "_comment_tech": "Technology-specific variables",
  "language_version": "1.0"
}
```

**Best Practices**:

- Use computed defaults where possible (e.g., `project_slug`)
- Provide sensible default values
- Group related variables with comments
- Use choice lists for limited options
- Keep variable names consistent across templates

**Validation**: Valid JSON, all required fields present

### 4. Implement Pre-Generation Hook

**Duration**: 30 minutes

**Create** `hooks/pre_gen_project.py`:

```python
"""Pre-generation validation for my-template."""
import re
import sys


def validate_project_slug(slug):
    """Validate project slug format."""
    pattern = r'^[a-z][a-z0-9-]*[a-z0-9]$'
    if not re.match(pattern, slug):
        print(f"ERROR: Invalid project_slug '{slug}'")
        print("Must be lowercase, start with letter, contain only letters, numbers, and hyphens")
        return False
    return True


def validate_author_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print(f"ERROR: Invalid email '{email}'")
        return False
    return True


def main():
    """Run all validations."""
    project_slug = '{{ cookiecutter.project_slug }}'
    author_email = '{{ cookiecutter.author_email }}'

    if not validate_project_slug(project_slug):
        sys.exit(1)

    if not validate_author_email(author_email):
        sys.exit(1)

    print(f"✓ Validation passed for: {project_slug}")


if __name__ == '__main__':
    main()
```

**Validation**: Run hook manually with test values

### 5. Create Template Files

**Duration**: 2-4 hours

**Actions**:

Create all necessary files in `{{cookiecutter.project_slug}}/`:

1. **README.md** - Project documentation
2. **Build configuration** - `package.json`, `pyproject.toml`, `go.mod`, etc.
3. **Source code** - Example application code
4. **Tests** - Example test files
5. **CI/CD** - `.github/workflows/ci.yml`
6. **Configuration** - `.gitignore`, `.editorconfig`, etc.
7. **Documentation** - User guides, API docs

**Jinja2 Templating Tips**:

```jinja2
# Conditional sections
{% if cookiecutter.enable_security_gates == "yes" %}
[security configuration]
{% endif %}

# Variable substitution
project_name = "{{ cookiecutter.project_name }}"

# Escaping GitHub Actions syntax
{% raw %}
env:
  NODE_VERSION: ${{ matrix.node-version }}
{% endraw %}

# Computed values
pkg_name = "{{ cookiecutter.project_slug.replace('-', '_') }}"
```

**Best Practices**:

- Follow language-specific conventions
- Include comprehensive examples
- Add inline comments explaining configurations
- Use conditional blocks for optional features
- Test all variable substitutions

**Validation**: Manually render template and verify all files

### 6. Implement Post-Generation Hook

**Duration**: 30-45 minutes

**Create** `hooks/post_gen_project.py`:

```python
"""Post-generation setup for my-template."""
import os
import shutil
import subprocess


def remove_optional_files():
    """Remove files for disabled features."""
    enable_security = '{{ cookiecutter.enable_security_gates }}'

    if enable_security != 'yes':
        files_to_remove = [
            '.github/workflows/security.yml',
            'SECURITY.md',
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                print(f"✓ Removed {file}")


def init_git_repo():
    """Initialize git repository."""
    try:
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit from template'],
            check=True,
            capture_output=True
        )
        print("✓ Git repository initialized")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Git initialization failed: {e}")


def install_dependencies():
    """Install project dependencies."""
    # Language-specific installation
    # e.g., npm install, pip install -e .[dev], go mod download
    pass


def print_next_steps():
    """Display next steps for user."""
    project_slug = '{{ cookiecutter.project_slug }}'

    print("\n" + "="*60)
    print(f"✓ Project '{project_slug}' created successfully!")
    print("="*60)
    print("\nNext steps:")
    print(f"  1. cd {project_slug}")
    print("  2. Review README.md for setup instructions")
    print("  3. Install dependencies")
    print("  4. Run tests to verify setup")
    print("  5. Push to GitHub and enable workflows")
    print("\nHappy coding! 🚀")


def main():
    """Run post-generation tasks."""
    remove_optional_files()
    init_git_repo()
    print_next_steps()


if __name__ == '__main__':
    main()
```

**Validation**: Hook executes without errors

### 7. Create Template Tests

**Duration**: 1-2 hours

**Add test to** `tests/test_cookiecutters.py`:

```python
def test_my_template_bakes(cookies):
    """Test that my-template renders successfully."""
    result = cookies.bake(
        extra_context={
            "project_name": "Demo Project",
            "project_slug": "demo-project",
            "description": "A demo project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "license": "MIT",
            "enable_security_gates": "yes",
            "ci_provider": "github",
        },
        template="templates/my-template"
    )

    # Verify successful generation
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()

    # Verify essential files exist
    assert (result.project_path / "README.md").exists()
    assert (result.project_path / "src").exists()
    assert (result.project_path / "tests").exists()
    assert (result.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_my_template_minimal(cookies):
    """Test my-template with minimal options."""
    result = cookies.bake(
        extra_context={
            "project_name": "Minimal Project",
            "project_slug": "minimal-project",
            "enable_security_gates": "no",
        },
        template="templates/my-template"
    )

    assert result.exception is None
    assert result.exit_code == 0

    # Security files should not exist
    assert not (result.project_path / ".github" / "workflows" / "security.yml").exists()


def test_my_template_invalid_slug(cookies):
    """Test that invalid project_slug is rejected."""
    result = cookies.bake(
        extra_context={
            "project_slug": "Invalid_Slug",
        },
        template="templates/my-template"
    )

    # Should fail validation
    assert result.exit_code != 0
```

**Run Tests**:

```bash
pytest tests/test_cookiecutters.py::test_my_template_bakes -v
```

**Validation**: All tests pass

### 8. Test Manual Generation

**Duration**: 30 minutes

**Commands**:

```bash
# Test template generation
cookiecutter templates/my-template

# Follow prompts and verify output
cd <generated-project>

# Test the generated project
# Run build
[language-specific build command]

# Run tests
[language-specific test command]

# Run linter
[language-specific lint command]
```

**Validation Checklist**:

- [ ] Template generates without errors
- [ ] All files are created correctly
- [ ] Variables are substituted properly
- [ ] Build succeeds
- [ ] Tests pass
- [ ] Linter runs clean
- [ ] Git repository initialized
- [ ] Documentation is accurate

### 9. Create Template Documentation

**Duration**: 1 hour

**Create** `templates/my-template/README.md`:

````markdown
# My Template

Description of what this template generates.

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

```bash
cookiecutter templates/my-template
```
````

## Template Variables

| Variable     | Description       | Default    | Options               |
| ------------ | ----------------- | ---------- | --------------------- |
| project_name | Project name      | My Project | Any string            |
| project_slug | URL-friendly name | (computed) | lowercase-kebab-case  |
| license      | License type      | MIT        | MIT, Apache-2.0, etc. |

## Generated Project Structure

```
project-name/
├── src/          # Source code
├── tests/        # Tests
├── .github/      # CI/CD workflows
└── README.md     # Documentation
```

## Optional Features

### Security Gates

Enable with `enable_security_gates: yes`

- CodeQL analysis
- Secret scanning
- Dependency review

## Next Steps

After generation:

1. Review README.md
2. Install dependencies
3. Run tests
4. Push to GitHub

## Examples

See `examples/my-template/` for complete example projects.

````

**Validation**: Documentation is clear and complete

### 10. Update Repository Documentation

**Duration**: 30 minutes

**Update** `README.md`:
- Add template to list of available templates
- Update feature matrix
- Add usage example

**Update** `TASKS.md`:
- Mark template as complete
- Update implementation status

**Update** `CHANGELOG.md`:
- Add entry for new template

**Validation**: All documentation updated

### 11. Submit Pull Request

**Duration**: 15 minutes

**Commands**:

```bash
# Create branch
git checkout -b feat/add-my-template

# Stage changes
git add templates/my-template/
git add tests/test_cookiecutters.py
git add README.md TASKS.md CHANGELOG.md

# Commit
git commit -m "feat: add my-template for [technology]

- Complete Cookiecutter template
- Pre/post generation hooks
- Comprehensive tests
- Documentation
"

# Push
git push origin feat/add-my-template

# Create PR
gh pr create \
  --title "feat: add my-template for [technology]" \
  --body "Adds new Cookiecutter template for [technology]..."
````

**Validation**: PR created, CI passes

## Troubleshooting

### Template Generation Fails

**Symptom**: `cookiecutter` command errors
**Cause**: Invalid JSON or Jinja2 syntax
**Solution**:

```bash
# Validate JSON
python -m json.tool templates/my-template/cookiecutter.json

# Check Jinja2 syntax
cookiecutter templates/my-template --no-input
```

### Tests Fail

**Symptom**: pytest fails with template errors
**Cause**: Missing files or incorrect paths
**Solution**:

```bash
# Run with verbose output
pytest tests/test_cookiecutters.py::test_my_template_bakes -vv

# Check generated project
ls -la /tmp/pytest-of-*/pytest-*/test_my_template_bakes*/
```

### GitHub Actions Syntax Errors

**Symptom**: Workflow files have syntax errors
**Cause**: Jinja2 conflicts with `${{ }}` syntax
**Solution**: Use `{% raw %}` blocks:

```yaml
{% raw %}
env:
  VERSION: ${{ github.ref }}
{% endraw %}
```

### Hook Execution Fails

**Symptom**: Pre or post hooks error
**Cause**: Python syntax or logic errors
**Solution**:

```bash
# Test hook manually
cd templates/my-template/hooks
python pre_gen_project.py
```

## Rollback

If something goes wrong:

```bash
# Discard changes
git checkout main
git branch -D feat/add-my-template

# Clean up test artifacts
rm -rf /tmp/pytest-of-*
```

## Validation Checklist

- [ ] Template generates successfully
- [ ] All tests pass
- [ ] Generated project builds
- [ ] Generated project tests pass
- [ ] Hooks execute without errors
- [ ] Documentation is complete
- [ ] Code review completed
- [ ] CI/CD workflows pass
- [ ] Template follows conventions
- [ ] Optional features work correctly

## References

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/en/3.1.x/templates/)
- [pytest-cookies Documentation](https://pytest-cookies.readthedocs.io/)
- [Existing Templates](../templates/)
- [ADR-001: Cookiecutter Multi-Template](../docs/adr/ADR-001-cookiecutter-multi-template.md)

## Success Criteria

✅ Template generates valid projects
✅ All tests pass consistently
✅ Documentation is comprehensive
✅ Code follows project conventions
✅ CI/CD integration works
✅ Community feedback positive

---

_For questions or issues, open a GitHub issue or discussion._

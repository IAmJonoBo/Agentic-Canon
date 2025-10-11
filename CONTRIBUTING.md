# Contributing Guide

## Welcome! 🎉

Thank you for considering contributing to Agentic Canon. This guide will help you get started with contributing to the framework itself.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Quality Standards](#quality-standards)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and constructive
- Focus on what's best for the community
- Show empathy towards others
- Accept constructive criticism gracefully

## Getting Started

### Prerequisites
- Git
- Python 3.11+
- pip or conda for package management
- Node.js 18+ (for testing Node templates)
- Go 1.21+ (for testing Go templates)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/IAmJonoBo/Agentic-Canon.git
cd Agentic-Canon

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest -v
```

### Repository Structure

```
Agentic-Canon/
├── .github/              # GitHub workflows and templates
├── docs/                 # Jupyter Book documentation
│   ├── _config.yml      # Jupyter Book configuration
│   ├── _toc.yml         # Table of contents
│   └── notebooks/       # MyST markdown mirrors
├── notebooks/           # Interactive executable notebooks
├── templates/           # Cookiecutter templates
│   ├── python-service/
│   ├── node-service/
│   ├── react-webapp/
│   ├── go-service/
│   └── docs-only/
├── tests/               # Test files
├── examples/            # Example projects and configurations
├── runbooks/            # Agent runbooks
├── binder/              # Binder environment
└── README.md
```

## Development Process

### 1. Branch Strategy

We use **trunk-based development**:
- `main` - Production-ready code
- Feature branches from `main`: `feature/description` or `copilot/description`
- Bug fixes: `fix/description`
- Hotfixes: `hotfix/description`

### 2. Creating a Branch

```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Making Changes

Follow these guidelines:

#### Code Style
- **Python**: Follow PEP 8, use Black for formatting, Ruff for linting
- **TypeScript/JavaScript**: Use ESLint and Prettier
- **Go**: Use gofmt and golangci-lint
- **Markdown**: Use markdownlint for consistency
- **Notebooks**: Use Jupytext for version control, strip outputs with nbstripout

#### Commit Messages
Use [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(templates): add Rust service template
fix(notebooks): correct SBOM generation example
docs(readme): update installation instructions
```

#### Tests
- Write tests for all new features
- Maintain minimum 80% coverage
- All tests must pass: `pytest -v`
- Test template rendering: `pytest tests/test_cookiecutters.py -v`
- Test notebooks execution: `pytest --nbmake notebooks/**/*.ipynb`

## Quality Standards

All contributions must meet these standards:

### Security
- ✅ No secrets in code
- ✅ SAST scan passes (CodeQL/Semgrep)
- ✅ Dependency scan clean
- ✅ No high/critical vulnerabilities

### Code Quality
- ✅ Linter passes
- ✅ Pre-commit hooks pass
- ✅ Code coverage ≥ 80%
- ✅ No code smells introduced

### Documentation
- ✅ Public APIs documented
- ✅ README updated (if needed)
- ✅ ADR created for significant decisions
- ✅ CHANGELOG updated
- ✅ Notebooks are executable and outputs stripped

### Templates
- ✅ Must render successfully with pytest-cookies
- ✅ Include complete CI/CD workflows
- ✅ Security scanning configured
- ✅ Quality gates implemented
- ✅ Documentation included

## Submitting Changes

### 1. Pull Request Process

```bash
# Ensure all tests pass
pytest -v

# Ensure pre-commit hooks pass
pre-commit run --all-files

# Push your branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### 2. PR Requirements

- [ ] Title follows conventional commit format
- [ ] Description explains what and why
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No merge conflicts
- [ ] CI checks pass
- [ ] At least one approval

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Template rendering tests pass
- [ ] Notebooks execute successfully

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added
- [ ] CHANGELOG updated
```

## Review Process

### 1. Automated Checks
- Notebooks test (nbmake)
- Cookiecutter templates test
- Jupyter Book build
- Pre-commit hooks
- CodeQL security scanning

### 2. Code Review
- At least one maintainer approval required
- Focus on:
  - Correctness and functionality
  - Security implications
  - Code clarity and maintainability
  - Test coverage
  - Documentation completeness

### 3. Response Times
- **Initial Review**: Within 3 business days
- **Follow-up Reviews**: Within 2 business days
- **Merge**: After approval and CI passes

### 4. Review Criteria
- ✅ Solves the stated problem
- ✅ Minimal, focused changes
- ✅ Well-tested
- ✅ Properly documented
- ✅ No regressions
- ✅ Follows project conventions

## Advanced Topics

### Working with Notebooks
```bash
# Create Jupytext pair for new notebook
jupytext --set-formats ipynb,md:myst notebooks/new_notebook.ipynb

# Sync changes between formats
jupytext --sync notebooks/*.ipynb

# Execute notebook with Papermill
papermill notebooks/01_bootstrap.ipynb output.ipynb -p run_mode ci
```

### Working with Templates
```bash
# Test template rendering
cookiecutter templates/python-service --no-input

# Run template tests
pytest tests/test_cookiecutters.py::test_python_service -v

# Validate all templates
./validate-templates.sh
```

### Building Documentation
```bash
# Build Jupyter Book
jupyter-book build docs

# Clean build
jupyter-book clean docs
jupyter-book build docs

# View locally
open docs/_build/html/index.html
```

## Release Process

### 1. Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 2. Release Checklist
- [ ] All tests pass
- [ ] CHANGELOG.md updated
- [ ] Version bumped in appropriate files
- [ ] Documentation updated
- [ ] Tag created: `git tag -a v1.2.3 -m "Release v1.2.3"`
- [ ] Tag pushed: `git push origin v1.2.3`
- [ ] GitHub release created with notes

### 3. Release Notes
Include:
- New features
- Bug fixes
- Breaking changes
- Deprecations
- Migration guide (if needed)

## Getting Help

- **Questions**: Open a [discussion](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
- **Bugs**: Create an [issue](https://github.com/IAmJonoBo/Agentic-Canon/issues)
- **Security**: Email security@agentic-canon.org or use [GitHub Security Advisories](https://github.com/IAmJonoBo/Agentic-Canon/security/advisories)

## Resources

### Documentation
- [README](README.md) - Project overview
- [BIBLE.md](BIBLE.md) - AI-friendly reference
- [INDEX.md](INDEX.md) - Navigation guide
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Technical implementation details
- [TASKS.md](TASKS.md) - Implementation roadmap
- [Security Policy](SECURITY.md)

### Tools
- **Linter**: Ruff (Python), ESLint (JS/TS), golangci-lint (Go)
- **Formatter**: Black (Python), Prettier (JS/TS), gofmt (Go)
- **Test Framework**: pytest (Python), Vitest (Node), go test (Go)
- **Build Tool**: Cookiecutter, Jupyter Book, GitHub Actions

### External
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [Jupyter Book Documentation](https://jupyterbook.org/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)

## Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- GitHub contributors page
- Annual contributor report
- Special acknowledgments for significant contributions

## License

By contributing, you agree that your contributions will be licensed under Apache-2.0.

---

Thank you for contributing to Agentic Canon! 🚀

*This guide implements frontier software excellence practices including NIST SSDF, OWASP SAMM, and DORA metrics.*

# Contributing Guide

## Welcome! 🎉

Thank you for considering contributing to Agentic Canon. This guide will help you get started with contributing to this comprehensive framework for frontier software excellence.

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

For details, see our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Git
- Python 3.11+
- pip or conda for Python package management
- Access to GitHub (for PRs and issues)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/IAmJonoBo/Agentic-Canon.git
cd Agentic-Canon

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# Run sanity check to verify current state
.dev/sanity-check.sh

# Run tests to verify setup
pytest tests/
```

### Understanding Project State

Before contributing, understand the current project state:

1. **Read the Progress Tracker:**
   - [TASKS.md](TASKS.md) - 📍 Single source of truth for all progress
   - [SUMMARY.md](SUMMARY.md) - Executive summary derived from TASKS.md
   - [IMPLEMENTATION.md](IMPLEMENTATION.md) - Technical decisions and handover guide

2. **Review Process Guides:**
   - [docs/adr/ADR-LIFECYCLE.md](docs/adr/ADR-LIFECYCLE.md) - How to create and manage ADRs
   - [docs/ISSUE_MANAGEMENT.md](docs/ISSUE_MANAGEMENT.md) - Issue creation and sprint management
   - [.github/LABELS.md](.github/LABELS.md) - Label taxonomy and usage

3. **Verify Current State:**

   ```bash
   # Run comprehensive sanity check
   .dev/sanity-check.sh

   # Current status (2025-10-12):
   # ✅ 44 checks passed
   # ⚠️ 2 warnings (Azure/GCP multi-cloud pending)
   # ❌ 0 failures
   ```

4. **Test Templates:**

   ```bash
   # Run template tests
   pytest tests/test_cookiecutters.py -v

   # Generate a test project
   cookiecutter templates/python-service
   ```

**⚠️ Important:** Documentation may lag behind implementation. Always:

- Run `.dev/sanity-check.sh` to verify ground truth
- Check actual file existence, not just documentation
- Run tests to confirm functionality

### Repository Structure

```
Agentic-Canon/
├── .github/          # GitHub workflows and templates
├── docs/             # Jupyter Book documentation
│   ├── notebooks/   # MyST markdown mirrors
│   └── _config.yml  # Jupyter Book configuration
├── notebooks/        # Executable Jupyter notebooks
├── templates/        # Cookiecutter templates
│   ├── python-service/
│   ├── node-service/
│   ├── react-webapp/
│   ├── go-service/
│   └── docs-only/
├── examples/         # Example configurations and projects
├── runbooks/         # Operational runbooks
├── tests/           # Test files
└── README.md
```

## Development Process

### 1. Branch Strategy

We use **trunk-based development**:

- `main` - Production-ready code
- Feature branches from `main`: `feature/description` or `fix/description`
- All PRs merge back to `main`

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

- For Python: Follow PEP 8 guidelines
- For JavaScript/TypeScript: Follow standard.js or the project's ESLint config
- For Markdown: Use consistent formatting
- Run formatters before committing

#### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:

```
feat(templates): add Rust service template

Implements a new Cookiecutter template for Rust services with:
- Cargo configuration
- CI/CD workflows
- Basic project structure

Closes #123
```

#### Tests

- Write tests for new features when applicable
- Ensure all existing tests pass
- For templates: Use pytest-cookies to test template rendering
- For notebooks: Ensure notebooks execute without errors

## Quality Standards

All contributions must meet the Agentic Canon quality standards. See our comprehensive framework:

- **[FRAMEWORK.md](FRAMEWORK.md)** - Overall framework and philosophy
- **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - Detailed quality requirements
- **[CONVENTIONS.md](CONVENTIONS.md)** - Development conventions

### Quick Checklist

All contributions should meet these standards:

#### For Code Changes

- ✅ Tests added/updated (80%+ coverage)
- ✅ Linting passes
- ✅ Type hints included (Python/TypeScript)
- ✅ Security scanning clean
- ✅ Documentation updated

### Documentation

- ✅ Public APIs and functions documented
- ✅ README updated if needed
- ✅ ADR created for significant architectural decisions (see [ADR Lifecycle](docs/adr/ADR-LIFECYCLE.md))
- ✅ CHANGELOG updated for user-facing changes
- ✅ Examples added for new features
- ✅ TASKS.md updated if tracking items

### Architecture Decisions

For **significant architectural decisions**, create an ADR:

1. **Determine if ADR is needed:**
   - Technology or framework choices
   - Design patterns or architecture changes
   - Infrastructure decisions
   - API design choices

2. **Create the ADR:**

   ```bash
   # Use the automated script
   .dev/scripts/create-adr.sh

   # Or manually
   cp templates/architecture/adr/template.md docs/adr/ADR-009-your-decision.md
   ```

3. **Follow the lifecycle:**
   - Propose → Review → Accept → Implement
   - See [ADR Lifecycle Guide](docs/adr/ADR-LIFECYCLE.md) for details

4. **Link the ADR:**
   - Reference in issues/PRs: "Implements ADR-009"
   - Update docs/adr/README.md
   - Link from TASKS.md if applicable

### Issues and Tasks

Use the appropriate issue template:

- **Bug Report** - For defects or unexpected behavior
- **Feature Request** - For new functionality or enhancements
- **Task** - For concrete work items
- **ADR Proposal** - For architectural decisions

See [Issue Management Guide](docs/ISSUE_MANAGEMENT.md) for best practices on:

- Creating well-formed issues
- Labeling and categorization
- Sprint planning
- Tracking progress

### Code Quality

- ✅ Code follows project conventions (see [CONVENTIONS.md](CONVENTIONS.md))
- ✅ No obvious code smells
- ✅ Appropriate error handling
- ✅ Clear variable and function names
- ✅ Type hints/annotations included (Python/TypeScript)

### Testing

- ✅ Tests added/updated for changes
- ✅ Code coverage maintained (≥80%)
- ✅ All tests pass locally
- ✅ No flaky tests introduced

### Security

- ✅ No secrets in code
- ✅ Input validation where appropriate
- ✅ Dependencies reviewed and approved
- ✅ Security best practices followed

### Templates

- ✅ Template renders successfully with pytest-cookies
- ✅ Generated project structure is valid
- ✅ CI/CD workflows included
- ✅ Documentation included
- ✅ All quality gates pass in generated project

## Submitting Changes

### 1. Before Submitting

Run validation:

```bash
# Format code (if applicable)
# For Python:
black .
isort .

# Run tests
pytest tests/

# Test template rendering
pytest tests/test_cookiecutters.py

# Test notebooks (if modified)
pytest --nbmake notebooks/*.ipynb
```

### 2. Push Changes

```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to GitHub and create a Pull Request
2. Fill out the PR template with:
   - Clear description of changes
   - Type of change (bug fix, feature, docs, etc.)
   - Checklist of completed items
   - Related issues
3. Request reviewers
4. Respond to feedback

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Template update
- [ ] Breaking change

## Checklist

- [ ] Tests added/updated (if applicable)
- [ ] Documentation updated
- [ ] Changelog updated (for user-facing changes)
- [ ] All tests passing
- [ ] Self-review completed
- [ ] Code follows style guidelines

## Testing

How was this tested?

## Related Issues

Closes #
```

## Review Process

### What Reviewers Check

1. **Functionality**
   - Does it work as intended?
   - Edge cases handled?
   - Error handling appropriate?

2. **Code Quality**
   - Follows style guide?
   - Well-structured and readable?
   - Appropriate abstractions?

3. **Documentation**
   - Code is documented?
   - README updated if needed?
   - Examples provided?

4. **Templates** (if applicable)
   - Template renders correctly?
   - Generated structure is valid?
   - CI/CD workflows work?

### Review Timeline

- **Initial Review**: Within 3-5 business days
- **Follow-up**: Within 1-2 business days
- **Approval**: 1-2 approvals typically required
- **Merge**: After all checks pass

### Addressing Feedback

1. Read feedback carefully
2. Ask questions if unclear
3. Make requested changes
4. Push updates to same branch
5. Respond to comments
6. Request re-review

## Advanced Topics

### Architecture Decision Records (ADR)

For significant architectural decisions, create an ADR in `docs/adr/`:

```bash
# Use the template
cp docs/adr/template.md docs/adr/NNN-decision-title.md
# Edit with your decision details
```

### Adding New Templates

1. Create template directory in `templates/`
2. Add `cookiecutter.json` with variables
3. Add hooks for validation and setup
4. Create template structure
5. Add tests in `tests/test_cookiecutters.py`
6. Document in README.md

### Contributing to Examples

1. Add example in appropriate `examples/` subdirectory
2. Include comprehensive README
3. Ensure example is complete and working
4. Add references in main documentation

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
- **Bugs**: Create an [Issue](https://github.com/IAmJonoBo/Agentic-Canon/issues)
- **Security**: See [SECURITY.md](SECURITY.md)

## Resources

### Documentation

- [README](README.md) - Project overview
- [TASKS.md](TASKS.md) - Implementation tracking
- [Agentic_Canon.md](Agentic_Canon.md) - Complete playbook
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Technical implementation details

### Tools

- Cookiecutter - Template generation
- Jupytext - Notebook version control
- Jupyter Book - Documentation publishing
- pytest-cookies - Template testing

### External

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)

## Recognition

Contributors are recognized in:

- CHANGELOG.md for significant contributions
- GitHub contributors page
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

---

Thank you for contributing to Agentic Canon! 🚀

_This project implements frontier software excellence practices including NIST SSDF, OWASP SAMM, SLSA, and other industry best practices._

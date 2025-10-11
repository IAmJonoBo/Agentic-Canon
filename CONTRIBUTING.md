# Contributing to Agentic Canon

## Welcome! 🎉

Thank you for considering contributing to Agentic Canon. This guide will help you get started with contributing to our frontier software excellence framework.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Quality Standards](#quality-standards)
- [Submitting Changes](#submitting-changes)
- [Areas for Contribution](#areas-for-contribution)
- [Review Process](#review-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:
- Be respectful and constructive in all interactions
- Focus on what's best for the community
- Show empathy towards other community members
- Accept constructive criticism gracefully
- Prioritize the success of the overall project

## Getting Started

### Prerequisites
- Git
- Python 3.8+
- pip or conda
- Jupyter
- Cookiecutter
- (Optional) Node.js 18+ for Node/React templates
- (Optional) Go 1.19+ for Go templates

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
pytest tests/ --nbmake notebooks/
```

### Repository Structure

```
Agentic-Canon/
├── .github/          # GitHub Actions workflows
├── docs/             # Jupyter Book documentation
├── notebooks/        # Executable Jupyter notebooks
├── templates/        # Cookiecutter templates
│   ├── python-service/
│   ├── node-service/
│   ├── react-webapp/
│   ├── go-service/
│   ├── docs-only/
│   └── [template subdirectories]/
├── examples/         # Example implementations
├── tests/            # Template and notebook tests
├── BIBLE.md          # AI-friendly implementation reference
├── INDEX.md          # Complete navigation guide
└── TASKS.md          # Active progress tracker
```

## Development Process

### 1. Branch Strategy

We use **trunk-based development**:
- `main` - Production-ready code
- Feature branches from `main`: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`

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
- Run linter before committing: `trunk check`
- Use Black formatter for Python: `black .`
- Follow language-specific style guides

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
- `template`: Template changes
- `notebook`: Notebook changes

Example:
```
feat(templates): add Rust service template

Implements a new Cookiecutter template for Rust services with:
- Cargo configuration
- CI/CD pipeline
- Security scanning
- Documentation setup

Closes #123
```

#### Tests
- Write tests for all template changes
- Test template rendering: `pytest tests/test_cookiecutters.py`
- Test notebooks: `pytest --nbmake notebooks/`
- Ensure all CI checks pass

## Quality Standards

All contributions must meet these standards:

### Security
- ✅ No secrets in code
- ✅ Templates include security scanning
- ✅ SBOM generation in templates
- ✅ No high/critical vulnerabilities

### Code Quality
- ✅ Templates render successfully
- ✅ Generated projects build correctly
- ✅ Notebooks execute without errors
- ✅ Documentation is clear and complete

### Template Quality
- ✅ Includes comprehensive README
- ✅ Has validation hooks
- ✅ Includes example tests
- ✅ Follows established patterns
- ✅ CI/CD pipeline included

### Documentation
- ✅ Templates documented in INDEX.md
- ✅ README updated if needed
- ✅ TASKS.md updated for progress tracking
- ✅ Examples provided

## Submitting Changes

### 1. Before Submitting

Run full validation:
```bash
# Format code
black .

# Run linter
trunk check

# Test templates
pytest tests/test_cookiecutters.py

# Test notebooks
pytest --nbmake notebooks/

# Validate templates
./validate-templates.sh
```

### 2. Push Changes

```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to GitHub and create a Pull Request
2. Fill out the PR template
3. Link related issues
4. Add appropriate labels
5. Request reviewers

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] TASKS.md updated
- [ ] All CI checks passing
- [ ] Self-review completed
- [ ] Code follows style guidelines
- [ ] No breaking changes (or documented)

## Areas for Contribution

We welcome contributions in these areas:

### 1. New Templates
- Additional programming languages (Rust, Java, C#, Ruby, PHP, etc.)
- Framework-specific templates (Django, Rails, Spring Boot, Laravel, etc.)
- Domain-specific templates (ML/AI, IoT, blockchain, gaming, etc.)
- Infrastructure templates (Kubernetes operators, Helm charts, Terraform modules)

See [examples/community/CONTRIBUTING-TEMPLATES.md](examples/community/CONTRIBUTING-TEMPLATES.md) for detailed template contribution guidelines.

### 2. Enhanced Dashboards
- Additional Grafana dashboards
- Prometheus alerting rules
- OpenTelemetry configurations
- SLO/SLI definitions

### 3. Examples and Tutorials
- Real-world example projects
- Step-by-step tutorials
- Video tutorial scripts
- Use case demonstrations

### 4. Documentation Improvements
- Clarifying existing documentation
- Adding missing documentation
- Improving navigation
- Creating diagrams and visualizations

### 5. Bug Fixes
- Template rendering issues
- Documentation errors
- Workflow failures
- Broken links

### 6. Cloud Integrations
- AWS-specific templates and workflows
- Azure-specific templates and workflows
- GCP-specific templates and workflows
- Multi-cloud orchestration

## Review Process

### What Reviewers Check

1. **Functionality**
   - Templates render correctly?
   - Generated projects work?
   - Notebooks execute successfully?

2. **Quality**
   - Follows established patterns?
   - Code is well-structured?
   - Documentation is complete?

3. **Completeness**
   - Tests included?
   - Examples provided?
   - Edge cases considered?

4. **Compliance**
   - Follows security standards?
   - Meets quality gates?
   - License compatible?

### Review Timeline

- **Initial Review**: Within 2-3 business days
- **Follow-up**: Within 1-2 business days
- **Approval**: 1-2 approvals required (depending on scope)
- **Merge**: After all checks pass

### Addressing Feedback

1. Read feedback carefully
2. Ask clarifying questions if needed
3. Make requested changes
4. Push updates to the same branch
5. Respond to comments
6. Request re-review when ready

## Advanced Topics

### Creating New Templates

1. Review existing templates for patterns
2. Use Cookiecutter best practices
3. Include validation hooks (pre_gen_project.py, post_gen_project.py)
4. Add comprehensive tests
5. Document in templates/README.md and INDEX.md

### Architecture Decision Records (ADR)

For significant architectural decisions:
```bash
# Create new ADR in templates/architecture/adr/
cp templates/architecture/adr/template.md docs/adr/NNN-decision-title.md
```

### Testing Templates

```bash
# Test single template
pytest tests/test_cookiecutters.py::test_python_service

# Test all templates
pytest tests/test_cookiecutters.py

# Test notebooks
pytest --nbmake notebooks/
```

### Building Documentation

```bash
# Build Jupyter Book locally
jupyter-book build docs/

# View in browser
open docs/_build/html/index.html
```

## Release Process

Releases are managed by maintainers:

1. Version bump following SemVer
2. Update CHANGELOG.md
3. Create release tag
4. Generate release notes
5. Publish to GitHub
6. Update documentation site

## Getting Help

- **Questions**: Start a [GitHub Discussion](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
- **Bugs**: Create an [Issue](https://github.com/IAmJonoBo/Agentic-Canon/issues)
- **Security**: See [SECURITY.md](SECURITY.md)
- **General**: Check [BIBLE.md](BIBLE.md) and [INDEX.md](INDEX.md)

## Resources

### Documentation
- [README](README.md) - Project overview
- [BIBLE.md](BIBLE.md) - AI-friendly implementation guide
- [INDEX.md](INDEX.md) - Complete navigation
- [TASKS.md](TASKS.md) - Progress tracker
- [Red Team + Software Excellence.md](Red%20Team%20+%20Software%20Excellence.md) - Comprehensive playbook

### Standards
- [NIST SSDF v1.1](https://csrc.nist.gov/Projects/ssdf)
- [OWASP SAMM](https://owaspsamm.org/)
- [SLSA](https://slsa.dev/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md
- Project documentation
- Community highlights

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

---

Thank you for contributing to Agentic Canon! 🚀

*This guide implements frontier software excellence practices following NIST SSDF, OWASP SAMM, and DORA metrics.*

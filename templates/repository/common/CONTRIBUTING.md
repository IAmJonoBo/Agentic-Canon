# Contributing Guide

## Welcome! 🎉

Thank you for considering contributing to {{ PROJECT_NAME }}. This guide will help you get started.

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
- {{ LANGUAGE }} {{ MIN_VERSION }}+
- {{ PACKAGE_MANAGER }}
- Access to required tools (see README.md)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/{{ ORG }}/{{ REPO }}.git
cd {{ REPO }}

# Install dependencies
{{ INSTALL_COMMAND }}

# Setup pre-commit hooks
{{ HOOK_SETUP_COMMAND }}

# Run tests to verify setup
{{ TEST_COMMAND }}
```

### Repository Structure

```
{{ REPO }}/
├── .github/          # GitHub workflows and templates
├── docs/             # Documentation
│   ├── adr/         # Architecture Decision Records
│   └── c4/          # C4 diagrams
├── src/             # Source code
├── tests/           # Test files
└── README.md
```

## Development Process

### 1. Branch Strategy

We use **trunk-based development**:

- `main` - Production-ready code
- `develop` - Integration branch (if needed)
- Feature branches from `main`: `feature/description`
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

- Run linter before committing: `{{ LINT_COMMAND }}`
- Use formatter: `{{ FORMAT_COMMAND }}`
- Follow {{ STYLE_GUIDE }}

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
feat(auth): add OAuth2 authentication

Implements OAuth2 flow with support for Google and GitHub providers.
Includes token refresh and revocation.

Closes #123
```

#### Tests

- Write tests for all new features
- Maintain minimum {{ COVERAGE_THRESHOLD }}% coverage
- All tests must pass: `{{ TEST_COMMAND }}`
- Run mutation tests: `{{ MUTATION_COMMAND }}`

## Quality Standards

All contributions must meet these standards:

### Security

- ✅ No secrets in code
- ✅ SAST scan passes (CodeQL/Semgrep)
- ✅ Dependency scan clean
- ✅ No high/critical vulnerabilities

### Code Quality

- ✅ Linter passes
- ✅ Code coverage ≥ {{ COVERAGE_THRESHOLD }}%
- ✅ Mutation score ≥ {{ MUTATION_THRESHOLD }}%
- ✅ SonarQube quality gate passes
- ✅ No code smells introduced

### Performance

- ✅ Performance budgets met
- ✅ No regressions in benchmarks
- ✅ Core Web Vitals maintained (web apps)

### Accessibility

- ✅ WCAG 2.2 AA compliant
- ✅ axe-core tests pass
- ✅ Keyboard navigation works

### Documentation

- ✅ Public APIs documented
- ✅ README updated (if needed)
- ✅ ADR created for significant decisions
- ✅ CHANGELOG updated

## Submitting Changes

### 1. Before Submitting

Run full validation:

```bash
# Lint and format
{{ LINT_COMMAND }}
{{ FORMAT_COMMAND }}

# Run all tests
{{ TEST_COMMAND }}

# Run security scans locally
{{ SECURITY_SCAN_COMMAND }}

# Build
{{ BUILD_COMMAND }}
```

### 2. Push Changes

```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to GitHub and create a Pull Request
2. Use the PR template
3. Link related issues
4. Add labels (bug, feature, documentation, etc.)
5. Request reviewers

### PR Template

Your PR should include:

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] All CI checks passing
- [ ] Self-review completed
- [ ] Code follows style guidelines

## Testing

How was this tested?

## Screenshots (if applicable)

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

3. **Tests**
   - Adequate coverage?
   - Tests are meaningful?
   - Edge cases tested?

4. **Security**
   - No vulnerabilities introduced?
   - Input validation present?
   - Authentication/authorization correct?

5. **Performance**
   - No performance regressions?
   - Efficient algorithms?
   - Resource usage acceptable?

6. **Documentation**
   - Code is documented?
   - README updated if needed?
   - API changes documented?

### Review Timeline

- **Initial Review**: Within 2 business days
- **Follow-up**: Within 1 business day
- **Approval**: 2 approvals required
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

For significant architectural decisions:

```bash
# Create new ADR
{{ ADR_CREATE_COMMAND }} "Decision title"

# Template location
docs/adr/template.md
```

### Contract Testing

For API changes:

```bash
# Run contract tests
{{ CONTRACT_TEST_COMMAND }}

# Publish contracts
{{ CONTRACT_PUBLISH_COMMAND }}
```

### Performance Testing

```bash
# Run benchmarks
{{ BENCHMARK_COMMAND }}

# Profile performance
{{ PROFILE_COMMAND }}
```

### Security Testing

```bash
# Run SAST
{{ SAST_COMMAND }}

# Run DAST
{{ DAST_COMMAND }}

# Check dependencies
{{ DEPENDENCY_CHECK_COMMAND }}
```

## Release Process

Releases are managed by maintainers:

1. Version bump (SemVer)
2. Update CHANGELOG
3. Create release tag
4. Generate SBOM
5. Sign artifacts
6. Create GitHub release
7. Deploy to production

## Getting Help

- **Questions**: Open a discussion
- **Bugs**: Create an issue
- **Security**: Email security@{{ DOMAIN }}
- **Chat**: Join {{ CHAT_PLATFORM }}

## Resources

### Documentation

- [README](README.md)
- [Architecture](docs/architecture/)
- [API Documentation](docs/api/)
- [Security Policy](SECURITY.md)

### Tools

- Linter: {{ LINTER }}
- Formatter: {{ FORMATTER }}
- Test Framework: {{ TEST_FRAMEWORK }}
- Build Tool: {{ BUILD_TOOL }}

### External

- [{{ STYLE_GUIDE }}]({{ STYLE_GUIDE_URL }})
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## Recognition

Contributors are recognized in:

- CHANGELOG.md
- GitHub contributors page
- Annual contributor report

## License

By contributing, you agree that your contributions will be licensed under {{ LICENSE }}.

---

Thank you for contributing to {{ PROJECT_NAME }}! 🚀

_This guide implements frontier software excellence practices including NIST SSDF, OWASP SAMM, and DORA metrics._

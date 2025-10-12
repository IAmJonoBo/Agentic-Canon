# GitHub Copilot Instructions for Agentic Canon

This repository implements **frontier software excellence** with comprehensive standards compliance and agent-friendly automation. When contributing to this repository, follow these guidelines to maintain consistency and quality.

## Project Context

**Agentic Canon** is a machine-readable, agent-friendly framework for fast, correct software scaffolding and delivery. It provides:

- 📓 Executable notebooks for bootstrapping, security, testing, observability, and documentation
- 🎨 Cookiecutter templates for Python, Node.js, React, Go, and documentation projects
- 🔄 Pre-configured CI/CD pipelines with security gates and SBOM generation
- ✅ Non-negotiable quality gates (80%+ coverage, mutation testing, security scanning)
- 📚 Jupyter Book integration for beautiful, searchable documentation

## Framework Documents (READ THESE FIRST!)

**Our comprehensive framework is documented in three core files:**

1. **[FRAMEWORK.md](../FRAMEWORK.md)** - Unified framework defining OUR approach to software excellence
   - Philosophy and principles
   - Framework architecture (4 layers)
   - Conformance requirements
   - Decision-making framework
   - Onboarding paths

2. **[QUALITY_STANDARDS.md](../QUALITY_STANDARDS.md)** - Comprehensive quality standards for ALL aspects of development
   - Non-negotiable quality gates
   - Code quality standards
   - Testing standards (unit, integration, E2E, mutation, contract)
   - Security standards (SAST, DAST, secrets, dependencies)
   - AI/LLM quality standards
   - Business logic quality
   - Orchestration quality
   - Documentation, performance, accessibility standards

3. **[CONVENTIONS.md](../CONVENTIONS.md)** - Development conventions and best practices
   - Code style conventions (Python, TypeScript, Go)
   - Naming conventions (files, variables, functions, classes)
   - Git conventions (branching, commits, PRs)
   - Documentation conventions
   - Testing conventions
   - Security conventions
   - API conventions (REST, GraphQL, gRPC)
   - Database conventions
   - Configuration conventions

**When in doubt, refer to these documents for guidance!**

## Standards Compliance

All code and templates must comply with:

- **NIST SSDF v1.1** - Secure Software Development Framework
- **OWASP SAMM & ASVS** - Software Assurance Maturity Model & Application Security Verification Standard
- **SLSA Level 3** - Supply-chain Levels for Software Artifacts
- **ISO/IEC 25010** - Software quality model
- **WCAG 2.2 AA** - Web Content Accessibility Guidelines (for web components)
- **OpenSSF Scorecard** - Security best practices

## Coding Standards

### Python

- **Style**: Follow PEP 8 guidelines strictly
- **Formatting**: Use Black (line length: 88 characters)
- **Linting**: Use Ruff for linting and import sorting
- **Type Hints**: Always include type hints for function parameters and return values
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Imports**: Sort with isort, group by standard library, third-party, and local
- **Configuration**: Use `pyproject.toml` for project configuration (not setup.py)

Example:
```python
from typing import Optional

def process_data(input_data: str, timeout: Optional[int] = None) -> dict[str, str]:
    """Process input data and return structured results.
    
    Args:
        input_data: Raw input string to process
        timeout: Optional timeout in seconds
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If input_data is empty
    """
    if not input_data:
        raise ValueError("input_data cannot be empty")
    return {"result": input_data.strip()}
```

### JavaScript/TypeScript

- **Style**: Follow standard.js or project's ESLint configuration
- **Formatting**: Use Prettier (2 spaces, single quotes, semicolons)
- **Type Safety**: Use TypeScript with strict mode enabled
- **Imports**: Use ES modules, not CommonJS
- **Configuration**: Use modern tooling (Vite, esbuild)

Example:
```typescript
interface ProcessOptions {
  timeout?: number;
  retries?: number;
}

export async function processData(
  inputData: string,
  options: ProcessOptions = {}
): Promise<Record<string, string>> {
  if (!inputData) {
    throw new Error('inputData cannot be empty');
  }
  return { result: inputData.trim() };
}
```

### Markdown

- Use **ATX-style headers** (`#` prefix)
- Use **fenced code blocks** with language identifiers
- **Line length**: Prefer 80-100 characters for readability
- Use **reference-style links** for repeated URLs
- Include **meaningful alt text** for images

## Testing Requirements

### Coverage Requirements

- **Unit tests**: Minimum 80% code coverage (enforced in CI)
- **Mutation testing**: Minimum 40% mutation score
- **Integration tests**: For all public APIs
- **E2E tests**: For user-facing workflows (where applicable)

### Python Testing

- Use **pytest** as the test framework
- Use **pytest-cov** for coverage reporting
- Use **mutmut** or **cosmic-ray** for mutation testing
- Name test files: `test_*.py` or `*_test.py`
- Structure: Mirror source structure in `tests/` directory

Example:
```python
import pytest
from myapp import process_data

def test_process_data_success():
    """Test process_data with valid input."""
    result = process_data("  test  ")
    assert result == {"result": "test"}

def test_process_data_empty_raises():
    """Test process_data raises on empty input."""
    with pytest.raises(ValueError, match="cannot be empty"):
        process_data("")
```

### JavaScript/TypeScript Testing

- Use **Jest** or **Vitest** as the test framework
- Use **Playwright** for E2E tests (React/web apps)
- Name test files: `*.test.ts` or `*.spec.ts`
- Include setup/teardown in `beforeEach`/`afterEach`

## Security Practices

### Secrets Management

- **Never** commit secrets, API keys, or credentials to git
- Use environment variables for all sensitive configuration
- Add `.env` files to `.gitignore`
- Use GitHub Secrets for CI/CD credentials
- Run **Gitleaks** on every commit (automated in pre-commit hooks)

### Dependency Security

- Pin dependency versions in lock files (`requirements.txt`, `package-lock.json`)
- Generate **SBOM** (Software Bill of Materials) for all builds using CycloneDX or SPDX
- Run **dependency scanning** in CI (Dependabot, Renovate)
- Address critical and high vulnerabilities immediately

### Code Security

- Run **SAST** (Static Application Security Testing) with CodeQL or Semgrep
- Validate and sanitize **all external inputs**
- Use **parameterized queries** for database operations
- Set secure defaults for cookies: `httpOnly`, `secure`, `sameSite: strict`
- Implement **zero-trust** architecture principles

### Build Security

- Use **SLSA Level 3** builds with signed provenance
- Sign all release artifacts
- Verify signatures before deployment
- Use reproducible builds where possible

## Documentation Requirements

### General Documentation

- Update **README.md** for user-facing changes
- Create **ADRs** (Architecture Decision Records) in `docs/adr/` for significant decisions
- Use the ADR template from `docs/adr/template.md`
- Update **CHANGELOG.md** following Keep a Changelog format
- Include **examples** for new features or templates

### Code Documentation

- Document all **public APIs** with clear descriptions, parameters, and return values
- Include **usage examples** in docstrings
- Keep documentation **synchronized** with code changes
- Use **MyST Markdown** for narrative documentation

### Jupyter Book

- All documentation builds with **Jupyter Book**
- Source files in `docs/` directory
- Configuration in `docs/_config.yml` and `docs/_toc.yml`
- Use **MyST Markdown** syntax for advanced features
- Auto-deploy to GitHub Pages on merge to main

## Notebook Guidelines

### Jupytext Pairing

- Use **Jupytext** to pair `.ipynb` ↔ `.md` (MyST format)
- Source notebooks in `notebooks/` directory
- MyST mirrors in `docs/notebooks/` for Jupyter Book
- Configuration in `jupytext.toml`:
  ```toml
  [formats]
  "notebooks/" = "ipynb"
  "docs/notebooks/" = "md:myst"
  ```

### Notebook Structure

- Include a **Parameters cell** tagged with `parameters` for Papermill:
  ```python
  # Parameters cell (tag: parameters)
  run_mode = "interactive"  # Options: interactive, ci, demo
  ```
- Use **clear section headers** with Markdown cells
- Keep notebooks **executable** from top to bottom
- Test notebooks in CI with `pytest --nbmake`

### Notebook Version Control

- **Never commit notebook outputs** to git
- Use **nbstripout** to strip outputs (configured in `.gitattributes`)
- Pre-commit hooks automatically sync Jupytext pairs
- Commit only `.md` files to version control when paired
- MyST markdown files are the source of truth for documentation

### Notebook CI/CD

- Execute notebooks in CI with **nbmake**: `pytest --nbmake notebooks/*.ipynb`
- Parameterize notebooks with **Papermill** for automation
- Schedule notebook runs with GitHub Actions cron
- Deploy notebook documentation with Jupyter Book

## Template Guidelines

### Cookiecutter Templates

- Templates in `templates/` directory
- Each template must have `cookiecutter.json` with variables
- Include **hooks** in `hooks/` for validation (`pre_gen_project.py`) and setup (`post_gen_project.py`)
- Template structure uses `{{cookiecutter.variable_name}}` syntax

### Generated Project Structure

All generated projects must include:

- **CI/CD workflows** in `.github/workflows/`:
  - `ci.yml` - Build, test, lint, coverage
  - `security.yml` - CodeQL, Gitleaks, dependency scanning, SBOM
  - `docs.yml` - Jupyter Book build and deployment (if applicable)
- **Pre-commit hooks** in `.pre-commit-config.yaml`
- **Quality gates** enforced in CI:
  - Tests passing
  - 80%+ code coverage
  - Linting/formatting passing
  - Security scans clean
  - SBOM generated
- **Documentation** with README, CONTRIBUTING, and LICENSE files
- **Security** with SECURITY.md and responsible disclosure process

### Template Testing

- Test templates with **pytest-cookies**
- Verify template renders successfully
- Verify generated project structure is valid
- Verify CI/CD workflows are functional
- Add tests in `tests/test_cookiecutters.py`

## Commit Message Format

Follow **Conventional Commits** specification:

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
- `security`: Security improvements
- `perf`: Performance improvements

Examples:
```
feat(templates): add Rust service template

Implements a new Cookiecutter template for Rust services with:
- Cargo configuration and workspace setup
- CI/CD workflows with security scanning
- Basic project structure with examples

Closes #123
```

```
fix(notebooks): correct Papermill parameter handling

Fixes parameter passing in scheduled notebook runs.
Ensures run_mode parameter is properly validated.

Fixes #456
```

## Quality Gates (Non-Negotiable)

All contributions must pass these gates:

### Build
- ✅ Code compiles/transpiles without errors
- ✅ Unit tests pass (green)
- ✅ Code coverage ≥ 80%
- ✅ Mutation score ≥ 40% (where applicable)

### Security
- ✅ No secrets in commits (Gitleaks)
- ✅ SAST critical issues = 0
- ✅ SBOM generated
- ✅ Provenance signed (for releases)

### Quality
- ✅ Code smells = 0 (SonarQube/equivalent)
- ✅ Code duplication ≤ 3%
- ✅ All linting rules pass
- ✅ Type checking passes (Python: mypy, TypeScript: tsc)

### Performance
- ✅ Core Web Vitals within budget (web apps)
- ✅ P95 latency ≤ threshold (services)

## File Structure

### Repository Layout

```
Agentic-Canon/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   └── copilot-instructions.md  # This file
├── docs/
│   ├── _config.yml         # Jupyter Book config
│   ├── _toc.yml            # Table of contents
│   ├── intro.md            # Documentation landing page
│   ├── adr/                # Architecture Decision Records
│   └── notebooks/          # MyST markdown mirrors
├── notebooks/              # Executable Jupyter notebooks
├── templates/              # Cookiecutter templates
│   ├── python-service/
│   ├── node-service/
│   ├── react-webapp/
│   ├── go-service/
│   └── docs-only/
├── examples/               # Example configurations
├── runbooks/               # Operational runbooks
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── jupytext.toml           # Jupytext configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md               # Project overview
```

## Branch Strategy

- **main** - Production-ready code, protected branch
- **Feature branches** - `feature/description` or `fix/description`
- Use **trunk-based development** - keep branches short-lived
- All PRs merge to main after review and CI passes

## Pre-commit Hooks

The repository uses pre-commit hooks for automated quality checks:

- **Black** - Python code formatting
- **Ruff** - Python linting
- **isort** - Python import sorting
- **mypy** - Python type checking
- **Jupytext** - Notebook synchronization
- **Gitleaks** - Secret scanning
- **prettier** - JavaScript/TypeScript/Markdown formatting (in templates)

Install hooks: `pre-commit install`

## Additional Context

### Key Reference Documents

- **BIBLE.md** - AI-friendly implementation reference with checklists and quality gates
- **INSTRUCTIONS.md** - Technical implementation details for notebooks and templates
- **CONTRIBUTING.md** - Contribution guidelines and workflow
- **control-traceability-matrix.json** - Machine-readable standards mapping
- **TASKS.md** - Single source of truth for implementation roadmap

### For AI Agents

- This repository is **agent-friendly** with machine-readable formats
- Use **control-traceability-matrix.json** for compliance requirements
- Execute **runbooks/agent-runbook.json** for automated workflows
- Templates support **autonomous generation** with validation hooks
- All quality gates are **automated** in CI/CD

### Example Workflows

1. **Adding a new template**: Create in `templates/`, add `cookiecutter.json`, write hooks, add tests
2. **Creating a notebook**: Use Jupytext pairing, add Parameters cell, test with nbmake
3. **Writing documentation**: Use MyST Markdown in `docs/`, update `_toc.yml`, build with Jupyter Book
4. **Adding a feature**: Create branch, write tests first, implement feature, update docs, open PR

---

## Quick Reference: Key Framework Documents

When working on Agentic Canon, reference these documents frequently:

- **[FRAMEWORK.md](../FRAMEWORK.md)** - Our philosophy, decision-making framework, and conformance requirements
- **[QUALITY_STANDARDS.md](../QUALITY_STANDARDS.md)** - All quality gates, testing standards, security requirements
- **[CONVENTIONS.md](../CONVENTIONS.md)** - Code style, naming, Git, documentation, API conventions
- **[BIBLE.md](../BIBLE.md)** - AI-friendly reference with implementation checklists
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute and get PRs merged

**Remember**: This repository implements frontier software excellence. All contributions should maintain or improve the high standards of security, quality, and reliability. **When in doubt, refer to FRAMEWORK.md, QUALITY_STANDARDS.md, or CONVENTIONS.md** or ask in a GitHub Discussion.

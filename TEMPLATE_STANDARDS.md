# Template Standards - What Must Be Met vs. What Can Be Omitted

**Version:** 1.0.0  
**Last Updated:** 2025-10-12  
**Purpose:** Define standards compliance requirements for templates and examples

---

## Overview

Templates and examples in Agentic Canon serve as **starting points** for projects, not complete implementations. They must meet certain standards to ensure quality and consistency, but are exempt from others because they:

1. **Are designed to be customized** by cookiecutter or copy-paste
2. **Contain template variables** (e.g., `{{ cookiecutter.project_name }}`)
3. **Represent parts of larger systems**, not standalone applications
4. **Serve as educational examples**, demonstrating patterns and best practices
5. **Will be completed by end users** who add business logic and features

This document clarifies which standards apply to templates and which can be reasonably omitted.

---

## Standards That MUST Be Met

Templates and examples must meet these standards to ensure quality and usability:

### 1. Structure and Organization

✅ **REQUIRED:**

- [ ] `README.md` with clear description and usage instructions
- [ ] Proper directory structure for the template type
- [ ] `.gitignore` file to exclude build artifacts and dependencies
- [ ] `cookiecutter.json` with well-defined variables (for cookiecutter templates)
- [ ] Hooks directory with validation scripts (`pre_gen_project.py`, `post_gen_project.py`)

**Rationale:** Users need clear guidance on how to use templates, and proper structure ensures generated projects follow conventions.

### 2. Syntax and Validation

✅ **REQUIRED:**

- [ ] Valid Python syntax in all `.py` files (hooks, validation modules)
- [ ] Valid JSON syntax in `cookiecutter.json` and configuration files
- [ ] Valid YAML syntax in actual workflow files (not template files with variables)
- [ ] No secrets or credentials committed to git
- [ ] Proper Jinja2 template syntax

**Rationale:** Syntax errors prevent templates from working. Secret exposure is a security risk.

**Note:** YAML files containing `{{ cookiecutter.* }}` variables are **exempt** from YAML validation until rendered, as these are Jinja2 templates that produce valid YAML after cookiecutter processing.

### 3. Documentation

✅ **REQUIRED:**

- [ ] `README.md` in each template directory explaining purpose and usage
- [ ] Comments in configuration files explaining key settings
- [ ] Links to relevant standards (NIST SSDF, OWASP, SLSA, etc.)
- [ ] Examples of expected outputs
- [ ] Usage instructions and prerequisites

**Rationale:** Documentation helps users understand and customize templates effectively.

### 4. CI/CD and Automation

✅ **REQUIRED:**

- [ ] CI/CD workflow files (`.github/workflows/ci.yml` or equivalent)
- [ ] Security scanning workflows (SAST, secret scanning, dependency scanning)
- [ ] Testing framework setup (pytest, jest, vitest, go test, etc.)
- [ ] Pre-commit hooks configuration (`.pre-commit-config.yaml`)
- [ ] Build automation (Makefile, package.json scripts, etc.)

**Rationale:** Templates should demonstrate best practices for automation and quality gates.

### 5. Security Baselines

✅ **REQUIRED:**

- [ ] Security scanning configured (CodeQL, Semgrep, Gitleaks)
- [ ] Dependency vulnerability scanning (Dependabot, Renovate)
- [ ] SBOM generation capability
- [ ] Secure defaults in configuration
- [ ] Input validation examples

**Rationale:** Security must be built in from the start, not added later.

### 6. Quality Gates

✅ **REQUIRED:**

- [ ] Linting and formatting configuration (Black, Ruff, ESLint, Prettier, golangci-lint)
- [ ] Testing framework and examples
- [ ] Coverage configuration (minimum thresholds)
- [ ] Type checking where applicable (mypy, TypeScript strict mode)
- [ ] Template validation pipeline executes render → lint → type → security → format via `.dev/validate-templates.sh --all`

**Rationale:** Templates should set users up for success with quality tooling.

---

## Standards That CAN Be Omitted

Templates and examples are **exempt** from these standards:

### 1. Code Coverage Requirements

⚠️ **EXEMPT:**

- Minimum 80% code coverage
- Mutation testing score of 40%+
- 100% branch coverage

**Rationale:** Templates contain minimal code and serve as starting points. Users will add business logic and tests. However, templates **should include example tests** to demonstrate testing patterns.

**What IS required:**

- Example test files showing testing patterns
- Testing framework properly configured
- Coverage tooling configured with sensible defaults

### 2. Complete Feature Implementation

⚠️ **EXEMPT:**

- Full business logic implementation
- Complete error handling for all edge cases
- Production-ready observability (though examples should be provided)
- Complete API implementations
- Comprehensive integration tests

**Rationale:** Templates demonstrate patterns, not complete applications. Users implement features based on their requirements.

**What IS required:**

- Working smoke tests or example tests
- Basic structure and patterns demonstrated
- Clear TODO comments where users should add logic

### 3. Performance Requirements

⚠️ **EXEMPT:**

- Meeting specific P95 latency targets
- Bundle size budgets for web apps
- Memory usage constraints
- Load testing

**Rationale:** Performance characteristics depend on the actual implementation and usage patterns.

**What IS required:**

- Performance testing framework configured (Lighthouse CI, k6, etc.)
- Performance budgets defined as examples
- Monitoring and observability setup

### 4. Comprehensive Documentation

⚠️ **EXEMPT:**

- Complete API documentation for all endpoints
- Architecture decision records (ADRs) for all decisions
- Detailed operational runbooks
- Complete user guides

**Rationale:** Templates provide starting points. Documentation grows with the project.

**What IS required:**

- README with clear usage instructions
- Comments explaining key configuration
- Links to relevant standards and best practices
- Examples of expected outputs

### 5. Deployment Configuration

⚠️ **EXEMPT:**

- Complete Kubernetes manifests for all environments
- Production-ready Helm charts
- Multi-cloud deployment configurations
- Complete IaC for all infrastructure

**Rationale:** Deployment requirements vary widely by organization and use case.

**What IS required:**

- Basic deployment examples
- Docker/container configuration
- Environment variable documentation
- Infrastructure-as-code templates where relevant

### 6. Advanced Features

⚠️ **EXEMPT:**

- Machine learning model serving
- Advanced caching strategies
- Complex state management
- Distributed tracing (though setup should be shown)
- Feature flags and experimentation

**Rationale:** These features are application-specific and beyond the scope of templates.

**What IS required:**

- Framework/library setup for these features if commonly used
- Examples or links to examples
- Configuration placeholders

---

## Sanity Check Standards Compliance

The `sanity-check.sh` script validates templates against the **REQUIRED** standards:

### What It Checks

✅ **Structure:**

- Template directories exist
- `cookiecutter.json` present
- Hooks directory present
- Project structure follows conventions
- Essential files present (`.gitignore`, `README.md`)

✅ **Syntax:**

- Python syntax valid in hooks
- JSON syntax valid in configuration
- YAML syntax valid (excluding template files)

✅ **Documentation:**

- `README.md` present in each template directory
- Framework documentation exists (FRAMEWORK.md, QUALITY_STANDARDS.md, CONVENTIONS.md)

✅ **CI/CD:**

- Workflow files present in `.github/workflows/`
- Testing framework configured

✅ **Standards Exemptions:**

- YAML files with `{{ cookiecutter.* }}` variables are skipped (they're Jinja2 templates)
- Code coverage thresholds are not enforced (but configuration is checked)
- Complete feature implementation is not required

### What It Does NOT Check

⚠️ **Not validated:**

- Code coverage percentages
- Performance metrics
- Complete feature implementation
- Production readiness
- Actual test execution (though framework presence is checked)

---

## Guidelines for Template Creators

When creating or updating templates:

### DO:

1. **Provide clear structure and organization**
   - Follow language and framework conventions
   - Include essential configuration files
   - Use consistent naming patterns

2. **Include working examples**
   - Smoke tests or basic unit tests
   - Example components or functions
   - Sample configuration

3. **Configure quality tooling**
   - Linting and formatting
   - Testing frameworks
   - Security scanning
   - CI/CD workflows

4. **Document clearly**
   - README with usage instructions
   - Comments explaining configuration
   - Links to standards and best practices

5. **Set secure defaults**
   - No secrets or credentials
   - Security scanning configured
   - Input validation examples
   - Least privilege principles

### DON'T:

1. **Don't implement complete features**
   - Templates are starting points
   - Leave room for customization
   - Use TODO comments for user additions

2. **Don't enforce production requirements**
   - Coverage and performance will vary
   - Let users tune for their needs
   - Provide guidance, not rigid requirements

3. **Don't make templates too specific**
   - Keep them general and adaptable
   - Avoid organization-specific patterns
   - Make customization easy

4. **Don't skip essential tooling**
   - Always include linting/formatting
   - Always include testing framework
   - Always include security scanning
   - Always include CI/CD workflows

---

## Validation Process

Templates go through this validation process:

1. **Automated Checks** (`sanity-check.sh`):
   - Structure validation
   - Syntax validation
   - Documentation presence
   - Essential files present

2. **Template Tests** (`pytest tests/test_cookiecutters.py`):
   - Template rendering succeeds
   - Generated project structure is valid
   - Validation hooks work correctly
   - Edge cases handled properly

3. **Manual Review**:
   - Code quality and clarity
   - Documentation completeness
   - Security best practices
   - Usability and user experience

---

## Standards Traceability

Templates support these standards while maintaining practical flexibility:

| Standard           | Template Requirement                       | Exemption Notes                           |
| ------------------ | ------------------------------------------ | ----------------------------------------- |
| **NIST SSDF v1.1** | Security scanning configured               | Full compliance in generated projects     |
| **OWASP SAMM**     | Secure defaults, input validation examples | Complete implementation by users          |
| **SLSA Level 3**   | Provenance workflow included               | Full implementation in generated projects |
| **ISO/IEC 25010**  | Quality tooling configured                 | Metrics measured in generated projects    |
| **WCAG 2.2 AA**    | Accessibility testing configured (web)     | Full compliance in generated projects     |

---

## Summary

**Templates MUST have:**

- Clear structure and documentation
- Valid syntax in all files
- Security scanning and quality tooling configured
- Working examples and patterns
- CI/CD workflows

**Templates CAN omit:**

- Complete feature implementation
- Production-level code coverage
- Comprehensive documentation
- Advanced features and optimizations
- Full deployment configurations

**Philosophy:** Templates are **foundations**, not **complete buildings**. They should be:

- **Correct** in what they include
- **Complete** in essential tooling and structure
- **Customizable** for diverse use cases
- **Clear** in documentation and examples
- **Compliant** with security and quality baselines

---

_Part of the Agentic Canon Framework - See FRAMEWORK.md, QUALITY_STANDARDS.md, and CONVENTIONS.md for complete standards._

# Architecture Templates

Comprehensive architecture documentation and governance templates for maintaining technical excellence.

## Purpose

These templates help teams document architectural decisions, visualize system structure, and implement automated architectural governance through fitness functions.

## Contents

### 📋 ADR Templates (`adr/`)

Architecture Decision Records (ADRs) document significant architectural decisions, their context, and consequences.

**File:** [`template.md`](adr/template.md)

**Features:**

- Structured decision documentation
- Context and rationale capture
- Alternatives analysis
- Impact assessment (performance, security, cost, DX)
- Standards compliance mapping (NIST, OWASP, ISO)
- Fitness functions for continuous validation
- Stakeholder tracking
- Review and maintenance schedule

**Usage:**

```bash
# Create a new ADR
cp templates/architecture/adr/template.md docs/adr/0001-use-postgresql.md

# Edit the template, replacing {{ PLACEHOLDERS }}
# Commit with descriptive message
git add docs/adr/0001-use-postgresql.md
git commit -m "docs: ADR-0001 - Use PostgreSQL for primary database"
```

**Best Practices:**

- Number ADRs sequentially (0001, 0002, etc.)
- Keep titles concise and action-oriented
- Update status as decisions evolve
- Link related ADRs
- Review ADRs annually or when context changes

### 📐 C4 Diagrams (`c4/`)

C4 (Context, Container, Component, Code) diagrams provide hierarchical system visualization using PlantUML.

**Files:**

- [`c4-context.puml`](c4/c4-context.puml) - Level 1: System context and external interactions
- [`c4-container.puml`](c4/c4-container.puml) - Level 2: Containers and their relationships

**Features:**

- Standards-based visualization (C4 model)
- PlantUML format (text-based, version control friendly)
- Multiple abstraction levels
- Clear system boundaries
- Technology stack documentation

**Usage:**

```bash
# Copy and customize for your system
cp templates/architecture/c4/c4-context.puml docs/architecture/system-context.puml
cp templates/architecture/c4/c4-container.puml docs/architecture/system-containers.puml

# Edit, replacing {{ PLACEHOLDERS }}
# Generate diagrams with PlantUML
plantuml docs/architecture/*.puml

# Or use online editor: https://www.plantuml.com/plantuml
```

**Rendering Options:**

- PlantUML CLI: `plantuml *.puml`
- VS Code extension: PlantUML
- Online: https://www.plantuml.com/plantuml
- CI/CD: Generate in GitHub Actions

**Best Practices:**

- Start with context diagram (Level 1)
- Add container diagram (Level 2) for implementation details
- Use component diagrams (Level 3) for complex containers
- Keep diagrams updated with architecture changes
- Store diagrams as code alongside documentation

### 🏗️ Fitness Functions (`fitness-functions/`)

Automated architectural governance checks that run in CI/CD pipelines.

**File:** [`fitness-functions.js`](fitness-functions/fitness-functions.js)

**Included Checks:**

1. **Coupling Check**
   - Detects circular dependencies
   - Enforces layered architecture
   - Validates module boundaries

2. **Performance Budget**
   - API response time limits
   - Bundle size constraints
   - Memory usage thresholds

3. **Security Constraints**
   - No hardcoded secrets
   - Dependency vulnerability checks
   - Attack surface metrics

4. **Code Quality**
   - Cyclomatic complexity limits
   - Code duplication thresholds
   - Test coverage requirements

**Usage:**

```bash
# Copy to your project
cp templates/architecture/fitness-functions/fitness-functions.js scripts/

# Install dependencies
npm install --save-dev madge lighthouse

# Run locally
node scripts/fitness-functions.js

# Add to CI/CD (package.json)
{
  "scripts": {
    "fitness": "node scripts/fitness-functions.js"
  }
}
```

**CI/CD Integration:**

```yaml
# .github/workflows/fitness-functions.yml
name: Fitness Functions
on: [push, pull_request]

jobs:
  fitness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run fitness
```

**Best Practices:**

- Run fitness functions on every commit
- Fail CI/CD if fitness functions fail
- Review and adjust thresholds quarterly
- Add new functions as architecture evolves
- Document rationale for each constraint

## Quick Start

### For New Projects

```bash
# Set up complete architecture documentation
mkdir -p docs/{adr,architecture}

# Copy ADR template
cp templates/architecture/adr/template.md docs/adr/

# Copy C4 diagrams
cp templates/architecture/c4/*.puml docs/architecture/

# Copy fitness functions
mkdir -p scripts
cp templates/architecture/fitness-functions/fitness-functions.js scripts/

# Create first ADR
cp docs/adr/template.md docs/adr/0001-initial-architecture.md
# Edit with your architecture decisions
```

### For Existing Projects

```bash
# Add ADR documentation
mkdir -p docs/adr
cp templates/architecture/adr/template.md docs/adr/0001-{{decision}}.md

# Add fitness functions
cp templates/architecture/fitness-functions/fitness-functions.js scripts/
npm install --save-dev madge lighthouse
```

## Integration Examples

### GitHub Actions Workflow

```yaml
name: Architecture Governance

on: [push, pull_request]

jobs:
  fitness-functions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: node scripts/fitness-functions.js

  c4-diagrams:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cloudbees/plantuml-github-action@master
        with:
          args: "docs/architecture/*.puml"
      - uses: actions/upload-artifact@v4
        with:
          name: diagrams
          path: docs/architecture/*.png
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: fitness-functions
        name: Run fitness functions
        entry: node scripts/fitness-functions.js
        language: system
        pass_filenames: false
```

## Standards Compliance

These templates help achieve compliance with:

- ✅ **ISO/IEC 25010**: Software quality characteristics (maintainability)
- ✅ **ISO/IEC 42010**: Architecture description standard
- ✅ **NIST SSDF**: Secure Software Development Framework
- ✅ **OWASP SAMM**: Software Assurance Maturity Model
- ✅ **C4 Model**: Software architecture visualization standard

## Additional Resources

### ADR Resources

- [ADR GitHub Organization](https://adr.github.io/)
- [Architecture Decision Records in Action](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [ADR Tools](https://github.com/npryce/adr-tools)

### C4 Model Resources

- [C4 Model Website](https://c4model.com/)
- [PlantUML for C4](https://github.com/plantuml-stdlib/C4-PlantUML)
- [Structurizr](https://structurizr.com/) - Advanced C4 tooling

### Fitness Functions Resources

- [Building Evolutionary Architectures](https://www.thoughtworks.com/books/building-evolutionary-architectures)
- [Fitness Function Driven Development](https://www.thoughtworks.com/insights/blog/fitness-function-driven-development)

## Customization Guide

### ADR Template Customization

1. Add organization-specific sections
2. Modify metadata fields
3. Adjust standards compliance mapping
4. Add required stakeholder roles
5. Customize review schedule

### C4 Diagram Customization

1. Add organization-specific systems
2. Customize color schemes
3. Add deployment diagrams (C4 Level 4)
4. Include database schemas
5. Add API documentation links

### Fitness Functions Customization

1. Add domain-specific constraints
2. Adjust thresholds for team context
3. Add new quality metrics
4. Integrate with monitoring tools
5. Create custom reports

## Support

For questions or issues:

1. Check [BIBLE.md](../../BIBLE.md) for conceptual guidance
2. Review [examples/](../../examples/) for real-world usage
3. Consult referenced standards documentation
4. Open an issue with specific questions

## Contributing

To improve these templates:

1. Fork the repository
2. Make your changes
3. Test with real projects
4. Submit a pull request with examples
5. Update this documentation

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

# ADR-001: Cookiecutter for Multi-Template Approach

## Status

Accepted

## Context

We need a way to provide multiple project templates (Python, Node.js, React, Go, docs-only) that can be easily customized and maintained. The templates must be:

1. Easy to use for developers and AI agents
2. Maintainable and updatable
3. Testable in CI/CD
4. Consistent across different technology stacks
5. Extensible for future templates

Several options were considered:

- Custom template generator
- Yeoman generators
- Cookiecutter
- Copier
- Manual template repositories

## Decision

We will use **Cookiecutter** as our template generation tool with a multi-template repository structure.

## Rationale

### Why Cookiecutter?

1. **Industry Standard**: Widely adopted in Python and other communities
2. **Simple**: Easy to understand and use for both humans and AI agents
3. **Multi-Template Support**: Native support for `--directory` flag to specify template subdirectories
4. **Hooks**: Pre and post-generation hooks for validation and setup
5. **Variables**: Simple `cookiecutter.json` for template variables
6. **Cross-Platform**: Works on Windows, macOS, and Linux
7. **Testing**: Well-supported by `pytest-cookies` for template testing
8. **Update Mechanism**: Can be paired with Cruft for template updates

### Why Multi-Template Repository?

1. **Centralized**: All templates in one place for easier maintenance
2. **Consistency**: Shared patterns and practices across templates
3. **Discovery**: Easy to browse all available templates
4. **Versioning**: Single version control for all templates
5. **Documentation**: Unified documentation and examples

### Template Structure

```
templates/
├── python-service/
│   ├── cookiecutter.json
│   ├── hooks/
│   │   ├── pre_gen_project.py
│   │   └── post_gen_project.py
│   └── {{cookiecutter.project_slug}}/
│       └── [template files]
├── node-service/
├── react-webapp/
├── go-service/
└── docs-only/
```

## Consequences

### Positive

- Developers can easily generate new projects with `cookiecutter templates/[template-name]`
- AI agents can parse `cookiecutter.json` to understand template variables
- Templates can be tested with `pytest-cookies` in CI/CD
- Updates can be propagated to generated projects using Cruft
- Common patterns can be shared across templates
- Easy to add new templates

### Negative

- Cookiecutter is primarily Python-focused (though it works for any language)
- Updates to generated projects require Cruft or manual intervention
- Some duplication across templates is inevitable
- Learning curve for Cookiecutter-specific features

### Mitigations

- Document Cookiecutter usage clearly in README and CONTRIBUTING
- Provide examples for each template
- Use Cruft to enable template updates
- Create shared components where possible
- Test templates thoroughly in CI/CD

## Alternatives Considered

### 1. Yeoman Generators

**Pros**:

- Popular in JavaScript ecosystem
- Interactive prompts
- Composable generators

**Cons**:

- Requires Node.js
- More complex to create generators
- Less suitable for non-JS templates

### 2. Copier

**Pros**:

- Built-in update mechanism
- Template versioning
- Jinja2 templating

**Cons**:

- Less widely adopted
- Fewer ecosystem tools
- More complex configuration

### 3. Custom Generator

**Pros**:

- Complete control
- Tailored to exact needs

**Cons**:

- Maintenance burden
- Reinventing the wheel
- Less community support

### 4. Manual Repositories

**Pros**:

- Simple
- Easy to understand

**Cons**:

- No customization during generation
- Hard to maintain multiple templates
- No update mechanism

## References

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [pytest-cookies](https://pytest-cookies.readthedocs.io/)
- [Cruft](https://cruft.github.io/cruft/)
- [Multi-template repositories](https://cookiecutter.readthedocs.io/en/latest/advanced/directories.html)

## Notes

- This decision aligns with Version 1.0 goals in TASKS.md
- Templates should follow security best practices from "Red Team + Software Excellence.md"
- All templates must include CI/CD, security scanning, and documentation
- Templates are tested in `.github/workflows/cookiecutters-test.yml`

---

**Date**: 2025-10-11  
**Author**: Jonathan Boardman (@IAmJonoBo)  
**Status**: Accepted

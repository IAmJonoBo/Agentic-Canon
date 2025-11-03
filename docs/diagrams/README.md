# Architecture Diagrams

This directory contains C4 architecture diagrams for the Agentic Canon project.

## What is C4?

The C4 model is a way to visualize software architecture through diagrams at different levels of abstraction:

1. **Context**: System and its users/external systems
2. **Container**: High-level technology choices
3. **Component**: Internal structure of containers
4. **Code**: (Optional) Class/implementation details

## Available Diagrams

### 1. [Context Diagram](c4-context-diagram.md)

**Level**: System Context  
**Shows**: How Agentic Canon fits into the wider ecosystem  
**Audience**: Everyone (technical and non-technical)  
**Key Elements**:

- Users (Developer, Platform Engineer, Security Analyst, AI Agent)
- Agentic Canon system boundary
- External systems (GitHub, Cloud Providers, Security Tools, Observability)

**Use this diagram to**:

- Understand the big picture
- See who uses the system and how
- Identify external dependencies
- Explain the system to stakeholders

### 2. [Container Diagram](c4-container-diagram.md)

**Level**: Container  
**Shows**: High-level technology choices and responsibilities  
**Audience**: Technical stakeholders  
**Key Elements**:

- CLI Wizard (Python/Click)
- Template Library (Cookiecutter/Jinja2)
- Documentation Notebooks (Jupyter/Jupytext)
- CI/CD Workflows (GitHub Actions)
- Dashboard Templates (Grafana)
- Generated project components

**Use this diagram to**:

- Understand the high-level architecture
- See technology choices
- Identify communication patterns
- Plan deployments

### 3. [Component Diagram](c4-component-diagram.md)

**Level**: Component  
**Shows**: Internal structure of the Template System  
**Audience**: Developers and architects  
**Key Elements**:

- CLI Wizard
- Template Engine
- Variable Resolver
- Validation Engine
- Hook Executor
- File Generator
- Git Initializer
- Individual template components

**Use this diagram to**:

- Understand internal architecture
- See component responsibilities
- Identify extension points
- Guide development work

## Diagram Formats

All diagrams are provided in multiple formats:

1. **Mermaid**: Embedded in Markdown for GitHub rendering
2. **Plain Text**: ASCII art for quick reference
3. **Tables and Lists**: Detailed component descriptions

## How to View

### On GitHub

Simply open the Markdown files - GitHub renders Mermaid diagrams automatically.

### Locally

1. **VS Code**: Install "Markdown Preview Mermaid Support" extension
2. **IntelliJ/PyCharm**: Mermaid plugin
3. **Browser**: Use [Mermaid Live Editor](https://mermaid.live/)

### Export to Images

Use [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli):

```bash
# Install
npm install -g @mermaid-js/mermaid-cli

# Convert to PNG
mmdc -i c4-context-diagram.md -o context.png

# Convert to SVG
mmdc -i c4-context-diagram.md -o context.svg
```

## Diagram Updates

When making architectural changes:

1. Update the relevant diagram(s)
2. Update the text descriptions
3. Keep diagrams in sync with code
4. Add version history notes

## Notation Guide

### C4 Element Types

| Symbol     | Meaning                           |
| ---------- | --------------------------------- |
| Person     | Human user of the system          |
| System     | Software system boundary          |
| Container  | Deployable/executable unit        |
| Component  | Grouping of related functionality |
| System_Ext | External system                   |

### Relationship Types

| Type        | Meaning         |
| ----------- | --------------- |
| `-->`       | Uses/depends on |
| `<-->`      | Bidirectional   |
| Solid line  | Synchronous     |
| Dashed line | Asynchronous    |

## Related Documentation

- [Architecture Decision Records](../adr/README.md)
- [TASKS.md](../../TASKS.md)
- [IMPLEMENTATION.md](../../IMPLEMENTATION.md)
- [README.md](../../README.md)

## Conventions

### Naming

- Use clear, descriptive names
- Avoid acronyms without explanation
- Be consistent across diagrams

### Colors (if using)

- Blue: Core Agentic Canon components
- Green: External systems (trusted)
- Yellow: Generated projects
- Red: Security-related components

### Grouping

- System boundaries show ownership
- Containers grouped by deployment unit
- Components grouped by responsibility

## Contributing

When contributing new diagrams:

1. Follow C4 model conventions
2. Use Mermaid format for consistency
3. Include plain text version
4. Add detailed descriptions
5. Update this README
6. Link from relevant documentation

## Tools and Resources

### Diagram Tools

- [Mermaid Live Editor](https://mermaid.live/)
- [PlantUML](https://plantuml.com/)
- [Draw.io](https://app.diagrams.net/)
- [Structurizr](https://structurizr.com/)

### Learning Resources

- [C4 Model](https://c4model.com/)
- [Mermaid Documentation](https://mermaid-js.github.io/)
- [Software Architecture Diagrams](https://www.infoq.com/articles/C4-architecture-model/)

## Validation

Before committing diagram changes:

- [ ] Diagram renders correctly in GitHub
- [ ] All relationships are labeled
- [ ] External systems are clearly marked
- [ ] Text descriptions match diagram
- [ ] Links to related docs are updated
- [ ] Diagram is at appropriate abstraction level

## Version History

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 1.0     | 2024-01-15 | Initial C4 diagrams (Context, Container, Component) |

---

_For questions about architecture, see [CONTRIBUTING.md](../../CONTRIBUTING.md) or open a discussion._

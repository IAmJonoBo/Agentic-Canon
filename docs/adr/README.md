# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for the Agentic Canon project. ADRs document significant architectural decisions made during the project's development.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

## Format

Each ADR follows this structure:

- **Title**: ADR-NNN: Short title of the decision
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: The situation that requires a decision
- **Decision**: The decision that was made
- **Rationale**: Why this decision was made
- **Consequences**: The positive and negative outcomes
- **Alternatives Considered**: Other options that were evaluated
- **References**: Links to relevant resources

## Current ADRs

### Foundation & Infrastructure

- [ADR-001: Cookiecutter for Multi-Template Approach](ADR-001-cookiecutter-multi-template.md) - Using Cookiecutter with multi-template repository structure
- [ADR-002: Jupytext for Notebook Version Control](ADR-002-jupytext-notebook-version-control.md) - Using Jupytext to version control notebooks as MyST Markdown

### Planned ADRs

The following ADRs are planned based on TASKS.md:

- **ADR-003**: GitHub Actions vs other CI/CD platforms
- **ADR-004**: OpenTelemetry for observability
- **ADR-005**: SLSA for supply chain security
- **ADR-006**: Trunk-based development workflow
- **ADR-007**: Progressive delivery strategy
- **ADR-008**: Error budgets and SLO tracking

## Creating a New ADR

1. Copy the template (if available) or use the existing ADRs as examples
2. Number it sequentially (ADR-NNN)
3. Fill in all sections thoughtfully
4. Submit as part of a pull request
5. Link from this README once accepted

## ADR Lifecycle

```
Proposed → Accepted → (Deprecated | Superseded)
```

- **Proposed**: Under discussion
- **Accepted**: Decision has been made and implemented
- **Deprecated**: No longer recommended but not replaced
- **Superseded**: Replaced by a newer ADR

## References

- [ADR GitHub Organization](https://adr.github.io/)
- [Michael Nygard's ADR Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Tools](https://github.com/npryce/adr-tools)

## Contributing

When making significant architectural decisions:

1. Create a new ADR document
2. Discuss with the team (open an issue or discussion)
3. Update the status as the decision progresses
4. Link related ADRs if the decision supersedes or relates to previous decisions

---

For questions about ADRs, see [CONTRIBUTING.md](../../CONTRIBUTING.md) or open a discussion.

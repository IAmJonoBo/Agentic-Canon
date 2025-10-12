# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for the Agentic Canon project. ADRs document significant architectural decisions made during the project's development.

## Quick Links

- **[ADR Lifecycle Guide](ADR-LIFECYCLE.md)** - Complete guide to creating, reviewing, and managing ADRs
- **[ADR Template](../../templates/architecture/adr/template.md)** - Template for creating new ADRs
- **[Create ADR Script](.dev/scripts/create-adr.sh)** - Automated ADR creation

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

**Total ADRs:** 8 (all accepted)

### Status Summary
- ✅ Accepted: 8
- 🔄 Proposed: 0  
- ⚠️ Deprecated: 0
- 🔀 Superseded: 0

### Foundation & Infrastructure

- [ADR-001: Cookiecutter for Multi-Template Approach](ADR-001-cookiecutter-multi-template.md) - Using Cookiecutter with multi-template repository structure
- [ADR-002: Jupytext for Notebook Version Control](ADR-002-jupytext-notebook-version-control.md) - Using Jupytext to version control notebooks as MyST Markdown
- [ADR-003: GitHub Actions for CI/CD](ADR-003-github-actions-cicd.md) - Using GitHub Actions as the primary CI/CD platform

### Observability & Operations

- [ADR-004: OpenTelemetry for Observability](ADR-004-opentelemetry-observability.md) - Using OpenTelemetry for vendor-neutral observability

### Security & Compliance

- [ADR-005: SLSA for Supply Chain Security](ADR-005-slsa-supply-chain-security.md) - Implementing SLSA framework for supply chain security
- [ADR-006: Security Scanning Strategy](ADR-006-security-scanning-strategy.md) - Multi-layered security scanning with specialized tools
- [ADR-007: Secret Management Approach](ADR-007-secret-management.md) - Prevention, detection, and secure storage of secrets
- [ADR-008: Dependency Management and Updates](ADR-008-dependency-management.md) - Automated dependency updates with safety checks

### Planned ADRs

The following ADRs are planned based on TASKS.md:

- **ADR-009**: Trunk-based development workflow
- **ADR-010**: Progressive delivery strategy
- **ADR-011**: Error budgets and SLO tracking

## Creating a New ADR

### Using the Script (Recommended)

```bash
# Run the interactive script
.dev/scripts/create-adr.sh

# Or create manually:
cp templates/architecture/adr/template.md docs/adr/ADR-NNN-your-decision.md
```

### Using GitHub Issue Template

1. Go to repository issues
2. Click "New Issue" 
3. Select "Architecture Decision Record (ADR) Proposal"
4. Fill in the template and submit
5. After approval, convert to ADR document

For detailed guidance, see [ADR Lifecycle Guide](ADR-LIFECYCLE.md).

## ADR Lifecycle

```
Proposed → [Review] → Accepted → [Implementation] → Active
                                                      ↓
                                            Deprecated/Superseded
```

- **Proposed**: Under discussion, gathering feedback
- **Accepted**: Decision approved and being/been implemented
- **Deprecated**: No longer recommended but not replaced
- **Superseded**: Replaced by a newer ADR

For complete lifecycle management, see [ADR Lifecycle Guide](ADR-LIFECYCLE.md).

## References

- [ADR GitHub Organization](https://adr.github.io/)
- [Michael Nygard's ADR Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Tools](https://github.com/npryce/adr-tools)

## Automation

### Workflows

- **ADR Validation** - Validates ADR format on PRs (`.github/workflows/adr-validation.yml`)
- **Tasks and ADR Sync** - Checks for unlinked ADRs weekly, enriches issues with ADR metadata (`.github/workflows/tasks-adr-sync.yml`)
- **Tasklist Scanner** - Creates issues from TASKS.md with ADR references (`.github/workflows/tasklist-scan.yml`)
- **Documentation Sanity Check** - Verifies ADR consistency (`.github/workflows/doc-sanity-check.yml`)

For complete details on how ADRs are automatically linked to tasks and issues, see [TASKS-ADR-SYNC.md](../TASKS-ADR-SYNC.md).

### Scripts

- **`.dev/scripts/create-adr.sh`** - Interactive ADR creation wizard
- Run `./.dev/scripts/create-adr.sh` to create a new ADR

## Contributing

When making significant architectural decisions:

1. **Propose**: Create ADR or use issue template
2. **Discuss**: Open PR and gather stakeholder feedback  
3. **Review**: Hold review meeting if needed
4. **Accept**: Update status when approved
5. **Implement**: Execute the decision
6. **Link**: Update this README with the new ADR
7. **Maintain**: Review annually and update as needed

See [ADR Lifecycle Guide](ADR-LIFECYCLE.md) for detailed instructions.

---

For questions about ADRs, see [CONTRIBUTING.md](../../CONTRIBUTING.md) or open a discussion.

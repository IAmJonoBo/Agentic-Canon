# Runbooks

This directory contains operational runbooks for Agentic Canon and generated projects.

## What are Runbooks?

Runbooks are step-by-step guides for common operational tasks, incident response, and troubleshooting. They provide:

- Clear procedures for routine operations
- Incident response workflows
- Troubleshooting guides
- Automation scripts and commands

## Current Runbooks

### Available

- `agent-runbook.json` - Machine-readable runbook for AI agents and automation

### Planned

Per TASKS.md, the following runbooks are planned:

- **Template Creation Runbook**: How to create new Cookiecutter templates
- **Deployment Runbook**: Deploying generated projects
- **Incident Response Runbook**: Handling production incidents
- **Agent-Oriented Automation Runbook**: Guide for AI agent automation

## Structure

Each runbook should include:

1. **Purpose**: What problem does this solve?
2. **Prerequisites**: What's needed before starting?
3. **Steps**: Clear, numbered steps
4. **Troubleshooting**: Common issues and solutions
5. **Rollback**: How to undo if something goes wrong
6. **Automation**: Scripts or commands to automate
7. **References**: Links to related documentation

## Using Runbooks

### For Humans

1. Read the entire runbook before starting
2. Ensure prerequisites are met
3. Follow steps sequentially
4. Document any deviations or issues
5. Update the runbook if improvements are found

### For AI Agents

- Machine-readable runbooks use JSON format
- Include clear success/failure criteria
- Provide automation commands
- Reference other documentation as needed

## Contributing

When creating a new runbook:

1. Use clear, concise language
2. Test the steps thoroughly
3. Include examples and screenshots
4. Add error handling guidance
5. Submit via pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## Format

Runbooks can be in:
- **Markdown** (`.md`) - Human-readable
- **JSON** (`.json`) - Machine-readable for automation
- **YAML** (`.yml`) - Structured and readable

## Examples

### Example Runbook Structure (Markdown)

```markdown
# Runbook: [Task Name]

## Purpose
What this runbook accomplishes

## Prerequisites
- Thing 1
- Thing 2

## Steps

### 1. First Step
Details and commands
```

### Example Machine-Readable Runbook (JSON)

```json
{
  "name": "example-task",
  "description": "Description of the task",
  "steps": [
    {
      "name": "Step 1",
      "command": "command to run",
      "validation": "how to verify"
    }
  ]
}
```

## References

- [Agent Runbook Specification](agent-runbook.json)
- [TASKS.md](../TASKS.md) - Planned runbooks
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute

---

For questions or suggestions, open an issue or discussion in the repository.

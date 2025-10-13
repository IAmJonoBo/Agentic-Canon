# Project Management Automation - Quick Reference

**TL;DR**: Automate task tracking with GitHub Actions. Zero manual overhead, full visibility.

## Quick Start (30 seconds)

### Option 1: New Project

```bash
cookiecutter templates/project-management
# Follow prompts, then:
cd your-project && git init && gh repo create
```

### Option 2: Existing Project

```bash
cd your-project
agentic-canon repo-init
git add . && git commit -m "feat: add project management automation"
git push
```

## What You Get

- ✅ **TODO → Issue**: Write `# TODO: Fix bug` → Auto-creates GitHub Issue
- ✅ **Tasklist → Issue**: Add `- [ ] Task` to TASKS.md → Auto-creates Issue
- ✅ **PR Review → Issue**: Say "follow-up" in review → Auto-creates Issue
- ✅ **Auto-triage**: New issues get smart labels automatically
- ✅ **Stale cleanup**: Inactive issues auto-close after 60 days

## Usage Patterns

### Pattern 1: TODO Comments

```python
# TODO: Add error handling
# FIXME: Memory leak in loop
# TODO: Optimize query performance
```

→ Each becomes a tracked GitHub Issue with issue URL written back

### Pattern 2: Task Lists (TASKS.md)

```markdown
## Sprint Tasks

- [ ] Implement authentication
- [ ] Write unit tests
- [ ] Update documentation
```

→ Automatically converted to `- [ ] #42 Implement authentication`

### Pattern 3: PR Follow-ups

```
LGTM! Follow-up: we should add comprehensive error handling.
This can be out of scope for this PR.
```

→ Creates issue with PR context, assigned to PR author

## CLI Commands

```bash
agentic-canon init         # New project wizard
agentic-canon repo-init    # Add to existing repo
agentic-canon validate     # Check project structure
agentic-canon doctor       # Check environment
agentic-canon audit        # Security & quality audit
```

## Configuration

Edit `.github/workflows/*.yml` to customize:

**TODO tracking** (`todos.yml`):

```yaml
LABELS: "task, from:todo, priority:medium" # Add custom labels
```

**Stale period** (`stale.yml`):

```yaml
days-before-stale: 30 # Change from 60 to 30
days-before-close: 14 # Change from 7 to 14
```

**Auto-labels** (`issue-triage.yml`):

```javascript
if (text.includes("database")) {
  labels.push("database"); // Add custom rules
}
```

## Setup Checklist

After generation:

1. ✅ Push to GitHub: `git push`
2. ✅ Create labels:
   ```bash
   gh label create "task" --color "0e8a16"
   gh label create "from:todo" --color "d4c5f9"
   gh label create "from:tasklist" --color "bfdadc"
   gh label create "needs-triage" --color "ededed"
   ```
3. ✅ Enable branch protection (optional)
4. ✅ Create GitHub Projects board (optional)
5. ✅ Test: Add a TODO, push, check Issues tab

## Common Scenarios

### Scenario: Quick Task Tracking

```bash
# In any code file:
# TODO: Add input validation

git commit -m "wip: partial implementation"
git push
# → Issue created automatically
```

### Scenario: Sprint Planning

```markdown
# In TASKS.md:

## Current Sprint

- [ ] User authentication
- [ ] API endpoints
- [ ] Database schema

git add TASKS.md && git commit -m "plan: sprint tasks"
git push

# → 3 issues created, tracked in TASKS.md
```

### Scenario: PR Review

1. Reviewer adds comment: "Follow-up: add more edge case tests"
2. Submit review
3. Issue created automatically, assigned to PR author

## Troubleshooting

**Workflows not running?**

- Check `.github/workflows/` files exist
- Verify Actions enabled in repo settings
- Check workflow logs in Actions tab

**Issues not created?**

- Check labels exist in repository
- Verify GITHUB_TOKEN has write permissions
- Look for duplicate issues

**TODOs not detected?**

- Use supported formats: `# TODO:`, `// TODO:`, `/* TODO: */`
- Ensure file is tracked by git
- Check workflow logs

## Best Practices

1. **Start simple** - Enable TODO tracking first, add others gradually
2. **Create labels upfront** - Prevents workflow errors
3. **Review automation** - Check created issues, adjust keywords
4. **Document patterns** - Team should know how to use it
5. **Monitor workflows** - Watch Actions tab for issues

## Resources

- **Full Documentation**: [templates/project-management/README.md](templates/project-management/README.md)
- **Implementation Details**: [PROJECT_MANAGEMENT_IMPLEMENTATION.md](PROJECT_MANAGEMENT_IMPLEMENTATION.md)
- **Template Source**: [templates/project-management/](templates/project-management/)
- **Workflow Examples**: [.github/workflows/](../.github/workflows/)

## Support

For issues or questions:

1. Check workflow logs in Actions tab
2. Review [PROJECT_MANAGEMENT.md](templates/project-management/{{cookiecutter.project_slug}}/PROJECT_MANAGEMENT.md)
3. Open an issue with label `question`

---

**Version**: 1.0 | **Last Updated**: 2025-10-12 | **Status**: Production Ready ✅

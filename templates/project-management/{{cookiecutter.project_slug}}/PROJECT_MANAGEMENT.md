# {{ cookiecutter.project_name }} - Project Management

This document describes the automated project management system implemented in this repository.

## Overview

This repository uses GitHub Actions and GitHub Issues/Projects to automate task tracking and project management. The goal is to eliminate manual overhead while maintaining visibility and traceability.

## System Architecture

```text
Code Changes → Workflows → GitHub Issues → GitHub Projects
                    ↓
              Auto-triage & Label
                    ↓
              Track & Update
                    ↓
              Close on Completion
```

## Automated Workflows

{% if cookiecutter.enable_todo_tracking == "yes" -%}

### 1. TODO Tracking (todos.yml)

**Trigger**: On every push to any branch

**What it does**:

- Scans code for TODO/FIXME comments
- Creates GitHub Issues for new TODOs
- Writes issue URL back into the comment
- Closes issues when TODO is removed

**Supported formats**:

```python
# TODO: Description here
# FIXME: Problem description
// TODO: JavaScript style
/* TODO: Block comment style */
```

**Configuration**:

- Labels: `task`, `from:todo`
- Auto-assign: Commit author
- Close on removal: Yes

**Example**:

```python
# TODO: Add input validation
# Becomes: # TODO: Add input validation https://github.com/org/repo/issues/123
```

{% endif -%}

{% if cookiecutter.enable_tasklist_tracking == "yes" -%}

### 2. Tasklist Tracking (tasklist-scan.yml)

**Trigger**: On push when markdown files change

**What it does**:

- Scans TASKS.md and other markdown files
- Finds unchecked checkbox items: `- [ ] Task description`
- Creates GitHub Issues for new items
- Updates markdown to reference issue: `- [ ] #123 Task description`
- Prevents duplicate issues

**Example TASKS.md**:

```markdown
## Sprint Tasks

- [ ] Implement user authentication
- [x] Set up database
- [ ] Write API documentation
```

After workflow runs:

```markdown
## Sprint Tasks

- [ ] #42 Implement user authentication
- [x] Set up database
- [ ] #43 Write API documentation
```

**Configuration**:

- Watches: `TASKS.md`, `docs/**/*.md`, `**/*.md`
- Labels: `task`, `from:tasklist`
- Auto-commits: Yes
  {% endif -%}

{% if cookiecutter.enable_pr_followups == "yes" -%}

### 3. PR Review Follow-ups (pr-review-followup.yml)

**Trigger**: When a PR review is submitted

**What it does**:

- Detects follow-up keywords in review comments
- Creates issue with full context
- Links back to PR and review
- Assigns to PR author

**Keywords detected**:

- "follow-up" / "follow up"
- "out of scope"
- "TODO:"
- "FIXME:"
- "future work"
- "next iteration"

**Example review comment**:

```text
LGTM! The implementation is solid.

Follow-up: We should add comprehensive error handling for edge cases.
This can be out of scope for this PR.
```

Creates issue:

```text
Title: Follow-up from PR #42: Add user authentication
Body:
  ## Context
  From PR #42 - Add user authentication

  ## Review Comment
  [original comment]

  ## Reviewer
  @reviewer-username

  ## PR Link
  https://github.com/org/repo/pull/42
```

**Configuration**:

- Labels: `follow-up`, `from:pr-review`
- Assignee: PR author
  {% endif -%}

{% if cookiecutter.enable_issue_triage == "yes" -%}

### 4. Issue Triage (issue-triage.yml)

**Trigger**: When a new issue is opened

**What it does**:

- Adds `needs-triage` label
- Analyzes title and body for keywords
- Adds relevant labels automatically
- Posts welcome comment with next steps

**Auto-labeling rules**:

- "bug", "error", "fail" → `bug` label
- "feature", "enhancement", "add" → `enhancement` label
- "doc", "readme" → `documentation` label
- "security", "vulnerability", "cve" → `security` label
- "performance", "slow" → `performance` label
- "question", "how to" → `question` label

**Welcome message includes**:

- Thank you note
- Contribution guidelines link
- Code of conduct link
- Next steps guidance
  {% endif -%}

{% if cookiecutter.auto_close_stale_issues == "yes" -%}

### 5. Stale Issue Management (stale.yml)

**Trigger**: Daily at midnight UTC

**What it does**:

- Marks issues inactive for {{ cookiecutter.stale_days }} days as stale
- Posts warning comment
- Closes issues 7 days after marking stale
- Exempts issues with labels: `pinned`, `security`, `critical`

**Configuration**:

- Stale after: {{ cookiecutter.stale_days }} days
- Close after: 7 days of stale
- Labels: `stale`
- Exemptions: `pinned`, `security`, `critical`
  {% endif -%}

## GitHub Projects Integration

{% if cookiecutter.enable_projects_board == "yes" -%}

### Setup

1. Create a new Project in GitHub
2. Choose "Board" view
3. Add custom fields:
   - **Priority**: Single select (High, Medium, Low)
   - **Iteration**: Iteration field (sprints)
   - **Size**: Single select (S, M, L, XL)

### Automation Rules

Configure these built-in automations:

1. **Auto-add items**
   - When: Issue/PR is opened
   - Then: Add to project
   - Status: Set to "Todo"

2. **Auto-archive**
   - When: Issue/PR is closed
   - Then: Set status to "Done"
   - After: 14 days, archive

3. **Status sync**
   - Sync issue state with project status
   - Closed issues → "Done" column
   - Open issues → Stay in current column

### Workflow

```text
New Issue → Auto-add → Todo
    ↓
Assign & Start → In Progress
    ↓
Create PR → In Review
    ↓
Merge PR → Close Issue → Done
    ↓
Auto-archive (14 days)
```

{% endif -%}

## Best Practices

### For Developers

1. **Use TODO comments liberally**
   - They automatically become tracked work items
   - Include enough context in the comment
   - Remove TODOs when work is complete

2. **Maintain TASKS.md**
   - Use for high-level project tracking
   - Break down large tasks into subtasks
   - Check off completed items

3. **Write meaningful commit messages**
   - Use "Closes #123" to auto-close issues
   - Reference related issues with "#123"
   - Follow Conventional Commits format

4. **In PR reviews**
   - Use "follow-up" for future work
   - Be specific about what needs follow-up
   - Use "out of scope" to defer work appropriately

### For Project Managers

1. **Triage regularly**
   - Review `needs-triage` issues daily
   - Assign priority and milestone
   - Assign to appropriate team members

2. **Use Projects board**
   - Organize work by iteration/sprint
   - Set priorities for each item
   - Track progress visually

3. **Monitor workflows**
   - Check Actions tab for failures
   - Review auto-created issues
   - Adjust labels and assignments

4. **Maintain labels**
   - Keep label taxonomy consistent
   - Use colors meaningfully
   - Document label meanings

## Maintenance

### Adjusting Workflows

Edit workflow files in `.github/workflows/`:

- **Change TODO label**: Edit `todos.yml` → `LABELS` field
- **Adjust stale timing**: Edit `stale.yml` → `days-before-stale`
- **Modify auto-labels**: Edit `issue-triage.yml` → keyword patterns
- **Change tasklist paths**: Edit `tasklist-scan.yml` → `paths` array

### Troubleshooting

**Workflow not running**:

1. Check `.github/workflows/` files exist
2. Verify permissions in workflow file
3. Check Actions tab for errors
4. Ensure branch protection allows Actions

**Issues not created**:

1. Check workflow logs in Actions tab
2. Verify GitHub token has write permissions
3. Check for duplicate issues
4. Verify label names exist

**Labels not applying**:

1. Create labels manually first (see README.md)
2. Check label names match workflow config
3. Verify label colors (optional but helpful)

## Security Considerations

1. **Permissions**
   - Workflows use `GITHUB_TOKEN` with minimal permissions
   - No secrets required for basic functionality
   - Review permission grants in workflow files

2. **Branch Protection**
   {% if cookiecutter.enable_branch_protection == "yes" -%}
   - {{ cookiecutter.require_approvals }} required approvals
     {% endif -%}
   - Status checks must pass
   - Linear history enforced
   - Force pushes disabled

3. **Code Owners**
   {% if cookiecutter.enable_codeowners == "yes" -%}
   - CODEOWNERS file defines reviewers
   - Automatic assignment on PR
   - Required for sensitive files
     {% endif -%}

## Customization

### Adding Custom Labels

```bash
gh label create "priority:high" --color "d93f0b" --description "High priority"
gh label create "priority:medium" --color "fbca04" --description "Medium priority"
gh label create "priority:low" --color "0e8a16" --description "Low priority"
```

### Custom Auto-labeling

Edit `.github/workflows/issue-triage.yml`:

```javascript
// Add custom rules
if (text.includes("ui") || text.includes("frontend")) {
  labels.push("frontend");
}
if (text.includes("api") || text.includes("backend")) {
  labels.push("backend");
}
```

### Custom Follow-up Keywords

Edit `.github/workflows/pr-review-followup.yml`:

```javascript
const followupPatterns = [
  /follow-up/i,
  /technical debt/i, // Add custom keyword
  /future enhancement/i, // Add another
];
```

## Metrics and Reporting

Track these metrics to measure effectiveness:

1. **Issue velocity**: Issues opened vs closed per week
2. **TODO coverage**: % of TODOs tracked as issues
3. **PR review time**: Time from open to first review
4. **Stale issue rate**: % of issues becoming stale
5. **Triage time**: Time from open to first label/assign

Use GitHub Insights and Projects for visualization.

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [TODO to Issue Action](https://github.com/alstr/todo-to-issue-action)
- [Stale Action](https://github.com/actions/stale)

---

**Version**: 1.0  
**Last Updated**: 2025-10-12  
**Template**: Agentic Canon Project Management

# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 🎯 Project Management Automation

This repository uses automated workflows to manage tasks and issues efficiently.

### Features

{% if cookiecutter.enable_todo_tracking == "yes" -%}

- ✅ **TODO Tracking**: Automatically creates issues from TODO/FIXME comments in code
  {% endif -%}
  {% if cookiecutter.enable_tasklist_tracking == "yes" -%}
- ✅ **Tasklist Tracking**: Converts unchecked markdown checklist items into GitHub Issues
  {% endif -%}
  {% if cookiecutter.enable_pr_followups == "yes" -%}
- ✅ **PR Follow-ups**: Creates issues for follow-up work mentioned in PR reviews
  {% endif -%}
  {% if cookiecutter.enable_issue_triage == "yes" -%}
- ✅ **Auto Triage**: Automatically labels and responds to new issues
  {% endif -%}
  {% if cookiecutter.auto_close_stale_issues == "yes" -%}
- ✅ **Stale Issue Management**: Automatically closes inactive issues after {{ cookiecutter.stale_days }} days
  {% endif -%}
  {% if cookiecutter.enable_codeowners == "yes" -%}
- ✅ **Code Owners**: Automatic reviewer assignment based on file paths
  {% endif -%}

### Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.project_slug }}.git
   cd {{ cookiecutter.project_slug }}
   ```

2. **Set up GitHub integration**
   - Ensure GitHub Actions are enabled
   - Configure branch protection rules (see below)
   - Set up GitHub Projects board (optional)

3. **Configure labels**

   ```bash
   # Install GitHub CLI if not already installed
   # https://cli.github.com/

   gh label create "task" --color "0e8a16" --description "General task"
   gh label create "from:todo" --color "d4c5f9" --description "Created from TODO comment"
   gh label create "from:tasklist" --color "bfdadc" --description "Created from tasklist"
   gh label create "from:pr-review" --color "fbca04" --description "Follow-up from PR review"
   gh label create "follow-up" --color "fef2c0" --description "Follow-up work required"
   gh label create "needs-triage" --color "ededed" --description "Needs initial triage"
   ```

{% if cookiecutter.enable_branch_protection == "yes" -%} 4. **Set up branch protection**

```bash
gh api repos/{{ cookiecutter.github_org }}/{{ cookiecutter.project_slug }}/branches/{{ cookiecutter.default_branch }}/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field enforce_admins=true \
  --field required_pull_request_reviews[dismiss_stale_reviews]=true \
  --field required_pull_request_reviews[require_code_owner_reviews]=true \
  --field required_pull_request_reviews[required_approving_review_count]={{ cookiecutter.require_approvals }} \
  --field required_linear_history=true \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

{% endif -%}

### Usage

{% if cookiecutter.enable_todo_tracking == "yes" -%}

#### TODO Comments

Add TODO comments in your code, and they will automatically become GitHub Issues:

```python
# TODO: Implement user authentication
# TODO: Add input validation
# FIXME: Handle edge case for empty strings
```

The workflow will:

- Create a GitHub Issue for each TODO/FIXME
- Add labels: `task`, `from:todo`
- Write the issue URL back into the code comment
- Close the issue when the TODO is removed
  {% endif -%}

{% if cookiecutter.enable_tasklist_tracking == "yes" -%}

#### Task Lists

Add unchecked items to `TASKS.md` or any markdown file:

```markdown
## Project Tasks

- [ ] Set up CI/CD pipeline
- [ ] Write unit tests
- [ ] Update documentation
```

The workflow will:

- Create a GitHub Issue for each unchecked item
- Replace the checkbox with a tracked issue link: `- [ ] #123 Set up CI/CD pipeline`
- Sync status with the issue state
  {% endif -%}

{% if cookiecutter.enable_pr_followups == "yes" -%}

#### PR Review Follow-ups

When reviewing PRs, mention follow-up work using keywords:

```text
This looks good! The implementation is solid, but we should follow-up with:
- Add more comprehensive error handling
- Consider performance optimization for large datasets

This can be out of scope for this PR.
```

The workflow will automatically create an issue with:

- Link to the PR
- The review comment
- Assignment to the PR author
- Labels: `follow-up`, `from:pr-review`
  {% endif -%}

### Workflows

The following GitHub Actions workflows are configured:

{% if cookiecutter.enable_todo_tracking == "yes" -%}

- **`todos.yml`**: Converts TODO/FIXME comments to issues
  {% endif -%}
  {% if cookiecutter.enable_tasklist_tracking == "yes" -%}
- **`tasklist-scan.yml`**: Tracks markdown checklist items
  {% endif -%}
  {% if cookiecutter.enable_pr_followups == "yes" -%}
- **`pr-review-followup.yml`**: Creates issues from PR review comments
  {% endif -%}
  {% if cookiecutter.enable_issue_triage == "yes" -%}
- **`issue-triage.yml`**: Auto-labels and responds to new issues
  {% endif -%}
  {% if cookiecutter.auto_close_stale_issues == "yes" -%}
- **`stale.yml`**: Closes inactive issues after {{ cookiecutter.stale_days }} days
  {% endif -%}

### Best Practices

1. **Task Management**
   - Use TODO comments for quick, inline task tracking
   - Use TASKS.md for high-level project tracking
   - Use GitHub Issues for detailed discussions and collaboration

2. **PR Reviews**
   - Use "follow-up" keyword for work that should be tracked
   - Use "out of scope" to document intentional deferrals
   - Link to created issues in review comments

3. **Issue Triage**
   - Review and refine auto-assigned labels
   - Update issue priority and milestone
   - Assign to appropriate team members

4. **Branch Protection**
   - Require {{ cookiecutter.require_approvals }} approvals before merging
   - Ensure all CI checks pass
   - Keep commit history clean with linear history

### Documentation

- [PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md) - Detailed workflow documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policy

### Support

For questions or issues with the automation:

1. Check the [workflow runs](https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.project_slug }}/actions)
2. Review workflow logs for errors
3. Open an issue with the `question` label

---

#### Generated with Agentic Canon Project Management Template

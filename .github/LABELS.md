# GitHub Labels Setup

This document lists all GitHub labels required for the project management automation workflows to function properly.

## Required Labels

These labels MUST be created in the repository for the workflows to function correctly:

### Issue Type Labels
- `bug` (color: `#d73a4a`) - Something isn't working
- `enhancement` (color: `#a2eeef`) - New feature or request
- `task` (color: `#0e8a16`) - Work item or task
- `documentation` (color: `#0075ca`) - Documentation improvements or additions
- `question` (color: `#d876e3`) - Further information is requested

### Workflow Labels
- `from:todo` (color: `#d4c5f9`) - Created from TODO/FIXME comment in code
- `from:tasklist` (color: `#bfdadc`) - Created from markdown checklist in TASKS.md
- `from:pr-review` (color: `#fbca04`) - Created from PR review follow-up comment
- `needs-triage` (color: `#ededed`) - Needs initial review and categorization

### Priority Labels (Optional but Recommended)
- `priority:high` (color: `#d93f0b`) - High priority item
- `priority:medium` (color: `#fbca04`) - Medium priority item
- `priority:low` (color: `#0e8a16`) - Low priority item

### Status Labels
- `stale` (color: `#cccccc`) - Issue/PR marked as stale due to inactivity
- `security` (color: `#ee0701`) - Security-related issue
- `performance` (color: `#1d76db`) - Performance-related issue
- `critical` (color: `#b60205`) - Critical issue that needs immediate attention

### Exemption Labels
These labels exempt issues/PRs from being marked as stale:
- `pinned` (color: `#0e8a16`) - Pinned, won't be marked stale
- `security` (color: `#ee0701`) - Security issues never go stale
- `critical` (color: `#b60205`) - Critical issues never go stale

## Setup Instructions

### Using GitHub CLI (gh)

```bash
# Install gh CLI if not already installed
# https://cli.github.com/

# Navigate to repository
cd /path/to/Agentic-Canon

# Create labels (will skip if already exists)
gh label create "bug" --color "d73a4a" --description "Something isn't working" || true
gh label create "enhancement" --color "a2eeef" --description "New feature or request" || true
gh label create "task" --color "0e8a16" --description "Work item or task" || true
gh label create "documentation" --color "0075ca" --description "Documentation improvements or additions" || true
gh label create "question" --color "d876e3" --description "Further information is requested" || true

gh label create "from:todo" --color "d4c5f9" --description "Created from TODO/FIXME comment" || true
gh label create "from:tasklist" --color "bfdadc" --description "Created from markdown checklist" || true
gh label create "from:pr-review" --color "fbca04" --description "Created from PR review follow-up" || true
gh label create "needs-triage" --color "ededed" --description "Needs initial review and categorization" || true

gh label create "priority:high" --color "d93f0b" --description "High priority item" || true
gh label create "priority:medium" --color "fbca04" --description "Medium priority item" || true
gh label create "priority:low" --color "0e8a16" --description "Low priority item" || true

gh label create "stale" --color "cccccc" --description "Marked as stale due to inactivity" || true
gh label create "security" --color "ee0701" --description "Security-related issue" || true
gh label create "performance" --color "1d76db" --description "Performance-related issue" || true
gh label create "critical" --color "b60205" --description "Critical issue needing immediate attention" || true
gh label create "pinned" --color "0e8a16" --description "Pinned, won't be marked stale" || true
```

### Using GitHub Web UI

1. Navigate to your repository on GitHub
2. Click on **Issues** tab
3. Click on **Labels**
4. Click **New label** for each label above
5. Enter the name, description, and color code
6. Click **Create label**

### Automated Setup Script

A script is provided in `scripts/setup-labels.sh` that will create all required labels:

```bash
./scripts/setup-labels.sh
```

## Verification

To verify all labels are created:

```bash
gh label list
```

You should see all labels listed above.

## Workflow Dependencies

### todos.yml
- Required: `task`, `from:todo`
- Optional: Any PROJECT field for GitHub Projects integration

### tasklist-scan.yml
- Required: `task`, `from:tasklist`
- Will commit changes back to TASKS.md with issue references

### pr-review-followup.yml
- Required: `from:pr-review`
- Auto-assigns: PR author

### issue-triage.yml
- Required: `needs-triage`
- Optional: `bug`, `enhancement`, `documentation`, `security`, `performance`, `question`
- Auto-labels based on keyword detection

### stale.yml
- Required: `stale`
- Exempts: `pinned`, `security`, `critical`

## Customization

To customize labels for your needs:

1. Edit the workflow files in `.github/workflows/`
2. Update the `labels` or `LABELS` fields
3. Create the new labels using the instructions above
4. Test the workflow with a manual trigger

## Troubleshooting

### Workflow fails with "Label does not exist"
- Ensure all required labels are created
- Check spelling and case sensitivity
- Run `gh label list` to verify

### Labels not being applied automatically
- Check workflow logs in Actions tab
- Verify workflow has `issues: write` permission
- Ensure GITHUB_TOKEN has proper permissions

### Duplicate issues being created
- tasklist-scan checks for existing issues by title
- todos workflow writes issue URL back to code to prevent duplicates
- If duplicates occur, check that URL insertion is working

## Additional Resources

- [GitHub Labels Documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [GitHub CLI Label Commands](https://cli.github.com/manual/gh_label)
- [PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md) - Complete automation guide

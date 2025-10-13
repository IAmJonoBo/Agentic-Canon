# Project Management Template

Cookiecutter template for automated project management using GitHub Actions and Issues.

## Features

- ✅ **TODO Tracking**: Automatically creates issues from TODO/FIXME comments
- ✅ **Tasklist Tracking**: Converts markdown checklist items into GitHub Issues
- ✅ **PR Follow-ups**: Creates issues for follow-up work from PR reviews
- ✅ **Auto Triage**: Automatically labels and responds to new issues
- ✅ **Stale Management**: Closes inactive issues automatically
- ✅ **Code Owners**: Automatic reviewer assignment
- ✅ **Issue/PR Templates**: Standardized templates for bugs, features, and tasks
- ✅ **Branch Protection**: Recommended branch protection rules
- ✅ **Projects Integration**: Ready for GitHub Projects board integration

## Quick Start

### Using Cookiecutter

```bash
# Install cookiecutter if needed
pip install cookiecutter

# Generate project management setup
cookiecutter templates/project-management

# Follow the prompts to configure your setup
```

### Using Agentic Canon CLI

```bash
# Install the CLI
pip install -e .

# Initialize with project management
agentic-canon repo-init
```

## Template Variables

| Variable                   | Description           | Default    | Options         |
| -------------------------- | --------------------- | ---------- | --------------- |
| `project_name`             | Project name          | My Project | Any string      |
| `project_slug`             | Kebab-case slug       | my-project | Kebab-case      |
| `github_org`               | GitHub org name       | my-org     | Org/user name   |
| `project_description`      | Description           | -          | Any string      |
| `enable_todo_tracking`     | Enable TODO→Issue     | yes        | yes/no          |
| `enable_tasklist_tracking` | Enable tasklist→Issue | yes        | yes/no          |
| `enable_pr_followups`      | Enable PR follow-ups  | yes        | yes/no          |
| `enable_issue_triage`      | Enable auto-triage    | yes        | yes/no          |
| `enable_projects_board`    | Setup for Projects    | yes        | yes/no          |
| `enable_branch_protection` | Show protection setup | yes        | yes/no          |
| `enable_codeowners`        | Include CODEOWNERS    | yes        | yes/no          |
| `default_branch`           | Default branch name   | main       | Any branch name |
| `require_approvals`        | Required PR approvals | 2          | Number          |
| `auto_close_stale_issues`  | Close stale issues    | yes        | yes/no          |
| `stale_days`               | Days before stale     | 60         | Number          |

## Generated Structure

```
my-project/
├── .github/
│   ├── workflows/
│   │   ├── todos.yml                  # TODO tracking
│   │   ├── tasklist-scan.yml          # Tasklist tracking
│   │   ├── pr-review-followup.yml     # PR follow-ups
│   │   ├── issue-triage.yml           # Auto-triage
│   │   └── stale.yml                  # Stale issue management
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── task.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS                     # Code ownership
├── README.md                          # Project overview
├── PROJECT_MANAGEMENT.md              # Detailed docs
└── TASKS.md                           # Task tracking file
```

## Workflows

### 1. TODO Tracking (todos.yml)

Scans code for TODO/FIXME comments and creates GitHub Issues.

**Supported formats**:

```python
# TODO: Add error handling
# FIXME: Fix memory leak
// TODO: JavaScript style
/* TODO: Block comment */
```

**Features**:

- Creates issue with task label
- Writes issue URL back to code
- Closes issue when TODO removed
- Auto-assigns to commit author

### 2. Tasklist Tracking (tasklist-scan.yml)

Converts markdown checklist items to GitHub Issues.

**Example TASKS.md**:

```markdown
## Sprint 1

- [ ] Implement authentication
- [ ] Write documentation
- [x] Set up CI/CD
```

**Features**:

- Creates issue for unchecked items
- Updates markdown with issue link
- Prevents duplicate issues
- Commits changes automatically

### 3. PR Review Follow-ups (pr-review-followup.yml)

Creates issues from PR review comments mentioning follow-up work.

**Keywords**:

- "follow-up"
- "out of scope"
- "TODO:"
- "future work"
- "next iteration"

**Features**:

- Links to PR and review
- Assigns to PR author
- Includes full context
- Labels for tracking

### 4. Issue Triage (issue-triage.yml)

Automatically labels and responds to new issues.

**Auto-labeling**:

- Bug keywords → `bug` label
- Feature keywords → `enhancement` label
- Security keywords → `security` label
- Performance keywords → `performance` label

**Features**:

- Adds `needs-triage` label
- Posts welcome message
- Links to contribution docs
- Smart keyword detection

### 5. Stale Management (stale.yml)

Closes inactive issues after configured period.

**Default behavior**:

- Mark stale after 60 days
- Close after 7 days of stale
- Exempts: `pinned`, `security`, `critical`

**Configurable**:

- Adjust stale period
- Customize messages
- Add exemptions
- Schedule frequency

## Usage Examples

### Example 1: New Project Setup

```bash
# Generate project management setup
cookiecutter templates/project-management

# Configuration
project_name: Awesome API
project_slug: awesome-api
github_org: my-company
enable_todo_tracking: yes
enable_tasklist_tracking: yes
enable_pr_followups: yes
enable_issue_triage: yes

# Result: Complete automation setup ready to use
cd awesome-api
git init
git add .
git commit -m "chore: initial project management setup"
gh repo create my-company/awesome-api --public --push
```

### Example 2: Add to Existing Project

```bash
# Generate in temporary directory
cookiecutter templates/project-management --output-dir /tmp

# Copy workflows to existing project
cp -r /tmp/my-project/.github/workflows/* .github/workflows/
cp /tmp/my-project/PROJECT_MANAGEMENT.md .
cp /tmp/my-project/TASKS.md .

# Commit and push
git add .
git commit -m "feat: add project management automation"
git push
```

### Example 3: Minimal Setup (Manual TODO Tracking Only)

```bash
cookiecutter templates/project-management

# Configuration
enable_todo_tracking: yes
enable_tasklist_tracking: no
enable_pr_followups: no
enable_issue_triage: no
auto_close_stale_issues: no

# Result: Only todos.yml workflow generated
```

## Customization

### Adjusting TODO Labels

Edit `.github/workflows/todos.yml`:

```yaml
LABELS: "task, from:todo, priority:medium" # Add custom labels
```

### Custom Auto-labeling Rules

Edit `.github/workflows/issue-triage.yml`:

```javascript
// Add your custom rules
if (text.includes("database") || text.includes("sql")) {
  labels.push("database");
}
```

### Change Stale Period

Edit `.github/workflows/stale.yml`:

```yaml
days-before-stale: 30 # Change from 60 to 30 days
days-before-close: 14 # Change from 7 to 14 days
```

## Post-Generation Steps

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "chore: add project management automation"
   git branch -M main
   git remote add origin https://github.com/org/repo.git
   git push -u origin main
   ```

2. **Create GitHub Labels**

   ```bash
   gh label create "task" --color "0e8a16"
   gh label create "from:todo" --color "d4c5f9"
   gh label create "from:tasklist" --color "bfdadc"
   gh label create "from:pr-review" --color "fbca04"
   gh label create "follow-up" --color "fef2c0"
   gh label create "needs-triage" --color "ededed"
   ```

3. **Enable Branch Protection** (if configured)

   ```bash
   gh api repos/org/repo/branches/main/protection \
     --method PUT \
     --field required_pull_request_reviews[required_approving_review_count]=2 \
     --field required_status_checks[strict]=true \
     --field enforce_admins=true
   ```

4. **Create GitHub Project** (if configured)
   - Go to: https://github.com/orgs/your-org/projects
   - Create new Board project
   - Add fields: Priority, Iteration, Size
   - Enable auto-add workflow

## Testing

### Test TODO Tracking

```python
# Add to any Python file
# TODO: Test the TODO tracking workflow
# FIXME: Verify issue creation
```

Push and check Actions tab for workflow run.

### Test Tasklist Tracking

Add to TASKS.md:

```markdown
- [ ] Test tasklist workflow
- [ ] Verify issue creation
```

Push and check for created issues.

### Test PR Follow-ups

1. Create a PR
2. Add review comment: "LGTM! Follow-up: add more tests"
3. Submit review
4. Check for created follow-up issue

## Troubleshooting

### Workflows Not Running

**Check**:

- Workflow files exist in `.github/workflows/`
- Workflows have correct permissions
- Actions enabled in repo settings
- No syntax errors in YAML

**Solution**:

```bash
# Validate workflow syntax
gh workflow list
gh workflow view todos.yml
```

### Issues Not Created

**Check**:

- Labels exist in repository
- No duplicate issues
- Workflow logs in Actions tab
- Token has write permissions

**Solution**:

```bash
# Check workflow logs
gh run list --workflow=todos.yml
gh run view <run-id>
```

### TODOs Not Detected

**Check**:

- Correct comment syntax
- File tracked by git
- Workflow triggered on push

**Solution**:

- Review supported TODO formats
- Check alstr/todo-to-issue-action docs
- Verify file in git index

## Best Practices

1. **Start Simple**
   - Enable one workflow at a time
   - Test thoroughly before adding more
   - Adjust configuration based on team feedback

2. **Label Hygiene**
   - Create all labels upfront
   - Use consistent colors
   - Document label meanings

3. **Issue Management**
   - Triage regularly
   - Close resolved issues promptly
   - Use milestones for planning

4. **Review Automation**
   - Monitor workflow runs
   - Adjust keywords and rules
   - Gather team feedback

5. **Documentation**
   - Keep PROJECT_MANAGEMENT.md updated
   - Document customizations
   - Share best practices with team

## Standards Compliance

This template helps achieve:

- ✅ **ISO/IEC 25010**: Maintainability through automation
- ✅ **GitHub Best Practices**: Issue templates, CODEOWNERS
- ✅ **Agile Practices**: Continuous improvement, transparency
- ✅ **DevOps**: Automation, collaboration, feedback loops

## Integration with Other Templates

This template can be combined with:

- **python-service**: Add to Python projects
- **node-service**: Add to Node.js projects
- **react-webapp**: Add to React projects
- **go-service**: Add to Go projects
- **docs-only**: Add to documentation projects

Example:

```bash
# Generate Python service
cookiecutter templates/python-service

cd my-service

# Add project management
cookiecutter templates/project-management --output-dir .
cp -r my-project/.github/* .github/
```

## Contributing

Improvements welcome! See [CONTRIBUTING.md](../../CONTRIBUTING.md).

Suggestions:

- Add more workflow examples
- Improve auto-labeling logic
- Add metrics and reporting
- Integration with other PM tools

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [TODO to Issue Action](https://github.com/alstr/todo-to-issue-action)
- [Stale Action](https://github.com/actions/stale)
- [Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Version**: 1.0.0  
**Last Updated**: 2025-10-12

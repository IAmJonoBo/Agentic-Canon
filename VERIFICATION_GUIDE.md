# Verifying Project Management Automation

This guide helps verify that all project management automation is working correctly.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Repository pushed to GitHub
- GitHub Actions enabled in repository settings

## Step 1: Set Up Labels

Run the label setup script to create all required labels:

```bash
./scripts/setup-labels.sh
```

**Expected output**:
```
🏷️  Setting up GitHub labels for project management automation...

📌 Creating Issue Type Labels...
✅ Created: bug
✅ Created: enhancement
✅ Created: task
...

✅ Label setup complete!
```

**Verify**:
```bash
gh label list
```

You should see all labels listed in `.github/LABELS.md`.

## Step 2: Test TODO Tracking

1. **Create a TODO comment** in code:

```python
# File: test_automation.py
# TODO: Test the automation system
def test_function():
    pass
```

2. **Commit and push**:

```bash
git add test_automation.py
git commit -m "test: add TODO for automation testing"
git push
```

3. **Check GitHub Actions**:

```bash
gh run list --workflow=todos.yml
```

4. **Verify issue created**:

```bash
gh issue list --label "from:todo"
```

**Expected**: A new issue titled "Test the automation system" should appear.

5. **Verify URL written back**:

Pull the changes and check that the TODO now has an issue URL:

```bash
git pull
cat test_automation.py
```

Should show:
```python
# TODO: Test the automation system https://github.com/owner/repo/issues/123
```

## Step 3: Test Tasklist Tracking

1. **Add unchecked item to TASKS.md**:

```markdown
## Test Section

- [ ] Test tasklist automation
- [ ] Another test task
```

2. **Commit and push**:

```bash
git add TASKS.md
git commit -m "test: add tasks for automation testing"
git push
```

3. **Check workflow**:

```bash
gh run list --workflow=tasklist-scan.yml
```

4. **Verify issues created**:

```bash
gh issue list --label "from:tasklist"
```

**Expected**: Two issues created with titles matching the tasks.

5. **Verify markdown updated**:

```bash
git pull
grep "Test tasklist automation" TASKS.md
```

Should show:
```markdown
- [ ] #124 Test tasklist automation
- [ ] #125 Another test task
```

## Step 4: Test PR Review Follow-ups

1. **Create a PR** (from a feature branch):

```bash
git checkout -b test-pr-automation
echo "test" > test_file.txt
git add test_file.txt
git commit -m "test: trigger PR automation"
git push -u origin test-pr-automation
gh pr create --title "Test PR Automation" --body "Testing follow-up automation"
```

2. **Add review comment** with follow-up keyword:

```bash
gh pr review --comment --body "LGTM! Follow-up: Add comprehensive tests for this feature."
```

3. **Check workflow**:

```bash
gh run list --workflow=pr-review-followup.yml
```

4. **Verify issue created**:

```bash
gh issue list --label "from:pr-review"
```

**Expected**: Issue titled "Follow-up from PR #X: Test PR Automation"

## Step 5: Test Issue Triage

1. **Create new issue**:

```bash
gh issue create --title "Test bug in authentication" --body "The login feature is broken"
```

2. **Check workflow**:

```bash
gh run list --workflow=issue-triage.yml
```

3. **Verify auto-labeling**:

```bash
gh issue view <issue-number> --json labels
```

**Expected**: Labels `needs-triage` and `bug` should be present.

4. **Check for welcome comment**:

```bash
gh issue view <issue-number>
```

**Expected**: Automated welcome comment with next steps.

## Step 6: Test Issue Templates

1. **Create issue from template**:

Go to GitHub UI → Issues → New Issue → Choose template

Or use CLI with template:

```bash
gh issue create --template bug_report.md
```

**Expected**: Template pre-fills issue with structured format.

## Step 7: Test PR Template

1. **Create PR** (will use template automatically):

```bash
gh pr create
```

**Expected**: PR description pre-filled with template checklist.

## Step 8: Test Stale Workflow

The stale workflow runs on a schedule, but you can test it manually:

1. **Trigger manually**:

```bash
gh workflow run stale.yml
```

2. **Check run**:

```bash
gh run list --workflow=stale.yml
```

**Note**: For testing, you may want to adjust `days-before-stale` to a lower value temporarily.

## Step 9: Test CLI Update Command

1. **Create project with Cruft**:

```bash
# Use Cruft instead of cookiecutter for projects that need updates
cruft create https://github.com/IAmJonoBo/Agentic-Canon --directory=templates/python-service
cd my-project
```

2. **Test update command**:

```bash
agentic-canon update
```

**Expected**: Shows "Project is up to date" or displays available updates.

## Monitoring Automation

### Check All Workflows

```bash
gh workflow list
```

### View Recent Runs

```bash
gh run list --limit 10
```

### View Specific Run Details

```bash
gh run view <run-id>
```

### Check for Failures

```bash
gh run list --status failure
```

## Troubleshooting

### Workflows Not Running

**Check**:
1. GitHub Actions enabled in repo settings
2. Workflows exist in `.github/workflows/`
3. Branch protection not blocking actions

**Fix**:
```bash
# Re-push to trigger
git commit --allow-empty -m "trigger: workflows"
git push
```

### Labels Not Working

**Check**:
```bash
gh label list | grep "from:todo"
```

**Fix**:
```bash
./scripts/setup-labels.sh
```

### Issues Not Created

**Check workflow logs**:
```bash
gh run list --workflow=todos.yml
gh run view <run-id> --log
```

**Common issues**:
- Token permissions (needs `issues: write`)
- Labels don't exist
- Duplicate issues (check by title)

### URLs Not Written Back

**Check**:
- Workflow has `contents: write` permission
- No conflicts in git
- File is tracked by git

## Clean Up Test Resources

After testing, clean up:

```bash
# Delete test files
git checkout main
git branch -D test-pr-automation
git push origin --delete test-pr-automation
rm test_automation.py test_file.txt

# Close test issues
gh issue list --json number -q '.[].number' | xargs -I {} gh issue close {}

# Or close specific test issues
gh issue close 123 124 125
```

## Success Criteria

✅ All workflows appear in Actions tab
✅ TODOs create issues automatically
✅ Tasklist items create issues with links
✅ PR reviews trigger follow-up issues
✅ New issues get auto-labeled and welcomed
✅ Issue templates work correctly
✅ PR template appears on PR creation
✅ Labels exist and are used correctly
✅ CLI update command works with Cruft projects

## Next Steps

Once verified:

1. **Configure Projects board** (optional):
   - Create Project in GitHub
   - Add "Auto-add" workflow
   - Set up Status, Priority, Iteration fields

2. **Set up branch protection** (recommended):
   - Require PR reviews
   - Require status checks
   - Enable CODEOWNERS

3. **Customize automation** (as needed):
   - Adjust stale timing in `stale.yml`
   - Modify auto-labels in `issue-triage.yml`
   - Add custom follow-up keywords in `pr-review-followup.yml`

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md) - Complete automation guide
- [.github/LABELS.md](.github/LABELS.md) - Label documentation

---

**Last Updated**: 2025-10-12

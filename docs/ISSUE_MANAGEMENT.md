# Issue Management Best Practices

This guide documents best practices for issue creation, categorization, and sprint management in Agentic Canon.

## Table of Contents

- [Issue Types](#issue-types)
- [Issue Templates](#issue-templates)
- [Labels and Categorization](#labels-and-categorization)
- [Sprint Management](#sprint-management)
- [Issue Lifecycle](#issue-lifecycle)
- [Automation](#automation)
- [Best Practices](#best-practices)

## Issue Types

### Bug Report
**Purpose:** Report defects or unexpected behavior

**When to use:**
- Something is broken or not working as expected
- Error messages or crashes
- Data corruption or loss
- Performance degradation

**Key elements:**
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Priority level

### Feature Request
**Purpose:** Propose new functionality or enhancements

**When to use:**
- Suggesting new features
- Proposing improvements to existing features
- User experience enhancements

**Key elements:**
- Problem statement (what pain point?)
- Proposed solution
- Alternative solutions considered
- Use cases
- Acceptance criteria

### Task
**Purpose:** Track concrete work items

**When to use:**
- Implementation work
- Refactoring
- Documentation updates
- Infrastructure changes
- Technical debt items

**Key elements:**
- Clear description of work
- Context and motivation
- Acceptance criteria
- Dependencies
- Effort estimate

### ADR Proposal
**Purpose:** Propose architectural decisions

**When to use:**
- Significant architectural changes
- Technology choices
- Design patterns
- Infrastructure decisions

**Key elements:**
- Decision title and context
- Problem statement
- Proposed solution
- Alternatives considered
- Impact assessment
- Stakeholders

## Issue Templates

All issue templates are in `.github/ISSUE_TEMPLATE/`:

1. **bug_report.md** - Bug reports
2. **feature_request.md** - Feature requests
3. **task.md** - Work items
4. **adr_proposal.md** - Architecture decisions
5. **config.yml** - Template configuration

### Template Features

All templates include:
- ✅ Priority selection
- ✅ Component/area categorization
- ✅ Effort estimation (for tasks)
- ✅ Related issues/ADRs linking
- ✅ Sprint/milestone assignment
- ✅ Automatic labels

## Labels and Categorization

### Label Hierarchy

```
Type Labels (what kind of work?)
├── type:bug - Bug fixes
├── type:feature - New features
└── type:task - General tasks

Component Labels (which area?)
├── component:templates - Cookiecutter templates
├── component:notebooks - Jupyter notebooks
├── component:docs - Documentation
├── component:cli - Command-line interface
├── component:ci-cd - CI/CD workflows
├── component:testing - Testing infrastructure
└── component:security - Security/compliance

Status Labels (current state?)
├── needs-triage - New, needs initial review
├── needs-review - Awaiting review
├── in-progress - Currently being worked on
├── blocked - Blocked by dependency
└── stale - Inactive

Priority Labels (how urgent?)
├── priority:high - Critical or urgent
├── priority:medium - Normal priority
└── priority:low - Nice to have

Special Labels
├── adr - Architecture Decision Record
├── architecture - Architectural work
├── security - Security issue
├── performance - Performance issue
├── documentation - Documentation work
└── critical - Critical issue
```

### Automatic Labeling

The `issue-triage.yml` workflow automatically adds labels based on:

- **Keywords in title/body:**
  - "bug", "error", "fail" → `bug`, `type:bug`
  - "feature", "enhancement" → `enhancement`, `type:feature`
  - "[ADR]" → `adr`, `architecture`
  - "security", "vulnerability" → `security`, `critical`
  - "template", "cookiecutter" → `component:templates`
  - "notebook", "jupyter" → `component:notebooks`
  - "cli" → `component:cli`

- **All new issues:** `needs-triage`

### Manual Labeling

Add labels manually for:
- Sprint/milestone assignments
- Effort estimates (if using labels)
- Additional categorization
- Cross-cutting concerns

## Sprint Management

### Sprint Structure

```
Sprint Cycle (2 weeks recommended)
├── Week 1: Planning & Execution
│   ├── Day 1: Sprint planning
│   ├── Day 2-5: Development
│   └── Day 5: Mid-sprint check
└── Week 2: Completion & Review
    ├── Day 6-9: Development
    ├── Day 9: Code freeze
    └── Day 10: Review & retrospective
```

### Sprint Planning Process

#### 1. Pre-Planning (Day -1)

```bash
# Review backlog
# - Triage new issues
# - Update priorities
# - Close stale issues
# - Check dependencies

# Review TASKS.md
# - Sync with closed issues
# - Update progress
# - Add new items
```

#### 2. Sprint Planning (Day 1)

**Agenda:**
1. Review sprint goal
2. Review velocity from last sprint
3. Select issues for sprint
4. Assign issues to team members
5. Set milestones

**Selection criteria:**
- Priority (high → low)
- Dependencies (unblocked first)
- Effort vs. capacity
- Sprint goal alignment

**Actions:**
```bash
# For each selected issue:
1. Add sprint milestone
2. Assign to team member
3. Move to "Sprint Backlog" project column
4. Add "in-progress" label when started
```

#### 3. During Sprint

**Daily:**
- Update issue progress
- Comment on blockers
- Link related PRs
- Update labels

**Mid-sprint (Day 5):**
- Review progress
- Adjust scope if needed
- Escalate blockers
- Update estimates

#### 4. Sprint Review (Day 10)

**Agenda:**
1. Demo completed work
2. Review metrics
3. Update TASKS.md
4. Close completed issues
5. Move incomplete issues to backlog

**Metrics to review:**
- Planned vs. completed
- Velocity (story points/tasks)
- Cycle time
- Bug vs. feature ratio
- Component distribution

#### 5. Retrospective

**Topics:**
- What went well?
- What could improve?
- Action items
- Process improvements

### Using GitHub Projects

#### Project Board Setup

```
Columns:
1. Backlog - All future work
2. Sprint Backlog - Selected for current sprint
3. In Progress - Actively being worked on
4. In Review - PR submitted, awaiting review
5. Done - Completed this sprint
```

#### Automation Rules

```yaml
# Move to "In Progress" when:
- Issue assigned
- Label added: "in-progress"

# Move to "In Review" when:
- PR linked and opened

# Move to "Done" when:
- Issue closed
- PR merged
```

### Sprint Metrics

Track these metrics:

1. **Velocity**
   - Tasks completed per sprint
   - Story points completed (if using)

2. **Cycle Time**
   - Time from "In Progress" to "Done"
   - Average per issue type

3. **Completion Rate**
   - Planned vs. actually completed
   - Target: 80%+

4. **Quality Metrics**
   - Bugs found in sprint
   - Bugs fixed in sprint
   - Code review time

## Issue Lifecycle

### 1. Creation

```
Issue Created
    ↓
Auto-triaged (issue-triage.yml)
    ├── Labels added
    ├── Comment posted
    └── Status: needs-triage
```

### 2. Triage

**Maintainer reviews:**
- [ ] Is this a valid issue?
- [ ] Is the information complete?
- [ ] What's the priority?
- [ ] Which component?
- [ ] Any dependencies?
- [ ] Assign to milestone?

**Actions:**
- Update labels
- Add to milestone
- Request more info (if needed)
- Close as duplicate/invalid (if applicable)
- Remove `needs-triage` label

### 3. Planning

**Add to sprint:**
- Assign to team member
- Add to project board
- Link related issues/ADRs
- Estimate effort
- Check dependencies

### 4. Implementation

**Developer actions:**
- Add `in-progress` label
- Comment on approach
- Create branch
- Link PR when ready
- Request review

### 5. Review

**Reviewer actions:**
- Review code/changes
- Test changes
- Approve or request changes
- Verify acceptance criteria

### 6. Completion

**Final steps:**
- Merge PR
- Close issue
- Update TASKS.md (automated)
- Update documentation
- Announce if significant

### 7. Follow-up

**After sprint:**
- Verify in production
- Monitor for issues
- Document learnings
- Update ADRs if needed

## Automation

### Workflows

#### 1. Issue Triage (`issue-triage.yml`)
- **Trigger:** Issue opened
- **Actions:**
  - Add labels based on content
  - Add welcome comment
  - Notify maintainers (if critical)

#### 2. Tasklist Scan (`tasklist-scan.yml`)
- **Trigger:** Push to TASKS.md
- **Actions:**
  - Create issues for unchecked items
  - Link issues in TASKS.md
  - Avoid duplicates

#### 3. Tasks and ADR Sync (`tasks-adr-sync.yml`)
- **Trigger:** Weekly schedule
- **Actions:**
  - Mark completed issues as checked
  - Find unlinked ADRs
  - Generate reports

#### 4. Stale Issues (`stale.yml`)
- **Trigger:** Daily schedule
- **Actions:**
  - Mark inactive issues as stale
  - Close after grace period
  - Exempt pinned/critical

#### 5. PR Review Followup (`pr-review-followup.yml`)
- **Trigger:** PR review submitted
- **Actions:**
  - Create issues from "Follow-up:" comments
  - Link to original PR
  - Assign to PR author

### Scripts

#### Setup Labels

```bash
# Create all required labels
.dev/scripts/setup-labels.sh

# Or manually with gh CLI
gh label create "component:templates" --color "c2e0c6"
```

## Best Practices

### ✅ Do

**Creating Issues:**
- Use appropriate template
- Provide clear, complete information
- Add screenshots/logs when relevant
- Search for duplicates first
- Link related issues/ADRs
- Set priority honestly

**Managing Issues:**
- Triage new issues within 2 days
- Update progress regularly
- Close issues when done
- Use labels consistently
- Keep TASKS.md in sync
- Link PRs to issues

**Sprint Planning:**
- Set realistic sprint goals
- Balance bug fixes and features
- Consider dependencies
- Leave buffer for unknowns
- Track velocity over time

### ❌ Don't

**Avoid:**
- Creating issues without templates
- Leaving issues in triage limbo
- Assigning issues without asking
- Forgetting to link PRs
- Closing issues without comment
- Over-committing in sprint
- Ignoring blocked issues

### Issue Hygiene

**Weekly:**
- [ ] Triage new issues
- [ ] Update in-progress issues
- [ ] Check for stale issues
- [ ] Sync TASKS.md
- [ ] Review blocked issues

**Monthly:**
- [ ] Review label usage
- [ ] Clean up old issues
- [ ] Update templates if needed
- [ ] Review automation

**Quarterly:**
- [ ] Analyze sprint metrics
- [ ] Optimize workflows
- [ ] Update documentation
- [ ] Team retrospective

## Examples

### Example 1: Bug Report Flow

```
1. User reports bug using template
   ↓
2. Auto-triaged: bug, type:bug, component:cli, needs-triage
   ↓
3. Maintainer reviews:
   - Confirms bug
   - Adds priority:high
   - Adds to current sprint
   - Assigns to developer
   ↓
4. Developer:
   - Adds in-progress label
   - Creates fix in PR
   - Links PR to issue
   ↓
5. Review and merge
   ↓
6. Issue auto-closed
   ↓
7. TASKS.md auto-updated (if tracked)
```

### Example 2: Feature Request Flow

```
1. User submits feature request
   ↓
2. Auto-triaged: enhancement, type:feature, needs-triage
   ↓
3. Maintainer reviews:
   - Discusses with team
   - Decides: requires ADR
   - Creates ADR proposal issue
   ↓
4. ADR process:
   - Draft ADR document
   - Review with stakeholders
   - Accept decision
   ↓
5. Implementation:
   - Break into tasks
   - Add to sprint
   - Track in TASKS.md
   ↓
6. Complete and close
   ↓
7. Document in CHANGELOG
```

### Example 3: Sprint Cycle

```
Week 1:
├── Monday: Sprint planning
│   - Select 10 issues
│   - Assign to team
│   - Set sprint goal
├── Tuesday-Friday: Development
│   - 6 issues in progress
│   - 2 issues completed
└── Friday: Mid-sprint check
    - On track for 8/10

Week 2:
├── Monday-Wednesday: Development
│   - 6 more issues completed
│   - 1 blocked, deferred
├── Thursday: Code freeze
│   - Final reviews
│   - Documentation
└── Friday: Review & Retro
    - 8/10 completed (80%)
    - Velocity: consistent
    - Identified blockers for next sprint
```

## Getting Help

- **Questions:** Open issue with `question` label
- **Process improvements:** Create issue with `process` label
- **Template updates:** Submit PR with changes
- **Automation issues:** Check workflow logs, create issue

## References

- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Projects Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Labels Guide](.github/LABELS.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Project Management Documentation](PROJECT_MANAGEMENT.md)

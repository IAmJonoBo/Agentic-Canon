# TASKS.md and ADR Sync Documentation

This document explains how the automated synchronization system works between TASKS.md, GitHub Issues, and Architecture Decision Records (ADRs).

## Overview

The Agentic Canon project uses an automated system to ensure that tasks, issues, and ADRs are properly linked and synchronized. This automation:

1. **Creates issues from TASKS.md** with rich metadata
2. **Syncs task completion status** from closed issues back to TASKS.md
3. **Detects unlinked ADRs** and creates tracking issues
4. **Enriches issues** with ADR references and context
5. **Maintains bidirectional links** between all artifacts

## System Components

### 1. Tasklist Scanner (`.github/workflows/tasklist-scan.yml`)

**Purpose:** Converts unchecked items in TASKS.md to GitHub Issues with full context.

**Triggers:**

- On push when markdown files change (TASKS.md, docs/\*\*/\*.md)

**What it does:**

1. **Scans TASKS.md** for unchecked items: `- [ ] Task description`
2. **Extracts metadata:**
   - Section and subsection context
   - ADR references (e.g., ADR-005, ADR-008)
   - Related issue numbers
   - Priority indicators
   - Component information
3. **Creates GitHub Issues** with:
   - Title from task description
   - Body with full context and surrounding lines
   - Related ADRs section with links
   - Source information (line number, section)
   - Appropriate labels (component, priority, type)
4. **Updates TASKS.md** to reference the issue: `- [ ] #123 Task description`
5. **Adds ADR comments** to issues with architectural context

**Example:**

Before (in TASKS.md):

```markdown
### Security Enhancements

- [ ] Implement SBOM generation for all builds (ADR-005)
```

After:

```markdown
### Security Enhancements

- [ ] #456 Implement SBOM generation for all builds (ADR-005)
```

And a new issue #456 is created with:

- Title: "Implement SBOM generation for all builds (ADR-005)"
- Body includes: section context, ADR link to ADR-005, source line number
- Labels: `task`, `from:tasklist`, `component:security`, `priority:medium`
- Comment with ADR details and guidance

### 2. Tasks and ADR Sync (`.github/workflows/tasks-adr-sync.yml`)

**Purpose:** Bidirectional sync between TASKS.md and Issues, plus ADR link management.

**Triggers:**

- Weekly schedule (Monday at 6 AM UTC)
- Manual workflow dispatch

**What it does:**

#### Part 1: Sync TASKS.md with Closed Issues

1. **Reads TASKS.md** and finds all issue references (#123)
2. **Checks each issue** to see if it's closed
3. **Marks completed items** in TASKS.md: `- [x] #123 Task description`
4. **Commits changes** back to repository

#### Part 2: Check for Unlinked ADRs

1. **Scans docs/adr/** for all ADR files
2. **Parses metadata** from each ADR:
   - Title
   - Status (proposed/accepted/deprecated/superseded)
   - Date
   - Number
3. **Checks README.md** to see if ADR is linked
4. **Creates tracking issue** if ADRs are missing from README with:
   - Full list of missing ADRs
   - Metadata for each (status, date, link)
   - Detailed checklist for updating README
   - Priority label based on ADR status

#### Part 3: Enrich Issues with ADR Metadata

1. **Finds all open issues** with `from:tasklist` label
2. **Extracts ADR references** from issue titles and TASKS.md
3. **Reads ADR files** to get full metadata
4. **Updates issue bodies** to include:
   - Related ADRs section
   - ADR titles and status
   - Links to ADR documents
   - Guidance notes

#### Part 4: Generate Sync Report

Reports on:

- TASKS.md completion percentage
- Open vs closed tasks
- ADR status breakdown (proposed, accepted, deprecated, superseded)
- Total counts and metrics

## Metadata Extraction

### From TASKS.md

The system extracts the following metadata from TASKS.md:

1. **Section Context:**
   - Main section (## heading)
   - Subsection (### heading)
   - Used to determine component and priority

2. **ADR References:**
   - Pattern: `ADR-XXX` where XXX is a 3-digit number
   - Found in task description or surrounding context
   - Used to link issues to architectural decisions

3. **Issue References:**
   - Pattern: `#123` where 123 is an issue number
   - Used for dependency tracking

4. **Priority Indicators:**
   - Section names: "High Priority", "Medium Priority", "Lower Priority"
   - Keywords: "CRITICAL", "urgent"
   - Mapped to priority labels

5. **Component Indicators:**
   - Based on section names:
     - "Template" → `component:templates`
     - "Notebook" → `component:notebooks`
     - "CLI" → `component:cli`
     - "Security" → `security`
     - "Documentation" → `component:documentation`
     - "Testing" → `component:testing`

### From ADR Files

The system extracts from ADR markdown files:

1. **Title:** From first `#` heading
2. **Status:** From `status:` metadata field
3. **Date:** From `date:` metadata field
4. **Number:** From filename `ADR-XXX-title.md`

## Issue Creation

### Automated Issue Structure

When an issue is created from TASKS.md, it includes:

```markdown
## Description

[Task description from TASKS.md]

## Context

**Section:** [Main Section] > [Subsection]

**Additional Context:**
[Up to 3 lines of context from surrounding text]

## Related ADRs

- ADR-005: [docs/adr/ADR-005.md](../docs/adr/ADR-005.md)
  - Status: accepted

## Related Issues

- #123
- #456

## Source

Created from TASKS.md (line 456)

**Automatically tracked** - This issue was created automatically from TASKS.md.
When this issue is closed, the corresponding item in TASKS.md will be marked as complete.
```

### Labels Applied

Automatically applied labels include:

- **Type:** `task`, `from:tasklist`
- **Component:** `component:templates`, `component:notebooks`, `component:cli`, etc.
- **Priority:** `priority:high`, `priority:medium`, `priority:low`
- **Topic:** `security`, `documentation`, `testing`

## Best Practices

### Writing TASKS.md Items

To get the best automatic metadata extraction:

1. **Reference ADRs explicitly:**

   ```markdown
   - [ ] Implement feature X (ADR-005, ADR-008)
   ```

2. **Use clear section headers:**

   ```markdown
   ## Version 2.0 - High Priority Features

   ### Security Enhancements

   - [ ] Task description
   ```

3. **Add context in surrounding text:**

   ```markdown
   ### Security Enhancements

   These tasks implement ADR-005 (SLSA compliance).

   - [ ] Generate SBOM for builds
   - [ ] Sign release artifacts
   ```

4. **Link related issues:**
   ```markdown
   - [ ] Complete feature Y (depends on #123)
   ```

### Creating ADRs

To ensure proper sync:

1. **Use the ADR template** with required metadata:

   ```markdown
   number: 009
   status: proposed
   date: 2025-01-15
   ```

2. **Follow naming convention:** `ADR-XXX-kebab-case-title.md`

3. **Update README.md** when merging ADRs (or let automation create a tracking issue)

4. **Reference ADRs in TASKS.md** when creating related tasks

### Managing Issues

1. **Use closing keywords** in commits/PRs:

   ```
   Fixes #123
   Closes #456
   Resolves #789
   ```

2. **Keep issue titles in sync** with TASKS.md descriptions

3. **Add ADR references** in issue descriptions when relevant

4. **Use appropriate labels** to help with organization

## Workflow Configuration

### Customizing tasklist-scan.yml

To adjust behavior:

```yaml
# Change trigger paths
on:
  push:
    paths: ["TASKS.md", "docs/**.md", "YOUR-FILE.md"]

# Adjust labels
labels: ['task', 'from:tasklist', 'your-label']

# Change component mapping (edit the script section)
if (currentSection.includes('YourSection')) {
  metadata.labels.push('component:your-component');
}
```

### Customizing tasks-adr-sync.yml

To adjust behavior:

```yaml
# Change schedule
on:
  schedule:
    - cron: "0 9 * * 1" # Monday at 9 AM instead of 6 AM

# Adjust issue creation
labels: ["adr", "documentation", "automated", "your-label"]
```

## Troubleshooting

### Issues not being created

1. Check that task items follow format: `- [ ] Description`
2. Verify workflow has write permissions for issues
3. Check workflow logs in Actions tab
4. Ensure TASKS.md is in repository root

### TASKS.md not updating

1. Check that workflow has write permissions for contents
2. Verify issue numbers are correct (#123 format)
3. Check that issues are actually closed
4. Look for conflicts in git commits

### ADR links not appearing

1. Verify ADR filename format: `ADR-XXX-title.md`
2. Check that ADR is in `docs/adr/` directory
3. Ensure ADR has proper metadata (title, status)
4. Verify issue has `from:tasklist` label

### Missing metadata in issues

1. Add more context lines around tasks in TASKS.md
2. Use explicit ADR references: `(ADR-005)`
3. Add clear section headers
4. Check that component/priority indicators are present

## Monitoring

### Check Sync Status

1. **View workflow runs:** Actions → Tasks and ADR Sync
2. **Check sync report:** In workflow logs, see completion percentage
3. **Review open issues:** Filter by `from:tasklist` label
4. **Verify ADR links:** Check for issues with `adr` + `documentation` labels

### Metrics Tracked

The sync report includes:

- Total task items in TASKS.md
- Completed vs open tasks
- Completion percentage
- Total ADRs by status
- Number of unlinked ADRs
- Issues enriched with ADR metadata

## Future Enhancements

Potential improvements to the sync system:

1. **Bidirectional sync:** Update TASKS.md when issues are modified
2. **Dependency tracking:** Parse and enforce task dependencies
3. **Milestone sync:** Sync sprint/milestone data between TASKS.md and issues
4. **ADR status tracking:** Track ADR lifecycle changes
5. **Dashboard:** Create a web dashboard for visualization
6. **Notifications:** Slack/email alerts for important changes
7. **Historical tracking:** Track completion velocity and trends

## Related Documentation

- [PROJECT_MANAGEMENT.md](../PROJECT_MANAGEMENT.md) - Full project management strategy
- [ADR-ISSUE-MANAGEMENT-IMPLEMENTATION.md](../ADR-ISSUE-MANAGEMENT-IMPLEMENTATION.md) - Implementation details
- [docs/adr/README.md](adr/README.md) - ADR index and guidelines
- [docs/adr/ADR-LIFECYCLE.md](adr/ADR-LIFECYCLE.md) - ADR lifecycle management
- [.github/LABELS.md](../.github/LABELS.md) - Label taxonomy

## Support

For issues with the sync system:

1. Check workflow logs in GitHub Actions
2. Review this documentation
3. Open an issue with the `automation` label
4. Reference relevant workflow runs and error messages

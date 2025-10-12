# TASKS.md and ADR Sync - Quick Reference

This is a quick reference for the automated TASKS.md and ADR synchronization system.

For complete documentation, see [docs/TASKS-ADR-SYNC.md](../docs/TASKS-ADR-SYNC.md).

## System Overview

The repository maintains **bidirectional sync** between:
- **TASKS.md** - Single source of truth for implementation tracking
- **GitHub Issues** - Individual trackable work items
- **ADRs** - Architecture Decision Records in `docs/adr/`

## Workflows

### 1. Tasklist Scanner (`.github/workflows/tasklist-scan.yml`)

**Trigger:** On push to markdown files  
**What it does:**
- Scans TASKS.md for unchecked items: `- [ ] Task description`
- Extracts metadata: ADR refs, section context, priority
- Creates GitHub Issues with rich body
- Updates TASKS.md: `- [ ] #123 Task description`

**Example:**
```markdown
### Security (ADR-005)
- [ ] Generate SBOM for builds
```
→ Creates issue #456 with ADR-005 link, security label, context

### 2. Tasks and ADR Sync (`.github/workflows/tasks-adr-sync.yml`)

**Trigger:** Weekly (Monday 6 AM UTC) + manual  
**What it does:**
- Syncs completed issues → TASKS.md: `- [x] #123 Done`
- Detects unlinked ADRs → creates tracking issues
- Enriches existing issues with ADR metadata
- Generates status reports

## How to Use

### Writing Tasks in TASKS.md

✅ **Good - Explicit ADR references:**
```markdown
## Version 2.0 - High Priority

### Security Enhancements
Implement ADR-005 (SLSA) and ADR-008 (dependencies).

- [ ] Generate SBOM for builds
- [ ] Sign release artifacts (ADR-005)
```

✅ **Good - Clear sections:**
```markdown
## High Priority Features
### Templates
- [ ] Add Python service template
### Security
- [ ] Implement secret scanning
```

### Closing Tasks

Use GitHub keywords in commits/PRs:
```
Fixes #123
Closes #456
Resolves #789
```

The next weekly sync will mark these as `[x]` in TASKS.md.

### Creating ADRs

1. Use `.dev/scripts/create-adr.sh` for new ADRs
2. Name files: `ADR-XXX-kebab-case.md`
3. Include metadata:
   ```markdown
   number: 009
   status: proposed
   date: 2025-01-15
   ```
4. Link from README or wait for auto-tracking issue

## Metadata Extraction

The system automatically extracts:

| Metadata | How | Example |
|----------|-----|---------|
| ADR refs | Pattern `ADR-XXX` in title/context | `ADR-005` → links to ADR file |
| Priority | Section name | "High Priority" → `priority:high` |
| Component | Subsection name | "Security" → `security` label |
| Context | Surrounding lines | Up to 5 lines before task |

## Labels Applied

Automatically applied labels:

- **Type:** `task`, `from:tasklist`
- **Component:** `component:templates`, `component:cli`, `component:documentation`, etc.
- **Priority:** `priority:high`, `priority:medium`, `priority:low`
- **Topic:** `security`, `performance`, `documentation`

## Issue Structure

Auto-created issues include:

```markdown
## Description
[Task from TASKS.md]

## Context
**Section:** Version 2.0 > Security
**Additional Context:** [Lines before task]

## Related ADRs
- ADR-005: [link](../docs/adr/ADR-005.md)
  - Status: accepted

## Source
Created from TASKS.md (line 456)
```

## Troubleshooting

### Issues not creating?
- Check format: `- [ ] Description` (space in brackets)
- Verify workflow permissions (issues: write)
- Check Actions tab for errors

### TASKS.md not updating?
- Verify issues are actually closed
- Check weekly sync ran (Actions tab)
- Look for merge conflicts

### ADR links missing?
- Verify ADR filename: `ADR-XXX-title.md`
- Check ADR is in `docs/adr/`
- Wait for weekly sync or trigger manually

## Manual Trigger

Trigger workflows manually:
1. Go to Actions tab
2. Select "Tasks and ADR Sync" or "Tasklists → Issues"
3. Click "Run workflow"
4. Select branch and run

## Status Monitoring

Check sync status:
- **Workflow runs:** Actions → "Tasks and ADR Sync"
- **Completion:** Workflow logs show % complete
- **Open tasks:** Issues with `from:tasklist` label
- **Unlinked ADRs:** Issues with `adr` + `documentation` labels

## Related Files

- [docs/TASKS-ADR-SYNC.md](../docs/TASKS-ADR-SYNC.md) - Complete documentation
- [docs/adr/ADR-LIFECYCLE.md](../docs/adr/ADR-LIFECYCLE.md) - ADR lifecycle guide
- [docs/ISSUE_MANAGEMENT.md](../docs/ISSUE_MANAGEMENT.md) - Issue management guide
- [PROJECT_MANAGEMENT.md](../PROJECT_MANAGEMENT.md) - Project management strategy
- [TASKS.md](../TASKS.md) - Implementation tracker

## Support

For issues or questions:
1. Check [docs/TASKS-ADR-SYNC.md](../docs/TASKS-ADR-SYNC.md) troubleshooting section
2. Review workflow logs in Actions tab
3. Open an issue with `automation` label

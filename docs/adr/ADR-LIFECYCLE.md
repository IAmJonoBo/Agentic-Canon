# ADR Lifecycle Management Guide

This guide explains how to manage Architecture Decision Records (ADRs) throughout their lifecycle.

## ADR Lifecycle States

```
┌──────────┐
│ Proposed │  ← New ADR created
└────┬─────┘
     │
     ├─→ Review & Discussion
     │   - Stakeholder feedback
     │   - Technical review
     │   - Impact assessment
     │
     ▼
┌──────────┐
│ Accepted │  ← Decision approved
└────┬─────┘
     │
     ├─→ Implementation
     │   - Code changes
     │   - Documentation updates
     │   - Fitness functions deployed
     │
     ▼
┌──────────┐     ┌────────────┐
│ Active   │────→│ Deprecated │  ← No longer recommended
└────┬─────┘     └────────────┘     but not replaced
     │
     ▼
┌────────────┐
│ Superseded │  ← Replaced by newer ADR
└────────────┘
```

## Creating a New ADR

### Using the Script (Recommended)

```bash
# Run the ADR creation script
.dev/scripts/create-adr.sh

# Follow the prompts:
# 1. Enter title (e.g., "Use PostgreSQL for primary database")
# 2. Select status (proposed/accepted/deprecated/superseded)
# 3. Enter decision makers
# 4. Provide problem statement

# The script will:
# - Generate next ADR number automatically
# - Create file from template
# - Open in your editor
```

### Manual Creation

```bash
# 1. Copy the template
cp templates/architecture/adr/template.md docs/adr/ADR-009-your-decision.md

# 2. Edit the file and replace all {{ PLACEHOLDERS }}
# 3. Update metadata section with correct information
# 4. Fill in all required sections
```

### Using GitHub Issue Template

1. Go to repository issues
2. Click "New Issue"
3. Select "Architecture Decision Record (ADR) Proposal"
4. Fill in the template
5. After discussion and approval, convert to ADR document

## ADR Review Process

### 1. Proposal Phase

**Status:** `proposed`

**Activities:**
- Create ADR document with all sections filled
- Open PR with ADR
- Tag stakeholders for review
- Hold discussion sessions if needed
- Gather feedback and update ADR

**Checklist:**
- [ ] All sections completed (no placeholder text)
- [ ] Alternatives analyzed and documented
- [ ] Impact assessment complete
- [ ] Standards compliance verified
- [ ] Stakeholders identified
- [ ] Review meeting scheduled

### 2. Review Phase

**Duration:** Typically 1-2 weeks

**Activities:**
- Stakeholder review
- Technical review
- Security review (if applicable)
- Performance analysis (if applicable)
- Cost analysis

**Review Checklist:**
- [ ] Technical feasibility confirmed
- [ ] Security implications assessed
- [ ] Performance impact analyzed
- [ ] Cost implications understood
- [ ] Operational complexity evaluated
- [ ] Migration path defined
- [ ] Rollback plan exists

### 3. Decision Phase

**Activities:**
- Final stakeholder meeting
- Address any remaining concerns
- Make go/no-go decision
- Update ADR status

**Outcomes:**
- **Accepted:** Move to implementation
- **Rejected:** Close PR, document reasoning
- **Deferred:** Update ADR, revisit later

### 4. Implementation Phase

**Status:** `accepted`

**Activities:**
- Implement the decision
- Update relevant documentation
- Deploy fitness functions
- Monitor implementation
- Communicate changes

**Implementation Checklist:**
- [ ] Code changes completed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Fitness functions deployed
- [ ] Team trained/informed
- [ ] Monitoring in place

## Updating ADRs

### When to Update

- **Add context:** New information discovered
- **Document impact:** Actual outcomes vs. expected
- **Add references:** Related decisions or documents
- **Update fitness functions:** Adjust thresholds or checks

### How to Update

```bash
# 1. Create a branch
git checkout -b update-adr-005

# 2. Edit the ADR
vim docs/adr/ADR-005-original-decision.md

# 3. Add "Updates" section at the end
## Updates

### 2025-01-15: Performance Impact

Initial implementation revealed higher latency than expected...

# 4. Commit and PR
git add docs/adr/ADR-005-original-decision.md
git commit -m "docs: update ADR-005 with performance findings"
git push origin update-adr-005
```

## Deprecating ADRs

### When to Deprecate

An ADR should be deprecated when:
- The decision is no longer recommended
- Better alternatives exist
- Technology has evolved
- BUT: No specific replacement exists yet

### How to Deprecate

```bash
# 1. Edit the ADR
vim docs/adr/ADR-003-old-decision.md

# 2. Update metadata
status: deprecated

# 3. Add deprecation notice
## Deprecation Notice

**Deprecated Date:** 2025-01-20
**Reason:** This approach is no longer recommended due to...
**Alternatives:** Consider ADR-009 or ADR-012 instead

# 4. Update README
vim docs/adr/README.md
# Move the ADR link to "Deprecated ADRs" section

# 5. Commit
git add docs/adr/ADR-003-old-decision.md docs/adr/README.md
git commit -m "docs: deprecate ADR-003"
```

## Superseding ADRs

### When to Supersede

An ADR should be superseded when:
- A new decision explicitly replaces it
- The new approach is incompatible with the old one
- The context has fundamentally changed

### How to Supersede

```bash
# 1. Create new ADR
.dev/scripts/create-adr.sh
# Title: "Use Alternative Approach" (the new decision)

# 2. In NEW ADR, reference the old one
supersedes: [003]

## Context
This decision supersedes ADR-003 because...

# 3. Update OLD ADR
vim docs/adr/ADR-003-old-decision.md

# Update metadata
status: superseded
superseded_by: 009

# Add supersession notice
## Supersession Notice

**Superseded Date:** 2025-01-20
**Superseded By:** ADR-009
**Reason:** This decision has been replaced by...

# 4. Update README
vim docs/adr/README.md
# Move old ADR to "Superseded ADRs" section
# Add new ADR to appropriate section

# 5. Commit both
git add docs/adr/ADR-003-old-decision.md docs/adr/ADR-009-new-decision.md docs/adr/README.md
git commit -m "docs: supersede ADR-003 with ADR-009"
```

## Linking ADRs

### In TASKS.md

```markdown
- [x] #123 Implement database migration (ADR-005)
- [ ] #145 Deploy caching layer (ADR-007)
```

### In Issues

```markdown
## Related ADRs

- Implements: ADR-005
- Depends on: ADR-003
- Related: ADR-007
```

### In Code

```python
# Implementation follows ADR-005: Use PostgreSQL for primary database
# See: docs/adr/ADR-005-postgresql-database.md
def connect_database():
    ...
```

### In PRs

```markdown
## Architecture Decision

This PR implements ADR-009: Use Redis for caching

**ADR Status:** Accepted
**Implementation Progress:** 75%

See [ADR-009](../docs/adr/ADR-009-redis-caching.md) for rationale and design.
```

## Review Schedule

### Regular Reviews

**Frequency:** Annually or when triggered

**Triggers:**
- Annual architecture review
- Major technology changes
- Performance issues
- Security incidents
- Compliance requirements change

**Process:**
1. Review all `accepted` ADRs
2. Assess if decisions are still valid
3. Check fitness functions are passing
4. Update or deprecate as needed
5. Document review in ADR

### Review Checklist

For each ADR:
- [ ] Is the decision still valid?
- [ ] Are fitness functions passing?
- [ ] Have assumptions changed?
- [ ] Are there better alternatives now?
- [ ] Is documentation still accurate?
- [ ] Should status be updated?

### Review Template

Add to ADR:

```markdown
## Reviews

### Review 2025-01-20

**Reviewer:** John Doe
**Status:** Still valid
**Findings:**
- Fitness functions passing
- Performance within expectations
- No changes needed

**Next Review:** 2026-01-20
```

## Automation

### Workflows

The following workflows help manage ADRs:

1. **ADR Validation** (`.github/workflows/adr-validation.yml`)
   - Validates ADR format
   - Checks for placeholder text
   - Verifies numbering sequence
   - Runs on PR and push

2. **Tasks and ADR Sync** (`.github/workflows/tasks-adr-sync.yml`)
   - Syncs TASKS.md with closed issues
   - Checks for unlinked ADRs and creates tracking issues
   - Enriches issues with ADR metadata
   - Generates comprehensive status reports
   - Runs weekly (Monday 6 AM UTC)
   - See [TASKS-ADR-SYNC.md](../TASKS-ADR-SYNC.md) for details

3. **Tasklist Scanner** (`.github/workflows/tasklist-scan.yml`)
   - Creates GitHub Issues from TASKS.md items
   - Extracts ADR references and metadata
   - Links tasks to relevant ADRs automatically
   - Runs on push to markdown files
   - See [TASKS-ADR-SYNC.md](../TASKS-ADR-SYNC.md) for details

4. **Documentation Sanity Check** (`.github/workflows/doc-sanity-check.yml`)
   - Verifies ADR README consistency
   - Checks for missing ADRs
   - Runs on push and schedule

### Scripts

- **`.dev/scripts/create-adr.sh`** - Interactive ADR creation
- **`.dev/scripts/validate-adrs.sh`** - Validate ADR format locally

### Automated Synchronization

The project maintains automated bidirectional sync between TASKS.md, GitHub Issues, and ADRs:

- **Task → Issue**: Unchecked items in TASKS.md automatically create issues with ADR links
- **Issue → Task**: Closed issues update TASKS.md completion status
- **ADR → Issue**: Missing ADR links trigger tracking issues with full metadata
- **Issue Enrichment**: Open issues get updated with related ADR information

For complete documentation on the sync system, see [TASKS-ADR-SYNC.md](../TASKS-ADR-SYNC.md).

## Best Practices

### ✅ Do

- Write ADRs for significant architectural decisions
- Keep ADRs concise and focused
- Update ADRs when you learn something new
- Link ADRs to issues and PRs
- Review ADRs regularly
- Use fitness functions to validate decisions
- Involve stakeholders early
- Document alternatives considered
- Be honest about trade-offs

### ❌ Don't

- Write ADRs for trivial decisions
- Leave placeholder text in ADRs
- Forget to update README when adding ADRs
- Skip the review process
- Change accepted ADRs without discussion
- Delete old ADRs (deprecate or supersede instead)
- Make decisions without considering alternatives
- Forget to communicate decisions to the team

## Examples

### Example 1: Full Lifecycle

```bash
# Day 1: Create proposal
.dev/scripts/create-adr.sh
# Title: Use GraphQL for API layer
# Status: proposed

# Day 3-10: Review period
# - Stakeholders provide feedback
# - Update ADR with new information
# - Hold review meeting

# Day 11: Accept decision
vim docs/adr/ADR-009-graphql-api.md
# Change status to "accepted"

# Day 12-30: Implementation
# - Build GraphQL schema
# - Implement resolvers
# - Deploy fitness functions
# - Update documentation

# Month 12: Annual review
# - Check fitness functions
# - Assess if decision still valid
# - Document review findings
```

### Example 2: Superseding

```bash
# Scenario: ADR-003 decided to use REST API
# Now we want to use GraphQL instead

# Create new ADR
.dev/scripts/create-adr.sh
# Title: Use GraphQL for API layer
# In ADR: supersedes: [003]

# Update old ADR
vim docs/adr/ADR-003-rest-api.md
# Change status to "superseded"
# Add superseded_by: 009

# Both ADRs now show the relationship clearly
```

## Getting Help

- **Questions:** Open a discussion or issue with the `question` label
- **Proposals:** Use the ADR Proposal issue template
- **Review requests:** Tag `@architecture-team` in PR
- **Documentation:** See `docs/adr/README.md` and this guide

## References

- [ADR Template](../../templates/architecture/adr/template.md)
- [Architecture Templates README](../../templates/architecture/README.md)
- [CONVENTIONS.md - ADR Section](../../CONVENTIONS.md#architecture-decision-records-adrs)
- [Michael Nygard's ADR Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)

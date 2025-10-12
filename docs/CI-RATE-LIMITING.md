# GitHub Actions Rate Limiting Strategy

## Overview

This document describes the rate limiting strategy implemented in Agentic Canon's automated workflows to prevent hitting GitHub API rate limits.

## Background

GitHub API has rate limits for authenticated requests:
- **REST API**: 5,000 requests per hour per user
- **Search API**: 30 requests per minute
- **Secondary Rate Limits**: Additional limits on concurrent requests and mutation operations

When workflows create multiple issues or make many API calls in rapid succession, they can trigger rate limiting, causing workflow failures.

## Implementation

### Rate Limiting in tasklist-scan.yml

The `tasklist-scan.yml` workflow converts unchecked items in TASKS.md to GitHub Issues. To prevent rate limiting:

#### 1. Batch Size Limiting
```javascript
const MAX_ISSUES_PER_RUN = 10;

if (tasks.length > MAX_ISSUES_PER_RUN) {
  console.log(`⚠️  Limiting to ${MAX_ISSUES_PER_RUN} issues per run`);
  tasks.length = MAX_ISSUES_PER_RUN;
}
```

**Rationale**: Limits each workflow run to creating a maximum of 10 issues. Remaining tasks will be processed in subsequent runs.

#### 2. Delays Between API Calls
```javascript
const DELAY_BETWEEN_CALLS = 2000; // 2 seconds

if (issuesCreated > 0) {
  await delay(DELAY_BETWEEN_CALLS);
}
```

**Rationale**: Adds a 2-second delay between issue creation operations to spread out API requests.

#### 3. Retry Logic with Exponential Backoff
```javascript
let retries = 3;
let created = null;
while (retries > 0 && !created) {
  try {
    created = await github.rest.issues.create({...});
  } catch (error) {
    retries--;
    if (retries > 0 && (error.status === 403 || error.status === 429)) {
      console.log(`⚠️  Rate limited, waiting 60 seconds...`);
      await delay(60000);
    } else {
      throw error;
    }
  }
}
```

**Rationale**: 
- Retries failed API calls up to 3 times
- Waits 60 seconds when rate limited (403 or 429 status)
- Allows workflow to recover from temporary rate limits

#### 4. Error Handling
```javascript
try {
  // Create issue
} catch (error) {
  console.log(`❌ Failed to create issue: ${error.message}`);
  continue; // Skip and continue with next task
}
```

**Rationale**: Individual failures don't stop the entire workflow, allowing partial progress.

### Rate Limiting in tasks-adr-sync.yml

The `tasks-adr-sync.yml` workflow syncs TASKS.md with closed issues and enriches issues with ADR metadata.

#### 1. Batch Processing
```javascript
const MAX_ISSUES_PER_RUN = 20;

if (issues.length > MAX_ISSUES_PER_RUN) {
  console.log(`⚠️  Limiting to ${MAX_ISSUES_PER_RUN} issues per run`);
  issues.length = MAX_ISSUES_PER_RUN;
}
```

**Rationale**: Processes maximum 20 issues per run for enrichment operations.

#### 2. Delays Between Operations
```javascript
const DELAY_BETWEEN_CALLS = 1000; // 1 second

if (enriched > 0) {
  await delay(DELAY_BETWEEN_CALLS);
}
```

**Rationale**: Adds 1-second delay between issue update operations.

#### 3. Early Exit on Rate Limit
```javascript
catch (error) {
  console.log(`⚠️  Failed to update issue: ${error.message}`);
  if (error.status === 403 || error.status === 429) {
    console.log(`⚠️  Rate limited, stopping enrichment`);
    break; // Exit loop to prevent further rate limit errors
  }
}
```

**Rationale**: Stops processing immediately when rate limited, allowing next scheduled run to continue.

## Best Practices

### 1. Monitor Workflow Runs
Check the Actions tab regularly for:
- Rate limit warnings in logs
- Failed API calls
- Partial completion messages

### 2. Adjust Parameters as Needed
If you frequently hit rate limits, consider:
- Reducing `MAX_ISSUES_PER_RUN`
- Increasing `DELAY_BETWEEN_CALLS`
- Running workflows less frequently

### 3. Schedule Workflows Wisely
- `tasklist-scan.yml`: Runs on push to TASKS.md
- `tasks-adr-sync.yml`: Runs weekly on Monday at 6 AM

Avoid triggering multiple runs simultaneously.

### 4. Use [skip ci] in Commits
When workflows commit back to the repository, they use `[skip ci]` to prevent triggering themselves:

```yaml
git commit -m "chore: track checklist items as issues [skip ci]"
```

## Troubleshooting

### Symptom: "API rate limit exceeded" Error

**Cause**: Too many API requests in a short time.

**Solution**:
1. Check recent workflow runs to see if multiple ran simultaneously
2. Wait 10-60 minutes for rate limit to reset
3. Manually trigger workflow with `workflow_dispatch` when needed

### Symptom: Workflow Partially Completes Tasks

**Cause**: Batch size limit or rate limiting kicked in.

**Solution**:
1. This is expected behavior - remaining tasks will process in next run
2. For immediate processing, manually trigger another run
3. Check logs for "Limiting to X issues per run" message

### Symptom: Issues Not Created Despite Unchecked Items

**Cause**: Issues may already exist or workflow hit error.

**Solution**:
1. Check if issues with same titles exist
2. Review workflow logs for errors
3. Verify TASKS.md syntax is correct

### Symptom: ADR Enrichment Incomplete

**Cause**: Rate limit during enrichment process.

**Solution**:
1. Wait for next scheduled run (weekly)
2. Manually trigger `tasks-adr-sync.yml` via workflow_dispatch
3. Issues will be enriched gradually over multiple runs

## Monitoring

### Key Metrics to Track

1. **Issues Created per Run**: Should not exceed 10 (tasklist-scan)
2. **Issues Enriched per Run**: Should not exceed 20 (tasks-adr-sync)
3. **Workflow Duration**: Should increase with more items (due to delays)
4. **Failure Rate**: Should be near 0% with proper rate limiting

### Logging

Workflows log rate limiting activities:
```
⚠️  Limiting to 10 issues per run to avoid rate limits
   Remaining 15 items will be processed in next run
```

```
⚠️  Rate limited, waiting 60 seconds... (2 retries left)
```

Look for these messages in the Actions logs.

## Configuration Reference

### tasklist-scan.yml Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MAX_ISSUES_PER_RUN` | 10 | Maximum issues created per run |
| `DELAY_BETWEEN_CALLS` | 2000ms | Delay between API calls |
| `retries` | 3 | Number of retry attempts |
| `retry delay` | 60000ms | Wait time when rate limited |

### tasks-adr-sync.yml Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MAX_ISSUES_PER_RUN` | 20 | Maximum issues processed per run |
| `DELAY_BETWEEN_CALLS` | 1000ms | Delay between operations |

## Future Improvements

Potential enhancements to consider:

1. **Adaptive Rate Limiting**: Adjust delays based on remaining rate limit quota
2. **Queue System**: Persist unprocessed tasks between runs
3. **Parallel Processing**: Use GitHub App tokens for higher rate limits
4. **Metrics Dashboard**: Track rate limit usage over time
5. **Smart Scheduling**: Avoid peak usage times

## References

- [GitHub REST API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [GitHub Actions Usage Limits](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)
- [Secondary Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#secondary-rate-limits)
- [Best Practices for Integrators](https://docs.github.com/en/rest/guides/best-practices-for-integrators)

---

**Last Updated**: 2025-10-12  
**Version**: 1.0  
**Status**: Active

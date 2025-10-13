# Grafana Dashboards for Agentic Canon

This directory contains Grafana dashboard JSON files for monitoring key metrics aligned with Agentic Canon standards.

## Available Dashboards

### DORA Metrics Dashboard

**File**: `dora-metrics.json`

Tracks the four key DORA (DevOps Research and Assessment) metrics:

1. **Deployment Frequency**
   - How often deployments occur
   - Target: Multiple times per day (elite)
   - Thresholds: Daily (green), Weekly (yellow), Monthly (red)

2. **Lead Time for Changes**
   - Time from commit to production
   - Target: < 1 day (elite)
   - Thresholds: < 1 day (green), < 1 week (yellow), > 1 week (red)

3. **Change Failure Rate**
   - Percentage of changes causing failures
   - Target: < 15% (elite)
   - Thresholds: < 15% (green), 15-30% (yellow), > 30% (red)

4. **Mean Time to Recovery (MTTR)**
   - Time to recover from failures
   - Target: < 1 hour (elite)
   - Thresholds: < 1 hour (green), < 1 day (yellow), > 1 day (red)

### SPACE Metrics Dashboard

**File**: `space-metrics.json`

Tracks developer experience and productivity using the SPACE framework:

1. **Satisfaction**: Developer satisfaction scores (1-5 scale)
2. **Performance**: Throughput metrics (PRs per developer/week)
3. **Activity**: Commits, reviews, and contributions
4. **Communication & Collaboration**: PR review times
5. **Efficiency & Flow**: Time in flow state, build times, context switches

## Setup Instructions

### 1. Import Dashboard

```bash
# Using Grafana API
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @dora-metrics.json \
  https://your-grafana-instance/api/dashboards/db
```

### 2. Configure Data Sources

These dashboards assume Prometheus as the data source with the following metrics:

**DORA Metrics:**

- `deployments_total` - Counter of deployments
- `failed_deployments_total` - Counter of failed deployments
- `lead_time_seconds` - Histogram of lead times
- `mttr_seconds` - Histogram of recovery times

**SPACE Metrics:**

- `developer_satisfaction_score` - Gauge from surveys (1-5)
- `pull_requests_merged` - Counter of merged PRs
- `commits_total` - Counter of commits
- `code_reviews_total` - Counter of code reviews
- `pr_review_time_seconds` - Histogram of review times
- `flow_state_percentage` - Gauge of flow time percentage
- `ci_pipeline_duration_seconds` - Histogram of CI durations
- `context_switches_per_day` - Gauge of context switches

### 3. Instrumenting Your Applications

Add instrumentation to export these metrics from your CI/CD pipeline and VCS:

```python
# Python example using prometheus_client
from prometheus_client import Counter, Histogram

deployments = Counter('deployments_total', 'Total deployments')
lead_time = Histogram('lead_time_seconds', 'Lead time from commit to deploy')

# Record metrics
deployments.inc()
lead_time.observe(deployment_duration)
```

## Customization

### Adjusting Thresholds

Edit the `thresholds` in each panel's `fieldConfig` to match your organization's targets:

```json
"thresholds": {
  "steps": [
    {"value": 0, "color": "green"},
    {"value": 24, "color": "yellow"},
    {"value": 168, "color": "red"}
  ]
}
```

### Adding Additional Panels

Follow the panel structure and add custom metrics relevant to your team.

## Best Practices

1. **Review Regularly**: Schedule weekly/monthly reviews of these metrics
2. **Set Baselines**: Establish baseline metrics before optimization
3. **Iterate**: Use insights to drive continuous improvement
4. **Team Visibility**: Make dashboards accessible to all team members
5. **Correlate Metrics**: Look for relationships between DORA and SPACE metrics

## References

- [DORA Metrics](https://www.devops-research.com/research.html)
- [SPACE Framework](https://queue.acm.org/detail.cfm?id=3454124)
- [Grafana Documentation](https://grafana.com/docs/)

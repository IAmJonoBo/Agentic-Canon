# Grafana Dashboard Templates

This directory contains Grafana dashboard JSON templates for monitoring software delivery and developer experience metrics.

## Available Dashboards

### 1. DORA Metrics Dashboard (`dora-metrics.json`)
Track the four key DevOps Research and Assessment (DORA) metrics:
- **Deployment Frequency**: How often you deploy to production
- **Lead Time for Changes**: Time from commit to production
- **Mean Time to Recovery (MTTR)**: Time to restore service after incident
- **Change Failure Rate**: Percentage of deployments causing failures

### 2. SPACE/DevEx Metrics Dashboard (`space-devex-metrics.json`)
Developer experience and productivity metrics:
- **Satisfaction**: Developer satisfaction scores
- **Performance**: Code review time, build time, test execution time
- **Activity**: Commits, PRs, code reviews
- **Communication & Collaboration**: PR interactions, review participation
- **Efficiency & Flow**: Flow time, blocked time, context switches

### 3. Security Metrics Dashboard (`security-metrics.json`)
Security posture and vulnerability tracking:
- SAST findings over time
- Secret scanning results
- Dependency vulnerabilities
- SBOM coverage
- Time to remediation

### 4. Quality Metrics Dashboard (`quality-metrics.json`)
Code quality and testing metrics:
- Test coverage trends
- Mutation test scores
- Code duplication
- Technical debt
- Bug density
- Code smells

## Installation

### Prerequisites

1. **Grafana** (v9.0+) installed and running
2. **Prometheus** as data source (or your preferred time-series DB)
3. **Exporters** configured to send metrics to Prometheus

### Import Dashboard

1. Open Grafana UI
2. Navigate to Dashboards → Import
3. Upload the JSON file or paste its contents
4. Select your Prometheus data source
5. Click Import

### Configure Data Sources

Update the datasource UID in each dashboard JSON:

```json
{
  "datasource": {
    "type": "prometheus",
    "uid": "YOUR_PROMETHEUS_UID"
  }
}
```

## Metrics Collection

### DORA Metrics

**Deployment Frequency:**
```promql
# Count deployments per day
sum(increase(deployments_total[24h]))
```

**Lead Time:**
```promql
# Average time from commit to deploy
histogram_quantile(0.5, rate(lead_time_seconds_bucket[1h]))
```

**MTTR:**
```promql
# Average time to recover from incidents
avg(incident_resolution_time_seconds) by (severity)
```

**Change Failure Rate:**
```promql
# Percentage of failed deployments
sum(failed_deployments_total) / sum(deployments_total) * 100
```

### SPACE Metrics

**Build Time:**
```promql
# Average build duration
avg(build_duration_seconds) by (project)
```

**PR Review Time:**
```promql
# Time from PR open to merge
histogram_quantile(0.95, rate(pr_review_duration_seconds_bucket[1h]))
```

**Flow Time:**
```promql
# Time from start to done
avg(issue_flow_time_seconds) by (team)
```

## Instrumentation

### Python Example (using Prometheus client)

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# DORA: Deployment counter
deployments = Counter('deployments_total', 'Total deployments', ['environment', 'status'])

# DORA: Lead time histogram
lead_time = Histogram('lead_time_seconds', 'Lead time from commit to deploy')

# SPACE: Build time histogram
build_time = Histogram('build_duration_seconds', 'Build duration')

# Example usage
def deploy(environment):
    start = time.time()
    try:
        # Deployment logic
        deployments.labels(environment=environment, status='success').inc()
    except Exception as e:
        deployments.labels(environment=environment, status='failure').inc()
    finally:
        lead_time.observe(time.time() - start)

def build():
    with build_time.time():
        # Build logic
        pass
```

### GitHub Actions Integration

Collect metrics from GitHub Actions:

```yaml
- name: Report Deployment Metric
  run: |
    curl -X POST http://pushgateway:9091/metrics/job/deployments \
      -d "deployments_total{environment=\"prod\",status=\"success\"} 1"
```

## Alerting Rules

### Prometheus Alerting Rules

Create `alerts.yml`:

```yaml
groups:
  - name: dora_metrics
    interval: 5m
    rules:
      - alert: HighChangeFailureRate
        expr: |
          (sum(failed_deployments_total) / sum(deployments_total)) > 0.15
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Change failure rate above 15%"
          description: "{{ $value }}% of deployments are failing"

      - alert: SlowLeadTime
        expr: |
          histogram_quantile(0.95, rate(lead_time_seconds_bucket[1h])) > 86400
        for: 2h
        labels:
          severity: warning
        annotations:
          summary: "Lead time exceeds 24 hours"
          description: "P95 lead time is {{ $value }}s"

      - alert: LowDeploymentFrequency
        expr: |
          sum(increase(deployments_total[24h])) < 1
        for: 48h
        labels:
          severity: info
        annotations:
          summary: "No deployments in 48 hours"
```

## Dashboard Variables

Each dashboard supports variables for filtering:

- **Environment**: dev, staging, production
- **Team**: engineering team name
- **Project**: specific project/service
- **Time Range**: Configurable time window

## Customization

### Adding Custom Metrics

1. Add metric queries in dashboard JSON:
```json
{
  "targets": [
    {
      "expr": "your_custom_metric",
      "legendFormat": "{{ label }}",
      "refId": "A"
    }
  ]
}
```

2. Update panel titles and descriptions
3. Adjust thresholds and colors
4. Save dashboard

### Changing Data Source

Update the datasource configuration:
```json
{
  "datasource": {
    "type": "prometheus",  // or "loki", "elasticsearch", etc.
    "uid": "YOUR_UID"
  }
}
```

## Best Practices

1. **Set Baselines**: Establish baseline metrics before optimization
2. **Track Trends**: Focus on trends over absolute values
3. **Team Context**: Compare teams to themselves, not others
4. **Regular Reviews**: Review dashboards weekly in team meetings
5. **Action-Oriented**: Each metric should drive specific actions
6. **Celebrate Wins**: Highlight improvements and successes

## DORA Performance Levels

### Elite Performers
- Deployment Frequency: On-demand (multiple per day)
- Lead Time: Less than one day
- MTTR: Less than one hour
- Change Failure Rate: 0-15%

### High Performers
- Deployment Frequency: Between once per day and once per week
- Lead Time: Between one day and one week
- MTTR: Less than one day
- Change Failure Rate: 0-15%

### Medium Performers
- Deployment Frequency: Between once per week and once per month
- Lead Time: Between one week and one month
- MTTR: Between one day and one week
- Change Failure Rate: 0-15%

### Low Performers
- Deployment Frequency: Fewer than once per month
- Lead Time: More than one month
- MTTR: More than one week
- Change Failure Rate: >15%

## Resources

- [DORA Research](https://dora.dev/)
- [SPACE Framework Paper](https://queue.acm.org/detail.cfm?id=3454124)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

## Contributing

To add a new dashboard:

1. Create the dashboard in Grafana UI
2. Export as JSON
3. Clean up datasource references
4. Add variables for reusability
5. Document required metrics and setup
6. Add example queries and alerts

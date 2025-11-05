# Runbook: Incident Response

## Purpose

This runbook provides procedures for responding to production incidents in systems built with Agentic Canon templates. It covers detection, triage, resolution, and post-incident activities.

## Incident Severity Levels

| Level    | Description                | Response Time        | Examples                                                 |
| -------- | -------------------------- | -------------------- | -------------------------------------------------------- |
| **SEV1** | Critical - Complete outage | Immediate (< 15 min) | Complete service down, data loss, security breach        |
| **SEV2** | High - Major degradation   | 30 minutes           | Partial outage, significant performance degradation      |
| **SEV3** | Medium - Minor impact      | 2 hours              | Limited functionality affected, minor performance issues |
| **SEV4** | Low - Minimal impact       | Next business day    | Cosmetic issues, documentation errors                    |

## Incident Response Phases

1. **Detection** - Identify the incident
2. **Triage** - Assess severity and impact
3. **Communication** - Notify stakeholders
4. **Investigation** - Determine root cause
5. **Resolution** - Fix the issue
6. **Recovery** - Restore normal operations
7. **Post-Incident** - Review and learn

## Phase 1: Detection

### Monitoring and Alerting

**Automated Detection Sources**:

- Prometheus/Grafana alerts
- OpenTelemetry metrics anomalies
- Error rate spikes in logs
- Health check failures
- User reports

**Manual Detection Sources**:

- Customer support tickets
- Social media mentions
- Team observations
- Scheduled tests failing

### Initial Actions

**Duration**: 1-5 minutes

**Steps**:

1. **Acknowledge Alert**

   ```bash
   # Acknowledge in PagerDuty/OpsGenie
   # Or silence alert temporarily
   ```

2. **Verify Incident**

   ```bash
   # Check service health
   curl https://api.example.com/health

   # Check metrics dashboard
   # Open Grafana and check key metrics

   # Check recent deployments
   kubectl rollout status deployment/my-app
   ```

3. **Document Start Time**
   ```bash
   # Create incident ticket
   gh issue create \
     --title "[INCIDENT] Service degradation" \
     --label incident,sev2 \
     --body "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```

**Validation**: Incident confirmed and documented

## Phase 2: Triage

### Assess Severity

**Duration**: 2-5 minutes

**Decision Tree**:

```
Is the service completely down?
├─ YES → SEV1
└─ NO → Continue

Are multiple users affected?
├─ YES → Is functionality critical?
│         ├─ YES → SEV2
│         └─ NO → SEV3
└─ NO → SEV4
```

**Quick Triage Commands**:

```bash
# Check error rates
kubectl logs deployment/my-app --tail=100 | grep ERROR | wc -l

# Check request success rate
curl https://metrics.example.com/query?query=rate(http_requests_total[5m])

# Check latency
curl https://metrics.example.com/query?query=http_request_duration_seconds

# Check active users affected
# Check analytics or monitoring dashboard
```

**Validation**: Severity level assigned

### Assess Impact

**Questions to Answer**:

- How many users are affected?
- Which features/services are impacted?
- What is the business impact?
- Are there data integrity concerns?
- Is there a security component?

**Document Impact**:

```markdown
## Impact Assessment

- **Affected Users**: ~1000 (10% of total)
- **Affected Services**: Authentication, API
- **Business Impact**: Cannot process orders
- **Data Integrity**: No concerns
- **Security**: No security implications
```

## Phase 3: Communication

### Initial Communication

**Duration**: 5 minutes

**SEV1/SEV2 Notifications**:

```bash
# Notify on-call team
# Send to Slack incident channel
slack-cli send --channel incidents \
  --message "🚨 SEV2 INCIDENT: API degradation. Investigation in progress."

# Create status page update
# Update https://status.example.com
```

**Communication Template**:

```markdown
🚨 **INCIDENT NOTIFICATION**

**Severity**: SEV2
**Status**: Investigating
**Impact**: API response times degraded (>2s)
**Affected**: ~10% of users
**Started**: 2024-01-15 14:30 UTC
**Incident Lead**: @engineer

We are aware of the issue and actively investigating.
Updates will be provided every 15 minutes.
```

### Stakeholder Communication

**SEV1**:

- Immediate notification to executive team
- Status page update
- Social media if customer-facing

**SEV2**:

- Notify product/engineering leadership
- Status page update
- Internal communication

**SEV3/SEV4**:

- Team notification only
- No status page update needed

### Regular Updates

**Update Frequency**:

- **SEV1**: Every 15 minutes
- **SEV2**: Every 30 minutes
- **SEV3**: Every 2 hours
- **SEV4**: As needed

**Update Template**:

```markdown
⏱️ **UPDATE [14:45 UTC]**

**Status**: Still investigating
**Progress**: Identified high database query latency as likely cause
**Next Steps**: Analyzing slow query logs, preparing index optimization
**ETA**: Resolution expected within 30 minutes
```

## Phase 4: Investigation

### Gather Information

**Duration**: 10-30 minutes (varies by incident)

**System Health Checks**:

```bash
# 1. Check pod/container status
kubectl get pods -n production
kubectl describe pod <pod-name> -n production

# 2. Check resource utilization
kubectl top pods -n production
kubectl top nodes

# 3. Check recent events
kubectl get events -n production --sort-by='.lastTimestamp'

# 4. Check application logs
kubectl logs deployment/my-app -n production --tail=500

# 5. Check database
# Connect to database and check:
# - Connection count
# - Long-running queries
# - Lock contention
# - Table sizes

# 6. Check external dependencies
curl -v https://api.external-service.com/health

# 7. Check network
kubectl exec -it <pod-name> -- nslookup database.internal
kubectl exec -it <pod-name> -- curl http://dependency:8080/health
```

**OpenTelemetry Traces**:

```bash
# Query traces in Jaeger/Grafana Tempo
# Look for:
# - High latency spans
# - Error spans
# - Abnormal trace patterns

# Example query in Grafana
{
  "query": "service:my-app AND error:true",
  "time_range": "last 15m"
}
```

**Metrics Analysis**:

Check Grafana dashboards for:

- Request rate changes
- Error rate spikes
- Latency increases
- Resource utilization
- Database metrics
- Cache hit rates

**Recent Changes**:

```bash
# Check recent deployments
kubectl rollout history deployment/my-app -n production

# Check recent commits
git log --oneline --since="2 hours ago"

# Check recent configuration changes
kubectl get configmap -n production -o yaml
kubectl get secret -n production
```

### Formulate Hypotheses

**Common Root Causes**:

1. **Recent Deployment**
   - New bug introduced
   - Configuration error
   - Resource limit changes

2. **Resource Exhaustion**
   - Memory leak
   - CPU saturation
   - Disk space full
   - Connection pool exhausted

3. **External Dependencies**
   - Third-party API down
   - Database overloaded
   - Network connectivity issues

4. **Traffic Spike**
   - DDoS attack
   - Viral content
   - Bot traffic

5. **Data Issues**
   - Corrupt data
   - Large payload
   - Infinite loop scenario

**Validation**: Top 2-3 hypotheses identified

## Phase 5: Resolution

### Quick Mitigation Strategies

**Duration**: 5-30 minutes

**1. Rollback Recent Deployment**

```bash
# Kubernetes
kubectl rollout undo deployment/my-app -n production

# Verify rollback
kubectl rollout status deployment/my-app -n production

# AWS Lambda
aws lambda update-function-code \
  --function-name my-app \
  --s3-bucket my-bucket \
  --s3-key previous-version.zip
```

**2. Scale Resources**

```bash
# Scale up replicas
kubectl scale deployment/my-app --replicas=10 -n production

# Increase resource limits
kubectl set resources deployment/my-app \
  --limits=cpu=2,memory=4Gi \
  -n production
```

**3. Restart Services**

```bash
# Rolling restart
kubectl rollout restart deployment/my-app -n production

# Force pod restart
kubectl delete pod <pod-name> -n production
```

**4. Enable Circuit Breaker**

```bash
# Temporarily disable problematic feature
kubectl set env deployment/my-app FEATURE_X_ENABLED=false

# Or use feature flag system
curl -X POST https://feature-flags.example.com/api/flags/feature-x/disable
```

**5. Route Traffic Away**

```bash
# Update ingress to maintenance page
kubectl apply -f maintenance-mode.yaml

# Or use load balancer
# Route traffic to static maintenance page
```

**6. Database Optimization**

```sql
-- Kill long-running queries
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active' AND query_start < NOW() - INTERVAL '5 minutes';

-- Add missing index (if safe)
CREATE INDEX CONCURRENTLY idx_table_column ON table(column);
```

**7. Clear Cache**

```bash
# Redis
redis-cli FLUSHALL

# Application cache
kubectl exec -it <pod-name> -- curl -X POST http://localhost:8080/admin/cache/clear
```

### Permanent Fix

**Duration**: Varies (30 minutes to several hours)

**Steps**:

1. **Develop Fix**
   - Write code to address root cause
   - Add tests to prevent regression
   - Test in staging environment

2. **Deploy Fix**

   ```bash
   # Create hotfix branch
   git checkout -b hotfix/incident-20240115

   # Make changes, commit
   git commit -m "fix: resolve database query performance issue"

   # Deploy via CI/CD or manually
   git push origin hotfix/incident-20240115
   ```

3. **Verify Fix**
   ```bash
   # Check metrics returning to normal
   # Check error rates dropping
   # Check user reports resolving
   ```

**Validation**: Metrics returned to normal, no errors

## Phase 6: Recovery

### Verification Steps

**Duration**: 15-30 minutes

**Checklist**:

```bash
# 1. All services healthy
kubectl get pods -n production
# All pods should be Running

# 2. Health checks passing
curl https://api.example.com/health
# Should return 200 OK

# 3. Error rates normal
# Check Grafana dashboard
# Error rate < 0.1%

# 4. Latency normal
# Check p95 latency
# Should be < 200ms

# 5. No alerts firing
# Check Prometheus/Grafana
# All alerts should be green

# 6. User reports resolved
# Check support tickets
# Recent complaints resolved
```

**Monitor for Regression**:

```bash
# Set up watch on key metrics
watch -n 60 'curl -s https://metrics.example.com/health | jq .status'

# Monitor logs for errors
kubectl logs -f deployment/my-app | grep -i error
```

**Validation**: All metrics normal for 15+ minutes

### Declare Incident Resolved

**Actions**:

1. **Update Status Page**

   ```markdown
   ✅ **RESOLVED**

   The incident has been resolved. All services are operating normally.
   We will continue to monitor the situation.

   **Duration**: 45 minutes
   **Root Cause**: Database query performance (details to follow in post-mortem)
   ```

2. **Notify Stakeholders**

   ```bash
   slack-cli send --channel incidents \
     --message "✅ INCIDENT RESOLVED: All services restored. Post-mortem to follow."
   ```

3. **Close Incident Ticket**
   ```bash
   gh issue close <issue-number> \
     --comment "Incident resolved at $(date -u +%Y-%m-%dT%H:%M:%SZ). Post-mortem scheduled."
   ```

## Phase 7: Post-Incident Review

### Immediate Actions (Same Day)

**Duration**: 1 hour

**Steps**:

1. **Preserve Evidence**

   ```bash
   # Save logs
   kubectl logs deployment/my-app -n production --since=2h > incident-logs.txt

   # Export metrics
   # Take screenshots of dashboards

   # Save traces
   # Export relevant traces from Jaeger/Tempo
   ```

2. **Create Post-Mortem Document**

   ```markdown
   # Post-Mortem: API Degradation - 2024-01-15

   ## Summary

   Brief description of the incident

   ## Timeline

   - 14:30 UTC: Alert triggered
   - 14:35 UTC: Incident declared (SEV2)
   - 14:45 UTC: Root cause identified
   - 15:00 UTC: Fix deployed
   - 15:15 UTC: Incident resolved

   ## Impact

   - Duration: 45 minutes
   - Users affected: ~1000 (10%)
   - Requests failed: ~5000
   - Revenue impact: $500 estimated

   ## Root Cause

   Detailed explanation of what went wrong

   ## Resolution

   How the issue was resolved

   ## What Went Well

   - Quick detection via automated alerts
   - Effective communication
   - Fast rollback capability

   ## What Could Be Improved

   - Better database monitoring
   - More comprehensive testing
   - Improved documentation

   ## Action Items

   - [ ] Add database query performance monitoring
   - [ ] Implement slow query alerting
   - [ ] Add integration tests for this scenario
   - [ ] Update runbook with learnings
   ```

3. **Schedule Post-Mortem Meeting**
   - Within 2 business days
   - Include all responders
   - Blameless culture focus

### Post-Mortem Meeting

**Duration**: 1 hour

**Agenda**:

1. **Review Timeline** (10 min)
   - Walk through events chronologically
   - Clarify any confusion

2. **Root Cause Analysis** (20 min)
   - Use 5 Whys technique
   - Identify contributing factors
   - Document systemic issues

3. **What Went Well** (10 min)
   - Celebrate successes
   - Identify processes that worked

4. **What Could Be Improved** (15 min)
   - Identify gaps and weaknesses
   - Brainstorm improvements

5. **Action Items** (5 min)
   - Assign owners and due dates
   - Prioritize items

**5 Whys Example**:

```
Problem: API was slow

Why? → Database queries were slow
Why? → Missing index on frequently queried column
Why? → Index was not added during recent migration
Why? → Migration review process didn't catch performance implications
Why? → No automated performance testing for migrations

Root Cause: Lack of automated performance testing for database migrations
```

### Action Items and Follow-Up

**Create GitHub Issues**:

```bash
# Create action items
gh issue create \
  --title "Add database query performance monitoring" \
  --label "incident-followup,priority:high" \
  --assignee @engineer \
  --body "From incident 2024-01-15: Add monitoring for slow queries"

gh issue create \
  --title "Implement automated migration performance tests" \
  --label "incident-followup,priority:high" \
  --body "Prevent future incidents by testing migration performance"
```

**Track Progress**:

```bash
# Weekly review of action items
gh issue list --label incident-followup
```

**Update Documentation**:

- Add learnings to this runbook
- Update architecture diagrams if needed
- Improve monitoring dashboards
- Enhance alerting rules

## Incident Response Tools

### Essential Tools

1. **Communication**
   - Slack/Teams incident channel
   - Status page (StatusPage.io, Atlassian)
   - PagerDuty/OpsGenie

2. **Monitoring**
   - Grafana dashboards
   - Prometheus alerts
   - OpenTelemetry traces (Jaeger/Tempo)
   - Log aggregation (ELK, Loki)

3. **Infrastructure**
   - kubectl (Kubernetes)
   - Cloud provider CLI (aws, az, gcloud)
   - Docker
   - Git

4. **Databases**
   - Database client (psql, mysql, etc.)
   - Query analyzers
   - Backup/restore tools

### Command Reference

**Quick Reference Card**:

```bash
# Check service health
curl https://api.example.com/health

# View recent logs
kubectl logs deployment/my-app --tail=100 -n production

# Check pod status
kubectl get pods -n production

# Rollback deployment
kubectl rollout undo deployment/my-app -n production

# Scale deployment
kubectl scale deployment/my-app --replicas=5 -n production

# Check metrics
curl https://metrics.example.com/api/v1/query?query=up

# Restart pods
kubectl rollout restart deployment/my-app -n production
```

## Best Practices

### During Incident

1. **Stay Calm**: Clear thinking is essential
2. **Communicate Clearly**: Regular updates reduce anxiety
3. **Document Everything**: Timeline, commands, observations
4. **Focus on Recovery**: Blame can wait
5. **Escalate When Needed**: Don't hesitate to ask for help
6. **Follow Runbook**: Don't improvise unless necessary

### After Incident

1. **Blameless Post-Mortem**: Focus on systems, not people
2. **Act on Learnings**: Implement action items
3. **Share Knowledge**: Update documentation
4. **Practice**: Run game days to test procedures
5. **Iterate**: Continuously improve processes

## References

- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)
- [Post-Mortem Templates](https://github.com/dastergon/postmortem-templates)

---

_For incident support, contact the on-call engineer via PagerDuty or Slack._

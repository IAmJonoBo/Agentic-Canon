---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 04 Observability & SLOs

This notebook covers:
- OpenTelemetry instrumentation
- Traces, metrics, and logs
- SLI/SLO definitions
- Error budgets
- Dashboards and alerting

```{code-cell} ipython3
:tags: [parameters]

# Parameters cell for Papermill
run_mode = "interactive"
```

## OpenTelemetry Overview

OpenTelemetry provides a unified observability framework for traces, metrics, and logs.

```{code-cell} ipython3
otel_components = {
    "SDK": "Instrument your application",
    "API": "Language-agnostic interface",
    "Collector": "Receive, process, and export telemetry",
    "Exporters": "Send data to backends (Jaeger, Prometheus, etc.)",
    "Auto-instrumentation": "Zero-code instrumentation for popular frameworks"
}

print("OpenTelemetry Components:")
for component, desc in otel_components.items():
    print(f"  • {component}: {desc}")
```

## The Three Pillars of Observability

### 1. Traces
Track requests across service boundaries

```{code-cell} ipython3
trace_example = """
Trace Example:

TraceID: abc123...
├─ Span: API Gateway (100ms)
│  ├─ Span: Auth Service (20ms)
│  └─ Span: User Service (70ms)
│     ├─ Span: Database Query (50ms)
│     └─ Span: Cache Lookup (5ms)

Benefits:
- Identify bottlenecks
- Debug latency issues
- Understand service dependencies
"""

print(trace_example)
```

### 2. Metrics
Quantitative measurements over time

```{code-cell} ipython3
metric_types = {
    "Counter": "Monotonically increasing (e.g., request count)",
    "Gauge": "Point-in-time value (e.g., CPU usage)",
    "Histogram": "Distribution of values (e.g., request duration)",
    "Summary": "Aggregated statistics (e.g., percentiles)"
}

print("Metric Types:")
for mtype, desc in metric_types.items():
    print(f"  • {mtype}: {desc}")

print("\nCommon Metrics:")
print("  - Request rate (requests/sec)")
print("  - Error rate (errors/sec or %)")
print("  - Latency (p50, p95, p99)")
print("  - Saturation (CPU, memory, disk)")
```

### 3. Logs
Structured event records

```{code-cell} ipython3
import json

structured_log = {
    "timestamp": "2024-01-01T12:00:00Z",
    "level": "ERROR",
    "message": "Database connection failed",
    "service": "user-service",
    "trace_id": "abc123",
    "span_id": "def456",
    "error": {
        "type": "ConnectionError",
        "message": "Connection timeout after 5s"
    },
    "context": {
        "user_id": "12345",
        "endpoint": "/api/users"
    }
}

print("Structured Log Example:")
print(json.dumps(structured_log, indent=2))

print("\nBest Practices:")
print("  • Use structured logging (JSON)")
print("  • Include trace/span IDs for correlation")
print("  • Add contextual information")
print("  • Avoid PII in logs")
```

## SLI/SLO/SLA Framework

Define and track service reliability targets.

```{code-cell} ipython3
sli_slo_example = {
    "service": "user-api",
    "slis": [
        {
            "name": "Availability",
            "description": "Percentage of successful requests",
            "measurement": "(successful_requests / total_requests) * 100"
        },
        {
            "name": "Latency",
            "description": "Request duration",
            "measurement": "p95 latency in milliseconds"
        }
    ],
    "slos": [
        {
            "sli": "Availability",
            "target": "99.9%",
            "window": "30 days"
        },
        {
            "sli": "Latency",
            "target": "< 200ms",
            "percentile": "p95",
            "window": "30 days"
        }
    ]
}

print("SLI/SLO Example:")
print(json.dumps(sli_slo_example, indent=2))

print("\nDefinitions:")
print("  • SLI (Service Level Indicator): A quantitative measure")
print("  • SLO (Service Level Objective): Target range for SLI")
print("  • SLA (Service Level Agreement): Contractual commitment")
```

## Error Budgets

Balance reliability and feature velocity using error budgets.

```{code-cell} ipython3
# Error budget calculation
slo_target = 99.9  # 99.9% availability
days_in_month = 30
minutes_in_month = days_in_month * 24 * 60

# Allowed downtime
error_budget_percent = 100 - slo_target
error_budget_minutes = minutes_in_month * (error_budget_percent / 100)

print(f"SLO Target: {slo_target}%")
print(f"Error Budget: {error_budget_percent}%")
print(f"Allowed Downtime: {error_budget_minutes:.2f} minutes/month")
print(f"                  {error_budget_minutes/60:.2f} hours/month")

print("\nError Budget Policy:")
print("  • 100% budget remaining: Full speed ahead")
print("  • 50% budget remaining: Review change velocity")
print("  • 0% budget remaining: Feature freeze, focus on reliability")
print("  • Negative budget: Incident response, postmortem required")
```

## Dashboards & Alerting

Visualize and alert on key metrics.

```{code-cell} ipython3
dashboard_structure = """
Golden Signals Dashboard:

1. Latency
   - p50, p95, p99 request duration
   - Breakdown by endpoint

2. Traffic
   - Requests per second
   - Breakdown by method/endpoint

3. Errors
   - Error rate (%)
   - Error count by type

4. Saturation
   - CPU utilization
   - Memory usage
   - Queue depth
"""

print(dashboard_structure)

alerting_rules = [
    "High error rate: > 1% for 5 minutes",
    "High latency: p95 > 500ms for 5 minutes",
    "SLO burn rate: Burning error budget 10x faster than acceptable",
    "Service unavailable: 0 healthy instances"
]

print("\nAlerting Rules:")
for rule in alerting_rules:
    print(f"  • {rule}")
```

```{code-cell} ipython3
print(f"Observability & SLOs notebook complete! (mode: {run_mode})")
```

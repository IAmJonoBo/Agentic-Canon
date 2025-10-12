# Observability Templates

OpenTelemetry configuration and SLO/SLI definition templates for comprehensive service observability.

## Purpose

These templates enable production-ready observability with distributed tracing, metrics collection, log aggregation, and SLO-based reliability engineering following ISO/IEC 25010 standards.

## Contents

### 📊 OpenTelemetry (`otel/`)

OpenTelemetry Collector configuration for vendor-neutral telemetry collection.

**File:** [`collector-config.yaml`](otel/collector-config.yaml)

**Features:**
- Multi-protocol receivers (OTLP gRPC/HTTP, Prometheus)
- Host metrics collection (CPU, memory, disk, network)
- Intelligent processing (batching, sampling, filtering)
- PII removal and data sanitization
- Multiple exporters (Prometheus, Jaeger, Logging)
- Resource attribute enrichment
- Memory limits and backpressure handling

**Receivers:**
- **OTLP** - Native OpenTelemetry protocol (gRPC:4317, HTTP:4318)
- **Prometheus** - Scrape metrics from exporters
- **Host Metrics** - System-level metrics (CPU, memory, disk, network)

**Processors:**
- **Batch** - Reduce API calls (10s timeout, 1024 batch size)
- **Memory Limiter** - Prevent OOM (512 MiB limit, 128 MiB spike)
- **Resource** - Add environment, namespace attributes
- **Attributes** - Remove PII (email, password, credit card, SSN)

**Exporters:**
- **Logging** - Console output for debugging
- **Prometheus** - Metrics export (port 8889)
- **Jaeger** - Distributed tracing
- **OTLP** - Forward to backend (optional)

**Usage:**
```bash
# Copy configuration
cp templates/observability/otel/collector-config.yaml otel-collector-config.yaml

# Customize environment
sed -i 's/{{ ENVIRONMENT }}/production/g' otel-collector-config.yaml
sed -i 's/{{ NAMESPACE }}/my-service/g' otel-collector-config.yaml

# Run collector with Docker
docker run -p 4317:4317 -p 4318:4318 -p 8889:8889 \
  -v $(pwd)/otel-collector-config.yaml:/etc/otel/config.yaml \
  otel/opentelemetry-collector:latest \
  --config=/etc/otel/config.yaml

# Or with Kubernetes
kubectl apply -f otel-collector-deployment.yaml
```

**Application Integration:**

**Node.js:**
```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: 'my-service',
});

sdk.start();
```

**Python:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
```

### 🎯 SLO Definitions (`slo/`)

Service Level Objectives, Indicators, and Error Budget management.

**File:** [`slo-definition.yaml`](slo/slo-definition.yaml)

**Features:**
- Availability SLO (99.9% uptime)
- Latency SLO (P95 < 300ms)
- Error Rate SLO (< 0.1% errors)
- Error budget tracking and burn rate alerts
- Multi-window alerting (1h, 6h, 24h)
- Progressive delivery integration
- Automated reporting
- Incident impact tracking

**SLO Components:**

**1. Availability SLO**
- **Target:** 99.9% (43.8 minutes downtime/month)
- **SLI Query:** Success rate from HTTP requests
- **Error Budget:** 10% buffer (4.38 minutes)
- **Burn Rate Alerts:** Critical (1h), High (6h), Medium (24h)

**2. Latency SLO**
- **Target:** P95 < 300ms
- **SLI Query:** 95th percentile response time
- **Error Budget:** 5% buffer
- **Compliance:** ISO/IEC 25010 Performance Efficiency

**3. Error Rate SLO**
- **Target:** < 0.1% error rate
- **SLI Query:** 5xx errors / total requests
- **Error Budget:** 10% buffer
- **Compliance:** ISO/IEC 25010 Reliability

**Error Budget Policy:**
- **100% consumed** → Block deployments, page on-call
- **75% consumed** → Slow rollouts, increase monitoring
- **50% consumed** → Alert team, review changes

**Usage:**
```bash
# Copy SLO definition
cp templates/observability/slo/slo-definition.yaml slo-config.yaml

# Customize for your service
sed -i 's/{{ SERVICE_NAME }}/my-service/g' slo-config.yaml
sed -i 's/{{ TEAM_NAME }}/platform-team/g' slo-config.yaml
sed -i 's/{{ TIER }}/tier-1/g' slo-config.yaml

# Generate Prometheus rules
./scripts/generate-slo-rules.sh slo-config.yaml > prometheus-slo-rules.yml

# Validate Prometheus rules
promtool check rules prometheus-slo-rules.yml

# Apply to Prometheus
kubectl apply -f prometheus-slo-rules.yml
```

**Prometheus Alerting Rules:**
```yaml
groups:
  - name: slo_alerts
    rules:
      - alert: HighErrorBudgetBurnRate
        expr: |
          (1 - slo:availability:ratio_rate1h) > 
          14.4 * (1 - 0.999)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error budget burn rate"
          description: "Burning {{ $value }}x faster than acceptable"

      - alert: SLOViolation
        expr: slo:availability:ratio_rate30d < 0.999
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "SLO violation detected"
          description: "Availability {{ $value }}, below 99.9%"
```

## Quick Start

### Complete Observability Setup

```bash
# 1. Set up OpenTelemetry Collector
cp templates/observability/otel/collector-config.yaml otel-config.yaml
# Edit environment and namespace

# 2. Deploy collector
docker-compose up -d otel-collector
# Or: kubectl apply -f otel-collector.yaml

# 3. Configure application instrumentation
# See language-specific examples above

# 4. Define SLOs
cp templates/observability/slo/slo-definition.yaml slos.yaml
# Edit service, team, and targets

# 5. Generate monitoring rules
./scripts/generate-slo-rules.sh slos.yaml

# 6. Set up dashboards
# Import Grafana dashboards for SLOs and metrics

# 7. Configure alerting
# Set up PagerDuty/Slack integration
```

### Kubernetes Deployment

```yaml
# otel-collector-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
spec:
  replicas: 2
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector:latest
        ports:
        - containerPort: 4317  # OTLP gRPC
        - containerPort: 4318  # OTLP HTTP
        - containerPort: 8889  # Prometheus metrics
        volumeMounts:
        - name: config
          mountPath: /etc/otel
      volumes:
      - name: config
        configMap:
          name: otel-collector-config
---
apiVersion: v1
kind: Service
metadata:
  name: otel-collector
spec:
  selector:
    app: otel-collector
  ports:
  - name: otlp-grpc
    port: 4317
  - name: otlp-http
    port: 4318
  - name: metrics
    port: 8889
```

## Best Practices

### OpenTelemetry

1. **Start with auto-instrumentation** - Easiest path to observability
2. **Use semantic conventions** - Consistent attribute naming
3. **Sample intelligently** - Head-based or tail-based sampling
4. **Batch exports** - Reduce backend load
5. **Set resource attributes** - Service name, version, environment
6. **Remove PII** - Use processors to sanitize data
7. **Monitor the collector** - Self-observability
8. **Use consistent naming** - Follow OpenTelemetry conventions

### SLOs/SLIs

1. **User-centric SLOs** - Measure what users experience
2. **Start simple** - Availability, latency, error rate
3. **Set realistic targets** - Based on historical data
4. **Error budgets** - Use for decision making
5. **Multi-window alerts** - Catch fast and slow burns
6. **Document exceptions** - When to bypass error budget
7. **Review regularly** - Adjust targets quarterly
8. **Incident integration** - Track impact on error budget

### Dashboards and Alerting

1. **RED method** - Rate, Errors, Duration for services
2. **USE method** - Utilization, Saturation, Errors for resources
3. **Alert on symptoms** - Not on causes
4. **Reduce noise** - Tune alert thresholds
5. **Actionable alerts** - Include runbook links
6. **Escalation policies** - Define on-call rotation
7. **Dashboard hierarchy** - Overview → Service → Detail

## Integration Examples

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Service SLO Dashboard",
    "panels": [
      {
        "title": "Availability",
        "targets": [{
          "expr": "slo:availability:ratio_rate30d * 100"
        }],
        "thresholds": [
          {"value": 99.9, "color": "green"},
          {"value": 99.5, "color": "yellow"},
          {"value": 0, "color": "red"}
        ]
      },
      {
        "title": "Error Budget Remaining",
        "targets": [{
          "expr": "slo:error_budget:remaining_percent"
        }]
      },
      {
        "title": "Burn Rate (1h)",
        "targets": [{
          "expr": "slo:availability:burn_rate_1h"
        }]
      }
    ]
  }
}
```

### Progressive Delivery with Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-service
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-service
  analysis:
    interval: 1m
    threshold: 5
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
    - name: error-budget
      thresholdRange:
        min: 10  # At least 10% budget remaining
      interval: 1m
```

## Monitoring Stack

### Recommended Stack

**Metrics:**
- **Prometheus** - Time-series database
- **Grafana** - Visualization and dashboards
- **Alertmanager** - Alert routing and silencing

**Traces:**
- **Jaeger** - Distributed tracing backend
- **Tempo** - Scalable tracing backend (Grafana)

**Logs:**
- **Loki** - Log aggregation (Grafana)
- **Elasticsearch** - Full-text search
- **Fluentd/Fluent Bit** - Log forwarding

**All-in-one:**
- **Grafana Cloud** - Managed observability
- **Datadog** - Commercial platform
- **New Relic** - Commercial platform

## Standards Compliance

These templates help achieve compliance with:

- ✅ **ISO/IEC 25010** - Software quality (Reliability, Performance)
- ✅ **SRE Principles** - Google SRE best practices
- ✅ **OpenTelemetry** - Vendor-neutral observability
- ✅ **DORA Metrics** - DevOps performance indicators

## Additional Resources

### OpenTelemetry
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)
- [Collector Configuration](https://opentelemetry.io/docs/collector/configuration/)
- [Language SDKs](https://opentelemetry.io/docs/instrumentation/)

### SLOs/SRE
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [SLO Generator](https://github.com/google/slo-generator)

### Related Templates
- [CI/CD Templates](../cicd/README.md) - Performance testing
- [Security Templates](../security/README.md) - Security metrics
- [Video Tutorial: Observability](../../examples/video-tutorials/05-observability-setup.md)

## Contributing

To improve these templates:
1. Share your observability configurations
2. Add platform-specific examples
3. Contribute dashboard JSON files
4. Document monitoring patterns
5. Submit PRs with improvements

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

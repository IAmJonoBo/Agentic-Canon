# ADR-004: OpenTelemetry for Observability

## Status

Accepted

## Context

Modern distributed systems require comprehensive observability to understand system behavior, troubleshoot issues, and ensure reliability. We need to instrument our generated applications with:

1. **Traces**: Request flows across services and components
2. **Metrics**: Quantitative measurements (latency, throughput, errors)
3. **Logs**: Discrete event records with context
4. **Correlation**: Ability to correlate traces, metrics, and logs

Several observability solutions were considered:

- Vendor-specific SDKs (Datadog, New Relic, Dynatrace)
- OpenTelemetry (vendor-neutral standard)
- Custom instrumentation
- Language-specific solutions (Prometheus client, APM libraries)
- Cloud provider solutions (CloudWatch, Application Insights, Cloud Trace)

## Decision

We will use **OpenTelemetry** as the standard observability framework for all templates, with language-specific SDKs and auto-instrumentation where available.

## Rationale

### Why OpenTelemetry?

1. **Vendor Neutral**: Not locked to specific observability vendor
2. **Industry Standard**: CNCF project with wide industry adoption
3. **Unified API**: Single SDK for traces, metrics, and logs
4. **Auto-Instrumentation**: Automatic instrumentation for popular frameworks
5. **Extensibility**: Plugin architecture for custom instrumentation
6. **Multi-Language**: SDKs for Python, Node.js, Go, Java, .NET, and more
7. **Backwards Compatible**: Works with existing Prometheus, Jaeger, Zipkin
8. **Future-Proof**: Active development and broad community support
9. **OTLP Protocol**: Standard protocol for telemetry data export

### Implementation Approach

#### Python Services

```python
# OpenTelemetry with automatic instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
```

#### Node.js Services

```typescript
// OpenTelemetry with automatic instrumentation
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

#### Go Services

```go
// OpenTelemetry with manual instrumentation
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
)

// Setup
exporter, _ := otlptracegrpc.New(ctx)
tp := trace.NewTracerProvider(trace.WithBatcher(exporter))
otel.SetTracerProvider(tp)
```

### Collector Configuration

All templates will include OpenTelemetry Collector configuration for:

- Receiving telemetry (OTLP, Jaeger, Zipkin, Prometheus)
- Processing (batching, filtering, sampling)
- Exporting to backends (Prometheus, Jaeger, cloud vendors)

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
  memory_limiter:

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  otlp:
    endpoint: jaeger:4317
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp, logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
```

### Integration Points

1. **Templates**: All service templates include OTel setup
2. **Notebooks**: Notebook `04_observability_slos.ipynb` demonstrates setup
3. **Examples**: Example projects show real-world usage
4. **Dashboards**: Grafana dashboards visualize OTel metrics
5. **Alerts**: Prometheus alerting rules use OTel metrics
6. **SLOs**: Service Level Objectives based on OTel data

## Consequences

### Positive

- **Flexibility**: Can switch observability backends without changing instrumentation
- **Consistency**: Same approach across all languages and templates
- **Automatic**: Auto-instrumentation reduces manual work
- **Standard**: Industry-standard approach improves interoperability
- **Correlation**: Built-in trace context propagation
- **Performance**: Efficient batching and sampling reduce overhead
- **Community**: Large ecosystem of integrations and exporters
- **Future-Proof**: Active CNCF project with long-term support

### Negative

- **Complexity**: Additional dependency and configuration
- **Learning Curve**: Teams must learn OpenTelemetry concepts
- **Overhead**: Some runtime overhead from instrumentation
- **Configuration**: Requires collector setup and configuration
- **Version Management**: Must keep OTel SDKs updated
- **Debugging**: Distributed tracing adds complexity when debugging

### Mitigation Strategies

1. **Documentation**: Comprehensive guides in notebooks and examples
2. **Defaults**: Sensible default configurations in templates
3. **Sampling**: Intelligent sampling to reduce overhead
4. **Toggles**: Optional instrumentation via template variables
5. **Examples**: Working examples in all templates
6. **Dashboards**: Pre-built Grafana dashboards for visualization

## Alternatives Considered

### Vendor-Specific SDKs

**Pros**: Often more feature-rich, better UI/UX, integrated experience
**Cons**: Vendor lock-in, switching costs, per-language differences
**Rejected**: Doesn't align with vendor-neutral, portable approach

### Custom Instrumentation

**Pros**: Full control, minimal dependencies
**Cons**: High maintenance, no standardization, reinventing wheel
**Rejected**: Doesn't scale across multiple templates and languages

### Cloud Provider Solutions

**Pros**: Deep integration with cloud services, managed
**Cons**: Cloud lock-in, limited portability
**Rejected**: Limits multi-cloud support strategy

### Language-Specific Solutions

**Pros**: Native idioms, optimized per language
**Cons**: No consistency across templates, harder to correlate
**Rejected**: Doesn't provide unified observability

## References

- [OpenTelemetry Official Documentation](https://opentelemetry.io/)
- [CNCF OpenTelemetry Project](https://www.cncf.io/projects/opentelemetry/)
- [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification)
- [Notebook 04: Observability & SLOs](../../notebooks/04_observability_slos.ipynb)
- [Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)
- [Observability Engineering](https://www.oreilly.com/library/view/observability-engineering/9781492076438/)

## Related ADRs

- [ADR-003: GitHub Actions for CI/CD](ADR-003-github-actions-cicd.md) - OTel integrates with CI/CD
- [ADR-005: SLSA for Supply Chain Security](ADR-005-slsa-supply-chain-security.md) - Observability supports security

## Implementation Status

- [x] OpenTelemetry concepts documented in notebook
- [x] Collector configuration examples created
- [x] Grafana dashboard examples include OTel metrics
- [ ] Python template includes OTel setup
- [ ] Node.js template includes OTel setup
- [ ] Go template includes OTel setup
- [ ] React template includes client-side tracing
- [ ] Example projects demonstrate OTel usage

## Future Enhancements

1. **eBPF Auto-Instrumentation**: Kernel-level instrumentation for zero-code observability
2. **Continuous Profiling**: CPU and memory profiling integration
3. **Distributed Context**: Propagate business context across services
4. **Custom Metrics**: Template-specific custom metrics and dashboards
5. **Cost Attribution**: Track resource usage per request/tenant
6. **AI/ML Integration**: Anomaly detection on telemetry data

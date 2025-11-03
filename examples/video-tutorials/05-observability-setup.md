# Video Tutorial Script: Adding Observability to Your Service

**Duration:** 10-12 minutes  
**Target Audience:** Developers, SREs, Platform Engineers  
**Prerequisites:** Understanding of metrics, logs, and traces; basic service development knowledge

---

## Introduction (1 minute)

### Opening (15 seconds)

"Welcome to the Agentic Canon observability tutorial! Today we're diving into one of the most critical aspects of modern software: making your services observable."

### What You'll Learn (45 seconds)

In this tutorial, you'll learn how to:

- Instrument services with OpenTelemetry
- Collect metrics, logs, and traces
- Set up Service Level Objectives (SLOs)
- Configure error budgets
- Create observability dashboards
- Implement proactive monitoring

"Let's transform your service from a black box into a transparent, debuggable system!"

---

## Section 1: The Three Pillars of Observability (2 minutes)

### Understanding Observability (1 minute)

"Observability isn't just monitoring—it's the ability to ask questions about your system without having to predict those questions in advance."

**The Three Pillars:**

1. **Metrics** - Quantitative measurements over time
   - Request rate, error rate, duration
   - Resource utilization (CPU, memory, disk)
   - Business metrics (signups, transactions)

2. **Logs** - Discrete event records
   - Application logs
   - Access logs
   - Error logs with context

3. **Traces** - Request journey through your system
   - End-to-end request flow
   - Service dependencies
   - Performance bottlenecks

### OpenTelemetry: The Standard (1 minute)

**Show on screen: OpenTelemetry logo and architecture**

"OpenTelemetry is the industry standard for observability. It provides:"

- Vendor-neutral instrumentation
- Unified API for metrics, logs, and traces
- Automatic instrumentation for popular frameworks
- Flexible export to any backend

"Agentic Canon templates come with OpenTelemetry pre-configured!"

---

## Section 2: Instrumenting Your Service (3 minutes)

### Auto-Instrumentation (1.5 minutes)

**Show on screen: Python service example**

```python
# app.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI

# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Create FastAPI app
app = FastAPI()

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    # This endpoint is automatically traced!
    return {"id": user_id, "name": "John Doe"}
```

"With just a few lines, every HTTP request is traced automatically!"

### Custom Instrumentation (1.5 minutes)

**Show on screen: Adding custom spans**

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

@app.post("/api/orders")
async def create_order(order: Order):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.id", order.id)
        span.set_attribute("order.total", order.total)

        try:
            # Validate order
            with tracer.start_as_current_span("validate_order"):
                validate_order(order)

            # Process payment
            with tracer.start_as_current_span("process_payment") as payment_span:
                payment_span.set_attribute("payment.method", order.payment_method)
                result = process_payment(order)
                payment_span.set_attribute("payment.status", result.status)

            # Save to database
            with tracer.start_as_current_span("save_order"):
                db.save(order)

            span.set_status(Status(StatusCode.OK))
            return {"status": "success", "order_id": order.id}

        except ValidationError as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

"Custom spans let you trace critical business logic and capture important attributes."

---

## Section 3: Metrics That Matter (2 minutes)

### The RED Method (1 minute)

"For every service, track these golden signals:"

**R**ate - Request throughput
**E**rrors - Error rate
**D**uration - Response time

**Show on screen: Prometheus metrics**

```python
from prometheus_client import Counter, Histogram, Gauge

# Request counter
requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Request duration histogram
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Active requests gauge
active_requests = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

@app.middleware("http")
async def observe_requests(request, call_next):
    method = request.method
    endpoint = request.url.path

    active_requests.inc()

    with request_duration.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)

    active_requests.dec()
    requests_total.labels(
        method=method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    return response
```

### Business Metrics (1 minute)

"Don't forget business-level metrics!"

```python
# Business metrics
orders_created = Counter('orders_created_total', 'Total orders created')
revenue = Counter('revenue_total', 'Total revenue', ['currency'])
user_signups = Counter('user_signups_total', 'Total user signups')

@app.post("/api/orders")
async def create_order(order: Order):
    # ... create order ...
    orders_created.inc()
    revenue.labels(currency=order.currency).inc(order.total)
    return result
```

---

## Section 4: Service Level Objectives (2 minutes)

### Defining SLOs (1 minute)

"SLOs define the reliability targets for your service."

**Show on screen: SLO definition**

```yaml
# slo.yaml
slos:
  - name: api_availability
    description: API availability SLO
    sli:
      metric: http_requests_total
      success_criteria: "status < 500"
    target: 99.9%
    window: 30d

  - name: api_latency
    description: API latency SLO (p95)
    sli:
      metric: http_request_duration_seconds
      percentile: 95
      threshold: 0.5 # 500ms
    target: 99.0%
    window: 30d

  - name: api_error_rate
    description: API error rate SLO
    sli:
      metric: http_requests_total
      error_criteria: "status >= 500"
    target: 0.1% # Max 0.1% error rate
    window: 7d
```

### Error Budgets (1 minute)

"Error budgets give you a quantifiable way to balance feature velocity with reliability."

**Show on screen: Error budget calculation**

```
SLO Target: 99.9%
Allowed Failure: 0.1%
Monthly Budget: 43 minutes (0.1% of 30 days)

Current Status:
- Used: 12 minutes (27.9%)
- Remaining: 31 minutes (72.1%)
- Status: 🟢 Healthy
```

**Show dashboard:**

- Error budget burn rate
- Projected exhaustion date
- Alert thresholds

"When your error budget is healthy, ship features fast. When it's low, focus on reliability!"

---

## Section 5: The Observability Stack (2 minutes)

### OpenTelemetry Collector (1 minute)

**Show on screen: otel-collector-config.yaml**

```yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_mib: 512

  attributes:
    actions:
      - key: service.namespace
        value: production
        action: insert

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"

  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [jaeger]

    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]

    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]
```

"The collector receives, processes, and routes telemetry data to your backends."

### Visualization with Grafana (1 minute)

**Show on screen: Grafana dashboard**

"Agentic Canon includes pre-built dashboards:"

1. **DORA Metrics**
   - Deployment frequency
   - Lead time for changes
   - MTTR
   - Change failure rate

2. **Service Health**
   - Request rate, errors, duration (RED)
   - SLO compliance
   - Error budget status

3. **Infrastructure**
   - CPU, memory, disk usage
   - Network throughput
   - Container metrics

**Demo: Import dashboard and show metrics**

---

## Section 6: Practical Tips & Best Practices (1.5 minutes)

### Do's and Don'ts (1 minute)

✅ **Do:**

- Start with auto-instrumentation
- Add custom spans for business logic
- Set meaningful SLOs based on user needs
- Alert on SLO violations, not raw metrics
- Use structured logging with context
- Correlate logs with traces via trace IDs

❌ **Don't:**

- Instrument everything (focus on critical paths)
- Set unrealistic SLOs (99.999% for non-critical services)
- Alert on every metric deviation
- Ignore the cost of high-cardinality metrics
- Log sensitive data (PII, secrets)

### Debugging with Observability (30 seconds)

"When something goes wrong:"

1. **Check SLOs** - Which service is violating?
2. **Review dashboards** - When did it start?
3. **Query traces** - Which requests are slow/failing?
4. **Examine logs** - What's the error context?
5. **Correlate** - Use trace IDs to connect the dots

---

## Conclusion (1 minute)

### Recap (30 seconds)

"Today we covered:"

- ✅ The three pillars of observability
- ✅ Instrumenting services with OpenTelemetry
- ✅ Tracking metrics that matter (RED method)
- ✅ Setting up SLOs and error budgets
- ✅ Configuring the observability stack
- ✅ Best practices for production

### Next Steps (30 seconds)

"In the next tutorial, we'll explore Jupyter Book for creating beautiful, interactive documentation."

**Show on screen:**

- 📚 Full guide: docs/notebooks/04_observability_slos.md
- 📊 Dashboard templates: examples/dashboards/
- 🔧 OTel config: examples/dashboards/otel-collector-config.yaml
- 📖 OpenTelemetry docs: https://opentelemetry.io

"Thanks for watching! Remember: you can't improve what you can't measure. Happy observing!"

---

## YouTube Description Template

```
📊 Adding Observability to Your Service with OpenTelemetry

Learn how to make your services observable using OpenTelemetry, metrics, logs, and traces. This tutorial covers instrumentation, SLOs, error budgets, and building a complete observability stack.

⏱️ Timestamps:
0:00 - Introduction
1:00 - Three Pillars of Observability
3:00 - Instrumenting Your Service
6:00 - Metrics That Matter
8:00 - Service Level Objectives
10:00 - The Observability Stack
12:00 - Practical Tips
13:30 - Conclusion

🔗 Resources:
- Repository: https://github.com/IAmJonoBo/Agentic-Canon
- Observability Guide: docs/notebooks/04_observability_slos.md
- Dashboard Templates: examples/dashboards/
- OpenTelemetry: https://opentelemetry.io

📚 Related Videos:
- Getting Started with Agentic Canon
- Implementing Security Gates
- Setting up CI/CD Pipelines

#Observability #OpenTelemetry #SRE #Monitoring #DevOps
```

---

## Social Media Snippets

**Twitter/X:**
"📊 New tutorial: Adding Observability with OpenTelemetry! Learn to instrument services, set up SLOs, configure error budgets, and build comprehensive observability dashboards. #Observability #OpenTelemetry #SRE"

**LinkedIn:**
"Excited to share our observability tutorial! Learn how to transform your services from black boxes into transparent, debuggable systems using OpenTelemetry, metrics, logs, and traces. Includes practical examples and pre-built Grafana dashboards!"

**Reddit (r/devops, r/sre):**
"Tutorial: Adding Observability with OpenTelemetry - Covers instrumentation, the RED method, SLOs, error budgets, and setting up a complete observability stack with Prometheus, Jaeger, and Grafana."

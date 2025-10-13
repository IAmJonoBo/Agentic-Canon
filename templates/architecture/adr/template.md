# Architecture Decision Record (ADR) Template

# Implements: Architectural decision documentation best practices

# Format: Markdown with YAML frontmatter for machine readability

---

# Metadata

number: {{ ADR_NUMBER }}
title: {{ DECISION_TITLE }}
date: {{ DATE }}
status: {{ STATUS }} # proposed | accepted | deprecated | superseded
supersedes: [] # List of ADR numbers this supersedes
superseded_by: null # ADR number that supersedes this one

---

## Context

<!-- Describe the forces at play (technical, business, regulatory, etc.)
     What is the issue we're trying to solve? -->

### Problem Statement

<!-- Clear, concise statement of the problem -->

### Constraints

<!-- Technical, business, or regulatory constraints that limit options -->

- **Technical**:
- **Business**:
- **Regulatory**:
- **Timeline**:
- **Resources**:

### Assumptions

<!-- What are we assuming to be true? -->

-
-

## Decision

<!-- What is the decision we're making? State it clearly and concisely. -->

We will {{ DECISION }}.

### Rationale

<!-- Why did we choose this option? -->

1. **Primary Reason**:
2. ## **Supporting Factors**:
   -

### Standards Compliance

<!-- How does this align with our standards? -->

- ✅ NIST SSDF:
- ✅ OWASP SAMM:
- ✅ ISO/IEC 25010:
- ✅ Internal standards:

## Alternatives Considered

### Option 1: {{ ALTERNATIVE_1 }}

**Pros:**

-
- **Cons:**

-
- **Trade-offs:**

- **Rejected because:**

### Option 2: {{ ALTERNATIVE_2 }}

**Pros:**

-
- **Cons:**

-
- **Trade-offs:**

- **Rejected because:**

### Option 3: Do Nothing

**Pros:**

- No immediate cost
- No disruption

**Cons:**

- Problem persists
- Technical debt accumulates

**Rejected because:**

## Consequences

### Positive

-
-

### Negative

-
-

### Neutral

-
-

### Risks

| Risk         | Impact       | Likelihood       | Mitigation       |
| ------------ | ------------ | ---------------- | ---------------- |
| {{ RISK_1 }} | {{ IMPACT }} | {{ LIKELIHOOD }} | {{ MITIGATION }} |
| {{ RISK_2 }} | {{ IMPACT }} | {{ LIKELIHOOD }} | {{ MITIGATION }} |

## Implementation

### Changes Required

1. ## **Code Changes**:
   -

2. ## **Infrastructure Changes**:
   -

3. ## **Process Changes**:
   -

4. ## **Documentation Updates**:
   -

### Migration Path

<!-- How do we get from current state to desired state? -->

**Phase 1**: {{ PHASE_1 }}

- Duration:
- Tasks:

**Phase 2**: {{ PHASE_2 }}

- Duration:
- Tasks:

**Phase 3**: {{ PHASE_3 }}

- Duration:
- Tasks:

### Rollback Plan

<!-- How can we reverse this decision if needed? -->

1.
2.
3.

**Rollback triggers:**

-
-

### Success Metrics

<!-- How will we measure success? -->

| Metric         | Baseline       | Target       | Timeline       |
| -------------- | -------------- | ------------ | -------------- |
| {{ METRIC_1 }} | {{ BASELINE }} | {{ TARGET }} | {{ TIMELINE }} |
| {{ METRIC_2 }} | {{ BASELINE }} | {{ TARGET }} | {{ TIMELINE }} |

## Impact Assessment

### Maintainability

Impact: {{ HIGH/MEDIUM/LOW }}

- **Code Complexity**:
- **Team Knowledge**:
- **Dependencies**:

### Performance

Impact: {{ HIGH/MEDIUM/LOW }}

- **Latency**:
- **Throughput**:
- **Resource Usage**:

### Security

Impact: {{ HIGH/MEDIUM/LOW }}

- **Attack Surface**:
- **Data Protection**:
- **Compliance**:

### Cost

Impact: {{ HIGH/MEDIUM/LOW }}

- **Implementation**:
- **Operational**:
- **Opportunity Cost**:

### Developer Experience

Impact: {{ HIGH/MEDIUM/LOW }}

- **Learning Curve**:
- **Productivity**:
- **Tool Friction**:

## Compliance & Standards

### Standards Mapping

| Standard      | Control                 | How This Addresses It |
| ------------- | ----------------------- | --------------------- |
| NIST SSDF     | {{ CONTROL }}           | {{ EXPLANATION }}     |
| OWASP SAMM    | {{ CONTROL }}           | {{ EXPLANATION }}     |
| ISO/IEC 25010 | {{ QUALITY_ATTRIBUTE }} | {{ EXPLANATION }}     |

### Evidence

<!-- What evidence supports this decision? -->

- **Research**:
- **Prototypes**:
- **Benchmarks**:
- **References**:

## Review & Maintenance

### Review Schedule

- **Next Review**: {{ DATE }}
- **Review Frequency**: {{ QUARTERLY/ANNUALLY }}
- **Review Owner**: {{ TEAM/PERSON }}

### Update History

| Date       | Author       | Change          | Version |
| ---------- | ------------ | --------------- | ------- |
| {{ DATE }} | {{ AUTHOR }} | Initial version | 1.0     |

## Stakeholders

### Decision Makers

- {{ NAME }} - {{ ROLE }}
- {{ NAME }} - {{ ROLE }}

### Consulted

- {{ NAME }} - {{ ROLE }}
- {{ NAME }} - {{ ROLE }}

### Informed

- {{ TEAM }}
- {{ TEAM }}

## References

<!-- Links to related documents, research, discussions -->

- [Related ADR #{{ NUMBER }}](../adr/{{ NUMBER }}.md)
- [Design Document]({{ URL }})
- [Spike Results]({{ URL }})
- [External Research]({{ URL }})

## Fitness Functions

<!-- Automated checks to ensure decision is still valid -->

```yaml
fitness_functions:
  - name: performance_regression
    check: p95_latency < 300ms
    frequency: continuous

  - name: complexity_ceiling
    check: cyclomatic_complexity < 10
    frequency: per_commit

  - name: dependency_count
    check: direct_dependencies < 50
    frequency: weekly
```

## Communication Plan

### Announcement

- **Date**: {{ DATE }}
- **Channels**: {{ SLACK/EMAIL/WIKI }}
- **Audience**: {{ TEAMS }}

### Training

- **Sessions**: {{ COUNT }}
- **Materials**: {{ LINKS }}
- **Timeline**: {{ DATES }}

### Documentation

- **Wiki Update**: {{ URL }}
- **README Update**: Required
- **API Docs**: {{ URL }}

---

## Template Usage

**To create a new ADR:**

```bash
cp templates/architecture/adr/template.md docs/adr/NNNN-decision-title.md
# Edit the file
# Update the number and metadata
# Submit for review
```

**ADR Lifecycle:**

```
proposed → [review] → accepted → [implementation] →
  → [time passes] → deprecated/superseded
```

**Status Definitions:**

- **Proposed**: Under discussion
- **Accepted**: Approved and being implemented
- **Deprecated**: No longer recommended but not replaced
- **Superseded**: Replaced by another ADR

# Quality Standards - Frontier Software Excellence

**Version:** 1.0.0  
**Last Updated:** 2025-10-12  
**Purpose:** Comprehensive quality standards for all aspects of software development  
**Standards Compliance:** NIST SSDF v1.1, OWASP SAMM 2.0, SLSA L3, ISO/IEC 25010, ISO/IEC 5055, WCAG 2.2 AA

---

## Table of Contents

- [Overview](#overview)
- [Non-Negotiable Quality Gates](#non-negotiable-quality-gates)
- [Code Quality Standards](#code-quality-standards)
- [Testing Standards](#testing-standards)
- [Security Quality Standards](#security-quality-standards)
- [AI/LLM Quality Standards](#ai-llm-quality-standards)
- [Business Logic Quality Standards](#business-logic-quality-standards)
- [Orchestration Quality Standards](#orchestration-quality-standards)
- [Documentation Quality Standards](#documentation-quality-standards)
- [Performance Quality Standards](#performance-quality-standards)
- [Accessibility Quality Standards](#accessibility-quality-standards)
- [Review & Approval Standards](#review--approval-standards)
- [Continuous Improvement](#continuous-improvement)
- [Enforcement & Tooling](#enforcement--tooling)

---

## Overview

This document defines the **frontier-grade quality standards** for all software development activities within the Agentic Canon framework. These standards are:

- **Non-negotiable**: Quality gates must pass before merge
- **Automated**: Enforced through CI/CD pipelines
- **Measurable**: Clear metrics and thresholds
- **Comprehensive**: Cover all aspects of software development
- **AI-friendly**: Machine-readable for automated enforcement
- **Standards-aligned**: Mapped to NIST SSDF, OWASP, ISO, SLSA, WCAG

**Part of the Agentic Canon Framework**: This document is Layer 2 of the [FRAMEWORK.md](FRAMEWORK.md) architecture, defining measurable quality criteria that are implemented consistently through the conventions in [CONVENTIONS.md](CONVENTIONS.md).

### Quality Philosophy

1. **Prevention over Detection**: Build quality in from the start
2. **Shift Left**: Catch issues early in the development cycle
3. **Automation First**: Automate all quality checks
4. **Continuous Improvement**: Regular review and enhancement of standards
5. **Evidence-Based**: All quality claims must be verifiable

---

## Non-Negotiable Quality Gates

All code changes must pass these gates before merge:

### Build Gate
```yaml
build:
  - compiles: true                    # Code must compile/transpile without errors
  - unit_tests: green                 # All unit tests must pass
  - coverage: ">= 80%"                # Minimum code coverage threshold
  - mutation_score: ">= 40%"          # Minimum mutation testing score
  - build_time: "<= baseline * 1.1"   # Build time cannot increase >10%
```

### Security Gate
```yaml
security:
  - secrets_scan: clean               # No secrets in code (Gitleaks)
  - sast_critical: 0                  # Zero critical SAST findings
  - sast_high: "<= 5"                 # Max 5 high-severity findings (with plan)
  - sbom_generated: true              # SBOM must be generated
  - provenance_signed: true           # Provenance must be signed (releases)
  - dependencies_current: true        # No critical CVEs in dependencies
  - license_compliance: true          # All dependencies have approved licenses
```

### Quality Gate
```yaml
quality:
  - code_smells: 0                    # Zero new code smells (SonarQube)
  - duplicates: "<= 3%"               # Max 3% code duplication
  - complexity: "<= 15"               # Max cyclomatic complexity per function
  - maintainability: ">= B"           # Minimum maintainability rating
  - technical_debt: "<= 5%"           # Technical debt ratio
  - sonar_quality_gate: passed        # Overall quality gate passes
```

### Performance Gate
```yaml
performance:
  - core_web_vitals: within_budget    # LCP, FID, CLS within thresholds
  - bundle_size: "<= budget"          # Bundle size within budget
  - p95_latency: "<= threshold"       # 95th percentile latency target
  - memory_usage: "<= baseline * 1.2" # Memory usage cannot increase >20%
  - error_rate: "<= 0.1%"             # Max 0.1% error rate
```

### Accessibility Gate
```yaml
accessibility:
  - wcag_aa_violations: 0             # Zero WCAG 2.2 AA violations
  - axe_core_critical: 0              # Zero critical axe-core findings
  - keyboard_navigation: complete     # Full keyboard navigation support
  - screen_reader: tested             # Screen reader compatibility verified
  - color_contrast: ">= 4.5:1"        # Minimum contrast ratio
```

---

## Code Quality Standards

### 1. Code Style & Formatting

**Python**
- **Style Guide**: PEP 8 strict compliance
- **Formatter**: Black (line length: 88)
- **Linter**: Ruff (all default rules enabled)
- **Type Checking**: mypy in strict mode
- **Import Sorting**: isort with Black compatibility
- **Docstrings**: Google-style for all public APIs

**TypeScript/JavaScript**
- **Style Guide**: Airbnb JavaScript Style Guide
- **Formatter**: Prettier (2 spaces, single quotes, semicolons)
- **Linter**: ESLint with strict configuration
- **Type Checking**: TypeScript strict mode enabled
- **Import Sorting**: ESLint plugin for import organization

**Go**
- **Formatter**: gofmt and goimports
- **Linter**: golangci-lint with all recommended linters
- **Style Guide**: Effective Go principles
- **Documentation**: godoc comments for all exported items

### 2. Code Structure & Organization

**File Organization**
- Maximum file length: 500 lines (excluding tests)
- Maximum function length: 50 lines
- Maximum function parameters: 5 (use objects/structs for more)
- One class/component per file (with exceptions for tightly coupled items)

**Naming Conventions** (see CONVENTIONS.md for details)
- Clear, descriptive names (no abbreviations except domain-standard)
- Boolean variables: prefix with `is`, `has`, `should`, `can`
- Functions: verb + noun (e.g., `getUserById`, `validateEmail`)
- Classes: PascalCase nouns
- Constants: UPPER_SNAKE_CASE

**Modularity Requirements**
- High cohesion: Related functionality grouped together
- Low coupling: Minimal dependencies between modules
- Single Responsibility Principle: Each module/class/function has one reason to change
- Dependency Injection: Dependencies injected, not hard-coded
- Interface Segregation: Small, focused interfaces

### 3. Complexity Metrics

**Cyclomatic Complexity**
- Maximum per function: 15
- Target: < 10 for most functions
- Action: Refactor functions exceeding threshold

**Cognitive Complexity**
- Maximum per function: 15
- Target: < 10 for most functions
- Focus on understandability and maintainability

**Nesting Depth**
- Maximum: 4 levels
- Prefer early returns and guard clauses
- Extract nested logic to separate functions

**Code Duplication**
- Maximum: 3% across codebase
- No copy-paste code blocks > 5 lines
- Extract common logic to shared functions/modules

### 4. Error Handling

**Required Practices**
- All errors must be handled explicitly (no silent failures)
- Use typed errors/exceptions (custom error types for domain errors)
- Provide context in error messages (what, why, how to fix)
- Log errors with appropriate severity levels
- Never catch and ignore errors without justification (document why)

**Error Message Quality**
- Include relevant context (user ID, resource ID, etc.)
- Suggest remediation steps when possible
- No sensitive data in error messages (sanitize)
- Use standard error codes/types for API responses

### 5. Comments & Documentation

**When to Comment**
- Complex algorithms: Explain the approach and reasoning
- Non-obvious code: Clarify intent when code alone is unclear
- API boundaries: Document all public interfaces
- Workarounds: Explain why and link to tracking issue
- Security considerations: Highlight security-critical sections

**When NOT to Comment**
- Obvious code: Let the code speak for itself
- Redundant information: Don't repeat what the code says
- Outdated comments: Remove or update stale comments
- TODO/FIXME without tracking: Create an issue and link to it

---

## Testing Standards

### 1. Testing Pyramid

**Unit Tests** (70% of tests)
- Test individual functions/methods in isolation
- Fast execution (< 1ms per test typically)
- No external dependencies (use mocks/stubs)
- Coverage target: 80% of all code
- Focus: Logic correctness and edge cases

**Integration Tests** (20% of tests)
- Test component interactions
- May use real dependencies (databases, APIs)
- Slower execution (< 100ms per test)
- Coverage: All integration points
- Focus: Component collaboration and data flow

**End-to-End Tests** (10% of tests)
- Test complete user workflows
- Use real system configuration
- Slowest execution (seconds per test)
- Coverage: Critical user paths
- Focus: User scenarios and business outcomes

### 2. Test Quality Requirements

**Test Structure**
- Follow AAA pattern: Arrange, Act, Assert
- One assertion per test (or closely related assertions)
- Clear test names: `test_<function>_<scenario>_<expected_result>`
- Independent tests: No test depends on another
- Deterministic tests: Same input always produces same output

**Test Coverage Metrics**
- Line coverage: ≥ 80%
- Branch coverage: ≥ 75%
- Function coverage: 100% of public APIs
- Mutation score: ≥ 40% (target: 60%)

**Test Data Management**
- Use factories/builders for test data creation
- Avoid magic numbers: Use named constants
- Minimize test data: Only include relevant fields
- Clean up after tests: Restore state

### 3. Mutation Testing

**Requirements**
- Minimum mutation score: 40%
- Target mutation score: 60%
- Run on all critical business logic
- Review surviving mutants and improve tests

**Mutation Operators** (check these)
- Arithmetic operators (+, -, *, /)
- Relational operators (<, >, <=, >=, ==, !=)
- Logical operators (&&, ||, !)
- Boundary values (off-by-one errors)
- Return values and statement deletion

### 4. Contract Testing

**API Contract Tests**
- Use Pact for HTTP API contracts
- Consumer-driven contracts for all service boundaries
- Run contract tests on every commit
- Publish contracts to broker
- Verify provider compatibility

**Event Contract Tests**
- Use AsyncAPI for event schemas
- Validate all event producers and consumers
- Schema versioning strategy enforced
- Breaking change detection automated

### 5. Property-Based Testing

**When to Use**
- Complex algorithms with many input combinations
- Functions with invariants (properties that always hold)
- Parsers and data transformations
- Stateful systems with state machines

**Requirements**
- Use hypothesis (Python), fast-check (JS), or similar
- Define clear properties to test
- Run with sufficient iterations (≥ 100)
- Shrink failing examples to minimal case

### 6. Performance Testing

**Load Testing**
- Baseline performance established
- Test at expected peak load + 50%
- Monitor key metrics (latency, throughput, error rate)
- No degradation > 10% from baseline

**Stress Testing**
- Test beyond normal capacity
- Verify graceful degradation
- Test recovery after stress

**Benchmarking**
- Benchmark critical paths
- Track performance over time
- Prevent performance regressions in CI

---

## Security Quality Standards

### 1. Secure Code Practices

**Input Validation**
- Validate all external inputs (user input, API requests, file uploads)
- Use allow-lists, not deny-lists
- Sanitize inputs for context (HTML, SQL, shell)
- Validate data types, ranges, formats, lengths
- Reject invalid input (fail closed)

**Authentication & Authorization**
- Use industry-standard protocols (OAuth 2.0, OpenID Connect)
- Never roll your own crypto
- Store passwords with bcrypt/Argon2 (never plain text)
- Implement proper session management
- Use principle of least privilege for authorization
- Verify authorization on every request

**Data Protection**
- Encrypt sensitive data at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- Never log sensitive data (passwords, tokens, PII)
- Implement proper key management
- Use secure random number generation

**Common Vulnerabilities Prevention**
- SQL Injection: Use parameterized queries only
- XSS: Escape all user input in output
- CSRF: Use CSRF tokens on state-changing operations
- Command Injection: Never pass user input to shell
- Path Traversal: Validate and sanitize file paths
- Insecure Deserialization: Validate before deserializing

### 2. Dependency Security

**Dependency Management**
- Pin all dependency versions (use lock files)
- Review dependencies before adding (security, maintenance, size)
- Minimize dependencies (only add when justified)
- Update dependencies regularly (at least monthly)
- Remove unused dependencies

**Vulnerability Scanning**
- Scan dependencies daily for CVEs
- Critical CVEs: Fix within 24 hours
- High CVEs: Fix within 7 days
- Medium CVEs: Fix within 30 days
- Low CVEs: Fix within 90 days or accept risk

**Supply Chain Security**
- Generate SBOM for all builds (CycloneDX or SPDX)
- Verify package signatures when available
- Use trusted package registries
- Implement SLSA Level 3 builds
- Sign release artifacts

### 3. Security Testing

**SAST (Static Application Security Testing)**
- Run on every commit
- Zero critical findings required for merge
- Tools: CodeQL, Semgrep, or equivalent
- Cover OWASP Top 10 and CWE Top 25

**DAST (Dynamic Application Security Testing)**
- Run on staging/pre-production environments
- Cover all authenticated and unauthenticated flows
- Test for OWASP Top 10 vulnerabilities
- Tools: OWASP ZAP, Burp Suite, or equivalent

**Secret Scanning**
- Run on every commit (Gitleaks)
- Block commits containing secrets
- Scan commit history for secrets
- Rotate secrets immediately if exposed

**Penetration Testing**
- Annual third-party penetration tests
- Address all findings within SLA
- Retest after remediation

---

## AI/LLM Quality Standards

### 1. Prompt Engineering Quality

**Prompt Design**
- Clear, specific instructions
- Structured format for consistency
- Include relevant context and constraints
- Define expected output format
- Use few-shot examples when appropriate
- Version control all prompts

**Prompt Testing**
- Test with diverse inputs (edge cases, adversarial)
- Validate output quality and format
- Measure consistency across runs
- Test for bias and fairness
- Monitor prompt performance in production

**Prompt Security**
- Validate all user input to prompts
- Prevent prompt injection attacks
- Sanitize LLM outputs before use
- Never execute code from LLM without review
- Implement rate limiting and abuse detection

### 2. RAG (Retrieval-Augmented Generation) Quality

**Data Quality**
- Clean, accurate source data
- Regular data updates and validation
- Remove PII unless required
- Version control knowledge bases
- Document data lineage

**Retrieval Quality**
- Relevance metrics (MRR, NDCG)
- Recall threshold: ≥ 90%
- Precision threshold: ≥ 80%
- Monitor and improve retrieval quality
- A/B test retrieval strategies

**Generation Quality**
- Factual accuracy verification
- Citation/source attribution
- Hallucination detection
- Consistency checks
- Human-in-the-loop review for critical outputs

### 3. Model Governance

**Model Selection & Deployment**
- Document model selection rationale
- Evaluate multiple models for task
- Monitor model performance metrics
- Implement fallback mechanisms
- Version all model configurations

**Model Monitoring**
- Track inference latency (p50, p95, p99)
- Monitor error rates and types
- Detect model drift
- Track cost per inference
- Alert on anomalies

**Bias & Fairness**
- Test for bias across demographics
- Monitor fairness metrics
- Regular bias audits
- Document known limitations
- Implement bias mitigation strategies

**LLM-Specific Security (OWASP LLM Top 10)**
- Prevent prompt injection (LLM01)
- Control data leakage (LLM02)
- Validate training data (LLM03)
- Prevent denial of service (LLM04)
- Secure supply chain (LLM05)
- Manage permissions properly (LLM06)
- Validate agent actions (LLM07)
- Prevent overreliance (LLM08)
- Avoid insecure plugins (LLM09)
- Secure model storage (LLM10)

---

## Business Logic Quality Standards

### 1. Domain Modeling

**Model Design**
- Use domain-driven design principles
- Clear bounded contexts
- Ubiquitous language throughout
- Rich domain models (not anemic)
- Explicit business rules in code

**Model Validation**
- Validate all business invariants
- Use value objects for validated data
- Fail fast on invalid state
- Clear error messages for violations
- Unit test all business rules

### 2. Business Rule Implementation

**Rule Clarity**
- One rule per function/method where possible
- Clear naming that reflects business language
- Document complex rules with examples
- Separate rules from infrastructure code

**Rule Testing**
- Test each rule independently
- Test rule combinations
- Test edge cases and boundaries
- Use business-readable test names
- Property-based testing for complex rules

**Rule Traceability**
- Map code to business requirements
- Document rule sources (policy, regulation, etc.)
- Version business rules
- Track rule changes over time

### 3. Data Validation & Transformation

**Validation Standards**
- Validate at system boundaries
- Use schema validation (JSON Schema, OpenAPI)
- Explicit validation rules
- Comprehensive error reporting
- Validation as documentation

**Transformation Standards**
- Pure functions where possible
- Explicit input/output types
- Lossless transformations (preserve information)
- Idempotent transformations
- Test round-trip transformations

### 4. State Management

**State Design**
- Minimize mutable state
- Explicit state transitions
- Use state machines for complex flows
- Immutable data structures preferred
- Clear state ownership

**State Testing**
- Test all state transitions
- Test invalid transitions
- Test state persistence and recovery
- Test concurrent state access
- Use property-based testing for state machines

---

## Orchestration Quality Standards

### 1. Workflow Patterns

**Workflow Design**
- Clear, linear flows where possible
- Explicit error handling paths
- Idempotent operations
- Compensation logic for failures
- Timeout and retry policies

**Supported Patterns**
- Saga pattern for distributed transactions
- Event-driven choreography
- Workflow orchestration (Temporal, Argo)
- Circuit breaker for external services
- Bulkhead for resource isolation

**Pattern Implementation**
- Document pattern choice and rationale
- Implement standard patterns consistently
- Test failure scenarios thoroughly
- Monitor workflow execution

### 2. Distributed System Quality

**Consistency**
- Define consistency requirements (strong, eventual)
- Implement appropriate consistency models
- Test for distributed edge cases
- Handle split-brain scenarios

**Reliability**
- Design for failure (assume failures will happen)
- Implement retries with exponential backoff
- Set appropriate timeouts
- Use circuit breakers for cascading failures
- Implement graceful degradation

**Observability**
- Distributed tracing for all requests
- Correlation IDs across services
- Structured logging with context
- Metrics for all operations
- Alerts for anomalies

### 3. Event-Driven Architecture

**Event Design**
- Immutable events
- Schema versioning strategy
- Event sourcing where appropriate
- Clear event naming (past tense)
- Include event metadata (timestamp, source, etc.)

**Event Processing**
- At-least-once or exactly-once semantics
- Idempotent event handlers
- Dead letter queues for failures
- Event replay capability
- Event ordering guarantees where required

**Event Testing**
- Test event handlers in isolation
- Test event ordering scenarios
- Test duplicate event handling
- Test event schema evolution
- Integration tests for event flows

### 4. Resilience Patterns

**Timeout Management**
- Set timeouts on all external calls
- Use appropriate timeout values (profile actual latency)
- Cascade timeouts properly (parent > child)
- Test timeout scenarios

**Retry Logic**
- Exponential backoff with jitter
- Maximum retry attempts
- Only retry transient failures
- Log all retry attempts
- Circuit breaker to stop excessive retries

**Fallback Strategies**
- Define fallback behavior for all critical paths
- Cache for read operations
- Stale data better than no data (where appropriate)
- Graceful degradation of features
- Clear user communication during degradation

---

## Documentation Quality Standards

### 1. Code Documentation

**Inline Documentation**
- Document all public APIs (functions, classes, modules)
- Include parameter descriptions and types
- Document return values and exceptions
- Provide usage examples for complex APIs
- Keep documentation synchronized with code

**Documentation Standards by Language**
- Python: Google-style or NumPy-style docstrings
- TypeScript/JavaScript: JSDoc comments
- Go: godoc comments
- All: Clear, concise, accurate

### 2. Architecture Documentation

**Architecture Decision Records (ADRs)**
- Use ADR template in `docs/adr/`
- Required for all significant decisions
- Include: Context, Decision, Consequences, Alternatives
- Link ADRs in relevant code locations
- Keep ADRs up to date

**Diagrams**
- Use C4 model (Context, Container, Component, Code)
- Include system context diagrams
- Component diagrams for major subsystems
- Sequence diagrams for complex interactions
- Keep diagrams as code (PlantUML, Mermaid)

**API Documentation**
- OpenAPI 3.x for REST APIs
- GraphQL schema documentation
- gRPC proto documentation
- AsyncAPI for event-driven APIs
- Include examples and error responses

### 3. User Documentation

**README Requirements**
- Clear project description
- Quick start guide (5 minutes or less)
- Installation instructions
- Usage examples
- Link to full documentation
- Contributing guidelines
- License information

**User Guides**
- Task-oriented documentation
- Step-by-step instructions
- Screenshots and examples
- Troubleshooting section
- FAQ for common questions

**Runbooks**
- Operational procedures
- Incident response playbooks
- Deployment procedures
- Rollback procedures
- Maintenance tasks

### 4. Documentation Testing

**Doc Validation**
- Test all code examples (include in CI)
- Verify all links (no broken links)
- Test installation instructions
- Spell check and grammar check
- Review for clarity and completeness

**Doc Maintenance**
- Update docs with code changes
- Review docs quarterly
- Deprecation notices for old versions
- Version documentation with releases

---

## Performance Quality Standards

### 1. Application Performance

**Response Time Targets**
- API endpoints: p95 < 200ms, p99 < 500ms
- Database queries: p95 < 50ms, p99 < 100ms
- Page load time: LCP < 2.5s
- Time to interactive: TTI < 3.5s
- First contentful paint: FCP < 1.8s

**Throughput Targets**
- Define throughput requirements per endpoint
- Load test at peak + 50% capacity
- Ensure linear scaling or document limits
- Monitor throughput in production

**Resource Usage**
- Memory: No memory leaks (stable over time)
- CPU: < 70% average utilization at peak
- Disk I/O: Monitor and optimize hot paths
- Network: Minimize payload sizes

### 2. Frontend Performance

**Core Web Vitals** (WCAG/ISO 9241-210 aligned)
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1

**Bundle Size Budgets**
- Initial bundle: < 170 KB (compressed)
- Total JavaScript: < 500 KB (compressed)
- Critical CSS: < 14 KB (inline)
- Images: WebP/AVIF with lazy loading

**Optimization Techniques**
- Code splitting by route
- Tree shaking unused code
- Lazy loading non-critical resources
- Service worker for caching
- CDN for static assets

### 3. Database Performance

**Query Performance**
- All queries profiled and optimized
- Indexes on foreign keys and query columns
- No N+1 query problems
- Use connection pooling
- Monitor slow query log

**Data Growth Strategy**
- Archival strategy for old data
- Partitioning for large tables
- Caching strategy for hot data
- Read replicas for read-heavy workloads

### 4. Performance Testing

**Load Testing**
- Test at expected peak load + 50%
- Sustained load tests (30+ minutes)
- Identify bottlenecks and address
- Establish performance baselines

**Performance Monitoring**
- Real user monitoring (RUM)
- Synthetic monitoring for critical paths
- Performance budgets enforced in CI
- Alerts on performance degradation

---

## Accessibility Quality Standards

### 1. WCAG 2.2 AA Compliance

**Perceivable** (Principle 1)
- Text alternatives for non-text content
- Captions and alternatives for multimedia
- Adaptable content (multiple presentations)
- Distinguishable content (color, contrast, audio control)
- Color contrast: ≥ 4.5:1 for normal text, ≥ 3:1 for large text

**Operable** (Principle 2)
- Full keyboard accessibility (no keyboard traps)
- Sufficient time for users to read and interact
- No content causing seizures (flashing < 3 per second)
- Clear navigation and wayfinding
- Multiple input methods supported

**Understandable** (Principle 3)
- Readable text (language declared, definitions provided)
- Predictable behavior (consistent navigation and identification)
- Input assistance (error prevention, correction, suggestions)
- Clear instructions and labels

**Robust** (Principle 4)
- Valid HTML/ARIA
- Compatible with assistive technologies
- Semantic HTML elements
- Proper heading structure
- ARIA attributes when needed

### 2. Accessibility Testing

**Automated Testing**
- axe-core in CI pipeline (zero critical issues)
- Lighthouse accessibility score ≥ 95
- Pa11y or similar for continuous monitoring
- Test with browser accessibility tools

**Manual Testing**
- Keyboard-only navigation testing
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Zoom to 200% (content still accessible)
- Color blindness simulation
- Test with assistive technologies

**User Testing**
- Include users with disabilities in testing
- Test with diverse assistive technologies
- Gather feedback and iterate
- Document accessibility issues and fixes

### 3. Accessible Development Practices

**HTML Practices**
- Semantic HTML elements (nav, main, article, etc.)
- Proper heading hierarchy (h1 → h2 → h3)
- Form labels properly associated
- Alt text for all images (empty alt for decorative)
- Link text descriptive and meaningful

**ARIA Practices**
- Use ARIA only when needed (HTML first)
- ARIA roles, states, properties correctly applied
- Live regions for dynamic content
- Focus management for modals and dialogs
- Aria-labels for icon buttons

**Keyboard Practices**
- All interactive elements keyboard accessible
- Visible focus indicators
- Logical tab order
- Skip links for repetitive content
- Keyboard shortcuts documented

---

## Review & Approval Standards

### 1. Code Review Requirements

**Review Scope**
- All code changes require review (no direct commits to main)
- Minimum 1 approval required for merge
- 2+ approvals for critical/security changes
- Architecture changes require tech lead approval

**Reviewer Responsibilities**
- Verify functionality and correctness
- Check for security vulnerabilities
- Ensure code quality and maintainability
- Validate tests and coverage
- Verify documentation updates
- Check standards compliance

**Review Checklist** (see CONVENTIONS.md for full list)
- [ ] Code follows style guide
- [ ] Tests added/updated for changes
- [ ] Documentation updated
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Accessibility verified (if UI changes)
- [ ] Error handling appropriate
- [ ] Logging sufficient
- [ ] Breaking changes documented

### 2. Pull Request Standards

**PR Description**
- Clear title (conventional commits format)
- Description of changes and rationale
- Link to related issues/tickets
- Screenshots for UI changes
- Migration/deployment notes if needed
- Breaking changes highlighted

**PR Size**
- Target: < 400 lines changed
- Maximum: 800 lines (excluding generated code)
- Large PRs split into smaller logical chunks
- Exceptions require justification

**PR Lifecycle**
- Draft PRs for early feedback
- CI must pass before review
- Address all review comments
- Re-request review after changes
- Squash commits before merge (or rebase)

### 3. Approval Workflows

**Standard Changes**
- 1 approving review from code owner
- All CI checks passing
- No outstanding review comments
- Up to date with target branch

**Security-Sensitive Changes**
- 2 approving reviews required
- Security team review required
- Security testing completed
- Deployment plan documented

**Infrastructure/Platform Changes**
- Platform team review required
- Impact assessment completed
- Rollback plan documented
- Phased rollout plan (if needed)

---

## Continuous Improvement

### 1. Quality Metrics Tracking

**Code Quality Metrics**
- Code coverage trend (target: ↑)
- Code smells trend (target: ↓)
- Technical debt ratio (target: < 5%)
- Cyclomatic complexity (target: < 10 avg)
- Duplication percentage (target: < 3%)

**Defect Metrics**
- Defect escape rate (target: < 5%)
- Mean time to detection (target: ↓)
- Mean time to resolution (target: ↓)
- Defect density (target: < 0.5 per KLOC)
- Critical defects in production (target: 0)

**Process Metrics**
- Build success rate (target: > 95%)
- PR cycle time (target: < 2 days)
- Code review turnaround (target: < 4 hours)
- Deployment frequency (target: ↑)
- Change failure rate (target: < 5%)

### 2. Quality Reviews

**Monthly Quality Reviews**
- Review quality metrics trends
- Identify quality improvement opportunities
- Address recurring issues
- Update standards as needed
- Share learnings across teams

**Quarterly Quality Audits**
- Deep dive on code quality
- Security posture assessment
- Performance review
- Accessibility audit
- Documentation review

**Annual Quality Retrospectives**
- Review year's quality improvements
- Set quality goals for next year
- Update quality standards
- Celebrate quality wins

### 3. Learning & Improvement

**Post-Incident Reviews**
- Blameless post-mortems for all incidents
- Identify root causes
- Document action items
- Track action item completion
- Share learnings widely

**Quality Training**
- Onboarding: Quality standards overview
- Ongoing: Quarterly quality workshops
- Specialized: Security, performance, accessibility training
- Tool training: SAST, testing frameworks, etc.

**Knowledge Sharing**
- Quality champions in each team
- Regular tech talks on quality
- Internal blog/wiki for quality practices
- External conference talks/blog posts

---

## Enforcement & Tooling

### 1. Automated Enforcement

**Pre-commit Hooks**
- Code formatting (Black, Prettier, gofmt)
- Linting (Ruff, ESLint, golangci-lint)
- Secret scanning (Gitleaks)
- Type checking (mypy, tsc)
- Unit test execution (fast tests only)

**CI Pipeline Enforcement**
- All quality gates automated
- Block merge on gate failures
- No manual override without approval
- Audit all quality gate bypasses

**Continuous Monitoring**
- SonarQube quality gate tracking
- Security vulnerability scanning
- Performance monitoring and alerting
- Accessibility monitoring

### 2. Tooling Stack

**Code Quality Tools**
- SonarQube/SonarCloud: Code quality and security
- Black/Prettier: Code formatting
- Ruff/ESLint: Linting
- mypy/TypeScript: Type checking

**Testing Tools**
- pytest/Jest/testing-library: Unit/integration testing
- pytest-cov/Istanbul: Code coverage
- mutmut/Stryker: Mutation testing
- Playwright/Cypress: E2E testing
- Pact: Contract testing

**Security Tools**
- Gitleaks: Secret scanning
- CodeQL/Semgrep: SAST
- Trivy/Snyk: Dependency scanning
- OWASP ZAP: DAST
- Cosign: Artifact signing

**Performance Tools**
- Lighthouse: Web performance
- k6/Locust: Load testing
- OpenTelemetry: Observability
- Prometheus/Grafana: Monitoring

**Accessibility Tools**
- axe-core: Automated accessibility testing
- Pa11y: Continuous accessibility monitoring
- WAVE: Browser-based testing
- Screen readers: Manual testing

### 3. Quality Dashboard

**Real-time Dashboard**
- Current quality gate status
- Code coverage trends
- Security vulnerability status
- Performance metrics
- Accessibility compliance

**Reporting**
- Weekly quality reports
- Monthly quality metrics review
- Quarterly quality audits
- Annual quality retrospective

---

## Appendix: Standards Mapping

### NIST SSDF v1.1 Mapping
- **PO.1**: Define security requirements → Security Quality Standards
- **PO.3**: Security requirements → Security Gate
- **PS.1**: Secure design → Code Quality Standards
- **PS.2**: Review design → Architecture Documentation
- **PW.1**: Secure coding → Code Quality + Security Standards
- **PW.2**: Build provenance → SBOM + Signing
- **PW.4**: Verify third-party → Dependency Security
- **PW.6**: Secure configuration → Configuration Standards
- **PW.7**: Review code → Review & Approval Standards
- **PW.8**: Test security → Security Testing
- **RV.1**: Vulnerability response → Continuous Improvement

### OWASP SAMM 2.0 Mapping
- **Governance**: Quality reviews, metrics tracking
- **Design**: Domain modeling, architecture documentation
- **Implementation**: Code quality, secure coding
- **Verification**: Testing standards, security testing
- **Operations**: Continuous monitoring, incident response

### ISO/IEC 25010 Mapping
- **Functional Suitability**: Business logic quality, testing
- **Performance Efficiency**: Performance quality standards
- **Compatibility**: Contract testing, API standards
- **Usability**: Accessibility standards, UX quality
- **Reliability**: Resilience patterns, error handling
- **Security**: Security quality standards
- **Maintainability**: Code quality, documentation
- **Portability**: Dependency management, configuration

### SLSA Level 3 Mapping
- **Source**: Version control, code review
- **Build**: Reproducible builds, SBOM generation
- **Provenance**: Signed artifacts, build attestation
- **Dependencies**: Dependency pinning, vulnerability scanning

---

**Version History**

- **1.0.0** (2025-10-12): Initial comprehensive quality standards document

---

**Maintained by**: Agentic Canon Contributors  
**Review Cycle**: Quarterly  
**Next Review**: 2026-01-12

---

*This document is part of the Agentic Canon framework for frontier software excellence.*

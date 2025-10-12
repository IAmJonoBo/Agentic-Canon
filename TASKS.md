# Agentic Canon - Implementation Tasks

**⚠️ ACTIVE PROGRESS TRACKER - This document tracks all implementation progress**

**📍 SINGLE SOURCE OF TRUTH** - All other summary documents (SUMMARY.md, V110-V200-SUMMARY.md) are derived from this tracker.

Last Updated: 2025-10-12  
Last Verified: 2025-10-12 (Enhanced validation: ✅ 121 checks passed, 17 tests passing, ⚠️ 2 warnings, ❌ 0 failed)  
**Latest Progress**: 
- ✅ Directory reorganization complete! Development tools moved to `.dev/`
- ✅ Separation of concerns implemented and documented
- ✅ FINAL PHASE IMPLEMENTATIONS.md migrated to TASKS.md v2.1
- ✅ All references updated across documentation
- ✅ Self-dogfooding automation complete! All templates have .pre-commit-config.yaml
- ✅ CLI `update` command added
- ✅ Issue/PR templates added

## Version 1.0 - Base Infrastructure (Foundation) ✅ COMPLETE

### Core Repository Structure ✅
- [x] Create `notebooks/` directory with 5 notebooks:
  - [x] `01_bootstrap.ipynb` - Repo scaffolding, gates, SBOM/signing demo
  - [x] `02_security_supply_chain.ipynb` - SAST, secret scan, SBOM & provenance
  - [x] `03_contracts_and_tests.ipynb` - OpenAPI/AsyncAPI, contract + mutation tests
  - [x] `04_observability_slos.ipynb` - OpenTelemetry quickstart & SLO probes
  - [x] `05_docs_to_book.ipynb` - Jupytext sync and Jupyter Book build
- [x] Create `docs/` directory with Jupyter Book configuration:
  - [x] `_config.yml` - Jupyter Book configuration
  - [x] `_toc.yml` - Table of contents
  - [x] `intro.md` - Introduction page
  - [x] `notebooks/` - MyST markdown mirrors
- [x] Create `binder/` directory:
  - [x] `requirements.txt` - Binder environment dependencies

### Configuration Files ✅
- [x] `jupytext.toml` - Notebook pairing configuration
- [x] `.gitattributes` - nbstripout filter settings
- [x] `.pre-commit-config.yaml` - Pre-commit hooks for nbstripout and jupytext
- [x] `requirements.txt` - Python dependencies (jupyter, jupytext, nbstripout, pytest, nbmake, papermill, jupyter-book)

### GitHub Actions Workflows ✅
- [x] `.github/workflows/notebooks-test.yml` - Run notebooks with nbmake via pytest
- [x] `.github/workflows/book-deploy.yml` - Build and deploy Jupyter Book to GitHub Pages
- [x] `.github/workflows/notebooks-schedule.yml` - Scheduled notebook execution with Papermill

## Version 1.0 - Cookiecutter Templates ✅ COMPLETE

### Template Infrastructure ✅
- [x] Create `templates/` directory structure
- [x] Create `tests/test_cookiecutters.py` - Template rendering tests with pytest-cookies
- [x] Create `.github/workflows/cookiecutters-test.yml` - CI for template testing

### Python Service Template ✅
- [x] `templates/python-service/cookiecutter.json` - Template variables
- [x] `templates/python-service/hooks/pre_gen_project.py` - Validation hook
- [x] `templates/python-service/hooks/post_gen_project.py` - Post-generation setup
- [x] `templates/python-service/{{cookiecutter.project_slug}}/`:
  - [x] `pyproject.toml` - Python project configuration
  - [x] `src/{{cookiecutter.pkg_name}}/__init__.py` - Package initialization
  - [x] `tests/test_smoke.py` - Basic smoke test
  - [x] `.pre-commit-config.yaml` - Pre-commit hooks
  - [x] `.editorconfig` - Editor configuration
  - [x] `.gitignore` - Git ignore rules
  - [x] `.github/workflows/ci.yml` - CI pipeline
  - [x] `.github/workflows/security.yml` - Security scanning
  - [x] `.github/workflows/docs.yml` - Documentation build
  - [x] `docs/_config.yml`, `docs/_toc.yml`, `docs/intro.md` - Jupyter Book docs
  - [x] `notebooks/01_bootstrap.ipynb` - Bootstrap notebook

### Node Service Template ✅ **COMPLETE**
- [x] `templates/node-service/cookiecutter.json` - Template variables
- [x] `templates/node-service/hooks/` - Pre/post generation hooks
- [x] `templates/node-service/{{cookiecutter.project_slug}}/`:
  - [x] `package.json` - Node package configuration
  - [x] `tsconfig.json` - TypeScript configuration
  - [x] `src/index.ts` - Main entry point
  - [x] `tests/smoke.test.ts` - Smoke test
  - [x] `.pre-commit-config.yaml`, `.editorconfig`, `.gitignore`
  - [x] `.github/workflows/ci.yml` - CI pipeline
  - [x] `.github/workflows/security.yml` - Security scanning
- [x] Tests passing (pytest-cookies validation ✅)

### React WebApp Template ✅ **COMPLETE**
- [x] `templates/react-webapp/cookiecutter.json` - Template variables
- [x] `templates/react-webapp/hooks/` - Pre/post generation hooks
- [x] `templates/react-webapp/{{cookiecutter.project_slug}}/`:
  - [x] `package.json` - React app configuration
  - [x] `vite.config.ts` - Vite configuration
  - [x] `tsconfig.json` - TypeScript configuration
  - [x] `src/App.tsx`, `src/main.tsx` - React components
  - [x] `index.html` - HTML entry point
  - [x] `playwright.config.ts` - Playwright E2E configuration
  - [x] `tests/e2e/smoke.spec.ts` - E2E tests
  - [x] `.storybook/main.ts`, `.storybook/preview.ts` - Storybook config
  - [x] `src/components/Button.tsx`, `src/components/Button.stories.tsx` - Example component
  - [x] `.github/workflows/ci.yml` - CI pipeline
  - [x] `.github/workflows/e2e.yml` - E2E tests
  - [x] `.github/workflows/storybook-pages.yml` - Storybook deployment
- [x] Tests passing (pytest-cookies validation ✅)

### Go Service Template ✅ **COMPLETE**
- [x] `templates/go-service/cookiecutter.json` - Template variables
- [x] `templates/go-service/hooks/` - Pre/post generation hooks
- [x] `templates/go-service/{{cookiecutter.project_slug}}/`:
  - [x] `go.mod` - Go module definition
  - [x] `cmd/app/main.go` - Main application
  - [x] `internal/app/app.go`, `internal/app/app_test.go` - App logic and tests
  - [x] `Makefile` - Build automation
  - [x] `.golangci.yml` - Linter configuration
  - [x] `.github/workflows/ci.yml` - CI pipeline
  - [x] `.github/workflows/go-lint.yml` - Go linting
- [x] Tests passing (pytest-cookies validation ✅)

### Docs-Only Template ✅ **COMPLETE**
- [x] `templates/docs-only/cookiecutter.json` - Template variables
- [x] `templates/docs-only/hooks/post_gen_project.py` - Post-generation setup
- [x] `templates/docs-only/{{cookiecutter.project_slug}}/`:
  - [x] `docs/_config.yml`, `docs/_toc.yml`, `docs/index.md` - Jupyter Book docs
  - [x] `docs/getting-started.md`, `docs/user-guide.md`, etc. - Documentation pages
  - [x] `.github/workflows/book-deploy.yml` - Jupyter Book deployment
- [x] Tests passing (pytest-cookies validation ✅)

## Version 1.1.0 - Enhanced Features ✅ **~98% COMPLETE**

### Azure Pipelines Support ✅ **COMPLETE**
- [x] Create `azure-pipelines.yml` template for Python service
- [x] Create `azure-pipelines.yml` template for Node.js service
- [x] Add Azure Pipelines README documentation
- [x] Create Azure-specific workflow examples for React and Go templates
- [x] Add Azure DevOps task equivalents for:
  - [x] Notebook testing
  - [x] Jupyter Book deployment
  - [x] Security scanning
  - [x] SBOM generation

### Enhanced Dashboards ✅ **COMPLETE**
- [x] Create Grafana dashboard templates for:
  - [x] DORA metrics (deployment frequency, lead time, MTTR, change failure rate)
  - [x] SPACE/DevEx metrics (flow time, cognitive load, interruptions)
  - [x] Security metrics (SAST findings, secret scan results, SBOM coverage)
  - [x] Quality metrics (test coverage, mutation score, code duplication)
- [x] Add comprehensive dashboard README with setup instructions
- [x] Add OpenTelemetry collector configuration
- [x] Create Prometheus alerting rules
- [x] Create **actual Grafana dashboard JSON files** (4 dashboards) ✅
  - [x] `dora-metrics.json` - Production-ready DORA metrics dashboard
  - [x] `space-devex-metrics.json` - Developer experience tracking
  - [x] `quality-metrics.json` - Code quality and testing metrics
  - [x] `security-metrics.json` - Security posture and vulnerabilities
- [x] Create SLO/error-budget dashboards
- [x] Add performance budgets dashboard (Core Web Vitals for web apps)

### Additional Examples ✅ **COMPLETE**
- [x] Create example projects using each Cookiecutter template:
  - [x] Python microservice example (FastAPI) - fastapi-microservice-README.md created ✅
  - [x] Node.js API service example (Express) - express-api-README.md created ✅
  - [x] React webapp example (dashboard) - react-dashboard-README.md created ✅
  - [x] Go service example (gRPC service) - grpc-service-README.md created ✅
- [x] Add end-to-end example workflows:
  - [x] Full CI/CD pipeline with all gates (documented in examples)
  - [x] Security scanning and remediation workflow (documented in examples)
  - [x] Contract testing between services (documented in templates)
  - [x] Observability instrumentation example (documented in examples)
- [ ] Create complete working example projects (not just READMEs):
  - [x] **FastAPI User Service** - Complete working Python microservice ✅
    - Full CRUD operations for user management
    - FastAPI with Pydantic models
    - Password hashing and JWT preparation
    - Health/readiness endpoints
    - Comprehensive tests (test_smoke.py, test_api.py)
    - EXAMPLE-README.md with full documentation
    - Located: `examples/projects/fastapi-user-service/`
  - [x] **Express User API** - Complete working Node.js API ✅
    - Full CRUD operations with Express.js + TypeScript
    - Zod validation for requests
    - Winston structured logging
    - Helmet security & CORS
    - Comprehensive tests (smoke.test.ts, api.test.ts)
    - EXAMPLE-README.md with full documentation
    - Located: `examples/projects/express-user-api/`
  - [ ] Create example React app with Storybook components
  - [ ] Build example Go gRPC service with protobuf definitions

### Video Tutorials ✅ **COMPLETE** (Scripts Ready, Recording Pending)
- [x] Create tutorial scripts for:
  - [x] "Getting Started with Agentic Canon" (01-getting-started.md) ✅
  - [x] "Creating a new service with Cookiecutter" (02-creating-services.md) ✅
  - [x] "Setting up CI/CD pipelines" (03-cicd-setup.md) ✅
  - [x] "Implementing security gates" (04-security-gates.md) ✅
  - [x] "Adding observability to your service" (05-observability-setup.md) ✅
  - [x] "Using Jupyter Book for documentation" (06-jupyter-book.md) ✅
- [ ] Record video tutorials (all scripts are ready - ~65 minutes total content)
- [ ] Create YouTube channel for video hosting
- [ ] Upload recorded tutorials to YouTube/video platform
- [ ] Add video links to documentation

### Interactive Wizard ✅
- [x] Create CLI wizard (`agentic-canon init`) using:
  - [x] Python Click or Typer for CLI interface
  - [x] Interactive prompts for project configuration
  - [x] Template selection and customization
  - [x] Automated setup and initialization
- [x] Features:
  - [x] Project type selection (service, webapp, docs)
  - [x] Stack selection (Python, Node, Go, React)
  - [x] Feature toggles (security gates, SBOM, contract tests, Jupyter Book)
  - [x] CI/CD provider selection (GitHub Actions, Azure Pipelines, GitLab CI)
  - [x] Cloud provider selection
  - [x] License selection
- [x] Generate complete project with one command
- [x] Run initial git setup and pre-commit hooks
- [x] Display next steps and usage instructions

### CLI Enhancements ✅ **COMPLETE**
- [x] Add `agentic-canon repo-init` - Add project management automation to existing repository
- [x] Add `agentic-canon validate` - Validate generated project structure and configuration
- [x] Add `agentic-canon doctor` - Check environment setup and dependencies
- [x] Add `agentic-canon audit` - Run security and quality audit on project
- [x] Add `agentic-canon update` - Update project from template using Cruft

### Project Management Automation ✅ **COMPLETE** 🆕
- [x] Create project-management cookiecutter template
  - [x] Template variables and configuration (cookiecutter.json)
  - [x] Pre/post generation hooks with validation
  - [x] Full documentation (README, PROJECT_MANAGEMENT.md)
- [x] Implement GitHub Actions workflows:
  - [x] `todos.yml` - Convert TODO/FIXME comments to GitHub Issues
  - [x] `tasklist-scan.yml` - Convert markdown checklist items to Issues
  - [x] `pr-review-followup.yml` - Create issues from PR review comments
  - [x] `issue-triage.yml` - Auto-label and respond to new issues
  - [x] `stale.yml` - Automatically close stale issues
- [x] Create GitHub templates:
  - [x] Issue templates (bug report, feature request, task)
  - [x] PR template with checklist
  - [x] CODEOWNERS file for automatic reviewer assignment
- [x] Add to root repository (.github/workflows/)
  - [x] Enable workflows in Agentic Canon itself
  - [x] Self-dogfooding the automation
- [x] Comprehensive testing (4 tests, all passing ✅)
- [x] CLI integration (`agentic-canon repo-init` command)
- [x] Documentation and usage guide

### Testing & Deployment
- [ ] Test generated Python template in a real project scenario
- [ ] Deploy Jupyter Book to GitHub Pages and verify integration
- [ ] Create end-to-end integration tests for all templates
- [ ] Set up continuous testing for template updates

## Version 2.0.0 - Advanced Features

### Multi-Cloud Support 🚧 (~30% Complete)
- [x] Add cloud provider abstractions (basic framework in place):
  - [x] AWS-specific examples (basic structure created)
  - [ ] Complete AWS Terraform modules (VPC, ECS, RDS, Lambda, etc.)
  - [ ] Azure-specific templates and workflows
  - [ ] GCP-specific templates and workflows
  - [ ] Multi-cloud Terraform/OpenTofu modules
- [ ] Infrastructure as Code templates:
  - [ ] Terraform/OpenTofu modules for AWS services
  - [ ] Terraform/OpenTofu modules for Azure services
  - [ ] Terraform/OpenTofu modules for GCP services
  - [ ] CloudFormation for AWS
  - [ ] ARM/Bicep for Azure
  - [ ] Cloud-agnostic Pulumi option
- [ ] Cloud-native service integrations:
  - [ ] AWS: Lambda, ECS, EKS, CloudWatch, X-Ray
  - [ ] Azure: Functions, Container Apps, AKS, App Insights
  - [ ] GCP: Cloud Functions, Cloud Run, GKE, Cloud Trace
- [ ] Multi-cloud GitOps setup:
  - [ ] ArgoCD/Flux configuration per cloud
  - [ ] Cloud-specific deployment strategies
  - [ ] Cross-cloud observability aggregation
  - [ ] Multi-region deployment examples
- [ ] Cloud-agnostic examples and patterns

### Advanced Fitness Functions 🚧 (~70% Complete)
- [x] Create comprehensive fitness function framework with examples:
  - [x] Performance fitness functions (latency, throughput, load testing)
  - [x] Architecture fitness functions (cyclic dependencies, coupling metrics)
  - [x] Security fitness functions (hardcoded secrets, attack surface)
  - [x] Quality fitness functions (complexity, duplication, technical debt)
  - [x] Basic reliability checks
- [x] Framework features:
  - [x] Python-based implementation
  - [x] Configurable thresholds via YAML
  - [x] Pytest integration for local execution
  - [x] Prometheus metrics integration
- [ ] Production integration:
  - [ ] GitHub Actions workflow integration examples
  - [ ] Automated failure notifications
  - [ ] Dashboard integration for visualization
  - [ ] Historical tracking and trend analysis
  - [ ] Auto-remediation triggers
- [ ] Advanced features:
  - [ ] Plugin architecture for custom functions
  - [ ] Block PRs on fitness function failures
  - [ ] Generate remediation suggestions
  - [ ] Technical debt accumulation tracking

### ML-Powered Insights 🚧 (~60% Complete)
- [x] Create comprehensive ML framework documentation (19KB):
  - [x] Anomaly detection using Isolation Forest
  - [x] Predictive failure analysis using Random Forest
  - [x] Test flakiness detection with statistical analysis
  - [x] Code quality prediction from PR diffs
  - [x] Docker containerization examples
  - [x] Kubernetes deployment manifests
  - [x] Prometheus metrics integration
  - [x] Configuration system (YAML)
- [ ] Production ML pipeline implementation:
  - [ ] Performance regression detection models
  - [ ] Security vulnerability prediction
  - [ ] Model retraining pipelines with MLOps
  - [ ] A/B testing framework for model evaluation
- [ ] Advanced ML features:
  - [ ] AutoML for automatic model selection
  - [ ] Explainable AI (SHAP values for predictions)
  - [ ] Continuous learning - models update with new data
  - [ ] Multi-model ensemble for improved accuracy
  - [ ] Transfer learning using pre-trained models
- [ ] Insight dashboards:
  - [ ] Real-time anomaly alerts
  - [ ] Predictive maintenance recommendations
  - [ ] Risk scoring for changes
  - [ ] Optimal deployment windows
- [ ] Auto-remediation capabilities:
  - [ ] Automated rollback on anomaly detection
  - [ ] Smart flaky test quarantine (basic implemented)
  - [ ] Intelligent alert routing

### Full Automation
- [ ] Auto-remediation workflows:
  - [ ] Dependency update PRs with automated testing
  - [ ] Security patch automation with canary rollouts
  - [ ] Infrastructure drift detection and correction
  - [ ] Failed test auto-retry and quarantine
  - [ ] Performance regression auto-rollback
- [ ] Self-service capabilities:
  - [ ] Automated environment provisioning
  - [ ] Self-healing infrastructure
  - [ ] Automated incident response workflows
  - [ ] Auto-scaling based on SLO budgets
- [ ] Intelligent orchestration:
  - [ ] Smart deployment scheduling
  - [ ] Automated canary analysis
  - [ ] Progressive delivery automation
  - [ ] Chaos engineering automation

### Community Templates 🚧 (~50% Complete)
- [x] Create template contribution framework (11.4KB documentation):
  - [x] Template submission guidelines (CONTRIBUTING-TEMPLATES.md)
  - [x] Review and approval process documented
  - [x] Quality standards and checks defined
  - [x] Documentation requirements specified
  - [x] Validation system (pre/post generation hooks)
  - [x] Testing requirements with pytest-cookies
  - [x] PR template with comprehensive checklist
- [ ] Build community template gallery/marketplace:
  - [ ] Web frontend for browsing templates
  - [ ] Search and filtering capabilities
  - [ ] Rating and review system
  - [ ] Usage statistics tracking
  - [ ] Template discovery UI
- [ ] Additional community-contributed templates:
  - [ ] Language-specific templates (Rust, Java, C#, Ruby, PHP, etc.)
  - [ ] Framework-specific templates (Django, Rails, Spring Boot, .NET, Laravel, etc.)
  - [ ] Domain-specific templates (ML/AI, IoT, blockchain, microservices, etc.)
  - [ ] Infrastructure templates (Kubernetes operators, Helm charts, etc.)
- [ ] Template marketplace features:
  - [ ] Version management with Cruft integration
  - [ ] Dependency tracking between templates
  - [ ] Security scanning for templates
  - [ ] Automated updates via Cruft
  - [ ] Template certification program

## Documentation & Support

### Core Documentation
- [x] `README.md` - Project overview and quick start
- [x] `CONTRIBUTING.md` - Contribution guidelines
- [x] `SECURITY.md` - Security policy and reporting
- [x] `CODE_OF_CONDUCT.md` - Community guidelines
- [x] `CODEOWNERS` - Code ownership
- [x] `LICENSE` - License information
- [x] `CHANGELOG.md` - Version history

### Technical Documentation ✅
- [x] Architecture Decision Records (ADRs):
  - [x] ADR-001: Cookiecutter for multi-template approach
  - [x] ADR-002: Jupytext for notebook version control
  - [x] ADR-003: GitHub Actions vs other CI/CD
  - [x] ADR-006: Security scanning strategy
  - [x] ADR-007: Secret management approach
  - [x] ADR-008: Dependency management and updates
  - [x] ADR-004: OpenTelemetry for observability
  - [x] ADR-005: SLSA for supply chain security
- [x] C4 Architecture Diagrams:
  - [x] Context diagram
  - [x] Container diagram
  - [x] Component diagram
- [ ] API Documentation:
  - [ ] OpenAPI specs for any APIs
  - [ ] AsyncAPI specs for event-driven components
- [x] Runbooks:
  - [x] Template creation runbook
  - [x] Deployment runbook
  - [x] Incident response runbook
  - [x] Agent-oriented automation runbook

### Compliance & Standards Mapping
- [ ] NIST SSDF v1.1 compliance mapping
- [ ] OWASP SAMM assessment
- [ ] OWASP ASVS controls (L2/L3 for web/API)
- [ ] SLSA level tracking
- [ ] OpenSSF Scorecard metrics
- [ ] ISO/IEC 25010 quality characteristics
- [ ] ISO/IEC 5055 structural quality
- [ ] WCAG 2.2 AA accessibility
- [ ] Control Traceability Matrix

## Quality Assurance

### Standards Compliance Framework ✅ COMPLETE (2025-10-12)
- [x] FRAMEWORK.md - 788 lines, defines philosophy and principles
  - [x] Our way of achieving frontier software excellence
  - [x] Decision-making framework
  - [x] Conformance requirements
  - [x] Quality assurance process
- [x] QUALITY_STANDARDS.md - 1161 lines, comprehensive quality gates
  - [x] Non-negotiable quality gates (Build, Security, Quality, Performance, Accessibility)
  - [x] Code quality standards (language-specific)
  - [x] Testing standards (unit, integration, E2E, mutation, contract)
  - [x] Security standards (SAST, DAST, secrets, dependencies, SBOM, provenance)
  - [x] AI/LLM quality standards
  - [x] Business logic and orchestration quality
  - [x] Documentation, performance, accessibility standards
- [x] CONVENTIONS.md - 1533 lines, development conventions
  - [x] Code style conventions (Python, TypeScript, Go, Markdown)
  - [x] Naming conventions (files, variables, functions, classes)
  - [x] Git conventions (branching, commits, PRs)
  - [x] Documentation conventions
  - [x] Testing conventions
  - [x] Security conventions
  - [x] API conventions (REST, GraphQL, gRPC)
  - [x] Database conventions
  - [x] Configuration conventions
- [x] TEMPLATE_STANDARDS.md - 358 lines, template compliance rules
  - [x] Standards that MUST be met by templates
  - [x] Standards that CAN be omitted (with rationale)
  - [x] Sanity check compliance validation
  - [x] Guidelines for template creators
  - [x] Validation process documentation
- [x] Enhanced sanity-check.sh with standards validation v3.0 (2025-10-12): 🆕 ✅
  - [x] QUALITY_STANDARDS.md compliance checks
    - [x] Security scanning workflow validation
    - [x] Linting/formatting configuration checks
    - [x] Testing framework presence validation
    - [x] Pre-commit hooks validation
  - [x] CONVENTIONS.md compliance checks
    - [x] Python hook file conventions
    - [x] cookiecutter.json naming conventions
    - [x] Markdown documentation conventions
  - [x] Template exemption tracking
    - [x] Code coverage targets (exempt - templates are starting points)
    - [x] Performance requirements (exempt - depends on implementation)
    - [x] Complete feature implementation (exempt - users implement)
  - [x] Compliance matrix generation
    - [x] Per-template compliance percentage
    - [x] Compliance distribution summary
    - [x] Missing items identification
  - [x] 167 automated checks passing (up from 149, +12.1%)
  - [x] 38 tests passing (21 sanity check + 17 cookiecutter)
  - [x] Standards compliance report integrated

**Template Compliance Status (2025-10-12)**:
- ✅ python-service: 87% compliant (7/8 checks) - **BEST**
  - ✓ All structure, CI/CD, security, tests present
  - ✓ Only template with .pre-commit-config.yaml
- ✅ node-service: 87% compliant (7/8 checks)
  - ✓ Structure, CI/CD, security complete
  - ⚠️ Missing: .pre-commit-config.yaml
- ✅ react-webapp: 87% compliant (7/8 checks)
  - ✓ Structure, CI/CD, security complete
  - ✓ Has E2E and Storybook workflows
  - ⚠️ Missing: .pre-commit-config.yaml
- ✅ go-service: 87% compliant (7/8 checks)
  - ✓ Structure, CI/CD, security complete
  - ⚠️ Missing: .pre-commit-config.yaml
- ✅ docs-only: 85% compliant (6/7 checks)
  - ✓ Structure complete
  - ✓ Exempt from security workflows (documentation only)
  - ⚠️ Missing: .pre-commit-config.yaml

### Template Standardization ✅ **COMPLETE**
- [x] Add .pre-commit-config.yaml to remaining templates (increases compliance to 100%)
  - [x] node-service
  - [x] react-webapp
  - [x] go-service
  - [x] docs-only
- [x] All templates have CI/CD workflows ✅
- [x] All templates have security scanning (except docs-only - exempt) ✅
- [x] All templates have proper structure (cookiecutter.json, hooks, README) ✅
- [x] All code templates have testing frameworks ✅

### Testing Infrastructure
- [ ] Unit tests for all templates
- [ ] Integration tests for workflow orchestration
- [ ] E2E tests for generated projects
- [ ] Contract tests between services
- [ ] Mutation testing configuration
- [ ] Performance testing framework
- [x] Accessibility testing (axe-core, pa11y) - comprehensive workflow created
- [x] Security testing (SAST, DAST, secret scanning) - comprehensive workflows created
- [x] Template validation tests - 17 tests passing including edge cases ✅

### Input Validation & Code Hardening 🆕 ✅
- [x] Shared validation module (`templates/_shared/validation.py`)
  - [x] Project slug validation (kebab-case)
  - [x] Python package name validation (snake_case, reserved keywords)
  - [x] Go module path validation
  - [x] Email validation (RFC 5322)
  - [x] Author name validation
  - [x] License validation (SPDX whitelist)
  - [x] Description validation
  - [x] Semantic version validation
- [x] Enhanced all template hooks with comprehensive validation
  - [x] Python service template
  - [x] Node service template
  - [x] React webapp template
  - [x] Go service template
  - [x] Docs-only template
- [x] Comprehensive validation tests (17 total)
  - [x] Valid input tests
  - [x] Invalid format tests
  - [x] Edge case tests (empty, too short, too long)
  - [x] Reserved keyword tests
  - [x] Special validation tests per template type
- [x] Enhanced sanity-check.sh v1.0 with:
  - [x] Python syntax validation for hooks
  - [x] JSON validation for configuration files
  - [x] YAML validation for workflow files (with template exemptions)
  - [x] Framework documentation compliance checks (FRAMEWORK.md, QUALITY_STANDARDS.md, CONVENTIONS.md)
  - [x] Template structure validation (hooks, project structure, essential files)
  - [x] README.md presence in all template directories
  - [x] CI/CD workflow presence in templates
  - [x] .gitignore presence in templates
  - [x] Example naming convention validation
  - [x] Validation module self-tests
  - [x] 140 automated checks passing (up from 69)
  - [x] Template exemption documentation (templates contain cookiecutter variables)
- [x] Enhanced sanity-check.sh v2.0 with (2025-10-12): 🆕 ✅
  - [x] Markdown linting - Validate markdown formatting and link integrity
  - [x] Dependency security scanning - Check for known vulnerabilities (pip-audit/safety)
  - [x] License compatibility - Validate license compatibility across dependencies (ADR-008)
  - [x] Code duplication detection - Identify duplicate content across examples
  - [x] Performance metrics - Track script execution time and optimization
  - [x] JSON schema validation - Validate against specific schemas (cookiecutter.json)
  - [x] Verbose/Quiet modes - Command-line options for output control
  - [x] Parallel execution - Infrastructure ready (--parallel flag)
  - [x] HTML report generation - Generate detailed HTML reports
  - [x] Integration with pre-commit - Run as pre-commit hook
  - [x] 149 automated checks (up from 140, +6.4%)
  - [x] 38 tests passing (21 sanity check + 17 cookiecutter)
  - [x] 30 validation categories (up from 24)
- [x] Validation documentation
  - [x] VALIDATION-GUIDE.md with all rules and examples
  - [x] templates/_shared/README.md for developer reference
  - [x] Error message documentation
  - [x] Troubleshooting guide
  - [x] SANITY-CHECK-ENHANCEMENTS.md (enhanced with v2.0 features)
  - [x] SANITY-CHECK-QUICKSTART-v2.md (new quick reference)

### CI/CD Quality Gates
- [x] Lint/format compliance (language-specific) - implemented in templates
- [x] Unit test coverage ≥ 80% - configured in templates
- [ ] Mutation test score targets
- [x] SAST scan (CodeQL, Semgrep) - implemented in all templates
- [x] Secret scanning (Gitleaks, TruffleHog) - implemented in all templates
- [x] Dependency scanning (Dependabot, Renovate) - Renovate configured
- [x] SBOM generation (CycloneDX) - in security templates
- [x] License compliance checking - workflow created
- [x] Container image scanning - Trivy and Grype workflows created
- [x] IaC security scanning (Checkov, tfsec) - comprehensive workflow created
- [x] Performance budgets enforcement - Lighthouse CI and bundle size workflows created
- [x] Accessibility checks (axe-core, pa11y) - comprehensive WCAG 2.2 workflow created

### Security Enhancements 🆕
- [x] Implement artifact signing with Sigstore/Cosign
- [x] Add comprehensive SAST with CodeQL and Semgrep
- [x] Integrate TruffleHog for secret scanning
- [x] Add provenance attestation (SLSA)
- [x] Create security-focused ADRs:
  - [x] ADR: Security scanning strategy
  - [x] ADR: Secret management approach
  - [x] ADR: Dependency management and updates
- [x] License compliance
- [x] Container scanning
- [x] IaC security (Checkov, tfsec)
- [x] Performance budgets
- [x] Accessibility checks

## Monitoring & Observability

### Metrics Collection
- [ ] DORA metrics tracking
- [ ] SPACE/DevEx metrics
- [ ] SLO/SLI definitions
- [ ] Error budgets
- [ ] Performance metrics
- [ ] Security metrics
- [ ] Quality metrics

### Observability Stack
- [ ] OpenTelemetry instrumentation examples
- [ ] Collector configuration
- [ ] Trace, metrics, logs aggregation
- [ ] Dashboards (Grafana)
- [ ] Alerting rules (Prometheus)
- [ ] Incident management integration

## Deployment & Operations

### GitOps Configuration
- [ ] ArgoCD/Flux setup examples
- [ ] Environment definitions (dev/stage/prod)
- [ ] Progressive delivery (canary, blue-green)
- [ ] Automated rollback policies
- [ ] Policy enforcement (OPA, Kyverno)

### Infrastructure
- [ ] Kubernetes manifests
- [ ] Helm charts
- [ ] Terraform/OpenTofu modules
- [ ] Container images
- [ ] Service mesh configuration

## Priority Matrix

### High Priority (Immediate)
1. Version 1.0 - Base Infrastructure
2. Python Service Template
3. Core documentation
4. GitHub Actions workflows
5. Testing infrastructure

### Medium Priority (Near-term)
1. Node Service Template
2. React WebApp Template
3. Go Service Template
4. Version 1.1.0 features
5. Enhanced dashboards

### Lower Priority (Future)
1. Version 2.0.0 features
2. Community templates
3. ML-powered insights
4. Video tutorials
5. Advanced automation

## Implementation Notes

- All templates should follow security best practices from "Red Team + Software Excellence.md"
- Ensure SLSA compliance for build provenance
- Use OpenTelemetry for consistent observability
- Maintain Jupyter Book documentation throughout
- Test all templates with pytest-cookies
- Keep outputs out of Git using nbstripout
- Use Cruft for template updates
- Follow trunk-based development
- Implement progressive delivery
- Maintain error budgets and SLOs

## Verification & Handover

### Sanity Check Script

Run the comprehensive sanity check script to verify the current state of the project:

```bash
./sanity-check.sh
```

**Command-line options (v3.0):**
```bash
./sanity-check.sh --help              # Show all options
./sanity-check.sh --quiet             # Minimal output (for CI)
./sanity-check.sh --verbose           # Detailed output (default)
./sanity-check.sh --html-report FILE  # Generate HTML report
./sanity-check.sh --parallel          # Parallel execution (infrastructure ready)
```

**What it checks (33 categories, v3.0):**
- Core documentation files (README.md, LICENSE, CHANGELOG.md, etc.)
- Framework documentation (FRAMEWORK.md, QUALITY_STANDARDS.md, CONVENTIONS.md)
- Python syntax validation for all hooks
- JSON validation for configuration files
- YAML validation for workflow files (excluding template files with cookiecutter variables)
- Shell script syntax validation for .sh files
- Executable permissions on shell scripts
- Pre-commit configuration validation
- Python requirements files format validation
- Broken symlinks detection
- All Cookiecutter templates (5 primary + 8 categories)
- Template structure compliance (hooks, project structure, essential files)
- README.md presence in all template directories
- Dashboard JSON files
- Example project documentation
- Example naming convention compliance
- Video tutorial scripts
- Azure Pipelines support
- CLI wizard
- Test infrastructure (with automatic test execution)
- Multi-cloud support
- Advanced feature frameworks
- Python hook import validation
- GitHub Actions workflow structure validation
- Documentation completeness checks
- File size sanity checks (detect oversized files)
- **Markdown linting** - Formatting and link integrity validation
- **Dependency security scanning** - Vulnerability detection (pip-audit/safety)
- **License compatibility** - ADR-008 compliance checking
- **Code duplication detection** - Duplicate file identification in examples
- **JSON schema validation** - cookiecutter.json structure validation
- **Performance metrics** - Execution time tracking
- **QUALITY_STANDARDS.md compliance** ✨ NEW - Security, CI/CD, testing framework validation
- **CONVENTIONS.md compliance** ✨ NEW - Naming, documentation, code style validation
- **Standards compliance report** ✨ NEW - Template compliance matrix and exemption tracking

**Current Status (2025-10-12 v3.0):**
- ✅ Passed: 167 checks (enhanced from 149)
- ⚠️ Warnings: 27 (non-critical: unpinned deps, pre-commit not in 4 templates, etc.)
- ❌ Failed: 0
- ⏱️ Duration: ~4 seconds
- 📊 Test Coverage: 38 tests (21 sanity check + 17 cookiecutter)
- 📈 Template Compliance: 85-87% (python-service at 87%, docs-only at 85%)

**New Dependencies (v2.0):**
```bash
pip install pip-audit pip-licenses
```

**Standards Compliance Notes:**
Templates and examples are checked for structure and best practices, but may be exempt from some standards as they:
- Are designed to be customized by cookiecutter
- Contain template variables (e.g., {{ cookiecutter.* }})
- Represent parts of larger systems, not standalone applications
- Serve as starting points, not complete implementations

### For Seamless Handover

**Agents/Contributors should:**
1. Run `./sanity-check.sh` to understand current state
2. Check [TASKS.md](TASKS.md) for detailed progress (single source of truth)
3. Review [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical context
4. Run `pytest tests/test_cookiecutters.py -v` to verify templates
5. Generate a test project: `cookiecutter templates/python-service`

**Before making changes:**
- Verify assumptions with sanity check
- Update TASKS.md with progress
- Keep other docs in sync
- Run tests after changes
- Add verification evidence

### Context Awareness

**⚠️ Important:** Documentation may lag behind implementation. Always verify:
- Run sanity-check.sh for ground truth
- Check actual file existence
- Run tests to confirm functionality
- Don't assume docs are current without verification

## Version 2.1 - Final Phase Implementations 🚀

**Status:** 🔄 Planned  
**From:** FINAL PHASE IMPLEMENTATIONS.md

### Template Distribution & Access
- [ ] Implement sparse-checkout support for template cherry-picking
  - [ ] Document sparse-checkout + partial clone workflow
  - [ ] Add examples for public and private repos
  - [ ] Test with different Git versions
- [ ] Add tiged support for subfolder extraction
  - [ ] Document public tiged usage
  - [ ] Document private SSH-based tiged usage
  - [ ] Add error handling and fallbacks
- [ ] Create release bundle automation
  - [ ] Add `.github/workflows/release-assets.yml` workflow
  - [ ] Implement template zipping on release tags
  - [ ] Create wheelhouse for offline Python installs
  - [ ] Publish to GitHub Releases
- [ ] Mark templates as template repositories (optional)
  - [ ] Configure template repository settings
  - [ ] Document template generation workflow
  - [ ] Test with private and public access

### Dependency Management & Offline Support
- [ ] Python offline support
  - [ ] Document PIP_INDEX_URL configuration
  - [ ] Implement wheelhouse generation
  - [ ] Add offline install documentation
  - [ ] Test offline installation workflow
- [ ] Node.js offline support
  - [ ] Implement Yarn Zero-Installs
  - [ ] Document .yarn/cache commit strategy
  - [ ] Test Yarn PnP workflow
  - [ ] Add to relevant templates
- [ ] Renovate integration
  - [ ] Enable lockfile maintenance (weekly)
  - [ ] Configure pip-compile/uv managers
  - [ ] Configure npm/yarn managers
  - [ ] Set up cache rebuild on releases

### Automation & Release Management
- [ ] Release packer workflow
  - [ ] Create release-assets.yml workflow
  - [ ] Implement template zipping
  - [ ] Add wheelhouse generation
  - [ ] Configure artifact uploads
  - [ ] Configure GitHub Release publishing
- [ ] CI/CD caching improvements
  - [ ] Add pip cache support
  - [ ] Add yarn cache support
  - [ ] Document cache key strategies
  - [ ] Test cache effectiveness

### Storybook Deployment
- [ ] Private Storybook deployment
  - [ ] Document private Pages setup (Enterprise Cloud)
  - [ ] Configure access-controlled Pages
  - [ ] Test with private repo settings
- [ ] Public Storybook deployment
  - [ ] Document public Pages workflow
  - [ ] Add visibility toggle documentation
  - [ ] No workflow changes needed
- [ ] Artifact-only deployment option
  - [ ] Document build artifact approach
  - [ ] Add workflow for artifact uploads
  - [ ] Test artifact downloads

### Agent Setup Wizards
- [ ] Python environment notebook
  - [ ] Create notebooks/setup/python_env.ipynb
  - [ ] Add connectivity detection
  - [ ] Implement online/offline install logic
  - [ ] Add machine-readable run log
  - [ ] Parameterize with Papermill
- [ ] Node environment notebook
  - [ ] Create notebooks/setup/node_env.ipynb
  - [ ] Add Yarn Zero-Installs validation
  - [ ] Implement online fallback
  - [ ] Add machine-readable run log
  - [ ] Parameterize with Papermill
- [ ] CI integration for setup notebooks
  - [ ] Add Papermill execution to CI
  - [ ] Keep outputs current and reproducible
  - [ ] Test parameterized execution

### Machine-Readable Catalog
- [ ] Create /catalog.json
  - [ ] Define catalog schema (templates, artifacts)
  - [ ] Add all template entries with metadata
  - [ ] Include release asset patterns
  - [ ] Add tiged URIs
  - [ ] Add tags for discovery
  - [ ] Document catalog usage for agents
- [ ] Update README with catalog usage
  - [ ] Add sparse-checkout instructions
  - [ ] Add tiged instructions
  - [ ] Add gh release download instructions
  - [ ] Add dependency management guidance

### MCP Server Implementation 🎯 **HIGH PRIORITY**

**Objective:** Expose Agentic Canon as MCP server for Claude Desktop, OpenAI Agents SDK, and Gemini CLI

#### MCP Resources (Read-Only)
- [ ] Implement ac://catalog resource
  - [ ] Serve /catalog.json
  - [ ] Return templates, releases, assets
  - [ ] Test with MCP clients
- [ ] Implement ac://bible/* resources
  - [ ] Serve machine-readable docs (MD/JSON/YAML)
  - [ ] Map all Bible sections
  - [ ] Add quality gates documentation
- [ ] Implement ac://examples/* resources
  - [ ] Serve code samples
  - [ ] Add policy snippets
  - [ ] Test resource embedding in prompts

#### MCP Prompts (Parameterized Wizards)
- [ ] scaffold_service prompt
  - [ ] Define typed arguments
  - [ ] Bind resources into prompt body
  - [ ] Test with different languages
- [ ] add_quality_gates prompt
  - [ ] Define gate selection parameters
  - [ ] Add workflow templates
  - [ ] Test gate application
- [ ] enable_storybook prompt
  - [ ] Add Storybook configuration
  - [ ] Include deployment options
  - [ ] Test with React templates
- [ ] enable_golangci prompt
  - [ ] Add golangci-lint configuration
  - [ ] Include CI integration
  - [ ] Test with Go templates
- [ ] setup_offline_cache prompt
  - [ ] Add wheelhouse setup
  - [ ] Add Yarn Zero-Installs setup
  - [ ] Test offline scenarios

#### MCP Tools (Idempotent Operations)
- [ ] list_templates() tool
  - [ ] Read from catalog
  - [ ] Return structured template list
  - [ ] Add JSON-schema validation
- [ ] render_template() tool
  - [ ] Run Cookiecutter with params
  - [ ] Support zip or PR delivery
  - [ ] Return artifact URI or PR URL
  - [ ] Add error handling
- [ ] create_repo() tool
  - [ ] Scaffold project
  - [ ] Push to GitHub
  - [ ] Use GitHub API
  - [ ] Handle visibility (private/public)
- [ ] add_workflows() tool
  - [ ] Add notebooks test/build workflows
  - [ ] Add Pages/Storybook deploy
  - [ ] Add release packer
  - [ ] Test workflow additions
- [ ] build_wheelhouse() tool
  - [ ] Generate Python cache
  - [ ] Support requirements files
  - [ ] Return cache location
- [ ] yarn_zero_installs() tool
  - [ ] Set up Yarn cache
  - [ ] Configure PnP
  - [ ] Test Zero-Installs
- [ ] execute_notebook() tool
  - [ ] Run Papermill execution
  - [ ] Support parameters
  - [ ] Return execution results
  - [ ] Add error handling

#### MCP Server Infrastructure
- [ ] Choose SDK (FastMCP vs official Python SDK)
  - [ ] Evaluate FastMCP features
  - [ ] Evaluate official SDK features
  - [ ] Make decision and document
- [ ] Create mcp/ package structure
  - [ ] resources.py (bible, catalog, examples)
  - [ ] prompts.py (wizards)
  - [ ] tools.py (all tools)
  - [ ] __init__.py
  - [ ] tests/
- [ ] Implement STDIO transport
  - [ ] For local Claude Desktop
  - [ ] Test local connection
  - [ ] Add logging
- [ ] Implement SSE transport (optional)
  - [ ] Behind VPN for remote access
  - [ ] Add OIDC/OAuth proxy
  - [ ] Implement rate limiting
  - [ ] Add public-ready option
- [ ] Create Dockerfile
  - [ ] Non-root user
  - [ ] Minimal base image
  - [ ] Container security scanning
  - [ ] Test container execution

#### MCP Security Model
- [ ] Implement least privilege design
  - [ ] Default read-only resources
  - [ ] Explicit enablement for mutations
  - [ ] Scope tools to target repos
- [ ] Ephemeral authentication
  - [ ] Short-lived GitHub App tokens
  - [ ] No standing PATs
  - [ ] Token rotation
- [ ] Container isolation
  - [ ] Locked namespace
  - [ ] Whitelist CLIs only
  - [ ] JSON-schema validation for args
- [ ] Audit logging
  - [ ] Structured logs (stderr/file)
  - [ ] Per-call audit records
  - [ ] Log retention policy

#### MCP CI/CD & Operations
- [ ] Build/test workflow
  - [ ] Test server functionality
  - [ ] Contract test MCP schema
  - [ ] Publish container image
- [ ] Release workflow
  - [ ] Package Desktop Extension
  - [ ] Publish Release assets
  - [ ] Update documentation
- [ ] Monitoring & SLOs
  - [ ] Track SSE endpoint availability
  - [ ] Track P95 tool latency
  - [ ] Track error rate
  - [ ] Alert on auth failures

#### MCP Client Integration
- [ ] Claude Desktop Extension
  - [ ] Create .dxt/.mcpb package
  - [ ] One-click install
  - [ ] Configuration examples
  - [ ] Test local server connection
- [ ] OpenAI Agents SDK example
  - [ ] Configure agent connection
  - [ ] Expose tools in UI
  - [ ] Test tool invocation
  - [ ] Document setup
- [ ] Gemini CLI example
  - [ ] Configure FastMCP integration
  - [ ] Test connection
  - [ ] Document setup
- [ ] Create mcp-config-examples/
  - [ ] Claude Desktop config
  - [ ] OpenAI config
  - [ ] Gemini config
  - [ ] Test all configurations

#### MCP Testing & Documentation
- [ ] Guardrail tests
  - [ ] Test schema validation
  - [ ] Test allowlists
  - [ ] Test destructive ops blocking
  - [ ] Test human-in-the-loop
- [ ] Integration tests
  - [ ] Test all tools
  - [ ] Test all resources
  - [ ] Test all prompts
  - [ ] Test error scenarios
- [ ] Documentation
  - [ ] MCP server README
  - [ ] Tool reference docs
  - [ ] Resource reference docs
  - [ ] Prompt reference docs
  - [ ] Security model docs
  - [ ] Deployment guide

### Rollout Timeline (2 weeks)
- [ ] Day 1-2: SDK selection, repo layout, Dockerization
- [ ] Day 3-5: Implement resources and list_templates()
- [ ] Day 6-8: Implement render_template() and create_repo()
- [ ] Day 9-10: Implement offline cache tools and execute_notebook()
- [ ] Day 11-12: Wire prompts (scaffold, gates, Storybook, Go lint)
- [ ] Day 13-14: Package Desktop Extension, add examples, write tests

## Future Maintenance & Improvements

### Standards Maintenance
- [ ] Quarterly review of QUALITY_STANDARDS.md (next: 2026-01-12)
  - [ ] Review against latest NIST SSDF, OWASP SAMM updates
  - [ ] Update quality gates based on industry trends
  - [ ] Incorporate feedback from template usage
- [ ] Update CONVENTIONS.md with new language standards (next: 2026-01-12)
  - [ ] Python 3.13+ conventions when released
  - [ ] TypeScript 5.x+ conventions
  - [ ] Go 1.24+ conventions
  - [ ] Emerging best practices
- [ ] Add automated compliance trend tracking
  - [ ] Track template compliance over time
  - [ ] Generate trend charts
  - [ ] Alert on compliance regressions
- [ ] Generate compliance badges for README
  - [ ] Shields.io integration
  - [ ] Per-template compliance badges
  - [ ] Overall project health badge

### Template Enhancement Backlog
- [ ] Add mutation testing examples to templates
  - [ ] mutmut for Python
  - [ ] Stryker for JavaScript/TypeScript
  - [ ] go-mutesting for Go
- [ ] Enhance SBOM generation in all templates
  - [ ] CycloneDX integration improvements
  - [ ] SPDX format support
  - [ ] Vulnerability correlation
- [ ] Add performance testing frameworks
  - [ ] k6 for load testing
  - [ ] Locust for Python services
  - [ ] Apache JMeter alternatives
- [ ] Implement accessibility testing in web templates
  - [ ] axe-core integration
  - [ ] pa11y in CI/CD
  - [ ] WCAG 2.2 AA compliance checks
- [x] Add .pre-commit-config.yaml to remaining templates (HIGH PRIORITY) ✅ **COMPLETE**
  - [x] node-service
  - [x] react-webapp
  - [x] go-service
  - [x] docs-only
  - [x] Standardize pre-commit hooks across all templates

### Documentation Improvements
- [ ] Create video tutorials for templates (scripts ready)
  - [ ] Record Getting Started (8 min)
  - [ ] Record Creating Services (12 min)
  - [ ] Record CI/CD Setup (10 min)
  - [ ] Record Security Gates (15 min)
  - [ ] Record Observability Setup (12 min)
  - [ ] Record Jupyter Book Usage (8 min)
- [ ] Expand TEMPLATE_STANDARDS.md
  - [ ] Add more examples of acceptable variations
  - [ ] Document edge cases
  - [ ] Add troubleshooting section
- [ ] Create interactive compliance dashboard
  - [ ] Web-based compliance viewer
  - [ ] Real-time sanity check results
  - [ ] Historical trend visualization

### Automation Enhancements
- [ ] Automated template updates via Cruft
  - [ ] Monitor for template drift
  - [ ] Auto-generate update PRs
  - [ ] Test updates before applying
- [ ] Continuous compliance monitoring
  - [ ] Scheduled sanity check runs
  - [ ] Slack/Discord notifications
  - [ ] GitHub status checks
- [ ] Template generator CLI improvements
  - [ ] Interactive template selection wizard
  - [ ] Preview before generation
  - [ ] Undo/rollback capability

### Community & Ecosystem
- [ ] Template marketplace development
  - [ ] Web frontend for browsing
  - [ ] Rating and review system
  - [ ] Usage statistics
- [ ] Community template contribution framework
  - [ ] Submission guidelines enforcement
  - [ ] Automated quality checks
  - [ ] Review workflow
- [ ] Plugin system for sanity check
  - [ ] Custom validation rules
  - [ ] Language-specific validators
  - [ ] Organization-specific checks

---

**Last Updated**: 2025-10-12  
**Next Review**: 2026-01-12 (quarterly)  
**Maintainers**: See CODEOWNERS

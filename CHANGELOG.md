# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### New Features

- Comprehensive CONTRIBUTING.md with contribution guidelines
- SECURITY.md with security policy and vulnerability reporting process
- Fixed notebook test workflow pattern to correctly find notebooks
- React dashboard working example with Storybook, Playwright, and CI workflows (examples/projects/react-dashboard)
- Go gRPC user service working example with Buf-managed protobufs and integration tests (examples/projects/grpc-service)
- Python template end-to-end integration test (`tests/test_python_template_integration.py`) and slow test marker configuration (`pytest.ini`)
- Jupyter Book documentation build verification (`tests/test_docs_build.py`) and refreshed Pages workflow environment
- Node/React/Go template integration coverage (`tests/test_template_e2e.py`) with tooling-aware slow tests
- Weekly template E2E CI workflow (`.github/workflows/template-e2e.yml`) and documented sanity-check guidance
- Added `--skip-templates` option to `.dev/sanity-check.sh` for template-aware runs
- Backstage portal module + README under `templates/platform/backstage/` (Task #130)
- Intelligent `--fix` flag + `agentic-canon fix` command to remediate common setup issues automatically
- OpenFeature/flagd starter kit (`templates/_shared/feature_flags/`) with docs (`docs/feature-flags.md`) (Task #131)

### Updates

- Updated repository structure documentation
- Enhanced documentation organization

## [1.0.0] - 2025-10-11

### New in 1.0.0

- Initial repository structure with core directories (notebooks/, docs/, templates/, examples/)
- 5 executable Jupyter notebooks covering bootstrap, security, contracts, observability, and documentation
- Jupyter Book documentation with MyST markdown support
- Cookiecutter templates for Python, Node.js, React, Go, and docs-only projects
- GitHub Actions workflows for notebook testing, book deployment, and template validation
- Jupytext configuration for notebook version control
- Pre-commit hooks for code quality
- Binder configuration for reproducible environments
- Example configurations for Azure Pipelines
- DORA and SPACE/DevEx metrics dashboard templates
- Comprehensive documentation: README.md, BIBLE.md, INDEX.md, Agentic_Canon.md, INSTRUCTIONS.md
- Control traceability matrix for standards compliance
- Interactive CLI wizard (agentic_canon_cli/)
- Multiple runbook examples
- CODE_OF_CONDUCT.md and CODEOWNERS files
- LICENSE (Apache-2.0)

### Documentation

- Unified playbook (Agentic_Canon.md) with implementation guide
- Machine-readable documentation for AI agents
- Standards mapping (NIST SSDF, OWASP SAMM/ASVS, SLSA, OpenSSF Scorecard)
- Implementation task tracking (TASKS.md)
- Project completion summary (SUMMARY.md)

### Templates

- Python service template with FastAPI/Flask support
- Node.js service template with TypeScript
- React webapp template with Vite, Playwright, and Storybook
- Go service template with standard project layout
- Docs-only template for documentation projects

### Infrastructure

- CI/CD workflows for GitHub Actions
- Azure Pipelines examples
- Grafana dashboards for metrics
- OpenTelemetry configuration examples
- Security scanning workflows (planned)
- SBOM generation setup (planned)

[Unreleased]: https://github.com/IAmJonoBo/Agentic-Canon/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IAmJonoBo/Agentic-Canon/releases/tag/v1.0.0

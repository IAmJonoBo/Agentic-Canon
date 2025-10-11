# Examples

This directory contains example configurations, projects, and resources to demonstrate Agentic Canon's capabilities.

## Overview

The examples provided here serve as:
- Reference implementations
- Starting points for new projects
- Demonstrations of best practices
- Integration examples with various platforms

## Directory Structure

### azure-pipelines/
Azure Pipelines examples for CI/CD.

**Contents**:
- `python-service/` - Azure Pipelines for Python projects
- `node-service/` - Azure Pipelines for Node.js projects
- `README.md` - Azure Pipelines documentation

**Use Cases**:
- Organizations using Azure DevOps
- Multi-cloud CI/CD strategies
- Azure-specific integrations

### projects/
Example projects generated from templates.

**Contents**:
- `fastapi-microservice-README.md` - FastAPI microservice example

**Planned**:
- Complete Python FastAPI microservice
- Node.js API service with Express/NestJS
- React webapp (e-commerce or dashboard)
- Go gRPC service

### community/
Community-contributed examples and templates.

**Contents**:
- `CONTRIBUTING-TEMPLATES.md` - Guide for contributing templates

**Purpose**:
- Encourage community contributions
- Share domain-specific examples
- Showcase different use cases

### dashboards/
Monitoring and observability dashboards.

**Contents**:
- `dora-metrics.json` - DORA metrics Grafana dashboard
- `space-devex-metrics.json` - SPACE/DevEx metrics
- `quality-metrics.json` - Code quality metrics
- `security-metrics.json` - Security metrics
- `prometheus-alerts.yaml` - Prometheus alerting rules
- `otel-collector-config.yaml` - OpenTelemetry collector configuration
- `grafana/` - Additional Grafana dashboards
- `README.md` - Dashboard documentation

**Use Cases**:
- Implementing DORA metrics tracking
- Developer experience monitoring
- Security posture visualization
- Quality trends analysis

### fitness-functions/
Architecture fitness function examples.

**Contents**:
- `README.md` - Fitness functions documentation

**Planned**:
- Performance fitness functions
- Architecture compliance checks
- Security boundary validation
- Code quality thresholds

### ml-insights/
Machine learning-powered insights.

**Contents**:
- `README.md` - ML insights documentation

**Planned**:
- Anomaly detection examples
- Predictive failure analysis
- Test flakiness detection
- Code quality prediction

### multi-cloud/
Multi-cloud deployment examples.

**Contents**:
- `aws/` - AWS-specific examples
- `README.md` - Multi-cloud documentation

**Planned**:
- AWS deployment configurations
- Azure deployment examples
- GCP deployment examples
- Cloud-agnostic infrastructure code

### video-tutorials/
Video tutorial scripts and resources.

**Contents**:
- `01-getting-started.md` - Getting started script (5-7 min)
- `02-creating-services.md` - Service creation script (8-10 min)
- `03-cicd-setup.md` - CI/CD setup script (10-12 min)
- `04-security-gates.md` - Security gates script (12-15 min)
- `05-observability-setup.md` - Observability setup script (10-12 min)
- `06-jupyter-book.md` - Jupyter Book usage script (8-10 min)
- `README.md` - Tutorial series overview and production checklist

**Status**: ✅ All scripts complete (~65 minutes total)

**Planned**:
- Video recordings
- YouTube channel setup
- Video links in documentation

## Using Examples

### Quick Start

1. **Browse**: Explore directories to find relevant examples
2. **Copy**: Copy example configuration to your project
3. **Customize**: Adapt to your specific needs
4. **Test**: Validate changes work as expected

### Integration

Most examples can be integrated by:

```bash
# Copy configuration
cp examples/dashboards/dora-metrics.json your-project/

# Or reference directly
curl -O https://raw.githubusercontent.com/IAmJonoBo/Agentic-Canon/main/examples/dashboards/dora-metrics.json
```

### Adaptation

Examples are designed to be:
- **Minimal**: Focus on core functionality
- **Documented**: Clear comments and README files
- **Tested**: Verified to work
- **Customizable**: Easy to adapt

## Contributing Examples

We welcome example contributions! To submit an example:

1. Create example in appropriate subdirectory
2. Add comprehensive README
3. Test thoroughly
4. Document prerequisites and usage
5. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

### Example Contribution Checklist

- [ ] Example is complete and working
- [ ] README with clear usage instructions
- [ ] Prerequisites documented
- [ ] Configuration files included
- [ ] No sensitive data (secrets, credentials)
- [ ] Follows project conventions
- [ ] Linked from this README

## Example Categories

### By Use Case

- **CI/CD**: Azure Pipelines, GitHub Actions workflows
- **Observability**: Dashboards, metrics, traces
- **Security**: SAST configurations, security dashboards
- **Quality**: Quality metrics, fitness functions
- **Documentation**: Jupyter Book examples
- **Deployment**: Cloud deployment configurations

### By Technology

- **Python**: FastAPI, Flask, Django examples
- **Node.js**: Express, NestJS examples
- **React**: Component libraries, full applications
- **Go**: gRPC services, CLI tools
- **Infrastructure**: Terraform, Kubernetes

### By Cloud Provider

- **AWS**: Lambda, ECS, EKS configurations
- **Azure**: Functions, Container Apps, AKS
- **GCP**: Cloud Functions, Cloud Run, GKE
- **Multi-cloud**: Portable configurations

## Best Practices

When creating examples:

1. **Keep it Simple**: Focus on demonstrating one concept
2. **Document Thoroughly**: Explain what, why, and how
3. **Test Completely**: Ensure example works
4. **Stay Current**: Update with new versions
5. **Remove Secrets**: Never include credentials
6. **Show Patterns**: Demonstrate best practices

## Maintenance

Examples are reviewed:
- Quarterly for accuracy
- When dependencies update
- Based on community feedback
- For security vulnerabilities

## Support

For questions about examples:

1. Check example's README
2. Review related documentation
3. Search existing issues
4. Open a new discussion
5. Create an issue if needed

## References

- [Templates](../templates/) - Cookiecutter templates
- [Notebooks](../notebooks/) - Interactive guides
- [Documentation](../docs/) - Full documentation
- [TASKS.md](../TASKS.md) - Planned examples

## Status

Current examples: **24 files across 8 directories**  
**Recent Additions:**
- ✅ 6 complete video tutorial scripts (~65 min total)
- ✅ 4 Grafana dashboards (DORA, SPACE, Security, Quality)
- ✅ OpenTelemetry collector configuration
- ✅ Prometheus alerting rules
- ✅ Comprehensive fitness functions framework
- ✅ ML insights framework documentation
- ✅ Community contribution guidelines

Planned additions: See [TASKS.md](../TASKS.md) Version 1.1.0 and 2.0.0

---

For the latest examples and updates, visit the [repository](https://github.com/IAmJonoBo/Agentic-Canon).

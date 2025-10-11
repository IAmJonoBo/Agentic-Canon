# Azure Pipelines Configuration Examples

This directory contains Azure Pipelines YAML templates for the Agentic Canon framework.

## Available Templates

### 1. Python Service (`python-service-pipeline.yml`)
Complete CI/CD pipeline for Python services including:
- Multi-version testing (Python 3.11, 3.12)
- Code quality checks (black, ruff, mypy)
- Security scanning (CodeQL, secret scanning)
- SBOM generation
- Test execution with coverage
- Notebook execution

### 2. Node.js Service (`node-service-pipeline.yml`)
Coming soon

### 3. React WebApp (`react-webapp-pipeline.yml`)
Coming soon

### 4. Go Service (`go-service-pipeline.yml`)
Coming soon

## Usage

### Quick Start

1. Copy the appropriate pipeline file to your repository root as `azure-pipelines.yml`
2. Update the variables section with your project-specific values
3. Commit and push to your Azure DevOps repository
4. Create a new pipeline in Azure DevOps pointing to the YAML file

### Configuration

Each pipeline template includes configurable variables at the top:

```yaml
variables:
  python.version: '3.11'
  project.name: 'your-project'
  # ... more variables
```

Adjust these to match your project needs.

## Features

All pipeline templates include:

- ✅ **Multi-stage pipelines**: Build → Test → Security → Deploy
- ✅ **Parallel execution**: Speed up CI/CD with parallel jobs
- ✅ **Caching**: Dependencies cached for faster builds
- ✅ **Artifacts**: Build outputs published for deployment
- ✅ **Security scanning**: SAST, secret scanning, dependency checks
- ✅ **Quality gates**: Code coverage, linting, type checking
- ✅ **SBOM generation**: Software Bill of Materials
- ✅ **Deployment stages**: Automatic deployment to environments

## Azure DevOps Setup

### Prerequisites

1. **Azure DevOps organization and project**
2. **Service connections** for:
   - Azure Container Registry (if using containers)
   - Azure App Service or AKS (for deployment)
3. **Variable groups** for secrets:
   - CODECOV_TOKEN (optional, for coverage upload)
   - Deployment credentials

### Pipeline Setup

1. Navigate to Pipelines → New Pipeline
2. Select "Azure Repos Git" (or your source)
3. Choose your repository
4. Select "Existing Azure Pipelines YAML file"
5. Point to `azure-pipelines.yml`
6. Review and run

### Environment Configuration

For deployment stages, configure environments:

1. Go to Environments in Azure Pipelines
2. Create environments: `dev`, `staging`, `production`
3. Add approval gates for production
4. Configure environment-specific variables

## Differences from GitHub Actions

| Feature | GitHub Actions | Azure Pipelines |
|---------|---------------|-----------------|
| Job definition | `jobs:` | `jobs:` |
| Steps | `steps:` | `steps:` |
| Conditions | `if:` | `condition:` |
| Matrix builds | `strategy.matrix` | `strategy.matrix` |
| Artifacts | `actions/upload-artifact` | `PublishBuildArtifacts@1` |
| Cache | `actions/cache` | `Cache@2` |
| Script execution | `run:` | `script:` or `bash:` |

## Examples

See the individual YAML files for complete examples:

- `python-service-pipeline.yml`: Full Python CI/CD
- More coming soon...

## Best Practices

1. **Use templates**: Reuse common steps across pipelines
2. **Cache dependencies**: Speed up builds with dependency caching
3. **Parallel jobs**: Run independent jobs in parallel
4. **Staged rollouts**: Use deployment stages with approvals
5. **Secure secrets**: Use variable groups, never commit secrets
6. **Monitor pipelines**: Set up alerts for failures
7. **Version control**: Keep pipeline YAML in source control

## Resources

- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [YAML Schema Reference](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema)
- [Pipeline Tasks](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/)

## Contributing

To add a new pipeline template:

1. Create a new YAML file in this directory
2. Follow the structure of existing templates
3. Document all variables and customization points
4. Add usage examples
5. Update this README

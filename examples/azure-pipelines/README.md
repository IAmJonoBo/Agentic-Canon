# Azure Pipelines Examples

This directory contains Azure DevOps Pipeline configurations for various project types, following Agentic Canon standards.

## Available Templates

### Python Service
- **File**: `python-service/azure-pipelines.yml`
- **Features**:
  - Multi-version Python testing (3.11, 3.12)
  - Test coverage reporting
  - Security scanning (Safety, Bandit)
  - Code quality checks (Ruff, Black, mypy)

### Node.js Service
- **File**: `node-service/azure-pipelines.yml`
- **Features**:
  - Multi-version Node.js testing (18, 20, 21)
  - TypeScript type checking
  - ESLint and Prettier verification
  - npm security audit
  - Build artifact publishing

## Usage

1. Copy the appropriate `azure-pipelines.yml` to your project root
2. Customize variables as needed (e.g., Python version, Node version)
3. Push to Azure DevOps repository
4. Create a new pipeline pointing to the YAML file

## Common Configuration

All pipelines follow these standards:
- Trigger on `main` branch
- Run on pull requests
- Multi-stage pipelines (Build, Security, Quality)
- Artifact publishing
- Coverage reporting

## Integration with Agentic Canon

These pipelines align with the quality gates and security standards defined in the Agentic Canon playbook:
- Coverage thresholds ≥ 80%
- Security scanning (SAST, dependency checks)
- Code quality enforcement
- Artifact attestation ready

## Next Steps

- Configure branch policies in Azure DevOps
- Set up required reviewers
- Enable status checks for pull requests
- Configure deployment stages for production

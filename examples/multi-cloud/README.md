# Multi-Cloud Infrastructure Examples

This directory contains Infrastructure as Code (IaC) examples for deploying Agentic Canon projects across multiple cloud providers.

## Cloud Providers

- **AWS** - Amazon Web Services
- **Azure** - Microsoft Azure
- **GCP** - Google Cloud Platform

## Structure

```
multi-cloud/
├── aws/
│   ├── terraform/          # AWS Terraform modules
│   ├── cloudformation/     # AWS CloudFormation templates
│   └── README.md
├── azure/
│   ├── terraform/          # Azure Terraform modules
│   ├── bicep/             # Azure Bicep templates
│   └── README.md
├── gcp/
│   ├── terraform/          # GCP Terraform modules
│   └── README.md
└── README.md              # This file
```

## Quick Start

### AWS

```bash
cd aws/terraform
terraform init
terraform plan
terraform apply
```

### Azure

```bash
cd azure/terraform
terraform init
terraform plan
terraform apply
```

### GCP

```bash
cd gcp/terraform
terraform init
terraform plan
terraform apply
```

## Common Patterns

All cloud examples include:

1. **Compute Resources**
   - Container orchestration (ECS/AKS/GKE)
   - Serverless functions (Lambda/Functions/Cloud Functions)
   - VM instances

2. **Networking**
   - VPC/VNet configuration
   - Load balancers
   - DNS configuration
   - Security groups/NSGs

3. **Storage**
   - Object storage (S3/Blob/GCS)
   - Databases (RDS/Azure SQL/Cloud SQL)
   - Cache (ElastiCache/Redis Cache/Memorystore)

4. **Monitoring**
   - CloudWatch/Monitor/Cloud Monitoring
   - Log aggregation
   - Alerting

5. **Security**
   - IAM roles and policies
   - Secrets management
   - Encryption at rest and in transit

## Module Structure

Each Terraform module follows this structure:

```
module-name/
├── main.tf           # Main resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Provider versions
├── README.md         # Module documentation
└── examples/         # Usage examples
```

## Best Practices

1. **State Management**
   - Use remote state (S3/Azure Storage/GCS)
   - Enable state locking
   - Encrypt state files

2. **Security**
   - Never commit credentials
   - Use secrets manager
   - Enable encryption
   - Follow least privilege

3. **Cost Optimization**
   - Use autoscaling
   - Right-size resources
   - Use spot/preemptible instances
   - Set budget alerts

4. **Tagging**
   - Consistent tagging strategy
   - Include: Environment, Owner, Project, Cost Center

5. **Documentation**
   - Document module inputs/outputs
   - Include examples
   - Maintain change log

## Multi-Cloud Strategies

### 1. Cloud-Agnostic (Recommended for v2.0.0)

Use abstraction layers:
- Pulumi for multi-cloud IaC
- Kubernetes for container orchestration
- OpenTelemetry for observability
- Terraform with cloud-agnostic modules

### 2. Cloud-Native

Leverage cloud-specific services:
- Better performance
- More features
- Easier integration
- Vendor lock-in

### 3. Hybrid

Mix of both approaches:
- Critical paths: Cloud-agnostic
- Specialized workloads: Cloud-native

## GitOps Integration

All examples support GitOps workflows:

- ArgoCD for Kubernetes deployments
- Flux for continuous deployment
- Atlantis for Terraform automation

See `gitops/` directory for configurations.

## Cost Estimation

Use these tools before deployment:

```bash
# AWS
aws pricing get-products ...

# Terraform Cost Estimation
terraform plan -out=plan.out
infracost breakdown --path plan.out

# Azure
az consumption usage list

# GCP
gcloud billing budgets list
```

## Compliance

All examples include:

- Encryption at rest
- Encryption in transit
- Network isolation
- Audit logging
- Backup configuration
- Disaster recovery

## Support

- AWS: [aws/README.md](aws/README.md)
- Azure: [azure/README.md](azure/README.md)
- GCP: [gcp/README.md](gcp/README.md)

## Contributing

When adding new cloud examples:

1. Follow the module structure
2. Include comprehensive documentation
3. Add usage examples
4. Test thoroughly
5. Update this README

## Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- [Terraform Registry](https://registry.terraform.io/)
- [OpenTofu](https://opentofu.org/)

# AWS Infrastructure Examples

Infrastructure as Code for deploying Agentic Canon projects on AWS.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                ┌──────▼──────┐
                │   Route 53  │  DNS
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │     ALB     │  Application Load Balancer
                └──────┬──────┘
                       │
        ┏━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━┓
        ┃          VPC                 ┃
        ┃  ┌────────────────────────┐  ┃
        ┃  │  Public Subnets        │  ┃
        ┃  │  (NAT Gateway)         │  ┃
        ┃  └────────────────────────┘  ┃
        ┃  ┌────────────────────────┐  ┃
        ┃  │  Private Subnets       │  ┃
        ┃  │  ┌──────────────────┐  │  ┃
        ┃  │  │   ECS Fargate    │  │  ┃
        ┃  │  │   (Containers)   │  │  ┃
        ┃  │  └──────────────────┘  │  ┃
        ┃  │  ┌──────────────────┐  │  ┃
        ┃  │  │   RDS Postgres   │  │  ┃
        ┃  │  └──────────────────┘  │  ┃
        ┃  │  ┌──────────────────┐  │  ┃
        ┃  │  │ ElastiCache Redis│  │  ┃
        ┃  │  └──────────────────┘  │  ┃
        ┃  └────────────────────────┘  ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │   S3    │   │ Secrets │   │CloudWatch│
   │ Bucket  │   │ Manager │   │   Logs   │
   └─────────┘   └─────────┘   └──────────┘
```

## Modules

### 1. VPC (`terraform/vpc/`)

Creates a multi-AZ VPC with public and private subnets.

**Resources:**

- VPC
- Internet Gateway
- NAT Gateways (one per AZ)
- Public/Private Subnets
- Route Tables
- Security Groups

**Usage:**

```hcl
module "vpc" {
  source = "./terraform/vpc"

  name               = "agentic-canon-vpc"
  cidr               = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  tags = {
    Environment = "production"
    Project     = "agentic-canon"
  }
}
```

### 2. ECS Fargate (`terraform/ecs-fargate/`)

Deploys containerized applications on ECS Fargate.

**Resources:**

- ECS Cluster
- Task Definition
- ECS Service
- Application Load Balancer
- Target Groups
- CloudWatch Log Groups
- IAM Roles

**Usage:**

```hcl
module "ecs_service" {
  source = "./terraform/ecs-fargate"

  name           = "my-api-service"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids
  container_image = "myorg/my-api:latest"
  container_port = 8000

  cpu    = 256
  memory = 512

  desired_count = 2

  environment_variables = {
    DATABASE_URL = "postgresql://..."
    LOG_LEVEL    = "info"
  }

  secrets = {
    SECRET_KEY = "arn:aws:secretsmanager:..."
  }
}
```

### 3. RDS Postgres (`terraform/rds/`)

Managed PostgreSQL database with multi-AZ deployment.

**Resources:**

- RDS Instance
- DB Subnet Group
- Security Groups
- Parameter Group
- Automated Backups

**Usage:**

```hcl
module "database" {
  source = "./terraform/rds"

  name               = "myapp-db"
  engine_version     = "15.3"
  instance_class     = "db.t3.medium"
  allocated_storage  = 100

  vpc_id            = module.vpc.vpc_id
  subnet_ids        = module.vpc.private_subnet_ids

  multi_az          = true
  backup_retention_period = 7

  username = "dbadmin"
  # Password stored in Secrets Manager
}
```

### 4. Lambda Functions (`terraform/lambda/`)

Serverless functions for event-driven workloads.

**Resources:**

- Lambda Function
- IAM Roles
- CloudWatch Logs
- API Gateway (optional)

**Usage:**

```hcl
module "lambda" {
  source = "./terraform/lambda"

  function_name = "data-processor"
  handler       = "index.handler"
  runtime       = "python3.11"

  source_dir = "../src/lambda"

  environment_variables = {
    BUCKET_NAME = module.s3.bucket_name
  }

  memory_size = 256
  timeout     = 30
}
```

### 5. S3 Storage (`terraform/s3/`)

Object storage for static assets and data.

**Resources:**

- S3 Bucket
- Bucket Policies
- Lifecycle Rules
- Versioning
- Encryption

**Usage:**

```hcl
module "s3" {
  source = "./terraform/s3"

  bucket_name = "myapp-assets"

  versioning_enabled = true
  encryption_enabled = true

  lifecycle_rules = [
    {
      id      = "archive-old-logs"
      enabled = true

      transition = {
        days          = 90
        storage_class = "GLACIER"
      }
    }
  ]
}
```

### 6. Monitoring (`terraform/monitoring/`)

CloudWatch dashboards, alarms, and log aggregation.

**Resources:**

- CloudWatch Dashboards
- CloudWatch Alarms
- SNS Topics
- Log Groups

**Usage:**

```hcl
module "monitoring" {
  source = "./terraform/monitoring"

  service_name = "my-api"

  alarms = {
    high_cpu = {
      metric_name         = "CPUUtilization"
      comparison_operator = "GreaterThanThreshold"
      threshold           = 80
      evaluation_periods  = 2
    }

    high_error_rate = {
      metric_name         = "5XXError"
      comparison_operator = "GreaterThanThreshold"
      threshold           = 10
      evaluation_periods  = 1
    }
  }

  notification_email = "ops@example.com"
}
```

## Complete Example

See `terraform/examples/complete/` for a full stack deployment:

```bash
cd terraform/examples/complete
terraform init
terraform plan
terraform apply
```

This creates:

- Multi-AZ VPC
- ECS Fargate cluster with API service
- RDS PostgreSQL database
- ElastiCache Redis
- S3 buckets
- CloudWatch monitoring
- Route 53 DNS

## Prerequisites

1. **AWS CLI**

   ```bash
   aws configure
   ```

2. **Terraform** (>= 1.5.0)

   ```bash
   terraform version
   ```

3. **IAM Permissions**
   - VPC management
   - ECS/Fargate
   - RDS
   - S3
   - IAM role creation
   - CloudWatch

## Best Practices

### Security

1. **Secrets Management**

   ```hcl
   # Use AWS Secrets Manager
   data "aws_secretsmanager_secret_version" "db_password" {
     secret_id = "prod/db/password"
   }
   ```

2. **Encryption**
   - Enable encryption at rest for RDS, S3, EBS
   - Use KMS for key management
   - TLS for data in transit

3. **Network Security**
   - Private subnets for application/data layers
   - Security groups with minimal access
   - VPC Flow Logs enabled

### Cost Optimization

1. **Right-Sizing**
   - Use cost explorer
   - Monitor CloudWatch metrics
   - Adjust instance sizes

2. **Reserved Instances**
   - For predictable workloads
   - 1-year or 3-year commitments

3. **Spot Instances**
   - For fault-tolerant workloads
   - ECS/Fargate Spot

4. **S3 Lifecycle Policies**
   - Transition to cheaper storage classes
   - Expire old objects

### High Availability

1. **Multi-AZ Deployment**
   - All services across 3 AZs
   - RDS Multi-AZ
   - ECS tasks distributed

2. **Auto Scaling**

   ```hcl
   resource "aws_appautoscaling_target" "ecs" {
     min_capacity = 2
     max_capacity = 10
   }
   ```

3. **Health Checks**
   - ALB health checks
   - ECS health checks
   - CloudWatch alarms

## Deployment

### Development

```bash
terraform workspace new dev
terraform apply -var-file=dev.tfvars
```

### Staging

```bash
terraform workspace new staging
terraform apply -var-file=staging.tfvars
```

### Production

```bash
terraform workspace new prod
terraform apply -var-file=prod.tfvars
```

## Monitoring

### Key Metrics

- ECS CPU/Memory utilization
- ALB request count and latency
- RDS CPU/Storage/Connections
- Lambda invocations and errors

### Dashboards

Import pre-built dashboards:

```bash
aws cloudwatch put-dashboard \
  --dashboard-name my-app \
  --dashboard-body file://dashboards/main.json
```

### Alarms

Critical alarms notify via SNS:

- Service unavailable
- High error rate
- Database connection failures
- Disk space critical

## Disaster Recovery

### Backups

- RDS automated backups (7-35 days)
- S3 versioning enabled
- Cross-region replication for critical data

### Recovery Procedures

1. **Database Restore**

   ```bash
   aws rds restore-db-instance-from-db-snapshot \
     --db-instance-identifier new-instance \
     --db-snapshot-identifier snapshot-id
   ```

2. **Infrastructure Rebuild**
   ```bash
   terraform apply -refresh-only
   terraform apply
   ```

## Cost Estimation

Monthly costs (estimated):

| Service           | Configuration              | Cost            |
| ----------------- | -------------------------- | --------------- |
| ECS Fargate       | 2 tasks, 0.25 vCPU, 0.5 GB | $15             |
| RDS PostgreSQL    | db.t3.medium, Multi-AZ     | $150            |
| ElastiCache Redis | cache.t3.micro             | $25             |
| NAT Gateway       | 3 AZs                      | $100            |
| ALB               | 1 load balancer            | $25             |
| S3                | 100 GB                     | $2              |
| CloudWatch Logs   | 10 GB                      | $5              |
| **Total**         |                            | **~$322/month** |

Use `infracost` for accurate estimates:

```bash
infracost breakdown --path .
```

## Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/)

## Support

- AWS Support: [AWS Console](https://console.aws.amazon.com/support/)
- Terraform: [Terraform Registry](https://registry.terraform.io/)
- Issues: [GitHub Issues](https://github.com/IAmJonoBo/Agentic-Canon/issues)

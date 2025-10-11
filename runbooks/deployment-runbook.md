# Runbook: Deployment

## Purpose

This runbook provides step-by-step instructions for deploying projects generated from Agentic Canon templates. It covers local development, staging, and production deployments across different platforms.

## Prerequisites

- Generated project from Agentic Canon template
- Git repository with code pushed
- Access to deployment platform (GitHub, cloud provider, etc.)
- Required credentials and secrets configured
- CI/CD pipeline configured

## Deployment Strategies

This runbook covers multiple deployment strategies:
1. **Static Documentation** - Jupyter Book to GitHub Pages
2. **Container Deployment** - Docker to cloud platforms
3. **Serverless Functions** - AWS Lambda, Azure Functions, Google Cloud Functions
4. **Platform as a Service** - Heroku, Render, Railway
5. **Kubernetes** - K8s clusters (EKS, AKS, GKE)

## Strategy 1: Static Documentation (Jupyter Book)

### Purpose
Deploy Jupyter Book documentation to GitHub Pages

### Duration
15-30 minutes (initial setup)

### Steps

#### 1. Enable GitHub Pages

**Actions**:
1. Navigate to repository on GitHub
2. Go to Settings → Pages
3. Select Source: "GitHub Actions"
4. Save configuration

**Commands**:
```bash
# Or via GitHub CLI
gh repo edit --enable-pages --pages-branch gh-pages
```

**Validation**: Pages settings show "GitHub Actions" as source

#### 2. Verify Workflow File

**Check** `.github/workflows/book-deploy.yml`:

```yaml
name: Deploy Jupyter Book
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Build book
        run: jupyter-book build docs/
      
      - name: Deploy to GitHub Pages
        run: ghp-import -n -p -f docs/_build/html
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Validation**: Workflow file exists and is valid

#### 3. Build Locally (Optional)

**Commands**:
```bash
# Install dependencies
pip install -r requirements.txt

# Build book
jupyter-book build docs/

# Preview locally
open docs/_build/html/index.html
```

**Validation**: Book builds without errors, preview looks correct

#### 4. Trigger Deployment

**Commands**:
```bash
# Commit and push changes
git add .
git commit -m "docs: update documentation"
git push origin main

# Or manually trigger
gh workflow run book-deploy.yml
```

**Validation**: Workflow runs successfully in GitHub Actions

#### 5. Verify Deployment

**Actions**:
1. Wait for workflow to complete (~2-3 minutes)
2. Visit `https://[username].github.io/[repo-name]/`
3. Verify documentation is accessible and correct

**Commands**:
```bash
# Check deployment status
gh run list --workflow=book-deploy.yml --limit 1

# View workflow logs if needed
gh run view [run-id] --log
```

**Validation**: Documentation site is live and accessible

### Troubleshooting

**Issue**: 404 error on GitHub Pages
**Solution**: Check that `gh-pages` branch exists and is deployed

**Issue**: Workflow fails with permissions error
**Solution**: Ensure workflow has `contents: write` permission

**Issue**: Book build fails
**Solution**: Run `jupyter-book build docs/` locally to debug

## Strategy 2: Container Deployment

### Purpose
Deploy containerized application to cloud platforms

### Duration
30-60 minutes (initial setup)

### Steps

#### 1. Create Dockerfile (if not exists)

**Python Example**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Node.js Example**:
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

**Validation**: Dockerfile follows best practices

#### 2. Build and Test Locally

**Commands**:
```bash
# Build image
docker build -t my-app:latest .

# Run container
docker run -p 8000:8000 my-app:latest

# Test endpoint
curl http://localhost:8000/health
```

**Validation**: Container runs and responds correctly

#### 3. Set Up Container Registry

**GitHub Container Registry**:
```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag image
docker tag my-app:latest ghcr.io/USERNAME/my-app:latest

# Push
docker push ghcr.io/USERNAME/my-app:latest
```

**Docker Hub**:
```bash
# Login
docker login

# Tag and push
docker tag my-app:latest username/my-app:latest
docker push username/my-app:latest
```

**Validation**: Image pushed successfully to registry

#### 4. Deploy to Cloud Platform

**AWS ECS/Fargate**:
```bash
# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-app \
  --task-definition my-app:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

**Azure Container Instances**:
```bash
# Deploy container
az container create \
  --resource-group myResourceGroup \
  --name my-app \
  --image ghcr.io/username/my-app:latest \
  --dns-name-label my-app-unique \
  --ports 8000
```

**Google Cloud Run**:
```bash
# Deploy
gcloud run deploy my-app \
  --image gcr.io/project-id/my-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Validation**: Service is running and accessible

#### 5. Configure CI/CD for Automatic Deployment

**GitHub Actions Example**:
```yaml
name: Deploy Container
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
      
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy my-app \
            --image ghcr.io/${{ github.repository }}:latest \
            --region us-central1
```

**Validation**: Deployments trigger automatically on push

## Strategy 3: Serverless Functions

### Purpose
Deploy serverless functions to cloud providers

### Duration
20-40 minutes

### AWS Lambda

#### 1. Package Function

**Python**:
```bash
# Install dependencies
pip install -r requirements.txt -t package/

# Package function
cd package
zip -r ../function.zip .
cd ..
zip -g function.zip lambda_function.py
```

**Node.js**:
```bash
# Install dependencies
npm ci --production

# Package
zip -r function.zip node_modules/ index.js
```

#### 2. Deploy Function

**Commands**:
```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/lambda-role \
  --handler lambda_function.handler \
  --zip-file fileb://function.zip

# Update function (subsequent deploys)
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip
```

**Validation**: Function created and invocable

#### 3. Configure API Gateway

**Commands**:
```bash
# Create REST API
aws apigateway create-rest-api --name my-api

# Create resource and method
# Configure integration with Lambda
# Deploy API stage
```

**Validation**: API accessible via URL

### Azure Functions

**Commands**:
```bash
# Initialize function app
func init my-function-app --python

# Create function
cd my-function-app
func new --name HttpTrigger --template "HTTP trigger"

# Deploy
func azure functionapp publish my-function-app
```

**Validation**: Function accessible via Azure URL

### Google Cloud Functions

**Commands**:
```bash
# Deploy function
gcloud functions deploy my-function \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point main \
  --source .
```

**Validation**: Function accessible via Google Cloud URL

## Strategy 4: Platform as a Service (PaaS)

### Purpose
Deploy to managed PaaS platforms

### Duration
15-30 minutes

### Heroku

**Commands**:
```bash
# Login
heroku login

# Create app
heroku create my-app

# Add buildpack (if needed)
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Scale
heroku ps:scale web=1

# Open app
heroku open
```

**Validation**: App running on Heroku

### Render

**Actions**:
1. Connect GitHub repository
2. Select branch and build command
3. Configure environment variables
4. Deploy

**Validation**: App running on Render

### Railway

**Commands**:
```bash
# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open app
railway open
```

**Validation**: App running on Railway

## Strategy 5: Kubernetes Deployment

### Purpose
Deploy to Kubernetes clusters

### Duration
1-2 hours (initial setup)

### Steps

#### 1. Create Kubernetes Manifests

**Deployment**:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: ghcr.io/username/my-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV
          value: production
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
```

**Service**:
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Ingress**:
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - my-app.example.com
    secretName: my-app-tls
  rules:
  - host: my-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
```

#### 2. Apply Manifests

**Commands**:
```bash
# Create namespace
kubectl create namespace my-app

# Apply manifests
kubectl apply -f deployment.yaml -n my-app
kubectl apply -f service.yaml -n my-app
kubectl apply -f ingress.yaml -n my-app

# Verify deployment
kubectl get pods -n my-app
kubectl get svc -n my-app
kubectl get ingress -n my-app
```

**Validation**: Pods running, service accessible

#### 3. Set Up GitOps (ArgoCD)

**Commands**:
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Create application
argocd app create my-app \
  --repo https://github.com/username/my-app \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace my-app \
  --sync-policy automated
```

**Validation**: ArgoCD syncing application automatically

## Post-Deployment

### Steps Common to All Strategies

#### 1. Verify Health Checks

**Commands**:
```bash
# HTTP health check
curl https://my-app.example.com/health

# Detailed status
curl https://my-app.example.com/status
```

**Expected Response**: 200 OK with healthy status

#### 2. Check Logs

**GitHub Pages**: Check GitHub Actions logs
**Containers**: Check cloud platform logs
**Kubernetes**:
```bash
kubectl logs -f deployment/my-app -n my-app
```

#### 3. Monitor Metrics

- Check deployment metrics in cloud dashboard
- Verify OpenTelemetry metrics flowing
- Check Grafana dashboards
- Review error rates and latency

#### 4. Configure Alerts

- Set up uptime monitoring (Pingdom, UptimeRobot)
- Configure error alerting
- Set up log monitoring
- Enable security alerts

#### 5. Document Deployment

Update documentation:
- Deployment URLs
- Access credentials (secure storage)
- Rollback procedures
- Incident contacts

## Rollback Procedures

### GitHub Pages
```bash
# Revert commit
git revert HEAD
git push origin main
```

### Container Deployment
```bash
# Roll back to previous version
docker pull ghcr.io/username/my-app:previous-tag
# Redeploy with previous tag
```

### Kubernetes
```bash
# Roll back deployment
kubectl rollout undo deployment/my-app -n my-app

# Roll back to specific revision
kubectl rollout undo deployment/my-app --to-revision=2 -n my-app
```

### Serverless
```bash
# AWS Lambda
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://previous-function.zip
```

## Troubleshooting

### Deployment Fails

**Check**:
- Build logs for errors
- Configuration and environment variables
- Network connectivity
- Resource quotas and limits
- Permissions and credentials

### Application Not Accessible

**Check**:
- DNS configuration
- Firewall rules
- Load balancer configuration
- Health check passing
- SSL certificates

### Performance Issues

**Check**:
- Resource utilization (CPU, memory)
- Database connection pool
- External service latency
- Caching configuration
- Query optimization

## Validation Checklist

- [ ] Application deployed successfully
- [ ] Health checks passing
- [ ] Logs accessible and monitored
- [ ] Metrics flowing to observability platform
- [ ] Alerts configured
- [ ] Documentation updated
- [ ] Rollback procedure tested
- [ ] Security scans passing
- [ ] Performance acceptable
- [ ] Team notified of deployment

## References

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)

---

*For deployment issues, consult platform-specific documentation or open a GitHub issue.*

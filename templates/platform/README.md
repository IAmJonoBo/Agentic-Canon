# Platform Templates

Internal Developer Platform (IDP) templates for service catalogs, GitOps, and policy-as-code.

## Purpose

These templates enable platform engineering teams to build golden paths, enforce standards, and provide self-service capabilities for development teams.

## Contents

### 🎭 Backstage Templates (`backstage/`)

Backstage Software Templates for standardized service creation.

**File:** [`service-template.yaml`](backstage/service-template.yaml)

**Features:**
- Self-service service creation
- Golden path enforcement
- Compliance by default
- Multi-language support (JavaScript, TypeScript, Python, Go, Java, C#)
- Framework selection (Express, NestJS, Django, Flask, Gin, Spring Boot, .NET)
- Database integration (PostgreSQL, MySQL, MongoDB, Redis)
- Service tier classification (tier-0, tier-1, tier-2)
- Automated repository setup
- CI/CD pipeline generation
- Security scanning enabled
- SBOM generation
- SLO definitions

**Service Tiers:**
- **Tier-0**: Business-critical services (99.99% SLO, 24/7 on-call)
- **Tier-1**: Important services (99.9% SLO, business hours support)
- **Tier-2**: Standard services (99.5% SLO, best effort support)

**Usage:**
```bash
# Add to Backstage catalog
# Place in your Backstage app repository

# File: backstage/templates/service-template.yaml
cp templates/platform/backstage/service-template.yaml \
   backstage-app/templates/

# Register in catalog
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: templates
spec:
  type: file
  targets:
    - ./templates/**/*.yaml
```

**Template Parameters:**

1. **Service Information**
   - Name (kebab-case)
   - Description
   - Owner (team)

2. **Technical Stack**
   - Programming language
   - Framework
   - Database

3. **Compliance & Standards**
   - Service tier
   - Compliance requirements
   - Security gates

4. **Repository Settings**
   - GitHub organization
   - Repository visibility
   - Default branch

**Generated Components:**
- Git repository with branch protection
- README with standards badge
- CI/CD pipeline (GitHub Actions or GitLab CI)
- Security scanning workflows
- Dependency management (Renovate)
- SLO definitions
- OpenTelemetry instrumentation
- Backstage catalog registration

### 🔐 Policy-as-Code (`policy/`)

OPA (Open Policy Agent) policies for Kubernetes admission control.

**File:** [`opa-k8s-policy.rego`](policy/opa-k8s-policy.rego)

**Policies Enforced:**

1. **Security Policies**
   - Deny containers running as root
   - Require resource limits (CPU, memory)
   - Deny privileged containers
   - Deny host network/PID/IPC access
   - Require image signatures (Cosign/Sigstore)

2. **Compliance Policies**
   - Require security labels (app, team, tier)
   - Enforce naming conventions
   - Require namespace quotas
   - Validate pod security standards

3. **Resource Policies**
   - CPU and memory limits
   - Storage quotas
   - Network policies required
   - Pod disruption budgets for critical services

**Usage:**

**Install OPA Gatekeeper:**
```bash
# Install Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Verify installation
kubectl get pods -n gatekeeper-system
```

**Deploy Policy:**
```bash
# Create constraint template
kubectl apply -f opa-k8s-constraint-template.yaml

# Create constraint
kubectl apply -f opa-k8s-constraint.yaml

# Test policy
kubectl apply -f test-pod.yaml
# Should fail if violates policy
```

**Example Constraint:**
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sPolicyCheck
metadata:
  name: require-non-root
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    message: "Containers must not run as root"
```

**Policy Testing:**
```bash
# Test policy locally
opa test opa-k8s-policy.rego

# Validate against Kubernetes manifest
opa eval -d opa-k8s-policy.rego \
  -i pod-manifest.yaml \
  data.kubernetes.admission.deny_root_containers
```

### 📂 GitOps (Planned)

GitOps configurations for ArgoCD and Flux (planned).

**Status:** Templates planned for future release

**Planned Features:**
- ArgoCD application templates
- Flux Kustomization templates
- Multi-environment configurations
- Progressive delivery patterns
- Rollback strategies

## Quick Start

### Backstage Software Template Setup

```bash
# 1. Install Backstage (if not already)
npx @backstage/create-app

# 2. Copy template to Backstage app
cp templates/platform/backstage/service-template.yaml \
   backstage-app/templates/frontier-service.yaml

# 3. Register template in catalog
# Edit backstage-app/catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: templates
spec:
  type: file
  targets:
    - ./templates/**/*.yaml

# 4. Start Backstage
cd backstage-app
yarn dev

# 5. Access Backstage UI
# Navigate to: http://localhost:3000
# Click "Create" → "Frontier Excellence Service"
```

### OPA Policy Deployment

```bash
# 1. Install OPA Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# 2. Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  -l control-plane=controller-manager \
  -n gatekeeper-system \
  --timeout=120s

# 3. Create constraint template
cat <<EOF | kubectl apply -f -
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8ssecuritypolicy
spec:
  crd:
    spec:
      names:
        kind: K8sSecurityPolicy
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
$(cat templates/platform/policy/opa-k8s-policy.rego | sed 's/^/        /')
EOF

# 4. Create constraints
cat <<EOF | kubectl apply -f -
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sSecurityPolicy
metadata:
  name: security-policy
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
EOF

# 5. Test policy
kubectl apply -f test-manifests/
```

## Best Practices

### Backstage Software Templates

1. **Golden paths** - Provide opinionated, best-practice templates
2. **Progressive disclosure** - Start simple, add complexity as needed
3. **Self-service** - Enable teams to create services without tickets
4. **Compliance by default** - Security and standards baked in
5. **Template versioning** - Version templates for consistency
6. **Documentation** - Include README and runbooks
7. **Automated testing** - Test generated projects in CI
8. **Feedback loops** - Collect usage metrics and iterate

### Policy-as-Code

1. **Fail safe** - Deny by default, allow explicitly
2. **Clear messages** - Provide actionable error messages
3. **Test policies** - Unit test all policies
4. **Version control** - Treat policies as code
5. **Audit mode first** - Deploy in audit mode, then enforce
6. **Performance** - Optimize policy evaluation
7. **Documentation** - Document why each policy exists
8. **Exceptions** - Support exceptions with approval

### Platform Engineering

1. **Developer experience** - Make it easy to do the right thing
2. **Self-service** - Reduce dependencies on platform team
3. **Standards** - Consistent across all services
4. **Automation** - Automate repetitive tasks
5. **Observability** - Monitor platform health
6. **Feedback** - Continuous improvement based on user feedback
7. **Documentation** - Comprehensive platform documentation

## Integration Examples

### Backstage + GitHub Actions

```yaml
# Template step in service-template.yaml
steps:
  - id: fetch
    name: Fetch Base Template
    action: fetch:template
    input:
      url: ./skeleton
      values:
        name: ${{ parameters.name }}
        owner: ${{ parameters.owner }}

  - id: publish
    name: Publish to GitHub
    action: publish:github
    input:
      allowedHosts: ['github.com']
      description: ${{ parameters.description }}
      repoUrl: ${{ parameters.repoUrl }}
      repoVisibility: ${{ parameters.repoVisibility }}

  - id: register
    name: Register Component
    action: catalog:register
    input:
      repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
      catalogInfoPath: '/catalog-info.yaml'
```

### OPA + Kubernetes

```yaml
# Admission webhook configuration
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: gatekeeper-validating-webhook-configuration
webhooks:
- name: validation.gatekeeper.sh
  rules:
  - operations: ["CREATE", "UPDATE"]
    apiGroups: ["*"]
    apiVersions: ["*"]
    resources: ["*"]
  clientConfig:
    service:
      name: gatekeeper-webhook-service
      namespace: gatekeeper-system
      path: "/v1/admit"
```

### Progressive Delivery

```yaml
# ArgoCD Application with Rollouts
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-service
spec:
  project: default
  source:
    repoURL: https://github.com/org/my-service
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Tools and Integrations

### Platform Tools
- **Backstage** - Developer portal and service catalog
- **Port** - Internal developer portal
- **Clutch** - Extensibility platform
- **Kratix** - Platform as a Product framework

### Policy Tools
- **OPA** - Open Policy Agent
- **Kyverno** - Kubernetes native policy engine
- **Admission Controllers** - Kubernetes admission control
- **Policy Reporter** - Policy violation reporting

### GitOps Tools
- **ArgoCD** - Declarative GitOps
- **Flux** - Progressive delivery
- **Helm** - Package management
- **Kustomize** - Template-free customization

## Monitoring Platform Health

### Key Metrics

**Developer Experience:**
- Time to first commit
- Service creation success rate
- Developer satisfaction (DORA)
- Support ticket volume

**Platform Reliability:**
- Platform uptime
- Policy enforcement rate
- GitOps sync success rate
- Template generation failures

**Security & Compliance:**
- Policy violation rate
- Non-compliant services
- Security scan coverage
- Vulnerability remediation time

## Standards Compliance

These templates help achieve compliance with:

- ✅ **NIST SSDF v1.1** - Secure Software Development Framework
- ✅ **ISO/IEC 25010** - Software quality characteristics
- ✅ **CIS Kubernetes Benchmark** - Kubernetes security
- ✅ **Pod Security Standards** - Kubernetes pod security
- ✅ **SLSA Level 3** - Supply chain security

## Additional Resources

### Backstage
- [Backstage Docs](https://backstage.io/docs/)
- [Software Templates](https://backstage.io/docs/features/software-templates/)
- [Scaffolder Actions](https://backstage.io/docs/features/software-templates/builtin-actions)

### OPA
- [OPA Documentation](https://www.openpolicyagent.org/docs/)
- [Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [Policy Library](https://github.com/open-policy-agent/gatekeeper-library)

### Platform Engineering
- [Team Topologies](https://teamtopologies.com/)
- [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/)

### Related Templates
- [CI/CD Templates](../cicd/README.md) - Pipeline templates
- [Security Templates](../security/README.md) - Security scanning
- [Observability Templates](../observability/README.md) - Monitoring setup

## Contributing

To improve these templates:
1. Share your platform configurations
2. Add service catalog examples
3. Contribute policy patterns
4. Document platform patterns
5. Submit PRs with improvements

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

# OPA Policy - Kubernetes Admission Control
# Implements: Policy-as-code, security gates, compliance enforcement
# Standards: NIST SSDF, ISO/IEC 25010

package kubernetes.admission

import data.kubernetes.namespaces
import future.keywords.if
import future.keywords.in

# Deny containers running as root
deny_root_containers contains msg if {
    some container in input.request.object.spec.containers
    container.securityContext.runAsNonRoot == false
    msg := sprintf("Container '%s' must not run as root", [container.name])
}

deny_root_containers contains msg if {
    some container in input.request.object.spec.containers
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container '%s' must explicitly set runAsNonRoot: true", [container.name])
}

# Require resource limits
deny_no_limits contains msg if {
    some container in input.request.object.spec.containers
    not container.resources.limits
    msg := sprintf("Container '%s' must have resource limits", [container.name])
}

deny_no_limits contains msg if {
    some container in input.request.object.spec.containers
    not container.resources.limits.cpu
    msg := sprintf("Container '%s' must have CPU limits", [container.name])
}

deny_no_limits contains msg if {
    some container in input.request.object.spec.containers
    not container.resources.limits.memory
    msg := sprintf("Container '%s' must have memory limits", [container.name])
}

# Require image signatures
deny_unsigned_images contains msg if {
    some container in input.request.object.spec.containers
    not has_signature(container.image)
    msg := sprintf("Container image '%s' must be signed", [container.image])
}

has_signature(image) if {
    # Check if image has a signature annotation
    input.request.object.metadata.annotations["cosign.sigstore.dev/signature"]
}

# Deny privileged containers
deny_privileged contains msg if {
    some container in input.request.object.spec.containers
    container.securityContext.privileged == true
    msg := sprintf("Container '%s' cannot run in privileged mode", [container.name])
}

# Deny host network/PID/IPC
deny_host_access contains msg if {
    input.request.object.spec.hostNetwork == true
    msg := "Pods cannot use host network"
}

deny_host_access contains msg if {
    input.request.object.spec.hostPID == true
    msg := "Pods cannot use host PID namespace"
}

deny_host_access contains msg if {
    input.request.object.spec.hostIPC == true
    msg := "Pods cannot use host IPC namespace"
}

# Require security labels
deny_missing_labels contains msg if {
    required_labels := {"app", "team", "tier"}
    some label in required_labels
    not input.request.object.metadata.labels[label]
    msg := sprintf("Missing required label: %s", [label])
}

# Enforce namespace restrictions
deny_namespace_violation contains msg if {
    input.request.namespace in {"kube-system", "kube-public"}
    input.request.userInfo.username != "system:serviceaccount:kube-system:admin"
    msg := "Cannot deploy to system namespaces"
}

# Require specific image registries
deny_untrusted_registry contains msg if {
    some container in input.request.object.spec.containers
    not startswith(container.image, "registry.example.com/")
    not startswith(container.image, "gcr.io/")
    msg := sprintf("Container image '%s' must come from approved registry", [container.image])
}

# Require read-only root filesystem
deny_writable_root contains msg if {
    some container in input.request.object.spec.containers
    not container.securityContext.readOnlyRootFilesystem
    msg := sprintf("Container '%s' must use read-only root filesystem", [container.name])
}

# Aggregate all denials
violation[{"msg": msg, "details": {}}] {
    msg := deny_root_containers[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_no_limits[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_unsigned_images[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_privileged[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_host_access[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_missing_labels[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_namespace_violation[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_untrusted_registry[_]
}

violation[{"msg": msg, "details": {}}] {
    msg := deny_writable_root[_]
}

---
# Gatekeeper ConstraintTemplate
# File: pod-security-template.yaml

apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8spodsecuritypolicy
spec:
  crd:
    spec:
      names:
        kind: K8sPodSecurityPolicy
      validation:
        openAPIV3Schema:
          type: object
          properties:
            requireNonRoot:
              type: boolean
            requireSignatures:
              type: boolean
            allowedRegistries:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8spodsecurity
        
        # Import OPA policy above
        import data.kubernetes.admission
        
        violation[{"msg": msg}] {
          msg := admission.violation[_].msg
        }

---
# Constraint Instance
# File: enforce-pod-security.yaml

apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sPodSecurityPolicy
metadata:
  name: enforce-pod-security
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces:
      - "production"
      - "staging"
  parameters:
    requireNonRoot: true
    requireSignatures: true
    allowedRegistries:
      - "registry.example.com"
      - "gcr.io"

---
# Validation Commands
#
# Test OPA policy:
#   opa test policy.rego policy_test.rego -v
#
# Evaluate policy:
#   opa eval -i input.json -d policy.rego "data.kubernetes.admission.violation"
#
# Install Gatekeeper:
#   kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml
#
# Apply ConstraintTemplate:
#   kubectl apply -f pod-security-template.yaml
#
# Apply Constraint:
#   kubectl apply -f enforce-pod-security.yaml
#
# Test constraint:
#   kubectl apply -f test-pod.yaml --dry-run=server

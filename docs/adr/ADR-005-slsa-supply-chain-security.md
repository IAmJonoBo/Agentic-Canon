# ADR-005: SLSA for Supply Chain Security

## Status

Accepted

## Context

Software supply chain attacks have increased dramatically, with high-profile incidents like SolarWinds and Log4Shell demonstrating the critical need for supply chain security. We need to ensure that:

1. **Build Integrity**: Builds are reproducible and tamper-proof
2. **Provenance**: Clear record of how artifacts were built
3. **Dependencies**: Verified and audited dependencies
4. **Attestation**: Cryptographic proof of build process
5. **Verification**: Ability to verify artifacts before use

Multiple supply chain security frameworks exist:
- SLSA (Supply-chain Levels for Software Artifacts)
- NIST SSDF (Secure Software Development Framework)
- OpenSSF Scorecard
- In-Toto framework
- Sigstore ecosystem
- Software Bill of Materials (SBOM)

## Decision

We will implement **SLSA (Supply-chain Levels for Software Artifacts)** as our primary supply chain security framework, with progressive levels of compliance (targeting SLSA Level 3 for production templates).

## Rationale

### Why SLSA?

1. **Industry Standard**: Created by Google, adopted by CNCF and OpenSSF
2. **Progressive Levels**: Four levels (0-3) allow incremental adoption
3. **Specific Requirements**: Clear, measurable requirements at each level
4. **Provenance Focus**: Emphasizes build provenance and attestation
5. **Tool Support**: Growing ecosystem of tools and integrations
6. **Framework Agnostic**: Works with any build system or language
7. **Verification**: Enables downstream verification of artifacts
8. **Complement Standards**: Works alongside NIST SSDF and OpenSSF

### SLSA Levels Overview

#### SLSA Level 0 (Baseline)
- No guarantees
- Manual or ad-hoc build process

#### SLSA Level 1 (Build Process Exists)
- ✅ Automated build process
- ✅ Provenance generated (unsigned)
- Basic documentation

#### SLSA Level 2 (Build Service)
- ✅ Hosted build service (GitHub Actions)
- ✅ Signed provenance
- ✅ Build service generates attestation
- ✅ Tamper-resistant build logs

#### SLSA Level 3 (Hardened Build Platform)
- ✅ Isolated build environment
- ✅ Ephemeral environments
- ✅ Hermetic builds (no network access)
- ✅ Non-falsifiable provenance
- ✅ Two-person review

#### SLSA Level 4 (Future)
- Two-person review enforced
- Hermetic builds with maximum security
- (Not implemented in initial templates)

### Implementation Strategy

Our templates will implement SLSA progressively:

1. **All Templates**: SLSA Level 1 (automated builds with provenance)
2. **Security-Enabled**: SLSA Level 2 (signed provenance)
3. **Production-Ready**: SLSA Level 3 (hardened builds)

### SLSA Components

#### 1. Build Provenance (in-toto format)

```yaml
# Example provenance for Python package
_type: https://in-toto.io/Statement/v0.1
subject:
  - name: demo-service-0.1.0.tar.gz
    digest:
      sha256: abc123...
predicateType: https://slsa.dev/provenance/v0.2
predicate:
  builder:
    id: https://github.com/actions/runner/v2
  buildType: https://github.com/actions/workflow
  invocation:
    configSource:
      uri: git+https://github.com/user/repo@refs/heads/main
      digest:
        sha1: def456...
  metadata:
    buildStartedOn: "2024-01-01T12:00:00Z"
    buildFinishedOn: "2024-01-01T12:05:00Z"
  materials:
    - uri: git+https://github.com/user/repo
      digest:
        sha1: def456...
```

#### 2. SBOM Generation (CycloneDX)

All builds generate Software Bill of Materials:
- Lists all dependencies with versions
- Identifies licenses
- Tracks vulnerability status
- Signed and attested

```bash
# Python
cyclonedx-py -o sbom.json

# Node.js
cyclonedx-node -o sbom.json

# Go
cyclonedx-gomod -json=true -output=sbom.json
```

#### 3. Artifact Signing (Sigstore)

Use keyless signing with Sigstore/Cosign:

```bash
# Sign artifacts
cosign sign-blob --bundle=signature.bundle artifact.tar.gz

# Verify
cosign verify-blob --bundle=signature.bundle \
  --certificate-identity-regexp=".*" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  artifact.tar.gz
```

#### 4. GitHub Actions Integration

```yaml
# Example workflow with SLSA provenance
name: Release with SLSA
on:
  release:
    types: [created]

permissions:
  id-token: write  # Required for OIDC
  contents: write
  attestations: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build artifact
        run: |
          # Build process
          make build
      
      - name: Generate SBOM
        run: cyclonedx-py -o sbom.json
      
      - name: Generate provenance
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: dist/*
      
      - name: Sign artifacts
        run: |
          cosign sign-blob --bundle=sig.bundle dist/artifact.tar.gz
```

### Security Controls

1. **Source Control**: All code in version control
2. **Branch Protection**: Required reviews, status checks
3. **Build Isolation**: Ephemeral, isolated build environments
4. **Dependency Pinning**: Lock files with exact versions
5. **Vulnerability Scanning**: Automated scanning of dependencies
6. **Secret Management**: No hardcoded secrets, use secret stores
7. **Access Control**: Least privilege for build systems
8. **Audit Logging**: All builds logged and auditable

## Consequences

### Positive

- **Trust**: Downstream consumers can verify artifact integrity
- **Transparency**: Clear record of build process and dependencies
- **Security**: Reduced risk of supply chain attacks
- **Compliance**: Meets industry standards and regulations
- **Automation**: Automated attestation and verification
- **Incident Response**: Better forensics when issues arise
- **Reputation**: Demonstrates security best practices
- **Ecosystem**: Integrates with growing SLSA ecosystem

### Negative

- **Complexity**: Additional steps in build process
- **Time**: Builds take slightly longer
- **Storage**: Provenance and attestations require storage
- **Maintenance**: Must keep attestation tools updated
- **Learning Curve**: Teams must understand SLSA concepts
- **Verification**: Downstream users must verify (if they choose)

### Mitigation Strategies

1. **Templates**: SLSA built into all templates by default
2. **Documentation**: Clear guides in notebooks and examples
3. **Automation**: Fully automated, no manual intervention
4. **Caching**: Efficient caching to minimize build time
5. **Toggles**: Optional SLSA features via template variables
6. **Examples**: Working examples in all templates
7. **Tools**: Use mature, supported tools (Sigstore, in-toto)

## Implementation Per Template

### Python Service
- ✅ SLSA Level 2 available via template option
- ✅ Provenance generation with GitHub attestations
- ✅ SBOM with CycloneDX
- ✅ Sigstore signing support
- ✅ Dependency verification with pip-audit

### Node.js Service
- ✅ SLSA Level 2 available via template option
- ✅ Provenance generation
- ✅ SBOM with CycloneDX
- ✅ npm audit for vulnerabilities
- ✅ Sigstore signing

### Go Service
- ✅ SLSA Level 2 available
- ✅ Provenance generation
- ✅ SBOM with CycloneDX
- ✅ Go module verification
- ✅ Sigstore signing

### React WebApp
- ✅ SLSA Level 2 for build artifacts
- ✅ Provenance for deployable bundles
- ✅ SBOM for dependencies
- ✅ Subresource Integrity (SRI) for CDN assets

## Verification Workflow

### Artifact Producer (Our Templates)
1. Build artifact in isolated environment
2. Generate SBOM listing all dependencies
3. Create provenance attestation
4. Sign artifact and provenance with Sigstore
5. Publish artifact with attestations

### Artifact Consumer (Downstream Users)
1. Download artifact and attestations
2. Verify signature with Sigstore
3. Verify provenance (builder, materials, process)
4. Check SBOM for known vulnerabilities
5. Validate against security policy
6. Use artifact if all checks pass

## Alternatives Considered

### Manual Documentation
**Pros**: Simple, no tooling required
**Cons**: Not verifiable, not machine-readable, error-prone
**Rejected**: Doesn't provide cryptographic guarantees

### Vendor-Specific Solutions
**Pros**: Integrated with specific platforms
**Cons**: Vendor lock-in, not standardized
**Rejected**: Doesn't align with open standards approach

### Custom Attestation
**Pros**: Full control, tailored to needs
**Cons**: Not interoperable, no ecosystem support
**Rejected**: Reinventing wheel, no community adoption

### NIST SSDF Only
**Pros**: Comprehensive security framework
**Cons**: More about process than technical implementation
**Rejected**: SLSA complements SSDF with technical specifics

## References

- [SLSA Official Specification](https://slsa.dev/)
- [SLSA GitHub Repository](https://github.com/slsa-framework/slsa)
- [in-toto Framework](https://in-toto.io/)
- [Sigstore Project](https://www.sigstore.dev/)
- [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [NIST SSDF](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [CycloneDX SBOM Specification](https://cyclonedx.org/)
- [GitHub Artifact Attestations](https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds)

## Related ADRs

- [ADR-003: GitHub Actions for CI/CD](ADR-003-github-actions-cicd.md) - Platform for SLSA implementation
- [ADR-006: Security Scanning Strategy](ADR-006-security-scanning-strategy.md) - Complementary security measures
- [ADR-007: Secret Management](ADR-007-secret-management.md) - Secure secrets in build
- [ADR-008: Dependency Management](ADR-008-dependency-management.md) - Managing supply chain dependencies

## Compliance Mapping

### SLSA → Other Standards

| SLSA Requirement | NIST SSDF | OWASP SAMM | OpenSSF |
|-----------------|-----------|------------|---------|
| Automated build | PO.3.1 | B-SB-1 | CI/CD |
| Build service | PO.3.2 | B-SB-2 | Scorecard |
| Provenance | PO.3.3 | B-SB-3 | Sigstore |
| Isolated builds | PO.5.1 | I-SD-1 | - |
| Signed attestation | PO.3.3 | V-ST-2 | Sigstore |

## Implementation Status

- [x] SLSA concepts documented
- [x] Provenance generation workflow
- [x] SBOM generation support
- [x] Sigstore signing examples
- [x] Security scanning workflows
- [ ] Python template includes SLSA Level 2
- [ ] Node.js template includes SLSA Level 2
- [ ] Go template includes SLSA Level 2
- [ ] React template includes SLSA Level 2
- [ ] Verification tooling documentation
- [ ] SLSA Level 3 implementation plan

## Roadmap

### Phase 1 (Current) - SLSA Level 2
- Automated builds with GitHub Actions
- Signed provenance attestations
- SBOM generation
- Sigstore keyless signing

### Phase 2 (Near-term) - SLSA Level 3
- Hermetic builds (no network access during build)
- Reproducible builds
- Two-person review enforcement
- Enhanced isolation

### Phase 3 (Future) - Advanced Features
- SLSA Level 4 exploration
- Policy enforcement with OPA
- Automated verification gates
- Supply chain risk scoring
- Dependency vulnerability auto-remediation

## Success Metrics

- ✅ All templates support SLSA Level 1
- 🎯 Security-enabled templates reach SLSA Level 2
- 🎯 100% of releases include provenance
- 🎯 100% of releases include SBOM
- 🎯 All artifacts signed with Sigstore
- 🔮 Example projects demonstrate verification
- 🔮 Documentation includes verification guides

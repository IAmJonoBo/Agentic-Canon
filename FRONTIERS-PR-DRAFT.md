# PR Draft — docs/frontiers-v1

## Summary

- Introduce MkDocs Material documentation system (`mkdocs.yml`) with Diátaxis-aligned navigation.
- Publish 20+ refreshed pages covering principles, quality, security, supply-chain, benchmarks, and contributor workflows with machine-validated front matter.
- Update AI-safety coverage to the 2025 OWASP LLM Top 10 and map NIST SP 800-218A (final) to existing controls, backed by refreshed policy YAMLs.
- Align supply-chain content and policies with SLSA v1.1, including verification-summary guidance and migration notes toward SLSA 1.2.

## Decisions

1. Adopt JSON Schema–validated front matter (`frontiers/policy/frontiers.schema.json`) with provenance requirements.
2. Treat SLSA Level 3 (v1.1), ASVS L2/L3, and OWASP LLM Top 10 (2025) controls as mandatory and codify via policy YAML.
3. Keep legacy Jupyter Book content archived in `docs_legacy/` while new MkDocs site becomes primary.

## Outstanding TODOs

- [ ] Wire schema validation and link checking into CI (e.g., `mkdocs build --strict` + custom script).
- [ ] Integrate mike-based docs versioning and publish pipeline to GitHub Pages.
- [ ] Update incident runbooks with AI-specific playbooks referenced in security docs.
- [ ] Automate waiver reminder comments before expiry.

## Maintainer Checklist

- [ ] Review new documentation structure and ensure nav matches product expectations.
- [ ] Confirm `frontiers/quality-gate.yml` imports cleanly in downstream repos (dry-run recommended).
- [ ] Verify policy YAMLs satisfy governance requirements and link correctly in docs.
- [ ] Run `mkdocs build --strict` locally (or via container) and inspect output for warnings.
- [ ] Decide timeline for decommissioning legacy Jupyter Book (`docs_legacy/`).

> Branch: `docs/frontiers-v1`

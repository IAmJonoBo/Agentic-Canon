Executive summary first, then we weaponise it for a model.

You want the Agentic-Canon repo  ￼ turned into a model-executable brief that: (1) turns every control into enforceable policy-as-code (Rego / Conftest / Semgrep) in the style of OPA/Conftest  ￼, (2) aligns to NIST AI RMF govern–map–measure–manage and the 2024–25 generative profile  ￼, (3) bakes in LLM/agent failure modes from OWASP LLM Top 10 2025 so we treat AI output as hostile  ￼, and (4) exposes the Canon as a policy oracle + self-healing repo loop. Talk of money is noise; we ignore it.

Below is the brief, in a form a code-gen model (your “Codex”) can run without guessing.

⸻

1. Meta

brief_id: agentic-canon/policy-oracle-v1
author: Jonathan (source conversation)
optimised_for: LLM/codegen agents (GitHub, MCP, REST)
status: draft-for-implementation
influence_alert: none_detected  # user request is descriptive, not coercive
primary_sources:
  - agentic-canon-repo: https://github.com/IAmJonoBo/Agentic-Canon
  - nist_ai_rmf_1_0: NIST.AI.100-1.pdf
  - nist_ai_rmf_genai_profile_2024: NIST.AI.600-1.pdf
  - owasp_llm_top_10_2025: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - opa/conftest: https://github.com/open-policy-agent/conftest

Sources:  ￼

⸻

2. Mission statement

Build an agent-addressable policy oracle over Agentic-Canon so that every LLM/agent action (scaffold service, add CI, generate SBOM, add threat model) must first ask: “what does the Canon require here?”; and so that repositories can self-heal to the Canon via nightly agents that open PRs with missing steps/templates and attach control IDs. This shifts policy to first-class, delivers lineage, and matches NIST AI RMF practice for governed AI artefacts.  ￼

⸻

3. Definition of done (high level)
	1.	Policy Oracle service exists (MCP + REST) that, given an intent ("new-fastapi-service", "add-sbom", "harden-llm"), returns:
	•	required Canon controls (IDs from control-traceability-matrix.json)
	•	canonical artefacts/templates (from catalog.json)
	•	evidence/attestation clauses
	•	emitted Rego/Conftest/Semgrep rules
	•	references to NIST AI RMF functions (govern/map/measure/manage) and AI-specific controls
Source: Canon structure at root of repo.  ￼
	2.	SDK for agents ships with verbs: create_service, add_ci, add_sbom, add_threatmodel, attest_artefact, open_canon_pr.
	3.	Pipelines emit attestations for every generated artefact, signed or at least content-addressed, naming Canon version + control pack.
	4.	Exporters can turn Canon controls into OPA/Rego/Conftest and Semgrep rules.  ￼
	5.	CI quality gates enforce: no green checks → no “done”; hostile-AI stance: SAST + IaC + dep policy + SBOM + provenance mandatory. This is consistent with 2025 LLM vuln base rates.  ￼
	6.	Reference integrations for GitHub Actions, GitLab CI, Azure DevOps, and GitHub’s MCP/agents. (One well-documented exemplar = enough.)
	7.	Feedback loop: CI scan results are ingested to auto-bump Canon rules that repeatedly catch LLM mistakes.

⸻

4. Inputs and artefacts (what Codex can rely on)
	•	control-traceability-matrix.json: machine-readable map of Canon controls. (Treat as authoritative source of control IDs.)  ￼
	•	catalog.json: catalogue of templates, CI blocks, doc skeletons. (Treat as authoritative source of artefact locations.)  ￼
	•	templates/ tree: supply CI, SBOM, SLSA, docs, ADR/C4, SLOs, runbooks.  ￼
	•	NIST AI RMF 1.0 + 2024 GenAI profile for control provenance.  ￼
	•	OWASP LLM Top 10 2025 for LLM-specific threat models.  ￼
	•	OPA/Conftest + Semgrep rule formats.  ￼

Assumption: SOC 2 and ISO/IEC 27001 mappings are referenced but not fully present → brief must create fields, not content. (Stateful gap.)

⸻

5. Data model for “every control gets fields”

{
  "control_id": "CANON-SBOM-BASE",
  "title": "SBOM present for all AI-generated artefacts",
  "source": [
    { "framework": "NIST AI RMF", "ref": "MEASURE.2", "version": "1.0" },
    { "framework": "OWASP LLM Top 10 2025", "ref": "LLM05", "version": "2025" },
    { "framework": "ISO/IEC 27001", "ref": "A.12.5.1", "version": "2022" }
  ],
  "rationale": "AI-generated artefacts have higher base-rate supply chain and output-handling risk in 2025; SBOM + provenance enables selective trust.",
  "version": "1.1.0",
  "rego": "package canon.sbom\n\ndeny[msg] {\n  not input.sbom.exists\n  msg := \"SBOM missing for artefact\"\n}\n",
  "conftest": "same as rego, path-bound to repo/.canon/policy",
  "semgrep": {
    "id": "canon.sbom.present",
    "pattern": "SBOM",
    "languages": ["generic"],
    "message": "SBOM reference must be present in generated artefact."
  },
  "attestation_template": {
    "source": "agentic-canon",
    "canon_version": "1.1.0",
    "controls": ["CANON-SBOM-BASE"],
    "generated_at": "$ISO_8601",
    "status": "pass|fail",
    "evidence": ["sbom.json", "slsa-provenance.json"]
  }
}

This is exactly what you described: advice → enforcement, PaC style, aligned with current OPA/Conftest practice.  ￼

⸻

6. Services to build

6.1 Policy Oracle API

Purpose: central governance plane (open, GitHub-first) that LLM agents must query before planning/executing. Mirrors AAGATE/NIST-aligned control planes.  ￼

Endpoints (Codex to implement):
	1.	POST /canon/controls/apply
	•	Input: { "intent": "new-fastapi-service", "stack": "python", "ai_origin": true }
	•	Output: list of controls, each with: control_id, rationale, source, version, enforcement (rego|conftest|semgrep), required_templates, evidence_clauses.
	2.	GET /canon/templates/{id}
	•	Arms the agent with the actual template from catalog.json.
	3.	POST /canon/attest
	•	Accepts artefact metadata and returns signed attestation blob.
	4.	POST /canon/scan-results
	•	Ingests CI/SAST/IaC/dependency findings and updates Canon rule weights.

Non-goals: user auth, billing, UI.

Quality gates for this service:
	•	100% of listed endpoints have OpenAPI 3.1 spec in repo (/docs/api/policy-oracle.openapi.yaml).
	•	Unit tests for schema validation.
	•	CI runs OPA/Conftest against sample payloads.
	•	“No green → no done” applies here too.

⸻

6.2 Agent SDK

Targets: Python (for GitHub/GitLab bots), Node/TS (for MCP/VS Code agents).

Exports (minimal):

canon = CanonClient(base_url="https://canon.local")
plan = canon.controls_for("new-fastapi-service")
repo = Repo(".")
repo.apply_templates(plan.required_templates)
repo.write_attestation(canon.attest(plan, artefacts=repo.artefacts()))
repo.open_pr_with_controls(plan.controls)

SDK MUST: (a) prefer Canon templates over internal scaffolding, (b) add audit-friendly PR descriptions with control IDs, (c) tag AI-origin SBOM entries.

⸻

6.3 Exporters
	1.	Canon → Rego/Conftest
	•	Input: control-traceability-matrix.json
	•	Output: policy/<control_id>.rego
	•	Optionally bundle into bundle.tar.gz for OPA sidecars.
	2.	Canon → Semgrep
	•	Generate a ruleset grouping AI-specific missteps (prompt injection mitigations, insecure output handling, excessive agency) mapped to OWASP LLM Top 10 2025.  ￼

Quality gate: exporter must produce policies that pass opa test / conftest test with sample inputs from repo.  ￼

⸻

6.4 CI reference integrations

Produce 3 reference pipelines:
	1.	GitHub Actions: checkout → format/lint → SAST → IaC (Conftest) → dep policy → SBOM (Syft or similar) → sigstore/in-toto-style provenance → call Canon /attest → fail on any red.
	2.	GitLab CI: same sequence.
	3.	Azure DevOps: same sequence.

These pipelines must consume the generated Rego/Semgrep to close the loop, just like cloud-native PaC described by vendors such as Wiz/Jit (mirroring the user’s analogy). We can model after public OPA/Conftest CI examples.  ￼

⸻

7. Milestones (no dates)
	1.	M1 – Canon schema hardening
	•	Formalise control JSON schema (fields above).
	•	Add NIST AI RMF and OWASP LLM Top 10 mappings to ≥80% of current controls.
	•	Add versioning & provenance rules.
	•	Gate: JSON schema tests pass; docs regenerated.
	2.	M2 – Policy Oracle MVP
	•	REST + MCP surface with 3 endpoints above.
	•	Uses control-traceability-matrix.json + catalog.json.
	•	Gate: Integration test: sample agent (new-fastapi-service) gets non-empty control list, ≥1 template, ≥1 evidence clause.
	3.	M3 – Agent SDKs
	•	Python + TS SDKs.
	•	PR autowriter that injects control IDs in description.
	•	Gate: Running the SDK against a repo without SBOM yields a PR adding SBOM + attestation.
	4.	M4 – Exporters
	•	Canon → Rego/Conftest
	•	Canon → Semgrep
	•	Gate: Generated policies run cleanly in CI exemplar.
	5.	M5 – Self-healing repo agent
	•	Nightly job: read Canon → diff repo → open PR with missing Canon bits (SBOM step, red-team readme, SLOs).  ￼
	•	Gate: At least 3 missing-control scenarios covered; PRs show control lineage.
	6.	M6 – Attestation everywhere
	•	Artefact-level attestation template baked into templates/.
	•	Provenance compatible with SLSA / in-toto style.  ￼
	•	Gate: CI fails when attestation missing.
	7.	M7 – Reference integrations
	•	3 CI/CD recipes published.
	•	GitHub MCP listing created (read-only).
	•	Gate: Agents in GitHub can call Canon without extra code.

⸻

8. Quality gates (global)
	•	QG1 – “No green → no done”: any of {format/lint, SAST, IaC policy, dep policy, SBOM+provenance} fails → pipeline fails → PR blocked. Mirrors 2025 enterprise ask for AI-assisted code.  ￼
	•	QG2 – AI-origin SBOM tag: every artefact generated by an LLM/agent has ai_origin: true in SBOM and in attestation.
	•	QG3 – Attested or rejected: merge only if there is an attestation referencing Canon version + control pack.
	•	QG4 – Policy tests present: OPA/Conftest tests exist for every generated Rego rule.
	•	QG5 – Traceability: PRs created by agents must mention control IDs from matrix and link to generated policies.
	•	QG6 – Security-by-default: default templates always emit SAST + IaC + dep policy hooks; no “quickstart” that bypasses security.
	•	QG7 – Alignment checks: prompts/tool calls for LLM agents pass through guardrails (NeMo Guardrails / Guardrails.ai) to reduce jailbreak noise before they hit Canon.  ￼

⸻

9. Example outputs for the model

9.1 Example Rego from Canon control

package canon.fastapi

deny[msg] {
  input.intent == "new-fastapi-service"
  not input.ci.includes["sbom"]
  msg := "FastAPI service must include SBOM step per CANON-SBOM-BASE"
}

9.2 Example Semgrep rule (LLM output handling)

rules:
  - id: canon.llm.insecure-output
    languages: [python]
    message: "LLM output must be sanitised or validated – see CANON-LLM-OUTPUT-001"
    patterns:
      - pattern: "response = llm.generate(...)"
      - pattern-not: "sanitize(response)"
    severity: ERROR
    metadata:
      canonical_control: CANON-LLM-OUTPUT-001
      source: OWASP-LLM-2025-LLM02

Maps to OWASP LLM “Insecure Output Handling”.  ￼

⸻

10. Non-functional
	•	Docs: add /docs/canon-oracle.md and update BIBLE.md to name the service.  ￼
	•	License: stay MIT.
	•	Security posture: treat all AI output as hostile; ingest → normalise → prove → attest. Mirrors NIST demand for measuring and managing AI risk.  ￼

⸻

11. Ranked build strategy
	1.	Minimal viable control plane (M1–M2): unlocks every other step.
	2.	Exporters (M4): closes advice → enforcement gap; highest leverage.
	3.	Self-healing agent (M5): makes Canon living, not static.
	4.	MCP publishing (M7): gives you network effects once GitHub/other agents can mount it.

⸻

12. Provenance block (as you asked)

Data. Agentic-Canon repo structure (controls + templates)  ￼; NIST AI RMF 1.0 + 2024 GenAI profile for governance verbs and auditability  ￼; OWASP LLM Top 10 2025 for LLM-specific risks  ￼; OPA/Conftest and Semgrep public patterns for PaC enforcement  ￼.

Methods. Mapped Canon controls → added source/rationale/version/emission fields → wrapped in REST/MCP policy-oracle → added CI-first gating → added exporters → added attestation and self-healing loop.

Key results. Single source of policy truth; agents forced to query it; all artefacts attested; CI blocks on policy; policies re-learn from scan feedback.

Uncertainty. Repo’s current JSON content could change; SOC 2 / ISO 27001 mappings are only sketched, not canonical; signing story depends on what the target platform already supports.

Safer alternative. Start with read-only policy oracle + exporters + GitHub Action that only warns (does not fail) for non-attested artefacts, then ratchet to “no green → no done”.

⸻

That’s the brief. It should be directly feedable to your code-gen agent with minimal hallucination space. Next natural extension is to add the “frontier arbitration” layer on top of the oracle, but that is optional for v1.

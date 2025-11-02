Brief: Canon Code-Quality Gates with HumanEval

1. Intent

Make code-quality evaluation as mandatory as SAST/IaC/SBOM in Agentic-Canon. Every AI/agent/model-sourced code path must be able to prove “this would have passed HumanEval-class tasks” using an execution harness that is (a) MIT-licensed and embeddable, (b) sandboxed, and (c) extendable to harsher suites (EvalPlus, HumanEval-X/XL) so we keep pace with 2025 multi-language work. HumanEval is MIT, so we can vendor it.  ￼

2. Background and evidence
	•	HumanEval (OpenAI, 2021) is still the canonical, execution-based test of function-level codegen; pass@k is the right metric for generators.  ￼
	•	Its tests are too shallow on their own; EvalPlus shows many models “pass” only because the test sets are tiny. So: HumanEval → EvalPlus-augmented → trustworthy score.  ￼
	•	There are 2024–25 multilingual extensions (HumanEval-X, HumanEval-XL) so, as soon as n00tropic emits non-Python, we can still run the same gate.  ￼
	•	HumanEval repo explicitly warns to run untrusted code in a robust security sandbox; the Canon must encode that.  ￼

3. What to build

3.1 Eval packs in the Canon
Add a new artefact type to catalog.json:

{
  "id": "evalpack-humaneval",
  "type": "eval_pack",
  "source": "openai/human-eval@<pinned-commit>",
  "license": "MIT",
  "rationale": "Execution-based functional correctness gate for AI/agent code.",
  "runner": "python -m human_eval.evaluate --samples $SAMPLES_JSONL",
  "variants": [
    { "id": "evalplus", "source": "EvalPlus 2023", "runner": "python -m evalplus.evaluate --enhanced" },
    { "id": "humaneval-x", "source": "CodeGeeX HumanEval-X", "runner": "python run_he_x.py" }
  ]
}

This makes HumanEval something an agent can ask the Oracle for just like “add SBOM”. Canon turns advice into execution.  ￼

3.2 CI step: “codegen-quality”
Extend the reference pipelines (GitHub/GitLab/Azure) you already plan to ship so that, when the PR is AI-origin (ai_origin: true in SBOM/attestation), an extra job runs:
	1.	Build an ephemeral, unprivileged container (rootless, seccomp, no Docker-in-Docker).
	2.	Pull / reuse vendored HumanEval harness.
	3.	Run one of:
	•	agent-produced samples in HumanEval format (PR attaches samples.jsonl);
	•	model’s current eval snapshot (from training artefacts) to track regressions.

Gate: if pass@1 on HumanEval or “#passed / #tasks” on EvalPlus < policy threshold (say 0.85 for internal agents, 0.9 for shipped model), pipeline fails. This is “no green → no done” extended to “no correct → no done.”  ￼

3.3 Sandboxing requirement
Because HumanEval literally executes arbitrary Python, the Canon must carry an execution profile:

{
  "execution_profile": {
    "runtime": "python3.11",
    "isolation": "docker+seccomp",
    "timeout_sec": 6,
    "mem_limit_mb": 512,
    "net": "off"
  }
}

No profile → job refused. That mirrors the HumanEval README warning.  ￼

3.4 Use in three places (one schema)
	1.	Generated content tests – every agent PR that adds code.
	2.	Agent-competence tests – when an agent is updated, run a fixed HumanEval/EvalPlus slice to prove it didn’t get dumber.
	3.	Model regression tests – when you train/finetune your n00tropic model, run the full suite + EvalPlus + one multilingual slice; record pass@{1,5,10}. That’s how open code models report in 2025.  ￼

Same harness, different subjects.

⸻

4. Milestones
	1.	CQ-M1 – Vendor & pin
	•	Vendor openai/human-eval into tools/eval/humaneval/ with MIT licence text.
	•	Add Canon entry evalpack-humaneval.
	•	Gate: python -m human_eval.evaluate ... runs inside repo CI.  ￼
	2.	CQ-M2 – EvalPlus augmentation
	•	Integrate EvalPlus to harden tests. Expose as evalpack-humaneval-strong.
	•	Gate: at least 30% of solutions that passed vanilla HumanEval must now fail → proves hardening worked.  ￼
	3.	CQ-M3 – CI job for AI-origin PRs
	•	Modify GitHub/GitLab templates to: detect AI PR → run eval pack → attach JSON result to PR.
	•	Gate: PR shows canon_eval: pass and failing PRs get a Canon-suggested patch.
	4.	CQ-M4 – Model regression runner
	•	Script that: runs model → produces HumanEval samples → runs EvalPlus → posts metrics to /canon/scan-results.
	•	Gate: Oracle stores per-model series for dashboarding.
	5.	CQ-M5 – Multilingual slice
	•	Add HumanEval-X/XL subset for languages your agents emit (start with JS/TS, Go).  ￼
	•	Gate: same CI job can switch language by label.

⸻

5. Quality gates (code-quality specific)
	•	QG-CQ1 – Licensed + pinned. HumanEval is MIT, so it can be redistributed, but Canon must pin commit SHA and keep LICENCE alongside.  ￼
	•	QG-CQ2 – Sandbox or reject. No sandbox spec → Canon refuses to run the eval.
	•	QG-CQ3 – EvalPlus first. If EvalPlus is available, prefer that score, since vanilla HumanEval overestimates correctness.  ￼
	•	QG-CQ4 – Attach to attestation. Attestation for the artefact must include:

"code_eval": {
  "suite": "humaneval+evalplus",
  "pass_at_1": 0.92,
  "date": "2025-11-02",
  "runner": "canon-humaneval-runner@<sha>"
}

That way auditors see functional quality, not just security.

	•	QG-CQ5 – Non-Python fallback. If language ≠ Python and suitable HumanEval-X task not found, gate downgrades to “warn” and suggests adding a task. (Noisy failure is better than silent success.)  ￼

⸻

6. How this fits the arbitration layer

Arbitration was: fan-out → score → pick. Now the scoring function gets an extra term:

score = w_policy*policy_score
      + w_security*security_score
      + w_eval*eval_pass_rate   # from HumanEval/EvalPlus
      - w_runtime*flakiness

So even if all 3 models produce policy-compliant code, the one that actually executes correctly in HumanEval wins. That’s the bridge from “syntactically sanctimonious” to “works”.  ￼

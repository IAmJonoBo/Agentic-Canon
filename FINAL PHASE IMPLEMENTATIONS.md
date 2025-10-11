#FINAL PHASE IMPLEMENTATIONS

1) Cherry-pick templates & assets (private + public)

Supported pulls (use any):
	•	Sparse-checkout + partial clone (built-in Git):

git clone --filter=blob:none --no-checkout https://github.com/<you>/agentic-canon.git
cd agentic-canon
git sparse-checkout init --cone
git sparse-checkout set templates/<id> assets/<id>
git checkout main

Partial clone keeps blobs out until checkout; sparse-checkout materialises selected paths only.  ￼

	•	tiged (degit fork) – grab a subfolder w/o git history:
Public: npx tiged <you>/agentic-canon/templates/<id> target/
Private: npx tiged --mode=git [email protected]:<you>/agentic-canon/templates/<id> target/ (SSH)  ￼
	•	Release bundles + GitHub CLI (immutable zips):

gh auth login
gh release download -R <you>/agentic-canon --pattern "template-<id>-*.zip" -D .

Works for both private and public; --pattern matches selected assets.  ￼

Optional: mark some subrepos as template repositories later; anyone with read access can generate a new repo from them (private or public org policy).  ￼

⸻

2) Dependencies: online-first, offline-ready, Renovate-kept

Python
	•	Online config: use environment or pip.conf:

PIP_INDEX_URL=https://pypi.org/simple
# (add a vetted mirror only if needed)

pip honours --index-url/--extra-index-url; prefer a single trusted index to reduce confusion.  ￼

	•	Offline fallback (wheelhouse):

# build cache
python -m pip download -r requirements.txt -d wheelhouse/
# offline install
python -m pip install --no-index --find-links=wheelhouse -r requirements.txt

This is the canonical pip path for offline installs.  ￼

Node
	•	Yarn Zero-Installs (commit .yarn/cache + .pnp.cjs) → works without yarn install after clone; perfect for agents and CI in private repos.  ￼

Keep them fresh (no drift)
	•	Renovate: enable lockfile maintenance weekly; update pip (pip-compile/uv) + npm/yarn managers; CI rebuilds wheelhouse and re-uploads caches on tag/release.

⸻

3) Automation: package “pickables” and caches

Release packer (private by default; works public too):
.github/workflows/release-assets.yml

name: Package templates & caches
on: { push: { tags: ['v*'] }, workflow_dispatch: {} }
jobs:
  pack:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Zip templates
        run: for d in templates/*; do zip -r "template-$(basename "$d")-${GITHUB_REF_NAME:-dev}.zip" "$d"; done
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: python -m pip download -r requirements.txt -d wheelhouse/
      - uses: actions/upload-artifact@v4
        with: { name: build-artifacts, path: "template-*.zip\nwheelhouse/**" }
      - name: Publish to release
        run: |
          gh release create "${GITHUB_REF_NAME}" -t "${GITHUB_REF_NAME}" -n "Automated assets" || true
          gh release upload "${GITHUB_REF_NAME}" template-*.zip wheelhouse/** --clobber
        env: { GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

Uses Artifacts for run distribution; publishes to Releases for long-term, authenticated fetch.  ￼

Cache installs in other workflows (example):

- uses: actions/cache@v4
  with: { path: ~/.cache/pip, key: pip-${{ hashFiles('requirements.txt') }} }
- uses: actions/cache@v4
  with: { path: .yarn/cache, key: yarn-${{ hashFiles('yarn.lock') }} }

GitHub cache action is the supported way to speed dependency restores.

⸻

4) Storybook deploy: private-first, public-ready
	•	Private (default): on GitHub Enterprise Cloud, enable access-controlled Pages so only repo readers can view the site. Use the same Actions flow; set Pages → private in repo settings.  ￼
	•	Public flip: change Pages visibility to public; no workflow change.
	•	If you don’t have Private Pages: keep Storybook as a build artifact instead of Pages (no public exposure). Publishing to Pages uses upload-pages-artifact + deploy-pages.  ￼

⸻

5) Notebook “setup wizards” for agents (auto-maintained)

Include parameterised notebooks for env bootstrap:
	•	notebooks/setup/python_env.ipynb → detects connectivity; online installs from index; offline installs from wheelhouse/; writes a short machine-readable run log.
	•	notebooks/setup/node_env.ipynb → validates Yarn Zero-Installs; if cache missing, falls back to online; logs results.

Run them in CI with Papermill to keep outputs current and reproducible:

papermill notebooks/setup/python_env.ipynb notebooks/_out/python_env.ipynb -p use_offline false

Papermill is designed for parameterised, headless notebook execution.

⸻

6) One machine-readable catalog for agents

/catalog.json

{
  "templates": [
    {
      "id": "react-webapp",
      "path": "templates/react-webapp",
      "release_asset_pattern": "template-react-webapp-*.zip",
      "tiged": "git@github.com:<you>/agentic-canon/templates/react-webapp",
      "tags": ["web","react","vite"]
    }
  ],
  "artifacts": [
    { "id": "python-wheelhouse", "release_asset_pattern": "wheelhouse/**" }
  ]
}

Agents choose sparse-checkout, tiged, or gh release download based on this index.  ￼

⸻

7) Copilot brief (drop in README)

Default private. To fetch a template:
1) Sparse-checkout (auth): git clone --filter=blob:none --no-checkout <repo>; git sparse-checkout set templates/<id>; git checkout main.
2) Private tiged: npx tiged --mode=git git@github.com:<you>/agentic-canon/templates/<id> <dir>.
3) Releases: gh release download -R <you>/agentic-canon --pattern "template-<id>-*.zip".
Deps: online via PIP_INDEX_URL / Yarn; offline via wheelhouse/.yarn/cache. Notebooks: run Papermill setup to auto-configure.


⸻

Practical toggles (what’s different between the two tracks)
	•	Auth: PAT/SSH for private pulls; public has anonymous tar or HTTPS. tiged supports --mode=git for private SSH.  ￼
	•	Storybook: Private Pages (Enterprise Cloud) vs public Pages; or keep as artifact only.  ￼
	•	Distribution: Private Releases are only visible to repo readers; public Releases are world-readable. gh release download works for both; add -R to target any repo.  ￼
	•	Dependencies: Same flows; Zero-Installs + wheelhouse remove internet requirement entirely when needed.  ￼

⸻

FINAL PREFLIGHT PHASE

Technical Brief — Agentic Canon MCP Server & Generators

Objective

Expose Agentic Canon as an MCP server so agents can discover, parameterise, and invoke scaffolds, docs, and automations through a standard protocol (tools, resources, prompts). Clients: Claude Desktop (local or remote server), ChatGPT via OpenAI Agents SDK, Gemini CLI; later any MCP-compatible IDE/agent.  ￼

Why MCP here
	•	Standardised surface: MCP defines tools, resources, and prompts—perfect for “generators + catalog + guide”.  ￼
	•	Multi-client reach: Claude Desktop supports local servers + one-click Desktop Extensions; OpenAI and Google now document MCP integrations.  ￼
	•	Ecosystem leverage: Official SDKs and reference servers (filesystem, GitHub, databases) accelerate delivery.  ￼

Scope (MVP → v1)
	1.	Resources (read-only by default)
	•	ac://catalog → serves /catalog.json (templates, releases, assets).
	•	ac://bible/* → machine-readable docs (MD/JSON/YAML) for the “Bible”.
	•	ac://examples/* → minimal code samples & policy snippets.
Map to MCP resources for direct model consumption or embedding in prompts.  ￼
	2.	Prompts (parameterised “wizards”)
	•	scaffold_service, add_quality_gates, enable_storybook, enable_golangci.
	•	setup_offline_cache (wheelhouse / Yarn Zero-Installs).
Provide typed args; bind resources into prompt bodies.  ￼
	3.	Tools (idempotent, safe operations)
	•	list_templates() → from catalog.
	•	render_template(template_id, params) → run Cookiecutter; return zip or open PR via GitHub API.
	•	create_repo(name, visibility) → scaffold + push.
	•	add_workflows(set) → notebooks test/build, Pages/Storybook deploy, release packer.
	•	build_wheelhouse(reqs) / offline_install_plan(runtime) → Python cache; yarn_zero_installs() for Node.
	•	execute_notebook(name, params) → Papermill for setup notebooks.
These are MCP tools with JSON-schema args and typed results.  ￼

Architecture

Server
	•	Language/SDK: Python + FastMCP (thin, production-oriented) or official Python SDK; export tools/resources/prompts.  ￼
	•	Transports:
	•	Private track (default): STDIO for local Claude Desktop; optional SSE behind VPN for remote.  ￼
	•	Public-ready track: SSE endpoint behind OIDC/OAuth proxy, rate-limited.
	•	Integrations: GitHub (MCP GitHub server or native API), filesystem server (read-only), optional database servers later.  ￼

Clients
	•	Claude Desktop: Local server + Desktop Extension for one-click install and config.  ￼
	•	OpenAI Agents SDK: Configure your agent to connect to the MCP server; expose tools/resources in the app UI.  ￼
	•	Gemini CLI: Uses MCP via FastMCP integration (future-friendly).  ￼

Security model
	•	Least privilege by design: default read-only resources; tools that mutate must be explicitly enabled and are scoped (e.g., only target repos).  ￼
	•	Ephemeral auth: short-lived GitHub App installation tokens; no standing long-lived PATs.
	•	Isolation: run server in a locked container/namespace; deny shelling out except whitelisted CLIs; strict JSON-schema validation for tool args.
	•	Auditability: structured logs (stderr/file) per MCP guidance; persist per-call audit records.  ￼
	•	Threats to watch: identity fragmentation across tools; consolidate identity and minimise static secrets (industry commentary).  ￼

Ops & CI/CD
	•	Repo: /mcp/ package; Dockerfile with non-root user.
	•	Workflows:
	•	Build/test server; contract test MCP schema; publish container image.
	•	Release: package Desktop Extension for Claude; push Release assets (template zips, wheelhouse).  ￼
	•	SLOs: availability of SSE endpoint; P95 tool latency; error rate; mean time to revoke credentials.
	•	Monitoring: basic metrics + structured logs; alert on auth failures & tool timeouts.

Private vs Public tracks
	•	Private (default): local STDIO for Claude; remote SSE behind VPN; private GitHub Releases; private Pages or artifact-only for Storybook.  ￼
	•	Public-ready: flip repo/Release visibility; keep same MCP schemas; enable public Pages for Storybook; rate limit & add CAPTCHA for external UI if any.

Deliverables
	•	mcp/ Python package (FastMCP or official SDK), with:
	•	resources.py (bible, catalog, examples)
	•	prompts.py (wizards)
	•	tools.py (render_template, create_repo, add_workflows, build_wheelhouse, yarn_zero_installs, execute_notebook)
	•	desktop-extension/ for Claude one-click install (.dxt/.mcpb).  ￼
	•	mcp-config-examples/ for Claude/OpenAI/Gemini clients.  ￼
	•	CI: build/test, release assets, security scan of container.

Rollout plan (2 weeks → MVP)
	1.	Day 1–2: Decide SDK (FastMCP vs official), set repo layout, Dockerise.  ￼
	2.	Day 3–5: Implement resources (ac://catalog, ac://bible/*), list_templates()`.
	3.	Day 6–8: Implement render_template() (Cookiecutter), create_repo() (GitHub App).
	4.	Day 9–10: Add offline caches tools (wheelhouse builder; Yarn Zero-Installs), execute_notebook().
	5.	Day 11–12: Wire prompts (scaffold, gates, Storybook, Go lint).
	6.	Day 13–14: Package Desktop Extension; connect from Claude Desktop; add OpenAI Agents SDK example; write guardrail tests.  ￼

Risks & mitigations
	•	Credential sprawl: use GitHub App tokens + short TTL; central secret store.
	•	Tool misuse: schema validation; allowlists; human-in-the-loop for destructive ops.
	•	Client variance: keep to MCP spec primitives (tools/resources/prompts).  ￼

Interfaces (schemas, sketched)
	•	Tool: render_template
Args: { "template_id": "string", "params": { ... }, "delivery": "zip|pr" }
Result: { "artifact_uri": "ac://artifact/<id>" | "pr_url": "https://..." }
	•	Resource: ac://bible/quality-gates.md → text/markdown
	•	Prompt: scaffold_service(name, language, ci="github", storybook=true, golangci=false)

⸻

Benefits recap
	•	Single, standards-based control plane for your templates and generators; plug-and-play across Claude, OpenAI Agents, and Gemini.  ￼
	•	Reduces glue code; reuses official servers (filesystem, GitHub) and SDKs.  ￼
	•	Tightens governance: typed tools, auditable runs, controlled resources; aligns with your quality-and-security gates.

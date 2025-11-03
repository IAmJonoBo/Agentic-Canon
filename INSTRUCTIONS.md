# Instructions

Next: v1.1.0

Azure Pipelines
More dashboards
Additional examples
Video tutorials
Interactive wizard

Future: v2.0.0

Multi-cloud support
Advanced fitness functions
ML-powered insights
Full automation
Community templates

⸻

## 1. Repo layout (copy/paste)

notebooks/
01_bootstrap.ipynb
02_security_supply_chain.ipynb
03_contracts_and_tests.ipynb
04_observability_slos.ipynb
05_docs_to_book.ipynb

docs/
\_config.yml
\_toc.yml
intro.md
notebooks/ # MyST mirrors of ipynb via Jupytext pairing

binder/ # repo2docker/Binder env for reproducibility
requirements.txt

.pre-commit-config.yaml
jupytext.toml
.gitattributes
requirements.txt

.github/workflows/
notebooks-test.yml
book-deploy.yml
notebooks-schedule.yml

Why these pieces:
Why these pieces:
• Jupytext pairs ipynb ↔ md:myst so notebooks are Git-diffable and render in Jupyter Book. ￼
• nbmake/pytest executes notebooks in CI to catch breakage; Papermill parameterises and runs them on a schedule. ￼
• nbstripout keeps outputs out of Git; optional Jupytext pre-commit hook keeps pairs in sync. ￼
• GitHub Actions builds and deploys Jupyter Book to Pages and runs on cron. ￼
• repo2docker/Binder gives a reproducible, one-click environment (public repos).

⸻

## 2. Config files (drop these in)

jupytext.toml

### Pair notebooks to MyST Markdown in docs/notebooks for Jupyter Book

[formats]
"notebooks/" = "ipynb"
"docs/notebooks/" = "md:myst"

Jupytext supports global pairing and directory mapping like this. ￼

.gitattributes
Jupytext supports global pairing and directory mapping like this. ￼
.gitattributes

_.ipynb filter=nbstripout
_.ipynb diff=ipynb
.pre-commit-config.yaml

Official nbstripout filter usage. ￼
.pre-commit-config.yaml

repos: - id: nbstripout

- repo: https://github.com/mwouts/jupytext
  rev: v1.14.7
  hooks:
  - id: jupytext
    args: ["--sync"]

Enables output-stripping and ipynb↔MyST sync on commit. ￼

requirements.txt

jupyter
Enables output-stripping and ipynb↔MyST sync on commit. ￼
requirements.txt

jupyter
jupytext
nbstripout
pytest
nbmake
papermill
jupyter-book

• nbmake: pytest --nbmake \*_/_.ipynb. ￼
• Jupyter Book CLI for docs build. ￼
binder/requirements.txt

-r ../requirements.txt

Repo2Docker uses binder/ or .binder/ for env build.  
￼
⸻

## 3. Jupyter Book source

only_build_toc_files: true
repository:
url: https://github.com/<org-or-user>/agentic-canon
path_to_book: docs
execute:
execute_notebooks: "off" # CI runs notebooks; book consumes MyST outputs

Core Jupyter Book options come from \_config.yml. ￼

docs/\_toc.yml

format: jb-book
root: intro
chapters:

- file: notebooks/01_bootstrap
  file: notebooks/02_security_supply_chain
- file: notebooks/03_contracts_and_tests
- file: notebooks/04_observability_slos
- file: notebooks/05_docs_to_book

ToC layout and numbering follow Jupyter Book conventions. ￼

docs/intro.md

## Agentic Canon Bible

This book is the machine-readable, agent-friendly guide and templates for fast, correct scaffolding and delivery. See `notebooks/` for executable playbooks.

⸻

## 4. GitHub Actions workflows

.github/workflows/notebooks-test.yml

name: Notebooks • test
on:
pull\*request:
push:
branches: [main]
jobs:
nbmake:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-python@v5
with: { python-version: '3.11' } - run: pip install -r requirements.txt - name: Run notebooks with nbmake
run: pytest --nbmake notebooks/\*\*/\_.ipynb

nbmake runs notebooks via pytest; catches execution errors early. ￼

.github/workflows/book-deploy.yml

name: Jupyter Book • deploy
on:
push:
branches: [main]
permissions:
contents: write
jobs:
build-and-deploy:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-python@v5
with: { python-version: '3.11' } - run: pip install jupyter-book ghp-import - run: jupyter-book build docs - name: Publish to gh-pages
run: ghp-import -n -p -f docs/\_build/html
env:
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

Enable Settings → Pages → Source: GitHub Actions in the repo. Jupyter Book’s docs recommend Actions + gh-pages for deployment. ￼

.github/workflows/notebooks-schedule.yml

name: Notebooks • scheduled run
on:
schedule: - cron: "0 5 \* \* 1" # Mondays 05:00 UTC
workflow_dispatch:
jobs:
papermill:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-python@v5
with: { python-version: '3.11' } - run: pip install -r requirements.txt - name: Execute notebooks with parameters
run: |
mkdir -p artifacts
papermill notebooks/01_bootstrap.ipynb artifacts/01_bootstrap.out.ipynb -p run_mode ci
papermill notebooks/02_security_supply_chain.ipynb artifacts/02_security_supply_chain.out.ipynb -p run_mode ci - uses: actions/upload-artifact@v4
with: { name: notebook-outputs, path: artifacts }

Cron scheduling is supported via on: schedule with POSIX syntax. Papermill parameterises and executes notebooks headlessly. ￼

⸻

## 5. One-time setup

pip install -r requirements.txt
pre-commit install

### Create first pairs (if starting from ipynb):

jupytext --set-formats ipynb,md:myst notebooks/_.ipynb
jupytext --sync notebooks/_.ipynb

Pre-commit + Jupytext pairing keep .ipynb and .md in sync. ￼

⸻

## 6. Minimal notebook intents (agent-friendly)

• 01_bootstrap: scaffold repo, enable gates, generate SBOM/signing demo (parameter run_mode).
• 02_security_supply_chain: SAST/secret scan, SBOM & provenance walkthrough.
• 03_contracts_and_tests: generate OpenAPI/AsyncAPI; run contract + mutation test demo.
• 04_observability_slos: OpenTelemetry quickstart & SLO probes.
• 05_docs_to_book: Jupytext sync and Jupyter Book build driver.

(You can let Copilot draft cells; CI will enforce execution correctness.)

⸻

## 7. Copilot instructions (paste this task list in Chat)

You are Repo Scaffolder Copilot for “Agentic Canon”.

1. Create folders/files exactly as in the provided tree.
1. Write jupytext.toml that pairs notebooks/ (ipynb) -> docs/notebooks/ (md:myst).
1. Add .gitattributes and .pre-commit-config.yaml to strip outputs and sync pairs.
1. Add requirements.txt with jupyter, jupytext, nbstripout, pytest, nbmake, papermill, jupyter-book.
1. Create `docs/_config.yml`, `_toc.yml`, `intro.md` per Jupyter Book.
1. Add three workflows: notebooks-test.yml (pytest --nbmake), book-deploy.yml (jupyter-book build + ghp-import), notebooks-schedule.yml (papermill).
1. Generate 5 small, parameterised notebooks matching the names; include a top “Parameters” cell for papermill.
1. Run pre-commit install and output the commands I must execute locally.

Abide by Jupytext/Jupyter Book conventions; no outputs checked in; fail on CI errors.

⸻

## 8. Cookiecutter templates & CI

### 8.1 Templates layout (multi-template repo)

templates/
python-service/
cookiecutter.json
hooks/{pre_gen_project.py,post_gen_project.py}
{{cookiecutter.project_slug}}/
pyproject.toml
src/{{cookiecutter.pkg_name}}/**init**.py
tests/test_smoke.py
.pre-commit-config.yaml
.editorconfig
.gitignore
.github/workflows/{ci.yml,security.yml,docs.yml}
docs/\_config.yml docs/\_toc.yml docs/intro.md
notebooks/01_bootstrap.ipynb
node-service/
cookiecutter.json
hooks/{pre_gen_project.py,post_gen_project.py}
{{cookiecutter.project_slug}}/
package.json tsconfig.json src/index.ts tests/smoke.test.ts
.pre-commit-config.yaml .editorconfig .gitignore
.github/workflows/{ci.yml,security.yml}
react-webapp/
cookiecutter.json
hooks/{pre_gen_project.py,post_gen_project.py}
{{cookiecutter.project_slug}}/
package.json vite.config.ts src/App.tsx e2e/playwright.config.ts
.github/workflows/{ci.yml,accessibility.yml}
go-service/
cookiecutter.json
hooks/{pre_gen_project.py,post_gen_project.py}
{{cookiecutter.project_slug}}/
go.mod cmd/app/main.go internal/app/app.go Makefile
.github/workflows/{ci.yml,security.yml}
docs-only/
cookiecutter.json
hooks/post_gen_project.py
{{cookiecutter.project_slug}}/
docs/\_config.yml docs/\_toc.yml docs/intro.md
tests/
test_cookiecutters.py

Why this structure: Cookiecutter supports multiple templates in one repo; callers pick via --directory. Hooks enable validation and post-scaffold steps. ￼

⸻

### 8.2 Minimal cookiecutter.json (Python flavour)

{
"project_name": "Acme Service",
"project_slug": "acme-service",
"pkg_name": "acme_service",
"license": ["Apache-2.0", "MIT", "Proprietary"],
"include_jupyter_book": ["yes", "no"],
"enable_security_gates": ["yes", "no"],
"enable_sbom_signing": ["yes", "no"],
"enable_contract_tests": ["yes", "no"],
"ci_provider": ["github", "gitlab"],
"\_copy_without_render": ["docs/_build", "notebooks/*.ipynb"]
}

⸻

### 8.3 Hooks (validation + safe bootstrap)

templates/python-service/hooks/pre_gen_project.py

import re, sys, json
slug = "{{ cookiecutter.project_slug }}"
pkg = "{{ cookiecutter.pkg_name }}"
if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)_$", slug):
sys.exit("project*slug must be kebab-case: [a-z0-9-].")
if not re.match(r"^[a-z*][a-z0-9_]\_$", pkg):
sys.exit("pkg_name must be a valid Python identifier (snake_case).")

templates/python-service/hooks/post_gen_project.py

import json, os, subprocess, sys, pathlib
cc = {
"book": "{{ cookiecutter.include_jupyter_book }}",
"sec": "{{ cookiecutter.enable_security_gates }}",
"sbom":"{{ cookiecutter.enable_sbom_signing }}",
"contract":"{{ cookiecutter.enable_contract_tests }}"
}
root = pathlib.Path(".")
def rm(\*paths):
for p in paths:
q = root / p
if q.exists():
(q.is_dir() and **import**("shutil").rmtree(q)) or q.unlink()

if cc["book"] == "no":
rm("docs/\_config.yml","docs/\_toc.yml","docs/intro.md")
if cc["sec"] == "no":
rm(".github/workflows/security.yml")
if cc["sbom"] == "no":
rm(".github/workflows/security.yml")
if cc["contract"] == "no":
rm("tests/contract")

subprocess.run(["git","init","-q"], check=False)
print("Next: create venv, pre-commit install, push to empty repo.")

Hooks are the official way to validate inputs and perform post-render cleanup/initialisation. ￼

⸻

### 8.4 CI to test the templates (cookiecutters must render)

tests/test_cookiecutters.py

import pytest
def test_python_cookiecutter_bakes(cookies):
result = cookies.bake(extra_context={
"project_name":"Demo Service",
"project_slug":"demo-service",
"pkg_name":"demo_service",
"include_jupyter_book":"yes",
"enable_security_gates":"yes",
"enable_sbom_signing":"yes",
"enable_contract_tests":"yes",
"license":"Apache-2.0",
"ci_provider":"github"
}, template="templates/python-service")
assert result.exception is None
assert (result.project_path / "pyproject.toml").exists()

pytest-cookies provides the cookies fixture that renders templates and cleans up. ￼

.github/workflows/cookiecutters-test.yml

name: Cookiecutters • render test
on: [push, pull_request]
jobs:
bake:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-python@v5
with: { python-version: '3.11' } - run: pip install cookiecutter pytest pytest-cookies - run: pytest -q

⸻

### 8.5 Keep downstream projects in sync (optional but gold)

Recommend Cruft so generated projects can check or pull template updates:
• In the template README: show cruft create gh:<org>/agentic-canon --directory templates/python-service.
• In generated projects: add a workflow running cruft check weekly. Cruft is designed to track and update Cookiecutter renderings. ￼

⸻

### 8.6 Example CI files embedded in templates

templates/python-service/{{cookiecutter.project_slug}}/.github/workflows/ci.yml

name: CI
on: { push: { branches: [main] }, pull\*request: {} }
jobs:
build:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-python@v5
with: { python-version: '3.12' } - run: pip install -U pip wheel - run: pip install -e .[dev] - run: pip install pytest pytest-cov nbmake - run: pytest --nbmake notebooks/\*\*/\_.ipynb -q

(Your security/SBOM/signing jobs from the master brief remain as separate workflow files and are toggled by the cookiecutter options.)

⸻

### 8.7 Usage (devs and agents)

• Local render, choosing a flavour:

cookiecutter gh:<org-or-user>/agentic-canon --directory templates/python-service

--directory selects a sub-template from the repository. ￼

• Test your cookiecutters before publishing: pytest -q (runs pytest-cookies). ￼
• Keep projects updated: cruft check / cruft update. ￼

⸻

### 8.8 Tiny Copilot brief (paste into Chat)

Repo task: Add Cookiecutter multi-templates under /templates (python-service, node-service, react-webapp, go-service, docs-only). Each has cookiecutter.json, hooks, and CI workflows. Add tests/test_cookiecutters.py using pytest-cookies; add cookiecutters-test.yml to render on PRs. Document usage with cookiecutter --directory and Cruft sync. No outputs in Git, hooks validate slugs.

⸻

### 8.9 Why these choices (quick evidence)

• Multi-template repos and the --directory flag are first-class in Cookiecutter. ￼
• Hooks are the supported mechanism for validation and post-render actions. ￼
• pytest-cookies is the de-facto way to test cookiecutters in CI. ￼
• Cruft fills Cookiecutter’s update gap, enabling “template drift” checks and updates. ￼

Absolutely. Here are ready-to-drop Cookiecutter files for the three extra templates so a fresh render “just works” and turns green in CI.

⸻

templates/node-service/{{cookiecutter.project_slug}}

package.json

{
"name": "{{cookiecutter.project_slug}}",
"version": "0.1.0",
"type": "module",
"main": "dist/index.js",
"types": "dist/index.d.ts",
"scripts": {
"dev": "tsx watch src/index.ts",
"build": "tsc -p tsconfig.json",
"test": "vitest run --coverage",
"start": "node dist/index.js",
"lint": "eslint .",
"format": "prettier -w ."
},
"devDependencies": {
"@tsconfig/node20": "_",
"@types/node": "_",
"typescript": "_",
"tsx": "_",
"vitest": "_",
"eslint": "_",
"prettier": "\*"
}
}

tsconfig.json

{
"extends": "@tsconfig/node20/tsconfig.json",
"compilerOptions": {
"rootDir": "src",
"outDir": "dist",
"moduleResolution": "bundler",
"resolveJsonModule": true,
"declaration": true,
"sourceMap": true,
"strict": true
},
"include": ["src", "tests"]
}

src/index.ts

export function ping(): string { return "pong"; }
if (import.meta.main) console.log(ping());

tests/smoke.test.ts

import { expect, test } from "vitest";
import { ping } from "../src/index";
test("ping", () => { expect(ping()).toBe("pong"); });

README.md (snippet)
Use Node 20+, extend @tsconfig/node20, and run via tsx in dev; compile with tsc for prod. ￼

⸻

templates/react-webapp/{{cookiecutter.project_slug}}

package.json

{
"name": "{{cookiecutter.project_slug}}",
"private": true,
"version": "0.1.0",
"type": "module",
"scripts": {
"dev": "vite",
"build": "vite build",
"preview": "vite preview",
"test": "vitest",
"test:e2e": "playwright test"
},
"dependencies": {
"react": "_",
"react-dom": "_"
},
"devDependencies": {
"@types/react": "_",
"@types/react-dom": "_",
"@vitejs/plugin-react-swc": "_",
"typescript": "_",
"vite": "_",
"vitest": "_",
"@playwright/test": "\*"
}
}

vite.config.ts

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
plugins: [react()]
});

tsconfig.json

{
"compilerOptions": {
"target": "ES2020",
"useDefineForClassFields": true,
"lib": ["ES2020", "DOM", "DOM.Iterable"],
"module": "ESNext",
"skipLibCheck": true,
"moduleResolution": "bundler",
"resolveJsonModule": true,
"isolatedModules": true,
"noEmit": true,
"jsx": "react-jsx",
"strict": true
},
"include": ["src", "vite.config.ts"]
}

src/App.tsx

export default function App() {
return <main style={{ padding: 24 }}><h1>It works 🚀</h1></main>;
}

src/main.tsx

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
createRoot(document.getElementById("root")!).render(<React.StrictMode><App/></React.StrictMode>);

index.html

<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{{cookiecutter.project_slug}}</title></head>
<body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>

playwright.config.ts

import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
testDir: "./tests/e2e",
timeout: 2 _ 60 _ 1000,
use: { baseURL: "http://localhost:5173/" },
webServer: {
command: "npm run dev",
url: "http://localhost:5173",
reuseExistingServer: !process.env.CI,
timeout: 120000
},
projects: [
{ name: "chromium", use: { ...devices["Desktop Chrome"] } },
{ name: "firefox", use: { ...devices["Desktop Firefox"] } },
{ name: "webkit", use: { ...devices["Desktop Safari"] } }
]
});

tests/e2e/smoke.spec.ts

import { expect, test } from "@playwright/test";
test("home loads", async ({ page }) => {
await page.goto("/");
await expect(page.locator("h1")).toHaveText(/It works/);
});

Rationale: Vite’s React+TS template conventions; Playwright config with webServer and multi-browser projects; GitHub Actions recipes exist if you want CI for E2E. ￼

⸻

templates/go-service/{{cookiecutter.project_slug}}

go.mod

module {{cookiecutter.module_path}}

go 1.22

cmd/app/main.go

package main

import (
"fmt"
)

func main() {
fmt.Println(Ping())
}

internal/app/app.go

package main

func Ping() string { return "pong" }

internal/app/app_test.go

package main

import "testing"

func TestPing(t \*testing.T) {
if Ping() != "pong" { t.Fatal("expected pong") }
}

Makefile

APP={{cookiecutter.project_slug}}

.PHONY: build run test tidy
build: ## Compile binaries
go build -o bin/$(APP) ./cmd/app
run: build ## Run app
 ./bin/$(APP)
test: ## Unit tests
go test ./...
tidy: ## Sync modules
go mod tidy

Rationale: go mod init generates go.mod; keep modules tidy and tests simple; official docs explain module semantics. ￼

⸻

How to render (for devs or agents)

## Pick a template by directory

cookiecutter gh:<org-or-user>/agentic-canon --directory templates/node-service
cookiecutter gh:<org-or-user>/agentic-canon --directory templates/react-webapp
cookiecutter gh:<org-or-user>/agentic-canon --directory templates/go-service

• --directory selects a sub-template in a multi-template repo (first-class feature). Test your cookiecutters with pytest-cookies. Keep projects in sync with Cruft (cruft check / cruft update). ￼

⸻

Optional CI seeds (drop-in)

Node (unit tests & build)

## .github/workflows/node-ci.yml

name: Node • CI
on: { push: { branches: [main] }, pull_request: {} }
jobs:
ci:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-node@v4
with: { node-version: '20', cache: 'npm' } - run: npm ci - run: npm run -s build - run: npm test

Using actions/setup-node is the recommended path for Node on Actions. ￼

Playwright E2E (webapp)

name: Webapp • E2E
on: [push, pull_request]
jobs:
e2e:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-node@v4
with: { node-version: '20', cache: 'npm' } - run: npm ci - name: Install Playwright deps
run: npx playwright install --with-deps - run: npm run test:e2e

Aligned with Playwright’s CI guidance and official action. ￼

⸻

Copilot task (paste this in Chat for automation)

Repo task: add Cookiecutter sub-templates for node-service, react-webapp (Vite+TS+Playwright), and go-service. Use files shown above verbatim. Ensure Node uses @tsconfig/node20 and tsx; React uses @vitejs/plugin-react-swc and Playwright config with webServer; Go has go.mod 1.22 and Makefile. Add CI seeds (node-ci.yml, webapp-e2e.yml). Output the exact changes as diffs.

⸻

Absolutely—here are drop-in additions to wire Storybook into the react-webapp template and golangci-lint into the go-service template, plus minimal CI. I’ve kept it terse and copy-pasteable.

⸻

React webapp → Storybook (+ a11y, Vite builder)

## 8.6.1 package.json (add scripts & devDeps)

templates/react-webapp/{{cookiecutter.project_slug}}/package.json

{
"scripts": {
"storybook": "storybook dev -p 6006",
"build-storybook": "storybook build"
},
"devDependencies": {
"@storybook/react-vite": "_",
"@storybook/addon-essentials": "_",
"@storybook/addon-a11y": "\*"
}
}

• Uses the React+Vite framework; a11y addon runs axe-core checks in the UI. ￼

### 8.6.2 Storybook config

Create: templates/react-webapp/{{cookiecutter.project_slug}}/.storybook/main.ts

import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
framework: { name: '@storybook/react-vite', options: {} },
stories: ['../src/**/*.stories.@(ts|tsx)'],
addons: ['@storybook/addon-essentials', '@storybook/addon-a11y']
};
export default config;

Create: templates/react-webapp/{{cookiecutter.project_slug}}/.storybook/preview.ts

import type { Preview } from '@storybook/react';

const preview: Preview = {
parameters: {
actions: { argTypesRegex: '^on[A-Z].\*' },
controls: { matchers: { color: /(background|color)$/i, date: /Date$/ } }
}
};
export default preview;

• Vite builder defaults live in Storybook; keep tweaks in vite.config.ts. ￼

#### 8.6.3 Example component + story

Create: templates/react-webapp/{{cookiecutter.project_slug}}/src/components/Button.tsx

type Props = { label: string; primary?: boolean } & React.ButtonHTMLAttributes<HTMLButtonElement>;
export function Button({ label, primary, ...rest }: Props) {
return <button {...rest} data-variant={primary ? 'primary' : 'default'}>{label}</button>;
}

Create: templates/react-webapp/{{cookiecutter.project_slug}}/src/components/Button.stories.tsx

import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = { title: 'Core/Button', component: Button };
export default meta;
type Story = StoryObj<typeof Button>;
export const Primary: Story = { args: { label: 'It works', primary: true } };
export const Default: Story = { args: { label: 'Hello' } };

• Type-safe stories are first-class. ￼

#### 8.6.4 CI: build Storybook (artifact)

Create: templates/react-webapp/{{cookiecutter.project_slug}}/.github/workflows/storybook-build.yml

name: Storybook • build
on: [push, pull_request]
jobs:
build:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-node@v4
with: { node-version: '20', cache: 'npm' } - run: npm ci - run: npm run build-storybook - uses: actions/upload-artifact@v4
with: { name: storybook-static, path: storybook-static }

• Uses storybook build CLI; you can swap in a Pages deploy later if you wish. ￼

Optional testing hooks
Add Test Runner to turn stories into Playwright-backed tests in CI: @storybook/test-runner and run test-storybook. ￼

⸻

Go service → golangci-lint (config + CI)

#### 8.6.5 Linter config

Create: templates/go-service/{{cookiecutter.project_slug}}/.golangci.yml

run:
timeout: 3m
tests: true
linters:
enable: - govet - staticcheck - gosimple - ineffassign - errcheck - revive - gocritic - unused
issues:
exclude-use-default: false
max-issues-per-linter: 0
max-same-issues: 0
new-from-rev: HEAD~1

• YAML config at .golangci.yml is auto-discovered; enabled set favours high-signal linters. Tune as needed. ￼

Create: templates/go-service/{{cookiecutter.project_slug}}/.github/workflows/go-lint.yml

name: Go • lint
on: [push, pull_request]
permissions: { contents: read }
jobs:
golangci:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v5 - uses: actions/setup-go@v6
with: { go-version: stable } - name: golangci-lint
uses: golangci/golangci-lint-action@v8
with:
version: v2.1

• Official action; v8 action targets golangci-lint ≥ v2.1 and provides annotations/caching. ￼

#### 8.6.7 Makefile (optional convenience)

Add to the existing Makefile:

lint:
golangci-lint run

• golangci-lint is the standard multi-linter for Go. ￼

⸻

Copilot task (paste to Chat to auto-insert)

Repo task: in templates/react-webapp add Storybook (React+Vite). Update package.json (storybook scripts, devDeps), add .storybook/{main.ts,preview.ts}, add Button.tsx + Button.stories.tsx, and .github/workflows/storybook-build.yml that builds and uploads artifact. In templates/go-service add .golangci.yml and .github/workflows/go-lint.yml using golangci-lint-action@v8 (version v2.1). Keep diffs small; no breaking changes.

Why this wiring
• Storybook React-Vite is the official path; put tweaks in Vite config; add a11y addon for WCAG checks. ￼
• golangci-lint action is the recommended way to run many linters quickly with cache/annotations. ￼

⸻

Absolutely—here’s a drop-in GitHub Pages deploy for the react-webapp Cookiecutter template, using GitHub’s official Pages actions.

Files to add (react-webapp template)

.github/workflows/storybook-pages.yml

name: Storybook • Pages
on:
push:
branches: [main]
workflow_dispatch:

# Required for Pages deployments

permissions:
contents: read
pages: write
id-token: write

# Avoid overlapping deploys

concurrency:
group: pages-storybook
cancel-in-progress: true

jobs:
build:
runs-on: ubuntu-latest
steps: - uses: actions/checkout@v4 - uses: actions/setup-node@v4
with: { node-version: '20', cache: 'npm' } - run: npm ci - run: npm run build-storybook # outputs ./storybook-static - name: Upload Pages artifact
uses: actions/upload-pages-artifact@v3
with:
path: storybook-static
deploy:
needs: build
runs-on: ubuntu-latest
environment:
name: github-pages
url: ${{ steps.deployment.outputs.page_url }}
steps: - name: Deploy to GitHub Pages
id: deployment
uses: actions/deploy-pages@v4

Repo setting (one-time): in Settings → Pages → Build and deployment, set Source: GitHub Actions. Deploy URL will surface from the job output (page_url). ￼

Why this wiring
• build → upload → deploy is the pattern GitHub recommends: build the static site, upload with actions/upload-pages-artifact, then deploy with actions/deploy-pages (with pages: write and id-token: write). ￼
• Storybook’s static export lands in storybook-static by default, which is exactly what we publish. ￼
• Optional concurrency prevents overlapping Page releases during busy commit streams. ￼

Copilot task (paste to Chat)

Add .github/workflows/storybook-pages.yml to the react-webapp template exactly as provided. Ensure npm run build-storybook is used, upload with actions/upload-pages-artifact@v3 (path: storybook-static), then deploy with actions/deploy-pages@v4. Remind me to set Settings→Pages→Source: GitHub Actions and return the expected public URL from the job output.

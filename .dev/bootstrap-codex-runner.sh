#!/usr/bin/env bash
# Provision an ephemeral Codex runner with all required tooling.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$REPO_ROOT"

python3 -m venv .venv
source .venv/bin/activate

SAFE_PIP_SPEC="pip @ git+https://github.com/pypa/pip@f2b92314da012b9fffa36b3f3e67748a37ef464a"
# GHSA-4xh5-x5gv-qwph: rely on patched pip commit until 25.3 lands.
# Keep this value in sync with agentic_canon_cli/cli.py::SAFE_PIP_SPEC.
pip install --upgrade "${SAFE_PIP_SPEC}"
pip install -r requirements.txt

if ! command -v trunk >/dev/null 2>&1; then
	curl -fsSL https://get.trunk.io -o /tmp/install-trunk.sh
	bash /tmp/install-trunk.sh -y
	rm -f /tmp/install-trunk.sh
	export PATH="$HOME/.trunk/bin:$PATH"
fi

.dev/trunk-with-progress.sh upgrade

deactivate

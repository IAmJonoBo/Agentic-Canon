#!/usr/bin/env bash
# Template validation orchestrator for Agentic Canon
#
# Provides a thin wrapper around Nox sessions so local developers, CI, and
# sanity-check tooling can share a single entry point.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

usage() {
	cat <<'EOF'
Usage: .dev/validate-templates.sh [options]

Options:
  --all              Run full validation (sync + render + lint + format)
  --linters           Run lint-only validation (render + lint_templates)
  --format            Run formatting validation (render + format_templates)
  --upgrade           Run upgrade_tools session
  --template NAME     Limit validation to a specific template (repeatable)
  --force-rebuild     Rebuild template render caches
  --help              Show this message

Without --linters/--format/--upgrade the script runs render + lint + format.
EOF
}

declare -a TEMPLATES=()
RUN_LINTERS=0
RUN_FORMAT=0
RUN_UPGRADE=0
RUN_ALL=0
FORCE_REBUILD=0

while [[ $# -gt 0 ]]; do
	case "$1" in
	--all)
		RUN_ALL=1
		shift
		;;
	--linters)
		RUN_LINTERS=1
		shift
		;;
	--format)
		RUN_FORMAT=1
		shift
		;;
	--upgrade)
		RUN_UPGRADE=1
		shift
		;;
	--force-rebuild)
		FORCE_REBUILD=1
		shift
		;;
	--template)
		if [[ $# -lt 2 ]]; then
			echo "error: --template requires a value" >&2
			exit 1
		fi
		TEMPLATES+=("$2")
		shift 2
		;;
	--help | -h)
		usage
		exit 0
		;;
	*)
		echo "error: unknown option '$1'" >&2
		echo "" >&2
		usage >&2
		exit 1
		;;
	esac
done

if [[ ${RUN_ALL} -eq 1 ]]; then
	RUN_LINTERS=0
	RUN_FORMAT=0
fi

if [[ ${RUN_LINTERS} -eq 0 && ${RUN_FORMAT} -eq 0 && ${RUN_UPGRADE} -eq 0 && ${RUN_ALL} -eq 0 ]]; then
	RUN_ALL=1
fi

declare -a NOX_ARGS=()
if ((${#TEMPLATES[@]})); then
	for template in "${TEMPLATES[@]}"; do
		NOX_ARGS+=("--template" "${template}")
	done
fi
if [[ ${FORCE_REBUILD} -eq 1 ]]; then
	NOX_ARGS+=("--force")
fi

run_nox() {
	local session="$1"
	shift
	echo "🔧 Running nox -s ${session} -- $*"
	(
		cd "${REPO_ROOT}"
		if [[ $# -eq 0 ]]; then
			nox -s "${session}"
		else
			nox -s "${session}" -- "$@"
		fi
	)
}

# Unified validation pipeline (sync + render + lint + format).
if [[ ${RUN_ALL} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox validate_templates_all "${NOX_ARGS[@]}"
	else
		run_nox validate_templates_all
	fi
fi

# Legacy flows retained for targeted runs.
if [[ ${RUN_LINTERS} -eq 1 || ${RUN_FORMAT} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox render_templates "${NOX_ARGS[@]}"
	else
		run_nox render_templates
	fi
fi

if [[ ${RUN_LINTERS} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox lint_templates "${NOX_ARGS[@]}"
	else
		run_nox lint_templates
	fi
fi

if [[ ${RUN_FORMAT} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox format_templates "${NOX_ARGS[@]}"
	else
		run_nox format_templates
	fi
fi

if [[ ${RUN_UPGRADE} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox upgrade_tools "${NOX_ARGS[@]}"
	else
		run_nox upgrade_tools
	fi
fi

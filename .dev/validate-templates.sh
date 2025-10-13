#!/usr/bin/env bash
# Template validation orchestrator for Agentic Canon
#
# Provides a thin wrapper around Nox sessions so local developers, CI, and
# sanity-check tooling can share a single entry point.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
TEMPLATES_DIR="${REPO_ROOT}/templates"

ensure_pythonpath() {
	local -a path_list=()
	local entry existing
	local updated=0

	if [[ -n ${PYTHONPATH-} ]]; then
		IFS=":" read -r -a path_list <<<"${PYTHONPATH}"
	fi

	for entry in "$@"; do
		local found=0
		for existing in "${path_list[@]}"; do
			if [[ ${existing} == "${entry}" ]]; then
				found=1
				break
			fi
		done
		if [[ ${found} -eq 0 ]]; then
			path_list=("${entry}" "${path_list[@]}")
			updated=1
		fi
	done

	if [[ ${updated} -eq 1 || -z ${PYTHONPATH-} ]]; then
		PYTHONPATH=$(
			IFS=":"
			echo "${path_list[*]}"
		)
	fi

	export PYTHONPATH
}

ensure_pythonpath "${REPO_ROOT}" "${TEMPLATES_DIR}"

usage() {
	cat <<'EOF'
Usage: .dev/validate-templates.sh [options]

Options:
  --all              Run full validation (sync + render + lint + type + security + format)
  --linters           Run lint-only validation (render + lint_templates)
  --type              Run type-check validation (render + type_templates)
  --security          Run security validation (render + security_templates)
  --format            Run formatting validation (render + format_templates)
  --upgrade           Run upgrade_tools session
  --template NAME     Limit validation to a specific template (repeatable)
  --force-rebuild     Rebuild template render caches
  --quiet             Reduce console noise while still surfacing failures
  --skip-safe-pip     Do not upgrade pip to the patched GHSA build
  --help              Show this message

Environment:
  AGENTIC_CANON_SKIP_SAFE_PIP   Skip pip upgrade even when --skip-safe-pip is not set
  AGENTIC_CANON_SAFE_PIP_SPEC   Override the pip spec used for the upgrade command

Without explicit mode flags the script runs the unified sync -> render -> lint -> format pipeline.
EOF
}

declare -a TEMPLATES=()
RUN_LINTERS=0
RUN_TYPE=0
RUN_SECURITY=0
RUN_FORMAT=0
RUN_UPGRADE=0
RUN_ALL=0
FORCE_REBUILD=0
QUIET=0
SKIP_SAFE_PIP=0

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
	--type)
		RUN_TYPE=1
		shift
		;;
	--security)
		RUN_SECURITY=1
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
        --quiet)
                QUIET=1
                shift
                ;;
        --skip-safe-pip)
                SKIP_SAFE_PIP=1
                shift
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
        RUN_TYPE=0
        RUN_SECURITY=0
        RUN_FORMAT=0
fi

if [[ ${SKIP_SAFE_PIP} -eq 0 && -n ${AGENTIC_CANON_SKIP_SAFE_PIP-} ]]; then
        case "${AGENTIC_CANON_SKIP_SAFE_PIP,,}" in
        1 | true | yes | y | on)
                SKIP_SAFE_PIP=1
                if [[ ${QUIET} -eq 0 ]]; then
                        echo "⚠️  Skipping pip upgrade via AGENTIC_CANON_SKIP_SAFE_PIP"
                fi
                ;;
        esac
fi

if [[ ${RUN_LINTERS} -eq 0 && ${RUN_TYPE} -eq 0 && ${RUN_SECURITY} -eq 0 && ${RUN_FORMAT} -eq 0 && ${RUN_UPGRADE} -eq 0 && ${RUN_ALL} -eq 0 ]]; then
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

if [[ ${SKIP_SAFE_PIP} -eq 0 ]]; then
        if [[ ${QUIET} -eq 0 ]]; then
                echo "🛡️ Ensuring pip includes GHSA-4xh5-x5gv-qwph patch"
        fi
        if [[ ${QUIET} -eq 1 ]]; then
                python -m agentic_canon_cli.pip_support --quiet >/dev/null
        else
                python -m agentic_canon_cli.pip_support
        fi
        if [[ $? -ne 0 ]]; then
                echo "error: unable to upgrade pip to patched build" >&2
                exit 1
        fi
fi

run_nox() {
        local session="$1"
        shift
        if [[ ${QUIET} -eq 0 ]]; then
                echo "🔧 Running nox -s ${session} -- $*"
	fi
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
if [[ ${RUN_LINTERS} -eq 1 || ${RUN_TYPE} -eq 1 || ${RUN_SECURITY} -eq 1 || ${RUN_FORMAT} -eq 1 ]]; then
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

if [[ ${RUN_TYPE} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox type_templates "${NOX_ARGS[@]}"
	else
		run_nox type_templates
	fi
fi

if [[ ${RUN_SECURITY} -eq 1 ]]; then
	if ((${#NOX_ARGS[@]})); then
		run_nox security_templates "${NOX_ARGS[@]}"
	else
		run_nox security_templates
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

#!/usr/bin/env bash
# Progress indicator wrapper for trunk commands with robust cleanup + TTY-aware spinner
# Usage: .dev/trunk-with-progress.sh <trunk-command> [args...]

set -euo pipefail

if [[ $# -eq 0 ]]; then
	echo "Usage: $0 <trunk-command> [args...]"
	echo "Example: $0 check --all"
	echo "Example: $0 fmt --all"
	exit 1
fi

COMMAND="$1"
shift

TEMP_OUTPUT=$(mktemp)
SPINNER_PID=""
CURSOR_HIDDEN=0

cleanup() {
	local exit_status=$1
	if [[ -n ${SPINNER_PID-} ]] && kill -0 "${SPINNER_PID}" 2>/dev/null; then
		kill "${SPINNER_PID}" 2>/dev/null || true
		wait "${SPINNER_PID}" 2>/dev/null || true
	fi
	if ((CURSOR_HIDDEN)); then
		echo -ne "\033[?25h"
		CURSOR_HIDDEN=0
	fi
	rm -f "${TEMP_OUTPUT}"
	return "${exit_status}"
}
trap 'cleanup $?' EXIT

supports_color() {
	[[ -t 1 ]] || return 1
	local term="${TERM-}"
	[[ -n ${term} && ${term} != "dumb" ]]
}

if supports_color; then
	GREEN='\033[0;32m'
	YELLOW='\033[1;33m'
	BLUE='\033[0;34m'
	RED='\033[0;31m'
	NC='\033[0m'
else
	GREEN=''
	YELLOW=''
	BLUE=''
	RED=''
	NC=''
fi

echo -e "${BLUE}🔍 Running: trunk ${COMMAND} $*${NC}"
[[ -t 1 ]] && echo -e "${YELLOW}⏳ This may take a moment...${NC}"

trunk "${COMMAND}" "$@" >"${TEMP_OUTPUT}" 2>&1 &
TRUNK_PID=$!

spinner() {
	local frames=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
	local i=0
	while kill -0 "${TRUNK_PID}" 2>/dev/null; do
		local frame=${frames[i % ${#frames[@]}]}
		echo -ne "\r${YELLOW}${frame}${NC} Working..."
		sleep 0.1
		((i++))
	done
	echo -ne "\r                \r"
}

if [[ -t 1 ]]; then
	echo -ne "\033[?25l"
	CURSOR_HIDDEN=1
	spinner &
	SPINNER_PID=$!
fi

set +e
wait "${TRUNK_PID}"
RESULT=$?
set -e

if [[ -n ${SPINNER_PID-} ]]; then
	wait "${SPINNER_PID}" 2>/dev/null || true
fi

if ((CURSOR_HIDDEN)); then
	echo -ne "\033[?25h"
	CURSOR_HIDDEN=0
fi

if [[ ${RESULT} -eq 0 ]]; then
	echo -e "${GREEN}✅ trunk ${COMMAND} completed successfully${NC}"
else
	echo -e "${RED}❌ trunk ${COMMAND} failed (exit code: ${RESULT})${NC}"
fi

cat "${TEMP_OUTPUT}"

exit "${RESULT}"

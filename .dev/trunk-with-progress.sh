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

supports_color() {
	[[ -t 1 ]] || return 1
	local term="${TERM-}"
	[[ -n ${term} && ${term} != "dumb" ]]
}

supports_color_result=1
if supports_color; then
	supports_color_result=0
fi

if [[ $supports_color_result -eq 0 ]]; then
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

restore_cursor() {
	if [[ -t 1 ]]; then
		echo -ne "\033[?25h"
		CURSOR_SHOWN=1
	fi
}

trap cleanup EXIT

echo -e "${BLUE}🔍 Running: trunk ${COMMAND} $*${NC}"
[[ -t 1 ]] && echo -e "${YELLOW}⏳ This may take a moment...${NC}"

trunk "${COMMAND}" "$@" >"${TEMP_OUTPUT}" 2>&1 &
TRUNK_PID=$!

if [[ -t 1 ]]; then
	echo -ne "\033[?25l"
	SPINNER_FRAMES=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
	spinner() {
		local i=0
		while kill -0 "${TRUNK_PID}" 2>/dev/null; do
			local frame=${SPINNER_FRAMES[i % ${#SPINNER_FRAMES[@]}]}
			echo -ne "\r${YELLOW}${frame}${NC} Working..."
			sleep 0.1
			((i++))
		done
		echo -ne "\r                \r"
	}
	spinner &
	SPINNER_PID=$!
fi

wait "${TRUNK_PID}"
RESULT=$?

restore_cursor

if [[ ${RESULT} -eq 0 ]]; then
	echo -e "${GREEN}✅ trunk ${COMMAND} completed successfully${NC}"
else
	echo -e "${RED}❌ trunk ${COMMAND} failed (exit code: ${RESULT})${NC}"
fi

cat "${TEMP_OUTPUT}"

exit "${RESULT}"

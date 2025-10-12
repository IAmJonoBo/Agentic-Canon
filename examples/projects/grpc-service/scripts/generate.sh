#!/usr/bin/env bash
set -euo pipefail

PATH="$HOME/go/bin:$PATH"

buf dep update
buf generate

go mod tidy

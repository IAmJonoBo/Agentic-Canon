#!/usr/bin/env bash
set -euo pipefail

GO_TEST_FLAGS=${GO_TEST_FLAGS-}

go test ./... $GO_TEST_FLAGS

SHELL := /bin/bash
MODULE := github.com/agentic-canon/examples/grpc-service
BIN_DIR := bin

.PHONY: all proto tidy build run test lint cover clean

all: build

proto:
	@echo "Generating gRPC code with Buf"
	@PATH="$$HOME/go/bin:$$PATH" buf generate api/proto

build:
	@echo "Building gRPC server"
	@mkdir -p $(BIN_DIR)
	@go build -o $(BIN_DIR)/grpc-service ./cmd/server

run:
	@go run ./cmd/server

lint:
	@PATH="$$HOME/go/bin:$$PATH" golangci-lint run

test:
	@go test ./...

cover:
	@go test ./... -coverprofile=coverage.out && go tool cover -html=coverage.out

clean:
	@rm -rf $(BIN_DIR)
	@rm -f coverage.out

APP={{cookiecutter.project_slug}}
BIN=bin/$(APP)

.PHONY: help build run test lint tidy clean

help: ## Show this help
@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build the application
@echo "Building $(APP)..."
@go build -o $(BIN) ./cmd/app
@echo "✓ Built $(BIN)"

run: build ## Run the application
@echo "Running $(APP)..."
@./$(BIN)

test: ## Run tests
@echo "Running tests..."
@go test -v -race -cover ./...

lint: ## Run linters
@echo "Running linters..."
@golangci-lint run || echo "golangci-lint not found, install it from https://golangci-lint.run/"

tidy: ## Tidy Go modules
@echo "Tidying modules..."
@go mod tidy
@go mod verify

clean: ## Clean build artifacts
@echo "Cleaning..."
@rm -rf bin/
@echo "✓ Cleaned"

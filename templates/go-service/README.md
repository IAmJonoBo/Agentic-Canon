# Go Service Cookiecutter Template

Production-ready Go service template with best practices, comprehensive testing, and security tooling.

## Quick Start

```bash
# Using Cookiecutter
cookiecutter templates/go-service

# Or using Agentic Canon CLI
agentic-canon init
# Select "Go Service" when prompted
```

## Features

### Core Capabilities

- ✅ **Modern Go** - Go 1.22+ with generics
- ✅ **Clean Architecture** - `cmd/` and `internal/` structure
- ✅ **Testing** - Table-driven tests with testify
- ✅ **Linting** - golangci-lint with comprehensive rules
- ✅ **Formatting** - gofmt + goimports
- ✅ **Makefile** - Build automation

### CI/CD

- ✅ **GitHub Actions** - Complete CI/CD pipeline
- ✅ **GitLab CI** - Alternative CI/CD support
- ✅ **Multi-version Testing** - Go 1.21, 1.22, 1.23
- ✅ **Cross-compilation** - Linux, macOS, Windows
- ✅ **Docker Support** - Multi-stage builds

### Security

- ✅ **CodeQL Analysis** - Go SAST
- ✅ **Semgrep** - Pattern-based scanning
- ✅ **govulncheck** - Vulnerability detection
- ✅ **Secret Scanning** - Gitleaks + TruffleHog
- ✅ **SBOM Generation** - CycloneDX format (optional)

## Template Configuration

### Required Parameters

| Parameter      | Description         | Example                              |
| -------------- | ------------------- | ------------------------------------ |
| `project_name` | Human-readable name | "Acme Go Service"                    |
| `project_slug` | URL-friendly name   | "acme-go-service"                    |
| `module_path`  | Go module path      | "github.com/example/acme-go-service" |
| `description`  | Short description   | "A production-ready Go service"      |
| `author_name`  | Your name           | "Jane Doe"                           |
| `author_email` | Your email          | "jane@example.com"                   |

### Optional Parameters

| Parameter               | Options                      | Default    | Description              |
| ----------------------- | ---------------------------- | ---------- | ------------------------ |
| `license`               | Apache-2.0, MIT, Proprietary | Apache-2.0 | License type             |
| `go_version`            | 1.21, 1.22, 1.23             | 1.22       | Minimum Go version       |
| `enable_security_gates` | yes, no                      | yes        | Enable security scanning |
| `ci_provider`           | github, gitlab               | github     | CI/CD platform           |

## Generated Project Structure

```
acme-go-service/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Main CI/CD pipeline
│       └── go-lint.yml         # Go linting
├── cmd/
│   └── app/
│       └── main.go             # Application entry point
├── internal/
│   └── app/
│       ├── app.go              # Application logic
│       └── app_test.go         # Tests
├── .gitignore                  # Git ignore patterns
├── .golangci.yml               # golangci-lint config
├── go.mod                      # Go module definition
├── Makefile                    # Build automation
└── README.md                   # Project documentation
```

## Usage

```bash
# Build
make build

# Run
make run

# Test
make test

# Test with coverage
make test-coverage

# Lint
make lint

# Format
make fmt

# Clean
make clean

# Install tools
make install-tools
```

## Development

### Writing Tests

```go
// internal/app/app_test.go
package app

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed", 2, -3, -1},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

### Project Structure

```go
// cmd/app/main.go
package main

import (
    "fmt"
    "github.com/example/acme-go-service/internal/app"
)

func main() {
    app := app.New()
    if err := app.Run(); err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
}

// internal/app/app.go
package app

type App struct {
    // dependencies
}

func New() *App {
    return &App{}
}

func (a *App) Run() error {
    // application logic
    return nil
}
```

## CI/CD Workflows

**ci.yml** - Main Pipeline:

- Go installation and caching
- Module download
- Unit tests with coverage
- Build verification
- Cross-platform builds
- Multi-version testing

**go-lint.yml** - Linting:

- golangci-lint with all linters
- Code formatting check
- Import organization
- Go vet analysis

## Best Practices

### Code Organization

1. **`cmd/` for binaries** - One directory per executable
2. **`internal/` for libraries** - Prevents external imports
3. **`pkg/` for public APIs** - Reusable packages
4. **Table-driven tests** - Comprehensive test coverage
5. **Interfaces** - Enable mocking and testing

### Error Handling

```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("failed to process: %w", err)
}

// Create custom error types
type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %v", e.Field, e.Err)
}
```

### Dependency Injection

```go
// Use interfaces for dependencies
type Repository interface {
    Get(id string) (*Item, error)
    Save(item *Item) error
}

type Service struct {
    repo Repository
}

func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}
```

## Makefile Commands

```makefile
# Common commands
build:        # Build the application
run:          # Run the application
test:         # Run tests
test-coverage:# Run tests with coverage
lint:         # Run golangci-lint
fmt:          # Format code
clean:        # Clean build artifacts
install-tools:# Install development tools
docker-build: # Build Docker image
docker-run:   # Run Docker container
```

## Standards Compliance

This template implements:

- ✅ **Effective Go** - Official Go guidelines
- ✅ **Go Project Layout** - Standard project structure
- ✅ **NIST SSDF** - Secure development framework
- ✅ **OWASP SAMM** - Software assurance maturity

## Related Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Project Layout](https://github.com/golang-standards/project-layout)
- [golangci-lint](https://golangci-lint.run/)
- [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Version**: 1.0.0

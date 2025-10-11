# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Features

- ✅ Go {{cookiecutter.go_version}}
- ✅ Clean project structure (cmd, internal)
- ✅ Comprehensive testing with race detection
- ✅ golangci-lint for code quality
- ✅ Makefile for common tasks
- ✅ GitHub Actions CI/CD
{% if cookiecutter.enable_security_gates == "yes" %}
- ✅ Security scanning
{% endif %}

## Getting Started

### Prerequisites

- Go {{cookiecutter.go_version}} or higher

### Installation

```bash
# Clone or create from cookiecutter
cd {{cookiecutter.project_slug}}

# Download dependencies
go mod download
```

### Development

```bash
# Build the application
make build

# Run the application
make run

# Run tests
make test

# Run linters
make lint

# Tidy dependencies
make tidy
```

## Project Structure

```
.
├── cmd/
│   └── app/           # Application entrypoint
├── internal/
│   └── app/           # Internal application logic
├── bin/               # Build output
├── Makefile           # Build automation
└── go.mod             # Go module definition
```

## Make Commands

Run `make help` to see all available commands:

- `make build` - Build the application
- `make run` - Build and run the application
- `make test` - Run tests with coverage and race detection
- `make lint` - Run golangci-lint
- `make tidy` - Tidy and verify Go modules
- `make clean` - Remove build artifacts

## Testing

```bash
# Run all tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run tests with race detection
go test -race ./...
```

## CI/CD

This project uses GitHub Actions:

- **CI Pipeline**: Runs on every push and PR
  - Multi-version Go testing (1.21, 1.22)
  - Dependency verification
  - Build verification
  - Test suite with race detection
  - Format checking (gofmt)

- **Linting**: Runs golangci-lint
  - Multiple linters enabled
  - Configurable via .golangci.yml

## License

{{cookiecutter.license}}

## Author

{{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

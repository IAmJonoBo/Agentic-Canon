# Go gRPC User Service

Production-ready gRPC service demonstrating the Agentic Canon Go template.

## Features

- 🛰️ gRPC API for user management (CRUD)
- 🌉 REST gateway powered by grpc-gateway v2
- 🧠 In-memory repository with dependency injection
- 🔐 JWT helper utilities ready for auth integration
- 🧪 Unit + bufconn integration tests
- 🧰 Make targets for build, test, and protobuf generation
- 🐳 Dockerfile and Kubernetes manifests
- ⚙️ GitHub Actions CI and security workflows

## Quick Start

```bash
cd examples/projects/grpc-service

# Generate protobuf stubs (requires protoc plugins via buf)
PATH="$HOME/go/bin:$PATH" buf generate api/proto

# Install dependencies
go mod tidy

# Run unit + integration tests
make test

# Start the service
make run
```

The gRPC server listens on `:9090`; the REST gateway listens on `:8080`.

## API Overview

- `CreateUser` – `POST /v1/users`
- `GetUser` – `GET /v1/users/{id}`
- `ListUsers` – `GET /v1/users`
- `UpdateUser` – `PATCH /v1/users/{id}`
- `DeleteUser` – `DELETE /v1/users/{id}`

Swagger/OpenAPI can be generated via grpc-gateway options or upstream tooling.

## Useful Commands

| Command             | Description                          |
| ------------------- | ------------------------------------ |
| `make proto`        | Generate protobuf stubs using Buf    |
| `make test`         | Run all Go tests                     |
| `make build`        | Compile binary to `bin/grpc-service` |
| `make run`          | Start server locally                 |
| `docker compose up` | Launch containerised service         |

## CI/CD

Workflows stored in `.github/workflows/`:

- `Go gRPC Service • CI` – lint, vet, tests, build
- `Go gRPC Service • Security` – weekly `govulncheck`

## Deployment

- Dockerfile ready for distroless image
- Kubernetes manifests under `deployments/k8s`
- Configurable via environment variables (`GRPC_PORT`, `HTTP_PORT`, `APP_ENV`)

## Testing

```
go test ./...
```

Integration tests use bufconn for fast, dependency-free execution.

## Next Steps

- Swap the in-memory repository with persistent storage (PostgreSQL, etc.)
- Integrate real authentication by wiring `internal/pkg/jwt`
- Extend REST gateway with additional services and OpenAPI docs

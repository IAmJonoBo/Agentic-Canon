# Go gRPC User Service – Working Example

This example shows how to build a production-grade gRPC backend with Agentic Canon’s Go template. It includes a gRPC API, grpc-gateway HTTP bridge, CI pipelines, container packaging, and tests.

## Architecture Summary

```
cmd/server/main.go      # Application entry point
internal/
  config/               # Environment-driven configuration
  repository/           # In-memory persistence (swap with real DB)
  service/              # gRPC business logic
  server/               # gRPC + HTTP gateway wiring
  middleware/           # Logging interceptors
  pkg/jwt/, pkg/logger/ # Utilities ready for expansion
api/proto/user/v1/      # Protobuf definitions + generated code
migrations/             # Example SQL migration seed
scripts/                # Helper scripts (generate, test)
```

## Running Locally

```bash
cd examples/projects/grpc-service

# Install Buf + protoc plugins (one-time)
go install github.com/bufbuild/buf/cmd/buf@latest
PATH="$HOME/go/bin:$PATH" buf dep update

# Generate protobuf sources
go generate ./...
# or
make proto

# Download dependencies and run tests
make test

# Start the service
make run
```

gRPC endpoint: `localhost:9090`  
HTTP gateway: `http://localhost:8080/v1/users`

### Example REST Calls

```bash
curl -X POST http://localhost:8080/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","name":"Alice","role":"Engineer"}'

curl http://localhost:8080/v1/users
```

### Example gRPC Call (Evans)

```bash
evans --proto api/proto/user/v1/user.proto repl
> call CreateUser
email (TYPE_STRING) => engineer@example.com
name (TYPE_STRING) => Engineer One
role (TYPE_STRING) => Engineer
```

## Testing Matrix

| Tests                 | Command                       |
| --------------------- | ----------------------------- |
| Unit tests            | `go test ./internal/...`      |
| Integration (bufconn) | `go test ./tests/integration` |
| Combined              | `make test`                   |

## CI/CD Walkthrough

1. **CI workflow** installs Buf, regenerates protobufs, runs lint/vet/tests, and builds the binary.
2. **Security workflow** runs `govulncheck` weekly for vulnerability scanning.
3. Extend with container scanning or deployment workflows as needed.

## Observability & Ops Hooks

- Logging interceptors capture method latency, errors, and metadata.
- Graceful shutdown window configurable via `GRACEFUL_SHUTDOWN` env var.
- Health/readiness via HTTP gateway (e.g., GET `/v1/users`).

## Customisation Tips

- Replace `repository.NewUserRepository()` with a persistent implementation.
- Wire authentication by plugging a JWT secret into `internal/pkg/jwt` and adding interceptors.
- Update the Dockerfile image reference before deploying (`image: ghcr.io/<org>/grpc-user-service`).
- Add OpenAPI generation using `protoc-gen-openapiv2` if you need Swagger docs.

## License

MIT – inherit from repository license or update to your organisation’s requirement.

# Go gRPC Service Example

This is a complete example of a production-ready Go gRPC service generated using Agentic Canon.

## Overview

A high-performance gRPC service for managing user profiles with:

- Full CRUD operations
- Protocol Buffers (protobuf) for efficient serialization
- Bidirectional streaming support
- Authentication and authorization
- Health checks
- Metrics and observability
- Comprehensive tests
- CI/CD pipelines

## Features

- **gRPC** - High-performance RPC framework
- **Protocol Buffers** - Efficient data serialization
- **Go 1.22+** - Latest Go features
- **gRPC-Gateway** - RESTful JSON API alongside gRPC
- **OpenTelemetry** - Distributed tracing
- **Prometheus** - Metrics collection
- **PostgreSQL** - Data persistence with pgx driver
- **JWT Authentication** - Secure service access
- **Rate Limiting** - Request throttling
- **GitHub Actions** - Automated CI/CD

## Quick Start

### Prerequisites

- Go 1.22+
- Protocol Buffers compiler (protoc)
- PostgreSQL (optional, uses SQLite for dev)

### Installation

```bash
# Clone this example
git clone <repo-url>
cd grpc-service

# Install dependencies
go mod download

# Install protoc plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@latest
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest

# Generate code from protobuf definitions
make proto

# Set up environment variables
cp .env.example .env

# Run database migrations
make migrate-up

# Start the server
make run
```

### Access the Service

- **gRPC**: localhost:9090
- **REST Gateway**: http://localhost:8080
- **Metrics**: http://localhost:8080/metrics
- **Health**: http://localhost:8080/health
- **OpenAPI**: http://localhost:8080/swagger.json

## Project Structure

```
grpc-service/
├── cmd/
│   └── server/
│       └── main.go              # Application entry point
├── internal/
│   ├── server/
│   │   ├── server.go            # gRPC server setup
│   │   └── interceptors.go     # Middleware (auth, logging, etc.)
│   ├── service/
│   │   ├── user_service.go      # User service implementation
│   │   └── auth_service.go      # Auth service implementation
│   ├── repository/
│   │   ├── user_repo.go         # User data access
│   │   └── postgres.go          # Database connection
│   ├── middleware/
│   │   ├── auth.go              # Authentication middleware
│   │   ├── logging.go           # Request logging
│   │   ├── metrics.go           # Metrics collection
│   │   └── recovery.go          # Panic recovery
│   ├── config/
│   │   └── config.go            # Configuration management
│   └── pkg/
│       ├── jwt/
│       │   └── jwt.go           # JWT utilities
│       └── logger/
│           └── logger.go        # Structured logging
├── api/
│   └── proto/
│       ├── user/
│       │   └── v1/
│       │       ├── user.proto           # User service protobuf
│       │       ├── user.pb.go           # Generated Go code
│       │       ├── user_grpc.pb.go      # Generated gRPC code
│       │       └── user.pb.gw.go        # Generated gateway code
│       └── auth/
│           └── v1/
│               ├── auth.proto           # Auth service protobuf
│               ├── auth.pb.go
│               ├── auth_grpc.pb.go
│               └── auth.pb.gw.go
├── migrations/
│   ├── 000001_create_users_table.up.sql
│   ├── 000001_create_users_table.down.sql
│   └── ...
├── tests/
│   ├── integration/
│   │   ├── user_test.go         # Integration tests
│   │   └── auth_test.go
│   └── e2e/
│       └── service_test.go      # End-to-end tests
├── deployments/
│   ├── docker/
│   │   ├── Dockerfile           # Production image
│   │   └── docker-compose.yml   # Local development
│   └── k8s/
│       ├── deployment.yaml      # Kubernetes deployment
│       ├── service.yaml         # Kubernetes service
│       └── configmap.yaml       # Configuration
├── scripts/
│   ├── generate.sh              # Code generation
│   └── test.sh                  # Run tests
├── .github/workflows/           # CI/CD pipelines
├── Makefile                     # Build automation
├── go.mod
├── go.sum
├── .env.example
└── README.md
```

## Protocol Buffer Definitions

### User Service

```protobuf
syntax = "proto3";

package user.v1;

option go_package = "github.com/example/grpc-service/api/proto/user/v1";

service UserService {
  // Create a new user
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);

  // Get user by ID
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  // Update user
  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);

  // Delete user
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);

  // List users with pagination
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);

  // Stream user updates (server streaming)
  rpc StreamUserUpdates(StreamUserUpdatesRequest) returns (stream UserUpdate);

  // Batch create users (client streaming)
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateUsersResponse);

  // Real-time user sync (bidirectional streaming)
  rpc SyncUsers(stream SyncUsersRequest) returns (stream SyncUsersResponse);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  string avatar_url = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  string password = 3;
}

message CreateUserResponse {
  User user = 1;
}

// ... other message definitions
```

## API Usage

### gRPC Client (Go)

```go
package main

import (
    "context"
    "log"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    pb "github.com/example/grpc-service/api/proto/user/v1"
)

func main() {
    // Connect to gRPC server
    conn, err := grpc.Dial("localhost:9090", grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    client := pb.NewUserServiceClient(conn)

    // Create user
    resp, err := client.CreateUser(context.Background(), &pb.CreateUserRequest{
        Email:    "user@example.com",
        Name:     "John Doe",
        Password: "securepass123",
    })
    if err != nil {
        log.Fatal(err)
    }

    log.Printf("Created user: %v", resp.User)
}
```

### REST API (via gRPC-Gateway)

```bash
# Create user
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepass123"
  }'

# Get user
curl http://localhost:8080/api/v1/users/{id}

# Update user
curl -X PUT http://localhost:8080/api/v1/users/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "avatar_url": "https://example.com/avatar.jpg"
  }'

# Delete user
curl -X DELETE http://localhost:8080/api/v1/users/{id}

# List users with pagination
curl "http://localhost:8080/api/v1/users?page_size=10&page_token=abc123"
```

### Authentication

```bash
# Login to get JWT token
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'

# Response: { "token": "eyJhbGc..." }

# Use token in subsequent requests
curl http://localhost:8080/api/v1/users \
  -H "Authorization: Bearer eyJhbGc..."
```

### Streaming Examples

**Server Streaming (Watch user updates)**

```go
stream, err := client.StreamUserUpdates(ctx, &pb.StreamUserUpdatesRequest{})
if err != nil {
    log.Fatal(err)
}

for {
    update, err := stream.Recv()
    if err == io.EOF {
        break
    }
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("User update: %v", update.User)
}
```

**Client Streaming (Batch create users)**

```go
stream, err := client.BatchCreateUsers(ctx)
if err != nil {
    log.Fatal(err)
}

users := []*pb.CreateUserRequest{
    {Email: "user1@example.com", Name: "User 1"},
    {Email: "user2@example.com", Name: "User 2"},
}

for _, user := range users {
    if err := stream.Send(user); err != nil {
        log.Fatal(err)
    }
}

resp, err := stream.CloseAndRecv()
if err != nil {
    log.Fatal(err)
}
log.Printf("Created %d users", resp.Count)
```

**Bidirectional Streaming (Real-time sync)**

```go
stream, err := client.SyncUsers(ctx)
if err != nil {
    log.Fatal(err)
}

// Send and receive concurrently
go func() {
    for {
        msg, err := stream.Recv()
        if err == io.EOF {
            return
        }
        if err != nil {
            log.Fatal(err)
        }
        log.Printf("Received: %v", msg)
    }
}()

// Send messages
for _, req := range requests {
    if err := stream.Send(req); err != nil {
        log.Fatal(err)
    }
}

stream.CloseSend()
```

## Development

### Running Locally

```bash
# Run with hot reload (using air)
make dev

# Run without hot reload
make run

# Build binary
make build

# Run tests
make test

# Run tests with coverage
make test-coverage

# Run benchmarks
make bench

# Lint code
make lint

# Format code
make fmt

# Generate protobuf code
make proto

# Run database migrations
make migrate-up
make migrate-down

# Clean build artifacts
make clean
```

### Code Generation

The project uses Protocol Buffers for API definition. Generate code with:

```bash
# Generate all protobuf code
make proto

# Or manually:
protoc \
  --go_out=. \
  --go_opt=paths=source_relative \
  --go-grpc_out=. \
  --go-grpc_opt=paths=source_relative \
  --grpc-gateway_out=. \
  --grpc-gateway_opt=paths=source_relative \
  --openapiv2_out=. \
  api/proto/user/v1/user.proto
```

### Database Migrations

```bash
# Create new migration
migrate create -ext sql -dir migrations -seq add_user_roles

# Apply migrations
migrate -path migrations -database "postgres://localhost:5432/grpcdb?sslmode=disable" up

# Rollback migrations
migrate -path migrations -database "postgres://localhost:5432/grpcdb?sslmode=disable" down

# Or use Makefile:
make migrate-up
make migrate-down
make migrate-create NAME=add_user_roles
```

### Environment Variables

```env
# Server Configuration
GRPC_PORT=9090
HTTP_PORT=8080
ENVIRONMENT=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=grpcdb
DB_SSL_MODE=disable

# Authentication
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRATION=24h

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=grpc-service
METRICS_ENABLED=true

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

## Deployment

### Docker

```bash
# Build image
docker build -t grpc-service:latest -f deployments/docker/Dockerfile .

# Run container
docker run -p 9090:9090 -p 8080:8080 \
  -e DB_HOST=postgres \
  -e JWT_SECRET=your-secret \
  grpc-service:latest

# Using docker-compose
docker-compose -f deployments/docker/docker-compose.yml up -d
```

### Kubernetes

```bash
# Create namespace
kubectl create namespace grpc-service

# Apply configurations
kubectl apply -f deployments/k8s/configmap.yaml
kubectl apply -f deployments/k8s/secret.yaml
kubectl apply -f deployments/k8s/deployment.yaml
kubectl apply -f deployments/k8s/service.yaml
kubectl apply -f deployments/k8s/ingress.yaml

# Check deployment
kubectl get pods -n grpc-service
kubectl logs -f deployment/grpc-service -n grpc-service

# Port forward for testing
kubectl port-forward svc/grpc-service 9090:9090 -n grpc-service
```

### Cloud Deployment

#### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/grpc-service

# Deploy
gcloud run deploy grpc-service \
  --image gcr.io/PROJECT_ID/grpc-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --use-http2
```

#### AWS ECS/Fargate

- Use provided Dockerfile
- Configure ALB with HTTP/2 support
- Set environment variables via Parameter Store
- Enable CloudWatch for logs and metrics

#### Azure Container Instances

```bash
# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name grpc-service \
  --image myregistry.azurecr.io/grpc-service:latest \
  --ports 9090 8080 \
  --environment-variables \
    DB_HOST=postgres.database.azure.com \
    JWT_SECRET=secret
```

## Monitoring

### Metrics

The service exposes Prometheus metrics at `/metrics`:

- **gRPC metrics**: Request duration, status codes, throughput
- **Business metrics**: Users created, logins, API calls
- **System metrics**: Go runtime, goroutines, memory
- **Database metrics**: Connection pool, query duration

Example metrics:

```
# HELP grpc_server_handled_total Total number of RPCs completed
# TYPE grpc_server_handled_total counter
grpc_server_handled_total{grpc_code="OK",grpc_method="CreateUser",grpc_service="user.v1.UserService"} 1234

# HELP grpc_server_handling_seconds Histogram of RPC handling duration
# TYPE grpc_server_handling_seconds histogram
grpc_server_handling_seconds_bucket{grpc_method="CreateUser",le="0.005"} 100
```

### Logging

Structured logging with multiple levels:

```json
{
  "level": "info",
  "ts": "2025-10-11T18:30:00.000Z",
  "caller": "service/user_service.go:45",
  "msg": "User created",
  "userId": "usr_123",
  "email": "user@example.com",
  "requestId": "req-abc-123",
  "duration": "45ms"
}
```

### Distributed Tracing

OpenTelemetry integration:

- Automatic gRPC instrumentation
- Database query tracing
- Custom spans for business logic
- Export to Jaeger, Zipkin, or OTLP

```go
// Custom span example
ctx, span := tracer.Start(ctx, "processUser")
defer span.End()

span.SetAttributes(
    attribute.String("user.id", userID),
    attribute.String("user.email", email),
)
```

### Health Checks

```bash
# Liveness probe (always returns 200 if server is running)
curl http://localhost:8080/health/live

# Readiness probe (checks database connectivity)
curl http://localhost:8080/health/ready

# gRPC health check
grpcurl -plaintext localhost:9090 grpc.health.v1.Health/Check
```

## Testing Strategy

### Unit Tests

Test individual functions and components:

```go
func TestCreateUser(t *testing.T) {
    repo := &mockUserRepo{}
    service := NewUserService(repo)

    req := &pb.CreateUserRequest{
        Email: "test@example.com",
        Name: "Test User",
    }

    resp, err := service.CreateUser(context.Background(), req)
    assert.NoError(t, err)
    assert.NotEmpty(t, resp.User.Id)
    assert.Equal(t, req.Email, resp.User.Email)
}
```

### Integration Tests

Test with real database and gRPC server:

```go
func TestUserServiceIntegration(t *testing.T) {
    // Start test server
    server := startTestServer(t)
    defer server.Stop()

    // Create client
    conn := dialServer(t, server.Addr())
    client := pb.NewUserServiceClient(conn)

    // Test create user
    resp, err := client.CreateUser(context.Background(), &pb.CreateUserRequest{
        Email: "test@example.com",
        Name: "Test User",
    })
    require.NoError(t, err)
    assert.NotEmpty(t, resp.User.Id)

    // Test get user
    getResp, err := client.GetUser(context.Background(), &pb.GetUserRequest{
        Id: resp.User.Id,
    })
    require.NoError(t, err)
    assert.Equal(t, resp.User.Id, getResp.User.Id)
}
```

### Benchmarks

Performance benchmarks:

```go
func BenchmarkCreateUser(b *testing.B) {
    service := setupTestService()
    req := &pb.CreateUserRequest{
        Email: "bench@example.com",
        Name: "Bench User",
    }

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, err := service.CreateUser(context.Background(), req)
        if err != nil {
            b.Fatal(err)
        }
    }
}
```

### Load Testing

Using ghz (gRPC benchmarking tool):

```bash
# Install ghz
go install github.com/bojand/ghz/cmd/ghz@latest

# Run load test
ghz --insecure \
  --proto api/proto/user/v1/user.proto \
  --call user.v1.UserService/CreateUser \
  -d '{"email":"load@example.com","name":"Load User"}' \
  -c 100 \
  -n 10000 \
  localhost:9090

# Results show RPS, latency, etc.
```

## CI/CD Pipeline

### GitHub Actions Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Go version matrix (1.22, 1.23)
   - Lint with golangci-lint
   - Run tests with race detector
   - Generate coverage report
   - Build binary

2. **Security Pipeline** (`.github/workflows/security.yml`)
   - CodeQL analysis
   - Dependency scanning (Dependabot)
   - Secret scanning
   - Trivy container scanning
   - gosec security scanner

3. **Deploy Pipeline** (`.github/workflows/deploy.yml`)
   - Build Docker image
   - Push to container registry
   - Deploy to environments
   - Run smoke tests

### Quality Gates

All PRs must pass:

- ✅ golangci-lint with all linters
- ✅ All tests passing
- ✅ Code coverage ≥ 80%
- ✅ No race conditions
- ✅ Security scans clean
- ✅ Build successful

## Performance

### Benchmarks

Typical performance (4 core, 8GB RAM):

- **Unary RPC**: ~20-30µs (p50), ~100µs (p99)
- **Streaming RPC**: ~10-15µs per message
- **Throughput**: 30,000-50,000 req/sec
- **Concurrent connections**: 10,000+
- **Memory**: ~50MB base, scales linearly

### Optimization Techniques

- **Connection pooling**: Database connection reuse
- **Request batching**: Batch database operations
- **Caching**: In-memory cache for frequent reads
- **Compression**: gRPC message compression
- **Keep-alive**: HTTP/2 connection reuse
- **Concurrent processing**: Goroutines for parallel work
- **Efficient serialization**: Protocol Buffers

## Security

### Implemented Measures

- ✅ **TLS/mTLS**: Encrypted connections
- ✅ **JWT Authentication**: Token-based auth
- ✅ **Authorization**: Role-based access control
- ✅ **Rate Limiting**: Per-client throttling
- ✅ **Input Validation**: Protobuf validation
- ✅ **SQL Injection Protection**: Parameterized queries
- ✅ **Secure Headers**: Security middleware
- ✅ **Audit Logging**: Security event tracking
- ✅ **Dependency Scanning**: Automated checks
- ✅ **Secret Management**: Environment-based config

### TLS Configuration

```go
// Server with TLS
creds, err := credentials.NewServerTLSFromFile("cert.pem", "key.pem")
if err != nil {
    log.Fatal(err)
}

server := grpc.NewServer(grpc.Creds(creds))

// Mutual TLS (mTLS)
cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
caCert, err := os.ReadFile("ca.pem")
caCertPool := x509.NewCertPool()
caCertPool.AppendCertsFromPEM(caCert)

creds := credentials.NewTLS(&tls.Config{
    Certificates: []tls.Certificate{cert},
    ClientAuth:   tls.RequireAndVerifyClientCert,
    ClientCAs:    caCertPool,
})
```

## Troubleshooting

### Common Issues

**Port already in use**

```bash
# Find process
lsof -i :9090
# Kill process
kill -9 <PID>
```

**Database connection errors**

```bash
# Test connection
psql -h localhost -U postgres -d grpcdb

# Check migrations
migrate -path migrations -database "postgres://..." version
```

**Protobuf compilation errors**

```bash
# Reinstall protoc plugins
make install-proto-deps

# Regenerate code
make proto
```

**gRPC reflection not working**

```bash
# Ensure reflection is registered
import "google.golang.org/grpc/reflection"
reflection.Register(grpcServer)

# Test with grpcurl
grpcurl -plaintext localhost:9090 list
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Run `make test` and `make lint`
5. Update protobuf definitions if needed
6. Submit a pull request

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## License

This example is part of Agentic Canon and is licensed under [Apache-2.0](../../LICENSE).

## Resources

- [gRPC Documentation](https://grpc.io/docs/)
- [Protocol Buffers](https://protobuf.dev/)
- [gRPC-Gateway](https://grpc-ecosystem.github.io/grpc-gateway/)
- [Go gRPC Tutorial](https://grpc.io/docs/languages/go/quickstart/)
- [OpenTelemetry Go](https://opentelemetry.io/docs/instrumentation/go/)
- [Agentic Canon Templates](../../templates/)

## Support

For questions or issues:

1. Check this README and documentation
2. Search [existing issues](https://github.com/IAmJonoBo/Agentic-Canon/issues)
3. Ask in [discussions](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
4. Open a new issue if needed

---

**Generated using Agentic Canon** - Production-ready project scaffolding

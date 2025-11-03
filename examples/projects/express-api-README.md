# Express API Service Example

This is a complete example of a production-ready Express.js API service generated using Agentic Canon.

## Overview

A RESTful API service for managing a blog platform with:

- CRUD operations for posts and comments
- Authentication (JWT)
- OpenAPI documentation (via Swagger)
- Health checks
- Metrics endpoint
- Full test coverage
- CI/CD pipelines

## Features

- **Express.js** - Fast, unopinionated web framework
- **TypeScript** - Type-safe development
- **Prisma** - Modern database ORM
- **JWT Authentication** - Secure API access
- **OpenTelemetry** - Distributed tracing
- **Prometheus** - Metrics collection
- **Vitest** - Fast unit testing framework
- **Supertest** - HTTP assertion library
- **GitHub Actions** - Automated CI/CD
- **Swagger/OpenAPI** - Interactive API documentation

## Quick Start

### Prerequisites

- Node.js 20+
- PostgreSQL (optional, uses SQLite by default)

### Installation

```bash
# Clone this example
git clone <repo-url>
cd express-api

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run database migrations
npx prisma migrate dev

# Generate Prisma client
npx prisma generate

# Start the development server
npm run dev
```

### Access the API

- **API**: http://localhost:3000
- **API Docs**: http://localhost:3000/api-docs
- **OpenAPI Spec**: http://localhost:3000/api-docs.json
- **Metrics**: http://localhost:3000/metrics
- **Health**: http://localhost:3000/health

## Project Structure

```
express-api/
├── src/
│   ├── index.ts              # Application entry point
│   ├── app.ts                # Express app configuration
│   ├── server.ts             # Server startup
│   ├── config/
│   │   ├── index.ts          # Configuration management
│   │   └── database.ts       # Database configuration
│   ├── middleware/
│   │   ├── auth.ts           # JWT authentication
│   │   ├── errorHandler.ts  # Error handling
│   │   ├── logger.ts         # Request logging
│   │   ├── metrics.ts        # Prometheus metrics
│   │   └── validation.ts    # Request validation
│   ├── routes/
│   │   ├── index.ts          # Route aggregation
│   │   ├── posts.ts          # Post endpoints
│   │   ├── comments.ts       # Comment endpoints
│   │   ├── auth.ts           # Authentication endpoints
│   │   └── health.ts         # Health check endpoint
│   ├── controllers/
│   │   ├── postController.ts    # Post business logic
│   │   ├── commentController.ts # Comment business logic
│   │   └── authController.ts    # Auth business logic
│   ├── services/
│   │   ├── postService.ts       # Post data access
│   │   ├── commentService.ts    # Comment data access
│   │   └── userService.ts       # User data access
│   ├── models/
│   │   └── schema.prisma        # Prisma schema
│   ├── types/
│   │   ├── index.ts             # Type definitions
│   │   └── express.d.ts         # Express type extensions
│   └── utils/
│       ├── jwt.ts               # JWT utilities
│       ├── logger.ts            # Winston logger
│       └── validation.ts        # Validation helpers
├── tests/
│   ├── setup.ts                 # Test setup
│   ├── unit/
│   │   ├── services/            # Service tests
│   │   └── utils/               # Utility tests
│   ├── integration/
│   │   ├── posts.test.ts        # Post endpoint tests
│   │   ├── comments.test.ts     # Comment endpoint tests
│   │   └── auth.test.ts         # Auth endpoint tests
│   └── e2e/
│       └── api.test.ts          # End-to-end tests
├── prisma/
│   ├── schema.prisma            # Database schema
│   ├── migrations/              # Database migrations
│   └── seed.ts                  # Database seeding
├── .github/workflows/           # CI/CD pipelines
├── docker/
│   ├── Dockerfile               # Production image
│   └── docker-compose.yml       # Local development
├── k8s/
│   ├── deployment.yaml          # Kubernetes deployment
│   ├── service.yaml             # Kubernetes service
│   └── ingress.yaml             # Kubernetes ingress
├── package.json
├── tsconfig.json
├── vitest.config.ts
├── .env.example
└── README.md
```

## API Endpoints

### Authentication

```bash
# Register user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Response: { "token": "eyJhbGc..." }

# Get current user
curl http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

### Posts

```bash
# List all posts
curl http://localhost:3000/api/posts

# Get a specific post
curl http://localhost:3000/api/posts/:id

# Create a new post (requires authentication)
curl -X POST http://localhost:3000/api/posts \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "tags": ["nodejs", "typescript"]
  }'

# Update a post (requires authentication)
curl -X PUT http://localhost:3000/api/posts/:id \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Post Title",
    "content": "Updated content."
  }'

# Delete a post (requires authentication)
curl -X DELETE http://localhost:3000/api/posts/:id \
  -H "Authorization: Bearer <token>"
```

### Comments

```bash
# Get comments for a post
curl http://localhost:3000/api/posts/:postId/comments

# Add a comment (requires authentication)
curl -X POST http://localhost:3000/api/posts/:postId/comments \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great post!"
  }'

# Update a comment (requires authentication)
curl -X PUT http://localhost:3000/api/comments/:id \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated comment"
  }'

# Delete a comment (requires authentication)
curl -X DELETE http://localhost:3000/api/comments/:id \
  -H "Authorization: Bearer <token>"
```

## Development

### Running Locally

```bash
# Development mode with hot reload
npm run dev

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Watch mode for tests
npm run test:watch

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run typecheck

# Build for production
npm run build

# Start production server
npm start
```

### Database Operations

```bash
# Create a new migration
npx prisma migrate dev --name add_new_field

# Apply migrations
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset

# Seed database
npx prisma db seed

# Open Prisma Studio (database GUI)
npx prisma studio
```

### Environment Variables

```env
# Server
NODE_ENV=development
PORT=3000
API_PREFIX=/api

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/express_api
# Or for SQLite in dev: file:./dev.db

# Authentication
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRES_IN=7d

# CORS
CORS_ORIGIN=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=info

# OpenTelemetry (optional)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_SERVICE_NAME=express-api

# Metrics
METRICS_ENABLED=true
```

## Configuration

The application uses a layered configuration approach:

1. **Default values** - Defined in `src/config/index.ts`
2. **Environment variables** - Override defaults via `.env`
3. **Runtime configuration** - Can be modified via environment

Key configurations:

- Server settings (port, host, API prefix)
- Database connection
- JWT settings (secret, expiration)
- CORS settings
- Logging configuration
- OpenTelemetry settings
- Rate limiting

## Deployment

### Docker

```bash
# Build image
docker build -t express-api:latest .

# Run container
docker run -p 3000:3000 \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET=your-secret \
  express-api:latest

# Using docker-compose
docker-compose up -d
```

### Kubernetes

```bash
# Create namespace
kubectl create namespace express-api

# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment
kubectl get pods -n express-api
kubectl logs -f deployment/express-api -n express-api
```

### Cloud Platforms

#### AWS (ECS/Fargate)

- Use provided Dockerfile
- Configure ALB with health checks
- Set environment variables via Parameter Store/Secrets Manager
- Configure CloudWatch for logs and metrics

#### Azure (Container Apps)

- Deploy using Azure CLI or Azure Portal
- Configure ingress and scaling rules
- Use Azure Key Vault for secrets
- Enable Application Insights

#### Google Cloud (Cloud Run)

- Deploy using `gcloud run deploy`
- Configure environment variables
- Enable Cloud Trace and Cloud Logging
- Set up Cloud SQL for database

## Monitoring

### Metrics

The service exposes Prometheus metrics at `/metrics`:

- **HTTP metrics**: Request duration, status codes, throughput
- **Business metrics**: Posts created, comments added, user registrations
- **System metrics**: Node.js heap usage, event loop lag
- **Database metrics**: Query duration, connection pool stats

### Logging

Structured logging using Winston:

```json
{
  "level": "info",
  "message": "HTTP POST /api/posts",
  "timestamp": "2025-10-11T18:30:00.000Z",
  "userId": "user-123",
  "requestId": "req-abc-123",
  "duration": 45,
  "statusCode": 201
}
```

### Distributed Tracing

OpenTelemetry integration for distributed tracing:

- Automatic HTTP instrumentation
- Database query tracing
- Custom spans for business logic
- Export to Jaeger, Zipkin, or any OTLP-compatible backend

### Health Checks

```bash
# Liveness probe
curl http://localhost:3000/health/live

# Readiness probe (includes database check)
curl http://localhost:3000/health/ready

# Detailed health status
curl http://localhost:3000/health
```

## Testing Strategy

### Unit Tests

Test individual functions and services in isolation:

```typescript
describe("PostService", () => {
  it("should create a post", async () => {
    const post = await postService.create({
      title: "Test Post",
      content: "Test content",
      authorId: "user-123",
    });
    expect(post.title).toBe("Test Post");
  });
});
```

### Integration Tests

Test API endpoints with database:

```typescript
describe("POST /api/posts", () => {
  it("should create a post with authentication", async () => {
    const token = await getAuthToken();
    const response = await request(app)
      .post("/api/posts")
      .set("Authorization", `Bearer ${token}`)
      .send({ title: "Test", content: "Content" })
      .expect(201);

    expect(response.body.title).toBe("Test");
  });
});
```

### E2E Tests

Test complete user workflows:

```typescript
describe("Blog workflow", () => {
  it("should allow user to register, create post, and comment", async () => {
    // Register
    const user = await register();
    // Login
    const token = await login(user);
    // Create post
    const post = await createPost(token);
    // Add comment
    const comment = await addComment(token, post.id);
    // Verify
    expect(comment.postId).toBe(post.id);
  });
});
```

### Test Coverage

Target coverage metrics:

- **Statements**: ≥ 80%
- **Branches**: ≥ 75%
- **Functions**: ≥ 80%
- **Lines**: ≥ 80%

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes comprehensive CI/CD pipelines:

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Lint code (ESLint, Prettier)
   - Type checking (TypeScript)
   - Run tests with coverage
   - Build project
   - Runs on: push, pull_request

2. **Security Pipeline** (`.github/workflows/security.yml`)
   - CodeQL analysis
   - Dependency scanning
   - Secret scanning (Gitleaks)
   - SBOM generation
   - Container scanning (Trivy)

3. **Deploy Pipeline** (`.github/workflows/deploy.yml`)
   - Build Docker image
   - Push to registry
   - Deploy to environments
   - Run smoke tests

### Quality Gates

All PRs must pass:

- ✅ All tests passing
- ✅ Code coverage ≥ 80%
- ✅ No linting errors
- ✅ No type errors
- ✅ Security scan passing
- ✅ No high/critical vulnerabilities

## Performance

### Benchmarks

Typical performance on a standard cloud instance (2 vCPU, 4GB RAM):

- **Simple GET**: ~50-100ms (p95)
- **POST with validation**: ~100-200ms (p95)
- **Database queries**: ~20-50ms (p95)
- **Throughput**: ~1000 req/sec
- **Concurrent connections**: 10,000+

### Optimization Techniques

- **Connection pooling**: Reuse database connections
- **Caching**: Redis for frequently accessed data
- **Compression**: Gzip/Brotli for responses
- **Rate limiting**: Protect against abuse
- **Database indexing**: Optimize query performance
- **Async operations**: Non-blocking I/O
- **Clustering**: Multi-process for CPU-bound tasks

### Load Testing

```bash
# Using autocannon
npx autocannon -c 100 -d 30 http://localhost:3000/api/posts

# Using k6
k6 run load-tests/api-test.js
```

## Security

### Implemented Measures

- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **Password Hashing**: bcrypt with salt rounds
- ✅ **Input Validation**: Zod schema validation
- ✅ **SQL Injection Protection**: Prisma ORM parameterized queries
- ✅ **XSS Protection**: Helmet.js security headers
- ✅ **CSRF Protection**: CSRF tokens for state-changing operations
- ✅ **Rate Limiting**: Express rate limit middleware
- ✅ **CORS Configuration**: Controlled cross-origin access
- ✅ **Security Headers**: Helmet.js (HSTS, CSP, etc.)
- ✅ **Dependency Scanning**: Automated vulnerability checks
- ✅ **Secret Management**: Environment-based configuration
- ✅ **API Key Rotation**: Support for multiple valid keys
- ✅ **Audit Logging**: Track security-relevant events

### Best Practices

1. **Never commit secrets** - Use environment variables
2. **Keep dependencies updated** - Regular security patches
3. **Use HTTPS in production** - Encrypt data in transit
4. **Implement proper RBAC** - Role-based access control
5. **Monitor for anomalies** - Real-time security monitoring
6. **Regular security audits** - Periodic penetration testing
7. **Secure database** - Network isolation, encryption at rest

## Troubleshooting

### Common Issues

**Port already in use**

```bash
# Find process using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
```

**Database connection errors**

```bash
# Verify PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL

# Test connection
npx prisma db execute --stdin <<< "SELECT 1"
```

**Test failures**

```bash
# Clear test database
npm run test:db:reset

# Run specific test
npm test -- posts.test.ts

# Debug mode
node --inspect-brk node_modules/.bin/vitest
```

**TypeScript errors**

```bash
# Clear cache
rm -rf node_modules dist
npm install

# Regenerate Prisma types
npx prisma generate
```

## Contributing

Contributions are welcome! Please follow:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run linting and tests locally
5. Submit a pull request

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## License

This example is part of Agentic Canon and is licensed under [Apache-2.0](../../LICENSE).

## Resources

- [Express.js Documentation](https://expressjs.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [OpenTelemetry Node.js](https://opentelemetry.io/docs/instrumentation/js/)
- [Vitest Documentation](https://vitest.dev/)
- [Agentic Canon Templates](../../templates/)

## Support

For questions or issues:

1. Check this README and project documentation
2. Search [existing issues](https://github.com/IAmJonoBo/Agentic-Canon/issues)
3. Ask in [discussions](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
4. Open a new issue if needed

---

**Generated using Agentic Canon** - Production-ready project scaffolding

# FastAPI Microservice Example

This is a complete example of a production-ready FastAPI microservice generated using Agentic Canon.

## Overview

A RESTful API service for managing a simple task/todo list with:
- CRUD operations
- Authentication (JWT)
- OpenAPI documentation
- Health checks
- Metrics endpoint
- Full test coverage
- CI/CD pipelines

## Features

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **JWT Authentication** - Secure API access
- **OpenTelemetry** - Distributed tracing
- **Prometheus** - Metrics collection
- **Pytest** - Comprehensive test suite
- **GitHub Actions** - Automated CI/CD

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (optional, uses SQLite by default)

### Installation

```bash
# Clone this example
git clone <repo-url>
cd fastapi-microservice

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

### Access the API

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **OpenAPI**: http://localhost:8000/openapi.json
- **Metrics**: http://localhost:8000/metrics
- **Health**: http://localhost:8000/health

## Project Structure

```
fastapi-microservice/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py           # JWT utilities
│   │   └── dependencies.py  # Auth dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Task endpoints
│   │   ├── users.py         # User endpoints
│   │   └── health.py        # Health check
│   └── middleware/
│       ├── __init__.py
│       ├── logging.py       # Request logging
│       └── metrics.py       # Prometheus metrics
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_tasks.py        # Task endpoint tests
│   ├── test_users.py        # User endpoint tests
│   └── test_auth.py         # Auth tests
├── alembic/                 # Database migrations
├── .github/workflows/       # CI/CD pipelines
├── pyproject.toml
├── README.md
└── docker-compose.yml       # Local development
```

## API Endpoints

### Authentication

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
```

### Tasks

```bash
# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "From the store"}'

# List tasks
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer <token>"

# Get task
curl http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer <token>"

# Update task
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "completed": true}'

# Delete task
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer <token>"
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_tasks.py

# With markers
pytest -m "not slow"
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint
ruff check app/ tests/

# Type check
mypy app/

# Run all checks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Configuration

Environment variables (create `.env` file):

```bash
# Application
APP_NAME=fastapi-microservice
APP_VERSION=1.0.0
DEBUG=false

# Database
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
ENABLE_METRICS=true
```

## Deployment

### Docker

```bash
# Build image
docker build -t fastapi-microservice .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./app.db \
  -e SECRET_KEY=your-secret-key \
  fastapi-microservice
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/fastapi-microservice
```

## Monitoring

### Metrics

Prometheus metrics available at `/metrics`:

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration
- `http_requests_in_progress` - Active requests
- `db_queries_total` - Database queries
- `task_operations_total` - Task operations by type

### Health Checks

```bash
# Liveness probe
curl http://localhost:8000/health/live

# Readiness probe
curl http://localhost:8000/health/ready
```

### Tracing

OpenTelemetry traces sent to configured endpoint:

```python
# Example: View trace in Jaeger
# http://localhost:16686
```

## Testing Strategy

- **Unit Tests**: Individual functions and classes
- **Integration Tests**: API endpoints with database
- **Contract Tests**: OpenAPI schema validation
- **Load Tests**: Performance testing with Locust

## CI/CD Pipeline

GitHub Actions workflows:

1. **CI** - Run tests, linting, type checking
2. **Security** - CodeQL, secret scanning, dependency check
3. **Build** - Build and push Docker image
4. **Deploy** - Deploy to staging/production

## Performance

- Average response time: <50ms
- P95 latency: <200ms
- Throughput: 1000+ req/s
- Memory usage: <100MB

## Security

- JWT authentication
- Password hashing (bcrypt)
- SQL injection protection (SQLAlchemy ORM)
- XSS protection (FastAPI auto-escaping)
- CORS configuration
- Rate limiting
- Security headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Agentic Canon](https://github.com/IAmJonoBo/Agentic-Canon)

## Support

- GitHub Issues: [Report a bug](https://github.com/your-org/fastapi-microservice/issues)
- Documentation: [Full docs](https://your-org.github.io/fastapi-microservice)
- Email: support@example.com

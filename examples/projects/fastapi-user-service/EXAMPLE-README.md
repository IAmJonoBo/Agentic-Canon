# FastAPI User Service - Working Example

A complete, production-ready FastAPI microservice demonstrating the Agentic Canon Python service template in action.

## Overview

This is a **working example** of a user management microservice built with FastAPI, showcasing:

- ✅ **Full CRUD operations** for user management
- ✅ **RESTful API** with automatic OpenAPI documentation
- ✅ **Data validation** with Pydantic models
- ✅ **Security features** including password hashing and JWT tokens
- ✅ **Comprehensive tests** with pytest and FastAPI TestClient
- ✅ **CI/CD workflows** with GitHub Actions
- ✅ **Health and readiness endpoints** for Kubernetes
- ✅ **CORS middleware** configured
- ✅ **Type hints** throughout with mypy validation
- ✅ **Code quality** enforced with black, ruff, and pre-commit hooks

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip and virtualenv

### Installation

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Run the Service

```bash
# Start the development server
uvicorn acme_service.main:app --reload

# Or use the installed module
python -m uvicorn acme_service.main:app --reload
```

The service will be available at:

- API: http://localhost:8000
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Health Checks

```bash
# Root health check
curl http://localhost:8000/

# Health endpoint
curl http://localhost:8000/health

# Readiness endpoint
curl http://localhost:8000/ready
```

### User Management

#### Create a User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "role": "user"
  }'
```

Response:

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
}
```

#### List All Users

```bash
curl http://localhost:8000/users
```

#### Get a Specific User

```bash
curl http://localhost:8000/users/{user_id}
```

#### Update a User

```bash
curl -X PUT http://localhost:8000/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Doe",
    "role": "admin"
  }'
```

#### Delete a User

```bash
curl -X DELETE http://localhost:8000/users/{user_id}
```

## Architecture

### Project Structure

```
fastapi-user-service/
├── src/
│   └── acme_service/
│       ├── __init__.py         # Package initialization
│       ├── main.py             # FastAPI application
│       ├── models.py           # Pydantic models
│       ├── database.py         # In-memory database
│       └── security.py         # Password hashing and JWT
├── tests/
│   ├── test_smoke.py          # Basic smoke tests
│   └── test_api.py            # API endpoint tests
├── .github/
│   └── workflows/
│       ├── ci.yml             # CI pipeline
│       └── security.yml       # Security scanning
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

### Key Components

1. **Models** (`models.py`):
    - `User`: Base user model with validation
    - `UserCreate`: For creating new users
    - `UserUpdate`: For updating existing users
    - `UserInDB`: User model as stored in database

2. **Database** (`database.py`):
    - In-memory database for demonstration
    - Would be replaced with SQLAlchemy/PostgreSQL in production

3. **Security** (`security.py`):
    - Password hashing with bcrypt
    - JWT token creation and validation
    - Ready for authentication implementation

4. **API** (`main.py`):
    - FastAPI application with all endpoints
    - CORS middleware configured
    - OpenAPI documentation enabled

## Development

### Run Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage report
pytest --cov=acme_service --cov-report=html
```

### Code Quality

```bash
# Format code with black
black src tests

# Lint with ruff
ruff check src tests

# Type check with mypy
mypy src

# Run all pre-commit hooks
pre-commit run --all-files
```

### Interactive Development

The service includes automatic reload for development:

```bash
uvicorn acme_service.main:app --reload --log-level debug
```

Make changes to the code and the server will automatically reload!

## Testing

Comprehensive test suite included:

- **Smoke tests**: Basic package functionality
- **API tests**: All CRUD operations
- **Error handling tests**: Validation and edge cases
- **Integration tests**: End-to-end workflows

Test coverage: **>80%** (enforced in CI)

## CI/CD

Automated workflows included:

### CI Pipeline (`.github/workflows/ci.yml`)

- ✅ Run tests on Python 3.11 and 3.12
- ✅ Check code coverage (≥80%)
- ✅ Run linters (black, ruff, mypy)
- ✅ Validate pre-commit hooks

### Security Pipeline (`.github/workflows/security.yml`)

- ✅ CodeQL static analysis
- ✅ Secret scanning with Gitleaks
- ✅ Dependency scanning with Dependabot
- ✅ SBOM generation with CycloneDX

## Production Readiness

### What's Included

✅ **Logging**: Structured logging with structlog  
✅ **Validation**: Pydantic models with comprehensive validation  
✅ **Error Handling**: Proper HTTP status codes and error messages  
✅ **CORS**: Configurable CORS middleware  
✅ **Health Checks**: Liveness and readiness endpoints  
✅ **API Documentation**: Automatic OpenAPI/Swagger docs  
✅ **Testing**: Comprehensive test suite with >80% coverage  
✅ **CI/CD**: Automated testing and security scanning

### Production Enhancements Needed

When deploying to production, consider adding:

- [ ] **Real Database**: Replace in-memory DB with PostgreSQL/MySQL
    - Use SQLAlchemy ORM
    - Add database migrations with Alembic
- [ ] **Authentication**: Implement JWT-based auth
    - Add login endpoint
    - Implement OAuth2 password flow
    - Add protected endpoints with dependencies
- [ ] **Rate Limiting**: Protect against abuse
    - Use slowapi or similar
- [ ] **Caching**: Improve performance
    - Redis for session storage
    - Cache frequently accessed data
- [ ] **Monitoring**: Production observability
    - OpenTelemetry instrumentation
    - Prometheus metrics
    - Distributed tracing
- [ ] **Configuration**: Environment-based config
    - Use pydantic-settings
    - Secrets management (AWS Secrets Manager, HashiCorp Vault)
- [ ] **Deployment**: Container and orchestration
    - Dockerfile for containerization
    - Kubernetes manifests
    - Helm charts

## Environment Variables

Configure the service with environment variables:

```bash
# Security (change in production!)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Database (when using real DB)
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "acme_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: fastapi-user-service
spec:
    replicas: 3
    selector:
        matchLabels:
            app: fastapi-user-service
    template:
        metadata:
            labels:
                app: fastapi-user-service
        spec:
            containers:
                - name: api
                  image: fastapi-user-service:0.1.0
                  ports:
                      - containerPort: 8000
                  livenessProbe:
                      httpGet:
                          path: /health
                          port: 8000
                  readinessProbe:
                      httpGet:
                          path: /ready
                          port: 8000
```

## Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Service Template](../../templates/python-service/README.md)
- [Agentic Canon Documentation](../../README.md)

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Generated from**: Agentic Canon Python Service Template  
**Part of**: Agentic Canon - Frontier Software Excellence  
**Version**: 0.1.0

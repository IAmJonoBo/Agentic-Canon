# Express User API - Working Example

A complete, production-ready Express.js API demonstrating the Agentic Canon Node service template in action.

## Overview

This is a **working example** of a user management RESTful API built with Express.js and TypeScript, showcasing:

- ✅ **Full CRUD operations** for user management
- ✅ **RESTful API** with proper HTTP methods and status codes
- ✅ **TypeScript** with strict type checking
- ✅ **Zod validation** for request validation
- ✅ **Structured logging** with Winston
- ✅ **Security headers** with Helmet
- ✅ **CORS** configured for cross-origin requests
- ✅ **Comprehensive tests** with Vitest and Supertest
- ✅ **Health and readiness endpoints** for Kubernetes
- ✅ **ESM modules** (modern JavaScript)
- ✅ **CI/CD workflows** with GitHub Actions

## Quick Start

### Prerequisites

- Node.js 20+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run in development mode (with auto-reload)
npm run dev

# Build for production
npm run build

# Run production build
npm start
```

The API will be available at http://localhost:3000

### Development

```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run typecheck
```

## API Endpoints

### Health Checks

```bash
# Root health check
curl http://localhost:3000/

# Health endpoint
curl http://localhost:3000/health

# Readiness endpoint
curl http://localhost:3000/ready
```

### User Management

#### Create a User

```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "fullName": "John Doe",
    "password": "securepass123",
    "role": "user"
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "fullName": "John Doe",
  "role": "user",
  "isActive": true,
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

#### List All Users

```bash
curl http://localhost:3000/users
```

#### Get a Specific User

```bash
curl http://localhost:3000/users/{user_id}
```

#### Update a User

```bash
curl -X PUT http://localhost:3000/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Jane Doe",
    "role": "admin"
  }'
```

#### Delete a User

```bash
curl -X DELETE http://localhost:3000/users/{user_id}
```

## Project Structure

```
express-user-api/
├── src/
│   ├── index.ts           # Application entry point
│   ├── app.ts             # Express app configuration
│   ├── types.ts           # Type definitions and Zod schemas
│   ├── database.ts        # In-memory database
│   └── logger.ts          # Winston logger configuration
├── tests/
│   ├── smoke.test.ts      # Basic smoke tests
│   └── api.test.ts        # API endpoint tests
├── .github/
│   └── workflows/
│       ├── ci.yml         # CI pipeline
│       └── security.yml   # Security scanning
├── package.json           # Project configuration
├── tsconfig.json          # TypeScript configuration
└── vitest.config.ts       # Test configuration
```

## Key Features

### Type Safety with TypeScript

All code is fully typed with TypeScript in strict mode:

```typescript
interface User {
  id: string;
  email: string;
  fullName: string;
  role: UserRole;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

### Request Validation with Zod

Input validation using Zod schemas:

```typescript
const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  fullName: z.string().min(1).max(100),
  password: z.string().min(8),
  role: z.nativeEnum(UserRole).default(UserRole.USER),
});
```

### Structured Logging

JSON-structured logging with Winston:

```typescript
logger.info('User created', { userId: user.id, email: user.email });
logger.error('Error creating user', { error });
```

### Security

- **Helmet**: Security headers
- **CORS**: Configurable cross-origin resource sharing
- **Input validation**: Zod schema validation
- **Error handling**: Centralized error handling

## Testing

Comprehensive test suite with Vitest and Supertest:

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm run test:watch
```

Test coverage: **>80%** (enforced in CI)

### Test Examples

```typescript
it('should create a new user', async () => {
  const response = await request(app)
    .post('/users')
    .send({
      email: 'test@example.com',
      fullName: 'Test User',
      password: 'securepass123'
    });

  expect(response.status).toBe(201);
  expect(response.body.email).toBe('test@example.com');
});
```

## CI/CD

Automated workflows included:

### CI Pipeline (`.github/workflows/ci.yml`)
- ✅ Run tests on Node.js 20 and 22
- ✅ Check code coverage (≥80%)
- ✅ Run linter (ESLint)
- ✅ Type check (TypeScript)
- ✅ Format check (Prettier)

### Security Pipeline (`.github/workflows/security.yml`)
- ✅ CodeQL static analysis
- ✅ Secret scanning with Gitleaks
- ✅ Dependency scanning with npm audit
- ✅ SBOM generation

## Environment Variables

Configure the service with environment variables:

```bash
# Server
PORT=3000
NODE_ENV=production

# Logging
LOG_LEVEL=info

# CORS
CORS_ORIGIN=http://localhost:3001
```

## Production Deployment

### Docker

Create a `Dockerfile`:

```dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-user-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: express-user-api
  template:
    metadata:
      labels:
        app: express-user-api
    spec:
      containers:
      - name: api
        image: express-user-api:0.1.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
```

## Production Enhancements

When deploying to production, consider adding:

- [ ] **Real Database**: Replace in-memory DB with PostgreSQL/MongoDB
  - Use Prisma or TypeORM
  - Add database migrations
  
- [ ] **Authentication**: Implement JWT-based auth
  - Add login/logout endpoints
  - Protect routes with middleware
  
- [ ] **Rate Limiting**: Protect against abuse
  - Use express-rate-limit
  
- [ ] **Caching**: Improve performance
  - Redis for session storage
  - Cache frequently accessed data
  
- [ ] **API Documentation**: Auto-generate docs
  - Use Swagger/OpenAPI
  - Add @types/swagger-ui-express
  
- [ ] **Monitoring**: Production observability
  - OpenTelemetry instrumentation
  - Prometheus metrics
  - Distributed tracing
  
- [ ] **Password Hashing**: Use bcrypt
  - Replace simplified hashing
  - Add salt rounds configuration

## Architecture

### Database Layer

In-memory database for demonstration. In production, use:

```typescript
// Example with Prisma
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

const user = await prisma.user.create({
  data: { email, fullName, hashedPassword }
});
```

### Middleware Stack

1. **helmet()** - Security headers
2. **cors()** - Cross-origin resource sharing
3. **express.json()** - JSON body parser
4. **Request logger** - Log all requests
5. **Routes** - Application routes
6. **Error handler** - Centralized error handling
7. **404 handler** - Catch-all for unknown routes

## Related Resources

- [Express Documentation](https://expressjs.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Zod Documentation](https://zod.dev/)
- [Node Service Template](../../templates/node-service/README.md)
- [Agentic Canon Documentation](../../README.md)

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Generated from**: Agentic Canon Node Service Template  
**Part of**: Agentic Canon - Frontier Software Excellence  
**Version**: 0.1.0

# Contract Templates

API contract templates for REST APIs and event-driven systems implementing contract-first development.

## Purpose

These templates enable contract-first API development, ensuring clear interfaces, consistent documentation, and automated contract testing between services.

## Contents

### 🔌 OpenAPI Templates (`openapi/`)

REST API specifications using OpenAPI 3.1 standard.

**File:** [`openapi-template.yaml`](openapi/openapi-template.yaml)

**Features:**

- OpenAPI 3.1 specification format
- Multiple authentication schemes (Bearer JWT, API Key, OAuth2)
- Comprehensive security definitions
- Reusable components (schemas, responses, parameters)
- Multiple server environments (production, staging, local)
- Error response standardization
- OWASP API Security Top 10 alignment
- Pagination and filtering patterns
- Rate limiting headers
- Content negotiation (JSON, XML)

**Key Sections:**

- **Info**: API metadata, version, contact, license
- **Servers**: Environment-specific URLs
- **Security**: Authentication/authorization schemes
- **Components**: Reusable schemas, responses, parameters
- **Paths**: API endpoints and operations
- **Tags**: Logical endpoint grouping

**Usage:**

```bash
# Copy and customize
cp templates/contracts/openapi/openapi-template.yaml api/openapi.yaml

# Replace placeholders
sed -i 's/{{ API_NAME }}/User Service API/g' api/openapi.yaml
sed -i 's/{{ VERSION }}/1.0.0/g' api/openapi.yaml

# Validate specification
npx @apidevtools/swagger-cli validate api/openapi.yaml

# Generate documentation
npx redoc-cli bundle api/openapi.yaml -o docs/api.html

# Generate client SDKs
npx @openapitools/openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g typescript-axios \
  -o client/
```

**Standards Implemented:**

- OpenAPI 3.1 Specification
- REST API Design Best Practices
- OWASP API Security Top 10
- OAuth 2.0 / OpenID Connect
- RFC 7807 (Problem Details for HTTP APIs)

### 📡 AsyncAPI Templates (`asyncapi/`)

Event-driven API specifications using AsyncAPI 3.0 standard.

**File:** [`asyncapi-template.yaml`](asyncapi/asyncapi-template.yaml)

**Features:**

- AsyncAPI 3.0 specification format
- CloudEvents specification alignment
- Multiple protocols (Kafka, AMQP, MQTT, WebSocket)
- Message schemas and validation
- Dead Letter Queue patterns
- Event versioning strategies
- Consumer groups and partitioning
- Idempotency and retry patterns
- Security schemes (SASL, TLS)

**Key Sections:**

- **Info**: Service metadata and description
- **Servers**: Message broker configurations
- **Channels**: Topics/queues and message flow
- **Operations**: Publish/subscribe operations
- **Components**: Reusable message schemas
- **Security**: Authentication schemes

**Usage:**

```bash
# Copy and customize
cp templates/contracts/asyncapi/asyncapi-template.yaml api/asyncapi.yaml

# Replace placeholders
sed -i 's/{{ API_NAME }}/Event Service/g' api/asyncapi.yaml
sed -i 's/{{ VERSION }}/1.0.0/g' api/asyncapi.yaml

# Validate specification
npx @asyncapi/cli validate api/asyncapi.yaml

# Generate documentation
npx @asyncapi/cli generate fromTemplate api/asyncapi.yaml @asyncapi/html-template -o docs/

# Generate client code
npx @asyncapi/cli generate fromTemplate api/asyncapi.yaml @asyncapi/nodejs-template -o src/
```

**Standards Implemented:**

- AsyncAPI 3.0 Specification
- CloudEvents specification
- OWASP API Security Top 10
- Event-driven architecture patterns
- Message schema evolution

### 🧪 Contract Testing (Planned)

Automated contract testing to ensure API compliance.

**Planned Features:**

- Pact consumer/provider contracts
- OpenAPI validation testing
- Schema validation
- Breaking change detection
- Contract versioning

## Quick Start

### REST API Development

```bash
# 1. Create OpenAPI specification
cp templates/contracts/openapi/openapi-template.yaml api/openapi.yaml

# 2. Define your API contract
# Edit openapi.yaml with your endpoints, schemas, etc.

# 3. Validate specification
npm install -g @apidevtools/swagger-cli
swagger-cli validate api/openapi.yaml

# 4. Generate server stubs
npx @openapitools/openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g nodejs-express-server \
  -o server/

# 5. Generate client SDK
npx @openapitools/openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g typescript-axios \
  -o client/

# 6. Generate documentation
npx redoc-cli bundle api/openapi.yaml -o docs/api.html
```

### Event-Driven Development

```bash
# 1. Create AsyncAPI specification
cp templates/contracts/asyncapi/asyncapi-template.yaml api/asyncapi.yaml

# 2. Define your events and channels
# Edit asyncapi.yaml with your event schemas

# 3. Validate specification
npm install -g @asyncapi/cli
asyncapi validate api/asyncapi.yaml

# 4. Generate documentation
asyncapi generate fromTemplate api/asyncapi.yaml @asyncapi/html-template -o docs/

# 5. Generate code
asyncapi generate fromTemplate api/asyncapi.yaml @asyncapi/nodejs-template -o src/

# 6. Set up contract testing
# Add validation in CI/CD
```

## Integration Examples

### GitHub Actions - OpenAPI Validation

```yaml
# .github/workflows/api-contracts.yml
name: API Contracts

on: [push, pull_request]

jobs:
  validate-openapi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate OpenAPI spec
        uses: char0n/swagger-editor-validate@v1
        with:
          definition-file: api/openapi.yaml

      - name: Generate documentation
        run: |
          npx redoc-cli bundle api/openapi.yaml -o api-docs.html

      - name: Upload docs
        uses: actions/upload-artifact@v4
        with:
          name: api-documentation
          path: api-docs.html

      - name: Check for breaking changes
        uses: oasdiff/oasdiff-action@v0.0.19
        with:
          base: main:api/openapi.yaml
          revision: HEAD:api/openapi.yaml
          fail-on-breaking: true
```

### GitHub Actions - AsyncAPI Validation

```yaml
# .github/workflows/async-contracts.yml
name: AsyncAPI Contracts

on: [push, pull_request]

jobs:
  validate-asyncapi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate AsyncAPI spec
        uses: WaleedAshraf/asyncapi-github-action@v0.0.8
        with:
          filepath: api/asyncapi.yaml

      - name: Generate documentation
        run: |
          npx @asyncapi/cli generate fromTemplate \
            api/asyncapi.yaml \
            @asyncapi/html-template \
            -o docs/events/

      - name: Upload docs
        uses: actions/upload-artifact@v4
        with:
          name: event-documentation
          path: docs/events/
```

### Contract Testing with Pact

```javascript
// tests/contract/user-service.contract.test.js
const { Pact } = require("@pact-foundation/pact");
const { UserService } = require("../../src/services/user");

describe("User Service Contract", () => {
  const provider = new Pact({
    consumer: "web-app",
    provider: "user-service",
    port: 8080,
  });

  beforeAll(() => provider.setup());
  afterEach(() => provider.verify());
  afterAll(() => provider.finalize());

  describe("GET /users/:id", () => {
    beforeEach(() => {
      return provider.addInteraction({
        state: "user exists",
        uponReceiving: "a request for a user",
        withRequest: {
          method: "GET",
          path: "/users/123",
          headers: { Accept: "application/json" },
        },
        willRespondWith: {
          status: 200,
          headers: { "Content-Type": "application/json" },
          body: {
            id: "123",
            name: "John Doe",
            email: "john@example.com",
          },
        },
      });
    });

    it("returns the user", async () => {
      const service = new UserService("http://localhost:8080");
      const user = await service.getUser("123");

      expect(user.id).toBe("123");
      expect(user.name).toBe("John Doe");
    });
  });
});
```

## Best Practices

### OpenAPI Best Practices

1. **Version your API** - Use semantic versioning in URL path or header
2. **Use consistent naming** - camelCase for JSON, kebab-case for URLs
3. **Document everything** - Add descriptions to all endpoints and fields
4. **Define error responses** - Standardize error format (RFC 7807)
5. **Security first** - Define security schemes and requirements
6. **Pagination** - Use consistent pagination patterns (limit/offset or cursor)
7. **Rate limiting** - Document rate limits and headers
8. **Deprecation** - Mark deprecated endpoints with `deprecated: true`
9. **Examples** - Provide request/response examples
10. **Validation** - Use JSON Schema validation for all inputs

### AsyncAPI Best Practices

1. **Event naming** - Use domain.object.action pattern (user.created, order.placed)
2. **Idempotency** - Include message ID for deduplication
3. **Versioning** - Version your events (v1, v2 in topic name or payload)
4. **Schema evolution** - Use backward-compatible changes
5. **Dead letter queues** - Handle failed messages
6. **Ordering guarantees** - Use partition keys for ordering
7. **CloudEvents** - Adopt CloudEvents specification for metadata
8. **Replay capability** - Support event replay for recovery
9. **Documentation** - Explain event flow and dependencies
10. **Monitoring** - Track message processing metrics

### Contract-First Development

1. **Design before code** - Create contract before implementation
2. **Stakeholder review** - Get feedback on contract before coding
3. **Version control** - Treat contracts as first-class code
4. **Breaking changes** - Use major version bumps
5. **Backward compatibility** - Avoid breaking existing consumers
6. **Contract testing** - Validate both provider and consumer
7. **Mock servers** - Use contract for development/testing
8. **Documentation generation** - Auto-generate from contract
9. **SDK generation** - Generate client libraries from contract
10. **CI/CD validation** - Validate contract on every commit

## Tools and Resources

### OpenAPI Tools

**Validation:**

- [Swagger CLI](https://github.com/APIDevTools/swagger-cli) - Validate and bundle
- [Spectral](https://stoplight.io/open-source/spectral) - API linting
- [openapi-validator](https://github.com/IBM/openapi-validator) - IBM validator

**Documentation:**

- [Redoc](https://github.com/Redocly/redoc) - Beautiful API docs
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Interactive docs
- [Stoplight](https://stoplight.io/) - Design platform

**Code Generation:**

- [OpenAPI Generator](https://openapi-generator.tech/) - Multi-language support
- [Swagger Codegen](https://swagger.io/tools/swagger-codegen/)
- [oapi-codegen](https://github.com/deepmap/oapi-codegen) - Go generator

**Testing:**

- [Dredd](https://dredd.org/) - HTTP API testing
- [Schemathesis](https://schemathesis.readthedocs.io/) - Property-based testing
- [Postman](https://www.postman.com/) - API testing platform

### AsyncAPI Tools

**Validation:**

- [AsyncAPI CLI](https://github.com/asyncapi/cli) - Official CLI tool
- [AsyncAPI Validator](https://www.asyncapi.com/tools/validator)

**Documentation:**

- [AsyncAPI HTML Template](https://github.com/asyncapi/html-template)
- [AsyncAPI React Component](https://github.com/asyncapi/asyncapi-react)

**Code Generation:**

- [AsyncAPI Generator](https://github.com/asyncapi/generator) - Template engine
- Language-specific templates (Node.js, Java, Python, etc.)

### Contract Testing Tools

- [Pact](https://pact.io/) - Consumer-driven contract testing
- [Spring Cloud Contract](https://spring.io/projects/spring-cloud-contract)
- [Portman](https://github.com/apideck-libraries/portman) - OpenAPI to Postman

## Standards Compliance

These templates help achieve compliance with:

- ✅ **OpenAPI 3.1** - REST API specification standard
- ✅ **AsyncAPI 3.0** - Event-driven API specification
- ✅ **CloudEvents** - Event metadata specification
- ✅ **OWASP API Security Top 10** - API security best practices
- ✅ **RFC 7807** - Problem Details for HTTP APIs
- ✅ **OAuth 2.0 / OIDC** - Authentication and authorization

## Related Documentation

- [CI/CD Templates](../cicd/README.md) - Contract validation in pipelines
- [Security Templates](../security/README.md) - API security scanning
- [Observability Templates](../observability/README.md) - API monitoring
- [Video Tutorial: Contracts](../../examples/video-tutorials/03-cicd-setup.md)

## Contributing

To improve these templates:

1. Add real-world API examples
2. Share contract testing patterns
3. Contribute language-specific generators
4. Improve documentation
5. Report issues or edge cases

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Last Updated**: 2025-10-12  
**Version**: 1.0.0

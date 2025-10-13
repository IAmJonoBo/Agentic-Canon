---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 03 Contracts & Tests

This notebook demonstrates:

- OpenAPI/Swagger specification generation
- AsyncAPI for event-driven architectures
- Contract testing with Pact
- Mutation testing for test quality

```{code-cell} ipython3
:tags: [parameters]

# Parameters cell for Papermill
run_mode = "interactive"
```

## OpenAPI Specification

Define REST APIs using OpenAPI 3.x for documentation and code generation.

```{code-cell} ipython3
import json

openapi_spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "Example API",
        "version": "1.0.0",
        "description": "A sample API demonstrating OpenAPI spec"
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "List users",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["id", "name", "email"]
            }
        }
    }
}

print("OpenAPI 3.0 Specification:")
print(json.dumps(openapi_spec, indent=2))
```

## AsyncAPI Specification

Define event-driven APIs for message brokers (Kafka, RabbitMQ, etc.).

```{code-cell} ipython3
asyncapi_spec = {
    "asyncapi": "2.6.0",
    "info": {
        "title": "User Events API",
        "version": "1.0.0"
    },
    "channels": {
        "user/created": {
            "description": "User creation events",
            "publish": {
                "message": {
                    "name": "UserCreated",
                    "payload": {
                        "type": "object",
                        "properties": {
                            "userId": {"type": "string"},
                            "email": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"}
                        }
                    }
                }
            }
        }
    }
}

print("AsyncAPI Specification:")
print(json.dumps(asyncapi_spec, indent=2))
```

## Contract Testing

Use Pact for consumer-driven contract testing between services.

```{code-cell} ipython3
contract_testing_flow = """
Contract Testing Flow:

1. Consumer defines expectations
   - Consumer test creates a Pact file
   - Pact file contains expected requests/responses

2. Publish Pacts to broker
   - Central Pact Broker stores contracts
   - Versioned and tagged

3. Provider verifies contracts
   - Provider runs tests against Pact expectations
   - Publishes verification results

4. Can-I-Deploy check
   - Before deployment, check compatibility
   - Prevents breaking changes
"""

print(contract_testing_flow)

pact_tools = {
    "pact-python": "Python Pact implementation",
    "pact-js": "JavaScript/TypeScript Pact",
    "pact-go": "Go Pact implementation",
    "pactflow": "Hosted Pact Broker"
}

print("\nPact Tools:")
for tool, desc in pact_tools.items():
    print(f"  • {tool}: {desc}")
```

## Mutation Testing

Test the quality of your tests by mutating the code and checking if tests fail.

```{code-cell} ipython3
mutation_tools = {
    "mutmut": "Python mutation testing",
    "Stryker": "JavaScript/TypeScript mutation testing",
    "PITest": "Java mutation testing",
    "go-mutesting": "Go mutation testing"
}

print("Mutation Testing Tools:")
for tool, desc in mutation_tools.items():
    print(f"  • {tool}: {desc}")

print("\nMutation Testing Workflow:")
print("1. Run mutation tool to create code variants")
print("2. Run test suite against each mutant")
print("3. Calculate mutation score (killed mutants / total mutants)")
print("4. Target: 60-80% mutation score for critical code")
```

## Testing Pyramid

Balanced testing strategy for optimal coverage and speed.

```{code-cell} ipython3
testing_pyramid = """
Testing Pyramid:

        /\\        E2E Tests (Few)
       /  \\       - Slow, expensive
      /    \\      - Full user flows
     /------\\     Integration Tests (Some)
    /        \\    - Service boundaries
   /          \\   - Contract tests
  /------------\\  Unit Tests (Many)
 /              \\ - Fast, isolated
/________________\\ - High coverage

Mutation testing ensures unit tests are effective.
Contract tests prevent integration failures.
E2E tests verify critical paths.
"""

print(testing_pyramid)
```

```{code-cell} ipython3
print(f"Contracts & Tests notebook complete! (mode: {run_mode})")
```

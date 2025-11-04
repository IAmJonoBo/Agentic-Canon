# Node.js Service Cookiecutter Template

Production-ready Node.js/TypeScript service template with modern tooling, comprehensive testing, and security scanning.

## Quick Start

```bash
# Using Cookiecutter
cookiecutter templates/node-service

# Or using Agentic Canon CLI
agentic-canon init
# Select "Node.js Service" when prompted
```

## Features

### Core Capabilities

- ✅ **Modern Node.js** - Node.js 20+ with TypeScript
- ✅ **TypeScript** - Full type safety with strict mode
- ✅ **ESM Support** - Native ES modules
- ✅ **Testing** - Vitest for fast unit tests
- ✅ **Linting** - ESLint with TypeScript support
- ✅ **Formatting** - Prettier for consistent code style
- ✅ **Pre-commit Hooks** - Automated quality checks

### CI/CD

- ✅ **GitHub Actions** - Complete CI/CD pipeline
- ✅ **GitLab CI** - Alternative CI/CD support
- ✅ **Multi-version Testing** - Node 18, 20, 22
- ✅ **npm Publishing** - Automated package publishing
- ✅ **Docker Support** - Multi-stage builds

### Security

- ✅ **CodeQL Analysis** - JavaScript/TypeScript SAST
- ✅ **Semgrep** - Pattern-based security scanning
- ✅ **Secret Scanning** - Gitleaks + TruffleHog
- ✅ **npm Audit** - Dependency vulnerability checks
- ✅ **SBOM Generation** - CycloneDX format (optional)
- ✅ **Artifact Signing** - Cosign/Sigstore (optional)

## Template Configuration

### Required Parameters

| Parameter      | Description                    | Example                              |
| -------------- | ------------------------------ | ------------------------------------ |
| `project_name` | Human-readable name            | "Acme Node Service"                  |
| `project_slug` | URL-friendly name (kebab-case) | "acme-node-service"                  |
| `description`  | Short description              | "A production-ready Node.js service" |
| `author_name`  | Your name                      | "Jane Doe"                           |
| `author_email` | Your email                     | "jane@example.com"                   |

### Optional Parameters

| Parameter               | Options                      | Default    | Description              |
| ----------------------- | ---------------------------- | ---------- | ------------------------ |
| `license`               | Apache-2.0, MIT, Proprietary | Apache-2.0 | License type             |
| `node_version`          | 18, 20, 22                   | 20         | Minimum Node.js version  |
| `enable_security_gates` | yes, no                      | yes        | Enable security scanning |
| `enable_sbom_signing`   | yes, no                      | yes        | Enable SBOM + signing    |
| `ci_provider`           | github, gitlab               | github     | CI/CD platform           |

## Generated Project Structure

```
acme-node-service/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Main CI/CD pipeline
│       └── security.yml        # Security scanning
├── src/
│   └── index.ts                # Main entry point
├── tests/
│   └── smoke.test.ts           # Test files
├── .editorconfig               # Editor configuration
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks
├── eslint.config.js            # ESLint configuration
├── package.json                # Project configuration
├── tsconfig.json               # TypeScript configuration
├── vitest.config.ts            # Vitest configuration
└── README.md                   # Project documentation
```

## Usage

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check

# Build for production
npm run build
```

## CI/CD Workflows

**ci.yml** - Main CI/CD Pipeline:

- Install and cache dependencies
- Lint and format checks
- Type checking
- Unit tests with coverage
- Build verification
- Multi-version testing (Node 18, 20, 22)

**security.yml** - Security Scanning:

- npm audit for dependencies
- CodeQL for JavaScript/TypeScript
- Semgrep for security patterns
- Secret scanning (Gitleaks, TruffleHog)
- SBOM generation (optional)
- Artifact signing (optional)

## Best Practices

### Project Structure

1. **Use TypeScript** - Type safety prevents bugs
2. **ESM modules** - Modern JavaScript standard
3. **Comprehensive tests** - ≥80% coverage
4. **Pre-commit hooks** - Catch issues early
5. **Linting + formatting** - Consistent code style

### Testing

```typescript
// tests/example.test.ts
import { describe, it, expect } from "vitest";
import { myFunction } from "../src/index";

describe("myFunction", () => {
  it("should return expected result", () => {
    const result = myFunction("input");
    expect(result).toBe("expected");
  });
});
```

### Adding Dependencies

```bash
# Production dependencies
npm install express

# Development dependencies
npm install -D @types/express

# Update package.json with proper types
```

## Standards Compliance

This template implements:

- ✅ **ESM Standard** - Native ES modules
- ✅ **TypeScript Strict Mode** - Maximum type safety
- ✅ **NIST SSDF** - Secure development framework
- ✅ **OWASP SAMM** - Software assurance maturity
- ✅ **Node.js Best Practices** - Security and performance

## Related Resources

- [Template Creation Runbook](../../runbooks/template-creation-runbook.md)
- [Video Tutorial: Creating Services](../../examples/video-tutorials/02-creating-services.md)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

---

**Part of n00-frontiers - Frontier Software Excellence**  
**Version**: 1.0.0

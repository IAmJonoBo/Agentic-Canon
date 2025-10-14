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

- ✅ **Modern Node.js** – Node.js 20+ baseline with TypeScript strict mode and native ESM
- ✅ **Testing** – Vitest with V8 coverage thresholds set to 80%
- ✅ **Quality Automation** – ESLint, Prettier (single-quote profile), and `npm run typecheck`
- ✅ **Developer Ergonomics** – `tsx`-powered dev loop and curated pre-commit hooks

### CI/CD

- ✅ **GitHub Actions** – `ci.yml` runs on Node.js 18, 20, and 22 using `npm ci`
- ✅ **Quality Gates** – Type checking, linting, formatting checks, build verification, and Vitest execution
- ✅ **Coverage Upload (Optional)** – Codecov upload enabled when `CODECOV_TOKEN` is provided

> ℹ️ GitLab pipelines, Docker images, and npm publishing are not yet scaffolded. See [What's Next](#whats-next) for planned work.

### Security

- ✅ **Dependency Scanning** – `npm audit --audit-level=moderate` (non-blocking) and `npm outdated`
- ✅ **CodeQL** – JavaScript/TypeScript SAST with scheduled weekly runs
- ✅ **Semgrep** – OWASP-aligned rulesets for JS/TS and secrets
- ✅ **Secret Scanning** – TruffleHog against the default branch history

> ℹ️ SBOM generation and artifact signing toggles are placeholders today.

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
| `enable_security_gates` | yes, no                      | yes        | Include security.yml     |
| `enable_sbom_signing`   | yes, no                      | yes        | _Reserved for future SBOM/signing support_ |
| `ci_provider`           | github                       | github     | GitHub Actions only (GitLab planned) |

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
├── .eslintrc.cjs               # ESLint configuration
├── .prettierrc                 # Prettier configuration
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
npm run typecheck

# Build for production
npm run build
```

## CI/CD Workflows

**ci.yml** – Main CI/CD pipeline:

- Install and cache dependencies via `npm ci`
- Type checking, linting, and Prettier verification
- Vitest execution with coverage artifacts
- Build verification across Node.js 18, 20, and 22
- Optional Codecov upload when secrets are present

**security.yml** – Security scanning suite:

- Weekly scheduled and PR-triggered runs
- `npm audit --audit-level=moderate` (non-blocking) and `npm outdated`
- GitHub CodeQL JavaScript analysis
- Semgrep OWASP/security bundle
- TruffleHog git history secret scanning

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

# Update types and lint rules as needed
```

## What's Next

- 🚀 **npm publishing automation** – Pipeline scaffolding is planned but not yet in place.
- 🐳 **Container images** – A Dockerfile and registry workflow are on the roadmap.
- 📦 **SBOM + signing toggle** – `enable_sbom_signing` will wire in CycloneDX generation and Cosign when ready.
- 🌐 **Additional CI providers** – GitLab CI support is a future enhancement.

Track progress in [`Next_Steps.md`](../../Next_Steps.md).

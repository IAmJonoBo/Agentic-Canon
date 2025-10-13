# Express User API

A production-ready Express.js API for user management

## Features

- ✅ TypeScript with strict mode
- ✅ Modern Node.js (v20+)
- ✅ Vitest for testing with coverage
- ✅ ESLint + Prettier for code quality
- ✅ GitHub Actions CI/CD

- ✅ Security scanning (CodeQL, npm audit, secret scanning)

- ✅ SBOM generation and signing

## Getting Started

### Prerequisites

- Node.js 20 or higher
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
# Run in development mode with hot reload
npm run dev

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Build for production
npm run build

# Run production build
npm start
```

### Code Quality

```bash
# Lint code
npm run lint

# Fix lint issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check

# Type check
npm run typecheck
```

## Project Structure

```
.
├── src/           # Source code
├── tests/         # Test files
├── dist/          # Compiled output
├── .github/       # GitHub Actions workflows
└── package.json   # Project configuration
```

## Scripts

- `dev` - Run in development mode with hot reload
- `build` - Compile TypeScript to JavaScript
- `test` - Run tests with coverage
- `test:watch` - Run tests in watch mode
- `start` - Run production build
- `lint` - Check code with ESLint
- `lint:fix` - Fix ESLint issues automatically
- `format` - Format code with Prettier
- `format:check` - Check code formatting
- `typecheck` - Run TypeScript type checking

## CI/CD

This project uses GitHub Actions for continuous integration:

- **CI Pipeline**: Runs on push and pull requests
  - Type checking
  - Linting
  - Format checking
  - Unit tests with coverage
  - Multi-version Node.js testing (18, 20, 21)

- **Security Pipeline**: Runs weekly and on changes
  - Dependency vulnerability scanning (npm audit)
  - Static analysis (CodeQL)
  - Secret scanning (TruffleHog)

## License

MIT

## Author

Agentic Canon Team <team@agenticcanon.dev>

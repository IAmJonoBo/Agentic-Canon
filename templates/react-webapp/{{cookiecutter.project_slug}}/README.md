# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Features

- ✅ React 18 with TypeScript
- ✅ Vite for fast development and optimized builds
- ✅ Vitest for unit testing
  {% if cookiecutter.include_storybook == "yes" %}
- ✅ Storybook for component development
  {% endif %}
  {% if cookiecutter.include_e2e_tests == "yes" %}
- ✅ Playwright for E2E testing
  {% endif %}
  {% if cookiecutter.enable_accessibility_tests == "yes" %}
- ✅ Accessibility testing with axe
  {% endif %}
- ✅ ESLint + Prettier for code quality
- ✅ GitHub Actions CI/CD

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run unit tests
npm test

# Run unit tests with UI
npm run test:ui
{% if cookiecutter.include_e2e_tests == "yes" %}
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
{% endif %}
```

{% if cookiecutter.include_storybook == "yes" %}

### Storybook

```bash
# Start Storybook dev server
npm run storybook

# Build Storybook
npm run build-storybook
```

{% endif %}

### Code Quality

```bash
# Lint code
npm run lint

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
├── src/
│   ├── components/    # React components
│   ├── App.tsx        # Main app component
│   └── main.tsx       # Entry point
{% if cookiecutter.include_e2e_tests == "yes" %}
├── tests/
│   └── e2e/          # E2E tests
{% endif %}
{% if cookiecutter.include_storybook == "yes" %}
├── .storybook/       # Storybook configuration
{% endif %}
└── .github/
    └── workflows/    # CI/CD workflows
```

## CI/CD

This project uses GitHub Actions:

- **CI Pipeline**: Runs on every push and PR
  - Type checking
  - Linting
  - Format checking
  - Unit tests
  - Production build
    {% if cookiecutter.include_e2e_tests == "yes" %}
- **E2E Tests**: Runs on every push and PR
  - Cross-browser testing (Chrome, Firefox, Safari)
  - Visual regression testing
    {% endif %}
    {% if cookiecutter.include_storybook == "yes" %}
- **Storybook**: Deploys to GitHub Pages on main branch
  {% endif %}

## License

{{cookiecutter.license}}

## Author

{{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

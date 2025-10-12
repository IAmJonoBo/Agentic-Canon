# React Dashboard WebApp Example

Production-ready analytics dashboard showcasing the Agentic Canon React template in action.

## Features

- ⚛️ React 18 + TypeScript with Vite
- 📈 Interactive charts powered by Recharts and TanStack Query
- 🔐 Lightweight auth/state management with Zustand
- 🌗 Tailwind CSS theming with dark/light toggle
- 📚 Storybook with accessibility testing enabled
- ✅ Unit tests (Vitest) & Playwright E2E coverage
- 🚀 GitHub Actions pipelines for CI, security, and Storybook deploys

## Getting Started

```bash
cd examples/projects/react-dashboard
npm install
npm run dev
```

Visit http://localhost:5173 to view the dashboard, http://localhost:6006 for Storybook.

Run tests and checks:

```bash
npm run lint
npm run typecheck
npm run test
npm run test:e2e      # Requires Playwright browsers (npx playwright install)
```

## Project Structure

```
react-dashboard/
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   ├── charts/
│   │   ├── layout/
│   │   └── ui/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── store/
│   └── types/
├── tests/
│   ├── unit/
│   └── e2e/
├── .github/workflows/
├── .storybook/
├── package.json
└── vite.config.ts
```

## CI/CD

- `React Dashboard • CI` – linting, type checking, unit tests, build
- `React Dashboard • Security` – weekly dependency audit
- `React Dashboard • Storybook` – builds Storybook and deploys to GitHub Pages

## Credentials

For the demo login flow use any `@example.com` email (e.g. `engineer@example.com`) with any password.

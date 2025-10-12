# React Dashboard WebApp – Working Example

A complete analytics dashboard demonstrating how to build a modern, production-ready frontend with the Agentic Canon React template.

## Overview

This example application highlights:

- **Realtime delivery metrics** surfaced with TanStack Query
- **Interactive charts** powered by Recharts
- **Operational insights** with predictive analytics mock data
- **Team directory and reports** for engineering stakeholders
- **Storybook-driven component development** with accessibility checks
- **End-to-end coverage** using Playwright and Vitest
- **Responsive layout** with Tailwind CSS + shadcn-inspired primitives

Use it as a reference implementation, a demo for stakeholders, or the starting point for your own dashboard.

## Quick Start

```bash
cd examples/projects/react-dashboard
npm install
npm run dev
```

The app runs on http://localhost:5173. Dashboard telemetry is mocked and refreshes periodically; toggle realtime behaviour from the settings panel.

### Storybook

```bash
npm run storybook
```

Access Storybook at http://localhost:6006 to browse UI components with accessibility tooling enabled by default.

### Tests

| Command             | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `npm run test`      | Vitest unit tests (jsdom) + Testing Library                            |
| `npm run test:e2e`  | Playwright smoke suite (requires `npx playwright install --with-deps`) |
| `npm run lint`      | ESLint with TypeScript support                                         |
| `npm run typecheck` | TypeScript compiler in no-emit mode                                    |

## Architecture

- **State management** – `@tanstack/react-query` for async data + `zustand` for local UI state
- **UI primitives** – Tailwind CSS, class-variance-authority, and Radix UI patterns for unstyled components
- **Charts** – Recharts for simple line/bar charts with tooltips & responsive layout
- **Routing** – `react-router-dom` with lazy-loaded pages
- **Auth flow** – Demo login that accepts `@example.com` addresses and persists a pseudo-token in memory
- **Realtime simulation** – Query invalidation loop that refreshes metrics every 12 seconds when enabled

## Directory Guide

```
src/
├── components/
│   ├── layout/        # Header, sidebar, shell layout
│   ├── dashboard/     # Feature widgets (metric cards, activity feed, team panel)
│   ├── charts/        # Recharts wrappers
│   └── ui/            # Reusable primitives (button, card, badge, avatar)
├── hooks/             # Custom hooks (auth)
├── services/          # Mock API with latency simulation
├── store/             # Zustand stores for dashboard + settings
├── pages/             # Route-level pages loaded lazily
└── types/             # Shared TypeScript contracts
```

## CI/CD Workflows

Located under `.github/workflows/`:

1. **React Dashboard • CI** – installs dependencies, lints, type checks, runs Vitest, builds production bundle.
2. **React Dashboard • Security** – weekly scheduled `npm audit` for dependency health.
3. **React Dashboard • Storybook** – builds Storybook and publishes to GitHub Pages (supports private repos via restricted pages).

## Implementation Tips

- Replace the mock API in `src/services/api.ts` with real backend calls (REST, GraphQL, or gRPC-web) when integrating.
- Hook up telemetry sources via TanStack Query; set `staleTime`/`refetchInterval` to match your data characteristics.
- Pair this frontend with the observability dashboards in `examples/dashboards` for a full DevEx observability stack.
- When enabling authentication, swap the demo `authenticate` function for your identity provider and store tokens in secure cookies.

## Screenshots & Assets

The `public/assets/` folder is reserved for marketing assets and favicons. Add diagrams or UI captures here when productizing.

## License

MIT – inherit from the repository, or replace with your organisation’s license before distribution.

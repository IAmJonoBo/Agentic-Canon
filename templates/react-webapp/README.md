# React WebApp Cookiecutter Template

Production-ready React application template with Vite, TypeScript, Storybook, and Playwright for E2E testing.

## Quick Start

```bash
# Using Cookiecutter
cookiecutter templates/react-webapp

# Or using Agentic Canon CLI
agentic-canon init
# Select "React WebApp" when prompted
```

## Features

### Core Capabilities

- ✅ **React 18** - Latest React with concurrent features
- ✅ **TypeScript** - Full type safety
- ✅ **Vite** - Lightning-fast build tool
- ✅ **Component Library** - Reusable UI components
- ✅ **CSS Modules** - Scoped styling
- ✅ **Testing** - Vitest for unit tests

### Development Experience

- ✅ **Storybook 8** - Component development with the Vite builder (optional)
- ✅ **Hot Module Replacement** - Instant feedback
- ✅ **ESLint + Prettier** - Code quality (single quotes by default)
- ✅ **Pre-commit Hooks** - Automated checks

### Testing & Quality

- ✅ **Unit Tests** - Vitest + React Testing Library
- ✅ **E2E Tests** - Playwright (optional)
- ✅ **Accessibility Tests** - axe-core (optional)
- ✅ **Visual Regression** - Playwright screenshots
- ✅ **Performance Budgets** - Lighthouse CI

### CI/CD

- ✅ **GitHub Actions** - Complete CI/CD
- ✅ **GitLab CI** - Alternative support
- ✅ **Storybook Deployment** - GitHub Pages
- ✅ **Bundle Analysis** - Size tracking

## Template Configuration

### Required Parameters

| Parameter      | Description         | Example                                |
| -------------- | ------------------- | -------------------------------------- |
| `project_name` | Human-readable name | "Acme React App"                       |
| `project_slug` | URL-friendly name   | "acme-react-app"                       |
| `description`  | Short description   | "A production-ready React application" |
| `author_name`  | Your name           | "Jane Doe"                             |
| `author_email` | Your email          | "jane@example.com"                     |

### Optional Parameters

| Parameter                    | Options                      | Default    | Description            |
| ---------------------------- | ---------------------------- | ---------- | ---------------------- |
| `license`                    | Apache-2.0, MIT, Proprietary | Apache-2.0 | License type           |
| `include_storybook`          | yes, no                      | yes        | Include Storybook      |
| `include_e2e_tests`          | yes, no                      | yes        | Include Playwright E2E |
| `enable_accessibility_tests` | yes, no                      | yes        | Include a11y tests     |
| `ci_provider`                | github, gitlab               | github     | CI/CD platform         |

## Generated Project Structure

```
acme-react-app/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Main CI/CD
│       ├── e2e.yml             # E2E tests
│       └── storybook-pages.yml # Storybook deployment
├── .storybook/                 # Storybook configuration
│   ├── main.ts
│   └── preview.ts
├── src/
│   ├── components/             # React components
│   │   ├── Button.tsx
│   │   └── Button.stories.tsx
│   ├── App.tsx                 # Main app component
│   └── main.tsx                # Entry point
├── tests/
│   └── e2e/                    # Playwright E2E tests
│       └── smoke.spec.ts
├── index.html                  # HTML entry
├── package.json                # Dependencies
├── playwright.config.ts        # Playwright config
├── tsconfig.json               # TypeScript config
├── vite.config.ts              # Vite config
└── README.md                   # Documentation
```

## Usage

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# → http://localhost:5173

# Run Storybook (if included)
npm run storybook
# → http://localhost:6006

# Run unit tests
npm test

# Run E2E tests (if included)
npm run test:e2e

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and format
npm run lint
npm run format
```

## Storybook 8 Upgrade Notes

- The generated project pins Storybook 8.6 with the Vite builder and runs it via the
  native `storybook dev` CLI (`npm run storybook`). This avoids broken symlinks in
  CI environments where `node_modules/.bin` is cached between runs.
- Node.js 20 LTS and newer (including Node 22) are fully supported. Ensure your
  local environment meets the `"node": ">=18.0.0"` engines requirement before
  installing dependencies.
- When upgrading Storybook yourself, keep the `storybook dev -p 6006` script shape
  so shared CI workflows and the validation pipeline continue to work without
  modification.

## Development

### Creating Components

```tsx
// src/components/Button.tsx
import React from "react";
import styles from "./Button.module.css";

interface ButtonProps {
  label: string;
  onClick?: () => void;
  variant?: "primary" | "secondary";
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = "primary",
}) => {
  return (
    <button className={styles[variant]} onClick={onClick}>
      {label}
    </button>
  );
};
```

### Storybook Stories

```tsx
// src/components/Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    label: "Primary Button",
    variant: "primary",
  },
};
```

### E2E Tests

```typescript
// tests/e2e/smoke.spec.ts
import { test, expect } from "@playwright/test";

test("homepage loads successfully", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Acme React App/);
});

test("button click works", async ({ page }) => {
  await page.goto("/");
  await page.click('button:has-text("Click me")');
  await expect(page.locator(".result")).toHaveText("Clicked!");
});
```

## CI/CD Workflows

**ci.yml** - Main Pipeline:

- Install and cache dependencies
- Lint and type check
- Unit tests with coverage
- Build verification
- Bundle size analysis

**e2e.yml** - E2E Tests:

- Install browsers
- Run Playwright tests
- Upload test results
- Screenshot comparisons

**storybook-pages.yml** - Storybook:

- Build Storybook
- Deploy to GitHub Pages
- Accessibility checks

## Best Practices

### Component Design

1. **TypeScript Props** - Always type component props
2. **Composition** - Compose from smaller components
3. **Accessibility** - ARIA labels and keyboard support
4. **Performance** - Lazy loading and code splitting
5. **Testing** - Unit + E2E + visual tests

### State Management

```tsx
// Use hooks for local state
const [count, setCount] = useState(0);

// Use context for shared state
const ThemeContext = createContext<Theme>("light");

// Consider libraries for complex state
// - Zustand (lightweight)
// - Redux Toolkit (complex apps)
// - TanStack Query (server state)
```

### Performance

```tsx
// Code splitting with lazy
const Dashboard = lazy(() => import("./Dashboard"));

// Memoization
const MemoizedComponent = React.memo(MyComponent);

// Use useMemo and useCallback
const expensiveValue = useMemo(() => computeExpensive(data), [data]);
const handleClick = useCallback(() => doSomething(), []);
```

## Standards Compliance

This template implements:

- ✅ **React Best Practices** - Hooks, functional components
- ✅ **WCAG 2.2 AA** - Accessibility standards
- ✅ **Web Vitals** - Performance metrics (LCP, FID, CLS)
- ✅ **Security Headers** - CSP, HSTS, etc.
- ✅ **SEO Best Practices** - Meta tags, semantic HTML

## Related Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Storybook Documentation](https://storybook.js.org/docs)
- [Playwright Documentation](https://playwright.dev/)

---

**Part of Agentic Canon - Frontier Software Excellence**  
**Version**: 1.0.0

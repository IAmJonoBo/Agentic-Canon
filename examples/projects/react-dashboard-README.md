# React Dashboard WebApp Example

This is a complete example of a production-ready React dashboard web application generated using Agentic Canon.

## Overview

A modern dashboard application for analytics and data visualization with:
- Multiple dashboard views
- Real-time data updates
- Interactive charts and graphs
- User authentication
- Responsive design
- Component library (Storybook)
- E2E tests
- CI/CD pipelines

## Features

- **React 18** - Latest React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching and caching
- **Zustand** - Lightweight state management
- **Recharts** - Composable charting library
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality component library
- **Vitest** - Fast unit testing
- **Playwright** - E2E testing
- **Storybook** - Component development and documentation
- **GitHub Actions** - Automated CI/CD

## Quick Start

### Prerequisites

- Node.js 20+
- Modern web browser

### Installation

```bash
# Clone this example
git clone <repo-url>
cd react-dashboard

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

### Access the Application

- **App**: http://localhost:5173
- **Storybook**: http://localhost:6006 (run `npm run storybook`)

## Project Structure

```
react-dashboard/
├── src/
│   ├── main.tsx                 # Application entry point
│   ├── App.tsx                  # Root component
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Header.tsx       # Application header
│   │   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   │   ├── Footer.tsx       # Application footer
│   │   │   └── Layout.tsx       # Main layout wrapper
│   │   ├── dashboard/
│   │   │   ├── MetricCard.tsx   # Metric display card
│   │   │   ├── Chart.tsx        # Chart wrapper
│   │   │   ├── DataTable.tsx    # Data table component
│   │   │   └── Widget.tsx       # Dashboard widget
│   │   ├── charts/
│   │   │   ├── LineChart.tsx    # Line chart
│   │   │   ├── BarChart.tsx     # Bar chart
│   │   │   ├── PieChart.tsx     # Pie chart
│   │   │   └── AreaChart.tsx    # Area chart
│   │   └── auth/
│   │       ├── LoginForm.tsx    # Login form
│   │       ├── RegisterForm.tsx # Registration form
│   │       └── ProtectedRoute.tsx # Auth guard
│   ├── pages/
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── Analytics.tsx        # Analytics page
│   │   ├── Reports.tsx          # Reports page
│   │   ├── Settings.tsx         # Settings page
│   │   ├── Login.tsx            # Login page
│   │   └── NotFound.tsx         # 404 page
│   ├── hooks/
│   │   ├── useAuth.ts           # Authentication hook
│   │   ├── useMetrics.ts        # Metrics data hook
│   │   ├── useWebSocket.ts      # WebSocket hook
│   │   └── useTheme.ts          # Theme management
│   ├── store/
│   │   ├── authStore.ts         # Auth state
│   │   ├── dashboardStore.ts    # Dashboard state
│   │   └── settingsStore.ts     # Settings state
│   ├── services/
│   │   ├── api.ts               # API client
│   │   ├── auth.ts              # Auth service
│   │   └── metrics.ts           # Metrics service
│   ├── lib/
│   │   ├── utils.ts             # Utility functions
│   │   ├── cn.ts                # Class name helper
│   │   └── constants.ts         # App constants
│   ├── types/
│   │   ├── index.ts             # Type definitions
│   │   ├── api.ts               # API types
│   │   └── dashboard.ts         # Dashboard types
│   └── styles/
│       ├── globals.css          # Global styles
│       └── tailwind.css         # Tailwind imports
├── tests/
│   ├── unit/
│   │   ├── components/          # Component tests
│   │   ├── hooks/               # Hook tests
│   │   └── utils/               # Utility tests
│   └── e2e/
│       ├── auth.spec.ts         # Auth E2E tests
│       ├── dashboard.spec.ts    # Dashboard E2E tests
│       └── navigation.spec.ts   # Navigation tests
├── .storybook/
│   ├── main.ts                  # Storybook config
│   ├── preview.ts               # Story preview config
│   └── preview-head.html        # Custom head content
├── stories/
│   ├── Button.stories.tsx       # Button stories
│   ├── Card.stories.tsx         # Card stories
│   ├── Chart.stories.tsx        # Chart stories
│   └── ...
├── public/
│   ├── assets/                  # Static assets
│   └── favicon.ico
├── .github/workflows/           # CI/CD pipelines
├── playwright.config.ts         # Playwright configuration
├── vite.config.ts               # Vite configuration
├── vitest.config.ts             # Vitest configuration
├── tailwind.config.js           # Tailwind configuration
├── tsconfig.json                # TypeScript configuration
├── package.json
├── .env.example
└── README.md
```

## Features Walkthrough

### Dashboard Overview

The main dashboard displays:
- **Key metrics**: Revenue, users, conversion rate, active sessions
- **Trend charts**: Line charts showing metrics over time
- **Data tables**: Recent transactions, user activity
- **Widgets**: Customizable dashboard widgets
- **Real-time updates**: Live data via WebSocket connections

### Authentication

Secure user authentication with:
- Login/logout functionality
- Registration with validation
- JWT token management
- Protected routes
- Session persistence
- Password reset flow

### Data Visualization

Rich charting capabilities:
- **Line Charts**: Time-series data, trends
- **Bar Charts**: Comparisons, categorical data
- **Pie Charts**: Proportions, distributions
- **Area Charts**: Cumulative trends
- **Interactive tooltips**: Detailed data on hover
- **Responsive**: Adapts to screen size

### State Management

Efficient state handling:
- **Zustand stores**: Lightweight, no boilerplate
- **TanStack Query**: Server state, caching, background updates
- **Local state**: Component-level state with hooks
- **Persistent state**: LocalStorage integration

### Theming

Dark and light mode support:
- Toggle between themes
- Persistent theme selection
- Tailwind CSS dark mode
- Accessible color contrasts

## Development

### Running Locally

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e:ui

# Run Storybook
npm run storybook

# Build Storybook
npm run build-storybook

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run typecheck
```

### Component Development

Using Storybook for isolated component development:

```bash
# Start Storybook
npm run storybook

# Create a new component story
cat > src/stories/NewComponent.stories.tsx << 'EOF'
import type { Meta, StoryObj } from '@storybook/react';
import { NewComponent } from '../components/NewComponent';

const meta: Meta<typeof NewComponent> = {
  title: 'Components/NewComponent',
  component: NewComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof NewComponent>;

export const Default: Story = {
  args: {
    // component props
  },
};
EOF
```

### Environment Variables

```env
# API Configuration
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000

# Authentication
VITE_AUTH_DOMAIN=auth.example.com
VITE_CLIENT_ID=your-client-id

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_REALTIME=true

# Analytics (optional)
VITE_GA_TRACKING_ID=G-XXXXXXXXXX
VITE_SENTRY_DSN=https://...

# Environment
VITE_ENVIRONMENT=development
```

## Configuration

### Vite Configuration

Key Vite settings in `vite.config.ts`:
- Build optimization
- Plugin configuration (React, PWA)
- Development server proxy
- Alias resolution
- Environment variable handling

### Tailwind Configuration

Customizations in `tailwind.config.js`:
- Custom color palette
- Extended spacing scale
- Custom breakpoints
- Plugin configuration
- Dark mode setup

### TypeScript Configuration

Type checking settings:
- Strict mode enabled
- Path aliases
- JSX configuration
- Library types

## Deployment

### Static Hosting

Build and deploy to static hosts:

```bash
# Build for production
npm run build

# Output is in dist/ directory
```

**Supported platforms:**
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Docker

```bash
# Build image
docker build -t react-dashboard:latest .

# Run container
docker run -p 8080:80 react-dashboard:latest

# Using docker-compose
docker-compose up -d
```

### Kubernetes

```bash
# Apply configurations
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment
kubectl get pods
kubectl logs -f deployment/react-dashboard
```

## Testing Strategy

### Unit Tests

Test components and utilities:

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

### Integration Tests

Test component interactions:

```typescript
import { render, screen } from '@testing-library/react';
import { Dashboard } from './Dashboard';

describe('Dashboard', () => {
  it('displays metrics after loading', async () => {
    render(<Dashboard />);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Total Revenue')).toBeInTheDocument();
    });
  });
});
```

### E2E Tests

Test user workflows with Playwright:

```typescript
import { test, expect } from '@playwright/test';

test('user can login and view dashboard', async ({ page }) => {
  await page.goto('/');
  
  // Login
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  // Verify dashboard loads
  await expect(page.locator('h1')).toContainText('Dashboard');
  await expect(page.locator('[data-testid="metric-card"]')).toBeVisible();
});
```

### Visual Regression

Storybook provides visual testing:
- Chromatic integration
- Snapshot testing
- Cross-browser testing
- Responsive testing

## CI/CD Pipeline

### GitHub Actions Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Lint and format check
   - Type checking
   - Unit tests with coverage
   - Build application
   - Upload build artifacts

2. **E2E Tests** (`.github/workflows/e2e.yml`)
   - Install Playwright browsers
   - Build application
   - Run E2E tests
   - Upload test results and screenshots

3. **Storybook** (`.github/workflows/storybook.yml`)
   - Build Storybook
   - Deploy to GitHub Pages
   - Run visual regression tests

4. **Deploy** (`.github/workflows/deploy.yml`)
   - Build production bundle
   - Deploy to hosting platform
   - Run smoke tests
   - Notify on deployment

### Quality Gates

All PRs must pass:
- ✅ Linting (ESLint, Prettier)
- ✅ Type checking (TypeScript)
- ✅ Unit tests (≥80% coverage)
- ✅ E2E tests passing
- ✅ Build successful
- ✅ Bundle size within budget
- ✅ Accessibility checks (axe)

## Performance

### Optimization Techniques

- **Code splitting**: Route-based lazy loading
- **Tree shaking**: Remove unused code
- **Asset optimization**: Image compression, lazy loading
- **Caching**: Service worker, HTTP caching
- **Prefetching**: Critical resources
- **Virtual scrolling**: Large lists
- **Memoization**: Expensive computations

### Bundle Size

Target bundle sizes:
- **Initial JS**: < 200KB gzipped
- **Initial CSS**: < 50KB gzipped
- **Lazy chunks**: < 100KB each
- **Images**: WebP format, responsive
- **Fonts**: Subset, preload

### Performance Metrics

Core Web Vitals targets:
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **FCP** (First Contentful Paint): < 1.8s
- **TTI** (Time to Interactive): < 3.8s

### Monitoring

```typescript
// Web Vitals reporting
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);

// Custom performance marks
performance.mark('data-fetch-start');
// ... fetch data
performance.mark('data-fetch-end');
performance.measure('data-fetch', 'data-fetch-start', 'data-fetch-end');
```

## Accessibility

### WCAG 2.1 Level AA Compliance

- ✅ **Semantic HTML**: Proper element usage
- ✅ **Keyboard navigation**: Full keyboard access
- ✅ **Screen reader support**: ARIA labels, roles
- ✅ **Color contrast**: 4.5:1 minimum
- ✅ **Focus indicators**: Visible focus states
- ✅ **Alt text**: All images described
- ✅ **Form labels**: Associated labels
- ✅ **Error messages**: Clear, accessible
- ✅ **Responsive**: Mobile-friendly

### Testing Accessibility

```bash
# Run axe accessibility tests
npm run test:a11y

# Lighthouse audit
lighthouse http://localhost:5173 --view

# Manual testing with screen reader
# - VoiceOver (macOS)
# - NVDA (Windows)
# - JAWS (Windows)
```

## Security

### Implemented Measures

- ✅ **XSS Prevention**: React auto-escaping, DOMPurify for HTML
- ✅ **CSRF Protection**: Token-based protection
- ✅ **Content Security Policy**: Strict CSP headers
- ✅ **HTTPS Only**: Force secure connections
- ✅ **Secure Headers**: HSTS, X-Frame-Options, etc.
- ✅ **Input Validation**: Client and server-side
- ✅ **Dependency Scanning**: Automated vulnerability checks
- ✅ **Secret Management**: Environment variables
- ✅ **Authentication**: JWT with secure storage
- ✅ **Authorization**: Role-based access control

### Best Practices

1. **Never expose secrets** in client code
2. **Validate all inputs** on client and server
3. **Use HTTPS** in production always
4. **Keep dependencies updated** regularly
5. **Implement CSP** to prevent XSS
6. **Use SRI** for external resources
7. **Sanitize HTML** before rendering

## Troubleshooting

### Common Issues

**Build errors**
```bash
# Clear cache and reinstall
rm -rf node_modules dist .vite
npm install
npm run build
```

**TypeScript errors**
```bash
# Regenerate types
npm run typecheck

# Check for conflicting versions
npm ls typescript
```

**Test failures**
```bash
# Update snapshots
npm test -- -u

# Run specific test
npm test -- Button.test.tsx

# Debug mode
npm test -- --inspect-brk
```

**Playwright issues**
```bash
# Reinstall browsers
npx playwright install

# Run with UI
npm run test:e2e:ui

# Debug specific test
npx playwright test --debug auth.spec.ts
```

**Storybook not loading**
```bash
# Clear cache
rm -rf node_modules/.cache

# Rebuild
npm run build-storybook
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## License

This example is part of Agentic Canon and is licensed under [Apache-2.0](../../LICENSE).

## Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TanStack Query](https://tanstack.com/query/)
- [Playwright](https://playwright.dev/)
- [Storybook](https://storybook.js.org/)
- [Agentic Canon Templates](../../templates/)

## Support

For questions or issues:
1. Check this README and documentation
2. Search [existing issues](https://github.com/IAmJonoBo/Agentic-Canon/issues)
3. Ask in [discussions](https://github.com/IAmJonoBo/Agentic-Canon/discussions)
4. Open a new issue if needed

## Roadmap

Future enhancements:
- [ ] Progressive Web App (PWA) support
- [ ] Offline mode with service workers
- [ ] Real-time collaborative features
- [ ] Advanced data export (PDF, Excel)
- [ ] Custom widget marketplace
- [ ] Multi-language support (i18n)
- [ ] Advanced filtering and search
- [ ] Data import wizards

---

**Generated using Agentic Canon** - Production-ready project scaffolding

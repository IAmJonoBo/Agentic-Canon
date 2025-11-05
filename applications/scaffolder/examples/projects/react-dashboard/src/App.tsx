import { Suspense, lazy } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

const DashboardPage = lazy(() => import('./pages/Dashboard'));
const AnalyticsPage = lazy(() => import('./pages/Analytics'));
const ReportsPage = lazy(() => import('./pages/Reports'));
const SettingsPage = lazy(() => import('./pages/Settings'));
const LoginPage = lazy(() => import('./pages/Login'));
const TeamPage = lazy(() => import('./pages/Team'));
const NotFoundPage = lazy(() => import('./pages/NotFound'));

export function App() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground">
          Loading dashboard…
        </div>
      }
    >
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/team" element={<TeamPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </Suspense>
  );
}

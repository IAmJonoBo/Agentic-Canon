import type { ActivityEvent, Metric, TrendPoint, UserProfile } from '../types/dashboard';

type DelayOptions = { min?: number; max?: number };

const mockDelay = (options: DelayOptions = {}) =>
  new Promise((resolve) => {
    const { min = 150, max = 400 } = options;
    const timeout = Math.floor(Math.random() * (max - min + 1)) + min;
    setTimeout(resolve, timeout);
  });

export const fetchMetrics = async (): Promise<Metric[]> => {
  await mockDelay();
  return [
    { id: 'deploys', label: 'Deployments', value: 28, change: 12.3 },
    { id: 'lead-time', label: 'Lead Time (hrs)', value: 4.6, change: -8.1 },
    { id: 'mttr', label: 'MTTR (hrs)', value: 1.2, change: -14.5 },
    { id: 'cfr', label: 'Change Failure Rate', value: 4.1, change: -2.0 },
  ];
};

export const fetchTrends = async (): Promise<TrendPoint[]> => {
  await mockDelay();
  const now = new Date();
  return Array.from({ length: 8 }).map((_, index) => {
    const date = new Date(now);
    date.setDate(now.getDate() - (7 - index));
    return {
      date: date.toISOString().slice(0, 10),
      deployments: Math.floor(18 + Math.random() * 10),
      incidents: Math.floor(Math.random() * 3),
      leadTime: Number((3 + Math.random() * 2).toFixed(2)),
    };
  });
};

export const fetchActivityFeed = async (): Promise<ActivityEvent[]> => {
  await mockDelay({ min: 200, max: 550 });
  return [
    {
      id: '1',
      title: 'Checkout service deployed',
      description: 'Deployment #842 completed successfully with zero incidents.',
      timestamp: new Date().toISOString(),
      severity: 'low',
    },
    {
      id: '2',
      title: 'Database migration',
      description: 'Migration 2024-05-01_23 executed in 1m 22s.',
      timestamp: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
      severity: 'medium',
    },
    {
      id: '3',
      title: 'Incident resolved',
      description: 'Critical alert on payments service resolved in 17 minutes.',
      timestamp: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
      severity: 'high',
    },
  ];
};

export const fetchTeam = async (): Promise<UserProfile[]> => {
  await mockDelay();
  return [
    {
      id: 'u1',
      name: 'Priya Gupta',
      email: 'priya.gupta@example.com',
      role: 'Engineer',
    },
    {
      id: 'u2',
      name: 'Miguel Alvarez',
      email: 'miguel.alvarez@example.com',
      role: 'SRE',
    },
    {
      id: 'u3',
      name: 'Jun Park',
      email: 'jun.park@example.com',
      role: 'Product Manager',
    },
  ];
};

export const authenticate = async (email: string, password: string): Promise<string> => {
  await mockDelay({ min: 300, max: 600 });
  // In production call real auth service; this is demo logic only.
  if (!email || !password) {
    throw new Error('Missing credentials');
  }
  if (!email.endsWith('@example.com')) {
    throw new Error('Invalid corporate email');
  }
  return btoa(`${email}:${Date.now()}`);
};

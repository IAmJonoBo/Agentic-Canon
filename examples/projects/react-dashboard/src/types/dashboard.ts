export interface Metric {
  id: string;
  label: string;
  value: number;
  change: number;
}

export interface ActivityEvent {
  id: string;
  title: string;
  description: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}

export interface TrendPoint {
  date: string;
  deployments: number;
  incidents: number;
  leadTime: number;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'Engineer' | 'Product Manager' | 'SRE';
  avatar?: string;
}

import { create } from 'zustand';
import type { Metric } from '../types/dashboard';

type DashboardStore = {
  timeframe: '7d' | '14d' | '30d';
  selectedMetric: Metric['id'] | null;
  setTimeframe: (timeframe: DashboardStore['timeframe']) => void;
  setSelectedMetric: (metricId: Metric['id']) => void;
};

export const useDashboardStore = create<DashboardStore>((set) => ({
  timeframe: '7d',
  selectedMetric: null,
  setTimeframe: (timeframe) => set({ timeframe }),
  setSelectedMetric: (selectedMetric) => set({ selectedMetric }),
}));

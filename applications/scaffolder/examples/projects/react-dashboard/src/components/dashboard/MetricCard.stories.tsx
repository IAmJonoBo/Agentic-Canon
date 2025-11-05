import type { Meta, StoryObj } from '@storybook/react';
import { MetricCard } from './MetricCard';

const meta: Meta<typeof MetricCard> = {
  component: MetricCard,
  title: 'Dashboard/MetricCard',
  args: {
    metric: {
      id: 'deploys',
      label: 'Deployments',
      value: 32,
      change: 8.2,
    },
  },
};

export default meta;

type Story = StoryObj<typeof MetricCard>;

export const Default: Story = {};

export const NegativeTrend: Story = {
  args: {
    metric: {
      id: 'mttr',
      label: 'MTTR (hours)',
      value: 1.4,
      change: -16.3,
    },
  },
};

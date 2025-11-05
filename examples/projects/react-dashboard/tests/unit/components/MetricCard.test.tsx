import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MetricCard } from '../../../src/components/dashboard/MetricCard';
import type { Metric } from '../../../src/types';

const metric: Metric = {
  id: 'deploys',
  label: 'Deployments',
  value: 42,
  change: 11.5,
};

describe('MetricCard', () => {
  it('renders metric information', () => {
    render(<MetricCard metric={metric} />);

    expect(screen.getByText(/Deployments/i)).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
    expect(screen.getByText('+11.5%')).toBeInTheDocument();
  });

  it('invokes callback when clicked', () => {
    const onSelect = vi.fn();
    render(<MetricCard metric={metric} onSelect={onSelect} />);

    screen.getByRole('button').click();
    expect(onSelect).toHaveBeenCalledWith(metric);
  });
});

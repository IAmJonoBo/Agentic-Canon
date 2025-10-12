import { TrendingDown, TrendingUp } from 'lucide-react';
import type { Metric } from '../../types/dashboard';
import { Card, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Badge } from '../ui/badge';

interface MetricCardProps {
  metric: Metric;
  onSelect?: (metric: Metric) => void;
  isActive?: boolean;
}

export function MetricCard({ metric, onSelect, isActive }: MetricCardProps) {
  const isPositive = metric.change >= 0;
  const TrendIcon = isPositive ? TrendingUp : TrendingDown;

  return (
    <button
      type="button"
      onClick={() => onSelect?.(metric)}
      className="w-full text-left"
      aria-pressed={isActive}
    >
      <Card className={isActive ? 'border-primary shadow-md ring-2 ring-primary/20' : ''}>
        <CardHeader className="flex flex-row items-start justify-between">
          <div>
            <CardTitle>{metric.label}</CardTitle>
            <CardDescription>Last 7 days</CardDescription>
          </div>
          <Badge
            variant={isPositive ? 'default' : 'destructive'}
            className="flex items-center gap-1"
          >
            <TrendIcon className="h-3.5 w-3.5" />
            {metric.change > 0 ? '+' : ''}
            {metric.change}%
          </Badge>
        </CardHeader>
        <div className="px-6 pb-4 text-3xl font-semibold">{metric.value}</div>
      </Card>
    </button>
  );
}

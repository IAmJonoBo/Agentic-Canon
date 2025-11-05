import { useQuery } from '@tanstack/react-query';
import { fetchMetrics, fetchTrends, fetchActivityFeed, fetchTeam } from '../services/api';
import { MetricCard } from '../components/dashboard/MetricCard';
import { TrendChart } from '../components/charts/TrendChart';
import { ActivityFeed } from '../components/dashboard/ActivityFeed';
import { TeamPanel } from '../components/dashboard/TeamPanel';
import { RealtimeToggle } from '../components/dashboard/RealtimeToggle';
import { useDashboardStore } from '../store/dashboardStore';

export default function DashboardPage() {
  const { data: metrics = [] } = useQuery({ queryKey: ['metrics'], queryFn: fetchMetrics });
  const { data: trends = [] } = useQuery({ queryKey: ['trends'], queryFn: fetchTrends });
  const { data: events = [] } = useQuery({ queryKey: ['activity'], queryFn: fetchActivityFeed });
  const { data: team = [] } = useQuery({ queryKey: ['team'], queryFn: fetchTeam });
  const setSelectedMetric = useDashboardStore((state) => state.setSelectedMetric);
  const selectedMetric = useDashboardStore((state) => state.selectedMetric);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Engineering operations</h1>
          <p className="text-sm text-muted-foreground">
            Key delivery and reliability metrics refreshed every few seconds.
          </p>
        </div>
        <RealtimeToggle />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => (
          <MetricCard
            key={metric.id}
            metric={metric}
            onSelect={(value) => setSelectedMetric(value.id)}
            isActive={selectedMetric === metric.id}
          />
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <TrendChart data={trends} />
        </div>
        <TeamPanel members={team} />
      </div>

      <ActivityFeed events={events} />
    </section>
  );
}

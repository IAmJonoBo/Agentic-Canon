import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

const insights = [
  {
    id: 'lead-time',
    title: 'Lead time forecast',
    description: 'Projected to decrease by 7% next week based on deployment cadence.',
    tags: ['Predictive'],
    impact: 'Medium',
  },
  {
    id: 'flaky-tests',
    title: 'Flaky test quarantine',
    description: '3 tests automatically quarantined; review suggested within 24 hours.',
    tags: ['Quality', 'Automation'],
    impact: 'High',
  },
  {
    id: 'service-health',
    title: 'Service health score',
    description:
      'Checkout service trending towards 92% health with increased observability coverage.',
    tags: ['Reliability'],
    impact: 'Low',
  },
];

export default function AnalyticsPage() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Predictive analytics</h1>
        <p className="text-sm text-muted-foreground">
          Machine learning insights generated from deployment, incident, and testing telemetry.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {insights.map((insight) => (
          <Card key={insight.id}>
            <CardHeader>
              <div className="flex flex-wrap items-center gap-3">
                <CardTitle>{insight.title}</CardTitle>
                <Badge variant="secondary">Impact: {insight.impact}</Badge>
                {insight.tags.map((tag) => (
                  <Badge key={tag} variant="outline">
                    #{tag}
                  </Badge>
                ))}
              </div>
              <CardDescription>{insight.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Recommended action: validate expected outcomes in staging and update runbooks.
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

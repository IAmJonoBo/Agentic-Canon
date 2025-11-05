import type { ActivityEvent } from '../../types/dashboard';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../ui/card';

interface ActivityFeedProps {
  events: ActivityEvent[];
}

function statusColor(severity: ActivityEvent['severity']) {
  switch (severity) {
    case 'high':
      return 'text-red-500';
    case 'medium':
      return 'text-amber-500';
    default:
      return 'text-emerald-500';
  }
}

export function ActivityFeed({ events }: ActivityFeedProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Activity feed</CardTitle>
        <CardDescription>Deployment and incident updates</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {events.map((event) => (
            <li key={event.id} className="rounded-lg border border-border/70 bg-background/60 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold text-sm">{event.title}</p>
                  <p className="mt-1 text-sm text-muted-foreground">{event.description}</p>
                </div>
                <span className={`text-xs font-medium ${statusColor(event.severity)}`}>
                  {event.severity.toUpperCase()}
                </span>
              </div>
              <p className="mt-3 text-xs text-muted-foreground">
                {new Date(event.timestamp).toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

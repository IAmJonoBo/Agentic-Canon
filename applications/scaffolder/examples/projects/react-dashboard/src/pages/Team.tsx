import { useQuery } from '@tanstack/react-query';
import { fetchTeam } from '../services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

export default function TeamPage() {
  const { data: team = [] } = useQuery({ queryKey: ['team'], queryFn: fetchTeam });

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Team directory</h1>
        <p className="text-sm text-muted-foreground">
          Who is on point for delivery and incident response.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {team.map((member) => (
          <Card key={member.id}>
            <CardHeader>
              <CardTitle>{member.name}</CardTitle>
              <CardDescription>{member.email}</CardDescription>
            </CardHeader>
            <CardContent>
              <Badge variant="secondary">{member.role}</Badge>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

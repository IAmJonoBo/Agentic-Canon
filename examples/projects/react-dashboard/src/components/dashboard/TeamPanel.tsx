import type { UserProfile } from '../../types/dashboard';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../ui/card';
import { Avatar, AvatarFallback } from '../ui/avatar';

interface TeamPanelProps {
  members: UserProfile[];
}

export function TeamPanel({ members }: TeamPanelProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>On-call roster</CardTitle>
        <CardDescription>People responsible for the current deployment window</CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4 text-sm">
          {members.map((member) => (
            <li key={member.id} className="flex items-center gap-3">
              <Avatar className="h-9 w-9">
                <AvatarFallback>{member.name.slice(0, 2).toUpperCase()}</AvatarFallback>
              </Avatar>
              <div>
                <p className="font-medium leading-tight">{member.name}</p>
                <p className="text-xs text-muted-foreground">{member.role}</p>
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

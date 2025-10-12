import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import type { TrendPoint } from '../../types/dashboard';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../ui/card';

interface TrendChartProps {
  data: TrendPoint[];
}

export function TrendChart({ data }: TrendChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Delivery velocity</CardTitle>
        <CardDescription>Deployments vs incidents over time</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80 w-full">
          <ResponsiveContainer>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(210 16% 82%)" />
              <XAxis dataKey="date" stroke="hsl(215 16% 47%)" tickLine={false} />
              <YAxis stroke="hsl(215 16% 47%)" tickLine={false} />
              <Tooltip contentStyle={{ background: 'hsl(224 71% 4%)', borderRadius: 12 }} />
              <Legend />
              <Line
                type="monotone"
                dataKey="deployments"
                stroke="hsl(221 83% 53%)"
                strokeWidth={2}
              />
              <Line type="monotone" dataKey="incidents" stroke="hsl(14 81% 56%)" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

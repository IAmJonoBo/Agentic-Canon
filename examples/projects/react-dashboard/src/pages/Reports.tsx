const data = [
  {
    id: 1,
    service: 'Checkout',
    deployments: 42,
    coverage: '92%',
    incidents: 1,
    owner: 'Platform Team',
  },
  {
    id: 2,
    service: 'Payments',
    deployments: 36,
    coverage: '88%',
    incidents: 2,
    owner: 'Payments Guild',
  },
  {
    id: 3,
    service: 'Identity',
    deployments: 28,
    coverage: '95%',
    incidents: 0,
    owner: 'Identity Squad',
  },
];

export default function ReportsPage() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Operational reports</h1>
        <p className="text-sm text-muted-foreground">
          Exportable data views for board meetings, reliability reviews, and quarterly planning.
        </p>
      </div>

      <div className="overflow-hidden rounded-lg border border-border bg-background/70 shadow">
        <table className="min-w-full divide-y divide-border/60 text-sm">
          <thead className="bg-muted/60">
            <tr>
              <th className="px-4 py-3 text-left font-semibold">Service</th>
              <th className="px-4 py-3 text-left font-semibold">Deployments</th>
              <th className="px-4 py-3 text-left font-semibold">Coverage</th>
              <th className="px-4 py-3 text-left font-semibold">Incidents</th>
              <th className="px-4 py-3 text-left font-semibold">Owner</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {data.map((row) => (
              <tr key={row.id} className="hover:bg-muted/40">
                <td className="px-4 py-3 font-medium">{row.service}</td>
                <td className="px-4 py-3">{row.deployments}</td>
                <td className="px-4 py-3">{row.coverage}</td>
                <td className="px-4 py-3">{row.incidents}</td>
                <td className="px-4 py-3">{row.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

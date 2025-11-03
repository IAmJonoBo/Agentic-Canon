import { useSettingsStore } from '../store/settingsStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';

export default function SettingsPage() {
  const theme = useSettingsStore((state) => state.theme);
  const toggleTheme = useSettingsStore((state) => state.toggleTheme);
  const enableRealtime = useSettingsStore((state) => state.enableRealtime);
  const toggleRealtime = useSettingsStore((state) => state.toggleRealtime);

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Configure experience, automation, and alerting preferences for your organization.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Theme</CardTitle>
            <CardDescription>Choose how the dashboard adapts to ambient lighting.</CardDescription>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">Current mode: {theme}</p>
            <Button onClick={() => toggleTheme()}>Toggle theme</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Realtime updates</CardTitle>
            <CardDescription>
              Automatically refresh metrics and charts every 12 seconds.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              Realtime updates are {enableRealtime ? 'enabled' : 'disabled'}
            </p>
            <Button
              variant={enableRealtime ? 'default' : 'outline'}
              onClick={() => toggleRealtime()}
            >
              {enableRealtime ? 'Disable' : 'Enable'} realtime
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}

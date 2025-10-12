import { useEffect } from 'react';
import { Signal } from 'lucide-react';
import { useQueryClient } from '@tanstack/react-query';
import { Button } from '../ui/button';
import { useSettingsStore } from '../../store/settingsStore';

export function RealtimeToggle() {
  const enableRealtime = useSettingsStore((state) => state.enableRealtime);
  const toggleRealtime = useSettingsStore((state) => state.toggleRealtime);
  const queryClient = useQueryClient();

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | undefined;
    if (enableRealtime) {
      interval = setInterval(() => {
        queryClient.invalidateQueries({ queryKey: ['metrics'] });
        queryClient.invalidateQueries({ queryKey: ['trends'] });
        queryClient.invalidateQueries({ queryKey: ['activity'] });
      }, 12_000);
    }
    return () => interval && clearInterval(interval);
  }, [enableRealtime, queryClient]);

  return (
    <Button variant={enableRealtime ? 'default' : 'outline'} onClick={() => toggleRealtime()}>
      <Signal className="mr-2 h-4 w-4" />
      {enableRealtime ? 'Realtime updates enabled' : 'Enable realtime updates'}
    </Button>
  );
}

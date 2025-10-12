import { Link } from 'react-router-dom';
import { Menu, Bell, Sun, Moon, LogOut } from 'lucide-react';
import { useState } from 'react';
import { Button } from '../ui/button';
import { useAuth } from '../../hooks/useAuth';
import { useSettingsStore } from '../../store/settingsStore';
import { cn } from '../../lib/cn';

interface HeaderProps {
  onToggleSidebar?: () => void;
}

export function Header({ onToggleSidebar }: HeaderProps) {
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const { user, logout, isAuthenticated } = useAuth();
  const theme = useSettingsStore((state) => state.theme);
  const toggleTheme = useSettingsStore((state) => state.toggleTheme);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/70 backdrop-blur">
      <div className="flex h-14 items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" className="lg:hidden" onClick={onToggleSidebar}>
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle navigation</span>
          </Button>
          <Link to="/" className="text-base font-semibold">
            Agentic Canon Dashboard
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            aria-label="Toggle theme"
            onClick={() => toggleTheme()}
          >
            {theme === 'light' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          <div className="relative">
            <Button
              variant="ghost"
              size="icon"
              aria-expanded={isNotificationsOpen}
              onClick={() => setIsNotificationsOpen((value) => !value)}
            >
              <Bell className="h-5 w-5" />
              <span className="sr-only">Toggle notifications</span>
            </Button>
            <div
              className={cn(
                'absolute right-0 mt-2 w-64 rounded-lg border border-border bg-background p-3 text-sm shadow-lg',
                isNotificationsOpen ? 'block' : 'hidden',
              )}
            >
              <p className="font-semibold">Latest alerts</p>
              <ul className="mt-2 space-y-2">
                <li className="rounded-md bg-muted/50 p-2">
                  📦 Deploy #842 completed successfully
                </li>
                <li className="rounded-md bg-muted/50 p-2">
                  ⚠️ Incident on checkout cluster resolved in 17m
                </li>
                <li className="rounded-md bg-muted/50 p-2">✅ MTTR trending downward</li>
              </ul>
            </div>
          </div>
          {isAuthenticated ? (
            <div className="flex items-center gap-2">
              <span className="hidden text-sm text-muted-foreground md:inline">
                {user?.name ?? 'Dashboard User'}
              </span>
              <Button variant="ghost" size="icon" onClick={() => logout()}>
                <LogOut className="h-5 w-5" />
                <span className="sr-only">Sign out</span>
              </Button>
            </div>
          ) : (
            <Button asChild>
              <Link to="/login">Sign in</Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}

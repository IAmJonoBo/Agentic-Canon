import { NavLink } from 'react-router-dom';
import { BarChart3, LineChart, PieChart, Settings, Users, LogIn } from 'lucide-react';
import { cn } from '../../lib/cn';
import { useAuth } from '../../hooks/useAuth';

interface SidebarProps {
  isOpen: boolean;
  onRouteSelected?: () => void;
}

const links = [
  { to: '/', icon: BarChart3, label: 'Dashboard' },
  { to: '/analytics', icon: LineChart, label: 'Analytics' },
  { to: '/reports', icon: PieChart, label: 'Reports' },
  { to: '/settings', icon: Settings, label: 'Settings' },
  { to: '/team', icon: Users, label: 'Team' },
];

export function Sidebar({ isOpen, onRouteSelected }: SidebarProps) {
  const { isAuthenticated } = useAuth();

  return (
    <aside
      className={cn(
        'border-border/80 bg-background/65 backdrop-blur transition-all duration-200 lg:w-64',
        'fixed inset-y-14 left-0 z-30 w-64 border-r px-4 py-6 lg:static lg:translate-x-0',
        isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
      )}
    >
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                isActive ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted/60',
              )
            }
            onClick={onRouteSelected}
          >
            <link.icon className="h-4 w-4" />
            {link.label}
          </NavLink>
        ))}
        {!isAuthenticated && (
          <NavLink
            to="/login"
            className={({ isActive }) =>
              cn(
                'mt-8 flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                isActive ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted/60',
              )
            }
            onClick={onRouteSelected}
          >
            <LogIn className="h-4 w-4" />
            Sign in
          </NavLink>
        )}
      </nav>
    </aside>
  );
}

import { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-br from-background via-background to-background/95 text-foreground">
      <Header onToggleSidebar={() => setSidebarOpen((value) => !value)} />
      <div className="flex flex-1">
        <Sidebar isOpen={isSidebarOpen} onRouteSelected={() => setSidebarOpen(false)} />
        <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl space-y-6">{children}</div>
        </main>
      </div>
    </div>
  );
}

import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';

export default function NotFoundPage() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-24 text-center">
      <div className="space-y-2">
        <p className="text-sm uppercase tracking-wide text-primary">404</p>
        <h1 className="text-3xl font-semibold">Page not found</h1>
        <p className="text-muted-foreground">
          The dashboard view you are looking for does not exist or has been archived.
        </p>
      </div>
      <Button asChild>
        <Link to="/">Return to dashboard</Link>
      </Button>
    </section>
  );
}

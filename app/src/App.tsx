import { ThemeProvider, useTheme } from './theme/ThemeProvider';
import { Button, Badge, Card, CardBody, ToggleGroup } from './components/ui';
import { useState } from 'react';

function Gallery() {
  const { theme, toggle } = useTheme();
  const [v, setV] = useState<string | null>('no');
  return (
    <div className="min-h-screen p-10 max-w-3xl mx-auto">
      <header className="flex items-center gap-3 mb-8">
        <div className="w-8 h-8 rounded-sm bg-accent text-accent-fg grid place-items-center font-display font-semibold">P</div>
        <h1 className="text-xl">Brass Editorial — design system</h1>
        <span className="flex-1" />
        <Button variant="outline" onClick={toggle}>Theme: {theme}</Button>
      </header>
      <div className="flex gap-2 mb-6">
        <Badge state="met">MET</Badge><Badge state="partial">PARTIAL</Badge>
        <Badge state="gap">GAP</Badge><Badge state="pending">PENDING</Badge><Badge outline>A1</Badge>
      </div>
      <Card className="mb-6"><CardBody>
        <p className="font-mono text-[10px] tracking-widest uppercase text-muted mb-2">coverage · gap ↔ partial</p>
        <p className="mb-4">Is secret push-protection deployed at all relevant gates?</p>
        <ToggleGroup value={v} onChange={setV} options={[
          { value: 'yes', label: 'Yes' }, { value: 'no', label: 'No' }, { value: 'na', label: 'N/A' }]} />
      </CardBody></Card>
      <div className="flex gap-3">
        <Button variant="outline">← Previous</Button>
        <Button>Save &amp; next →</Button>
      </div>
    </div>
  );
}

export default function App() {
  return <ThemeProvider><Gallery /></ThemeProvider>;
}

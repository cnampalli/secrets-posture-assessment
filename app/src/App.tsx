import { useEffect, useRef } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { AssessmentProvider, useAssessment } from './assessment/store';
import { Sidebar } from './components/Sidebar';
import { ThemeToggle } from './components/ThemeToggle';
import { ToastProvider, useToast } from './components/Toast';
import { UseCaseView } from './components/UseCaseView';
import { Button } from './components/ui';
import { RUBRIC } from './assessment/rubric';

function Header() {
  const a = useAssessment();
  const toast = useToast();
  const fileRef = useRef<HTMLInputElement>(null);

  function doExport() {
    const blob = new Blob([a.exportRecord()], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a'); link.href = url; link.download = 'assessment-record.json'; link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <header className="h-14 flex items-center gap-3 px-5 border-b border-border bg-bg/80 backdrop-blur sticky top-0 z-20">
      <div className="w-8 h-8 rounded-sm bg-accent text-accent-fg grid place-items-center font-display font-semibold">P</div>
      <b className="font-display">Posture Assessment</b>
      <span className="text-muted text-sm">/ Questionnaire</span>
      <span className="flex-1" />
      <span className="font-mono text-xs text-muted">{a.scored} / {RUBRIC.length} scored</span>
      <input ref={fileRef} type="file" accept="application/json" className="hidden"
        onChange={e => {
          const f = e.target.files?.[0];
          if (!f) return;
          const rd = new FileReader();
          rd.onload = () => {
            try {
              a.importText(String(rd.result));
              toast('Record imported');
            } catch {
              toast('Import failed — check the file');
            }
          };
          rd.readAsText(f);
          e.currentTarget.value = '';
        }} />
      <Button variant="outline" onClick={() => fileRef.current?.click()}>Import</Button>
      <Button onClick={doExport}>Export record</Button>
      <ThemeToggle />
    </header>
  );
}

function Shell() {
  const a = useAssessment();
  const mainRef = useRef<HTMLElement>(null);
  // Reset main-pane scroll to top whenever the active use case changes,
  // so navigating from a deep scroll position doesn't land on a blank view.
  useEffect(() => { mainRef.current?.scrollTo(0, 0); }, [a.current.uc_id]);
  return (
    <ToastProvider>
      <div className="h-screen overflow-hidden flex flex-col">
        <Header />
        <div className="flex flex-1 min-h-0">
          <Sidebar />
          <main ref={mainRef} className="flex-1 overflow-auto p-8 max-w-[920px]">
            <UseCaseView />
          </main>
        </div>
      </div>
    </ToastProvider>
  );
}

export default function App() {
  return <ThemeProvider><AssessmentProvider><Shell /></AssessmentProvider></ThemeProvider>;
}

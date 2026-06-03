import { ThemeProvider } from './theme/ThemeProvider';
import { AssessmentProvider, useAssessment } from './assessment/store';
import { Sidebar } from './components/Sidebar';
import { ThemeToggle } from './components/ThemeToggle';
import { RUBRIC } from './assessment/rubric';

function Header() {
  const a = useAssessment();
  return (
    <header className="h-14 flex items-center gap-3 px-5 border-b border-border bg-bg/80 backdrop-blur sticky top-0 z-20">
      <div className="w-8 h-8 rounded-sm bg-accent text-accent-fg grid place-items-center font-display font-semibold">P</div>
      <b className="font-display">Posture Assessment</b>
      <span className="text-muted text-sm">/ Questionnaire</span>
      <span className="flex-1" />
      <span className="font-mono text-xs text-muted">{a.scored} / {RUBRIC.length} scored</span>
      <ThemeToggle />
    </header>
  );
}

function Shell() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex flex-1 min-h-0">
        <Sidebar />
        <main className="flex-1 overflow-auto p-8 max-w-[920px]">
          <p className="text-muted">Use-case view — Task 7.</p>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return <ThemeProvider><AssessmentProvider><Shell /></AssessmentProvider></ThemeProvider>;
}

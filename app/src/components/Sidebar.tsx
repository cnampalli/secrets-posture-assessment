import { useAssessment } from '../assessment/store';
import { byCategory } from '../assessment/rubric';
import type { State } from '../assessment/types';

const dotClass: Record<State, string> = {
  GAP: 'bg-gap', PARTIAL: 'bg-partial', MET: 'bg-met', PENDING: 'bg-pending', NA: 'bg-na',
};

export function Sidebar() {
  const a = useAssessment();
  const groups = byCategory();
  return (
    <nav className="w-[280px] shrink-0 border-r border-border bg-bg2 overflow-auto p-3">
      {Object.entries(groups).map(([cat, ucs]) => (
        <div key={cat}>
          <div className="font-mono text-[10px] tracking-[0.14em] uppercase text-faint px-2.5 pt-4 pb-1.5">{cat}</div>
          {ucs.map(uc => {
            const active = a.current.uc_id === uc.uc_id;
            return (
              <button key={uc.uc_id} onClick={() => a.go(uc.uc_id)}
                className={`w-full flex items-center gap-2.5 px-2.5 py-2 rounded-sm text-left text-[13px] ${
                  active ? 'bg-card shadow-sm text-ink font-medium' : 'text-ink2 hover:bg-card/60'}`}>
                <span className={`w-[7px] h-[7px] rounded-full shrink-0 ${dotClass[a.finalOf(uc.uc_id)]}`} />
                <span className="flex-1 truncate">{uc.title || uc.uc_id}</span>
                <span className="font-mono text-[10.5px] text-faint">{uc.archetype}</span>
              </button>
            );
          })}
        </div>
      ))}
    </nav>
  );
}

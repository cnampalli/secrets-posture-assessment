import { useState, useEffect } from 'react';
import { useAssessment } from '../assessment/store';
import { useToast } from './Toast';
import { Badge, ToggleGroup } from './ui';
import type { State } from '../assessment/types';

const STATES: State[] = ['GAP', 'PARTIAL', 'MET', 'PENDING', 'NA'];
const lower = (s: State) => s.toLowerCase() as Lowercase<State>;

export function ScorePanel() {
  const a = useAssessment();
  const toast = useToast();
  const uc = a.current;
  const [needRat, setNeedRat] = useState(false);
  useEffect(() => { setNeedRat(false); }, [uc.uc_id]);
  const proposed = a.proposedOf(uc.uc_id);
  const final = a.finalOf(uc.uc_id);
  const r = a.responses[uc.uc_id];

  return (
    <section className="border border-border-strong rounded-lg bg-card shadow-md mt-6">
      <div className="flex items-center gap-3.5 p-4 flex-wrap">
        <Badge state={lower(final)}>{uc.kind === 'bespoke' ? 'State' : 'Proposed'} · {final}</Badge>
        <span className="text-muted text-xs flex-1 min-w-[200px]">Finish the ladder to derive a state, or override below.</span>
      </div>
      <div className="h-px bg-border" />
      <div className="p-4 bg-bg2 rounded-b-lg">
        <label className="font-mono text-[10px] tracking-widest uppercase text-muted mb-1.5 block">Override rationale</label>
        <textarea aria-label="Override rationale" value={r?.rationale ?? ''} onChange={e => a.setRationale(e.target.value)}
          className={`w-full min-h-[62px] border rounded-sm p-2.5 font-body text-sm bg-card text-ink resize-y ${needRat ? 'border-gap' : 'border-border-strong'}`} />
        <div className="flex gap-7 items-end mt-3.5 flex-wrap">
          <div>
            <label className="font-mono text-[10px] tracking-widest uppercase text-muted mb-1.5 block">Confidence</label>
            <ToggleGroup value={r?.confidence ?? 'MED'} onChange={v => v && a.setConfidence(v as 'LOW'|'MED'|'HIGH')}
              options={[{ value: 'LOW', label: 'LOW' }, { value: 'MED', label: 'MED' }, { value: 'HIGH', label: 'HIGH' }]} />
          </div>
          <div>
            <label className="font-mono text-[10px] tracking-widest uppercase text-muted mb-1.5 block">Final state</label>
            <select value={r?.overridden ? (r?.final_state ?? '') : ''} aria-label="Final state"
              onChange={e => { const res = a.setFinal(e.target.value as State | ''); if (res.needRationale) { setNeedRat(true); toast('Rationale required to override'); } else setNeedRat(false); }}
              className="h-9 border border-border-strong rounded-sm px-2.5 bg-card text-ink text-sm cursor-pointer">
              <option value="">{proposed ? `(proposed: ${proposed})` : '(choose)'}</option>
              {STATES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
      </div>
    </section>
  );
}

import { useEffect } from 'react';
import { useAssessment } from '../assessment/store';
import { Badge, Button, Card, CardBody, ToggleGroup, Checkbox } from './ui';
import { ScorePanel } from './ScorePanel';
import { EvidencePanel } from './EvidencePanel';

export function UseCaseView({ startId }: { startId?: string }) {
  const a = useAssessment();
  useEffect(() => { if (startId) a.go(startId); /* once */ }, [startId]); // eslint-disable-line
  const uc = a.current;
  const r = a.responses[uc.uc_id];
  const rubric = a.rubric;
  const idx = rubric.findIndex(u => u.uc_id === uc.uc_id);

  return (
    <div>
      <div className="font-mono text-[11px] tracking-widest uppercase text-faint mb-3">{uc.category} · Use case</div>
      <div className="flex items-baseline gap-3 flex-wrap">
        <h1 className="text-2xl font-display">{uc.title || uc.uc_id}</h1>
        <Badge outline>{uc.archetype} · {uc.archetype_name}</Badge>
      </div>
      <div className="font-mono text-xs text-muted mt-1.5 mb-6">{uc.uc_id}</div>

      {uc.kind === 'ladder' ? uc.questions!.map(q => {
        const v = (r?.answers?.[q.qid] as string) ?? null;
        return (
          <Card key={q.qid} className="mb-3.5"><CardBody>
            <div className="flex gap-2 mb-2.5">
              <span className="font-mono text-[10px] uppercase tracking-wider text-muted bg-bg2 rounded-pill px-2 py-1">{q.dimension}</span>
              <Badge state={q.informs_state === 'GAP_PARTIAL' ? 'gap' : 'partial'}>{q.informs_state === 'GAP_PARTIAL' ? 'GAP ↔ PARTIAL' : 'PARTIAL ↔ MET'}</Badge>
            </div>
            <p className="mb-3.5">{q.text}</p>
            <ToggleGroup value={v} onChange={val => val && a.answer(q.qid, val as 'yes'|'no'|'na')}
              options={[{ value: 'yes', label: 'Yes' }, { value: 'no', label: 'No' }, { value: 'na', label: 'N/A' }]} />
          </CardBody></Card>
        );
      }) : (
        <Card><CardBody>
          {uc.sub_criteria!.map(sc => (
            <label key={sc.sub_id} className="flex gap-2.5 items-start py-2.5 border-t border-border first:border-0 cursor-pointer">
              <Checkbox checked={!!r?.answers?.[sc.sub_id]} onChange={e => a.check(sc.sub_id, e.target.checked)} />
              <span className="text-sm">{sc.sub_criterion}<span className="block text-xs text-muted mt-1">{sc.question} — <i>{sc.evidence}</i></span></span>
            </label>
          ))}
        </CardBody></Card>
      )}

      <ScorePanel />

      <EvidencePanel />

      <div className="flex justify-between mt-6">
        <Button variant="outline" disabled={idx <= 0} onClick={() => a.go(rubric[idx - 1].uc_id)}>← Previous</Button>
        <Button disabled={idx >= rubric.length - 1} onClick={() => a.go(rubric[idx + 1].uc_id)}>Save &amp; next →</Button>
      </div>
    </div>
  );
}

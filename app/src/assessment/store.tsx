import { createContext, useContext, useMemo, useRef, useState, type ReactNode } from 'react';
import type { Answer, Response, State, UseCase } from './types';
import { RUBRIC, byId } from './rubric';
import { blankResponse, proposedFor, finalFor, scoredCount, buildRecord } from './record';
import { loadResponses, saveResponses, importRecord } from './persistence';

interface Api {
  current: UseCase; responses: Record<string, Response>; scored: number;
  go: (uc_id: string) => void;
  answer: (qid: string, v: Answer) => void;
  check: (subId: string, on: boolean) => void;
  setRationale: (v: string) => void;
  setConfidence: (c: 'LOW' | 'MED' | 'HIGH') => void;
  setFinal: (v: State | '') => { needRationale: boolean };
  proposedOf: (uc_id: string) => State | null;
  finalOf: (uc_id: string) => State;
  exportRecord: () => string;
  importText: (text: string) => void;
}
const Ctx = createContext<Api | null>(null);
// Deterministic-friendly timestamp hook; real app uses Date, tests can ignore value.
const now = () => new Date().toISOString();

export function AssessmentProvider({ children }: { children: ReactNode }) {
  const [responses, setResponses] = useState<Record<string, Response>>(() => loadResponses());
  const [currentId, setCurrentId] = useState<string>(RUBRIC[0]?.uc_id ?? '');
  const ref = useRef(responses); ref.current = responses;

  function persist(next: Record<string, Response>) { setResponses(next); saveResponses(next, now()); }
  function mutate(id: string, fn: (r: Response) => Response) {
    const cur = ref.current[id] ?? blankResponse();
    persist({ ...ref.current, [id]: fn({ ...cur, answers: { ...cur.answers } }) });
  }

  const api: Api = useMemo(() => ({
    get current() { return byId(currentId) ?? RUBRIC[0]; },
    responses, scored: scoredCount(RUBRIC, responses),
    go: (uc_id) => setCurrentId(uc_id),
    answer: (qid, v) => mutate(currentId, r => {
      const a = { ...r.answers };
      if (a[qid] === v) delete a[qid]; else a[qid] = v;
      return { ...r, answers: a };
    }),
    check: (subId, on) => mutate(currentId, r => ({ ...r, answers: { ...r.answers, [subId]: on } })),
    setRationale: (v) => mutate(currentId, r => ({ ...r, rationale: v })),
    setConfidence: (c) => mutate(currentId, r => ({ ...r, confidence: c })),
    setFinal: (v) => {
      const uc = byId(currentId)!; const r = ref.current[currentId] ?? blankResponse();
      if (!v) { mutate(currentId, x => ({ ...x, overridden: false, final_state: null })); return { needRationale: false }; }
      const proposed = proposedFor(uc, r);
      const needRationale = uc.kind === 'bespoke' ? true : !!(proposed && v !== proposed);
      if (needRationale && !(r.rationale || '').trim()) return { needRationale: true };
      mutate(currentId, x => ({ ...x, overridden: uc.kind === 'bespoke' ? true : v !== proposed, final_state: v }));
      return { needRationale: false };
    },
    proposedOf: (id) => { const uc = byId(id); const r = responses[id]; return uc && r ? proposedFor(uc, r) : (uc ? proposedFor(uc, blankResponse()) : null); },
    finalOf: (id) => { const uc = byId(id); return uc ? finalFor(uc, responses[id] ?? blankResponse()) : 'PENDING'; },
    exportRecord: () => JSON.stringify(buildRecord(RUBRIC, ref.current, now()), null, 2),
    importText: (text) => persist(importRecord(ref.current, text, id => !!byId(id))),
  }), [responses, currentId]); // eslint-disable-line react-hooks/exhaustive-deps

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAssessment(): Api {
  const v = useContext(Ctx);
  if (!v) throw new Error('useAssessment must be used within AssessmentProvider');
  return v;
}

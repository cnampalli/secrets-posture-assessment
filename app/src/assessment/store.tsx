import { createContext, useContext, useMemo, useRef, useState, type ReactNode } from 'react';
import type { Answer, Response, State, UseCase, EvidenceMeta } from './types';
import { RUBRIC, byId } from './rubric';
import { blankResponse, proposedFor, finalFor, scoredCount } from './record';
import { loadResponses, saveResponses, importRecord, loadEvidence } from './persistence';
import { putFile, deleteFile, getBlob, validateFile, genId, buildExportRecord, restoreEvidence } from './evidence';

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
  evidenceFor: (uc_id: string) => EvidenceMeta[];
  addEvidence: (files: FileList | File[]) => Promise<{ added: number; rejected: string[] }>;
  removeEvidence: (id: string) => Promise<void>;
  exportRecord: () => Promise<{ text: string; skipped: number }>;
  importText: (text: string) => Promise<void>;
}
const Ctx = createContext<Api | null>(null);
// Deterministic-friendly timestamp hook; real app uses Date, tests can ignore value.
const now = () => new Date().toISOString();

export function AssessmentProvider({ children }: { children: ReactNode }) {
  const [responses, setResponses] = useState<Record<string, Response>>(() => loadResponses());
  const [currentId, setCurrentId] = useState<string>(RUBRIC[0]?.uc_id ?? '');
  const ref = useRef(responses); ref.current = responses;

  const [evidence, setEvidence] = useState<Record<string, EvidenceMeta[]>>(() => loadEvidence());
  const evRef = useRef(evidence); evRef.current = evidence;

  function persistAll(nextResp: Record<string, Response>, nextEv: Record<string, EvidenceMeta[]>) {
    setResponses(nextResp); setEvidence(nextEv); saveResponses(nextResp, now(), nextEv);
  }

  function persist(next: Record<string, Response>) { persistAll(next, evRef.current); }
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
    evidenceFor: (id) => evidence[id] ?? [],
    addEvidence: async (files) => {
      const uc = currentId; const accepted: EvidenceMeta[] = []; const rejected: string[] = [];
      for (const f of Array.from(files)) {
        const v = validateFile(f);
        if (!v.ok) { rejected.push(`${f.name} — ${v.reason}`); continue; }
        const id = genId();
        try { await putFile(id, f); accepted.push({ id, name: f.name, type: f.type, size: f.size, added: now() }); }
        catch { rejected.push(`${f.name} — couldn't store`); }
      }
      if (accepted.length) persistAll(ref.current, { ...evRef.current, [uc]: [ ...(evRef.current[uc] ?? []), ...accepted ] });
      return { added: accepted.length, rejected };
    },
    removeEvidence: async (id) => {
      const uc = currentId;
      await deleteFile(id).catch(() => {});
      persistAll(ref.current, { ...evRef.current, [uc]: (evRef.current[uc] ?? []).filter(m => m.id !== id) });
    },
    exportRecord: async () => {
      const { record, skipped } = await buildExportRecord(RUBRIC, ref.current, evRef.current, now(), getBlob);
      return { text: JSON.stringify(record, null, 2), skipped };
    },
    importText: async (text) => {
      const mergedResp = importRecord(ref.current, text, id => !!byId(id));
      let parsed: { evidence?: unknown } = {};
      try { parsed = JSON.parse(text); } catch { /* importRecord already validated/threw */ }
      const { evidence: mergedEv } = await restoreEvidence(evRef.current, parsed.evidence ?? {}, id => !!byId(id));
      persistAll(mergedResp, mergedEv);
    },
  }), [responses, currentId, evidence]); // eslint-disable-line react-hooks/exhaustive-deps

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAssessment(): Api {
  const v = useContext(Ctx);
  if (!v) throw new Error('useAssessment must be used within AssessmentProvider');
  return v;
}

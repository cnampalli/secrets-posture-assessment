import { createContext, useContext, useMemo, useRef, useState, type ReactNode } from 'react';
import type { Answer, Response, State, UseCase, EvidenceMeta } from './types';
import { makeRubric, type RubricView } from './rubric';
import { DEFAULT_DOMAIN, isDomainId, type DomainId } from './domains';
import { blankResponse, proposedFor, finalFor, scoredCount, unscoredUseCases } from './record';
import { loadResponses, saveResponses, importRecord, loadEvidence, migrateLegacy } from './persistence';
import { putFile, deleteFile, getBlob, validateFile, genId, buildExportRecord, restoreEvidence } from './evidence';

interface Api {
  current: UseCase; responses: Record<string, Response>; scored: number; unscored: UseCase[];
  domainId: DomainId; setDomain: (id: DomainId) => void;
  rubric: UseCase[]; byCategory: () => Record<string, UseCase[]>;
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

const ACTIVE_DOMAIN_KEY = 'posture-active-domain';
function initialDomain(): DomainId {
  try { const v = localStorage.getItem(ACTIVE_DOMAIN_KEY); if (isDomainId(v)) return v; } catch { /* ignore */ }
  return DEFAULT_DOMAIN;
}

export function AssessmentProvider({ children }: { children: ReactNode }) {
  const [domainId, setDomainId] = useState<DomainId>(() => { migrateLegacy(); return initialDomain(); });
  const view = useMemo<RubricView>(() => makeRubric(domainId), [domainId]);
  const viewRef = useRef(view); viewRef.current = view;

  const [responses, setResponses] = useState<Record<string, Response>>(() => loadResponses(domainId));
  const [currentId, setCurrentId] = useState<string>(view.rubric[0]?.uc_id ?? '');
  const ref = useRef(responses); ref.current = responses;

  const [evidence, setEvidence] = useState<Record<string, EvidenceMeta[]>>(() => loadEvidence(domainId));
  const evRef = useRef(evidence); evRef.current = evidence;

  function persistAll(nextResp: Record<string, Response>, nextEv: Record<string, EvidenceMeta[]>) {
    setResponses(nextResp); setEvidence(nextEv);
    saveResponses(domainId, viewRef.current.rubric, nextResp, now(), nextEv);
  }

  function setDomain(id: DomainId) {
    if (id === domainId) return;
    try { localStorage.setItem(ACTIVE_DOMAIN_KEY, id); } catch { /* ignore */ }
    const nextView = makeRubric(id);
    const nextResp = loadResponses(id);
    const nextEv = loadEvidence(id);
    setDomainId(id);
    setResponses(nextResp); ref.current = nextResp;
    setEvidence(nextEv); evRef.current = nextEv;
    setCurrentId(nextView.rubric[0]?.uc_id ?? '');
    // Deliberately NOT syncing viewRef/domainId here: the Api (and its mutate/persist
    // closures) is useMemo'd on [domainId, view], so the next write can only fire after
    // React re-renders with the new domain — at which point persistAll already targets
    // the new namespace. Hand-syncing them here would be redundant; don't add it.
  }

  function persist(next: Record<string, Response>) { persistAll(next, evRef.current); }
  function mutate(id: string, fn: (r: Response) => Response) {
    const cur = ref.current[id] ?? blankResponse();
    persist({ ...ref.current, [id]: fn({ ...cur, answers: { ...cur.answers } }) });
  }

  const api: Api = useMemo(() => ({
    get current() { return view.byId(currentId) ?? view.rubric[0]; },
    responses, scored: scoredCount(view.rubric, responses),
    unscored: unscoredUseCases(view.rubric, responses),
    domainId, setDomain, rubric: view.rubric, byCategory: view.byCategory,
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
      const uc = view.byId(currentId)!; const r = ref.current[currentId] ?? blankResponse();
      if (!v) { mutate(currentId, x => ({ ...x, overridden: false, final_state: null })); return { needRationale: false }; }
      const proposed = proposedFor(uc, r);
      const needRationale = uc.kind === 'bespoke' ? true : !!(proposed && v !== proposed);
      if (needRationale && !(r.rationale || '').trim()) return { needRationale: true };
      mutate(currentId, x => ({ ...x, overridden: uc.kind === 'bespoke' ? true : v !== proposed, final_state: v }));
      return { needRationale: false };
    },
    proposedOf: (id) => { const uc = view.byId(id); const r = responses[id]; return uc && r ? proposedFor(uc, r) : (uc ? proposedFor(uc, blankResponse()) : null); },
    finalOf: (id) => { const uc = view.byId(id); return uc ? finalFor(uc, responses[id] ?? blankResponse()) : 'PENDING'; },
    evidenceFor: (id) => evidence[id] ?? [],
    addEvidence: async (files) => {
      const uc = currentId; const accepted: EvidenceMeta[] = []; const rejected: string[] = [];
      for (const f of Array.from(files)) {
        const v = validateFile(f);
        if (!v.ok) { rejected.push(`${f.name} — ${v.reason}`); continue; }
        const id = `${domainId}/${genId()}`;
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
      const { record, skipped } = await buildExportRecord(view.rubric, ref.current, evRef.current, now(), getBlob, domainId);
      return { text: JSON.stringify(record, null, 2), skipped };
    },
    importText: async (text) => {
      const mergedResp = importRecord(ref.current, text, id => !!view.byId(id));
      let parsed: { evidence?: unknown } = {};
      try { parsed = JSON.parse(text); } catch { /* importRecord already validated/threw */ }
      const { evidence: mergedEv } = await restoreEvidence(evRef.current, parsed.evidence ?? {}, id => !!view.byId(id));
      persistAll(mergedResp, mergedEv);
    },
  }), [domainId, view, responses, currentId, evidence]); // eslint-disable-line react-hooks/exhaustive-deps

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAssessment(): Api {
  const v = useContext(Ctx);
  if (!v) throw new Error('useAssessment must be used within AssessmentProvider');
  return v;
}

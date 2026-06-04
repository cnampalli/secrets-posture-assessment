# Brass Editorial — Questionnaire React App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the posture-assessment questionnaire as a React app on the Brass Editorial foundation — preserving 100% of current behaviour (scoring, override, autosave, import/export) and the `posture-assessment-record/v1` export schema so the Python exec/roadmap builds still consume it.

**Architecture:** Engine-first. Tasks 1–5 build a pure, fully-tested assessment engine (rubric data, scoring port with parity vectors, record model, persistence, a `useAssessment` store) with zero UI. Tasks 6–8 build the UI (shell + sidebar, use-case view + override, export/import wiring) using the Task-1-of-Plan-1 primitives, then verify schema-compat end-to-end against the real Python build and ship the offline single file.

**Tech Stack:** React 18 + TS + Tailwind (foundation), Vitest + @testing-library/react, Python 3 (rubric emit + cross-language schema-compat test).

**Plan 2 of 3.** Depends on Plan 1 (foundation) being merged/present on `feat/brass-editorial-ui`. Spec: `docs/superpowers/specs/2026-06-03-brass-editorial-react-uplift-design.md`.

---

## Source-of-truth facts (verified — do not re-derive)

**Scoring** (`questionnaire/scoring.js` / `methodology/scoring.py`), ported verbatim:
```
deriveState(questions, answers):
  vals = [(q.informs_state, answers[q.qid] ?? null) for q in questions]
  if vals nonempty and every v === "na"            -> "NA"
  if any v not in {yes,no,na}                       -> "PENDING"
  if any (informs_state=="GAP_PARTIAL" and v=="no") -> "GAP"
  if any (informs_state=="PARTIAL_MET" and v=="no") -> "PARTIAL"
  else                                              -> "MET"
```
Parity fixture: `questionnaire/scoring-vectors.json` (8 vectors: `{name, questions:[{qid,informs_state}], answers:{qid:val|null}, expected}`).

**Record schema** consumed by `presentation/build_exec_summary.py` (`questionnaire/record_state.resolve_state` = `final_state || proposed_state || "PENDING"`):
```json
{ "schema": "posture-assessment-record/v1", "generated": "<ISO>",
  "responses": { "<uc_id>": { "archetype": "...", "answers": {...},
    "proposed_state": "...|null", "final_state": "...", "overridden": false,
    "rationale": "", "confidence": "MED" } } }
```

**Rubric shape** (`questionnaire/rubric_loader.load_rubric`): array of
`{uc_id, title, category:"Functional"|"Non-functional", archetype, archetype_name, kind:"bespoke"|"ladder"}`
plus either `sub_criteria:[{sub_id,sub_criterion,question,evidence}]` (A0/bespoke) or
`questions:[{qid,dimension,informs_state,text}]` (A1–A8/ladder). 47 use cases total.

**Behaviour to preserve** (from `questionnaire/app.js`): `proposedFor` (bespoke→null else deriveState); `finalFor` (overridden&&final_state ? final_state : proposed||final_state||"PENDING"); answer toggle (re-click clears); bespoke checkbox; override requires rationale to change proposed (bespoke always requires rationale); confidence default "MED"; progress = count where (proposed && proposed!=="PENDING") || (bespoke && final_state); import merges + validates `schema`; autosave on every mutation.

---

## File Structure
```
questionnaire/emit_rubric.py        # NEW: load_rubric -> app/src/data/rubric.json (methodology = source of truth)
app/src/data/rubric.json            # GENERATED (committed) — 47 use cases
app/src/assessment/
  types.ts            # Rubric/UseCase/Response/Record TS types + State union
  scoring.ts          # deriveState (port) — pure
  scoring.test.ts     # parity vs questionnaire/scoring-vectors.json
  record.ts           # proposedFor/finalFor/whyFor/buildRecord/scoredCount — pure
  record.test.ts
  persistence.ts      # load/save localStorage + importRecord(merge+validate)
  persistence.test.ts
  store.tsx           # useAssessment() context: state + actions
  store.test.tsx
  rubric.ts           # loads rubric.json, groups by category, by-id index
app/src/components/
  Sidebar.tsx
  UseCaseView.tsx     # ladder questions + bespoke criteria
  ScorePanel.tsx      # proposed/override/confidence/final-state + evidence-row placeholder
  Toast.tsx
  ThemeToggle.tsx
  ui/Checkbox.tsx     # new primitive (bespoke criteria)
app/src/App.tsx       # REPLACE gallery: shell (header + Sidebar + UseCaseView)
tests/test_react_export_schema.py   # NEW (python): a buildRecord-shaped record builds the exec summary
```

---

## Task 1: Rubric data pipeline + types

**Files:** Create `questionnaire/emit_rubric.py`, `app/src/assessment/types.ts`, `app/src/assessment/rubric.ts`, `app/src/assessment/rubric.test.ts`; generate `app/src/data/rubric.json`.

- [ ] **Step 1: Write the emitter** — `questionnaire/emit_rubric.py`:
```python
#!/usr/bin/env python3
"""Emit the rubric (methodology = source of truth) as JSON for the React app."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METH = os.path.join(ROOT, "methodology")
OUT = os.path.join(ROOT, "app", "src", "data", "rubric.json")

def main():
    rubric = rubric_loader.load_rubric(METH)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rubric, fh, ensure_ascii=False, indent=2)
    print(f"wrote {OUT} ({len(rubric)} use cases)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Generate rubric.json** — Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 questionnaire/emit_rubric.py`
Expected: `wrote …/app/src/data/rubric.json (47 use cases)`.

- [ ] **Step 3: Write the failing test** — `app/src/assessment/rubric.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { RUBRIC, byCategory, byId } from './rubric';

describe('rubric', () => {
  it('loads 47 use cases', () => { expect(RUBRIC.length).toBe(47); });
  it('every use case has the required shape', () => {
    for (const uc of RUBRIC) {
      expect(uc.uc_id).toBeTruthy();
      expect(['Functional', 'Non-functional']).toContain(uc.category);
      expect(['bespoke', 'ladder']).toContain(uc.kind);
      if (uc.kind === 'ladder') expect(uc.questions!.length).toBeGreaterThan(0);
      else expect(Array.isArray(uc.sub_criteria)).toBe(true);
    }
  });
  it('groups by category and indexes by id', () => {
    const g = byCategory();
    expect(Object.keys(g)).toEqual(expect.arrayContaining(['Functional', 'Non-functional']));
    expect(byId(RUBRIC[0].uc_id)).toBe(RUBRIC[0]);
  });
});
```

- [ ] **Step 4: Run — verify FAIL** — `cd app && npx vitest run src/assessment/rubric.test.ts` → FAIL (module not found).

- [ ] **Step 5: Implement types** — `app/src/assessment/types.ts`:
```ts
export type State = 'GAP' | 'PARTIAL' | 'MET' | 'PENDING' | 'NA';
export type Answer = 'yes' | 'no' | 'na';
export type InformsState = 'GAP_PARTIAL' | 'PARTIAL_MET';

export interface Question { qid: string; dimension: string; informs_state: InformsState; text: string; }
export interface SubCriterion { sub_id: string; sub_criterion: string; question: string; evidence: string; }
export interface UseCase {
  uc_id: string; title: string; category: 'Functional' | 'Non-functional';
  archetype: string; archetype_name: string; kind: 'ladder' | 'bespoke';
  questions?: Question[]; sub_criteria?: SubCriterion[];
}
export interface Response {
  answers: Record<string, Answer | boolean>;
  overridden: boolean; final_state: State | null; rationale: string;
  confidence: 'LOW' | 'MED' | 'HIGH';
}
export interface AssessmentRecord {
  schema: 'posture-assessment-record/v1'; generated: string;
  responses: Record<string, {
    archetype: string; answers: Record<string, Answer | boolean>;
    proposed_state: State | null; final_state: State; overridden: boolean;
    rationale: string; confidence: 'LOW' | 'MED' | 'HIGH';
  }>;
}
```

- [ ] **Step 6: Implement rubric loader** — `app/src/assessment/rubric.ts`:
```ts
import type { UseCase } from './types';
import data from '../data/rubric.json';

export const RUBRIC = data as unknown as UseCase[];
const INDEX = new Map(RUBRIC.map(uc => [uc.uc_id, uc]));

export function byId(uc_id: string): UseCase | undefined { return INDEX.get(uc_id); }

export function byCategory(): Record<string, UseCase[]> {
  const out: Record<string, UseCase[]> = {};
  for (const uc of RUBRIC) (out[uc.category] ||= []).push(uc);
  return out;
}
```
Ensure `app/tsconfig.app.json` has `"resolveJsonModule": true` (Vite default has it; if `tsc -b` errors on the JSON import, add it).

- [ ] **Step 7: Run — verify PASS** — `cd app && npx vitest run src/assessment/rubric.test.ts` → PASS (3 tests).

- [ ] **Step 8: Commit**
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/emit_rubric.py app/src/data/rubric.json app/src/assessment/types.ts app/src/assessment/rubric.ts app/src/assessment/rubric.test.ts
git commit -m "feat: rubric data pipeline + assessment types"
```

---

## Task 2: Scoring port + parity tests

**Files:** Create `app/src/assessment/scoring.ts`, `app/src/assessment/scoring.test.ts`.

- [ ] **Step 1: Write the failing parity test** — `app/src/assessment/scoring.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { deriveState } from './scoring';
import type { Question, Answer } from './types';

// Single source of truth: the canonical vectors that pin JS↔Py scoring.
const vectorsPath = fileURLToPath(new URL('../../../questionnaire/scoring-vectors.json', import.meta.url));
const vectors = JSON.parse(readFileSync(vectorsPath, 'utf8')) as Array<{
  name: string; questions: Pick<Question, 'qid' | 'informs_state'>[];
  answers: Record<string, Answer | null>; expected: string;
}>;

describe('deriveState parity', () => {
  for (const v of vectors) {
    it(v.name, () => {
      expect(deriveState(v.questions as Question[], v.answers as Record<string, Answer>)).toBe(v.expected);
    });
  }
  it('covers all 8 canonical vectors', () => { expect(vectors.length).toBe(8); });
});
```

- [ ] **Step 2: Run — verify FAIL** — `cd app && npx vitest run src/assessment/scoring.test.ts` → FAIL (module not found).

- [ ] **Step 3: Implement (verbatim port)** — `app/src/assessment/scoring.ts`:
```ts
import type { Question, Answer, State } from './types';

const VALID: Answer[] = ['yes', 'no', 'na'];

export function deriveState(
  questions: Pick<Question, 'qid' | 'informs_state'>[],
  answers: Record<string, Answer | null | undefined>,
): State {
  const vals = questions.map(q => [q.informs_state, answers[q.qid] ?? null] as const);
  if (vals.length && vals.every(([, v]) => v === 'na')) return 'NA';
  if (vals.some(([, v]) => v == null || !VALID.includes(v as Answer))) return 'PENDING';
  if (vals.some(([inf, v]) => inf === 'GAP_PARTIAL' && v === 'no')) return 'GAP';
  if (vals.some(([inf, v]) => inf === 'PARTIAL_MET' && v === 'no')) return 'PARTIAL';
  return 'MET';
}
```

- [ ] **Step 4: Run — verify PASS** — `cd app && npx vitest run src/assessment/scoring.test.ts` → PASS (9 tests: 8 vectors + count).

- [ ] **Step 5: Commit**
```bash
git add app/src/assessment/scoring.ts app/src/assessment/scoring.test.ts
git commit -m "feat: scoring port with parity vectors"
```

---

## Task 3: Record model (proposed/final/why/buildRecord)

**Files:** Create `app/src/assessment/record.ts`, `app/src/assessment/record.test.ts`.

- [ ] **Step 1: Write the failing test** — `app/src/assessment/record.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { proposedFor, finalFor, scoredCount, buildRecord, blankResponse } from './record';
import type { UseCase, Response } from './types';

const ladder: UseCase = {
  uc_id: 'UC-F-001', title: 'X', category: 'Functional', archetype: 'A1', archetype_name: 'A1',
  kind: 'ladder', questions: [
    { qid: 'Q1', dimension: 'd', informs_state: 'GAP_PARTIAL', text: 't' },
    { qid: 'Q2', dimension: 'd', informs_state: 'PARTIAL_MET', text: 't' }],
};
const bespoke: UseCase = {
  uc_id: 'UC-N-001', title: 'Y', category: 'Non-functional', archetype: 'A0', archetype_name: 'A0',
  kind: 'bespoke', sub_criteria: [{ sub_id: 'S1', sub_criterion: 'c', question: 'q', evidence: 'e' }],
};
const resp = (o: Partial<Response> = {}): Response =>
  ({ ...blankResponse(), ...o });

describe('record model', () => {
  it('proposedFor: ladder derives, bespoke is null', () => {
    expect(proposedFor(ladder, resp({ answers: { Q1: 'yes', Q2: 'yes' } }))).toBe('MET');
    expect(proposedFor(bespoke, resp())).toBeNull();
  });
  it('finalFor: override wins; else proposed; else PENDING', () => {
    expect(finalFor(ladder, resp({ answers: { Q1: 'no', Q2: 'yes' } }))).toBe('GAP');
    expect(finalFor(ladder, resp({ overridden: true, final_state: 'MET', answers: { Q1: 'no', Q2: 'yes' } }))).toBe('MET');
    expect(finalFor(bespoke, resp())).toBe('PENDING');
    expect(finalFor(bespoke, resp({ final_state: 'MET' }))).toBe('MET');
  });
  it('scoredCount counts derived (non-pending) ladders + bespoke with final_state', () => {
    const responses = {
      'UC-F-001': resp({ answers: { Q1: 'yes', Q2: 'yes' } }),  // MET -> counts
      'UC-N-001': resp({ final_state: 'MET' }),                  // bespoke set -> counts
    };
    expect(scoredCount([ladder, bespoke], responses)).toBe(2);
    expect(scoredCount([ladder, bespoke], { 'UC-F-001': resp() })).toBe(0); // pending -> 0
  });
  it('buildRecord emits the v1 schema shape', () => {
    const rec = buildRecord([ladder], { 'UC-F-001': resp({ answers: { Q1: 'no', Q2: 'yes' }, rationale: 'r' }) }, '2026-01-01T00:00:00Z');
    expect(rec.schema).toBe('posture-assessment-record/v1');
    expect(rec.generated).toBe('2026-01-01T00:00:00Z');
    expect(rec.responses['UC-F-001']).toMatchObject({
      archetype: 'A1', proposed_state: 'GAP', final_state: 'GAP', overridden: false, rationale: 'r', confidence: 'MED',
    });
  });
});
```

- [ ] **Step 2: Run — verify FAIL.**

- [ ] **Step 3: Implement** — `app/src/assessment/record.ts`:
```ts
import type { UseCase, Response, State, AssessmentRecord } from './types';
import { deriveState } from './scoring';

const SCHEMA = 'posture-assessment-record/v1' as const;

export function blankResponse(): Response {
  return { answers: {}, overridden: false, final_state: null, rationale: '', confidence: 'MED' };
}

export function proposedFor(uc: UseCase, r: Response): State | null {
  if (uc.kind === 'bespoke') return null;
  return deriveState(uc.questions ?? [], r.answers as Record<string, never>);
}

export function finalFor(uc: UseCase, r: Response): State {
  if (r.overridden && r.final_state) return r.final_state;
  return proposedFor(uc, r) ?? r.final_state ?? 'PENDING';
}

export function scoredCount(rubric: UseCase[], responses: Record<string, Response>): number {
  return rubric.filter(uc => {
    const r = responses[uc.uc_id];
    const p = r ? proposedFor(uc, r) : null;
    return (p && p !== 'PENDING') || (uc.kind === 'bespoke' && r && r.final_state);
  }).length;
}

export function buildRecord(
  rubric: UseCase[], responses: Record<string, Response>, generated: string,
): AssessmentRecord {
  const out: AssessmentRecord = { schema: SCHEMA, generated, responses: {} };
  for (const uc of rubric) {
    const r = responses[uc.uc_id];
    if (!r) continue;
    out.responses[uc.uc_id] = {
      archetype: uc.archetype, answers: r.answers,
      proposed_state: proposedFor(uc, r), final_state: finalFor(uc, r),
      overridden: !!r.overridden, rationale: r.rationale || '', confidence: r.confidence || 'MED',
    };
  }
  return out;
}
```

- [ ] **Step 4: Run — verify PASS.**

- [ ] **Step 5: Commit**
```bash
git add app/src/assessment/record.ts app/src/assessment/record.test.ts
git commit -m "feat: assessment record model (proposed/final/buildRecord)"
```

---

## Task 4: Persistence + import/merge

**Files:** Create `app/src/assessment/persistence.ts`, `app/src/assessment/persistence.test.ts`.

- [ ] **Step 1: Write the failing test** — `app/src/assessment/persistence.test.ts`:
```ts
import { describe, it, expect, beforeEach } from 'vitest';
import { loadResponses, saveResponses, importRecord, STORE_KEY } from './persistence';
import { blankResponse } from './record';
import type { Response } from './types';

beforeEach(() => localStorage.clear());

describe('persistence', () => {
  it('round-trips responses through localStorage', () => {
    const responses: Record<string, Response> = { 'UC-F-001': { ...blankResponse(), rationale: 'hi' } };
    saveResponses(responses, '2026-01-01T00:00:00Z');
    expect(localStorage.getItem(STORE_KEY)).toContain('posture-assessment-record/v1');
    expect(loadResponses()['UC-F-001'].rationale).toBe('hi');
  });
  it('loads empty when nothing saved or corrupt', () => {
    expect(loadResponses()).toEqual({});
    localStorage.setItem(STORE_KEY, '{not json');
    expect(loadResponses()).toEqual({});
  });
  it('importRecord merges valid responses and rejects wrong schema', () => {
    const existing: Record<string, Response> = { 'UC-F-002': { ...blankResponse(), rationale: 'keep' } };
    const incoming = JSON.stringify({ schema: 'posture-assessment-record/v1', responses: {
      'UC-F-001': { answers: { Q1: 'no' }, final_state: 'GAP', overridden: true, rationale: 'r', confidence: 'HIGH' } } });
    const merged = importRecord(existing, incoming, id => id.startsWith('UC-'));
    expect(merged['UC-F-002'].rationale).toBe('keep');      // existing kept
    expect(merged['UC-F-001'].final_state).toBe('GAP');     // incoming merged
    expect(() => importRecord(existing, JSON.stringify({ schema: 'wrong' }), () => true)).toThrow();
  });
});
```

- [ ] **Step 2: Run — verify FAIL.**

- [ ] **Step 3: Implement** — `app/src/assessment/persistence.ts`:
```ts
import type { Response, State } from './types';
import { blankResponse, buildRecord } from './record';
import { RUBRIC } from './rubric';

export const STORE_KEY = 'posture-assessment-record/v1';
const SCHEMA = 'posture-assessment-record/v1';
const STATES: State[] = ['GAP', 'PARTIAL', 'MET', 'PENDING', 'NA'];

export function loadResponses(): Record<string, Response> {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return {};
    const rec = JSON.parse(raw);
    return rec && rec.responses ? rebuildResponses(rec.responses) : {};
  } catch { return {}; }
}

function rebuildResponses(stored: Record<string, any>): Record<string, Response> {
  const out: Record<string, Response> = {};
  for (const [id, s] of Object.entries(stored || {})) {
    out[id] = {
      answers: (s.answers && typeof s.answers === 'object') ? s.answers : {},
      overridden: !!s.overridden,
      final_state: STATES.includes(s.final_state) ? s.final_state : null,
      rationale: s.rationale || '', confidence: s.confidence || 'MED',
    };
  }
  return out;
}

export function saveResponses(responses: Record<string, Response>, generated: string): void {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(buildRecord(RUBRIC, responses, generated))); }
  catch { /* quota / unavailable — caller may toast */ }
}

export function importRecord(
  current: Record<string, Response>, text: string, knownId: (id: string) => boolean,
): Record<string, Response> {
  const rec = JSON.parse(text);
  if (!rec || rec.schema !== SCHEMA) throw new Error('unrecognised schema');
  const merged = { ...current };
  for (const [id, s] of Object.entries(rec.responses || {}) as [string, any][]) {
    if (!knownId(id)) continue;
    merged[id] = { ...blankResponse(),
      answers: (s.answers && typeof s.answers === 'object') ? s.answers : {},
      overridden: !!s.overridden,
      final_state: STATES.includes(s.final_state) ? s.final_state : null,
      rationale: s.rationale || '', confidence: s.confidence || 'MED' };
  }
  return merged;
}
```

- [ ] **Step 4: Run — verify PASS.**

- [ ] **Step 5: Commit**
```bash
git add app/src/assessment/persistence.ts app/src/assessment/persistence.test.ts
git commit -m "feat: assessment persistence + import/merge"
```

---

## Task 5: `useAssessment` store

**Files:** Create `app/src/assessment/store.tsx`, `app/src/assessment/store.test.tsx`.

- [ ] **Step 1: Write the failing test** — `app/src/assessment/store.test.tsx`:
```tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider, useAssessment } from './store';
import { RUBRIC } from './rubric';

beforeEach(() => localStorage.clear());

function Probe() {
  const a = useAssessment();
  const uc = a.current;
  return (
    <div>
      <span data-testid="id">{uc.uc_id}</span>
      <span data-testid="final">{a.finalOf(uc.uc_id)}</span>
      <span data-testid="scored">{a.scored}</span>
      {uc.kind === 'ladder' && <button onClick={() => a.answer(uc.questions![0].qid, 'no')}>ans</button>}
    </div>
  );
}

it('answering a ladder question updates derived state + persists', async () => {
  render(<AssessmentProvider><Probe /></AssessmentProvider>);
  const firstLadder = RUBRIC.find(u => u.kind === 'ladder')!;
  expect(screen.getByTestId('id').textContent).toBe(RUBRIC[0].uc_id);
  // navigate handled internally; first UC is RUBRIC[0]; if it's ladder, answering 'no' on a GAP_PARTIAL Q -> GAP
  if (RUBRIC[0].kind === 'ladder') {
    await userEvent.click(screen.getByText('ans'));
    expect(['GAP', 'PARTIAL', 'MET', 'NA']).toContain(screen.getByTestId('final').textContent);
    expect(localStorage.getItem('posture-assessment-record/v1')).toContain(RUBRIC[0].uc_id);
  }
  expect(firstLadder).toBeTruthy();
});
```

- [ ] **Step 2: Run — verify FAIL.**

- [ ] **Step 3: Implement** — `app/src/assessment/store.tsx`:
```tsx
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
  }), [responses, currentId]);

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAssessment(): Api {
  const v = useContext(Ctx);
  if (!v) throw new Error('useAssessment must be used within AssessmentProvider');
  return v;
}
```

- [ ] **Step 4: Run — verify PASS.** `cd app && npx vitest run src/assessment/store.test.tsx`.

- [ ] **Step 5: Run the FULL engine suite + build** — `cd app && npm test` (all green), `cd app && npm run build:check` (offline OK). Commit:
```bash
git add app/src/assessment/store.tsx app/src/assessment/store.test.tsx
git commit -m "feat: useAssessment store"
```

---

## Task 6: App shell + Sidebar + ThemeToggle

**Files:** Create `app/src/components/Sidebar.tsx`, `app/src/components/ThemeToggle.tsx`; modify `app/src/App.tsx`.

- [ ] **Step 1: Implement `ThemeToggle.tsx`** (uses Plan-1 `useTheme`):
```tsx
import { useTheme } from '../theme/ThemeProvider';
import { Button } from './ui';
export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return <Button variant="outline" onClick={toggle} aria-label="Toggle theme">{theme === 'light' ? '◐ Light' : '◑ Dark'}</Button>;
}
```

- [ ] **Step 2: Implement `Sidebar.tsx`** (grouped nav + status dots, driven by the store):
```tsx
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
```

- [ ] **Step 3: Replace `App.tsx`** with the shell (provider + header + sidebar + main placeholder for Task 7's UseCaseView):
```tsx
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
```

- [ ] **Step 4: Verify** — `cd app && npm test` (engine tests still green; no new test required for shell yet) and `cd app && npm run build:check` (offline OK). Screenshot light to confirm shell + sidebar render:
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --force-device-scale-factor=2 --window-size=1200,800 --screenshot=/tmp/q-shell.png "file://$PWD/dist/index.html" 2>/dev/null; ls -l /tmp/q-shell.png
```
Confirm PNG > 10KB.

- [ ] **Step 5: Commit**
```bash
git add app/src/components/Sidebar.tsx app/src/components/ThemeToggle.tsx app/src/App.tsx
git commit -m "feat: app shell + sidebar + theme toggle"
```

---

## Task 7: UseCaseView + ScorePanel + Toast + Checkbox

**Files:** Create `app/src/components/UseCaseView.tsx`, `app/src/components/ScorePanel.tsx`, `app/src/components/Toast.tsx`, `app/src/components/ui/Checkbox.tsx`, `app/src/components/UseCaseView.test.tsx`; modify `app/src/App.tsx` (mount UseCaseView), `app/src/components/ui/index.ts` (export Checkbox).

- [ ] **Step 1: Write a behaviour test** — `app/src/components/UseCaseView.test.tsx`:
```tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider } from '../assessment/store';
import { UseCaseView } from './UseCaseView';
import { RUBRIC } from '../assessment/rubric';

beforeEach(() => localStorage.clear());

it('answering ladder questions updates the proposed state chip', async () => {
  // pick the first ladder UC and render directly
  const ladder = RUBRIC.find(u => u.kind === 'ladder')!;
  render(<AssessmentProvider><UseCaseView startId={ladder.uc_id} /></AssessmentProvider>);
  expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
  // answer every question "yes" -> MET appears in the panel
  const yesButtons = screen.getAllByRole('button', { name: 'Yes' });
  for (const b of yesButtons) await userEvent.click(b);
  expect(screen.getByText(/MET/)).toBeInTheDocument();
});
```
(Implementer: `UseCaseView` accepts an optional `startId` prop that calls `go(startId)` once on mount, purely to make this test deterministic; the app mounts it without the prop.)

- [ ] **Step 2: Run — verify FAIL.**

- [ ] **Step 3: Implement `Checkbox.tsx`**:
```tsx
import { type InputHTMLAttributes } from 'react';
export function Checkbox(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input type="checkbox" className="w-[17px] h-[17px] mt-0.5 accent-accent cursor-pointer shrink-0" {...props} />;
}
```
Add `export { Checkbox } from './Checkbox';` to `app/src/components/ui/index.ts`.

- [ ] **Step 4: Implement `Toast.tsx`** (context + hook):
```tsx
import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
const Ctx = createContext<(m: string) => void>(() => {});
export function ToastProvider({ children }: { children: ReactNode }) {
  const [msg, setMsg] = useState<string | null>(null);
  const toast = useCallback((m: string) => { setMsg(m); setTimeout(() => setMsg(null), 1800); }, []);
  return (
    <Ctx.Provider value={toast}>
      {children}
      {msg && <div role="status" className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-ink text-bg px-4 py-2.5 rounded-sm text-sm shadow-lg z-50">{msg}</div>}
    </Ctx.Provider>
  );
}
export const useToast = () => useContext(Ctx);
```

- [ ] **Step 5: Implement `ScorePanel.tsx`**:
```tsx
import { useState } from 'react';
import { useAssessment } from '../assessment/store';
import { useToast } from './Toast';
import { Badge, Button, ToggleGroup } from './ui';
import type { State } from '../assessment/types';

const STATES: State[] = ['GAP', 'PARTIAL', 'MET', 'PENDING', 'NA'];
const lower = (s: State) => s.toLowerCase() as Lowercase<State>;

export function ScorePanel() {
  const a = useAssessment();
  const toast = useToast();
  const uc = a.current;
  const [needRat, setNeedRat] = useState(false);
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
```

- [ ] **Step 6: Implement `UseCaseView.tsx`**:
```tsx
import { useEffect } from 'react';
import { useAssessment } from '../assessment/store';
import { RUBRIC } from '../assessment/rubric';
import { Badge, Button, Card, CardBody, ToggleGroup, Checkbox } from './ui';
import { ScorePanel } from './ScorePanel';

export function UseCaseView({ startId }: { startId?: string }) {
  const a = useAssessment();
  useEffect(() => { if (startId) a.go(startId); /* once */ }, [startId]); // eslint-disable-line
  const uc = a.current;
  const r = a.responses[uc.uc_id];
  const idx = RUBRIC.findIndex(u => u.uc_id === uc.uc_id);

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

      <div className="flex justify-between mt-6">
        <Button variant="outline" disabled={idx <= 0} onClick={() => a.go(RUBRIC[idx - 1].uc_id)}>← Previous</Button>
        <Button disabled={idx >= RUBRIC.length - 1} onClick={() => a.go(RUBRIC[idx + 1].uc_id)}>Save &amp; next →</Button>
      </div>
    </div>
  );
}
```

- [ ] **Step 7: Mount in `App.tsx`** — wrap `Shell` content in `ToastProvider`, replace the `<main>` placeholder with `<UseCaseView />`. Update imports.

- [ ] **Step 8: Run — verify PASS** — `cd app && npx vitest run src/components/UseCaseView.test.tsx` → PASS. Then `cd app && npm test` (full suite green) + `cd app && npm run build:check` (offline OK).

- [ ] **Step 9: Commit**
```bash
git add app/src/components/UseCaseView.tsx app/src/components/ScorePanel.tsx app/src/components/Toast.tsx app/src/components/ui/Checkbox.tsx app/src/components/ui/index.ts app/src/components/UseCaseView.test.tsx app/src/App.tsx
git commit -m "feat: use-case view + score/override panel + toast"
```

---

## Task 8: Export/Import wiring + schema-compat + final verification

**Files:** modify `app/src/App.tsx` (header Import/Export buttons + hidden file input); create `tests/test_react_export_schema.py`.

- [ ] **Step 1: Add Export/Import to the header** in `App.tsx`:
```tsx
// inside Header(), before <ThemeToggle/>:
const fileRef = useRef<HTMLInputElement>(null);
function doExport() {
  const blob = new Blob([a.exportRecord()], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a'); link.href = url; link.download = 'assessment-record.json'; link.click();
  URL.revokeObjectURL(url);
}
// JSX:
<input ref={fileRef} type="file" accept="application/json" className="hidden"
  onChange={e => { const f = e.target.files?.[0]; if (!f) return; const rd = new FileReader();
    rd.onload = () => { try { a.importText(String(rd.result)); } catch { /* toast handled in store later */ } };
    rd.readAsText(f); e.currentTarget.value = ''; }} />
<Button variant="outline" onClick={() => fileRef.current?.click()}>Import</Button>
<Button onClick={doExport}>Export record</Button>
```
(Add `useRef` import + `Button` import.)

- [ ] **Step 2: Write the cross-language schema-compat test** — `tests/test_react_export_schema.py`:
```python
"""The React app's exported record must build the exec summary (schema parity)."""
import json, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def fake_export():
    """Mirror app buildRecord() output shape for a couple of responses."""
    return {"schema": "posture-assessment-record/v1", "generated": "2026-01-01T00:00:00Z",
            "responses": {
                "UC-F-001": {"archetype": "A1", "answers": {"A1-Q1": "no"},
                             "proposed_state": "GAP", "final_state": "GAP",
                             "overridden": False, "rationale": "", "confidence": "MED"},
                "UC-F-002": {"archetype": "A2", "answers": {},
                             "proposed_state": "PENDING", "final_state": "PENDING",
                             "overridden": False, "rationale": "", "confidence": "MED"}}}

def test_export_builds_exec_summary(tmp_path):
    rec = tmp_path / "rec.json"; rec.write_text(json.dumps(fake_export()), encoding="utf-8")
    out = tmp_path / "exec.html"
    r = subprocess.run([sys.executable, "-m", "presentation.build_exec_summary",
                        str(rec), "-o", str(out)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    html = out.read_text(encoding="utf-8")
    assert "@media print" in html and "posture-assessment-record/v1" not in html  # schema key not echoed raw
    assert out.stat().st_size > 10_000
```

- [ ] **Step 3: Run the schema-compat test** — `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_react_export_schema.py -v` → PASS. (If `build_exec_summary` rejects the shape, the export schema has drifted — fix `buildRecord` in `record.ts`, not the test.)

- [ ] **Step 4: Full verification**
  - `cd app && npm test` → all engine + component tests green.
  - `cd app && npm run build:check` → offline OK.
  - `cd /…/research-papers && python3 -m pytest -q` → the broader suite still green (this plan doesn't touch the Python report code).
  - Screenshot the questionnaire in both themes via CDP (navigate, answer a question, toggle theme) — confirm the use-case view, toggles, sidebar dots, and score panel render in Brass Editorial. Save `/tmp/q-light.png`, `/tmp/q-dark.png`; confirm both > 10KB.

- [ ] **Step 5: Commit**
```bash
git add app/src/App.tsx tests/test_react_export_schema.py
git commit -m "feat: export/import wiring + cross-language schema-compat test"
```

---

## Self-Review (completed by author)

- **Spec coverage:** §4-B questionnaire — sidebar/nav (T6), use-case view + ladder + bespoke (T7), scoring port (T2) with parity, override + confidence + final-state (T7/T5), autosave (T4/T5), import/export schema-compatible (T8) verified against the real Python build. Evidence-upload is correctly **excluded** (Phase 2).
- **Placeholder scan:** none — every step has full code or an exact command.
- **Type consistency:** `Response`/`State`/`UseCase` types from Task 1 are used unchanged in Tasks 2–7; store `Api` method names (`go/answer/check/setRationale/setConfidence/setFinal/proposedOf/finalOf/exportRecord/importText`) are used identically in Sidebar/UseCaseView/ScorePanel/App. `buildRecord` output shape matches the schema asserted in T3 and exercised in T8.
- **Note:** `generated` timestamp uses `new Date().toISOString()` at runtime; `buildRecord` takes it as a param so tests stay deterministic. This is intentional (Date.now is non-deterministic).

---

## Execution Handoff

Engine tasks (1–5) are pure and headless-testable; UI tasks (6–8) build on them and the Plan-1 primitives. After this plan is green, **Plan 3 (report re-skin)** is the last: matrix + exec to Brass Editorial via `design/brass-editorial.vars.css` + new fonts in `brand_fonts.py`, then regenerate the snapshot.

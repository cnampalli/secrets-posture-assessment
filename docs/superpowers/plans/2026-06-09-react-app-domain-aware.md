# React App Domain-Awareness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the interactive React assessment app load and isolate **both** Secrets (47 UCs) and PAM (17 UCs), switchable via a header dropdown, with per-domain storage that never collides.

**Architecture:** A Python emit step writes one rubric JSON per domain (bundled). A `domains.ts` registry + a `makeRubric(domainId)` factory replace the single hard-coded rubric. The `AssessmentProvider` store holds the active `domainId` and `RubricView`; `setDomain` swaps the rubric and reloads that domain's responses/evidence from a per-domain namespace (localStorage key suffix + IndexedDB id prefix), with a one-shot migration of legacy un-namespaced data into the `secrets` namespace.

**Tech Stack:** Python 3 (rubric emit), React 19 + TypeScript + Vite + Vitest, Tailwind. Offline single-file build via `vite-plugin-singlefile` (`npm run build:check`).

**Spec:** `docs/superpowers/specs/2026-06-09-react-app-domain-aware-design.md`

**Incremental strategy:** Tasks keep the app compiling and green at every commit. `rubric.ts` keeps `RUBRIC`/`byId`/`byCategory` as default-domain **shims** until the final task removes them, so consumers migrate one task at a time.

---

### Task 1: Multi-domain rubric emit (Python)

**Files:**
- Modify: `questionnaire/emit_rubric.py`
- Create: `tests/test_emit_rubric.py`
- Generated (by running the script): `app/src/data/rubric.secrets.json`, `app/src/data/rubric.pam.json`

- [ ] **Step 1: Write the failing test**

Create `tests/test_emit_rubric.py`:

```python
import json, pathlib
import questionnaire.emit_rubric as emit

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_emits_both_domains(tmp_path, monkeypatch):
    # redirect output into a temp app/src/data so the test never clobbers the repo copy
    out_dir = tmp_path / "data"
    monkeypatch.setattr(emit, "OUT_DIR", str(out_dir))
    emit.main()
    secrets = json.loads((out_dir / "rubric.secrets.json").read_text(encoding="utf-8"))
    pam = json.loads((out_dir / "rubric.pam.json").read_text(encoding="utf-8"))
    assert len(secrets) == 47
    assert len(pam) == 17
    assert {u["uc_id"] for u in pam} == {f"UC-P-{i:03d}" for i in range(1, 18)}
    # methodology-only secrets carry no evidence; both are ladder/bespoke shaped
    assert all("uc_id" in u and "questions" in u or u["kind"] == "bespoke" for u in secrets)


def test_domains_registry_drives_output():
    # the script exposes a DOMAINS list so adding a domain is a one-line change
    ids = {d["id"] for d in emit.DOMAINS}
    assert {"secrets", "pam"} <= ids
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_emit_rubric.py -q`
Expected: FAIL — `emit_rubric` has no `DOMAINS` / `OUT_DIR` attributes.

- [ ] **Step 3: Rewrite `questionnaire/emit_rubric.py`**

Replace the whole file with:

```python
#!/usr/bin/env python3
"""Emit one rubric JSON per domain for the React app.

methodology/ is the source of truth for the shared question templates; each
domain's uc-archetype map (+ optional evidence/regulatory data) comes from its
data dir. Add a domain by adding one row to DOMAINS."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METH = os.path.join(ROOT, "methodology")
OUT_DIR = os.path.join(ROOT, "app", "src", "data")

# data_dir=None => methodology-only (secrets). file = rubric.<id>.json
DOMAINS = [
    {"id": "secrets", "data_dir": None},
    {"id": "pam", "data_dir": os.path.join(ROOT, "matrix", "domains", "pam")},
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for d in DOMAINS:
        rubric = rubric_loader.load_rubric(METH, data_dir=d["data_dir"])
        out = os.path.join(OUT_DIR, f"rubric.{d['id']}.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(rubric, fh, ensure_ascii=False, indent=2)
        print(f"wrote {out} ({len(rubric)} use cases)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the emit script + tests**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 questionnaire/emit_rubric.py && python3 -m pytest tests/test_emit_rubric.py -q`
Expected: prints `wrote …/rubric.secrets.json (47 use cases)` and `…/rubric.pam.json (17 use cases)`; tests PASS. (Leave the old `app/src/data/rubric.json` in place — Task 2 removes it.)

- [ ] **Step 5: Run the full Python suite (no regression)**

Run: `python3 -m pytest -q`
Expected: all pass (was 232 + the 2 new emit tests).

- [ ] **Step 6: Commit**

```bash
git add questionnaire/emit_rubric.py tests/test_emit_rubric.py app/src/data/rubric.secrets.json app/src/data/rubric.pam.json
git commit -m "feat(emit): emit per-domain rubric JSON (secrets 47 / pam 17)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Domain registry + rubric factory (shims preserved)

**Files:**
- Create: `app/src/assessment/domains.ts`
- Modify: `app/src/assessment/rubric.ts`
- Delete: `app/src/data/rubric.json`
- Test: `app/src/assessment/domains.test.ts`

- [ ] **Step 1: Write the failing test**

Create `app/src/assessment/domains.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { DOMAINS, DEFAULT_DOMAIN, getDomain } from './domains';
import { makeRubric } from './rubric';

describe('domain registry', () => {
  it('registers secrets and pam', () => {
    expect(DOMAINS.map(d => d.id).sort()).toEqual(['pam', 'secrets']);
    expect(DEFAULT_DOMAIN).toBe('secrets');
  });

  it('carries the right rubric per domain', () => {
    expect(getDomain('secrets').rubric.length).toBe(47);
    expect(getDomain('pam').rubric.length).toBe(17);
  });

  it('falls back to the default domain on an unknown id', () => {
    // @ts-expect-error exercising the runtime fallback
    expect(getDomain('nope').id).toBe('secrets');
  });
});

describe('makeRubric factory', () => {
  it('indexes and groups the active domain', () => {
    const pam = makeRubric('pam');
    expect(pam.byId('UC-P-017')?.archetype).toBe('A8');
    expect(pam.byId('NOPE')).toBeUndefined();
    const groups = pam.byCategory();
    expect(Object.keys(groups).length).toBeGreaterThan(0);
    const total = Object.values(groups).reduce((n, l) => n + l.length, 0);
    expect(total).toBe(17);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd app && npm test -- domains`
Expected: FAIL — `./domains` not found / `makeRubric` not exported.

- [ ] **Step 3: Create `app/src/assessment/domains.ts`**

```ts
import type { UseCase } from './types';
import secrets from '../data/rubric.secrets.json';
import pam from '../data/rubric.pam.json';

export type DomainId = 'secrets' | 'pam';

export interface Domain { id: DomainId; label: string; rubric: UseCase[]; }

export const DOMAINS: Domain[] = [
  { id: 'secrets', label: 'Secrets Management', rubric: secrets as unknown as UseCase[] },
  { id: 'pam', label: 'Privileged Access (PAM)', rubric: pam as unknown as UseCase[] },
];

export const DEFAULT_DOMAIN: DomainId = 'secrets';

const BY_ID = new Map(DOMAINS.map(d => [d.id, d]));

/** Never throws into render: unknown ids resolve to the default domain. */
export function getDomain(id: DomainId): Domain {
  return BY_ID.get(id) ?? BY_ID.get(DEFAULT_DOMAIN)!;
}

export function isDomainId(v: unknown): v is DomainId {
  return typeof v === 'string' && BY_ID.has(v as DomainId);
}
```

- [ ] **Step 4: Rewrite `app/src/assessment/rubric.ts`** (factory + shims)

```ts
import type { UseCase } from './types';
import { getDomain, DEFAULT_DOMAIN, type DomainId } from './domains';

export interface RubricView {
  rubric: UseCase[];
  byId: (uc_id: string) => UseCase | undefined;
  byCategory: () => Record<string, UseCase[]>;
}

export function makeRubric(domainId: DomainId): RubricView {
  const rubric = getDomain(domainId).rubric;
  const index = new Map(rubric.map(uc => [uc.uc_id, uc]));
  return {
    rubric,
    byId: (uc_id) => index.get(uc_id),
    byCategory: () => {
      const out: Record<string, UseCase[]> = {};
      for (const uc of rubric) (out[uc.category] ||= []).push(uc);
      return out;
    },
  };
}

// --- Back-compat shims (default domain). Removed in the final task once every
// consumer reads the active rubric from the store. ---
const DEFAULT_VIEW = makeRubric(DEFAULT_DOMAIN);
export const RUBRIC = DEFAULT_VIEW.rubric;
export const byId = DEFAULT_VIEW.byId;
export function byCategory(): Record<string, UseCase[]> { return DEFAULT_VIEW.byCategory(); }
```

- [ ] **Step 5: Delete the obsolete single rubric**

Run: `rm app/src/data/rubric.json`

- [ ] **Step 6: Run tests + typecheck**

Run: `cd app && npm test -- domains && npx tsc -b`
Expected: domains tests PASS; `tsc` clean (shims keep store/Sidebar/persistence compiling).

- [ ] **Step 7: Commit**

```bash
git add app/src/assessment/domains.ts app/src/assessment/domains.test.ts app/src/assessment/rubric.ts
git rm app/src/data/rubric.json
git commit -m "feat(app): domain registry + makeRubric factory (shims kept)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Per-domain persistence + legacy migration

**Files:**
- Modify: `app/src/assessment/persistence.ts`
- Modify (call sites only, behaviour-preserving): `app/src/assessment/store.tsx`
- Test: `app/src/assessment/persistence.test.ts` (exists — add cases)

**Interface change:** persistence functions become domain-scoped. New signatures:
- `keyFor(domainId: DomainId): string`
- `migrateLegacy(): void` — one-shot copy of the old un-suffixed key into the `secrets` namespace
- `loadResponses(domainId: DomainId)`
- `saveResponses(domainId: DomainId, rubric: UseCase[], responses, generated, evidence?)`
- `loadEvidence(domainId: DomainId)`
- `importRecord(current, text, knownId)` — **unchanged** (no key access)

- [ ] **Step 1: Write the failing tests** — **REPLACE the whole file** `app/src/assessment/persistence.test.ts`

The existing file imports `STORE_KEY` and calls the old single-domain signatures (`saveResponses(responses, …)`, `loadResponses()`), which this task removes. Replace the entire file with the migrated cases + the new isolation/migration cases:

```ts
import { describe, it, test, expect, beforeEach } from 'vitest';
import { keyFor, migrateLegacy, loadResponses, saveResponses, importRecord, loadEvidence } from './persistence';
import { blankResponse } from './record';
import { makeRubric } from './rubric';
import type { Response, EvidenceMeta } from './types';

const SECRETS = makeRubric('secrets').rubric;
const PAM = makeRubric('pam').rubric;

beforeEach(() => localStorage.clear());

describe('persistence (per-domain)', () => {
  it('round-trips responses through the domain-scoped key', () => {
    const responses: Record<string, Response> = { 'UC-F-001': { ...blankResponse(), rationale: 'hi' } };
    saveResponses('secrets', SECRETS, responses, '2026-01-01T00:00:00Z');
    expect(localStorage.getItem(keyFor('secrets'))).toContain('posture-assessment-record/v1');
    expect(loadResponses('secrets')['UC-F-001'].rationale).toBe('hi');
  });

  it('loads empty when nothing saved or corrupt', () => {
    expect(loadResponses('secrets')).toEqual({});
    localStorage.setItem(keyFor('secrets'), '{not json');
    expect(loadResponses('secrets')).toEqual({});
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

  it('namespaces the storage key by domain', () => {
    expect(keyFor('secrets')).toBe('posture-assessment-record/v1/secrets');
    expect(keyFor('pam')).toBe('posture-assessment-record/v1/pam');
  });

  it('isolates domains: a PAM save is invisible to secrets', () => {
    const resp: Record<string, Response> = { 'UC-P-001': { ...blankResponse(), answers: { 'A4-Q1': 'yes' } } };
    saveResponses('pam', PAM, resp, '2026-01-01T00:00:00Z');
    expect(Object.keys(loadResponses('secrets'))).toHaveLength(0);
    expect(loadResponses('pam')['UC-P-001'].answers['A4-Q1']).toBe('yes');
  });

  it('migrates a legacy un-namespaced record into the secrets namespace', () => {
    localStorage.setItem('posture-assessment-record/v1', JSON.stringify({
      schema: 'posture-assessment-record/v1', generated: 'x',
      responses: { 'UC-F-001': { archetype: 'A1', answers: { 'A1-Q1': 'yes' }, proposed_state: 'PARTIAL', final_state: 'PARTIAL', overridden: false, rationale: '', confidence: 'MED' } },
    }));
    migrateLegacy();
    expect(localStorage.getItem(keyFor('secrets'))).toBeTruthy();
    expect(loadResponses('secrets')['UC-F-001'].answers['A1-Q1']).toBe('yes');
    expect(localStorage.getItem('posture-assessment-record/v1')).toBeNull();
  });

  it('migrateLegacy is a no-op when the secrets namespace already exists', () => {
    localStorage.setItem(keyFor('secrets'), JSON.stringify({ schema: 'posture-assessment-record/v1', generated: 'kept', responses: {} }));
    localStorage.setItem('posture-assessment-record/v1', JSON.stringify({ schema: 'posture-assessment-record/v1', generated: 'legacy', responses: {} }));
    migrateLegacy();
    expect(JSON.parse(localStorage.getItem(keyFor('secrets'))!).generated).toBe('kept');
  });
});

test('saveResponses persists evidence metadata; loadEvidence reads it back', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [SECRETS[0].uc_id]: [{ id: 'p1', name: 'a.pdf', type: 'application/pdf', size: 9, added: 'T' }],
  };
  saveResponses('secrets', SECRETS, {}, 'T', ev);
  expect(loadEvidence('secrets')).toEqual(ev);
});

test('loadEvidence returns {} when nothing stored', () => {
  localStorage.clear();
  expect(loadEvidence('secrets')).toEqual({});
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd app && npm test -- persistence`
Expected: FAIL — `keyFor`/`migrateLegacy` not exported; `loadResponses`/`saveResponses` arity wrong.

- [ ] **Step 3: Rewrite `app/src/assessment/persistence.ts`**

```ts
import type { Response, State, EvidenceMeta, UseCase } from './types';
import { blankResponse, buildRecord } from './record';
import { DEFAULT_DOMAIN, type DomainId } from './domains';

const PREFIX = 'posture-assessment-record/v1';
const LEGACY_KEY = PREFIX; // the old single, un-namespaced key
const SCHEMA = 'posture-assessment-record/v1';
const STATES: State[] = ['GAP', 'PARTIAL', 'MET', 'PENDING', 'NA'];

export function keyFor(domainId: DomainId): string { return `${PREFIX}/${domainId}`; }

/** One-shot: fold a legacy un-namespaced record into the secrets namespace. */
export function migrateLegacy(): void {
  try {
    const legacy = localStorage.getItem(LEGACY_KEY);
    if (legacy === null) return;
    if (localStorage.getItem(keyFor(DEFAULT_DOMAIN)) === null) {
      localStorage.setItem(keyFor(DEFAULT_DOMAIN), legacy);
    }
    localStorage.removeItem(LEGACY_KEY);
  } catch { /* storage unavailable — nothing to migrate */ }
}

function rebuildResponses(stored: Record<string, unknown>): Record<string, Response> {
  const out: Record<string, Response> = {};
  for (const [id, s] of Object.entries(stored || {})) {
    const entry = s as Record<string, unknown>;
    out[id] = {
      answers: (entry.answers && typeof entry.answers === 'object') ? entry.answers as Record<string, never> : {},
      overridden: !!entry.overridden,
      final_state: STATES.includes(entry.final_state as State) ? (entry.final_state as State) : null,
      rationale: (entry.rationale as string) || '', confidence: (entry.confidence as 'LOW' | 'MED' | 'HIGH') || 'MED',
    };
  }
  return out;
}

export function loadResponses(domainId: DomainId): Record<string, Response> {
  try {
    const raw = localStorage.getItem(keyFor(domainId));
    if (!raw) return {};
    const rec = JSON.parse(raw);
    return rec && rec.responses ? rebuildResponses(rec.responses) : {};
  } catch { return {}; }
}

export function saveResponses(
  domainId: DomainId, rubric: UseCase[],
  responses: Record<string, Response>, generated: string,
  evidence?: Record<string, EvidenceMeta[]>,
): void {
  try { localStorage.setItem(keyFor(domainId), JSON.stringify(buildRecord(rubric, responses, generated, evidence))); }
  catch { /* quota / unavailable — caller may toast */ }
}

export function loadEvidence(domainId: DomainId): Record<string, EvidenceMeta[]> {
  try {
    const raw = localStorage.getItem(keyFor(domainId));
    if (!raw) return {};
    const rec = JSON.parse(raw);
    const ev = rec && rec.evidence;
    if (!ev || typeof ev !== 'object') return {};
    const out: Record<string, EvidenceMeta[]> = {};
    for (const [id, list] of Object.entries(ev)) if (Array.isArray(list)) out[id] = list as EvidenceMeta[];
    return out;
  } catch { return {}; }
}

export function importRecord(
  current: Record<string, Response>, text: string, knownId: (id: string) => boolean,
): Record<string, Response> {
  const rec = JSON.parse(text) as Record<string, unknown>;
  if (!rec || rec['schema'] !== SCHEMA) throw new Error('unrecognised schema');
  const merged = { ...current };
  for (const [id, s] of Object.entries((rec['responses'] as Record<string, unknown>) || {})) {
    if (!knownId(id)) continue;
    const entry = s as Record<string, unknown>;
    merged[id] = { ...blankResponse(),
      answers: (entry.answers && typeof entry.answers === 'object') ? entry.answers as Record<string, never> : {},
      overridden: !!entry.overridden,
      final_state: STATES.includes(entry.final_state as State) ? (entry.final_state as State) : null,
      rationale: (entry.rationale as string) || '', confidence: (entry.confidence as 'LOW' | 'MED' | 'HIGH') || 'MED' };
  }
  return merged;
}
```

Note: `STORE_KEY` export is removed. If anything imports it, update to `keyFor(...)`. (Only `persistence.ts` used it internally.)

- [ ] **Step 4: Update `store.tsx` call sites (behaviour-preserving, still single-domain)**

In `app/src/assessment/store.tsx`, the provider still uses the `RUBRIC` shim and the default domain for now. Make these edits:

Change the persistence import line to add `migrateLegacy`:
```ts
import { loadResponses, saveResponses, importRecord, loadEvidence, migrateLegacy } from './persistence';
```
Add the default-domain import:
```ts
import { DEFAULT_DOMAIN } from './domains';
```
Run the migration once before initial load, and pass the domain + rubric to persistence. Replace the two `useState` initialisers and `persistAll`:
```ts
  const [responses, setResponses] = useState<Record<string, Response>>(() => { migrateLegacy(); return loadResponses(DEFAULT_DOMAIN); });
  const [currentId, setCurrentId] = useState<string>(RUBRIC[0]?.uc_id ?? '');
  const ref = useRef(responses); ref.current = responses;

  const [evidence, setEvidence] = useState<Record<string, EvidenceMeta[]>>(() => loadEvidence(DEFAULT_DOMAIN));
  const evRef = useRef(evidence); evRef.current = evidence;

  function persistAll(nextResp: Record<string, Response>, nextEv: Record<string, EvidenceMeta[]>) {
    setResponses(nextResp); setEvidence(nextEv); saveResponses(DEFAULT_DOMAIN, RUBRIC, nextResp, now(), nextEv);
  }
```

- [ ] **Step 5: Run tests + typecheck**

Run: `cd app && npm test -- persistence && npx tsc -b`
Expected: persistence tests PASS; `tsc` clean. Run `npm test` to confirm the existing record/store tests still pass.

- [ ] **Step 6: Commit**

```bash
git add app/src/assessment/persistence.ts app/src/assessment/persistence.test.ts app/src/assessment/store.tsx
git commit -m "feat(app): namespace responses/evidence per domain + legacy migration

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Store carries active domain + setDomain

**Files:**
- Modify: `app/src/assessment/store.tsx`
- Test: `app/src/assessment/store.test.tsx` (exists — add cases)

**Api additions:** `domainId: DomainId`, `setDomain: (id: DomainId) => void`, `byCategory: () => Record<string, UseCase[]>`, `rubric: UseCase[]`. Evidence ids gain a `<domainId>/` prefix. Persistence calls use the active domain + active rubric (`makeRubric`).

- [ ] **Step 1: Write the failing tests** (append to `app/src/assessment/store.test.tsx`)

```tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { act, render } from '@testing-library/react';
import { AssessmentProvider, useAssessment } from './store';

function harness() {
  const api: { current: ReturnType<typeof useAssessment> | null } = { current: null };
  function Probe() { api.current = useAssessment(); return null; }
  render(<AssessmentProvider><Probe /></AssessmentProvider>);
  return api;
}

describe('domain-aware store', () => {
  beforeEach(() => localStorage.clear());

  it('defaults to secrets and exposes its rubric', () => {
    const api = harness();
    expect(api.current!.domainId).toBe('secrets');
    expect(api.current!.rubric.length).toBe(47);
  });

  it('setDomain swaps to PAM and its 17-UC rubric', () => {
    const api = harness();
    act(() => api.current!.setDomain('pam'));
    expect(api.current!.domainId).toBe('pam');
    expect(api.current!.rubric.length).toBe(17);
    expect(api.current!.current.uc_id.startsWith('UC-P-')).toBe(true);
    const total = Object.values(api.current!.byCategory()).reduce((n, l) => n + l.length, 0);
    expect(total).toBe(17);
  });

  it('isolates responses across domains', () => {
    const api = harness();
    act(() => { api.current!.go('UC-F-001'); api.current!.answer('A1-Q1', 'yes'); });
    act(() => api.current!.setDomain('pam'));
    // PAM starts clean — the secrets answer is not visible here
    expect(Object.keys(api.current!.responses)).toHaveLength(0);
    act(() => api.current!.setDomain('secrets'));
    expect(api.current!.responses['UC-F-001'].answers['A1-Q1']).toBe('yes');
  });

  it('persists the selected domain across remounts', () => {
    const a1 = harness();
    act(() => a1.current!.setDomain('pam'));
    const a2 = harness();
    expect(a2.current!.domainId).toBe('pam');
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd app && npm test -- store`
Expected: FAIL — `domainId`/`setDomain`/`rubric`/`byCategory` not on the Api.

- [ ] **Step 3: Update `app/src/assessment/store.tsx`**

Replace the imports of `RUBRIC, byId` and add the factory + domains:
```ts
import { makeRubric, type RubricView } from './rubric';
import { DEFAULT_DOMAIN, isDomainId, type DomainId } from './domains';
```
Add the persisted-domain key constant near the top (after imports):
```ts
const ACTIVE_DOMAIN_KEY = 'posture-active-domain';
function initialDomain(): DomainId {
  try { const v = localStorage.getItem(ACTIVE_DOMAIN_KEY); if (isDomainId(v)) return v; } catch { /* ignore */ }
  return DEFAULT_DOMAIN;
}
```
Extend the `Api` interface with:
```ts
  domainId: DomainId; setDomain: (id: DomainId) => void;
  rubric: UseCase[]; byCategory: () => Record<string, UseCase[]>;
```
Rewrite the top of `AssessmentProvider` to hold domain + view, run migration once, and load per-domain:
```ts
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
  }
```
Inside the `useMemo` Api object, replace every `byId(` with `view.byId(` and every `RUBRIC` with `view.rubric`, and add the new fields. Specifically:
- `get current() { return view.byId(currentId) ?? view.rubric[0]; }`
- `responses, scored: scoredCount(view.rubric, responses),`
- add `domainId, setDomain, rubric: view.rubric, byCategory: view.byCategory,`
- in `setFinal`: `const uc = view.byId(currentId)!;`
- in `proposedOf`/`finalOf`: `const uc = view.byId(id);`
- in `evidence` `addEvidence`: prefix the id — `const id = \`${domainId}/${genId()}\`;`
- in `exportRecord`: `buildExportRecord(view.rubric, ...)`
- in `importText`: `importRecord(ref.current, text, id => !!view.byId(id))` and `restoreEvidence(evRef.current, parsed.evidence ?? {}, id => !!view.byId(id))`
- update the `useMemo` dep array to `[domainId, view, responses, currentId, evidence]`.

Also add `UseCase` to the type import from `./types` if not already present (it is).

- [ ] **Step 4: Run tests + typecheck**

Run: `cd app && npm test -- store && npx tsc -b`
Expected: new store tests PASS; `tsc` clean. Run full `cd app && npm test` — all green.

- [ ] **Step 5: Commit**

```bash
git add app/src/assessment/store.tsx app/src/assessment/store.test.tsx
git commit -m "feat(app): store carries active domain + setDomain (per-domain isolation)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Domain dropdown, Sidebar wiring, export tagging, remove shims

**Files:**
- Create: `app/src/components/DomainPicker.tsx`
- Create: `app/src/components/DomainPicker.test.tsx`
- Modify: `app/src/App.tsx` (mount picker in header, domain-aware export filename + import warning)
- Modify: `app/src/components/Sidebar.tsx` (use `a.byCategory()`)
- Modify: `app/src/assessment/types.ts` (`AssessmentRecord.domain?`)
- Modify: `app/src/assessment/record.ts` (`buildRecord` writes `domain`)
- Modify: `app/src/assessment/rubric.ts` (delete shims)

- [ ] **Step 1: Write the failing test**

Create `app/src/components/DomainPicker.test.tsx`:

```tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AssessmentProvider, useAssessment } from '../assessment/store';
import { DomainPicker } from './DomainPicker';

function Probe() { const a = useAssessment(); return <span data-testid="dom">{a.domainId}</span>; }

describe('DomainPicker', () => {
  beforeEach(() => localStorage.clear());

  it('lists both domains and switches the active domain', async () => {
    render(<AssessmentProvider><DomainPicker /><Probe /></AssessmentProvider>);
    const select = screen.getByLabelText(/assessment domain/i) as HTMLSelectElement;
    expect(select.value).toBe('secrets');
    expect(screen.getByRole('option', { name: /Privileged Access/ })).toBeInTheDocument();
    await userEvent.selectOptions(select, 'pam');
    expect(screen.getByTestId('dom').textContent).toBe('pam');
  });
});
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd app && npm test -- DomainPicker`
Expected: FAIL — `./DomainPicker` not found.

- [ ] **Step 3: Create `app/src/components/DomainPicker.tsx`**

```tsx
import { useAssessment } from '../assessment/store';
import { DOMAINS, type DomainId } from '../assessment/domains';

export function DomainPicker() {
  const a = useAssessment();
  return (
    <label className="flex items-center gap-1.5 text-sm">
      <span className="sr-only">Assessment domain</span>
      <select
        aria-label="Assessment domain"
        value={a.domainId}
        onChange={e => a.setDomain(e.target.value as DomainId)}
        className="bg-bg2 border border-border rounded-sm px-2 py-1 text-ink2 font-display"
      >
        {DOMAINS.map(d => <option key={d.id} value={d.id}>{d.label}</option>)}
      </select>
    </label>
  );
}
```

- [ ] **Step 4: Mount the picker + domain-aware export/import in `app/src/App.tsx`**

Add the import:
```ts
import { DomainPicker } from './components/DomainPicker';
```
In `Header`, place the picker right after the `/ Questionnaire` span:
```tsx
      <span className="text-muted text-sm">/ Questionnaire</span>
      <DomainPicker />
```
Make the export filename domain-aware — in `doExport`, change the download name:
```ts
      const link = document.createElement('a'); link.href = url; link.download = `assessment-${a.domainId}.json`; link.click();
```
Warn on a cross-domain import — in the file `onChange` handler, after a successful `importText`, compare the parsed domain:
```ts
          rd.onload = async () => {
            try {
              const parsed = JSON.parse(String(rd.result));
              await a.importText(String(rd.result));
              if (parsed && parsed.domain && parsed.domain !== a.domainId)
                toast(`Imported — note: file domain "${parsed.domain}" differs from "${a.domainId}"; only matching items were merged`);
              else toast('Record imported');
            }
            catch { toast('Import failed — check the file'); }
          };
```

- [ ] **Step 5: Wire `Sidebar.tsx` to the active domain**

Replace the module import + usage:
```ts
import { useAssessment } from '../assessment/store';
import type { State } from '../assessment/types';
```
(remove `import { byCategory } from '../assessment/rubric';`) and inside the component:
```ts
  const a = useAssessment();
  const groups = a.byCategory();
```

- [ ] **Step 6: Tag the exported record with its domain**

In `app/src/assessment/types.ts`, add `domain` to `AssessmentRecord` (import `DomainId`):
```ts
import type { DomainId } from './domains';
```
```ts
export interface AssessmentRecord {
  schema: 'posture-assessment-record/v1'; domain?: DomainId; generated: string;
  responses: Record<string, { /* unchanged */ }>;
  evidence?: Record<string, EvidenceMeta[]>;
}
```
In `app/src/assessment/record.ts`, give `buildRecord` an optional domain and write it:
```ts
import type { UseCase, Response, State, AssessmentRecord, EvidenceMeta } from './types';
import type { DomainId } from './domains';
import { deriveState } from './scoring';
```
Change the signature + first line:
```ts
export function buildRecord(
  rubric: UseCase[], responses: Record<string, Response>, generated: string,
  evidence?: Record<string, EvidenceMeta[]>, domain?: DomainId,
): AssessmentRecord {
  const out: AssessmentRecord = { schema: SCHEMA, generated, responses: {} };
  if (domain) out.domain = domain;
```
Thread the domain through the two callers:
- `persistence.ts` `saveResponses`: `buildRecord(rubric, responses, generated, evidence, domainId)`.
- `evidence.ts` `buildExportRecord`: add a `domain?: DomainId` param (last) and pass it to `buildRecord(rubric, responses, generated, undefined, domain)`; then in `store.tsx` `exportRecord`, pass `domainId`.

(These are small signature threads; the export domain field is what enables the filename + import warning.)

- [ ] **Step 7: Remove the shims from `app/src/assessment/rubric.ts`**

Delete the back-compat block (the `DEFAULT_VIEW`, `RUBRIC`, `byId`, `byCategory` exports). Keep only `RubricView` + `makeRubric`. Confirm nothing still imports them:

Run: `cd app && grep -rn "RUBRIC\b\|from './rubric'\|from '../assessment/rubric'" src | grep -v makeRubric | grep -v RubricView`
Expected: no remaining `RUBRIC`/`byId`/`byCategory` singleton imports (only `makeRubric`/`RubricView`).

- [ ] **Step 8: Run the full app test suite + typecheck**

Run: `cd app && npm test && npx tsc -b`
Expected: all PASS; `tsc` clean.

- [ ] **Step 9: Commit**

```bash
git add app/src/components/DomainPicker.tsx app/src/components/DomainPicker.test.tsx app/src/App.tsx app/src/components/Sidebar.tsx app/src/assessment/types.ts app/src/assessment/record.ts app/src/assessment/evidence.ts app/src/assessment/store.tsx app/src/assessment/rubric.ts
git commit -m "feat(app): domain dropdown + domain-tagged export; drop rubric shims

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Offline build gate + verification + roadmap

**Files:**
- Modify: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`

- [ ] **Step 1: Offline single-file build still works with both rubrics bundled**

Run: `cd app && npm run build:check`
Expected: `tsc -b` + `vite build` succeed and `check-offline.mjs` reports the single-file bundle has no external references. (If `check:offline` flags the two JSONs, they are bundled/inlined — investigate only if it fails.)

- [ ] **Step 2: Full regression — app + Python**

Run: `cd app && npm test` then `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest -q`
Expected: both suites green.

- [ ] **Step 3: Manual smoke (developer)**

Run: `cd app && npm run dev`, open the URL, switch the dropdown Secrets⇄PAM, score a use case and attach a file in each, Export then Import the file, and confirm the other domain's data is untouched. (Document result in the commit message.)

- [ ] **Step 4: Mark Phase 2.7 #2 done in the roadmap**

In `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`, under "Phase 2.7", change task **#2** to a ✅ with a one-line note: the React app now loads/isolates both domains via a header dropdown (per-domain localStorage + IndexedDB; legacy data migrated to the secrets namespace).

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/MULTI-DOMAIN-ROADMAP.md
git commit -m "docs(roadmap): Phase 2.7 #2 done — React app is domain-aware

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Notes for the executor
- Run app commands from `app/` (its own `package.json`); run Python/pytest from the repo root.
- Keep each task's commit green: `npx tsc -b` + the task's tests before committing.
- Do **not** surface PAM's regulatory evidence packs in the UI — explicitly out of scope here.
- If `check:offline` fails because the bundled rubric JSON pushed the single file past a size assertion (not an external-reference failure), that's a real finding — stop and flag it rather than loosening the check.

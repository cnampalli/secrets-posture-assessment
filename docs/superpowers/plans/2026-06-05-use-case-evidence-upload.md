# Use-case Evidence Upload Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a facilitator attach reference/audit documents (PDF, images, Office docs ≤10 MB) to each use case in the questionnaire React app, persisted in IndexedDB, embedded into the single `assessment-record.json` on export and restored on import.

**Architecture:** File bytes live in IndexedDB (`posture-evidence` DB); the in-memory record + `localStorage` hold only lightweight `EvidenceMeta`. The record schema gains an optional top-level `evidence` map keyed by `uc_id` (additive to `posture-assessment-record/v1` — `responses` untouched, so the Python report builders and the cross-language test are unaffected). Base64 is materialized from IndexedDB only at export and stripped back to bytes-in-IDB on import. App-only feature; no Python changes.

**Tech Stack:** React + TS, Vite single-file bundle, Vitest + jsdom; new dev-dep `fake-indexeddb` for tests. Raw IndexedDB API (no runtime dep). Spec: `docs/superpowers/specs/2026-06-04-use-case-evidence-upload-design.md`.

**Branch:** `feat/uc-evidence-upload` (already checked out; the spec is already committed on it).

---

## File Structure

```
app/src/assessment/
  types.ts          # +EvidenceMeta, +EvidenceExport, +MAX_BYTES, +ALLOWED_TYPES, extend AssessmentRecord
  evidence.ts       # NEW — IDB wrapper, base64, validateFile, humanSize, genId, buildExportRecord, restoreEvidence
  evidence.test.ts  # NEW
  record.ts         # buildRecord gains optional evidence-metadata param (additive)
  record.test.ts    # +case: evidence metadata included
  persistence.ts    # saveResponses gains optional evidence; +loadEvidence
  persistence.test.ts # +case: evidence round-trips through localStorage
  store.tsx         # +evidence state, +addEvidence/removeEvidence/evidenceFor, async exportRecord/importText
  store.test.tsx    # +evidence add/remove/round-trip cases
app/src/components/
  EvidencePanel.tsx      # NEW — dropzone + chips + remove, bound to current UC
  EvidencePanel.test.tsx # NEW
  UseCaseView.tsx        # render <EvidencePanel/> below ScorePanel
App.tsx                  # await the now-async exportRecord; toast skipped count
app/src/test-setup.ts    # + import 'fake-indexeddb/auto'
```

**Module dependency direction:** `evidence.ts` may import `record.ts` (for `buildRecord`) — never the reverse. `record.ts` stays pure (no IDB). `buildExportRecord`/`restoreEvidence` live in `evidence.ts` because they are IDB-coupled (this refines the spec's table, which tentatively placed them in `record.ts`).

---

## Task 1: Types, constants, and the evidence IndexedDB module

**Files:**
- Modify: `app/src/assessment/types.ts`
- Create: `app/src/assessment/evidence.ts`
- Create: `app/src/assessment/evidence.test.ts`
- Modify: `app/src/test-setup.ts`
- Modify: `app/package.json` (dev-dep)

- [ ] **Step 1: Install the test-only IndexedDB shim**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/app
npm install -D fake-indexeddb
```
Expected: `fake-indexeddb` added under `devDependencies`.

- [ ] **Step 2: Register the shim for tests**

Prepend to `app/src/test-setup.ts` (line 1, above the existing `@testing-library/jest-dom` import):
```ts
import 'fake-indexeddb/auto';
```
(Leave the rest of the file unchanged.)

- [ ] **Step 3: Add types + constants**

Append to `app/src/assessment/types.ts`:
```ts
export interface EvidenceMeta { id: string; name: string; type: string; size: number; added: string; }
export type EvidenceExport = EvidenceMeta & { data: string }; // base64 (no data: URI prefix)

export const MAX_BYTES = 10 * 1024 * 1024; // 10 MB
export const ALLOWED_TYPES = {
  mime: [
    'application/pdf',
    'image/png', 'image/jpeg', 'image/webp',
    'text/plain', 'text/csv',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  ] as string[],
  ext: ['pdf','png','jpg','jpeg','webp','txt','csv','docx','xlsx','pptx'] as string[],
};
```
Then extend the existing `AssessmentRecord` interface by adding this line after its `responses: …` property:
```ts
  evidence?: Record<string, EvidenceMeta[]>;
```

- [ ] **Step 4: Write the failing evidence tests**

Create `app/src/assessment/evidence.test.ts`:
```ts
import { describe, test, expect, beforeEach } from 'vitest';
import { indexedDB } from 'fake-indexeddb';
import {
  putFile, getBlob, deleteFile, blobToBase64, base64ToBlob,
  validateFile, humanSize, genId,
} from './evidence';

function fileOf(name: string, type: string, bytes = 10): File {
  return new File([new Uint8Array(bytes).fill(65)], name, { type });
}

beforeEach(async () => {
  // wipe the fake IDB between tests
  await new Promise<void>(res => { const r = indexedDB.deleteDatabase('posture-evidence'); r.onsuccess = r.onerror = () => res(); });
});

test('putFile/getBlob/deleteFile round-trip', async () => {
  const blob = new Blob([new Uint8Array([1, 2, 3, 4])], { type: 'application/pdf' });
  await putFile('id1', blob);
  const got = await getBlob('id1');
  expect(got).not.toBeNull();
  expect(new Uint8Array(await got!.arrayBuffer())).toEqual(new Uint8Array([1, 2, 3, 4]));
  await deleteFile('id1');
  expect(await getBlob('id1')).toBeNull();
});

test('blobToBase64 / base64ToBlob preserve bytes', async () => {
  const bytes = new Uint8Array([0, 1, 250, 99, 7, 255]);
  const b64 = await blobToBase64(new Blob([bytes]));
  const round = new Uint8Array(await base64ToBlob(b64, 'application/octet-stream').arrayBuffer());
  expect(round).toEqual(bytes);
});

test('validateFile accepts allowed types and rejects oversize + unsupported', () => {
  expect(validateFile(fileOf('a.pdf', 'application/pdf')).ok).toBe(true);
  expect(validateFile(fileOf('a.docx', '')).ok).toBe(true);        // ext fallback when MIME empty
  const big = new File([new Uint8Array(2)], 'big.pdf', { type: 'application/pdf' });
  Object.defineProperty(big, 'size', { value: 10 * 1024 * 1024 + 1 });
  const r1 = validateFile(big); expect(r1.ok).toBe(false); if (!r1.ok) expect(r1.reason).toMatch(/10 MB/);
  const r2 = validateFile(fileOf('evil.zip', 'application/zip')); expect(r2.ok).toBe(false);
});

test('humanSize formats bytes/KB/MB', () => {
  expect(humanSize(512)).toBe('512 B');
  expect(humanSize(2048)).toBe('2 KB');
  expect(humanSize(1572864)).toBe('1.5 MB');
});

test('genId returns a unique non-empty string', () => {
  const a = genId(), b = genId();
  expect(a).toBeTruthy(); expect(typeof a).toBe('string'); expect(a).not.toBe(b);
});
```

- [ ] **Step 5: Run — verify it fails**

Run: `cd app && npx vitest run src/assessment/evidence.test.ts`
Expected: FAIL — `Cannot find module './evidence'`.

- [ ] **Step 6: Implement `evidence.ts`**

Create `app/src/assessment/evidence.ts`:
```ts
import { MAX_BYTES, ALLOWED_TYPES } from './types';

const DB_NAME = 'posture-evidence';
const STORE = 'files';

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE, { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function putFile(id: string, blob: Blob): Promise<void> {
  const db = await openDb();
  try {
    await new Promise<void>((res, rej) => {
      const t = db.transaction(STORE, 'readwrite');
      t.objectStore(STORE).put({ id, blob });
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
      t.onabort = () => rej(t.error);
    });
  } finally { db.close(); }
}

export async function getBlob(id: string): Promise<Blob | null> {
  const db = await openDb();
  try {
    return await new Promise<Blob | null>((res, rej) => {
      const r = db.transaction(STORE, 'readonly').objectStore(STORE).get(id);
      r.onsuccess = () => res(r.result ? (r.result.blob as Blob) : null);
      r.onerror = () => rej(r.error);
    });
  } finally { db.close(); }
}

export async function deleteFile(id: string): Promise<void> {
  const db = await openDb();
  try {
    await new Promise<void>((res, rej) => {
      const t = db.transaction(STORE, 'readwrite');
      t.objectStore(STORE).delete(id);
      t.oncomplete = () => res();
      t.onerror = () => rej(t.error);
    });
  } finally { db.close(); }
}

export function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onerror = () => reject(fr.error);
    fr.onload = () => {
      const res = String(fr.result);
      const comma = res.indexOf(',');
      resolve(comma >= 0 ? res.slice(comma + 1) : res);
    };
    fr.readAsDataURL(blob);
  });
}

export function base64ToBlob(b64: string, type: string): Blob {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return new Blob([bytes], { type });
}

export type Validation = { ok: true } | { ok: false; reason: string };
export function validateFile(file: File): Validation {
  if (file.size > MAX_BYTES) return { ok: false, reason: 'over 10 MB' };
  const ext = (file.name.split('.').pop() || '').toLowerCase();
  const ok = ALLOWED_TYPES.mime.includes(file.type) || ALLOWED_TYPES.ext.includes(ext);
  return ok ? { ok: true } : { ok: false, reason: 'unsupported type' };
}

export function humanSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// file://-safe id: prefer crypto.randomUUID, fall back to getRandomValues, then Math.random.
export function genId(): string {
  const c = (globalThis as { crypto?: Crypto }).crypto;
  if (c?.randomUUID) return c.randomUUID();
  if (c?.getRandomValues) {
    const b = c.getRandomValues(new Uint8Array(16));
    return Array.from(b, x => x.toString(16).padStart(2, '0')).join('');
  }
  return `${Date.now().toString(16)}-${Math.random().toString(16).slice(2)}`;
}
```

- [ ] **Step 7: Run — verify it passes**

Run: `cd app && npx vitest run src/assessment/evidence.test.ts`
Expected: PASS (5 tests).

- [ ] **Step 8: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add app/src/assessment/types.ts app/src/assessment/evidence.ts app/src/assessment/evidence.test.ts app/src/test-setup.ts app/package.json app/package-lock.json
git commit -m "feat(evidence): types + IndexedDB module (put/get/delete, base64, validate)"
```

---

## Task 2: Export-embedding + import-restore (in evidence.ts) and record metadata

**Files:**
- Modify: `app/src/assessment/record.ts` (optional evidence-metadata param on `buildRecord`)
- Modify: `app/src/assessment/evidence.ts` (`buildExportRecord`, `restoreEvidence`)
- Modify: `app/src/assessment/record.test.ts`
- Modify: `app/src/assessment/evidence.test.ts`

- [ ] **Step 1: Add the failing record-metadata test**

Append to `app/src/assessment/record.test.ts`:
```ts
import { EvidenceMeta } from './types';

test('buildRecord includes evidence metadata only when provided and non-empty', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [RUBRIC[0].uc_id]: [{ id: 'x', name: 'a.pdf', type: 'application/pdf', size: 5, added: '2026-06-05T00:00:00Z' }],
  };
  const withEv = buildRecord(RUBRIC, {}, 'T', ev);
  expect(withEv.evidence).toEqual(ev);
  // omitted / empty → no evidence key at all (byte-stable with existing behavior)
  expect('evidence' in buildRecord(RUBRIC, {}, 'T')).toBe(false);
  expect('evidence' in buildRecord(RUBRIC, {}, 'T', {})).toBe(false);
});
```
> `RUBRIC` and `buildRecord` are already imported in `record.test.ts`; if `RUBRIC` is not, add `import { RUBRIC } from './rubric';`.

- [ ] **Step 2: Run — verify it fails**

Run: `cd app && npx vitest run src/assessment/record.test.ts`
Expected: FAIL — `buildRecord` takes 3 args / `evidence` undefined.

- [ ] **Step 3: Extend `buildRecord`**

In `app/src/assessment/record.ts`, change the import line to include the new type:
```ts
import type { UseCase, Response, State, AssessmentRecord, EvidenceMeta } from './types';
```
Replace the `buildRecord` signature + body to accept optional evidence (additive — output is byte-identical when omitted/empty):
```ts
export function buildRecord(
  rubric: UseCase[], responses: Record<string, Response>, generated: string,
  evidence?: Record<string, EvidenceMeta[]>,
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
  if (evidence) {
    const ev: Record<string, EvidenceMeta[]> = {};
    for (const [id, list] of Object.entries(evidence)) if (list && list.length) ev[id] = list;
    if (Object.keys(ev).length) out.evidence = ev;
  }
  return out;
}
```

- [ ] **Step 4: Run — verify record test passes**

Run: `cd app && npx vitest run src/assessment/record.test.ts`
Expected: PASS.

- [ ] **Step 5: Add the failing export/restore tests**

Append to `app/src/assessment/evidence.test.ts`:
```ts
import { buildExportRecord, restoreEvidence } from './evidence';
import { RUBRIC } from './rubric';

test('buildExportRecord embeds base64 for stored blobs and reports skips', async () => {
  const uc = RUBRIC[0].uc_id;
  await putFile('e1', new Blob([new Uint8Array([9, 9, 9])], { type: 'application/pdf' }));
  const evidence = { [uc]: [
    { id: 'e1', name: 'a.pdf', type: 'application/pdf', size: 3, added: 'T' },
    { id: 'missing', name: 'gone.pdf', type: 'application/pdf', size: 3, added: 'T' },
  ]};
  const { record, skipped } = await buildExportRecord(RUBRIC, {}, evidence, 'T', getBlob);
  expect(skipped).toBe(1);
  expect(record.evidence![uc]).toHaveLength(1);
  expect(typeof (record.evidence![uc][0] as { data: string }).data).toBe('string');
});

test('restoreEvidence writes blobs to IDB, strips data, replaces per uc, returns skipped', async () => {
  const uc = RUBRIC[0].uc_id;
  const data = await blobToBase64(new Blob([new Uint8Array([1, 2])], { type: 'application/pdf' }));
  const parsed = { [uc]: [{ id: 'r1', name: 'a.pdf', type: 'application/pdf', size: 2, added: 'T', data }] };
  const { evidence, skipped } = await restoreEvidence({}, parsed, (id) => id === uc);
  expect(skipped).toBe(0);
  expect(evidence[uc]).toEqual([{ id: 'r1', name: 'a.pdf', type: 'application/pdf', size: 2, added: 'T' }]);
  expect(await getBlob('r1')).not.toBeNull();
  // unknown uc id is ignored
  const res2 = await restoreEvidence({}, { 'NOPE': parsed[uc] }, (id) => id === uc);
  expect(res2.evidence['NOPE']).toBeUndefined();
});
```

- [ ] **Step 6: Run — verify it fails**

Run: `cd app && npx vitest run src/assessment/evidence.test.ts`
Expected: FAIL — `buildExportRecord`/`restoreEvidence` not exported.

- [ ] **Step 7: Implement `buildExportRecord` + `restoreEvidence`**

Append to `app/src/assessment/evidence.ts`:
```ts
import type { UseCase, Response, AssessmentRecord, EvidenceMeta, EvidenceExport } from './types';
import { buildRecord } from './record';

// Export form: AssessmentRecord whose evidence carries base64 payloads.
export type ExportRecord = Omit<AssessmentRecord, 'evidence'> & { evidence?: Record<string, EvidenceExport[]> };

export async function buildExportRecord(
  rubric: UseCase[], responses: Record<string, Response>,
  evidence: Record<string, EvidenceMeta[]>, generated: string,
  load: (id: string) => Promise<Blob | null> = getBlob,
): Promise<{ record: ExportRecord; skipped: number }> {
  const record = buildRecord(rubric, responses, generated) as ExportRecord;
  let skipped = 0;
  const ev: Record<string, EvidenceExport[]> = {};
  for (const [uc, list] of Object.entries(evidence)) {
    const out: EvidenceExport[] = [];
    for (const m of list) {
      const blob = await load(m.id);
      if (!blob) { skipped++; continue; }
      out.push({ ...m, data: await blobToBase64(blob) });
    }
    if (out.length) ev[uc] = out;
  }
  if (Object.keys(ev).length) record.evidence = ev;
  return { record, skipped };
}

export async function restoreEvidence(
  current: Record<string, EvidenceMeta[]>,
  parsed: unknown,
  knownId: (id: string) => boolean,
): Promise<{ evidence: Record<string, EvidenceMeta[]>; skipped: number }> {
  const merged: Record<string, EvidenceMeta[]> = { ...current };
  let skipped = 0;
  const src = (parsed && typeof parsed === 'object') ? parsed as Record<string, unknown> : {};
  for (const [uc, list] of Object.entries(src)) {
    if (!knownId(uc) || !Array.isArray(list)) continue;
    for (const old of current[uc] ?? []) await deleteFile(old.id).catch(() => {}); // drop replaced blobs
    const metas: EvidenceMeta[] = [];
    for (const e of list as EvidenceExport[]) {
      if (!e || typeof e.data !== 'string' || typeof e.id !== 'string') { skipped++; continue; }
      try {
        await putFile(e.id, base64ToBlob(e.data, e.type || 'application/octet-stream'));
        metas.push({ id: e.id, name: String(e.name ?? e.id), type: String(e.type ?? ''), size: Number(e.size ?? 0), added: String(e.added ?? '') });
      } catch { skipped++; }
    }
    merged[uc] = metas;
  }
  return { evidence: merged, skipped };
}
```

- [ ] **Step 8: Run — verify all evidence + record tests pass**

Run: `cd app && npx vitest run src/assessment/evidence.test.ts src/assessment/record.test.ts`
Expected: PASS (evidence 7 + record cases).

- [ ] **Step 9: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add app/src/assessment/record.ts app/src/assessment/record.test.ts app/src/assessment/evidence.ts app/src/assessment/evidence.test.ts
git commit -m "feat(evidence): export-embed base64 + import-restore; record metadata"
```

---

## Task 3: Persistence — save/load the evidence metadata map

**Files:**
- Modify: `app/src/assessment/persistence.ts`
- Modify: `app/src/assessment/persistence.test.ts`

- [ ] **Step 1: Add the failing persistence test**

Append to `app/src/assessment/persistence.test.ts`:
```ts
import { loadEvidence } from './persistence';
import type { EvidenceMeta } from './types';

test('saveResponses persists evidence metadata; loadEvidence reads it back', () => {
  const ev: Record<string, EvidenceMeta[]> = {
    [RUBRIC[0].uc_id]: [{ id: 'p1', name: 'a.pdf', type: 'application/pdf', size: 9, added: 'T' }],
  };
  saveResponses({}, 'T', ev);
  expect(loadEvidence()).toEqual(ev);
});

test('loadEvidence returns {} when nothing stored', () => {
  localStorage.clear();
  expect(loadEvidence()).toEqual({});
});
```
> If `RUBRIC`/`saveResponses` are not already imported in this file, add `import { saveResponses } from './persistence';` and `import { RUBRIC } from './rubric';`.

- [ ] **Step 2: Run — verify it fails**

Run: `cd app && npx vitest run src/assessment/persistence.test.ts`
Expected: FAIL — `loadEvidence` not exported / `saveResponses` ignores 3rd arg.

- [ ] **Step 3: Implement**

In `app/src/assessment/persistence.ts`:

(a) Add `EvidenceMeta` to the type import:
```ts
import type { Response, State, EvidenceMeta } from './types';
```
(b) Replace `saveResponses` to accept and store optional evidence:
```ts
export function saveResponses(
  responses: Record<string, Response>, generated: string,
  evidence?: Record<string, EvidenceMeta[]>,
): void {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(buildRecord(RUBRIC, responses, generated, evidence))); }
  catch { /* quota / unavailable — caller may toast */ }
}
```
(c) Add `loadEvidence` (reads the same record's `evidence` map):
```ts
export function loadEvidence(): Record<string, EvidenceMeta[]> {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (!raw) return {};
    const rec = JSON.parse(raw);
    const ev = rec && rec.evidence;
    if (!ev || typeof ev !== 'object') return {};
    const out: Record<string, EvidenceMeta[]> = {};
    for (const [id, list] of Object.entries(ev)) if (Array.isArray(list)) out[id] = list as EvidenceMeta[];
    return out;
  } catch { return {}; }
}
```

- [ ] **Step 4: Run — verify it passes (and existing persistence tests still pass)**

Run: `cd app && npx vitest run src/assessment/persistence.test.ts`
Expected: PASS (existing + 2 new).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add app/src/assessment/persistence.ts app/src/assessment/persistence.test.ts
git commit -m "feat(evidence): persist + load evidence metadata in the v1 record"
```

---

## Task 4: Store wiring — evidence state, actions, async export/import

**Files:**
- Modify: `app/src/assessment/store.tsx`
- Modify: `app/src/App.tsx`
- Modify: `app/src/assessment/store.test.tsx`

- [ ] **Step 1: Add the failing store tests**

Append to `app/src/assessment/store.test.tsx`. Match the file's existing render/act/hook helper style; the snippet below uses `@testing-library/react`'s `renderHook` + `act` — adapt the import to whatever the file already uses:
```tsx
import { renderHook, act } from '@testing-library/react';
import { AssessmentProvider, useAssessment } from './store';
import { RUBRIC } from './rubric';

function pdf(name = 'a.pdf') {
  return new File([new Uint8Array([1, 2, 3])], name, { type: 'application/pdf' });
}
const wrapper = ({ children }: { children: React.ReactNode }) => <AssessmentProvider>{children}</AssessmentProvider>;

test('addEvidence stores a file under the current uc; evidenceFor returns it; removeEvidence clears it', async () => {
  localStorage.clear();
  const { result } = renderHook(() => useAssessment(), { wrapper });
  const uc = result.current.current.uc_id;
  let res: { added: number; rejected: string[] };
  await act(async () => { res = await result.current.addEvidence([pdf()] as unknown as FileList); });
  expect(res!.added).toBe(1);
  expect(result.current.evidenceFor(uc)).toHaveLength(1);
  const id = result.current.evidenceFor(uc)[0].id;
  await act(async () => { await result.current.removeEvidence(id); });
  expect(result.current.evidenceFor(uc)).toHaveLength(0);
});

test('addEvidence rejects an oversize file with a reason', async () => {
  localStorage.clear();
  const big = new File([new Uint8Array(2)], 'big.pdf', { type: 'application/pdf' });
  Object.defineProperty(big, 'size', { value: 11 * 1024 * 1024 });
  const { result } = renderHook(() => useAssessment(), { wrapper });
  let res: { added: number; rejected: string[] };
  await act(async () => { res = await result.current.addEvidence([big] as unknown as FileList); });
  expect(res!.added).toBe(0);
  expect(res!.rejected[0]).toMatch(/10 MB/);
});

test('export then import round-trips evidence', async () => {
  localStorage.clear();
  const { result } = renderHook(() => useAssessment(), { wrapper });
  const uc = result.current.current.uc_id;
  await act(async () => { await result.current.addEvidence([pdf('round.pdf')] as unknown as FileList); });
  let text = '';
  await act(async () => { text = (await result.current.exportRecord()).text; });
  // fresh store imports the exported JSON
  const fresh = renderHook(() => useAssessment(), { wrapper });
  await act(async () => { await fresh.result.current.importText(text); });
  expect(fresh.result.current.evidenceFor(uc).map(m => m.name)).toEqual(['round.pdf']);
});
```

- [ ] **Step 2: Run — verify it fails**

Run: `cd app && npx vitest run src/assessment/store.test.tsx`
Expected: FAIL — `addEvidence`/`evidenceFor`/`removeEvidence` missing; `exportRecord` returns a string, not `{text}`.

- [ ] **Step 3: Update the store API type**

In `app/src/assessment/store.tsx`, update the `Api` interface: add the evidence members and change `exportRecord`/`importText` to async:
```ts
  evidenceFor: (uc_id: string) => EvidenceMeta[];
  addEvidence: (files: FileList | File[]) => Promise<{ added: number; rejected: string[] }>;
  removeEvidence: (id: string) => Promise<void>;
  exportRecord: () => Promise<{ text: string; skipped: number }>;
  importText: (text: string) => Promise<void>;
```
(Remove the old synchronous `exportRecord: () => string;` and `importText: (text: string) => void;` lines.)

- [ ] **Step 4: Wire the imports + state**

In `store.tsx`, extend imports:
```ts
import type { Answer, Response, State, UseCase, EvidenceMeta } from './types';
import { loadResponses, saveResponses, importRecord, loadEvidence } from './persistence';
import { putFile, deleteFile, getBlob, validateFile, genId, buildExportRecord, restoreEvidence } from './evidence';
```
Inside `AssessmentProvider`, after the existing `responses`/`currentId` state, add evidence state + a ref + a unified persist helper:
```ts
  const [evidence, setEvidence] = useState<Record<string, EvidenceMeta[]>>(() => loadEvidence());
  const evRef = useRef(evidence); evRef.current = evidence;

  function persistAll(nextResp: Record<string, Response>, nextEv: Record<string, EvidenceMeta[]>) {
    setResponses(nextResp); setEvidence(nextEv); saveResponses(nextResp, now(), nextEv);
  }
```
Then replace the existing `persist`/`mutate` to keep evidence intact:
```ts
  function persist(next: Record<string, Response>) { persistAll(next, evRef.current); }
  function mutate(id: string, fn: (r: Response) => Response) {
    const cur = ref.current[id] ?? blankResponse();
    persist({ ...ref.current, [id]: fn({ ...cur, answers: { ...cur.answers } }) });
  }
```

- [ ] **Step 5: Add the evidence actions + async export/import to the `api` object**

In the `useMemo` `api`, add these members (and add `evidence` to the `useMemo` dependency array — change `[responses, currentId]` to `[responses, currentId, evidence]`):
```ts
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
```
(Remove the previous synchronous `exportRecord`/`importText` entries.)

- [ ] **Step 6: Update `App.tsx` Header for async export**

In `app/src/App.tsx`, the `Header` already has `const toast = useToast();`. Replace `doExport` with an async version that awaits the record and toasts skipped files:
```tsx
  async function doExport() {
    const { text, skipped } = await a.exportRecord();
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a'); link.href = url; link.download = 'assessment-record.json'; link.click();
    URL.revokeObjectURL(url);
    if (skipped) toast(`${skipped} file(s) couldn't be exported`);
  }
```
And the import `onChange` handler already calls `a.importText(...)` inside `rd.onload`; make that callback async and await it:
```tsx
          rd.onload = async () => {
            try { await a.importText(String(rd.result)); toast('Record imported'); }
            catch { toast('Import failed — check the file'); }
          };
```

- [ ] **Step 7: Run — verify store tests pass**

Run: `cd app && npx vitest run src/assessment/store.test.tsx`
Expected: PASS (existing + 3 new).

- [ ] **Step 8: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add app/src/assessment/store.tsx app/src/App.tsx app/src/assessment/store.test.tsx
git commit -m "feat(evidence): store actions + async export/import wiring"
```

---

## Task 5: EvidencePanel component + UseCaseView integration

**Files:**
- Create: `app/src/components/EvidencePanel.tsx`
- Create: `app/src/components/EvidencePanel.test.tsx`
- Modify: `app/src/components/UseCaseView.tsx`

- [ ] **Step 1: Write the failing component test**

Create `app/src/components/EvidencePanel.test.tsx`:
```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AssessmentProvider } from '../assessment/store';
import { ToastProvider } from './Toast';
import { EvidencePanel } from './EvidencePanel';

function setup() {
  localStorage.clear();
  return render(
    <ToastProvider><AssessmentProvider><EvidencePanel /></AssessmentProvider></ToastProvider>
  );
}

test('shows the dropzone and empty state', () => {
  setup();
  expect(screen.getByText(/click to browse/i)).toBeInTheDocument();
});

test('attaching a file shows a chip with its name; remove clears it', async () => {
  setup();
  const input = screen.getByTestId('evidence-input') as HTMLInputElement;
  const file = new File([new Uint8Array([1, 2, 3])], 'policy.pdf', { type: 'application/pdf' });
  fireEvent.change(input, { target: { files: [file] } });
  await waitFor(() => expect(screen.getByText('policy.pdf')).toBeInTheDocument());
  fireEvent.click(screen.getByRole('button', { name: /remove policy.pdf/i }));
  await waitFor(() => expect(screen.queryByText('policy.pdf')).not.toBeInTheDocument());
});
```

- [ ] **Step 2: Run — verify it fails**

Run: `cd app && npx vitest run src/components/EvidencePanel.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `EvidencePanel.tsx`**

Create `app/src/components/EvidencePanel.tsx`:
```tsx
import { useRef, useState } from 'react';
import { useAssessment } from '../assessment/store';
import { useToast } from './Toast';
import { humanSize } from '../assessment/evidence';

export function EvidencePanel() {
  const a = useAssessment();
  const toast = useToast();
  const uc = a.current;
  const files = a.evidenceFor(uc.uc_id);
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  async function add(list: FileList | File[]) {
    const { rejected } = await a.addEvidence(list);
    if (rejected.length) toast(rejected[0]);
  }

  return (
    <section className="mt-6">
      <div className="flex items-center gap-2 mb-2">
        <span className="font-mono text-[10px] tracking-widest uppercase text-muted">Evidence</span>
        {files.length > 0 && <span className="font-mono text-[10px] text-faint">{files.length} file{files.length > 1 ? 's' : ''}</span>}
      </div>
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={e => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={e => { e.preventDefault(); setDrag(false); if (e.dataTransfer.files.length) void add(e.dataTransfer.files); }}
        className={`cursor-pointer rounded-md border border-dashed px-4 py-5 text-center text-sm transition-colors ${
          drag ? 'border-accent bg-accent-soft text-ink' : 'border-border-strong bg-bg2 text-muted hover:border-accent'}`}
      >
        <div className="font-medium">⬆ Drag files here or click to browse</div>
        <div className="text-xs text-faint mt-1">PDF · images · Office docs — max 10 MB each</div>
      </div>
      <input
        ref={inputRef} data-testid="evidence-input" type="file" multiple className="hidden"
        accept=".pdf,.png,.jpg,.jpeg,.webp,.txt,.csv,.docx,.xlsx,.pptx"
        onChange={e => { const fl = e.target.files; if (fl && fl.length) void add(fl); e.currentTarget.value = ''; }}
      />
      {files.length > 0 && (
        <ul className="flex flex-wrap gap-2 mt-3">
          {files.map(f => (
            <li key={f.id} className="inline-flex items-center gap-2 bg-card border border-border rounded-pill pl-3 pr-2 py-1 text-[12.5px]">
              <span className="truncate max-w-[200px]">{f.name}</span>
              <span className="font-mono text-[10.5px] text-faint">{humanSize(f.size)}</span>
              <button type="button" aria-label={`Remove ${f.name}`} onClick={() => void a.removeEvidence(f.id)}
                className="text-muted hover:text-gap leading-none px-1">✕</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
```

- [ ] **Step 4: Render it in `UseCaseView`**

In `app/src/components/UseCaseView.tsx`, add the import:
```tsx
import { EvidencePanel } from './EvidencePanel';
```
And render it right after `<ScorePanel />` (before the Previous/Save&next `<div className="flex justify-between mt-6">`):
```tsx
      <ScorePanel />

      <EvidencePanel />

      <div className="flex justify-between mt-6">
```

- [ ] **Step 5: Run — verify component tests pass**

Run: `cd app && npx vitest run src/components/EvidencePanel.test.tsx`
Expected: PASS (3 tests).

- [ ] **Step 6: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add app/src/components/EvidencePanel.tsx app/src/components/EvidencePanel.test.tsx app/src/components/UseCaseView.tsx
git commit -m "feat(evidence): EvidencePanel dropzone + chips in UseCaseView"
```

---

## Task 6: Full verification + offline build + Python regression

**Files:** none (verification only)

- [ ] **Step 1: Full app test suite**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/app && npm test`
Expected: all PASS — the prior 28 plus the new evidence/record/persistence/store/component tests. If any pre-existing test broke, fix it (the signature changes were designed to be backward-compatible; investigate the specific failure).

- [ ] **Step 2: Offline single-file build guard**

Run: `cd app && npm run build:check`
Expected: `OK — single self-contained offline index.html`. (Confirms `fake-indexeddb` did not leak into the bundle and no external URL was introduced.)

- [ ] **Step 3: Python regression (additive schema is ignored downstream)**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest -q`
Expected: still 117 passed — confirms the additive top-level `evidence` key didn't disturb the report builders or the cross-language export-schema test.

- [ ] **Step 4: Manual QA under `file://`**

Run: `cd app && npm run build && open dist/index.html`
Then verify by hand:
1. Open a use case → drag/drop or click-browse a PDF and a PNG → both appear as chips with sizes.
2. Attach a `.zip` → rejected with a toast; attach a >10 MB file → rejected with a "10 MB" toast.
3. Remove a chip → it disappears.
4. **Reload the page** → attachments persist (IndexedDB + localStorage).
5. **Export record** → open the JSON, confirm a top-level `"evidence"` map with base64 `data`.
6. Clear site data (or use a fresh browser profile) → **Import** that JSON → attachments reappear on their use cases.

- [ ] **Step 5: Commit any rebuild artifact (if dist is tracked — it is gitignored, so likely nothing)**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git status --short app/
```
Expected: clean (the build output `app/dist/` is gitignored). No commit needed.

---

## Self-Review (completed by author)

- **Spec coverage:** purpose/audit-only + no Python changes (Task 6 Step 3 confirms); per-UC scope (EvidencePanel bound to `a.current`, Task 5); file policy PDF/images/Office ≤10 MB (`ALLOWED_TYPES`/`MAX_BYTES` + `validateFile`, Task 1); one self-contained export with base64 (`buildExportRecord`, Task 2) + restore on import (`restoreEvidence`, Task 2/4); additive `evidence` map on v1 (`buildRecord` optional param, Task 2; `localStorage` round-trip Task 3); IndexedDB for bytes / metadata in record (Tasks 1–3); UI dropzone+chips+remove (Task 5); error handling — reject toast, skip missing on export, skip dataless on import, best-effort remove (Tasks 2/4/5); orphan cleanup on replace (`restoreEvidence` deletes replaced ids, Task 2) and on remove (`removeEvidence`, Task 4); tests incl. export→import round-trip + regression (Tasks 1–6). Offline guard (Task 6 Step 2). All spec sections map to a task.
- **Placeholder scan:** none — every code/test/command step is complete and runnable.
- **Type consistency:** `EvidenceMeta`/`EvidenceExport`/`ExportRecord` defined in Task 1/2 and used consistently; `buildRecord(rubric, responses, generated, evidence?)`, `buildExportRecord(rubric, responses, evidence, generated, load)` returning `{record, skipped}`, `restoreEvidence(current, parsed, knownId)` returning `{evidence, skipped}`, `saveResponses(responses, generated, evidence?)`, `loadEvidence()`, and the store's `addEvidence→{added,rejected}` / `exportRecord→{text,skipped}` / `evidenceFor` / `removeEvidence` signatures all match across tasks and their call sites (`App.tsx`, `EvidencePanel`). `evidence` added to the store `useMemo` deps so the API closes over fresh state.

---

## Execution Handoff

Spec: `docs/superpowers/specs/2026-06-04-use-case-evidence-upload-design.md`. After all tasks: whole-feature review (`superpowers:requesting-code-review`) then `superpowers:finishing-a-development-branch` to open a PR against `main`.

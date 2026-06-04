# Design — Use-case evidence upload (Phase 2, feature 1)

**Date:** 2026-06-04
**Status:** Approved design; ready for implementation planning
**Context:** First Phase-2 feature on top of the merged Brass Editorial UI rebuild (PR #11 → `main`).
The questionnaire React app (`app/`) is a single offline `file://` bundle; this feature adds the
ability to attach supporting documents ("evidence") to each use case.

---

## 1. Purpose & scope

Let a facilitator attach supporting documents to a use case as a **reference / audit trail** — so
that whoever opens the exported assessment can see what backs each score.

**Decisions locked during brainstorming:**
- **Consumption:** reference/audit only. Evidence does **NOT** appear in the generated matrix viewer
  or executive summary. **No Python / report-builder changes.** This is an app-only feature.
- **Attachment scope:** **per use case only** (all 47). No assessment-level/global evidence area.
- **File policy:** allow PDF, common images (png/jpg/jpeg/webp), and Office docs (docx/xlsx/pptx) plus
  txt/csv. **Max 10 MB per file.**
- **Export model:** **one self-contained file** — evidence base64 is embedded into the existing
  `assessment-record.json` on export and restored on import.
- **Schema:** **additive to `posture-assessment-record/v1`** (Approach A) — a new optional top-level
  `evidence` map keyed by `uc_id`, leaving `responses` (the contract Python reads) untouched. No
  version bump, no `localStorage`-key migration.

**Non-goals:** no evidence in reports; no global/assessment-level evidence; no server, OCR, preview/
viewer, thumbnails, versioning, or file editing; no type conversion. YAGNI.

---

## 2. Storage architecture

Forced by the 10 MB cap vs the ~5 MB `localStorage` quota: **file bytes never touch `localStorage`.**

- **IndexedDB** — DB `posture-evidence`, object store `files`, key = file `id`, value = `{ id, blob }`
  (stored as a `Blob`, not base64, to avoid in-DB bloat). Persists across sessions and works under
  `file://`.
- **`localStorage`** (key unchanged: `posture-assessment-record/v1`) — stores the full record
  including the evidence **metadata** map only (small). Never the bytes.
- **Export** — materializes base64 from IndexedDB into each metadata entry (`data` field) → one
  self-contained JSON.
- **Import** — decodes each `data` back to a `Blob` → IndexedDB; keeps metadata in the record;
  strips `data` from the in-memory/`localStorage` copy.

### Data model (`app/src/assessment/types.ts`, additive)
```ts
export interface EvidenceMeta {
  id: string;      // crypto.randomUUID()
  name: string;    // original filename
  type: string;    // MIME type
  size: number;    // bytes
  added: string;   // ISO timestamp
}

// In the EXPORTED record only, each entry is widened with the base64 payload:
export type EvidenceExport = EvidenceMeta & { data: string }; // base64 (no data: URI prefix)

export interface AssessmentRecord {
  schema: 'posture-assessment-record/v1';
  generated: string;
  responses: Record<string, { /* unchanged */ }>;
  evidence?: Record<string, EvidenceMeta[]>; // NEW — optional, keyed by uc_id
}

export const MAX_BYTES = 10 * 1024 * 1024; // 10 MB
// Accept by MIME where reliable; fall back to extension for Office types.
export const ALLOWED_TYPES = {
  mime: [
    'application/pdf',
    'image/png', 'image/jpeg', 'image/webp',
    'text/plain', 'text/csv',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  // docx
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',        // xlsx
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',// pptx
  ],
  ext: ['pdf','png','jpg','jpeg','webp','txt','csv','docx','xlsx','pptx'],
};
```
> Note: the in-memory `evidence` map and the `localStorage` copy hold `EvidenceMeta[]` (no `data`).
> Only the downloaded export file carries `EvidenceExport[]`.

---

## 3. Module boundaries

| File | Status | Responsibility |
|---|---|---|
| `assessment/evidence.ts` | **NEW** | IndexedDB wrapper (`openDb`, `putFile(id, blob)`, `getBlob(id)`, `deleteFile(id)`); `blobToBase64`/`base64ToBlob`; `validateFile(file)` (type allowlist + `MAX_BYTES`). Pure & independently testable. |
| `assessment/types.ts` | change | add `EvidenceMeta`/`EvidenceExport`, extend `AssessmentRecord`, export `MAX_BYTES` + `ALLOWED_TYPES`. |
| `assessment/record.ts` | change | `buildRecord` carries the evidence **metadata** map (sync, used by autosave); new async `buildExportRecord(rubric, responses, evidence, generated, getBlob)` embeds base64; new async `restoreEvidence(recordEvidence, putFile)` writes imported blobs to IDB and returns the metadata map (sans `data`). |
| `assessment/persistence.ts` | change | `loadResponses` returns `{ responses, evidence }`; `saveResponses` round-trips the evidence metadata map; `importRecord` becomes **async** and returns `{ responses, evidence }` after restoring blobs to IDB + merging metadata. |
| `assessment/store.tsx` | change | hold `evidence: Record<uc_id, EvidenceMeta[]>`; actions `addEvidence(files)`, `removeEvidence(id)`, `evidenceFor(uc_id)`; `exportRecord` becomes **async** (materialize base64); import restores evidence. |
| `components/EvidencePanel.tsx` | **NEW** | dropzone + file-chip list + remove, bound to the current UC via the store. |
| `components/UseCaseView.tsx` | change | render `<EvidencePanel/>` in the evidence row (below `ScorePanel`, above the Prev/Next bar). |
| `App.tsx` | change | `await` the now-async export in the Header handler. |

---

## 4. Data flow

1. **Add:** drop/pick files → `validateFile` each → `crypto.randomUUID()` id → `putFile(id, blob)` →
   append `EvidenceMeta` to `evidence[uc_id]` → persist (metadata → `localStorage`).
2. **Remove:** `deleteFile(id)` → drop metadata → persist.
3. **Export:** `buildExportRecord` reads each blob → base64 → attaches `data` → download single
   `assessment-record.json`. Missing blobs are skipped with a toast count.
4. **Import:** parse → merge `responses` (existing behavior) → for each evidence entry **with** `data`:
   decode → `putFile` → keep metadata; entries lacking `data` or with corrupt base64 are skipped.
   Strip `data` from the in-memory/`localStorage` copy. Evidence merges **per `uc_id`**: for each
   `uc_id` present in the imported record, its evidence list **replaces** that UC's current list
   (mirroring how `responses` merge per `uc_id`, and avoiding duplicate files); UCs absent from the
   import keep their existing evidence untouched.
5. **Reload:** `localStorage` metadata → `store.evidence`; bytes already persist in IDB by `id`.

---

## 5. UI / UX

`EvidencePanel` renders below `ScorePanel`, above the Prev/Next bar, using existing Brass primitives
and tokens (`Card`/`CardBody`, a mono uppercase eyebrow like `ScorePanel`, dashed
`border-border-strong` dropzone that highlights brass on drag-over, state-neutral chips).

```
EVIDENCE                                          2 files
┌──────────────────────────────────────────────────────┐
│   ⬆  Drag files here or click to browse                │
│      PDF · images · Office docs — max 10 MB each        │
└──────────────────────────────────────────────────────┘
┌ 📄 push-protection.pdf  1.2 MB ✕┐ ┌ 🖼 scan-config.png 340 KB ✕┐
```
- Click anywhere on the dropzone opens the native picker (`<input type="file" multiple accept=…>`),
  using `ALLOWED_TYPES.ext`/mime for the `accept` hint (validation is still enforced in code).
- Drag-over toggles a brass highlight class; drop reads `dataTransfer.files`.
- Chip = type icon + filename + human-readable size + `✕` remove. Empty state: dropzone only, count
  hidden.
- Accessibility: the dropzone is a labeled button/region; the file input is keyboard-reachable; remove
  buttons have `aria-label="Remove <filename>"`.

---

## 6. Error handling

| Situation | Behavior |
|---|---|
| File too big / disallowed type | Reject that file; toast `"<name> — over 10 MB"` / `"<name> — unsupported type"`. Other valid files in the same drop still attach. |
| IndexedDB unavailable / quota exceeded on store | Toast `"Couldn't store file (storage full or unavailable)"`; metadata **not** added (no dangling ref). |
| Export: a metadata entry's blob is missing in IDB | Skip it; toast `"N file(s) couldn't be exported"`. |
| Import: evidence entry lacking `data` / corrupt base64 | Skip that file, continue; toast skipped count if any. Schema mismatch keeps today's "Import failed" toast. |
| Remove fails in IDB | Best-effort: drop metadata anyway, persist. |

---

## 7. Testing

Vitest + a new dev-dependency **`fake-indexeddb`** (registered in `app/src/test-setup.ts` via
`import 'fake-indexeddb/auto'`). Dev-only — not bundled, so the offline single-file guarantee holds.

- **`evidence.ts`:** put/get/delete round-trip; `blob↔base64` byte-equality round-trip; `validateFile`
  accepts each allowed type and rejects oversize + disallowed type.
- **`record.ts`:** `buildRecord` carries evidence metadata while `responses` shape is unchanged;
  `buildExportRecord` embeds base64 for stored blobs; `restoreEvidence` writes blobs and returns
  metadata without `data`.
- **`store.tsx`:** add/remove updates state + persists; **export→import round-trip** yields identical
  files in IDB and the same metadata; import merges evidence without dropping responses.
- **Regression:** the existing 28 app tests stay green. The Python cross-language test
  (`tests/test_react_export_schema.py`) is untouched — the additive top-level `evidence` key is
  ignored by the Python builders. (Optional: a Python test asserting an evidence-bearing record still
  builds the exec summary.)
- **Manual QA:** built single file under `file://` — attach, remove, export, reload (persists via
  IDB + `localStorage`), and import into a fresh browser profile (bytes restored).

---

## 8. Verification

- `cd app && npm test` green (existing 28 + new evidence tests).
- `cd app && npm run build:check` → single self-contained offline `index.html` (no new external URLs).
- Manual `file://` round-trip per §7.
- `python3 -m pytest -q` still green (no Python changes; confirms additive schema didn't break the
  cross-language contract).

---

## 9. Risks & mitigations

- **Export bloat** — many 10 MB files → very large JSON. Accepted (user chose one self-contained
  file). Mitigation: base64 is materialized only at export (not held in memory/`localStorage`), and
  missing blobs are skipped rather than failing the whole export.
- **IndexedDB under `file://`** — supported in Chromium/Firefox/Safari; guarded with try/catch +
  toast so the questionnaire still works if IDB is blocked (evidence simply unavailable).
- **Metadata/bytes drift** — only add metadata after a successful `putFile`; on remove, drop metadata
  even if `deleteFile` fails (favor no dangling refs over orphaned bytes).
- **Async export regression** — `exportRecord` becomes async; the Header handler must `await` it and
  the existing export test updated accordingly.
- **Orphaned blobs** — re-importing a record replaces a UC's evidence list, which can leave its prior
  blobs unreferenced in IDB. Mitigation: on replace (import) and on `removeEvidence`, delete the
  now-unreferenced `id`s from IDB so storage doesn't grow silently.

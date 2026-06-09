# React App Domain-Awareness — Design Spec

_2026-06-09. Phase 2.7 task #2 (both-domain demo parity). Makes the interactive
React assessment app load and isolate **both** Secrets and PAM, replacing the single
hard-coded Secrets rubric._

## Problem

The React app (`app/`, "Posture Assessment / Questionnaire") loads one bundled rubric
(`app/src/data/rubric.json` via `app/src/assessment/rubric.ts`) that is **Secrets-only**
(47 UCs). There is no PAM rubric and no domain switcher, so the polished interactive
surface can demo only one of the two domains. The Python static questionnaires already
cover both; the React app must reach the same parity.

Storage is also domain-blind: responses live in `localStorage['posture-assessment-record/v1']`
and evidence blobs in IndexedDB `posture-evidence` / store `files`, both global. A second
domain would collide with the first.

## Goal

The app loads the correct rubric per domain (Secrets 47 / PAM 17), a header dropdown switches
domains at runtime, and each domain's responses + evidence are namespaced so they never
collide. PAM's per-question regulatory evidence packs are **out of scope** for this task
(tracked separately under Phase 2.7).

**Acceptance:** a reviewer picks "Secrets" or "PAM" in the live app and runs a full posture
assessment end-to-end in either — score a use case, attach evidence, export/import a record —
with no cross-domain contamination, and the offline single-file build still passes.

## Non-goals (YAGNI)

- Rendering PAM's regulatory evidence packs (the "what artifact proves this control" hints) in
  the React UI. Separate Phase 2.7 follow-up.
- Routing / deep-linking to a domain (`?domain=pam`). Context-driven switching is enough.
- More than the two domains that exist today; the registry is shaped to extend, not pre-wired
  for IGA.

## Approach (chosen: domain in the store/context)

The active rubric and storage namespace flow through React state (the existing
`AssessmentProvider`). Rejected alternatives: build-time per-domain artifacts (no in-app
switch, two builds) and URL-param routing (adds routing to a single-view app for little gain).

## Components

### 1. Multi-domain emit — `questionnaire/emit_rubric.py`
Generalize from a single hard-coded `load_rubric(METH)` → single `rubric.json`, to a loop over
a small domain list writing one JSON per domain:

| Domain id | Source | Output | UCs |
|---|---|---|---|
| `secrets` | `load_rubric(METH)` | `app/src/data/rubric.secrets.json` | 47 |
| `pam` | `load_rubric(METH, data_dir=matrix/domains/pam)` | `app/src/data/rubric.pam.json` | 17 |

The old `app/src/data/rubric.json` is **removed** (replaced by the two per-domain files). The
domain list lives in one place so adding IGA later is a one-line change. Emit stays
indent=2 JSON, `ensure_ascii=False`, source-of-truth = the Python rubric loader.

### 2. Domain registry — `app/src/assessment/domains.ts` (new)
```
import secrets from '../data/rubric.secrets.json';
import pam from '../data/rubric.pam.json';
export type DomainId = 'secrets' | 'pam';
export interface Domain { id: DomainId; label: string; rubric: UseCase[]; }
export const DOMAINS: Domain[] = [
  { id: 'secrets', label: 'Secrets Management',        rubric: secrets as UseCase[] },
  { id: 'pam',     label: 'Privileged Access (PAM)',   rubric: pam     as UseCase[] },
];
export const DEFAULT_DOMAIN: DomainId = 'secrets';
export function getDomain(id: DomainId): Domain;   // throws/falls back to default on unknown
```
Both JSONs are statically imported → bundled into the offline single-file build.

### 3. `rubric.ts` → domain-parameterized
Replace the module-level `RUBRIC` singleton + `INDEX` with a factory:
```
export interface RubricView { rubric: UseCase[]; byId(id): UseCase|undefined; byCategory(): ...; }
export function makeRubric(domainId: DomainId): RubricView;
```
All consumers of the old `RUBRIC`/`byId`/`byCategory` (App.tsx header counter, Sidebar,
persistence, record) receive the active rubric from the store instead of importing the
singleton.

### 4. Store carries the active domain — `app/src/assessment/store.tsx`
The `AssessmentProvider` gains:
- `domainId: DomainId` (initialised from `localStorage['posture-active-domain']` or default)
- the active `RubricView` (derived from `domainId`)
- `setDomain(id)`: persists the choice, swaps the rubric, and **reloads that domain's
  responses + evidence from its own namespace** (resets current UC, scored count, etc.)

Switching domains never mutates the other domain's stored state.

### 5. Storage namespacing — `app/src/assessment/persistence.ts` + `evidence.ts`
- localStorage responses key: `posture-assessment-record/v1/<domainId>`
  (was `posture-assessment-record/v1`).
- IndexedDB evidence file ids prefixed `<domainId>/…` so blobs for one domain are invisible to
  the other (same DB/store, namespaced keys).
- **Legacy migration (one-shot):** on first load, if the un-namespaced
  `posture-assessment-record/v1` key exists, copy it to the `secrets` namespace and mark
  migrated (so an in-progress Secrets assessment survives the upgrade). Evidence blobs written
  under the old un-prefixed ids are treated as `secrets` (prefix-on-read fallback) — no
  destructive rewrite required.

### 6. Domain dropdown — `app/src/components/DomainPicker.tsx` (new)
A header `<select>` (mirrors the placement of `ThemeToggle`) listing `DOMAINS` by label,
bound to `store.domainId` → `setDomain`. Sits next to the "Posture Assessment / Questionnaire"
title. Keyboard-accessible; labelled for screen readers.

### 7. Export / import — `record.ts`, App header
- The exported record gains a `domain: DomainId` field; the download filename becomes
  `assessment-<domain>.json`.
- Import continues to merge only known UC ids (`knownId` filter), so a Secrets record dropped
  into PAM contributes nothing. If the file's `domain` differs from the active domain, toast a
  warning and still import only matching ids (no silent cross-load).

## Data flow

```
emit_rubric.py ──► rubric.secrets.json ┐
               └─► rubric.pam.json ─────┤ (build-time, bundled)
                                        ▼
        domains.ts (registry) ──► makeRubric(domainId) ──► RubricView
                                        ▼
   DomainPicker ──setDomain──► AssessmentProvider(domainId, RubricView)
                                        ▼
        responses/evidence  ◄─► persistence(key = …/<domainId>)
                            ◄─► evidence(IndexedDB ids = <domainId>/…)
```

## Error handling

- Unknown/garbage `posture-active-domain` value → fall back to `DEFAULT_DOMAIN`.
- Unknown domain id passed to `getDomain`/`makeRubric` → fall back to default (never throw into
  render).
- localStorage quota / unavailable → existing silent-catch + toast path is preserved per domain.
- Import of a record whose `domain` ≠ active → warn, import only known ids.

## Testing

Vitest (mirrors existing `app/src/assessment/*.test.ts`):
- **domains**: `DOMAINS` has secrets+pam; rubric lengths 47 and 17; `getDomain('pam').rubric`
  contains `UC-P-017`; unknown id falls back to default.
- **rubric factory**: `makeRubric('pam').byId('UC-P-007')` resolves; `byCategory` groups.
- **persistence isolation**: save under `pam`, load under `secrets` → empty; the two keys are
  distinct; round-trip within a domain is lossless.
- **legacy migration**: seed the old un-namespaced key → first load surfaces it under `secrets`
  and the namespaced key now holds it.
- **evidence isolation**: a blob put for `pam/UC-P-001/q` is not returned for the `secrets`
  namespace.
- **store**: `setDomain('pam')` swaps the rubric (scored/total reflect 17) and does not mutate
  the secrets-namespace store.
- **build**: `npm run build:check` (tsc + vite + `check:offline`) passes with both rubrics
  bundled.

Python side: extend `tests/test_build_questionnaire.py` (or a small `tests/test_emit_rubric.py`)
to assert `emit_rubric` writes both per-domain files with the expected UC counts.

## Rollout / verification

1. `python3 questionnaire/emit_rubric.py` → both JSONs written (47 / 17).
2. `cd app && npm test` green; `npm run build:check` green (offline single file intact).
3. Manual: `npm run dev`, switch Secrets⇄PAM in the dropdown, score + attach evidence in each,
   export/import, confirm no cross-contamination.

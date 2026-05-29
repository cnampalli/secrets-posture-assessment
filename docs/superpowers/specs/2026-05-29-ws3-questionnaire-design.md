# WS-3 — Interactive Assessment Instrument (slice 1) — Design Spec

**Date:** 2026-05-29
**Branch:** `ws3-questionnaire` (off `main`; WS-1 + WS-2 merged)
**Status:** Approved design — awaiting spec review before planning
**Source:** `meta/IMPROVEMENT-BACKLOG.md` WS-3; brainstorming + sketch session 2026-05-29
**Sketch:** `.planning/sketches/004-ws3-questionnaire/` (Variant A chosen)

---

## 1. Purpose

The **front door** of the posture-assessment instrument: a self-contained HTML questionnaire
that a consultant drives live with a client. It renders each use case's rubric questions,
auto-derives a proposed posture state from the answers (the WS-1 laddering rule), lets the
assessor override with rationale + confidence, and exports a rich, re-importable assessment
record. It operationalises the WS-1 rubric — turning the archetype library into a working
scoring instrument.

## 2. Non-goals (explicit scope boundary)

This is **slice 1**. Deferred to later slices:

- **Report adapter** — projecting the assessment record into the `current-state.csv` the report
  (`matrix/build_matrix_viewer.py`) consumes. The answer→report loop is NOT closed this slice;
  the deliverable is the instrument + a canonical record. (Accepted trade-off.)
- **Framework-selection UI** — choosing frameworks / writing the WS-2 `engagement.yaml` stays a
  separate concern (WS-2 config).
- **Variant B worksheet view** — the dense all-UCs view; architecture keeps engine + rubric data
  reusable so it layers on later.
- **Numeric quantitative inputs** — coverage questions stay binary with the threshold in the prompt.
- **Self-serve guidance copy** — facilitated-primary only for now.

## 3. Decisions locked (brainstorming 2026-05-29)

| # | Decision | Outcome |
|---|----------|---------|
| 1 | Flow | **Variant A focused wizard**, architected so Variant B worksheet reuses the same engine. |
| 2 | Export | **Rich record only** (`assessment-record.json`); report adapter deferred. |
| 3 | Quantitative criteria | **Yes/No with threshold shown** in the prompt text. |
| 4 | A0 bespoke UCs | **Manual state** — sub-criteria shown as a guidance checklist; assessor sets state. |
| 5 | Persistence | **Autosave (localStorage) + import** the rich record to resume / re-assess. |

## 4. Architecture

A **Python build step bakes the WS-1 rubric into a self-contained HTML questionnaire**, mirroring
the established `matrix/build_matrix_viewer.py` pattern (read CSVs → resolve → JSON →
`/*__TOKEN__*/` injection into a raw template → write one offline HTML file; no server, no
external requests).

The **scoring engine is authored once in Python** (`methodology/scoring.py`) as the reusable,
unit-tested reference, and **mirrored in `questionnaire/scoring.js`** which the build *inlines*
into the HTML. This keeps the engine independently testable while the shipped file stays
self-contained. Both implementations are pinned to a shared canonical vector fixture so they
cannot drift.

Presentation (the wizard, `app.js`) is kept separate from the engine and the rubric data, so the
deferred Variant B worksheet view can reuse both without re-architecting.

```
WS-1 rubric CSVs ──> rubric_loader.py ──┐
(archetypes,                            │ resolved UC JSON (params filled)
 questions, uc-map,                     ▼
 bespoke)                    build_questionnaire.py ──> questionnaire.html (self-contained)
                                        ▲                    │ inlines scoring.js + app.js
methodology/scoring.py  <—same ladder—> questionnaire/scoring.js
        │ (Python reference, tested)         │ (browser mirror)
        └────── scoring-vectors.json ────────┘ (drift guard, both test against it)
```

## 5. Components

| File | Status | Responsibility |
|---|---|---|
| `methodology/scoring.py` | Create | **Reference engine.** `derive_state(questions, answers) -> str`. Pure, no I/O. Reusable by the future report adapter. |
| `questionnaire/rubric_loader.py` | Create | Reads the 4 rubric CSVs; resolves each of the 47 UCs into a renderable question set with `{slot}` params filled from `uc-archetype-map.csv`; A0 → bespoke sub-criteria list. Errors on an unfilled slot. |
| `questionnaire/scoring.js` | Create | JS mirror of `derive_state` for live UX. |
| `questionnaire/app.js` | Create | Variant-A wizard UI: rail, UC view, live scoring card, override drawer, autosave, import, export. |
| `questionnaire/template.html` | Create | Raw HTML+CSS shell with `/*__RUBRIC__*/`, `/*__SCORING__*/`, `/*__APP__*/` injection tokens. |
| `questionnaire/build_questionnaire.py` | Create | Orchestrates loader → JSON; inlines `scoring.js` + `app.js` + rubric JSON into `template.html`; writes `questionnaire/questionnaire.html`. |
| `questionnaire/scoring-vectors.json` | Create | Canonical `(questions, answers) -> expected state` vectors. |
| `tests/test_scoring.py` | Create | pytest: ladder cases + reads `scoring-vectors.json`. |
| `tests/test_rubric_loader.py` | Create | All 47 UCs resolve; param-fill correctness; A0 detection; no leftover `{slots}`. |
| `tests/test_build_questionnaire.py` | Create | Build produces a self-contained HTML (no `http`/`src=`/`href=` external refs), embeds all 47 UCs, inlines scoring.js + app.js. |
| `questionnaire/scoring.test.mjs` | Create | Node conformance: JS engine matches `scoring-vectors.json`. Run from a pytest test via subprocess; skipped if node absent. |
| `docs/adr/ADR-010-questionnaire-instrument.md` | Create | Records the dual-engine (Python reference + inlined JS mirror) + rich-record decisions. |
| `meta/IMPROVEMENT-BACKLOG.md` | Modify | Mark WS-3 slice 1 done; note deferred items. |

## 6. Rubric resolution (`rubric_loader.py`)

Inputs (all in `methodology/`): `assessment-archetypes.csv`, `archetype-questions.csv`,
`uc-archetype-map.csv`, `bespoke-criteria.csv`. The questionnaire depends only on `methodology/`
— UC **title** comes from the `notes` field of `uc-archetype-map.csv`, and **category** is
derived from the uc_id prefix (`UC-F-*` → Functional, `UC-N-*` → Non-functional). No dependency
on `matrix/use-cases.csv`.

For each UC in `uc-archetype-map.csv`:
- Parse `params` (`k=v;k=v`) into a dict.
- If archetype ≠ A0: take that archetype's questions from `archetype-questions.csv`, fill every
  `{slot}` in `question_template` from the params dict. A slot with no matching param is a hard
  error (surfaces a rubric data gap). Emit `{qid, dimension, informs_state, text}`.
- If archetype = A0: emit the UC's rows from `bespoke-criteria.csv` as
  `{sub_id, sub_criterion, question, evidence}` (guidance checklist; no `informs_state`).

Output (per UC): `{uc_id, title, category, archetype, archetype_name, kind: "ladder"|"bespoke",
questions:[...] | sub_criteria:[...]}`.

## 7. Scoring engine (`scoring.py` / `scoring.js`)

`derive_state(questions, answers)` — `questions` is the ladder list (each with `informs_state` ∈
{`GAP_PARTIAL`, `PARTIAL_MET`}); `answers` maps `qid -> "yes"|"no"|"na"|null`:

1. If every question is `na` (and there is ≥1) → **NA**.
2. Else if any non-NA question is unanswered (`null`) → **PENDING** (insufficient evidence).
3. Else if any `GAP_PARTIAL` question is `no` → **GAP**.
4. Else if any `PARTIAL_MET` question is `no` → **PARTIAL**.
5. Else → **MET**.

A0 (bespoke) UCs do not call the ladder — the UI shows the guidance checklist and the assessor
selects the state directly. An assessor override (any UC) supersedes the derived state and
requires a rationale.

The Python reference and JS mirror are both asserted against `scoring-vectors.json`, which
enumerates at least one case per outcome (GAP / PARTIAL / MET / PENDING / NA) plus edge cases
(mixed NA + answered, all-NA, single-question sets).

## 8. Data model — `assessment-record.json`

Export and import share this format (the single source of truth):

```json
{
  "schema": "posture-assessment-record/v1",
  "generated": "<iso8601>",
  "responses": {
    "UC-F-001": {
      "archetype": "A1",
      "answers": {"A1-Q1": "no", "A1-Q2": null, "A1-Q3": null},
      "proposed_state": "GAP",
      "final_state": "GAP",
      "overridden": false,
      "rationale": "",
      "confidence": "HIGH"
    }
  }
}
```

- For A0 UCs, `answers` holds sub-criterion checks (`sub_id -> bool`) and `proposed_state` is
  `null` (manual); `final_state` is the assessor's pick.
- `final_state` = `proposed_state` unless `overridden` is true.
- Autosave writes this object to `localStorage` on every change.
- Import validates `schema === "posture-assessment-record/v1"`; on mismatch or malformed JSON it
  warns and leaves the current session intact (never silently wipes answers).

## 9. Wizard UI (`app.js`, Variant A)

- **Rail:** all 47 UCs grouped by category, each with a state dot; click to jump.
- **UC view:** title + archetype badge + mono UC id; ladder questions with Yes/No/NA segmented
  controls (or, for A0, the bespoke guidance checklist + a manual state selector).
- **Scoring card (sticky):** proposed state chip + a one-line "why" (which rule/qid fired);
  expandable drawer with rationale textarea, confidence (LOW/MED/HIGH), and a final-state override
  select. Override requires a rationale before it is accepted.
- **Header:** overall progress (scored / 47), Import, Export.

## 10. Error handling

| Condition | Behaviour |
|---|---|
| Missing rubric CSV (build) | Hard error, non-zero exit. |
| `{slot}` with no matching param (build) | Hard error naming the UC + slot. |
| Import: schema mismatch / malformed JSON | Warn in-page; keep current session. |
| localStorage unavailable or quota exceeded | Warn once; continue without autosave. |
| Override selected without rationale | Block the override; prompt for rationale. |

## 11. Testing (TDD)

1. `derive_state` unit cases for all five outcomes + edge cases (`tests/test_scoring.py`).
2. Both engines conform to `scoring-vectors.json` (pytest + node `scoring.test.mjs`).
3. `rubric_loader`: all 47 UCs resolve; params fill with no leftover `{slot}`; A0 UCs yield
   sub-criteria; archetype UCs yield ladder questions (`tests/test_rubric_loader.py`).
4. Build: output is self-contained (no external `http(s)`/`src`/`href` refs), embeds all 47 UCs,
   inlines scoring.js + app.js (`tests/test_build_questionnaire.py`).

## 12. Process

- Branch `ws3-questionnaire` off `main` (WS-1 + WS-2 merged).
- TDD discipline (RED → GREEN → REFACTOR), atomic commits.
- `requesting-code-review` before PR; `code-review` on the diff.
- No new ANZ tokens (locked naming constraint).
- On completion: mark WS-3 slice 1 done in `meta/IMPROVEMENT-BACKLOG.md`; record deferred items
  (report adapter, framework-selection UI, Variant B, numeric inputs) as follow-ups.

## 13. Tradeoffs recorded

- **Rich-record-only export** keeps the data model clean and closes the import/re-assess
  round-trip, but defers closing the answer→report loop to a later slice (report adapter). The
  rich record is a superset of what the report needs, so the adapter is a pure projection later.
- **Dual engine (Python reference + inlined JS mirror)** risks drift; mitigated by a shared
  canonical vector fixture both suites assert against. Chosen over a single JS engine because the
  Python reference is reusable by the future report adapter and is easier to unit-test.
- **Binary quantitative questions** keep the engine and data model simple; numeric inputs can be
  added later without changing the ladder.

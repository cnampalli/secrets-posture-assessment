# WS-4 Slice 3 — Exec-Summary Print View (Design Spec)

**Status:** Approved (brainstorming, 2026-05-31)
**Workstream:** WS-4 — the consulting product. Slice 3 of 3 (final).
**Builds on:** WS-4 slice 2 roadmap generator (`engagement-menu/v1`), `questionnaire/record_state.py`, the WS-1/2/3 stack.
**Consumes:** an assessment record (`posture-assessment-record/v1`) → posture snapshot + engagement menu.

---

## 1. Goal

Render the assessment into a **slick, modern, client-facing exec-summary** — an interactive
single-file HTML microsite that also prints clean — closing WS-4. It surfaces the posture snapshot
and the prioritised engagement menu (the wedge) as a polished deliverable.

## 2. Locked decisions (brainstorming, 2026-05-31)

| # | Decision |
|---|----------|
| 1 | **Content:** page/section 1 = posture snapshot + the prioritised tier (Quick wins + Major projects); appendix = full 27-item menu grouped by quadrant. |
| 2 | **Build/data:** new `presentation/build_exec_summary.py` reads the record, computes the snapshot directly, calls `roadmap_generator.build_engagement_menu(...)` as a library; inlines data + assets into a template → one self-contained HTML. No schema change. |
| 3 | **Treatment:** dark signal-lime brand on screen; `@media print` flips to clean white/ink with page breaks. |
| 4 | **Experience:** **interactive microsite** — animated snapshot count-up, filterable/sortable quadrant board, expand/collapse findings (lean dependency-free JS), with a static fully-expanded print path. |
| 5 | **Aesthetic:** built with the `frontend-design` skill — distinctive, modern, extends existing tokens; avoid generic AI-template look. |

## 3. Architecture

Mirror the questionnaire build (`questionnaire/build_questionnaire.py`): template + inlined assets +
inlined data → one self-contained file.

**Files (new):**
- `presentation/build_exec_summary.py` — the build pipeline + CLI.
- `presentation/exec-summary-template.html` — shell with `/*__TOKEN__*/` injection points.
- `presentation/exec-summary.css` — design-system styles (screen + `@media print`).
- `presentation/exec-summary.js` — interactivity over the inlined data.

**`build(record_path, out_path=None, preset="financial", frameworks=None)`:**
1. Load the record JSON.
2. **Snapshot:** `Counter(resolve_state(r) for r in responses.values())` over *all* responses → `{MET, PARTIAL, GAP, PENDING}` (reuses `questionnaire.record_state.resolve_state`).
3. **Menu:** `roadmap_generator.build_engagement_menu(record, use_cases, trace, {}, scope, source_record=...)` using the generator's loaders; `scope` from the preset (or `--frameworks`).
4. **Inline** `exec-summary.css`, `exec-summary.js`, and `data = {snapshot, menu, meta:{generated_omitted, frameworks_scope}}` (as JSON) into the template via `/*__TOKEN__*/` replacement. Validate each token exists (raise if missing — same guard as `build_questionnaire.py`).
5. Write self-contained `exec-summary.html` (default `presentation/exec-summary.html`).

**Self-contained rule:** no external references except the same Google-Fonts CDN the existing
`presentation/*.html` decks already use, plus a system-font fallback stack. No other `http(s)`/`src`
references; CSS, JS, and data all inlined.

**No timestamp** in inlined data/output (byte-stable rebuild, matching the report/menu posture).

**CLI:** `python3 -m presentation.build_exec_summary <record.json> -o exec-summary.html [--preset financial | --frameworks slug,slug]`.

## 4. The experience & layout

Built with `frontend-design`. Latest CSS (fluid type, grid, container queries, tasteful
CSS-driven motion); JS lean and dependency-free.

- **Hero / snapshot:** client + framework scope + date; posture at a glance — animated count-up
  tiles for MET / PARTIAL / GAP / PENDING with state colors (red=gap, amber=partial, slate=pending,
  lime=met); the headline gap called out as a one-liner.
- **Prioritised tier:** Quick wins + Major projects lead — card per finding showing
  `state · risk · effort · regulatory driver · proposed engagement`, expandable for dependency/detail.
- **Quadrant board:** all 27 items as an interactive grid — **filter** by quadrant/state, **sort**
  by risk/effort. The modern, product-like view.
- **Appendix (print-primary):** complete grouped list, always fully expanded on paper.

**Print behavior (`@media print`):** white background, dark ink, expand all collapsibles, neutralise
filters (show everything), sensible `page-break` between major sections; the snapshot + prioritised
tier read as page 1, the appendix follows.

## 5. Honesty guardrails (project standard)

Render only real data from the record/menu. **No invented numbers** — no fabricated ROI, effort,
cost, or duration; risk/effort are the qualitative bands they are. Zero/empty states render honestly
("0 MET"). Enforced in code review.

## 6. Verification / tests

**Python (pytest) — `tests/test_exec_summary.py`:**
1. `snapshot_counts(record)` returns `{"MET":0,"PARTIAL":16,"GAP":11,"PENDING":20}` on the XYZ-derived record.
2. `build()` writes a file that: contains every one of the 27 menu `uc_id`s; contains the four snapshot counts; contains an `@media print` block; has **no** external `http(s)`/`src` refs except `fonts.googleapis.com`/`fonts.gstatic.com`.
3. Token guard: removing a `/*__TOKEN__*/` from the template raises (mirrors build_questionnaire test).
4. Byte-stable: two consecutive builds of the same record produce identical bytes.

**JS logic (node `.mjs`, mirrors `questionnaire/scoring.test.mjs`) — `presentation/exec-summary.test.mjs`:**
5. Quadrant grouping over the inlined data yields correct uc_id sets.
6. Filter "Quick wins" → only Quick-wins uc_ids; sort by risk orders High→Med→Low.

**Dogfood:** build on the XYZ record (record built from `matrix/anz-current-state.csv`, as in the
slice-2 dogfood) → an open-able `exec-summary.html`; smoke-check snapshot + 27 items present; headless
screenshot if Chrome available (matching the WS-3 questionnaire smoke test). Full suite stays green.

## 7. Scope boundaries

**In scope:** `build_exec_summary.py`, `exec-summary-template.html`, `exec-summary.css`,
`exec-summary.js`, tests, ADR-014, backlog update.

**Out of scope:** changing `engagement-menu/v1` or the record schema; new regulatory/data; server-side
PDF generation (use the browser "Print → Save as PDF" path); multi-client theming (YAGNI).

## 8. Artifacts produced

- `presentation/build_exec_summary.py`
- `presentation/exec-summary-template.html`, `exec-summary.css`, `exec-summary.js`
- `tests/test_exec_summary.py`, `presentation/exec-summary.test.mjs`
- `docs/adr/ADR-014-exec-summary-view.md`
- `meta/IMPROVEMENT-BACKLOG.md` (WS-4 slice 3 / WS-4 complete)

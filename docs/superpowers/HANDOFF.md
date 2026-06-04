# HANDOFF — Brass Editorial UI rebuild (pause 2026-06-03)

**Resume point:** Plans 1 (foundation) + 2 (questionnaire) are **done and committed** on
branch `feat/brass-editorial-ui`. **Next session: (1) fix one layout bug, then (2) do
Plan 3 — re-skin the matrix viewer + exec summary to Brass Editorial.** After Plan 3,
run a whole-branch review + `superpowers:finishing-a-development-branch` (PR/merge).

---

## 1. The locked direction (decided via visual-companion mockups)

- **Aesthetic:** "Brass Editorial × Technical" — one type system, two themes.
  - Fonts: **Fraunces** (serif display) · **Inter** (body) · **JetBrains Mono** (metadata/IDs).
  - **Editorial Light** default (warm paper `#f7f3ea`, ink `#231f1a`); **Technical Dark**
    toggle (warm near-black `#141216`, ink `#ece6dc`).
  - **Signature accent: Brass `#9A7B32` (light) → `#D6B25A` (dark, +glow).**
  - Semantic states: MET green `#2f6b4f` · PARTIAL ochre `#9a6a1e` · GAP claret `#9b2f2f`
    · PENDING slate `#475069` · NA grey (each with soft tints; light+dark values).
- **Build:** **React + TS + Tailwind**, bundled by **Vite + vite-plugin-singlefile** to ONE
  offline `.html` (no network — opens via `file://`). User chose React over vanilla/shadcn.
- **UI scope = "Middle"** (Phase 2): launcher + questionnaire + evidence in-browser;
  matrix/exec stay Python-generated, triggered from UI. ⚠️ Open tension: a `file://` app
  can't spawn Python — resolve in Phase 2 (in-browser generation OR export+double-click bundle).
- **Phasing:** uplift first, then features. **Evidence upload is a Phase-2 feature — NOT built.**

Spec: `docs/superpowers/specs/2026-06-03-brass-editorial-react-uplift-design.md`
Plans: `docs/superpowers/plans/2026-06-03-brass-editorial-foundation.md` (done),
`…-questionnaire.md` (done). Plan 3 not yet written.

> This **supersedes** the earlier indigo "Modern SaaS" uplift (which is still sitting as
> uncommitted working-tree edits — see §5).

---

## 2. What's DONE (committed on `feat/brass-editorial-ui`)

**Plan 1 — Foundation (9 commits, `44679a4`→`21d86b3`):** Vite React-TS single-file offline
build + `check-offline.mjs` guard; shared tokens `design/brass-editorial.tokens.json` +
`design/emit-tokens.mjs` → emits BOTH `app/src/styles/tokens.css` AND
`design/brass-editorial.vars.css` (the latter is **for Plan 3's Python reports**); embedded
fonts (base64, offline); `ThemeProvider` (light/dark, persisted, `.dark` class); UI primitives
`Button/Badge/Card/ToggleGroup` (token-styled, `app/src/components/ui/`).

**Plan 2 — Questionnaire (8 commits, `174bdb8`→`c48ff94`):**
- Engine (`app/src/assessment/`): `rubric.ts` (loads committed `app/src/data/rubric.json`,
  47 UCs, emitted by `questionnaire/emit_rubric.py`), `scoring.ts` (verbatim port, passes the
  8 vectors in `questionnaire/scoring-vectors.json`), `record.ts` (`buildRecord` → exact
  `posture-assessment-record/v1` schema), `persistence.ts` (localStorage + import/merge),
  `store.tsx` (`useAssessment`).
- UI: `App.tsx` (shell + header), `Sidebar.tsx`, `UseCaseView.tsx`, `ScorePanel.tsx`,
  `Toast.tsx`, `ui/Checkbox.tsx`.
- Export/import wired; **cross-language test `tests/test_react_export_schema.py`** proves a
  React-exported record builds the Python exec summary.

**Verification (all green):** `cd app && npm test` = **28**; `python3 -m pytest -q` = **112**;
`cd app && npm run build:check` = single offline file; **both themes screenshot-verified**.

**Build/run the app:** `cd app && npm run build` → open `app/dist/index.html` (or
`npm run dev` for hot-reload). Headless verify: `cd app && npm run build:check`.

---

## 3. ⚠️ FIX FIRST next session — sidebar/scroll layout bug

**Symptom (user-reported):** scroll the sidebar down, click a lower use case → the main
panel appears blank; you must scroll back up to see the questions. The whole page scrolls as
one, and navigating doesn't reset scroll.

**Root cause:** `app/src/App.tsx` `Shell` uses `min-h-screen` on the outer div, so the page
grows and the WINDOW scrolls instead of the sidebar/main scrolling independently. Also `go()`
doesn't reset the main scroll position (the old `app.js` did `window.scrollTo(0,0)`).

**Fix (small):**
1. In `App.tsx` `Shell`: make the outer `h-screen overflow-hidden flex flex-col`; keep the
   inner row `flex flex-1 min-h-0`; the `<main>` already has `overflow-auto` — with a fixed
   parent height it will scroll internally (sidebar already `overflow-auto`). Verify the
   sidebar and main now scroll independently and the header stays put.
2. Reset main scroll on UC change: give `<main>` a ref and, in `UseCaseView`,
   `useEffect(() => { mainRef.current?.scrollTo(0,0) }, [uc.uc_id])` — OR scroll the main
   container to top inside the store `go`. Add a quick test or just visually verify.
3. Rebuild + screenshot both themes to confirm.

---

## 4. Plan 3 — Report re-skin (the remaining plan; write + execute next session)

Re-skin the matrix viewer + exec summary to Brass Editorial so all three deliverables are
one product. Per spec §4-C / §3.2–3.3 (these stay **Python-generated**, not React):
- Swap `brand_fonts.py` fonts to **Fraunces / Inter / JetBrains Mono** woff2. The app already
  downloaded these to `app/src/assets/fonts/` — copy them to repo-root `assets/fonts/` (or
  re-fetch via the fontsource jsDelivr URLs in `app/scripts/fetch-fonts.mjs`), and update
  `brand_fonts._FACES` family names accordingly.
- Re-skin `matrix/report-template.html` `<style>` and `presentation/exec-summary.css` to the
  Brass Editorial tokens. **Reuse `design/brass-editorial.vars.css`** (already emitted by
  Plan 1) — inject it into the report templates so the reports share the SAME tokens as the
  app. Preserve all JS-keyed classes + `/*__X__*/` markers + the exec `@media print` path.
- Rebuild both; **regenerate `tests/fixtures/report.snapshot.html`**; `python3 -m pytest -q`
  green; update the exec-summary external-fonts test (already done in the indigo round — verify).
- Visual QA: screenshot all 3 deliverables in Brass Editorial, confirm cohesion + print.

**Writing the plan:** follow the same pattern as the foundation/questionnaire plans
(`writing-plans` skill), then execute with `subagent-driven-development`.

---

## 5. Git state (read carefully)

- Branch **`feat/brass-editorial-ui`** (off `main` base `4e989eb`). 17 committed commits (§2).
- **Uncommitted working-tree edits (20 tracked files): the SUPERSEDED indigo Modern-SaaS round**
  — edits to `matrix/report-template.html`, `matrix/report_render.py`,
  `presentation/exec-summary.css`, `presentation/build_exec_summary.py`,
  `questionnaire/app.js`, `questionnaire/build_questionnaire.py`, etc. **Plan 3 will re-skin
  these same files to Brass Editorial, overwriting the indigo edits.** Safe to `git checkout --`
  them at Plan 3 start (or just let Plan 3 overwrite). They are NOT the Brass direction.
- **Untracked (KEEP):** `docs/superpowers/` (spec + plans + this HANDOFF), `brand_fonts.py` +
  `assets/fonts/` (from the indigo round — **reuse/repurpose for Plan 3**, but swap fonts),
  `questionnaire/questionnaire.html` (indigo-built output, superseded by the React app).
- **Untracked, NOT from this work (leave alone):** `matrix/REGULATOR-AUDIT-2026-06-03.md`,
  `matrix/build_stakeholder_pack.py`, `stakeholder/` — pre-existing, unrelated.
- Nothing has been pushed; no PR yet (deliberate — finish Plan 3 first).
- `.superpowers/` (visual-companion mockups) is gitignored; mockups live in
  `.superpowers/brainstorm/*/content/` if you want to revisit the direction.

---

## 6. How to resume

1. Read this file + the spec + the two plan docs.
2. `git checkout feat/brass-editorial-ui` (already there).
3. Fix the scroll bug (§3), rebuild, eyeball both themes.
4. Write Plan 3 (§4) → execute via subagent-driven-development.
5. Whole-branch final review → `superpowers:finishing-a-development-branch` (decide PR/merge;
   ask the user — they've been carrying the indigo edits intentionally).

**Phase 2 (future, after the uplift trilogy):** launcher app-shell (mockup at
`.superpowers/brainstorm/*/content/06-launcher.html`), use-case **evidence upload**
(IndexedDB, base64, embedded in export), and the "Middle" UI-triggered generation
(resolve the file://-can't-run-Python tension).

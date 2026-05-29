# Improvement Backlog — Posture-Assessment Instrument

**Created:** 2026-05-29
**Status:** Planning (grill-me session complete; not yet executing)
**Source:** Deep-research project map (Explore agent) + grill-me goal-setting session

---

## Vision (locked this session)

Evolve the one-off XYZ secrets-management report into a **reusable posture-assessment
instrument for any client in any industry, in Australia**, whose **heart is a formalised
assessment methodology** (the questionnaire). The assessment's GAP/PARTIAL/PENDING findings
remain the engagement menu — the recurring-revenue consulting wedge.

## Locked decisions (grill-me, 2026-05-29)

| # | Decision | Outcome |
|---|----------|---------|
| 1 | Primary goal | Reusable instrument, **any AU client, any industry**; methodology is the core |
| 2 | De-target model | **Universal core + selectable regulatory overlay.** Client picks framework(s) — ISM / Essential 8 maturity / Zero Trust / APRA / etc. — report scopes to selection + 1–2 comparison overlays. Engine-filtering change, not new research (all 7 frameworks already in `regulatory-trace.csv`). |
| 3 | Methodology shape | **All three, sequenced:** (1) scoring rubric → (2) interactive instrument → (3) end-to-end process doc |
| 4 | Scoring autonomy | **Rubric-assisted + override** — rubric proposes a state from answers; assessor confirms/overrides with rationale + confidence (column already exists) |
| 5 | Front door | **Facilitated-primary, architected as "both."** Optimise first build for a consultant driving it live; current-state file = single source of truth (hub-and-spoke) so self-serve drops in later without rebuild |

Jurisdiction stays **AU only** (other jurisdictions = swappable data later; YAGNI now).

---

## Workstreams

Ordered by the locked dependency chain. WS-1 → WS-2 → WS-3 → WS-4 is the critical path;
WS-5 is opportunistic enablement pulled in where it unblocks the others.

### WS-0 — PARKED: Phase 1A engine generalization
**Status: parked this session — come back later.** Original approved plan
(`~/.claude/plans/observing-one-more-thing-prancy-leaf.md`): generalize ANZ→client engine,
`new_client.py` scaffold, intake, client branding, ANZ regression guard, rename 4 lowercase-`anz`
files. **Not dead** — it becomes the *engineering enabler* pulled into WS-2/WS-3/WS-5 piecemeal,
rather than executed as a monolithic phase. The multi-client file layering (Library / AU-jurisdiction /
Client-engagement) is still the target architecture.

### WS-1 — Scoring rubric (methodology substance) — ✅ DONE (2026-05-29, branch `ws1-assessment-rubric`)
Delivered as an **archetype library + A0 fallback** (chosen over derive-then-refine). Artifacts in
`methodology/`: `assessment-archetypes.csv` (A0–A8), `archetype-questions.csv`, `uc-archetype-map.csv`
(all 47 UCs mapped), `bespoke-criteria.csv`, `RUBRIC.md`, `validate_rubric.py` (+ `tests/test_rubric.py`,
13 tests), `posture-rescore.csv` + `compare_dogfood.py`. ADR-008 records the decision. **Dogfood: 98%
(46/47) reproduction of the frozen expert verdicts**, one principled divergence (UC-N-012 PENDING→GAP).
Spec: `docs/superpowers/specs/2026-05-29-assessment-rubric-design.md`; plan:
`docs/superpowers/plans/2026-05-29-ws1-assessment-rubric.md`. No new ANZ references introduced.
Follow-up noted: several baseline rows have mislabeled evidence text (data-quality cleanup, didn't affect verdicts).

The credibility core and a prerequisite for the instrument.
- For each of the 48 use-cases, define what **MET vs PARTIAL vs GAP vs PENDING** concretely means.
- Map the **diagnostic question(s)** that produce each verdict (the questionnaire item ↔ use-case ↔ state link).
- Define **confidence rules** (evidence quality → confidence level).
- Output: a rubric artifact (likely a new CSV/markdown pair) the engine and instrument both consume.
- **Skills:** `superpowers:brainstorming` (rubric structure), `superpowers:writing-plans`,
  `deep-research` (ground the maturity definitions in real models — Essential 8 maturity levels,
  ZT maturity, NIST), `gsd-spec-phase` (ambiguity-scored WHAT).

### WS-2 — Selectable regulatory overlay (engine) — **enables industry-agnostic**
- Externalize `FRAMEWORK_LABELS`, framework scoping, and the AU-specific `VENDOR_RESIDENCY`/IRAP
  logic out of `build_matrix_viewer.py` into config (YAML/JSON).
- Add a **framework-selection input**: report regenerates scoped to chosen framework(s) + 1–2 overlays.
- Decouple FI-only residency weighting → industry-tunable (IRAP weight high for gov, low for retail).
- Keep Essential 8 + Privacy Act as always-on AU baseline.
- **Skills:** `gsd-plan-phase` + `gsd-execute-phase`, `superpowers:test-driven-development`
  (scoring/filtering logic), `code-review` / `requesting-code-review`, `superpowers:systematic-debugging`.

### WS-3 — Interactive instrument (questionnaire UI) — **the front door**
- Self-contained HTML questionnaire (matches the no-server moat).
- Rubric-assisted scoring: proposes state from answers, **override + rationale + confidence**.
- Exports the **current-state file** (the single source of truth) that feeds the report.
- Facilitated-primary UX; architected so self-serve guidance layers on later.
- **Skills:** `frontend-design`, `gsd-ui-phase` (UI-SPEC) / `gsd-sketch` (throwaway mockup first),
  `superpowers:test-driven-development`, `gsd-ui-review`.

### WS-4 — End-to-end process doc (playbook) — **the consulting product**
- Document the methodology: scoping → evidence collection → scoring → **gap report + remediation
  roadmap** → re-assessment cadence.
- Remediation roadmap output: turn GAP/PARTIAL findings into a prioritised engagement menu (the wedge).
- Exec-summary print view.
- **Skills:** `brand-guidelines` (polish), document-generation skills if Word/Excel exports wanted,
  `gsd-docs-update`.

### WS-5 — Codebase hygiene (opportunistic enabler)
Pull in only where it unblocks WS-2/WS-3.
- Rename `anz-current-state.*`, `ADR-005-anz-evidence-policy.md`, `07-anz-current-state-synthesizer.md`
  → client-generic names; update references.
- Remove stale `GEMINI.md`; archive `research/vendors/_checkpoint-*.md`.
- Add **CSV schema validation** (required columns, referential integrity, row-count asserts) — highest-ROI
  robustness item given zero current guards.
- Modularize the 957-line monolith: split CSV I/O / business logic / HTML templating.
- Tests + CI only once a second client proves the seams.
- **Skills:** `superpowers:test-driven-development`, `requesting-code-review`, `git-commit`,
  `superpowers:systematic-debugging`.

---

## Skills verdict

**Install nothing.** Marketplace search (compliance / questionnaire / gap-analysis / maturity)
returned only low-install (18–36), unproven skills. The installed stack — superpowers, gsd-*,
frontend-design, deep-research, brand-guidelines, code-review, skill-creator — covers every workstream.
Two marketplace skills were noted but rejected: `claude-office-skills@form-builder` (frontend-design is
the better fit for self-contained HTML) and official xlsx/docx skills (export is nice-to-have, not core).

Idea worth revisiting: once the methodology is formalised, the **assessment process itself could be
encoded as a reusable skill** (`skill-creator`) so any future engagement runs the same playbook.

---

## Open secondary decisions (not yet grilled — resolve at WS start)
- Exact framework-selection UX (pre-build config flag vs in-report toggle vs questionnaire-driven).
- Remediation-roadmap prioritisation model (risk × effort? regulatory-deadline-driven?).
- Whether the current-state file format changes (CSV today) to carry rationale + per-answer evidence.
- Industry list + which framework set each maps to (FI→APRA; gov→PSPF/ISM; health→Privacy/MyHR;
  critical-infra→SOCI; baseline→Essential 8 + Privacy Act).

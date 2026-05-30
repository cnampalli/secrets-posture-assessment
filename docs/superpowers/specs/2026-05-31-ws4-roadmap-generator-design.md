# WS-4 Slice 2 — Roadmap Generator (Design Spec)

**Status:** Approved (brainstorming + review-agent audit + human authorization, 2026-05-31)
**Workstream:** WS-4 — the consulting product. Slice 2 of N.
**Builds on:** WS-4 slice 1 playbook (the documented prioritisation method), WS-1 rubric, WS-2 overlay presets, WS-3 questionnaire record, report adapter (ADR-011).
**Defers to later slices:** the exec-summary print view (renders the JSON this slice emits).

---

## 1. Goal

Turn the playbook's documented risk × effort prioritisation method into code: a generator that
reads an `assessment-record.json`, applies the method, and emits a structured **engagement-menu
JSON** — the prioritised consulting wedge — for the future exec-summary print view to render.

## 2. Locked decisions

| # | Decision | Source |
|---|----------|--------|
| 1 | New module `questionnaire/roadmap_generator.py`: pure transform + writer + thin CLI, mirroring `report_adapter.py`. | brainstorming |
| 2 | Effort band from a per-engagement input CSV; missing → **Med** default. | brainstorming Q1 |
| 3 | Risk band seeded from `use-cases.csv.priority_fi` (P0→High, P1→Med, **else→Low** incl. blank/unknown), overridable in the per-engagement CSV. | brainstorming Q2 |
| 4 | Output = `engagement-menu/v1` JSON. Human rendering is a later slice. | brainstorming Q3 |
| 5 | Regulation = **ordering tie-breaker only** (no auto risk-band escalation). Soften PLAYBOOK Stage 5 + METHODOLOGY to describe escalation as an assessor judgment recorded in the input file. | authorization Q1(a) |
| 6 | Default framework scope = **financial preset** (APRA + Essential 8 + ZTMM); MITRE always excluded; `--frameworks` overrides. | authorization Q2(a) |
| 7 | Regulatory driver cap = **one control per in-scope framework, max 3**, regulator (BACK-MAP/APRA) first. | authorization Q3(a) |
| 8 | Bundle both slice-1 doc corrections into this branch: `RUBRIC.md` `override_reason`→`rationale`, and the escalation softening. | authorization Q4 |

## 3. Architecture

`questionnaire/roadmap_generator.py` — same shape as `report_adapter.py`:
- **Pure function** `build_engagement_menu(record, use_cases, reg_trace, engagement_inputs, frameworks) -> dict`. No file I/O. Fully unit-testable.
- **Loaders** (thin): read `use-cases.csv`, `regulatory-trace.csv`, the engagement-input CSV, and the preset YAML for default scope.
- **Writer** `write_menu(menu, path)` — emits JSON.
- **CLI** (`python3 -m questionnaire.roadmap_generator`): mirrors the adapter.

**Shared state resolver (de-dup with adapter):** the GAP/PARTIAL filter MUST resolve state identically
to the report. Extract `resolve_state(response) -> final_state or proposed_state or "PENDING"` into a
small shared helper that BOTH `report_adapter.py` and `roadmap_generator.py` import, so the engagement
menu can never disagree with the Stage-4 report. (Adapter currently inlines this at `report_adapter.py:36`;
refactor it to call the shared helper — behaviour-preserving, covered by existing adapter tests.)

## 4. Pipeline (pure function)

1. **Filter:** for each UC in `record["responses"]`, resolve state via the shared resolver; keep only
   resolved ∈ {`GAP`, `PARTIAL`}. (MET/PENDING are not engagement items.)
2. **Risk band:** `engagement_inputs[uc].risk_override` if non-blank, else seed from
   `use-cases.csv.priority_fi`: `P0→High`, `P1→Med`, **anything else (incl. P2/blank/unknown)→Low**.
3. **Effort band:** `engagement_inputs[uc].effort` if non-blank, else **Med**.
4. **Quadrant:** from (risk, effort):
   - High risk / Low effort → **Quick wins**
   - High risk / High effort → **Major projects**
   - Low risk / Low effort → **Fill-ins**
   - Low risk / High effort → **Hard slogs**
   - Med on either axis: Med risk is treated as High for quadrant *band-pairing* only where the playbook's
     2×2 needs a binary — **rule:** risk∈{High,Med}=“high side”, risk=Low=“low side”; effort∈{High,Med}=
     "high side" for the Major/Hard axis, effort=Low="low side". Concretely: quadrant uses
     `risk_high = risk in {High,Med}` and `effort_high = effort == High`. (Documented explicitly so the
     mapping is unambiguous; Med-effort lands in the Low-effort column — i.e. actionable — by design.)
5. **Regulatory driver:** from `regulatory-trace.csv`, take rows whose `uc_ids` contains this UC AND whose
   `framework_slug` is in scope. **Scope** = the `--frameworks` list if given, else the slugs from the
   **financial preset** (`matrix/config/presets/financial.yaml`) plus Essential 8 baseline. **Always exclude
   `framework_role == ADVERSARY-LENS` (MITRE)** — it is not a regulatory obligation. **Cap:** one control
   per in-scope framework, max 3, ordered regulator-first (`BACK-MAP` before `PRIMARY-LENS`). Each driver
   entry = `{framework_slug, control_code, control_short_title}`.
6. **Dependency:** `engagement_inputs[uc].dependency` free text if present, else `""`.
7. **proposed_engagement:** template from `short_title` + resolved state only — `"{state} → remediate: {short_title}"`.
   **No** effort/duration/cost words (honesty standard).
8. **Order:** quadrant priority (Quick wins → Major projects → Fill-ins → Hard slogs), then risk desc
   (High→Med→Low), then **regulatory-driven first** (findings with ≥1 driver before those without — the
   tie-breaker), then `uc_id` ascending.

## 5. Output schema — `engagement-menu/v1`

```json
{
  "schema": "engagement-menu/v1",
  "source_record": "<input record path or its embedded id>",
  "frameworks_scope": ["apra-cps-234", "essential-8", "cisa-ztmm-v2"],
  "items": [
    {
      "uc_id": "UC-F-001",
      "state": "GAP",
      "risk_band": "High",
      "effort_band": "Low",
      "quadrant": "Quick wins",
      "regulatory_driver": [
        {"framework_slug": "apra-cps-234", "control_code": "CPS234-§28a", "control_short_title": "..."}
      ],
      "dependency": "",
      "proposed_engagement": "GAP → remediate: Prevent plaintext secrets in source repos"
    }
  ]
}
```

`generated` timestamp is intentionally **omitted** (non-deterministic; would break golden tests and
byte-stable diffs — consistent with the report's no-timestamp build posture). Provenance is carried by
`source_record` + `frameworks_scope`.

## 6. Per-engagement input CSV

Columns: `uc_id, risk_override, effort, dependency, escalation_control`
- `risk_override` ∈ {High, Med, Low} — blank = use the `priority_fi` seed.
- `effort` ∈ {High, Med, Low} — blank = Med.
- `dependency` — free text — blank = "".
- `escalation_control` — optional cited control code carrying the assessor's logged escalation judgment
  (honors the playbook's "always with a control reference" rule; recorded, surfaced in output as a driver
  if in scope, but does NOT auto-mutate the band).

The flag is `--engagement <csv>` (optional). With no file, every finding uses seed risk + Med effort.

## 7. Slice-1 doc corrections (bundled, decision #8)

- `methodology/RUBRIC.md §5`: rename `override_reason` → `rationale` (the schema is frozen; the doc is the outlier).
- `methodology/PLAYBOOK.md` Stage 5 + `methodology/METHODOLOGY.md`: reword the regulatory-escalation
  sentences so escalation is an **assessor judgment recorded in the per-engagement file** (logged with its
  control reference), not an automatic behavior. Tie-breaker ordering stays as the automatic part.

## 8. Scope boundaries

**In scope:** `roadmap_generator.py` (function + loaders + writer + CLI); shared state-resolver refactor;
the per-engagement CSV contract; `engagement-menu/v1`; tests; the two doc corrections; ADR-013; backlog update.

**Out of scope:** the exec-summary print view (renders this JSON — later slice); any change to the
questionnaire/record schema; auto risk-band escalation; new regulatory data (e.g. Privacy Act trace rows,
which do not exist — the Privacy Act baseline remains a methodology stance, not a driver source).

## 9. Verification / tests (TDD)

Unit (pure function, no I/O — pass in-memory dicts/lists):
1. Filter keeps only resolved GAP/PARTIAL; MET/PENDING excluded; `final_state=null` falls back to `proposed_state`.
2. Risk seed mapping P0/P1/P2/blank → High/Med/Low/Low; risk_override wins when present.
3. Effort default Med; effort override wins.
4. Quadrant mapping for all four corners + Med-on-each-axis rule.
5. Regulatory driver: MITRE/ADVERSARY-LENS excluded; scoped to frameworks; capped at 3 one-per-framework; regulator-first ordering; entry shape.
6. proposed_engagement template exact; no effort words.
7. Ordering: quadrant → risk → regulatory-driven-first → uc_id.
8. Output schema/version + frameworks_scope provenance; no `generated` key.
Shared resolver: existing `report_adapter` tests still pass after the refactor (regression guard).
CLI: writes valid JSON from a record path; `--engagement` and `--frameworks` honored; default scope = financial preset.
Dogfood: run on the XYZ data (the 11 GAP + 16 PARTIAL = 27 findings) → a stable `engagement-menu/v1`. UC-F-001 (priority_fi P0→risk High; no effort override→Med→effort-low-side) lands in **Quick wins**. With an engagement file giving UC-N-001 `effort=High`, it lands in **Major projects**. Assert structure + these key placements, not invented counts.
Full suite (currently 65) stays green.

## 10. Artifacts produced

- `questionnaire/roadmap_generator.py`
- shared state-resolver helper (small; e.g. `questionnaire/_state.py` or a function in an existing shared module) + `report_adapter.py` refactored to use it
- `tests/test_roadmap_generator.py`
- `methodology/RUBRIC.md`, `methodology/PLAYBOOK.md`, `methodology/METHODOLOGY.md` (doc corrections)
- `docs/adr/ADR-013-roadmap-generator.md`
- `meta/IMPROVEMENT-BACKLOG.md` (WS-4 slice 2 marked)

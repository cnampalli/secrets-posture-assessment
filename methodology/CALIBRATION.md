# External calibration protocol (A6)

**Status:** protocol ACCEPTED 2026-07-02 · panel NOT YET RUN — until a panel result is
recorded below, the instrument's only calibration evidence is internal (98% dogfood
reproduction of frozen expert verdicts) and every external claim must say so.

The 2026-06-15 and 2026-07-02 independent reviews both scored dimension A6
(calibration) band 1: scoring is validated only against internal frozen verdicts and a
synthetic benchmark cohort. This protocol is the remediation: cheap, repeatable,
honest, and executable by a solo architect.

## 1. SME panel

- **Panel:** 2–3 external reviewers, each with current practitioner depth in at least
  one domain (one PAM, one IGA, one secrets/platform). Recorded with role + years +
  independence statement (no commercial stake in this instrument); anonymised in
  published output if requested.
- **Sample:** `calibration/sme-panel-template.csv` — 15 use cases (5 per domain,
  stratified across the UC range so agentic and non-functional UCs are represented).
  Re-generate the sample only between panels, never mid-panel.
- **Materials given to reviewers:** `RUBRIC.md` (archetype bands + state definitions),
  the sampled UCs' stories/acceptance criteria, and the SAME current-state evidence the
  instrument scored from. Reviewers do NOT see the instrument's verdicts (blind).
- **Task:** for each sampled UC, record `reviewer_state` (MET/PARTIAL/GAP/PENDING) and
  `reviewer_confidence` (HIGH/MEDIUM/LOW) in a copy of the template.
- **Scoring:** merge the instrument's `instrument_state`/`instrument_confidence` into
  the filled sheet, then run
  `python3 methodology/calibration/compute_agreement.py <filled.csv>`.
  Metric = quadratic-weighted Cohen's kappa on GAP<PARTIAL<MET (PENDING excluded,
  reported). Raw agreement reported alongside.

## 2. Interpretation bands (declared BEFORE any panel runs)

| weighted kappa | reading | action |
|---|---|---|
| ≥ 0.75 | strong external agreement | citable: "externally calibrated" |
| 0.55–0.74 | moderate | citable with the number; review divergent archetypes |
| < 0.55 | weak | NOT citable as calibration; rubric revision required |

Divergences are analysed per-archetype (a systematic divergence on one archetype is a
rubric defect, not reviewer noise) and recorded in §4 with the rationale — the same
override-with-rationale discipline the instrument itself uses.

## 3. Benchmark cohort honesty (wired, enforced)

`matrix/config/benchmark-cohort.json` bands now carry `cohort_type: synthetic|measured`
and `n`. `matrix/benchmark.py::load_cohort` refuses `measured` below n=5 anonymised
engagements (MEASURED_MIN_N) — the label is earned, never asserted. Engagement met-%
distributions are added per-domain as anonymised aggregates only (no client-identifiable
data; see the no-multi-tenant decision in ADR history).

## 4. Panel results ledger

| date | panel (roles, anonymised) | n scoreable | raw | weighted kappa | verdict | notes |
|---|---|---|---|---|---|---|
| — | *(no panel run yet)* | — | — | — | — | — |

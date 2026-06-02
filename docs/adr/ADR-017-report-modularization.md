# ADR-017: Report Generator Modularization

**Status:** Accepted
**Date:** 2026-06-03
**Workstream:** WS-5 slice 3 (5d) — completes WS-5

## Context
`matrix/build_matrix_viewer.py` had grown to 949 lines mixing four concerns: CSV
loading, model transforms (REGDATA/RECDATA/glossary/meta), a ~590-line inline HTML/CSS/JS
template string, and orchestration. It was hard to navigate and the logic was untestable in
isolation.

## Decision
Split it into flat sibling modules in `matrix/` (the same convention as `engagement_config.py`
and `overlay.py`, which rely on the script's dir being on `sys.path[0]`):

- `report_io.py` — CSV loading + the static vendor maps (`VENDOR_LAYER`/`SHORT`/`LAYER_LABEL`/
  `SUBSTRATE_SLUG`) + config-driven residency/label loads.
- `report_logic.py` — pure model transforms (`build_regdata`, `build_recdata`, `build_glossary`,
  `compute_meta`) with the logic constants. No I/O.
- `report-template.html` — the `TEMPLATE` raw string, extracted verbatim.
- `report_render.py` — loads the template and performs the token-replacement assembly.

`build_matrix_viewer.py` shrinks to an **89-line** orchestrator + CLI (was 949): parse args →
load → resolve engagement → build model → render → write.

The refactor is pure structural extraction — **no output change**, enforced by a permanent HTML
byte-snapshot test (`tests/test_report_render.py` vs `tests/fixtures/report.snapshot.html`) plus the
pre-existing `REGDATA`/`RECDATA` golden (`test_engine_integration`). The report build is deterministic
(verified identical md5 across runs), so the snapshot is stable. Each extraction step kept the report
byte-identical.

## Alternatives considered (rejected)
- **Keep the template as a Python string** in a module: a separate `.html` matches
  `build_questionnaire`'s `template.html` pattern and is diff-able / editable without touching Python.
- **A `matrix` package with `__init__.py`:** flat siblings match the existing
  `engagement_config`/`overlay` convention and avoid touching the run/build mechanics (the byte-stable
  default build).

## Consequences
- The report logic is now unit-testable in isolation (`tests/test_report_logic.py` added).
- The template is editable without touching Python.
- The HTML byte-snapshot guards the deliverable against future drift.
- **WS-5 is complete** (5a cleanup + 5c validation → 5b rename → 5d modularization).

# WS-5 Slice 3 (5d) — Monolith Split (Design Spec)

**Status:** Approved (brainstorming, 2026-06-03)
**Workstream:** WS-5 — codebase hygiene. Slice 3 (final) — completes WS-5.
**Sequence:** 5a cleanup ✅ → 5c validation ✅ → 5b rename ✅ → **5d split (this)**.

---

## 1. Goal

Split the 949-line `matrix/build_matrix_viewer.py` into focused, independently-understandable units
(CSV I/O / business logic / HTML templating + a thin orchestrator) **without changing the report
output by a single byte**. Pure structural extraction; no behavior change.

## 2. Locked decisions (brainstorming, 2026-06-03)

| # | Decision |
|---|----------|
| 1 | 4 flat siblings in `matrix/` (matching `engagement_config.py`/`overlay.py`): `report_io.py`, `report_logic.py`, `report_render.py`, and the orchestrator `build_matrix_viewer.py`; plus `report-template.html` (the `TEMPLATE` extracted verbatim). |
| 2 | Output preservation via a **permanent HTML byte-snapshot test** (`tests/fixtures/report.snapshot.html` + `tests/test_report_render.py`) captured BEFORE the refactor, combined with the existing `REGDATA`/`RECDATA` golden. |
| 3 | Pure extraction — **no logic/output change**. Verified deterministic (identical md5 across two builds), so the snapshot is stable. |

## 3. Target structure & interfaces

- **`matrix/report_io.py`** — input loading.
  - `read_csv(here, name) -> list[dict]`.
  - `load_inputs(here, current_state_path) -> Inputs` (a small dataclass/namedtuple or dict) with
    `all_rows, ranked, ucs, nhis, current, reg_rows`.
  - Owns the static vendor maps used to classify/load: `VENDOR_LAYER`, `SHORT`, `LAYER_LABEL`,
    `SUBSTRATE_SLUG`, and the config loads `VENDOR_RESIDENCY`, `FRAMEWORK_LABELS` (via `overlay`).
- **`matrix/report_logic.py`** — pure model transforms (no I/O).
  - `build_regdata(inputs, engagement, framework_labels) -> REGDATA` (frameworks, controls,
    per-control worst-state rollup via `STATE_RANK`, ucs index, vendor_uc, framework_selection).
  - `build_recdata(inputs, engagement, vendor_residency) -> RECDATA` (`_vendor_stat`, layer sorts,
    `top_picks`, `complementary`, coverage_proof, substrate).
  - `build_glossary(nhis, ucs) -> dict`; `compute_meta(inputs) -> dict`.
  - Logic-only constants: `APRA_FRAMEWORKS`, `STATE_RANK`, `ORDER`, `REC_UC_DOMAIN`.
- **`matrix/report-template.html`** — the current `TEMPLATE` raw string, extracted **verbatim**
  (every `/*__TOKEN__*/` placeholder and `__RV__/__NHI__/__UC__` marker unchanged).
- **`matrix/report_render.py`** — templating.
  - `render(here, model) -> str`: loads `report-template.html`, performs the exact token-replacement
    assembly (`/*__DATA__*/[]`, `/*__XYZ__*/[]`, … `__RV__/__NHI__/__UC__`) → the final HTML string.
- **`matrix/build_matrix_viewer.py`** — thin orchestrator + CLI (unchanged external behavior):
  parse args → resolve `ENGAGEMENT` (via `engagement_config`/`overlay`) → `report_io.load_inputs` →
  `report_logic.build_*` → `report_render.render` → write `matrix-viewer.html`; `--emit-data` dumps
  `{REGDATA, RECDATA}` exactly as today; the print summary lines preserved.

**Imports stay flat siblings** (`import report_io`, etc.) — works because Python puts the script's
dir (`matrix/`) on `sys.path[0]`, the same mechanism `engagement_config`/`overlay` already rely on.

## 4. Approach (output-preserving, incremental)

1. **Snapshot first.** Build the current report; save `tests/fixtures/report.snapshot.html`. Add
   `tests/test_report_render.py`: build to a temp path (or via `--emit-data`-style helper) and assert
   the HTML bytes equal the fixture. Lock the deliverable before any move.
2. **Extract incrementally**, re-running the full suite + byte-snapshot after each step:
   (a) `report-template.html` + `report_render.py`; (b) `report_io.py`; (c) `report_logic.py`;
   (d) shrink `build_matrix_viewer.py` to the orchestrator.
3. Each step keeps `matrix-viewer.html` byte-identical and `--emit-data` `REGDATA`/`RECDATA`
   identical.

## 5. Testing / verification

- **New byte-snapshot** (`test_report_render.py`): the built report equals `report.snapshot.html`
  byte-for-byte.
- **Existing golden** (`test_engine_integration`): `REGDATA`/`RECDATA` unchanged; all 6 engine tests
  (default + presets + CLI overrides) still pass.
- **New targeted `report_logic` unit tests** (the payoff of isolation): e.g. `build_glossary`
  truncates >170-char descriptions to `...` and includes UC titles; `compute_meta` counts; the
  control worst-state rollup picks the `STATE_RANK`-min state.
- `validate_data.py` exit 0; full suite green (106 + new tests).

## 6. Scope boundaries

**In scope:** the 4-way split; `report-template.html`; the snapshot fixture + test; targeted
`report_logic` unit tests; ADR-017; backlog (mark WS-5 complete).
**Out of scope:** any behavior/output change; engine generalization (WS-0); modifying
`engagement_config.py`/`overlay.py`; the report's content/branding; performance work.

## 7. Artifacts produced

- `matrix/report_io.py`, `matrix/report_logic.py`, `matrix/report_render.py`, `matrix/report-template.html`
- `matrix/build_matrix_viewer.py` (reduced to orchestrator + CLI)
- `tests/fixtures/report.snapshot.html`, `tests/test_report_render.py`, `tests/test_report_logic.py`
- `docs/adr/ADR-017-report-modularization.md`
- `meta/IMPROVEMENT-BACKLOG.md` (WS-5 complete)

# Phase 0 — Defects & follow-ups (code review of PR #13)

Date: 2026-06-05 · Branch: `feat/phase0-vendor-mix-optimizer` · Review: high-effort multi-angle (7 finder angles → adversarial verify).

5 findings survived verification. **#1 and #2 are fixed** (commit `32ab231`); **#3–#5 are open** and tracked here for a follow-up PR. Three additional candidates were verified and dropped (see bottom).

---

## Fixed (commit 32ab231)

### #1 — 🔴 Correctness: unassessed UCs counted as MET / hidden from gap-to-target
- **File:** `matrix/compliance.py`
- **Defect:** `STATE_RANK` ranked `UNKNOWN` as 9 (above `MET`); worst-state aggregation uses `min()`, so a control mapping a `MET` UC + an *unassessed* UC (absent from the current-state input → `UNKNOWN`) resolved to `MET`. The coverage indicator inflated and gap-to-target dropped exactly the unmeasured controls.
- **Reachability:** the questionnaire-driven path — `questionnaire/report_adapter.record_to_rows` emits rows only for answered UCs, so a partial response set leaves UCs `UNKNOWN`.
- **Fix:** `UNKNOWN` now ranks below `MET` (`GAP<PARTIAL<PENDING<UNKNOWN<MET`); data-absence blocks `MET` and surfaces as a gap, while real deficiencies still rank ahead of it. Regression tests added. No change to committed-data output (all 47 UCs assessed) — snapshot byte-identical.

### #2 — 🟠 Maintainability: duplicated domain vocabulary
- **Files:** `compliance.py`, `optimizer.py`, `resilience.py`, `vendor_intel.py`, `report_logic.py`
- **Defect:** `STATE_RANK`, the coverage-order map (`ORDER`/`COVERAGE_RANK`), and `("UC-F","UC-N")` were copy-pasted across five modules. Drift would let the compliance scorecard and the matrix control chips disagree on worst-state, and it made the #1 fix a multi-place edit.
- **Fix:** hoisted into a new leaf module `matrix/matrix_vocab.py` (no import cycle — `report_logic` imports the leaves; the leaves import `matrix_vocab`) and imported everywhere.

---

## Open follow-ups

### #3 — 🟡 Altitude: informative-framework classification hardcoded
- **File:** `matrix/report_logic.py:116` — `INFORMATIVE_FRAMEWORKS = {"mitre-attack"}`
- **Problem:** control-vs-informative is a data concept (`regulatory-trace.framework_role`; per-framework registry/labels YAML), but it's a Python constant. A second informative catalog (e.g. an adversary-TTP set) requires a code edit; a miss would score TTPs as a meaningless `MET %`.
- **Proposed fix:** drive exclusion from config (e.g. a `role: informative` flag in `config/frameworks.yaml` or reuse `framework_role`), and have `build_compliance` read it.
- **Effort:** S.

### #4 — 🟡 Doc-drift: stale `render()` model-keys docstring + `--emit-data` help
- **Files:** `matrix/report_render.py:28`; `matrix/build_matrix_viewer.py:38`
- **Problem:** `render()`'s documented `model keys` list omits `compliance` and `vendorintel` (read via `model.get(..., {})`), so a caller following the docstring silently ships a report missing those sections. `--emit-data` help still says `{REGDATA,RECDATA}` though five keys are emitted.
- **Proposed fix:** update both strings; optionally assert required keys in `render()` instead of silently defaulting to `{}`.
- **Effort:** XS.

### #5 — 🔵 Reuse: cloned YAML loaders
- **Files:** `matrix/overlay.py:24` (`load_vendor_ownership`) + `matrix/report_io.py:68` wrapper
- **Problem:** line-for-line clone of the `load_vendor_residency` pair; every new injected YAML config spawns an identical passthrough, so missing-file/encoding/validation handling can drift between them.
- **Proposed fix:** one generic `load_yaml_map(cfgdir, filename)` in `overlay`, with thin named wrappers (or call sites passing the filename).
- **Effort:** S.

---

## Verified and dropped (no action)
- **head-to-head last-row-wins** (`vendor_intel.head_to_head`): real data has 0 duplicate `(vendor_slug, target_id)` pairs and the data model is one-row-per-pair — not reachable.
- **`_control_rows` KeyError** on missing `control_code`: `csv.DictReader` guarantees the key exists when the header has the column (value `""`); the header is the contract.
- **`complement` → None hides white-space**: white-space is surfaced independently in the vendor-mix card (`cover.white_space`); `complement` correctly reports nothing to *add* when an incumbent already covers everything coverable.
- **Efficiency** (greedy_cover full rescan per iteration; `best_for` per-UC scans; double-validation of provider rows): negligible at real scale (18 vendors × 47 UCs × 1,597 rows) per the finders' own assessment; revisit only if the optimizer is reused on a much larger catalog.

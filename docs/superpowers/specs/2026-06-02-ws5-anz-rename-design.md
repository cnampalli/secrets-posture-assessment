# WS-5 Slice 2 (5b) — Legacy `anz` Schema Rename (Design Spec)

**Status:** Approved (brainstorming, 2026-06-02)
**Workstream:** WS-5 — codebase hygiene. Slice 2 (the multi-client unblock).
**Sequence:** 5a cleanup ✅ → 5c validation ✅ → **5b rename (this)** → 5d monolith split.

---

## 1. Goal

Remove the legacy ANZ-client coupling from the **data schema** so the engine is genuinely
client-agnostic: rename the `anz_state` column, the `anz-current-state.csv` file, and the
`sources_at_anz_likely` column to client-generic names, updating every code reader, the data, and
the tests in lockstep. Guarded by the WS-5c validator + the existing 104-test suite.

## 2. Locked decisions (brainstorming, 2026-06-02)

| # | Decision |
|---|----------|
| 1 | Names: `anz_state`→`current_state`; `anz-current-state.csv`→`current-state.csv`; `sources_at_anz_likely`→`sources_likely`. |
| 2 | Scope: **code + active data + tests only.** Leave all historical docs (PRD, prompts, ADR-005, `research/`, checkpoints), `dist/`, `.planning/sketches`, and the user-facing "XYZ" client branding in the report. |
| 3 | **Schema tokens only** — do NOT rename cosmetic internal vars (`XYZ` JS array, `anz` py var, `anz-card`, `anz_overrides`, `anzHtml`); they collide with XYZ branding and add risk for no reuse benefit. |
| 4 | Add a small `check_no_legacy_token` guard to `validate_data.py` so the legacy header can't silently return. |

## 3. The rename (exact tokens — all unambiguous `replace_all`)

| Legacy | New |
|--------|-----|
| `anz_state` | `current_state` |
| `anz-current-state.csv` | `current-state.csv` |
| `sources_at_anz_likely` | `sources_likely` |

These three tokens are distinct substrings (they do **not** appear inside the cosmetic
`anz`/`XYZ`/`anz-card`/`anz_overrides`/`anzHtml` identifiers), so a per-file `replace_all` is safe
and surgical.

### 3.1 Files touched

**Data:**
- `git mv matrix/anz-current-state.csv matrix/current-state.csv`; change header `anz_state`→`current_state`.
- `matrix/identity-catalog.csv`: header `sources_at_anz_likely`→`sources_likely`.

**Code (`replace_all` of the relevant tokens):**
- `questionnaire/report_adapter.py` — `COLUMNS` `anz_state`→`current_state`.
- `matrix/build_matrix_viewer.py` — `--current-state` default `anz-current-state.csv`→`current-state.csv`; the Python reader keys and the embedded report **JS** reads (`a.anz_state`→`a.current_state`) — all via `replace_all "anz_state"→"current_state"`. (The `XYZ` JS var and `anz` py var keep their names; only the data key changes.)
- `methodology/compare_dogfood.py` — file path + column.
- `matrix/validate_data.py` — `CORE_REQUIRED` key + `anz_state`/`sources_at_anz_likely` columns + message strings.

**Tests:**
- `tests/test_report_adapter.py`, `tests/test_exec_summary.py`, `tests/test_validate_data.py` — `anz_state`→`current_state`, filename refs.
- `tests/test_report_adapter_e2e.py`, `tests/test_engine_integration.py` — update only if they reference the legacy token/filename (verified during execution).

**Left untouched:** historical docs, `dist/`, `.planning/`, the report's user-facing "XYZ" branding, and the cosmetic `anz`/`XYZ` variable identifiers.

## 4. New guard — `check_no_legacy_token` (in `validate_data.py`)

A small check asserting the **data headers** carry no legacy token: `current-state.csv` must NOT
contain `anz_state`, and `identity-catalog.csv` must NOT contain `sources_at_anz_likely`. Returns
violation strings like the other checks; wired into `validate_all`. Mirrors the `check_no_anz`
pattern in `validate_rubric.py`. Catches a future regression automatically. ~10 lines + 1 test.

## 5. Verification

- **Full suite green** (104 tests) after the rename — the primary safety net.
- **Validator** (`python3 matrix/validate_data.py`) exits 0 against the renamed data.
- **Rebuilds succeed:** `build_matrix_viewer.py` (the report), `build_questionnaire.py`, and
  `build_exec_summary.py` all produce valid output with the renamed schema.
- **Residual-token scan returns zero** over code/data/tests (excluding `dist/`, `.planning/`, and
  historical doc dirs):
  `grep -rn 'anz_state\|anz-current-state\|sources_at_anz' --include=*.py --include=*.csv --include=*.html --include=*.mjs matrix/ questionnaire/ methodology/ tests/`
- The WS-2 golden snapshots (`tests/fixtures/*.snapshot.json`) are **unaffected** (no `anz_state` in them) and must still pass untouched.

## 6. Scope boundaries

**In scope:** the three-token rename across code/data/tests; the `check_no_legacy_token` guard; ADR-016; backlog.
**Out of scope:** engine generalization (WS-0); the monolith split (5d); cosmetic var renames; any doc/prompt/ADR file renames; `dist/` regeneration; client-branding parameterization.

## 7. Artifacts produced

- `matrix/current-state.csv` (renamed, new header); `matrix/identity-catalog.csv` (header change)
- edits to `report_adapter.py`, `build_matrix_viewer.py`, `compare_dogfood.py`, `validate_data.py` (+ guard), and the affected tests
- `docs/adr/ADR-016-anz-schema-rename.md`
- `meta/IMPROVEMENT-BACKLOG.md` (WS-5 slice 2 marked)

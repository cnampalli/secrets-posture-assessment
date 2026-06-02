# WS-5 Legacy `anz` Schema Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Rename the legacy ANZ schema tokens (`anz_state`→`current_state`, `anz-current-state.csv`→`current-state.csv`, `sources_at_anz_likely`→`sources_likely`) across code, data, and tests so the engine is client-agnostic.

**Architecture:** A rename adds no behavior; the existing 104-test suite + the WS-5c validator are the regression net. Task 1 is one atomic coordinated edit (data + all readers + tests together — partial renames break the suite mid-flight), then a hard gate. Task 2 adds a guard so the legacy header can't silently return. The three tokens are distinct substrings, so per-file `replace_all` is surgical (they do NOT appear inside the cosmetic `anz`/`XYZ`/`anz-card`/`anz_overrides`/`anzHtml` identifiers, which stay).

**Tech Stack:** Python 3 stdlib; pytest. Repo root `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`.

**Exact rename map:** `anz_state`→`current_state`; `anz-current-state.csv`→`current-state.csv`; `sources_at_anz_likely`→`sources_likely`.

---

### Task 1: Atomic schema rename (data + code + tests)

**Files:** `matrix/anz-current-state.csv` (→ `current-state.csv`), `matrix/identity-catalog.csv`, `questionnaire/report_adapter.py`, `matrix/build_matrix_viewer.py`, `methodology/compare_dogfood.py`, `matrix/validate_data.py`, `tests/test_report_adapter.py`, `tests/test_exec_summary.py`, `tests/test_validate_data.py` (and `tests/test_report_adapter_e2e.py`, `tests/test_engine_integration.py` if they reference the tokens).

- [ ] **Step 1: Rename the data file (preserve history)**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git mv matrix/anz-current-state.csv matrix/current-state.csv
```

- [ ] **Step 2: Update the data headers**

In `matrix/current-state.csv`, change the first line's `anz_state` → `current_state` (header only; data rows unchanged).
In `matrix/identity-catalog.csv`, change the first line's `sources_at_anz_likely` → `sources_likely`.

- [ ] **Step 3: Rename the token in every code + test file**

Apply these `replace_all` substitutions (each token is unambiguous):
- `anz_state` → `current_state` in: `questionnaire/report_adapter.py`, `matrix/build_matrix_viewer.py`, `methodology/compare_dogfood.py`, `matrix/validate_data.py`, `tests/test_report_adapter.py`, `tests/test_exec_summary.py`, `tests/test_validate_data.py`.
- `anz-current-state.csv` → `current-state.csv` in: `matrix/build_matrix_viewer.py` (the `--current-state` default), `methodology/compare_dogfood.py`, `matrix/validate_data.py`, `tests/test_exec_summary.py`, `tests/test_validate_data.py`.
- `sources_at_anz_likely` → `sources_likely` in: `matrix/validate_data.py`.

Do NOT touch: the user-facing "XYZ" branding strings, the `XYZ` JS array variable, the `anz` Python variable, `anz-card`, `anz_overrides`, `anzHtml` (these do not contain the three tokens, so `replace_all` leaves them alone — verify after).

- [ ] **Step 4: Verify — full suite, validator, rebuilds, residual scan**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q 2>&1 | tail -3
python3 matrix/validate_data.py; echo "validator exit: $?"
# rebuilds produce valid output with the renamed schema
python3 matrix/build_matrix_viewer.py >/tmp/buildlog 2>&1 && echo "report build OK" || { echo "REPORT BUILD FAILED"; tail -5 /tmp/buildlog; }
python3 questionnaire/build_questionnaire.py >/dev/null 2>&1 && echo "questionnaire build OK" || echo "Q BUILD FAILED"
python3 -c "import csv,json; rows=list(csv.DictReader(open('matrix/current-state.csv'))); json.dump({'schema':'posture-assessment-record/v1','responses':{r['uc_id']:{'proposed_state':r['current_state'],'final_state':r['current_state']} for r in rows}}, open('/tmp/cs.json','w'))"
python3 -m presentation.build_exec_summary /tmp/cs.json -o /tmp/es.html >/dev/null 2>&1 && echo "exec-summary build OK" || echo "ES BUILD FAILED"
# residual-token scan (code/data/tests only) must be empty
grep -rn 'anz_state\|anz-current-state\|sources_at_anz' --include='*.py' --include='*.csv' --include='*.html' --include='*.mjs' matrix/ questionnaire/ methodology/ tests/ && echo "RESIDUAL TOKENS FOUND" || echo "OK no residual tokens"
```
Expected: full suite green (104 passed); validator exit 0; all three builds `OK`; `OK no residual tokens`. If the suite fails, the failure names the file/line still on the old token — fix it (likely `test_report_adapter_e2e.py` or `test_engine_integration.py` referencing the filename/column) and re-run.

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/current-state.csv matrix/identity-catalog.csv questionnaire/report_adapter.py matrix/build_matrix_viewer.py methodology/compare_dogfood.py matrix/validate_data.py tests/
git commit -m "refactor(ws5): rename anz_state->current_state, current-state.csv, sources_likely

Client-agnostic data schema. Code+data+tests in lockstep; historical docs/dist untouched.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
(Stage only the renamed/edited files — leave any pre-existing unrelated working-tree changes, e.g. `matrix/matrix-viewer.html`, `questionnaire/questionnaire.html`, out.)

---

### Task 2: `check_no_legacy_token` guard

**Files:** `matrix/validate_data.py`, `tests/test_validate_data.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_validate_data.py`:
```python
def test_no_legacy_token_clean():
    cur = [{"uc_id": "UC-1", "current_state": "GAP"}]
    idc = [{"nhi_id": "NHI-1", "sources_likely": "x"}]
    assert vd.check_no_legacy_token(cur, idc) == []


def test_no_legacy_token_flags_old_headers():
    cur = [{"uc_id": "UC-1", "anz_state": "GAP"}]          # legacy column back
    idc = [{"nhi_id": "NHI-1", "sources_at_anz_likely": "x"}]
    errs = vd.check_no_legacy_token(cur, idc)
    assert any("anz_state" in e for e in errs)
    assert any("sources_at_anz_likely" in e for e in errs)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: FAIL — `AttributeError: ... 'check_no_legacy_token'`.

- [ ] **Step 3: Implement the guard + wire it into `validate_all`**

In `matrix/validate_data.py`, add after `validate_referential`:
```python
LEGACY_TOKENS = ("anz_state", "sources_at_anz_likely")


def check_no_legacy_token(current_state, identity):
    """Fail if a legacy ANZ-era header has crept back into the data."""
    errs = []
    cur_cols = set(current_state[0].keys()) if current_state else set()
    idc_cols = set(identity[0].keys()) if identity else set()
    if "anz_state" in cur_cols:
        errs.append("current-state.csv: legacy column 'anz_state' present (use 'current_state')")
    if "sources_at_anz_likely" in idc_cols:
        errs.append("identity-catalog.csv: legacy column 'sources_at_anz_likely' present (use 'sources_likely')")
    return errs
```
Then, inside `validate_all`, add this line just before `return errs` (after the `validate_referential` call):
```python
    errs += check_no_legacy_token(current, identity)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: PASS (16 validator tests). Also run `python3 matrix/validate_data.py; echo $?` → exit 0 (real data has the new headers).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/validate_data.py tests/test_validate_data.py
git commit -m "feat(ws5): guard against legacy anz_state/sources_at_anz headers returning

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: ADR-016 + backlog + final gate

**Files:** `docs/adr/ADR-016-anz-schema-rename.md`, `meta/IMPROVEMENT-BACKLOG.md`

- [ ] **Step 1: Write ADR-016**

Create `docs/adr/ADR-016-anz-schema-rename.md` in the `docs/adr/ADR-011-report-adapter.md` style. Required content:
- **Status:** Accepted. **Date:** 2026-06-02.
- **Context:** The data schema hardcoded the legacy ANZ client (`anz_state`, `anz-current-state.csv`, `sources_at_anz_likely`) — a coupling that undermined the "reusable instrument for any client" vision. WS-5c added a validator (the safety net); 5b removes the coupling.
- **Decision:** Rename the three schema tokens to client-generic names (`current_state`, `current-state.csv`, `sources_likely`) across code, active data, and tests in lockstep. Scope limited to the data schema — cosmetic internal vars (`XYZ` JS array, `anz` py var) and the user-facing "XYZ" client branding are left as-is (the branding is legitimate per-engagement content; the vars collide with it and carry no reuse benefit). A `check_no_legacy_token` guard prevents regression. Historical docs, `dist/`, and `.planning/` are untouched as the record of the real ANZ engagement.
- **Alternatives rejected:** renaming the cosmetic `XYZ`/`anz` variables too (risk amid branding, no reuse gain); renaming historical docs/ADR-005/prompts (rewrites the engagement record); a back-compat alias column (YAGNI — the rename is atomic and tested).
- **Consequences:** the engine no longer names a client in its schema (multi-client unblock); `dist/` retains the old `anz-current-state.csv` (frozen artifact); the report's "XYZ" branding remains until engine-generalization (WS-0); the monolith split (5d) is the remaining WS-5 slice.

- [ ] **Step 2: Update the backlog**

In `meta/IMPROVEMENT-BACKLOG.md`, under the WS-5 section, add beneath the slice-1 block:
```
**Slice 2 (5b) — ✅ DONE (2026-06-02, branch ws5-anz-rename):** legacy schema tokens renamed client-generic
— `anz_state`→`current_state`, `anz-current-state.csv`→`current-state.csv`, `sources_at_anz_likely`→`sources_likely`
— across code/data/tests in lockstep; `check_no_legacy_token` guard added. Historical docs/dist/sketches and the
"XYZ" client branding left as-is. ADR-016. 104 tests green; validator clean. **Remaining:** 5d monolith split.
```

- [ ] **Step 3: Final gate**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q 2>&1 | tail -2
python3 matrix/validate_data.py >/dev/null; echo "validator exit: $?"
grep -nE "TBD|TODO|FIXME" docs/adr/ADR-016-anz-schema-rename.md || echo "OK no placeholders"
ls docs/adr/ADR-01{4,5,6}-*.md
```
Expected: full suite green (104 + the new guard tests = 106); validator exit 0; `OK no placeholders`; ADR-016 listed.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add docs/adr/ADR-016-anz-schema-rename.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws5): ADR-016 + mark anz schema rename slice done in backlog

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria

- `matrix/current-state.csv` (renamed, `current_state` header); `identity-catalog.csv` has `sources_likely`.
- All code/test readers use the new tokens; cosmetic vars + XYZ branding untouched.
- Residual-token scan over code/data/tests is empty; all three builds succeed.
- `check_no_legacy_token` guard + tests; full suite green; validator exit 0.
- ADR-016 + backlog updated. All commits on `ws5-anz-rename`.

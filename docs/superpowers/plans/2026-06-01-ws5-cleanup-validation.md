# WS-5 Cleanup + CSV Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Archive stale files (5a) and add `matrix/validate_data.py` — the project's first CSV schema + referential-integrity validator over the core 4 contracts + all vendor CSVs (5c).

**Architecture:** A read-only stdlib validator mirroring `methodology/validate_rubric.py`: pure check functions return lists of violation strings (empty = clean); `validate_all(root)` aggregates; a CLI exits 1 on any violation. Not wired into builds. `matrix/` stays a non-package; tests load the module via a `sys.path` insert.

**Tech Stack:** Python 3 stdlib (`csv`, `glob`, `os`, `argparse`); pytest. Repo root `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`.

**Verified data facts (the validator MUST NOT false-positive on these):**
- use-cases & current-state both 47 rows, identical `uc_id` set; identity-catalog 37 `nhi_id`s.
- `anz_state` real values: GAP/PARTIAL/PENDING (enum is a superset incl. MET/NA). `framework_role`: PRIMARY-LENS/BACK-MAP/ADVERSARY-LENS.
- **Intentional sentinels** `MISSING-UC`/`MISSING-NHI` appear in 3 `regulatory-trace.csv` rows (E8-MAC, E8-RAP-NHI-GAP, ISM-0039) — allowlisted, skipped in referential checks.
- vendor schema: `target_type` ∈ {NHI, UC-F, UC-N}; `maturity` ranges **0–4** (validate 0–5); `coverage` values NATIVE/PARTNER/ADD-ON/GAP/N-A (all non-empty). 19 per-vendor files + 1 aggregate `vendor-capabilities.csv`; all per-vendor headers match the aggregate; 893 UC-* vendor targets all resolve; 0 dangling NHI targets.
- The real data validates **clean** under the checks below (verified by probe) — the integration test asserts zero violations.

---

### Task 1: 5a — cleanup (remove stale file + archive checkpoints)

**Files:**
- Delete: `GEMINI.md`
- Move: `research/vendors/_checkpoint-*.md` (12 files) → `research/vendors/_archive/`

- [ ] **Step 1: Remove the stale file and archive the checkpoints**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git rm GEMINI.md
mkdir -p research/vendors/_archive
git mv research/vendors/_checkpoint-*.md research/vendors/_archive/
```

- [ ] **Step 2: Verify**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
test ! -e GEMINI.md && echo "OK GEMINI.md gone" || echo "STILL PRESENT"
ls research/vendors/_checkpoint-*.md 2>/dev/null && echo "STILL IN PLACE" || echo "OK none left at source"
echo "archived: $(ls research/vendors/_archive/_checkpoint-*.md | wc -l | tr -d ' ') files"
python3 -m pytest -q 2>&1 | tail -1
```
Expected: `OK GEMINI.md gone`; `OK none left at source`; `archived: 12 files`; suite still green (90).

- [ ] **Step 3: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add -A
git commit -m "chore(ws5): remove stale GEMINI.md; archive vendor research checkpoints

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: validate_data.py — structural checks (columns, uniqueness, enums)

**Files:**
- Create: `matrix/validate_data.py`
- Create: `tests/test_validate_data.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_validate_data.py`:
```python
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import validate_data as vd


def test_required_columns_flags_missing():
    rows = [{"uc_id": "UC-1", "category": "F"}]   # missing most cols
    errs = vd.check_required_columns("use-cases.csv", rows, vd.CORE_REQUIRED["use-cases.csv"])
    assert any("short_title" in e for e in errs)
    assert all("use-cases.csv" in e for e in errs)


def test_required_columns_empty():
    assert vd.check_required_columns("x.csv", [], ("a",)) == ["x.csv: empty (no data rows)"]


def test_required_columns_clean():
    rows = [{c: "v" for c in vd.CORE_REQUIRED["identity-catalog.csv"]}]
    assert vd.check_required_columns("identity-catalog.csv", rows, vd.CORE_REQUIRED["identity-catalog.csv"]) == []


def test_unique_flags_duplicate():
    rows = [{"uc_id": "UC-1"}, {"uc_id": "UC-1"}]
    assert vd.check_unique("use-cases.csv", rows, "uc_id") == ["use-cases.csv: duplicate uc_id 'UC-1'"]


def test_enum_flags_invalid_and_allows_blank():
    rows = [{"anz_state": "GAP"}, {"anz_state": "BOGUS"}, {"anz_state": ""}]
    errs = vd.check_enum("anz-current-state.csv", rows, "anz_state", vd.VALID_STATES)
    assert errs == ["anz-current-state.csv: invalid anz_state 'BOGUS'"]


def test_ids_drops_blanks_and_sentinels():
    assert vd._ids("UC-1;;MISSING-UC;UC-2") == ["UC-1", "UC-2"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_validate_data.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'validate_data'`.

- [ ] **Step 3: Write the module head + structural checks**

Create `matrix/validate_data.py`:
```python
#!/usr/bin/env python3
"""Read-only CSV schema + referential-integrity validator for the matrix data contracts.

Pure check functions return lists of violation strings (empty = clean); validate_all
aggregates; the CLI exits 1 on any violation. Mirrors methodology/validate_rubric.py.
Read-only — never mutates data.

CLI: python3 matrix/validate_data.py [--root .]
"""
import argparse
import csv
import glob
import os
import sys

CORE_REQUIRED = {
    "use-cases.csv": ("uc_id", "category", "short_title", "story", "acceptance_criteria",
                      "nhis_in_scope", "outcome_lens", "backmap_codes", "priority_fi", "citation_keys"),
    "anz-current-state.csv": ("uc_id", "anz_state", "confidence", "evidence_q_ids",
                              "evidence_redacted", "gap_notes", "sensitivity_tag", "citation_keys"),
    "regulatory-trace.csv": ("framework_slug", "framework_role", "control_code", "control_short_title",
                             "uc_ids", "nhi_ids", "maturity_level", "evidence_url", "evidence_quote",
                             "citation_keys"),
    "identity-catalog.csv": ("nhi_id", "bucket", "short_name", "description", "typical_secrets",
                             "lifecycle", "governance_maturity", "sources_at_anz_likely", "citation_keys"),
}
VENDOR_REQUIRED = ("vendor_slug", "vendor_name", "target_id", "target_type", "coverage",
                   "maturity", "evidence_url", "evidence_quote", "citation_keys", "notes")
VALID_STATES = {"MET", "PARTIAL", "GAP", "PENDING", "NA"}
VALID_ROLES = {"PRIMARY-LENS", "BACK-MAP", "ADVERSARY-LENS"}
SENTINELS = {"MISSING-UC", "MISSING-NHI"}


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ids(value):
    """Split a ;-list, dropping blanks and intentional sentinels."""
    return [t.strip() for t in (value or "").split(";")
            if t.strip() and t.strip() not in SENTINELS]


def check_required_columns(name, rows, required):
    if not rows:
        return [f"{name}: empty (no data rows)"]
    have = set(rows[0].keys())
    return [f"{name}: missing required column '{c}'" for c in required if c not in have]


def check_unique(name, rows, key):
    seen, errs = set(), []
    for r in rows:
        v = r.get(key, "")
        if v in seen:
            errs.append(f"{name}: duplicate {key} '{v}'")
        seen.add(v)
    return errs


def check_enum(name, rows, col, allowed):
    errs = []
    for r in rows:
        v = (r.get(col) or "").strip()
        if v and v not in allowed:
            errs.append(f"{name}: invalid {col} '{v}'")
    return errs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/validate_data.py tests/test_validate_data.py
git commit -m "feat(ws5): CSV validator structural checks (columns, unique, enum)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Referential integrity + vendor row checks

**Files:**
- Modify: `matrix/validate_data.py` (add `validate_vendor_rows`, `validate_referential`)
- Modify: `tests/test_validate_data.py` (add tests)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_validate_data.py`:
```python
def test_vendor_rows_flags_maturity_and_coverage():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"target_id": "NHI-1", "maturity": "9", "coverage": ""})
    errs = vd.validate_vendor_rows("v.csv", rows)
    assert any("maturity '9'" in e for e in errs)
    assert any("empty coverage" in e for e in errs)


def test_vendor_rows_accepts_zero_maturity():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"maturity": "0", "coverage": "GAP"})
    assert vd.validate_vendor_rows("v.csv", rows) == []


def test_vendor_rows_single_slug():
    rows = [dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="a", maturity="1", coverage="NATIVE"),
            dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="b", maturity="1", coverage="NATIVE")]
    assert any("multiple vendor_slug" in e for e in vd.validate_vendor_rows("v.csv", rows, single_slug=True))


def test_referential_clean():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-1"}]
    cs = [{"uc_id": "UC-F-1"}]
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-F-1;MISSING-UC", "nhi_ids": "NHI-1;MISSING-NHI"}]
    vendors = [("v.csv", [{"target_type": "UC-F", "target_id": "UC-F-1"},
                          {"target_type": "NHI", "target_id": "NHI-1"}])]
    assert vd.validate_referential(uc, cs, rt, idc, vendors) == []


def test_referential_catches_dangling():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-9"}]   # NHI-9 missing
    cs = [{"uc_id": "UC-F-2"}]                              # not in use-cases
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-X", "nhi_ids": "NHI-Y"}]
    vendors = [("v.csv", [{"target_type": "NHI", "target_id": "NHI-Z"}])]
    errs = vd.validate_referential(uc, cs, rt, idc, vendors)
    assert any("NHI-9" in e for e in errs)
    assert any("UC-F-2" in e for e in errs)
    assert any("UC-X" in e for e in errs)
    assert any("NHI-Y" in e for e in errs)
    assert any("NHI-Z" in e for e in errs)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: FAIL — `AttributeError: module 'validate_data' has no attribute 'validate_vendor_rows'`.

- [ ] **Step 3: Implement the checks**

Append to `matrix/validate_data.py` (after `check_enum`):
```python
def validate_vendor_rows(name, rows, single_slug=False):
    """Per-vendor / aggregate row checks: required cols, maturity 0-5, non-empty coverage,
    and (per-vendor only) a single consistent vendor_slug."""
    errs = check_required_columns(name, rows, VENDOR_REQUIRED)
    if errs:
        return errs   # missing columns -> key access below is unsafe
    slugs = set()
    for r in rows:
        tid = r.get("target_id", "?")
        m = (r.get("maturity") or "").strip()
        if not (m.isdigit() and 0 <= int(m) <= 5):
            errs.append(f"{name}: maturity '{m}' not integer 0-5 (target {tid})")
        if not (r.get("coverage") or "").strip():
            errs.append(f"{name}: empty coverage (target {tid})")
        slugs.add((r.get("vendor_slug") or "").strip())
    if single_slug and len(slugs) > 1:
        errs.append(f"{name}: multiple vendor_slug values {sorted(slugs)} in one per-vendor file")
    return errs


def validate_referential(use_cases, current_state, reg_trace, identity, vendor_files):
    """Cross-file integrity: uc_id / nhi_id references resolve (sentinels skipped)."""
    errs = []
    uc_ids = {r.get("uc_id", "") for r in use_cases}
    nhi_ids = {r.get("nhi_id", "") for r in identity}
    cs_ids = {r.get("uc_id", "") for r in current_state}
    for i in sorted(cs_ids - uc_ids):
        errs.append(f"anz-current-state.csv: uc_id '{i}' not in use-cases")
    for i in sorted(uc_ids - cs_ids):
        errs.append(f"anz-current-state.csv: missing uc_id '{i}' present in use-cases")
    for r in reg_trace:
        cc = r.get("control_code", "?")
        for u in _ids(r.get("uc_ids")):
            if u not in uc_ids:
                errs.append(f"regulatory-trace.csv: uc_id '{u}' (control {cc}) not in use-cases")
        for n in _ids(r.get("nhi_ids")):
            if n not in nhi_ids:
                errs.append(f"regulatory-trace.csv: nhi_id '{n}' (control {cc}) not in identity-catalog")
    for r in use_cases:
        for n in _ids(r.get("nhis_in_scope")):
            if n not in nhi_ids:
                errs.append(f"use-cases.csv: nhis_in_scope '{n}' (uc {r.get('uc_id')}) not in identity-catalog")
    for name, rows in vendor_files:
        for r in rows:
            tt = (r.get("target_type") or "").strip()
            tid = (r.get("target_id") or "").strip()
            if tt == "NHI" and tid not in nhi_ids:
                errs.append(f"{name}: target_id '{tid}' (NHI) not in identity-catalog")
            elif tt.startswith("UC") and tid not in uc_ids:
                errs.append(f"{name}: target_id '{tid}' (UC) not in use-cases")
    return errs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: PASS (11 tests).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/validate_data.py tests/test_validate_data.py
git commit -m "feat(ws5): referential integrity + vendor row checks

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: validate_all aggregator + CLI + real-data integration

**Files:**
- Modify: `matrix/validate_data.py` (add `validate_all`, `main`)
- Modify: `tests/test_validate_data.py` (add integration + CLI tests)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_validate_data.py`:
```python
import shutil


def test_validate_all_real_data_is_clean():
    # The shipped data is the golden baseline — zero violations.
    assert vd.validate_all(str(ROOT)) == []


def test_main_exit_zero_on_clean():
    assert vd.main(["--root", str(ROOT)]) == 0


def test_validate_all_catches_injected_break(tmp_path):
    src = ROOT / "matrix"
    dst = tmp_path / "matrix"
    dst.mkdir()
    for p in src.glob("*.csv"):
        shutil.copy(p, dst / p.name)
    # inject a current-state row whose uc_id is not in use-cases
    cs = dst / "anz-current-state.csv"
    cs.write_text(cs.read_text() + "UC-ZZZ-999,GAP,MED,,,,,\n", encoding="utf-8")
    viol = vd.validate_all(str(tmp_path))
    assert any("UC-ZZZ-999" in v for v in viol)
    assert vd.main(["--root", str(tmp_path)]) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: FAIL — `AttributeError: ... 'validate_all'`.

- [ ] **Step 3: Implement `validate_all` + `main`**

Append to `matrix/validate_data.py`:
```python
def validate_all(root="."):
    """Run all checks against the matrix data under <root>/matrix; return all violations."""
    m = os.path.join(root, "matrix")
    use_cases = load_csv(os.path.join(m, "use-cases.csv"))
    current = load_csv(os.path.join(m, "anz-current-state.csv"))
    trace = load_csv(os.path.join(m, "regulatory-trace.csv"))
    identity = load_csv(os.path.join(m, "identity-catalog.csv"))

    errs = []
    errs += check_required_columns("use-cases.csv", use_cases, CORE_REQUIRED["use-cases.csv"])
    errs += check_unique("use-cases.csv", use_cases, "uc_id")
    errs += check_required_columns("anz-current-state.csv", current, CORE_REQUIRED["anz-current-state.csv"])
    errs += check_unique("anz-current-state.csv", current, "uc_id")
    errs += check_enum("anz-current-state.csv", current, "anz_state", VALID_STATES)
    errs += check_required_columns("regulatory-trace.csv", trace, CORE_REQUIRED["regulatory-trace.csv"])
    errs += check_enum("regulatory-trace.csv", trace, "framework_role", VALID_ROLES)
    errs += check_required_columns("identity-catalog.csv", identity, CORE_REQUIRED["identity-catalog.csv"])
    errs += check_unique("identity-catalog.csv", identity, "nhi_id")

    vendor_files = []
    agg_path = os.path.join(m, "vendor-capabilities.csv")
    agg_rows = load_csv(agg_path)
    vendor_files.append(("vendor-capabilities.csv", agg_rows))
    errs += validate_vendor_rows("vendor-capabilities.csv", agg_rows)
    for p in sorted(glob.glob(os.path.join(m, "vendor-capabilities-*.csv"))):
        name = os.path.basename(p)
        rows = load_csv(p)
        vendor_files.append((name, rows))
        errs += validate_vendor_rows(name, rows, single_slug=True)

    errs += validate_referential(use_cases, current, trace, identity, vendor_files)
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate the matrix CSV data contracts.")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args(argv)
    violations = validate_all(args.root)
    for v in violations:
        print(v)
    if violations:
        print(f"\n{len(violations)} violation(s) found.")
        return 1
    print("All CSV data contracts valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_validate_data.py -q`
Expected: PASS (14 tests). The real-data check returns `[]` (clean baseline); the injected break is caught; `main` exits 0 clean / 1 broken.

- [ ] **Step 5: Verify the CLI directly**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 matrix/validate_data.py; echo "exit: $?"
```
Expected: `All CSV data contracts valid.` and `exit: 0`.

- [ ] **Step 6: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/validate_data.py tests/test_validate_data.py
git commit -m "feat(ws5): validate_all aggregator + CLI; real data certified clean

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: ADR-015 + backlog + full-suite gate

**Files:**
- Create: `docs/adr/ADR-015-csv-validation.md`
- Modify: `meta/IMPROVEMENT-BACKLOG.md`

- [ ] **Step 1: Write ADR-015**

Create `docs/adr/ADR-015-csv-validation.md` in the `docs/adr/ADR-011-report-adapter.md` style. Required content:
- **Status:** Accepted. **Date:** 2026-06-01.
- **Context:** The data layer (core CSVs + 19 vendor CSVs) had zero guards; a dangling `uc_id`/`nhi_id` or a missing column would surface only as a downstream build/report bug. WS-5 slice 1 adds the first validator.
- **Decision:** A read-only `matrix/validate_data.py` (pure check functions → violation lists; `validate_all` aggregator; CLI exits 1) mirroring `validate_rubric.py`. Checks: required columns, uniqueness, same use-cases/current-state `uc_id` set, value enums (`anz_state`, `framework_role`, vendor `maturity` 0–5, non-empty `coverage`), and referential integrity (current-state/regulatory-trace `uc_ids`, regulatory-trace/use-cases `nhi_ids`, vendor `target_id` by `target_type`). Standalone + pytest; **not wired into builds** (keeps them byte-stable). `MISSING-UC`/`MISSING-NHI` are allowlisted intentional sentinels.
- **Alternatives rejected:** wiring validation into the builds (adds failure modes — deferred until a second client); a schema library/JSON-Schema (stdlib mirrors the existing `validate_rubric.py` precedent); hardcoding the vendor `coverage` enum (risk of false positives).
- **Consequences:** the shipped data is certified the golden baseline (the integration test fails if a future edit breaks a contract); the validator is importable so a build can call it later (5d / second client); the legacy `anz_state` column name is validated as-is and will be renamed in WS-5 slice 5b.

- [ ] **Step 2: Update the backlog**

In `meta/IMPROVEMENT-BACKLOG.md`, under the WS-5 section, mark slice 1 done (mirroring how earlier workstreams are marked). Add:
```
**Slice 1 — ✅ DONE (2026-06-01, branch ws5-cleanup-validation):** stale `GEMINI.md` removed; 12 vendor
research checkpoints archived to `research/vendors/_archive/`; `matrix/validate_data.py` added — first CSV
schema + referential-integrity validator (core 4 + aggregate + 19 vendor files), standalone CLI + pytest,
not wired into builds. Real data certified clean. ADR-015. **Next:** 5b legacy `anz` rename → 5d monolith split.
```

- [ ] **Step 3: Final gate**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q 2>&1 | tail -3
python3 matrix/validate_data.py; echo "validator exit: $?"
grep -nE "TBD|TODO|FIXME" docs/adr/ADR-015-csv-validation.md || echo "OK no placeholders"
ls docs/adr/ADR-01{3,4,5}-*.md
```
Expected: full suite green (90 + 14 new validator tests); validator exit 0; `OK no placeholders`; ADR-015 listed.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add docs/adr/ADR-015-csv-validation.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws5): ADR-015 + mark cleanup+validation slice done in backlog

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria (whole slice)

- `GEMINI.md` removed; 12 checkpoints under `research/vendors/_archive/`.
- `matrix/validate_data.py`: structural + enum + referential + vendor checks; `validate_all`; CLI exit codes.
- Real data validates clean (`validate_all(ROOT) == []`, CLI exit 0); an injected break is caught (exit 1).
- 14 new pytest tests; full suite green; ADR-015 + backlog updated.
- Sentinels (`MISSING-UC`/`MISSING-NHI`) allowlisted; maturity 0–5; `UC-*` target types handled — no false positives.
- All commits on `ws5-cleanup-validation`.

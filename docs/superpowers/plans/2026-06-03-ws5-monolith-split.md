# WS-5 Monolith Split Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline — this extraction needs whole-file context). Steps use checkbox (`- [ ]`) syntax.

**Goal:** Split `matrix/build_matrix_viewer.py` (949 lines) into `report_io.py` / `report_logic.py` / `report_render.py` + `report-template.html` + a thin orchestrator, with **byte-identical** report output.

**Architecture:** Pure structural extraction, no behavior change. A permanent HTML byte-snapshot test (captured FIRST) plus the existing `REGDATA`/`RECDATA` golden make every step provably output-preserving. Flat sibling modules in `matrix/` (same import mechanism as `engagement_config.py`/`overlay.py`: the script's dir is on `sys.path[0]`).

**Tech Stack:** Python 3 stdlib; pytest. Repo root `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`. Output verified deterministic (identical md5 across builds).

**Golden rule for every task:** after each change, the report HTML is byte-identical (snapshot test) AND `test_engine_integration` passes AND the full suite is green. If any diverges, the step is wrong — revert and retry.

---

### Task 1: Capture the byte-snapshot guard FIRST (before any refactor)

**Files:** Create `tests/fixtures/report.snapshot.html`, `tests/test_report_render.py`.

- [ ] **Step 1: Build the current report and freeze it as the fixture**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
(cd matrix && python3 build_matrix_viewer.py >/dev/null)
cp matrix/matrix-viewer.html tests/fixtures/report.snapshot.html
echo "frozen: $(wc -c < tests/fixtures/report.snapshot.html) bytes"
```

- [ ] **Step 2: Write the byte-snapshot test**

Create `tests/test_report_render.py`:
```python
import hashlib, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENGINE = ROOT / "matrix" / "build_matrix_viewer.py"
SNAPSHOT = ROOT / "tests" / "fixtures" / "report.snapshot.html"


def test_default_report_is_byte_identical(tmp_path):
    # Build the default report and compare to the frozen snapshot, byte-for-byte.
    subprocess.run([sys.executable, str(ENGINE)], cwd=ROOT, check=True,
                   capture_output=True)
    built = (ROOT / "matrix" / "matrix-viewer.html").read_bytes()
    frozen = SNAPSHOT.read_bytes()
    assert hashlib.md5(built).hexdigest() == hashlib.md5(frozen).hexdigest(), \
        "report HTML changed vs frozen snapshot"
```

- [ ] **Step 3: Run it (passes now — baseline)**

Run: `python3 -m pytest tests/test_report_render.py -q`
Expected: PASS (the snapshot equals the freshly-built report).

- [ ] **Step 4: Commit the guard**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add tests/fixtures/report.snapshot.html tests/test_report_render.py
git commit -m "test(ws5): freeze report HTML byte-snapshot before monolith split

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Extract `report-template.html` + `report_render.py`

**Files:** Create `matrix/report-template.html`, `matrix/report_render.py`; modify `matrix/build_matrix_viewer.py`.

- [ ] **Step 1: Extract the template verbatim**

In `matrix/build_matrix_viewer.py`, the `TEMPLATE = r"""..."""` assignment (the ~590-line raw string from `<!DOCTYPE html>` to the closing `</html>`) holds the template. Move its **exact contents** (everything between the `r"""` and the closing `"""`, unchanged — every `/*__TOKEN__*/` and `__RV__/__NHI__/__UC__`) into a new file `matrix/report-template.html`. Do not alter a single character.

- [ ] **Step 2: Create `report_render.py`**

Create `matrix/report_render.py`. It must reproduce the EXACT token-replacement chain currently in `build_matrix_viewer.py` (the `TEMPLATE.replace(...)` block) so output is byte-identical:
```python
"""Render the stakeholder report HTML from the model + report-template.html."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_template():
    with open(os.path.join(HERE, "report-template.html"), encoding="utf-8") as fh:
        return fh.read()


def render(model):
    """model keys: ranked, anz, ucs, nhis, glossary, layer_label, short, reg,
    regdata, recdata, meta. Returns the final HTML string (byte-identical to the
    legacy inline TEMPLATE assembly)."""
    return (load_template()
            .replace("/*__DATA__*/[]", json.dumps(model["ranked"], ensure_ascii=False))
            .replace("/*__XYZ__*/[]", json.dumps(model["anz"], ensure_ascii=False))
            .replace("/*__UCS__*/[]", json.dumps(model["ucs"], ensure_ascii=False))
            .replace("/*__NHIS__*/[]", json.dumps(model["nhis"], ensure_ascii=False))
            .replace("/*__GLOSSARY__*/{}", json.dumps(model["glossary"], ensure_ascii=False))
            .replace("/*__LAYERLABEL__*/{}", json.dumps(model["layer_label"], ensure_ascii=False))
            .replace("/*__SHORT__*/{}", json.dumps(model["short"], ensure_ascii=False))
            .replace("/*__REG__*/{}", json.dumps(model["reg"], ensure_ascii=False))
            .replace("/*__REGDATA__*/{}", json.dumps(model["regdata"], ensure_ascii=False))
            .replace("/*__RECDATA__*/{}", json.dumps(model["recdata"], ensure_ascii=False))
            .replace("/*__META__*/{}", json.dumps(model["meta"], ensure_ascii=False))
            .replace("__RV__", str(model["meta"]["ranked_vendors"]))
            .replace("__NHI__", str(model["meta"]["nhis"]))
            .replace("__UC__", str(model["meta"]["ucs"])))
```

- [ ] **Step 3: Wire the orchestrator to use it**

In `matrix/build_matrix_viewer.py`: delete the `TEMPLATE = r"""..."""` block and the inline `html = (TEMPLATE.replace(...))` chain. Add `import report_render` near the other sibling imports, and replace the assembly with:
```python
html = report_render.render({
    "ranked": ranked, "anz": anz, "ucs": ucs, "nhis": nhis,
    "glossary": GLOSSARY, "layer_label": LAYER_LABEL, "short": SHORT,
    "reg": REG, "regdata": REGDATA, "recdata": RECDATA, "meta": meta,
})
```
(Variable names `ranked, anz, ucs, nhis, GLOSSARY, LAYER_LABEL, SHORT, REG, REGDATA, RECDATA, meta` are the existing module-level names — unchanged.)

- [ ] **Step 4: Verify byte-identical + suite**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest tests/test_report_render.py tests/test_engine_integration.py -q
python3 -m pytest -q 2>&1 | tail -2
```
Expected: byte-snapshot passes (HTML unchanged); engine golden passes; full suite green. If the snapshot fails, the template extraction altered a character — diff and fix.

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/report-template.html matrix/report_render.py matrix/build_matrix_viewer.py
git commit -m "refactor(ws5): extract report-template.html + report_render (byte-identical)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Extract `report_io.py`

**Files:** Create `matrix/report_io.py`; modify `matrix/build_matrix_viewer.py`.

- [ ] **Step 1: Move loading + static vendor maps into `report_io.py`**

Create `matrix/report_io.py` containing, moved verbatim from the orchestrator: the `read_csv` helper (re-parameterised to take the matrix dir), the static maps `VENDOR_LAYER`, `SHORT`, `LAYER_LABEL`, `SUBSTRATE_SLUG`, the `VENDOR_RESIDENCY`/`FRAMEWORK_LABELS` config loads (via `overlay`), and a `load_inputs(here, current_state_name)` that returns the existing structures. Exact interface:
```python
"""Report input loading: CSVs + static vendor maps + config-driven labels."""
import csv
import os
import overlay as _ov

SUBSTRATE_SLUG = "fortanix-dsm"
VENDOR_LAYER = { ... }      # moved verbatim from build_matrix_viewer.py
SHORT = { ... }             # moved verbatim
LAYER_LABEL = { ... }       # moved verbatim


def read_csv(here, name):
    path = os.path.join(here, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_vendor_residency(cfgdir):
    return _ov.load_vendor_residency(os.path.join(cfgdir, "vendor-residency.yaml"))


def load_framework_labels(cfgdir):
    return _ov.load_framework_labels(os.path.join(cfgdir, "frameworks.yaml"))


def load_inputs(here, current_state_name):
    """Returns a dict: all_rows, ranked, ucs, nhis, current, reg_rows."""
    all_rows = read_csv(here, "vendor-capabilities.csv")
    # ... the ranked/ucs/nhis/current/reg_rows construction moved verbatim from
    # build_matrix_viewer.py lines ~104-139 (using read_csv(here, ...)), returning the dict.
    return {"all_rows": all_rows, "ranked": ranked, "ucs": ucs, "nhis": nhis,
            "current": current, "reg_rows": reg_rows}
```
Keep the `sys.exit("No rows ...")`/`Unmapped vendor_slug` guards inside `load_inputs` (same messages).

- [ ] **Step 2: Wire the orchestrator**

In `build_matrix_viewer.py`: `import report_io`; replace the inline loading block + the `VENDOR_LAYER/SHORT/LAYER_LABEL/SUBSTRATE_SLUG/VENDOR_RESIDENCY/FRAMEWORK_LABELS/read_csv` definitions with calls into `report_io`. Bind the returned structures to the same local names (`all_rows, ranked, ucs, nhis, anz, reg_rows`, where `anz = inputs["current"]`-derived list exactly as before; note the legacy local variable is named `anz` — keep it) and `VENDOR_LAYER = report_io.VENDOR_LAYER`, etc., so downstream logic is untouched.

- [ ] **Step 3: Verify byte-identical + suite**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest tests/test_report_render.py tests/test_engine_integration.py -q
python3 -m pytest -q 2>&1 | tail -2
```
Expected: snapshot + golden + full suite green.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/report_io.py matrix/build_matrix_viewer.py
git commit -m "refactor(ws5): extract report_io (CSV loading + vendor maps)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Extract `report_logic.py`

**Files:** Create `matrix/report_logic.py`; modify `matrix/build_matrix_viewer.py`.

- [ ] **Step 1: Move the model transforms into `report_logic.py`**

Create `matrix/report_logic.py` with the transform code moved verbatim (parameterised, no I/O). Functions:
```python
"""Pure model transforms for the report (no I/O)."""
from collections import defaultdict

APRA_FRAMEWORKS = {"apra-cps-234", "apra-cps-230", "apra-cpg-234"}
STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "MET": 3, "UNKNOWN": 9}
ORDER = {"NATIVE": 0, "ADD-ON": 1, "PARTNER": 2, "GAP": 3, "N/A": 4}
REC_UC_DOMAIN = { ... }     # moved verbatim from build_matrix_viewer.py


def build_glossary(nhis, ucs):
    ...    # moved verbatim from build_glossary()


def compute_meta(all_rows, ranked, nhis, ucs):
    ...    # the meta = {...} dict, moved verbatim


def build_regdata(inputs, anz, engagement, framework_labels, available):
    ...    # reg/REG/framework_controls/state_by_uc/STATE_RANK rollup/uc_index/REGDATA, verbatim


def build_recdata(inputs, ranked, vendor_layer, vendor_residency, short, engagement, nhis):
    ...    # _vendor_stat + layer sorts + top_picks + complementary + RECDATA, verbatim
```
Signatures may be adjusted during execution to thread exactly the data each block uses — the constraint is that the returned `REGDATA`/`RECDATA`/`GLOSSARY`/`meta` are identical to today (the goldens enforce this).

- [ ] **Step 2: Wire the orchestrator**

In `build_matrix_viewer.py`: `import report_logic`; replace the inline transform blocks with calls producing the same `REGDATA`, `RECDATA`, `GLOSSARY`, `meta` locals. Keep `ENGAGEMENT` resolution (via `engagement_config`/`overlay`) in the orchestrator and pass it in.

- [ ] **Step 3: Verify byte-identical + suite**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest tests/test_report_render.py tests/test_engine_integration.py -q
python3 -m pytest -q 2>&1 | tail -2
```
Expected: snapshot + golden + full suite green.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add matrix/report_logic.py matrix/build_matrix_viewer.py
git commit -m "refactor(ws5): extract report_logic (REGDATA/RECDATA/glossary/meta transforms)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Confirm orchestrator is thin + add report_logic unit tests

**Files:** Create `tests/test_report_logic.py`; (optionally tidy) `matrix/build_matrix_viewer.py`.

- [ ] **Step 1: Confirm the orchestrator shrank**

Run: `wc -l matrix/build_matrix_viewer.py`
Expected: well under ~250 lines (CLI + ENGAGEMENT resolution + orchestration only — the ~590-line template, the loading block, and the transforms are now in their modules).

- [ ] **Step 2: Write targeted `report_logic` unit tests**

Create `tests/test_report_logic.py`:
```python
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import report_logic as rl


def test_build_glossary_truncates_long_description():
    long = "x" * 200
    nhis = [{"nhi_id": "NHI-1", "short_name": "Svc", "description": long}]
    g = rl.build_glossary(nhis, [])
    assert g["NHI-1"].startswith("Svc — ")
    assert g["NHI-1"].endswith("...")
    assert len(g["NHI-1"]) < len("Svc — ") + 200


def test_build_glossary_includes_uc_titles_and_legend():
    g = rl.build_glossary([], [{"uc_id": "UC-F-001", "short_title": "Prevent secrets"}])
    assert g["UC-F-001"] == "Prevent secrets"
    assert g["NATIVE"].startswith("Vendor's first-class")


def test_compute_meta_counts():
    m = rl.compute_meta(all_rows=[{"vendor_slug": "a"}, {"vendor_slug": "a"}],
                        ranked=[{"vendor_slug": "a"}], nhis=[{}, {}], ucs=[{}])
    assert m["nhis"] == 2 and m["ucs"] == 1 and m["total_rows"] == 2
```
(If a signature differs from the implemented one, align the test to the real signature — the behaviours asserted are fixed: >170-char truncation with `...`, UC titles present, legend keys present, correct counts.)

- [ ] **Step 3: Run + full gate**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q 2>&1 | tail -2
python3 matrix/validate_data.py >/dev/null; echo "validator exit: $?"
```
Expected: full suite green (106 + byte-snapshot + 3 logic tests); validator exit 0.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add tests/test_report_logic.py matrix/build_matrix_viewer.py
git commit -m "test(ws5): unit tests for extracted report_logic; thin orchestrator

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: ADR-017 + backlog (WS-5 complete)

**Files:** Create `docs/adr/ADR-017-report-modularization.md`; modify `meta/IMPROVEMENT-BACKLOG.md`.

- [ ] **Step 1: Write ADR-017**

Create `docs/adr/ADR-017-report-modularization.md` (ADR-011 style):
- **Status:** Accepted. **Date:** 2026-06-03.
- **Context:** `build_matrix_viewer.py` had grown to 949 lines mixing CSV loading, model transforms, a 590-line inline HTML template, and orchestration — hard to navigate and untestable in parts.
- **Decision:** Split into flat siblings `report_io.py` (loading + vendor maps), `report_logic.py` (pure REGDATA/RECDATA/glossary/meta transforms), `report_render.py` + `report-template.html` (templating), and a thin `build_matrix_viewer.py` orchestrator + CLI. Pure structural extraction — no output change, enforced by a permanent HTML byte-snapshot test plus the existing REGDATA/RECDATA golden.
- **Alternatives rejected:** keeping the template as a Python string (a separate `.html` matches `build_questionnaire`'s pattern and is diffable); a `matrix` package with `__init__.py` (flat siblings match the existing `engagement_config`/`overlay` convention and avoid touching the run/build mechanics).
- **Consequences:** the report logic is now unit-testable in isolation; the template is editable without touching Python; WS-5 is complete; the byte-snapshot guards the deliverable against future drift.

- [ ] **Step 2: Mark WS-5 complete in the backlog**

In `meta/IMPROVEMENT-BACKLOG.md`, under WS-5, add beneath the slice-2 block:
```
**Slice 3 (5d) — ✅ DONE (2026-06-03, branch ws5-monolith-split):** the 949-line `build_matrix_viewer.py`
split into `report_io.py` / `report_logic.py` / `report_render.py` + `report-template.html` + a thin
orchestrator. Byte-identical output (permanent HTML snapshot test + REGDATA/RECDATA golden); report_logic
now unit-tested. ADR-017. **WS-5 COMPLETE** — cleanup + validation (5a/5c) → anz rename (5b) → modularization (5d).
```
Also append ` — ✅ COMPLETE` to the `### WS-5 …` heading.

- [ ] **Step 3: Final gate**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 -m pytest -q 2>&1 | tail -2
grep -nE "TBD|TODO|FIXME" docs/adr/ADR-017-report-modularization.md || echo "OK no placeholders"
ls docs/adr/ADR-01{5,6,7}-*.md
wc -l matrix/build_matrix_viewer.py matrix/report_io.py matrix/report_logic.py matrix/report_render.py
```
Expected: full suite green; `OK no placeholders`; ADR-017 listed; the orchestrator is small and the modules are focused.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add docs/adr/ADR-017-report-modularization.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws5): ADR-017 + mark WS-5 complete (report modularization)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria

- `report_io.py` / `report_logic.py` / `report_render.py` / `report-template.html` created; `build_matrix_viewer.py` reduced to a thin orchestrator + CLI.
- Report HTML byte-identical at every step (snapshot test); `REGDATA`/`RECDATA` golden unchanged; all 6 engine tests pass.
- `report_logic` unit-tested; full suite green; validator exit 0.
- ADR-017 + backlog mark **WS-5 complete**. All commits on `ws5-monolith-split`.

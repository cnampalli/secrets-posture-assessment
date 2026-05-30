# WS-4 Roadmap Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `questionnaire/roadmap_generator.py` — a pure transform + CLI that reads an `assessment-record.json` and emits a prioritised `engagement-menu/v1` JSON applying the playbook's risk × effort method.

**Architecture:** Mirror `report_adapter.py` (pure functions + thin CLI). Extract the state-resolution rule into a shared `questionnaire/record_state.py` so the menu's GAP/PARTIAL filter can never disagree with the report. Risk seeds from `use-cases.csv.priority_fi` (overridable), effort from a per-engagement CSV (default Med), quadrant from risk×effort, regulatory driver scoped to the financial preset (MITRE excluded, capped one-per-framework/max 3, regulator-first), regulation as an ordering tie-breaker only.

**Tech Stack:** Python 3 stdlib (`argparse`, `csv`, `json`, `os`) + PyYAML 6 (already available) for preset scope. pytest. All paths relative to repo root `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`.

**Verified data facts (cite/rely on these):**
- `record["responses"][uc]` keys: `archetype, answers, proposed_state, final_state, overridden, rationale, confidence`. State resolution = `final_state or proposed_state or "PENDING"`.
- `use-cases.csv` cols include `uc_id, short_title, priority_fi`. priority_fi values: P0 (12), P1 (26), P2 (9), no blanks.
- `regulatory-trace.csv` cols: `framework_slug, framework_role, control_code, control_short_title, uc_ids(;-sep), ...`. Roles: `BACK-MAP` (apra-cps-234/230, apra-cpg-234, asd-ism), `PRIMARY-LENS` (essential-8, cisa-ztmm-v2), `ADVERSARY-LENS` (mitre-attack).
- `matrix/config/presets/financial.yaml`: `primary: [apra-cps-234, apra-cps-230, apra-cpg-234]`, `overlays: [cisa-ztmm-v2]`, `baseline: [essential-8]`.
- XYZ data: 11 GAP + 16 PARTIAL = 27 engagement findings in `matrix/anz-current-state.csv` (but the generator reads a *record*, not this CSV — the dogfood builds a record-shaped fixture or uses an exported record).

---

### Task 1: Shared state resolver + adapter refactor

**Files:**
- Create: `questionnaire/record_state.py`
- Create: `tests/test_record_state.py`
- Modify: `questionnaire/report_adapter.py` (imports + the inline state expr)

- [ ] **Step 1: Write the failing test**

Create `tests/test_record_state.py`:
```python
import questionnaire.record_state as rs


def test_resolve_prefers_final():
    assert rs.resolve_state({"final_state": "GAP", "proposed_state": "PARTIAL"}) == "GAP"


def test_resolve_falls_back_to_proposed():
    assert rs.resolve_state({"final_state": None, "proposed_state": "MET"}) == "MET"


def test_resolve_defaults_pending():
    assert rs.resolve_state({"final_state": None, "proposed_state": None}) == "PENDING"
    assert rs.resolve_state({}) == "PENDING"
    assert rs.resolve_state(None) == "PENDING"


def test_schema_constant():
    assert rs.SCHEMA == "posture-assessment-record/v1"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_record_state.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'questionnaire.record_state'`.

- [ ] **Step 3: Write the module**

Create `questionnaire/record_state.py`:
```python
"""Shared assessment-record helpers (used by report_adapter and roadmap_generator)."""

SCHEMA = "posture-assessment-record/v1"


def resolve_state(response):
    """Effective state of a response: final_state -> proposed_state -> 'PENDING'."""
    response = response or {}
    return response.get("final_state") or response.get("proposed_state") or "PENDING"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_record_state.py -q`
Expected: PASS (4 tests).

- [ ] **Step 5: Refactor the adapter to use the shared resolver (behaviour-preserving)**

In `questionnaire/report_adapter.py`:
- Replace the line `SCHEMA = "posture-assessment-record/v1"` with an import. Change the import block so it reads:
```python
import argparse
import csv
import json
import sys

from questionnaire.record_state import SCHEMA, resolve_state
```
- In `record_to_rows`, replace:
```python
            "anz_state": r.get("final_state") or r.get("proposed_state") or "PENDING",
```
with:
```python
            "anz_state": resolve_state(r),
```

- [ ] **Step 6: Run the adapter tests to verify no regression**

Run: `python3 -m pytest tests/test_report_adapter.py tests/test_record_state.py -q`
Expected: PASS (all adapter tests + 4 new — the schema/fallback/pending behaviours are unchanged).

- [ ] **Step 7: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/record_state.py tests/test_record_state.py questionnaire/report_adapter.py
git commit -m "refactor(ws4): extract shared resolve_state; adapter reuses it

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Banding helpers — risk seed + quadrant

**Files:**
- Create: `questionnaire/roadmap_generator.py` (start the module)
- Create: `tests/test_roadmap_generator.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_roadmap_generator.py`:
```python
import questionnaire.roadmap_generator as rg


def test_seed_risk_mapping():
    assert rg.seed_risk("P0") == "High"
    assert rg.seed_risk("P1") == "Med"
    assert rg.seed_risk("P2") == "Low"
    assert rg.seed_risk("") == "Low"
    assert rg.seed_risk(None) == "Low"
    assert rg.seed_risk("weird") == "Low"


def test_quadrant_corners():
    assert rg.quadrant("High", "Low") == "Quick wins"
    assert rg.quadrant("High", "High") == "Major projects"
    assert rg.quadrant("Low", "Low") == "Fill-ins"
    assert rg.quadrant("Low", "High") == "Hard slogs"


def test_quadrant_med_bands():
    # Med risk counts as the high side; Med effort counts as the low (actionable) side.
    assert rg.quadrant("Med", "Med") == "Quick wins"
    assert rg.quadrant("Med", "High") == "Major projects"
    assert rg.quadrant("Low", "Med") == "Fill-ins"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'questionnaire.roadmap_generator'`.

- [ ] **Step 3: Write the module head + helpers**

Create `questionnaire/roadmap_generator.py`:
```python
#!/usr/bin/env python3
"""Generate a prioritised engagement-menu JSON from an assessment-record.json.

Applies the WS-4 playbook's risk x effort prioritisation method:
- risk seeded from use-cases.csv priority_fi (overridable per engagement)
- effort from a per-engagement CSV (default Med)
- quadrant from risk x effort
- regulatory driver scoped to a framework set (financial preset default), MITRE
  excluded, capped at one control per framework (max 3), regulator-first
- regulation is an ordering tie-breaker only (no automatic band escalation)

CLI: python3 -m questionnaire.roadmap_generator <record.json> -o engagement-menu.json \
        [--engagement engagement.csv] [--frameworks slug,slug] [--preset financial]
"""
import argparse
import csv
import json
import os
import sys

from questionnaire.record_state import SCHEMA, resolve_state

OUTPUT_SCHEMA = "engagement-menu/v1"
ENGAGEMENT_STATES = ("GAP", "PARTIAL")
_RISK_BY_PRIORITY = {"P0": "High", "P1": "Med"}          # anything else -> Low
_QUADRANT_ORDER = {"Quick wins": 0, "Major projects": 1, "Fill-ins": 2, "Hard slogs": 3}
_RISK_ORDER = {"High": 0, "Med": 1, "Low": 2}
_ROLE_ORDER = {"BACK-MAP": 0, "PRIMARY-LENS": 1}         # regulator first; ADVERSARY-LENS excluded


class RoadmapError(Exception):
    pass


def seed_risk(priority_fi):
    """Map a use-case's priority_fi to a default risk band (P0->High, P1->Med, else Low)."""
    return _RISK_BY_PRIORITY.get((priority_fi or "").strip(), "Low")


def quadrant(risk, effort):
    """Risk x effort -> one of the four engagement quadrants."""
    risk_high = risk in ("High", "Med")
    effort_high = effort == "High"
    if risk_high and not effort_high:
        return "Quick wins"
    if risk_high and effort_high:
        return "Major projects"
    if not risk_high and not effort_high:
        return "Fill-ins"
    return "Hard slogs"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/roadmap_generator.py tests/test_roadmap_generator.py
git commit -m "feat(ws4): roadmap generator banding helpers (risk seed + quadrant)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Regulatory driver derivation

**Files:**
- Modify: `questionnaire/roadmap_generator.py` (add `regulatory_driver`)
- Modify: `tests/test_roadmap_generator.py` (add tests)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_roadmap_generator.py`:
```python
TRACE = [
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP",
     "control_code": "CPS234-§35b", "control_short_title": "Testing", "uc_ids": "UC-F-001;UC-F-002"},
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP",
     "control_code": "CPS234-§28a", "control_short_title": "Controls", "uc_ids": "UC-F-001"},
    {"framework_slug": "essential-8", "framework_role": "PRIMARY-LENS",
     "control_code": "E8-AppControl", "control_short_title": "App control", "uc_ids": "UC-F-001"},
    {"framework_slug": "cisa-ztmm-v2", "framework_role": "PRIMARY-LENS",
     "control_code": "ZT-Identity", "control_short_title": "Identity", "uc_ids": "UC-F-001"},
    {"framework_slug": "mitre-attack", "framework_role": "ADVERSARY-LENS",
     "control_code": "T1552", "control_short_title": "Unsecured creds", "uc_ids": "UC-F-001"},
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP",
     "control_code": "ISM-1619", "control_short_title": "Out of scope fw", "uc_ids": "UC-F-001"},
]
SCOPE = {"apra-cps-234", "essential-8", "cisa-ztmm-v2"}  # note: asd-ism NOT in scope; mitre excluded


def test_driver_excludes_mitre_and_out_of_scope():
    drivers = rg.regulatory_driver("UC-F-001", TRACE, SCOPE)
    slugs = [d["framework_slug"] for d in drivers]
    assert "mitre-attack" not in slugs          # adversary lens excluded
    assert "asd-ism" not in slugs                # not in scope


def test_driver_one_per_framework_min_control_code_regulator_first():
    drivers = rg.regulatory_driver("UC-F-001", TRACE, SCOPE)
    # one per framework (apra picks the lexicographically smallest code §28a < §35b)
    assert [d["framework_slug"] for d in drivers] == ["apra-cps-234", "cisa-ztmm-v2", "essential-8"]
    assert drivers[0]["control_code"] == "CPS234-§28a"   # regulator (BACK-MAP) first
    assert set(drivers[0]) == {"framework_slug", "control_code", "control_short_title"}


def test_driver_caps_at_three():
    big_scope = {"apra-cps-234", "essential-8", "cisa-ztmm-v2", "asd-ism"}
    assert len(rg.regulatory_driver("UC-F-001", TRACE, big_scope)) == 3


def test_driver_empty_when_no_match():
    assert rg.regulatory_driver("UC-NONE", TRACE, SCOPE) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: FAIL — `AttributeError: module ... has no attribute 'regulatory_driver'`.

- [ ] **Step 3: Implement `regulatory_driver`**

Append to `questionnaire/roadmap_generator.py` (after `quadrant`):
```python
def regulatory_driver(uc_id, trace_rows, scope, cap=3):
    """In-scope control drivers for a UC: one per framework, regulator-first, capped.

    Excludes ADVERSARY-LENS (e.g. MITRE) — not a regulatory obligation. Within a
    framework the lexicographically smallest control_code is chosen (deterministic).
    """
    by_fw = {}
    for row in trace_rows:
        slug = row["framework_slug"]
        if row.get("framework_role") == "ADVERSARY-LENS" or slug not in scope:
            continue
        if uc_id not in (row.get("uc_ids") or "").split(";"):
            continue
        cand = {
            "framework_slug": slug,
            "control_code": row["control_code"],
            "control_short_title": row.get("control_short_title", ""),
            "_role": row.get("framework_role", ""),
        }
        cur = by_fw.get(slug)
        if cur is None or cand["control_code"] < cur["control_code"]:
            by_fw[slug] = cand
    ordered = sorted(by_fw.values(),
                     key=lambda d: (_ROLE_ORDER.get(d["_role"], 9), d["framework_slug"]))
    return [{k: v for k, v in d.items() if not k.startswith("_")} for d in ordered[:cap]]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: PASS (7 tests total).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/roadmap_generator.py tests/test_roadmap_generator.py
git commit -m "feat(ws4): regulatory driver derivation (scoped, MITRE-excluded, capped)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Assemble the engagement menu (filter, fields, ordering, schema)

**Files:**
- Modify: `questionnaire/roadmap_generator.py` (add `build_engagement_menu`)
- Modify: `tests/test_roadmap_generator.py` (add tests)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_roadmap_generator.py`:
```python
RECORD = {
    "schema": "posture-assessment-record/v1",
    "responses": {
        "UC-F-001": {"proposed_state": "GAP", "final_state": "GAP"},      # P0 -> High
        "UC-F-002": {"proposed_state": "PARTIAL", "final_state": None},   # fallback PARTIAL; P1 -> Med
        "UC-MET":   {"proposed_state": "MET", "final_state": "MET"},      # excluded
        "UC-PEND":  {"proposed_state": None, "final_state": None},        # PENDING -> excluded
    },
}
USE_CASES = {
    "UC-F-001": {"uc_id": "UC-F-001", "short_title": "Prevent plaintext secrets in source repos", "priority_fi": "P0"},
    "UC-F-002": {"uc_id": "UC-F-002", "short_title": "Detect and remediate secrets in history", "priority_fi": "P1"},
}


def test_build_filters_to_gap_partial():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    ids = [it["uc_id"] for it in menu["items"]]
    assert ids == ["UC-F-001", "UC-F-002"]          # MET + PENDING excluded; ordered
    assert menu["schema"] == "engagement-menu/v1"
    assert menu["frameworks_scope"] == sorted(SCOPE)


def test_build_bands_and_quadrant_and_proposed():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    item = {it["uc_id"]: it for it in menu["items"]}["UC-F-001"]
    assert item["state"] == "GAP"
    assert item["risk_band"] == "High"              # P0 seed
    assert item["effort_band"] == "Med"             # default
    assert item["quadrant"] == "Quick wins"
    assert item["proposed_engagement"] == "GAP → remediate: Prevent plaintext secrets in source repos"
    assert item["dependency"] == ""
    assert item["regulatory_driver"][0]["framework_slug"] == "apra-cps-234"


def test_engagement_overrides_apply():
    eng = {"UC-F-001": {"risk_override": "Low", "effort": "High", "dependency": "inventory layer first"}}
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, eng, SCOPE)
    item = {it["uc_id"]: it for it in menu["items"]}["UC-F-001"]
    assert item["risk_band"] == "Low"
    assert item["effort_band"] == "High"
    assert item["quadrant"] == "Hard slogs"
    assert item["dependency"] == "inventory layer first"


def test_ordering_quadrant_then_risk_then_driver_then_id():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    # UC-F-001 (Quick wins) before UC-F-002 (Med risk default effort -> Quick wins too),
    # tie broken by risk desc: High (F-001) before Med (F-002).
    assert [it["uc_id"] for it in menu["items"]] == ["UC-F-001", "UC-F-002"]


def test_wrong_schema_raises():
    import pytest
    with pytest.raises(rg.RoadmapError):
        rg.build_engagement_menu({"schema": "nope", "responses": {}}, {}, [], {}, SCOPE)


def test_no_generated_timestamp_key():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    assert "generated" not in menu
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: FAIL — `AttributeError: ... 'build_engagement_menu'`.

- [ ] **Step 3: Implement `build_engagement_menu`**

Append to `questionnaire/roadmap_generator.py` (after `regulatory_driver`):
```python
def build_engagement_menu(record, use_cases, trace_rows, engagement_inputs, scope, source_record=""):
    """Pure transform: assessment record -> engagement-menu/v1 dict (GAP/PARTIAL only)."""
    if (record or {}).get("schema") != SCHEMA:
        raise RoadmapError(
            f"unrecognised record schema: {(record or {}).get('schema')!r} (expected {SCHEMA!r})")
    items = []
    for uc_id, resp in (record.get("responses") or {}).items():
        state = resolve_state(resp)
        if state not in ENGAGEMENT_STATES:
            continue
        uc = use_cases.get(uc_id, {})
        ov = engagement_inputs.get(uc_id, {})
        risk = (ov.get("risk_override") or "").strip() or seed_risk(uc.get("priority_fi"))
        effort = (ov.get("effort") or "").strip() or "Med"
        items.append({
            "uc_id": uc_id,
            "state": state,
            "risk_band": risk,
            "effort_band": effort,
            "quadrant": quadrant(risk, effort),
            "regulatory_driver": regulatory_driver(uc_id, trace_rows, scope),
            "dependency": ov.get("dependency") or "",
            "proposed_engagement": f"{state} → remediate: {uc.get('short_title', uc_id)}",
        })
    items.sort(key=lambda it: (
        _QUADRANT_ORDER.get(it["quadrant"], 9),
        _RISK_ORDER.get(it["risk_band"], 9),
        0 if it["regulatory_driver"] else 1,    # regulatory-driven first (tie-breaker)
        it["uc_id"],
    ))
    menu = {"schema": OUTPUT_SCHEMA}
    if source_record:
        menu["source_record"] = source_record
    menu["frameworks_scope"] = sorted(scope)
    menu["items"] = items
    return menu
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: PASS (13 tests total).

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/roadmap_generator.py tests/test_roadmap_generator.py
git commit -m "feat(ws4): assemble engagement-menu/v1 (filter, bands, ordering, schema)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Loaders, writer, CLI + XYZ dogfood

**Files:**
- Modify: `questionnaire/roadmap_generator.py` (loaders + `write_menu` + `main`)
- Modify: `tests/test_roadmap_generator.py` (CLI + dogfood tests)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_roadmap_generator.py`:
```python
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_preset_scope_reads_financial():
    scope = rg.preset_scope(str(ROOT / "matrix" / "config" / "presets" / "financial.yaml"))
    assert scope == {"apra-cps-234", "apra-cps-230", "apra-cpg-234", "cisa-ztmm-v2", "essential-8"}


def test_cli_writes_menu(tmp_path):
    record = {"schema": "posture-assessment-record/v1", "responses": {
        "UC-F-001": {"proposed_state": "GAP", "final_state": "GAP"}}}
    rec_path = tmp_path / "record.json"
    rec_path.write_text(json.dumps(record), encoding="utf-8")
    out = tmp_path / "menu.json"
    rc = subprocess.run(
        [sys.executable, "-m", "questionnaire.roadmap_generator", str(rec_path), "-o", str(out)],
        cwd=ROOT, capture_output=True, text=True)
    assert rc.returncode == 0, rc.stderr
    menu = json.loads(out.read_text(encoding="utf-8"))
    assert menu["schema"] == "engagement-menu/v1"
    assert menu["frameworks_scope"] == sorted(
        {"apra-cps-234", "apra-cps-230", "apra-cpg-234", "cisa-ztmm-v2", "essential-8"})
    item = menu["items"][0]
    assert item["uc_id"] == "UC-F-001"
    assert item["risk_band"] == "High" and item["quadrant"] == "Quick wins"
    # regulatory driver populated from the real trace, regulator-first, MITRE absent
    assert item["regulatory_driver"]
    assert all(d["framework_slug"] != "mitre-attack" for d in item["regulatory_driver"])


def test_cli_frameworks_override(tmp_path):
    record = {"schema": "posture-assessment-record/v1", "responses": {
        "UC-F-001": {"proposed_state": "GAP", "final_state": "GAP"}}}
    rec_path = tmp_path / "r.json"; rec_path.write_text(json.dumps(record), encoding="utf-8")
    out = tmp_path / "m.json"
    rc = subprocess.run(
        [sys.executable, "-m", "questionnaire.roadmap_generator", str(rec_path),
         "-o", str(out), "--frameworks", "essential-8"],
        cwd=ROOT, capture_output=True, text=True)
    assert rc.returncode == 0, rc.stderr
    menu = json.loads(out.read_text(encoding="utf-8"))
    assert menu["frameworks_scope"] == ["essential-8"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: FAIL — `AttributeError: ... 'preset_scope'` (and CLI tests error).

- [ ] **Step 3: Implement loaders, writer, CLI**

Append to `questionnaire/roadmap_generator.py`:
```python
def load_use_cases(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["uc_id"]: row for row in csv.DictReader(fh)}


def load_trace(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_engagement(path):
    if not path:
        return {}
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["uc_id"]: row for row in csv.DictReader(fh)}


def preset_scope(preset_path):
    """Union of primary + overlays + baseline framework slugs from a preset YAML."""
    import yaml
    with open(preset_path, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}
    slugs = []
    for key in ("primary", "overlays", "baseline"):
        slugs += cfg.get(key) or []
    return set(slugs)


def write_menu(menu, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(menu, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    ap = argparse.ArgumentParser(
        description="Generate engagement-menu.json from an assessment record.")
    ap.add_argument("record", help="path to assessment-record.json")
    ap.add_argument("-o", "--output", default="engagement-menu.json", help="output JSON path")
    ap.add_argument("--engagement", help="per-engagement CSV "
                    "(uc_id,risk_override,effort,dependency,escalation_control)")
    ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides preset scope)")
    ap.add_argument("--preset", default="financial",
                    help="preset name for default framework scope (default: financial)")
    ap.add_argument("--use-cases", default=os.path.join(root, "matrix", "use-cases.csv"))
    ap.add_argument("--trace", default=os.path.join(root, "matrix", "regulatory-trace.csv"))
    args = ap.parse_args(argv)

    with open(args.record, encoding="utf-8") as fh:
        record = json.load(fh)
    use_cases = load_use_cases(args.use_cases)
    trace = load_trace(args.trace)
    engagement = load_engagement(args.engagement)
    if args.frameworks:
        scope = {s.strip() for s in args.frameworks.split(",") if s.strip()}
    else:
        scope = preset_scope(os.path.join(
            root, "matrix", "config", "presets", f"{args.preset}.yaml"))

    menu = build_engagement_menu(record, use_cases, trace, engagement, scope,
                                 source_record=args.record)
    write_menu(menu, args.output)
    print(f"Wrote {args.output} ({len(menu['items'])} engagement items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_roadmap_generator.py -q`
Expected: PASS (16 tests total).

- [ ] **Step 5: Dogfood against real XYZ data and eyeball the output**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
python3 - <<'PY'
import csv, json
# Build a record-shaped fixture from the frozen XYZ current-state CSV (GAP/PARTIAL drive the menu).
rows = list(csv.DictReader(open("matrix/anz-current-state.csv", encoding="utf-8")))
rec = {"schema": "posture-assessment-record/v1", "responses": {
    r["uc_id"]: {"proposed_state": r["anz_state"], "final_state": r["anz_state"],
                 "rationale": r.get("gap_notes", "")} for r in rows}}
json.dump(rec, open("/tmp/xyz-record.json", "w"), indent=2)
print("record UCs:", len(rec["responses"]))
PY
python3 -m questionnaire.roadmap_generator /tmp/xyz-record.json -o /tmp/xyz-menu.json
python3 - <<'PY'
import json
m = json.load(open("/tmp/xyz-menu.json"))
items = m["items"]
print("items:", len(items), "| expect 27 (11 GAP + 16 PARTIAL)")
from collections import Counter
print("by quadrant:", Counter(i["quadrant"] for i in items))
f = {i["uc_id"]: i for i in items}
print("UC-F-001:", f.get("UC-F-001", {}).get("quadrant"), f.get("UC-F-001", {}).get("risk_band"))
print("scope:", m["frameworks_scope"])
assert len(items) == 27, items
assert f["UC-F-001"]["quadrant"] == "Quick wins"     # P0 -> High risk, Med effort default
PY
```
Expected: `items: 27`; UC-F-001 in Quick wins / High; scope = the 5 financial slugs; no exception. If the count is not 27, investigate the GAP/PARTIAL filter before continuing.

- [ ] **Step 6: Run the full suite (regression guard)**

Run: `python3 -m pytest -q`
Expected: PASS — previously-green suite (65) plus the new tests, all passing.

- [ ] **Step 7: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add questionnaire/roadmap_generator.py tests/test_roadmap_generator.py
git commit -m "feat(ws4): roadmap generator loaders + CLI; dogfood 27 XYZ findings

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Doc corrections + ADR-013 + backlog

**Files:**
- Modify: `methodology/RUBRIC.md` (override_reason -> rationale)
- Modify: `methodology/PLAYBOOK.md` (soften escalation bullet)
- Modify: `methodology/METHODOLOGY.md` (soften escalation sentence)
- Create: `docs/adr/ADR-013-roadmap-generator.md`
- Modify: `meta/IMPROVEMENT-BACKLOG.md` (WS-4 section)

- [ ] **Step 1: Fix RUBRIC.md field name**

In `methodology/RUBRIC.md`, replace the table row:
```
| `override_reason` | **Required whenever `final_state` differs from `proposed_state`.** Must cite the dimension(s) where the rubric's answer differed from the assessor's read and why. |
```
with:
```
| `rationale` | **Required whenever `final_state` differs from `proposed_state`.** Must cite the dimension(s) where the rubric's answer differed from the assessor's read and why. |
```

- [ ] **Step 2: Soften the PLAYBOOK escalation bullet**

In `methodology/PLAYBOOK.md`, replace the entire `- **Regulatory tie-breaker / escalator.** ...` bullet (the one ending "...trace why a finding moved.") with:
```
- **Regulatory tie-breaker.** A binding regulatory obligation (APRA CPS 234 / CPS 230, the
  ASD ISM, or the selected overlay) **breaks ties** between findings that land in the same cell —
  the obligation-bearing finding sorts first, and the generator applies this automatically. Where
  an obligation makes an exposure non-discretionary, the assessor may additionally **escalate that
  finding's risk band by one** as a deliberate, recorded judgment — captured in the per-engagement
  input (the `escalation_control` column) with the specific control reference, never applied
  silently. Band escalation is the assessor's logged call, not an automatic consequence of a
  control merely mapping to the finding.
```

- [ ] **Step 3: Soften the METHODOLOGY escalation sentence**

In `methodology/METHODOLOGY.md`, replace:
```
first, why, and what each item depends on. Regulatory obligations escalate priority — where an
obligation makes an exposure non-discretionary, it raises a finding's standing, and we always
record the specific control reference so you can trace why a finding moved. We deliberately use
```
with:
```
first, why, and what each item depends on. Where a regulatory obligation makes an exposure
non-discretionary, our assessor may raise that finding's standing — a recorded judgment tied to
the specific control reference, so you can always trace why a finding moved. We deliberately use
```

- [ ] **Step 4: Write ADR-013**

Create `docs/adr/ADR-013-roadmap-generator.md` following the `docs/adr/ADR-011-report-adapter.md` style. Required content:
- **Status:** Accepted. **Date:** 2026-05-31.
- **Context:** WS-4 slice 1 documented the risk × effort prioritisation method; this slice turns it into code that emits the engagement menu (the wedge) from an assessment record, for the future exec-summary print view.
- **Decision:** New `questionnaire/roadmap_generator.py` (pure transform + CLI, mirroring the adapter). Risk seeds from `priority_fi` (P0/P1/else→High/Med/Low), overridable in a per-engagement CSV; effort from that CSV (default Med); quadrant from risk×effort; regulatory driver scoped to the financial preset by default (MITRE/ADVERSARY-LENS excluded, capped one-per-framework/max 3, regulator-first); **regulation is an ordering tie-breaker only** — band escalation is a logged assessor judgment via `escalation_control`, not automatic. Output is `engagement-menu/v1` JSON (no timestamp, for byte-stable diffs). The state-resolution rule was extracted into shared `questionnaire/record_state.py` so the menu and the report never disagree.
- **Alternatives rejected:** auto risk-band escalation on control presence (would inflate nearly every FI gap — dishonest); archetype-derived effort (proxy, not real effort); emitting the full control list (4–39 controls — unreadable); a human-rendered output this slice (deferred to the print-view slice).
- **Consequences:** the exec-summary print view (renders this JSON) is the next slice; effort + risk overrides + dependency + escalation are consultant inputs (facilitated-primary); no Privacy Act driver exists (no trace data — methodology stance only).

- [ ] **Step 5: Update the backlog**

In `meta/IMPROVEMENT-BACKLOG.md`, under the WS-4 section, add beneath the slice-1 marker:
```
**Slice 2 — ✅ DONE (2026-05-31, branch ws4-roadmap-generator):** `questionnaire/roadmap_generator.py`
emits `engagement-menu/v1` JSON from an assessment record (risk seed from priority_fi, effort from a
per-engagement CSV, risk×effort quadrants, regulatory driver scoped to the financial preset / MITRE
excluded / capped, regulation as ordering tie-breaker). Shared `record_state.py` resolver keeps the menu
and report in agreement. ADR-013. Bundled doc fixes: RUBRIC `rationale`, escalation softened to a logged
assessor judgment. **Deferred:** the exec-summary print view (renders this JSON).
```

- [ ] **Step 6: Verify the doc edits and full suite**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
grep -n "override_reason" methodology/RUBRIC.md && echo "STILL PRESENT — fix" || echo "OK rubric fixed"
grep -nc "Regulatory tie-breaker\." methodology/PLAYBOOK.md
grep -nE "TBD|TODO|FIXME" docs/adr/ADR-013-roadmap-generator.md || echo "OK no placeholders"
ls docs/adr/ADR-0{11,12,13}-*.md
python3 -m pytest -q 2>&1 | tail -3
```
Expected: `OK rubric fixed`; the PLAYBOOK grep prints `1`; `OK no placeholders`; ADR-013 listed; full suite green.

- [ ] **Step 7: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add methodology/RUBRIC.md methodology/PLAYBOOK.md methodology/METHODOLOGY.md docs/adr/ADR-013-roadmap-generator.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws4): ADR-013 + soften escalation + RUBRIC rationale fix + backlog

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria (whole slice)

- `questionnaire/record_state.py` shared resolver; adapter refactored to use it; adapter tests still green.
- `questionnaire/roadmap_generator.py`: `seed_risk`, `quadrant`, `regulatory_driver`, `build_engagement_menu`, loaders, `write_menu`, CLI.
- Emits `engagement-menu/v1` with structured `regulatory_driver`, `frameworks_scope` provenance, no timestamp.
- Dogfood on XYZ data yields 27 engagement items; UC-F-001 in Quick wins.
- Both slice-1 doc corrections applied; doc and code agree on regulation (tie-breaker auto, escalation = logged judgment).
- ADR-013 + backlog updated. Full suite green (65 prior + new tests).
- All commits on `ws4-roadmap-generator`.

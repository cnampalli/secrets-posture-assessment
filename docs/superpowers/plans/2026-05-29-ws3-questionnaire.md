# WS-3 Interactive Assessment Instrument (slice 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a self-contained HTML questionnaire that renders the WS-1 rubric, auto-derives a posture state from answers, supports assessor override + confidence, and imports/exports a rich `assessment-record.json`.

**Architecture:** A Python build step (the `build_matrix_viewer.py` pattern) bakes the WS-1 rubric CSVs into one offline HTML file. The scoring ladder is authored once in `methodology/scoring.py` (tested reference), mirrored in `questionnaire/scoring.js` (inlined into the HTML), with both pinned to a shared `scoring-vectors.json` so they can't drift. The Variant-A wizard (`app.js`) is presentation only.

**Tech Stack:** Python 3 (stdlib), Node 26 (test conformance only), pytest 8, vanilla browser JS.

---

## Design references

- Spec: `docs/superpowers/specs/2026-05-29-ws3-questionnaire-design.md`
- Sketch (chosen flow): `.planning/sketches/004-ws3-questionnaire/variant-a-focused-wizard.html`
- Rubric inputs (all in `methodology/`): `assessment-archetypes.csv`, `archetype-questions.csv`, `uc-archetype-map.csv`, `bespoke-criteria.csv`
- Ground-truth facts:
  - 47 UCs in `uc-archetype-map.csv`; **2 are A0** (`UC-F-017`, `UC-F-026`, empty params).
  - Each archetype's `Q1` is `informs_state=GAP_PARTIAL`; all other questions are `PARTIAL_MET`.
  - UC **title** = the `notes` column of `uc-archetype-map.csv`; **category** = `UC-F-*`→Functional, `UC-N-*`→Non-functional.
  - `params` format: `key=value;key=value`. Templates contain `{slot}` placeholders filled from params.
  - WS-1 imports `methodology/` as a package (`import methodology.validate_rubric`). `methodology/__init__.py` exists. The repo root is pytest's rootdir (on `sys.path`). `tests/conftest.py` additionally puts `matrix/` on the path.
- The ladder (the credibility core): all-NA→`NA`; else any non-NA unanswered→`PENDING`; else any `GAP_PARTIAL`=`no`→`GAP`; else any `PARTIAL_MET`=`no`→`PARTIAL`; else `MET`. A0 UCs are scored manually (no ladder).

## File structure (all created)

| Path | Responsibility |
|---|---|
| `methodology/scoring.py` | Reference engine: `derive_state(questions, answers) -> str`. Pure, no I/O. |
| `questionnaire/__init__.py` | Make `questionnaire` a package (so tests can `import questionnaire.x`). |
| `questionnaire/scoring-vectors.json` | Canonical `(questions, answers) -> expected` vectors; drift guard. |
| `questionnaire/scoring.js` | JS mirror of `derive_state` (browser + node-testable). |
| `questionnaire/scoring.test.mjs` | Node conformance: JS engine matches the vectors. |
| `questionnaire/rubric_loader.py` | `load_rubric(meth_dir) -> list[dict]`: resolve 47 UCs, fill `{slot}` params, A0→sub-criteria. |
| `questionnaire/template.html` | Raw HTML/CSS shell with `/*__SCORING__*/`, `/*__RUBRIC__*/`, `/*__APP__*/` tokens. |
| `questionnaire/app.js` | Variant-A wizard UI: rail, UC view, live scoring card, override drawer, autosave, import, export. |
| `questionnaire/build_questionnaire.py` | `build(out_path=None)`: loader→JSON, inline scoring.js + app.js → self-contained `questionnaire.html`. |
| `tests/test_scoring.py` | pytest: ladder outcomes + vectors. |
| `tests/test_scoring_js.py` | pytest: runs `node scoring.test.mjs`; skipped if node absent. |
| `tests/test_rubric_loader.py` | pytest: 47 UCs resolve; params fill; A0 detection; no leftover slots; title/category. |
| `tests/test_build_questionnaire.py` | pytest: build is self-contained, embeds 47 UCs, inlines scoring + app. |
| `docs/adr/ADR-010-questionnaire-instrument.md` | Records dual-engine + rich-record decisions. |
| `meta/IMPROVEMENT-BACKLOG.md` | (Modify) mark WS-3 slice 1 done + deferred items. |

**All commands assume CWD = repo root** (`/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`). Run pytest as `python3 -m pytest`.

---

## Task 1: Scoring reference engine + canonical vectors

**Files:** Create `methodology/scoring.py`, `questionnaire/scoring-vectors.json`, `tests/test_scoring.py`

- [ ] **Step 1: Create the canonical vectors** `questionnaire/scoring-vectors.json`

```json
[
  {"name": "all met",        "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"yes","Q2":"yes"}, "expected": "MET"},
  {"name": "gp no -> gap",   "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"no","Q2":"yes"},  "expected": "GAP"},
  {"name": "pm no -> partial","questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"yes","Q2":"no"},  "expected": "PARTIAL"},
  {"name": "unanswered -> pending", "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"yes"}, "expected": "PENDING"},
  {"name": "null -> pending", "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"}], "answers": {"Q1": null}, "expected": "PENDING"},
  {"name": "all na -> na",    "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"na","Q2":"na"}, "expected": "NA"},
  {"name": "na neutral on gate", "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"na","Q2":"yes"}, "expected": "MET"},
  {"name": "gp precedence over pm", "questions": [{"qid":"Q1","informs_state":"GAP_PARTIAL"},{"qid":"Q2","informs_state":"PARTIAL_MET"}], "answers": {"Q1":"no","Q2":"no"}, "expected": "GAP"}
]
```

- [ ] **Step 2: Write the failing test** `tests/test_scoring.py`

```python
import json, pathlib
import methodology.scoring as scoring

ROOT = pathlib.Path(__file__).resolve().parents[1]
VECTORS = json.load(open(ROOT / "questionnaire" / "scoring-vectors.json"))


def test_all_met():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes", "Q2": "yes"}) == "MET"


def test_gap_partial_no_is_gap():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "no", "Q2": "yes"}) == "GAP"


def test_partial_met_no_is_partial():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes", "Q2": "no"}) == "PARTIAL"


def test_unanswered_is_pending():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes"}) == "PENDING"


def test_all_na_is_na():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}]
    assert scoring.derive_state(qs, {"Q1": "na"}) == "NA"


def test_vectors_fixture():
    for v in VECTORS:
        assert scoring.derive_state(v["questions"], v["answers"]) == v["expected"], v["name"]
```

- [ ] **Step 3: Run, confirm RED**

Run: `python3 -m pytest tests/test_scoring.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'methodology.scoring'`

- [ ] **Step 4: Implement** `methodology/scoring.py`

```python
"""Reference posture-state derivation for the WS-1 archetype rubric.

derive_state applies the laddering rule for an archetype use case (A1-A8).
A0 (bespoke) use cases are scored manually and do NOT call this function.
Pure: no I/O, no globals. Mirrored by questionnaire/scoring.js."""

VALID_ANSWERS = {"yes", "no", "na"}


def derive_state(questions, answers):
    """questions: [{"qid": str, "informs_state": "GAP_PARTIAL"|"PARTIAL_MET"}].
    answers: {qid: "yes"|"no"|"na"|None}. Returns GAP|PARTIAL|MET|PENDING|NA."""
    vals = [(q["informs_state"], answers.get(q["qid"])) for q in questions]
    if vals and all(v == "na" for _, v in vals):
        return "NA"
    if any(v not in VALID_ANSWERS for _, v in vals):   # None or missing
        return "PENDING"
    if any(inf == "GAP_PARTIAL" and v == "no" for inf, v in vals):
        return "GAP"
    if any(inf == "PARTIAL_MET" and v == "no" for inf, v in vals):
        return "PARTIAL"
    return "MET"
```

- [ ] **Step 5: Run, confirm GREEN**

Run: `python3 -m pytest tests/test_scoring.py -v`
Expected: PASS (6 tests).

- [ ] **Step 6: Commit**

```bash
git add methodology/scoring.py questionnaire/scoring-vectors.json tests/test_scoring.py
git commit -m "feat(ws3): scoring reference engine + canonical vectors"
```

---

## Task 2: JS mirror + node conformance

**Files:** Create `questionnaire/scoring.js`, `questionnaire/scoring.test.mjs`, `tests/test_scoring_js.py`

- [ ] **Step 1: Implement** `questionnaire/scoring.js`

The function is global (no module system) so the build can inline it verbatim into the browser, and `scoring.test.mjs` can import the file's text. Use a `globalThis` attach + an ESM-friendly export guard:

```javascript
// Mirror of methodology/scoring.py — keep in lockstep via scoring-vectors.json.
function deriveState(questions, answers) {
  const vals = questions.map(q => [q.informs_state, answers[q.qid] ?? null]);
  if (vals.length && vals.every(([, v]) => v === "na")) return "NA";
  if (vals.some(([, v]) => v !== "yes" && v !== "no" && v !== "na")) return "PENDING";
  if (vals.some(([inf, v]) => inf === "GAP_PARTIAL" && v === "no")) return "GAP";
  if (vals.some(([inf, v]) => inf === "PARTIAL_MET" && v === "no")) return "PARTIAL";
  return "MET";
}
if (typeof module !== "undefined" && module.exports) module.exports = { deriveState };
```

- [ ] **Step 2: Write the node conformance test** `questionnaire/scoring.test.mjs`

```javascript
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
// Load scoring.js by evaluating its source (it is a plain script, not ESM).
const src = readFileSync(join(here, "scoring.js"), "utf8");
const deriveState = new Function(src + "\nreturn deriveState;")();
const vectors = JSON.parse(readFileSync(join(here, "scoring-vectors.json"), "utf8"));

let failed = 0;
for (const v of vectors) {
  const got = deriveState(v.questions, v.answers);
  if (got !== v.expected) { console.error(`FAIL ${v.name}: got ${got}, want ${v.expected}`); failed++; }
}
if (failed) { console.error(`${failed} vector(s) failed`); process.exit(1); }
console.log(`scoring.js: ${vectors.length} vectors OK`);
```

- [ ] **Step 3: Run it directly, confirm it passes**

Run: `node questionnaire/scoring.test.mjs`
Expected: `scoring.js: 8 vectors OK`

- [ ] **Step 4: Write the pytest wrapper** `tests/test_scoring_js.py`

```python
import shutil, subprocess, pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("node") is None, reason="node not available")
def test_js_engine_conforms_to_vectors():
    r = subprocess.run(["node", str(ROOT / "questionnaire" / "scoring.test.mjs")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "vectors OK" in r.stdout
```

- [ ] **Step 5: Run via pytest, confirm GREEN**

Run: `python3 -m pytest tests/test_scoring_js.py -v`
Expected: PASS (1 test).

- [ ] **Step 6: Commit**

```bash
git add questionnaire/scoring.js questionnaire/scoring.test.mjs tests/test_scoring_js.py
git commit -m "feat(ws3): JS scoring mirror + node conformance against shared vectors"
```

---

## Task 3: Rubric loader

**Files:** Create `questionnaire/__init__.py`, `questionnaire/rubric_loader.py`, `tests/test_rubric_loader.py`

- [ ] **Step 1: Create the package marker** `questionnaire/__init__.py` (empty file)

```python
```

- [ ] **Step 2: Write the failing test** `tests/test_rubric_loader.py`

```python
import pathlib, re
import pytest
import questionnaire.rubric_loader as rl

ROOT = pathlib.Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
UCS = rl.load_rubric(METH)
BY_ID = {u["uc_id"]: u for u in UCS}


def test_all_47_use_cases_resolve():
    assert len(UCS) == 47


def test_category_from_prefix():
    assert BY_ID["UC-F-001"]["category"] == "Functional"
    assert BY_ID["UC-N-002"]["category"] == "Non-functional"


def test_title_from_notes():
    assert BY_ID["UC-F-001"]["title"] == "Prevent plaintext secrets in repos"


def test_ladder_uc_fills_params():
    uc = BY_ID["UC-F-001"]
    assert uc["kind"] == "ladder"
    assert uc["archetype"] == "A1"
    q1 = uc["questions"][0]
    assert q1["qid"] == "A1-Q1"
    assert q1["informs_state"] == "GAP_PARTIAL"
    assert q1["text"] == "Is secret push-protection deployed at all relevant gates for repo-committed secrets?"


def test_no_leftover_slots_anywhere():
    for uc in UCS:
        if uc["kind"] == "ladder":
            for q in uc["questions"]:
                assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled: {q['text']}"


def test_a0_use_cases_are_bespoke():
    uc = BY_ID["UC-F-017"]
    assert uc["kind"] == "bespoke"
    assert uc["archetype"] == "A0"
    assert len(uc["sub_criteria"]) == 3
    sc = uc["sub_criteria"][0]
    assert sc["sub_id"] == "UC-F-017.1"
    assert "TEE attestation" in sc["question"]


def test_missing_param_raises(tmp_path):
    # a template needing {control} but params lacking it must error
    aq = tmp_path / "archetype-questions.csv"
    aq.write_text("archetype_id,q_id,question_template,dimension,informs_state\n"
                  'AX,AX-Q1,"Is {control} on?",coverage,GAP_PARTIAL\n', encoding="utf-8")
    arch = tmp_path / "assessment-archetypes.csv"
    arch.write_text("archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation\n"
                    "AX,Test,i,m,p,g,n,e\n", encoding="utf-8")
    mp = tmp_path / "uc-archetype-map.csv"
    mp.write_text("uc_id,archetype_id,params,notes\nUC-F-900,AX,nope=1,Title\n", encoding="utf-8")
    bs = tmp_path / "bespoke-criteria.csv"
    bs.write_text("uc_id,sub_id,sub_criterion,question,evidence\n", encoding="utf-8")
    with pytest.raises(rl.RubricError):
        rl.load_rubric(tmp_path)
```

- [ ] **Step 3: Run, confirm RED**

Run: `python3 -m pytest tests/test_rubric_loader.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'questionnaire.rubric_loader'`

- [ ] **Step 4: Implement** `questionnaire/rubric_loader.py`

```python
"""Resolve the WS-1 rubric CSVs into renderable use-case question sets.

Depends only on methodology/: title comes from uc-archetype-map's `notes`,
category from the uc_id prefix. A0 use cases yield bespoke sub-criteria;
A1-A8 yield param-filled ladder questions."""
import csv
import os
import re
from collections import defaultdict


class RubricError(Exception):
    pass


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _parse_params(raw):
    out = {}
    for chunk in (raw or "").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise RubricError(f"malformed param (no '='): {chunk!r}")
        k, v = chunk.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def _fill(template, params, uc_id, qid):
    def repl(m):
        slot = m.group(1)
        if slot not in params:
            raise RubricError(f"{uc_id} {qid}: no param for slot '{{{slot}}}'")
        return params[slot]
    return re.sub(r"\{([^}]+)\}", repl, template)


def load_rubric(meth_dir):
    meth_dir = str(meth_dir)
    questions_by_arch = defaultdict(list)
    for r in _read(os.path.join(meth_dir, "archetype-questions.csv")):
        questions_by_arch[r["archetype_id"]].append(r)
    arch_name = {r["archetype_id"]: r["name"]
                 for r in _read(os.path.join(meth_dir, "assessment-archetypes.csv"))}
    bespoke_by_uc = defaultdict(list)
    for r in _read(os.path.join(meth_dir, "bespoke-criteria.csv")):
        bespoke_by_uc[r["uc_id"]].append(r)

    out = []
    for row in _read(os.path.join(meth_dir, "uc-archetype-map.csv")):
        uc_id = row["uc_id"]
        arch = row["archetype_id"]
        category = "Functional" if uc_id.startswith("UC-F") else "Non-functional"
        base = {"uc_id": uc_id, "title": row.get("notes", ""), "category": category,
                "archetype": arch, "archetype_name": arch_name.get(arch, arch)}
        if arch == "A0":
            base["kind"] = "bespoke"
            base["sub_criteria"] = [
                {"sub_id": b["sub_id"], "sub_criterion": b["sub_criterion"],
                 "question": b["question"], "evidence": b["evidence"]}
                for b in bespoke_by_uc.get(uc_id, [])]
        else:
            params = _parse_params(row.get("params", ""))
            base["kind"] = "ladder"
            base["questions"] = [
                {"qid": q["q_id"], "dimension": q["dimension"],
                 "informs_state": q["informs_state"],
                 "text": _fill(q["question_template"], params, uc_id, q["q_id"])}
                for q in questions_by_arch.get(arch, [])]
        out.append(base)
    return out
```

- [ ] **Step 5: Run, confirm GREEN**

Run: `python3 -m pytest tests/test_rubric_loader.py -v`
Expected: PASS (7 tests).

- [ ] **Step 6: Commit**

```bash
git add questionnaire/__init__.py questionnaire/rubric_loader.py tests/test_rubric_loader.py
git commit -m "feat(ws3): rubric loader resolves 47 UCs (param-fill + A0 bespoke)"
```

---

## Task 4: Build pipeline + template + stub app

**Files:** Create `questionnaire/template.html`, `questionnaire/app.js` (stub), `questionnaire/build_questionnaire.py`, `tests/test_build_questionnaire.py`

This proves the CSV→JSON→self-contained-HTML pipeline before the full wizard. `app.js` starts as a stub that only proves rubric data arrives; Task 5 replaces it.

- [ ] **Step 1: Create the template** `questionnaire/template.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Posture Assessment Instrument</title>
<style>
  :root{--ink:#1a1d21;--muted:#5b6470;--line:#e2e6ea;--paper:#f6f7f9;--card:#fff;
    --gap:#c0392b;--partial:#c97a14;--met:#2e7d52;--pending:#7a8593;--na:#9aa3ad;--accent:#2a4d8f}
  *{box-sizing:border-box}
  body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--paper)}
  h1,h2,h3{font-family:Georgia,"Times New Roman",serif;font-weight:600;margin:0}
  .mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
  header{display:flex;align-items:center;gap:18px;padding:12px 22px;background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
  header h1{font-size:17px}
  .grow{flex:1}
  .btn{font:13px/1 inherit;padding:9px 14px;border-radius:5px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}
  .btn.ghost{background:#fff;color:var(--accent)}
  .wrap{display:grid;grid-template-columns:268px 1fr;min-height:calc(100vh - 53px)}
  nav{background:var(--card);border-right:1px solid var(--line);padding:12px 0;overflow:auto}
  .rail-grp{font:11px/1 sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:12px 18px 6px}
  .rail-item{display:flex;align-items:center;gap:10px;padding:8px 18px;cursor:pointer;border-left:3px solid transparent}
  .rail-item:hover{background:var(--paper)}
  .rail-item.active{background:#eef3fb;border-left-color:var(--accent)}
  .rail-item .t{font-size:12.5px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .rail-item .mono{font-size:12px;color:var(--muted)}
  .dot{width:9px;height:9px;border-radius:50%;background:var(--pending);flex:none}
  .dot.GAP{background:var(--gap)}.dot.PARTIAL{background:var(--partial)}.dot.MET{background:var(--met)}.dot.NA{background:var(--na)}
  main{padding:28px 38px;max-width:880px}
  .crumb{font-size:12.5px;color:var(--muted);margin-bottom:6px}
  .uc-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  .uc-head h2{font-size:23px}
  .arch-badge{font:11px/1 sans-serif;color:var(--accent);background:#eef3fb;border:1px solid #d3e0f5;padding:5px 9px;border-radius:20px}
  .uc-sub{color:var(--muted);font-size:13px;margin:2px 0 22px}
  .q{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:15px 18px;margin-bottom:11px}
  .qmeta{display:flex;gap:8px;margin-bottom:8px}
  .pill{font:10.5px/1 sans-serif;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);background:var(--paper);border:1px solid var(--line);padding:4px 7px;border-radius:12px}
  .pill.gp{color:#8a4b12;border-color:#e7cba3;background:#fdf6ec}
  .pill.pm{color:#1f5e3f;border-color:#bfe0cd;background:#eef7f1}
  .q p{margin:0 0 12px;font-size:15px}
  .seg{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
  .seg button{font:13px/1 inherit;padding:8px 16px;border:0;background:#fff;cursor:pointer;color:var(--muted);border-right:1px solid var(--line)}
  .seg button:last-child{border-right:0}
  .seg button.on[data-v=yes]{background:var(--met);color:#fff}
  .seg button.on[data-v=no]{background:var(--gap);color:#fff}
  .seg button.on[data-v=na]{background:var(--na);color:#fff}
  .bespoke{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:15px 18px;margin-bottom:11px}
  .bespoke label{display:flex;gap:10px;align-items:flex-start;padding:7px 0;font-size:14px}
  .bespoke .ev{font-size:12px;color:var(--muted);margin-left:26px}
  .score{position:sticky;bottom:0;margin-top:24px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;box-shadow:0 -6px 18px rgba(20,30,50,.05)}
  .score-row{display:flex;align-items:center;gap:16px}
  .state-chip{font-family:Georgia,serif;font-size:20px;font-weight:600;padding:8px 18px;border-radius:7px;color:#fff;min-width:118px;text-align:center}
  .state-chip.GAP{background:var(--gap)}.state-chip.PARTIAL{background:var(--partial)}.state-chip.MET{background:var(--met)}.state-chip.PENDING{background:var(--pending)}.state-chip.NA{background:var(--na)}
  .why{font-size:13px;color:var(--muted);flex:1}.why b{color:var(--ink)}
  .ovr-toggle{font-size:13px;color:var(--accent);cursor:pointer;user-select:none}
  .ovr{margin-top:14px;padding-top:14px;border-top:1px dashed var(--line);display:none}
  .ovr.open{display:block}
  .ovr label{font-size:12.5px;color:var(--muted);display:block;margin-bottom:5px}
  .ovr textarea{width:100%;min-height:54px;border:1px solid var(--line);border-radius:6px;padding:9px;font:13.5px/1.45 inherit;resize:vertical}
  .ovr textarea.need{border-color:var(--gap);background:#fdeeea}
  .ovr-grid{display:flex;gap:24px;align-items:flex-end;margin-top:12px}
  .conf{display:flex;gap:6px}
  .conf button{font:12px/1 inherit;padding:7px 12px;border:1px solid var(--line);background:#fff;border-radius:5px;cursor:pointer;color:var(--muted)}
  .conf button.on{border-color:var(--accent);background:#eef3fb;color:var(--accent);font-weight:600}
  .ovr-final select{padding:7px;border:1px solid var(--line);border-radius:5px;font:13px inherit}
  .navrow{display:flex;justify-content:space-between;margin-top:22px}
  .toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#1a1d21;color:#fff;padding:10px 16px;border-radius:6px;font-size:13px;opacity:0;transition:opacity .2s;pointer-events:none}
  .toast.show{opacity:.95}
</style>
</head>
<body>
<header>
  <h1>Posture Assessment Instrument</h1>
  <span class="mono" id="progress" style="font-size:12px;color:var(--muted)"></span>
  <span class="grow"></span>
  <input type="file" id="importFile" accept="application/json" style="display:none">
  <button class="btn ghost" onclick="document.getElementById('importFile').click()">⤒ Import</button>
  <button class="btn" onclick="App.exportRecord()">⤓ Export record</button>
</header>
<div class="wrap"><nav id="rail"></nav><main id="main"></main></div>
<div class="toast" id="toast"></div>
<script>
/*__SCORING__*/
const RUBRIC = /*__RUBRIC__*/[];
/*__APP__*/
</script>
</body>
</html>
```

- [ ] **Step 2: Create the stub app** `questionnaire/app.js`

```javascript
// STUB — replaced in Task 5. Proves rubric data is injected and reachable.
const App = {
  exportRecord() { /* replaced in Task 5 */ }
};
document.getElementById("main").innerHTML =
  "<p>Loaded <b>" + RUBRIC.length + "</b> use cases. (stub)</p>";
```

- [ ] **Step 3: Write the failing test** `tests/test_build_questionnaire.py`

```python
import pathlib
import questionnaire.build_questionnaire as bq

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_build_writes_self_contained_html(tmp_path):
    out = tmp_path / "questionnaire.html"
    bq.build(out_path=out)
    html = out.read_text(encoding="utf-8")
    # all 47 UC ids embedded
    assert html.count("UC-F-001") >= 1
    assert "UC-F-017" in html and "UC-N-002" in html
    # scoring + app inlined (no external script/link refs)
    assert "function deriveState" in html
    assert "const App" in html
    assert "<script src" not in html and "<link " not in html
    assert "http://" not in html and "https://" not in html
    # injection tokens consumed
    assert "/*__RUBRIC__*/[]" not in html
    assert "/*__SCORING__*/" not in html and "/*__APP__*/" not in html


def test_build_default_output_path():
    out = bq.build()
    p = pathlib.Path(out)
    assert p.exists() and p.name == "questionnaire.html"
```

- [ ] **Step 4: Run, confirm RED**

Run: `python3 -m pytest tests/test_build_questionnaire.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'questionnaire.build_questionnaire'`

- [ ] **Step 5: Implement** `questionnaire/build_questionnaire.py`

```python
#!/usr/bin/env python3
"""Bake the WS-1 rubric into a self-contained questionnaire HTML.

Pattern mirrors matrix/build_matrix_viewer.py: resolve rubric -> JSON, inline
scoring.js + app.js into template.html via /*__TOKEN__*/ replacement, write one
offline file with no external references."""
import json
import os

from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
METH = os.path.join(os.path.dirname(HERE), "methodology")


def build(out_path=None):
    out_path = str(out_path) if out_path else os.path.join(HERE, "questionnaire.html")
    rubric = rubric_loader.load_rubric(METH)
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    scoring = open(os.path.join(HERE, "scoring.js"), encoding="utf-8").read()
    app = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()
    html = (template
            .replace("/*__SCORING__*/", scoring)
            .replace("/*__RUBRIC__*/[]", json.dumps(rubric, ensure_ascii=False))
            .replace("/*__APP__*/", app))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes; {len(rubric)} use cases)")
    return out_path


if __name__ == "__main__":
    build()
```

- [ ] **Step 6: Run, confirm GREEN**

Run: `python3 -m pytest tests/test_build_questionnaire.py -v`
Expected: PASS (2 tests). Note: `scoring.js` contains `function deriveState`; the stub `app.js` contains `const App`; the `module.exports` guard line in scoring.js is harmless in-browser (`typeof module` is `"undefined"`).

- [ ] **Step 7: Commit**

```bash
git add questionnaire/template.html questionnaire/app.js questionnaire/build_questionnaire.py tests/test_build_questionnaire.py
git commit -m "feat(ws3): self-contained build pipeline (template + inlined engine)"
```

---

## Task 5: The wizard (full app.js)

**Files:** Modify `questionnaire/app.js` (replace the stub with the full Variant-A wizard)

This is presentation glue over the node-tested `deriveState` engine. It is verified by re-running the build test (structure) plus a manual browser smoke (the engine itself is already conformance-tested).

- [ ] **Step 1: Replace** `questionnaire/app.js` **with the full wizard**

```javascript
/* Variant-A wizard. Engine: deriveState() (inlined from scoring.js).
   Rich record is the single source of truth; autosaved to localStorage. */
const STORE_KEY = "posture-assessment-record/v1";
const SCHEMA = "posture-assessment-record/v1";
const STATES = ["GAP", "PARTIAL", "MET", "PENDING", "NA"];
const RUBRIC_BY_ID = Object.fromEntries(RUBRIC.map(u => [u.uc_id, u]));

// responses[uc_id] = {answers:{}, overridden:bool, final_state:str|null, rationale:str, confidence:str}
let responses = {};
let current = RUBRIC[0] ? RUBRIC[0].uc_id : null;
const uiOpen = {};

function blankResponse() { return {answers: {}, overridden: false, final_state: null, rationale: "", confidence: "MED"}; }
function resp(id) { return (responses[id] = responses[id] || blankResponse()); }

function loadSaved() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) { const rec = JSON.parse(raw); if (rec && rec.responses) responses = rec.responses; }
  } catch (e) { /* ignore corrupt autosave */ }
}
function save() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(buildRecord())); }
  catch (e) { toast("Autosave unavailable"); }
}

function proposedFor(uc) {
  if (uc.kind === "bespoke") return null;          // A0 manual
  return deriveState(uc.questions, resp(uc.uc_id).answers);
}
function finalFor(uc) {
  const r = resp(uc.uc_id);
  if (r.overridden && r.final_state) return r.final_state;
  const p = proposedFor(uc);
  return p || r.final_state || "PENDING";
}
function whyFor(uc) {
  const r = resp(uc.uc_id);
  if (uc.kind === "bespoke") return "Bespoke (A0) — assessor sets the state from the criteria below";
  const p = proposedFor(uc), a = r.answers, qs = uc.questions;
  if (p === "PENDING") { const n = qs.filter(q => !["yes","no","na"].includes(a[q.qid])).length; return n + " of " + qs.length + " question(s) unanswered"; }
  if (p === "NA") return "All criteria marked not-applicable";
  if (p === "GAP") { const q = qs.find(q => q.informs_state === "GAP_PARTIAL" && a[q.qid] === "no"); return "GAP↔PARTIAL question is No (" + q.qid + ", " + q.dimension + ")"; }
  if (p === "PARTIAL") { const q = qs.find(q => q.informs_state === "PARTIAL_MET" && a[q.qid] === "no"); return "A PARTIAL↔MET question is No (" + q.qid + ", " + q.dimension + ")"; }
  return "All criteria satisfied across every dimension";
}

function buildRecord() {
  const out = {schema: SCHEMA, generated: new Date().toISOString(), responses: {}};
  RUBRIC.forEach(uc => {
    const r = responses[uc.uc_id]; if (!r) return;
    out.responses[uc.uc_id] = {
      archetype: uc.archetype, answers: r.answers,
      proposed_state: proposedFor(uc), final_state: finalFor(uc),
      overridden: !!r.overridden, rationale: r.rationale || "", confidence: r.confidence || "MED"
    };
  });
  return out;
}

/* ---- rendering ---- */
function renderRail() {
  const groups = {};
  RUBRIC.forEach(u => (groups[u.category] = groups[u.category] || []).push(u));
  let h = "";
  for (const g in groups) {
    h += '<div class="rail-grp">' + g + "</div>";
    groups[g].forEach(u => {
      h += '<div class="rail-item ' + (u.uc_id === current ? "active" : "") + '" onclick="App.go(\'' + u.uc_id + '\')">' +
        '<span class="dot ' + finalFor(u) + '"></span><span class="t">' + esc(u.title) + '</span>' +
        '<span class="mono">' + u.uc_id + "</span></div>";
    });
  }
  document.getElementById("rail").innerHTML = h;
  const scored = RUBRIC.filter(u => { const p = proposedFor(u); const r = responses[u.uc_id];
    return (p && p !== "PENDING") || (u.kind === "bespoke" && r && r.final_state); }).length;
  document.getElementById("progress").textContent = scored + " / " + RUBRIC.length + " scored";
}

function renderMain() {
  const uc = RUBRIC_BY_ID[current]; if (!uc) return;
  const r = resp(uc.uc_id);
  let h = '<div class="crumb">' + uc.category + " · use case</div>" +
    '<div class="uc-head"><h2>' + esc(uc.title) + '</h2><span class="arch-badge mono">' + uc.archetype + " · " + esc(uc.archetype_name) + "</span></div>" +
    '<div class="uc-sub mono">' + uc.uc_id + "</div>";

  if (uc.kind === "bespoke") {
    h += '<div class="bespoke"><div class="qmeta"><span class="pill">bespoke criteria (A0) — guidance</span></div>';
    uc.sub_criteria.forEach(sc => {
      const on = r.answers[sc.sub_id] === true;
      h += '<label><input type="checkbox" ' + (on ? "checked" : "") + ' onchange="App.check(\'' + sc.sub_id + '\',this.checked)">' +
        "<span>" + esc(sc.sub_criterion) + "<div class=\"ev\">" + esc(sc.question) + " — <i>" + esc(sc.evidence) + "</i></div></span></label>";
    });
    h += "</div>";
  } else {
    uc.questions.forEach(q => {
      const a = r.answers[q.qid] || "";
      h += '<div class="q"><div class="qmeta"><span class="pill">' + q.dimension + '</span><span class="pill ' +
        (q.informs_state === "GAP_PARTIAL" ? "gp" : "pm") + '">' + (q.informs_state === "GAP_PARTIAL" ? "GAP ↔ PARTIAL" : "PARTIAL ↔ MET") + "</span></div>" +
        "<p>" + esc(q.text) + "</p><div class=\"seg\">" +
        ["yes", "no", "na"].map(v => '<button data-v="' + v + '" class="' + (a === v ? "on" : "") + '" onclick="App.answer(\'' + q.qid + '\',\'' + v + '\')">' + v.toUpperCase() + "</button>").join("") +
        "</div></div>";
    });
  }

  const proposed = proposedFor(uc), final = finalFor(uc);
  h += '<div class="score"><div class="score-row">' +
    '<span class="state-chip ' + final + '">' + final + "</span>" +
    '<span class="why"><b>' + (uc.kind === "bespoke" ? "State." : "Proposed.") + "</b> " + whyFor(uc) + "</span>" +
    '<span class="ovr-toggle" onclick="App.toggleOvr()">' + (uiOpen[uc.uc_id] ? "▾ hide" : "▸ override / confidence") + "</span></div>" +
    '<div class="ovr ' + (uiOpen[uc.uc_id] ? "open" : "") + '">' +
    "<label>" + (uc.kind === "bespoke" ? "Rationale" : "Override rationale (required to change the proposed state)") + "</label>" +
    '<textarea id="rat" oninput="App.setRationale(this.value)">' + esc(r.rationale) + "</textarea>" +
    '<div class="ovr-grid"><div><label>Confidence</label><div class="conf">' +
    ["LOW", "MED", "HIGH"].map(c => '<button class="' + (r.confidence === c ? "on" : "") + '" onclick="App.setConf(\'' + c + '\')">' + c + "</button>").join("") +
    "</div></div><div><label>Final state</label> " +
    '<select onchange="App.setFinal(this.value)"><option value="">' + (proposed ? "(proposed: " + proposed + ")" : "(choose)") + "</option>" +
    STATES.map(s => '<option value="' + s + '" ' + (r.final_state === s ? "selected" : "") + ">" + s + "</option>").join("") +
    "</select></div></div></div></div>";

  const idx = RUBRIC.findIndex(u => u.uc_id === current);
  h += '<div class="navrow"><button class="btn ghost" ' + (idx === 0 ? "disabled" : "") +
    ' onclick="App.go(RUBRIC[' + (idx - 1) + ']&&RUBRIC[' + (idx - 1) + '].uc_id)">← Previous</button>' +
    '<button class="btn" onclick="App.go(RUBRIC[' + (idx + 1) + ']&&RUBRIC[' + (idx + 1) + '].uc_id)">Save &amp; next →</button></div>';
  document.getElementById("main").innerHTML = h;
}

function render() { renderRail(); renderMain(); }
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c])); }
function toast(m) { const t = document.getElementById("toast"); t.textContent = m; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 1600); }

const App = {
  go(id) { if (id) { current = id; render(); window.scrollTo(0, 0); } },
  answer(qid, v) { const a = resp(current).answers; a[qid] = (a[qid] === v ? undefined : v); if (a[qid] === undefined) delete a[qid]; save(); render(); },
  check(sid, on) { resp(current).answers[sid] = on; save(); renderRail(); },
  toggleOvr() { uiOpen[current] = !uiOpen[current]; renderMain(); },
  setRationale(v) { resp(current).rationale = v; save(); },
  setConf(c) { resp(current).confidence = c; save(); renderMain(); },
  setFinal(v) {
    const uc = RUBRIC_BY_ID[current], r = resp(current);
    if (!v) { r.overridden = false; r.final_state = null; save(); render(); return; }
    const proposed = proposedFor(uc);
    if (proposed && v !== proposed && !(r.rationale || "").trim()) {
      uiOpen[current] = true; renderMain();
      const ta = document.getElementById("rat"); if (ta) ta.classList.add("need");
      toast("Rationale required to override"); return;
    }
    r.overridden = uc.kind === "bespoke" ? true : (v !== proposed);
    r.final_state = v; save(); render();
  },
  exportRecord() {
    const blob = new Blob([JSON.stringify(buildRecord(), null, 2)], {type: "application/json"});
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
    a.download = "assessment-record.json"; a.click(); toast("Record exported");
  },
  importRecord(text) {
    let rec; try { rec = JSON.parse(text); } catch (e) { toast("Import failed: invalid JSON"); return; }
    if (!rec || rec.schema !== SCHEMA) { toast("Import failed: unrecognised schema"); return; }
    const incoming = rec.responses || {};
    Object.keys(incoming).forEach(id => {
      if (!RUBRIC_BY_ID[id]) return;
      const s = incoming[id];
      responses[id] = {answers: s.answers || {}, overridden: !!s.overridden,
        final_state: s.final_state || null, rationale: s.rationale || "", confidence: s.confidence || "MED"};
    });
    save(); render(); toast("Record imported");
  }
};

document.getElementById("importFile").addEventListener("change", e => {
  const f = e.target.files[0]; if (!f) return;
  const rd = new FileReader(); rd.onload = () => App.importRecord(rd.result); rd.readAsText(f); e.target.value = "";
});

loadSaved();
render();
```

- [ ] **Step 2: Rebuild and confirm the build test still passes**

Run: `python3 questionnaire/build_questionnaire.py && python3 -m pytest tests/test_build_questionnaire.py -v`
Expected: `Wrote .../questionnaire.html (... ; 47 use cases)` then PASS (2 tests). The `const App` and `function deriveState` assertions still hold.

- [ ] **Step 3: Manual browser smoke (the engine is already conformance-tested; this checks the glue)**

Run: `open questionnaire/questionnaire.html`
Verify:
1. Rail lists 47 UCs in Functional / Non-functional groups; header shows "x / 47 scored".
2. Open `UC-F-001`: answer Q1 = **No** → state card shows **GAP**, why cites `A1-Q1`. Set Q1=Yes, Q2=No → **PARTIAL**. All Yes → **MET**.
3. Open `UC-F-017` (A0): shows the 3 bespoke criteria as checkboxes + a manual Final-state select; choosing a state updates the chip.
4. Override on a ladder UC: change Final state away from proposed with an empty rationale → blocked + "Rationale required" toast + rationale box highlighted; add rationale → accepted.
5. Export record → `assessment-record.json` downloads; re-open the page (autosave restores answers); Import that file → answers reload, toast "Record imported".

- [ ] **Step 4: Commit**

```bash
git add questionnaire/app.js
git commit -m "feat(ws3): Variant-A wizard — live scoring, A0 manual, override, import/export"
```

---

## Task 6: ADR + backlog + finalize

**Files:** Create `docs/adr/ADR-010-questionnaire-instrument.md`; Modify `meta/IMPROVEMENT-BACKLOG.md`

- [ ] **Step 1: Write** `docs/adr/ADR-010-questionnaire-instrument.md`

```markdown
# ADR-010: Interactive Assessment Instrument (WS-3 slice 1)

**Status:** Accepted
**Date:** 2026-05-29
**Workstream:** WS-3

## Context
The WS-1 rubric (archetype library) needed an operational front door: a way for a
consultant to score a client's posture live and produce a portable assessment artifact.

## Decision
Build a self-contained HTML questionnaire baked from the rubric CSVs by a Python build
step (the build_matrix_viewer.py pattern). The scoring ladder is authored once in
`methodology/scoring.py` (tested reference) and mirrored in `questionnaire/scoring.js`,
both pinned to a shared `scoring-vectors.json` to prevent drift. The instrument exports
and imports a rich `assessment-record.json` (the single source of truth); answers autosave
to localStorage. A0 use cases are scored manually with their bespoke criteria as guidance.
The Variant-A focused wizard is the chosen flow.

## Consequences
- (+) Operational instrument that closes the answer→export→re-import round-trip; engine is
  unit-tested in Python and conformance-tested in JS.
- (+) Presentation is separated from engine + rubric, so the Variant-B worksheet view can
  layer on later without re-architecting.
- (−) Dual engine risks drift — mitigated by the shared vector fixture.
- Deferred: the report adapter (assessment-record → current-state.csv consumed by
  build_matrix_viewer.py), framework-selection UI, Variant-B view, and numeric quantitative
  inputs. The answer→report loop is therefore not yet closed.
```

- [ ] **Step 2: Mark WS-3 done in** `meta/IMPROVEMENT-BACKLOG.md`

Find the heading line beginning `### WS-3 — Interactive instrument (questionnaire UI)` and append
` — ✅ DONE slice 1 (2026-05-29, branch ws3-questionnaire)`. Immediately below that heading line,
insert this paragraph (preserve the existing bullets below it):

```markdown
Delivered (slice 1): self-contained questionnaire baked from the WS-1 rubric
(`questionnaire/`), Python scoring reference (`methodology/scoring.py`) + JS mirror pinned to
shared vectors, Variant-A wizard with live laddering, A0 manual scoring, override+rationale+
confidence, autosave, and import/export of a rich `assessment-record.json`. ADR-010.
**Deferred:** report adapter (record→current-state.csv), framework-selection UI, Variant-B
worksheet view, numeric quantitative inputs.
```

- [ ] **Step 3: Run the full suite + a clean build**

Run: `python3 -m pytest tests/ -q && python3 questionnaire/build_questionnaire.py`
Expected: all tests PASS (WS-1 + WS-2 + the new WS-3 scoring/loader/build/js tests); build prints `47 use cases`.

- [ ] **Step 4: Commit**

```bash
git add docs/adr/ADR-010-questionnaire-instrument.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws3): ADR-010 + mark WS-3 slice 1 done in backlog"
```

- [ ] **Step 5: Push + open PR** (after the final review in subagent-driven-development)

```bash
git push -u origin ws3-questionnaire
gh pr create --title "WS-3: Interactive assessment instrument (slice 1)" \
  --body "Self-contained HTML questionnaire baked from the WS-1 rubric. Live laddering engine (Python reference + inlined JS mirror, drift-guarded by shared vectors), A0 manual scoring, override+rationale+confidence, autosave, and import/export of a rich assessment-record.json. Report adapter / framework-selection UI / Variant-B view / numeric inputs deferred.

Spec: docs/superpowers/specs/2026-05-29-ws3-questionnaire-design.md
Plan: docs/superpowers/plans/2026-05-29-ws3-questionnaire.md"
```

---

## Self-review notes (author)

- **Spec coverage:** §4 architecture → Tasks 1–5; §5 components → all created; §6 rubric resolution → Task 3; §7 ladder → Task 1 (+ JS Task 2); §8 record model → Task 5 (`buildRecord`/`importRecord`); §9 wizard UI → Task 5; §10 error handling → Task 3 (`RubricError`, missing slot), Task 5 (import schema check, localStorage try/catch, override-needs-rationale); §11 testing → Tasks 1–4; §12 process → Task 6.
- **Self-contained guarantee:** `test_build_questionnaire` asserts no `<script src` / `<link` / `http(s)://` and that all injection tokens are consumed.
- **Drift guard:** Python (`test_scoring.py`) and JS (`scoring.test.mjs` via `test_scoring_js.py`) both assert against `questionnaire/scoring-vectors.json`.
- **Type/name consistency:** `derive_state` (py) ↔ `deriveState` (js); both take `(questions, answers)`; `informs_state` values `GAP_PARTIAL`/`PARTIAL_MET`; record fields `archetype/answers/proposed_state/final_state/overridden/rationale/confidence` consistent between §8 and `buildRecord`. Loader keys `kind` ∈ {`ladder`,`bespoke`}, `questions[].{qid,dimension,informs_state,text}`, `sub_criteria[].{sub_id,sub_criterion,question,evidence}` consistent between Task 3 and Task 5 render.
```

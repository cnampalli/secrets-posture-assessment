# Cross-Domain Consolidation View — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone cross-domain report that rolls up every registered domain's ranked vendors by ultimate corporate parent and renders a parent×domain footprint map plus concentration (risk) and consolidation (opportunity) panels.

**Architecture:** Mirror the engine's 4 layers, additive only. New pure logic module `crossdomain.py` builds the model from each domain's `ranked` rows (loaded via the existing `report_io.load_inputs`) and the shared ownership graph (`resilience.parent_of`); `cross_render.py` + `cross-domain-template.html` render a self-contained offline HTML page; `build_cross_domain.py` orchestrates. No existing module is edited.

**Tech Stack:** Python 3 (stdlib + PyYAML via existing loaders), pytest, the project's `brand_fonts`/`brand_tokens` CSS injectors, vanilla JS in the template. Spec: `docs/superpowers/specs/2026-06-05-cross-domain-consolidation-design.md`.

---

## File Structure
- `matrix/crossdomain.py` — pure model builder (`build_crossmap` + private helpers). No I/O.
- `tests/test_crossdomain.py` — unit tests for the logic, synthetic data only.
- `matrix/cross-domain-template.html` — self-contained HTML template with injection slots.
- `matrix/cross_render.py` — loads the template, injects fonts/tokens + model JSON.
- `matrix/build_cross_domain.py` — orchestrator: load all domains → build model → render → write `matrix/cross-domain-report.html`.
- `tests/test_cross_build.py` — build smoke test (end-to-end, asserts spanning parent + HTML).

Tests live in `tests/`; `tests/conftest.py` already puts `matrix/` on `sys.path`, so `import crossdomain` works.

---

### Task 1: Cross-domain model — parent rollup, spans, native_ucs

**Files:**
- Create: `matrix/crossdomain.py`
- Test: `tests/test_crossdomain.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_crossdomain.py
import crossdomain


def _row(slug, name, tid, cov, tt="UC-F"):
    return {"vendor_slug": slug, "vendor_name": name, "target_id": tid,
            "target_type": tt, "coverage": cov, "maturity": "3"}


# ownership: conjur + pam roll up to the cyberark parent; others are their own parent
OWN = {"cyberark-conjur": {"parent": "cyberark"}, "cyberark-pam": {"parent": "cyberark"}}


def _domains_data():
    secrets = [_row("cyberark-conjur", "Conjur", "UC-F-001", "NATIVE"),
               _row("cyberark-conjur", "Conjur", "UC-F-002", "NATIVE"),
               _row("hashicorp-vault", "Vault", "UC-F-001", "NATIVE")]
    pam = [_row("cyberark-pam", "CyberArk PAM", "UC-P-001", "NATIVE"),
           _row("beyondtrust", "BeyondTrust", "UC-P-001", "NATIVE")]
    return [{"slug": "secrets", "label": "Secrets", "ranked": secrets},
            {"slug": "pam", "label": "PAM", "ranked": pam}]


def test_parent_rollup_spans_and_native_ucs():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    assert [d["slug"] for d in m["domains"]] == ["secrets", "pam"]
    cyber = next(p for p in m["parents"] if p["parent"] == "cyberark")
    # cyberark spans both domains via Conjur (secrets) + CyberArk PAM (pam)
    assert cyber["spans"] == 2
    assert cyber["domains_present"] == ["secrets", "pam"]
    assert cyber["by_domain"]["secrets"]["native_ucs"] == 2   # UC-F-001, UC-F-002
    assert cyber["by_domain"]["pam"]["native_ucs"] == 1
    assert [b["slug"] for b in cyber["by_domain"]["secrets"]["brands"]] == ["cyberark-conjur"]
    # single-domain parents have spans == 1
    bt = next(p for p in m["parents"] if p["parent"] == "beyondtrust")
    assert bt["spans"] == 1
    # sorted: spanning parents first
    assert m["parents"][0]["parent"] == "cyberark"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_crossdomain.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'crossdomain'`.

- [ ] **Step 3: Write minimal implementation**

```python
# matrix/crossdomain.py
"""Cross-domain consolidation/concentration view — pure model builder.

Aggregates every registered domain's ranked vendors by ultimate corporate parent
(via the shared ownership graph), so a parent that spans multiple domains — the
cross-cutting signal single-domain analysis misses — surfaces as both a
concentration risk and a consolidation opportunity. Pure: no file I/O.
"""
from matrix_vocab import UC_TYPES
from resilience import parent_of


def _native_ucs(rows):
    """Count of distinct NATIVE use-case target_ids among a set of ranked rows."""
    return len({r["target_id"] for r in rows
                if r.get("coverage") == "NATIVE" and r.get("target_type") in UC_TYPES})


def build_crossmap(domains_data, ownership):
    """Build the cross-domain model.

    domains_data: ordered list of {"slug", "label", "ranked"} (one per domain);
                  `ranked` is that domain's ranked vendor rows (substrate excluded).
    ownership:    {vendor_slug: {"parent": <slug>, ...}} (unlisted vendors are their own parent).
    """
    domains = [{"slug": d["slug"], "label": d["label"]} for d in domains_data]

    # parent -> domain slug -> brand slug -> {"name", "rows"}
    acc = {}
    for d in domains_data:
        for r in d["ranked"]:
            p = parent_of(r["vendor_slug"], ownership)
            brands = acc.setdefault(p, {}).setdefault(d["slug"], {})
            b = brands.setdefault(r["vendor_slug"], {"name": r["vendor_name"], "rows": []})
            b["rows"].append(r)

    parents = []
    for p, doms in acc.items():
        by_domain = {}
        for slug, brands in doms.items():
            allrows = [row for b in brands.values() for row in b["rows"]]
            by_domain[slug] = {
                "brands": [{"slug": s, "name": b["name"]} for s, b in sorted(brands.items())],
                "native_ucs": _native_ucs(allrows),
            }
        parents.append({
            "parent": p,
            "by_domain": by_domain,
            "spans": len(by_domain),
            "domains_present": [d["slug"] for d in domains if d["slug"] in by_domain],
        })
    parents.sort(key=lambda x: (-x["spans"], x["parent"]))

    return {"domains": domains, "parents": parents}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_crossdomain.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add matrix/crossdomain.py tests/test_crossdomain.py
git commit -m "feat(crossdomain): parent rollup + spans + native_ucs model (cross-domain view)"
```

---

### Task 2: Concentration + consolidation panels

**Files:**
- Modify: `matrix/crossdomain.py` (add `_concentration`, `_consolidation`, wire into `build_crossmap` return)
- Test: `tests/test_crossdomain.py` (add tests)

- [ ] **Step 1: Write the failing test**

```python
# append to tests/test_crossdomain.py
def test_concentration_only_lists_spanning_parents():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    conc = m["concentration"]
    assert [c["parent"] for c in conc] == ["cyberark"]      # only spans>=2
    c = conc[0]
    assert c["spans"] == 2 and c["brands_total"] == 2       # Conjur + CyberArk PAM
    assert "CPS 230" in c["note"]


def test_consolidation_ranks_spanning_parents_by_breadth():
    m = crossdomain.build_crossmap(_domains_data(), OWN)
    cons = m["consolidation"]
    assert [c["parent"] for c in cons] == ["cyberark"]
    assert cons[0]["domains"] == 2
    assert cons[0]["native_ucs_total"] == 3                 # 2 (secrets) + 1 (pam)


def test_single_domain_only_yields_empty_panels():
    one = [{"slug": "secrets", "label": "Secrets",
            "ranked": [_row("hashicorp-vault", "Vault", "UC-F-001", "NATIVE")]}]
    m = crossdomain.build_crossmap(one, {})
    assert m["concentration"] == [] and m["consolidation"] == []


def test_empty_domain_does_not_error():
    data = [{"slug": "secrets", "label": "Secrets", "ranked": []},
            {"slug": "pam", "label": "PAM", "ranked": []}]
    m = crossdomain.build_crossmap(data, {})
    assert m["parents"] == [] and m["concentration"] == [] and m["consolidation"] == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_crossdomain.py -q`
Expected: FAIL — `KeyError: 'concentration'` (build_crossmap return lacks the panels).

- [ ] **Step 3: Write minimal implementation**

Add these helpers to `matrix/crossdomain.py` (above `build_crossmap`):

```python
def _label(domains, slug):
    return next((d["label"] for d in domains if d["slug"] == slug), slug)


def _concentration(parents, domains):
    """Parents present in >1 domain — the risk reading."""
    n = len(domains)
    out = []
    for p in parents:
        if p["spans"] < 2:
            continue
        present = ", ".join(_label(domains, s) for s in p["domains_present"])
        out.append({
            "parent": p["parent"],
            "spans": p["spans"],
            "domains_present": p["domains_present"],
            "brands_total": sum(len(v["brands"]) for v in p["by_domain"].values()),
            "note": (f"Spans {p['spans']}/{n} assessed domains ({present}). A 'second source' in one "
                     "domain and the platform in another can be the same ultimate parent — not "
                     "independent (CPS 230 service-provider concentration). Ownership is point-in-time; "
                     "re-verify before client use."),
        })
    return out


def _consolidation(parents):
    """Same spanning parents, ranked by cross-domain breadth — the opportunity reading."""
    out = []
    for p in parents:
        if p["spans"] < 2:
            continue
        out.append({
            "parent": p["parent"],
            "domains": p["spans"],
            "native_ucs_total": sum(v["native_ucs"] for v in p["by_domain"].values()),
            "note": (f"One parent covers needs across {p['spans']} domains "
                     "→ fewer vendors / contracts to manage (decision-support, not a buy list)."),
        })
    out.sort(key=lambda x: (-x["domains"], -x["native_ucs_total"], x["parent"]))
    return out
```

Then change the final `return` of `build_crossmap` to:

```python
    return {"domains": domains, "parents": parents,
            "concentration": _concentration(parents, domains),
            "consolidation": _consolidation(parents)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_crossdomain.py -q`
Expected: PASS (all 5 tests in the file).

- [ ] **Step 5: Commit**

```bash
git add matrix/crossdomain.py tests/test_crossdomain.py
git commit -m "feat(crossdomain): concentration + consolidation panels"
```

---

### Task 3: Template + renderer

**Files:**
- Create: `matrix/cross-domain-template.html`
- Create: `matrix/cross_render.py`

No test in this task (rendering is exercised by Task 4's build smoke test); this task produces the artifacts it needs.

- [ ] **Step 1: Create the template**

Create `matrix/cross-domain-template.html` with exactly this content:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cross-Domain Vendor Map — Concentration &amp; Consolidation</title>
<style>
/*__FONTS__*/
/*__TOKENS__*/
body{font-family:var(--font-body,system-ui,sans-serif);margin:0;background:#faf9f7;color:#1a1a1a}
.wrap{max-width:1100px;margin:0 auto;padding:28px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:#666;font-size:13px;margin-bottom:20px}
table{width:100%;border-collapse:collapse;font-size:13px;background:#fff}
th,td{text-align:left;border-bottom:1px solid #eee;padding:8px 10px;vertical-align:top}
th{border-bottom:2px solid #ccc;font-size:12px}
.chip{display:inline-block;background:#eef;border-radius:10px;padding:1px 8px;margin:1px 2px;font-size:11px}
.hint{color:#777;font-size:11px}
.star{color:#b8860b;font-weight:700}
.muted{color:#888}
.card{background:#fff;border:1px solid #eee;border-left:4px solid var(--l1,#446);border-radius:4px;padding:14px 16px;margin:16px 0}
.card.risk{border-left-color:#a33}
.card h3{margin:0 0 8px;font-size:15px}
.card li{margin:6px 0}
.note{color:#666;font-size:12px}
</style>
</head>
<body>
<div class="wrap">
  <h1>Cross-Domain Vendor Map — by corporate parent</h1>
  <div class="sub">One parent spanning multiple identity-security domains is both a consolidation opportunity and a concentration risk. Decision-support, not a buy list. Ownership data is point-in-time — re-verify before client use.</div>
  <table id="map"><thead></thead><tbody></tbody></table>
  <div id="panels"></div>
</div>
<script>
const CROSSMAP = /*__CROSSMAP__*/{};
function esc(s){return String(s).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function renderMap(){
  const ds=CROSSMAP.domains||[], ps=CROSSMAP.parents||[];
  document.querySelector("#map thead").innerHTML =
    "<tr><th>Corporate parent</th>"+ds.map(d=>"<th>"+esc(d.label)+"</th>").join("")+"<th>Spans</th></tr>";
  document.querySelector("#map tbody").innerHTML = ps.map(p=>{
    const cells = ds.map(d=>{
      const cell=p.by_domain[d.slug];
      if(!cell) return '<td class="muted">—</td>';
      const chips=cell.brands.map(b=>'<span class="chip">'+esc(b.name)+'</span>').join("");
      return "<td>"+chips+'<div class="hint">NATIVE on '+esc(cell.native_ucs)+' UCs</div></td>';
    }).join("");
    const star=p.spans>=2?'<span class="star">★ </span>':"";
    return "<tr><td><b>"+esc(p.parent)+"</b></td>"+cells+"<td>"+star+esc(p.spans)+"</td></tr>";
  }).join("");
}
function renderPanels(){
  const conc=CROSSMAP.concentration||[], cons=CROSSMAP.consolidation||[];
  let h="";
  if(conc.length){
    h+='<div class="card risk"><h3>▶ Concentration (risk reading)</h3><ul>'+
      conc.map(c=>"<li><b>"+esc(c.parent)+"</b> — "+esc(c.note)+"</li>").join("")+"</ul></div>";
  }
  if(cons.length){
    h+='<div class="card"><h3>▶ Consolidation (opportunity reading)</h3><ul>'+
      cons.map(c=>"<li><b>"+esc(c.parent)+"</b> — covers "+esc(c.domains)+" domains, "+
        esc(c.native_ucs_total)+" NATIVE UCs total. "+esc(c.note)+"</li>").join("")+"</ul></div>";
  }
  if(!h) h='<p class="note">No parent spans more than one domain in the current data.</p>';
  document.getElementById("panels").innerHTML=h;
}
renderMap();
renderPanels();
</script>
</body>
</html>
```

- [ ] **Step 2: Create the renderer**

Create `matrix/cross_render.py` with exactly this content:

```python
"""Render the cross-domain report HTML from the model + cross-domain-template.html."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # repo root for brand_fonts/brand_tokens
import brand_fonts
import brand_tokens


def load_template():
    with open(os.path.join(HERE, "cross-domain-template.html"), encoding="utf-8") as fh:
        return fh.read()


def render(model):
    """Assemble the cross-domain report HTML. `model` is crossdomain.build_crossmap output."""
    payload = json.dumps(model, ensure_ascii=False).replace("</", "<\\/")   # </script> safety
    return (load_template()
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__CROSSMAP__*/{}", payload))
```

- [ ] **Step 3: Smoke-check the renderer in isolation**

Run:
```bash
python3 -c "import sys; sys.path.insert(0,'matrix'); import cross_render; \
print('OK' if '/*__CROSSMAP__*/' not in cross_render.render({'domains':[],'parents':[],'concentration':[],'consolidation':[]}) else 'TOKEN-LEFT')"
```
Expected: `OK` (the CROSSMAP token was substituted; no token left behind).

- [ ] **Step 4: Commit**

```bash
git add matrix/cross-domain-template.html matrix/cross_render.py
git commit -m "feat(crossdomain): self-contained report template + renderer"
```

---

### Task 4: Orchestrator + build smoke test

**Files:**
- Create: `matrix/build_cross_domain.py`
- Test: `tests/test_cross_build.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cross_build.py
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import build_cross_domain


def test_build_produces_report_with_spanning_cyberark():
    model, dst = build_cross_domain.build()
    parents = {p["parent"]: p for p in model["parents"]}
    # cyberark owns brands in BOTH the secrets and pam domains → spans 2
    assert "cyberark" in parents and parents["cyberark"]["spans"] == 2
    html = pathlib.Path(dst).read_text(encoding="utf-8")
    assert "Cross-Domain Vendor Map" in html
    assert "CyberArk PAM" in html            # a brand chip rendered
    assert "Concentration (risk reading)" in html
    assert "/*__CROSSMAP__*/" not in html    # token fully substituted
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_cross_build.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'build_cross_domain'`.

- [ ] **Step 3: Write minimal implementation**

```python
# matrix/build_cross_domain.py
#!/usr/bin/env python3
"""Build the standalone cross-domain consolidation/concentration report.

Loads every registered domain's ranked vendors (via report_io.load_inputs), rolls
them up by ultimate corporate parent (crossdomain.build_crossmap), and writes a
self-contained offline HTML report to matrix/cross-domain-report.html.
"""
import os

import domains
import report_io
import crossdomain
import cross_render

HERE = os.path.dirname(os.path.abspath(__file__))
_CFGDIR = os.path.join(HERE, "config")
DST = os.path.join(HERE, "cross-domain-report.html")


def build():
    """Build the model + write the report. Returns (model, dst_path)."""
    ownership = report_io.load_vendor_ownership(_CFGDIR)
    domains_data = []
    for dom in domains.DOMAINS.values():
        inp = report_io.load_inputs(dom.data_dir, None, dom)
        domains_data.append({"slug": dom.slug, "label": dom.label, "ranked": inp["ranked"]})
    model = crossdomain.build_crossmap(domains_data, ownership)
    with open(DST, "w", encoding="utf-8") as f:
        f.write(cross_render.render(model))
    return model, DST


if __name__ == "__main__":
    model, dst = build()
    spanning = [p["parent"] for p in model["parents"] if p["spans"] >= 2]
    print(f"Wrote {dst} ({os.path.getsize(dst)} bytes)")
    print(f"Domains: {[d['slug'] for d in model['domains']]}; parents: {len(model['parents'])}; "
          f"spanning >1 domain: {spanning or 'none'}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_cross_build.py -q`
Expected: PASS.

- [ ] **Step 5: Run the full suite (no regressions) + build the report**

Run: `python3 -m pytest -q && python3 matrix/build_cross_domain.py`
Expected: full suite green; build prints `spanning >1 domain: ['cyberark']`.

- [ ] **Step 6: Commit**

```bash
git add matrix/build_cross_domain.py tests/test_cross_build.py matrix/cross-domain-report.html
git commit -m "feat(crossdomain): orchestrator + build smoke test; report generated"
```

---

### Task 5: Runtime verification + roadmap update

**Files:**
- Modify: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md` (mark X1–X2 done)

- [ ] **Step 1: Runtime-verify the report in a browser (Playwright)**

Write `/tmp/verify_cross.js`:
```javascript
const { chromium } = require('playwright');
(async () => {
  const errors = [];
  const b = await chromium.launch();
  const p = await b.newPage();
  p.on('console', m => { if (m.type()==='error') errors.push('console.error: '+m.text()); });
  p.on('pageerror', e => errors.push('pageerror: '+e.message));
  await p.goto('file://' + process.argv[2], { waitUntil:'networkidle' });
  const rows = await p.$$eval('#map tbody tr', trs => trs.length);
  const star = await p.$eval('#map tbody', el => el.innerText.includes('★'));
  const panels = await p.$eval('#panels', el => el.innerText.slice(0, 120));
  await p.screenshot({ path:'/tmp/cross-domain.png', fullPage:true });
  console.log(JSON.stringify({ jsErrors: errors, rows, hasStar: star, panels }, null, 2));
  await b.close();
})();
```
Run:
```bash
export NODE_PATH="/Users/cnampalli/.npm/_npx/e41f203b7505f1fb/node_modules"
node /tmp/verify_cross.js "$(pwd)/matrix/cross-domain-report.html"
```
Expected: `jsErrors: []`, `rows` ≥ number of distinct parents, `hasStar: true`, panels text mentions Concentration. Eyeball `/tmp/cross-domain.png`.

- [ ] **Step 2: Update the roadmap**

In `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`, change the Phase 2 status-board row to mark the cross-domain consolidation view (X1–X2) **DONE**, and update the "NEXT — the moat" section to note it's built (`matrix/build_cross_domain.py` → `cross-domain-report.html`), with future domains appearing automatically.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/MULTI-DOMAIN-ROADMAP.md
git commit -m "docs(roadmap): cross-domain consolidation view (X1-X2) built"
```

---

## Self-Review
- **Spec coverage:** standalone report (Task 4) ✓; generic over `domains.DOMAINS` (Task 4 iterates the registry) ✓; parent×domain map (Task 1 + template Task 3) ✓; concentration panel (Task 2 + Task 3) ✓; consolidation panel (Task 2 + Task 3) ✓; one `native_ucs` definition (Task 1 `_native_ucs`) ✓; guardrails — ultimate parent (`parent_of`), decision-support framing + point-in-time note (Task 2 notes, Task 3 sub-header) ✓; testing — unit (Tasks 1–2), build smoke (Task 4), runtime verify (Task 5) ✓; `</script>` escaping (Task 3 renderer) ✓.
- **Type consistency:** `build_crossmap(domains_data, ownership)` signature used identically in Tasks 1, 2, 4. Model keys (`domains`, `parents`, `by_domain.<slug>.{brands,native_ucs}`, `concentration`, `consolidation`) match across the logic, template JS, and tests. `parent_of`/`UC_TYPES` imports match `resilience.py`/`matrix_vocab.py`.
- **Placeholders:** none — every step has full code/commands.

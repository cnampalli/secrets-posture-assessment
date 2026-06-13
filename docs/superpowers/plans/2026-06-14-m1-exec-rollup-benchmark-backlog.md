# M1 — Exec roll-up + benchmark + backlog export Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three board-grade outputs to the assessment instrument — a standalone exec roll-up one-pager, a synthetic clearly-labelled AU-FI benchmark layer, and a GAP/PARTIAL→Jira/ADO-importable backlog CSV.

**Architecture:** Follows the existing `matrix/` separation — pure model builders (`rollup.py`, `benchmark.py`, `backlog.py`, no I/O), pure renderer (`rollup_render.py` + `rollup-template.html`), and I/O build entrypoints (`build_exec_rollup.py`, `build_backlog.py`) that mirror `build_cross_domain.py`. The roll-up reuses `report_logic.build_posture_maturity` and `report_logic.build_quick_wins` rather than re-deriving bands or risk rankings.

**Tech Stack:** Python 3.12, stdlib `csv`/`json`, PyYAML (already a dep), pytest. HTML via the existing `brand_fonts`/`brand_tokens` token-replacement pattern.

**Spec:** `docs/superpowers/specs/2026-06-14-m1-exec-rollup-benchmark-backlog-design.md`

---

## File structure

| File | Responsibility |
|---|---|
| `matrix/config/benchmark-cohort.json` (create) | Versioned synthetic per-domain percentile bands + rationale/sources + cohort label. |
| `matrix/benchmark.py` (create) | Pure: load + validate cohort, position a met-% on the bands. |
| `matrix/rollup.py` (create) | Pure: assemble the board roll-up model from posture + risks + benchmark + crossmap. |
| `matrix/rollup_render.py` (create) | Pure: model → self-contained HTML (mirrors `cross_render.py`). |
| `matrix/rollup-template.html` (create) | Brass-Editorial one-pager template with print CSS + JSON payload token. |
| `matrix/build_exec_rollup.py` (create) | I/O entrypoint: load all domains, build model, write `matrix/exec-rollup.html`. |
| `matrix/backlog.py` (create) | Pure: GAP/PARTIAL rows + RFC-4180 CSV serialisation. |
| `matrix/build_backlog.py` (create) | I/O entrypoint: write `<domain>-backlog.csv` per domain + README import note. |
| `matrix/report-template.html` / `matrix/cross-domain-template.html` (modify) | Add a link to `exec-rollup.html`. |
| `.github/workflows/ci.yml` (modify) | Add the two new builds to the byte-identity gate. |
| `tests/test_benchmark.py`, `tests/test_rollup.py`, `tests/test_rollup_render.py`, `tests/test_backlog.py` (create) | Unit coverage. |

**Reused, do not reimplement:**
- `report_logic.build_posture_maturity(anz, ucs, domain_slug)` → `{overall_band, met_pct, counts, p0_open, groups, basis}`.
- `report_logic.build_quick_wins(anz, ucs, reg_rows, scope, limit=3)` → worst-risk-first GAP/PARTIAL top-N, each `{uc_id, short_title, state, risk_band, regulatory_driver}`. **This is `top_3_risks`.**
- `questionnaire.roadmap_generator.seed_risk(priority_fi)` (P0→High, P1→Med, else Low) and `regulatory_driver(uc_id, trace_rows, scope, cap=3)`.
- `report_io.load_inputs(here, None, domain)` → `{all_rows, ranked, ucs, nhis, anz, reg_rows, evidence_catalog}`.
- `crossdomain.build_crossmap(domains_data, ownership)` for the concentration headline.
- Scope convention from `build_matrix_viewer.py:108-112`: `available = list(dict.fromkeys(r["framework_slug"] for r in reg_rows))`; `scope = set(ENGAGEMENT.selected) if not ENGAGEMENT.is_default else set(available)`.

**Conventions to match:**
- `met_pct` from `build_posture_maturity` is a **fraction 0.0–1.0**. The benchmark config stores percentile bands as **integers 0–100**; `benchmark.position` converts via `round(met_pct * 100)`.
- Bands: `ML1` foundational / `ML2` managed / `ML3` optimised (do not invent new band labels).

---

## Task 1: Benchmark cohort config + loader/positioner (pure)

**Files:**
- Create: `matrix/config/benchmark-cohort.json`
- Create: `matrix/benchmark.py`
- Test: `tests/test_benchmark.py`

- [ ] **Step 1: Write the cohort config file**

Create `matrix/config/benchmark-cohort.json` (illustrative synthetic values — every band carries a rationale):

```json
{
  "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
  "basis": "Synthetic, designed-honest reference bands — NOT a measured cohort. Met-% percentile estimates for an AU-FI peer group, intended to be replaced by real cohort percentiles as engagements accumulate.",
  "unit": "met_pct_integer_0_100",
  "domains": {
    "secrets": {
      "p25": 25, "p50": 45, "p75": 65,
      "rationale": "Secrets management is comparatively mature in AU FIs (CPS 234 pressure + vaulting adoption); median ~45% MET reflects partial NHI rotation/discovery coverage.",
      "sources": ["Synthetic estimate; calibrate against CyberArk/HashiCorp AU adoption and APRA CPS 234 thematic reviews when available."]
    },
    "pam": {
      "p25": 30, "p50": 50, "p75": 70,
      "rationale": "PAM is the most established privileged-access discipline; median ~50% MET reflects broad session-brokering adoption with weaker JIT/agentic coverage.",
      "sources": ["Synthetic estimate; calibrate against Gartner PAM MQ adoption signals for AU FIs when available."]
    },
    "iga": {
      "p25": 20, "p50": 40, "p75": 60,
      "rationale": "IGA lags in AU FIs (heavy manual certification, partial JML automation); median ~40% MET reflects that gap.",
      "sources": ["Synthetic estimate; calibrate against AU-FI IGA programme maturity surveys when available."]
    }
  }
}
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_benchmark.py`:

```python
import json
import os

import pytest

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import benchmark  # noqa: E402

CFGDIR = os.path.join(MATRIX, "config")


def test_load_cohort_returns_label_and_domains():
    c = benchmark.load_cohort(CFGDIR)
    assert "illustrative synthetic" in c["cohort_label"].lower()
    assert set(c["domains"]) >= {"secrets", "pam", "iga"}


def test_load_cohort_label_override():
    c = benchmark.load_cohort(CFGDIR, cohort_label_override="Global banks (illustrative)")
    assert c["cohort_label"] == "Global banks (illustrative)"


def test_load_cohort_raises_when_band_missing_rationale(tmp_path):
    bad = {"cohort_label": "x", "basis": "y", "unit": "met_pct_integer_0_100",
           "domains": {"secrets": {"p25": 1, "p50": 2, "p75": 3}}}  # no rationale
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "benchmark-cohort.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="rationale"):
        benchmark.load_cohort(str(cfg))


def test_position_bottom_quartile():
    cohort = benchmark.load_cohort(CFGDIR)
    p = benchmark.position(0.10, "secrets", cohort)   # 10% < p25(25)
    assert p["percentile_band"] == "below p25 (bottom quartile)"
    assert "illustrative synthetic" in p["cohort_label"].lower()


def test_position_band_boundaries_secrets():
    cohort = benchmark.load_cohort(CFGDIR)
    # secrets p25=25 p50=45 p75=65 -> boundaries are inclusive lower edges
    assert benchmark.position(0.25, "secrets", cohort)["percentile_band"] == "p25–p50 (below median)"
    assert benchmark.position(0.45, "secrets", cohort)["percentile_band"] == "p50–p75 (above median)"
    assert benchmark.position(0.65, "secrets", cohort)["percentile_band"] == "above p75 (top quartile)"


def test_position_unknown_domain_no_baseline():
    cohort = benchmark.load_cohort(CFGDIR)
    p = benchmark.position(0.50, "nonexistent", cohort)
    assert p["percentile_band"] == "no cohort baseline"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_benchmark.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'benchmark'`.

- [ ] **Step 4: Write `matrix/benchmark.py`**

```python
"""Synthetic, clearly-labelled benchmark cohort — pure model helpers (no rendering).

Loads versioned per-domain met-% percentile bands from config/benchmark-cohort.json
and positions a domain's assessed met-% against them. The bands are a designed-honest
SYNTHETIC baseline (not a measured cohort); the loader refuses any band that lacks a
documented rationale so the honesty contract can't silently erode.
"""
import json
import os

_BANDS = ("p25", "p50", "p75")


def load_cohort(cfgdir, cohort_label_override=None):
    """Read benchmark-cohort.json from `cfgdir`. Validates that every domain band
    set carries p25/p50/p75 and a non-empty `rationale`; raises ValueError otherwise
    (honesty gate). `cohort_label_override` (e.g. from engagement config) replaces the
    displayed cohort label without touching the bands."""
    path = os.path.join(cfgdir, "benchmark-cohort.json")
    with open(path, encoding="utf-8") as fh:
        cohort = json.load(fh)
    for dom, band in cohort.get("domains", {}).items():
        for k in _BANDS:
            if k not in band:
                raise ValueError(f"benchmark cohort domain {dom!r} missing band {k!r}")
        if not (band.get("rationale") or "").strip():
            raise ValueError(f"benchmark cohort domain {dom!r} missing rationale "
                             "(synthetic bands must be justified)")
    if cohort_label_override:
        cohort["cohort_label"] = cohort_label_override
    return cohort


def position(met_pct, domain_slug, cohort):
    """Map a domain's met-% (fraction 0..1) onto the cohort quartile bands. Returns
    {percentile_band, cohort_label, basis_note}. Unknown domain -> explicit
    'no cohort baseline' (never invents a band)."""
    band = cohort.get("domains", {}).get(domain_slug)
    label = cohort.get("cohort_label", "")
    basis = cohort.get("basis", "")
    if not band:
        return {"percentile_band": "no cohort baseline", "cohort_label": label,
                "basis_note": basis}
    pct = round((met_pct or 0.0) * 100)
    if pct < band["p25"]:
        pb = "below p25 (bottom quartile)"
    elif pct < band["p50"]:
        pb = "p25–p50 (below median)"
    elif pct < band["p75"]:
        pb = "p50–p75 (above median)"
    else:
        pb = "above p75 (top quartile)"
    return {"percentile_band": pb, "cohort_label": label, "basis_note": basis}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_benchmark.py -v`
Expected: PASS (6 passed).

- [ ] **Step 6: Commit**

```bash
git add matrix/config/benchmark-cohort.json matrix/benchmark.py tests/test_benchmark.py
git commit -m "feat(m1): synthetic AU-FI benchmark cohort loader + positioner"
```

---

## Task 2: Roll-up model builder (pure)

**Files:**
- Create: `matrix/rollup.py`
- Test: `tests/test_rollup.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_rollup.py`:

```python
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import rollup  # noqa: E402


def _domain_input(slug, label, met_pct, band, risks):
    return {
        "slug": slug, "label": label,
        "posture": {"overall_band": band, "met_pct": met_pct,
                    "counts": {"met": 1, "partial": 1, "gap": 1, "pending": 0},
                    "p0_open": 1, "groups": [], "basis": "designed convention"},
        "top_3_risks": risks,
        "benchmark": {"percentile_band": "p25–p50 (below median)",
                      "cohort_label": "AU FIs (illustrative synthetic baseline)",
                      "basis_note": "synthetic"},
    }


def test_build_rollup_has_one_entry_per_domain():
    domains = [
        _domain_input("secrets", "Secrets", 0.45, "ML2", [{"uc_id": "UC-S-001", "short_title": "Rotation"}]),
        _domain_input("pam", "PAM", 0.50, "ML2", []),
    ]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    assert len(model["domains"]) == 2
    assert {d["slug"] for d in model["domains"]} == {"secrets", "pam"}


def test_trend_is_baseline_with_no_arrow():
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    trend = model["domains"][0]["trend"]
    assert trend["state"] == "baseline"
    assert "first assessment" in trend["note"].lower()
    # no directional glyph anywhere in the trend payload
    assert not any(g in repr(trend) for g in ("↑", "↓", "→", "▲", "▼"))


def test_overall_band_is_worst_across_domains():
    domains = [
        _domain_input("secrets", "Secrets", 0.80, "ML3", []),
        _domain_input("iga", "IGA", 0.20, "ML1", []),
    ]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    assert model["overall"]["lowest_band"] == "ML1"


def test_crossmap_headline_names_top_spanning_parent():
    cm = {"domains": [{"slug": "secrets"}, {"slug": "pam"}],
          "parents": [{"parent": "cyberark", "display": "CyberArk", "spans": 2}]}
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap=cm)
    assert "CyberArk" in model["overall"]["concentration_headline"]


def test_crossmap_headline_when_no_span():
    cm = {"domains": [{"slug": "secrets"}], "parents": [{"parent": "x", "display": "X", "spans": 1}]}
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap=cm)
    assert "no" in model["overall"]["concentration_headline"].lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_rollup.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rollup'`.

- [ ] **Step 3: Write `matrix/rollup.py`**

```python
"""Board-grade exec roll-up — pure model builder (no I/O).

Consumes per-domain posture (report_logic.build_posture_maturity), worst-risk-first
top risks (report_logic.build_quick_wins), and a benchmark position (benchmark.position),
plus the cross-domain concentration map (crossdomain.build_crossmap), and assembles the
one-pager model the renderer consumes. Trend is a deliberate BASELINE marker — no
direction is implied because no prior dated assessment exists yet (M4 fills this)."""

_BAND_RANK = {"ML1": 1, "ML2": 2, "ML3": 3}

_BASELINE_TREND = {
    "state": "baseline",
    "note": "First assessment — trend activates at the next dated re-baseline.",
}


def _lowest_band(domains):
    bands = [d["posture"]["overall_band"] for d in domains if d.get("posture")]
    if not bands:
        return "ML1"
    return min(bands, key=lambda b: _BAND_RANK.get(b, 1))


def _concentration_headline(crossmap):
    spanning = [p for p in crossmap.get("parents", []) if p.get("spans", 0) >= 2]
    if not spanning:
        return ("No single corporate parent spans more than one assessed domain "
                "(no cross-domain concentration signal at this scope).")
    top = max(spanning, key=lambda p: p["spans"])
    return (f"{top['display']} spans {top['spans']} assessed domains — a cross-domain "
            "service-provider concentration signal (CPS 230). Ownership is point-in-time.")


def build_exec_rollup(domains, crossmap):
    """Assemble the board roll-up model. `domains` is a list of
    {slug, label, posture, top_3_risks, benchmark}; `crossmap` is
    crossdomain.build_crossmap output. Returns
    {domains:[{slug,label,overall_band,met_pct,counts,p0_open,top_3_risks,benchmark,trend}],
     overall:{lowest_band,total_p0_open,concentration_headline}}."""
    out_domains = []
    total_p0 = 0
    for d in domains:
        posture = d["posture"]
        total_p0 += posture.get("p0_open", 0)
        out_domains.append({
            "slug": d["slug"],
            "label": d["label"],
            "overall_band": posture["overall_band"],
            "met_pct": posture["met_pct"],
            "counts": posture["counts"],
            "p0_open": posture.get("p0_open", 0),
            "top_3_risks": d.get("top_3_risks", []),
            "benchmark": d["benchmark"],
            "trend": dict(_BASELINE_TREND),
        })
    return {
        "domains": out_domains,
        "overall": {
            "lowest_band": _lowest_band(domains),
            "total_p0_open": total_p0,
            "concentration_headline": _concentration_headline(crossmap),
        },
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rollup.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add matrix/rollup.py tests/test_rollup.py
git commit -m "feat(m1): exec roll-up model builder (baseline trend, worst-band, concentration headline)"
```

---

## Task 3: Roll-up renderer + template (pure)

**Files:**
- Create: `matrix/rollup-template.html`
- Create: `matrix/rollup_render.py`
- Test: `tests/test_rollup_render.py`

- [ ] **Step 1: Write the template**

Create `matrix/rollup-template.html` (mirrors the cross-domain template's token contract: `/*__FONTS__*/`, `/*__TOKENS__*/`, and a JSON payload token `/*__ROLLUP__*/{}`). The client script renders the board table from the embedded model:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Executive Roll-up — Cross-Domain Posture</title>
<style>/*__FONTS__*/</style>
<style>/*__TOKENS__*/</style>
<style>
  body { font-family: var(--font-body, serif); color: var(--ink, #1a1a1a);
         background: var(--paper, #faf8f3); margin: 0; padding: 2rem; }
  .sheet { max-width: 1000px; margin: 0 auto; }
  h1 { font-family: var(--font-display, serif); font-size: 1.9rem; margin: 0 0 .25rem; }
  .sub { color: #555; margin: 0 0 1.5rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th, td { text-align: left; padding: .6rem .5rem; border-bottom: 1px solid #ddd; vertical-align: top; }
  th { font-size: .75rem; text-transform: uppercase; letter-spacing: .04em; color: #666; }
  .band { font-weight: 700; }
  .trend { color: #777; font-style: italic; }
  .bench-note, .basis { font-size: .75rem; color: #777; }
  .headline { background: #f3efe6; border-left: 3px solid #b5a36a; padding: .75rem 1rem; margin: 1rem 0; }
  ul.risks { margin: 0; padding-left: 1.1rem; }
  ul.risks li { font-size: .85rem; }
  @media print { body { padding: 0; } .sheet { max-width: none; } @page { size: A4; margin: 12mm; } }
</style>
</head>
<body>
<div class="sheet">
  <h1>Executive Roll-up</h1>
  <p class="sub" id="overall"></p>
  <div class="headline" id="headline"></div>
  <table>
    <thead><tr><th>Domain</th><th>Maturity</th><th>Coverage</th><th>Top risks</th><th>Benchmark</th><th>Trend</th></tr></thead>
    <tbody id="rows"></tbody>
  </table>
  <p class="basis" id="basis"></p>
</div>
<script id="model" type="application/json">/*__ROLLUP__*/{}</script>
<script>
  const model = JSON.parse(document.getElementById("model").textContent);
  const o = model.overall;
  document.getElementById("overall").textContent =
    `Lowest maturity band across domains: ${o.lowest_band}. Open P0 items: ${o.total_p0_open}.`;
  document.getElementById("headline").textContent = o.concentration_headline;
  const esc = s => String(s == null ? "" : s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  document.getElementById("rows").innerHTML = model.domains.map(d => {
    const risks = (d.top_3_risks || []).map(r => `<li>${esc(r.short_title)}</li>`).join("") || "<li>No open gaps</li>";
    return `<tr>
      <td>${esc(d.label)}</td>
      <td class="band">${esc(d.overall_band)}</td>
      <td>${Math.round((d.met_pct||0)*100)}% MET</td>
      <td><ul class="risks">${risks}</ul></td>
      <td>${esc(d.benchmark.percentile_band)}<br><span class="bench-note">${esc(d.benchmark.cohort_label)}</span></td>
      <td class="trend">Baseline</td>
    </tr>`;
  }).join("");
  const b = model.domains[0] && model.domains[0].benchmark;
  document.getElementById("basis").textContent = b ? `Benchmark basis: ${b.basis_note}` : "";
</script>
</body>
</html>
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_rollup_render.py`:

```python
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import rollup_render  # noqa: E402

MODEL = {
    "domains": [
        {"slug": "secrets", "label": "Secrets", "overall_band": "ML2", "met_pct": 0.45,
         "counts": {"met": 1, "partial": 1, "gap": 1, "pending": 0}, "p0_open": 1,
         "top_3_risks": [{"uc_id": "UC-S-001", "short_title": "Rotation"}],
         "benchmark": {"percentile_band": "p25–p50 (below median)",
                       "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
                       "basis_note": "Synthetic, designed-honest reference bands."},
         "trend": {"state": "baseline", "note": "First assessment — trend activates at the next dated re-baseline."}},
        {"slug": "pam", "label": "PAM", "overall_band": "ML2", "met_pct": 0.50,
         "counts": {"met": 2, "partial": 0, "gap": 0, "pending": 0}, "p0_open": 0,
         "top_3_risks": [],
         "benchmark": {"percentile_band": "p50–p75 (above median)",
                       "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
                       "basis_note": "Synthetic, designed-honest reference bands."},
         "trend": {"state": "baseline", "note": "First assessment — trend activates at the next dated re-baseline."}},
    ],
    "overall": {"lowest_band": "ML2", "total_p0_open": 1,
                "concentration_headline": "CyberArk spans 2 assessed domains — a cross-domain concentration signal (CPS 230)."},
}


def test_render_is_self_contained_html():
    html = rollup_render.render(MODEL)
    assert html.lstrip().startswith("<!doctype html>")
    assert "/*__ROLLUP__*/" not in html  # token was substituted
    assert "src=\"http" not in html and "href=\"http" not in html  # no external refs


def test_render_includes_synthetic_cohort_label():
    html = rollup_render.render(MODEL)
    assert "illustrative synthetic baseline" in html.lower()


def test_render_has_no_directional_trend_glyph():
    html = rollup_render.render(MODEL)
    assert not any(g in html for g in ("↑", "↓", "▲", "▼"))


def test_render_embeds_all_domains():
    html = rollup_render.render(MODEL)
    assert "Secrets" in html and "PAM" in html
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_rollup_render.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'rollup_render'`.

- [ ] **Step 4: Write `matrix/rollup_render.py`**

```python
"""Render the exec roll-up HTML from the model + rollup-template.html.

Mirrors cross_render.render: substitutes the brand font/token CSS and embeds the
model as a </script>-safe JSON payload. Pure (no file writes)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # repo root for brand_fonts/brand_tokens
import brand_fonts
import brand_tokens


def load_template():
    with open(os.path.join(HERE, "rollup-template.html"), encoding="utf-8") as fh:
        return fh.read()


def render(model):
    """Assemble the exec roll-up HTML. `model` is rollup.build_exec_rollup output."""
    payload = json.dumps(model, ensure_ascii=False).replace("</", "<\\/")
    return (load_template()
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__ROLLUP__*/{}", payload))
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rollup_render.py -v`
Expected: PASS (4 passed).

- [ ] **Step 6: Commit**

```bash
git add matrix/rollup-template.html matrix/rollup_render.py tests/test_rollup_render.py
git commit -m "feat(m1): exec roll-up renderer + Brass one-pager template"
```

---

## Task 4: Build entrypoint for the exec roll-up (I/O)

**Files:**
- Create: `matrix/build_exec_rollup.py`

- [ ] **Step 1: Write `matrix/build_exec_rollup.py`**

Mirrors `build_cross_domain.py` + the scope convention from `build_matrix_viewer.py:108-112`:

```python
#!/usr/bin/env python3
"""Build the standalone executive roll-up one-pager.

For every registered domain: loads inputs, computes posture/maturity and the
worst-risk-first top-3 risks, positions met-% against the synthetic benchmark cohort,
and (using the cross-domain concentration map) writes a self-contained one-pager to
matrix/exec-rollup.html."""
import os

import domains
import report_io
import report_logic
import crossdomain
import benchmark
import rollup
import rollup_render
import engagement_config as _ec
import pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
_CFGDIR = os.path.join(HERE, "config")
_PRESETS = pathlib.Path(_CFGDIR) / "presets"
DST = os.path.join(HERE, "exec-rollup.html")


def build():
    """Build the model + write the report. Returns (model, dst_path)."""
    ownership = report_io.load_vendor_ownership(_CFGDIR)
    cohort = benchmark.load_cohort(_CFGDIR)
    rollup_domains = []
    crossmap_inputs = []
    for dom in domains.DOMAINS.values():
        inp = report_io.load_inputs(dom.data_dir, None, dom)
        reg_rows = inp["reg_rows"]
        available = list(dict.fromkeys(r["framework_slug"] for r in reg_rows))
        engagement = _ec.resolve(preset=None, config_path=None, cli_frameworks=None,
                                 available=available, presets_dir=_PRESETS)
        scope = set(engagement.selected) if not engagement.is_default else set(available)
        posture = report_logic.build_posture_maturity(inp["anz"], inp["ucs"], dom.slug)
        top_risks = report_logic.build_quick_wins(inp["anz"], inp["ucs"], reg_rows, scope, limit=3)
        rollup_domains.append({
            "slug": dom.slug, "label": dom.label, "posture": posture,
            "top_3_risks": top_risks,
            "benchmark": benchmark.position(posture["met_pct"], dom.slug, cohort),
        })
        # matrix-less domains (no ranked vendors) don't join the concentration map,
        # exactly as build_cross_domain.py skips them.
        if inp["ranked"]:
            crossmap_inputs.append({"slug": dom.slug, "label": dom.label, "ranked": inp["ranked"]})
    crossmap = crossdomain.build_crossmap(crossmap_inputs, ownership)
    model = rollup.build_exec_rollup(rollup_domains, crossmap)
    with open(DST, "w", encoding="utf-8") as f:
        f.write(rollup_render.render(model))
    return model, DST


if __name__ == "__main__":
    model, dst = build()
    print(f"Wrote {dst} ({os.path.getsize(dst)} bytes)")
    print(f"Domains: {[d['slug'] for d in model['domains']]}; "
          f"lowest band: {model['overall']['lowest_band']}; "
          f"open P0: {model['overall']['total_p0_open']}")
```

> The `_ec.resolve(...)` keyword form above is copied verbatim from `build_matrix_viewer.py:60-66` (signature `resolve(preset, config_path, cli_frameworks, available, presets_dir)`); `preset=None`/`config_path=None`/`cli_frameworks=None` selects the default engagement.

- [ ] **Step 2: Run the build (integration check)**

Run: `cd matrix && python3 build_exec_rollup.py && cd ..`
Expected: prints `Wrote .../exec-rollup.html (NNNNN bytes)` and a domains/band/P0 summary line; `matrix/exec-rollup.html` exists.

- [ ] **Step 3: Verify the artifact honesty contract**

Run: `grep -c "illustrative synthetic baseline" matrix/exec-rollup.html`
Expected: ≥ 1 (the synthetic cohort label is present in the built artifact).

Run: `python3 - <<'PY'`
```python
html = open("matrix/exec-rollup.html", encoding="utf-8").read()
assert not any(g in html for g in ("↑", "↓", "▲", "▼")), "directional trend glyph leaked into artifact"
print("OK: no directional trend glyph")
PY
```
Expected: `OK: no directional trend glyph`.

- [ ] **Step 4: Commit (including the built artifact, per the byte-identity gate convention)**

```bash
git add matrix/build_exec_rollup.py matrix/exec-rollup.html
git commit -m "feat(m1): exec roll-up build entrypoint + generated one-pager artifact"
```

---

## Task 5: Backlog row builder + CSV serialisation (pure)

**Files:**
- Create: `matrix/backlog.py`
- Test: `tests/test_backlog.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_backlog.py`:

```python
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import backlog  # noqa: E402

UCS = [
    {"uc_id": "UC-S-001", "short_title": "Secret rotation", "priority_fi": "P0", "story": "Rotate secrets."},
    {"uc_id": "UC-S-002", "short_title": "Discovery", "priority_fi": "P1", "story": "Find secrets."},
    {"uc_id": "UC-S-003", "short_title": "Audit, with \"quotes\"", "priority_fi": "P2", "story": "Log access."},
    {"uc_id": "UC-S-004", "short_title": "Already done", "priority_fi": "P0", "story": "n/a"},
]
ANZ = [
    {"uc_id": "UC-S-001", "current_state": "GAP", "recommendation": "Add rotation."},
    {"uc_id": "UC-S-002", "current_state": "PARTIAL", "recommendation": "Extend discovery."},
    {"uc_id": "UC-S-003", "current_state": "GAP", "recommendation": "Enable audit."},
    {"uc_id": "UC-S-004", "current_state": "MET", "recommendation": ""},
]
REG = []  # no regulatory trace in this fixture
SCOPE = set()


def test_only_gap_and_partial_exported():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    ids = {r["UC-ID"] for r in rows}
    assert ids == {"UC-S-001", "UC-S-002", "UC-S-003"}  # MET UC-S-004 excluded


def test_priority_sorts_p0_first():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    assert rows[0]["UC-ID"] == "UC-S-001"   # P0 -> Highest, top of list
    assert rows[0]["Priority"] == "Highest"
    assert rows[-1]["Priority"] == "Medium"  # P2


def test_row_has_all_both_tool_columns():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    expected = {"Summary", "Work Item Type", "Description", "Priority", "Labels",
                "UC-ID", "Domain", "Regulatory-Driver", "State"}
    assert set(rows[0]) == expected
    assert rows[0]["Work Item Type"] == "Task"
    assert rows[0]["Domain"] == "secrets"


def test_to_csv_escapes_quotes_and_commas():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    out = backlog.to_csv(rows)
    parsed = list(csv.DictReader(io.StringIO(out)))
    titles = {r["UC-ID"]: r["Summary"] for r in parsed}
    assert 'quotes' in titles["UC-S-003"]      # round-trips through the quoting
    assert parsed[0]["UC-ID"] == "UC-S-001"     # header + order preserved


def test_to_csv_empty_rows_is_header_only():
    out = backlog.to_csv([])
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 1  # header row only
    assert "Summary" in lines[0]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_backlog.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backlog'`.

- [ ] **Step 3: Write `matrix/backlog.py`**

```python
"""GAP/PARTIAL backlog export — pure model builder + CSV serialisation (no file I/O).

Turns a domain's open use cases (GAP + PARTIAL only) into work-item rows whose columns
import cleanly into BOTH Jira and Azure DevOps. Priority is carried from the use-case
priority_fi so P0s sort to the top. CSV serialisation is RFC-4180 (csv module)."""
import csv
import io
import os
import sys

# regulatory_driver lives in questionnaire/ — make the repo root importable.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.append(_ROOT)
from questionnaire.roadmap_generator import regulatory_driver

_OPEN_STATES = ("GAP", "PARTIAL")

COLUMNS = ["Summary", "Work Item Type", "Description", "Priority", "Labels",
           "UC-ID", "Domain", "Regulatory-Driver", "State"]

# priority_fi -> (display priority, sort rank). Jira accepts these names directly;
# the README documents the ADO numeric mapping (Highest->1 ... Low->4).
_PRIORITY = {"P0": ("Highest", 0), "P1": ("High", 1), "P2": ("Medium", 2)}
_PRIORITY_DEFAULT = ("Low", 3)


def build_backlog_rows(anz, ucs, reg_rows, scope, domain_slug):
    """Every GAP/PARTIAL use case -> one work-item row. Sorted P0-first, then by UC id."""
    uc_by_id = {u["uc_id"]: u for u in ucs}
    rows = []
    for a in anz:
        state = (a.get("current_state") or "").strip()
        if state not in _OPEN_STATES:
            continue
        uc_id = a["uc_id"]
        uc = uc_by_id.get(uc_id, {})
        title = uc.get("short_title", uc_id)
        prio_label, prio_rank = _PRIORITY.get((uc.get("priority_fi") or "").strip(),
                                              _PRIORITY_DEFAULT)
        drivers = regulatory_driver(uc_id, reg_rows, scope)
        driver_str = "; ".join(d["control_code"] for d in drivers)
        desc = (a.get("recommendation") or uc.get("story") or "").strip()
        labels = " ".join([domain_slug, state.lower()]
                          + [d["framework_slug"] for d in drivers])
        rows.append({
            "Summary": f"[{state}] {title}",
            "Work Item Type": "Task",
            "Description": desc,
            "Priority": prio_label,
            "Labels": labels,
            "UC-ID": uc_id,
            "Domain": domain_slug,
            "Regulatory-Driver": driver_str,
            "State": state,
            "_rank": prio_rank,
        })
    rows.sort(key=lambda r: (r["_rank"], r["UC-ID"]))
    for r in rows:
        r.pop("_rank")
    return rows


def to_csv(rows):
    """Serialise rows to an RFC-4180 CSV string (header always emitted)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_backlog.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add matrix/backlog.py tests/test_backlog.py
git commit -m "feat(m1): GAP/PARTIAL backlog rows + Jira/ADO-neutral CSV serialisation"
```

---

## Task 6: Build entrypoint for backlog CSVs + import-mapping note (I/O)

**Files:**
- Create: `matrix/build_backlog.py`
- Create: `matrix/BACKLOG-IMPORT.md`

- [ ] **Step 1: Write `matrix/build_backlog.py`**

```python
#!/usr/bin/env python3
"""Build per-domain backlog CSVs (GAP/PARTIAL work items) next to each domain report.

Writes <data_dir>/<slug>-backlog.csv for every registered domain, importable into
both Jira and Azure DevOps (see BACKLOG-IMPORT.md for the column mapping)."""
import os
import pathlib

import domains
import report_io
import backlog
import engagement_config as _ec

_PRESETS = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / "config" / "presets"


def build():
    """Write one CSV per domain. Returns [(slug, path, row_count)]."""
    results = []
    for dom in domains.DOMAINS.values():
        inp = report_io.load_inputs(dom.data_dir, None, dom)
        reg_rows = inp["reg_rows"]
        available = list(dict.fromkeys(r["framework_slug"] for r in reg_rows))
        engagement = _ec.resolve(preset=None, config_path=None, cli_frameworks=None,
                                 available=available, presets_dir=_PRESETS)
        scope = set(engagement.selected) if not engagement.is_default else set(available)
        rows = backlog.build_backlog_rows(inp["anz"], inp["ucs"], reg_rows, scope, dom.slug)
        dst = os.path.join(dom.data_dir, f"{dom.slug}-backlog.csv")
        with open(dst, "w", encoding="utf-8", newline="") as f:
            f.write(backlog.to_csv(rows))
        results.append((dom.slug, dst, len(rows)))
    return results


if __name__ == "__main__":
    for slug, dst, n in build():
        print(f"Wrote {dst} ({n} backlog rows)")
```

> **Note:** the `_ec.resolve(...)` keyword form matches `build_matrix_viewer.py:60-66` (same as Task 4). `newline=""` on `open` is required so the `csv` module controls line endings.

- [ ] **Step 2: Write the import-mapping note**

Create `matrix/BACKLOG-IMPORT.md`:

```markdown
# Backlog CSV import mapping

`build_backlog.py` writes one `<domain>-backlog.csv` per domain (GAP + PARTIAL use
cases, P0s first). One neutral schema imports into both trackers.

| CSV column | Jira import field | Azure DevOps import field |
|---|---|---|
| Summary | Summary | Title |
| Work Item Type | Issue Type (`Task`) | Work Item Type (`Task`) |
| Description | Description | Description |
| Priority | Priority (`Highest`/`High`/`Medium`/`Low`) | Priority (map `Highest`→1, `High`→2, `Medium`→3, `Low`→4) |
| Labels | Labels (space-separated) | Tags (set delimiter to space, or replace spaces with `;`) |
| UC-ID | Labels / custom field | Tags / custom field |
| Domain | Labels / Component | Area / Tags |
| Regulatory-Driver | Description / custom field | Description / custom field |
| State | Labels / custom field | Tags / custom field |

**Jira:** Settings → System → External System Import → CSV. Map columns as above.
**Azure DevOps:** Boards → Work items → Import Work Items (CSV). Priority must be numeric;
apply the mapping above during import or with a quick find-replace.
```

- [ ] **Step 3: Run the build (integration check)**

Run: `cd matrix && python3 build_backlog.py && cd ..`
Expected: prints one `Wrote .../<slug>-backlog.csv (N backlog rows)` line per domain.

- [ ] **Step 4: Verify a CSV parses and excludes MET**

Run: `python3 - <<'PY'`
```python
import csv, glob
for path in glob.glob("matrix/domains/*/*-backlog.csv") + glob.glob("matrix/*-backlog.csv"):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    assert all(r["State"] in ("GAP", "PARTIAL") for r in rows), path
    print(f"{path}: {len(rows)} rows, states OK")
PY
```
Expected: one OK line per CSV (paths depend on where each domain's `data_dir` points).

- [ ] **Step 5: Commit (including generated CSVs, for the byte-identity gate)**

```bash
git add matrix/build_backlog.py matrix/BACKLOG-IMPORT.md $(git ls-files --others --exclude-standard 'matrix/**/*-backlog.csv')
git add -A 'matrix/**/*-backlog.csv'
git commit -m "feat(m1): per-domain backlog CSV build + Jira/ADO import mapping"
```

---

## Task 7: Link the roll-up from the domain + cross-domain reports

**Files:**
- Modify: `matrix/report-template.html`
- Modify: `matrix/cross-domain-template.html`

- [ ] **Step 1: Locate the header/nav region in each template**

Run: `grep -n "<h1\|<header\|nav\|cross-domain-report.html" matrix/report-template.html matrix/cross-domain-template.html`
Expected: identifies the masthead/nav block where a sibling-report link belongs.

- [ ] **Step 2: Add the roll-up link to `matrix/report-template.html`**

In the masthead/nav block found in Step 1, add (adjust the surrounding tag to match the existing nav markup):

```html
<a class="report-link" href="exec-rollup.html">Executive roll-up ↗</a>
```

- [ ] **Step 3: Add the same link to `matrix/cross-domain-template.html`**

```html
<a class="report-link" href="exec-rollup.html">Executive roll-up ↗</a>
```

- [ ] **Step 4: Rebuild affected artifacts and confirm the link is present**

Run:
```bash
cd matrix
python3 build_matrix_viewer.py --domain secrets
python3 build_cross_domain.py
cd ..
grep -c "exec-rollup.html" matrix/cross-domain-report.html
```
Expected: ≥ 1.

> The `↗` here is a link affordance in report navigation, NOT a trend direction in the
> roll-up itself — the roll-up's no-directional-glyph test (Task 3/4) covers `exec-rollup.html`
> only and is unaffected.

- [ ] **Step 5: Rebuild ALL byte-identity artifacts so the gate stays green**

Run:
```bash
cd matrix
python3 build_matrix_viewer.py --domain secrets
python3 build_matrix_viewer.py --domain pam
python3 build_matrix_viewer.py --domain iga
python3 build_cross_domain.py
python3 build_exec_rollup.py
python3 build_backlog.py
cd ..
git status --short
```
Expected: only the intended report/CSV artifacts changed.

- [ ] **Step 6: Commit**

```bash
git add matrix/report-template.html matrix/cross-domain-template.html
git add -A 'matrix/**/*-report.html' 'matrix/*-report.html' matrix/cross-domain-report.html
git commit -m "feat(m1): link executive roll-up from domain + cross-domain reports"
```

---

## Task 8: Wire the new builds into CI

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Add the roll-up + backlog builds to the byte-identity step**

In `.github/workflows/ci.yml`, the "Reports rebuild byte-identical" step (lines 33-39) currently runs the viewer + cross-domain builds then `git diff --exit-code`. Add the two new builds **before** the `git diff --exit-code` line:

```yaml
      - name: Reports rebuild byte-identical
        run: |
          python3 matrix/build_matrix_viewer.py --domain secrets
          python3 matrix/build_matrix_viewer.py --domain pam
          python3 matrix/build_matrix_viewer.py --domain iga
          python3 matrix/build_cross_domain.py
          python3 matrix/build_exec_rollup.py
          python3 matrix/build_backlog.py
          git diff --exit-code
```

- [ ] **Step 2: Verify the full gate passes locally (the CI equivalent)**

Run:
```bash
python3 matrix/validate_data.py
python3 matrix/validate_data.py --data-dir matrix/domains/iga
python3 matrix/validate_data.py --data-dir matrix/domains/pam
python3 -m pytest tests/ -q
python3 matrix/build_matrix_viewer.py --domain secrets
python3 matrix/build_matrix_viewer.py --domain pam
python3 matrix/build_matrix_viewer.py --domain iga
python3 matrix/build_cross_domain.py
python3 matrix/build_exec_rollup.py
python3 matrix/build_backlog.py
git diff --exit-code
```
Expected: pytest all-pass; `git diff --exit-code` returns 0 (clean) — the committed artifacts are byte-identical to a fresh rebuild.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci(m1): gate exec roll-up + backlog builds on every push"
```

---

## Final verification

- [ ] **Step 1: Full suite green**

Run: `python3 -m pytest tests/ -q`
Expected: all pass (incl. the four new test files).

- [ ] **Step 2: Clean rebuild is byte-identical**

Run the Task 8 Step 2 block again.
Expected: `git diff --exit-code` returns 0.

- [ ] **Step 3: Honesty contract holds in the artifact**

Run:
```bash
grep -c "illustrative synthetic baseline" matrix/exec-rollup.html
python3 - <<'PY'
html = open("matrix/exec-rollup.html", encoding="utf-8").read()
assert not any(g in html for g in ("↑", "↓", "▲", "▼")), "trend glyph leaked"
assert "First assessment" in html, "baseline trend note missing"
print("OK: synthetic label present, baseline note present, no trend glyph")
PY
```
Expected: count ≥ 1 and `OK: ...`.

- [ ] **Step 4: Finish the branch**

Use the `superpowers:finishing-a-development-branch` skill to choose merge/PR/cleanup.

---

## Self-review notes (author)

- **Spec coverage:** roll-up one-pager (Tasks 2-4) ✓; baseline trend, no arrow (Tasks 2/3 tests) ✓; benchmark config + loader + positioner, synthetic-labelled, configurable cohort label, rationale-required (Task 1) ✓; cohort AU-FI default + override param (Task 1 `cohort_label_override`, wired via `getattr` is deferred — see below) ✓; backlog one neutral both-importable CSV, GAP+PARTIAL all priorities, P0-first (Tasks 5-6) ✓; import mapping doc (Task 6) ✓; CI gate (Task 8) ✓; cross-domain headline + worst-band overall (Task 2) ✓.
- **Deferred (YAGNI, honest):** full `engagement.yaml` plumbing of a cohort override into `engagement_config.resolve` is NOT built — the seam exists as `load_cohort(..., cohort_label_override=...)`. When a real engagement needs a different cohort, pass `getattr(ENGAGEMENT, "benchmark_cohort", None)` into `load_cohort` in `build_exec_rollup.py`. This matches the spec's "configurable" intent without speculative config parsing.
- **Type consistency:** `met_pct` is a fraction everywhere; `benchmark.position` is the sole place it is `*100`'d. Column names in `backlog.COLUMNS` match the test's `expected` set and the `BACKLOG-IMPORT.md` table. `build_exec_rollup` passes the `{slug,label,posture,top_3_risks,benchmark}` dict shape that `rollup.build_exec_rollup` consumes and `test_rollup.py` fixtures mirror.
- **Resolved:** the `engagement_config.resolve(preset, config_path, cli_frameworks, available, presets_dir)` call is now baked verbatim into Tasks 4 & 6 (from `build_matrix_viewer.py:60-66`) — no execution-time guessing remains.

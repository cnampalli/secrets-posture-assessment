#!/usr/bin/env python3
"""Sketch 003: Regulatory Traceability Drill-down.

Generates index.html with three variants of the compliance-facing drill-down view.
Reads:
  matrix/regulatory-trace.csv     (146 rows across 7 frameworks)
  matrix/use-cases.csv            (47 UCs with backmap_codes and priority)
  matrix/identity-catalog.csv     (37 NHIs)
  matrix/anz-current-state.csv    (47 UC states for XYZ residual exposure)
  matrix/vendor-capabilities.csv  (vendor evidence per UC, ~893 UC rows)
"""
import csv
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MATRIX = os.path.join(ROOT, "matrix")
DST = os.path.join(HERE, "index.html")


def load_csv(name):
    path = os.path.join(MATRIX, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- load
reg = load_csv("regulatory-trace.csv")
ucs = load_csv("use-cases.csv")
nhis = load_csv("identity-catalog.csv")
states = load_csv("anz-current-state.csv")
caps = load_csv("vendor-capabilities.csv")

uc_by_id = {r["uc_id"]: r for r in ucs}
nhi_by_id = {r["nhi_id"]: r for r in nhis}
state_by_uc = {r["uc_id"]: r["anz_state"] for r in states}

# Friendly framework labels
FRAMEWORK_LABELS = {
    "essential-8":          ("Essential 8",                  "ACSC · Maturity baseline"),
    "nist-sp-800-207-zt":   ("NIST SP 800-207 (Zero Trust)", "NIST · ZTA pillars"),
    "apra-cps-234":         ("APRA CPS 234",                 "Prudential · Information security"),
    "apra-cps-230":         ("APRA CPS 230",                 "Prudential · Operational risk"),
    "apra-cpg-234":         ("APRA CPG 234 (guidance)",      "Prudential · Practice guide"),
    "asd-ism":              ("ASD ISM",                      "ACSC · Australian Govt baseline"),
    "mitre-attack":         ("MITRE ATT&CK",                 "Adversary TTPs (informative)"),
}

# Build controls list per framework (preserve original CSV order)
frameworks = []
fw_seen = set()
for r in reg:
    if r["framework_slug"] not in fw_seen:
        fw_seen.add(r["framework_slug"])
        frameworks.append(r["framework_slug"])

framework_controls = defaultdict(list)
for r in reg:
    uc_ids = [u for u in r["uc_ids"].split(";") if u]
    nhi_ids = [n for n in r["nhi_ids"].split(";") if n]
    framework_controls[r["framework_slug"]].append({
        "code": r["control_code"],
        "title": r["control_short_title"],
        "role": r.get("framework_role", ""),
        "maturity_level": r.get("maturity_level", ""),
        "uc_ids": uc_ids,
        "nhi_ids": nhi_ids,
        "evidence_url": r.get("evidence_url", ""),
        "evidence_quote": (r.get("evidence_quote") or "")[:300],
    })

# UC index (for drill display)
uc_index = {}
for r in ucs:
    uc_index[r["uc_id"]] = {
        "id": r["uc_id"],
        "title": r["short_title"],
        "category": r["category"],
        "priority": r["priority_fi"],
        "state": state_by_uc.get(r["uc_id"], "UNKNOWN"),
        "nhi_ids": [n for n in r.get("nhis_in_scope", "").split(";") if n],
        "acceptance": (r.get("acceptance_criteria") or "")[:240],
    }

# NHI index
nhi_index = {n["nhi_id"]: {"id": n["nhi_id"], "name": n["short_name"], "bucket": n["bucket"]}
             for n in nhis}

# Vendor evidence per UC (only UC target rows)
vendor_uc = defaultdict(list)  # uc_id → [{vendor, coverage, maturity, ...}]
for r in caps:
    if r["target_type"] not in ("UC-F", "UC-N"):
        continue
    vendor_uc[r["target_id"]].append({
        "vendor_slug": r["vendor_slug"],
        "vendor_name": r["vendor_name"],
        "coverage": r["coverage"],
        "maturity": int(r["maturity"]) if r["maturity"].isdigit() else 0,
        "quote": (r.get("evidence_quote") or "")[:240],
        "url": r.get("evidence_url") or "",
    })

# Sort vendor evidence by coverage tier then maturity (descending), so the strongest
# vendors land first in the drill panel.
ORDER = {"NATIVE": 0, "ADD-ON": 1, "PARTNER": 2, "GAP": 3, "N/A": 4}
for k in vendor_uc:
    vendor_uc[k].sort(key=lambda x: (ORDER.get(x["coverage"], 9), -x["maturity"]))

# Per-control roll-up: vendor coverage strength for the UCs the control demands.
# Average of best-per-UC coverage scores.
COV_SCORE = {"NATIVE": 4, "ADD-ON": 2, "PARTNER": 1, "GAP": 0, "N/A": 0}
for fw, controls in framework_controls.items():
    for c in controls:
        if not c["uc_ids"]:
            c["vendor_strength"] = 0
            c["best_vendors"] = []
            continue
        best_per_uc = []
        for u in c["uc_ids"]:
            best = max((COV_SCORE.get(v["coverage"], 0) for v in vendor_uc.get(u, [])), default=0)
            best_per_uc.append(best)
        c["vendor_strength"] = round(sum(best_per_uc) / max(len(best_per_uc), 1), 2)
        # Find vendors that are NATIVE on the most UCs in this control
        vendor_uc_count = defaultdict(int)
        for u in c["uc_ids"]:
            for vrow in vendor_uc.get(u, []):
                if vrow["coverage"] == "NATIVE":
                    vendor_uc_count[vrow["vendor_slug"]] += 1
        c["best_vendors"] = sorted(vendor_uc_count.items(), key=lambda x: -x[1])[:5]
        # Roll-up XYZ residual state across UCs
        uc_states = [state_by_uc.get(u, "UNKNOWN") for u in c["uc_ids"]]
        STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "MET": 3}
        c["anz_state"] = min(uc_states, key=lambda s: STATE_RANK.get(s, 9)) if uc_states else "UNKNOWN"

# ---------------------------------------------------------------- shape data for client
DATA = {
    "frameworks": [{"slug": s,
                    "label": FRAMEWORK_LABELS.get(s, (s, ""))[0],
                    "subtitle": FRAMEWORK_LABELS.get(s, (s, ""))[1],
                    "control_count": len(framework_controls[s])}
                   for s in frameworks],
    "controls": framework_controls,
    "ucs": uc_index,
    "nhis": nhi_index,
    "vendor_uc": dict(vendor_uc),
}
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

# ---------------------------------------------------------------- HTML
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sketch 003 — Regulatory Drill-down · XYZ Secrets-Management PRD</title>
<link rel="stylesheet" href="../themes/default.css">
<style>
  body {
    margin: 0; padding: 0; padding-top: 48px;
    font-family: var(--font-sans);
    background: var(--color-bg); color: var(--color-text);
    font-size: var(--text-sm);
  }
  h1, h2, h3 { margin: 0; font-family: var(--font-display); font-weight: 600; }

  #variant-nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 9998;
    background: var(--color-surface); border-bottom: 1px solid var(--color-border);
    padding: 8px 16px; display: flex; gap: 8px; align-items: center;
    box-shadow: var(--shadow-sm);
  }
  #variant-nav .label { font-size: var(--text-xs); color: var(--color-text-muted);
    margin-right: 8px; font-family: var(--font-mono); }
  .variant-tab {
    padding: 5px 12px; border: 1px solid var(--color-border);
    background: var(--color-surface); border-radius: var(--radius-sm);
    font-size: var(--text-xs); cursor: pointer;
    color: var(--color-text-muted);
  }
  .variant-tab.active {
    background: var(--color-primary); color: var(--color-text-inverse);
    border-color: var(--color-primary);
  }

  .variant { display: none; padding: 16px 20px; max-width: 1500px; margin: 0 auto; }
  .variant.active { display: block; }

  .doc-header {
    border-bottom: 2px solid var(--color-primary); padding-bottom: 10px;
    margin-bottom: 14px; display: flex; justify-content: space-between; align-items: baseline;
  }
  .doc-header .title { font-size: var(--text-lg); color: var(--color-primary); }
  .doc-header .meta { font-size: var(--text-xs); color: var(--color-text-muted); font-family: var(--font-mono); }

  /* Variant A — master-detail */
  .md-layout { display: grid; grid-template-columns: 320px 1fr; gap: 14px; }
  .md-rail {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); padding: 8px; max-height: 80vh; overflow-y: auto;
  }
  .fw-group { margin-bottom: 8px; }
  .fw-head {
    background: var(--color-primary); color: white; padding: 6px 8px;
    font-family: var(--font-mono); font-size: var(--text-xxs);
    text-transform: uppercase; letter-spacing: 0.04em; border-radius: var(--radius-sm);
    margin-bottom: 4px;
  }
  .fw-head .sub { font-family: var(--font-sans); text-transform: none; opacity: 0.8;
    font-size: 10px; margin-top: 1px; }
  .ctrl-item {
    padding: 6px 8px; border-bottom: 1px solid var(--color-border);
    cursor: pointer; font-size: var(--text-xs);
    border-left: 3px solid transparent;
  }
  .ctrl-item:hover { background: var(--color-primary-soft); }
  .ctrl-item.active { background: var(--color-primary-soft); border-left-color: var(--color-primary); }
  .ctrl-item .code { font-family: var(--font-mono); color: var(--color-primary); font-weight: 700; }
  .ctrl-item .title { color: var(--color-text); display: block; margin-top: 2px; }
  .ctrl-item .meta { font-family: var(--font-mono); color: var(--color-text-faint);
    font-size: 10px; margin-top: 3px; }
  .ctrl-item .state-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    margin-right: 4px; vertical-align: middle;
  }
  .state-dot.GAP { background: var(--rag-red); }
  .state-dot.PARTIAL { background: var(--rag-amber); }
  .state-dot.PENDING { background: var(--rag-grey); }
  .state-dot.MET { background: var(--rag-green); }
  .state-dot.UNKNOWN { background: var(--rag-grey); opacity: 0.4; }

  .md-detail {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); padding: 16px 20px; min-height: 60vh;
  }

  .ctrl-header { border-bottom: 1px solid var(--color-border); padding-bottom: 10px; margin-bottom: 12px; }
  .ctrl-header .code { font-family: var(--font-mono); font-weight: 700;
    color: var(--color-primary); font-size: var(--text-md); }
  .ctrl-header .title { font-size: var(--text-base); color: var(--color-text);
    margin-top: 2px; }
  .ctrl-header .quote { font-style: italic; font-size: var(--text-xs);
    color: var(--color-text-muted); margin-top: 8px; padding-left: 10px;
    border-left: 3px solid var(--color-border); }
  .ctrl-header .meta-row { display: flex; gap: 14px; margin-top: 8px;
    font-family: var(--font-mono); font-size: var(--text-xxs); color: var(--color-text-muted); }
  .ctrl-header .meta-row b { color: var(--color-primary); }

  .section-title { font-size: var(--text-sm); color: var(--color-primary);
    margin: 16px 0 8px; padding-bottom: 3px;
    border-bottom: 1px dotted var(--color-border-strong);
    font-family: var(--font-display); font-weight: 600; }

  /* UC rows */
  .uc-row {
    border: 1px solid var(--color-border); border-radius: var(--radius-sm);
    padding: 8px 10px; margin-bottom: 6px;
    background: var(--color-surface-alt);
  }
  .uc-row .uc-id { font-family: var(--font-mono); font-weight: 700; color: var(--color-primary); }
  .uc-row .uc-state { display: inline-block; padding: 1px 6px; border-radius: var(--radius-sm);
    font-family: var(--font-mono); font-weight: 700; font-size: 10px; color: white; margin-left: 6px; }
  .uc-row .uc-state.GAP     { background: var(--rag-red); }
  .uc-row .uc-state.PARTIAL { background: var(--rag-amber); }
  .uc-row .uc-state.PENDING { background: var(--rag-grey); }
  .uc-row .uc-state.MET     { background: var(--rag-green); }
  .uc-row .uc-state.UNKNOWN { background: var(--rag-grey); opacity: 0.5; }
  .uc-row .uc-pri { font-family: var(--font-mono); font-weight: 700; font-size: 10px; margin-left: 6px; padding: 1px 4px; border-radius: var(--radius-sm); }
  .uc-row .uc-pri.P0 { background: #ffe0e0; color: var(--rag-red); }
  .uc-row .uc-pri.P1 { background: #ffeed1; color: var(--rag-amber); }
  .uc-row .uc-pri.P2 { background: var(--color-border); color: var(--color-text-muted); }
  .uc-row .uc-title { font-size: var(--text-sm); color: var(--color-text); margin-top: 4px; }
  .uc-row .uc-accept { font-size: var(--text-xxs); color: var(--color-text-muted); margin-top: 4px; font-style: italic; }
  .uc-row .nhi-pills { margin-top: 6px; display: flex; flex-wrap: wrap; gap: 3px; }
  .nhi-pill { font-family: var(--font-mono); font-size: 10px;
    background: var(--color-primary-soft); color: var(--color-primary);
    padding: 1px 6px; border-radius: var(--radius-sm); }

  .vendor-row { display: grid; grid-template-columns: 24px 160px 80px 1fr; gap: 8px;
    align-items: start; padding: 4px 0; border-bottom: 1px solid var(--color-border);
    font-size: var(--text-xxs); }
  .vendor-row:last-child { border-bottom: none; }
  .vendor-row .mat { font-family: var(--font-mono); font-weight: 700; text-align: center;
    background: var(--color-primary-soft); border-radius: var(--radius-sm); padding: 2px 0; color: var(--color-primary); }
  .vendor-row .v-name { font-weight: 600; color: var(--color-text); }
  .vendor-row .v-slug { font-family: var(--font-mono); font-size: 10px; color: var(--color-text-faint); display: block; margin-top: 1px; }
  .vendor-row .cov-tag { font-family: var(--font-mono); font-weight: 700;
    padding: 2px 6px; border-radius: var(--radius-sm); color: white;
    font-size: 10px; text-align: center; }
  .cov-tag.NATIVE  { background: var(--cov-native); }
  .cov-tag.ADD-ON  { background: var(--cov-addon); }
  .cov-tag.PARTNER { background: var(--cov-partner); }
  .cov-tag.GAP     { background: var(--cov-gap); }
  .cov-tag.N       { background: var(--cov-na); }
  .vendor-row .quote { color: var(--color-text-muted); font-style: italic; line-height: 1.4; }
  .vendor-row .quote a { color: var(--color-primary); text-decoration: none; }

  /* Variant B — cascading columns */
  .casc { display: grid; grid-template-columns: 220px 280px 1fr 1fr; gap: 8px;
    height: 75vh; }
  .casc-col {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); overflow-y: auto; padding: 4px;
  }
  .casc-col .col-head {
    background: var(--color-primary); color: white;
    padding: 6px 8px; font-size: var(--text-xxs); font-family: var(--font-mono);
    text-transform: uppercase; letter-spacing: 0.04em;
    margin: -4px -4px 4px; border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  }
  .casc-col .item { padding: 6px 8px; cursor: pointer; border-radius: var(--radius-sm);
    font-size: var(--text-xs); border-bottom: 1px solid var(--color-border); }
  .casc-col .item.active { background: var(--color-primary-soft); }
  .casc-col .item:hover { background: var(--color-primary-soft); }

  /* Variant C — tree, all expanded for print */
  .tree { font-size: var(--text-xs); }
  .tree-fw {
    background: var(--color-primary); color: white;
    padding: 6px 12px; font-family: var(--font-mono); font-size: var(--text-sm);
    margin: 14px 0 4px; border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    text-transform: uppercase; letter-spacing: 0.05em;
  }
  .tree-fw .sub { text-transform: none; font-family: var(--font-sans);
    opacity: 0.85; font-size: 10px; margin-left: 8px; }
  .tree-ctrl {
    background: var(--color-surface); padding: 8px 12px;
    border-left: 4px solid var(--color-primary);
    margin-bottom: 1px;
  }
  .tree-ctrl .code { font-family: var(--font-mono); font-weight: 700; color: var(--color-primary); }
  .tree-ctrl .title { font-size: var(--text-sm); color: var(--color-text); margin-left: 10px; }
  .tree-uc {
    background: var(--color-surface-alt); padding: 6px 12px 6px 30px;
    border-left: 4px solid var(--color-border-strong); font-size: var(--text-xxs);
    margin-bottom: 1px;
  }
  .tree-vendor {
    padding: 4px 12px 4px 50px; font-size: 11px;
    border-left: 4px solid var(--color-border); background: white;
    color: var(--color-text-muted);
  }

  /* Sketch toolbar */
  #sketch-tools {
    position: fixed; bottom: 12px; right: 12px; z-index: 9999;
    background: rgba(0,0,0,0.7); color: white; padding: 8px 12px;
    border-radius: 8px; opacity: 0.4; transition: opacity 0.2s; font-size: 11px;
  }
  #sketch-tools:hover { opacity: 1; }
  #sketch-tools button { background: transparent; border: 1px solid rgba(255,255,255,0.3);
    color: white; padding: 2px 8px; margin-left: 4px; border-radius: 3px; cursor: pointer; font-size: 11px; }
  #sketch-tools button:hover { background: rgba(255,255,255,0.1); }

  .footer-note { color: var(--color-text-faint); font-size: var(--text-xxs);
    font-family: var(--font-mono); margin-top: 14px; text-align: right; }
</style>
</head>
<body>

<nav id="variant-nav">
  <span class="label">SKETCH 003 — REGULATORY DRILL-DOWN</span>
  <button class="variant-tab active" data-variant="a">A · Master/detail</button>
  <button class="variant-tab" data-variant="b">B · Cascading columns</button>
  <button class="variant-tab" data-variant="c">C · Tree (print-ready)</button>
  <span style="flex:1"></span>
  <span style="font-size:11px;color:var(--color-text-muted);font-family:var(--font-mono)">146 controls · 7 frameworks · 47 UCs</span>
</nav>

<!-- =================================================================== -->
<!-- VARIANT A — Master / Detail                                         -->
<!-- =================================================================== -->
<section class="variant active" id="variant-a">
  <div class="doc-header">
    <div>
      <h1 class="title">Regulatory traceability — Control → UCs → NHIs → Vendor evidence</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">For Risk &amp; Compliance · APRA-facing defensibility</div>
    </div>
    <div class="meta">PRD v0.1 · CONFIDENTIAL · Draft</div>
  </div>

  <div class="md-layout">
    <div class="md-rail" id="rail-a"></div>
    <div class="md-detail" id="detail-a">
      <div style="color:var(--color-text-muted);font-style:italic;text-align:center;padding:80px 20px">
        Select a control on the left to trace its UCs, NHIs, and vendor evidence.
      </div>
    </div>
  </div>
  <div class="footer-note">Source: matrix/regulatory-trace.csv · matrix/use-cases.csv · matrix/vendor-capabilities.csv · build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT B — Cascading Columns                                       -->
<!-- =================================================================== -->
<section class="variant" id="variant-b">
  <div class="doc-header">
    <div>
      <h1 class="title">Regulatory traceability — Cascading drill</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">Click left → right: framework → control → UC → vendor evidence</div>
    </div>
    <div class="meta">PRD v0.1 · CONFIDENTIAL · Draft</div>
  </div>

  <div class="casc">
    <div class="casc-col"><div class="col-head">Framework</div><div id="casc-fw"></div></div>
    <div class="casc-col"><div class="col-head">Control</div><div id="casc-ctrl"></div></div>
    <div class="casc-col"><div class="col-head">Use Case</div><div id="casc-uc"></div></div>
    <div class="casc-col"><div class="col-head">Vendor evidence</div><div id="casc-vendor"></div></div>
  </div>
  <div class="footer-note">Source: matrix/regulatory-trace.csv · matrix/use-cases.csv · matrix/vendor-capabilities.csv · build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT C — Tree (print-ready)                                      -->
<!-- =================================================================== -->
<section class="variant" id="variant-c">
  <div class="doc-header">
    <div>
      <h1 class="title">Regulatory traceability — Full tree (APRA-ready)</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">All frameworks · all controls · all UC + top-3 vendor evidence — expanded for print</div>
    </div>
    <div class="meta">PRD v0.1 · CONFIDENTIAL · Draft · APRA CPS-234 focus</div>
  </div>

  <div style="margin-bottom:10px;font-size:var(--text-xs);color:var(--color-text-muted)">
    Filter to framework:
    <select id="tree-fw-filter" style="padding:3px 8px;border:1px solid var(--color-border);border-radius:3px;font-size:12px"></select>
    <span style="margin-left:14px;font-family:var(--font-mono);font-size:11px">
      Each control shows its uc_ids, the XYZ-state rollup, and the top-3 NATIVE-coverage vendors.
    </span>
  </div>

  <div class="tree" id="tree-c"></div>
  <div class="footer-note">Source: matrix/regulatory-trace.csv · matrix/use-cases.csv · matrix/vendor-capabilities.csv · build.py</div>
</section>

<!-- Sketch tools -->
<div id="sketch-tools" class="no-print">
  Sketch 003 ·
  <button onclick="window.print()">Print to PDF</button>
</div>

<script>
const DATA = __DATA_JSON__;

document.querySelectorAll('.variant-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.variant;
    document.querySelectorAll('.variant-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.variant').forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('variant-' + id).classList.add('active');
  });
});

function escapeHtml(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, ch => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[ch]));
}

function covClass(c) { return c === 'N/A' ? 'N' : c; }

// ============================ Variant A — Master/Detail
(function renderA(){
  const rail = document.getElementById('rail-a');
  let html = '';
  for (const fw of DATA.frameworks) {
    html += '<div class="fw-group">' +
      '<div class="fw-head">' + escapeHtml(fw.label) +
        ' <span class="sub">' + escapeHtml(fw.subtitle) + ' · ' + fw.control_count + '</span>' +
      '</div>';
    const ctrls = DATA.controls[fw.slug] || [];
    for (const c of ctrls) {
      html += '<div class="ctrl-item" data-fw="' + fw.slug + '" data-code="' + escapeHtml(c.code) + '">' +
        '<span class="state-dot ' + (c.anz_state || 'UNKNOWN') + '"></span>' +
        '<span class="code">' + escapeHtml(c.code) + '</span>' +
        '<span class="title">' + escapeHtml(c.title) + '</span>' +
        '<div class="meta">' +
          c.uc_ids.length + ' UCs · ' +
          c.nhi_ids.length + ' NHIs · ' +
          'state ' + (c.anz_state || 'UNKNOWN') +
        '</div>' +
      '</div>';
    }
    html += '</div>';
  }
  rail.innerHTML = html;

  rail.addEventListener('click', e => {
    const item = e.target.closest('.ctrl-item');
    if (!item) return;
    rail.querySelectorAll('.ctrl-item').forEach(x => x.classList.remove('active'));
    item.classList.add('active');
    renderDetail(item.dataset.fw, item.dataset.code);
  });

  function renderDetail(fw, code) {
    const c = (DATA.controls[fw] || []).find(x => x.code === code);
    if (!c) return;
    const detail = document.getElementById('detail-a');
    let h = '<div class="ctrl-header">' +
      '<span class="code">' + escapeHtml(c.code) + '</span> · ' +
      '<span class="title">' + escapeHtml(c.title) + '</span>' +
      (c.evidence_quote ? '<div class="quote">' + escapeHtml(c.evidence_quote) + '</div>' : '') +
      '<div class="meta-row">' +
        '<span><b>' + c.uc_ids.length + '</b> UCs satisfy this</span>' +
        '<span><b>' + c.nhi_ids.length + '</b> NHIs in scope</span>' +
        '<span>XYZ rollup: <b>' + (c.anz_state || 'UNKNOWN') + '</b></span>' +
        '<span>Maturity: <b>' + (c.maturity_level || '—') + '</b></span>' +
        (c.evidence_url ? '<span><a href="' + escapeHtml(c.evidence_url) + '" target="_blank" rel="noopener" style="color:var(--color-primary)">control source ↗</a></span>' : '') +
      '</div>' +
    '</div>';

    h += '<h3 class="section-title">Use cases that satisfy this control</h3>';
    if (c.uc_ids.length === 0) {
      h += '<div style="color:var(--color-text-muted);font-style:italic">No UCs map to this control.</div>';
    } else {
      for (const uid of c.uc_ids) {
        const uc = DATA.ucs[uid];
        if (!uc) continue;
        h += '<div class="uc-row">' +
          '<span class="uc-id">' + uc.id + '</span>' +
          '<span class="uc-state ' + uc.state + '">' + uc.state + '</span>' +
          '<span class="uc-pri ' + uc.priority + '">' + uc.priority + '</span>' +
          '<div class="uc-title">' + escapeHtml(uc.title) + '</div>' +
          (uc.acceptance ? '<div class="uc-accept">"' + escapeHtml(uc.acceptance) + '…"</div>' : '') +
          '<div class="nhi-pills">' +
            uc.nhi_ids.map(nid => {
              const n = DATA.nhis[nid];
              return '<span class="nhi-pill" title="' + escapeHtml((n && n.name) || nid) + '">' + nid + '</span>';
            }).join('') +
          '</div>' +
        '</div>';
      }
    }

    h += '<h3 class="section-title">Vendor evidence — top NATIVE / ADD-ON coverage per UC</h3>';
    if (c.uc_ids.length === 0) {
      h += '<div style="color:var(--color-text-muted);font-style:italic">No UCs → no vendor evidence.</div>';
    } else {
      for (const uid of c.uc_ids) {
        const vendors = (DATA.vendor_uc[uid] || []).slice(0, 4);
        if (!vendors.length) continue;
        h += '<div style="margin:8px 0 4px;font-family:var(--font-mono);font-size:11px;color:var(--color-primary)"><b>' + uid + '</b> · ' + escapeHtml((DATA.ucs[uid] && DATA.ucs[uid].title) || '') + '</div>';
        for (const v of vendors) {
          h += '<div class="vendor-row">' +
            '<div class="mat">' + (v.maturity || 0) + '</div>' +
            '<div><div class="v-name">' + escapeHtml(v.vendor_name) + '</div><div class="v-slug">' + escapeHtml(v.vendor_slug) + '</div></div>' +
            '<div class="cov-tag ' + covClass(v.coverage) + '">' + escapeHtml(v.coverage) + '</div>' +
            '<div class="quote">' + (v.quote ? '"' + escapeHtml(v.quote) + '"' : '') +
              (v.url ? '<br><a href="' + escapeHtml(v.url) + '" target="_blank" rel="noopener">' + escapeHtml(v.url.slice(0, 80)) + '↗</a>' : '') +
            '</div>' +
          '</div>';
        }
      }
    }
    detail.innerHTML = h;
  }

  // Open first APRA CPS 234 control by default to ground the page
  const firstApra = (DATA.controls['apra-cps-234'] || [])[0];
  if (firstApra) {
    const sel = rail.querySelector('.ctrl-item[data-fw="apra-cps-234"]');
    if (sel) sel.click();
  }
})();

// ============================ Variant B — Cascading
(function renderB(){
  const cFw = document.getElementById('casc-fw');
  const cCtrl = document.getElementById('casc-ctrl');
  const cUc = document.getElementById('casc-uc');
  const cV = document.getElementById('casc-vendor');

  cFw.innerHTML = DATA.frameworks.map(fw =>
    '<div class="item" data-fw="' + fw.slug + '">' +
      '<div style="font-weight:600">' + escapeHtml(fw.label) + '</div>' +
      '<div style="font-size:10px;color:var(--color-text-muted);font-family:var(--font-mono)">' +
        fw.control_count + ' controls · ' + escapeHtml(fw.subtitle) +
      '</div>' +
    '</div>'
  ).join('');

  function showControls(fwSlug) {
    cFw.querySelectorAll('.item').forEach(x => x.classList.toggle('active', x.dataset.fw === fwSlug));
    const list = DATA.controls[fwSlug] || [];
    cCtrl.innerHTML = list.map(c =>
      '<div class="item" data-fw="' + fwSlug + '" data-code="' + escapeHtml(c.code) + '">' +
        '<span class="state-dot ' + (c.anz_state || 'UNKNOWN') + '"></span>' +
        '<b style="font-family:var(--font-mono);color:var(--color-primary)">' + escapeHtml(c.code) + '</b>' +
        (c.maturity_level ? ' <span style="font-family:var(--font-mono);font-size:9px;background:var(--color-primary);color:white;padding:0 4px;border-radius:2px">' + escapeHtml(c.maturity_level) + '</span>' : '') +
        '<div style="font-size:11px;margin-top:2px">' + escapeHtml(c.title) + '</div>' +
        (c.evidence_quote ? '<div style="font-size:10px;color:var(--color-text-muted);margin-top:3px;font-style:italic;line-height:1.35;border-left:2px solid var(--color-border);padding-left:6px">' + escapeHtml(c.evidence_quote.slice(0, 110)) + (c.evidence_quote.length > 110 ? '…' : '') + '</div>' : '') +
        '<div style="font-size:10px;color:var(--color-text-muted);font-family:var(--font-mono);margin-top:3px">' +
          c.uc_ids.length + ' UCs · ' + (c.anz_state || 'UNKNOWN') +
        '</div>' +
      '</div>'
    ).join('');
    cUc.innerHTML = '<div style="padding:20px;color:var(--color-text-muted);font-style:italic;text-align:center">← Pick a control</div>';
    cV.innerHTML = '';
  }

  function showUcs(fwSlug, code) {
    cCtrl.querySelectorAll('.item').forEach(x => x.classList.toggle('active', x.dataset.code === code));
    const ctrl = (DATA.controls[fwSlug] || []).find(c => c.code === code);
    if (!ctrl) return;
    // Definition header — full quote + source standard link + maturity
    let header = '<div style="background:var(--color-primary-soft);border-bottom:1px solid var(--color-border-strong);padding:8px 10px;margin:-4px -4px 6px;border-radius:var(--radius-sm) var(--radius-sm) 0 0">' +
      '<div style="font-family:var(--font-mono);font-weight:700;color:var(--color-primary);font-size:var(--text-xs)">' +
        escapeHtml(ctrl.code) +
        (ctrl.maturity_level ? ' <span style="background:var(--color-primary);color:white;padding:0 5px;border-radius:2px;margin-left:4px">' + escapeHtml(ctrl.maturity_level) + '</span>' : '') +
      '</div>' +
      '<div style="font-size:11px;font-weight:600;margin-top:2px">' + escapeHtml(ctrl.title) + '</div>' +
      (ctrl.evidence_quote ? '<div style="font-size:10px;color:var(--color-text-muted);margin-top:4px;font-style:italic;line-height:1.4;border-left:3px solid var(--color-primary);padding-left:6px">"' + escapeHtml(ctrl.evidence_quote) + '"</div>' : '') +
      (ctrl.evidence_url ? '<div style="margin-top:4px;font-size:10px"><a href="' + escapeHtml(ctrl.evidence_url) + '" target="_blank" rel="noopener" style="color:var(--color-primary);font-family:var(--font-mono)">source standard ↗</a></div>' : '') +
    '</div>';
    let body = ctrl.uc_ids.map(uid => {
      const uc = DATA.ucs[uid] || {};
      return '<div class="item" data-uc="' + uid + '">' +
        '<b style="font-family:var(--font-mono);color:var(--color-primary)">' + uid + '</b>' +
        ' <span class="uc-state ' + (uc.state || 'UNKNOWN') + '" style="padding:0 4px;border-radius:2px;color:white;font-size:9px;font-family:var(--font-mono)">' + (uc.state || '?') + '</span>' +
        '<div style="font-size:11px;margin-top:2px">' + escapeHtml(uc.title || '(unknown)') + '</div>' +
        '<div style="font-size:10px;color:var(--color-text-muted);margin-top:2px">' +
          (uc.priority || '') + ' · ' + (uc.nhi_ids || []).length + ' NHIs · '+ (DATA.vendor_uc[uid] || []).length + ' vendor rows' +
        '</div>' +
      '</div>';
    }).join('') || '<div style="padding:20px;color:var(--color-text-muted);font-style:italic">No UCs.</div>';
    cUc.innerHTML = header + body;
    cV.innerHTML = '<div style="padding:20px;color:var(--color-text-muted);font-style:italic;text-align:center">← Pick a UC</div>';
  }

  function showVendors(uid) {
    cUc.querySelectorAll('.item').forEach(x => x.classList.toggle('active', x.dataset.uc === uid));
    const vlist = DATA.vendor_uc[uid] || [];
    const uc = DATA.ucs[uid] || {};
    let h = '<div style="padding:6px 8px;background:var(--color-primary-soft);border-radius:var(--radius-sm);margin-bottom:6px">' +
      '<b style="font-family:var(--font-mono);color:var(--color-primary)">' + uid + '</b><br>' +
      '<span style="font-size:11px">' + escapeHtml(uc.title || '') + '</span>' +
    '</div>';
    h += vlist.map(v => {
      return '<div class="vendor-row" style="padding:5px 4px">' +
        '<div class="mat">' + (v.maturity || 0) + '</div>' +
        '<div><div class="v-name">' + escapeHtml(v.vendor_name) + '</div><div class="v-slug">' + escapeHtml(v.vendor_slug) + '</div></div>' +
        '<div class="cov-tag ' + covClass(v.coverage) + '">' + escapeHtml(v.coverage) + '</div>' +
        '<div class="quote">' + (v.quote ? '"' + escapeHtml(v.quote.slice(0, 140)) + '"' : '') + '</div>' +
      '</div>';
    }).join('');
    cV.innerHTML = h;
  }

  cFw.addEventListener('click', e => {
    const it = e.target.closest('.item'); if (!it) return;
    showControls(it.dataset.fw);
  });
  cCtrl.addEventListener('click', e => {
    const it = e.target.closest('.item'); if (!it) return;
    showUcs(it.dataset.fw, it.dataset.code);
  });
  cUc.addEventListener('click', e => {
    const it = e.target.closest('.item'); if (!it) return;
    showVendors(it.dataset.uc);
  });

  // Default to APRA CPS-234
  const def = cFw.querySelector('[data-fw="apra-cps-234"]');
  if (def) def.click();
})();

// ============================ Variant C — Tree (print-ready)
(function renderC(){
  const tree = document.getElementById('tree-c');
  const fwSel = document.getElementById('tree-fw-filter');
  fwSel.innerHTML = '<option value="all">All frameworks</option>' +
    DATA.frameworks.map(fw =>
      '<option value="' + fw.slug + '"' + (fw.slug === 'apra-cps-234' ? ' selected' : '') + '>' + escapeHtml(fw.label) + '</option>'
    ).join('');

  function render(filter) {
    let h = '';
    for (const fw of DATA.frameworks) {
      if (filter !== 'all' && fw.slug !== filter) continue;
      h += '<div class="tree-fw">' + escapeHtml(fw.label) +
           ' <span class="sub">' + escapeHtml(fw.subtitle) + ' · ' + fw.control_count + ' controls</span></div>';
      for (const c of (DATA.controls[fw.slug] || [])) {
        const bestVendors = (c.best_vendors || []).map(([slug, n]) => slug + ' (' + n + ')').join(' · ') || '—';
        h += '<div class="tree-ctrl">' +
          '<span class="state-dot ' + (c.anz_state || 'UNKNOWN') + '"></span>' +
          '<span class="code">' + escapeHtml(c.code) + '</span>' +
          '<span class="title">' + escapeHtml(c.title) + '</span>' +
          '<span style="float:right;font-family:var(--font-mono);font-size:10px;color:var(--color-text-muted)">' +
            c.uc_ids.length + ' UCs · ' + (c.anz_state || 'UNKNOWN') +
          '</span>' +
          (c.evidence_quote ? '<div style="font-style:italic;font-size:11px;color:var(--color-text-muted);margin-top:4px;padding-left:18px">"' + escapeHtml(c.evidence_quote) + '"</div>' : '') +
          '<div style="font-family:var(--font-mono);font-size:10px;color:var(--color-primary);margin-top:4px;padding-left:18px">' +
            'Top NATIVE vendors: ' + bestVendors +
          '</div>' +
        '</div>';
        for (const uid of c.uc_ids) {
          const uc = DATA.ucs[uid] || {};
          h += '<div class="tree-uc">' +
            '<b style="font-family:var(--font-mono);color:var(--color-primary)">' + uid + '</b>' +
            ' <span class="uc-state ' + (uc.state || 'UNKNOWN') + '" style="padding:0 4px;border-radius:2px;color:white;font-size:9px;font-family:var(--font-mono)">' + (uc.state || '?') + '</span>' +
            ' <span style="font-family:var(--font-mono);font-size:9px;color:var(--color-text-muted)">' + (uc.priority || '') + '</span>' +
            ' — ' + escapeHtml(uc.title || '(unknown)') +
            ' <span style="float:right;font-family:var(--font-mono);font-size:9px;color:var(--color-text-faint)">' +
              (uc.nhi_ids || []).join(' ') +
            '</span>' +
          '</div>';
          const topVendors = (DATA.vendor_uc[uid] || []).slice(0, 3);
          for (const v of topVendors) {
            h += '<div class="tree-vendor">' +
              '<span class="cov-tag ' + covClass(v.coverage) + '" style="font-size:9px;padding:0 4px">' + v.coverage + '</span>' +
              ' <b>' + escapeHtml(v.vendor_name) + '</b>' +
              ' <span style="font-family:var(--font-mono);font-size:9px;color:var(--color-text-faint)">m' + (v.maturity || 0) + '</span>' +
              (v.quote ? ' — <i>' + escapeHtml(v.quote.slice(0, 120)) + '</i>' : '') +
            '</div>';
          }
        }
      }
    }
    tree.innerHTML = h;
  }

  fwSel.addEventListener('change', () => render(fwSel.value));
  render('apra-cps-234');
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA_JSON__", DATA_JSON)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Frameworks: {len(frameworks)}")
for s in frameworks:
    print(f"  {s:>25}: {len(framework_controls[s])} controls")
print(f"UCs indexed: {len(uc_index)}")
print(f"Vendor-UC evidence rows: {sum(len(v) for v in vendor_uc.values())}")
print(f"NHIs indexed: {len(nhi_index)}")

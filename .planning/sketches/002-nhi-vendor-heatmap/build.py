#!/usr/bin/env python3
"""Sketch 002: NHI × Vendor Coverage Heatmap.

Generates index.html with three variants of the architect-facing coverage matrix.
Reads:
  matrix/identity-catalog.csv     (37 NHIs)
  matrix/vendor-capabilities.csv  (1,597 rows, filtered to NHI target_type)
  matrix/anz-current-state.csv    (47 UC states, joined via use-cases.csv for GAP-NHI filter)
  matrix/use-cases.csv            (47 UCs, for NHI→UC mapping)
"""
import csv
import html
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
nhis_all = load_csv("identity-catalog.csv")
caps = load_csv("vendor-capabilities.csv")
ucs = load_csv("use-cases.csv")
states = load_csv("anz-current-state.csv")

# vendor list (sorted, stable)
vendors = sorted({r["vendor_slug"] for r in caps})

# NHIs ordered: COMMON first, then UNCOMMON; preserve catalog order within bucket
nhis_common = [n for n in nhis_all if n["bucket"] == "COMMON"]
nhis_uncommon = [n for n in nhis_all if n["bucket"] == "UNCOMMON"]
nhis_ordered = nhis_common + nhis_uncommon

# Build coverage map: (vendor, nhi_id) → {coverage, maturity, ...}
cov = {}
for r in caps:
    if r["target_type"] != "NHI":
        continue
    cov[(r["vendor_slug"], r["target_id"])] = {
        "coverage": r["coverage"],
        "maturity": int(r["maturity"]) if r["maturity"].isdigit() else 0,
        "quote": (r.get("evidence_quote") or "")[:200],
        "url": r.get("evidence_url") or "",
        "notes": (r.get("notes") or "")[:200],
    }

# Vendor display names
vendor_name = {}
for r in caps:
    vendor_name.setdefault(r["vendor_slug"], r["vendor_name"])

# Coverage score for sorting (higher = better)
SCORE = {"NATIVE": 4, "ADD-ON": 2, "PARTNER": 1, "GAP": 0, "N/A": 0}


def score_cell(c):
    return SCORE.get(c["coverage"], 0) * (1 + 0.2 * c["maturity"]) if c else 0


# Per-vendor totals
vendor_score = defaultdict(float)
vendor_native = defaultdict(int)
vendor_addon = defaultdict(int)
vendor_partner = defaultdict(int)
vendor_gap = defaultdict(int)
for n in nhis_ordered:
    for v in vendors:
        c = cov.get((v, n["nhi_id"]))
        if not c:
            continue
        vendor_score[v] += score_cell(c)
        if c["coverage"] == "NATIVE": vendor_native[v] += 1
        elif c["coverage"] == "ADD-ON": vendor_addon[v] += 1
        elif c["coverage"] == "PARTNER": vendor_partner[v] += 1
        elif c["coverage"] == "GAP": vendor_gap[v] += 1

# Per-NHI totals
nhi_native_vendor_count = defaultdict(int)
nhi_any_coverage_count = defaultdict(int)
for n in nhis_ordered:
    for v in vendors:
        c = cov.get((v, n["nhi_id"]))
        if not c:
            continue
        if c["coverage"] == "NATIVE":
            nhi_native_vendor_count[n["nhi_id"]] += 1
        if c["coverage"] in ("NATIVE", "ADD-ON", "PARTNER"):
            nhi_any_coverage_count[n["nhi_id"]] += 1

# GAP-NHI filter — NHIs where XYZ has a confirmed UC-level GAP
state_by_uc = {r["uc_id"]: r["anz_state"] for r in states}
gap_nhis = set()
for uc in ucs:
    if state_by_uc.get(uc["uc_id"]) == "GAP":
        for nid in uc.get("nhis_in_scope", "").split(";"):
            if nid:
                gap_nhis.add(nid)

# Vendor ranking
ranked_vendors = sorted(vendors, key=lambda v: -vendor_score[v])

# ---------------------------------------------------------------- assemble
DATA = {
    "vendors": [{"slug": v, "name": vendor_name[v],
                 "native": vendor_native[v], "addon": vendor_addon[v],
                 "partner": vendor_partner[v], "gap": vendor_gap[v],
                 "score": round(vendor_score[v], 1)}
                for v in vendors],
    "vendors_ranked": [{"slug": v, "name": vendor_name[v],
                        "native": vendor_native[v], "addon": vendor_addon[v],
                        "partner": vendor_partner[v], "gap": vendor_gap[v],
                        "score": round(vendor_score[v], 1)}
                       for v in ranked_vendors],
    "nhis": [{"id": n["nhi_id"], "name": n["short_name"], "bucket": n["bucket"],
              "lifecycle": n.get("lifecycle", "")[:32],
              "gov_maturity": n.get("governance_maturity", "")[:16],
              "native_vendor_count": nhi_native_vendor_count[n["nhi_id"]],
              "any_coverage_count": nhi_any_coverage_count[n["nhi_id"]],
              "anz_gap": n["nhi_id"] in gap_nhis}
             for n in nhis_ordered],
    "cov": {v: {n["nhi_id"]: cov.get((v, n["nhi_id"]), {"coverage": "N/A", "maturity": 0})
                for n in nhis_ordered}
            for v in vendors},
    "totals": {
        "vendors": len(vendors),
        "nhis": len(nhis_ordered),
        "cells": len(nhis_ordered) * len(vendors),
        "gap_nhis": len(gap_nhis),
        "common_count": len(nhis_common),
        "uncommon_count": len(nhis_uncommon),
    },
}
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

# ---------------------------------------------------------------- HTML
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sketch 002 — NHI × Vendor Coverage Heatmap · XYZ Secrets-Management PRD</title>
<link rel="stylesheet" href="../themes/default.css">
<style>
  body {
    margin: 0; padding: 0; padding-top: 48px;
    font-family: var(--font-sans);
    background: var(--color-bg); color: var(--color-text);
    font-size: var(--text-sm);
  }
  h1, h2 { margin: 0; font-family: var(--font-display); font-weight: 600; }

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

  .variant { display: none; padding: 20px 24px; max-width: 1600px; margin: 0 auto; }
  .variant.active { display: block; }

  .doc-header {
    border-bottom: 2px solid var(--color-primary); padding-bottom: 10px;
    margin-bottom: 14px; display: flex; justify-content: space-between; align-items: baseline;
  }
  .doc-header .title { font-size: var(--text-lg); color: var(--color-primary); }
  .doc-header .meta { font-size: var(--text-xs); color: var(--color-text-muted); font-family: var(--font-mono); }

  /* Heatmap */
  .hm-wrap { overflow-x: auto; border: 1px solid var(--color-border); background: var(--color-surface);
    border-radius: var(--radius-sm); }
  table.heatmap { border-collapse: collapse; font-size: var(--text-xxs); width: 100%; }
  table.heatmap th, table.heatmap td { padding: 0; border: 1px solid var(--color-border); }
  table.heatmap th.col-vendor {
    background: var(--color-primary); color: white;
    text-align: center; vertical-align: bottom;
    font-family: var(--font-mono); font-size: var(--text-xxs); font-weight: 500;
    padding: 6px 4px; min-width: 50px; max-width: 70px;
    writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap;
    height: 100px;
  }
  table.heatmap th.row-nhi {
    background: var(--color-primary-soft); color: var(--color-text);
    text-align: left; padding: 3px 6px; font-family: var(--font-mono);
    font-size: var(--text-xxs); font-weight: 500;
    min-width: 200px; max-width: 240px; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; position: sticky; left: 0;
  }
  table.heatmap th.row-nhi.gap { background: var(--rag-red-soft); }
  table.heatmap th.row-nhi .nhi-id { color: var(--color-primary); font-weight: 700; }
  table.heatmap th.row-nhi .nhi-name { color: var(--color-text-muted); margin-left: 4px;
    font-family: var(--font-sans); font-size: var(--text-xxs); }
  table.heatmap td.cell {
    width: 56px; height: 24px; text-align: center; cursor: pointer;
    font-family: var(--font-mono); font-size: 10px; color: white;
    transition: outline 0.1s;
  }
  table.heatmap td.cell:hover { outline: 2px solid var(--color-primary); outline-offset: -1px; z-index: 5; position: relative; }
  table.heatmap td.cell.NATIVE   { background: var(--cov-native); }
  table.heatmap td.cell.ADD-ON   { background: var(--cov-addon); }
  table.heatmap td.cell.PARTNER  { background: var(--cov-partner); }
  table.heatmap td.cell.GAP      { background: var(--cov-gap); }
  td.cell.GAP, td.cell.N { color: rgba(255,255,255,0.4); }
  table.heatmap td.cell.N        { background: var(--cov-na); }
  table.heatmap td.cell .m { opacity: 0.85; }

  table.heatmap tfoot td, table.heatmap tfoot th {
    background: var(--color-primary-soft); font-weight: 700;
    color: var(--color-text); font-family: var(--font-mono);
    font-size: 10px; padding: 4px; text-align: center;
  }
  table.heatmap tfoot th.row-nhi { font-weight: 700; text-align: right; padding-right: 8px; }

  /* Bucket divider in Variant B */
  tr.bucket-divider th, tr.bucket-divider td {
    background: var(--color-primary) !important; color: white !important;
    font-family: var(--font-display); font-weight: 600;
    padding: 6px 8px !important; text-align: left; font-size: var(--text-xs) !important;
    text-transform: uppercase; letter-spacing: 0.05em;
  }

  /* Legend */
  .legend { display: flex; gap: 14px; align-items: center; margin: 8px 0 12px;
    font-size: var(--text-xs); color: var(--color-text-muted); }
  .legend .sw { display: inline-block; width: 16px; height: 16px;
    border-radius: var(--radius-sm); vertical-align: middle; margin-right: 4px; }
  .legend .sw.NATIVE   { background: var(--cov-native); }
  .legend .sw.ADD-ON   { background: var(--cov-addon); }
  .legend .sw.PARTNER  { background: var(--cov-partner); }
  .legend .sw.GAP      { background: var(--cov-gap); }
  .legend .sw.N        { background: var(--cov-na); }

  /* Detail popover */
  #popover {
    position: fixed; display: none; z-index: 9997;
    background: var(--color-surface); border: 1px solid var(--color-border-strong);
    border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
    padding: 12px 14px; max-width: 380px; font-size: var(--text-xs);
    line-height: 1.45; pointer-events: none;
  }
  #popover .pop-title { font-size: var(--text-sm); font-weight: 700;
    color: var(--color-primary); font-family: var(--font-mono); margin-bottom: 4px; }
  #popover .pop-cov { display: inline-block; padding: 1px 6px; border-radius: var(--radius-sm);
    color: white; font-family: var(--font-mono); font-weight: 600; font-size: 10px; margin-right: 4px; }
  #popover .pop-cov.NATIVE  { background: var(--cov-native); }
  #popover .pop-cov.ADD-ON  { background: var(--cov-addon); }
  #popover .pop-cov.PARTNER { background: var(--cov-partner); }
  #popover .pop-cov.GAP     { background: var(--cov-gap); }
  #popover .pop-cov.N       { background: var(--cov-na); }
  #popover .pop-quote { color: var(--color-text); margin-top: 6px; font-style: italic; }
  #popover .pop-notes { color: var(--color-text-muted); margin-top: 6px; font-size: 11px; }

  /* Vendor totals bar (Variant C) */
  .leaderboard { display: grid; grid-template-columns: 30px 1fr 80px 280px 60px;
    gap: 6px; align-items: center; padding: 4px 8px; }
  .leaderboard.head { background: var(--color-primary); color: white;
    font-family: var(--font-mono); font-size: var(--text-xxs);
    text-transform: uppercase; letter-spacing: 0.04em; padding: 6px 8px; }
  .leaderboard.row { background: var(--color-surface); border-bottom: 1px solid var(--color-border);
    font-size: var(--text-xs); }
  .leaderboard.row:nth-child(even) { background: var(--color-surface-alt); }
  .leaderboard.row .rank { font-weight: 700; color: var(--color-primary); font-family: var(--font-mono); text-align: right; }
  .leaderboard.row .name { font-weight: 600; }
  .leaderboard.row .slug { color: var(--color-text-faint); font-family: var(--font-mono); font-size: 10px; }
  .leaderboard.row .bar-wrap { background: var(--color-border); height: 14px; border-radius: 2px;
    display: flex; overflow: hidden; }
  .leaderboard.row .bar-seg { height: 100%; }
  .leaderboard.row .bar-seg.NATIVE  { background: var(--cov-native); }
  .leaderboard.row .bar-seg.ADD-ON  { background: var(--cov-addon); }
  .leaderboard.row .bar-seg.PARTNER { background: var(--cov-partner); }
  .leaderboard.row .bar-seg.GAP     { background: var(--cov-gap); }
  .leaderboard.row .score { text-align: right; font-family: var(--font-mono); font-weight: 700; color: var(--color-primary); }

  /* Sketch toolbar */
  #sketch-tools {
    position: fixed; bottom: 12px; right: 12px; z-index: 9999;
    background: rgba(0,0,0,0.7); color: white; padding: 8px 12px;
    border-radius: 8px; opacity: 0.4; transition: opacity 0.2s; font-size: 11px;
  }
  #sketch-tools:hover { opacity: 1; }
  #sketch-tools button { background: transparent; border: 1px solid rgba(255,255,255,0.3);
    color: white; padding: 2px 8px; margin-left: 4px; border-radius: 3px; cursor: pointer;
    font-size: 11px; }
  #sketch-tools button:hover { background: rgba(255,255,255,0.1); }

  .footer-note { color: var(--color-text-faint); font-size: var(--text-xxs);
    font-family: var(--font-mono); margin-top: 14px; text-align: right; }
</style>
</head>
<body>

<nav id="variant-nav">
  <span class="label">SKETCH 002 — NHI × VENDOR HEATMAP</span>
  <button class="variant-tab active" data-variant="a">A · Full density</button>
  <button class="variant-tab" data-variant="b">B · Bucketed (COMMON / UNCOMMON)</button>
  <button class="variant-tab" data-variant="c">C · Vendor leaderboard</button>
  <span style="flex:1"></span>
  <span style="font-size:11px;color:var(--color-text-muted);font-family:var(--font-mono)">703 cells · 37 NHI × 19 vendors</span>
</nav>

<!-- =================================================================== -->
<!-- VARIANT A — Full Density                                            -->
<!-- =================================================================== -->
<section class="variant active" id="variant-a">
  <div class="doc-header">
    <div>
      <h1 class="title">Coverage matrix — every NHI × every vendor</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">For Enterprise Architect / Platform Engineering</div>
    </div>
    <div class="meta">37 NHI × 19 vendors = 703 cells · PRD v0.1</div>
  </div>

  <div class="legend">
    <span><span class="sw NATIVE"></span>NATIVE — built-in</span>
    <span><span class="sw ADD-ON"></span>ADD-ON — extension / config</span>
    <span><span class="sw PARTNER"></span>PARTNER — via integration</span>
    <span><span class="sw GAP"></span>GAP — not addressed</span>
    <span><span class="sw N"></span>N/A — not applicable</span>
    <span style="margin-left:auto;font-family:var(--font-mono)">Cell label = maturity 0–5 · hover for evidence</span>
  </div>

  <div class="hm-wrap"><table class="heatmap" id="hm-a"></table></div>
  <div class="footer-note">Source: matrix/vendor-capabilities.csv (NHI rows) · matrix/identity-catalog.csv · build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT B — Bucketed                                                -->
<!-- =================================================================== -->
<section class="variant" id="variant-b">
  <div class="doc-header">
    <div>
      <h1 class="title">Coverage matrix — bucketed by NHI prevalence</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">COMMON identities (14) above the line · UNCOMMON / emerging (23) below</div>
    </div>
    <div class="meta">37 NHI × 19 vendors · PRD v0.1</div>
  </div>

  <div class="legend">
    <span><span class="sw NATIVE"></span>NATIVE</span>
    <span><span class="sw ADD-ON"></span>ADD-ON</span>
    <span><span class="sw PARTNER"></span>PARTNER</span>
    <span><span class="sw GAP"></span>GAP</span>
    <span><span class="sw N"></span>N/A</span>
    <span style="margin-left:auto;font-family:var(--font-mono)">Row colored red = XYZ has a confirmed UC-level gap on this NHI</span>
  </div>

  <div class="hm-wrap"><table class="heatmap" id="hm-b"></table></div>
  <div class="footer-note">Source: matrix/vendor-capabilities.csv · matrix/identity-catalog.csv · matrix/anz-current-state.csv · build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT C — Vendor Leaderboard                                      -->
<!-- =================================================================== -->
<section class="variant" id="variant-c">
  <div class="doc-header">
    <div>
      <h1 class="title">Vendor coverage leaderboard</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">Vendors ranked by NHI coverage score = NATIVE × maturity + ADD-ON / 2 + PARTNER / 4</div>
    </div>
    <div class="meta">19 vendors · scored against 37 NHI · PRD v0.1</div>
  </div>

  <div class="leaderboard head">
    <span>#</span><span>Vendor</span><span>Score</span><span>NATIVE / ADD-ON / PARTNER / GAP</span><span>NHIs</span>
  </div>
  <div id="leaderboard-c"></div>

  <h2 style="margin:18px 0 10px;font-size:var(--text-md);color:var(--color-primary);border-bottom:1px dotted var(--color-border-strong);padding-bottom:4px">Top 5 vendors — NHI coverage drill</h2>
  <div class="hm-wrap"><table class="heatmap" id="hm-c"></table></div>
  <div class="footer-note">Source: matrix/vendor-capabilities.csv · build.py</div>
</section>

<!-- Popover -->
<div id="popover"></div>

<!-- Sketch tools -->
<div id="sketch-tools" class="no-print">
  Sketch 002 ·
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

function cellClass(c) {
  if (!c || !c.coverage) return 'N';
  return (c.coverage === 'N/A') ? 'N' : c.coverage;
}

function renderHeatmap(tableEl, nhis, vendors, withBucketDivider = false) {
  // Header row: blank corner + vendor columns
  let html = '<thead><tr><th class="row-nhi" style="background:var(--color-primary);color:white">NHI</th>';
  for (const v of vendors) {
    html += '<th class="col-vendor" title="' + escapeHtml(v.name) + '">' + escapeHtml(v.slug) + '</th>';
  }
  html += '<th class="col-vendor" style="background:var(--color-text-muted);writing-mode:horizontal-tb;transform:none;height:auto;font-family:var(--font-mono);min-width:50px">cov</th>';
  html += '</tr></thead><tbody>';

  let lastBucket = null;
  for (const n of nhis) {
    if (withBucketDivider && n.bucket !== lastBucket) {
      html += '<tr class="bucket-divider"><th colspan="' + (vendors.length + 2) + '">' +
        n.bucket + ' identities' +
        (n.bucket === 'COMMON' ? ' — present in most regulated-FI environments today' :
                                 ' — emerging, edge-of-estate, or AU-specific') +
        '</th></tr>';
      lastBucket = n.bucket;
    }
    const rowClass = n.anz_gap ? 'gap' : '';
    html += '<tr><th class="row-nhi ' + rowClass + '" title="' + escapeHtml(n.name) + '">' +
      '<span class="nhi-id">' + n.id + '</span>' +
      '<span class="nhi-name">' + escapeHtml(n.name) + '</span>' +
    '</th>';
    for (const v of vendors) {
      const c = DATA.cov[v.slug] && DATA.cov[v.slug][n.id];
      const cls = cellClass(c);
      const mat = c ? c.maturity : 0;
      html += '<td class="cell ' + cls + '" ' +
        'data-vendor="' + v.slug + '" data-nhi="' + n.id + '">' +
        (mat > 0 ? '<span class="m">' + mat + '</span>' : '·') +
      '</td>';
    }
    html += '<td class="cell" style="background:var(--color-primary-soft);color:var(--color-text);font-weight:700">' +
      (n.any_coverage_count) + '/' + vendors.length + '</td>';
    html += '</tr>';
  }
  html += '</tbody><tfoot><tr><th class="row-nhi">NATIVE count →</th>';
  for (const v of vendors) {
    html += '<td>' + v.native + '</td>';
  }
  html += '<td></td></tr></tfoot>';
  tableEl.innerHTML = html;
}

// --- Variant A: full density, all 37 NHIs, all 19 vendors ----
renderHeatmap(document.getElementById('hm-a'), DATA.nhis, DATA.vendors, false);

// --- Variant B: bucketed
renderHeatmap(document.getElementById('hm-b'), DATA.nhis, DATA.vendors, true);

// --- Variant C: leaderboard + top-5 drill
const lb = document.getElementById('leaderboard-c');
lb.innerHTML = DATA.vendors_ranked.map((v, i) => {
  const total = v.native + v.addon + v.partner + v.gap;
  const seg = (cls, n) => '<div class="bar-seg ' + cls + '" style="width:' + (100*n/total).toFixed(1) + '%"></div>';
  return '<div class="leaderboard row">' +
    '<span class="rank">' + (i+1) + '</span>' +
    '<span><div class="name">' + escapeHtml(v.name) + '</div><div class="slug">' + v.slug + '</div></span>' +
    '<span class="score">' + v.score + '</span>' +
    '<div class="bar-wrap" title="N=' + v.native + ' A=' + v.addon + ' P=' + v.partner + ' G=' + v.gap + '">' +
      seg('NATIVE', v.native) + seg('ADD-ON', v.addon) + seg('PARTNER', v.partner) + seg('GAP', v.gap) +
    '</div>' +
    '<span style="text-align:right;font-family:var(--font-mono);font-size:11px">' +
      '<b>' + v.native + '</b>N · ' + v.addon + 'A · ' + v.partner + 'P · ' + v.gap + 'G' +
    '</span>' +
  '</div>';
}).join('');

renderHeatmap(document.getElementById('hm-c'), DATA.nhis, DATA.vendors_ranked.slice(0, 5), false);

// --- Hover popover (delegated, all tables)
const pop = document.getElementById('popover');
document.addEventListener('mouseover', e => {
  const td = e.target.closest('td.cell');
  if (!td || !td.dataset.vendor) return;
  const v = td.dataset.vendor;
  const n = td.dataset.nhi;
  const c = (DATA.cov[v] && DATA.cov[v][n]) || {};
  const nhiObj = DATA.nhis.find(x => x.id === n) || {};
  const venObj = DATA.vendors.find(x => x.slug === v) || {};
  pop.innerHTML =
    '<div class="pop-title">' + n + ' × ' + escapeHtml(venObj.name || v) + '</div>' +
    '<div style="font-size:11px;color:var(--color-text-muted)">' + escapeHtml(nhiObj.name || '') + '</div>' +
    '<div style="margin-top:6px"><span class="pop-cov ' + cellClass(c) + '">' + (c.coverage || 'N/A') + '</span>' +
    ' <span style="font-family:var(--font-mono);font-size:11px">maturity ' + (c.maturity || 0) + '/5</span></div>' +
    (c.quote ? '<div class="pop-quote">' + escapeHtml(c.quote) + '</div>' : '') +
    (c.notes ? '<div class="pop-notes">' + escapeHtml(c.notes) + '</div>' : '');
  pop.style.display = 'block';
  const r = td.getBoundingClientRect();
  let x = r.right + 8, y = r.top;
  if (x + 400 > window.innerWidth) x = r.left - 400 - 8;
  if (y + 200 > window.innerHeight) y = window.innerHeight - 220;
  if (y < 60) y = 60;
  pop.style.left = x + 'px';
  pop.style.top = y + 'px';
});
document.addEventListener('mouseout', e => {
  if (e.target.closest('td.cell')) pop.style.display = 'none';
});
</script>
</body>
</html>
"""

out = HTML.replace("__DATA_JSON__", DATA_JSON)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Cells: {len(nhis_ordered)} NHI × {len(vendors)} vendors = {len(nhis_ordered)*len(vendors)}")
print(f"Coverage tally:")
from collections import Counter
ctotal = Counter()
for v in vendors:
    for n in nhis_ordered:
        c = cov.get((v, n["nhi_id"]))
        ctotal[(c or {}).get("coverage", "missing")] += 1
for k, v in ctotal.most_common():
    print(f"  {k:>10}: {v}")
print(f"GAP NHIs (XYZ-confirmed via UC-level GAP): {len(gap_nhis)}")
print(f"Top vendor by score: {ranked_vendors[0]} ({vendor_score[ranked_vendors[0]]:.1f})")
print(f"Bottom vendor by score: {ranked_vendors[-1]} ({vendor_score[ranked_vendors[-1]]:.1f})")

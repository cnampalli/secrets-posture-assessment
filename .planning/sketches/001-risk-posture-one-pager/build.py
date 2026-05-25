#!/usr/bin/env python3
"""Sketch 001: Risk Posture One-Pager.

Generates index.html with three variants of the board / exec one-pager.
Reads:
  matrix/identity-catalog.csv     (37 NHIs)
  matrix/use-cases.csv            (47 UCs)
  matrix/anz-current-state.csv    (47 UC states)
  matrix/regulatory-trace.csv     (APRA CPS-234 slice)
"""
import csv
import html
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MATRIX = os.path.join(ROOT, "matrix")
DST = os.path.join(HERE, "index.html")


def load_csv(name):
    path = os.path.join(MATRIX, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- data load
nhis = load_csv("identity-catalog.csv")
ucs = load_csv("use-cases.csv")
states = load_csv("anz-current-state.csv")
reg = load_csv("regulatory-trace.csv")

state_by_uc = {r["uc_id"]: r for r in states}
uc_by_id = {r["uc_id"]: r for r in ucs}
nhi_by_id = {r["nhi_id"]: r for r in nhis}

# ---------------------------------------------------------------- aggregates
state_counts = Counter(r["anz_state"] for r in states)
priority_counts = Counter(r["priority_fi"] for r in ucs)

# state x priority crosstab
xtab = defaultdict(lambda: defaultdict(int))
for r in states:
    uc = uc_by_id.get(r["uc_id"])
    if not uc:
        continue
    xtab[r["anz_state"]][uc["priority_fi"]] += 1

# NHI coverage by bucket (count of NHIs in each bucket, then map UCs touching them)
buckets = defaultdict(list)
for n in nhis:
    buckets[n["bucket"]].append(n)

# For each NHI, roll up state of UCs that touch it.
# Semantic: GAP is the strongest signal (known bad), then PARTIAL (some coverage,
# imperfect), then PENDING (unknown), then MET (good). A board reads RED on GAP.
nhi_worst_state = {}
STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "MET": 3}  # most-attention → least
RANK_STATE = {v: k for k, v in STATE_RANK.items()}
for n in nhis:
    nid = n["nhi_id"]
    relevant_ucs = [uc for uc in ucs if nid in uc.get("nhis_in_scope", "").split(";")]
    rel_states = [state_by_uc.get(uc["uc_id"], {}).get("anz_state") for uc in relevant_ucs]
    rel_states = [s for s in rel_states if s]
    if not rel_states:
        nhi_worst_state[nid] = "UNKNOWN"
    else:
        nhi_worst_state[nid] = min(rel_states, key=lambda s: STATE_RANK.get(s, 9))

bucket_state_counts = defaultdict(Counter)
for n in nhis:
    s = nhi_worst_state[n["nhi_id"]]
    bucket_state_counts[n["bucket"]][s] += 1

# APRA CPS-234 exposure: control → list of UCs → roll up worst state
apra = [r for r in reg if r["framework_slug"] == "apra-cps-234"]
apra_exposure = []
for c in apra:
    uc_ids = [u for u in c["uc_ids"].split(";") if u]
    uc_states = [state_by_uc.get(u, {}).get("anz_state", "UNKNOWN") for u in uc_ids]
    worst = min(uc_states, key=lambda s: STATE_RANK.get(s, 9)) if uc_states else "UNKNOWN"
    apra_exposure.append({
        "code": c["control_code"],
        "title": c["control_short_title"],
        "uc_count": len(uc_ids),
        "uc_ids": uc_ids,
        "worst_state": worst,
        "p0_count": sum(1 for u in uc_ids if uc_by_id.get(u, {}).get("priority_fi") == "P0"),
        "states": Counter(uc_states),
    })

# Headlines
total_ucs = len(ucs)
total_nhis = len(nhis)
p0_total = priority_counts.get("P0", 0)
p0_gap = sum(1 for r in states
             if r["anz_state"] == "GAP"
             and uc_by_id.get(r["uc_id"], {}).get("priority_fi") == "P0")
gov_nhis = sum(1 for n in nhis if nhi_worst_state[n["nhi_id"]] in ("MET", "PARTIAL"))
gap_nhis = sum(1 for n in nhis if nhi_worst_state[n["nhi_id"]] == "GAP")
pending_nhis = sum(1 for n in nhis if nhi_worst_state[n["nhi_id"]] == "PENDING")

apra_red = sum(1 for a in apra_exposure if a["worst_state"] in ("GAP", "PENDING"))
apra_amber = sum(1 for a in apra_exposure if a["worst_state"] == "PARTIAL")
apra_green = sum(1 for a in apra_exposure if a["worst_state"] == "MET")

# ---------------------------------------------------------------- emit data
DATA = {
    "headline": {
        "total_ucs": total_ucs,
        "total_nhis": total_nhis,
        "p0_total": p0_total,
        "p0_gap": p0_gap,
        "gov_nhis": gov_nhis,
        "gap_nhis": gap_nhis,
        "pending_nhis": pending_nhis,
        "apra_total": len(apra_exposure),
        "apra_red": apra_red,
        "apra_amber": apra_amber,
        "apra_green": apra_green,
    },
    "state_counts": dict(state_counts),
    "priority_counts": dict(priority_counts),
    "xtab": {k: dict(v) for k, v in xtab.items()},
    "buckets": {k: [{"nhi_id": n["nhi_id"],
                     "short_name": n["short_name"],
                     "lifecycle": n.get("lifecycle", ""),
                     "gov_maturity": n.get("governance_maturity", ""),
                     "worst_state": nhi_worst_state[n["nhi_id"]]}
                    for n in v]
                for k, v in buckets.items()},
    "bucket_state_counts": {k: dict(v) for k, v in bucket_state_counts.items()},
    "apra_exposure": apra_exposure,
}

DATA_JSON = json.dumps(DATA, ensure_ascii=False)


# ---------------------------------------------------------------- HTML emit
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sketch 001 — Risk Posture One-Pager · XYZ Secrets-Management PRD</title>
<link rel="stylesheet" href="../themes/default.css">
<style>
  body {
    margin: 0; padding: 0; padding-top: 48px;
    font-family: var(--font-sans);
    background: var(--color-bg); color: var(--color-text);
    font-size: var(--text-sm);
  }
  h1, h2, h3 { margin: 0; font-family: var(--font-display); font-weight: 600; }

  /* Variant nav */
  #variant-nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 9998;
    background: var(--color-surface); border-bottom: 1px solid var(--color-border);
    padding: 8px 16px; display: flex; gap: 8px; align-items: center;
    box-shadow: var(--shadow-sm); font-family: var(--font-sans);
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
  .variant-tab:hover { border-color: var(--color-primary); }

  /* Variant container — A3 portrait-ish */
  .variant { display: none; padding: 24px 32px; max-width: 1200px; margin: 0 auto; }
  .variant.active { display: block; }

  /* Reusable */
  .doc-header { border-bottom: 2px solid var(--color-primary); padding-bottom: 12px;
    margin-bottom: 20px; display: flex; justify-content: space-between; align-items: baseline; }
  .doc-header .title { font-size: var(--text-xl); color: var(--color-primary); }
  .doc-header .meta { font-size: var(--text-xs); color: var(--color-text-muted);
    font-family: var(--font-mono); }
  .section-title { font-size: var(--text-md); color: var(--color-primary);
    margin: 18px 0 10px 0; padding-bottom: 4px;
    border-bottom: 1px dotted var(--color-border-strong); }

  /* KPI tiles */
  .kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 16px; }
  .kpi {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); padding: 14px 16px;
    border-left: 4px solid var(--color-primary);
  }
  .kpi .num { font-size: var(--text-2xl); font-weight: 700; color: var(--color-text);
    font-family: var(--font-display); line-height: 1; }
  .kpi .label { font-size: var(--text-xxs); color: var(--color-text-muted);
    text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px;
    font-family: var(--font-mono); }
  .kpi.gap   { border-left-color: var(--rag-red); }
  .kpi.amber { border-left-color: var(--rag-amber); }
  .kpi.green { border-left-color: var(--rag-green); }

  /* RAG bucket card */
  .bucket-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .bucket-card {
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-md); padding: 14px 16px;
  }
  .bucket-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
  .bucket-name { font-size: var(--text-base); font-weight: 600; color: var(--color-text); }
  .bucket-count { font-size: var(--text-xs); color: var(--color-text-muted); font-family: var(--font-mono); }
  .nhi-chip-grid { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 6px; }
  .nhi-chip {
    font-size: var(--text-xxs); font-family: var(--font-mono);
    padding: 2px 6px; border-radius: var(--radius-sm); color: white;
    cursor: default;
  }
  .nhi-chip.GAP     { background: var(--rag-red); }
  .nhi-chip.PARTIAL { background: var(--rag-amber); }
  .nhi-chip.PENDING { background: var(--rag-grey); }
  .nhi-chip.MET     { background: var(--rag-green); }
  .nhi-chip.UNKNOWN { background: var(--rag-grey); opacity: 0.5; }

  /* APRA strip */
  .apra-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
  .apra-cell {
    padding: 8px 10px; border-radius: var(--radius-sm);
    font-size: var(--text-xxs); font-family: var(--font-mono);
    background: var(--color-surface); border: 1px solid var(--color-border);
    border-left: 3px solid var(--rag-grey);
  }
  .apra-cell.red    { border-left-color: var(--rag-red);   background: var(--rag-red-soft); }
  .apra-cell.amber  { border-left-color: var(--rag-amber); background: var(--rag-amber-soft); }
  .apra-cell.green  { border-left-color: var(--rag-green); background: var(--rag-green-soft); }
  .apra-cell .code { font-weight: 700; color: var(--color-primary); }
  .apra-cell .title { font-size: var(--text-xxs); color: var(--color-text-muted); margin-top: 2px;
    line-height: 1.3; font-family: var(--font-sans); }

  /* Variant B (narrative) */
  .narrative {
    text-align: center; padding: 30px 20px 20px;
  }
  .narrative .hook {
    font-family: var(--font-display); font-size: var(--text-3xl);
    color: var(--color-primary); line-height: 1.15; max-width: 740px; margin: 0 auto 12px;
  }
  .narrative .sub {
    font-size: var(--text-base); color: var(--color-text-muted); max-width: 640px;
    margin: 0 auto 24px;
  }
  .narrative .stat { color: var(--rag-red); font-weight: 700; }
  .narrative .stat.green { color: var(--rag-green); }
  .narrative .stat.amber { color: var(--rag-amber); }

  /* Stacked bar (Variant B focal) */
  .stack-bar { display: flex; height: 36px; width: 100%; border-radius: var(--radius-sm);
    overflow: hidden; margin: 8px 0; background: var(--rag-grey-soft); }
  .stack-seg { display: flex; align-items: center; justify-content: center;
    color: white; font-size: var(--text-xs); font-weight: 600; font-family: var(--font-mono); }
  .stack-seg.GAP     { background: var(--rag-red); }
  .stack-seg.PARTIAL { background: var(--rag-amber); }
  .stack-seg.PENDING { background: var(--rag-grey); }
  .stack-seg.MET     { background: var(--rag-green); }
  .stack-legend { display: flex; gap: 14px; justify-content: center; font-size: var(--text-xs);
    color: var(--color-text-muted); margin-top: 6px; font-family: var(--font-mono); }
  .stack-legend .sw { display: inline-block; width: 10px; height: 10px;
    border-radius: 2px; margin-right: 4px; vertical-align: middle; }

  /* Variant C — risk register table */
  .risk-table {
    width: 100%; border-collapse: collapse; font-size: var(--text-xs);
    background: var(--color-surface); border: 1px solid var(--color-border);
  }
  .risk-table th {
    background: var(--color-primary); color: white; padding: 6px 8px;
    text-align: left; font-weight: 600; font-size: var(--text-xxs);
    text-transform: uppercase; letter-spacing: 0.04em; font-family: var(--font-mono);
  }
  .risk-table td {
    padding: 5px 8px; border-bottom: 1px solid var(--color-border);
    vertical-align: top; font-family: var(--font-sans);
  }
  .risk-table td.id { font-family: var(--font-mono); font-weight: 600; color: var(--color-primary); white-space: nowrap; }
  .risk-table td.pri { font-family: var(--font-mono); font-weight: 700; text-align: center; }
  .risk-table td.pri.P0 { color: var(--rag-red); }
  .risk-table td.pri.P1 { color: var(--rag-amber); }
  .risk-table td.pri.P2 { color: var(--color-text-muted); }
  .risk-table td.state { font-family: var(--font-mono); font-weight: 700; }
  .risk-table td.state.GAP     { color: var(--rag-red); }
  .risk-table td.state.PARTIAL { color: var(--rag-amber); }
  .risk-table td.state.PENDING { color: var(--rag-grey); }
  .risk-table tr:hover td { background: var(--color-primary-soft); }

  /* Sketch tools */
  #sketch-tools {
    position: fixed; bottom: 12px; right: 12px; z-index: 9999;
    font-family: system-ui; font-size: 11px;
    background: rgba(0,0,0,0.7); color: white; padding: 8px 12px;
    border-radius: 8px; opacity: 0.4; transition: opacity 0.2s;
  }
  #sketch-tools:hover { opacity: 1; }
  #sketch-tools button { background: transparent; border: 1px solid rgba(255,255,255,0.3);
    color: white; padding: 2px 8px; margin-left: 4px; border-radius: 3px; cursor: pointer;
    font-size: 11px; }
  #sketch-tools button:hover { background: rgba(255,255,255,0.1); }

  .footer-note { color: var(--color-text-faint); font-size: var(--text-xxs);
    font-family: var(--font-mono); margin-top: 18px; text-align: right; }
</style>
</head>
<body>

<nav id="variant-nav">
  <span class="label">SKETCH 001 — RISK POSTURE</span>
  <button class="variant-tab active" data-variant="a">A · Classic dashboard</button>
  <button class="variant-tab" data-variant="b">B · Narrative one-liner</button>
  <button class="variant-tab" data-variant="c">C · Risk register</button>
  <span style="flex:1"></span>
  <span style="font-size:11px;color:var(--color-text-muted);font-family:var(--font-mono)">A3-portrait · print Ctrl/Cmd-P</span>
</nav>

<!-- =================================================================== -->
<!-- VARIANT A — Classic Dashboard                                       -->
<!-- =================================================================== -->
<section class="variant active" id="variant-a">
  <div class="doc-header">
    <div>
      <h1 class="title">XYZ Secrets-Management — Risk Posture Snapshot</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">For Board / Executive review · PRD v0.1</div>
    </div>
    <div class="meta">2026-Q2 · CONFIDENTIAL · Draft</div>
  </div>

  <h2 class="section-title">Headline indicators</h2>
  <div class="kpi-row" id="kpi-row-a"></div>

  <h2 class="section-title">Coverage by non-human-identity bucket</h2>
  <div class="bucket-grid" id="bucket-grid-a"></div>

  <h2 class="section-title">APRA CPS-234 exposure (25 controls)</h2>
  <div class="apra-grid" id="apra-grid-a"></div>

  <div class="footer-note">Source: matrix/anz-current-state.csv · matrix/regulatory-trace.csv · matrix/identity-catalog.csv · generated by build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT B — Narrative One-Liner                                     -->
<!-- =================================================================== -->
<section class="variant" id="variant-b">
  <div class="doc-header">
    <div>
      <h1 class="title">XYZ Secrets-Management — Where we stand</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">For Board / Executive review · PRD v0.1</div>
    </div>
    <div class="meta">2026-Q2 · CONFIDENTIAL · Draft</div>
  </div>

  <div class="narrative" id="narrative-b"></div>

  <h2 class="section-title" style="text-align:center">All 47 controlled outcomes, by current state and priority</h2>
  <div id="stack-b"></div>

  <h2 class="section-title" style="text-align:center;margin-top:28px">APRA CPS-234 — what the regulator will ask about</h2>
  <div id="apra-narrative-b"></div>

  <div class="footer-note">Source: matrix/anz-current-state.csv · matrix/regulatory-trace.csv · matrix/identity-catalog.csv · generated by build.py</div>
</section>

<!-- =================================================================== -->
<!-- VARIANT C — Risk Register Table                                     -->
<!-- =================================================================== -->
<section class="variant" id="variant-c">
  <div class="doc-header">
    <div>
      <h1 class="title">XYZ Secrets-Management — Risk Register (PRD v0.1 baseline)</h1>
      <div style="font-size:12px;color:var(--color-text-muted);margin-top:4px">For Risk Committee / Internal Audit</div>
    </div>
    <div class="meta">2026-Q2 · CONFIDENTIAL · Draft</div>
  </div>

  <h2 class="section-title">Open exposures by priority and state</h2>
  <div id="risk-summary-c" style="margin-bottom:12px;font-size:var(--text-xs);color:var(--color-text-muted);font-family:var(--font-mono)"></div>

  <table class="risk-table" id="risk-table-c">
    <thead><tr>
      <th style="width:80px">UC ID</th>
      <th style="width:60px">Pri</th>
      <th style="width:80px">State</th>
      <th>Title</th>
      <th style="width:140px">NHIs in scope</th>
      <th style="width:120px">APRA back-map</th>
    </tr></thead>
    <tbody></tbody>
  </table>

  <div class="footer-note">Source: matrix/use-cases.csv · matrix/anz-current-state.csv · matrix/regulatory-trace.csv · generated by build.py</div>
</section>

<!-- Sketch toolbar -->
<div id="sketch-tools" class="no-print">
  Sketch 001 ·
  <button onclick="window.print()">Print to PDF</button>
  <button onclick="document.body.classList.toggle('compact')">Toggle density</button>
</div>

<script>
const DATA = __DATA_JSON__;

// ============================ variant switcher
document.querySelectorAll('.variant-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.variant;
    document.querySelectorAll('.variant-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.variant').forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('variant-' + id).classList.add('active');
  });
});

// ============================ Variant A
(function renderA(){
  const h = DATA.headline;
  const kpi = document.getElementById('kpi-row-a');
  const tiles = [
    { num: h.total_ucs, label: 'Controlled outcomes (UCs)', cls: '' },
    { num: h.p0_gap + ' / ' + h.p0_total, label: 'P0 outcomes with GAPs', cls: h.p0_gap > 0 ? 'gap' : 'green' },
    { num: h.gap_nhis,  label: 'NHI types with GAP coverage', cls: 'gap' },
    { num: h.pending_nhis, label: 'NHI types not yet assessed', cls: 'amber' },
    { num: h.apra_red,  label: 'APRA controls at GAP / PENDING', cls: 'gap' },
  ];
  kpi.innerHTML = tiles.map(t =>
    '<div class="kpi ' + t.cls + '"><div class="num">' + t.num + '</div><div class="label">' + t.label + '</div></div>'
  ).join('');

  const bg = document.getElementById('bucket-grid-a');
  bg.innerHTML = Object.entries(DATA.buckets).map(([bucket, nhis]) => {
    const sc = DATA.bucket_state_counts[bucket] || {};
    const total = nhis.length;
    const gap = sc.GAP || 0; const partial = sc.PARTIAL || 0;
    const pending = sc.PENDING || 0; const met = sc.MET || 0;
    return '<div class="bucket-card">' +
      '<div class="bucket-header">' +
        '<span class="bucket-name">' + bucket + '</span>' +
        '<span class="bucket-count">' + total + ' NHIs · ' +
          gap + ' gap · ' + partial + ' partial · ' + pending + ' pending' +
        '</span>' +
      '</div>' +
      '<div class="nhi-chip-grid">' +
        nhis.map(n =>
          '<span class="nhi-chip ' + n.worst_state + '" title="' +
            n.nhi_id + ' — ' + (n.short_name || '').replace(/"/g, '&quot;') + ' [' + n.worst_state + ']">' +
            n.nhi_id +
          '</span>'
        ).join('') +
      '</div>' +
    '</div>';
  }).join('');

  const apra = document.getElementById('apra-grid-a');
  apra.innerHTML = DATA.apra_exposure.map(a => {
    const cls = (a.worst_state === 'GAP' || a.worst_state === 'PENDING') ? 'red'
              : (a.worst_state === 'PARTIAL') ? 'amber'
              : (a.worst_state === 'MET') ? 'green' : '';
    return '<div class="apra-cell ' + cls + '" title="' + a.uc_count + ' UCs; worst=' + a.worst_state + '">' +
      '<div class="code">' + a.code + '</div>' +
      '<div class="title">' + a.title + '</div>' +
      '<div style="font-size:10px;color:var(--color-text-faint);margin-top:3px">' +
        a.uc_count + ' UCs · ' + (a.p0_count > 0 ? '<b>' + a.p0_count + ' P0</b>' : '') +
      '</div>' +
    '</div>';
  }).join('');
})();

// ============================ Variant B (narrative)
(function renderB(){
  const h = DATA.headline;
  const n = document.getElementById('narrative-b');
  n.innerHTML =
    '<div class="hook">' +
      'Of ' + h.total_ucs + ' controlled outcomes the bank needs to manage, ' +
      '<span class="stat">' + (DATA.state_counts.GAP || 0) + ' are open gaps</span>, ' +
      '<span class="stat amber">' + (DATA.state_counts.PARTIAL || 0) + ' partial</span>, ' +
      '<span class="stat" style="color:var(--rag-grey)">' + (DATA.state_counts.PENDING || 0) + ' not yet assessed</span>.' +
    '</div>' +
    '<div class="sub">' +
      'Of ' + h.p0_total + ' priority-zero outcomes, <b>' + h.p0_gap + ' remain open as of today</b>. ' +
      'NHI estate: ' + h.total_nhis + ' identity types tracked — ' + h.gap_nhis + ' with confirmed coverage gaps.' +
    '</div>';

  // Stack bar — state distribution
  const stb = document.getElementById('stack-b');
  const tot = h.total_ucs;
  const segs = [
    ['GAP',     DATA.state_counts.GAP || 0],
    ['PARTIAL', DATA.state_counts.PARTIAL || 0],
    ['PENDING', DATA.state_counts.PENDING || 0],
    ['MET',     DATA.state_counts.MET || 0],
  ];
  stb.innerHTML =
    '<div class="stack-bar">' +
      segs.filter(([k,v]) => v > 0).map(([k,v]) =>
        '<div class="stack-seg ' + k + '" style="width:' + (100*v/tot).toFixed(2) + '%">' + v + ' ' + k + '</div>'
      ).join('') +
    '</div>' +
    '<div class="stack-legend">' +
      segs.map(([k,v]) =>
        '<span><span class="sw" style="background:var(--rag-' + ({GAP:'red',PARTIAL:'amber',PENDING:'grey',MET:'green'}[k]) + ')"></span>' + k + ' (' + v + ')</span>'
      ).join('') +
    '</div>';

  // APRA roll-up — narrative form (one row per RAG tier)
  const apraN = document.getElementById('apra-narrative-b');
  apraN.innerHTML =
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:8px">' +
      '<div class="apra-cell red" style="font-family:var(--font-sans);font-size:var(--text-base);text-align:center;padding:14px"><div style="font-size:var(--text-2xl);font-weight:700;font-family:var(--font-display)">' + h.apra_red + '</div><div>controls at GAP / PENDING</div></div>' +
      '<div class="apra-cell amber" style="font-family:var(--font-sans);font-size:var(--text-base);text-align:center;padding:14px"><div style="font-size:var(--text-2xl);font-weight:700;font-family:var(--font-display)">' + h.apra_amber + '</div><div>controls PARTIAL</div></div>' +
      '<div class="apra-cell green" style="font-family:var(--font-sans);font-size:var(--text-base);text-align:center;padding:14px"><div style="font-size:var(--text-2xl);font-weight:700;font-family:var(--font-display)">' + h.apra_green + '</div><div>controls MET</div></div>' +
    '</div>';
})();

// ============================ Variant C
(function renderC(){
  // Build joined risk rows
  const allUcs = []; // gather joined
  for (const s of Object.entries(DATA.state_counts)) { /* unused, kept for clarity */ }

  // We use raw DATA — build from ucs (we need title + nhis + apra back-map)
  // We didn't ship ucs in DATA shape; recompose from buckets+exposure indirectly is wrong.
  // Instead include UC rows via DATA.uc_rows (filled below if present).
  let rows = DATA.uc_rows || [];

  // Sort: P0 first, then P1, then P2; within each, GAP > PARTIAL > PENDING > MET
  const priOrder = { P0:0, P1:1, P2:2 };
  const stOrder  = { GAP:0, PENDING:1, PARTIAL:2, MET:3 };
  rows.sort((a,b) => (priOrder[a.priority]||9) - (priOrder[b.priority]||9)
                  || (stOrder[a.state]||9) - (stOrder[b.state]||9));

  const summary = document.getElementById('risk-summary-c');
  const byPri = {};
  for (const r of rows) {
    byPri[r.priority] = byPri[r.priority] || { total:0, gap:0, partial:0, pending:0 };
    byPri[r.priority].total++;
    if (r.state === 'GAP') byPri[r.priority].gap++;
    else if (r.state === 'PARTIAL') byPri[r.priority].partial++;
    else if (r.state === 'PENDING') byPri[r.priority].pending++;
  }
  summary.innerHTML = Object.entries(byPri).sort().map(([p,c]) =>
    p + ': ' + c.total + ' UCs (' + c.gap + ' gap · ' + c.partial + ' partial · ' + c.pending + ' pending)'
  ).join('  ·  ');

  const tbody = document.querySelector('#risk-table-c tbody');
  tbody.innerHTML = rows.map(r =>
    '<tr>' +
      '<td class="id">' + r.uc_id + '</td>' +
      '<td class="pri ' + r.priority + '">' + r.priority + '</td>' +
      '<td class="state ' + r.state + '">' + r.state + '</td>' +
      '<td>' + r.title + '</td>' +
      '<td style="font-family:var(--font-mono);font-size:var(--text-xxs);color:var(--color-text-muted)">' + (r.nhis || '') + '</td>' +
      '<td style="font-family:var(--font-mono);font-size:var(--text-xxs);color:var(--color-text-muted)">' + (r.apra || '') + '</td>' +
    '</tr>'
  ).join('');
})();
</script>
</body>
</html>
"""

# Build UC rows for Variant C
uc_rows = []
for r in ucs:
    s = state_by_uc.get(r["uc_id"], {})
    apra_codes = [code for code in r.get("backmap_codes", "").split(";")
                  if code.startswith("CPS234")]
    uc_rows.append({
        "uc_id": r["uc_id"],
        "priority": r.get("priority_fi", ""),
        "state": s.get("anz_state", "UNKNOWN"),
        "title": r.get("short_title", ""),
        "nhis": r.get("nhis_in_scope", "")[:80],
        "apra": ";".join(apra_codes)[:60],
    })
DATA["uc_rows"] = uc_rows
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

out = HTML.replace("__DATA_JSON__", DATA_JSON)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Aggregates: UCs={total_ucs} (GAP={state_counts['GAP']}, PARTIAL={state_counts['PARTIAL']}, PENDING={state_counts['PENDING']})")
print(f"            NHIs={total_nhis} (worst-state GAP={gap_nhis}, PENDING={pending_nhis})")
print(f"            APRA CPS-234={len(apra_exposure)} (red={apra_red}, amber={apra_amber}, green={apra_green})")
print(f"            P0 UCs: {p0_total} total, {p0_gap} GAP")

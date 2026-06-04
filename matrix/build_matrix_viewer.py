#!/usr/bin/env python3
"""Build the self-contained XYZ Secrets-Management stakeholder report.

Reads the matrix + catalog CSVs and writes matrix-viewer.html — a single
offline HTML file (no server, no internet) with four views:

  1. XYZ posture dashboard (landing) — MET/PARTIAL/GAP/PENDING, clickable
     top gaps, and a stakeholder "mark as MET" override (persists locally).
  2. By Use Case — decision card: a one-line recommendation, a vendor-as-
     columns coverage/maturity grid (by layer), the mapped APRA CPS 234 +
     ASD ISM controls, and XYZ current state (with a MET override).
  3. By Identity (NHI) — vendor-as-columns coverage/maturity grid.
  4. Browse all — the full filterable capability table.

Orchestrator only: input loading lives in report_io, the model transforms in
report_logic, and the HTML assembly in report_render (+ report-template.html).
Per ADR-007, Fortanix DSM is a Layer-0 crypto-substrate DEPENDENCY excluded from
all ranked views (→ 18 ranked vendors). The source CSVs are never modified.
"""
import argparse
import json
import os
import pathlib

import engagement_config as _ec
import report_io
import report_logic
import report_render

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "matrix-viewer.html")
_CFGDIR = os.path.join(HERE, "config")

_ap = argparse.ArgumentParser(description="Build the secrets-management report.")
_ap.add_argument("--config", help="path to an engagement.yaml")
_ap.add_argument("--preset", help="named preset (financial|government|retail|baseline)")
_ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides primary)")
_ap.add_argument("--emit-data", help="(test hook) also dump {REGDATA,RECDATA} JSON to this path")
_ap.add_argument("--current-state", default="current-state.csv",
                 help="current-state CSV the report scores against (a questionnaire export via "
                      "questionnaire/report_adapter.py). Default keeps existing behaviour.")
_ARGS, _ = _ap.parse_known_args()

# ---- load inputs + config ----
_inputs = report_io.load_inputs(HERE, _ARGS.current_state)
reg_rows = _inputs["reg_rows"]
vendor_residency = report_io.load_vendor_residency(_CFGDIR)
framework_labels = report_io.load_framework_labels(_CFGDIR)

# ---- resolve the engagement (framework selection + residency knobs) ----
available = list(dict.fromkeys(r["framework_slug"] for r in reg_rows))
cli_fw = [s.strip() for s in _ARGS.frameworks.split(",")] if _ARGS.frameworks else None
ENGAGEMENT = _ec.resolve(
    preset=_ARGS.preset,
    config_path=_ARGS.config,
    cli_frameworks=cli_fw,
    available=available,
    presets_dir=pathlib.Path(_CFGDIR) / "presets",
)

# ---- build the model (report_logic) ----
REG, REGDATA = report_logic.build_regdata(
    reg_rows, _inputs["anz"], _inputs["ucs"], _inputs["ranked"],
    framework_labels, ENGAGEMENT, available)
GLOSSARY = report_logic.build_glossary(_inputs["nhis"], _inputs["ucs"])
meta = report_logic.compute_meta(_inputs["all_rows"], _inputs["ranked"], _inputs["nhis"], _inputs["ucs"])
RECDATA = report_logic.build_recdata(
    _inputs["ranked"], _inputs["nhis"], report_io.VENDOR_LAYER, report_io.SHORT,
    vendor_residency, report_io.SUBSTRATE_SLUG, ENGAGEMENT)

# ---- resilience-first vendor-mix + concentration (Phase 0, parent-aware) ----
vendor_ownership = report_io.load_vendor_ownership(_CFGDIR)
_anchors = [s for s, (lay, t) in report_io.VENDOR_LAYER.items() if t == "cloud-native"]
VENDORMIX = report_logic.build_vendormix(
    _inputs["ranked"], vendor_ownership, _anchors, report_io.SHORT)

# ---- identity-control coverage indicator + gap-to-target (Phase 0, D3/D4) ----
COMPLIANCE = report_logic.build_compliance(reg_rows, _inputs["anz"], framework_labels)

# ---- render + write ----
html = report_render.render({
    "ranked": _inputs["ranked"], "anz": _inputs["anz"], "ucs": _inputs["ucs"], "nhis": _inputs["nhis"],
    "glossary": GLOSSARY, "layer_label": report_io.LAYER_LABEL, "short": report_io.SHORT,
    "reg": REG, "regdata": REGDATA, "recdata": RECDATA, "vendormix": VENDORMIX,
    "compliance": COMPLIANCE, "meta": meta,
})

if _ARGS.emit_data:
    with open(_ARGS.emit_data, "w", encoding="utf-8") as _ef:
        json.dump({"REGDATA": REGDATA, "RECDATA": RECDATA, "VENDORMIX": VENDORMIX,
                   "COMPLIANCE": COMPLIANCE}, _ef, ensure_ascii=False, sort_keys=True)

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Ranked vendors: {meta['ranked_vendors']}; ranked rows: {meta['ranked_rows']} (of {meta['total_rows']})")
print(f"UCs: {meta['ucs']}; NHIs: {meta['nhis']}; XYZ: {len(_inputs['anz'])}; "
      f"REG-mapped UCs: {len(REG)}; glossary: {len(GLOSSARY)}")

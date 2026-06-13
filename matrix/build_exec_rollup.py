#!/usr/bin/env python3
"""Build the standalone executive roll-up one-pager.

For every registered domain: loads inputs, computes posture/maturity and the
worst-risk-first top-3 risks, positions met-% against the synthetic benchmark cohort,
and (using the cross-domain concentration map) writes a self-contained one-pager to
matrix/exec-rollup.html."""
import os
import pathlib

import domains
import report_io
import report_logic
import crossdomain
import benchmark
import rollup
import rollup_render
import engagement_config as _ec

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

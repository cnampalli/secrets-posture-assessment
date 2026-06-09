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
        # Matrix-less domains (IGA ships a header-only vendor-capabilities.csv and uses
        # a bespoke per-area vendor-fit model) have no ranked vendors and a disjoint
        # vendor set, so they don't participate in the NATIVE/ADD-ON cross-domain
        # spanning/concentration map. Skip them rather than rolling up an empty domain.
        if not inp["ranked"]:
            print(f"cross-domain: skipping matrix-less domain {dom.slug}")
            continue
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

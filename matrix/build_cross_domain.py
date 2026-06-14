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
import identity_spine

HERE = os.path.dirname(os.path.abspath(__file__))
_CFGDIR = os.path.join(HERE, "config")
DST = os.path.join(HERE, "cross-domain-report.html")


def build():
    """Build the model + write the report. Returns (model, dst_path)."""
    ownership = report_io.load_vendor_ownership(_CFGDIR)
    domains_data = []
    spine_domains = []          # M2: identity catalogs for EVERY domain (incl. matrix-less IGA)
    for dom in domains.DOMAINS.values():
        inp = report_io.load_inputs(dom.data_dir, None, dom)
        # Identity catalogs exist for all domains, so the identity spine includes IGA even
        # though it is matrix-less for the vendor map below.
        spine_domains.append({"slug": dom.slug, "label": dom.label, "identities": inp["nhis"]})
        # Matrix-less domains (IGA ships a header-only vendor-capabilities.csv and uses
        # a bespoke per-area vendor-fit model) have no ranked vendors and a disjoint
        # vendor set, so they don't participate in the NATIVE/ADD-ON cross-domain
        # spanning/concentration map. Skip them rather than rolling up an empty domain.
        #
        # PRECONDITION (grill Q5): this exclusion is honest ONLY while a matrix-less
        # domain's vendor set is parent-disjoint from every matrix-using domain. The
        # concentration map rolls up by ultimate corporate PARENT, so if a matrix-less
        # domain ever shares a corporate parent with a matrix-using one (e.g. a
        # Microsoft secrets/PAM SKU alongside Microsoft Entra in IGA), skipping it here
        # would SUPPRESS a real parent-concentration signal. Revisit this skip — fold
        # the matrix-less domain's parents into the rollup — before that day.
        if not inp["ranked"]:
            print(f"cross-domain: skipping matrix-less domain {dom.slug}")
            continue
        domains_data.append({"slug": dom.slug, "label": dom.label, "ranked": inp["ranked"]})
    model = crossdomain.build_crossmap(domains_data, ownership)
    spine = identity_spine.build_spine_view(spine_domains, identity_spine.load_spine(_CFGDIR))
    with open(DST, "w", encoding="utf-8") as f:
        f.write(cross_render.render(model, spine))
    return model, DST


if __name__ == "__main__":
    model, dst = build()
    spanning = [p["parent"] for p in model["parents"] if p["spans"] >= 2]
    print(f"Wrote {dst} ({os.path.getsize(dst)} bytes)")
    print(f"Domains: {[d['slug'] for d in model['domains']]}; parents: {len(model['parents'])}; "
          f"spanning >1 domain: {spanning or 'none'}")

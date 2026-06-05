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


def _label(domains, slug):
    return next((d["label"] for d in domains if d["slug"] == slug), slug)


# Corporate parents that are not themselves a vendor brand in the data need a curated label.
_PARENT_DISPLAY = {"cyberark": "CyberArk", "ibm": "IBM"}


def _display(parent, by_domain):
    """Human display name for a parent so the report never shows a raw slug: a self-parent
    vendor uses its own brand name; a known corporate parent uses a curated label; else the
    slug is title-cased."""
    for dom in by_domain.values():
        for b in dom["brands"]:
            if b["slug"] == parent:
                return b["name"]
    return _PARENT_DISPLAY.get(parent, parent.replace("-", " ").title())


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
            "display": p["display"],
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
            "display": p["display"],
            "domains": p["spans"],
            "native_ucs_total": sum(v["native_ucs"] for v in p["by_domain"].values()),
            "note": (f"One parent covers needs across {p['spans']} domains "
                     "→ fewer vendors / contracts to manage (decision-support, not a buy list)."),
        })
    out.sort(key=lambda x: (-x["domains"], -x["native_ucs_total"], x["parent"]))
    return out


def build_crossmap(domains_data, ownership):
    """Build the cross-domain model.

    domains_data: ordered list of {"slug", "label", "ranked"} (one per domain);
                  `ranked` is that domain's ranked vendor rows (substrate excluded).
    ownership:    {vendor_slug: {"parent": <slug>, ...}} (unlisted vendors are their own parent).
    """
    domains = [{"slug": d["slug"], "label": d["label"]} for d in domains_data]

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
            "display": _display(p, by_domain),
            "by_domain": by_domain,
            "spans": len(by_domain),
            "domains_present": [d["slug"] for d in domains if d["slug"] in by_domain],
        })
    parents.sort(key=lambda x: (-x["spans"], x["parent"]))

    return {"domains": domains, "parents": parents,
            "concentration": _concentration(parents, domains),
            "consolidation": _consolidation(parents)}

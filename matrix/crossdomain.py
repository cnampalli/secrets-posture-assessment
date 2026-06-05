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

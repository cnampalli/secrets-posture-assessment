"""Parent-aware vendor concentration / lock-in resilience analytics (pure, no I/O).

Operates on the same `ranked` row shape report_logic consumes. Every measure
counts by *ultimate corporate parent*, not brand: sibling brands under one
parent (e.g. CyberArk owns Conjur + Venafi) must NOT read as independent
second-sources, or the CPS 230 concentration signal inverts.

`ownership` is injected (dependency-injection, like vendor_residency): a
{vendor_slug: {"parent": <slug>, ...}} map. Unlisted vendors are their own parent.
"""
from matrix_vocab import UC_TYPES as _UC_TYPES


def parent_of(slug, ownership):
    """Resolve a vendor slug to its ultimate parent. Defaults to itself.

    Follows a parent chain (brand -> parent -> grandparent) so a multi-hop
    ownership map still collapses to the root; guards against cycles.

    H4: an edge is only followed when its ownership is VERIFIED. An edge whose
    `confidence` is explicitly MEDIUM or LOW is NOT collapsed — the child stays
    its own parent — so an unverified acquisition claim cannot inflate a parent's
    concentration. This is the rule that would have stopped the Entro error (a
    MEDIUM-confidence 'CyberArk owns Entro' edge) from reaching a reader. Edges
    with no/HIGH confidence collapse as before (back-compatible).
    """
    seen = set()
    cur = slug
    while cur in ownership and cur not in seen:
        seen.add(cur)
        edge = ownership[cur]
        if str(edge.get("confidence", "")).strip().upper() in ("MEDIUM", "LOW"):
            break  # unverified collapse -> treat the child as its own parent
        nxt = edge.get("parent", cur)
        if nxt == cur:
            break
        cur = nxt
    return cur


def coverage_by_parent(ranked, ownership, coverage="NATIVE"):
    """For each UC target, the brands and distinct parents providing `coverage`.

    Returns {uc_id: {"brands": [...], "parents": [...],
                     "brand_count": int, "parent_count": int}}.
    UCs with no row at `coverage` are absent from the result.
    """
    brands = {}
    parents = {}
    for r in ranked:
        if r["target_type"] not in _UC_TYPES or r["coverage"] != coverage:
            continue
        uc = r["target_id"]
        brands.setdefault(uc, set()).add(r["vendor_slug"])
        parents.setdefault(uc, set()).add(parent_of(r["vendor_slug"], ownership))
    return {
        uc: {
            "brands": sorted(brands[uc]),
            "parents": sorted(parents[uc]),
            "brand_count": len(brands[uc]),
            "parent_count": len(parents[uc]),
        }
        for uc in brands
    }


def _uc_universe(ranked):
    """All UC target_ids appearing in ranked at any coverage."""
    return {r["target_id"] for r in ranked if r["target_type"] in _UC_TYPES}


def single_source(ranked, ownership, coverage="NATIVE"):
    """Substitutability risk, counted by parent.

    Returns {"single_source": [...], "uncovered": [...]}:
      - single_source: UCs with exactly one *parent* at `coverage`.
      - uncovered: UCs present in the data but with zero `coverage` coverage.
    """
    cov = coverage_by_parent(ranked, ownership, coverage)
    universe = _uc_universe(ranked)
    single = [uc for uc, c in cov.items() if c["parent_count"] == 1]
    uncovered = [uc for uc in universe if uc not in cov]
    return {"single_source": sorted(single), "uncovered": sorted(uncovered)}


def concentration(ranked, ownership, coverage="NATIVE"):
    """Per-parent blast radius across natively-covered UCs.

    Returns {parent: {"ucs": [...], "uc_count": int, "share": float,
                      "brands": [...], "sole_source_ucs": [...]}}:
      - share: fraction of natively-covered UCs this parent touches.
      - sole_source_ucs: UCs where this parent is the ONLY parent at `coverage`.
    """
    cov = coverage_by_parent(ranked, ownership, coverage)
    total = len(cov)
    out = {}
    for uc, c in cov.items():
        for p in c["parents"]:
            slot = out.setdefault(
                p, {"ucs": set(), "brands": set(), "sole_source_ucs": set()})
            slot["ucs"].add(uc)
            if c["parent_count"] == 1:
                slot["sole_source_ucs"].add(uc)
    # brands per parent (only those actually providing `coverage`).
    for r in ranked:
        if r["target_type"] not in _UC_TYPES or r["coverage"] != coverage:
            continue
        p = parent_of(r["vendor_slug"], ownership)
        if p in out:
            out[p]["brands"].add(r["vendor_slug"])
    return {
        p: {
            "ucs": sorted(s["ucs"]),
            "uc_count": len(s["ucs"]),
            "share": round(len(s["ucs"]) / total, 4) if total else 0.0,
            "brands": sorted(s["brands"]),
            "sole_source_ucs": sorted(s["sole_source_ucs"]),
        }
        for p, s in out.items()
    }

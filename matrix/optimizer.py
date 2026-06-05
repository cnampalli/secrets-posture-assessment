"""Resilience-first vendor-mix optimizer (pure, no I/O).

A greedy set-cover over `ranked` rows that selects a vendor portfolio covering
the target use cases at a given coverage level. The "resilience-first" twist:
when two candidates add the same number of new UCs, prefer the one whose
*corporate parent* is not yet represented in the portfolio — diversifying
away from single-parent concentration (CPS 230) instead of blindly minimising
vendor count. Also reports white-space (UCs no vendor covers at NATIVE, C3)
and the chosen portfolio's parent concentration.

NOT a recommendation engine: it is blind to price, contracts, stack fit, and
support. Output is "candidate portfolios to interrogate", not "buy this".
"""
import resilience as rz
from matrix_vocab import UC_TYPES as _UC_TYPES


def vendor_uc_coverage(ranked, coverage="NATIVE"):
    """{vendor_slug: set(uc_ids covered at `coverage`)}."""
    out = {}
    for r in ranked:
        if r["target_type"] not in _UC_TYPES or r["coverage"] != coverage:
            continue
        out.setdefault(r["vendor_slug"], set()).add(r["target_id"])
    return out


def _uc_universe(ranked):
    return {r["target_id"] for r in ranked if r["target_type"] in _UC_TYPES}


def greedy_cover(ranked, ownership=None, ucs=None, coverage="NATIVE",
                 resilience_first=True):
    """Greedily cover the target UC set; diversify parents on ties when
    resilience_first. Returns {chosen, covered, uncovered, steps}.

    ucs: target UC set (default = every UC in the data). uncovered = white-space.
    """
    ownership = ownership or {}
    target = set(ucs) if ucs is not None else _uc_universe(ranked)
    cov = vendor_uc_coverage(ranked, coverage)

    remaining = set(target)
    chosen, steps = [], []
    chosen_parents = set()

    while remaining:
        # Candidate gain restricted to still-needed, in-target UCs.
        gains = {v: (ucs_ & remaining) for v, ucs_ in cov.items()}
        best = max((len(g) for g in gains.values()), default=0)
        if best == 0:
            break  # nothing left can cover the remainder -> white-space
        candidates = [v for v, g in gains.items() if len(g) == best]

        def rank(v):
            new_parent = rz.parent_of(v, ownership) not in chosen_parents
            # resilience_first: a new parent sorts first (0 < 1); then by name.
            diversify = 0 if (resilience_first and new_parent) else 1
            return (diversify, v)

        pick = min(candidates, key=rank)
        new_ucs = sorted(gains[pick])
        chosen.append(pick)
        chosen_parents.add(rz.parent_of(pick, ownership))
        steps.append({"pick": pick, "new_ucs": new_ucs})
        remaining -= gains[pick]

    covered = sorted(target - remaining)
    return {"chosen": chosen, "covered": covered,
            "uncovered": sorted(remaining), "steps": steps}


def complement(start, ranked, coverage="NATIVE"):
    """Data-driven "have X -> add Y" (C4). Given an incumbent vendor `start`,
    find the single vendor that NATIVE-covers the most use cases `start` misses.

    Returns {"have", "add", "fills", "still_open"} or None if `start` already
    covers everything any vendor could add (no coverable gap remains).
    """
    cov = vendor_uc_coverage(ranked, coverage)
    universe = _uc_universe(ranked)
    gaps = universe - cov.get(start, set())
    if not gaps:
        return None
    candidates = sorted(
        ((len(cov.get(v, set()) & gaps), v) for v in cov if v != start),
        key=lambda t: (-t[0], t[1]))
    if not candidates or candidates[0][0] == 0:
        return None
    fills, add = candidates[0]
    still_open = sorted(gaps - cov.get(add, set()))
    return {"have": start, "add": add, "fills": fills, "still_open": still_open}


def portfolio_concentration(chosen, ranked, ownership, coverage="NATIVE"):
    """Parent concentration WITHIN a chosen portfolio's NATIVE coverage.

    Returns {distinct_parents, max_parent, max_parent_share, by_parent}:
      share = parent's covered UCs / all UCs the portfolio covers.
    """
    chosen = set(chosen)
    sub = [r for r in ranked if r["vendor_slug"] in chosen]
    con = rz.concentration(sub, ownership, coverage)
    if not con:
        return {"distinct_parents": 0, "max_parent": None,
                "max_parent_share": 0.0, "by_parent": {}}
    max_parent = max(con, key=lambda p: con[p]["uc_count"])
    return {
        "distinct_parents": len(con),
        "max_parent": max_parent,
        "max_parent_share": con[max_parent]["share"],
        "by_parent": con,
    }

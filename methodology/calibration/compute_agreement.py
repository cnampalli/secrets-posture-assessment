#!/usr/bin/env python3
"""SME-panel agreement scorer (A6 external calibration).

Reads a filled sme-panel-template.csv (one row per domain×uc×reviewer with both
reviewer_state and instrument_state populated) and reports per-domain and overall
agreement: raw agreement, and quadratic-weighted Cohen's kappa over the ordered
state scale GAP < PARTIAL < MET (PENDING rows are excluded from kappa — "no signal
gathered" is not a scoreable disagreement — but counted and reported).

Stdlib only, deterministic, read-only. Publication rules live in
methodology/CALIBRATION.md; this script only computes.

CLI: python3 methodology/calibration/compute_agreement.py <filled-panel.csv>
"""
import csv
import sys
from collections import defaultdict

# Ordered scale for weighted kappa. NA/PENDING are excluded (reported separately).
SCALE = {"GAP": 0, "PARTIAL": 1, "MET": 2}


def _pairs(rows):
    """Yield (domain, reviewer_score, instrument_score) for scoreable rows."""
    for r in rows:
        rev = (r.get("reviewer_state") or "").strip().upper()
        ins = (r.get("instrument_state") or "").strip().upper()
        if rev in SCALE and ins in SCALE:
            yield (r.get("domain") or "?", SCALE[rev], SCALE[ins])


def weighted_kappa(pairs):
    """Quadratic-weighted Cohen's kappa for a list of (a, b) score pairs on SCALE.
    Returns None when kappa is undefined (fewer than 2 pairs, or no variance)."""
    if len(pairs) < 2:
        return None
    k = len(SCALE)
    obs = [[0.0] * k for _ in range(k)]
    for a, b in pairs:
        obs[a][b] += 1
    n = float(len(pairs))
    row = [sum(obs[i][j] for j in range(k)) / n for i in range(k)]
    col = [sum(obs[i][j] for i in range(k)) / n for j in range(k)]
    w = [[((i - j) ** 2) / float((k - 1) ** 2) for j in range(k)] for i in range(k)]
    num = sum(w[i][j] * obs[i][j] / n for i in range(k) for j in range(k))
    den = sum(w[i][j] * row[i] * col[j] for i in range(k) for j in range(k))
    if den == 0:
        return None
    return 1.0 - num / den


def score_panel(rows):
    """Aggregate a filled panel: per-domain + overall raw agreement and weighted
    kappa, plus the excluded (PENDING/blank) row count."""
    by_dom = defaultdict(list)
    scoreable = 0
    for dom, a, b in _pairs(rows):
        by_dom[dom].append((a, b))
        scoreable += 1
    out = {"domains": {}, "excluded_rows": len(rows) - scoreable,
           "scoreable_rows": scoreable}
    allp = []
    for dom in sorted(by_dom):
        p = by_dom[dom]
        allp += p
        out["domains"][dom] = {
            "n": len(p),
            "raw_agreement": sum(1 for a, b in p if a == b) / len(p),
            "weighted_kappa": weighted_kappa(p),
        }
    out["overall"] = {
        "n": len(allp),
        "raw_agreement": (sum(1 for a, b in allp if a == b) / len(allp)) if allp else None,
        "weighted_kappa": weighted_kappa(allp),
    }
    return out


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        return 2
    with open(argv[0], encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    res = score_panel(rows)
    print(f"scoreable rows: {res['scoreable_rows']}  (excluded/pending: {res['excluded_rows']})")
    for dom, d in res["domains"].items():
        wk = "undefined" if d["weighted_kappa"] is None else f"{d['weighted_kappa']:.3f}"
        print(f"  {dom:8} n={d['n']:3}  raw={d['raw_agreement']:.2f}  weighted-kappa={wk}")
    o = res["overall"]
    wk = "undefined" if o["weighted_kappa"] is None else f"{o['weighted_kappa']:.3f}"
    print(f"  overall  n={o['n']:3}  raw={o['raw_agreement']:.2f}  weighted-kappa={wk}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Board-grade exec roll-up — pure model builder (no I/O).

Consumes per-domain posture (report_logic.build_posture_maturity), worst-risk-first
top risks (report_logic.build_quick_wins), and a benchmark position (benchmark.position),
plus the cross-domain concentration map (crossdomain.build_crossmap), and assembles the
one-pager model the renderer consumes. Trend is a deliberate BASELINE marker — no
direction is implied because no prior dated assessment exists yet (M4 fills this)."""

_BAND_RANK = {"ML1": 1, "ML2": 2, "ML3": 3}

_BASELINE_TREND = {
    "state": "baseline",
    "note": "First assessment — trend activates at the next dated re-baseline.",
}


def _lowest_band(domains):
    bands = [d["posture"]["overall_band"] for d in domains if d.get("posture")]
    if not bands:
        return "ML1"
    return min(bands, key=lambda b: _BAND_RANK.get(b, 1))


def _concentration_headline(crossmap):
    spanning = [p for p in crossmap.get("parents", []) if p.get("spans", 0) >= 2]
    if not spanning:
        return ("No single corporate parent spans more than one assessed domain "
                "(no cross-domain concentration signal at this scope).")
    top = max(spanning, key=lambda p: p["spans"])
    return (f"{top['display']} spans {top['spans']} assessed domains — a cross-domain "
            "service-provider concentration signal (CPS 230). Ownership is point-in-time.")


def build_exec_rollup(domains, crossmap):
    """Assemble the board roll-up model. `domains` is a list of
    {slug, label, posture, top_3_risks, benchmark}; `crossmap` is
    crossdomain.build_crossmap output. Returns
    {domains:[{slug,label,overall_band,met_pct,counts,p0_open,top_3_risks,benchmark,trend}],
     overall:{lowest_band,total_p0_open,concentration_headline}}."""
    out_domains = []
    total_p0 = 0
    for d in domains:
        posture = d["posture"]
        total_p0 += posture.get("p0_open", 0)
        out_domains.append({
            "slug": d["slug"],
            "label": d["label"],
            "overall_band": posture["overall_band"],
            "met_pct": posture["met_pct"],
            "counts": posture["counts"],
            "p0_open": posture.get("p0_open", 0),
            "top_3_risks": d.get("top_3_risks", []),
            "benchmark": d["benchmark"],
            "trend": dict(_BASELINE_TREND),
        })
    return {
        "domains": out_domains,
        "overall": {
            "lowest_band": _lowest_band(domains),
            "total_p0_open": total_p0,
            "concentration_headline": _concentration_headline(crossmap),
        },
    }

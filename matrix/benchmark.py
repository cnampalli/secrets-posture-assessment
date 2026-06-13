"""Synthetic, clearly-labelled benchmark cohort — pure model helpers (no rendering).

Loads versioned per-domain met-% percentile bands from config/benchmark-cohort.json
and positions a domain's assessed met-% against them. The bands are a designed-honest
SYNTHETIC baseline (not a measured cohort); the loader refuses any band that lacks a
documented rationale so the honesty contract can't silently erode.
"""
import json
import os

_BANDS = ("p25", "p50", "p75")


def load_cohort(cfgdir, cohort_label_override=None):
    """Read benchmark-cohort.json from `cfgdir`. Validates that every domain band
    set carries p25/p50/p75 and a non-empty `rationale`; raises ValueError otherwise
    (honesty gate). `cohort_label_override` (e.g. from engagement config) replaces the
    displayed cohort label without touching the bands."""
    path = os.path.join(cfgdir, "benchmark-cohort.json")
    with open(path, encoding="utf-8") as fh:
        cohort = json.load(fh)
    for dom, band in cohort.get("domains", {}).items():
        for k in _BANDS:
            if k not in band:
                raise ValueError(f"benchmark cohort domain {dom!r} missing band {k!r}")
        if not (band.get("rationale") or "").strip():
            raise ValueError(f"benchmark cohort domain {dom!r} missing rationale "
                             "(synthetic bands must be justified)")
    if cohort_label_override:
        cohort["cohort_label"] = cohort_label_override
    return cohort


def position(met_pct, domain_slug, cohort):
    """Map a domain's met-% (fraction 0..1) onto the cohort quartile bands. Returns
    {percentile_band, cohort_label, basis_note}. Unknown domain -> explicit
    'no cohort baseline' (never invents a band)."""
    band = cohort.get("domains", {}).get(domain_slug)
    label = cohort.get("cohort_label", "")
    basis = cohort.get("basis", "")
    if not band:
        return {"percentile_band": "no cohort baseline", "cohort_label": label,
                "basis_note": basis}
    pct = round((met_pct or 0.0) * 100)
    if pct < band["p25"]:
        pb = "below p25 (bottom quartile)"
    elif pct < band["p50"]:
        pb = "p25–p50 (below median)"
    elif pct < band["p75"]:
        pb = "p50–p75 (above median)"
    else:
        pb = "above p75 (top quartile)"
    return {"percentile_band": pb, "cohort_label": label, "basis_note": basis}

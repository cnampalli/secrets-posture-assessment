"""Synthetic, clearly-labelled benchmark cohort — pure model helpers (no rendering).

Loads versioned per-domain met-% percentile bands from config/benchmark-cohort.json
and positions a domain's assessed met-% against them. The bands are a designed-honest
SYNTHETIC baseline (not a measured cohort); the loader refuses any band that lacks a
documented rationale so the honesty contract can't silently erode.
"""
import json
import os

_BANDS = ("p25", "p50", "p75")
# A6 honesty contract: every band set declares whether it is designed (synthetic)
# or observed (measured). `measured` is EARNED — it requires a sample size of at
# least MEASURED_MIN_N anonymised engagements; below that the label stays synthetic
# no matter how good the estimates feel.
VALID_COHORT_TYPES = ("synthetic", "measured")
MEASURED_MIN_N = 5


def load_cohort(cfgdir, cohort_label_override=None):
    """Read benchmark-cohort.json from `cfgdir`. Validates that every domain band
    set carries p25/p50/p75, a non-empty `rationale`, and an explicit `cohort_type`
    (synthetic | measured; `measured` additionally requires n >= MEASURED_MIN_N);
    raises ValueError otherwise (honesty gate). `cohort_label_override` (e.g. from
    engagement config) replaces the displayed cohort label without touching bands."""
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
        ct = band.get("cohort_type")
        if ct not in VALID_COHORT_TYPES:
            raise ValueError(f"benchmark cohort domain {dom!r} invalid/missing cohort_type "
                             f"{ct!r} (expected one of {VALID_COHORT_TYPES})")
        if ct == "measured" and int(band.get("n") or 0) < MEASURED_MIN_N:
            raise ValueError(f"benchmark cohort domain {dom!r} claims measured with "
                             f"n={band.get('n')!r} — measured requires n >= {MEASURED_MIN_N}")
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
                "basis_note": basis, "cohort_type": None, "n": 0}
    pct = round((met_pct or 0.0) * 100)
    if pct < band["p25"]:
        pb = "below p25 (bottom quartile)"
    elif pct < band["p50"]:
        pb = "p25–p50 (below median)"
    elif pct < band["p75"]:
        pb = "p50–p75 (above median)"
    else:
        pb = "above p75 (top quartile)"
    return {"percentile_band": pb, "cohort_label": label, "basis_note": basis,
            "cohort_type": band.get("cohort_type"), "n": int(band.get("n") or 0)}

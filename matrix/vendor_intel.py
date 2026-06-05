"""Vendor intelligence (pure, no I/O): best-vendor-for-X (B2) + head-to-head (B4).

Operates on the `ranked` row shape report_logic consumes. "Best for X" ranks the
actual providers of a target (UC / NHI / control-mapped UC) by coverage strength
then maturity; head-to-head builds a per-UC comparison grid for a vendor subset.
"""
from matrix_vocab import COVERAGE_ORDER as COVERAGE_RANK, UC_TYPES as _UC_TYPES

_PROVIDER = {"NATIVE", "ADD-ON", "PARTNER"}


def _mat(r):
    return int(r["maturity"]) if str(r.get("maturity", "")).isdigit() else 0


def best_for(target_id, ranked, coverage=None):
    """Rank the vendors that actually provide `target_id`, best first.

    Sort: coverage strength (NATIVE>ADD-ON>PARTNER) then maturity desc then slug.
    Non-providers (GAP / N/A) are excluded. `coverage`, if given, filters to a
    single coverage level. Each item carries evidence_quote/notes (B3 seed).
    """
    rows = [r for r in ranked if r["target_id"] == target_id
            and r["coverage"] in _PROVIDER
            and (coverage is None or r["coverage"] == coverage)]
    rows.sort(key=lambda r: (COVERAGE_RANK.get(r["coverage"], 9), -_mat(r), r["vendor_slug"]))
    return [{"vendor_slug": r["vendor_slug"], "vendor_name": r.get("vendor_name", r["vendor_slug"]),
             "coverage": r["coverage"], "maturity": _mat(r),
             "evidence_quote": r.get("evidence_quote", ""), "notes": r.get("notes", "")}
            for r in rows]


def head_to_head(slugs, ranked, uc_ids=None):
    """Per-UC comparison grid for `slugs`: {uc_id: {slug: {coverage, maturity}}}.

    uc_ids defaults to the union of UC targets any of the slugs touches. A vendor
    with no row for a UC is simply absent from that UC's dict (treat as GAP).
    """
    slugset = set(slugs)
    rel = [r for r in ranked if r["vendor_slug"] in slugset and r["target_type"] in _UC_TYPES]
    if uc_ids is None:
        uc_ids = sorted({r["target_id"] for r in rel})
    targets = set(uc_ids)
    grid = {u: {} for u in uc_ids}
    for r in rel:
        if r["target_id"] in targets:
            grid[r["target_id"]][r["vendor_slug"]] = {
                "coverage": r["coverage"], "maturity": _mat(r)}
    return grid

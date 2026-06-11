"""Resilience analytics against the real matrix data + the ownership config.

Proves the parent-aware fix actually changes the answer: collapsing sibling
brands under one corporate parent surfaces concentration that brand-counting hides.
"""
import os
import pathlib

import overlay as ov
import report_io
import resilience as rz

ROOT = pathlib.Path(__file__).resolve().parents[1]
MATRIX = ROOT / "matrix"
DATA = MATRIX / "domains" / "secrets"
CFGDIR = MATRIX / "config"


def _ownership():
    return ov.load_vendor_ownership(os.path.join(CFGDIR, "vendor-ownership.yaml"))


def test_load_vendor_ownership_maps_venafi_to_cyberark():
    own = _ownership()
    assert rz.parent_of("venafi", own) == "cyberark"
    assert rz.parent_of("cyberark-conjur", own) == "cyberark"
    # An independent vendor is its own parent.
    assert rz.parent_of("aws-secrets-manager", own) == "aws-secrets-manager"


def test_ownership_entries_carry_provenance():
    own = _ownership()
    # Acquisitions (parent != slug) must declare confidence so consultants can verify.
    for slug, meta in own.items():
        if meta.get("parent", slug) != slug:
            assert "confidence" in meta, f"{slug} missing confidence provenance"


def test_parent_collapse_never_removes_single_source_and_is_not_inert():
    ranked = report_io.load_inputs(str(DATA), "current-state.csv")["ranked"]
    own = _ownership()
    brand = rz.single_source(ranked, {})          # empty map -> count by brand
    parent = rz.single_source(ranked, own)        # collapse by parent
    # Collapsing can only add single-source UCs, never remove them.
    assert set(brand["single_source"]).issubset(set(parent["single_source"]))
    # The map must actually merge brands on at least one UC, or it is inert.
    cov = rz.coverage_by_parent(ranked, own)
    collapsed = [u for u, c in cov.items() if c["brand_count"] > c["parent_count"]]
    assert collapsed, "ownership map collapses no UCs — it is inert"


def test_parent_concentration_exceeds_largest_single_brand():
    """The headline CPS 230 signal: one parent's blast radius is far larger than
    any of its individual brands, which brand-counting hides."""
    ranked = report_io.load_inputs(str(DATA), "current-state.csv")["ranked"]
    own = _ownership()
    by_parent = rz.concentration(ranked, own)
    by_brand = rz.concentration(ranked, {})
    cy = by_parent["cyberark"]
    largest_brand = max(by_brand[b]["uc_count"] for b in cy["brands"])
    assert cy["uc_count"] > largest_brand          # parent dependency >> any one brand
    assert cy["share"] >= 0.5                       # CyberArk touches a majority of UCs


def test_cyberark_is_a_multi_brand_concentration_parent():
    ranked = report_io.load_inputs(str(DATA), "current-state.csv")["ranked"]
    con = rz.concentration(ranked, _ownership())
    assert "cyberark" in con
    assert len(con["cyberark"]["brands"]) >= 2     # ≥2 brands collapse into one parent

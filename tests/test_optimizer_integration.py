"""Optimizer against the real matrix data — regression oracle + white-space check."""
import os
import pathlib

import overlay as ov
import optimizer as opt
import report_io
import resilience as rz

ROOT = pathlib.Path(__file__).resolve().parents[1]
MATRIX = ROOT / "matrix"
DATA = MATRIX / "domains" / "secrets"
CFGDIR = MATRIX / "config"


def _load():
    ranked = report_io.load_inputs(str(DATA), "current-state.csv")["ranked"]
    own = ov.load_vendor_ownership(os.path.join(CFGDIR, "vendor-ownership.yaml"))
    return ranked, own


def test_first_pick_is_broadest_coverage_vendor():
    """Regression oracle: greedy's first pick is the broadest-coverage L1
    platform — the same vendor build_recdata flags as 'highest-coverage'."""
    ranked, own = _load()
    res = opt.greedy_cover(ranked, own)
    assert res["chosen"][0] == "hashicorp-vault-enterprise"


def test_whitespace_matches_resilience_uncovered():
    ranked, own = _load()
    res = opt.greedy_cover(ranked, own)
    uncovered = rz.single_source(ranked, own)["uncovered"]
    assert res["uncovered"] == sorted(uncovered)
    assert res["uncovered"]                          # there IS genuine white-space


def test_full_cover_is_not_monolithic_and_flags_concentration():
    ranked, own = _load()
    res = opt.greedy_cover(ranked, own)
    con = opt.portfolio_concentration(res["chosen"], ranked, own)
    assert con["distinct_parents"] >= 2              # not a single-vendor "win"
    assert 0.0 < con["max_parent_share"] < 1.0       # concentration is measured, bounded

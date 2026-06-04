"""Vendor intelligence: best-vendor-for-X ranking (B2) and head-to-head (B4)."""
import vendor_intel as vi

RANKED = [
    {"vendor_slug": "v1", "vendor_name": "V One", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3", "evidence_quote": "broad", "notes": "n1"},
    {"vendor_slug": "v2", "vendor_name": "V Two", "target_type": "UC-F", "target_id": "UC-1", "coverage": "ADD-ON", "maturity": "2", "evidence_quote": "", "notes": ""},
    {"vendor_slug": "v3", "vendor_name": "V Three", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "4", "evidence_quote": "best", "notes": ""},
    {"vendor_slug": "v4", "vendor_name": "V Four", "target_type": "UC-F", "target_id": "UC-1", "coverage": "GAP", "maturity": "0", "evidence_quote": "", "notes": ""},
    {"vendor_slug": "v1", "vendor_name": "V One", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "2", "evidence_quote": "", "notes": ""},
    {"vendor_slug": "v1", "vendor_name": "V One", "target_type": "NHI", "target_id": "NHI-1", "coverage": "NATIVE", "maturity": "4", "evidence_quote": "", "notes": ""},
]


def test_best_for_ranks_native_high_maturity_first():
    res = vi.best_for("UC-1", RANKED)
    assert [r["vendor_slug"] for r in res] == ["v3", "v1", "v2"]   # NAT4, NAT3, ADD2
    assert res[0]["maturity"] == 4                                 # maturity is int


def test_best_for_excludes_non_providers():
    res = vi.best_for("UC-1", RANKED)
    assert "v4" not in [r["vendor_slug"] for r in res]            # GAP is not a provider


def test_best_for_carries_evidence_for_feature_matrix():
    # B3 seed: the winning row carries its evidence quote for differentiator display.
    res = vi.best_for("UC-1", RANKED)
    assert res[0]["evidence_quote"] == "best"


def test_head_to_head_builds_per_uc_grid():
    grid = vi.head_to_head(["v1", "v3"], RANKED, uc_ids=["UC-1", "UC-2"])
    assert grid["UC-1"]["v1"]["coverage"] == "NATIVE"
    assert grid["UC-1"]["v3"]["maturity"] == 4
    # v3 has no UC-2 row -> absent / GAP sentinel
    assert grid["UC-2"]["v1"]["coverage"] == "NATIVE"
    assert grid["UC-2"].get("v3", {}).get("coverage", "GAP") == "GAP"


def test_head_to_head_defaults_to_union_of_uc_targets():
    grid = vi.head_to_head(["v1", "v3"], RANKED)
    assert set(grid.keys()) == {"UC-1", "UC-2"}                    # NHI target excluded

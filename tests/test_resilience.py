"""Parent-aware vendor concentration / lock-in resilience analytics.

The substitutability and concentration math MUST count by ultimate corporate
parent, not by brand — otherwise sibling brands under one parent (e.g.
CyberArk owns Conjur + Venafi) read as independent second-sources, inverting
the CPS 230 concentration signal.
"""
import resilience as rz

# Two CyberArk brands + independents. `parent` follows brand -> parent.
OWNERSHIP = {
    "cyberark-conjur": {"parent": "cyberark"},
    "venafi": {"parent": "cyberark"},
    "cyberark-pam": {"parent": "cyberark"},
}

RANKED = [
    # UC-1: NATIVE by two CyberArk brands only -> ONE parent (single-source).
    {"vendor_slug": "cyberark-conjur", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "venafi", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "2"},
    # UC-2: NATIVE by two distinct parents -> not single-source.
    {"vendor_slug": "cyberark-conjur", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "aws-secrets-manager", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "4"},
    # UC-3: only ADD-ON / GAP -> uncovered (zero NATIVE).
    {"vendor_slug": "aws-secrets-manager", "target_type": "UC-N", "target_id": "UC-3", "coverage": "ADD-ON", "maturity": "2"},
    {"vendor_slug": "doppler", "target_type": "UC-N", "target_id": "UC-3", "coverage": "GAP", "maturity": "0"},
    # An NHI row — must be ignored by the UC-scoped resilience math.
    {"vendor_slug": "aws-secrets-manager", "target_type": "NHI", "target_id": "NHI-1", "coverage": "NATIVE", "maturity": "4"},
]


def test_parent_of_defaults_to_self_when_unlisted():
    assert rz.parent_of("aws-secrets-manager", OWNERSHIP) == "aws-secrets-manager"


def test_parent_of_maps_acquired_brand_to_parent():
    assert rz.parent_of("venafi", OWNERSHIP) == "cyberark"


def test_coverage_by_parent_collapses_sibling_brands():
    cov = rz.coverage_by_parent(RANKED, OWNERSHIP)
    assert cov["UC-1"]["brand_count"] == 2
    assert cov["UC-1"]["parent_count"] == 1          # the whole point
    assert cov["UC-1"]["parents"] == ["cyberark"]


def test_coverage_by_parent_keeps_distinct_parents():
    cov = rz.coverage_by_parent(RANKED, OWNERSHIP)
    assert cov["UC-2"]["parent_count"] == 2
    assert cov["UC-2"]["parents"] == ["aws-secrets-manager", "cyberark"]


def test_coverage_by_parent_ignores_nhi_targets():
    cov = rz.coverage_by_parent(RANKED, OWNERSHIP)
    assert "NHI-1" not in cov


def test_single_source_counts_by_parent_not_brand():
    res = rz.single_source(RANKED, OWNERSHIP)
    # UC-1 has two brands but one parent -> single-source.
    assert "UC-1" in res["single_source"]
    # UC-2 has two parents -> not single-source.
    assert "UC-2" not in res["single_source"]


def test_uncovered_lists_ucs_with_no_native():
    res = rz.single_source(RANKED, OWNERSHIP)
    assert res["uncovered"] == ["UC-3"]
    assert "UC-3" not in res["single_source"]        # uncovered != single-source


def test_concentration_blast_radius_and_share():
    con = rz.concentration(RANKED, OWNERSHIP)
    # cyberark is native on UC-1 and UC-2 (2 of 2 natively-covered UCs).
    assert con["cyberark"]["uc_count"] == 2
    assert con["cyberark"]["share"] == 1.0
    assert con["aws-secrets-manager"]["uc_count"] == 1
    assert con["aws-secrets-manager"]["share"] == 0.5


def test_concentration_sole_source_ucs():
    con = rz.concentration(RANKED, OWNERSHIP)
    # cyberark is the ONLY native parent for UC-1, but UC-2 is also covered by aws.
    assert con["cyberark"]["sole_source_ucs"] == ["UC-1"]
    assert con["aws-secrets-manager"]["sole_source_ucs"] == []

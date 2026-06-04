"""Resilience-first vendor-mix optimizer: greedy set-cover that, on ties,
diversifies corporate parents rather than blindly minimising vendor count.
Reports white-space (uncoverable UCs) and the chosen portfolio's concentration.
"""
import optimizer as opt

# vA covers 3 UCs (clear first pick). UC-4 is then coverable by a sibling brand
# of A (vB, same parent P) OR by an independent (vC, parent Q).
OWNERSHIP = {"vA": {"parent": "P"}, "vB": {"parent": "P"}}

RANKED = [
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-3", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vB", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    {"vendor_slug": "vC", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    # UC-5 only ADD-ON -> white-space at NATIVE.
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-5", "coverage": "ADD-ON", "maturity": "1"},
    # NHI row must be ignored.
    {"vendor_slug": "vA", "target_type": "NHI", "target_id": "NHI-1", "coverage": "NATIVE", "maturity": "4"},
]


def test_greedy_cover_picks_highest_coverage_first():
    res = opt.greedy_cover(RANKED, OWNERSHIP)
    assert res["chosen"][0] == "vA"                 # covers the most UCs


def test_greedy_cover_reports_whitespace():
    res = opt.greedy_cover(RANKED, OWNERSHIP)
    assert res["uncovered"] == ["UC-5"]             # no NATIVE provider exists
    assert set(res["covered"]) == {"UC-1", "UC-2", "UC-3", "UC-4"}


def test_greedy_cover_minimises_vendor_count():
    res = opt.greedy_cover(RANKED, OWNERSHIP)
    assert len(res["chosen"]) == 2                  # vA + one provider of UC-4


def test_resilience_first_breaks_ties_toward_new_parent():
    res = opt.greedy_cover(RANKED, OWNERSHIP, resilience_first=True)
    # UC-4 tie: vB (parent P, already represented) vs vC (parent Q, new) -> vC.
    assert res["chosen"] == ["vA", "vC"]


def test_consolidation_mode_breaks_ties_deterministically():
    res = opt.greedy_cover(RANKED, OWNERSHIP, resilience_first=False)
    # No parent-diversity preference -> deterministic by gain then name -> vB.
    assert res["chosen"] == ["vA", "vB"]


def test_cover_restricted_to_priority_uc_subset():
    res = opt.greedy_cover(RANKED, OWNERSHIP, ucs={"UC-1", "UC-2"})
    assert set(res["covered"]) == {"UC-1", "UC-2"}
    assert res["chosen"] == ["vA"]
    assert res["uncovered"] == []


def test_portfolio_concentration_reports_max_parent_share():
    con = opt.portfolio_concentration(["vA", "vC"], RANKED, OWNERSHIP)
    assert con["distinct_parents"] == 2
    assert con["max_parent_share"] == 0.75          # P covers 3 of 4 covered UCs
    assert con["max_parent"] == "P"


def test_complement_finds_vendor_that_fills_most_gaps():
    # Have vA (covers UC-1,2,3). Gaps = UC-4 (coverable) + UC-5 (white-space).
    rec = opt.complement("vA", RANKED)
    assert rec["add"] in ("vB", "vC")               # both fill UC-4
    assert rec["fills"] == 1
    assert "UC-5" in rec["still_open"]              # white-space remains open
    assert "UC-4" not in rec["still_open"]


def test_complement_returns_none_when_nothing_left_to_fill():
    # vA covers everything coverable in this reduced set.
    rows = [r for r in RANKED if r["target_id"] in ("UC-1", "UC-2", "UC-3")]
    rec = opt.complement("vA", rows)
    assert rec is None

"""Identity-control coverage indicator (D3) + gap-to-target planner (D4).

A control counts as MET only when ALL its mapped use cases are MET (worst-state
rule). Coverage is reported against the identity-scoped control set — a coverage
indicator, NOT a full-framework compliance score.
"""
import compliance as cp

REG_ROWS = [
    {"framework_slug": "e8", "control_code": "E8-1", "control_short_title": "MFA", "uc_ids": "UC-1;UC-2"},
    {"framework_slug": "e8", "control_code": "E8-2", "control_short_title": "App control", "uc_ids": "UC-3"},
    {"framework_slug": "e8", "control_code": "E8-3", "control_short_title": "Restrict admin", "uc_ids": "UC-4"},
    {"framework_slug": "ism", "control_code": "ISM-1", "control_short_title": "Logging", "uc_ids": "UC-1"},
]
ANZ = [
    {"uc_id": "UC-1", "current_state": "MET"},
    {"uc_id": "UC-2", "current_state": "GAP"},
    {"uc_id": "UC-3", "current_state": "MET"},
    {"uc_id": "UC-4", "current_state": "PARTIAL"},
]


def test_coverage_indicator_counts_met_and_pct():
    ind = cp.coverage_indicator(REG_ROWS, ANZ)
    assert ind["e8"]["total"] == 3
    assert ind["e8"]["met"] == 1                  # only E8-2 (UC-3 MET)
    assert ind["e8"]["met_pct"] == round(1 / 3, 4)
    assert ind["ism"]["met"] == 1 and ind["ism"]["met_pct"] == 1.0


def test_control_met_only_when_all_mapped_ucs_met():
    ind = cp.coverage_indicator(REG_ROWS, ANZ)
    # E8-1 maps UC-1(MET)+UC-2(GAP) -> worst state GAP -> not met; counted as gap.
    assert ind["e8"]["gap"] == 1
    assert ind["e8"]["partial"] == 1             # E8-3 (UC-4 PARTIAL)


def test_gap_to_target_lists_blocking_ucs_only():
    gaps = cp.gap_to_target(REG_ROWS, ANZ, framework="e8")
    e81 = next(g for g in gaps if g["code"] == "E8-1")
    blocking = {b["uc"] for b in e81["blocking_ucs"]}
    assert blocking == {"UC-2"}                   # UC-1 is MET, not blocking


def test_gap_to_target_sorted_worst_first():
    gaps = cp.gap_to_target(REG_ROWS, ANZ, framework="e8")
    # GAP (E8-1) before PARTIAL (E8-3); MET control E8-2 absent.
    assert [g["code"] for g in gaps] == ["E8-1", "E8-3"]

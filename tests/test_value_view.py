"""Tests for the curated Value Proposition view builders (report_logic).

Covers the three pure builders that feed the unified `view-value` narrative:
- build_posture_maturity (board ML1/2/3 banding + per-group, incl. the P0-GAP cap)
- build_quick_wins (risk x effort ordering, GAP/PARTIAL-only, limit)
- build_value_callouts (provenance count + honest currency emerging-gap branch)
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import report_logic as rl


# ---------------------------------------------------------------------------
# build_posture_maturity
# ---------------------------------------------------------------------------

def _ucs(*pairs):
    return [{"uc_id": u, "priority_fi": p, "short_title": u} for u, p in pairs]


def test_posture_maturity_ml3_when_high_coverage_no_p0_gap_or_partial():
    ucs = _ucs(("UC-F-001", "P0"), ("UC-F-002", "P0"), ("UC-F-003", "P1"), ("UC-F-005", "P1"))
    anz = [{"uc_id": "UC-F-001", "current_state": "MET"},
           {"uc_id": "UC-F-002", "current_state": "MET"},
           {"uc_id": "UC-F-003", "current_state": "MET"},
           {"uc_id": "UC-F-005", "current_state": "PARTIAL"}]   # P1 partial is fine
    m = rl.build_posture_maturity(anz, ucs, "secrets")
    assert m["met_pct"] == 0.75
    assert m["overall_band"] == "ML3"
    assert m["p0_open"] == 0


def test_posture_maturity_ml2_when_managed_coverage_no_p0_gap():
    ucs = _ucs(("UC-F-001", "P0"), ("UC-F-002", "P1"), ("UC-F-003", "P1"), ("UC-F-005", "P1"))
    anz = [{"uc_id": "UC-F-001", "current_state": "MET"},
           {"uc_id": "UC-F-002", "current_state": "MET"},
           {"uc_id": "UC-F-003", "current_state": "PARTIAL"},
           {"uc_id": "UC-F-005", "current_state": "GAP"}]       # P1 gap only
    m = rl.build_posture_maturity(anz, ucs, "secrets")
    assert m["met_pct"] == 0.5
    assert m["overall_band"] == "ML2"


def test_posture_maturity_p0_gap_caps_at_ml1_even_with_high_coverage():
    # 3/4 MET = 0.75 (would be ML3) but a P0 UC is in GAP -> capped to ML1.
    ucs = _ucs(("UC-F-001", "P0"), ("UC-F-002", "P0"), ("UC-F-003", "P0"), ("UC-F-005", "P0"))
    anz = [{"uc_id": "UC-F-001", "current_state": "MET"},
           {"uc_id": "UC-F-002", "current_state": "MET"},
           {"uc_id": "UC-F-003", "current_state": "MET"},
           {"uc_id": "UC-F-005", "current_state": "GAP"}]
    m = rl.build_posture_maturity(anz, ucs, "secrets")
    assert m["overall_band"] == "ML1"
    assert m["p0_open"] >= 1


def test_posture_maturity_low_coverage_is_ml1():
    ucs = _ucs(("UC-F-001", "P1"), ("UC-F-002", "P1"), ("UC-F-003", "P1"))
    anz = [{"uc_id": "UC-F-001", "current_state": "MET"},
           {"uc_id": "UC-F-002", "current_state": "GAP"},
           {"uc_id": "UC-F-003", "current_state": "GAP"}]
    m = rl.build_posture_maturity(anz, ucs, "secrets")
    assert m["met_pct"] < 0.40
    assert m["overall_band"] == "ML1"


def test_posture_maturity_counts_and_basis_caption():
    ucs = _ucs(("UC-F-001", "P0"), ("UC-F-002", "P1"))
    anz = [{"uc_id": "UC-F-001", "current_state": "MET"},
           {"uc_id": "UC-F-002", "current_state": "PENDING"}]
    m = rl.build_posture_maturity(anz, ucs, "secrets")
    assert m["counts"] == {"met": 1, "partial": 0, "gap": 0, "pending": 1}
    assert isinstance(m["basis"], str) and m["basis"]              # honest convention caption


def test_posture_maturity_iga_groups_by_governance_area():
    # IGA per-area: 001-004 JML, 005-007 Cert, 008-010 SoD, 011-013 Role/Request.
    ucs = _ucs(("UC-I-001", "P0"), ("UC-I-002", "P0"),       # JML
               ("UC-I-005", "P0"), ("UC-I-006", "P0"),       # Certification
               ("UC-I-008", "P0"), ("UC-I-011", "P1"))       # SoD / Role-Request
    anz = [{"uc_id": "UC-I-001", "current_state": "MET"},
           {"uc_id": "UC-I-002", "current_state": "MET"},
           {"uc_id": "UC-I-005", "current_state": "GAP"},    # caps Certification at ML1
           {"uc_id": "UC-I-006", "current_state": "MET"},
           {"uc_id": "UC-I-008", "current_state": "MET"},
           {"uc_id": "UC-I-011", "current_state": "PARTIAL"}]
    m = rl.build_posture_maturity(anz, ucs, "iga")
    groups = {g["label"]: g for g in m["groups"]}
    assert "JML" in groups and "Certification" in groups
    assert groups["JML"]["band"] in ("ML2", "ML3")           # both P0 MET
    assert groups["Certification"]["band"] == "ML1"          # P0 GAP caps it


def test_posture_maturity_iga_unknown_id_bucketed_other():
    ucs = _ucs(("UC-I-099", "P1"))
    anz = [{"uc_id": "UC-I-099", "current_state": "MET"}]
    m = rl.build_posture_maturity(anz, ucs, "iga")
    assert any(g["label"] == "Other" for g in m["groups"])


# ---------------------------------------------------------------------------
# build_quick_wins
# ---------------------------------------------------------------------------

_QW_UCS = [
    {"uc_id": "UC-1", "priority_fi": "P0", "short_title": "High risk one"},
    {"uc_id": "UC-2", "priority_fi": "P1", "short_title": "Med risk two"},
    {"uc_id": "UC-3", "priority_fi": "P2", "short_title": "Low risk three"},
    {"uc_id": "UC-4", "priority_fi": "P0", "short_title": "Already met"},
]
_QW_ANZ = [
    {"uc_id": "UC-1", "current_state": "GAP"},
    {"uc_id": "UC-2", "current_state": "PARTIAL"},
    {"uc_id": "UC-3", "current_state": "GAP"},
    {"uc_id": "UC-4", "current_state": "MET"},        # excluded (not GAP/PARTIAL)
]
_QW_REG = [
    {"framework_slug": "apra-cps-234", "framework_role": "PRIMARY-LENS",
     "control_code": "CPS234-1", "control_short_title": "Access", "uc_ids": "UC-1"},
]
_QW_SCOPE = {"apra-cps-234"}


def test_quick_wins_excludes_met_and_orders_worst_risk_first():
    wins = rl.build_quick_wins(_QW_ANZ, _QW_UCS, _QW_REG, _QW_SCOPE)
    ids = [w["uc_id"] for w in wins]
    assert "UC-4" not in ids                       # MET excluded
    assert set(ids) <= {"UC-1", "UC-2", "UC-3"}    # only GAP/PARTIAL
    assert ids[0] == "UC-1"                         # P0 -> High risk first


def test_quick_wins_respects_limit():
    wins = rl.build_quick_wins(_QW_ANZ, _QW_UCS, _QW_REG, _QW_SCOPE, limit=2)
    assert len(wins) == 2


def test_quick_wins_carries_regulatory_driver_control_codes():
    wins = rl.build_quick_wins(_QW_ANZ, _QW_UCS, _QW_REG, _QW_SCOPE)
    uc1 = next(w for w in wins if w["uc_id"] == "UC-1")
    codes = [d["control_code"] for d in uc1["regulatory_driver"]]
    assert "CPS234-1" in codes
    assert uc1["state"] in ("GAP", "PARTIAL")
    assert uc1["risk_band"] == "High"


# ---------------------------------------------------------------------------
# build_value_callouts
# ---------------------------------------------------------------------------

_VC_REG = [
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP", "control_code": "CPS234-1",
     "evidence_url": "https://apra/1", "evidence_quote": "must control access"},
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP", "control_code": "CPS234-1",
     "evidence_url": "https://apra/1", "evidence_quote": "must control access"},   # dup control
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP", "control_code": "ISM-9",
     "evidence_url": "https://ism/9", "evidence_quote": "rotate keys"},
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP", "control_code": "ISM-99",
     "evidence_url": "", "evidence_quote": "no url -> not counted"},
]


def test_callouts_provenance_counts_distinct_controls_with_url_and_quote():
    co = rl.build_value_callouts(_VC_REG, identity_rows=[], igavfit={}, vendormix={})
    assert co["provenance"]["controls_with_source"] == 2     # CPS234-1, ISM-9 (deduped; ISM-99 no url)


def test_callouts_currency_emerging_zero_for_secrets_like_identities():
    # secrets/PAM identities have no EMERGING bucket -> honest forward-looking gap branch.
    ids = [{"nhi_id": "x", "bucket": "UNCOMMON"}, {"nhi_id": "y", "bucket": "COMMON"}]
    co = rl.build_value_callouts(_VC_REG, ids, igavfit={}, vendormix={})
    assert co["currency"]["emerging_count"] == 0
    assert co["currency"]["classes"] == []


def test_callouts_currency_emerging_two_for_iga():
    ids = [{"nhi_id": "IGID-012", "bucket": "EMERGING", "short_name": "Agentic-AI"},
           {"nhi_id": "IGID-013", "bucket": "EMERGING", "short_name": "OAuth consent-grant"},
           {"nhi_id": "IGID-001", "bucket": "COMMON", "short_name": "Service account"}]
    co = rl.build_value_callouts(_VC_REG, ids, igavfit={}, vendormix={})
    assert co["currency"]["emerging_count"] == 2
    assert "Agentic-AI" in co["currency"]["classes"]


def test_callouts_independence_from_igavfit_per_area():
    igavfit = {"areas": ["JML", "Certification"], "vendors": [
        {"vendor": "V1", "cells": {"JML": {"fit": "NATIVE"}, "Certification": {"fit": "PARTIAL"}}},
        {"vendor": "V2", "cells": {"JML": {"fit": "PARTIAL"}, "Certification": {"fit": "ADD-ON"}}},
    ]}
    co = rl.build_value_callouts(_VC_REG, [], igavfit=igavfit, vendormix={})
    assert co["independence"]["native"] == 1
    assert co["independence"]["partial"] == 2

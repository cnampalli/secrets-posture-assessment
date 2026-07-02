"""A6 calibration scaffolding tests: agreement math + panel template integrity."""
import csv
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "methodology" / "calibration"))

import compute_agreement as ca  # noqa: E402


def test_weighted_kappa_perfect_agreement():
    assert ca.weighted_kappa([(0, 0), (1, 1), (2, 2), (0, 0)]) == 1.0


def test_weighted_kappa_undefined_on_tiny_input():
    assert ca.weighted_kappa([(1, 1)]) is None


def test_weighted_kappa_penalises_far_disagreement_more():
    near = ca.weighted_kappa([(0, 0), (1, 1), (2, 2), (1, 2), (0, 0), (2, 2)])
    far = ca.weighted_kappa([(0, 0), (1, 1), (2, 2), (0, 2), (0, 0), (2, 2)])
    assert near is not None and far is not None and near > far


def test_score_panel_excludes_pending_and_blank():
    rows = [
        {"domain": "pam", "reviewer_state": "MET", "instrument_state": "MET"},
        {"domain": "pam", "reviewer_state": "PENDING", "instrument_state": "MET"},
        {"domain": "pam", "reviewer_state": "", "instrument_state": "GAP"},
    ]
    res = ca.score_panel(rows)
    assert res["scoreable_rows"] == 1 and res["excluded_rows"] == 2
    assert res["domains"]["pam"]["raw_agreement"] == 1.0


def test_panel_template_matches_live_use_cases():
    # every sampled uc_id must exist in its domain's live use-cases.csv, 5 per domain
    tpl = list(csv.DictReader(open(ROOT / "methodology" / "calibration"
                                   / "sme-panel-template.csv", encoding="utf-8")))
    assert len(tpl) == 15
    by_dom = {}
    for r in tpl:
        by_dom.setdefault(r["domain"], []).append(r["uc_id"])
    assert {d: len(v) for d, v in by_dom.items()} == {"secrets": 5, "pam": 5, "iga": 5}
    for dom, ids in by_dom.items():
        live = {r["uc_id"] for r in csv.DictReader(
            open(ROOT / "matrix" / "domains" / dom / "use-cases.csv", encoding="utf-8"))}
        missing = set(ids) - live
        assert not missing, f"{dom}: template samples unknown UCs {sorted(missing)}"


def test_template_reviewer_columns_blank():
    # the committed template must be UNFILLED (a filled sheet is engagement data)
    tpl = list(csv.DictReader(open(ROOT / "methodology" / "calibration"
                                   / "sme-panel-template.csv", encoding="utf-8")))
    for r in tpl:
        assert r["reviewer_state"] == "" and r["reviewer_id"] == ""

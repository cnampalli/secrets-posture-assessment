import json, pathlib
import methodology.scoring as scoring

ROOT = pathlib.Path(__file__).resolve().parents[1]
VECTORS = json.load(open(ROOT / "questionnaire" / "scoring-vectors.json"))


def test_all_met():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes", "Q2": "yes"}) == "MET"


def test_gap_partial_no_is_gap():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "no", "Q2": "yes"}) == "GAP"


def test_partial_met_no_is_partial():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes", "Q2": "no"}) == "PARTIAL"


def test_unanswered_is_pending():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}, {"qid": "Q2", "informs_state": "PARTIAL_MET"}]
    assert scoring.derive_state(qs, {"Q1": "yes"}) == "PENDING"


def test_all_na_is_na():
    qs = [{"qid": "Q1", "informs_state": "GAP_PARTIAL"}]
    assert scoring.derive_state(qs, {"Q1": "na"}) == "NA"


def test_vectors_fixture():
    for v in VECTORS:
        assert scoring.derive_state(v["questions"], v["answers"]) == v["expected"], v["name"]

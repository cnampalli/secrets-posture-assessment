import questionnaire.record_state as rs


def test_resolve_prefers_final():
    assert rs.resolve_state({"final_state": "GAP", "proposed_state": "PARTIAL"}) == "GAP"


def test_resolve_falls_back_to_proposed():
    assert rs.resolve_state({"final_state": None, "proposed_state": "MET"}) == "MET"


def test_resolve_defaults_pending():
    assert rs.resolve_state({"final_state": None, "proposed_state": None}) == "PENDING"
    assert rs.resolve_state({}) == "PENDING"
    assert rs.resolve_state(None) == "PENDING"


def test_schema_constant():
    assert rs.SCHEMA == "posture-assessment-record/v1"

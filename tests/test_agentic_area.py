import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "matrix"))
import report_logic as rl  # noqa: E402


def test_agentic_ucs_map_to_agentic_area():
    assert rl._iga_area_for("UC-I-017") == "Agentic governance"
    assert rl._iga_area_for("UC-I-018") == "Agentic governance"
    assert rl._iga_area_for("UC-I-019") == "Agentic governance"


def test_existing_areas_unchanged():
    assert rl._iga_area_for("UC-I-001") == "JML"
    assert rl._iga_area_for("UC-I-005") == "Certification"


def test_agentic_area_in_posture_order_not_in_vendor_fit():
    assert "Agentic governance" in rl._IGA_POSTURE_AREAS
    assert "Agentic governance" not in rl.IGA_AREAS

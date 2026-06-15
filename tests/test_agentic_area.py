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


# --- M3.2: secrets "Agentic" posture area ---

def test_secrets_has_agentic_posture_group():
    g = rl.MATURITY_GROUPS["secrets"]
    assert "Agentic" in g
    agentic = set(g["Agentic"])
    assert {"UC-F-011", "UC-F-015", "UC-F-018",
            "UC-F-028", "UC-F-029", "UC-F-030", "UC-N-019"} <= agentic


def test_secrets_agentic_ucs_counted_once():
    g = rl.MATURITY_GROUPS["secrets"]
    seen = {}
    for ids in g.values():
        for uc in ids:
            seen[uc] = seen.get(uc, 0) + 1
    for uc in ("UC-F-015", "UC-F-018"):  # these were in REC_UC_DOMAIN["secrets"]
        assert seen.get(uc) == 1, f"{uc} appears in more than one posture group"


def test_rec_uc_domain_not_mutated():
    # REC_UC_DOMAIN is shared with the recommendations engine; subtraction must be non-mutating.
    assert "UC-F-015" in rl.REC_UC_DOMAIN["secrets"]
    assert "UC-F-018" in rl.REC_UC_DOMAIN["secrets"]


# --- M3.3: PAM "Agentic privileged access" posture area ---

def test_pam_has_agentic_posture_group():
    g = rl.MATURITY_GROUPS["pam"]
    assert "Agentic privileged access" in g
    assert set(g["Agentic privileged access"]) == {"UC-P-019", "UC-P-020", "UC-P-021"}

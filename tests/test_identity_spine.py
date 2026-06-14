import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import identity_spine  # noqa: E402
import validate_data  # noqa: E402

CFGDIR = os.path.join(MATRIX, "config")


# ---- load_spine ----

def test_load_spine_parses_registry():
    spine = identity_spine.load_spine(CFGDIR)
    assert len(spine["archetypes"]) >= 10
    # index keyed by spine_id
    first = spine["archetypes"][0]
    assert spine["by_id"][first["spine_id"]] is first


def test_load_spine_has_all_three_classes():
    spine = identity_spine.load_spine(CFGDIR)
    classes = {a["identity_class"] for a in spine["archetypes"]}
    assert classes == {"human", "npe", "agentic"}


# ---- check_identity_spine_registry ----

def _spine(archetypes):
    return {"archetypes": archetypes, "by_id": {a["spine_id"]: a for a in archetypes}}


_GOOD = [
    {"spine_id": "SPN-001", "label": "Privileged human administrator", "identity_class": "human",
     "privileged": True, "description": "x", "csa_nhi_anchor": "NIST AC-6", "spiffe_ref": ""},
    {"spine_id": "SPN-007", "label": "Cloud / workload identity", "identity_class": "npe",
     "privileged": False, "description": "y", "csa_nhi_anchor": "CSA NHI: cloud workload",
     "spiffe_ref": "SPIFFE SVID"},
]


def test_registry_clean_passes():
    assert validate_data.check_identity_spine_registry(_spine(_GOOD)) == []


def test_registry_missing_file_fails():
    errs = validate_data.check_identity_spine_registry({"archetypes": [], "by_id": {}})
    assert len(errs) == 1 and "missing" in errs[0].lower()


def test_registry_duplicate_id_fails():
    dup = _GOOD + [dict(_GOOD[0])]
    errs = validate_data.check_identity_spine_registry(_spine(dup))
    assert any("SPN-001" in e and "duplicate" in e.lower() for e in errs)


def test_registry_bad_class_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-099", identity_class="robot")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("identity_class" in e for e in errs)


def test_registry_non_bool_privileged_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-098", privileged="yes")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("privileged" in e for e in errs)


def test_registry_missing_anchor_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-097", csa_nhi_anchor="")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("csa_nhi_anchor" in e for e in errs)

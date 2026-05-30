import questionnaire.roadmap_generator as rg


def test_seed_risk_mapping():
    assert rg.seed_risk("P0") == "High"
    assert rg.seed_risk("P1") == "Med"
    assert rg.seed_risk("P2") == "Low"
    assert rg.seed_risk("") == "Low"
    assert rg.seed_risk(None) == "Low"
    assert rg.seed_risk("weird") == "Low"


def test_quadrant_corners():
    assert rg.quadrant("High", "Low") == "Quick wins"
    assert rg.quadrant("High", "High") == "Major projects"
    assert rg.quadrant("Low", "Low") == "Fill-ins"
    assert rg.quadrant("Low", "High") == "Hard slogs"


def test_quadrant_med_bands():
    # Med risk counts as the high side; Med effort counts as the low (actionable) side.
    assert rg.quadrant("Med", "Med") == "Quick wins"
    assert rg.quadrant("Med", "High") == "Major projects"
    assert rg.quadrant("Low", "Med") == "Fill-ins"


TRACE = [
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP",
     "control_code": "CPS234-§35b", "control_short_title": "Testing", "uc_ids": "UC-F-001;UC-F-002"},
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP",
     "control_code": "CPS234-§28a", "control_short_title": "Controls", "uc_ids": "UC-F-001"},
    {"framework_slug": "essential-8", "framework_role": "PRIMARY-LENS",
     "control_code": "E8-AppControl", "control_short_title": "App control", "uc_ids": "UC-F-001"},
    {"framework_slug": "cisa-ztmm-v2", "framework_role": "PRIMARY-LENS",
     "control_code": "ZT-Identity", "control_short_title": "Identity", "uc_ids": "UC-F-001"},
    {"framework_slug": "mitre-attack", "framework_role": "ADVERSARY-LENS",
     "control_code": "T1552", "control_short_title": "Unsecured creds", "uc_ids": "UC-F-001"},
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP",
     "control_code": "ISM-1619", "control_short_title": "Out of scope fw", "uc_ids": "UC-F-001"},
]
SCOPE = {"apra-cps-234", "essential-8", "cisa-ztmm-v2"}  # note: asd-ism NOT in scope; mitre excluded


def test_driver_excludes_mitre_and_out_of_scope():
    drivers = rg.regulatory_driver("UC-F-001", TRACE, SCOPE)
    slugs = [d["framework_slug"] for d in drivers]
    assert "mitre-attack" not in slugs          # adversary lens excluded
    assert "asd-ism" not in slugs                # not in scope


def test_driver_one_per_framework_min_control_code_regulator_first():
    drivers = rg.regulatory_driver("UC-F-001", TRACE, SCOPE)
    # one per framework (apra picks the lexicographically smallest code §28a < §35b)
    assert [d["framework_slug"] for d in drivers] == ["apra-cps-234", "cisa-ztmm-v2", "essential-8"]
    assert drivers[0]["control_code"] == "CPS234-§28a"   # regulator (BACK-MAP) first
    assert set(drivers[0]) == {"framework_slug", "control_code", "control_short_title"}


def test_driver_caps_at_three():
    big_scope = {"apra-cps-234", "essential-8", "cisa-ztmm-v2", "asd-ism"}
    assert len(rg.regulatory_driver("UC-F-001", TRACE, big_scope)) == 3


def test_driver_empty_when_no_match():
    assert rg.regulatory_driver("UC-NONE", TRACE, SCOPE) == []

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


RECORD = {
    "schema": "posture-assessment-record/v1",
    "responses": {
        "UC-F-001": {"proposed_state": "GAP", "final_state": "GAP"},      # P0 -> High
        "UC-F-002": {"proposed_state": "PARTIAL", "final_state": None},   # fallback PARTIAL; P1 -> Med
        "UC-MET":   {"proposed_state": "MET", "final_state": "MET"},      # excluded
        "UC-PEND":  {"proposed_state": None, "final_state": None},        # PENDING -> excluded
    },
}
USE_CASES = {
    "UC-F-001": {"uc_id": "UC-F-001", "short_title": "Prevent plaintext secrets in source repos", "priority_fi": "P0"},
    "UC-F-002": {"uc_id": "UC-F-002", "short_title": "Detect and remediate secrets in history", "priority_fi": "P1"},
}


def test_build_filters_to_gap_partial():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    ids = [it["uc_id"] for it in menu["items"]]
    assert ids == ["UC-F-001", "UC-F-002"]          # MET + PENDING excluded; ordered
    assert menu["schema"] == "engagement-menu/v1"
    assert menu["frameworks_scope"] == sorted(SCOPE)


def test_build_bands_and_quadrant_and_proposed():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    item = {it["uc_id"]: it for it in menu["items"]}["UC-F-001"]
    assert item["state"] == "GAP"
    assert item["risk_band"] == "High"              # P0 seed
    assert item["effort_band"] == "Med"             # default
    assert item["quadrant"] == "Quick wins"
    assert item["proposed_engagement"] == "GAP → remediate: Prevent plaintext secrets in source repos"
    assert item["dependency"] == ""
    assert item["regulatory_driver"][0]["framework_slug"] == "apra-cps-234"


def test_engagement_overrides_apply():
    eng = {"UC-F-001": {"risk_override": "Low", "effort": "High", "dependency": "inventory layer first"}}
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, eng, SCOPE)
    item = {it["uc_id"]: it for it in menu["items"]}["UC-F-001"]
    assert item["risk_band"] == "Low"
    assert item["effort_band"] == "High"
    assert item["quadrant"] == "Hard slogs"
    assert item["dependency"] == "inventory layer first"


def test_ordering_quadrant_then_risk_then_driver_then_id():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    # Both land in Quick wins; tie broken by risk desc: High (F-001) before Med (F-002).
    assert [it["uc_id"] for it in menu["items"]] == ["UC-F-001", "UC-F-002"]


def test_wrong_schema_raises():
    import pytest
    with pytest.raises(rg.RoadmapError):
        rg.build_engagement_menu({"schema": "nope", "responses": {}}, {}, [], {}, SCOPE)


def test_no_generated_timestamp_key():
    menu = rg.build_engagement_menu(RECORD, USE_CASES, TRACE, {}, SCOPE)
    assert "generated" not in menu

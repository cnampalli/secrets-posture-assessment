import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import report_logic as rl


def test_build_glossary_truncates_long_description():
    long = "x" * 200
    nhis = [{"nhi_id": "NHI-1", "short_name": "Svc", "description": long}]
    g = rl.build_glossary(nhis, [])
    assert g["NHI-1"].startswith("Svc — ")
    assert g["NHI-1"].endswith("...")
    assert len(g["NHI-1"]) < len("Svc — ") + 200


def test_build_glossary_short_desc_and_legend_keys():
    nhis = [{"nhi_id": "NHI-2", "short_name": "Bot", "description": "short"}]
    ucs = [{"uc_id": "UC-F-001", "short_title": "Prevent secrets"}]
    g = rl.build_glossary(nhis, ucs)
    assert g["NHI-2"] == "Bot — short"
    assert g["UC-F-001"] == "Prevent secrets"          # UC titles included
    assert g["NATIVE"].startswith("Vendor's first-class")  # legend present
    assert "0" in g and "4" in g                        # maturity legend present


def test_build_glossary_empty_description_uses_short_name_only():
    g = rl.build_glossary([{"nhi_id": "NHI-3", "short_name": "Svc", "description": ""}], [])
    assert g["NHI-3"] == "Svc"


_VM_OWN = {"vA": {"parent": "P"}, "vB": {"parent": "P"}}
_VM_RANKED = [
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-3", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vB", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    {"vendor_slug": "vC", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-5", "coverage": "ADD-ON", "maturity": "1"},
]
_VM_SHORT = {"vA": "Vendor A", "vB": "Vendor B", "vC": "Vendor C"}


def test_build_vendormix_reports_cover_and_whitespace():
    vm = rl.build_vendormix(_VM_RANKED, _VM_OWN, anchors=["vA"], short=_VM_SHORT)
    assert vm["cover"]["white_space"] == ["UC-5"]
    assert vm["cover"]["covered_count"] == 4
    assert vm["cover"]["uc_total"] == 5
    # chosen carries display names alongside slugs
    assert vm["cover"]["chosen"][0]["name"] == "Vendor A"


def test_build_vendormix_includes_concentration_and_complementary():
    vm = rl.build_vendormix(_VM_RANKED, _VM_OWN, anchors=["vA"], short=_VM_SHORT)
    # concentration scorecard sorted by share desc; P (vA) is the top parent.
    assert vm["concentration"][0]["parent"] == "P"
    # data-driven complementary: have Vendor A -> add a UC-4 provider.
    rec = vm["complementary"][0]
    assert rec["have"] == "Vendor A"
    assert rec["add"] in ("Vendor B", "Vendor C")


_CMP_REG = [
    {"framework_slug": "e8", "control_code": "E8-1", "control_short_title": "MFA", "uc_ids": "UC-1;UC-2"},
    {"framework_slug": "e8", "control_code": "E8-2", "control_short_title": "App", "uc_ids": "UC-3"},
]
_CMP_ANZ = [
    {"uc_id": "UC-1", "current_state": "MET"}, {"uc_id": "UC-2", "current_state": "GAP"},
    {"uc_id": "UC-3", "current_state": "MET"},
]
_CMP_LABELS = {"e8": ("Essential 8", "ACSC")}


def test_build_compliance_shapes_frameworks_with_labels():
    cmp = rl.build_compliance(_CMP_REG, _CMP_ANZ, _CMP_LABELS)
    fw = {f["slug"]: f for f in cmp["frameworks"]}["e8"]
    assert fw["label"] == "Essential 8"
    assert fw["total"] == 2 and fw["met"] == 1
    assert fw["met_pct"] == round(1 / 2, 4)


def test_build_compliance_lists_gap_to_target():
    cmp = rl.build_compliance(_CMP_REG, _CMP_ANZ, _CMP_LABELS)
    codes = [g["code"] for g in cmp["gap_to_target"]]
    assert "E8-1" in codes and "E8-2" not in codes        # E8-2 is MET


def test_build_compliance_exclusion_is_caller_driven_not_hardcoded():
    # report_logic no longer hardcodes the informative-framework list; the caller
    # (the domain descriptor) supplies it. Default = exclude nothing.
    reg = [{"framework_slug": "mitre-attack", "control_code": "T1", "control_short_title": "x", "uc_ids": "UC-1"},
           {"framework_slug": "e8", "control_code": "E8-1", "control_short_title": "y", "uc_ids": "UC-1"}]
    anz = [{"uc_id": "UC-1", "current_state": "GAP"}]
    labels = {"e8": ("E8", ""), "mitre-attack": ("ATT&CK", "")}
    default = {f["slug"] for f in rl.build_compliance(reg, anz, labels)["frameworks"]}
    assert "mitre-attack" in default                      # not excluded by default anymore
    scoped = {f["slug"] for f in rl.build_compliance(reg, anz, labels, exclude={"mitre-attack"})["frameworks"]}
    assert "mitre-attack" not in scoped                   # caller's exclude is honoured


_VI_UCS = [
    {"uc_id": "UC-1", "short_title": "One", "priority_fi": "P0"},
    {"uc_id": "UC-2", "short_title": "Two", "priority_fi": "P1"},
]
_VI_RANKED = [
    {"vendor_slug": "v1", "vendor_name": "V1", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3", "evidence_quote": "ev1", "notes": ""},
    {"vendor_slug": "v2", "vendor_name": "V2", "target_type": "UC-F", "target_id": "UC-1", "coverage": "ADD-ON", "maturity": "2", "evidence_quote": "", "notes": ""},
    {"vendor_slug": "v1", "vendor_name": "V1", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "4", "evidence_quote": "", "notes": ""},
]
_VI_SHORT = {"v1": "Vee One", "v2": "Vee Two"}


def test_build_vendor_intel_best_per_uc_with_evidence():
    vi = rl.build_vendor_intel(_VI_RANKED, _VI_UCS, ["v1"], _VI_SHORT)
    by_uc = {b["uc"]: b for b in vi["best_per_uc"]}
    assert by_uc["UC-1"]["vendor"] == "Vee One"
    assert by_uc["UC-1"]["coverage"] == "NATIVE" and by_uc["UC-1"]["maturity"] == 3
    assert by_uc["UC-1"]["evidence"] == "ev1"        # B3 differentiator
    assert by_uc["UC-1"]["alternatives"] == 1        # v2 is the other provider


def test_build_vendor_intel_head_to_head_scopes_to_p0():
    vi = rl.build_vendor_intel(_VI_RANKED, _VI_UCS, ["v1"], _VI_SHORT)
    h = vi["head_to_head"]
    assert h["uc_ids"] == ["UC-1"]                    # only P0
    assert h["grid"]["UC-1"]["v1"]["maturity"] == 3


def test_compute_meta_counts():
    m = rl.compute_meta(all_rows=[{"vendor_slug": "a"}, {"vendor_slug": "a"}],
                        ranked=[{"vendor_slug": "a"}], nhis=[{}, {}], ucs=[{}])
    assert m["nhis"] == 2
    assert m["ucs"] == 1
    assert m["total_rows"] == 2
    assert m["ranked_rows"] == 1
    assert m["ranked_vendors"] == 1


# --- regulatory evidence packs in the compliance-trace model ----------------

_EV_REG = [
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP", "control_code": "ISM-1619",
     "uc_ids": "UC-P-001;UC-P-006", "evidence_item_ids": "EV-A;EV-SHARED"},
    {"framework_slug": "apra-cps-234", "framework_role": "BACK-MAP", "control_code": "CPS234-§21(b)",
     "uc_ids": "UC-P-001", "evidence_item_ids": "EV-SHARED"},
    {"framework_slug": "asd-ism", "framework_role": "BACK-MAP", "control_code": "ISM-9999",
     "uc_ids": "UC-P-002", "evidence_item_ids": ""},                       # no pack
    {"framework_slug": "mitre-attack", "framework_role": "ADVERSARY-LENS", "control_code": "T-1",
     "uc_ids": "UC-P-001", "evidence_item_ids": "EV-A"},                   # adversary -> ignored
]
_EV_CAT = [
    {"ev_id": "EV-A", "requirement": "register of vaulted accounts", "dimension": "coverage",
     "tier": "primary", "example_artifact": "e.g. export", "sensitivity_tag": "[INTERNAL]",
     "citation_keys": "c1"},
    {"ev_id": "EV-SHARED", "requirement": "rotation policy", "dimension": "depth",
     "tier": "primary", "example_artifact": "", "sensitivity_tag": "[SENSITIVE]", "citation_keys": "c2"},
]


def test_control_evidence_resolves_items_per_control():
    ev = rl.build_control_evidence(_EV_REG, _EV_CAT)
    items = {e["ev_id"]: e for e in ev["by_control"]["ISM-1619"]}
    assert set(items) == {"EV-A", "EV-SHARED"}
    assert items["EV-A"]["requirement"] == "register of vaulted accounts"
    assert items["EV-A"]["tier"] == "primary"
    assert items["EV-A"]["sensitivity_tag"] == "[INTERNAL]"


def test_control_evidence_reverse_satisfies_lists_all_controls():
    ev = rl.build_control_evidence(_EV_REG, _EV_CAT)
    shared = next(e for e in ev["by_control"]["CPS234-§21(b)"] if e["ev_id"] == "EV-SHARED")
    assert shared["satisfies"] == ["CPS234-§21(b)", "ISM-1619"]   # sorted, both controls


def test_control_evidence_index_dedupes_and_counts_ucs():
    idx = {e["ev_id"]: e for e in rl.build_control_evidence(_EV_REG, _EV_CAT)["index"]}
    assert set(idx) == {"EV-A", "EV-SHARED"}
    # EV-SHARED is referenced by ISM-1619 (UC-P-001;UC-P-006) and CPS234-§21(b) (UC-P-001)
    assert idx["EV-SHARED"]["satisfies"] == ["CPS234-§21(b)", "ISM-1619"]
    assert idx["EV-SHARED"]["uc_count"] == 2                       # UC-P-001, UC-P-006 (deduped)
    assert idx["EV-A"]["uc_count"] == 2


def test_control_evidence_skips_adversary_and_handles_empty_catalog():
    ev = rl.build_control_evidence(_EV_REG, _EV_CAT)
    assert "T-1" not in ev["by_control"]                          # adversary-lens excluded
    assert ev["by_control"].get("ISM-9999", []) == []             # control with no pack
    empty = rl.build_control_evidence(_EV_REG, [])
    assert empty["by_control"] == {} and empty["index"] == []     # no catalog -> nothing

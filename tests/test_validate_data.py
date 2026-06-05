import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import validate_data as vd


def test_required_columns_flags_missing():
    rows = [{"uc_id": "UC-1", "category": "F"}]   # missing most cols
    errs = vd.check_required_columns("use-cases.csv", rows, vd.CORE_REQUIRED["use-cases.csv"])
    assert any("short_title" in e for e in errs)
    assert all("use-cases.csv" in e for e in errs)


def test_required_columns_empty():
    assert vd.check_required_columns("x.csv", [], ("a",)) == ["x.csv: empty (no data rows)"]


def test_required_columns_clean():
    rows = [{c: "v" for c in vd.CORE_REQUIRED["identity-catalog.csv"]}]
    assert vd.check_required_columns("identity-catalog.csv", rows, vd.CORE_REQUIRED["identity-catalog.csv"]) == []


def test_unique_flags_duplicate():
    rows = [{"uc_id": "UC-1"}, {"uc_id": "UC-1"}]
    assert vd.check_unique("use-cases.csv", rows, "uc_id") == ["use-cases.csv: duplicate uc_id 'UC-1'"]


def test_enum_flags_invalid_and_allows_blank():
    rows = [{"current_state": "GAP"}, {"current_state": "BOGUS"}, {"current_state": ""}]
    errs = vd.check_enum("current-state.csv", rows, "current_state", vd.VALID_STATES)
    assert errs == ["current-state.csv: invalid current_state 'BOGUS'"]


def test_ids_drops_blanks_and_sentinels():
    assert vd._ids("UC-1;;MISSING-UC;UC-2") == ["UC-1", "UC-2"]


def test_vendor_rows_flags_maturity_and_coverage():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"target_id": "NHI-1", "maturity": "9", "coverage": ""})
    errs = vd.validate_vendor_rows("v.csv", rows)
    assert any("maturity '9'" in e for e in errs)
    assert any("empty coverage" in e for e in errs)


def test_vendor_rows_accepts_zero_maturity():
    rows = [{c: "x" for c in vd.VENDOR_REQUIRED}]
    rows[0].update({"maturity": "0", "coverage": "GAP"})
    assert vd.validate_vendor_rows("v.csv", rows) == []


def test_vendor_rows_single_slug():
    rows = [dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="a", maturity="1", coverage="NATIVE"),
            dict({c: "x" for c in vd.VENDOR_REQUIRED}, vendor_slug="b", maturity="1", coverage="NATIVE")]
    assert any("multiple vendor_slug" in e for e in vd.validate_vendor_rows("v.csv", rows, single_slug=True))


def test_referential_clean():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-1"}]
    cs = [{"uc_id": "UC-F-1"}]
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-F-1;MISSING-UC", "nhi_ids": "NHI-1;MISSING-NHI"}]
    vendors = [("v.csv", [{"target_type": "UC-F", "target_id": "UC-F-1"},
                          {"target_type": "NHI", "target_id": "NHI-1"}])]
    assert vd.validate_referential(uc, cs, rt, idc, vendors) == []


def test_referential_catches_dangling():
    uc = [{"uc_id": "UC-F-1", "nhis_in_scope": "NHI-9"}]   # NHI-9 missing
    cs = [{"uc_id": "UC-F-2"}]                              # not in use-cases
    idc = [{"nhi_id": "NHI-1"}]
    rt = [{"control_code": "C1", "uc_ids": "UC-X", "nhi_ids": "NHI-Y"}]
    vendors = [("v.csv", [{"target_type": "NHI", "target_id": "NHI-Z"}])]
    errs = vd.validate_referential(uc, cs, rt, idc, vendors)
    assert any("NHI-9" in e for e in errs)
    assert any("UC-F-2" in e for e in errs)
    assert any("UC-X" in e for e in errs)
    assert any("NHI-Y" in e for e in errs)
    assert any("NHI-Z" in e for e in errs)


import shutil


def test_validate_all_real_data_is_clean():
    # The shipped data is the golden baseline — zero violations.
    assert vd.validate_all(str(ROOT)) == []


def test_main_exit_zero_on_clean():
    assert vd.main(["--root", str(ROOT)]) == 0


def test_validate_all_accepts_external_data_dir(tmp_path):
    # The gate must validate a non-default domain data dir (e.g. matrix/domains/pam),
    # resolving the shared cross-domain config from <root>/matrix/config. Copying the
    # clean secrets data into an arbitrary dir and validating it there must stay clean.
    ddir = tmp_path / "pam"
    ddir.mkdir()
    for p in (ROOT / "matrix").glob("*.csv"):
        shutil.copy(p, ddir / p.name)
    assert vd.validate_all(root=str(ROOT), data_dir=str(ddir)) == []


def test_main_accepts_data_dir_flag(tmp_path):
    ddir = tmp_path / "pam"
    ddir.mkdir()
    for p in (ROOT / "matrix").glob("*.csv"):
        shutil.copy(p, ddir / p.name)
    assert vd.main(["--root", str(ROOT), "--data-dir", str(ddir)]) == 0


def test_validate_all_catches_injected_break(tmp_path):
    src = ROOT / "matrix"
    dst = tmp_path / "matrix"
    dst.mkdir()
    for p in src.glob("*.csv"):
        shutil.copy(p, dst / p.name)
    # inject a current-state row whose uc_id is not in use-cases
    cs = dst / "current-state.csv"
    cs.write_text(cs.read_text() + "UC-ZZZ-999,GAP,MED,,,,,\n", encoding="utf-8")
    viol = vd.validate_all(str(tmp_path))
    assert any("UC-ZZZ-999" in v for v in viol)
    assert vd.main(["--root", str(tmp_path)]) == 1


def test_no_legacy_token_clean():
    cur = [{"uc_id": "UC-1", "current_state": "GAP"}]
    idc = [{"nhi_id": "NHI-1", "sources_likely": "x"}]
    assert vd.check_no_legacy_token(cur, idc) == []


def test_no_legacy_token_flags_old_headers():
    cur = [{"uc_id": "UC-1", "anz_state": "GAP"}]          # legacy column back
    idc = [{"nhi_id": "NHI-1", "sources_at_anz_likely": "x"}]
    errs = vd.check_no_legacy_token(cur, idc)
    assert any("anz_state" in e for e in errs)
    assert any("sources_at_anz_likely" in e for e in errs)


# ---- F3: control-ID verification registry gate ----
_REGISTRY = {
    "asd-ism": {"pattern": r"^ISM-\d{4}$", "controls": ["ISM-0027", "ISM-1139"]},
    "essential-8": {"controls": ["E8-MFA-ML1"]},
}


def test_control_id_registry_flags_unregistered_code():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-9999"}]
    errs = vd.check_control_id_registry(trace, _REGISTRY)
    assert any("ISM-9999" in e for e in errs)


def test_control_id_registry_passes_known_code():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    assert vd.check_control_id_registry(trace, _REGISTRY) == []


def test_control_id_registry_flags_unknown_framework():
    trace = [{"framework_slug": "nope", "control_code": "X-1"}]
    assert any("nope" in e for e in vd.check_control_id_registry(trace, _REGISTRY))


def test_control_id_registry_missing_registry_is_violation():
    assert vd.check_control_id_registry([{"framework_slug": "x", "control_code": "y"}], {})


# ---- F2: no uncited provider claims ----
def test_provider_claims_cited_flags_uncited():
    rows = [{"coverage": "NATIVE", "target_id": "UC-1", "vendor_slug": "v",
             "evidence_url": "", "citation_keys": "", "notes": ""}]
    assert any("uncited" in e.lower() for e in vd.check_provider_claims_cited("vc", rows))


def test_provider_claims_cited_accepts_url_citation_or_tag():
    base = {"coverage": "NATIVE", "target_id": "UC-1", "vendor_slug": "v",
            "evidence_url": "", "citation_keys": "", "notes": ""}
    assert vd.check_provider_claims_cited("vc", [{**base, "evidence_url": "http://x"}]) == []
    assert vd.check_provider_claims_cited("vc", [{**base, "citation_keys": "k-2024"}]) == []
    assert vd.check_provider_claims_cited("vc", [{**base, "notes": "[INDUSTRY-CONSENSUS] likely"}]) == []


def test_provider_claims_cited_ignores_non_provider_rows():
    rows = [{"coverage": "GAP", "target_id": "UC-1", "vendor_slug": "v",
             "evidence_url": "", "citation_keys": "", "notes": ""}]
    assert vd.check_provider_claims_cited("vc", rows) == []


# ---- F1/F4: data-provenance manifest ----
_PROV = {"asd-ism": {"as_of": "2026-05-24", "source_tier": "PRIMARY"},
         "vendor-capabilities": {"as_of": "2025", "source_tier": "PRIMARY"}}


def test_data_provenance_flags_missing_entry():
    trace = [{"framework_slug": "essential-8", "control_code": "E8-1"}]
    assert any("essential-8" in e for e in vd.check_data_provenance(trace, _PROV))


def test_data_provenance_flags_invalid_tier():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    prov = {"asd-ism": {"as_of": "2026", "source_tier": "BOGUS"},
            "vendor-capabilities": {"as_of": "2025", "source_tier": "PRIMARY"}}
    assert any("source_tier" in e for e in vd.check_data_provenance(trace, prov))


def test_data_provenance_clean():
    trace = [{"framework_slug": "asd-ism", "control_code": "ISM-0027"}]
    assert vd.check_data_provenance(trace, _PROV) == []

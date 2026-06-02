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

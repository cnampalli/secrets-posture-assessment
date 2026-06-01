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
    rows = [{"anz_state": "GAP"}, {"anz_state": "BOGUS"}, {"anz_state": ""}]
    errs = vd.check_enum("anz-current-state.csv", rows, "anz_state", vd.VALID_STATES)
    assert errs == ["anz-current-state.csv: invalid anz_state 'BOGUS'"]


def test_ids_drops_blanks_and_sentinels():
    assert vd._ids("UC-1;;MISSING-UC;UC-2") == ["UC-1", "UC-2"]

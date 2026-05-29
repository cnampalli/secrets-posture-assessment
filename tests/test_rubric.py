from pathlib import Path
import methodology.validate_rubric as vr

ROOT = Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"

def test_load_csv_reads_header_and_rows(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("a,b\n1,2\n", encoding="utf-8")
    rows = vr.load_csv(f)
    assert rows == [{"a": "1", "b": "2"}]

def test_no_anz_passes_clean_text(tmp_path):
    f = tmp_path / "clean.csv"
    f.write_text("uc_id,note\nUC-F-001,client-generic\n", encoding="utf-8")
    assert vr.check_no_anz([f]) == []

def test_no_anz_flags_anz_token(tmp_path):
    f = tmp_path / "dirty.csv"
    f.write_text("uc_id,note\nUC-F-001,a" + "nz_state here\n", encoding="utf-8")
    assert f.name in " ".join(vr.check_no_anz([f]))

REQUIRED_ARCH_COLS = {
    "archetype_id", "name", "intent", "met_def",
    "partial_def", "gap_def", "na_def", "evidence_expectation",
}
EXPECTED_IDS = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"}

def test_archetypes_have_all_ids_and_filled_cells():
    rows = vr.load_csv(METH / "assessment-archetypes.csv")
    ids = {r["archetype_id"] for r in rows}
    assert ids == EXPECTED_IDS
    errors = vr.validate_archetypes(rows)
    assert errors == [], errors

def test_archetypes_file_has_no_anz():
    assert vr.check_no_anz([METH / "assessment-archetypes.csv"]) == []

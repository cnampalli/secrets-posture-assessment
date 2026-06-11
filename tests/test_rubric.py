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

ALLOWED_BOUNDARY = {"GAP_PARTIAL", "PARTIAL_MET"}

def test_questions_valid_and_cover_each_non_a0_archetype():
    archs = vr.load_csv(METH / "assessment-archetypes.csv")
    qs = vr.load_csv(METH / "archetype-questions.csv")
    errors = vr.validate_questions(archs, qs)
    assert errors == [], errors

def test_questions_file_has_no_anz():
    assert vr.check_no_anz([METH / "archetype-questions.csv"]) == []

USE_CASES = ROOT / "matrix" / "domains" / "secrets" / "use-cases.csv"

def test_every_uc_is_mapped_with_valid_archetype_and_slots():
    ucs = vr.load_csv(USE_CASES)
    archs = vr.load_csv(METH / "assessment-archetypes.csv")
    qs = vr.load_csv(METH / "archetype-questions.csv")
    mapping = vr.load_csv(METH / "uc-archetype-map.csv")
    errors = vr.validate_mapping(ucs, archs, qs, mapping)
    assert errors == [], errors

def test_mapping_file_has_no_anz():
    assert vr.check_no_anz([METH / "uc-archetype-map.csv"]) == []

def test_every_a0_uc_has_bespoke_criteria_and_vice_versa():
    mapping = vr.load_csv(METH / "uc-archetype-map.csv")
    bespoke = vr.load_csv(METH / "bespoke-criteria.csv")
    errors = vr.validate_bespoke(mapping, bespoke)
    assert errors == [], errors

def test_bespoke_file_has_no_anz():
    assert vr.check_no_anz([METH / "bespoke-criteria.csv"]) == []

def test_run_all_returns_no_errors_on_real_data():
    errors = vr.run_all()
    assert errors == [], errors

def test_rescore_covers_all_ucs_and_no_anz():
    ucs = vr.load_csv(USE_CASES)
    rescore = vr.load_csv(METH / "posture-rescore.csv")
    rescored_ids = {r["uc_id"] for r in rescore}
    assert rescored_ids == {u["uc_id"] for u in ucs}
    for r in rescore:
        assert r["proposed_state"] in {"MET", "PARTIAL", "GAP", "N/A", "PENDING"}, r
    assert vr.check_no_anz([METH / "posture-rescore.csv"]) == []

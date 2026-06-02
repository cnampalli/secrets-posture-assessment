import csv, json, pathlib, subprocess, sys
import pytest
import questionnaire.report_adapter as ra

ROOT = pathlib.Path(__file__).resolve().parents[1]

SAMPLE = {
    "schema": "posture-assessment-record/v1",
    "generated": "2026-05-30T00:00:00Z",
    "responses": {
        "UC-F-003": {"archetype": "A2", "answers": {"A2-Q1": "yes", "A2-Q2": "no"},
                     "proposed_state": "PARTIAL", "final_state": "PARTIAL", "overridden": False,
                     "rationale": "82% migrated", "confidence": "HIGH"},
        "UC-F-001": {"archetype": "A1", "answers": {"A1-Q1": "no"},
                     "proposed_state": "GAP", "final_state": "GAP", "overridden": False,
                     "rationale": "push-protection off", "confidence": "MED"},
    },
}


def test_record_to_rows_maps_and_sorts():
    rows = ra.record_to_rows(SAMPLE)
    assert [r["uc_id"] for r in rows] == ["UC-F-001", "UC-F-003"]   # sorted
    r3 = {r["uc_id"]: r for r in rows}["UC-F-003"]
    assert r3["current_state"] == "PARTIAL"
    assert r3["confidence"] == "HIGH"
    assert r3["gap_notes"] == "82% migrated"
    assert "A2-Q1" in r3["evidence_q_ids"] and "A2-Q2" in r3["evidence_q_ids"]
    assert set(r3.keys()) == set(ra.COLUMNS)


def test_state_fallback_to_pending():
    rec = {"schema": "posture-assessment-record/v1", "responses": {
        "UC-X": {"archetype": "A0", "answers": {}, "proposed_state": None, "final_state": None,
                 "overridden": False, "rationale": "", "confidence": "MED"}}}
    assert ra.record_to_rows(rec)[0]["current_state"] == "PENDING"


def test_proposed_used_when_no_final():
    rec = {"schema": "posture-assessment-record/v1", "responses": {
        "UC-Y": {"archetype": "A1", "answers": {"A1-Q1": "yes"}, "proposed_state": "MET",
                 "final_state": None, "overridden": False, "rationale": "", "confidence": "LOW"}}}
    assert ra.record_to_rows(rec)[0]["current_state"] == "MET"


def test_wrong_schema_raises():
    with pytest.raises(ra.AdapterError):
        ra.record_to_rows({"schema": "nope", "responses": {}})


def test_missing_responses_yields_empty():
    assert ra.record_to_rows({"schema": "posture-assessment-record/v1"}) == []


def test_write_csv_roundtrip(tmp_path):
    out = tmp_path / "cs.csv"
    ra.write_csv(ra.record_to_rows(SAMPLE), out)
    with open(out, newline="", encoding="utf-8") as fh:
        got = list(csv.DictReader(fh))
    assert {r["uc_id"] for r in got} == {"UC-F-001", "UC-F-003"}
    assert list(got[0].keys()) == ra.COLUMNS


def test_cli_writes_csv(tmp_path):
    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps(SAMPLE), encoding="utf-8")
    out = tmp_path / "out.csv"
    r = subprocess.run([sys.executable, "-m", "questionnaire.report_adapter", str(rec), "-o", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    with open(out, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 2

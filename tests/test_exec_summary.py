import csv, json, pathlib
import pytest
import presentation.build_exec_summary as es

ROOT = pathlib.Path(__file__).resolve().parents[1]


def xyz_record():
    rows = list(csv.DictReader(open(ROOT / "matrix" / "anz-current-state.csv", encoding="utf-8")))
    return {"schema": "posture-assessment-record/v1", "responses": {
        r["uc_id"]: {"proposed_state": r["anz_state"], "final_state": r["anz_state"],
                     "rationale": r.get("gap_notes", "")} for r in rows}}


def test_snapshot_counts_xyz():
    assert es.snapshot_counts(xyz_record()) == {"MET": 0, "PARTIAL": 16, "GAP": 11, "PENDING": 20}


def test_inject_replaces_tokens():
    tmpl = "<style>/*__CSS__*/</style><script>window.__EXEC_DATA__ = /*__DATA__*/null;</script><script>/*__APP__*/</script>"
    out = es.inject(tmpl, "BODY{}", {"a": 1}, "console.log(1)")
    assert "BODY{}" in out
    assert '"a": 1' in out or '"a":1' in out
    assert "/*__DATA__*/null" not in out
    assert "console.log(1)" in out


def test_inject_missing_token_raises():
    with pytest.raises(es.ExecSummaryError):
        es.inject("<style>/*__CSS__*/</style>", "x", {}, "y")  # missing DATA + APP tokens

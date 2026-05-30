import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENGINE = ROOT / "matrix" / "build_matrix_viewer.py"

RECORD = {
    "schema": "posture-assessment-record/v1",
    "generated": "2026-05-30T00:00:00Z",
    "responses": {
        "UC-F-001": {"archetype": "A1", "answers": {"A1-Q1": "no"}, "proposed_state": "GAP",
                     "final_state": "GAP", "overridden": False, "rationale": "off", "confidence": "HIGH"},
        "UC-F-003": {"archetype": "A2", "answers": {"A2-Q1": "yes", "A2-Q2": "yes"},
                     "proposed_state": "MET", "final_state": "MET", "overridden": False,
                     "rationale": "", "confidence": "HIGH"},
    },
}


def test_questionnaire_record_drives_report(tmp_path):
    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps(RECORD), encoding="utf-8")
    cs = tmp_path / "cs.csv"
    subprocess.run([sys.executable, "-m", "questionnaire.report_adapter", str(rec), "-o", str(cs)],
                   cwd=ROOT, check=True)
    data = tmp_path / "data.json"
    subprocess.run([sys.executable, str(ENGINE), "--current-state", str(cs),
                    "--emit-data", str(data)], cwd=ROOT, check=True)
    ucs = json.load(open(data))["REGDATA"]["ucs"]
    # the report's UC states now reflect the assessment record
    assert ucs["UC-F-001"]["state"] == "GAP"
    assert ucs["UC-F-003"]["state"] == "MET"

"""The React app's exported record must build the exec summary (schema parity)."""
import json, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def fake_export():
    """Mirror app buildRecord() output shape for a couple of responses."""
    return {"schema": "posture-assessment-record/v1", "generated": "2026-01-01T00:00:00Z",
            "responses": {
                "UC-F-001": {"archetype": "A1", "answers": {"A1-Q1": "no"},
                             "proposed_state": "GAP", "final_state": "GAP",
                             "overridden": False, "rationale": "", "confidence": "MED"},
                "UC-F-002": {"archetype": "A2", "answers": {},
                             "proposed_state": "PENDING", "final_state": "PENDING",
                             "overridden": False, "rationale": "", "confidence": "MED"}}}

def test_export_builds_exec_summary(tmp_path):
    rec = tmp_path / "rec.json"; rec.write_text(json.dumps(fake_export()), encoding="utf-8")
    out = tmp_path / "exec.html"
    r = subprocess.run([sys.executable, "-m", "presentation.build_exec_summary",
                        str(rec), "-o", str(out)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    html = out.read_text(encoding="utf-8")
    assert "@media print" in html and "posture-assessment-record/v1" not in html  # schema key not echoed raw
    assert out.stat().st_size > 10_000

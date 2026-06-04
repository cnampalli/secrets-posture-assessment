import csv, json, pathlib
import pytest
import presentation.build_exec_summary as es

ROOT = pathlib.Path(__file__).resolve().parents[1]


def xyz_record():
    rows = list(csv.DictReader(open(ROOT / "matrix" / "current-state.csv", encoding="utf-8")))
    return {"schema": "posture-assessment-record/v1", "responses": {
        r["uc_id"]: {"proposed_state": r["current_state"], "final_state": r["current_state"],
                     "rationale": r.get("gap_notes", "")} for r in rows}}


def test_snapshot_counts_xyz():
    assert es.snapshot_counts(xyz_record()) == {"MET": 0, "PARTIAL": 16, "GAP": 11, "PENDING": 20}


def test_inject_replaces_tokens():
    tmpl = ("<style>/*__FONTS__*/\n/*__TOKENS__*/\n/*__CSS__*/</style>"
            "<script>window.__EXEC_DATA__ = /*__DATA__*/null;</script><script>/*__APP__*/</script>")
    out = es.inject(tmpl, "BODY{}", {"a": 1}, "console.log(1)",
                    fonts="@font-face{}", tokens=":root{--accent:#9a7b32}")
    assert "BODY{}" in out
    assert "@font-face{}" in out
    assert "--accent:#9a7b32" in out
    assert "/*__FONTS__*/" not in out and "/*__TOKENS__*/" not in out
    assert '"a": 1' in out or '"a":1' in out
    assert "/*__DATA__*/null" not in out
    assert "console.log(1)" in out


def test_inject_missing_token_raises():
    with pytest.raises(es.ExecSummaryError):
        es.inject("<style>/*__CSS__*/</style>", "x", {}, "y")  # missing DATA + APP tokens


import re


def test_build_self_contained_and_complete(tmp_path):
    rec = tmp_path / "rec.json"
    rec.write_text(json.dumps(xyz_record()), encoding="utf-8")
    out = tmp_path / "exec.html"
    es.build(str(rec), out_path=str(out))
    html = out.read_text(encoding="utf-8")
    assert '"GAP": 11' in html and '"PARTIAL": 16' in html
    menu_ids = [it["uc_id"] for it in json.loads(
        re.search(r"window\.__EXEC_DATA__\s*=\s*(\{.*?\});", html, re.S).group(1))["menu"]["items"]]
    assert len(menu_ids) == 27
    assert "@media print" in html
    # Fully offline: brand fonts are embedded as base64 woff2, so the output has
    # NO external URLs at all (no Google Fonts link, no CDN) — firewall-proof.
    externals = re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html)
    assert externals == [], externals
    assert "@font-face" in html and "data:font/woff2;base64," in html


def test_build_is_byte_stable(tmp_path):
    rec = tmp_path / "r.json"; rec.write_text(json.dumps(xyz_record()), encoding="utf-8")
    a = tmp_path / "a.html"; b = tmp_path / "b.html"
    es.build(str(rec), out_path=str(a)); es.build(str(rec), out_path=str(b))
    assert a.read_bytes() == b.read_bytes()

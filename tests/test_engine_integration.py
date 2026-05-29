import json, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ROOT / "matrix" / "build_matrix_viewer.py"
BASELINE = json.load(open(ROOT / "tests" / "fixtures" / "data-baseline.json"))


def _run(tmp_path, *args):
    out = tmp_path / "data.json"
    subprocess.run([sys.executable, str(ENGINE), "--emit-data", str(out), *args],
                   cwd=ROOT, check=True)
    return json.load(open(out))


def test_default_run_matches_frozen_baseline(tmp_path):
    new = _run(tmp_path)
    assert [f["slug"] for f in new["REGDATA"]["frameworks"]] == \
           [f["slug"] for f in BASELINE["REGDATA"]["frameworks"]]
    assert new["RECDATA"] == BASELINE["RECDATA"]


def test_financial_preset_scopes_frameworks(tmp_path):
    new = _run(tmp_path, "--preset", "financial")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert slugs == {"apra-cps-234", "apra-cps-230", "apra-cpg-234",
                     "essential-8", "cisa-ztmm-v2"}
    assert "asd-ism" not in slugs and "mitre-attack" not in slugs


def test_government_preset_scopes_to_ism_and_e8(tmp_path):
    new = _run(tmp_path, "--preset", "government")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert slugs == {"asd-ism", "essential-8", "cisa-ztmm-v2"}


def test_framework_selection_metadata_present(tmp_path):
    new = _run(tmp_path, "--preset", "financial")
    sel = new["REGDATA"]["framework_selection"]
    assert sel["baseline"] == ["essential-8"]
    assert set(sel["available"]) >= {"asd-ism", "mitre-attack"}   # full menu retained


def test_cli_frameworks_override(tmp_path):
    new = _run(tmp_path, "--frameworks", "asd-ism")
    slugs = {f["slug"] for f in new["REGDATA"]["frameworks"]}
    assert "asd-ism" in slugs and "apra-cps-234" not in slugs


def test_residency_weight_off_changes_vendor_order(tmp_path):
    cfg = tmp_path / "off.yaml"
    cfg.write_text("primary: [apra-cps-234]\nbaseline: [essential-8]\n"
                   "residency: {weight: off, irap_required: false}\n")
    new = _run(tmp_path, "--config", str(cfg))
    base_primary = BASELINE["RECDATA"]["top_picks"][0]["slug"]
    new_primary = new["RECDATA"]["top_picks"][0]["slug"]
    assert new["RECDATA"]["top_picks"] != BASELINE["RECDATA"]["top_picks"] \
        or new_primary != base_primary

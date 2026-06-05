import pathlib
import questionnaire.build_questionnaire as bq

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_build_writes_self_contained_html(tmp_path):
    out = tmp_path / "questionnaire.html"
    bq.build(out_path=out)
    html = out.read_text(encoding="utf-8")
    assert html.count("UC-F-001") >= 1
    assert "UC-F-017" in html and "UC-N-002" in html
    assert "function deriveState" in html
    assert "const App" in html
    assert "<script src" not in html and "<link " not in html
    assert "http://" not in html and "https://" not in html
    assert "/*__RUBRIC__*/[]" not in html
    assert "/*__SCORING__*/" not in html and "/*__APP__*/" not in html


def test_build_default_output_path():
    out = bq.build()
    p = pathlib.Path(out)
    assert p.exists() and p.name == "questionnaire.html"


def test_build_pam_domain_bakes_evidence(tmp_path):
    out = tmp_path / "pam.html"
    bq.build(out_path=out, data_dir=ROOT / "matrix" / "domains" / "pam")
    html = out.read_text(encoding="utf-8")
    assert html.count("UC-P-001") >= 1
    assert "UC-F-001" not in html                      # SECRETS rubric not used
    assert "EV-PAM-VAULT-ROTATION-POLICY" in html      # evidence baked into the rubric JSON
    assert "register of in-scope privileged accounts" in html  # a requirement string
    assert "/*__RUBRIC__*/[]" not in html

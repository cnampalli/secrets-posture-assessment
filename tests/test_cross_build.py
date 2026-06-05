import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import build_cross_domain


def test_build_produces_report_with_spanning_cyberark():
    model, dst = build_cross_domain.build()
    parents = {p["parent"]: p for p in model["parents"]}
    # cyberark owns brands in BOTH the secrets and pam domains → spans 2
    assert "cyberark" in parents and parents["cyberark"]["spans"] == 2
    html = pathlib.Path(dst).read_text(encoding="utf-8")
    assert "Cross-Domain Vendor Map" in html
    assert "CyberArk PAM" in html            # a brand chip rendered
    assert "Concentration (risk reading)" in html
    assert "/*__CROSSMAP__*/" not in html    # token fully substituted

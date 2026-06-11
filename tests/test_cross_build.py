import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import build_cross_domain


def test_build_produces_report_with_spanning_palo_alto_networks():
    model, dst = build_cross_domain.build()
    parents = {p["parent"]: p for p in model["parents"]}
    # the PANW/CyberArk cluster owns brands in BOTH the secrets and pam domains → spans 2
    assert "palo-alto-networks" in parents and parents["palo-alto-networks"]["spans"] == 2
    assert "cyberark" not in parents             # cyberark is no longer an ultimate parent
    # Entro Security is independent — it must NOT sit under any acquisition parent.
    for p in model["parents"]:
        if p["parent"] != "entro-security":
            for dom in p.get("by_domain", {}).values():
                assert all(b["slug"] != "entro-security" for b in dom["brands"])
    html = pathlib.Path(dst).read_text(encoding="utf-8")
    assert "Cross-Domain Vendor Map" in html
    assert "CyberArk PAM" in html            # a brand chip rendered
    assert "Concentration (risk reading)" in html
    assert "/*__CROSSMAP__*/" not in html    # token fully substituted

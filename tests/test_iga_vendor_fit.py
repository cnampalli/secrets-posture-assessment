"""Phase 3: the bespoke per-AREA IGA vendor-fit view.

IGA is process-shaped — the NATIVE/ADD-ON per-use-case capability matrix used by
secrets/PAM does NOT fit it. Instead IGA ships a small per-AREA vendor-fit grid:
vendors × the 4 governance areas {JML, Certification, SoD, Role/Request} →
fit ∈ {NATIVE, PARTIAL, ADD-ON}, each with a one-line justification + citation.

These tests pin:
  1. build_iga_vendor_fit() returns the ordered 4×4 grid with the honest
     PARTIAL verdicts (Entra/Okta SoD = PARTIAL; SailPoint/Saviynt all NATIVE).
  2. the rendered IGA report contains the per-area view and NOT the
     NATIVE/ADD-ON capability matrix; secrets/PAM keep the matrix.
"""
import os

import report_logic
import report_render
import domains

IGA_DATA_DIR = domains.IGA.data_dir
AREAS = ["JML", "Certification", "SoD", "Role/Request"]


def test_build_iga_vendor_fit_returns_4x4_grid_ordered():
    grid = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    assert grid["areas"] == AREAS
    # four vendors, in CSV (data) order
    assert [v["vendor"] for v in grid["vendors"]] == [
        "SailPoint Identity Security Cloud",
        "Saviynt Enterprise Identity Cloud",
        "Microsoft Entra ID Governance",
        "Okta Identity Governance",
    ]
    # every vendor has a cell for every area
    for v in grid["vendors"]:
        assert list(v["cells"].keys()) == AREAS


def test_iga_partial_and_native_verdicts_are_honest():
    grid = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    by_name = {v["vendor"]: v for v in grid["vendors"]}

    # SailPoint + Saviynt are NATIVE on all four areas
    for name in ("SailPoint Identity Security Cloud", "Saviynt Enterprise Identity Cloud"):
        for area in AREAS:
            assert by_name[name]["cells"][area]["fit"] == "NATIVE", (name, area)

    # Entra + Okta are PARTIAL on SoD (the honest, non-marketing verdict)
    assert by_name["Microsoft Entra ID Governance"]["cells"]["SoD"]["fit"] == "PARTIAL"
    assert by_name["Okta Identity Governance"]["cells"]["SoD"]["fit"] == "PARTIAL"

    # ...but NATIVE on the other three areas
    for name in ("Microsoft Entra ID Governance", "Okta Identity Governance"):
        for area in ("JML", "Certification", "Role/Request"):
            assert by_name[name]["cells"][area]["fit"] == "NATIVE", (name, area)


def test_iga_cells_carry_justification_and_citation():
    grid = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    by_name = {v["vendor"]: v for v in grid["vendors"]}
    # the honest Entra SoD caveat is carried through verbatim-ish
    entra_sod = by_name["Microsoft Entra ID Governance"]["cells"]["SoD"]
    assert "access-package incompatibility" in entra_sod["justification"]
    assert entra_sod["evidence_url"].startswith("https://")
    assert entra_sod["citation_keys"]
    # Saviynt marketing-grade caveat stays visible
    sav_jml = by_name["Saviynt Enterprise Identity Cloud"]["cells"]["JML"]
    assert "marketing-grade" in sav_jml["justification"]


def _render_iga():
    model = report_render and None  # placeholder; built below
    igavfit = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    dm = domains.IGA.report_meta()
    dc = domains.IGA.report_content()
    return report_render.render({
        "ranked": [], "anz": [], "ucs": [], "nhis": [],
        "glossary": {}, "layer_label": dict(domains.IGA.layer_label), "short": dict(domains.IGA.short),
        "reg": {}, "regdata": {}, "recdata": {},
        "vendormix": {}, "compliance": {}, "vendorintel": {}, "igavfit": igavfit,
        "meta": {"ranked_vendors": 4, "nhis": 0, "ucs": 0},
        "domain_meta": dm, "domain_content": dc,
    })


def test_rendered_iga_report_has_per_area_view_and_no_capability_matrix():
    html = _render_iga()
    # the per-area vendor-fit view is present (its heading + the area columns)
    assert "Vendor fit by governance area" in html
    assert "Role/Request" in html
    assert "PARTIAL" in html
    # the NATIVE/ADD-ON capability-matrix builder is gated OFF for IGA
    assert "function vendorMixHtml()" not in html
    assert "Resilience-first vendor mix" not in html
    # no region markers leak
    assert "__IGA_VENDOR_FIT_START__" not in html
    assert "__VENDORMIX_REGION_START__" not in html


def test_rendered_secrets_report_keeps_capability_matrix_and_no_iga_view():
    # secrets/PAM (igavfit absent) keep the matrix; the IGA view is removed.
    dm = domains.SECRETS.report_meta()
    dc = domains.SECRETS.report_content()
    html = report_render.render({
        "ranked": [], "anz": [], "ucs": [], "nhis": [],
        "glossary": {}, "layer_label": {}, "short": {},
        "reg": {}, "regdata": {}, "recdata": {},
        "vendormix": {}, "compliance": {}, "vendorintel": {},
        "meta": {"ranked_vendors": 0, "nhis": 0, "ucs": 0},
        "domain_meta": dm, "domain_content": dc,
    })
    assert "function vendorMixHtml()" in html      # matrix kept for secrets
    assert "Vendor fit by governance area" not in html
    assert "__IGA_VENDOR_FIT_START__" not in html

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

import pytest

import report_logic
import report_render
import domains

IGA_DATA_DIR = domains.IGA.data_dir
AREAS = ["JML", "Certification", "SoD", "Role/Request"]

_FIT_HEADER = "vendor,vendor_slug,area,fit,justification,evidence_url,citation_keys\n"


def test_real_iga_vendor_fit_data_does_not_raise():
    # The shipped iga-vendor-fit.csv (areas JML/Certification/SoD/Role/Request)
    # must still build cleanly under the area guard.
    grid = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    assert grid["areas"] == AREAS


def test_unrecognized_area_raises_loudly(tmp_path):
    # A mistyped/unknown non-blank area must fail at build time rather than being
    # silently dropped (which would render a blank cell and hide the typo).
    (tmp_path / "iga-vendor-fit.csv").write_text(
        _FIT_HEADER
        + 'Acme IGA,acme,Certifcation,NATIVE,typo in area,https://example.com,acme-cert\n',
        encoding="utf-8")
    with pytest.raises(ValueError):
        report_logic.build_iga_vendor_fit(str(tmp_path))


def test_blank_area_is_tolerated(tmp_path):
    # A blank area is not a typo signal — it must NOT raise (the row is simply
    # not a recognized governance-area cell).
    (tmp_path / "iga-vendor-fit.csv").write_text(
        _FIT_HEADER
        + 'Acme IGA,acme,,NATIVE,no area,https://example.com,acme\n'
        + 'Acme IGA,acme,JML,NATIVE,real cell,https://example.com,acme-jml\n',
        encoding="utf-8")
    grid = report_logic.build_iga_vendor_fit(str(tmp_path))
    assert grid["vendors"][0]["cells"]["JML"]["fit"] == "NATIVE"


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


def test_csv_vendor_slugs_subset_of_descriptor_vendor_layer():
    """Drift guard: every vendor_slug in iga-vendor-fit.csv must exist as a key in
    the IGA descriptor's vendor_layer map. The two vocabularies diverged once
    (product-accurate CSV slugs vs short YAML keys); this fails the moment a
    second consumer joins the CSV slug to the descriptor and they drift again."""
    grid = report_logic.build_iga_vendor_fit(IGA_DATA_DIR)
    csv_slugs = {v["vendor_slug"] for v in grid["vendors"]}
    layer_keys = set(domains.DOMAINS["iga"].vendor_layer.keys())
    assert csv_slugs <= layer_keys, (
        f"CSV vendor_slugs not in descriptor vendor_layer: {sorted(csv_slugs - layer_keys)}")


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

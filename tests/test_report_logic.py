import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import report_logic as rl


def test_build_glossary_truncates_long_description():
    long = "x" * 200
    nhis = [{"nhi_id": "NHI-1", "short_name": "Svc", "description": long}]
    g = rl.build_glossary(nhis, [])
    assert g["NHI-1"].startswith("Svc — ")
    assert g["NHI-1"].endswith("...")
    assert len(g["NHI-1"]) < len("Svc — ") + 200


def test_build_glossary_short_desc_and_legend_keys():
    nhis = [{"nhi_id": "NHI-2", "short_name": "Bot", "description": "short"}]
    ucs = [{"uc_id": "UC-F-001", "short_title": "Prevent secrets"}]
    g = rl.build_glossary(nhis, ucs)
    assert g["NHI-2"] == "Bot — short"
    assert g["UC-F-001"] == "Prevent secrets"          # UC titles included
    assert g["NATIVE"].startswith("Vendor's first-class")  # legend present
    assert "0" in g and "4" in g                        # maturity legend present


def test_build_glossary_empty_description_uses_short_name_only():
    g = rl.build_glossary([{"nhi_id": "NHI-3", "short_name": "Svc", "description": ""}], [])
    assert g["NHI-3"] == "Svc"


def test_compute_meta_counts():
    m = rl.compute_meta(all_rows=[{"vendor_slug": "a"}, {"vendor_slug": "a"}],
                        ranked=[{"vendor_slug": "a"}], nhis=[{}, {}], ucs=[{}])
    assert m["nhis"] == 2
    assert m["ucs"] == 1
    assert m["total_rows"] == 2
    assert m["ranked_rows"] == 1
    assert m["ranked_vendors"] == 1

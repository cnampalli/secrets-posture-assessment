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


_VM_OWN = {"vA": {"parent": "P"}, "vB": {"parent": "P"}}
_VM_RANKED = [
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-1", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-2", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-3", "coverage": "NATIVE", "maturity": "3"},
    {"vendor_slug": "vB", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    {"vendor_slug": "vC", "target_type": "UC-F", "target_id": "UC-4", "coverage": "NATIVE", "maturity": "2"},
    {"vendor_slug": "vA", "target_type": "UC-F", "target_id": "UC-5", "coverage": "ADD-ON", "maturity": "1"},
]
_VM_SHORT = {"vA": "Vendor A", "vB": "Vendor B", "vC": "Vendor C"}


def test_build_vendormix_reports_cover_and_whitespace():
    vm = rl.build_vendormix(_VM_RANKED, _VM_OWN, anchors=["vA"], short=_VM_SHORT)
    assert vm["cover"]["white_space"] == ["UC-5"]
    assert vm["cover"]["covered_count"] == 4
    assert vm["cover"]["uc_total"] == 5
    # chosen carries display names alongside slugs
    assert vm["cover"]["chosen"][0]["name"] == "Vendor A"


def test_build_vendormix_includes_concentration_and_complementary():
    vm = rl.build_vendormix(_VM_RANKED, _VM_OWN, anchors=["vA"], short=_VM_SHORT)
    # concentration scorecard sorted by share desc; P (vA) is the top parent.
    assert vm["concentration"][0]["parent"] == "P"
    # data-driven complementary: have Vendor A -> add a UC-4 provider.
    rec = vm["complementary"][0]
    assert rec["have"] == "Vendor A"
    assert rec["add"] in ("Vendor B", "Vendor C")


def test_compute_meta_counts():
    m = rl.compute_meta(all_rows=[{"vendor_slug": "a"}, {"vendor_slug": "a"}],
                        ranked=[{"vendor_slug": "a"}], nhis=[{}, {}], ucs=[{}])
    assert m["nhis"] == 2
    assert m["ucs"] == 1
    assert m["total_rows"] == 2
    assert m["ranked_rows"] == 1
    assert m["ranked_vendors"] == 1

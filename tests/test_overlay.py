import json, pathlib
import overlay

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = ROOT / "matrix" / "config"
FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def test_load_framework_labels_matches_snapshot():
    snap = json.load(open(FIX / "framework-labels.snapshot.json"))
    labels = overlay.load_framework_labels(CFG / "frameworks.yaml")
    assert set(labels) == set(snap)
    for slug, (lab, sub) in labels.items():
        assert [lab, sub] == snap[slug]            # tuple shape preserved


def test_load_vendor_residency_matches_snapshot():
    snap = json.load(open(FIX / "vendor-residency.snapshot.json"))
    assert overlay.load_vendor_residency(CFG / "vendor-residency.yaml") == snap


def test_vendor_sort_key_high_is_residency_first():
    # capability_keys are pre-negated (lower = better), as the engine builds them
    k = overlay.vendor_sort_key("high", "SAAS-ONLY", (-5, -2))
    assert k == (2, -5, -2)                         # res rank leads


def test_vendor_sort_key_off_drops_residency():
    assert overlay.vendor_sort_key("off", "SAAS-ONLY", (-5, -2)) == (-5, -2)


def test_vendor_sort_key_low_is_final_tiebreaker():
    assert overlay.vendor_sort_key("low", "CONDITIONAL", (-5, -2)) == (-5, -2, 1)


def test_vendor_sort_key_medium_after_primary_metric():
    assert overlay.vendor_sort_key("medium", "CONDITIONAL", (-5, -2)) == (-5, 1, -2)


def test_select_primary_gate_on_prefers_irap_au():
    vendors = [
        {"slug": "v-cap", "residency": "AU-RESIDENT", "irap": "NO"},
        {"slug": "v-irap", "residency": "AU-RESIDENT", "irap": "YES"},
    ]
    assert overlay.select_primary(vendors, irap_required=True)["slug"] == "v-irap"


def test_select_primary_gate_off_takes_capability_leader():
    vendors = [
        {"slug": "v-cap", "residency": "SAAS-ONLY", "irap": "NO"},
        {"slug": "v-irap", "residency": "AU-RESIDENT", "irap": "YES"},
    ]
    # list is already capability-sorted; gate off -> first wins
    assert overlay.select_primary(vendors, irap_required=False)["slug"] == "v-cap"

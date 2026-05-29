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

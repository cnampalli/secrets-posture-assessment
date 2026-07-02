import json
import os

import pytest

import sys
HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import benchmark  # noqa: E402

CFGDIR = os.path.join(MATRIX, "config")


def test_load_cohort_returns_label_and_domains():
    c = benchmark.load_cohort(CFGDIR)
    assert "illustrative synthetic" in c["cohort_label"].lower()
    assert set(c["domains"]) >= {"secrets", "pam", "iga"}


def test_load_cohort_label_override():
    c = benchmark.load_cohort(CFGDIR, cohort_label_override="Global banks (illustrative)")
    assert c["cohort_label"] == "Global banks (illustrative)"


def test_load_cohort_raises_when_band_missing_rationale(tmp_path):
    bad = {"cohort_label": "x", "basis": "y", "unit": "met_pct_integer_0_100",
           "domains": {"secrets": {"p25": 1, "p50": 2, "p75": 3}}}  # no rationale
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "benchmark-cohort.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="rationale"):
        benchmark.load_cohort(str(cfg))


def test_position_bottom_quartile():
    cohort = benchmark.load_cohort(CFGDIR)
    p = benchmark.position(0.10, "secrets", cohort)   # 10% < p25(25)
    assert p["percentile_band"] == "below p25 (bottom quartile)"
    assert "illustrative synthetic" in p["cohort_label"].lower()


def test_position_band_boundaries_secrets():
    cohort = benchmark.load_cohort(CFGDIR)
    # secrets p25=25 p50=45 p75=65 -> boundaries are inclusive lower edges
    assert benchmark.position(0.25, "secrets", cohort)["percentile_band"] == "p25–p50 (below median)"
    assert benchmark.position(0.45, "secrets", cohort)["percentile_band"] == "p50–p75 (above median)"
    assert benchmark.position(0.65, "secrets", cohort)["percentile_band"] == "above p75 (top quartile)"


def test_position_unknown_domain_no_baseline():
    cohort = benchmark.load_cohort(CFGDIR)
    p = benchmark.position(0.50, "nonexistent", cohort)
    assert p["percentile_band"] == "no cohort baseline"


# --- A6 honesty contract: cohort_type synthetic|measured, measured is earned ---

def _cohort_with(band_extra, tmp_path):
    band = {"p25": 1, "p50": 2, "p75": 3, "rationale": "r"}
    band.update(band_extra)
    bad = {"cohort_label": "x", "basis": "y", "unit": "met_pct_integer_0_100",
           "domains": {"secrets": band}}
    cfg = tmp_path / "config"
    cfg.mkdir()
    (cfg / "benchmark-cohort.json").write_text(json.dumps(bad), encoding="utf-8")
    return str(cfg)


def test_load_cohort_requires_explicit_cohort_type(tmp_path):
    with pytest.raises(ValueError, match="cohort_type"):
        benchmark.load_cohort(_cohort_with({}, tmp_path))


def test_load_cohort_rejects_off_vocab_cohort_type(tmp_path):
    with pytest.raises(ValueError, match="cohort_type"):
        benchmark.load_cohort(_cohort_with({"cohort_type": "estimated"}, tmp_path))


def test_load_cohort_measured_requires_min_n(tmp_path):
    with pytest.raises(ValueError, match="measured requires n >="):
        benchmark.load_cohort(_cohort_with({"cohort_type": "measured", "n": 3}, tmp_path))


def test_load_cohort_measured_ok_at_min_n(tmp_path):
    c = benchmark.load_cohort(_cohort_with({"cohort_type": "measured", "n": 5}, tmp_path))
    assert c["domains"]["secrets"]["cohort_type"] == "measured"


def test_position_surfaces_cohort_type_and_n():
    c = benchmark.load_cohort(CFGDIR)
    pos = benchmark.position(0.5, "secrets", c)
    assert pos["cohort_type"] == "synthetic" and pos["n"] == 0


def test_real_cohort_is_synthetic_labelled():
    # the shipped baseline must stay honestly synthetic until real engagements land
    c = benchmark.load_cohort(CFGDIR)
    for dom, band in c["domains"].items():
        assert band["cohort_type"] == "synthetic", dom

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

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import rollup  # noqa: E402


def _domain_input(slug, label, met_pct, band, risks):
    return {
        "slug": slug, "label": label,
        "posture": {"overall_band": band, "met_pct": met_pct,
                    "counts": {"met": 1, "partial": 1, "gap": 1, "pending": 0},
                    "p0_open": 1, "groups": [], "basis": "designed convention"},
        "top_3_risks": risks,
        "benchmark": {"percentile_band": "p25–p50 (below median)",
                      "cohort_label": "AU FIs (illustrative synthetic baseline)",
                      "basis_note": "synthetic"},
    }


def test_build_rollup_has_one_entry_per_domain():
    domains = [
        _domain_input("secrets", "Secrets", 0.45, "ML2", [{"uc_id": "UC-S-001", "short_title": "Rotation"}]),
        _domain_input("pam", "PAM", 0.50, "ML2", []),
    ]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    assert len(model["domains"]) == 2
    assert {d["slug"] for d in model["domains"]} == {"secrets", "pam"}


def test_trend_is_baseline_with_no_arrow():
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    trend = model["domains"][0]["trend"]
    assert trend["state"] == "baseline"
    assert "first assessment" in trend["note"].lower()
    # no directional glyph anywhere in the trend payload
    assert not any(g in repr(trend) for g in ("↑", "↓", "→", "▲", "▼"))


def test_overall_band_is_worst_across_domains():
    domains = [
        _domain_input("secrets", "Secrets", 0.80, "ML3", []),
        _domain_input("iga", "IGA", 0.20, "ML1", []),
    ]
    model = rollup.build_exec_rollup(domains, crossmap={"parents": [], "domains": []})
    assert model["overall"]["lowest_band"] == "ML1"


def test_crossmap_headline_names_top_spanning_parent():
    cm = {"domains": [{"slug": "secrets"}, {"slug": "pam"}],
          "parents": [{"parent": "cyberark", "display": "CyberArk", "spans": 2}]}
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap=cm)
    assert "CyberArk" in model["overall"]["concentration_headline"]


def test_crossmap_headline_when_no_span():
    cm = {"domains": [{"slug": "secrets"}], "parents": [{"parent": "x", "display": "X", "spans": 1}]}
    domains = [_domain_input("secrets", "Secrets", 0.45, "ML2", [])]
    model = rollup.build_exec_rollup(domains, crossmap=cm)
    assert "no" in model["overall"]["concentration_headline"].lower()

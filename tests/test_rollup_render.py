import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import rollup_render  # noqa: E402

MODEL = {
    "domains": [
        {"slug": "secrets", "label": "Secrets", "overall_band": "ML2", "met_pct": 0.45,
         "counts": {"met": 1, "partial": 1, "gap": 1, "pending": 0}, "p0_open": 1,
         "top_3_risks": [{"uc_id": "UC-S-001", "short_title": "Rotation"}],
         "benchmark": {"percentile_band": "p25–p50 (below median)",
                       "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
                       "basis_note": "Synthetic, designed-honest reference bands."},
         "trend": {"state": "baseline", "note": "First assessment — trend activates at the next dated re-baseline."}},
        {"slug": "pam", "label": "PAM", "overall_band": "ML2", "met_pct": 0.50,
         "counts": {"met": 2, "partial": 0, "gap": 0, "pending": 0}, "p0_open": 0,
         "top_3_risks": [],
         "benchmark": {"percentile_band": "p50–p75 (above median)",
                       "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
                       "basis_note": "Synthetic, designed-honest reference bands."},
         "trend": {"state": "baseline", "note": "First assessment — trend activates at the next dated re-baseline."}},
    ],
    "overall": {"lowest_band": "ML2", "total_p0_open": 1,
                "concentration_headline": "CyberArk spans 2 assessed domains — a cross-domain concentration signal (CPS 230)."},
}


def test_render_is_self_contained_html():
    html = rollup_render.render(MODEL)
    assert html.lstrip().startswith("<!doctype html>")
    assert "/*__ROLLUP__*/" not in html  # token was substituted
    assert "src=\"http" not in html and "href=\"http" not in html  # no external refs


def test_render_includes_synthetic_cohort_label():
    html = rollup_render.render(MODEL)
    assert "illustrative synthetic baseline" in html.lower()


def test_render_has_no_directional_trend_glyph():
    html = rollup_render.render(MODEL)
    assert not any(g in html for g in ("↑", "↓", "▲", "▼"))


def test_render_embeds_all_domains():
    html = rollup_render.render(MODEL)
    assert "Secrets" in html and "PAM" in html

"""Marketing collateral counts are machine-derived from live data — never stale.

(a) instrument_stats values equal independent recounts of the CSVs;
(b) built collateral HTML carries the live counts and zero __STAT_ tokens;
(c) build_collateral fails (nonzero exit / raises) on templates with unknown tokens.
"""
import csv
import json
import pathlib
import shutil
import subprocess
import sys

import pytest

import presentation.build_collateral as bc
import presentation.instrument_stats as istats

ROOT = pathlib.Path(__file__).resolve().parents[1]
PRES = ROOT / "presentation"
DOMAINS = ("secrets", "pam", "iga")


def _count(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.DictReader(fh))


@pytest.fixture(scope="module")
def stats():
    return istats.compute_stats()


# ---------- (a) stats equal independent recounts ----------

def test_uc_counts_match_csvs(stats):
    total = 0
    for d in DOMAINS:
        n = _count(ROOT / "matrix" / "domains" / d / "use-cases.csv")
        assert stats[f"uc_{d}"] == n
        total += n
    assert stats["uc_total"] == total


def test_identity_counts_match_csvs(stats):
    total = 0
    for d in DOMAINS:
        n = _count(ROOT / "matrix" / "domains" / d / "identity-catalog.csv")
        assert stats[f"identity_{d}"] == n
        total += n
    assert stats["identity_total"] == total


def test_vendor_counts_match_data(stats):
    for d in ("secrets", "pam"):
        files = list((ROOT / "matrix" / "domains" / d).glob("vendor-capabilities-*.csv"))
        assert stats[f"vendors_{d}"] == len(files)
    rows = list(csv.DictReader(open(
        ROOT / "matrix" / "domains" / "iga" / "iga-vendor-fit.csv", encoding="utf-8")))
    assert stats["vendors_iga"] == len({r["vendor_slug"] for r in rows})
    assert stats["vendors_total"] == sum(stats[f"vendors_{d}"] for d in DOMAINS)


def test_archetype_counts_match_csv(stats):
    rows = list(csv.DictReader(open(
        ROOT / "methodology" / "assessment-archetypes.csv", encoding="utf-8")))
    ids = [r["archetype_id"] for r in rows]
    assert stats["archetypes"] == len(ids)
    assert stats["archetype_range"] == f"{min(ids)}–{max(ids)}"


def test_trace_quote_and_framework_counts_match_csvs(stats):
    rows_total = verbatim = elided = 0
    control = set()
    for d in DOMAINS:
        rows = list(csv.DictReader(open(
            ROOT / "matrix" / "domains" / d / "regulatory-trace.csv", encoding="utf-8")))
        assert stats[f"trace_rows_{d}"] == len(rows)
        rows_total += len(rows)
        verbatim += sum(1 for r in rows if r["quote_type"] == "verbatim")
        elided += sum(1 for r in rows if r["quote_type"] == "verbatim-elided")
        control |= {r["framework_slug"] for r in rows
                    if r["framework_role"] in ("PRIMARY-LENS", "BACK-MAP")}
    assert stats["trace_rows_total"] == rows_total
    assert stats["quotes_verbatim"] == verbatim
    assert stats["quotes_verbatim_elided"] == elided
    assert stats["quotes_total"] == verbatim + elided
    assert stats["frameworks_control_level"] == len(control)
    assert stats["frameworks_control_level_slugs"] == sorted(control)


def test_control_level_slugs_exist_in_frameworks_yaml(stats):
    text = (ROOT / "matrix" / "config" / "frameworks.yaml").read_text(encoding="utf-8")
    for slug in stats["frameworks_control_level_slugs"]:
        assert f"{slug}:" in text


# ---------- (b) built HTML carries live counts, zero tokens ----------

@pytest.fixture(scope="module")
def built(tmp_path_factory, stats):
    out = tmp_path_factory.mktemp("collateral")
    bc.build_all(template_dir=str(PRES), out_dir=str(out), stats=stats)
    return out


@pytest.mark.parametrize("name", sorted(bc.TEMPLATES.values()))
def test_built_html_has_live_counts_and_no_tokens(built, stats, name):
    html = (built / name).read_text(encoding="utf-8")
    assert "__STAT_" not in html
    for needle in (str(stats["uc_total"]), str(stats["identity_total"]),
                   str(stats["frameworks_control_level"])):
        assert needle in html
    # stale legacy headline counts must be gone
    assert f">{stats['uc_total']}<" in html or f"{stats['uc_total']}<small" in html
    assert ">84<" not in html and "84<small" not in html
    assert ">70<" not in html and "70<small" not in html


def test_built_stats_json_is_deterministic(built, stats):
    data = json.loads((built / "instrument-stats.json").read_text(encoding="utf-8"))
    assert data == json.loads(json.dumps(stats))
    assert list(data) == sorted(data)


def test_checked_in_collateral_matches_live_data(stats):
    """The committed instrument-*.html must already carry the live counts."""
    for name in bc.TEMPLATES.values():
        html = (PRES / name).read_text(encoding="utf-8")
        assert "__STAT_" not in html
        assert str(stats["uc_total"]) in html


# ---------- (c) unknown token -> nonzero exit ----------

def test_inject_raises_on_unknown_token(stats):
    tokens = istats.stat_tokens(stats)
    with pytest.raises(bc.CollateralError):
        bc.inject("<b>__STAT_BOGUS__</b>", tokens, name="bogus")


def test_cli_exits_nonzero_on_unknown_token(tmp_path, stats):
    for tpl in bc.TEMPLATES:
        shutil.copy(PRES / tpl, tmp_path / tpl)
    bad = tmp_path / "instrument-a4-template.html"
    bad.write_text(bad.read_text(encoding="utf-8")
                   + "\n<!-- __STAT_DOES_NOT_EXIST__ -->\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(PRES / "build_collateral.py"),
         "--templates", str(tmp_path), "--out", str(tmp_path)],
        capture_output=True, text=True)
    assert proc.returncode != 0
    assert "__STAT_DOES_NOT_EXIST__" in proc.stderr

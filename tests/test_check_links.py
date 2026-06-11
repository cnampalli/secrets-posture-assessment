"""Tests for matrix/check_links.py — link-rot + quote-presence checker (H1d).

No real network: every test injects a fake fetch function (or monkeypatches
check_links.fetch_url). The tool REPORTS drift only — it never mutates data,
so these tests only ever assert on returned results and exit codes.
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))
import check_links as cl


# --- helpers -----------------------------------------------------------------

def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def fake_fetch_factory(pages, calls=None):
    """Return a fetch function serving canned pages.

    `pages` maps url -> html string (served as 200) or an int status (DEAD).
    `calls` (optional list) records every URL fetched, for de-dup assertions.
    """
    def fetch(url, timeout=None, want_body=False):
        if calls is not None:
            calls.append(url)
        page = pages.get(url)
        if page is None:
            return cl.FetchResult(None, "", "DNS failure")
        if isinstance(page, int):
            return cl.FetchResult(page, "", f"HTTP {page}")
        return cl.FetchResult(200, page, "")
    return fetch


VENDOR_FIELDS = ("vendor_slug", "vendor_name", "target_id", "target_type", "coverage",
                 "maturity", "evidence_url", "evidence_quote", "citation_keys", "notes")


def vendor_row(url, quote, **extra):
    row = {f: "x" for f in VENDOR_FIELDS}
    row.update({"evidence_url": url, "evidence_quote": quote})
    row.update(extra)
    return row


# --- text normalisation ------------------------------------------------------

def test_normalize_curly_quotes_become_straight():
    assert cl.normalize_text("‘it’s a “test”") == "'it's a \"test\""


def test_normalize_dashes_become_hyphen():
    assert cl.normalize_text("approach – preventative—remediative") == \
        "approach - preventative-remediative"


def test_normalize_collapses_whitespace():
    assert cl.normalize_text("a\n  b\t\tc   d") == "a b c d"


def test_quote_in_page_tolerates_punctuation_drift():
    # CSV quote uses curly quotes + en-dash + wrapped whitespace; the live page
    # uses straight quotes and a hyphen — the WS3 normalisation must MATCH them.
    quote = "the “dual approach” – preventative\n   and remediative"
    page = "<html><body><p>We support the \"dual approach\" - preventative and remediative controls.</p></body></html>"
    assert cl.quote_in_page(quote, page) is True


def test_quote_in_page_absent_is_false():
    assert cl.quote_in_page("this sentence is nowhere", "<p>unrelated content</p>") is False


def test_strip_html_drops_script_and_style():
    html = "<html><script>var x = 'hidden';</script><style>.a{}</style><p>visible text</p></html>"
    text = cl.strip_html(html)
    assert "visible text" in text
    assert "hidden" not in text


# --- link-rot check ----------------------------------------------------------

def test_check_links_ok_and_dead():
    fetch = fake_fetch_factory({
        "https://ok.example/a": "<p>fine</p>",
        "https://dead.example/b": 404,
    })
    results = cl.check_links(["https://ok.example/a", "https://dead.example/b"], fetch=fetch)
    assert results["https://ok.example/a"]["status"] == "OK"
    assert results["https://dead.example/b"]["status"] == "DEAD"


def test_check_links_unreachable_is_dead():
    fetch = fake_fetch_factory({})  # every URL -> DNS failure
    results = cl.check_links(["https://gone.example/"], fetch=fetch)
    assert results["https://gone.example/"]["status"] == "DEAD"


def test_check_links_deduplicates_urls():
    calls = []
    fetch = fake_fetch_factory({"https://ok.example/a": "<p>fine</p>"}, calls=calls)
    cl.check_links(["https://ok.example/a", "https://ok.example/a", "https://ok.example/a"],
                   fetch=fetch)
    assert calls == ["https://ok.example/a"]


# --- quote-presence check ----------------------------------------------------

def test_check_quotes_match_and_drift():
    page = "<p>Auth methods provide full coverage of cloud identities.</p>"
    fetch = fake_fetch_factory({"https://ok.example/doc": page})
    records = [
        cl.Record("v.csv", 2, "https://ok.example/doc", "full coverage of cloud identities", None),
        cl.Record("v.csv", 3, "https://ok.example/doc", "this quote drifted away", None),
    ]
    results = cl.check_quotes(records, fetch=fetch)
    assert [r["result"] for r in results] == ["MATCH", "DRIFT"]


def test_check_quotes_unreachable_source():
    fetch = fake_fetch_factory({"https://dead.example/doc": 503})
    records = [cl.Record("v.csv", 2, "https://dead.example/doc", "any quote", None)]
    results = cl.check_quotes(records, fetch=fetch)
    assert results[0]["result"] == "SOURCE-UNREACHABLE"


def test_check_quotes_caches_page_per_url():
    calls = []
    page = "<p>shared page text here</p>"
    fetch = fake_fetch_factory({"https://ok.example/doc": page}, calls=calls)
    records = [
        cl.Record("v.csv", 2, "https://ok.example/doc", "shared page", None),
        cl.Record("v.csv", 3, "https://ok.example/doc", "text here", None),
    ]
    cl.check_quotes(records, fetch=fetch)
    assert calls == ["https://ok.example/doc"]


def test_check_quotes_skips_non_verbatim_when_column_present():
    page = "<p>only the verbatim text appears</p>"
    fetch = fake_fetch_factory({"https://ok.example/doc": page})
    records = [
        cl.Record("v.csv", 2, "https://ok.example/doc", "verbatim text appears", "verbatim"),
        cl.Record("v.csv", 3, "https://ok.example/doc", "analyst summary of things", "analyst-note"),
        cl.Record("v.csv", 4, "https://ok.example/doc", "a paraphrase of things", "paraphrase"),
    ]
    results = cl.check_quotes(records, fetch=fetch)
    assert len(results) == 1
    assert results[0]["row"] == 2
    assert results[0]["result"] == "MATCH"


def test_check_quotes_column_absent_treats_all_as_verbatim():
    page = "<p>only the verbatim text appears</p>"
    fetch = fake_fetch_factory({"https://ok.example/doc": page})
    records = [
        cl.Record("v.csv", 2, "https://ok.example/doc", "verbatim text appears", None),
        cl.Record("v.csv", 3, "https://ok.example/doc", "not on the page at all", None),
    ]
    results = cl.check_quotes(records, fetch=fetch)
    assert len(results) == 2
    assert [r["result"] for r in results] == ["MATCH", "DRIFT"]


# --- CSV collection ----------------------------------------------------------

def test_collect_records_reads_evidence_columns(tmp_path):
    write_csv(tmp_path / "vendor-capabilities.csv", VENDOR_FIELDS, [
        vendor_row("https://a.example/", "quote a"),
        vendor_row("https://b.example/", ""),          # url but no quote
        vendor_row("", "orphan quote"),                 # no url -> skipped
    ])
    records = cl.collect_records(str(tmp_path))
    assert [(r.url, r.quote) for r in records] == \
        [("https://a.example/", "quote a"), ("https://b.example/", "")]
    # no quote_type column in this file -> None
    assert all(r.quote_type is None for r in records)


def test_collect_records_picks_up_quote_type_column(tmp_path):
    fields = VENDOR_FIELDS + ("quote_type",)
    write_csv(tmp_path / "vendor-capabilities.csv", fields, [
        vendor_row("https://a.example/", "quote a", quote_type="verbatim"),
        vendor_row("https://b.example/", "note b", quote_type="analyst-note"),
    ])
    records = cl.collect_records(str(tmp_path))
    assert [r.quote_type for r in records] == ["verbatim", "analyst-note"]


def test_collect_records_ignores_csvs_without_evidence_url(tmp_path):
    write_csv(tmp_path / "use-cases.csv", ("uc_id", "story"), [{"uc_id": "UC-1", "story": "s"}])
    assert cl.collect_records(str(tmp_path)) == []


# --- CLI ---------------------------------------------------------------------

def make_data_dir(tmp_path, url_ok, url_dead):
    write_csv(tmp_path / "vendor-capabilities.csv", VENDOR_FIELDS, [
        vendor_row(url_ok, "matching quote text"),
        vendor_row(url_dead, "whatever quote"),
    ])
    return str(tmp_path)


def test_cli_strict_exits_nonzero_on_dead(tmp_path, monkeypatch, capsys):
    data_dir = make_data_dir(tmp_path, "https://ok.example/", "https://dead.example/")
    monkeypatch.setattr(cl, "fetch_url", fake_fetch_factory({
        "https://ok.example/": "<p>matching quote text</p>",
        "https://dead.example/": 404,
    }))
    rc = cl.main(["--data-dir", data_dir, "--links-only", "--strict"])
    assert rc != 0
    out = capsys.readouterr().out
    assert "DEAD" in out and "https://dead.example/" in out


def test_cli_non_strict_reports_but_exits_zero(tmp_path, monkeypatch, capsys):
    data_dir = make_data_dir(tmp_path, "https://ok.example/", "https://dead.example/")
    monkeypatch.setattr(cl, "fetch_url", fake_fetch_factory({
        "https://ok.example/": "<p>matching quote text</p>",
        "https://dead.example/": 404,
    }))
    rc = cl.main(["--data-dir", data_dir, "--links-only"])
    assert rc == 0
    assert "DEAD" in capsys.readouterr().out


def test_cli_all_clean_exits_zero_even_strict(tmp_path, monkeypatch, capsys):
    write_csv(tmp_path / "vendor-capabilities.csv", VENDOR_FIELDS, [
        vendor_row("https://ok.example/", "matching quote text"),
    ])
    monkeypatch.setattr(cl, "fetch_url", fake_fetch_factory({
        "https://ok.example/": "<p>some matching quote text here</p>",
    }))
    rc = cl.main(["--data-dir", str(tmp_path), "--strict"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "MATCH" in out or "match" in out.lower()


def test_cli_quotes_only_reports_drift(tmp_path, monkeypatch, capsys):
    write_csv(tmp_path / "vendor-capabilities.csv", VENDOR_FIELDS, [
        vendor_row("https://ok.example/", "text that is not on the page"),
    ])
    monkeypatch.setattr(cl, "fetch_url", fake_fetch_factory({
        "https://ok.example/": "<p>entirely different content</p>",
    }))
    rc = cl.main(["--data-dir", str(tmp_path), "--quotes-only", "--strict"])
    assert rc != 0
    assert "DRIFT" in capsys.readouterr().out

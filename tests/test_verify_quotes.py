"""Tests for scripts/verify_quotes.py — the verbatim-fidelity quote ledger.

NO network: all fetching is stubbed. Covers hash normalisation stability,
verbatim match logic, elided segment-order logic, ledger write determinism,
and mismatch recording.
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import verify_quotes as vq  # noqa: E402
from verify_quotes import (  # noqa: E402
    PoliteFetcher, elided_segments, entry_key, load_ledger, mark_mismatch,
    mark_verified, new_entry, quote_matches, quote_sha256, run_fetch_pass,
    select_for_fetch, sync_entries, write_ledger,
)

FR = vq.check_links.FetchResult


def stub_fetch(pages):
    """fetch_url stand-in: pages maps url -> FetchResult or html string."""
    def fetch(url, timeout=None, want_body=True):
        res = pages.get(url, FR(None, "", "unreachable: stub"))
        if isinstance(res, str):
            return FR(200, res, "")
        return res
    return fetch


def make_fetcher(pages):
    # no throttling delays in tests
    return PoliteFetcher(fetch=stub_fetch(pages), sleep=lambda s: None)


# --- hashing / normalisation --------------------------------------------------

def test_hash_normalisation_stable_across_typography():
    a = quote_sha256("Access to “systems” — validated\n when   first requested.")
    b = quote_sha256('Access to "systems" - validated when first requested.')
    assert a == b
    assert len(a) == 64
    # stable across calls
    assert a == quote_sha256("Access to “systems” — validated\n when   first requested.")


def test_hash_differs_for_different_quotes():
    assert quote_sha256("alpha") != quote_sha256("beta")


def test_hash_folds_case_and_trailing_punctuation():
    # excerpt-initial capital + sentence-final '.' hash identically to the
    # raw source text — hashing agrees with the matcher's tolerance
    assert quote_sha256("Maintain an information security capability.") == \
        quote_sha256("maintain an information security capability")


def test_match_normalize_folds_punctuation_spacing():
    # HTML rendering artifact: "criteria ] ;" (csf.tools) == "criteria];"
    assert vq.match_normalize("criteria ] ; and") == \
        vq.match_normalize("criteria]; and")


# --- verbatim match logic ------------------------------------------------------

PAGE = ("<html><body><p>Requests for privileged access to systems, "
        "applications and data repositories are validated when first "
        "requested.</p><p>Other text here about access control.</p>"
        "<script>ignore.me()</script></body></html>")
PAGE_NORM = vq.check_links.normalize_text(vq.check_links.strip_html(PAGE))


def test_verbatim_match_with_curly_quotes_and_whitespace():
    quote = ("Requests for privileged access to systems,\n applications "
             "and data repositories are validated when first requested.")
    ok, detail = quote_matches(quote, "verbatim", PAGE_NORM)
    assert ok and detail == ""


def test_verbatim_no_match():
    ok, detail = quote_matches("this text is nowhere", "verbatim", PAGE_NORM)
    assert not ok
    assert "not found" in detail


def test_verbatim_excerpt_case_and_final_period_tolerated():
    # source (mid-sentence, continuing): "...applications and data
    # repositories are validated when first requested."
    ok, _ = quote_matches(
        "Applications and data repositories are validated.", "verbatim",
        PAGE_NORM)
    assert ok


def test_real_word_difference_is_still_a_mismatch():
    # leniency must not swallow real edits ("their resources" != "applications")
    ok, _ = quote_matches(
        "Requests for privileged access to systems and their resources are "
        "validated when first requested.", "verbatim", PAGE_NORM)
    assert not ok


# --- elided segment-order logic ------------------------------------------------

def test_elided_segments_split_on_both_ellipsis_styles():
    assert elided_segments("alpha ... beta … gamma") == ["alpha", "beta", "gamma"]
    assert elided_segments("alpha [...] beta") == ["alpha", "beta"]


def test_elided_match_in_order():
    ok, _ = quote_matches(
        "Requests for privileged access … validated when first requested.",
        "verbatim-elided", PAGE_NORM)
    assert ok


def test_elided_out_of_order_is_mismatch():
    ok, detail = quote_matches(
        "validated when first requested ... Requests for privileged access",
        "verbatim-elided", PAGE_NORM)
    assert not ok
    assert "segment 2" in detail


def test_elided_missing_segment_is_mismatch():
    ok, detail = quote_matches(
        "Requests for privileged access ... text that is absent",
        "verbatim-elided", PAGE_NORM)
    assert not ok


# --- fetch pass / mismatch recording -------------------------------------------

K1 = entry_key("secrets", "essential-8", "E8-RAP-ML1", "acsc-e8-2023",
               quote_sha256("Requests for privileged access to systems, "
                            "applications and data repositories are validated "
                            "when first requested."))
K2 = entry_key("pam", "apra-cps-234", "CPS234-21", "apra-cps234",
               quote_sha256("this quote does not appear anywhere"))
K3 = entry_key("iga", "apra-cps-230", "CPS230-36", "apra-cps230",
               quote_sha256("segment one ... segment two"))

ROWS = {
    K1: {"quote": ("Requests for privileged access to systems, applications "
                   "and data repositories are validated when first requested."),
         "quote_type": "verbatim", "source_url": "https://example.org/e8"},
    K2: {"quote": "this quote does not appear anywhere",
         "quote_type": "verbatim", "source_url": "https://example.org/e8"},
    K3: {"quote": "segment one ... segment two",
         "quote_type": "verbatim-elided", "source_url": "https://example.org/pdf.pdf"},
}
PAGES = {"https://example.org/e8": PAGE,
         "https://example.org/pdf.pdf": FR(200, "%PDF-1.7 binary...", "")}


def fresh_entries():
    return {k: new_entry(k, ROWS[k]["source_url"]) for k in ROWS}


def test_fetch_pass_verifies_matches_and_records_mismatch():
    entries = fresh_entries()
    run_fetch_pass(entries, ROWS, list(ROWS), make_fetcher(PAGES),
                   today="2026-07-02")
    assert entries[K1]["status"] == "verified"
    assert entries[K1]["method"] == "fetched"
    assert entries[K1]["verified_on"] == "2026-07-02"
    # quote genuinely absent -> recorded as mismatch, not hidden
    assert entries[K2]["status"] == "mismatch"
    assert entries[K2]["method"] == "fetched"
    assert "not found" in entries[K2]["note"]


def test_pdf_source_stays_pending_manual():
    entries = fresh_entries()
    run_fetch_pass(entries, ROWS, list(ROWS), make_fetcher(PAGES))
    assert entries[K3]["status"] == "pending-manual"
    assert entries[K3]["note"] == "PDF source"
    assert entries[K3]["method"] is None


def test_http_failure_stays_pending_with_note():
    pages = dict(PAGES)
    pages["https://example.org/e8"] = FR(403, "", "HTTP 403")
    entries = fresh_entries()
    run_fetch_pass(entries, ROWS, [K1], make_fetcher(pages))
    assert entries[K1]["status"] == "pending-manual"
    assert entries[K1]["note"] == "HTTP 403"


def test_fetch_retries_once_then_gives_up():
    calls = []
    def flaky(url, timeout=None, want_body=True):
        calls.append(url)
        return FR(None, "", "unreachable: reset")
    f = PoliteFetcher(fetch=flaky, sleep=lambda s: None)
    ok, _, detail = f.page_text("https://example.org/x")
    assert not ok and detail.startswith("unreachable")
    assert len(calls) == 2                      # one retry
    f.page_text("https://example.org/x")        # cached — no third call
    assert len(calls) == 2


def test_human_verification_survives_refresh_selection():
    entries = fresh_entries()
    mark_verified(entries, K3[4][:16], "fetched-pdf", "PDF p.7",
                  today="2026-07-02")
    assert entries[K3]["status"] == "verified"
    keys = select_for_fetch(entries, ROWS, "all")
    assert K3 not in keys and K1 in keys and K2 in keys


# --- ledger write determinism ---------------------------------------------------

def test_ledger_write_is_deterministic(tmp_path):
    entries = fresh_entries()
    run_fetch_pass(entries, ROWS, list(ROWS), make_fetcher(PAGES),
                   today="2026-07-02")
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    write_ledger(entries, str(p1), today="2026-07-02")
    # same input in a different dict insertion order -> identical bytes
    shuffled = {k: dict(entries[k]) for k in reversed(list(entries))}
    write_ledger(shuffled, str(p2), today="2026-07-02")
    assert p1.read_bytes() == p2.read_bytes()
    doc = json.loads(p1.read_text())
    assert doc["schema_version"] == vq.SCHEMA_VERSION
    assert doc["generated_on"] == "2026-07-02"
    assert [e["quote_sha256"] for e in doc["entries"]] == \
        [k[4] for k in sorted(entries)]
    assert list(doc["entries"][0]) == list(vq.ENTRY_FIELDS)


def test_ledger_roundtrip_preserves_entries(tmp_path):
    entries = fresh_entries()
    run_fetch_pass(entries, ROWS, list(ROWS), make_fetcher(PAGES),
                   today="2026-07-02")
    path = tmp_path / "ledger.json"
    write_ledger(entries, str(path), today="2026-07-02")
    loaded = load_ledger(str(path))
    assert loaded == {k: {f: entries[k][f] for f in vq.ENTRY_FIELDS}
                      for k in entries}
    # sync keeps verification state, drops vanished rows, adds new pending
    rows2 = {K1: ROWS[K1]}
    synced = sync_entries(rows2, loaded)
    assert set(synced) == {K1}
    assert synced[K1]["status"] == "verified"


# --- mark-verified resolution ---------------------------------------------------

def test_mark_verified_requires_note_and_unique_key():
    entries = fresh_entries()
    with pytest.raises(SystemExit):
        mark_verified(entries, K1[4][:12], "manual", "")     # note required
    with pytest.raises(SystemExit):
        mark_verified(entries, "no-such-key", "manual", "n")
    key = mark_verified(entries, "secrets|essential-8|E8-RAP-ML1",
                        "manual", "checked by hand", today="2026-07-02")
    assert key == K1
    assert entries[K1]["method"] == "manual"
    assert entries[K1]["note"] == "checked by hand"


def test_mark_mismatch_records_adjudicated_mismatch():
    entries = fresh_entries()
    key = mark_mismatch(entries, K3[4][:16], "fetched-pdf",
                        "PDF p.6: source sentence continues past the quote",
                        today="2026-07-02")
    assert key == K3
    assert entries[K3]["status"] == "mismatch"
    assert entries[K3]["method"] == "fetched-pdf"
    assert entries[K3]["verified_on"] == "2026-07-02"
    # human-adjudicated mismatches also survive --refresh selection
    assert K3 not in select_for_fetch(entries, ROWS, "all")
    with pytest.raises(SystemExit):
        mark_mismatch(entries, K1[4][:12], "fetched-pdf", "")  # note required


def test_mark_pending_records_precise_note():
    entries = fresh_entries()
    key = vq.mark_pending(entries, K3[4][:16],
                          "HTTP 404 - vendor removed the incident post")
    assert key == K3
    assert entries[K3]["status"] == "pending-manual"
    assert entries[K3]["method"] is None
    assert "404" in entries[K3]["note"]
    with pytest.raises(SystemExit):
        vq.mark_pending(entries, K1[4][:12], "")           # note required


def test_load_rows_scope_matches_expected_shape():
    rows = vq.load_rows()
    # ~168 in-scope rows since the paraphrase re-labelling of 2026-07-03
    assert len(rows) >= 160
    assert all(v["quote_type"] in ("verbatim", "verbatim-elided")
               for v in rows.values())
    assert all(len(k[4]) == 64 for k in rows)

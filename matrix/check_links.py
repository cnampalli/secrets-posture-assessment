#!/usr/bin/env python3
"""Link-rot + quote-presence checker for the matrix evidence trail (H1d).

Standalone provenance tool — NOT part of the build-failing validate_data gate.
Runs on the data-provenance.yaml refresh cadence and REPORTS drift; it never
rewrites data.

Two checks across the data CSVs in a domain data dir:

1. Link rot — every distinct `evidence_url` gets an HTTP request (HEAD with a
   GET fallback, redirects followed). 2xx/3xx -> OK; 4xx/5xx/timeout/DNS -> DEAD.
2. Quote presence — for each row with a non-empty `evidence_quote`, fetch the
   page, strip HTML to text, normalise whitespace + quote characters
   (curly -> straight quotes, en/em-dash -> hyphen; the WS3 verification method
   documented in research/iga/vendor-fit.md "Citation verification"), then
   require the quote as a contiguous substring. MATCH / DRIFT /
   SOURCE-UNREACHABLE per row. Only rows whose `quote_type` is absent or
   `verbatim` are checked (a missing column means all quoted rows are verbatim).

CLI: python3 matrix/check_links.py [--data-dir DIR] [--links-only]
                                   [--quotes-only] [--strict] [--timeout S]

Exit code: 0 unless --strict and any DEAD link / DRIFT / SOURCE-UNREACHABLE.
Stdlib only (urllib.request) — no new dependency.
"""
import argparse
import csv
import glob
import os
import re
import socket
import sys
import urllib.error
import urllib.request
from collections import namedtuple
from html.parser import HTMLParser

DEFAULT_TIMEOUT = 20
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 provenance-check/1.0")

FetchResult = namedtuple("FetchResult", ("status", "body", "error"))
Record = namedtuple("Record", ("file", "row", "url", "quote", "quote_type"))

# WS3 normalisation gotchas: curly quotes and en/em dashes drift between CSV
# quotes and live pages; both sides are mapped to ASCII before comparison.
_CHAR_MAP = {
    "‘": "'", "’": "'", "‚": "'", "′": "'", "`": "'", "´": "'",
    "“": '"', "”": '"', "„": '"',
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ",
}
_CHAR_TABLE = str.maketrans(_CHAR_MAP)
_WS_RE = re.compile(r"\s+")


def normalize_text(text):
    """Normalise quote characters, dashes, and whitespace for comparison."""
    return _WS_RE.sub(" ", (text or "").translate(_CHAR_TABLE)).strip()


class _TextExtractor(HTMLParser):
    """Strip HTML to visible text, skipping script/style/noscript content."""
    _SKIP = {"script", "style", "noscript", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._chunks = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self._chunks.append(data)

    def text(self):
        return " ".join(self._chunks)


def strip_html(html):
    parser = _TextExtractor()
    try:
        parser.feed(html or "")
    except Exception:                       # malformed HTML — keep what we got
        pass
    return parser.text()


def quote_in_page(quote, html):
    """True if the normalised quote appears contiguously in the page text."""
    return normalize_text(quote) in normalize_text(strip_html(html))


# --- HTTP --------------------------------------------------------------------

def _request(url, method, timeout):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = "" if method == "HEAD" else resp.read().decode(
            resp.headers.get_content_charset() or "utf-8", errors="replace")
        return FetchResult(resp.status, body, "")


def fetch_url(url, timeout=DEFAULT_TIMEOUT, want_body=False):
    """Fetch a URL, following redirects. HEAD first unless the body is needed;
    GET fallback for servers that reject HEAD. Returns FetchResult(status,
    body, error) — status is None when no HTTP response was obtained."""
    methods = ["GET"] if want_body else ["HEAD", "GET"]
    result = FetchResult(None, "", "no request made")
    for method in methods:
        try:
            return _request(url, method, timeout)
        except urllib.error.HTTPError as exc:
            result = FetchResult(exc.code, "", f"HTTP {exc.code}")
        except (urllib.error.URLError, socket.timeout, TimeoutError) as exc:
            reason = getattr(exc, "reason", exc)
            result = FetchResult(None, "", f"unreachable: {reason}")
        except Exception as exc:            # noqa: BLE001 — report, never crash
            result = FetchResult(None, "", f"error: {exc}")
    return result


def _is_ok(res):
    return res.status is not None and 200 <= res.status < 400


# --- checks ------------------------------------------------------------------

def check_links(urls, fetch=None, timeout=DEFAULT_TIMEOUT):
    """Check each distinct URL once. Returns {url: {"status": OK|DEAD,
    "detail": str}} preserving first-seen order."""
    fetch = fetch or fetch_url
    results = {}
    for url in urls:
        if url in results:
            continue
        res = fetch(url, timeout=timeout, want_body=False)
        results[url] = {
            "status": "OK" if _is_ok(res) else "DEAD",
            "detail": f"HTTP {res.status}" if res.status is not None else res.error,
        }
    return results


def _is_verbatim(quote_type):
    # Column absent (None) -> all quoted rows are verbatim; otherwise only
    # blank or explicit "verbatim" rows are checked.
    return quote_type is None or quote_type.strip().lower() in ("", "verbatim")


def check_quotes(records, fetch=None, timeout=DEFAULT_TIMEOUT):
    """Check quote presence for verbatim-quoted rows. Returns a list of
    {"file", "row", "url", "result": MATCH|DRIFT|SOURCE-UNREACHABLE, "detail"}.
    Pages are fetched once per URL."""
    fetch = fetch or fetch_url
    page_cache = {}                          # url -> (ok, normalised_text, detail)
    results = []
    for rec in records:
        if not rec.quote.strip() or not _is_verbatim(rec.quote_type):
            continue
        if rec.url not in page_cache:
            res = fetch(rec.url, timeout=timeout, want_body=True)
            if _is_ok(res):
                page_cache[rec.url] = (True, normalize_text(strip_html(res.body)), "")
            else:
                detail = f"HTTP {res.status}" if res.status is not None else res.error
                page_cache[rec.url] = (False, "", detail)
        ok, page_text, detail = page_cache[rec.url]
        if not ok:
            verdict = "SOURCE-UNREACHABLE"
        elif normalize_text(rec.quote) in page_text:
            verdict = "MATCH"
        else:
            verdict, detail = "DRIFT", "quote not found on page"
        results.append({"file": rec.file, "row": rec.row, "url": rec.url,
                        "result": verdict, "detail": detail})
    return results


# --- CSV collection ----------------------------------------------------------

def collect_records(data_dir):
    """Collect (file, row, url, quote, quote_type) from every *.csv in
    data_dir that has an evidence_url column. quote_type is None when the
    column is absent from that file."""
    records = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.csv"))):
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fields = reader.fieldnames or []
            if "evidence_url" not in fields:
                continue
            has_quote_type = "quote_type" in fields
            for i, row in enumerate(reader, start=2):   # 1-based, after header
                url = (row.get("evidence_url") or "").strip()
                if not url:
                    continue
                records.append(Record(
                    file=os.path.basename(path), row=i, url=url,
                    quote=(row.get("evidence_quote") or "").strip(),
                    quote_type=(row.get("quote_type") or "") if has_quote_type else None,
                ))
    return records


def default_data_dir(root="."):
    """The secrets descriptor's data dir, matching validate_data's default."""
    try:
        sys.path.insert(0, os.path.join(root, "matrix"))
        import validate_data                 # noqa: PLC0415 — optional reuse
        return validate_data.default_data_dir(root)
    except Exception:
        return os.path.join(root, "matrix", "domains", "secrets")


# --- CLI ---------------------------------------------------------------------

def _print_link_report(link_results, records):
    urls_by_file = {}
    for rec in records:
        urls_by_file.setdefault(rec.url, set()).add(rec.file)
    dead = {u: r for u, r in link_results.items() if r["status"] == "DEAD"}
    ok_n = len(link_results) - len(dead)
    print(f"\nLink-rot check: {len(link_results)} distinct URLs — {ok_n} OK, {len(dead)} DEAD")
    if dead:
        print(f"  {'STATUS':<6} {'DETAIL':<28} URL  [files]")
        for url, res in dead.items():
            files = ",".join(sorted(urls_by_file.get(url, ())))
            print(f"  {'DEAD':<6} {res['detail']:<28} {url}  [{files}]")
    return len(dead)


def _print_quote_report(quote_results, skipped):
    counts = {"MATCH": 0, "DRIFT": 0, "SOURCE-UNREACHABLE": 0}
    for r in quote_results:
        counts[r["result"]] += 1
    print(f"\nQuote-presence check: {len(quote_results)} verbatim quotes — "
          f"{counts['MATCH']} MATCH, {counts['DRIFT']} DRIFT, "
          f"{counts['SOURCE-UNREACHABLE']} SOURCE-UNREACHABLE "
          f"({skipped} non-verbatim rows skipped)")
    problems = [r for r in quote_results if r["result"] != "MATCH"]
    if problems:
        print(f"  {'RESULT':<19} {'WHERE':<34} URL")
        for r in problems:
            where = f"{r['file']}:{r['row']}"
            print(f"  {r['result']:<19} {where:<34} {r['url']}")
    return counts["DRIFT"] + counts["SOURCE-UNREACHABLE"]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Report link rot and evidence-quote drift in the matrix data CSVs. "
                    "Read-only: reports drift, never rewrites data.")
    ap.add_argument("--data-dir", default=None,
                    help="domain data dir (default: the secrets descriptor's data_dir)")
    ap.add_argument("--links-only", action="store_true", help="run only the link-rot check")
    ap.add_argument("--quotes-only", action="store_true", help="run only the quote-presence check")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero on any DEAD link, DRIFT, or SOURCE-UNREACHABLE quote")
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                    help=f"per-request timeout in seconds (default {DEFAULT_TIMEOUT})")
    args = ap.parse_args(argv)

    data_dir = args.data_dir or default_data_dir(".")
    records = collect_records(data_dir)
    print(f"check_links: {len(records)} evidence rows in {data_dir}")
    if not records:
        print("nothing to check")
        return 0

    problems = 0
    if not args.quotes_only:
        link_results = check_links((r.url for r in records), timeout=args.timeout)
        problems += _print_link_report(link_results, records)
    if not args.links_only:
        quoted = [r for r in records if r.quote.strip()]
        checked = check_quotes(quoted, timeout=args.timeout)
        skipped = len(quoted) - len(checked)
        problems += _print_quote_report(checked, skipped)

    print(f"\n{'PROBLEMS: ' + str(problems) if problems else 'ALL CLEAN'}"
          f"{' (strict: failing)' if problems and args.strict else ''}")
    return 1 if (problems and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())

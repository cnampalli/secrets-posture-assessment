#!/usr/bin/env python3
"""Verbatim-fidelity quote ledger for The Instrument (Wave 1.1, F-04).

Machine evidence that every "verbatim" regulatory quote actually appears in
its cited source. Scope: every row in
matrix/domains/{secrets,pam,iga}/regulatory-trace.csv whose quote_type is
`verbatim` or `verbatim-elided`.

Reuses the verification machinery from matrix/check_links.py (H1d):
normalize_text (curly-quote / en-dash / whitespace normalisation), strip_html,
and fetch_url — so hashing and matching agree with the existing provenance
tooling.

Match rules — normalisation is check_links.normalize_text (curly-quote /
en-dash / whitespace folding) PLUS, on both sides of every comparison:
casefolding, punctuation-spacing folding ("word ] ;" -> "word];", an HTML
rendering artifact on sites like csf.tools), and trailing-punctuation
tolerance (an excerpt may capitalise its first word and close with "."
where the source sentence continues — standard citation practice):
  verbatim         whole normalised quote must appear as a contiguous
                   substring of the normalised source text.
  verbatim-elided  each `...` / `…`-separated segment must appear in the
                   source, in order (each match starts after the previous
                   segment's end).

Ledger: meta/quote-ledger.json
  {schema_version, generated_on, entries: [{domain, framework_slug,
   control_code, citation_key, quote_sha256, source_url, status, method,
   verified_on, note}]}
  status: "verified" | "pending-manual" | "mismatch"
  method: "fetched" | "fetched-pdf" | "manual" | null
  Entries are keyed by (domain, framework_slug, control_code, citation_key,
  quote_sha256) — citation_key is the row's full `citation_keys` value —
  sorted deterministically and stable across runs.

CLI
  python3 scripts/verify_quotes.py                # fetch new / never-checked entries
  python3 scripts/verify_quotes.py --refresh      # re-fetch everything (human
                                                  #   verifications — method
                                                  #   manual / fetched-pdf —
                                                  #   are preserved)
  python3 scripts/verify_quotes.py --only-pending # re-fetch pending-manual only
  python3 scripts/verify_quotes.py --report       # summary, no network
  python3 scripts/verify_quotes.py --mark-verified KEY --method fetched-pdf \
      --note "CPS 234 PDF p.7"                    # record a human verification
  KEY is the sha256 (or unique prefix) or a prefix of
  "domain|framework_slug|control_code|citation_key|sha256".

Politeness: <=1 request/sec per host, 15s timeout, one retry. Fetch failures
and non-HTML content (PDF) are recorded as pending-manual — never guessed.
Stdlib only.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from datetime import date
from urllib.parse import urlparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "matrix"))
import check_links  # noqa: E402  — reuse H1d machinery, do not reinvent

SCHEMA_VERSION = 1
DOMAINS = ("secrets", "pam", "iga")
IN_SCOPE_TYPES = ("verbatim", "verbatim-elided")
LEDGER_PATH = os.path.join(REPO_ROOT, "meta", "quote-ledger.json")
TRACE_TEMPLATE = os.path.join(REPO_ROOT, "matrix", "domains", "{domain}",
                              "regulatory-trace.csv")
FETCH_TIMEOUT = 15          # seconds
HOST_MIN_INTERVAL = 1.0     # <=1 request/sec per host
HUMAN_METHODS = ("manual", "fetched-pdf")

_ELLIPSIS_RE = re.compile(r"\[\s?\.\.\.\s?\]|\[…\]|\.\.\.|…")


# --- normalisation / hashing --------------------------------------------------

_PUNCT_BEFORE_RE = re.compile(r"\s+([.,;:)\]])")
_PUNCT_AFTER_RE = re.compile(r"([(\[])\s+")
_TRAIL_PUNCT_RE = re.compile(r"[.,;:]+$")


def match_normalize(text):
    """H1d normalisation (check_links.normalize_text: curly quotes, dashes,
    whitespace) plus casefolding and punctuation-spacing folding. Applied to
    BOTH the quote and the source text, and to hashing, so they agree."""
    t = check_links.normalize_text(text).casefold()
    return _PUNCT_AFTER_RE.sub(r"\1", _PUNCT_BEFORE_RE.sub(r"\1", t))


def _strip_trailing_punct(text):
    """Drop sentence-final punctuation: an excerpt may end with '.' where the
    source sentence continues."""
    return _TRAIL_PUNCT_RE.sub("", text).strip()


def quote_sha256(quote):
    """sha256 of the match-normalised evidence_quote (same normalisation the
    matcher uses, minus trailing punctuation, so hashing and matching agree)."""
    return hashlib.sha256(
        _strip_trailing_punct(match_normalize(quote)).encode("utf-8")).hexdigest()


def entry_key(domain, framework_slug, control_code, citation_key, sha):
    return (domain, framework_slug, control_code, citation_key, sha)


def key_str(key):
    return "|".join(key)


def load_rows(repo_root=REPO_ROOT):
    """In-scope rows across all domains -> {key: {"quote", "quote_type",
    "source_url"}}. Later duplicates of an identical key are collapsed."""
    rows = {}
    for domain in DOMAINS:
        path = TRACE_TEMPLATE.format(domain=domain).replace(REPO_ROOT, repo_root)
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                qtype = (row.get("quote_type") or "").strip().lower()
                if qtype not in IN_SCOPE_TYPES:
                    continue
                quote = (row.get("evidence_quote") or "").strip()
                key = entry_key(
                    domain,
                    (row.get("framework_slug") or "").strip(),
                    (row.get("control_code") or "").strip(),
                    (row.get("citation_keys") or "").strip(),
                    quote_sha256(quote))
                rows.setdefault(key, {
                    "quote": quote,
                    "quote_type": qtype,
                    "source_url": (row.get("evidence_url") or "").strip(),
                })
    return rows


# --- matching ----------------------------------------------------------------

def elided_segments(quote):
    """Match-normalised, non-empty segments of an elided quote, in source
    order, each with sentence-final punctuation stripped."""
    return [s for s in
            (_strip_trailing_punct(seg.strip()) for seg in
             _ELLIPSIS_RE.split(match_normalize(quote)))
            if s]


def quote_matches(quote, quote_type, page_text_norm):
    """(matched, detail). page_text_norm is the fetched source text after
    check_links normalisation; the extra match-normalisation (case,
    punctuation spacing) is applied here to both sides."""
    page = match_normalize(page_text_norm)      # idempotent over H1d folding
    if quote_type == "verbatim":
        if _strip_trailing_punct(match_normalize(quote)) in page:
            return True, ""
        return False, "quote not found in fetched source text"
    # verbatim-elided: each segment present, in source order
    pos = 0
    for n, seg in enumerate(elided_segments(quote), start=1):
        i = page.find(seg, pos)
        if i < 0:
            return False, (f"elided segment {n} not found in order "
                           f"in fetched source text")
        pos = i + len(seg)
    return True, ""


# --- polite fetching ---------------------------------------------------------

def looks_like_pdf(url, body):
    if urlparse(url).path.lower().endswith(".pdf"):
        return True
    return (body or "").lstrip()[:5] in ("%PDF-", "%PDF")


class PoliteFetcher:
    """<=1 request/sec per host, 15s timeout, one retry on failure.
    Caches by URL so each unique source is fetched once per run."""

    def __init__(self, fetch=None, timeout=FETCH_TIMEOUT,
                 min_interval=HOST_MIN_INTERVAL, sleep=time.sleep,
                 clock=time.monotonic):
        self._fetch = fetch or check_links.fetch_url
        self._timeout = timeout
        self._min_interval = min_interval
        self._sleep = sleep
        self._clock = clock
        self._last_hit = {}     # host -> monotonic time
        self._cache = {}        # url -> (ok, page_text_norm, detail)

    def _throttle(self, host):
        last = self._last_hit.get(host)
        if last is not None:
            wait = self._min_interval - (self._clock() - last)
            if wait > 0:
                self._sleep(wait)
        self._last_hit[host] = self._clock()

    def page_text(self, url):
        """(ok, normalised_page_text, detail). detail explains failures
        ("HTTP 403", "PDF source", "unreachable: ...")."""
        if url in self._cache:
            return self._cache[url]
        host = urlparse(url).netloc
        res = None
        for attempt in (1, 2):                       # one retry
            self._throttle(host)
            res = self._fetch(url, timeout=self._timeout, want_body=True)
            if res.status is not None and 200 <= res.status < 400:
                break
        if res.status is None or not (200 <= res.status < 400):
            detail = f"HTTP {res.status}" if res.status is not None else res.error
            out = (False, "", detail)
        elif looks_like_pdf(url, res.body):
            out = (False, "", "PDF source")
        else:
            out = (True,
                   check_links.normalize_text(check_links.strip_html(res.body)),
                   "")
        self._cache[url] = out
        return out


# --- ledger ------------------------------------------------------------------

ENTRY_FIELDS = ("domain", "framework_slug", "control_code", "citation_key",
                "quote_sha256", "source_url", "status", "method",
                "verified_on", "note")


def new_entry(key, source_url):
    d, fw, cc, ck, sha = key
    return {"domain": d, "framework_slug": fw, "control_code": cc,
            "citation_key": ck, "quote_sha256": sha, "source_url": source_url,
            "status": "pending-manual", "method": None,
            "verified_on": None, "note": "not yet checked"}


def entry_key_of(entry):
    return entry_key(entry["domain"], entry["framework_slug"],
                     entry["control_code"], entry["citation_key"],
                     entry["quote_sha256"])


def load_ledger(path=LEDGER_PATH):
    """{key: entry} from an existing ledger, or {} when absent."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {entry_key_of(e): e for e in data.get("entries", [])}


def write_ledger(entries_by_key, path=LEDGER_PATH, today=None):
    """Deterministic write: entries sorted by key, fixed field order,
    2-space indent, trailing newline. Same input -> identical bytes
    (generated_on aside, which is the run date)."""
    entries = [
        {f: entries_by_key[k].get(f) for f in ENTRY_FIELDS}
        for k in sorted(entries_by_key)
    ]
    doc = {"schema_version": SCHEMA_VERSION,
           "generated_on": today or date.today().isoformat(),
           "entries": entries}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def sync_entries(rows, existing):
    """Ledger entries for exactly the current in-scope rows: existing entries
    are kept (their verification state survives), new rows get fresh pending
    entries, entries for vanished/changed rows are dropped."""
    out = {}
    for key, row in rows.items():
        e = existing.get(key)
        if e is None:
            e = new_entry(key, row["source_url"])
        else:
            e = dict(e)
            e["source_url"] = row["source_url"]   # follow the CSV
        out[key] = e
    return out


# --- verification passes -----------------------------------------------------

def select_for_fetch(entries, rows, mode):
    """Keys to (re-)fetch. mode: "new" (default — never-checked entries),
    "pending" (--only-pending), "all" (--refresh). Human verifications
    (method manual / fetched-pdf) are never clobbered by a fetch pass."""
    keys = []
    for key in sorted(entries):
        e = entries[key]
        if e.get("method") in HUMAN_METHODS:
            continue
        if mode == "all":
            keys.append(key)
        elif mode == "pending":
            if e["status"] == "pending-manual":
                keys.append(key)
        else:  # new: never successfully checked and never annotated
            if e["status"] == "pending-manual" and e.get("note") == "not yet checked":
                keys.append(key)
    return keys


def run_fetch_pass(entries, rows, keys, fetcher, today=None, progress=None):
    """Fetch each entry's source and update status in place."""
    today = today or date.today().isoformat()
    for key in keys:
        e, row = entries[key], rows[key]
        ok, page_text, detail = fetcher.page_text(e["source_url"])
        if not ok:
            e.update(status="pending-manual", method=None,
                     verified_on=None, note=detail)
        else:
            matched, mdetail = quote_matches(row["quote"], row["quote_type"],
                                             page_text)
            if matched:
                e.update(status="verified", method="fetched",
                         verified_on=today, note="")
            else:
                e.update(status="mismatch", method="fetched",
                         verified_on=today, note=mdetail)
        if progress:
            progress(key, e)
    return entries


# --- mark-verified -----------------------------------------------------------

def resolve_key(entries, needle):
    """Resolve a user-supplied key: the sha256 (or a prefix of it), or a
    prefix of "domain|framework_slug|control_code|citation_key|sha256".
    Must match exactly one entry."""
    hits = [k for k in sorted(entries)
            if k[4].startswith(needle) or key_str(k).startswith(needle)]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit(f"mark-verified: no ledger entry matches {needle!r}")
    listing = "\n  ".join(key_str(k) for k in hits[:10])
    raise SystemExit(
        f"mark-verified: {needle!r} is ambiguous ({len(hits)} matches):\n  {listing}")


def mark_verified(entries, needle, method, note, today=None):
    key = resolve_key(entries, needle)
    if method not in ("manual", "fetched-pdf"):
        raise SystemExit("mark-verified: --method must be manual or fetched-pdf")
    if not note:
        raise SystemExit("mark-verified: --note is required (say what was checked)")
    entries[key].update(status="verified", method=method,
                        verified_on=today or date.today().isoformat(),
                        note=note)
    return key


def mark_mismatch(entries, needle, method, note, today=None):
    """Record a human-adjudicated mismatch (e.g. a PDF source whose text was
    inspected and genuinely differs from the quote). Note is mandatory —
    it must say HOW the quote differs."""
    key = resolve_key(entries, needle)
    if method not in ("manual", "fetched-pdf"):
        raise SystemExit("mark-mismatch: --method must be manual or fetched-pdf")
    if not note:
        raise SystemExit("mark-mismatch: --note is required (say how it differs)")
    entries[key].update(status="mismatch", method=method,
                        verified_on=today or date.today().isoformat(),
                        note=note)
    return key


def mark_pending(entries, needle, note):
    """Keep an entry pending-manual but record a precise note on why it
    could not be verified (dead URL, blocked fetch, ...)."""
    key = resolve_key(entries, needle)
    if not note:
        raise SystemExit("mark-pending: --note is required (say why unverifiable)")
    entries[key].update(status="pending-manual", method=None,
                        verified_on=None, note=note)
    return key


# --- report ------------------------------------------------------------------

def summarize(entries):
    counts = {"verified": 0, "pending-manual": 0, "mismatch": 0}
    methods = {"fetched": 0, "fetched-pdf": 0, "manual": 0}
    for e in entries.values():
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        if e["status"] == "verified" and e.get("method") in methods:
            methods[e["method"]] += 1
    return counts, methods


def print_report(entries):
    counts, methods = summarize(entries)
    print(f"quote ledger: {len(entries)} entries")
    print(f"  verified        {counts['verified']:4d}  "
          f"(fetched {methods['fetched']}, fetched-pdf {methods['fetched-pdf']}, "
          f"manual {methods['manual']})")
    print(f"  pending-manual  {counts['pending-manual']:4d}")
    print(f"  mismatch        {counts['mismatch']:4d}")
    mismatches = [e for _, e in sorted(entries.items())
                  if e["status"] == "mismatch"]
    if mismatches:
        print("\nMISMATCHES (quote not found in cited source):")
        for e in mismatches:
            print(f"  {key_str(entry_key_of(e))}\n"
                  f"    {e['source_url']}\n    {e['note']}")
    pending = [e for _, e in sorted(entries.items())
               if e["status"] == "pending-manual"]
    if pending:
        print("\npending-manual:")
        for e in pending:
            print(f"  {e['domain']}|{e['framework_slug']}|{e['control_code']}"
                  f"|{e['quote_sha256'][:12]}  [{e['note']}]  {e['source_url']}")
    return counts["mismatch"]


# --- CLI ---------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Verbatim-fidelity quote ledger: verify that every "
                    "verbatim/verbatim-elided evidence quote appears in its "
                    "cited source, and record the result in meta/quote-ledger.json.")
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch all entries (human verifications preserved)")
    ap.add_argument("--only-pending", action="store_true",
                    help="re-fetch only pending-manual entries")
    ap.add_argument("--report", action="store_true",
                    help="print a summary from the ledger; no network")
    ap.add_argument("--mark-verified", metavar="KEY",
                    help="record a human verification for KEY (sha256 or "
                         "key-string prefix); requires --method and --note")
    ap.add_argument("--mark-mismatch", metavar="KEY",
                    help="record a human-adjudicated mismatch for KEY; "
                         "requires --method and --note saying how it differs")
    ap.add_argument("--mark-pending", metavar="KEY",
                    help="keep KEY pending-manual but record a precise --note "
                         "on why it could not be verified")
    ap.add_argument("--method", choices=("manual", "fetched-pdf"),
                    help="verification method for --mark-verified")
    ap.add_argument("--note", default="",
                    help="verification note for --mark-verified "
                         "(e.g. the PDF page checked)")
    ap.add_argument("--ledger", default=LEDGER_PATH, help=argparse.SUPPRESS)
    ap.add_argument("--timeout", type=float, default=FETCH_TIMEOUT,
                    help=f"per-request timeout in seconds (default {FETCH_TIMEOUT})")
    args = ap.parse_args(argv)

    rows = load_rows()
    entries = sync_entries(rows, load_ledger(args.ledger))

    if args.report:
        print_report(entries)
        return 0

    if args.mark_verified:
        key = mark_verified(entries, args.mark_verified,
                            args.method or "manual", args.note)
        write_ledger(entries, args.ledger)
        print(f"marked verified ({entries[key]['method']}): {key_str(key)}")
        return 0

    if args.mark_mismatch:
        key = mark_mismatch(entries, args.mark_mismatch,
                            args.method or "manual", args.note)
        write_ledger(entries, args.ledger)
        print(f"marked mismatch ({entries[key]['method']}): {key_str(key)}")
        return 0

    if args.mark_pending:
        key = mark_pending(entries, args.mark_pending, args.note)
        write_ledger(entries, args.ledger)
        print(f"marked pending-manual: {key_str(key)}")
        return 0

    mode = "all" if args.refresh else ("pending" if args.only_pending else "new")
    keys = select_for_fetch(entries, rows, mode)
    print(f"verify_quotes: {len(rows)} in-scope rows, fetching {len(keys)} "
          f"entries across {len({entries[k]['source_url'] for k in keys})} URLs "
          f"(mode: {mode})")
    fetcher = PoliteFetcher(timeout=args.timeout)

    def progress(key, e):
        print(f"  {e['status']:<15} {key[0]}|{key[1]}|{key[2]}"
              f"{('  [' + e['note'] + ']') if e['note'] else ''}")

    run_fetch_pass(entries, rows, keys, fetcher, progress=progress)
    write_ledger(entries, args.ledger)
    print()
    mismatches = print_report(entries)
    print(f"\nledger written: {args.ledger}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())

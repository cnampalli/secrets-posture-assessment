"""F-04 offline quote-ledger gate: unit tests (fixture ledger, zero network).

The gate must (a) fail-closed without tool/ledger, (b) detect silent quote edits
via the hash-in-key, (c) fail ledger-recorded mismatches, (d) fail stale
verifications, (e) pass honest pending-manual entries.
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "matrix"))

import validate_data as vd  # noqa: E402

_VQ = vd._load_verify_quotes(str(ROOT))
QUOTE = "Access to information assets must be restricted."
SHA = _VQ.quote_sha256(QUOTE)


def _row(quote=QUOTE, qtype="verbatim"):
    return {"framework_slug": "apra-cps-234", "control_code": "CPS234-§X",
            "citation_keys": "k1", "quote_type": qtype, "evidence_quote": quote}


def _repo(tmp_path, entry):
    """Minimal fake repo root: the real verify_quotes tool + a fixture ledger."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "verify_quotes.py", tmp_path / "scripts")
    # verify_quotes imports check_links from <root>/matrix
    (tmp_path / "matrix").mkdir()
    shutil.copy(ROOT / "matrix" / "check_links.py", tmp_path / "matrix")
    (tmp_path / "meta").mkdir()
    base = {"domain": "pam", "framework_slug": "apra-cps-234",
            "control_code": "CPS234-§X", "citation_key": "k1",
            "quote_sha256": SHA, "source_url": "https://x", "status": "verified",
            "method": "fetched", "verified_on": "2026-07-01", "note": ""}
    base.update(entry)
    (tmp_path / "meta" / "quote-ledger.json").write_text(
        json.dumps({"schema_version": 1, "generated_on": "2026-07-01",
                    "entries": [base]}), encoding="utf-8")
    return str(tmp_path)


def test_fail_closed_without_ledger(tmp_path):
    (tmp_path / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "verify_quotes.py", tmp_path / "scripts")
    (tmp_path / "matrix").mkdir()
    shutil.copy(ROOT / "matrix" / "check_links.py", tmp_path / "matrix")
    errs = vd.check_quote_ledger(str(tmp_path), "pam", [_row()], today="2026-07-03")
    assert len(errs) == 1 and "quote-ledger.json: missing" in errs[0]


def test_fail_closed_without_tool(tmp_path):
    errs = vd.check_quote_ledger(str(tmp_path), "pam", [_row()], today="2026-07-03")
    assert len(errs) == 1 and "verify_quotes.py: missing" in errs[0]


def test_verified_entry_passes(tmp_path):
    root = _repo(tmp_path, {})
    assert vd.check_quote_ledger(root, "pam", [_row()], today="2026-07-03") == []


def test_silently_edited_quote_reads_as_missing(tmp_path):
    root = _repo(tmp_path, {})
    edited = _row(quote=QUOTE.replace("restricted", "unrestricted"))
    errs = vd.check_quote_ledger(root, "pam", [edited], today="2026-07-03")
    assert len(errs) == 1 and "no quote-ledger entry" in errs[0]


def test_mismatch_status_fails(tmp_path):
    root = _repo(tmp_path, {"status": "mismatch", "note": "paraphrase-mislabelled"})
    errs = vd.check_quote_ledger(root, "pam", [_row()], today="2026-07-03")
    assert len(errs) == 1 and "MISMATCH" in errs[0] and "paraphrase-mislabelled" in errs[0]


def test_stale_verification_fails(tmp_path):
    root = _repo(tmp_path, {"verified_on": "2025-06-01"})
    errs = vd.check_quote_ledger(root, "pam", [_row()], today="2026-07-03")
    assert len(errs) == 1 and "stale" in errs[0]


def test_pending_manual_passes_hash_still_pinned(tmp_path):
    root = _repo(tmp_path, {"status": "pending-manual", "method": None,
                            "verified_on": None})
    assert vd.check_quote_ledger(root, "pam", [_row()], today="2026-07-03") == []
    # ...but an edit under pending-manual is still caught by the hash pin
    edited = _row(quote=QUOTE + " Extra invented clause.")
    errs = vd.check_quote_ledger(root, "pam", [edited], today="2026-07-03")
    assert len(errs) == 1 and "no quote-ledger entry" in errs[0]


def test_non_verbatim_rows_out_of_scope(tmp_path):
    root = _repo(tmp_path, {"status": "mismatch"})
    assert vd.check_quote_ledger(root, "pam", [_row(qtype="paraphrase")],
                                 today="2026-07-03") == []


def test_unknown_status_fails(tmp_path):
    root = _repo(tmp_path, {"status": "probably-fine"})
    errs = vd.check_quote_ledger(root, "pam", [_row()], today="2026-07-03")
    assert len(errs) == 1 and "unknown ledger status" in errs[0]

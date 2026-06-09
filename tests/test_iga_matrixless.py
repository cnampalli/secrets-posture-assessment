"""Regression-safety guards for the matrix-less IGA domain (Phase 3 gate).

Two distinct guards are exercised here:

  1. report_io: a *header-only* vendor-capabilities.csv is the deliberate signal
     that a domain doesn't use the NATIVE/ADD-ON capability matrix (IGA → bespoke
     per-area vendor-fit). load_inputs must NOT sys.exit on it — it just yields an
     empty `ranked`. A truly-empty (0-byte) or missing matrix for a matrix-USING
     domain (secrets/PAM) is still fatal (sys.exit) — the no-rows guard must not be
     weakened.
  2. build_cross_domain: the corporate-parent concentration map skips the
     matrix-less IGA domain (no ranked vendors) and includes secrets + pam.
"""
import csv

import pytest

import report_io
import build_cross_domain
import domains


def _write_header_only(here, name, header):
    with open(here / name, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(header)


# ---- report_io._has_header / load_inputs header-only branch ----

def test_header_only_matrix_does_not_exit_and_yields_empty_ranked(tmp_path):
    # A header-only vendor-capabilities.csv (zero data rows) is the matrix-less
    # signal: load_inputs must return without exiting and with no ranked vendors.
    _write_header_only(tmp_path, domains.PAM.vendor_capabilities,
                       ["vendor_slug", "vendor_name", "target_id", "target_type",
                        "coverage", "maturity", "evidence_url", "evidence_quote",
                        "citation_keys", "notes"])
    inp = report_io.load_inputs(str(tmp_path), None, domains.PAM)
    assert inp["ranked"] == []
    assert inp["all_rows"] == []


def test_has_header_distinguishes_header_only_from_missing_and_empty(tmp_path):
    # header-only → True; missing → False; truly-empty (0-byte) → False.
    _write_header_only(tmp_path, "header-only.csv", ["a", "b"])
    (tmp_path / "empty.csv").write_text("", encoding="utf-8")
    assert report_io._has_header(str(tmp_path), "header-only.csv") is True
    assert report_io._has_header(str(tmp_path), "missing.csv") is False
    assert report_io._has_header(str(tmp_path), "empty.csv") is False


def test_missing_matrix_for_matrix_using_domain_still_exits(tmp_path):
    # No vendor-capabilities.csv at all for a matrix-using domain (PAM) is fatal.
    with pytest.raises(SystemExit):
        report_io.load_inputs(str(tmp_path), None, domains.PAM)


def test_truly_empty_matrix_for_matrix_using_domain_still_exits(tmp_path):
    # A 0-byte vendor-capabilities.csv (no header, no rows) is fatal for a
    # matrix-using domain — the no-rows guard must not be weakened.
    (tmp_path / domains.PAM.vendor_capabilities).write_text("", encoding="utf-8")
    with pytest.raises(SystemExit):
        report_io.load_inputs(str(tmp_path), None, domains.PAM)


# ---- build_cross_domain skips the matrix-less IGA domain ----

def test_cross_build_skips_iga_and_includes_secrets_and_pam():
    model, _dst = build_cross_domain.build()
    slugs = {d["slug"] for d in model["domains"]}
    assert {"secrets", "pam"} <= slugs   # matrix-using domains participate
    assert "iga" not in slugs            # matrix-less IGA is excluded, no crash

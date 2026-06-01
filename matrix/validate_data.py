#!/usr/bin/env python3
"""Read-only CSV schema + referential-integrity validator for the matrix data contracts.

Pure check functions return lists of violation strings (empty = clean); validate_all
aggregates; the CLI exits 1 on any violation. Mirrors methodology/validate_rubric.py.
Read-only — never mutates data.

CLI: python3 matrix/validate_data.py [--root .]
"""
import argparse
import csv
import glob
import os
import sys

CORE_REQUIRED = {
    "use-cases.csv": ("uc_id", "category", "short_title", "story", "acceptance_criteria",
                      "nhis_in_scope", "outcome_lens", "backmap_codes", "priority_fi", "citation_keys"),
    "anz-current-state.csv": ("uc_id", "anz_state", "confidence", "evidence_q_ids",
                              "evidence_redacted", "gap_notes", "sensitivity_tag", "citation_keys"),
    "regulatory-trace.csv": ("framework_slug", "framework_role", "control_code", "control_short_title",
                             "uc_ids", "nhi_ids", "maturity_level", "evidence_url", "evidence_quote",
                             "citation_keys"),
    "identity-catalog.csv": ("nhi_id", "bucket", "short_name", "description", "typical_secrets",
                             "lifecycle", "governance_maturity", "sources_at_anz_likely", "citation_keys"),
}
VENDOR_REQUIRED = ("vendor_slug", "vendor_name", "target_id", "target_type", "coverage",
                   "maturity", "evidence_url", "evidence_quote", "citation_keys", "notes")
VALID_STATES = {"MET", "PARTIAL", "GAP", "PENDING", "NA"}
VALID_ROLES = {"PRIMARY-LENS", "BACK-MAP", "ADVERSARY-LENS"}
SENTINELS = {"MISSING-UC", "MISSING-NHI"}


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ids(value):
    """Split a ;-list, dropping blanks and intentional sentinels."""
    return [t.strip() for t in (value or "").split(";")
            if t.strip() and t.strip() not in SENTINELS]


def check_required_columns(name, rows, required):
    if not rows:
        return [f"{name}: empty (no data rows)"]
    have = set(rows[0].keys())
    return [f"{name}: missing required column '{c}'" for c in required if c not in have]


def check_unique(name, rows, key):
    seen, errs = set(), []
    for r in rows:
        v = r.get(key, "")
        if v in seen:
            errs.append(f"{name}: duplicate {key} '{v}'")
        seen.add(v)
    return errs


def check_enum(name, rows, col, allowed):
    errs = []
    for r in rows:
        v = (r.get(col) or "").strip()
        if v and v not in allowed:
            errs.append(f"{name}: invalid {col} '{v}'")
    return errs

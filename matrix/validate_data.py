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


def validate_vendor_rows(name, rows, single_slug=False):
    """Per-vendor / aggregate row checks: required cols, maturity 0-5, non-empty coverage,
    and (per-vendor only) a single consistent vendor_slug."""
    errs = check_required_columns(name, rows, VENDOR_REQUIRED)
    if errs:
        return errs   # missing columns -> key access below is unsafe
    slugs = set()
    for r in rows:
        tid = r.get("target_id", "?")
        m = (r.get("maturity") or "").strip()
        if not (m.isdigit() and 0 <= int(m) <= 5):
            errs.append(f"{name}: maturity '{m}' not integer 0-5 (target {tid})")
        if not (r.get("coverage") or "").strip():
            errs.append(f"{name}: empty coverage (target {tid})")
        slugs.add((r.get("vendor_slug") or "").strip())
    if single_slug and len(slugs) > 1:
        errs.append(f"{name}: multiple vendor_slug values {sorted(slugs)} in one per-vendor file")
    return errs


def validate_referential(use_cases, current_state, reg_trace, identity, vendor_files):
    """Cross-file integrity: uc_id / nhi_id references resolve (sentinels skipped)."""
    errs = []
    uc_ids = {r.get("uc_id", "") for r in use_cases}
    nhi_ids = {r.get("nhi_id", "") for r in identity}
    cs_ids = {r.get("uc_id", "") for r in current_state}
    for i in sorted(cs_ids - uc_ids):
        errs.append(f"anz-current-state.csv: uc_id '{i}' not in use-cases")
    for i in sorted(uc_ids - cs_ids):
        errs.append(f"anz-current-state.csv: missing uc_id '{i}' present in use-cases")
    for r in reg_trace:
        cc = r.get("control_code", "?")
        for u in _ids(r.get("uc_ids")):
            if u not in uc_ids:
                errs.append(f"regulatory-trace.csv: uc_id '{u}' (control {cc}) not in use-cases")
        for n in _ids(r.get("nhi_ids")):
            if n not in nhi_ids:
                errs.append(f"regulatory-trace.csv: nhi_id '{n}' (control {cc}) not in identity-catalog")
    for r in use_cases:
        for n in _ids(r.get("nhis_in_scope")):
            if n not in nhi_ids:
                errs.append(f"use-cases.csv: nhis_in_scope '{n}' (uc {r.get('uc_id')}) not in identity-catalog")
    for name, rows in vendor_files:
        for r in rows:
            tt = (r.get("target_type") or "").strip()
            tid = (r.get("target_id") or "").strip()
            if tt == "NHI" and tid not in nhi_ids:
                errs.append(f"{name}: target_id '{tid}' (NHI) not in identity-catalog")
            elif tt.startswith("UC") and tid not in uc_ids:
                errs.append(f"{name}: target_id '{tid}' (UC) not in use-cases")
    return errs


def validate_all(root="."):
    """Run all checks against the matrix data under <root>/matrix; return all violations."""
    m = os.path.join(root, "matrix")
    use_cases = load_csv(os.path.join(m, "use-cases.csv"))
    current = load_csv(os.path.join(m, "anz-current-state.csv"))
    trace = load_csv(os.path.join(m, "regulatory-trace.csv"))
    identity = load_csv(os.path.join(m, "identity-catalog.csv"))

    errs = []
    errs += check_required_columns("use-cases.csv", use_cases, CORE_REQUIRED["use-cases.csv"])
    errs += check_unique("use-cases.csv", use_cases, "uc_id")
    errs += check_required_columns("anz-current-state.csv", current, CORE_REQUIRED["anz-current-state.csv"])
    errs += check_unique("anz-current-state.csv", current, "uc_id")
    errs += check_enum("anz-current-state.csv", current, "anz_state", VALID_STATES)
    errs += check_required_columns("regulatory-trace.csv", trace, CORE_REQUIRED["regulatory-trace.csv"])
    errs += check_enum("regulatory-trace.csv", trace, "framework_role", VALID_ROLES)
    errs += check_required_columns("identity-catalog.csv", identity, CORE_REQUIRED["identity-catalog.csv"])
    errs += check_unique("identity-catalog.csv", identity, "nhi_id")

    vendor_files = []
    agg_rows = load_csv(os.path.join(m, "vendor-capabilities.csv"))
    vendor_files.append(("vendor-capabilities.csv", agg_rows))
    errs += validate_vendor_rows("vendor-capabilities.csv", agg_rows)
    for p in sorted(glob.glob(os.path.join(m, "vendor-capabilities-*.csv"))):
        name = os.path.basename(p)
        rows = load_csv(p)
        vendor_files.append((name, rows))
        errs += validate_vendor_rows(name, rows, single_slug=True)

    errs += validate_referential(use_cases, current, trace, identity, vendor_files)
    return errs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate the matrix CSV data contracts.")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args(argv)
    violations = validate_all(args.root)
    for v in violations:
        print(v)
    if violations:
        print(f"\n{len(violations)} violation(s) found.")
        return 1
    print("All CSV data contracts valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

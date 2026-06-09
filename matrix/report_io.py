"""Report input loading: CSVs + config-driven residency/label loads.

The I/O layer of the report build. Reads a domain's catalog CSVs into the plain
structures the logic layer consumes. Vendor classification maps + filenames live
in the per-domain descriptor (domains.py) — access them via the Domain, e.g.
domains.SECRETS.vendor_layer.
"""
import csv
import os
import sys

import overlay as _ov
from domains import SECRETS


def read_csv(here, name):
    path = os.path.join(here, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _has_header(here, name):
    """True iff <here>/<name> exists and carries a non-empty header line — i.e. a
    deliberately *header-only* CSV (zero data rows) is distinguishable from a
    missing/truly-empty file. Used to recognise a matrix-less domain (IGA ships a
    header-only vendor-capabilities.csv on purpose) without weakening the
    no-rows guard for domains that genuinely depend on the matrix."""
    path = os.path.join(here, name)
    if not os.path.exists(path):
        return False
    with open(path, newline="", encoding="utf-8") as fh:
        return any(h.strip() for h in (next(csv.reader(fh), []) or []))


def load_vendor_residency(cfgdir):
    return _ov.load_vendor_residency(os.path.join(cfgdir, "vendor-residency.yaml"))


def load_framework_labels(cfgdir):
    return _ov.load_framework_labels(os.path.join(cfgdir, "frameworks.yaml"))


def load_vendor_ownership(cfgdir):
    return _ov.load_vendor_ownership(os.path.join(cfgdir, "vendor-ownership.yaml"))


def load_inputs(here, current_state_name=None, domain=SECRETS):
    """Load a domain's report inputs from <here>/*.csv. Returns a dict with
    all_rows, ranked, ucs, nhis, anz, reg_rows.

    Filenames + the vendor layer/substrate maps come from `domain` (defaults to
    the secrets domain). `here` is the data directory; `current_state_name`
    defaults to the domain's default current-state file."""
    current_state_name = current_state_name or domain.default_current_state
    all_rows = read_csv(here, domain.vendor_capabilities)
    if not all_rows and not _has_header(here, domain.vendor_capabilities):
        # Missing / truly-empty matrix for a matrix-using domain (secrets/PAM) is fatal.
        # A *header-only* matrix is the deliberate signal that this domain doesn't use
        # the NATIVE/ADD-ON capability matrix (IGA → bespoke per-area vendor-fit): it
        # simply has no ranked vendors, which must NOT be a fatal error.
        sys.exit(f"No rows in {domain.vendor_capabilities}")
    unmapped = sorted({r["vendor_slug"] for r in all_rows if r["vendor_slug"] not in domain.vendor_layer})
    if unmapped:
        sys.exit(f"Unmapped vendor_slug(s): {unmapped}")

    ranked = []
    for r in all_rows:
        if r["vendor_slug"] == domain.substrate_slug:
            continue
        lay, tier = domain.vendor_layer[r["vendor_slug"]]
        ranked.append({
            "vendor_slug": r["vendor_slug"], "vendor_name": r["vendor_name"],
            "target_id": r["target_id"], "target_type": r["target_type"],
            "coverage": r["coverage"], "maturity": r["maturity"],
            "evidence_url": r.get("evidence_url", ""), "evidence_quote": r.get("evidence_quote", ""),
            "citation_keys": r.get("citation_keys", ""), "notes": r.get("notes", ""),
            "layer": lay, "tier": tier,
        })

    ucs = [{"uc_id": r["uc_id"], "category": r.get("category", ""), "short_title": r.get("short_title", ""),
            "story": r.get("story", ""), "outcome_lens": r.get("outcome_lens", ""),
            "backmap_codes": r.get("backmap_codes", ""), "nhis_in_scope": r.get("nhis_in_scope", ""),
            "priority_fi": r.get("priority_fi", "")} for r in read_csv(here, domain.use_cases)]

    nhis = [{"nhi_id": r["nhi_id"], "bucket": r.get("bucket", ""), "short_name": r.get("short_name", ""),
             "description": r.get("description", "")} for r in read_csv(here, domain.identity_catalog)]

    anz = [{"uc_id": r["uc_id"], "current_state": r.get("current_state", ""), "confidence": r.get("confidence", ""),
            "evidence": r.get("evidence_redacted", ""), "recommendation": r.get("gap_notes", ""),
            "sensitivity": r.get("sensitivity_tag", "")} for r in read_csv(here, current_state_name)]

    reg_rows = read_csv(here, domain.regulatory_trace)
    evidence_catalog = read_csv(here, "evidence-catalog.csv")   # optional per domain (secrets ships none)

    return {"all_rows": all_rows, "ranked": ranked, "ucs": ucs, "nhis": nhis,
            "anz": anz, "reg_rows": reg_rows, "evidence_catalog": evidence_catalog}

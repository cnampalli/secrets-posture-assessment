"""Report input loading: CSVs + static vendor maps + config-driven labels.

The I/O layer of the report build. Reads the matrix/catalog CSVs into the plain
structures the logic layer consumes, and owns the static vendor classification
maps + the config-driven residency/label loads.
"""
import csv
import os
import sys

import overlay as _ov

SUBSTRATE_SLUG = "fortanix-dsm"

VENDOR_LAYER = {
    SUBSTRATE_SLUG: ("L0", "data-security"),
    "hashicorp-vault-enterprise": ("L1", "core"),
    "cyberark-conjur": ("L1", "core"),
    "cyberark-pam": ("L1", "core"),
    "delinea-secret-server": ("L1", "core"),
    "aws-secrets-manager": ("L1", "cloud-native"),
    "azure-key-vault": ("L1", "cloud-native"),
    "gcp-secret-manager": ("L1", "cloud-native"),
    "akeyless": ("L1", "cloud-native"),
    "doppler": ("L1", "emerging"),
    "infisical": ("L1", "emerging"),
    "1password-secrets-automation": ("L1", "emerging"),
    "venafi": ("L1", "pki-mim"),
    "keyfactor": ("L1", "pki-mim"),
    "astrix-security": ("L2", "nhi-discovery"),
    "entro-security": ("L2", "nhi-discovery"),
    "oasis-security": ("L2", "nhi-discovery"),
    "aembit": ("L2", "nhi-discovery"),
    "clutch-security": ("L2", "nhi-discovery"),
}
SHORT = {
    "hashicorp-vault-enterprise": "Vault Ent", "cyberark-conjur": "Conjur",
    "cyberark-pam": "CyberArk PAM", "delinea-secret-server": "Delinea",
    "aws-secrets-manager": "AWS SM", "azure-key-vault": "Azure KV",
    "gcp-secret-manager": "GCP SM", "akeyless": "AKEYLESS", "doppler": "Doppler",
    "infisical": "Infisical", "1password-secrets-automation": "1Password",
    "venafi": "Venafi", "keyfactor": "Keyfactor", "astrix-security": "Astrix",
    "entro-security": "Entro", "oasis-security": "Oasis", "aembit": "Aembit",
    "clutch-security": "Clutch",
}
LAYER_LABEL = {
    "L1": "L1 · Secrets management (the vault tier) — NATIVE = brokers / stores / rotates secrets",
    "L2": "L2 · NHI discovery / governance (above the vault) — NATIVE = discovers / governs (not brokers)",
}


def read_csv(here, name):
    path = os.path.join(here, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_vendor_residency(cfgdir):
    return _ov.load_vendor_residency(os.path.join(cfgdir, "vendor-residency.yaml"))


def load_framework_labels(cfgdir):
    return _ov.load_framework_labels(os.path.join(cfgdir, "frameworks.yaml"))


def load_inputs(here, current_state_name):
    """Load the report inputs from <here>/*.csv. Returns a dict with
    all_rows, ranked, ucs, nhis, anz, reg_rows."""
    all_rows = read_csv(here, "vendor-capabilities.csv")
    if not all_rows:
        sys.exit("No rows in vendor-capabilities.csv")
    unmapped = sorted({r["vendor_slug"] for r in all_rows if r["vendor_slug"] not in VENDOR_LAYER})
    if unmapped:
        sys.exit(f"Unmapped vendor_slug(s): {unmapped}")

    ranked = []
    for r in all_rows:
        if r["vendor_slug"] == SUBSTRATE_SLUG:
            continue
        lay, tier = VENDOR_LAYER[r["vendor_slug"]]
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
            "priority_fi": r.get("priority_fi", "")} for r in read_csv(here, "use-cases.csv")]

    nhis = [{"nhi_id": r["nhi_id"], "bucket": r.get("bucket", ""), "short_name": r.get("short_name", ""),
             "description": r.get("description", "")} for r in read_csv(here, "identity-catalog.csv")]

    anz = [{"uc_id": r["uc_id"], "current_state": r.get("current_state", ""), "confidence": r.get("confidence", ""),
            "evidence": r.get("evidence_redacted", ""), "recommendation": r.get("gap_notes", ""),
            "sensitivity": r.get("sensitivity_tag", "")} for r in read_csv(here, current_state_name)]

    reg_rows = read_csv(here, "regulatory-trace.csv")

    return {"all_rows": all_rows, "ranked": ranked, "ucs": ucs, "nhis": nhis,
            "anz": anz, "reg_rows": reg_rows}

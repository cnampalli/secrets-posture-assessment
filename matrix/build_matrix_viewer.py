#!/usr/bin/env python3
"""Build the self-contained XYZ Secrets-Management stakeholder report.

Reads the matrix + catalog CSVs and writes matrix-viewer.html — a single
offline HTML file (no server, no internet) with four views:

  1. XYZ posture dashboard (landing) — MET/PARTIAL/GAP/PENDING, clickable
     top gaps, and a stakeholder "mark as MET" override (persists locally).
  2. By Use Case — decision card: a one-line recommendation, a vendor-as-
     columns coverage/maturity grid (by layer), the mapped APRA CPS 234 +
     ASD ISM controls, and XYZ current state (with a MET override).
  3. By Identity (NHI) — vendor-as-columns coverage/maturity grid.
  4. Browse all — the full filterable capability table.

Per ADR-007, Fortanix DSM is a Layer-0 crypto-substrate DEPENDENCY and is
EXCLUDED from all ranked views (→ 18 ranked vendors). The source CSV is
never modified. The HTML is built from a raw template with /*__TOKEN__*/
placeholders (not an f-string) so braces in CSS/JS need no escaping.
"""
import csv
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "matrix-viewer.html")
SUBSTRATE_SLUG = "fortanix-dsm"

import argparse
import engagement_config as _ec
import overlay as _ov
import report_render

_CFGDIR = os.path.join(HERE, "config")

_ap = argparse.ArgumentParser(description="Build the secrets-management report.")
_ap.add_argument("--config", help="path to an engagement.yaml")
_ap.add_argument("--preset", help="named preset (financial|government|retail|baseline)")
_ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides primary)")
_ap.add_argument("--emit-data", help="(test hook) also dump {REGDATA,RECDATA} JSON to this path")
_ap.add_argument("--current-state", default="current-state.csv",
                 help="current-state CSV the report scores against (a questionnaire export via "
                      "questionnaire/report_adapter.py). Default keeps existing behaviour.")
_ARGS, _ = _ap.parse_known_args()

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
APRA_FRAMEWORKS = {"apra-cps-234", "apra-cps-230", "apra-cpg-234"}

# AU data-residency / IRAP per vendor — externalized to config/vendor-residency.yaml (WS-2).
VENDOR_RESIDENCY = _ov.load_vendor_residency(os.path.join(_CFGDIR, "vendor-residency.yaml"))

# UC capability domains (from use-cases.csv) used to score domain strength.
REC_UC_DOMAIN = {
    "secrets": ["UC-F-001", "UC-F-002", "UC-F-003", "UC-F-005", "UC-F-006", "UC-F-007",
                "UC-F-008", "UC-F-010", "UC-F-012", "UC-F-015", "UC-F-016", "UC-F-018",
                "UC-F-020", "UC-F-026", "UC-N-003"],
    "governance": ["UC-F-017", "UC-F-025", "UC-F-027", "UC-N-002", "UC-N-004", "UC-N-006",
                   "UC-N-009", "UC-N-010", "UC-N-016", "UC-N-017", "UC-N-018", "UC-N-020"],
}


def read_csv(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


all_rows = read_csv("vendor-capabilities.csv")
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
        "priority_fi": r.get("priority_fi", "")} for r in read_csv("use-cases.csv")]

nhis = [{"nhi_id": r["nhi_id"], "bucket": r.get("bucket", ""), "short_name": r.get("short_name", ""),
         "description": r.get("description", "")} for r in read_csv("identity-catalog.csv")]

anz = [{"uc_id": r["uc_id"], "current_state": r.get("current_state", ""), "confidence": r.get("confidence", ""),
        "evidence": r.get("evidence_redacted", ""), "recommendation": r.get("gap_notes", ""),
        "sensitivity": r.get("sensitivity_tag", "")} for r in read_csv(_ARGS.current_state)]

# Regulatory data (read once): per-UC APRA/ISM chips + the full
# Framework -> Control -> UC -> Vendor-evidence cascade (Compliance-trace tab).
reg_rows = read_csv("regulatory-trace.csv")

reg = defaultdict(lambda: {"APRA": set(), "ISM": set()})
for r in reg_rows:
    fs = r.get("framework_slug", "")
    bucket = "APRA" if fs in APRA_FRAMEWORKS else ("ISM" if fs == "asd-ism" else None)
    if not bucket:
        continue
    for u in (r.get("uc_ids", "") or "").split(";"):
        u = u.strip()
        if u.startswith("UC-"):
            reg[u][bucket].add(r["control_code"])
REG = {u: {"APRA": sorted(v["APRA"]), "ISM": sorted(v["ISM"])} for u, v in reg.items()}

# Framework labels — externalized to config/frameworks.yaml (WS-2).
FRAMEWORK_LABELS = _ov.load_framework_labels(os.path.join(_CFGDIR, "frameworks.yaml"))
fw_order, fw_seen = [], set()
for r in reg_rows:
    if r["framework_slug"] not in fw_seen:
        fw_seen.add(r["framework_slug"]); fw_order.append(r["framework_slug"])
_available = list(dict.fromkeys(fw_order))     # the framework slugs present in the data
_cli_fw = [s.strip() for s in _ARGS.frameworks.split(",")] if _ARGS.frameworks else None
import pathlib as _pl
ENGAGEMENT = _ec.resolve(
    preset=_ARGS.preset,
    config_path=_ARGS.config,
    cli_frameworks=_cli_fw,
    available=_available,
    presets_dir=_pl.Path(_CFGDIR) / "presets",
)
fw_order = _ov.scope_frameworks(fw_order, ENGAGEMENT)
state_by_uc = {a["uc_id"]: a["current_state"] for a in anz}
framework_controls = defaultdict(list)
for r in reg_rows:
    framework_controls[r["framework_slug"]].append({
        "code": r["control_code"], "title": r.get("control_short_title", ""),
        "maturity_level": r.get("maturity_level", ""),
        "uc_ids": [u for u in r.get("uc_ids", "").split(";") if u],
        "evidence_url": r.get("evidence_url", ""),
        "evidence_quote": (r.get("evidence_quote") or "")[:300],
    })
STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "MET": 3, "UNKNOWN": 9}
for fw, controls in framework_controls.items():
    for c in controls:
        states = [state_by_uc.get(u, "UNKNOWN") for u in c["uc_ids"]]
        c["current_state"] = min(states, key=lambda s: STATE_RANK.get(s, 9)) if states else "UNKNOWN"
# Vendor evidence per UC (ranked rows only — Fortanix excluded per ADR-007)
ORDER = {"NATIVE": 0, "ADD-ON": 1, "PARTNER": 2, "GAP": 3, "N/A": 4}
vendor_uc = defaultdict(list)
for r in ranked:
    if r["target_type"] not in ("UC-F", "UC-N"):
        continue
    vendor_uc[r["target_id"]].append({
        "vendor_name": r["vendor_name"], "coverage": r["coverage"],
        "maturity": int(r["maturity"]) if str(r["maturity"]).isdigit() else 0,
        "quote": (r.get("evidence_quote") or "")[:200],
    })
for k in vendor_uc:
    vendor_uc[k].sort(key=lambda x: (ORDER.get(x["coverage"], 9), -x["maturity"]))
uc_index = {u["uc_id"]: {"title": u["short_title"], "priority": u["priority_fi"],
                         "state": state_by_uc.get(u["uc_id"], "UNKNOWN"),
                         "nhi_count": len([n for n in u["nhis_in_scope"].split(";") if n])} for u in ucs}
REGDATA = {
    "frameworks": [{"slug": s, "label": FRAMEWORK_LABELS.get(s, (s, ""))[0],
                    "subtitle": FRAMEWORK_LABELS.get(s, (s, ""))[1],
                    "control_count": len(framework_controls[s])} for s in fw_order],
    "controls": framework_controls, "ucs": uc_index, "vendor_uc": dict(vendor_uc),
    "framework_selection": {
        "selected": list(ENGAGEMENT.selected) if not ENGAGEMENT.is_default else list(_available),
        "overlays": list(ENGAGEMENT.overlays),
        "baseline": list(ENGAGEMENT.baseline) if not ENGAGEMENT.is_default else [],
        "available": list(_available),
    },
}


def build_glossary():
    g = {}
    for r in nhis:
        desc = (r["description"] or "").strip()
        if len(desc) > 170:
            desc = desc[:167].rstrip() + "..."
        g[r["nhi_id"]] = (r["short_name"] + " — " + desc) if desc else r["short_name"]
    for r in ucs:
        g[r["uc_id"]] = r["short_title"]
    g.update({
        "NATIVE": "Vendor's first-class, documented capability (meaning is layer-relative).",
        "ADD-ON": "Supported via a paid add-on / separate module.",
        "PARTNER": "Delivered via a partner / third-party integration.",
        "GAP": "Not addressed by the vendor.", "N/A": "Not applicable to this identity bucket.",
        "0": "Maturity 0 — none / not announced.", "1": "Maturity 1 — announced / preview.",
        "2": "Maturity 2 — GA basic.", "3": "Maturity 3 — GA mature, reference customers.",
        "4": "Maturity 4 — industry-leading.",
    })
    return g


GLOSSARY = build_glossary()
meta = {"ranked_vendors": len({r["vendor_slug"] for r in ranked}), "ranked_rows": len(ranked),
        "total_rows": len(all_rows), "nhis": len(nhis), "ucs": len(ucs)}

# ---- Recommendations tab (residency-first, layer-scoped per ADR-007) ----
_SECRETS_UCS = set(REC_UC_DOMAIN["secrets"])
_GOV_UCS = set(REC_UC_DOMAIN["governance"])


def _vendor_stat(slug):
    rows = [r for r in ranked if r["vendor_slug"] == slug]

    def dom(ucset):
        sel = [r for r in rows if r["target_type"] in ("UC-F", "UC-N") and r["target_id"] in ucset]
        nat = [r for r in sel if r["coverage"] == "NATIVE"]
        mats = [int(r["maturity"]) for r in nat if str(r["maturity"]).isdigit()]
        return len(nat), len(sel), (round(sum(mats) / len(mats), 1) if mats else 0)

    s_nat, s_tot, s_mat = dom(_SECRETS_UCS)
    g_nat, g_tot, g_mat = dom(_GOV_UCS)
    nhi = [r for r in rows if r["target_type"] == "NHI"]
    res = VENDOR_RESIDENCY.get(slug, {})
    return {
        "slug": slug, "name": SHORT.get(slug, slug), "tier": VENDOR_LAYER[slug][1],
        "secrets_native": s_nat, "secrets_total": s_tot, "secrets_mat": s_mat,
        "gov_native": g_nat, "gov_total": g_tot, "gov_mat": g_mat,
        "nhi_native": sum(1 for r in nhi if r["coverage"] == "NATIVE"),
        "nhi_gap": sum(1 for r in nhi if r["coverage"] == "GAP"),
        "residency": res.get("residency", "?"), "irap": res.get("irap", "?"),
        "res_note": res.get("note", ""),
    }


_l1 = [s for s, (lay, t) in VENDOR_LAYER.items() if lay == "L1" and t != "pki-mim"]
_pki = [s for s, (lay, t) in VENDOR_LAYER.items() if lay == "L1" and t == "pki-mim"]
_l2 = [s for s, (lay, t) in VENDOR_LAYER.items() if lay == "L2"]

l1_secrets = sorted((_vendor_stat(s) for s in _l1),
                    key=lambda v: _ov.vendor_sort_key(
                        ENGAGEMENT.residency_weight, v["residency"],
                        (-v["secrets_native"], -v["nhi_native"])))
pki_mim = sorted((_vendor_stat(s) for s in _pki),
                 key=lambda v: _ov.vendor_sort_key(
                     ENGAGEMENT.residency_weight, v["residency"],
                     (-v["secrets_native"],)))
l2_governance = sorted((_vendor_stat(s) for s in _l2),
                       key=lambda v: _ov.vendor_sort_key(
                           ENGAGEMENT.residency_weight, v["residency"],
                           (-v["gov_native"], -v["nhi_native"])))

# Most compliance-defensible primary = AU-resident AND IRAP-assessed (by coverage);
# highest-capability multi-cloud alternative = Vault.
_primary = _ov.select_primary(l1_secrets, ENGAGEMENT.irap_required)
_multicloud = next((v for v in l1_secrets if v["slug"] == "hashicorp-vault-enterprise"), l1_secrets[0])
_overlay = l2_governance[0]
_pki_lead = pki_mim[0]


def _slot(role, v, why):
    return {"role": role, "pick": v["name"], "slug": v["slug"], "why": why,
            "residency": v["residency"], "irap": v["irap"]}


top_picks = [
    _slot("Primary secrets platform — most compliance-defensible (Layer 1)", _primary,
          "AU-resident AND IRAP-assessed — the safest system-of-record for APRA-regulated workloads (Azure Key Vault / GCP Secret Manager are equivalent AU-resident + IRAP options)."),
    _slot("Highest-coverage / multi-cloud secrets platform (Layer 1)", _multicloud,
          "Broadest capability (NATIVE on the most identity types) and cloud-agnostic brokering/rotation across AWS/Azure/GCP + on-prem. AU-resident via self-host; no vendor IRAP — deploy in an IRAP-assessed environment."),
    _slot("NHI discovery & governance overlay (Layer 2)", _overlay,
          "Strongest NHI discovery/inventory above the vault; SaaS-only today — pursue BYOC / AU-residency before production use."),
    _slot("PKI / machine-identity — certificates (Layer 1)", _pki_lead,
          "Certificate & key lifecycle most vaults don't own; self-host for AU residency."),
]

complementary = [
    {"have": "A cloud-native vault (AWS Secrets Manager / Azure Key Vault / GCP Secret Manager)",
     "add": "An L2 NHI discovery/governance overlay + PKI/MIM + an L0 HSM key-root",
     "why": "Native vaults broker secrets well but don't discover/govern NHIs across clouds or own certificate lifecycle — add the layers they don't cover."},
    {"have": "CyberArk PAM (human privileged access)",
     "add": "A secrets broker for app/NHI secrets (Conjur or Vault) + an L2 overlay",
     "why": "PAM governs human privileged sessions; machine/app secrets and NHI inventory need a broker plus a discovery layer."},
    {"have": "A single-cloud footprint going multi-cloud",
     "add": "A cloud-agnostic broker (HashiCorp Vault; AKEYLESS gateway-conditional)",
     "why": "Avoids per-cloud vault sprawl and lock-in — one rotation/brokering control plane across clouds."},
    {"have": "Developer-experience secrets tooling (Doppler / Infisical / 1Password)",
     "add": "An AU-sovereign backend (AWS Sydney / Azure AU / self-host) as the authoritative store",
     "why": "These are SaaS/DX layers without an AU region — keep the system of record AU-resident."},
]

RECDATA = {
    "l1_secrets": l1_secrets, "pki_mim": pki_mim, "l2_governance": l2_governance,
    "top_picks": top_picks, "complementary": complementary,
    "coverage_proof": {"max_l1_nhi": max((v["nhi_native"] for v in l1_secrets), default=0),
                       "nhi_total": len(nhis)},
    "substrate": {"name": "Fortanix DSM / Thales SafeNet (XYZ migration)",
                  "note": VENDOR_RESIDENCY.get(SUBSTRATE_SLUG, {}).get("note", "")},
}


html = report_render.render({
    "ranked": ranked, "anz": anz, "ucs": ucs, "nhis": nhis,
    "glossary": GLOSSARY, "layer_label": LAYER_LABEL, "short": SHORT,
    "reg": REG, "regdata": REGDATA, "recdata": RECDATA, "meta": meta,
})

if _ARGS.emit_data:
    with open(_ARGS.emit_data, "w", encoding="utf-8") as _ef:
        json.dump({"REGDATA": REGDATA, "RECDATA": RECDATA}, _ef,
                  ensure_ascii=False, sort_keys=True)

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Ranked vendors: {meta['ranked_vendors']}; ranked rows: {meta['ranked_rows']} (of {meta['total_rows']})")
print(f"UCs: {meta['ucs']}; NHIs: {meta['nhis']}; XYZ: {len(anz)}; REG-mapped UCs: {len(REG)}; glossary: {len(GLOSSARY)}")

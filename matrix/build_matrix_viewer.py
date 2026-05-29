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

_CFGDIR = os.path.join(HERE, "config")

_ap = argparse.ArgumentParser(description="Build the secrets-management report.")
_ap.add_argument("--config", help="path to an engagement.yaml")
_ap.add_argument("--preset", help="named preset (financial|government|retail|baseline)")
_ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides primary)")
_ap.add_argument("--emit-data", help="(test hook) also dump {REGDATA,RECDATA} JSON to this path")
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

anz = [{"uc_id": r["uc_id"], "anz_state": r.get("anz_state", ""), "confidence": r.get("confidence", ""),
        "evidence": r.get("evidence_redacted", ""), "recommendation": r.get("gap_notes", ""),
        "sensitivity": r.get("sensitivity_tag", "")} for r in read_csv("anz-current-state.csv")]

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
state_by_uc = {a["uc_id"]: a["anz_state"] for a in anz}
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
        c["anz_state"] = min(states, key=lambda s: STATE_RANK.get(s, 9)) if states else "UNKNOWN"
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

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>XYZ Secrets-Management — Stakeholder Report (PRD v0.1)</title>
<style>
  :root{ --bg:#f4f6f8;--fg:#1a1a1a;--muted:#667;--border:#dcdfe3;--card:#fff;--accent:#2a4d6e;
    --l1:#2a4d6e;--l2:#00838f;--l0:#8d6e63;--native:#2e7d32;--addon:#ed6c02;--partner:#6a1b9a;
    --gap:#c62828;--na:#757575;--met:#2e7d32;--partial:#ed6c02;--pending:#5c6bc0; }
  *{box-sizing:border-box;}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;background:var(--bg);
    color:var(--fg);margin:0;padding:0;font-size:13px;line-height:1.5;}
  .internal-bar{background:#7a1212;color:#fff;text-align:center;font-size:11px;font-weight:600;padding:3px;}
  header{background:var(--accent);color:#fff;padding:14px 18px;}
  header h1{margin:0;font-size:17px;} header .sub{font-size:12px;opacity:.85;margin-top:3px;}
  nav{display:flex;gap:2px;background:#1f3a52;padding:0 10px;flex-wrap:wrap;}
  nav button{background:transparent;color:#cdd8e3;border:0;border-bottom:3px solid transparent;
    padding:9px 14px;font-size:13px;cursor:pointer;font-family:inherit;}
  nav button:hover{color:#fff;} nav button.active{color:#fff;border-bottom-color:#ffb74d;font-weight:600;}
  main{padding:16px;max-width:1180px;margin:0 auto;}
  .view{display:none;} .view.active{display:block;}
  h2{font-size:15px;color:var(--accent);margin:0 0 10px;} .muted{color:var(--muted);}
  .gloss{cursor:help;border-bottom:1px dotted var(--muted);}
  .kpis{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;}
  .kpi{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:10px 14px;min-width:96px;}
  .kpi .n{font-size:22px;font-weight:700;color:var(--accent);} .kpi .l{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;}
  .posture{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:14px;margin-bottom:16px;}
  .bar{display:flex;height:30px;border-radius:4px;overflow:hidden;margin:8px 0;}
  .bar span{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600;font-size:12px;}
  .seg-MET{background:var(--met);} .seg-PARTIAL{background:var(--partial);} .seg-GAP{background:var(--gap);} .seg-PENDING{background:var(--pending);}
  .legend{font-size:11px;color:var(--muted);} .legend b{color:var(--fg);}
  .adj{font-size:12px;margin-top:8px;padding:6px 8px;background:#eef6ee;border:1px solid #cfe3cf;border-radius:4px;}
  .adj a{color:var(--accent);cursor:pointer;}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;} @media(max-width:760px){.grid2{grid-template-columns:1fr;}}
  .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;} @media(max-width:760px){.grid3{grid-template-columns:1fr;}}
  .card{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:14px;margin-bottom:14px;}
  .card h3{margin:0 0 6px;font-size:14px;color:var(--accent);}
  .gaplist{list-style:none;padding:0;margin:0;} .gaplist li{padding:7px 8px;border-bottom:1px solid var(--border);cursor:pointer;display:flex;gap:8px;align-items:center;}
  .gaplist li:hover{background:#eef3f8;} .gaplist .id{font-family:ui-monospace,monospace;color:var(--accent);font-size:12px;min-width:74px;}
  .pill{display:inline-block;padding:1px 7px;border-radius:10px;color:#fff;font-size:11px;font-weight:600;}
  .pill-GAP{background:var(--gap);} .pill-PARTIAL{background:var(--partial);} .pill-PENDING{background:var(--pending);} .pill-MET{background:var(--met);}
  .lchip{display:inline-block;padding:1px 6px;border-radius:3px;color:#fff;font-weight:600;font-size:11px;}
  .lchip.L0{background:var(--l0);} .lchip.L1{background:var(--l1);} .lchip.L2{background:var(--l2);}
  .reco{background:#eef3f8;border-left:4px solid var(--accent);border-radius:4px;padding:9px 11px;margin-bottom:10px;font-size:13px;}
  .layerhdr{margin:12px 0 4px;font-weight:600;}
  .gridwrap{overflow-x:auto;border:1px solid var(--border);border-radius:4px;}
  table.vgrid{border-collapse:collapse;font-size:11px;white-space:nowrap;min-width:100%;}
  table.vgrid th,table.vgrid td{border:1px solid var(--border);padding:4px 6px;text-align:center;}
  table.vgrid thead th{background:#eef1f4;position:sticky;top:0;font-weight:600;}
  table.vgrid tbody th{background:#f7f9fb;text-align:right;position:sticky;left:0;font-weight:600;color:var(--muted);}
  table.vgrid td.matcell{font-weight:700;}
  .cell-NATIVE{background:#e6f4ea;color:var(--native);font-weight:700;} .cell-ADD-ON{background:#fdf0e3;color:var(--addon);}
  .cell-PARTNER{background:#f3e9f7;color:var(--partner);} .cell-GAP{background:#fdecec;color:var(--gap);} .cell-NA{background:#f0f0f0;color:var(--na);}
  .chips{margin-top:6px;} .chips b{font-size:12px;}
  .chips span{display:inline-block;background:#eef1f4;border:1px solid var(--border);border-radius:10px;padding:1px 8px;margin:2px 3px 2px 0;font-size:11px;}
  .anz-card{border-left:4px solid var(--partial);}
  .rec{background:#eef6ee;border:1px solid #cfe3cf;border-radius:4px;padding:8px 10px;margin-top:8px;}
  .met-toggle{margin-top:10px;padding:8px;background:#f7f9fb;border:1px dashed var(--border);border-radius:4px;}
  .met-toggle label{cursor:pointer;}
  .tag-internal{background:#7a1212;color:#fff;font-size:10px;padding:1px 6px;border-radius:3px;font-weight:700;}
  .controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px;background:var(--card);border:1px solid var(--border);border-radius:4px;padding:8px;}
  .controls label{font-size:12px;color:var(--muted);}
  .layer-toggles{display:flex;gap:10px;align-items:center;padding:4px 8px;border:1px solid var(--border);border-radius:3px;background:#f7f9fb;}
  .layer-toggles label{display:inline-flex;align-items:center;gap:4px;cursor:pointer;color:var(--fg);}
  #count{margin-left:auto;font-weight:600;color:var(--accent);}
  .tablewrap{overflow-x:auto;border:1px solid var(--border);border-radius:4px;}
  table.matrix{width:100%;min-width:1220px;border-collapse:collapse;background:var(--card);font-size:12px;}
  table.matrix th,table.matrix td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--border);vertical-align:top;}
  table.matrix th{background:var(--accent);color:#fff;cursor:pointer;user-select:none;position:sticky;top:0;white-space:nowrap;}
  table.matrix th.sort-asc::after{content:" ▲";} table.matrix th.sort-desc::after{content:" ▼";}
  table.matrix td.wrap{white-space:normal;word-break:break-word;}
  .cov{font-weight:600;padding:1px 6px;border-radius:3px;color:#fff;display:inline-block;font-size:11px;}
  .cov-NATIVE{background:var(--native);} .cov-ADD-ON{background:var(--addon);} .cov-PARTNER{background:var(--partner);} .cov-GAP{background:var(--gap);} .cov-NA{background:var(--na);}
  .ev-url a{color:var(--accent);word-break:break-all;}
  .note{font-size:12px;color:var(--muted);margin-top:8px;}
  .colw-vendor{width:150px;} .colw-target{width:80px;} .colw-type{width:54px;} .colw-cov{width:90px;}
  .colw-mat{width:80px;} .colw-url{width:230px;} .colw-quote{width:260px;} .colw-cite{width:150px;} .colw-notes{width:230px;} .colw-layer{width:46px;}
  /* compliance-trace cascade */
  .casc{display:grid;grid-template-columns:215px 290px 1fr 1fr;gap:8px;height:68vh;}
  @media(max-width:900px){.casc{grid-template-columns:1fr 1fr;height:auto;}}
  .casc-col{border:1px solid var(--border);border-radius:6px;background:var(--card);display:flex;flex-direction:column;min-height:0;}
  .casc-col .col-head{background:#eef1f4;padding:6px 10px;font-weight:600;font-size:12px;border-bottom:1px solid var(--border);}
  .casc-col .scroll{overflow-y:auto;padding:4px;flex:1;min-height:120px;}
  .item{padding:7px 8px;border-bottom:1px solid var(--border);cursor:pointer;border-radius:4px;}
  .item:hover{background:#eef3f8;} .item.active{background:#dfeaf4;outline:2px solid var(--accent);}
  .mono{font-family:ui-monospace,monospace;} .ctrlcode{font-family:ui-monospace,monospace;color:var(--accent);font-weight:700;}
  .ml{font-family:ui-monospace,monospace;font-size:9px;background:var(--accent);color:#fff;padding:0 4px;border-radius:2px;margin-left:4px;}
  .state-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle;}
  .state-dot.GAP{background:var(--gap);} .state-dot.PARTIAL{background:var(--partial);} .state-dot.PENDING{background:var(--pending);} .state-dot.MET{background:var(--met);} .state-dot.UNKNOWN{background:#bbb;}
  .ustate{padding:0 4px;border-radius:2px;color:#fff;font-size:9px;font-family:ui-monospace,monospace;}
  .ustate.GAP{background:var(--gap);} .ustate.PARTIAL{background:var(--partial);} .ustate.PENDING{background:var(--pending);} .ustate.MET{background:var(--met);} .ustate.UNKNOWN{background:#999;}
  .ctrlhdr{background:#eef3f8;border:1px solid var(--border);border-radius:4px;padding:8px 10px;margin-bottom:6px;}
  .subtle{font-size:10px;color:var(--muted);font-family:ui-monospace,monospace;}
  .quotebox{font-size:10px;color:var(--muted);font-style:italic;line-height:1.4;border-left:3px solid var(--accent);padding-left:6px;margin-top:4px;}
  .vrow2{display:grid;grid-template-columns:26px 1fr 74px;gap:6px;padding:5px 4px;border-bottom:1px dotted var(--border);align-items:start;}
  .vrow2 .m{font-weight:700;text-align:center;color:var(--accent);} .vrow2 .vq{grid-column:1/4;font-size:10px;color:var(--muted);font-style:italic;line-height:1.35;}
  .placeholder{padding:20px;color:var(--muted);font-style:italic;text-align:center;}
  /* business-value view */
  .vsec{font-size:14px;color:var(--accent);margin:18px 0 8px;border-bottom:1px solid var(--border);padding-bottom:5px;}
  .loop{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 2px;}
  .loop .step{flex:1;min-width:128px;background:var(--card);border:1px solid var(--border);border-top:3px solid var(--accent);border-radius:6px;padding:9px 11px;}
  .loop .step .num{font-family:ui-monospace,monospace;font-size:10px;color:var(--muted);}
  .loop .step b{display:block;font-size:13px;color:var(--fg);margin:2px 0;}
  .loop .step .d{font-size:11px;color:var(--muted);line-height:1.3;}
  .loparrow{color:var(--accent);font-weight:700;flex:none;}
  .ocard .mech{margin:6px 0 8px;font-size:13px;}
  .ocard .measure{font-size:12px;color:var(--muted);border-top:1px dotted var(--border);padding-top:6px;}
  .ocard .measure b{color:var(--accent);}
  .vtag{display:inline-block;font-family:ui-monospace,monospace;font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:10px;color:#fff;}
  .vtag.hard{background:var(--native);} .vtag.hours{background:var(--accent);} .vtag.risk{background:var(--gap);} .vtag.kpi{background:var(--pending);}
  .kpitable{width:100%;border-collapse:collapse;font-size:12px;}
  .kpitable th{text-align:left;border-bottom:2px solid #ccc;padding:6px;color:var(--accent);}
  .kpitable td{padding:6px;border-bottom:1px solid #eee;vertical-align:top;}
  .roi-banner{background:#eef6ee;border:1px solid #cfe3cf;border-left:4px solid var(--native);border-radius:6px;padding:14px 16px;margin-top:16px;font-size:13px;line-height:1.5;}
  .roi-banner b{color:var(--native);}
</style>
</head>
<body>
<div class="internal-bar">INTERNAL — prepared for a major AU Tier-1 FI (XYZ). Contains [INTERNAL] current-state findings. Do not distribute externally (open question O2).</div>
<header>
  <h1>XYZ Secrets-Management — Stakeholder Report</h1>
  <div class="sub">PRD v0.1 · __RV__ ranked vendors (+ a Layer-0 crypto-substrate dependency) · __NHI__ identities · __UC__ use cases</div>
</header>
<nav>
  <button data-view="dashboard" class="active">XYZ posture</button>
  <button data-view="uc">By use case</button>
  <button data-view="nhi">By identity</button>
  <button data-view="reg">Compliance trace</button>
  <button data-view="rec">Recommendations</button>
  <button data-view="value">Business value</button>
  <button data-view="table">Browse all</button>
</nav>
<main>

<section id="view-dashboard" class="view active">
  <h2>Where XYZ stands today</h2>
  <div class="kpis" id="kpis"></div>
  <div class="posture">
    <b>XYZ secrets posture — __UC__ use cases scored</b>
    <div class="bar" id="posture-bar"></div>
    <div class="legend" id="posture-legend"></div>
    <div class="adj" id="posture-adj" style="display:none"></div>
  </div>
  <div class="grid3">
    <div class="card">
      <h3>Top gaps — click to open the decision card</h3>
      <ul class="gaplist" id="gaplist"></ul>
    </div>
    <div class="card">
      <h3>Partial coverage — tick what XYZ actually considers MET</h3>
      <p class="muted" style="margin-top:0">Your assessment is saved in this browser and updates the posture above.</p>
      <ul class="gaplist" id="partiallist"></ul>
    </div>
    <div class="card">
      <h3>Pending / in progress — click to open the decision card</h3>
      <ul class="gaplist" id="pendinglist"></ul>
    </div>
  </div>
  <div class="card" style="border-left:4px solid var(--l0);">
    <h3><span class="lchip L0">L0</span> Crypto-substrate dependency (not ranked)</h3>
    <p class="muted">The vault is unsealed / key-rooted by an HSM substrate beneath it — a
    <b>dependency, not a vendor in this comparison</b> (ADR-007). XYZ's live decision is the
    <b>Thales SafeNet Luna → Fortanix DSM</b> migration. Evaluate as crypto infrastructure
    (FIPS 140-3, IRAP, PQC, vault PKCS#11), not against the vaults ranked here.</p>
  </div>
</section>

<section id="view-uc" class="view">
  <h2>Pick a use case → recommendation, vendor coverage, controls, XYZ stance</h2>
  <div style="margin-bottom:12px;"><label class="muted">Use case&nbsp;</label><select id="uc-select" style="min-width:380px;max-width:100%"></select></div>
  <div id="uc-card"></div>
</section>

<section id="view-nhi" class="view">
  <h2>Pick a machine identity → which vendors handle it, by layer</h2>
  <div style="margin-bottom:12px;"><label class="muted">Identity&nbsp;</label><select id="nhi-select" style="min-width:380px;max-width:100%"></select></div>
  <div id="nhi-card"></div>
</section>

<section id="view-reg" class="view">
  <h2>Trace a regulatory control → use cases → vendor evidence</h2>
  <p class="muted">Click left → right: <b>framework → control → use case → vendor evidence</b>. Default: APRA CPS 234. Built for Risk &amp; Compliance / APRA audit packs.</p>
  <div class="casc">
    <div class="casc-col"><div class="col-head">Framework</div><div class="scroll" id="casc-fw"></div></div>
    <div class="casc-col"><div class="col-head">Control</div><div class="scroll" id="casc-ctrl"></div></div>
    <div class="casc-col"><div class="col-head">Use case</div><div class="scroll" id="casc-uc"></div></div>
    <div class="casc-col"><div class="col-head">Vendor evidence</div><div class="scroll" id="casc-vendor"></div></div>
  </div>
  <p class="note">Vendor evidence is the 18 ranked vendors (Fortanix excluded per ADR-007). State dot = worst XYZ state across the control's use cases (GAP &gt; PARTIAL &gt; PENDING &gt; MET).</p>
</section>

<section id="view-rec" class="view">
  <h2>Vendor recommendations — compose a best-of-breed stack</h2>
  <p class="muted">Layer-scoped and AU-residency-first. Rank <i>within</i> a layer; compose <i>across</i> layers (ADR-007). Generic XYZ-FI guidance — no assumption about incumbent tooling.</p>
  <div id="rec-body"></div>
</section>

<section id="view-value" class="view">
  <h2>Business value — what this assessment is worth</h2>
  <p class="muted">A posture grade is a diagnosis; the value is in the loop it drives — <b>assess &rarr; prioritise &rarr; remediate &rarr; measure</b>. Each outcome below maps to how it is measured and where the return comes from.</p>
  <div id="value-body"></div>
  <p class="note">ROI here is cost-avoidance and decision-efficiency, not new revenue. Figures are intentionally not invented — this view supplies the metrics to quantify against the institution's own baselines.</p>
</section>

<section id="view-table" class="view">
  <h2>Browse all capability rows</h2>
  <div class="controls">
    <div class="layer-toggles" title="Show/hide stack layers">
      <span class="muted">Layers:</span>
      <label><input type="checkbox" class="layer-toggle" value="L1" checked> <span class="lchip L1">L1</span></label>
      <label><input type="checkbox" class="layer-toggle" value="L2" checked> <span class="lchip L2">L2</span></label>
    </div>
    <label for="search">Search</label><input id="search" type="text" placeholder="any column...">
    <label for="vendor-filter">Vendor</label><select id="vendor-filter"><option value="">all</option></select>
    <label for="cov-filter">Coverage</label><select id="cov-filter"><option value="">all</option></select>
    <button id="reset">reset</button><span id="count"></span>
  </div>
  <div class="tablewrap">
  <table class="matrix" id="matrix-table">
    <thead><tr>
      <th class="colw-layer" data-key="layer">Layer</th>
      <th class="colw-vendor" data-key="vendor_name">Vendor</th>
      <th class="colw-target" data-key="target_id">Target</th>
      <th class="colw-type" data-key="target_type">Type</th>
      <th class="colw-cov" data-key="coverage">Coverage</th>
      <th class="colw-mat" data-key="maturity">Maturity</th>
      <th class="colw-url" data-key="evidence_url">Evidence URL</th>
      <th class="colw-quote" data-key="evidence_quote">Evidence quote</th>
      <th class="colw-cite" data-key="citation_keys">Citations</th>
      <th class="colw-notes" data-key="notes">Notes</th>
    </tr></thead>
    <tbody id="matrix-body"></tbody>
  </table>
  </div>
  <p class="note">Fortanix DSM (Layer-0 substrate) is excluded here per ADR-007 — see the XYZ-posture tab. Scroll the table sideways to see all columns.</p>
</section>

</main>
<script>
const DATA = /*__DATA__*/[];
const XYZ = /*__XYZ__*/[];
const UCS = /*__UCS__*/[];
const NHIS = /*__NHIS__*/[];
const GLOSSARY = /*__GLOSSARY__*/{};
const LAYER_LABEL = /*__LAYERLABEL__*/{};
const SHORT = /*__SHORT__*/{};
const REG = /*__REG__*/{};
const REGDATA = /*__REGDATA__*/{};
const RECDATA = /*__RECDATA__*/{};
const META = /*__META__*/{};

function esc(s){ if(s==null) return ""; return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function gloss(code){ const d=GLOSSARY[code]; const t=esc(code); return d?'<span class="gloss" title="'+esc(d)+'">'+t+'</span>':t; }
function covClass(c){ return "cov cov-"+(c==="N/A"?"NA":c); }
function cellClass(c){ return "cell-"+(c==="N/A"?"NA":c); }
function covAbbr(c){ return {NATIVE:"NAT","ADD-ON":"ADD",PARTNER:"PTR",GAP:"—","N/A":"N/A"}[c]||c; }
function byId(a,k,v){ return a.find(x=>x[k]===v); }
const COVRANK={NATIVE:0,"ADD-ON":1,PARTNER:2,GAP:3,"N/A":4};

// vendor metadata derived from ranked DATA
const VLAYER={}, VNAME={};
DATA.forEach(r=>{ VLAYER[r.vendor_slug]=r.layer; VNAME[r.vendor_slug]=r.vendor_name; });
const VENDOR_SLUGS=[...new Set(DATA.map(r=>r.vendor_slug))];

// ---- XYZ override state (stakeholder "mark as MET"), persisted ----
function loadOv(){ try{ return JSON.parse(localStorage.getItem("anz_overrides")||"{}"); }catch(e){ return {}; } }
function saveOv(){ try{ localStorage.setItem("anz_overrides",JSON.stringify(OV)); }catch(e){} }
let OV=loadOv();
function effState(a){ return OV[a.uc_id] ? "MET" : a.anz_state; }
function toggleMet(uc){ if(OV[uc]) delete OV[uc]; else OV[uc]=true; saveOv(); renderDashboard();
  const s=document.getElementById("uc-select"); if(s && s.value) renderUCCard(s.value); }
function resetOv(){ OV={}; saveOv(); renderDashboard(); }

// ---- navigation ----
const NAVBTNS=document.querySelectorAll("nav button");
function showView(n){ document.querySelectorAll(".view").forEach(v=>v.classList.remove("active"));
  document.getElementById("view-"+n).classList.add("active"); NAVBTNS.forEach(b=>b.classList.toggle("active",b.dataset.view===n)); }
NAVBTNS.forEach(b=>b.addEventListener("click",()=>showView(b.dataset.view)));

// ---- vendor-as-columns coverage/maturity grid ----
function vgrid(targetId){
  let html="";
  [["L1","Secrets management"],["L2","NHI governance"]].forEach(([L,lbl])=>{
    const entries = VENDOR_SLUGS.filter(s=>VLAYER[s]===L)
      .map(s=>({slug:s, r:DATA.find(d=>d.vendor_slug===s && d.target_id===targetId)}))
      .filter(e=>e.r)
      .sort((a,b)=>(COVRANK[a.r.coverage]-COVRANK[b.r.coverage])||(parseFloat(b.r.maturity||0)-parseFloat(a.r.maturity||0)));
    if(!entries.length) return;
    html += '<div class="layerhdr"><span class="lchip '+L+'">'+L+'</span> '+esc(lbl)+
      ' <span class="muted" style="font-weight:400">(vendors as columns — hover a code for its meaning)</span></div>';
    html += '<div class="gridwrap"><table class="vgrid"><thead><tr><th></th>'+
      entries.map(e=>'<th title="'+esc(VNAME[e.slug])+'">'+esc(SHORT[e.slug]||VNAME[e.slug])+'</th>').join("")+
      '</tr></thead><tbody><tr><th>Satisfies</th>'+
      entries.map(e=>'<td class="'+cellClass(e.r.coverage)+'" title="'+esc(GLOSSARY[e.r.coverage]||"")+'">'+covAbbr(e.r.coverage)+'</td>').join("")+
      '</tr><tr><th>Maturity</th>'+
      entries.map(e=>'<td class="matcell" title="'+esc(GLOSSARY[e.r.maturity]||"")+'">'+(e.r.coverage==="GAP"?"—":esc(e.r.maturity))+'</td>').join("")+
      '</tr></tbody></table></div>';
  });
  return html || '<p class="muted">No coverage rows for this target.</p>';
}

function recommend(targetId){
  const fit=DATA.filter(r=>r.target_id===targetId && (r.coverage==="NATIVE"||r.coverage==="ADD-ON"||r.coverage==="PARTNER"))
    .sort((a,b)=>(COVRANK[a.coverage]-COVRANK[b.coverage])||(parseFloat(b.maturity||0)-parseFloat(a.maturity||0)));
  const l1=fit.find(r=>r.layer==="L1"), l2=fit.find(r=>r.layer==="L2");
  if(!l1 && !l2) return "No vendor offers first-class coverage here — a structural market gap.";
  let s="";
  if(l1) s='Best fit: <b>'+esc(l1.vendor_name)+'</b> — '+esc(l1.coverage)+', maturity '+esc(l1.maturity)+' (L1 secrets management).';
  if(l2) s+=(s?" ":"")+'Complement above the vault with <b>'+esc(l2.vendor_name)+'</b> ('+esc(l2.coverage)+', m'+esc(l2.maturity)+', L2 governance).';
  return s;
}

function regChips(uc){
  const r=REG[uc]; if(!r) return "";
  const mk=(arr,lbl)=> '<div class="chips"><b>'+lbl+':</b> '+(arr.length?arr.map(c=>'<span>'+esc(c)+'</span>').join(""):'<span class="muted">none</span>')+'</div>';
  return mk(r.APRA||[],"APRA CPS 234")+mk(r.ISM||[],"ASD ISM");
}

// ---- dashboard ----
function renderDashboard(){
  document.getElementById("kpis").innerHTML =
    [["ranked vendors",META.ranked_vendors],["machine identities",META.nhis],["use cases",META.ucs]]
    .map(([l,n])=>'<div class="kpi"><div class="n">'+esc(n)+'</div><div class="l">'+esc(l)+'</div></div>').join("");
  const order=["MET","PARTIAL","GAP","PENDING"];
  const base={MET:0,PARTIAL:0,GAP:0,PENDING:0}, adj={MET:0,PARTIAL:0,GAP:0,PENDING:0};
  XYZ.forEach(a=>{ if(base[a.anz_state]!=null) base[a.anz_state]++; const e=effState(a); if(adj[e]!=null) adj[e]++; });
  const total=XYZ.length||1;
  document.getElementById("posture-bar").innerHTML = order.filter(s=>base[s]>0).map(s=>{
    const pct=(100*base[s]/total).toFixed(1);
    return '<span class="seg-'+s+'" style="width:'+pct+'%" title="'+s+' '+base[s]+'">'+(base[s]>=2?base[s]:"")+'</span>'; }).join("");
  document.getElementById("posture-legend").innerHTML = order.map(s=>'<span class="pill pill-'+s+'">'+s+'</span> <b>'+base[s]+'</b> &nbsp;').join("")+
    ' — assessed baseline. 0 MET reflects the dominant finding: with no inventory layer, XYZ cannot quantify "working" as "met".';
  const adjEl=document.getElementById("posture-adj");
  const nOv=Object.keys(OV).length;
  if(nOv){ adjEl.style.display="block";
    adjEl.innerHTML='<b>With your assessment ('+nOv+' marked MET):</b> '+order.map(s=>'<span class="pill pill-'+s+'">'+s+'</span> <b>'+adj[s]+'</b> &nbsp;').join("")+
      ' &nbsp;<a onclick="resetOv()">reset</a>'; }
  else { adjEl.style.display="none"; }

  const ucTitle=id=>{ const u=byId(UCS,"uc_id",id); return u?u.short_title:id; };
  document.getElementById("gaplist").innerHTML = XYZ.filter(a=>a.anz_state==="GAP").map(a=>
    '<li onclick="goToUC(\''+a.uc_id+'\')"><span class="id">'+esc(a.uc_id)+'</span><span>'+esc(ucTitle(a.uc_id))+'</span>'+
    '<span class="pill pill-GAP" style="margin-left:auto">'+esc(a.confidence)+'</span></li>').join("")||'<li class="muted">none</li>';
  document.getElementById("pendinglist").innerHTML = XYZ.filter(a=>a.anz_state==="PENDING").map(a=>
    '<li onclick="goToUC(\''+a.uc_id+'\')"><span class="id">'+esc(a.uc_id)+'</span><span>'+esc(ucTitle(a.uc_id))+'</span>'+
    '<span class="pill pill-PENDING" style="margin-left:auto">'+esc(a.confidence)+'</span></li>').join("")||'<li class="muted">none</li>';
  document.getElementById("partiallist").innerHTML = XYZ.filter(a=>a.anz_state==="PARTIAL").map(a=>{
    const checked=OV[a.uc_id]?"checked":"";
    return '<li><input type="checkbox" '+checked+' onclick="event.stopPropagation();toggleMet(\''+a.uc_id+'\')" title="XYZ considers this MET">'+
      '<span class="id" onclick="goToUC(\''+a.uc_id+'\')">'+esc(a.uc_id)+'</span>'+
      '<span onclick="goToUC(\''+a.uc_id+'\')">'+esc(ucTitle(a.uc_id))+'</span>'+
      (OV[a.uc_id]?'<span class="pill pill-MET" style="margin-left:auto">MET ✓</span>':'<span class="pill pill-PARTIAL" style="margin-left:auto">PARTIAL</span>')+'</li>'; }).join("")||'<li class="muted">none</li>';
}

// ---- use-case card ----
function goToUC(id){ const s=document.getElementById("uc-select"); s.value=id; renderUCCard(id); showView("uc"); }
function renderUCCard(id){
  const u=byId(UCS,"uc_id",id), a=byId(XYZ,"uc_id",id), el=document.getElementById("uc-card");
  if(!u){ el.innerHTML=""; return; }
  const nhiChips=(u.nhis_in_scope||"").split(";").filter(Boolean).map(n=>'<span>'+gloss(n.trim())+'</span>').join("");
  const lensChips=(u.outcome_lens||"").split(";").filter(Boolean).map(x=>'<span>'+esc(x.trim())+'</span>').join("");
  let anzHtml='<p class="muted">No XYZ current-state record.</p>';
  if(a){
    const eff=effState(a), overridden=!!OV[a.uc_id];
    anzHtml='<div><span class="pill pill-'+eff+'">'+esc(eff)+'</span> '+
      (overridden?'<span class="muted">(stakeholder-assessed; baseline '+esc(a.anz_state)+')</span>':'<span class="muted">confidence '+esc(a.confidence)+'</span>')+' '+
      (a.sensitivity?'<span class="tag-internal">'+esc(a.sensitivity.replace(/[\[\]]/g,""))+'</span>':'')+'</div>'+
      (a.evidence?'<p>'+esc(a.evidence)+'</p>':'')+
      (a.recommendation?'<div class="rec"><b>Recommended:</b> '+esc(a.recommendation)+'</div>':'')+
      '<div class="met-toggle"><label><input type="checkbox" '+(overridden?"checked":"")+' onclick="toggleMet(\''+a.uc_id+'\')"> '+
      'XYZ considers this use case <b>MET</b> (stakeholder assessment — saved in this browser)</label></div>';
  }
  el.innerHTML =
    '<div class="card"><h3>'+esc(u.uc_id)+' · '+esc(u.short_title)+' <span class="muted" style="font-weight:400">('+esc(u.category)+' · '+esc(u.priority_fi)+')</span></h3>'+
      (u.story?'<p class="muted">"'+esc(u.story)+'"</p>':"")+
      '<div class="chips"><b>Lens:</b> '+lensChips+'</div>'+
      '<div class="chips"><b>Identities in scope:</b> '+nhiChips+'</div>'+
      regChips(id)+'</div>'+
    '<div class="card"><h3>Recommendation &amp; vendor coverage</h3>'+
      '<div class="reco">'+recommend(id)+'</div>'+ vgrid(id)+
      '<p class="note">A discovery tool (L2) complements a vault (L1) — it does not replace it. NAT=NATIVE · ADD=add-on · PTR=partner · —=gap.</p></div>'+
    '<div class="card anz-card"><h3>Where XYZ stands</h3>'+anzHtml+'</div>';
}

// ---- nhi card ----
function renderNHICard(id){
  const n=byId(NHIS,"nhi_id",id), el=document.getElementById("nhi-card");
  if(!n){ el.innerHTML=""; return; }
  el.innerHTML='<div class="card"><h3>'+esc(n.nhi_id)+' · '+esc(n.short_name)+' <span class="muted" style="font-weight:400">('+esc(n.bucket)+')</span></h3>'+
    (n.description?'<p class="muted">'+esc(n.description)+'</p>':"")+'</div>'+
    '<div class="card"><h3>Vendor coverage (all vendors, by layer)</h3>'+vgrid(id)+
    '<p class="note">v0.1 has no per-identity XYZ score (XYZ is assessed per use case). NAT=NATIVE · ADD=add-on · PTR=partner · —=gap.</p></div>';
}

// ---- selectors ----
(function(){
  const sel=document.getElementById("uc-select");
  [["FUNCTIONAL","Functional"],["NON_FUNCTIONAL","Non-functional"]].forEach(([cat,lbl])=>{
    const g=document.createElement("optgroup"); g.label=lbl;
    UCS.filter(u=>u.category===cat).forEach(u=>{ const o=document.createElement("option"); o.value=u.uc_id; o.textContent=u.uc_id+" · "+u.short_title; g.appendChild(o); });
    if(g.children.length) sel.appendChild(g);
  });
  sel.addEventListener("change",()=>renderUCCard(sel.value));
  if(sel.options.length){ sel.selectedIndex=0; renderUCCard(sel.value); }
  const nsel=document.getElementById("nhi-select");
  NHIS.forEach(n=>{ const o=document.createElement("option"); o.value=n.nhi_id; o.textContent=n.nhi_id+" · "+n.short_name; nsel.appendChild(o); });
  nsel.addEventListener("change",()=>renderNHICard(nsel.value));
  if(nsel.options.length){ nsel.selectedIndex=0; renderNHICard(nsel.value); }
})();

// ---- browse table ----
const TBODY=document.getElementById("matrix-body"), SEARCH=document.getElementById("search"),
  VFILT=document.getElementById("vendor-filter"), CFILT=document.getElementById("cov-filter"),
  HEADERS=document.querySelectorAll("#matrix-table th"), TOGGLES=document.querySelectorAll(".layer-toggle");
let sortKey="vendor_name", sortDir=1;
VENDOR_SLUGS.slice().sort().forEach(v=>{ const o=document.createElement("option"); o.value=v;o.textContent=v;VFILT.appendChild(o); });
[...new Set(DATA.map(r=>r.coverage))].sort().forEach(c=>{ const o=document.createElement("option"); o.value=c;o.textContent=c;CFILT.appendChild(o); });
function activeLayers(){ const s=new Set(); TOGGLES.forEach(t=>{ if(t.checked) s.add(t.value); }); return s; }
function renderTable(){
  const q=SEARCH.value.trim().toLowerCase(), v=VFILT.value, c=CFILT.value, layers=activeLayers();
  const rows=DATA.filter(r=>{ if(!layers.has(r.layer)) return false; if(v&&r.vendor_slug!==v) return false;
    if(c&&r.coverage!==c) return false; if(q&&Object.values(r).join(" ").toLowerCase().indexOf(q)===-1) return false; return true; });
  rows.sort((a,b)=>{ const av=a[sortKey]||"",bv=b[sortKey]||"";
    if(sortKey==="maturity") return (parseFloat(av)-parseFloat(bv))*sortDir; return String(av).localeCompare(String(bv))*sortDir; });
  TBODY.innerHTML=rows.map(r=>'<tr>'+
    '<td><span class="lchip '+r.layer+'" title="'+esc(LAYER_LABEL[r.layer]||"")+'">'+esc(r.layer)+'</span></td>'+
    '<td>'+esc(r.vendor_name)+'</td>'+
    '<td>'+gloss(r.target_id)+'</td><td>'+esc(r.target_type)+'</td>'+
    '<td><span class="'+covClass(r.coverage)+'" title="'+esc(GLOSSARY[r.coverage]||"")+'">'+esc(r.coverage)+'</span></td>'+
    '<td><span class="gloss" title="'+esc(GLOSSARY[r.maturity]||"")+'"><b>'+esc(r.maturity)+'</b></span></td>'+
    '<td class="wrap">'+(r.evidence_url&&/^https?:/i.test(r.evidence_url)?'<span class="ev-url"><a href="'+esc(r.evidence_url)+'" target="_blank" rel="noopener">'+esc(r.evidence_url)+'</a></span>':esc(r.evidence_url))+'</td>'+
    '<td class="wrap">'+esc(r.evidence_quote)+'</td><td class="wrap">'+esc(r.citation_keys)+'</td><td class="wrap">'+esc(r.notes)+'</td></tr>').join("");
  document.getElementById("count").textContent=rows.length+" of "+DATA.length+" rows";
  HEADERS.forEach(h=>{ h.classList.remove("sort-asc","sort-desc"); if(h.dataset.key===sortKey) h.classList.add(sortDir===1?"sort-asc":"sort-desc"); });
}
SEARCH.addEventListener("input",renderTable); VFILT.addEventListener("change",renderTable); CFILT.addEventListener("change",renderTable);
TOGGLES.forEach(t=>t.addEventListener("change",renderTable));
document.getElementById("reset").addEventListener("click",()=>{ SEARCH.value="";VFILT.value="";CFILT.value="";TOGGLES.forEach(t=>t.checked=true);sortKey="vendor_name";sortDir=1;renderTable(); });
HEADERS.forEach(h=>h.addEventListener("click",()=>{ const k=h.dataset.key; if(sortKey===k) sortDir=-sortDir; else {sortKey=k;sortDir=1;} renderTable(); }));

// ---- compliance-trace cascade (Framework → Control → UC → Vendor evidence) ----
(function(){
  const cFw=document.getElementById("casc-fw"), cCtrl=document.getElementById("casc-ctrl"),
    cUc=document.getElementById("casc-uc"), cV=document.getElementById("casc-vendor");
  if(!cFw) return;
  cFw.innerHTML = REGDATA.frameworks.map(fw=>'<div class="item" data-fw="'+esc(fw.slug)+'">'+
    '<div style="font-weight:600">'+esc(fw.label)+'</div><div class="subtle">'+fw.control_count+' controls · '+esc(fw.subtitle)+'</div></div>').join("");
  function showControls(fw){
    cFw.querySelectorAll(".item").forEach(x=>x.classList.toggle("active",x.dataset.fw===fw));
    const list=REGDATA.controls[fw]||[];
    cCtrl.innerHTML=list.map(c=>'<div class="item" data-code="'+esc(c.code)+'">'+
      '<span class="state-dot '+(c.anz_state||"UNKNOWN")+'"></span><span class="ctrlcode">'+esc(c.code)+'</span>'+
      (c.maturity_level?'<span class="ml">'+esc(c.maturity_level)+'</span>':"")+
      '<div style="font-size:11px;margin-top:2px">'+esc(c.title)+'</div>'+
      '<div class="subtle" style="margin-top:3px">'+c.uc_ids.length+' UCs · '+(c.anz_state||"UNKNOWN")+'</div></div>').join("")
      || '<div class="placeholder">No controls.</div>';
    cUc.innerHTML='<div class="placeholder">← Pick a control</div>'; cV.innerHTML="";
  }
  function showUcs(fw,code){
    cCtrl.querySelectorAll(".item").forEach(x=>x.classList.toggle("active",x.dataset.code===code));
    const c=(REGDATA.controls[fw]||[]).find(x=>x.code===code); if(!c) return;
    let hdr='<div class="ctrlhdr"><span class="ctrlcode">'+esc(c.code)+'</span>'+
      (c.maturity_level?'<span class="ml">'+esc(c.maturity_level)+'</span>':"")+
      '<div style="font-size:11px;font-weight:600;margin-top:2px">'+esc(c.title)+'</div>'+
      (c.evidence_quote?'<div class="quotebox">"'+esc(c.evidence_quote)+'"</div>':"")+
      (c.evidence_url&&/^https?:/i.test(c.evidence_url)?'<div style="margin-top:4px;font-size:10px"><a href="'+esc(c.evidence_url)+'" target="_blank" rel="noopener">source standard ↗</a></div>':"")+'</div>';
    let body=c.uc_ids.map(uid=>{ const u=REGDATA.ucs[uid]||{};
      return '<div class="item" data-uc="'+esc(uid)+'"><span class="ctrlcode">'+esc(uid)+'</span> '+
        '<span class="ustate '+(u.state||"UNKNOWN")+'">'+(u.state||"?")+'</span>'+
        '<div style="font-size:11px;margin-top:2px">'+esc(u.title||"(unknown)")+'</div>'+
        '<div class="subtle" style="margin-top:2px">'+esc(u.priority||"")+' · '+(u.nhi_count||0)+' NHIs · '+((REGDATA.vendor_uc[uid]||[]).length)+' vendor rows</div></div>'; }).join("")
      || '<div class="placeholder">No UCs.</div>';
    cUc.innerHTML=hdr+body; cV.innerHTML='<div class="placeholder">← Pick a use case</div>';
  }
  function showVendors(uid){
    cUc.querySelectorAll(".item").forEach(x=>x.classList.toggle("active",x.dataset.uc===uid));
    const u=REGDATA.ucs[uid]||{}, vlist=REGDATA.vendor_uc[uid]||[];
    let h='<div class="ctrlhdr"><span class="ctrlcode">'+esc(uid)+'</span><div style="font-size:11px;margin-top:2px">'+esc(u.title||"")+'</div></div>';
    h+=vlist.map(v=>'<div class="vrow2"><div class="m">'+(v.maturity||0)+'</div><div><b>'+esc(v.vendor_name)+'</b></div>'+
      '<div><span class="'+covClass(v.coverage)+'">'+esc(v.coverage)+'</span></div>'+
      (v.quote?'<div class="vq">"'+esc(v.quote)+'"</div>':"")+'</div>').join("") || '<div class="placeholder">No vendor rows.</div>';
    cV.innerHTML=h;
  }
  cFw.addEventListener("click",e=>{ const it=e.target.closest(".item"); if(it) showControls(it.dataset.fw); });
  cCtrl.addEventListener("click",e=>{ const it=e.target.closest(".item"); if(it){ const a=cFw.querySelector(".item.active"); showUcs(a?a.dataset.fw:REGDATA.frameworks[0].slug, it.dataset.code); } });
  cUc.addEventListener("click",e=>{ const it=e.target.closest(".item"); if(it&&it.dataset.uc) showVendors(it.dataset.uc); });
  const def=cFw.querySelector('[data-fw="apra-cps-234"]'); if(def) def.click(); else if(cFw.firstChild) cFw.firstChild.click();
})();

// ---- Recommendations tab (residency-first, layer-scoped) ----
function recChip(res, irap){
  const m={"AU-RESIDENT":["AU-resident","#1a7f37"],"CONDITIONAL":["AU conditional","#9a6700"],"SAAS-ONLY":["SaaS-only","#b35900"]};
  const x=m[res]||[res,"#555"];
  const ir = irap==="YES"?" · IRAP ✓":(irap==="PARTIAL"?" · IRAP ~":" · no IRAP");
  return '<span style="display:inline-block;padding:1px 7px;border-radius:10px;color:#fff;font-size:10px;font-weight:600;background:'+x[1]+'">'+esc(x[0])+ir+'</span>';
}
function recVendorRow(v, metric){
  const lay=VLAYER[v.slug]||"";
  return '<div style="padding:7px 0;border-bottom:1px solid #eee">'+
    '<span class="lchip '+lay+'">'+lay+'</span> <b>'+esc(v.name)+'</b> '+
    '<span class="muted" style="font-size:11px">('+esc(v.tier)+')</span> '+recChip(v.residency,v.irap)+
    '<div class="muted" style="font-size:11px;margin-top:2px">'+metric+
    ' · '+v.nhi_native+'/'+RECDATA.coverage_proof.nhi_total+' identities NATIVE'+(v.nhi_gap?' · '+v.nhi_gap+' gaps':'')+'</div>'+
    (v.res_note?'<div style="font-size:11px;color:#666;margin-top:2px">'+esc(v.res_note)+'</div>':'')+'</div>';
}
function renderRecommendations(){
  const el=document.getElementById("rec-body"); if(!el||!RECDATA.coverage_proof) return;
  const cp=RECDATA.coverage_proof; let h="";
  h+='<div class="card" style="border-left:4px solid var(--l1)"><h3>Why a stack, not a single vendor</h3>'+
     '<p>No single vendor covers all '+META.ucs+' use cases. The strongest Layer-1 vault is NATIVE on only <b>'+cp.max_l1_nhi+' of '+cp.nhi_total+'</b> identity types — and a Layer-1 vault cannot <i>discover / govern</i> identities, while a Layer-2 tool cannot <i>broker</i> secrets. So compose across layers; rank within a layer (ADR-007). Large enterprises deliberately run best-of-breed for exactly this reason.</p></div>';
  h+='<div class="card"><h3><span class="lchip L1">L1</span> Secrets management — top picks (AU-residency first)</h3>'+
     '<p class="muted" style="font-size:11px">'+esc(LAYER_LABEL.L1)+'</p>'+
     RECDATA.l1_secrets.map(v=>recVendorRow(v, v.secrets_native+'/'+v.secrets_total+' secrets-mgmt use cases NATIVE')).join("")+'</div>';
  h+='<div class="card"><h3><span class="lchip L1">L1</span> PKI / machine-identity (certificates) — a distinct discipline</h3>'+
     '<p class="muted" style="font-size:11px">Certificate &amp; key lifecycle that most vaults do not own.</p>'+
     RECDATA.pki_mim.map(v=>recVendorRow(v, v.secrets_native+'/'+v.secrets_total+' secrets-mgmt use cases NATIVE')).join("")+'</div>';
  h+='<div class="card"><h3><span class="lchip L2">L2</span> NHI discovery / governance — top picks (residency first)</h3>'+
     '<p class="muted" style="font-size:11px">'+esc(LAYER_LABEL.L2)+'</p>'+
     '<p class="note">Every Layer-2 vendor is SaaS-only with no AU region / IRAP today — material under APRA CPS 234 §22 / CPS 230 §39. Treat as an observability / governance overlay above an AU-resident vault; pursue BYOC or an AU-residency commitment before production. Human-workforce IGA (SailPoint, Saviynt, Okta IGA) is a separate adjacent market — evaluate it on its own if workforce-identity governance is in scope.</p>'+
     RECDATA.l2_governance.map(v=>recVendorRow(v, v.gov_native+'/'+v.gov_total+' governance use cases NATIVE')).join("")+'</div>';
  h+='<div class="card" style="border-left:4px solid var(--l2)"><h3>Top 4 recommendations — by role, not a league table</h3>'+
     RECDATA.top_picks.map((p,i)=>'<div style="padding:7px 0;border-bottom:1px solid #eee"><b>'+(i+1)+'. '+esc(p.role)+'</b> → <b>'+esc(p.pick)+'</b> '+recChip(p.residency,p.irap)+
       '<div style="font-size:11px;color:#666;margin-top:2px">'+esc(p.why)+'</div></div>').join("")+
     '<p class="note">Plus a paired <span class="lchip L0">L0</span> crypto substrate ('+esc(RECDATA.substrate.name)+') beneath the vault — a dependency, not a ranked pick (ADR-007).</p></div>';
  h+='<div class="card"><h3>Complementary stack — if you already run X, add Y</h3>'+
     '<table style="width:100%;border-collapse:collapse;font-size:12px"><thead><tr>'+
     '<th style="text-align:left;border-bottom:2px solid #ccc;padding:4px">You already have</th>'+
     '<th style="text-align:left;border-bottom:2px solid #ccc;padding:4px">Add to complement</th>'+
     '<th style="text-align:left;border-bottom:2px solid #ccc;padding:4px">Why</th></tr></thead><tbody>'+
     RECDATA.complementary.map(c=>'<tr>'+
       '<td style="padding:5px;border-bottom:1px solid #eee;vertical-align:top"><b>'+esc(c.have)+'</b></td>'+
       '<td style="padding:5px;border-bottom:1px solid #eee;vertical-align:top">'+esc(c.add)+'</td>'+
       '<td style="padding:5px;border-bottom:1px solid #eee;vertical-align:top" class="muted">'+esc(c.why)+'</td></tr>').join("")+
     '</tbody></table></div>';
  el.innerHTML=h;
}

// ---- business value ----
function renderValue(){
  const gaps=XYZ.filter(a=>a.anz_state==="GAP").length;
  const part=XYZ.filter(a=>a.anz_state==="PARTIAL").length;
  const pend=XYZ.filter(a=>a.anz_state==="PENDING").length;
  const targets=gaps+part+pend;
  const nf=UCS.filter(u=>/NON[_-]?FUNCTIONAL/i.test(u.category||"")).length;

  const steps=[["01","Assess","grade "+META.ucs+" capabilities vs E8 / Zero Trust / CPS 234 / ISM"],
    ["02","Prioritise","rank gaps by risk × regulatory weight"],
    ["03","Remediate","sequenced, owned roadmap actions"],
    ["04","Measure","KPIs on coverage &amp; gap-closure"],
    ["05","Re-assess","refresh the baseline, delta-tracked"]];
  const loop=steps.map(s=>'<div class="step"><div class="num">'+s[0]+'</div><b>'+esc(s[1])+'</b><span class="d">'+s[2]+'</span></div>').join('<div class="loparrow">&rarr;</div>');

  const LBL={hard:"Hard $",hours:"Hours",risk:"Risk",kpi:"KPI"};
  const outcomes=[
    ["hard","Rationalise tooling spend","The vendor matrix exposes overlapping vault / secrets tools running in parallel and gives a layer-scoped consolidation path.","Tool count &darr; · avoided licence + procurement effort"],
    ["hours","Audit &amp; compliance efficiency","A pre-built control-evidence pack (3-click framework &rarr; control &rarr; use case &rarr; evidence) answers APRA / ISM audits and cuts findings.","Audit hours &darr; · findings &darr; · avoided enforcement"],
    ["risk","Lower expected breach loss","Closing prioritised credential-access gaps (MITRE T1552) reduces the probability × impact of a machine-identity breach.","Gaps closed · risk-adjusted expected-loss &darr;"],
    ["kpi","Reduce operational toil","Dynamic credentials, just-in-time access and automated rotation remove manual secret handling and rotation-driven incidents.","Manual rotations &darr; · credential incidents &darr;"]];
  const ocards=outcomes.map(o=>'<div class="card ocard"><h3><span class="vtag '+o[0]+'">'+LBL[o[0]]+'</span> '+o[1]+'</h3>'+
    '<div class="mech">'+o[2]+'</div><div class="measure"><b>Measured by:</b> '+o[3]+'</div></div>').join("");

  const kpis=[
    ["NHI inventory completeness","% of machine identities discovered &amp; owner-attested","Inventory / attestation use cases","per cycle"],
    ["Rotation coverage &amp; freshness","% of secrets under managed rotation within SLA","Rotation / lifecycle use cases","monthly"],
    ["Gap-closure rate","assessed GAP / PARTIAL &rarr; MET over time","this assessment baseline","per cycle"],
    ["Plaintext secrets in repos","secrets detected in source &amp; history","pre-commit + history-scan use cases","continuous"],
    ["Tool consolidation","count of overlapping secrets / vault tools","vendor matrix","per cycle"]];
  const kpirows=kpis.map(k=>'<tr><td><b>'+k[0]+'</b></td><td class="muted">'+k[1]+'</td><td class="muted">'+k[2]+'</td><td class="mono">'+k[3]+'</td></tr>').join("");

  document.getElementById("value-body").innerHTML =
    '<div class="loop">'+loop+'</div>'+
    '<p class="muted" style="margin:8px 0 0">Current baseline feeds the loop: <b>'+targets+'</b> prioritised remediation targets ('+gaps+' GAP · '+part+' PARTIAL · '+pend+' PENDING) tracked to closure.</p>'+
    '<h3 class="vsec">Where the return comes from</h3>'+
    '<div class="grid2">'+ocards+'</div>'+
    '<h3 class="vsec">How it&rsquo;s measured — KPIs (underpinned by '+nf+' non-functional use cases)</h3>'+
    '<div class="card"><table class="kpitable"><thead><tr><th>KPI</th><th>What it measures</th><th>Source</th><th>Cadence</th></tr></thead><tbody>'+kpirows+'</tbody></table></div>'+
    '<div class="roi-banner"><b>Return is cost-avoidance, not new revenue.</b> The biggest single avoided event — one credential-driven breach, one regulatory enforcement action, or one duplicated vault platform — typically exceeds the whole assessment cost by an order of magnitude. Quantify against the institution&rsquo;s own baselines (current licences, audit effort, FAIR-style expected loss): this view supplies the metrics, not invented figures.</div>';
}

renderDashboard();
renderTable();
renderRecommendations();
renderValue();
</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("/*__DATA__*/[]", json.dumps(ranked, ensure_ascii=False))
        .replace("/*__XYZ__*/[]", json.dumps(anz, ensure_ascii=False))
        .replace("/*__UCS__*/[]", json.dumps(ucs, ensure_ascii=False))
        .replace("/*__NHIS__*/[]", json.dumps(nhis, ensure_ascii=False))
        .replace("/*__GLOSSARY__*/{}", json.dumps(GLOSSARY, ensure_ascii=False))
        .replace("/*__LAYERLABEL__*/{}", json.dumps(LAYER_LABEL, ensure_ascii=False))
        .replace("/*__SHORT__*/{}", json.dumps(SHORT, ensure_ascii=False))
        .replace("/*__REG__*/{}", json.dumps(REG, ensure_ascii=False))
        .replace("/*__REGDATA__*/{}", json.dumps(REGDATA, ensure_ascii=False))
        .replace("/*__RECDATA__*/{}", json.dumps(RECDATA, ensure_ascii=False))
        .replace("/*__META__*/{}", json.dumps(meta, ensure_ascii=False))
        .replace("__RV__", str(meta["ranked_vendors"]))
        .replace("__NHI__", str(meta["nhis"]))
        .replace("__UC__", str(meta["ucs"])))

if _ARGS.emit_data:
    with open(_ARGS.emit_data, "w", encoding="utf-8") as _ef:
        json.dump({"REGDATA": REGDATA, "RECDATA": RECDATA}, _ef,
                  ensure_ascii=False, sort_keys=True)

with open(DST, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {DST} ({os.path.getsize(DST)} bytes)")
print(f"Ranked vendors: {meta['ranked_vendors']}; ranked rows: {meta['ranked_rows']} (of {meta['total_rows']})")
print(f"UCs: {meta['ucs']}; NHIs: {meta['nhis']}; XYZ: {len(anz)}; REG-mapped UCs: {len(REG)}; glossary: {len(GLOSSARY)}")

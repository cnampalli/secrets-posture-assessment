"""Pure model transforms for the report (no I/O).

Turns the loaded inputs (+ the resolved engagement) into the REG/REGDATA/RECDATA/
GLOSSARY/meta structures the template consumes. No file or CSV access.
"""
from collections import defaultdict

import optimizer as _opt
import overlay as _ov
import resilience as _rz

APRA_FRAMEWORKS = {"apra-cps-234", "apra-cps-230", "apra-cpg-234"}
STATE_RANK = {"GAP": 0, "PARTIAL": 1, "PENDING": 2, "MET": 3, "UNKNOWN": 9}
ORDER = {"NATIVE": 0, "ADD-ON": 1, "PARTNER": 2, "GAP": 3, "N/A": 4}

# UC capability domains (from use-cases.csv) used to score domain strength.
REC_UC_DOMAIN = {
    "secrets": ["UC-F-001", "UC-F-002", "UC-F-003", "UC-F-005", "UC-F-006", "UC-F-007",
                "UC-F-008", "UC-F-010", "UC-F-012", "UC-F-015", "UC-F-016", "UC-F-018",
                "UC-F-020", "UC-F-026", "UC-N-003"],
    "governance": ["UC-F-017", "UC-F-025", "UC-F-027", "UC-N-002", "UC-N-004", "UC-N-006",
                   "UC-N-009", "UC-N-010", "UC-N-016", "UC-N-017", "UC-N-018", "UC-N-020"],
}


def build_glossary(nhis, ucs):
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


def compute_meta(all_rows, ranked, nhis, ucs):
    return {"ranked_vendors": len({r["vendor_slug"] for r in ranked}), "ranked_rows": len(ranked),
            "total_rows": len(all_rows), "nhis": len(nhis), "ucs": len(ucs)}


def build_regdata(reg_rows, anz, ucs, ranked, framework_labels, engagement, available):
    """Returns (REG, REGDATA): the per-UC APRA/ISM chips and the
    Framework -> Control -> UC -> Vendor-evidence cascade data."""
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

    fw_order, fw_seen = [], set()
    for r in reg_rows:
        if r["framework_slug"] not in fw_seen:
            fw_seen.add(r["framework_slug"]); fw_order.append(r["framework_slug"])
    fw_order = _ov.scope_frameworks(fw_order, engagement)
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
    for fw, controls in framework_controls.items():
        for c in controls:
            states = [state_by_uc.get(u, "UNKNOWN") for u in c["uc_ids"]]
            c["current_state"] = min(states, key=lambda s: STATE_RANK.get(s, 9)) if states else "UNKNOWN"
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
        "frameworks": [{"slug": s, "label": framework_labels.get(s, (s, ""))[0],
                        "subtitle": framework_labels.get(s, (s, ""))[1],
                        "control_count": len(framework_controls[s])} for s in fw_order],
        "controls": framework_controls, "ucs": uc_index, "vendor_uc": dict(vendor_uc),
        "framework_selection": {
            "selected": list(engagement.selected) if not engagement.is_default else list(available),
            "overlays": list(engagement.overlays),
            "baseline": list(engagement.baseline) if not engagement.is_default else [],
            "available": list(available),
        },
    }
    return REG, REGDATA


def build_vendormix(ranked, ownership, anchors, short):
    """Resilience-first vendor-mix + concentration model section (Phase 0).

    Separate from RECDATA (which stays frozen) — assembles the optimizer +
    parent-aware resilience analytics the report surfaces: minimal cover,
    white-space (C3), parent concentration scorecard (E5), single-source
    risk (E1, by parent), and data-driven complementary picks (C4).
    """
    cover = _opt.greedy_cover(ranked, ownership, resilience_first=True)
    uc_total = len(cover["covered"]) + len(cover["uncovered"])

    con = _rz.concentration(ranked, ownership)
    concentration = sorted(
        ({"parent": p, "name": short.get(p, p), "uc_count": c["uc_count"],
          "share": c["share"], "brands": [short.get(b, b) for b in c["brands"]],
          "sole_source_count": len(c["sole_source_ucs"]),
          "sole_source_ucs": c["sole_source_ucs"]}
         for p, c in con.items()),
        key=lambda d: (-d["share"], -d["uc_count"], d["parent"]))

    complementary = []
    for a in anchors:
        rec = _opt.complement(a, ranked)
        if rec:
            complementary.append({
                "have": short.get(a, a), "add": short.get(rec["add"], rec["add"]),
                "fills": rec["fills"], "still_open": rec["still_open"]})

    return {
        "cover": {
            "chosen": [{"slug": s, "name": short.get(s, s)} for s in cover["chosen"]],
            "covered_count": len(cover["covered"]), "uc_total": uc_total,
            "white_space": cover["uncovered"], "steps": cover["steps"],
        },
        "portfolio": _opt.portfolio_concentration(cover["chosen"], ranked, ownership),
        "concentration": concentration,
        "single_source": _rz.single_source(ranked, ownership)["single_source"],
        "complementary": complementary,
    }


def build_recdata(ranked, nhis, vendor_layer, short, vendor_residency, substrate_slug, engagement):
    secrets_ucs = set(REC_UC_DOMAIN["secrets"])
    gov_ucs = set(REC_UC_DOMAIN["governance"])

    def vendor_stat(slug):
        rows = [r for r in ranked if r["vendor_slug"] == slug]

        def dom(ucset):
            sel = [r for r in rows if r["target_type"] in ("UC-F", "UC-N") and r["target_id"] in ucset]
            nat = [r for r in sel if r["coverage"] == "NATIVE"]
            mats = [int(r["maturity"]) for r in nat if str(r["maturity"]).isdigit()]
            return len(nat), len(sel), (round(sum(mats) / len(mats), 1) if mats else 0)

        s_nat, s_tot, s_mat = dom(secrets_ucs)
        g_nat, g_tot, g_mat = dom(gov_ucs)
        nhi = [r for r in rows if r["target_type"] == "NHI"]
        res = vendor_residency.get(slug, {})
        return {
            "slug": slug, "name": short.get(slug, slug), "tier": vendor_layer[slug][1],
            "secrets_native": s_nat, "secrets_total": s_tot, "secrets_mat": s_mat,
            "gov_native": g_nat, "gov_total": g_tot, "gov_mat": g_mat,
            "nhi_native": sum(1 for r in nhi if r["coverage"] == "NATIVE"),
            "nhi_gap": sum(1 for r in nhi if r["coverage"] == "GAP"),
            "residency": res.get("residency", "?"), "irap": res.get("irap", "?"),
            "res_note": res.get("note", ""),
        }

    _l1 = [s for s, (lay, t) in vendor_layer.items() if lay == "L1" and t != "pki-mim"]
    _pki = [s for s, (lay, t) in vendor_layer.items() if lay == "L1" and t == "pki-mim"]
    _l2 = [s for s, (lay, t) in vendor_layer.items() if lay == "L2"]

    l1_secrets = sorted((vendor_stat(s) for s in _l1),
                        key=lambda v: _ov.vendor_sort_key(
                            engagement.residency_weight, v["residency"],
                            (-v["secrets_native"], -v["nhi_native"])))
    pki_mim = sorted((vendor_stat(s) for s in _pki),
                     key=lambda v: _ov.vendor_sort_key(
                         engagement.residency_weight, v["residency"],
                         (-v["secrets_native"],)))
    l2_governance = sorted((vendor_stat(s) for s in _l2),
                           key=lambda v: _ov.vendor_sort_key(
                               engagement.residency_weight, v["residency"],
                               (-v["gov_native"], -v["nhi_native"])))

    _primary = _ov.select_primary(l1_secrets, engagement.irap_required)
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

    return {
        "l1_secrets": l1_secrets, "pki_mim": pki_mim, "l2_governance": l2_governance,
        "top_picks": top_picks, "complementary": complementary,
        "coverage_proof": {"max_l1_nhi": max((v["nhi_native"] for v in l1_secrets), default=0),
                           "nhi_total": len(nhis)},
        "substrate": {"name": "Fortanix DSM / Thales SafeNet (XYZ migration)",
                      "note": vendor_residency.get(substrate_slug, {}).get("note", "")},
    }

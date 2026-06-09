"""Pure model transforms for the report (no I/O).

Turns the loaded inputs (+ the resolved engagement) into the REG/REGDATA/RECDATA/
GLOSSARY/meta structures the template consumes. No file or CSV access.
"""
import csv as _csv
import os as _os
from collections import defaultdict

import compliance as _cmp
import optimizer as _opt
import overlay as _ov
import resilience as _rz
import vendor_intel as _vi
from matrix_vocab import COVERAGE_ORDER as ORDER, STATE_RANK, UC_TYPES

APRA_FRAMEWORKS = {"apra-cps-234", "apra-cps-230", "apra-cpg-234"}

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


_EVIDENCE_COMPLIANCE_ROLES = {"PRIMARY-LENS", "BACK-MAP"}


def build_control_evidence(reg_rows, evidence_catalog):
    """Resolve each control's regulatory evidence pack and the reverse
    'one artifact -> many controls' index. Compliance-role rows only.

    Returns {"by_control": {control_code: [item,...]}, "index": [item,...]} where
    each item carries the catalog fields plus `satisfies` (sorted control codes that
    reference it); index items also carry `uc_count` (distinct UCs across those
    controls). Empty/absent catalog -> empty maps (the secrets domain ships none)."""
    catalog = {(r.get("ev_id") or "").strip(): r for r in (evidence_catalog or [])
               if (r.get("ev_id") or "").strip()}
    if not catalog:
        return {"by_control": {}, "index": []}

    ev_controls = defaultdict(set)      # ev_id -> {control_code,...}
    ev_ucs = defaultdict(set)           # ev_id -> {uc_id,...}
    control_evids = defaultdict(list)   # control_code -> [ev_id,...] (dedup, in row order)
    for r in reg_rows:
        if (r.get("framework_role") or "").strip() not in _EVIDENCE_COMPLIANCE_ROLES:
            continue
        cc = (r.get("control_code") or "").strip()
        ucs_here = [u.strip() for u in (r.get("uc_ids") or "").split(";") if u.strip()]
        for ev in (e.strip() for e in (r.get("evidence_item_ids") or "").split(";") if e.strip()):
            if ev not in catalog:
                continue            # the F-gate guarantees resolution; skip defensively
            ev_controls[ev].add(cc)
            ev_ucs[ev].update(ucs_here)
            if ev not in control_evids[cc]:
                control_evids[cc].append(ev)

    def item(ev):
        r = catalog[ev]
        return {"ev_id": ev, "requirement": r.get("requirement", ""),
                "dimension": (r.get("dimension") or "").strip(),
                "tier": (r.get("tier") or "").strip(),
                "example_artifact": r.get("example_artifact", ""),
                "sensitivity_tag": r.get("sensitivity_tag", ""),
                "satisfies": sorted(ev_controls[ev])}

    def primary_first(ev):
        return (0 if (catalog[ev].get("tier") or "").strip() == "primary" else 1, ev)

    by_control = {cc: [item(e) for e in sorted(evids, key=primary_first)]
                  for cc, evids in control_evids.items()}
    index = []
    for ev in sorted(ev_controls, key=lambda e: (-len(ev_controls[e]), e)):
        it = item(ev)
        it["uc_count"] = len(ev_ucs[ev])
        index.append(it)
    return {"by_control": by_control, "index": index}


def build_regdata(reg_rows, anz, ucs, ranked, framework_labels, engagement, available,
                  evidence_catalog=None):
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
    evidence = build_control_evidence(reg_rows, evidence_catalog)
    for fw, controls in framework_controls.items():
        for c in controls:
            states = [state_by_uc.get(u, "UNKNOWN") for u in c["uc_ids"]]
            c["current_state"] = min(states, key=lambda s: STATE_RANK.get(s, 9)) if states else "UNKNOWN"
            c["evidence"] = evidence["by_control"].get(c["code"], [])
    vendor_uc = defaultdict(list)
    for r in ranked:
        if r["target_type"] not in UC_TYPES:
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
        "evidence_index": evidence["index"],
        "framework_selection": {
            "selected": list(engagement.selected) if not engagement.is_default else list(available),
            "overlays": list(engagement.overlays),
            "baseline": list(engagement.baseline) if not engagement.is_default else [],
            "available": list(available),
        },
    }
    return REG, REGDATA


def build_compliance(reg_rows, anz, framework_labels, gap_limit=15, exclude=frozenset()):
    """Identity-control coverage indicator (D3) + gap-to-target list (D4).

    Separate additive model section. Coverage is against the identity-scoped
    control set — an indicator, not a full-framework compliance score.
    `exclude` is the set of informative frameworks (e.g. MITRE ATT&CK — adversary
    TTPs, not controls a posture can be "MET" against); the caller supplies it
    from the domain descriptor (domain.informative_frameworks) — it is not
    hardcoded here, so each domain owns its own informative set.
    """
    rows = [r for r in reg_rows if r.get("framework_slug") not in exclude]
    ind = _cmp.coverage_indicator(rows, anz)
    frameworks = sorted(
        ({"slug": fw, "label": framework_labels.get(fw, (fw, ""))[0],
          "subtitle": framework_labels.get(fw, (fw, ""))[1], **stats}
         for fw, stats in ind.items()),
        key=lambda d: (-d["met_pct"], d["slug"]))
    return {"frameworks": frameworks,
            "gap_to_target": _cmp.gap_to_target(rows, anz)[:gap_limit]}


def build_vendor_intel(ranked, ucs, chosen_slugs, short, evidence_len=160):
    """Best-vendor-per-UC feature matrix (B2/B3) + head-to-head (B4).

    best_per_uc: the leading provider for each UC with its coverage, maturity,
    count of alternatives, and the evidence quote (the B3 differentiator).
    head_to_head: a compact per-UC grid for the chosen vendor mix, scoped to
    P0-priority UCs to stay legible.
    """
    best_per_uc = []
    for u in ucs:
        prov = _vi.best_for(u["uc_id"], ranked)
        if not prov:
            continue
        top = prov[0]
        best_per_uc.append({
            "uc": u["uc_id"], "title": u.get("short_title", ""),
            "vendor": short.get(top["vendor_slug"], top["vendor_name"]),
            "coverage": top["coverage"], "maturity": top["maturity"],
            "alternatives": len(prov) - 1,
            "evidence": (top["evidence_quote"] or "")[:evidence_len],
        })
    p0 = [u["uc_id"] for u in ucs if u.get("priority_fi") == "P0"]
    grid = _vi.head_to_head(chosen_slugs, ranked, uc_ids=p0) if p0 else {}
    return {"best_per_uc": best_per_uc,
            "head_to_head": {"uc_ids": p0, "vendors": chosen_slugs, "grid": grid}}


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


# IGA is process-shaped: the NATIVE/ADD-ON per-use-case capability matrix
# (build_vendormix) does NOT fit it. IGA is assessed per governance AREA instead.
IGA_AREAS = ["JML", "Certification", "SoD", "Role/Request"]


def build_iga_vendor_fit(data_dir, fit_csv="iga-vendor-fit.csv"):
    """Bespoke per-AREA vendor-fit grid for IGA (Phase 3).

    Reads `<data_dir>/iga-vendor-fit.csv` (cols: vendor, vendor_slug, area, fit,
    justification, evidence_url, citation_keys) into an ordered vendors × areas
    grid suitable for HTML rendering. fit ∈ {NATIVE, PARTIAL, ADD-ON}. Vendors
    keep first-seen (data) order; areas are pinned to IGA_AREAS. Each cell carries
    {fit, justification, evidence_url, citation_keys} — the honest PARTIAL
    rationale and the Saviynt marketing-grade caveat survive verbatim.

    This is the IGA analogue of build_vendormix; the two are mutually exclusive
    (a domain renders one or the other, never both)."""
    path = _os.path.join(data_dir, fit_csv)
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(_csv.DictReader(fh))

    order = []                                  # vendors in first-seen order
    cells = defaultdict(dict)                   # vendor -> {area -> cell}
    slug_of = {}
    for r in rows:
        vendor = (r.get("vendor") or "").strip()
        area = (r.get("area") or "").strip()
        # Fail loudly on a mistyped/unknown non-blank area rather than silently
        # dropping the row (which would render a blank cell and hide the typo). A
        # blank area is not a typo signal — it's simply not a governance-area cell.
        if area and area not in IGA_AREAS:
            raise ValueError(
                f"Unrecognized IGA area {area!r} for vendor {vendor!r}; "
                f"expected one of {IGA_AREAS}")
        if not vendor or area not in IGA_AREAS:
            continue
        if vendor not in cells:
            order.append(vendor)
        slug_of.setdefault(vendor, (r.get("vendor_slug") or "").strip())
        cells[vendor][area] = {
            "fit": (r.get("fit") or "").strip(),
            "justification": (r.get("justification") or "").strip(),
            "evidence_url": (r.get("evidence_url") or "").strip(),
            "citation_keys": (r.get("citation_keys") or "").strip(),
        }

    vendors = [{
        "vendor": v, "vendor_slug": slug_of.get(v, ""),
        "cells": {a: cells[v].get(a, {"fit": "", "justification": "",
                                      "evidence_url": "", "citation_keys": ""})
                  for a in IGA_AREAS},
    } for v in order]
    return {"areas": list(IGA_AREAS), "vendors": vendors}


def build_recdata(ranked, nhis, vendor_layer, short, vendor_residency, substrate_slug, engagement):
    secrets_ucs = set(REC_UC_DOMAIN["secrets"])
    gov_ucs = set(REC_UC_DOMAIN["governance"])

    def vendor_stat(slug):
        rows = [r for r in ranked if r["vendor_slug"] == slug]

        def dom(ucset):
            sel = [r for r in rows if r["target_type"] in UC_TYPES and r["target_id"] in ucset]
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

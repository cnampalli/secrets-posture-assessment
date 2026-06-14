"""Cross-domain identity spine — pure model helpers (no rendering, no validation).

Loads the canonical archetype registry (config/identity-spine.yaml) and projects every
domain's identity catalog onto it, so the same logical identity modelled in secrets / PAM /
IGA surfaces as ONE archetype seen through each domain's lens. The registry's honesty
contract (anchors present, ids unique, class enum) is enforced by validate_data, not here.
"""
import os

import yaml

# Sentinel `spine_id` for catalog rows that are not identities (credentials, attributes).
NOT_AN_IDENTITY = "NOT-AN-IDENTITY"

# How each domain "sees" an identity — surfaced as the spine matrix column lens.
DOMAIN_LENS = {
    "secrets": "credential issuance & rotation",
    "pam": "privileged session brokering",
    "iga": "lifecycle & certification",
}


def load_spine(cfgdir):
    """Read identity-spine.yaml from `cfgdir`. Returns
    {archetypes: [..], by_id: {spine_id: archetype}, basis: str}. Missing file -> empty
    (the validator turns an empty registry into a build failure)."""
    path = os.path.join(cfgdir, "identity-spine.yaml")
    if not os.path.exists(path):
        return {"archetypes": [], "by_id": {}, "basis": ""}
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    archetypes = doc.get("archetypes") or []
    return {"archetypes": archetypes,
            "by_id": {a.get("spine_id"): a for a in archetypes},
            "basis": doc.get("basis", "")}


def build_spine_view(domains_identities, spine):
    """Project per-domain identities onto the archetype registry (pure).

    `domains_identities` is [{slug, label, identities:[{spine_id, short_name, ...}]}] for
    EVERY domain (identity catalogs exist for all domains, so IGA is included — the
    matrix-less vendor skip does not apply here). Returns
    {archetypes:[{spine_id,label,identity_class,privileged,csa_nhi_anchor,spiffe_ref,
                  by_domain:{slug:[short_name..]}, span}],
     cross_domain:[archetypes span>=2], classes:{human,npe,agentic}, unmapped:[span 0],
     lens:{slug:lens}}.
    Rows carrying the NOT-AN-IDENTITY sentinel are skipped (never surface under an archetype)."""
    # accumulate short_names per archetype per domain
    by_arch = {a["spine_id"]: {d["slug"]: [] for d in domains_identities}
               for a in spine["archetypes"]}
    for d in domains_identities:
        for ident in d.get("identities", []):
            sid = (ident.get("spine_id") or "").strip()
            if sid == NOT_AN_IDENTITY or sid not in by_arch:
                continue
            by_arch[sid][d["slug"]].append(ident.get("short_name", ""))

    archetypes, classes = [], {"human": 0, "npe": 0, "agentic": 0}
    for a in spine["archetypes"]:
        by_domain = {slug: names for slug, names in by_arch[a["spine_id"]].items() if names}
        span = len(by_domain)
        classes[a["identity_class"]] = classes.get(a["identity_class"], 0) + 1
        archetypes.append({
            "spine_id": a["spine_id"],
            "label": a["label"],
            "identity_class": a["identity_class"],
            "privileged": a["privileged"],
            "csa_nhi_anchor": a.get("csa_nhi_anchor", ""),
            "spiffe_ref": a.get("spiffe_ref", ""),
            "by_domain": by_domain,
            "span": span,
        })
    return {
        "archetypes": archetypes,
        "cross_domain": [a for a in archetypes if a["span"] >= 2],
        "classes": classes,
        "unmapped": [a for a in archetypes if a["span"] == 0],
        "lens": {d["slug"]: DOMAIN_LENS.get(d["slug"], d["slug"]) for d in domains_identities},
    }

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import identity_spine  # noqa: E402
import validate_data  # noqa: E402

CFGDIR = os.path.join(MATRIX, "config")


# ---- load_spine ----

def test_load_spine_parses_registry():
    spine = identity_spine.load_spine(CFGDIR)
    assert len(spine["archetypes"]) >= 10
    # index keyed by spine_id
    first = spine["archetypes"][0]
    assert spine["by_id"][first["spine_id"]] is first


def test_load_spine_has_all_three_classes():
    spine = identity_spine.load_spine(CFGDIR)
    classes = {a["identity_class"] for a in spine["archetypes"]}
    assert classes == {"human", "npe", "agentic"}


# ---- check_identity_spine_registry ----

def _spine(archetypes):
    return {"archetypes": archetypes, "by_id": {a["spine_id"]: a for a in archetypes}}


_GOOD = [
    {"spine_id": "SPN-001", "label": "Privileged human administrator", "identity_class": "human",
     "privileged": True, "description": "x", "csa_nhi_anchor": "NIST AC-6", "spiffe_ref": ""},
    {"spine_id": "SPN-007", "label": "Cloud / workload identity", "identity_class": "npe",
     "privileged": False, "description": "y", "csa_nhi_anchor": "CSA NHI: cloud workload",
     "spiffe_ref": "SPIFFE SVID"},
]


def test_registry_clean_passes():
    assert validate_data.check_identity_spine_registry(_spine(_GOOD)) == []


def test_registry_missing_file_fails():
    errs = validate_data.check_identity_spine_registry({"archetypes": [], "by_id": {}})
    assert len(errs) == 1 and "missing" in errs[0].lower()


def test_registry_duplicate_id_fails():
    dup = _GOOD + [dict(_GOOD[0])]
    errs = validate_data.check_identity_spine_registry(_spine(dup))
    assert any("SPN-001" in e and "duplicate" in e.lower() for e in errs)


def test_registry_bad_class_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-099", identity_class="robot")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("identity_class" in e for e in errs)


def test_registry_non_bool_privileged_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-098", privileged="yes")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("privileged" in e for e in errs)


def test_registry_missing_anchor_fails():
    bad = [dict(_GOOD[1], spine_id="SPN-097", csa_nhi_anchor="")]
    errs = validate_data.check_identity_spine_registry(_spine(bad))
    assert any("csa_nhi_anchor" in e for e in errs)


# ---- check_identity_spine_mapping ----

def test_mapping_clean_passes():
    spine = identity_spine.load_spine(CFGDIR)
    rows = [{"nhi_id": "X-1", "spine_id": "SPN-001"},
            {"nhi_id": "X-2", "spine_id": identity_spine.NOT_AN_IDENTITY}]
    assert validate_data.check_identity_spine_mapping(rows, spine) == []


def test_mapping_empty_spine_id_fails():
    spine = identity_spine.load_spine(CFGDIR)
    errs = validate_data.check_identity_spine_mapping([{"nhi_id": "X-3", "spine_id": ""}], spine)
    assert len(errs) == 1 and "X-3" in errs[0]


def test_mapping_unknown_spine_id_fails():
    # injection: a bogus archetype id must be rejected
    spine = identity_spine.load_spine(CFGDIR)
    errs = validate_data.check_identity_spine_mapping(
        [{"nhi_id": "X-4", "spine_id": "SPN-999"}], spine)
    assert len(errs) == 1 and "SPN-999" in errs[0]


# ---- build_spine_view ----

_VIEW_SPINE = _spine([
    {"spine_id": "SPN-001", "label": "Priv admin", "identity_class": "human", "privileged": True,
     "csa_nhi_anchor": "NIST AC-6", "spiffe_ref": ""},
    {"spine_id": "SPN-009", "label": "Service account", "identity_class": "npe", "privileged": False,
     "csa_nhi_anchor": "CSA NHI: service accounts", "spiffe_ref": ""},
    {"spine_id": "SPN-015", "label": "Agentic agent", "identity_class": "agentic", "privileged": False,
     "csa_nhi_anchor": "CSA NHI emerging", "spiffe_ref": ""},
])

_VIEW_DOMAINS = [
    {"slug": "secrets", "label": "Secrets", "identities": [
        {"spine_id": "SPN-009", "short_name": "DB svc acct"},
        {"spine_id": "SPN-009", "short_name": "AD svc acct"},
        {"spine_id": "NOT-AN-IDENTITY", "short_name": "TDE key custodian"}]},
    {"slug": "pam", "label": "PAM", "identities": [
        {"spine_id": "SPN-001", "short_name": "Domain admin"},
        {"spine_id": "SPN-009", "short_name": "Generic svc acct"}]},
    {"slug": "iga", "label": "IGA", "identities": [
        {"spine_id": "SPN-015", "short_name": "Agentic-AI agent"}]},
]


def test_view_by_domain_and_span():
    v = identity_spine.build_spine_view(_VIEW_DOMAINS, _VIEW_SPINE)
    sa = next(a for a in v["archetypes"] if a["spine_id"] == "SPN-009")
    assert sa["by_domain"] == {"secrets": ["DB svc acct", "AD svc acct"], "pam": ["Generic svc acct"]}
    assert sa["span"] == 2


def test_view_cross_domain_filter():
    v = identity_spine.build_spine_view(_VIEW_DOMAINS, _VIEW_SPINE)
    cross = {a["spine_id"] for a in v["cross_domain"]}
    assert cross == {"SPN-009"}          # only the service account spans >=2 domains


def test_view_sentinel_never_surfaces():
    v = identity_spine.build_spine_view(_VIEW_DOMAINS, _VIEW_SPINE)
    blob = repr(v)
    assert "TDE key custodian" not in blob and "NOT-AN-IDENTITY" not in blob


def test_view_class_rollup_and_lens():
    v = identity_spine.build_spine_view(_VIEW_DOMAINS, _VIEW_SPINE)
    assert v["classes"] == {"human": 1, "npe": 1, "agentic": 1}
    assert v["lens"]["iga"] == "lifecycle & certification"


def test_view_on_real_data_links_service_account_across_domains():
    # the live registry + catalogs: the application/service-account archetype must span
    # all three domains (the 'same service account modelled 3x' the spine resolves)
    import os, sys, csv as _csv
    spine = identity_spine.load_spine(CFGDIR)
    doms = []
    for slug in ("secrets", "pam", "iga"):
        path = os.path.join(MATRIX, "domains", slug, "identity-catalog.csv")
        with open(path, encoding="utf-8") as fh:
            rows = [{"spine_id": r["spine_id"], "short_name": r["short_name"]}
                    for r in _csv.DictReader(fh)]
        doms.append({"slug": slug, "label": slug, "identities": rows})
    v = identity_spine.build_spine_view(doms, spine)
    sa = next(a for a in v["archetypes"] if a["spine_id"] == "SPN-009")
    assert sa["span"] == 3               # secrets + pam + iga all map a service account

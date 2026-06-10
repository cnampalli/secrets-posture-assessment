"""Phase 1: per-domain descriptor — the secrets domain expressed as config."""
import pytest

import domains


def test_secrets_maps_are_immutable_but_copyable():
    d = domains.SECRETS
    # in-place mutation of a domain's maps must fail (no silent cross-domain corruption)
    with pytest.raises((TypeError, AttributeError)):
        d.vendor_layer["x"] = ("L9", "z")
    with pytest.raises((TypeError, AttributeError)):
        d.short["x"] = "X"
    # building a new domain from a copy still works
    m = dict(d.vendor_layer)
    m["x"] = ("L9", "z")
    assert m["x"] == ("L9", "z") and "x" not in d.vendor_layer


def test_registry_has_secrets():
    assert "secrets" in domains.DOMAINS
    assert domains.DOMAINS["secrets"] is domains.SECRETS


def test_secrets_carries_legacy_vendor_maps():
    d = domains.SECRETS
    assert d.substrate_slug == "fortanix-dsm"
    assert d.vendor_layer["hashicorp-vault-enterprise"] == ("L1", "core")
    assert d.short["hashicorp-vault-enterprise"] == "Vault Ent"
    assert set(d.layer_label) == {"L1", "L2"}
    assert len(d.vendor_layer) == 19          # 18 ranked vendors + the L0 substrate


def test_anchors_tier_selects_cloud_native_vendors():
    d = domains.SECRETS
    anchors = {s for s, (lay, t) in d.vendor_layer.items() if t == d.anchors_tier}
    assert anchors == {"aws-secrets-manager", "azure-key-vault",
                       "gcp-secret-manager", "akeyless"}


def test_informative_frameworks_is_domain_config():
    assert domains.SECRETS.informative_frameworks == frozenset({"mitre-attack"})


def test_data_filenames_present():
    d = domains.SECRETS
    assert d.vendor_capabilities == "vendor-capabilities.csv"
    assert d.use_cases == "use-cases.csv"
    assert d.identity_catalog == "identity-catalog.csv"
    assert d.regulatory_trace == "regulatory-trace.csv"
    assert d.default_current_state == "current-state.csv"


def test_secrets_report_labels_reproduce_current_text():
    d = domains.SECRETS
    assert d.report_title == "XYZ Secrets-Management — Stakeholder Report (PRD v0.1)"
    assert d.report_heading == "XYZ Secrets-Management — Stakeholder Report"
    assert d.object_singular == "identity"      # nav: "By identity"
    assert d.object_plural == "identities"      # subtitle: "… identities …"
    assert d.substrate_note == " (+ a Layer-0 crypto-substrate dependency)"


def test_secrets_uses_legacy_recdata_pam_does_not():
    # The legacy RECDATA recommendations (build_recdata) are secrets-specific and
    # frozen; non-secrets domains render the domain-agnostic Phase 0 sections instead.
    assert domains.SECRETS.legacy_recdata is True
    assert domains.PAM.legacy_recdata is False


def test_pam_domain_registered_and_substrateless():
    assert domains.DOMAINS["pam"] is domains.PAM
    d = domains.PAM
    assert d.substrate_slug == ""            # PAM has no L0 crypto substrate
    assert d.substrate_note == ""            # so no subtitle parenthetical
    assert d.informative_frameworks == frozenset()   # PAM trace has no mitre-attack lens


def test_pam_vendor_layer_and_anchors():
    d = domains.PAM
    # every vendor in the PAM capability data must be mapped (loader errors otherwise)
    assert set(d.vendor_layer) == {"cyberark-pam", "delinea", "beyondtrust",
                                   "one-identity-safeguard", "wallix-bastion", "teleport"}
    # anchors seed the complement view — the established suites, not the modern challenger
    anchors = {s for s, (lay, t) in d.vendor_layer.items() if t == d.anchors_tier}
    assert "teleport" not in anchors and len(anchors) == 5
    assert d.short["cyberark-pam"] == "CyberArk"


def test_pam_report_labels():
    d = domains.PAM
    assert "Privileged Access" in d.report_title
    assert d.object_singular == "privileged identity"
    assert d.object_plural == "privileged identities"


def test_iga_domain_registered_and_substrateless():
    assert "iga" in domains.DOMAINS
    assert domains.DOMAINS["iga"] is domains.IGA
    d = domains.IGA
    assert d.label == "Identity Governance & Administration"
    assert d.substrate_slug == ""            # IGA has no L0 crypto substrate
    assert d.substrate_note == ""            # so no subtitle parenthetical
    assert d.anchors_tier == "suite"
    assert d.posture_noun == "identity-governance"
    assert d.legacy_recdata is False
    # THREAT-CONTEXT framings are informative-only, not compliance obligations
    assert d.informative_frameworks == frozenset({"mitre-attack", "ms-incident", "owasp-llm"})


def test_iga_vendor_layer_and_shorts():
    d = domains.IGA
    assert set(d.vendor_layer) == {"sailpoint-isc", "saviynt-eic",
                                   "microsoft-entra-idg", "okta-oig"}
    # IGA uses a single "suite" layer for all four platforms (fit is per-area)
    assert all(lay == "L1" and tier == "suite"
               for lay, tier in d.vendor_layer.values())
    assert d.short["saviynt-eic"] == "Saviynt"
    assert d.short["okta-oig"] == "Okta"


def test_report_meta_is_single_source_token_map():
    # Phase 1 #3: the report-label token map is built in ONE place (off the
    # descriptor), so the orchestrator can't hand-assemble a drifting dict and
    # render() has an explicit contract to read from.
    d = domains.SECRETS
    assert d.report_meta() == {
        "title": d.report_title,
        "heading": d.report_heading,
        "object_singular": d.object_singular,
        "object_plural": d.object_plural,
        "substrate_note": d.substrate_note,
    }

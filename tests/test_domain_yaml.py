"""Phase 1 #8 — `Domain` loadable from per-domain YAML (project convention keeps
config in YAML so analysts can add a domain without code).

Coverage split (the descriptors are now YAML-sourced, so `domains.SECRETS` *is* a
load of `secrets.yaml`):
  * `*_round_trips_through_registry` — `load_domain(file)` is deterministic and the
    module registry exposes the same instance (loader + registry contract).
  * `*_anchors_to_historical_values` — hardcoded literals pin the YAML to the exact
    values the deleted Python descriptor carried, independent of the module, so a
    YAML edit that drifts a label / map / flag is caught here (and in test_domains.py).
  * read-only maps / tuple coercion — the in-memory invariants YAML can't express.
"""
import os

import pytest

from matrix import domains

CONFIG_DIR = os.path.join(domains.HERE, "config", "domains")


def test_secrets_round_trips_through_registry():
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "secrets.yaml"))
    assert loaded == domains.SECRETS
    assert domains.DOMAINS["secrets"] is domains.SECRETS


def test_pam_round_trips_through_registry():
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "pam.yaml"))
    assert loaded == domains.PAM
    assert domains.DOMAINS["pam"] is domains.PAM


def test_iga_round_trips_through_registry():
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "iga.yaml"))
    assert loaded == domains.IGA
    assert domains.DOMAINS["iga"] is domains.IGA


def test_secrets_yaml_anchors_to_historical_values():
    """Independent pin to the values the hand-written Python SECRETS descriptor
    carried — does NOT route through domains.SECRETS (which is itself YAML-loaded),
    so a drift in secrets.yaml fails here rather than passing both operands."""
    d = domains.load_domain(os.path.join(CONFIG_DIR, "secrets.yaml"))
    assert d.label == "Secrets management / NHI"
    assert d.report_heading == "XYZ Secrets-Management — Stakeholder Report"
    assert d.substrate_slug == "fortanix-dsm"
    assert d.anchors_tier == "cloud-native"
    assert d.vendor_layer["hashicorp-vault-enterprise"] == ("L1", "core")
    assert d.short["hashicorp-vault-enterprise"] == "Vault Ent"
    assert len(d.vendor_layer) == 19
    assert d.informative_frameworks == frozenset({"mitre-attack"})
    assert d.legacy_recdata is True


def test_pam_yaml_anchors_to_historical_values():
    d = domains.load_domain(os.path.join(CONFIG_DIR, "pam.yaml"))
    assert d.label == "Privileged Access Management"
    assert d.report_heading == "Privileged Access Management — Vendor Selection"
    assert d.substrate_slug == ""
    assert d.anchors_tier == "suite"
    assert set(d.vendor_layer) == {"cyberark-pam", "delinea", "beyondtrust",
                                   "one-identity-safeguard", "wallix-bastion", "teleport"}
    assert d.short["cyberark-pam"] == "CyberArk"
    assert d.informative_frameworks == frozenset()
    assert d.legacy_recdata is False


def test_iga_yaml_anchors_to_historical_values():
    d = domains.load_domain(os.path.join(CONFIG_DIR, "iga.yaml"))
    assert d.label == "Identity Governance & Administration"
    assert d.report_heading == "Identity Governance & Administration — Vendor Selection"
    assert d.object_singular == "identity"
    assert d.posture_noun == "identity-governance"
    assert d.substrate_slug == ""
    assert d.anchors_tier == "suite"
    assert set(d.vendor_layer) == {"sailpoint-isc", "saviynt-eic",
                                   "microsoft-entra-idg", "okta-oig"}
    assert d.vendor_layer["sailpoint-isc"] == ("L1", "suite")
    assert d.vendor_layer["okta-oig"] == ("L1", "suite")
    assert d.short["sailpoint-isc"] == "SailPoint"
    assert d.short["microsoft-entra-idg"] == "Microsoft Entra"
    # THREAT-CONTEXT framings are informative-only, not compliance obligations
    assert d.informative_frameworks == frozenset({"mitre-attack", "ms-incident", "owasp-llm"})
    assert d.legacy_recdata is False


def test_loaded_domain_maps_are_read_only():
    """Maps come back as the same read-only _FrozenDict the Python descriptor uses,
    so a domain built by copy-edit can't corrupt the source."""
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "secrets.yaml"))
    with pytest.raises(TypeError):
        loaded.vendor_layer["x"] = ("L9", "bogus")


def test_loaded_domain_vendor_layer_values_are_tuples():
    """vendor_layer values stay (layer, tier) tuples — not YAML lists — so they
    compare equal to the Python descriptor and json-serialise identically."""
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "secrets.yaml"))
    for slug, val in loaded.vendor_layer.items():
        assert isinstance(val, tuple), f"{slug} layer value should be a tuple"

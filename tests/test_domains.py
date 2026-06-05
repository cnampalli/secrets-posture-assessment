"""Phase 1: per-domain descriptor — the secrets domain expressed as config."""
import domains


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

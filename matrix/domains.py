"""Per-domain descriptors — the secrets-specific seams expressed as config (Phase 1).

The engine (loader, model builders, report) is domain-agnostic; everything that
made it *secrets-specific* — the data filenames, the vendor layer/short/label maps,
the L0 substrate, the complementary-anchor tier, and which frameworks are
informative-only — lives in a `Domain` descriptor here. Adding PAM / IGA becomes a
new `Domain` + data, not new code (validated by the Phase 0.5 PAM spike).
"""
import os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))


class _FrozenDict(dict):
    """A read-only dict: a Domain's maps can't be mutated in place, so a new
    domain built by copy-edit (`dict(SECRETS.vendor_layer)`) can't silently
    corrupt the source. Still a `dict` subclass, so json.dumps serialises it."""

    def _ro(self, *_a, **_k):
        raise TypeError("Domain maps are read-only; copy with dict(...) to derive a new domain")

    __setitem__ = __delitem__ = update = setdefault = pop = popitem = clear = _ro


# --- secrets / NHI domain constants (moved verbatim from report_io) ---
_SECRETS_SUBSTRATE = "fortanix-dsm"

_SECRETS_VENDOR_LAYER = {
    _SECRETS_SUBSTRATE: ("L0", "data-security"),
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
_SECRETS_SHORT = {
    "hashicorp-vault-enterprise": "Vault Ent", "cyberark-conjur": "Conjur",
    "cyberark-pam": "CyberArk PAM", "delinea-secret-server": "Delinea",
    "aws-secrets-manager": "AWS SM", "azure-key-vault": "Azure KV",
    "gcp-secret-manager": "GCP SM", "akeyless": "AKEYLESS", "doppler": "Doppler",
    "infisical": "Infisical", "1password-secrets-automation": "1Password",
    "venafi": "Venafi", "keyfactor": "Keyfactor", "astrix-security": "Astrix",
    "entro-security": "Entro", "oasis-security": "Oasis", "aembit": "Aembit",
    "clutch-security": "Clutch",
}
_SECRETS_LAYER_LABEL = {
    "L1": "L1 · Secrets management (the vault tier) — NATIVE = brokers / stores / rotates secrets",
    "L2": "L2 · NHI discovery / governance (above the vault) — NATIVE = discovers / governs (not brokers)",
}


@dataclass(frozen=True)
class Domain:
    """Everything the engine needs to assess one domain. Data + config, no code."""
    slug: str
    label: str
    data_dir: str
    # CSV filenames (relative to data_dir)
    vendor_capabilities: str
    use_cases: str
    identity_catalog: str
    regulatory_trace: str
    default_current_state: str
    # vendor classification maps
    vendor_layer: dict
    short: dict
    layer_label: dict
    substrate_slug: str
    # analysis policy
    anchors_tier: str                       # vendor tier that seeds complementary picks
    informative_frameworks: frozenset = field(default_factory=frozenset)
    # report labels (domain-identifying copy in the template)
    report_title: str = ""
    report_heading: str = ""
    object_singular: str = "identity"       # nav noun, e.g. "By identity"
    object_plural: str = "identities"       # subtitle noun
    substrate_note: str = ""                # subtitle parenthetical when a substrate exists


SECRETS = Domain(
    slug="secrets",
    label="Secrets management / NHI",
    data_dir=HERE,
    vendor_capabilities="vendor-capabilities.csv",
    use_cases="use-cases.csv",
    identity_catalog="identity-catalog.csv",
    regulatory_trace="regulatory-trace.csv",
    default_current_state="current-state.csv",
    vendor_layer=_FrozenDict(_SECRETS_VENDOR_LAYER),
    short=_FrozenDict(_SECRETS_SHORT),
    layer_label=_FrozenDict(_SECRETS_LAYER_LABEL),
    substrate_slug=_SECRETS_SUBSTRATE,
    anchors_tier="cloud-native",
    informative_frameworks=frozenset({"mitre-attack"}),
    report_title="XYZ Secrets-Management — Stakeholder Report (PRD v0.1)",
    report_heading="XYZ Secrets-Management — Stakeholder Report",
    object_singular="identity",
    object_plural="identities",
    substrate_note=" (+ a Layer-0 crypto-substrate dependency)",
)

DOMAINS = {SECRETS.slug: SECRETS}

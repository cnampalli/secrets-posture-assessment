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


# --- business-value tab content (per-domain; reproduces the former hardcoded copy) ---
_SECRETS_VALUE = {
    "outcomes": [
        ["hard", "Rationalise tooling spend", "The vendor matrix exposes overlapping vault / secrets tools running in parallel and gives a layer-scoped consolidation path.", "Tool count &darr; · avoided licence + procurement effort"],
        ["hours", "Audit &amp; compliance efficiency", "A pre-built control-evidence pack (3-click framework &rarr; control &rarr; use case &rarr; evidence) answers APRA / ISM audits and cuts findings.", "Audit hours &darr; · findings &darr; · avoided enforcement"],
        ["risk", "Lower expected breach loss", "Closing prioritised credential-access gaps (MITRE T1552) reduces the probability × impact of a machine-identity breach.", "Gaps closed · risk-adjusted expected-loss &darr;"],
        ["kpi", "Reduce operational toil", "Dynamic credentials, just-in-time access and automated rotation remove manual secret handling and rotation-driven incidents.", "Manual rotations &darr; · credential incidents &darr;"],
    ],
    "kpis": [
        ["NHI inventory completeness", "% of machine identities discovered &amp; owner-attested", "Inventory / attestation use cases", "per cycle"],
        ["Rotation coverage &amp; freshness", "% of secrets under managed rotation within SLA", "Rotation / lifecycle use cases", "monthly"],
        ["Gap-closure rate", "assessed GAP / PARTIAL &rarr; MET over time", "this assessment baseline", "per cycle"],
        ["Plaintext secrets in repos", "secrets detected in source &amp; history", "pre-commit + history-scan use cases", "continuous"],
        ["Tool consolidation", "count of overlapping secrets / vault tools", "vendor matrix", "per cycle"],
    ],
    "roi_events": "one credential-driven breach, one regulatory enforcement action, or one duplicated vault platform",
}

_PAM_VALUE = {
    "outcomes": [
        ["hard", "Rationalise tooling spend", "The vendor matrix exposes overlapping PAM / session / vaulting tools running in parallel and gives a layer-scoped consolidation path.", "Tool count &darr; · avoided licence + procurement effort"],
        ["hours", "Audit &amp; compliance efficiency", "A pre-built control-evidence pack (3-click framework &rarr; control &rarr; use case &rarr; evidence) answers APRA / ISM privileged-access audits and cuts findings.", "Audit hours &darr; · findings &darr; · avoided enforcement"],
        ["risk", "Lower expected breach loss", "Closing prioritised privileged-access gaps (standing privilege, shared admin credentials) reduces the probability × impact of a privileged-account compromise.", "Gaps closed · risk-adjusted expected-loss &darr;"],
        ["kpi", "Reduce operational toil", "Just-in-time elevation, session brokering and automated credential rotation remove manual privileged-access handling and standing-privilege incidents.", "Manual elevations &darr; · privileged incidents &darr;"],
    ],
    "kpis": [
        ["Privileged-account inventory", "% of privileged accounts discovered &amp; owner-attested", "Discovery / attestation use cases", "per cycle"],
        ["Standing-privilege reduction", "% of privileged access brokered just-in-time", "JIT / ZSP use cases", "monthly"],
        ["Gap-closure rate", "assessed GAP / PARTIAL &rarr; MET over time", "this assessment baseline", "per cycle"],
        ["Session coverage", "% of privileged sessions isolated &amp; recorded", "Session-management use cases", "continuous"],
        ["Tool consolidation", "count of overlapping PAM / session tools", "vendor matrix", "per cycle"],
    ],
    "roi_events": "one privileged-account compromise, one regulatory enforcement action, or one duplicated PAM platform",
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
    legacy_recdata: bool = False            # build the secrets-specific RECDATA section?
                                            # (the frozen legacy recommendations; new domains
                                            #  use the domain-agnostic VENDORMIX/COMPLIANCE)
    # report labels (domain-identifying copy in the template)
    report_title: str = ""
    report_heading: str = ""
    object_singular: str = "identity"       # nav noun, e.g. "By identity"
    object_plural: str = "identities"       # subtitle noun
    substrate_note: str = ""                # subtitle parenthetical when a substrate exists
    # per-domain body copy (Phase 1 #1 — content blocks, not hardcoded template strings)
    posture_noun: str = "identity"          # dashboard: "XYZ <posture_noun> posture — N use cases scored"
    object_picker: str = "identity"         # identity tab: "Pick a <object_picker> → …"
    substrate_exclusion_note: str = ""      # compliance-trace note: "(<substrate> excluded per ADR-007)"
    substrate_table_note: str = ""          # browse-all note about the excluded substrate
    kpi_object_label: str = "identities"    # dashboard KPI tile: "N <kpi_object_label>"
    layer_groups: tuple = ()                # vgrid column groups: ((code,label), …) per layer
    value_content: dict = field(default_factory=dict)   # business-value tab: outcomes/kpis/roi_events

    def report_meta(self):
        """The domain-identifying token map the report template consumes.

        Built in one place (off the descriptor) so the orchestrator can't
        hand-assemble a drifting dict and `render()` has an explicit contract:
        a new domain that omits a field fails fast rather than silently
        rendering secrets vocabulary.
        """
        return {
            "title": self.report_title,
            "heading": self.report_heading,
            "object_singular": self.object_singular,
            "object_plural": self.object_plural,
            "substrate_note": self.substrate_note,
        }

    def report_content(self):
        """Per-domain body-copy blocks the template consumes (Phase 1 #1). Secrets values
        reproduce the current template strings exactly; new domains override. The L0
        crypto-substrate dashboard card is shown only for domains that have a substrate."""
        return {
            "posture_noun": self.posture_noun,
            "object_picker": self.object_picker,
            "substrate_card_display": "" if self.substrate_slug else "display:none",
            "substrate_exclusion_note": self.substrate_exclusion_note,
            "substrate_table_note": self.substrate_table_note,
            "kpi_object_label": self.kpi_object_label,     # KPI tile: "N <kpi_object_label>"
            "layer_groups": [list(g) for g in self.layer_groups],   # vgrid column-group [code,label] pairs
            "value_content": self.value_content,
        }


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
    posture_noun="secrets",
    object_picker="machine identity",
    substrate_exclusion_note=" (Fortanix excluded per ADR-007)",
    substrate_table_note="Fortanix DSM (Layer-0 substrate) is excluded here per ADR-007 — see the XYZ-posture tab. ",
    kpi_object_label="machine identities",
    layer_groups=(("L1", "Secrets management"), ("L2", "NHI governance")),
    value_content=_SECRETS_VALUE,
    legacy_recdata=True,
)


# --- PAM (Privileged Access Management) domain (Phase 2) ---
# Capability-shaped like secrets (the PAM spike validated the shared engine). Two
# layers: L1 = established PAM suites; L2 = modern identity-native infrastructure
# access. No L0 crypto substrate; no informative MITRE lens in the PAM trace.
_PAM_VENDOR_LAYER = {
    "cyberark-pam": ("L1", "suite"),
    "delinea": ("L1", "suite"),
    "beyondtrust": ("L1", "suite"),
    "one-identity-safeguard": ("L1", "suite"),
    "wallix-bastion": ("L1", "suite"),
    "teleport": ("L2", "modern-access"),
}
_PAM_SHORT = {
    "cyberark-pam": "CyberArk", "delinea": "Delinea", "beyondtrust": "BeyondTrust",
    "one-identity-safeguard": "One Identity", "wallix-bastion": "WALLIX",
    "teleport": "Teleport",
}
_PAM_LAYER_LABEL = {
    "L1": "L1 · PAM platforms (vault / session control / brokering) — NATIVE = first-party privileged-access capability",
    "L2": "L2 · Modern identity-native infrastructure access — NATIVE = ephemeral, certificate-based access (not classic vaulting)",
}

PAM = Domain(
    slug="pam",
    label="Privileged Access Management",
    data_dir=os.path.join(HERE, "domains", "pam"),
    vendor_capabilities="vendor-capabilities.csv",
    use_cases="use-cases.csv",
    identity_catalog="identity-catalog.csv",
    regulatory_trace="regulatory-trace.csv",
    default_current_state="current-state.csv",
    vendor_layer=_FrozenDict(_PAM_VENDOR_LAYER),
    short=_FrozenDict(_PAM_SHORT),
    layer_label=_FrozenDict(_PAM_LAYER_LABEL),
    substrate_slug="",                       # PAM has no L0 crypto substrate
    anchors_tier="suite",                    # the established suites seed the complement view
    informative_frameworks=frozenset(),      # PAM trace carries no mitre-attack lens
    report_title="Privileged Access Management — Vendor-Selection Report",
    report_heading="Privileged Access Management — Vendor Selection",
    object_singular="privileged identity",
    object_plural="privileged identities",
    substrate_note="",
    posture_noun="privileged-access",
    object_picker="privileged identity",
    substrate_table_note="",                 # PAM has no excluded substrate
    kpi_object_label="privileged identities",
    layer_groups=(("L1", "PAM platforms"), ("L2", "Modern access")),
    value_content=_PAM_VALUE,
    legacy_recdata=False,
)

DOMAINS = {SECRETS.slug: SECRETS, PAM.slug: PAM}

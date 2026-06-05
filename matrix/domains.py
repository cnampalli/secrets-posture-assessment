"""Per-domain descriptors — the secrets-specific seams expressed as config (Phase 1).

The engine (loader, model builders, report) is domain-agnostic; everything that
made it *secrets-specific* — the data filenames, the vendor layer/short/label maps,
the L0 substrate, the complementary-anchor tier, and which frameworks are
informative-only — lives in a per-domain **YAML descriptor** (`config/domains/*.yaml`)
loaded into the `Domain` dataclass below. Adding PAM / IGA becomes a new YAML + data,
not new code (Phase 1 #8; validated by the Phase 0.5 PAM spike).
"""
import os
from dataclasses import dataclass, field

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
_DOMAIN_DIR = os.path.join(HERE, "config", "domains")


class _FrozenDict(dict):
    """A read-only dict: a Domain's maps can't be mutated in place, so a new
    domain built by copy-edit (`dict(SECRETS.vendor_layer)`) can't silently
    corrupt the source. Still a `dict` subclass, so json.dumps serialises it."""

    def _ro(self, *_a, **_k):
        raise TypeError("Domain maps are read-only; copy with dict(...) to derive a new domain")

    __setitem__ = __delitem__ = update = setdefault = pop = popitem = clear = _ro


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
    card_copy: dict = field(default_factory=dict)       # uc/identity card + posture-legend prose
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
            "card_copy": self.card_copy,                   # uc/identity card + posture-legend prose
            "value_content": self.value_content,
        }


def load_domain(path):
    """Build a `Domain` from a per-domain YAML descriptor (Phase 1 #8).

    Keeps the dataclass as the in-memory shape but lets analysts add a domain by
    authoring data (YAML) rather than editing Python. The YAML mirrors the dataclass
    fields one-to-one; this loader only re-imposes the in-memory invariants that YAML
    can't express: read-only maps (`_FrozenDict`), `(layer, tier)` tuples in
    `vendor_layer`, a `frozenset` of informative frameworks, tuple-of-tuple
    `layer_groups`, and `data_dir` resolved relative to matrix/.
    """
    with open(path, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)

    return Domain(
        slug=d["slug"],
        label=d["label"],
        data_dir=os.path.normpath(os.path.join(HERE, d["data_dir"])),
        vendor_capabilities=d["vendor_capabilities"],
        use_cases=d["use_cases"],
        identity_catalog=d["identity_catalog"],
        regulatory_trace=d["regulatory_trace"],
        default_current_state=d["default_current_state"],
        vendor_layer=_FrozenDict({k: tuple(v) for k, v in d["vendor_layer"].items()}),
        short=_FrozenDict(d["short"]),
        layer_label=_FrozenDict(d["layer_label"]),
        substrate_slug=d["substrate_slug"],
        anchors_tier=d["anchors_tier"],
        informative_frameworks=frozenset(d.get("informative_frameworks", [])),
        legacy_recdata=d.get("legacy_recdata", False),
        report_title=d.get("report_title", ""),
        report_heading=d.get("report_heading", ""),
        object_singular=d.get("object_singular", "identity"),
        object_plural=d.get("object_plural", "identities"),
        substrate_note=d.get("substrate_note", ""),
        posture_noun=d.get("posture_noun", "identity"),
        object_picker=d.get("object_picker", "identity"),
        substrate_exclusion_note=d.get("substrate_exclusion_note", ""),
        substrate_table_note=d.get("substrate_table_note", ""),
        kpi_object_label=d.get("kpi_object_label", "identities"),
        layer_groups=tuple(tuple(g) for g in d.get("layer_groups", ())),
        card_copy=d.get("card_copy", {}),
        value_content=d.get("value_content", {}),
    )


# Canonical display order; any additional domain YAMLs are appended alphabetically,
# so dropping a new descriptor into config/domains/ registers it without code.
_DOMAIN_ORDER = ("secrets", "pam")


def load_domains(dir=_DOMAIN_DIR):
    """Discover and load every `config/domains/*.yaml` descriptor, ordered by
    `_DOMAIN_ORDER` first (the established offerings) then alphabetically."""
    doms = [
        load_domain(os.path.join(dir, fn))
        for fn in sorted(os.listdir(dir))
        if fn.endswith((".yaml", ".yml"))
    ]
    doms.sort(key=lambda d: (
        _DOMAIN_ORDER.index(d.slug) if d.slug in _DOMAIN_ORDER else len(_DOMAIN_ORDER),
        d.slug,
    ))
    return {d.slug: d for d in doms}


DOMAINS = load_domains()
SECRETS = DOMAINS["secrets"]
PAM = DOMAINS["pam"]

"""Pure scoping/ordering helpers + config-file loaders for the regulatory
overlay engine. No global state; safe to import from tests."""
import yaml

RES_RANK = {"AU-RESIDENT": 0, "CONDITIONAL": 1, "SAAS-ONLY": 2}


def _load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_framework_labels(path):
    """Return {slug: (label, subtitle)} — tuple shape the engine expects."""
    raw = _load_yaml(path)
    return {slug: (d["label"], d["subtitle"]) for slug, d in raw.items()}


def load_vendor_residency(path):
    """Return {slug: {residency, irap, note}} verbatim."""
    return _load_yaml(path)


def vendor_sort_key(weight, residency, capability_keys):
    """Compose a sort key placing residency rank per the configured weight.

    capability_keys: tuple of already-negated capability metrics (lower=better),
    exactly as the engine builds them (e.g. (-secrets_native, -nhi_native)).
    """
    r = RES_RANK.get(residency, 9)
    if weight == "high":
        return (r,) + tuple(capability_keys)
    if weight == "medium":
        return (capability_keys[0], r) + tuple(capability_keys[1:])
    if weight == "low":
        return tuple(capability_keys) + (r,)
    if weight == "off":
        return tuple(capability_keys)
    raise ValueError(f"unknown residency weight: {weight!r}")


def select_primary(l1_secrets, irap_required):
    """Pick the primary secrets platform. Reproduces the engine's gate when
    irap_required=True; otherwise takes the capability leader (l1_secrets[0])."""
    if irap_required:
        irap_au = [v for v in l1_secrets
                   if v["residency"] == "AU-RESIDENT" and v["irap"] == "YES"]
        if irap_au:
            return irap_au[0]
        return next((v for v in l1_secrets if v["residency"] == "AU-RESIDENT"),
                    l1_secrets[0])
    return l1_secrets[0]


def scope_frameworks(fw_order, cfg):
    """Filter fw_order to the configured scope, preserving fw_order's ordering.
    Default config (no preset/flags) passes through unchanged (regression anchor)."""
    if getattr(cfg, "is_default", False):
        return list(fw_order)
    scope = set(cfg.framework_scope)
    return [s for s in fw_order if s in scope]

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

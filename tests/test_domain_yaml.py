"""Phase 1 #8 — `Domain` loadable from per-domain YAML (project convention keeps
config in YAML so analysts can add a domain without code).

Fidelity contract: a YAML-loaded domain must be *exactly* equal (frozen-dataclass
equality over every field) to the hand-written Python descriptor it replaces — so
the migration to YAML cannot silently drift a label, map, or policy flag.
"""
import os

import pytest

from matrix import domains

CONFIG_DIR = os.path.join(domains.HERE, "config", "domains")


def test_load_secrets_domain_from_yaml_matches_python_descriptor():
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "secrets.yaml"))
    assert loaded == domains.SECRETS


def test_load_pam_domain_from_yaml_matches_python_descriptor():
    loaded = domains.load_domain(os.path.join(CONFIG_DIR, "pam.yaml"))
    assert loaded == domains.PAM


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

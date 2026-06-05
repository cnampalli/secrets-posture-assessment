"""Phase 1 #3/#5: render() consumes the domain token map with an explicit
contract — values flow from the domain descriptor, and a missing label fails
fast instead of silently rendering secrets vocabulary in a non-secrets report.
"""
import pytest

import report_render


def _minimal_model(domain_meta):
    """The smallest model render() will assemble — every JSON section empty,
    so the only thing under test is the domain-label substitution."""
    return {
        "ranked": [], "anz": [], "ucs": [], "nhis": [],
        "glossary": {}, "layer_label": {}, "short": {},
        "reg": {}, "regdata": {}, "recdata": {},
        "meta": {"ranked_vendors": 0, "nhis": 0, "ucs": 0},
        "domain_meta": domain_meta,
    }


def _full_domain_meta(**overrides):
    dm = {"title": "T-SENTINEL", "heading": "H-SENTINEL",
          "object_singular": "account", "object_plural": "PLURAL-SENTINEL",
          "substrate_note": ""}
    dm.update(overrides)
    return dm


def test_render_injects_domain_meta_values_verbatim():
    # The label tokens resolve from domain_meta, not from a hardcoded default.
    html = report_render.render(_minimal_model(_full_domain_meta()))
    assert "T-SENTINEL" in html
    assert "PLURAL-SENTINEL" in html


def test_render_fails_fast_when_domain_meta_missing_a_label():
    # A non-secrets domain that forgets a label must error, NOT inherit
    # secrets vocabulary ("identities") via a silent .get() default.
    dm = _full_domain_meta()
    del dm["object_plural"]
    with pytest.raises(KeyError):
        report_render.render(_minimal_model(dm))


def test_render_requires_domain_meta():
    model = _minimal_model(_full_domain_meta())
    del model["domain_meta"]
    with pytest.raises(KeyError):
        report_render.render(model)

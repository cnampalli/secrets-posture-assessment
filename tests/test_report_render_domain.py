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
        "domain_content": {"posture_noun": "secrets", "object_picker": "machine identity",
                           "substrate_card_display": "", "substrate_exclusion_note": "",
                           "substrate_table_note": "", "kpi_object_label": "identities",
                           "layer_groups": [], "card_copy": {}, "value_content": {},
                           "has_substrate": True, "legacy_recdata": True},
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


def test_domain_label_containing_a_count_token_is_not_mangled():
    # Phase 1 #4: count tokens (__RV__/__NHI__/__UC__) must be substituted in the
    # SAME pass as the label tokens. Otherwise a domain whose heading legitimately
    # contains a "__RV__"-style sequence gets clobbered by the later count replace.
    model = _minimal_model(_full_domain_meta(heading="Vendor __RV__ Edition"))
    model["meta"] = {"ranked_vendors": 7, "nhis": 0, "ucs": 0}
    html = report_render.render(model)
    assert "Vendor __RV__ Edition" in html      # injected literal survives verbatim
    assert "Vendor 7 Edition" not in html        # NOT rewritten by the count substitution


def test_domain_label_containing_another_label_token_is_not_mangled():
    # Same single-pass guarantee across label tokens: a title containing
    # __OBJECT_PLURAL__ must not be rewritten by the object-plural substitution.
    model = _minimal_model(_full_domain_meta(title="The __OBJECT_PLURAL__ Report"))
    html = report_render.render(model)
    assert "The __OBJECT_PLURAL__ Report" in html
    assert "The PLURAL-SENTINEL Report" not in html


# Phase 1 #1-residual: gated secrets-specific source must be ABSENT (not just
# display:none / runtime-skipped) for non-secrets domains — and no raw region
# markers may leak into any rendered output.

def test_non_legacy_domain_omits_secrets_recommendation_block():
    model = _minimal_model(_full_domain_meta())
    model["domain_content"]["legacy_recdata"] = False
    html = report_render.render(model)
    assert "RECDATA.coverage_proof" not in html          # secrets if-block gone from source
    assert "Secrets management — top picks" not in html
    assert "__LEGACY_REC_START__" not in html            # marker must not leak
    # the generic function shell + tail still render for every domain
    assert "function renderRecommendations()" in html
    assert "vendorMixHtml()" in html


def test_legacy_domain_keeps_secrets_recommendation_block_without_markers():
    model = _minimal_model(_full_domain_meta())
    model["domain_content"]["legacy_recdata"] = True
    html = report_render.render(model)
    assert "RECDATA.coverage_proof" in html
    assert "Secrets management — top picks" in html
    assert "__LEGACY_REC_START__" not in html            # markers stripped, content kept
    assert "__LEGACY_REC_END__" not in html


def test_non_substrate_domain_omits_l0_crypto_card():
    model = _minimal_model(_full_domain_meta())
    model["domain_content"]["has_substrate"] = False
    html = report_render.render(model)
    assert "Fortanix DSM" not in html
    assert "Crypto-substrate dependency" not in html
    assert "__SUBSTRATE_CARD_START__" not in html


def test_substrate_domain_keeps_l0_crypto_card_without_markers():
    model = _minimal_model(_full_domain_meta())
    model["domain_content"]["has_substrate"] = True
    html = report_render.render(model)
    assert "Crypto-substrate dependency" in html
    assert "__SUBSTRATE_CARD_START__" not in html
    assert "__SUBSTRATE_CARD_END__" not in html

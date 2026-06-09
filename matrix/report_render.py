"""Render the stakeholder report HTML from the model + report-template.html.

Templating layer of the report build: loads the raw template and performs the
exact token-replacement assembly that build_matrix_viewer.py used inline, so the
output is byte-identical.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Repo root on path so `brand_fonts` resolves when this runs as a script
# (build_matrix_viewer.py adds matrix/ to sys.path[0], not the root).
sys.path.insert(0, os.path.dirname(HERE))
import brand_fonts
import brand_tokens


def load_template():
    with open(os.path.join(HERE, "report-template.html"), encoding="utf-8") as fh:
        return fh.read()


def _apply_region(html, name, keep):
    """Resolve a template region delimited by `__name_START__` … `__name_END__`
    marker lines (Phase 1 #1-residual). `keep=True` strips just the marker lines,
    leaving the content byte-identical; `keep=False` removes the whole region so a
    non-applicable domain doesn't even ship the source (e.g. secrets recommendation
    JS / the Fortanix L0 card never appear in a PAM report)."""
    marker = lambda tag: re.compile(r"^[^\n]*__" + name + "_" + tag + r"__[^\n]*\n", re.M)
    if keep:
        return marker("END").sub("", marker("START").sub("", html))
    region = re.compile(
        r"^[^\n]*__" + name + r"_START__.*?__" + name + r"_END__[^\n]*\n", re.S | re.M)
    return region.sub("", html)


def render(model):
    """Assemble the final report HTML.

    model keys: ranked, anz, ucs, nhis, glossary, layer_label, short, reg,
    regdata, recdata, vendormix, compliance, vendorintel, domain_meta,
    domain_content, meta.

    `domain_meta` is a domain's `report_meta()` token map; its labels are read
    by required key (no secrets-vocab fallback) so a domain missing a label
    fails fast instead of silently rendering the wrong vocabulary.
    """
    dm = model["domain_meta"]
    dc = model["domain_content"]
    # Resolve the domain-gated source regions first: applicable domains keep the
    # content (markers stripped → byte-identical); others have it removed entirely.
    template = _apply_region(load_template(), "SUBSTRATE_CARD", keep=dc["has_substrate"])
    template = _apply_region(template, "LEGACY_REC", keep=dc["legacy_recdata"])
    # IGA is process-shaped: it renders the bespoke per-AREA vendor-fit grid
    # (model["igavfit"]) and gates OFF the NATIVE/ADD-ON capability matrix
    # (VENDORMIX). secrets/PAM (no igavfit) keep the matrix and drop the IGA view.
    # The two source regions are mutually exclusive — never both in one report.
    is_iga = bool(model.get("igavfit"))
    template = _apply_region(template, "IGA_VENDOR_FIT", keep=is_iga)
    template = _apply_region(template, "VENDORMIX_REGION", keep=not is_iga)
    # Then the delimited JSON/CSS injections (each `/*__X__*/[]`/`{}` placeholder is
    # distinct and carries model data, not user-facing prose).
    html = (template
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__DATA__*/[]", json.dumps(model["ranked"], ensure_ascii=False))
            .replace("/*__XYZ__*/[]", json.dumps(model["anz"], ensure_ascii=False))
            .replace("/*__UCS__*/[]", json.dumps(model["ucs"], ensure_ascii=False))
            .replace("/*__NHIS__*/[]", json.dumps(model["nhis"], ensure_ascii=False))
            .replace("/*__GLOSSARY__*/{}", json.dumps(model["glossary"], ensure_ascii=False))
            .replace("/*__LAYERLABEL__*/{}", json.dumps(model["layer_label"], ensure_ascii=False))
            .replace("/*__SHORT__*/{}", json.dumps(model["short"], ensure_ascii=False))
            .replace("/*__REG__*/{}", json.dumps(model["reg"], ensure_ascii=False))
            .replace("/*__REGDATA__*/{}", json.dumps(model["regdata"], ensure_ascii=False))
            .replace("/*__RECDATA__*/{}", json.dumps(model["recdata"], ensure_ascii=False))
            .replace("/*__VENDORMIX__*/{}", json.dumps(model.get("vendormix", {}), ensure_ascii=False))
            .replace("/*__IGAVFIT__*/{}", json.dumps(model.get("igavfit", {}), ensure_ascii=False))
            .replace("/*__COMPLIANCE__*/{}", json.dumps(model.get("compliance", {}), ensure_ascii=False))
            .replace("/*__VENDORINTEL__*/{}", json.dumps(model.get("vendorintel", {}), ensure_ascii=False))
            .replace("/*__META__*/{}", json.dumps(model["meta"], ensure_ascii=False))
            .replace("/*__VALUECFG__*/{}", json.dumps(dc["value_content"], ensure_ascii=False))
            .replace("/*__DOMAINCFG__*/{}", json.dumps(
                {"kpi_object_label": dc["kpi_object_label"], "layer_groups": dc["layer_groups"],
                 "card": dc["card_copy"]},
                ensure_ascii=False)))

    # Then the bare `__X__` label/count tokens in a SINGLE pass (Phase 1 #4): a
    # value injected here (e.g. a heading legitimately containing "__RV__") is never
    # re-scanned by a later replace, so it can't be mangled. Keys read eagerly so a
    # domain missing a label still fails fast (KeyError) rather than rendering blank.
    tokens = {
        "__DOMAIN_TITLE__": dm["title"],
        "__DOMAIN_HEADING__": dm["heading"],
        "__SUBSTRATE_NOTE__": dm["substrate_note"],
        "__OBJECT_PLURAL__": dm["object_plural"],
        "__OBJECT_SINGULAR__": dm["object_singular"],
        "__POSTURE_NOUN__": dc["posture_noun"],
        "__OBJECT_PICKER__": dc["object_picker"],
        "__SUBSTRATE_CARD_DISPLAY__": dc["substrate_card_display"],
        "__SUBSTRATE_EXCL__": dc["substrate_exclusion_note"],
        "__SUBSTRATE_TABLE_NOTE__": dc["substrate_table_note"],
        "__RV__": str(model["meta"]["ranked_vendors"]),
        "__NHI__": str(model["meta"]["nhis"]),
        "__UC__": str(model["meta"]["ucs"]),
    }
    # Longest token first so no token that is a substring of another is matched early.
    pattern = re.compile("|".join(re.escape(k) for k in sorted(tokens, key=len, reverse=True)))
    return pattern.sub(lambda m: tokens[m.group(0)], html)

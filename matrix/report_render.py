"""Render the stakeholder report HTML from the model + report-template.html.

Templating layer of the report build: loads the raw template and performs the
exact token-replacement assembly that build_matrix_viewer.py used inline, so the
output is byte-identical.
"""
import json
import os
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


def render(model):
    """Assemble the final report HTML.

    model keys: ranked, anz, ucs, nhis, glossary, layer_label, short, reg,
    regdata, recdata, vendormix, meta.
    """
    return (load_template()
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
            .replace("/*__COMPLIANCE__*/{}", json.dumps(model.get("compliance", {}), ensure_ascii=False))
            .replace("/*__VENDORINTEL__*/{}", json.dumps(model.get("vendorintel", {}), ensure_ascii=False))
            .replace("/*__META__*/{}", json.dumps(model["meta"], ensure_ascii=False))
            .replace("__RV__", str(model["meta"]["ranked_vendors"]))
            .replace("__NHI__", str(model["meta"]["nhis"]))
            .replace("__UC__", str(model["meta"]["ucs"])))

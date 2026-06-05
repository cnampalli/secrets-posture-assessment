"""Render the cross-domain report HTML from the model + cross-domain-template.html."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # repo root for brand_fonts/brand_tokens
import brand_fonts
import brand_tokens


def load_template():
    with open(os.path.join(HERE, "cross-domain-template.html"), encoding="utf-8") as fh:
        return fh.read()


def render(model):
    """Assemble the cross-domain report HTML. `model` is crossdomain.build_crossmap output."""
    payload = json.dumps(model, ensure_ascii=False).replace("</", "<\\/")   # </script> safety
    return (load_template()
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__CROSSMAP__*/{}", payload))

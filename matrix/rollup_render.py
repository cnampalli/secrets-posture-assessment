"""Render the exec roll-up HTML from the model + rollup-template.html.

Mirrors cross_render.render: substitutes the brand font/token CSS and embeds the
model as a </script>-safe JSON payload. Pure (no file writes)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))   # repo root for brand_fonts/brand_tokens
import brand_fonts
import brand_tokens


def load_template():
    with open(os.path.join(HERE, "rollup-template.html"), encoding="utf-8") as fh:
        return fh.read()


def render(model):
    """Assemble the exec roll-up HTML. `model` is rollup.build_exec_rollup output."""
    payload = json.dumps(model, ensure_ascii=False).replace("</", "<\\/")
    return (load_template()
            .replace("/*__FONTS__*/", brand_fonts.fontface_css())
            .replace("/*__TOKENS__*/", brand_tokens.tokens_css())
            .replace("/*__ROLLUP__*/{}", payload))

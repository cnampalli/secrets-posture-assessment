#!/usr/bin/env python3
"""Shared Brass Editorial design tokens for the generated reports.

The single source of truth for colour/type tokens is
``design/brass-editorial.tokens.json`` → emitted to
``design/brass-editorial.vars.css`` (a ``:root`` light block + a ``.dark``
block) by ``design/emit-tokens.mjs`` (Plan 1). The React app and these Python
reports both consume that one file, so a colour change in the tokens JSON
propagates everywhere after a single re-emit.

We inject the vars CSS into each report's ``<style>`` (via a ``/*__TOKENS__*/``
token) ahead of the report's own stylesheet, whose local ``:root`` then aliases
its token names to these canonical vars. Reports are light-only (no theme
toggle); the ``.dark`` block is inert but harmless. Reading a committed,
generated file keeps the build deterministic / byte-stable.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_VARS = os.path.join(_HERE, "design", "brass-editorial.vars.css")


def tokens_css():
    """Return the canonical Brass Editorial CSS-variable block (`:root` + `.dark`)."""
    with open(_VARS, encoding="utf-8") as fh:
        return fh.read()


if __name__ == "__main__":
    css = tokens_css()
    print(f"tokens_css(): {len(css)} chars from design/brass-editorial.vars.css")

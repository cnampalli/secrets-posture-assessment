#!/usr/bin/env python3
"""Shared, offline-safe @font-face block for every generated deliverable.

The posture-assessment HTML artifacts (questionnaire, matrix viewer, exec
summary) are single self-contained files that travel to stakeholders and are
often opened offline / behind corporate firewalls. To render the unified
Brass Editorial type system identically everywhere — with no network call —
each build inlines the brand fonts as base64 woff2 via a /*__FONTS__*/ token.

Keeping the (large) base64 out of the HTML/CSS source files and producing it
here at build time mirrors the codebase's existing inject-at-build pattern and
keeps the sources reviewable. The woff2 binaries live in assets/fonts/ and are
OFL-licensed (see assets/fonts/LICENSES.md). Output is deterministic — same
bytes in, same CSS out — so byte-stable / snapshot tests stay stable.

Families (variable, weight axis 100–900):
  - Inter            → UI / body
  - Fraunces         → display / headings (serif)
  - JetBrains Mono   → IDs, codes, metrics
"""
import base64
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_DIR = os.path.join(_HERE, "assets", "fonts")

# (CSS family name, woff2 filename) — variable fonts, full 100–900 weight axis.
_FACES = (
    ("Fraunces", "fraunces.woff2"),
    ("Inter", "inter.woff2"),
    ("JetBrains Mono", "jetbrains-mono.woff2"),
)


def _b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


def fontface_css():
    """Return @font-face rules embedding every brand font as base64 woff2."""
    rules = []
    for family, fname in _FACES:
        data = _b64(os.path.join(_FONT_DIR, fname))
        rules.append(
            "@font-face{font-family:'%s';font-style:normal;font-display:swap;"
            "font-weight:100 900;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (family, data)
        )
    return "\n".join(rules)


if __name__ == "__main__":
    css = fontface_css()
    print(f"fontface_css(): {len(_FACES)} faces, {len(css)} chars")

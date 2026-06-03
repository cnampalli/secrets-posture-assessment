import re
import brand_tokens


def test_tokens_css_contains_canonical_root_and_dark():
    css = brand_tokens.tokens_css()
    assert ":root" in css and ".dark" in css


def test_tokens_css_carries_brass_accent_and_fonts():
    css = brand_tokens.tokens_css()
    assert "--accent: #9a7b32;" in css          # light brass
    assert "--accent: #d6b25a;" in css          # dark brass
    assert "--font-display: 'Fraunces'" in css
    assert "--font-body: 'Inter'" in css
    assert "--font-mono: 'JetBrains Mono'" in css


def test_tokens_css_is_offline():
    assert not re.search(r"https?://", brand_tokens.tokens_css())

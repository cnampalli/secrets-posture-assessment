import re
import brand_fonts


def test_faces_are_the_brass_editorial_families():
    families = {family for family, _ in brand_fonts._FACES}
    assert families == {"Fraunces", "Inter", "JetBrains Mono"}


def test_fontface_css_embeds_three_base64_woff2():
    css = brand_fonts.fontface_css()
    assert css.count("@font-face") == 3
    assert css.count("data:font/woff2;base64,") == 3
    for family in ("Fraunces", "Inter", "JetBrains Mono"):
        assert f"font-family:'{family}'" in css
    assert not re.search(r"https?://", css)

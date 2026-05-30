#!/usr/bin/env python3
"""Bake the WS-1 rubric into a self-contained questionnaire HTML.

Pattern mirrors matrix/build_matrix_viewer.py: resolve rubric -> JSON, inline
scoring.js + app.js into template.html via /*__TOKEN__*/ replacement, write one
offline file with no external references."""
import json
import os
import sys

# Put the repo root on sys.path so `questionnaire` resolves whether this file is
# run as a script (`python3 questionnaire/build_questionnaire.py`) or imported as
# a package member (pytest: `import questionnaire.build_questionnaire`).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
METH = os.path.join(os.path.dirname(HERE), "methodology")


def build(out_path=None):
    out_path = str(out_path) if out_path else os.path.join(HERE, "questionnaire.html")
    rubric = rubric_loader.load_rubric(METH)
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    scoring = open(os.path.join(HERE, "scoring.js"), encoding="utf-8").read()
    app = open(os.path.join(HERE, "app.js"), encoding="utf-8").read()
    for tok in ("/*__SCORING__*/", "/*__RUBRIC__*/[]", "/*__APP__*/"):
        if tok not in template:
            raise ValueError(f"template.html is missing injection token: {tok}")
    html = (template
            .replace("/*__SCORING__*/", scoring)
            .replace("/*__RUBRIC__*/[]", json.dumps(rubric, ensure_ascii=False))
            .replace("/*__APP__*/", app))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes; {len(rubric)} use cases)")
    return out_path


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""Emit one rubric JSON per domain for the React app.

methodology/ is the source of truth for the shared question templates; each
domain's uc-archetype map (+ optional evidence/regulatory data) comes from its
data dir. Add a domain by adding one row to DOMAINS."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METH = os.path.join(ROOT, "methodology")
OUT_DIR = os.path.join(ROOT, "app", "src", "data")

# data_dir=None => methodology-only (secrets). file = rubric.<id>.json
DOMAINS = [
    {"id": "secrets", "data_dir": None},
    {"id": "pam", "data_dir": os.path.join(ROOT, "matrix", "domains", "pam")},
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for d in DOMAINS:
        rubric = rubric_loader.load_rubric(METH, data_dir=d["data_dir"])
        out = os.path.join(OUT_DIR, f"rubric.{d['id']}.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(rubric, fh, ensure_ascii=False, indent=2)
        print(f"wrote {out} ({len(rubric)} use cases)")


if __name__ == "__main__":
    main()

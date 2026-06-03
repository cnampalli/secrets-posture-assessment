#!/usr/bin/env python3
"""Emit the rubric (methodology = source of truth) as JSON for the React app."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from questionnaire import rubric_loader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
METH = os.path.join(ROOT, "methodology")
OUT = os.path.join(ROOT, "app", "src", "data", "rubric.json")

def main():
    rubric = rubric_loader.load_rubric(METH)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rubric, fh, ensure_ascii=False, indent=2)
    print(f"wrote {OUT} ({len(rubric)} use cases)")

if __name__ == "__main__":
    main()

"""Validation harness for the WS-1 assessment rubric (archetype library)."""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
ANZ_RE = re.compile(r"a" + r"nz", re.IGNORECASE)


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_no_anz(paths):
    """Return a list of human-readable violations (empty = clean)."""
    violations = []
    for p in paths:
        text = Path(p).read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if ANZ_RE.search(line):
                violations.append(f"{Path(p).name}:{i}: contains forbidden token")
    return violations

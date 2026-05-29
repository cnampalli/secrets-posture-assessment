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


REQUIRED_ARCH_COLS = (
    "archetype_id", "name", "intent", "met_def",
    "partial_def", "gap_def", "na_def", "evidence_expectation",
)


def validate_archetypes(rows):
    errors = []
    seen = set()
    for r in rows:
        aid = r.get("archetype_id", "")
        if aid in seen:
            errors.append(f"duplicate archetype_id {aid}")
        seen.add(aid)
        # A0 carries definitions per-UC in bespoke-criteria.csv; only id/name/intent required.
        cols = ("archetype_id", "name", "intent") if aid == "A0" else REQUIRED_ARCH_COLS
        for c in cols:
            if not (r.get(c) or "").strip():
                errors.append(f"{aid}: empty required column '{c}'")
    return errors

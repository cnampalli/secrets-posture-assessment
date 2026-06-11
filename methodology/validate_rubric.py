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


ALLOWED_BOUNDARY = {"GAP_PARTIAL", "PARTIAL_MET"}


def validate_questions(archetype_rows, question_rows):
    errors = []
    arch_ids = {r["archetype_id"] for r in archetype_rows}
    non_a0 = arch_ids - {"A0"}
    covered = set()
    for q in question_rows:
        aid = q.get("archetype_id", "")
        if aid not in arch_ids:
            errors.append(f"question {q.get('q_id')}: unknown archetype_id {aid}")
        covered.add(aid)
        for c in ("q_id", "question_template", "dimension", "informs_state"):
            if not (q.get(c) or "").strip():
                errors.append(f"question {q.get('q_id')}: empty '{c}'")
        if q.get("informs_state") not in ALLOWED_BOUNDARY:
            errors.append(
                f"question {q.get('q_id')}: informs_state must be one of {ALLOWED_BOUNDARY}"
            )
    for aid in sorted(non_a0 - covered):
        errors.append(f"archetype {aid}: has no diagnostic questions")
    return errors


SLOT_RE = re.compile(r"\{([a-zA-Z_]+)\}")


def _slots_for_archetype(aid, archetype_rows, question_rows):
    """All {slot} names referenced by an archetype's defs + its questions."""
    slots = set()
    for r in archetype_rows:
        if r["archetype_id"] == aid:
            for col in ("met_def", "partial_def", "gap_def", "na_def", "intent"):
                slots |= set(SLOT_RE.findall(r.get(col, "")))
    for q in question_rows:
        if q["archetype_id"] == aid:
            slots |= set(SLOT_RE.findall(q.get("question_template", "")))
    return slots


def _parse_params(raw):
    out = {}
    for pair in (raw or "").split(";"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            return None  # malformed
        k, v = pair.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def validate_bespoke(mapping_rows, bespoke_rows):
    errors = []
    a0_ucs = {m["uc_id"] for m in mapping_rows if m.get("archetype_id") == "A0"}
    bespoke_ucs = {b["uc_id"] for b in bespoke_rows}
    for uc in sorted(a0_ucs - bespoke_ucs):
        errors.append(f"A0 use-case {uc}: no bespoke criteria authored")
    for uc in sorted(bespoke_ucs - a0_ucs):
        errors.append(f"bespoke criteria for {uc}: but {uc} is not mapped to A0")
    for b in bespoke_rows:
        for c in ("uc_id", "sub_id", "sub_criterion", "question", "evidence"):
            if not (b.get(c) or "").strip():
                errors.append(f"bespoke {b.get('uc_id')}/{b.get('sub_id')}: empty '{c}'")
    return errors


def validate_mapping(use_case_rows, archetype_rows, question_rows, mapping_rows):
    errors = []
    arch_ids = {r["archetype_id"] for r in archetype_rows}
    uc_ids = {r["uc_id"] for r in use_case_rows}
    mapped = set()
    used_archetypes = set()
    for m in mapping_rows:
        uc = m.get("uc_id", "")
        aid = m.get("archetype_id", "")
        if uc not in uc_ids:
            errors.append(f"mapping: unknown uc_id {uc}")
        if aid not in arch_ids:
            errors.append(f"mapping {uc}: unknown archetype_id {aid}")
            continue
        mapped.add(uc)
        used_archetypes.add(aid)
        if aid == "A0":
            continue  # slots not required; criteria live in bespoke-criteria.csv
        params = _parse_params(m.get("params", ""))
        if params is None:
            errors.append(f"mapping {uc}: malformed params (need key=value;key=value)")
            continue
        needed = _slots_for_archetype(aid, archetype_rows, question_rows)
        missing = needed - set(params)
        if missing:
            errors.append(f"mapping {uc} ({aid}): params missing slots {sorted(missing)}")
    for uc in sorted(uc_ids - mapped):
        errors.append(f"use-case {uc}: not mapped to any archetype")
    for aid in sorted((arch_ids - {"A0"}) - used_archetypes):
        errors.append(f"archetype {aid}: never used by any UC (dead archetype)")
    return errors


def run_all():
    archs = load_csv(METH / "assessment-archetypes.csv")
    qs = load_csv(METH / "archetype-questions.csv")
    mapping = load_csv(METH / "uc-archetype-map.csv")
    bespoke = load_csv(METH / "bespoke-criteria.csv")
    ucs = load_csv(ROOT / "matrix" / "domains" / "secrets" / "use-cases.csv")
    files = [
        METH / "assessment-archetypes.csv",
        METH / "archetype-questions.csv",
        METH / "uc-archetype-map.csv",
        METH / "bespoke-criteria.csv",
    ]
    errors = []
    errors += validate_archetypes(archs)
    errors += validate_questions(archs, qs)
    errors += validate_mapping(ucs, archs, qs, mapping)
    errors += validate_bespoke(mapping, bespoke)
    errors += check_no_anz(files)
    return errors


if __name__ == "__main__":
    problems = run_all()
    if problems:
        print("RUBRIC VALIDATION FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Rubric validation passed.")

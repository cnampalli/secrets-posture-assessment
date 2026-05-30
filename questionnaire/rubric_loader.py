"""Resolve the WS-1 rubric CSVs into renderable use-case question sets.

Depends only on methodology/: title comes from uc-archetype-map's `notes`,
category from the uc_id prefix. A0 use cases yield bespoke sub-criteria;
A1-A8 yield param-filled ladder questions."""
import csv
import os
import re
from collections import defaultdict


class RubricError(Exception):
    pass


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _parse_params(raw):
    out = {}
    for chunk in (raw or "").split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise RubricError(f"malformed param (no '='): {chunk!r}")
        k, v = chunk.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def _fill(template, params, uc_id, qid):
    def repl(m):
        slot = m.group(1)
        if slot not in params:
            raise RubricError(f"{uc_id} {qid}: no param for slot '{{{slot}}}'")
        return params[slot]
    return re.sub(r"\{([^}]+)\}", repl, template)


def load_rubric(meth_dir):
    meth_dir = str(meth_dir)
    questions_by_arch = defaultdict(list)
    for r in _read(os.path.join(meth_dir, "archetype-questions.csv")):
        questions_by_arch[r["archetype_id"]].append(r)
    arch_name = {r["archetype_id"]: r["name"]
                 for r in _read(os.path.join(meth_dir, "assessment-archetypes.csv"))}
    bespoke_by_uc = defaultdict(list)
    for r in _read(os.path.join(meth_dir, "bespoke-criteria.csv")):
        bespoke_by_uc[r["uc_id"]].append(r)

    out = []
    for row in _read(os.path.join(meth_dir, "uc-archetype-map.csv")):
        uc_id = row["uc_id"]
        arch = row["archetype_id"]
        category = "Functional" if uc_id.startswith("UC-F") else "Non-functional"
        base = {"uc_id": uc_id, "title": row.get("notes", ""), "category": category,
                "archetype": arch, "archetype_name": arch_name.get(arch, arch)}
        if arch == "A0":
            base["kind"] = "bespoke"
            base["sub_criteria"] = [
                {"sub_id": b["sub_id"], "sub_criterion": b["sub_criterion"],
                 "question": b["question"], "evidence": b["evidence"]}
                for b in bespoke_by_uc.get(uc_id, [])]
        else:
            params = _parse_params(row.get("params", ""))
            base["kind"] = "ladder"
            base["questions"] = [
                {"qid": q["q_id"], "dimension": q["dimension"],
                 "informs_state": q["informs_state"],
                 "text": _fill(q["question_template"], params, uc_id, q["q_id"])}
                for q in questions_by_arch.get(arch, [])]
        out.append(base)
    return out

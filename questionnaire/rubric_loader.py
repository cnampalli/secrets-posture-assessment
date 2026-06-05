"""Resolve the rubric CSVs into renderable use-case question sets.

Two modes:
- methodology-only (``data_dir`` omitted): the original WS-1 behaviour — title from
  uc-archetype-map's ``notes``, category from the uc_id prefix, no evidence packs.
- domain-aware (``data_dir`` given): shared question templates still come from
  ``meth_dir`` (archetype-questions / assessment-archetypes), but the uc-archetype
  map, bespoke criteria, evidence catalog and regulatory trace come from the domain
  ``data_dir``. Each control's evidence items flow down to the use cases that back it
  and bind to questions by shared ``dimension`` (regulatory-driven evidence packs)."""
import csv
import os
import re
from collections import defaultdict

# Evidence packs are a compliance-evidence concept; refs are collected only from
# compliance-role trace rows (ADVERSARY-LENS frameworks are skipped).
_COMPLIANCE_ROLES = {"PRIMARY-LENS", "BACK-MAP"}
_CATEGORY = {"FUNCTIONAL": "Functional", "NON_FUNCTIONAL": "Non-functional"}


class RubricError(Exception):
    pass


def _read(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ids(raw):
    return [t.strip() for t in (raw or "").split(";") if t.strip()]


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


def _load_evidence(src):
    """Return (catalog_by_id, uc_to_items) for a domain data dir.

    ``uc_to_items`` maps uc_id -> {ev_id -> set(control_codes backing this uc that
    reference the item)}. Empty maps if the domain ships no evidence catalog/trace."""
    cat_path = os.path.join(src, "evidence-catalog.csv")
    trace_path = os.path.join(src, "regulatory-trace.csv")
    if not (os.path.exists(cat_path) and os.path.exists(trace_path)):
        return {}, {}
    catalog = {(r.get("ev_id") or "").strip(): r
               for r in _read(cat_path) if (r.get("ev_id") or "").strip()}
    uc_items = defaultdict(lambda: defaultdict(set))
    for row in _read(trace_path):
        if (row.get("framework_role") or "").strip() not in _COMPLIANCE_ROLES:
            continue
        cc = (row.get("control_code") or "").strip()
        evs = _ids(row.get("evidence_item_ids"))
        if not evs:
            continue
        for uc in _ids(row.get("uc_ids")):
            for ev in evs:
                uc_items[uc][ev].add(cc)
    return catalog, uc_items


def _evidence_item(catalog, ev_id, controls):
    r = catalog[ev_id]
    return {
        "ev_id": ev_id,
        "requirement": r.get("requirement", ""),
        "dimension": (r.get("dimension") or "").strip(),
        "tier": (r.get("tier") or "").strip(),
        "example_artifact": r.get("example_artifact", ""),
        "sensitivity_tag": r.get("sensitivity_tag", ""),
        "citation_keys": _ids(r.get("citation_keys")),
        "satisfies": sorted(controls),   # the "one artifact -> many controls" reverse view
    }


def _attach_evidence(uc_obj, catalog, items_for_uc):
    """Bind a UC's deduped evidence items to its questions by shared dimension;
    items whose dimension matches no question fall to ``evidence_additional``."""
    resolved = [_evidence_item(catalog, ev, controls)
                for ev, controls in items_for_uc.items() if ev in catalog]
    # primary first (the headline ask), then deterministic by id
    resolved.sort(key=lambda e: (0 if e["tier"] == "primary" else 1, e["ev_id"]))

    questions = uc_obj.get("questions", [])
    dims = {q["dimension"] for q in questions}
    for q in questions:
        bound = [e for e in resolved if e["dimension"] == q["dimension"]]
        if bound:
            q["evidence"] = bound
    uc_obj["evidence_additional"] = [e for e in resolved if e["dimension"] not in dims]


def load_rubric(meth_dir, data_dir=None):
    meth_dir = str(meth_dir)
    questions_by_arch = defaultdict(list)
    for r in _read(os.path.join(meth_dir, "archetype-questions.csv")):
        questions_by_arch[r["archetype_id"]].append(r)
    arch_name = {r["archetype_id"]: r["name"]
                 for r in _read(os.path.join(meth_dir, "assessment-archetypes.csv"))}

    # Domain-specific inputs come from data_dir when given, else methodology/.
    src = str(data_dir) if data_dir else meth_dir

    bespoke_by_uc = defaultdict(list)
    bespoke_path = os.path.join(src, "bespoke-criteria.csv")
    if os.path.exists(bespoke_path):
        for r in _read(bespoke_path):
            bespoke_by_uc[r["uc_id"]].append(r)

    # Category from the domain's use-cases.csv (prefix logic mislabels non-UC-F ids).
    category_by_uc = {}
    uc_path = os.path.join(src, "use-cases.csv")
    if os.path.exists(uc_path):
        category_by_uc = {r["uc_id"]: _CATEGORY.get((r.get("category") or "").strip(),
                                                     "Non-functional")
                          for r in _read(uc_path)}

    catalog, uc_items = ({}, {})
    if data_dir is not None:
        catalog, uc_items = _load_evidence(src)
    binding = data_dir is not None and bool(catalog)

    out = []
    for row in _read(os.path.join(src, "uc-archetype-map.csv")):
        uc_id = row["uc_id"]
        arch = row["archetype_id"]
        category = category_by_uc.get(
            uc_id, "Functional" if uc_id.startswith("UC-F") else "Non-functional")
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
            if not base["questions"]:
                raise RubricError(
                    f"{uc_id}: archetype {arch!r} has no questions in archetype-questions.csv")
        if binding:
            _attach_evidence(base, catalog, uc_items.get(uc_id, {}))
        out.append(base)
    return out

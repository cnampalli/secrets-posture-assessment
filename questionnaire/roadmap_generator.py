#!/usr/bin/env python3
"""Generate a prioritised engagement-menu JSON from an assessment-record.json.

Applies the WS-4 playbook's risk x effort prioritisation method:
- risk seeded from use-cases.csv priority_fi (overridable per engagement)
- effort from a per-engagement CSV (default Med)
- quadrant from risk x effort
- regulatory driver scoped to a framework set (financial preset default), MITRE
  excluded, capped at one control per framework (max 3), regulator-first
- regulation is an ordering tie-breaker only (no automatic band escalation)

CLI: python3 -m questionnaire.roadmap_generator <record.json> -o engagement-menu.json \
        [--engagement engagement.csv] [--frameworks slug,slug] [--preset financial]
"""
import argparse
import csv
import json
import os
import sys

from questionnaire.record_state import SCHEMA, resolve_state

OUTPUT_SCHEMA = "engagement-menu/v1"
ENGAGEMENT_STATES = ("GAP", "PARTIAL")
_RISK_BY_PRIORITY = {"P0": "High", "P1": "Med"}          # anything else -> Low
_QUADRANT_ORDER = {"Quick wins": 0, "Major projects": 1, "Fill-ins": 2, "Hard slogs": 3}
_RISK_ORDER = {"High": 0, "Med": 1, "Low": 2}
_ROLE_ORDER = {"BACK-MAP": 0, "PRIMARY-LENS": 1}         # regulator first; ADVERSARY-LENS excluded


class RoadmapError(Exception):
    pass


def seed_risk(priority_fi):
    """Map a use-case's priority_fi to a default risk band (P0->High, P1->Med, else Low)."""
    return _RISK_BY_PRIORITY.get((priority_fi or "").strip(), "Low")


def quadrant(risk, effort):
    """Risk x effort -> one of the four engagement quadrants."""
    risk_high = risk in ("High", "Med")
    effort_high = effort == "High"
    if risk_high and not effort_high:
        return "Quick wins"
    if risk_high and effort_high:
        return "Major projects"
    if not risk_high and not effort_high:
        return "Fill-ins"
    return "Hard slogs"


def regulatory_driver(uc_id, trace_rows, scope, cap=3):
    """In-scope control drivers for a UC: one per framework, regulator-first, capped.

    Excludes ADVERSARY-LENS (e.g. MITRE) — not a regulatory obligation. Within a
    framework the lexicographically smallest control_code is chosen (deterministic).
    """
    by_fw = {}
    for row in trace_rows:
        slug = row["framework_slug"]
        if row.get("framework_role") == "ADVERSARY-LENS" or slug not in scope:
            continue
        if uc_id not in (row.get("uc_ids") or "").split(";"):
            continue
        cand = {
            "framework_slug": slug,
            "control_code": row["control_code"],
            "control_short_title": row.get("control_short_title", ""),
            "_role": row.get("framework_role", ""),
        }
        cur = by_fw.get(slug)
        if cur is None or cand["control_code"] < cur["control_code"]:
            by_fw[slug] = cand
    ordered = sorted(by_fw.values(),
                     key=lambda d: (_ROLE_ORDER.get(d["_role"], 9), d["framework_slug"]))
    return [{k: v for k, v in d.items() if not k.startswith("_")} for d in ordered[:cap]]


def build_engagement_menu(record, use_cases, trace_rows, engagement_inputs, scope, source_record=""):
    """Pure transform: assessment record -> engagement-menu/v1 dict (GAP/PARTIAL only)."""
    if (record or {}).get("schema") != SCHEMA:
        raise RoadmapError(
            f"unrecognised record schema: {(record or {}).get('schema')!r} (expected {SCHEMA!r})")
    items = []
    for uc_id, resp in (record.get("responses") or {}).items():
        state = resolve_state(resp)
        if state not in ENGAGEMENT_STATES:
            continue
        uc = use_cases.get(uc_id, {})
        ov = engagement_inputs.get(uc_id, {})
        risk = (ov.get("risk_override") or "").strip() or seed_risk(uc.get("priority_fi"))
        effort = (ov.get("effort") or "").strip() or "Med"
        items.append({
            "uc_id": uc_id,
            "state": state,
            "risk_band": risk,
            "effort_band": effort,
            "quadrant": quadrant(risk, effort),
            "regulatory_driver": regulatory_driver(uc_id, trace_rows, scope),
            "dependency": ov.get("dependency") or "",
            "proposed_engagement": f"{state} → remediate: {uc.get('short_title', uc_id)}",
        })
    items.sort(key=lambda it: (
        _QUADRANT_ORDER.get(it["quadrant"], 9),
        _RISK_ORDER.get(it["risk_band"], 9),
        0 if it["regulatory_driver"] else 1,    # regulatory-driven first (tie-breaker)
        it["uc_id"],
    ))
    menu = {"schema": OUTPUT_SCHEMA}
    if source_record:
        menu["source_record"] = source_record
    menu["frameworks_scope"] = sorted(scope)
    menu["items"] = items
    return menu


def load_use_cases(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["uc_id"]: row for row in csv.DictReader(fh)}


def load_trace(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_engagement(path):
    if not path:
        return {}
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["uc_id"]: row for row in csv.DictReader(fh)}


def preset_scope(preset_path):
    """Union of primary + overlays + baseline framework slugs from a preset YAML."""
    import yaml
    with open(preset_path, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}
    slugs = []
    for key in ("primary", "overlays", "baseline"):
        slugs += cfg.get(key) or []
    return set(slugs)


def write_menu(menu, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(menu, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    ap = argparse.ArgumentParser(
        description="Generate engagement-menu.json from an assessment record.")
    ap.add_argument("record", help="path to assessment-record.json")
    ap.add_argument("-o", "--output", default="engagement-menu.json", help="output JSON path")
    ap.add_argument("--engagement", help="per-engagement CSV "
                    "(uc_id,risk_override,effort,dependency,escalation_control)")
    ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides preset scope)")
    ap.add_argument("--preset", default="financial",
                    help="preset name for default framework scope (default: financial)")
    ap.add_argument("--use-cases", default=os.path.join(root, "matrix", "domains", "secrets", "use-cases.csv"))
    ap.add_argument("--trace", default=os.path.join(root, "matrix", "domains", "secrets", "regulatory-trace.csv"))
    args = ap.parse_args(argv)

    with open(args.record, encoding="utf-8") as fh:
        record = json.load(fh)
    use_cases = load_use_cases(args.use_cases)
    trace = load_trace(args.trace)
    engagement = load_engagement(args.engagement)
    if args.frameworks:
        scope = {s.strip() for s in args.frameworks.split(",") if s.strip()}
    else:
        scope = preset_scope(os.path.join(
            root, "matrix", "config", "presets", f"{args.preset}.yaml"))

    menu = build_engagement_menu(record, use_cases, trace, engagement, scope,
                                 source_record=args.record)
    write_menu(menu, args.output)
    print(f"Wrote {args.output} ({len(menu['items'])} engagement items)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

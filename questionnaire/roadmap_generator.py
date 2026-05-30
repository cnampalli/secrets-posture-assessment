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

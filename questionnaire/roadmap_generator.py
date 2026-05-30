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

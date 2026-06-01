#!/usr/bin/env python3
"""Build a self-contained, interactive exec-summary HTML from an assessment record.

Mirrors questionnaire/build_questionnaire.py: inline a JSON data block +
exec-summary.css + exec-summary.js into exec-summary-template.html via
/*__TOKEN__*/ replacement -> one offline file. Snapshot counts are computed here
(reusing record_state.resolve_state); the engagement menu comes from
roadmap_generator (generator-as-library).

CLI: python3 -m presentation.build_exec_summary <record.json> -o exec-summary.html \
        [--preset financial | --frameworks slug,slug] [--client NAME] [--as-of DATE]
"""
import argparse
import json
import os
import sys
from collections import Counter

from questionnaire.record_state import resolve_state
from questionnaire import roadmap_generator as rg

_STATES = ("MET", "PARTIAL", "GAP", "PENDING")
TOKENS = ("/*__CSS__*/", "/*__DATA__*/null", "/*__APP__*/")


class ExecSummaryError(Exception):
    pass


def snapshot_counts(record):
    """Count resolved states across all responses -> {MET, PARTIAL, GAP, PENDING}."""
    c = Counter(resolve_state(r) for r in (record.get("responses") or {}).values())
    return {s: c.get(s, 0) for s in _STATES}


def inject(template, css, data, app):
    """Replace the three injection tokens; raise if any is missing."""
    for tok in TOKENS:
        if tok not in template:
            raise ExecSummaryError(f"template missing injection token: {tok}")
    return (template
            .replace("/*__CSS__*/", css)
            .replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
            .replace("/*__APP__*/", app))

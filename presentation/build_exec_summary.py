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
import brand_fonts
import brand_tokens

_STATES = ("MET", "PARTIAL", "GAP", "PENDING")
TOKENS = ("/*__FONTS__*/", "/*__TOKENS__*/", "/*__CSS__*/", "/*__DATA__*/null", "/*__APP__*/")


class ExecSummaryError(Exception):
    pass


def snapshot_counts(record):
    """Count resolved states across all responses -> {MET, PARTIAL, GAP, PENDING}."""
    c = Counter(resolve_state(r) for r in (record.get("responses") or {}).values())
    return {s: c.get(s, 0) for s in _STATES}


def inject(template, css, data, app, fonts="", tokens=""):
    """Replace the injection tokens; raise if any is missing."""
    for tok in TOKENS:
        if tok not in template:
            raise ExecSummaryError(f"template missing injection token: {tok}")
    return (template
            .replace("/*__FONTS__*/", fonts)
            .replace("/*__TOKENS__*/", tokens)
            .replace("/*__CSS__*/", css)
            .replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
            .replace("/*__APP__*/", app))


def build(record_path, out_path=None, preset="financial", frameworks=None, client="", as_of=""):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    out_path = str(out_path) if out_path else os.path.join(here, "exec-summary.html")

    with open(record_path, encoding="utf-8") as fh:
        record = json.load(fh)
    snapshot = snapshot_counts(record)
    use_cases = rg.load_use_cases(os.path.join(root, "matrix", "use-cases.csv"))
    trace = rg.load_trace(os.path.join(root, "matrix", "regulatory-trace.csv"))
    if frameworks:
        scope = {s.strip() for s in frameworks.split(",") if s.strip()}
    else:
        scope = rg.preset_scope(os.path.join(
            root, "matrix", "config", "presets", f"{preset}.yaml"))
    menu = rg.build_engagement_menu(record, use_cases, trace, {}, scope,
                                    source_record=os.path.basename(record_path))
    data = {"snapshot": snapshot, "menu": menu,
            "meta": {"client": client, "as_of": as_of,
                     "frameworks_scope": menu["frameworks_scope"],
                     "total_ucs": sum(snapshot.values())}}

    template = open(os.path.join(here, "exec-summary-template.html"), encoding="utf-8").read()
    css = open(os.path.join(here, "exec-summary.css"), encoding="utf-8").read()
    app = open(os.path.join(here, "exec-summary.js"), encoding="utf-8").read()
    html = inject(template, css, data, app,
                  fonts=brand_fonts.fontface_css(), tokens=brand_tokens.tokens_css())
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes; "
          f"{len(menu['items'])} engagement items)")
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Build a self-contained exec-summary HTML from an assessment record.")
    ap.add_argument("record", help="path to assessment-record.json")
    ap.add_argument("-o", "--output", default=None, help="output HTML path")
    ap.add_argument("--preset", default="financial", help="preset for framework scope")
    ap.add_argument("--frameworks", help="comma-separated framework slugs (overrides preset)")
    ap.add_argument("--client", default="", help="client name for the header (optional)")
    ap.add_argument("--as-of", default="", dest="as_of", help="as-of date for the header (optional)")
    args = ap.parse_args(argv)
    build(args.record, out_path=args.output, preset=args.preset,
          frameworks=args.frameworks, client=args.client, as_of=args.as_of)
    return 0


if __name__ == "__main__":
    sys.exit(main())

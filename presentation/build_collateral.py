#!/usr/bin/env python3
"""Build The Instrument's marketing collateral from templates + live-data stats.

Mirrors presentation/build_exec_summary.py: token injection into template HTML.
All headline numbers come from instrument_stats.compute_stats() (recomputed from
the live CSVs on every build) — no count is ever hardcoded in the collateral.

For each instrument-*-template.html this script substitutes every __STAT_*__
token and writes the final instrument-*.html. The build FAILS (nonzero exit) if
a template carries a token with no computed stat, or if any __STAT_ token
survives substitution. It also refreshes instrument-stats.json.

CLI: python3 presentation/build_collateral.py [--templates DIR] [--out DIR]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import instrument_stats  # noqa: E402

TEMPLATES = {
    "instrument-overview-template.html": "instrument-overview.html",
    "instrument-one-slide-template.html": "instrument-one-slide.html",
    "instrument-a4-template.html": "instrument-a4.html",
}
_TOKEN_RE = re.compile(r"__STAT_[A-Z0-9_]*?__")


class CollateralError(Exception):
    pass


def inject(template, tokens, name="template"):
    """Substitute every __STAT_*__ token; raise on unknown or leftover tokens."""
    found = set(_TOKEN_RE.findall(template))
    unknown = found - set(tokens)
    if unknown:
        raise CollateralError(f"{name}: unknown stat token(s): {sorted(unknown)}")
    html = template
    for tok in sorted(found):
        html = html.replace(tok, tokens[tok])
    leftover = _TOKEN_RE.findall(html)
    if leftover:
        raise CollateralError(f"{name}: unsubstituted token(s) remain: {sorted(set(leftover))}")
    return html


def build_all(template_dir=HERE, out_dir=None, stats=None):
    """Build every collateral HTML; returns list of written paths."""
    out_dir = out_dir or template_dir
    if stats is None:
        stats = instrument_stats.compute_stats()
    tokens = instrument_stats.stat_tokens(stats)
    written = []
    for tpl_name, out_name in sorted(TEMPLATES.items()):
        tpl_path = os.path.join(template_dir, tpl_name)
        if not os.path.exists(tpl_path):
            raise CollateralError(f"missing template: {tpl_path}")
        with open(tpl_path, encoding="utf-8") as fh:
            template = fh.read()
        if not _TOKEN_RE.search(template):
            raise CollateralError(f"{tpl_name}: no __STAT_ tokens found — not a template?")
        html = inject(template, tokens, name=tpl_name)
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(out_path)
    written.append(instrument_stats.write_stats_json(
        stats, os.path.join(out_dir, "instrument-stats.json")))
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Inject live-data stats into the instrument collateral templates.")
    ap.add_argument("--templates", default=HERE, help="directory holding the *-template.html files")
    ap.add_argument("--out", default=None, help="output directory (default: templates dir)")
    args = ap.parse_args(argv)
    try:
        written = build_all(template_dir=args.templates, out_dir=args.out)
    except (CollateralError, instrument_stats.StatsError, OSError) as exc:
        print(f"build_collateral: FAIL: {exc}", file=sys.stderr)
        return 1
    for path in written:
        print(f"Wrote {path} ({os.path.getsize(path)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build per-domain backlog CSVs (GAP/PARTIAL work items) next to each domain report.

Writes <data_dir>/<slug>-backlog.csv for every registered domain, importable into
both Jira and Azure DevOps (see BACKLOG-IMPORT.md for the column mapping)."""
import os
import pathlib

import domains
import report_io
import backlog
import engagement_config as _ec

_PRESETS = pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / "config" / "presets"


def build():
    """Write one CSV per domain. Returns [(slug, path, row_count)]."""
    results = []
    for dom in domains.DOMAINS.values():
        inp = report_io.load_inputs(dom.data_dir, None, dom)
        reg_rows = inp["reg_rows"]
        available = list(dict.fromkeys(r["framework_slug"] for r in reg_rows))
        engagement = _ec.resolve(preset=None, config_path=None, cli_frameworks=None,
                                 available=available, presets_dir=_PRESETS)
        scope = set(engagement.selected) if not engagement.is_default else set(available)
        rows = backlog.build_backlog_rows(inp["anz"], inp["ucs"], reg_rows, scope, dom.slug)
        dst = os.path.join(dom.data_dir, f"{dom.slug}-backlog.csv")
        with open(dst, "w", encoding="utf-8", newline="") as f:
            f.write(backlog.to_csv(rows))
        results.append((dom.slug, dst, len(rows)))
    return results


if __name__ == "__main__":
    for slug, dst, n in build():
        print(f"Wrote {dst} ({n} backlog rows)")

#!/usr/bin/env python3
"""Compute live headline stats for The Instrument's marketing collateral.

Every number the collateral claims (use cases, identity classes, vendors,
archetypes, control-level frameworks, regulatory-trace rows, verbatim quotes)
is derived here, directly from the live data files — never hardcoded:

  - matrix/domains/{secrets,pam,iga}/use-cases.csv        -> uc_* counts
  - matrix/domains/{secrets,pam,iga}/identity-catalog.csv -> identity_* counts
  - matrix/domains/{secrets,pam,iga}/regulatory-trace.csv -> trace/quote/framework counts
  - matrix/domains/{secrets,pam}/vendor-capabilities-*.csv + iga/iga-vendor-fit.csv
                                                          -> vendors_* counts
  - methodology/assessment-archetypes.csv                 -> archetypes + range
  - matrix/config/frameworks.yaml                         -> slug validation

"Frameworks mapped at control level" is defensibly defined as the distinct
framework slugs that appear in any domain's regulatory-trace with a
control-mapping role (PRIMARY-LENS or BACK-MAP). Threat-context, adversary-lens
and informative rows (MITRE ATT&CK, OWASP LLM, incident disclosures) are
excluded: they carry cited quotes but are not control-level mappings.

CLI: python3 presentation/instrument_stats.py [-o instrument-stats.json]
Emits a deterministic (sorted-keys) JSON stats file.
"""
import argparse
import csv
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DOMAINS = ("secrets", "pam", "iga")
CONTROL_LEVEL_ROLES = {"PRIMARY-LENS", "BACK-MAP"}
STATS_JSON = os.path.join(HERE, "instrument-stats.json")


class StatsError(Exception):
    pass


def _rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _framework_slugs(path):
    """Top-level keys of frameworks.yaml (minimal parse; no yaml dep needed)."""
    slugs = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            stripped = line.rstrip()
            if stripped and not line[0].isspace() and not stripped.startswith("#") \
                    and stripped.endswith(":"):
                slugs.add(stripped[:-1])
    return slugs


def _vendor_count(domain_dir, domain):
    """Vendors per domain: per-vendor capability CSVs; IGA uses iga-vendor-fit.csv."""
    if domain == "iga":
        fit = _rows(os.path.join(domain_dir, "iga-vendor-fit.csv"))
        return len({r["vendor_slug"] for r in fit})
    return len(glob.glob(os.path.join(domain_dir, "vendor-capabilities-*.csv")))


def compute_stats(root=ROOT):
    """Return the flat stats dict, every value recomputed from live data."""
    stats = {"domains": len(DOMAINS)}
    uc_total = identity_total = vendors_total = 0
    trace_total = verbatim = elided = 0
    control_slugs = set()

    for domain in DOMAINS:
        ddir = os.path.join(root, "matrix", "domains", domain)
        uc = len(_rows(os.path.join(ddir, "use-cases.csv")))
        ident = len(_rows(os.path.join(ddir, "identity-catalog.csv")))
        trace = _rows(os.path.join(ddir, "regulatory-trace.csv"))
        vendors = _vendor_count(ddir, domain)
        if not uc or not ident or not trace or not vendors:
            raise StatsError(f"empty live-data count for domain {domain!r}")
        stats[f"uc_{domain}"] = uc
        stats[f"identity_{domain}"] = ident
        stats[f"vendors_{domain}"] = vendors
        stats[f"trace_rows_{domain}"] = len(trace)
        uc_total += uc
        identity_total += ident
        vendors_total += vendors
        trace_total += len(trace)
        for row in trace:
            if row.get("framework_role") in CONTROL_LEVEL_ROLES:
                control_slugs.add(row["framework_slug"])
            qt = row.get("quote_type", "")
            if qt == "verbatim":
                verbatim += 1
            elif qt == "verbatim-elided":
                elided += 1

    known = _framework_slugs(os.path.join(root, "matrix", "config", "frameworks.yaml"))
    unknown = control_slugs - known
    if unknown:
        raise StatsError(f"trace framework slugs missing from frameworks.yaml: {sorted(unknown)}")

    archetypes = _rows(os.path.join(root, "methodology", "assessment-archetypes.csv"))
    ids = [r["archetype_id"] for r in archetypes]
    if not ids:
        raise StatsError("no archetypes found in methodology/assessment-archetypes.csv")

    stats.update({
        "uc_total": uc_total,
        "identity_total": identity_total,
        "vendors_total": vendors_total,
        "trace_rows_total": trace_total,
        "quotes_verbatim": verbatim,
        "quotes_verbatim_elided": elided,
        "quotes_total": verbatim + elided,
        "archetypes": len(ids),
        "archetype_range": f"{min(ids)}–{max(ids)}",
        "frameworks_control_level": len(control_slugs),
        "frameworks_control_level_slugs": sorted(control_slugs),
    })
    return stats


def stat_tokens(stats):
    """Map __STAT_*__ template tokens -> string values (collateral headline numbers)."""
    return {
        "__STAT_DOMAINS__": str(stats["domains"]),
        "__STAT_UC_TOTAL__": str(stats["uc_total"]),
        "__STAT_UC_SECRETS__": str(stats["uc_secrets"]),
        "__STAT_UC_PAM__": str(stats["uc_pam"]),
        "__STAT_UC_IGA__": str(stats["uc_iga"]),
        "__STAT_IDENTITY_CLASSES__": str(stats["identity_total"]),
        "__STAT_IDENTITY_SECRETS__": str(stats["identity_secrets"]),
        "__STAT_IDENTITY_PAM__": str(stats["identity_pam"]),
        "__STAT_IDENTITY_IGA__": str(stats["identity_iga"]),
        "__STAT_VENDORS_SECRETS__": str(stats["vendors_secrets"]),
        "__STAT_VENDORS_PAM__": str(stats["vendors_pam"]),
        "__STAT_VENDORS_IGA__": str(stats["vendors_iga"]),
        "__STAT_ARCHETYPES__": str(stats["archetypes"]),
        "__STAT_ARCHETYPE_RANGE__": stats["archetype_range"],
        "__STAT_FRAMEWORKS_CONTROL_LEVEL__": str(stats["frameworks_control_level"]),
    }


def write_stats_json(stats, out_path=STATS_JSON):
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compute live collateral stats and emit instrument-stats.json.")
    ap.add_argument("-o", "--output", default=STATS_JSON, help="output JSON path")
    args = ap.parse_args(argv)
    try:
        stats = compute_stats()
    except (StatsError, OSError, KeyError) as exc:
        print(f"instrument_stats: {exc}", file=sys.stderr)
        return 1
    out = write_stats_json(stats, args.output)
    print(f"Wrote {out} ({len(stats)} stats; uc_total={stats['uc_total']}, "
          f"identity_total={stats['identity_total']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

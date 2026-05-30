#!/usr/bin/env python3
"""Project an assessment-record.json into a report-ready current-state CSV.

Closes the answer->report loop: matrix/build_matrix_viewer.py reads the CSV this
writes (point it via --current-state). Keeps the legacy column schema so the
report is unchanged; the column/file rename is deferred to WS-5.

CLI: python3 -m questionnaire.report_adapter <record.json> -o <current-state.csv>
"""
import argparse
import csv
import json
import os
import sys

# Put repo root on sys.path so this resolves as `questionnaire.report_adapter`
# whether run as a script or imported as a package member.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SCHEMA = "posture-assessment-record/v1"
COLUMNS = ["uc_id", "anz_state", "confidence", "evidence_q_ids",
           "evidence_redacted", "gap_notes", "sensitivity_tag", "citation_keys"]


class AdapterError(Exception):
    pass


def record_to_rows(record):
    """Map an assessment record's responses to current-state CSV rows (sorted by uc_id)."""
    if record.get("schema") != SCHEMA:
        raise AdapterError(
            f"unrecognised record schema: {record.get('schema')!r} (expected {SCHEMA!r})")
    rows = []
    for uc_id in sorted(record.get("responses") or {}):
        r = record["responses"][uc_id] or {}
        answers = r.get("answers") or {}
        answered = [k for k, v in answers.items() if v not in (None, False)]
        rows.append({
            "uc_id": uc_id,
            "anz_state": r.get("final_state") or r.get("proposed_state") or "PENDING",
            "confidence": r.get("confidence") or "MED",
            "evidence_q_ids": ";".join(sorted(answered)),
            "evidence_redacted": "",
            "gap_notes": r.get("rationale") or "",
            "sensitivity_tag": "",
            "citation_keys": "",
        })
    return rows


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Project assessment-record.json -> report current-state CSV.")
    ap.add_argument("record", help="path to assessment-record.json")
    ap.add_argument("-o", "--output", default="current-state.csv", help="output CSV path")
    args = ap.parse_args(argv)
    with open(args.record, encoding="utf-8") as fh:
        record = json.load(fh)
    rows = record_to_rows(record)
    write_csv(rows, args.output)
    print(f"Wrote {args.output} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

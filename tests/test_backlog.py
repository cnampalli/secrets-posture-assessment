import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(os.path.dirname(HERE), "matrix")
sys.path.insert(0, MATRIX)
import backlog  # noqa: E402

UCS = [
    {"uc_id": "UC-S-001", "short_title": "Secret rotation", "priority_fi": "P0", "story": "Rotate secrets."},
    {"uc_id": "UC-S-002", "short_title": "Discovery", "priority_fi": "P1", "story": "Find secrets."},
    {"uc_id": "UC-S-003", "short_title": "Audit, with \"quotes\"", "priority_fi": "P2", "story": "Log access."},
    {"uc_id": "UC-S-004", "short_title": "Already done", "priority_fi": "P0", "story": "n/a"},
]
ANZ = [
    {"uc_id": "UC-S-001", "current_state": "GAP", "recommendation": "Add rotation."},
    {"uc_id": "UC-S-002", "current_state": "PARTIAL", "recommendation": "Extend discovery."},
    {"uc_id": "UC-S-003", "current_state": "GAP", "recommendation": "Enable audit."},
    {"uc_id": "UC-S-004", "current_state": "MET", "recommendation": ""},
]
REG = []  # no regulatory trace in this fixture
SCOPE = set()


def test_only_gap_and_partial_exported():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    ids = {r["UC-ID"] for r in rows}
    assert ids == {"UC-S-001", "UC-S-002", "UC-S-003"}  # MET UC-S-004 excluded


def test_priority_sorts_p0_first():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    assert rows[0]["UC-ID"] == "UC-S-001"   # P0 -> Highest, top of list
    assert rows[0]["Priority"] == "Highest"
    assert rows[-1]["Priority"] == "Medium"  # P2


def test_row_has_all_both_tool_columns():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    expected = {"Summary", "Work Item Type", "Description", "Priority", "Labels",
                "UC-ID", "Domain", "Regulatory-Driver", "State"}
    assert set(rows[0]) == expected
    assert rows[0]["Work Item Type"] == "Task"
    assert rows[0]["Domain"] == "secrets"


def test_to_csv_escapes_quotes_and_commas():
    rows = backlog.build_backlog_rows(ANZ, UCS, REG, SCOPE, "secrets")
    out = backlog.to_csv(rows)
    parsed = list(csv.DictReader(io.StringIO(out)))
    titles = {r["UC-ID"]: r["Summary"] for r in parsed}
    assert 'quotes' in titles["UC-S-003"]      # round-trips through the quoting
    assert parsed[0]["UC-ID"] == "UC-S-001"     # header + order preserved


def test_to_csv_empty_rows_is_header_only():
    out = backlog.to_csv([])
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 1  # header row only
    assert "Summary" in lines[0]

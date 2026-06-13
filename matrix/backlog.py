"""GAP/PARTIAL backlog export — pure model builder + CSV serialisation (no file I/O).

Turns a domain's open use cases (GAP + PARTIAL only) into work-item rows whose columns
import cleanly into BOTH Jira and Azure DevOps. Priority is carried from the use-case
priority_fi so P0s sort to the top. CSV serialisation is RFC-4180 (csv module)."""
import csv
import io
import os
import sys

# regulatory_driver lives in questionnaire/ — make the repo root importable.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.append(_ROOT)
from questionnaire.roadmap_generator import regulatory_driver

_OPEN_STATES = ("GAP", "PARTIAL")

COLUMNS = ["Summary", "Work Item Type", "Description", "Priority", "Labels",
           "UC-ID", "Domain", "Regulatory-Driver", "State"]

# priority_fi -> (display priority, sort rank). Jira accepts these names directly;
# the README documents the ADO numeric mapping (Highest->1 ... Low->4).
_PRIORITY = {"P0": ("Highest", 0), "P1": ("High", 1), "P2": ("Medium", 2)}
_PRIORITY_DEFAULT = ("Low", 3)


def build_backlog_rows(anz, ucs, reg_rows, scope, domain_slug):
    """Every GAP/PARTIAL use case -> one work-item row. Sorted P0-first, then by UC id."""
    uc_by_id = {u["uc_id"]: u for u in ucs}
    rows = []
    for a in anz:
        state = (a.get("current_state") or "").strip()
        if state not in _OPEN_STATES:
            continue
        uc_id = a["uc_id"]
        uc = uc_by_id.get(uc_id, {})
        title = uc.get("short_title", uc_id)
        prio_label, prio_rank = _PRIORITY.get((uc.get("priority_fi") or "").strip(),
                                              _PRIORITY_DEFAULT)
        drivers = regulatory_driver(uc_id, reg_rows, scope)
        driver_str = "; ".join(d["control_code"] for d in drivers)
        desc = (a.get("recommendation") or uc.get("story") or "").strip()
        labels = " ".join([domain_slug, state.lower()]
                          + [d["framework_slug"] for d in drivers])
        rows.append({
            "Summary": f"[{state}] {title}",
            "Work Item Type": "Task",
            "Description": desc,
            "Priority": prio_label,
            "Labels": labels,
            "UC-ID": uc_id,
            "Domain": domain_slug,
            "Regulatory-Driver": driver_str,
            "State": state,
            "_rank": prio_rank,
        })
    rows.sort(key=lambda r: (r["_rank"], r["UC-ID"]))
    for r in rows:
        r.pop("_rank")
    return rows


def to_csv(rows):
    """Serialise rows to an RFC-4180 CSV string (header always emitted)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return buf.getvalue()

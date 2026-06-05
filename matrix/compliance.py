"""Identity-control coverage indicator (D3) + gap-to-target planner (D4). Pure.

Coverage is computed against the *identity-scoped* control set in
regulatory-trace.csv — deliberately not the full GRC control set of each
framework. Outputs are a coverage INDICATOR, not a compliance score.

A control's state is the worst state among its mapped use cases, so a control is
MET only when every mapped UC is MET. An unassessed mapped UC (UNKNOWN) ranks
below MET, so it blocks MET and surfaces in gap-to-target rather than being ignored.
"""
from matrix_vocab import STATE_RANK


def _state_by_uc(anz):
    return {a["uc_id"]: a.get("current_state", "UNKNOWN") for a in anz}


def _control_state(uc_ids, state_by_uc):
    states = [state_by_uc.get(u, "UNKNOWN") for u in uc_ids]
    if not states:
        return "UNKNOWN"
    return min(states, key=lambda s: STATE_RANK.get(s, 9))


def _control_rows(reg_rows):
    for r in reg_rows:
        uc_ids = [u.strip() for u in (r.get("uc_ids", "") or "").split(";") if u.strip()]
        yield r["framework_slug"], r["control_code"], r.get("control_short_title", ""), uc_ids


def coverage_indicator(reg_rows, anz):
    """Per-framework identity-control coverage indicator.

    {framework: {total, met, partial, pending, gap, unknown, met_pct}}.
    met_pct = met / total (controls where every mapped UC is MET).
    """
    sbu = _state_by_uc(anz)
    out = {}
    for fw, _code, _title, uc_ids in _control_rows(reg_rows):
        bucket = out.setdefault(fw, {"total": 0, "met": 0, "partial": 0,
                                     "pending": 0, "gap": 0, "unknown": 0})
        bucket["total"] += 1
        st = _control_state(uc_ids, sbu)
        bucket[{"MET": "met", "PARTIAL": "partial", "PENDING": "pending",
                "GAP": "gap"}.get(st, "unknown")] += 1
    for b in out.values():
        b["met_pct"] = round(b["met"] / b["total"], 4) if b["total"] else 0.0
    return out


def gap_to_target(reg_rows, anz, framework=None, target_state="MET"):
    """Controls not yet at `target_state`, with the UCs blocking them (D4).

    Returns [{framework, code, title, state, blocking_ucs:[{uc, state}]}],
    sorted worst control-state first then code. blocking_ucs are the mapped UCs
    below the target.
    """
    sbu = _state_by_uc(anz)
    target_rank = STATE_RANK.get(target_state, 3)
    rows = []
    for fw, code, title, uc_ids in _control_rows(reg_rows):
        if framework is not None and fw != framework:
            continue
        st = _control_state(uc_ids, sbu)
        if STATE_RANK.get(st, 9) >= target_rank:
            continue  # already at/above target
        blocking = [{"uc": u, "state": sbu.get(u, "UNKNOWN")}
                    for u in uc_ids
                    if STATE_RANK.get(sbu.get(u, "UNKNOWN"), 9) < target_rank]
        rows.append({"framework": fw, "code": code, "title": title,
                     "state": st, "blocking_ucs": blocking})
    rows.sort(key=lambda r: (STATE_RANK.get(r["state"], 9), r["code"]))
    return rows

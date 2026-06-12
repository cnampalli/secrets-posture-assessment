"""Reference posture-state derivation for the WS-1 archetype rubric.

derive_state applies the laddering rule for an archetype use case (A1-A8).
A0 (bespoke) use cases are scored manually and do NOT call this function.
Pure: no I/O, no globals. Mirrored by questionnaire/scoring.js."""

VALID_ANSWERS = {"yes", "no", "na"}


def derive_state(questions, answers):
    """questions: [{"qid": str, "informs_state": "GAP_PARTIAL"|"PARTIAL_MET"}].
    answers: {qid: "yes"|"no"|"na"|None}. Returns GAP|PARTIAL|MET|PENDING|NA.

    Empty `questions` is a programming error (an archetype UC always has questions;
    A0/bespoke is scored manually and never calls this) — raise rather than silently
    fall through to MET, which would mark an unassessed use case as fully covered."""
    if not questions:
        raise ValueError("derive_state requires at least one question "
                         "(empty input would silently return MET)")
    vals = [(q["informs_state"], answers.get(q["qid"])) for q in questions]
    if vals and all(v == "na" for _, v in vals):
        return "NA"
    if any(v not in VALID_ANSWERS for _, v in vals):   # None or missing
        return "PENDING"
    if any(inf == "GAP_PARTIAL" and v == "no" for inf, v in vals):
        return "GAP"
    if any(inf == "PARTIAL_MET" and v == "no" for inf, v in vals):
        return "PARTIAL"
    return "MET"

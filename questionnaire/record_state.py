"""Shared assessment-record helpers (used by report_adapter and roadmap_generator)."""

SCHEMA = "posture-assessment-record/v1"


def resolve_state(response):
    """Effective state of a response: final_state -> proposed_state -> 'PENDING'."""
    response = response or {}
    return response.get("final_state") or response.get("proposed_state") or "PENDING"

# ADR-012: Methodology Playbook (make the engagement reproducible)

**Status:** Accepted
**Date:** 2026-05-30
**Workstream:** WS-4

## Context
WS-1 through WS-3 built the *instrument* — the scoring rubric, the selectable regulatory overlay,
the questionnaire, and the report adapter that closes the answer→report loop. But the end-to-end
*procedure* that turns those parts into a client engagement was undocumented. WS-4 needs a
repeatable, written methodology so the assessment — and its GAP/PARTIAL engagement menu (the
consulting wedge) — is reproducible across clients rather than re-improvised each time.

## Decision
Write two separate markdown docs in `methodology/`, sharing one engagement-lifecycle skeleton:

- `PLAYBOOK.md` — the internal consultant operating manual.
- `METHODOLOGY.md` — the client-facing, distilled view.

Both follow the same **6-stage lifecycle**: Scope → Collect evidence → Score → Report current state
→ Build the remediation roadmap → Re-assess. Finding prioritisation uses **risk × effort quadrants
with regulation as the tie-breaker/escalator** — qualitative bands only, no invented numbers. The
spine is client-agnostic; the XYZ worked example is confined to marked blockquote callouts so the
procedure reads as reusable, not as one client's case study.

## Alternatives considered (rejected)
- **A single layered doc for both audiences** — blurs the consultant runbook into the client
  deliverable; neither reads cleanly.
- **Single-source-generated views** (one source emitting both docs) — premature machinery for two
  short docs; YAGNI until the content stabilises.
- **A client-facing HTML deck this slice** — conflates the runbook with a presentation artifact;
  deferred to a later WS-4 slice.

## Consequences
- (+) The engagement is now reproducible end-to-end: a new client can be run through the same six
  stages with the same prioritisation logic.
- (+) Two audiences, two docs — the consultant manual can carry internal detail the client view omits.
- (−) The remediation-roadmap **generator** (auto-emit the engagement menu from
  `assessment-record.json`) and the exec-summary print view remain later WS-4 slices; the
  prioritisation method is documented but not yet code.
- Cross-doc hygiene follow-up: `RUBRIC.md` §5 names the override field `override_reason`, while the
  implemented schema and this playbook use `rationale` — reconcile in a later cleanup.

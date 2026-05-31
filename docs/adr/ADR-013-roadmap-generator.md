# ADR-013: Roadmap Generator (emit the engagement menu from a record)

**Status:** Accepted
**Date:** 2026-05-31
**Workstream:** WS-4 slice 2

## Context
WS-4 slice 1 documented the risk × effort prioritisation method — how gaps become a sequenced
engagement menu. That slice produced prose, not code. This slice turns the method into a transform
that emits the engagement menu (the consulting wedge) from an `assessment-record.json`, so a future
exec-summary print view can render it.

## Decision
Add `questionnaire/roadmap_generator.py` — a pure transform plus a thin CLI, mirroring the
report adapter. Risk seeds from `priority_fi` (P0→High, P1→Med, else→Low) and is overridable in a
per-engagement CSV; effort comes from that same CSV (default Med); each finding's quadrant is the
risk × effort product. The regulatory driver is scoped to the financial preset by default
(MITRE / ADVERSARY-LENS excluded), capped one-per-framework and at most three, regulator-first.
**Regulation is an ordering tie-breaker only** — the obligation-bearing finding sorts first;
band escalation is a logged assessor judgment carried in the `escalation_control` column, never an
automatic consequence of a control mapping to the finding. Output is `engagement-menu/v1` JSON with
no timestamp, so diffs are byte-stable. The state-resolution rule was extracted into a shared
`questionnaire/record_state.py` so the menu and the report never disagree on a finding's state.

## Alternatives rejected
- **Auto risk-band escalation on control presence** — would inflate nearly every FI gap, since most
  map to some obligation; dishonest and unusable.
- **Archetype-derived effort** — a proxy for effort, not real effort; the assessor's per-engagement
  read is the source of truth.
- **Emitting the full control list** (4–39 controls per finding) — unreadable as a menu; the capped
  regulator-first driver is the signal that matters.
- **A human-rendered output this slice** — deferred to the print-view slice; this slice emits
  machine-stable JSON only.

## Consequences
- (+) The wedge is now generated from a real record, not hand-authored.
- (+) Shared `record_state.py` keeps the menu and report in agreement by construction.
- The exec-summary print view (which renders this JSON) is the next slice.
- Effort, risk overrides, dependencies, and escalation are consultant inputs
  (facilitated-primary) supplied via the per-engagement CSV, not derived.
- (−) No Privacy Act driver exists — there is no trace data for it; it remains a methodology
  stance only.

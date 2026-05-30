# ADR-010: Interactive Assessment Instrument (WS-3 slice 1)

**Status:** Accepted
**Date:** 2026-05-29
**Workstream:** WS-3

## Context
The WS-1 rubric (archetype library) needed an operational front door: a way for a
consultant to score a client's posture live and produce a portable assessment artifact.

## Decision
Build a self-contained HTML questionnaire baked from the rubric CSVs by a Python build
step (the build_matrix_viewer.py pattern). The scoring ladder is authored once in
`methodology/scoring.py` (tested reference) and mirrored in `questionnaire/scoring.js`,
both pinned to a shared `scoring-vectors.json` to prevent drift. The instrument exports
and imports a rich `assessment-record.json` (the single source of truth); answers autosave
to localStorage. A0 use cases are scored manually with their bespoke criteria as guidance.
The Variant-A focused wizard is the chosen flow.

## Consequences
- (+) Operational instrument that closes the answer→export→re-import round-trip; engine is
  unit-tested in Python and conformance-tested in JS.
- (+) Presentation is separated from engine + rubric, so the Variant-B worksheet view can
  layer on later without re-architecting.
- (−) Dual engine risks drift — mitigated by the shared vector fixture.
- Deferred: the report adapter (assessment-record → current-state.csv consumed by
  build_matrix_viewer.py), framework-selection UI, Variant-B view, and numeric quantitative
  inputs. The answer→report loop is therefore not yet closed.

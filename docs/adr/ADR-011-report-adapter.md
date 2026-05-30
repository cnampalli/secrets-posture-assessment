# ADR-011: Report Adapter (close the answer→report loop)

**Status:** Accepted
**Date:** 2026-05-30
**Workstream:** WS-3 follow-up

## Context
The WS-3 questionnaire exports a rich `assessment-record.json`, but the report
(`matrix/build_matrix_viewer.py`) reads a `current-state.csv`. Nothing connected the two, so a
real assessment could not drive the report (the answer→report loop was open).

## Decision
Add `questionnaire/report_adapter.py` that projects a record's responses into the report's
current-state schema (`final_state`→`anz_state`, `confidence`, `rationale`→`gap_notes`, answered
qids as `evidence_q_ids` provenance). Wire it with an additive `--current-state <path>` flag on
`build_matrix_viewer.py` that defaults to the existing `anz-current-state.csv` — so the default
build is byte-unchanged and the frozen demo data is untouched. An end-to-end test proves a record
drives the report's UC states.

## Consequences
- (+) The instrument is now end-to-end: questionnaire → record → CSV → report.
- (+) Regression-safe: default behaviour and the frozen demo are unchanged (WS-2 golden test
  still passes); the adapter writes a separate client-supplied file.
- (−) The output keeps the legacy `anz_state` column name so the report reads it unchanged.
  Renaming the column and the `anz-current-state.csv` file to client-generic names is deferred to
  WS-5.
- The adapter projects only what the questionnaire captures; `evidence_redacted`, `sensitivity_tag`,
  and `citation_keys` are emitted blank (future enrichment).

# Report Adapter — Design Spec

**Date:** 2026-05-30
**Branch:** `report-adapter` (off `main`)
**Status:** Approved-by-delegation ("follow the next steps") — regression-safe defaults
**Source:** WS-3 deferred follow-up — close the answer→report loop

---

## 1. Purpose

Close the **answer → report** loop. The WS-3 questionnaire exports a rich
`assessment-record.json`; the report (`matrix/build_matrix_viewer.py`) reads a
`current-state.csv`. This adapter projects the record into that CSV so a real
assessment drives the report.

## 2. Non-goals

- No rename of the `anz_state` column or the `anz-current-state.csv` file (WS-5 scope).
- No change to default report behaviour: the frozen `anz-current-state.csv` demo stays the
  default input; a no-flag build is byte-identical to today.
- No new evidence capture — the adapter projects only what the record holds.

## 3. Report input contract (ground truth)

`build_matrix_viewer.py:130-132` reads `read_csv("anz-current-state.csv")` and uses columns:
`uc_id, anz_state, confidence, evidence_redacted, gap_notes, sensitivity_tag`. The full file
schema also has `evidence_q_ids, citation_keys`. `state_by_uc` maps `anz_state`.

## 4. Mapping (`assessment-record.json` → current-state row)

| CSV column | From record |
|---|---|
| `uc_id` | response key |
| `anz_state` | `final_state` (fallback `proposed_state`, fallback `PENDING`) |
| `confidence` | `confidence` (default `MED`) |
| `evidence_q_ids` | `;`-joined answered qids/sub_ids (provenance) |
| `evidence_redacted` | `""` (not captured by the questionnaire) |
| `gap_notes` | `rationale` |
| `sensitivity_tag` | `""` |
| `citation_keys` | `""` |

Rows sorted by `uc_id` for deterministic output.

## 5. Components

| File | Status | Responsibility |
|---|---|---|
| `questionnaire/report_adapter.py` | Create | `record_to_rows(record) -> list[dict]` (pure) + `write_csv(rows, path)` + CLI (`python3 -m questionnaire.report_adapter <record.json> -o <out.csv>`). |
| `matrix/build_matrix_viewer.py` | Modify | Add `--current-state <path>` arg (default `anz-current-state.csv`); use it in the `read_csv(...)` for the current-state read. Additive, backward-compatible. |
| `tests/test_report_adapter.py` | Create | Mapping correctness, fallbacks, deterministic order, CLI round-trip. |
| `tests/test_report_adapter_e2e.py` | Create | record → adapter CSV → `build_matrix_viewer --current-state ... --emit-data` → REGDATA UC states reflect the record. |
| `docs/adr/ADR-011-report-adapter.md` | Create | Decision + deferred column rename. |
| `meta/IMPROVEMENT-BACKLOG.md` | Modify | Mark report adapter done. |

## 6. Wiring (`--current-state`)

`read_csv` joins under `matrix/`; an absolute path passed to `--current-state` is used as-is
(os.path.join ignores the base when the second arg is absolute). Default
`"anz-current-state.csv"` → unchanged behaviour (regression anchor).

## 7. Error handling

- Adapter: malformed/old-schema record → clear error (`schema` must be
  `posture-assessment-record/v1`).
- Missing `responses` → empty CSV (header only) rather than crash.
- Report: a `--current-state` path that doesn't exist → the existing `read_csv` returns `[]`
  (report already tolerates an empty current-state).

## 8. Testing (TDD)

1. `record_to_rows`: state fallback chain, rationale→gap_notes, qid provenance, sorted order.
2. Schema guard raises on wrong/absent schema.
3. CLI writes a valid 8-column CSV.
4. Default report build unchanged (no `--current-state`) — byte-faithful.
5. E2E: a 2-UC record drives the report's REGDATA UC states.

## 9. Tradeoff

The output keeps the legacy `anz_state` column name so the report reads it unchanged; renaming
to a client-generic `current_state` (and the file) is deferred to WS-5 to keep this slice
regression-safe.

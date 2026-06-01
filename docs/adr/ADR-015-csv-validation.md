# ADR-015: CSV Schema + Referential-Integrity Validation

**Status:** Accepted
**Date:** 2026-06-01
**Workstream:** WS-5 slice 1 (cleanup + validation)

## Context
The data layer — the core contracts (`use-cases.csv`, `anz-current-state.csv`,
`regulatory-trace.csv`, `identity-catalog.csv`) plus the aggregate and 19 per-vendor
`vendor-capabilities-*.csv` — had **zero** guards. A dangling `uc_id`/`nhi_id` reference, a missing
column, or a bad enum value would surface only as a downstream build/report bug, far from its cause.
WS-5 slice 1 adds the project's first data validator.

## Decision
Add a read-only `matrix/validate_data.py` mirroring the existing `methodology/validate_rubric.py`
precedent: pure check functions return lists of violation strings (empty = clean), `validate_all(root)`
aggregates them, and a CLI exits **1** on any violation else **0**.

Checks: required columns; uniqueness (`uc_id`, `nhi_id`); the use-cases/current-state `uc_id` sets
must match; value enums (`anz_state ∈ {MET,PARTIAL,GAP,PENDING,NA}`, `framework_role ∈
{PRIMARY-LENS,BACK-MAP,ADVERSARY-LENS}`, vendor `maturity` an integer 0–5, non-empty vendor
`coverage`); and referential integrity (current-state & regulatory-trace `uc_ids` ⊆ use-cases;
regulatory-trace & use-cases `nhi_ids` ⊆ identity-catalog; vendor `target_id` resolved by
`target_type` — `NHI` ⊆ identity-catalog, `UC-*` ⊆ use-cases).

The validator is **standalone + pytest**, **not wired into the builds** — this keeps the builds
byte-stable and adds no new failure modes to the build path. It is written importable so a build (or a
second-client onboarding) can call it later. `MISSING-UC`/`MISSING-NHI` are allowlisted intentional
"no-mapping" sentinels (3 `regulatory-trace.csv` rows), not dangling references.

## Alternatives considered (rejected)
- **Wire validation into the builds (fail-fast):** strongest guarantee, but adds failure modes to the
  byte-stable build path — deferred until a second client proves the seams.
- **A schema library / JSON-Schema:** stdlib mirrors the existing `validate_rubric.py` precedent with
  no new dependency.
- **Hardcoding the vendor `coverage` enum:** risked false positives; `coverage` is checked non-empty
  instead.

## Consequences
- The shipped data is certified the **golden baseline** — the integration test (`validate_all(ROOT) == []`)
  fails if a future edit breaks a contract.
- The validator is importable, so a build can adopt it later (WS-5 slice 5d / second client).
- The legacy `anz_state` column and `anz-current-state.csv` filename are validated **as-is**; their
  rename is WS-5 slice 5b.

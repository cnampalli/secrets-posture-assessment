# ADR-016: Legacy `anz` Schema Rename

**Status:** Accepted
**Date:** 2026-06-02
**Workstream:** WS-5 slice 2 (5b)

## Context
The data schema hardcoded the legacy ANZ client: the `anz_state` column, the
`anz-current-state.csv` file, and the `sources_at_anz_likely` column in `identity-catalog.csv`.
This coupling undermined the project's vision — a reusable posture-assessment instrument for *any*
AU client. WS-5c added the first data validator (the safety net); this slice removes the coupling.

## Decision
Rename the three schema tokens to client-generic names across code, active data, and tests in
lockstep:

| Legacy | New |
|--------|-----|
| `anz_state` | `current_state` |
| `anz-current-state.csv` | `current-state.csv` |
| `sources_at_anz_likely` | `sources_likely` |

Scope is limited to the **data schema**. Cosmetic internal identifiers (the `XYZ` JS array
variable, the `anz` Python variable, `anz-card`, `anz_overrides`, `anzHtml`) and the user-facing
"XYZ" client branding in the report are left as-is — the branding is legitimate per-engagement
content, and the variables collide with it while carrying no reuse benefit. A `check_no_legacy_token`
check (wired into `validate_all`) prevents the legacy headers from silently returning. The frozen
engine golden (`tests/fixtures/data-baseline.json`) was regenerated; the only change is the
`anz_state`→`current_state` key inside `REGDATA.controls` (values, framework order, and `RECDATA`
verified identical).

## Alternatives considered (rejected)
- **Rename the cosmetic `XYZ`/`anz` variables too:** ~25 precise edits amid the XYZ branding with
  real breakage risk and no reuse gain.
- **Rename historical docs / ADR-005 / prompts / `research/` files:** rewrites the record of the
  real ANZ engagement; ADRs are conventionally immutable.
- **A back-compat alias column:** YAGNI — the rename is atomic and fully covered by the 104-test
  suite + the validator.

## Consequences
- The engine no longer names a client in its data schema — the multi-client unblock.
- `dist/` retains the old `anz-current-state.csv` as a frozen artifact (out of scope).
- The report's "XYZ" branding remains until engine generalization (WS-0).
- The 949-line `build_matrix_viewer.py` monolith split (5d) is the remaining WS-5 slice.

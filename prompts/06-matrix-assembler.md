# Prompt 06 — Matrix Assembler

**Role:** main thread (deterministic join — no sub-agent).
**Model:** Opus 4.7.
**Concurrency:** —
**Version:** v0.1 (2026-05-20).

---

## Objective

Join the per-source CSVs into the project's **single master matrix**, and
render two consumer-friendly views: a markdown table (for inline use in
the PRD) and a filterable HTML viewer (for socialisation).

## Inputs (must all exist before this prompt runs)

- `matrix/identity-catalog.csv`
- `matrix/use-cases.csv`
- `matrix/vendor-capabilities.csv` (after M2 vendor sub-agents)
- `matrix/regulatory-trace.csv` (after M2 regulatory mappers + adversary mapper)
- `matrix/anz-current-state.csv` (after prompt 07 runs)

## Outputs (write directly)

- `matrix/matrix.csv` — long-form join, one row per
  `(UC, NHI, Vendor, Coverage, Maturity, AnzState, EvidenceURL)`. This
  is the single source of truth.
- `matrix/matrix.md` — a readable, pivoted, paginated markdown view —
  one table per UC cluster (functional / non-functional), columns are
  vendors + XYZ column, rows are NHIs.
- `matrix/matrix-viewer.html` — self-contained HTML page with vanilla
  JS filter / sort / search. No external dependencies. Reads embedded
  JSON (the matrix.csv parsed into a JS array at the top of the HTML).
- `meta/agents.md` log row.

## Join algorithm (deterministic)

1. Read `identity-catalog.csv` → map `NHI-ID → {bucket, short_name, …}`.
2. Read `use-cases.csv` → map `UC-ID → {category, story, outcome_lens, backmap_codes, nhis_in_scope, …}`.
3. Read `vendor-capabilities.csv` → group rows by `(vendor_slug,
   target_id)`. Each row gives `(coverage, maturity, evidence_url,
   citation_keys)`.
4. Read `anz-current-state.csv` → `(uc_id, nhi_id) → {anz_state,
   evidence, gap_notes}`.
5. Read `regulatory-trace.csv` → `(control_code) →
   {framework, uc_ids, nhi_ids}`. Inversely, build `uc_id →
   list of (framework, control_code)`.
6. **Long-form output:** for every `(UC, NHI)` pair declared compatible
   (UC's `nhis_in_scope` includes NHI), emit one row per vendor:
   ```
   uc_id, uc_category, uc_outcome_lens, nhi_id, nhi_bucket,
   vendor_slug, coverage, maturity, evidence_url,
   anz_state, anz_evidence, anz_gap_notes,
   frameworks_implicated, citation_keys
   ```

## matrix.md rendering

Two top-level tables:

### Functional UCs
Rows = NHIs (grouped: COMMON first, then UNCOMMON).
Columns = `UC summary` + one column per vendor (12) + `XYZ`.
Cells = compact glyph encoding:
- `●3` = NATIVE, maturity 3.
- `◐2` = ADD-ON, maturity 2.
- `○1` = PARTNER, maturity 1.
- `✕` = GAP.
- `—` = N/A.
- XYZ column uses: `✓` Met / `~` Partial / `✕` Gap / `?` Pending.

Footnote glyphs at the bottom of each table.

### Non-functional UCs
Same shape.

## matrix-viewer.html rendering

Single static HTML page. Embed the CSV as a JS array. Provide:
- Search box (matches any column).
- Filter dropdowns: vendor, NHI bucket, UC category, coverage tier, XYZ
  state.
- Sortable column headers.
- Counts in the page header (`Showing X of Y rows`).
- Vanilla JS only (no jQuery, no React). Inline CSS.
- File must be openable directly in Safari / Chrome without a server.

## Sensitivity policy (Invariant #7)

XYZ-state column carries the deployer's evidence. Any cell whose
underlying evidence is `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` must
display only `?` (pending) in `matrix.md` and `matrix-viewer.html`. The
`matrix.csv` `anz_evidence` column may still contain the raw evidence
but the `matrix.md` / HTML do not render it.

## Token budget

No word budget (deterministic join), but matrix.md should be readable
without scrolling 100 pages — split tables across functional /
non-functional / by NHI bucket as needed.

## 70% checkpoint-and-handoff (Invariant #8)

Main-thread analogue. Checkpoint at
`meta/_main-checkpoint-matrix-<NNN>.md` if needed (low risk here, the
work is deterministic and bounded).

## Log line for `meta/agents.md`

`Matrix Assembler (main, Opus 4.7) — joined N inputs → matrix.csv (X rows) + matrix.md + matrix-viewer.html. Status: OK.`

## Acceptance criteria

- Every `(UC, NHI)` pair declared compatible has at least one vendor row.
- XYZ-state column populated for every `(UC, NHI)` pair (with `?` for
  PENDING TASK 0 INPUT where applicable).
- `matrix-viewer.html` opens in a browser with no errors and filters
  work.
- `matrix.md` is readable (no row > 12 columns of glyphs per table).

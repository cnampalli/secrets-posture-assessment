# Prompt 08 — PRD Writer

**Role:** main thread (synthesises all upstream artifacts).
**Model:** Opus 4.7.
**Concurrency:** —
**Version:** v0.1 (2026-05-20).

---

## Objective

Assemble the final `PRD/PRD-FI-v0.1.md` from upstream artifacts, write
the six ADRs, and write the four appendices.

## Inputs (must all exist before running)

- `research/identity-taxonomy.md`
- `research/use-cases.md`
- `research/vendors/*.md` (12)
- `research/regulatory/*.md` (5)
- `research/adversary/*.md` (2)
- `research/anz-current-state-evidence.md`
- `matrix/matrix.csv`, `matrix/matrix.md`, `matrix/matrix-viewer.html`
- `task0/responses.md` (with sensitivity tags respected — see prompt 07
  redaction rules)
- All ADR drafting notes in `notes/decisions.md`.

## Outputs (write directly)

- `PRD/PRD-FI-v0.1.md` — main deliverable (21 sections).
- `PRD/adrs/ADR-001-format-choice.md`
- `PRD/adrs/ADR-002-identity-taxonomy-source.md`
- `PRD/adrs/ADR-003-regulatory-lens.md`
- `PRD/adrs/ADR-004-vendor-shortlist.md`
- `PRD/adrs/ADR-005-anz-evidence-policy.md`
- `PRD/adrs/ADR-006-scoring-rubric.md`
- `PRD/appendices/A-compliance-traceability.md`
- `PRD/appendices/B-vendor-profiles-index.md`
- `PRD/appendices/C-glossary-and-NHI-definitions.md`
- `PRD/appendices/D-adversary-context.md`

## PRD section ordering and word budgets

| § | Title | Budget | Source |
|---|---|---|---|
| 0 | Document control | ≤ 80 w | inline |
| 1 | Executive summary | ≤ 400 w | synthesised |
| 2 | Stakeholders and audience | ≤ 250 w | `task0/responses.md` §A |
| 3 | Problem statement | ≤ 400 w | synthesised |
| 4 | Goals and non-goals | ≤ 250 w | `meta/workflow.md` |
| 5 | Scope and assumptions | ≤ 300 w | inline |
| 6 | Machine-identity taxonomy | ≤ 500 w | links + `research/identity-taxonomy.md` |
| 7 | Use cases | ≤ 500 w | links + `research/use-cases.md` |
| 8 | Evaluation rubric | ≤ 350 w | ADR-006 |
| 9 | Vendor capability matrix | ≤ 250 w + matrix.md | inline + link |
| 10 | XYZ current-state gap matrix | ≤ 250 w + linked view | inline + link |
| 11 | Findings — vendor side | ≤ 700 w | synthesised |
| 12 | Findings — XYZ side | ≤ 800 w | synthesised (respect ADR-005) |
| 13 | Adversary context | ≤ 500 w | links + `research/adversary/*` |
| 14 | Regulatory traceability summary | ≤ 350 w + appendix A link | synthesised |
| 15 | Risks and dependencies | ≤ 350 w | synthesised |
| 16 | Recommendations | ≤ 600 w | synthesised |
| 17 | Open questions | ≤ 350 w | gathered |
| 18 | Glossary | ≤ 100 w + appendix C link | link |
| 19 | Appendices | ≤ 60 w | links |
| 20 | ADR log | ≤ 100 w | links |

Total budget: **~7,500 words** for the PRD body, plus ADRs (≈ 600 w
each × 6 = 3,600 w), plus appendices (≈ 1,500 w each × 4 = 6,000 w).

## Style guide

- **Plain English**, Australian / international neutral spelling.
- Section headings as numbered above.
- Inline citations: link text to source by relative path
  (`[evidence](../research/vendors/hashicorp-vault-enterprise.md)`).
- Inline ADR references: `[ADR-006](./adrs/ADR-006-scoring-rubric.md)`.
- Every claim is either **cited** or marked
  `[SPECULATION]` / `[USER-SUPPLIED]` / `[INDUSTRY-CONSENSUS]`.
- No emoji, no decorative formatting.
- Tables must fit within 110 columns.

## ADR format (Michael Nygard original)

```
# ADR-<NNN> — <Title>

**Status:** Accepted | Proposed | Superseded by ADR-<NNN>
**Date:** YYYY-MM-DD
**Authors:** (Architect — name omitted unless `[PUBLIC]` per ADR-005)

## Context
≤ 200 w.

## Decision
≤ 150 w.

## Consequences
Positive, negative, neutral. ≤ 200 w.

## Alternatives considered
≤ 150 w.

## References
Inline links to PRD sections, research artifacts, memory entries.
```

## Appendices

- **A — Compliance traceability:** full table from
  `matrix/regulatory-trace.csv` joined into UC × Framework
  cross-references.
- **B — Vendor profiles index:** one paragraph per vendor with link to
  full profile under `research/vendors/`.
- **C — Glossary and NHI definitions:** every NHI ID expanded; every
  acronym used in PRD defined.
- **D — Adversary context:** consolidated narrative from
  `research/adversary/*` — MITRE family + breach catalog, organised by
  NHI bucket.

## Sensitivity policy (Invariant #7 + ADR-005)

Enforce redaction rules from prompt 07 throughout. Do not reproduce
`[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` content.

## 70% checkpoint-and-handoff (Invariant #8)

This is the longest single piece of writing in the project. Checkpoint
after each completed PRD section (every ~500–800 words). Use:
`meta/_main-checkpoint-prd-<NNN>.md`.

## Log line for `meta/agents.md`

`PRD Writer (main, Opus 4.7) — wrote PRD-FI-v0.1.md (X words) + 6 ADRs + 4 appendices. Citations: Y. Sensitivity audit clean. Status: OK.`

## Acceptance criteria

- Every section is populated; no `[TBD]` / `[TODO]` (deferred items go
  to PRD §17 explicitly).
- Every ADR linked from ≥ 1 PRD section.
- All inline links resolve.
- Word budget ±10 % per section.
- Reviewer (prompt 09) sign-off recorded in `meta/agents.md` before
  declaring M3 complete.

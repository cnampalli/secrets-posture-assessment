# ADR-001 — PRD format choice

**Status:** Accepted
**Date:** 2026-05-20 (re-confirmed 2026-05-23 at M3 PRD assembly)
**Authors:** Project architect (per ADR-005 attribution policy).

## Context

The stakeholder asked for a **universal buyer's framework for FI secrets
management with criteria around products**, applied to XYZ's current
state ([`task0/responses.md`](../../task0/responses.md) §Q-A.04). Three
formats were live in the kickoff conversation:

1. **Industry whitepaper** — narrative-first, light on traceability.
   Easy to read; hard to defend a specific recommendation to APRA or
   ASD-aligned audit.
2. **Comparative product report** (à la Forrester / Gartner) — vendor-
   first, score-first. Strong for procurement; weak at expressing
   XYZ-specific state vs. a universal framework.
3. **Enterprise PRD with ADRs + a dual matrix + a compliance trace
   appendix** — combines a numbered narrative spine (§1–§20) with a
   filterable evidence layer (`matrix/`) and decision-grade Architecture
   Decision Records.

The FI lens demands an **outcomes-first** read (E8 + ZT primary, CPS 234
+ ISM back-map — see [ADR-003](./ADR-003-regulatory-lens.md)) and the
ability to attest each claim to either a primary URL or an approved tag.
Format (1) cannot carry that load; format (2) inverts the unit of
analysis (vendor-as-row, when the right unit is `(UC, NHI, control)`).

## Decision

Adopt the **Enterprise PRD with ADRs + DUAL MATRIX + compliance-trace
appendix** format:

- Numbered PRD body §1–§20 carries the narrative.
- A **dual matrix** scored to the same rubric across two axes:
  (a) `(UC × NHI × Vendor)` — the universal framework
  ([matrix/matrix.md](../../matrix/matrix.md)); (b) `(UC × NHI × XYZ-state)`
  — the current-state read
  ([matrix/domains/secrets/current-state.csv](../../matrix/domains/secrets/current-state.csv)).
- **ADRs** (this file + ADR-002..006) record the load-bearing choices
  (taxonomy source, regulatory lens, vendor shortlist, sensitivity policy,
  scoring rubric) so reviewers can challenge the spine without re-reading
  the body.
- **Appendix A** is the **compliance traceability** view of the matrix
  (UC × framework) so APRA / ASD scoping is one page deep.

## Consequences

**Positive:**

- Recommendations in §16 are pinned to UC IDs + NHI IDs + framework
  back-maps — every claim is falsifiable against the matrix.
- Reviewers can challenge a single ADR without re-reading the body.
- The matrix is reusable: refreshing a vendor row at v1.0 does not force
  a PRD rewrite; the same shape supports an industry-agnostic v2.

**Negative:**

- Heavier authoring cost than a whitepaper. Mitigated by per-vendor +
  per-framework sub-agents producing the matrix in parallel
  ([`meta/workflow.md`](../../meta/workflow.md) §Wave-by-wave dispatch).
- Two surfaces to keep consistent (PRD body and matrix); reviewer
  prompt 09 enforces drift checks at every milestone gate.

**Neutral:**

- The format trades narrative density for evidence density; readers used
  to vendor-first reports may need the §1 executive summary to orient.

## Alternatives considered

- **Whitepaper-only** — rejected (cannot carry CPS 234 §22 / §28 trace).
- **Forrester-style vendor scorecard** — rejected (vendor-as-row hides
  the UC × NHI gaps that drive the FI risk story).
- **RFI/RFP-shaped PRD** — explicitly out of scope per §4 Non-goal N2;
  the PRD must precede an RFI, not displace it.

## References

- PRD §0 Document control, §8 Evaluation rubric, §9 Vendor matrix,
  §10 XYZ matrix, §14 Regulatory traceability, §19 Appendices.
- [`meta/workflow.md`](../../meta/workflow.md) §Format choice.
- [`notes/decisions.md`](../../notes/decisions.md) 2026-05-20 entry.
- Companion ADRs: [ADR-003](./ADR-003-regulatory-lens.md),
  [ADR-006](./ADR-006-scoring-rubric.md).

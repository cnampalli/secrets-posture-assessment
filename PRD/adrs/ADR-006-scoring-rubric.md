# ADR-006 — Scoring rubric

**Status:** Accepted
**Date:** 2026-05-20 (re-confirmed 2026-05-23 — applied uniformly
across 19 vendors × 84 rows = 1,596 capability cells per
[`matrix/matrix.md`](../../matrix/matrix.md))
**Authors:** Project architect.

## Context

The PRD scores **two surfaces** against the same UC × NHI catalog:
(a) every vendor in scope ([ADR-004](./ADR-004-vendor-shortlist.md));
(b) XYZ current-state. A scoring rubric must (1) distinguish "vendor
ships this natively" from "vendor needs a partner integration" from
"this is a gap"; (2) capture **maturity** independently of coverage so
a checkbox-but-immature capability is not over-credited; (3) give the
XYZ-state axis a parallel but distinct vocabulary that reads natively to
audit; (4) be cheap enough to apply at 1,596-row scale.

Two-axis (coverage × maturity) rubrics are an analyst-industry
[INDUSTRY-CONSENSUS] pattern (Gartner Magic Quadrant, Forrester Wave
both use parallel axes). The novelty here is that we apply the *same*
rubric across vendor and XYZ axes so the two matrices are directly
joinable.

## Decision

Adopt the **two-axis rubric** below, applied per `(UC, NHI, Vendor)`
cell on the vendor matrix and per `(UC, NHI)` cell on the XYZ matrix
([`matrix/anz-current-state.csv`](../../matrix/anz-current-state.csv)
applied at the UC level for v0.1 — per-pair deferred to v1.0).

### Vendor axis — coverage tier (per `(UC, NHI, Vendor)`)

| Tier | Meaning |
|---|---|
| `NATIVE` | Vendor's first-class, documented capability. |
| `ADD-ON` | Vendor supports via paid add-on / SKU / module. |
| `PARTNER` | Vendor relies on a named partner / integration. |
| `GAP` | Vendor does not address this UC × NHI. |
| `N/A` | UC does not apply to this NHI (e.g., mainframe-only UC scored against a cloud-native vendor). |

### Vendor axis — maturity (0–4)

| Level | Meaning |
|---|---|
| 0 | None / not announced. |
| 1 | Announced / preview / unsupported. |
| 2 | GA basic. |
| 3 | GA mature with reference customers. |
| 4 | Industry-leading. |

### XYZ-state axis (per `(UC, NHI)`)

| State | Meaning |
|---|---|
| `MET` | Capability deployed; objective evidenced. |
| `PARTIAL` | Capability exists but adoption / observability lags. |
| `GAP` | Material gap with evidence. |
| `N/A` | Capability not in XYZ scope. |
| `PENDING` | Insufficient Task 0 signal to score; surfaces as PRD §17 open question. |

Each XYZ-state cell additionally carries: **confidence** (HIGH /
MEDIUM / LOW), **evidence quote** (≤ 30 words, ADR-005-paraphrased
where `[INTERNAL]`), **gap notes**.

## Consequences

**Positive:**

- Cross-axis joinability — PRD §16 recommendations name the UC × NHI
  cells where XYZ is `GAP` *and* the matrix shows a NATIVE+Maturity ≥ 3
  vendor option (after AU-residency filtering).
- Maturity decouples capability claims from operational reality —
  Vault's database secrets engine scores NATIVE 4 at the vendor level
  but PARTIAL at XYZ (shelf-ware — [`research/anz-current-state-evidence.md`](../../research/anz-current-state-evidence.md) §1.5).
- Cheap to apply: each cell is one (tier, maturity, evidence-quote)
  tuple — 1,596 cells in M2 budget.

**Negative:**

- The bias toward PARTIAL / PENDING in the XYZ matrix (47 rows: 0 MET /
  16 PARTIAL / 11 GAP / 20 PENDING) is a direct consequence of the
  rubric's honesty about evidence sufficiency and the 1-hour Task 0
  pass.
- Comparing maturity across vendor tiers requires reading the three-layer
  stack model — naive max-NATIVE-count comparison is misleading (a
  discovery tool's NATIVE ≠ a vault's NATIVE; Fortanix DSM's 5 NATIVE rows
  are the right ones). This is now formalized in
  [ADR-007](./ADR-007-reading-model-and-confidence.md) and surfaced in
  [`matrix/matrix.md`](../../matrix/matrix.md) §0 + PRD §9.

**Neutral:**

- Confidence labels (HIGH / MEDIUM / LOW) are a coarse proxy for
  evidence depth; v1.0 may move to a Bayesian-style explicit-evidence
  count.

## Alternatives considered

- **Single-axis NATIVE/GAP only** — rejected (over-credits shelf-ware).
- **Numerical 0–10 capability score** — rejected (false precision; the
  underlying evidence base does not support 11-bucket discrimination at
  v0.1).
- **Per-pair XYZ scoring at v0.1** — deferred; the 1-hour Task 0 pass
  did not yield per-NHI-per-UC depth for XYZ. Surfaced in PRD §17 O5.

## References

- [`matrix/matrix.md`](../../matrix/matrix.md) §1, §2, §3.
- [`matrix/vendor-capabilities.csv`](../../matrix/vendor-capabilities.csv)
  (1,596 rows; 19 vendors × 84 cells).
- [`matrix/anz-current-state.csv`](../../matrix/anz-current-state.csv)
  (47 rows).
- Companion ADRs: [ADR-001](./ADR-001-format-choice.md),
  [ADR-002](./ADR-002-identity-taxonomy-source.md),
  [ADR-004](./ADR-004-vendor-shortlist.md).

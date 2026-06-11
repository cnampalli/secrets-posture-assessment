# ADR-007 — Three-layer reading model & sourcing-confidence policy

**Status:** Accepted
**Date:** 2026-05-24 (stakeholder-readiness reframing on the frozen v0.1
matrix; supersedes the scattered caveats in ADR-006 §Consequences, PRD
§11 F-V-4/F-V-5, and the former `matrix/matrix.md` §1 footnote)
**Authors:** Project architect.

## Context

The v0.1 matrix scores **all 19 vendors against the same 84-row
(37 NHI + 47 UC) rubric** (ADR-006). Two problems surfaced in
stakeholder-readiness review:

1. **Category coupling.** The 19 vendors are not one competitive set.
   They occupy three different layers of the machine-identity stack, and
   a `NATIVE` score means a *different thing* in each. Scored on one grid,
   complementary tools look like competitors: an NHI-discovery tool's
   `NATIVE` (it *discovers* the identity) looked identical to a vault's
   `NATIVE` (it *brokers secrets* for it), and Fortanix (a crypto
   substrate *below* the vault) ranked dead-last by NATIVE count, making
   a different-layer product look weak. ADR-006 already flagged that
   "naive max-NATIVE-count comparison is misleading", but the caveats
   lived in prose/footnotes while the headline §9 ranking and the
   CSV/viewer still flattened everything.

2. **Sourcing transparency.** The vendor research was produced by AI
   sub-agents reading vendor documentation. A procurement reader needs to
   know what is independently verified versus vendor-claimed. Capability
   *existence* is mostly vendor-doc-cited (primary but self-reported);
   maturity scores are analyst judgment; some GA dates are unverified
   roadmap. None of this was stated up front.

The constraint: v0.1 is frozen and going to stakeholder review — fixes
must be a **reading layer over the existing data**, not a re-score of
1,596 cells or a research redo (both deferred to v1.0).

## Decision

### A. Three-layer stack model (rank within layer; compose across layers)

Regroup the vendors by **stack layer**. **18 vendors are ranked** across
two comparison layers; the third (L0) is a **dependency, not ranked**
(see §A.1). Rank only *within* a layer; present cross-layer relationships
as stack *composition*, never as a head-to-head ranking.

| Layer | Position | Vendors | `NATIVE` means |
|---|---|---|---|
| **L2 — NHI discovery / governance** | above the vault | Astrix, Entro, Oasis, Aembit, Clutch (5) | *discovers / inventories / governs* this identity |
| **L1 — Secrets management** (this PRD) | the vault tier | Vault Ent, Conjur, CyberArk PAM, Delinea, AWS, Azure, GCP, AKEYLESS, Doppler, Infisical, 1Password + PKI/MIM lane (Venafi, Keyfactor) (13) | *brokers / stores / rotates secrets* for this identity |
| **L0 — Crypto substrate** *(dependency, NOT ranked)* | below the vault | Fortanix DSM (XYZ substrate) | *provides the HSM / key-root* — paired with, not shortlisted against, the vault |

The **PKI/MIM lane** (Venafi, Keyfactor) sits inside L1 but is a distinct
certificate/key-lifecycle discipline — judged on PKI/MIM rows, not vault
rows. A high GAP count there against the secrets-broker rubric is
expected, not a weakness.

### A.1. Layer 0 is a dependency, not a ranked vendor (revised 2026-05-24)

On stakeholder challenge, Fortanix DSM was **removed from the ranked
vendor set** (19 → **18 ranked**). Rationale: scoring an HSM / key-management
substrate on a 37-NHI / 47-UC *secrets-management* rubric is a category
error (it GAPs ~21/37 NHIs by design — it never brokers application
secrets), and a crypto substrate is **paired with** a vault, not
**shortlisted against** one. It is therefore excluded from the rankings,
the per-UC/per-NHI decision cards, the XYZ posture dashboard, and the
interactive viewer's ranked views. It is **not deleted**: the secrets
layer's trust-root is a real dependency, and XYZ has a live
Thales SafeNet → Fortanix migration (Task 0 §D), so L0 is surfaced as a
**dependency callout** (PRD §9.x, `matrix/matrix.md` §1.x, Appendix B §B.6)
and its profile + 84 CSV cells are retained as substrate reference.
Alternatives "keep as ranked vendor #19" and "delete entirely" were both
rejected — the first misleads, the second hides a load-bearing dependency.

### B. `NATIVE` is layer-relative; the CSV is NOT re-scored for v0.1

The 1,596-row CSV keeps a single `NATIVE`/`ADD-ON`/`PARTNER`/`GAP`/`N/A`
vocabulary (ADR-006 unchanged). Rather than re-tag every cell, v0.1 ships
a **reading key**: the layer model above is surfaced in PRD §9,
`matrix/matrix.md` §0, every Appendix B tier header, and the HTML viewer
(layer toggles + a "how to read this" panel). A reader must interpret a
`NATIVE` through its vendor's layer. **Sub-typing the score itself**
(`NATIVE-BROKER` / `NATIVE-DISCOVER` / `NATIVE-KEYROOT`) is deferred to
v1.0 (PRD §17).

### C. Sourcing-confidence taxonomy & forward-dated register

State the honest posture in PRD §8.1. Capability *existence* is mostly
vendor-doc-cited (~60-70 % primary URLs); **maturity scores (0-4) are
analyst judgment against the ADR-006 rubric, not independently
evidence-gated**; rankings are writer synthesis of the CSV; forward-dated
GA claims are unverified vendor roadmap. Every claim reads against:

| Tag | Meaning | Trust |
|---|---|---|
| `VERIFIED-PRIMARY` | Vendor doc / spec / changelog cited | Med-High (vendor-authored) |
| `ANALYST` | Third-party (Gartner / Forrester / etc.) | Medium |
| `INDUSTRY-CONSENSUS` | Widely held, not single-source-verified | Low-Med |
| `FORWARD-DATED` | Future / unverified GA date | Low — confirm with vendor SE |

A **forward-dated claims register** (PRD §8.1) lists every future/unverified
GA claim (Aembit MCP "Apr 2026", Oasis AAM "Nov 2025", Fortanix FX3400
FIPS 140-3 "pending", Doppler MCP "experimental"). None is asserted as
present fact in the scoring.

## Consequences

**Positive:**

- A skimming stakeholder is no longer misled: Fortanix is read as a
  substrate, the discovery tools as a control-plane, and the like-for-like
  vault comparison stands on its own.
- The procurement reader knows exactly how much to trust each number, and
  the forward-dated claims are carried into any RFI rather than hidden.
- Achieved with zero changes to the frozen CSV — the viewer is regenerated
  from unchanged data with layer/tier derived at build time.

**Negative:**

- `NATIVE` remains overloaded in the raw CSV; correct reading still
  depends on the layer key (mitigated by surfacing it everywhere a reader
  meets the data, including viewer tooltips).
- Per-layer confidence is coarse (no per-cell confidence column at v0.1).

**Neutral:**

- v1.0 may sub-type `NATIVE` and add a per-cell confidence column,
  superseding the reading-key approach with structural separation.

## Alternatives considered

- **Re-score the CSV into three sub-typed NATIVE values now** — rejected
  for v0.1: touches 1,596 frozen cells under a Monday deadline and risks
  new drift; deferred to v1.0.
- **Split into three separate matrices** — rejected for v0.1: fragments
  the single filterable artifact the stakeholder is getting; the layer
  toggles in the viewer achieve the same isolation without a split.
- **Independent web re-verification of all claims** — deferred (PRD §17);
  v0.1 ships a transparency/labeling pass, not new research.

## References

- [`PRD-FI-v0.1.md`](../PRD-FI-v0.1.md) §8.1 (sourcing & confidence), §9
  (three-layer matrix).
- [`matrix/matrix.md`](../../matrix/matrix.md) §0 (stack model), §1
  (layer-grouped coverage).
- [`matrix/build_matrix_viewer.py`](../../matrix/build_matrix_viewer.py)
  (`VENDOR_LAYER`, glossary, layer toggles).
- Companion ADRs: [ADR-004](./ADR-004-vendor-shortlist.md) (tier
  structure), [ADR-006](./ADR-006-scoring-rubric.md) (scoring rubric),
  [ADR-005](./ADR-005-fi-evidence-policy.md) (sensitivity).

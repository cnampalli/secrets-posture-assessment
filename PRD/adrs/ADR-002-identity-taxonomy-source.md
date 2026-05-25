# ADR-002 — Identity taxonomy source

**Status:** Accepted
**Date:** 2026-05-20 (re-confirmed 2026-05-23 at M3 PRD assembly)
**Authors:** Project architect (per ADR-005 attribution policy).

## Context

The PRD scores vendors and XYZ current-state against a **Non-Human
Identity (NHI) taxonomy**. The taxonomy needs to (a) cover the FI long
tail (mainframe, RPA, branch peripherals, code-signing, AI agents) that
a single-vendor taxonomy would underweight; (b) align with terms the
stakeholder will already encounter in audit, regulator briefings and
vendor RFIs; (c) carry primary citations so reviewers can challenge
inclusions.

Candidate source taxonomies surveyed:

- **CSA NHI Working Group taxonomy (2024)** — the most up-to-date NHI
  canon; broad enough to cover OAuth-app sprawl and AI-agent NHIs;
  vendor-neutral.
- **Gartner Machine Identity Management (MIM) market guide (2023)** —
  procurement-ready framing; bridges to PAM / MIM / KMS analyst lanes.
- **SPIFFE / SPIRE workload-identity spec (2023)** — anchors workload-
  attested NHI rows (NHI-036) and informs the ephemeral-vs-static
  ephemerality axis.
- **NIST SP 800-63-4 / 800-204D** — lifecycle and microservice-security
  framing for short-lived credentials.
- **OWASP Secrets Management Cheat Sheet (2024)** — operational lens;
  cross-checks acceptance criteria.

None of these alone fully covers the FI estate XYZ runs (cloud-native
+ Vault + PAM + mainframe + RPA + Open Banking + emerging AI agents
per [`research/anz-current-state-evidence.md`](../../research/anz-current-state-evidence.md) §1.3).

## Decision

Adopt **CSA NHI WG as the primary spine + Gartner MIM bridge terms +
SPIFFE deltas for workload-attested identity**, codified as **37 NHIs
(14 COMMON + 23 UNCOMMON)** in
[`research/identity-taxonomy.md`](../../research/identity-taxonomy.md).

The "long tail" rows (NHI-018 TEE attestation, NHI-019 AI agent,
NHI-022 mainframe, NHI-024 HSM operator, NHI-026 backup agent,
NHI-028 Open Banking, NHI-034 PQC, NHI-035 vault-internal) are
explicitly retained as first-class rows so PRD §16 recommendations can
target them by ID rather than disappearing into "miscellaneous".

## Consequences

**Positive:**

- Taxonomy is defensible to APRA / ASD review (CSA + NIST + SPIFFE are
  cited; no vendor capture).
- Long-tail rows (mainframe, RPA, AI agent, Open Banking) get scored
  rather than glossed — directly addresses the
  [`research/anz-current-state-evidence.md`](../../research/anz-current-state-evidence.md) §1.10
  finding that ZT workload identity is poorly understood operationally.
- One taxonomy spans all 19 vendor matrices and all 47 UCs — no rebase
  needed at v1.0.

**Negative:**

- 37 NHIs is wide; the matrix viewer relies on filtering / faceting to
  remain readable. Mitigated by [matrix-viewer.html](../../matrix/matrix-viewer.html).
- Some NHI rows (NHI-029 service-account-as-human, NHI-037 orphan)
  sit on the NHI/IGA boundary and may be re-classified at v1.0; flagged
  in PRD §17.

**Neutral:**

- Anchoring to CSA NHI WG ties annual refresh to that body's release
  cadence; PRD §17 carries this as a maintenance dependency.

## Alternatives considered

- **Gartner MIM-only** — rejected; misses AI-agent and SPIFFE-class
  identities.
- **SPIFFE-only** — rejected; the workload-attested lens is necessary
  but not sufficient for mainframe / RPA / Open Banking / observability.
- **Build a bespoke XYZ taxonomy from Task 0** — rejected; would not be
  reusable as a universal FI buyer's framework (§4 G1) and would not
  carry external citations.

## References

- [`research/identity-taxonomy.md`](../../research/identity-taxonomy.md).
- CSA NHI Working Group, Gartner MIM 2023, SPIFFE spec v1.0,
  NIST SP 800-63-4, NIST SP 800-204D, OWASP SM Cheat Sheet — see
  [`meta/citations.bib`](../../meta/citations.bib).
- Companion ADRs: [ADR-006](./ADR-006-scoring-rubric.md) (scoring),
  [ADR-004](./ADR-004-vendor-shortlist.md) (vendor scope).

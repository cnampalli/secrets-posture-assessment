# ADR-003 — Regulatory lens (outcomes-first)

**Status:** Accepted
**Date:** 2026-05-20 (re-confirmed 2026-05-23 — NIST CSF 2.0 deferral
explicitly accepted at M2 gate per
[`meta/review-M2-2026-05-23.md`](../../meta/review-M2-2026-05-23.md) §F.1)
**Authors:** Project architect (per ADR-005 attribution policy).

## Context

The FI buyer's framework must back-map to multiple regulatory and
guidance frameworks without becoming a compliance-checkbox exercise.
Task 0 surfaced (§Q-B.03) that **XYZ engagements most often cite ACSC
Essential 8 + ASD ISM + APRA CPS 234 / 230 / CPG 234**, with
**PCI-DSS + SOX + OAIC Privacy Act** as downstream regulatory frames.
**NIST CSF and the 800-series were not specifically cited in
conversations** — supports an outcomes-first read rather than a
control-checkbox read.

The risk of leading with control IDs (CPS 234 §28, ISM-1619, CSF
PR.AC-1) is that the PRD ends up rephrasing controls back to the
auditor without saying anything new about NHI-class risk. The
opportunity, instead, is to use **outcome lenses** (E8 maturity levels,
CISA ZTMM pillars) as the primary spine and back-map control IDs into the
matrix appendix so the auditor view is one filter away.

## Decision

Adopt an **outcomes-first regulatory lens** comprising:

| Tier | Frameworks | Role |
|---|---|---|
| **PRIMARY-LENS** | ASD Essential 8 (ML1/2/3) + CISA Zero Trust Maturity Model v2.0 — 5 pillars + 3 cross-cutting capabilities (Identity, Devices, Networks, Workloads, Data + Visibility/Analytics, Automation/Orchestration, Governance), aligned to NIST SP 800-207, with Federation, Workload-mTLS, CICD, Runtime, NHIDR, PQC sub-pillars | Spine of PRD §14 + dual matrix scoring axis |
| **BACK-MAP** | APRA CPS 234 + CPS 230 + CPG 234; ASD ISM (11 domains, 41 controls) | Filterable view in Appendix A; quoted in PRD §14 only where load-bearing |
| **DEFERRED** | NIST CSF 2.0 | Out of v0.1 scope per Task 0 §Q-B.03 stakeholder direction; revisit at v1.0 |
| **ADVERSARY-LENS** | MITRE ATT&CK T1552-family + 15 breach post-mortems | PRD §13 + Appendix D |

All 47 UCs back-map to ≥ 1 PRIMARY-LENS code; all 47 UCs back-map to
≥ 1 BACK-MAP code. PCI-DSS / SOX / OAIC are noted as downstream
frames but not separately mapped at v0.1 (PRD §17).

## Consequences

**Positive:**

- §14 reads as "investing in UC-F-X moves E8 ML2→ML3 and reduces ZT-
  Identity-pillar gap"; control IDs are evidentiary, not narrative.
- The 4-framework scope (E8 + ZT + CPS 234 + ISM) is achievable inside
  v0.1's budget; CSF 2.0 deferral is logged and revisitable.
- Adversary lens prevents the framework from being purely declarative —
  every UC mitigates a named TTP and a named breach.

**Negative:**

- Readers expecting a CSF 2.0 column will be redirected to v1.0;
  surfaced in PRD §17 O-Q.
- ISM control IDs change at each ISM release (typically annually);
  matrix refresh cadence required.

**Neutral:**

- CPS 234 paragraph numbering was normalised mid-project (§21(a)-(d) /
  §27(a)-(e) / §35(a)-(b)) from the dispatch prompt's earlier shorthand
  — surfaced in PRD §14 and `regulatory/apra-cps-234-mapping.md` §6.

## Alternatives considered

- **CSF 2.0 as the primary spine** — rejected per Task 0 §Q-B.03
  stakeholder direction; CSF 2.0 deferred to v1.0.
- **CPS 234 as the primary spine** — rejected; control-checkbox framing
  hides the FI-specific NHI gaps and is harder to apply to vendors not
  inside XYZ's perimeter.
- **PCI-DSS-first** — out of scope (the framework targets the
  enterprise NHI estate, not the PCI cryptographic boundary alone).

## References

- [`research/regulatory/essential-8-mapping.md`](../../research/regulatory/essential-8-mapping.md)
- [`research/regulatory/nist-sp-800-207-zt-mapping.md`](../../research/regulatory/nist-sp-800-207-zt-mapping.md)
- [`research/regulatory/apra-cps-234-mapping.md`](../../research/regulatory/apra-cps-234-mapping.md)
- [`research/regulatory/asd-ism-mapping.md`](../../research/regulatory/asd-ism-mapping.md)
- [`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv)
- Companion ADRs: [ADR-001](./ADR-001-format-choice.md) (format),
  [ADR-006](./ADR-006-scoring-rubric.md) (scoring rubric).

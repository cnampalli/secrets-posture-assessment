# ADR-004 — Vendor shortlist for the comparative matrix

**Status:** Accepted
**Date:** 2026-05-22 (revised from original 12-vendor list of 2026-05-20)
**Authors:** Project architect (per ADR-005 attribution policy).

## Context

The PRD must score a vendor set broad enough to be a credible
**universal buyer's framework** (`task0/responses.md` §Q-A.04) yet
narrow enough to remain readable. Task 0 surfaced material refinements
to the original 12-vendor list:

- **CyberArk PAM is entrenched at XYZ for AD service-account
  governance** (Q-I.03). The Vault migration was rolled back. Treating
  PAM as a footnote under "CyberArk Conjur" would conceal a load-bearing
  governance platform.
- **XYZ has no NHI inventory / discovery layer** above its vaults
  (§C.00 headline finding). PRD §16 needs a defensible recommendation,
  which requires explicit capability scoring of the emerging NHI
  discovery / governance vendor category.

## Decision

**19 vendor candidates across 5 tiers** (revised 2026-05-22 post-Wave-2):

| Tier | Vendors |
|---|---|
| **Core (4)** | HashiCorp Vault Enterprise; CyberArk Conjur; CyberArk PAM; Delinea Secret Server |
| **Cloud-native (4)** | AWS Secrets Manager; Azure Key Vault; GCP Secret Manager; AKEYLESS |
| **Emerging + PKI/MIM (5)** | Doppler; Infisical; 1Password Secrets Automation; Venafi (now CyberArk-owned); Keyfactor |
| **NHI discovery / governance (5)** | Astrix Security; Entro Security; Oasis Security; Aembit; Clutch Security |
| **Data security / HSM (1, new)** | **Fortanix DSM** — promoted from v1.0 to v0.1 given XYZ's SafeNet → Fortanix migration + GCP Cloud EKM partnership |

All 19 are scored against the same UC × NHI rubric (ADR-006). Each
vendor produces a per-vendor CSV
(`matrix/vendor-capabilities-<slug>.csv`) which the Matrix Assembler
(prompt 06) concatenates at M3 to avoid parallel-write races.

## Consequences

**Positive:**
- XYZ's lived multi-vendor reality (Vault + PAM + cloud-native) is
  represented directly in the matrix rather than inferred.
- The NHI-inventory recommendation in PRD §16 is grounded in capability
  scoring, not just narrative.
- The matrix becomes reusable as an industry buyer's framework — 19
  vendors covers the FI-relevant secrets / machine-identity market.

**Negative:**
- Research spend is materially higher. Each new vendor is ~1 Sonnet 4.6
  agent run (~75–100k tokens). 6 additional vendors ≈ 500k–600k extra
  tokens. Mitigated by per-vendor CSV strategy + Sonnet model choice.
- 19 columns is wide for the markdown matrix; viewer will rely on the
  HTML filter to remain readable.

**Neutral:**
- ADR-004 supersedes the original 12-vendor list in
  `meta/workflow.md`. The workflow doc has been re-anchored.

## Alternatives considered

1. **Keep 12 vendors; treat PAM and NHI-discovery in narrative only.**
   Rejected — narrative without scoring is unfalsifiable; the
   stakeholder asked specifically for "criteria around products."
2. **Add only PAM (13 total); defer NHI discovery to v1.0.**
   Rejected — the inventory gap is the dominant XYZ finding (§C.00);
   PRD §16 needs the scoring now, not later.
3. **Add a 14th "tokenisation / data security" tier (Fortanix DSM,
   Thales CipherTrust, Protegrity).** Deferred to v1.0 — the
   Vault-Transform PCI use case at XYZ is narrow enough that one
   vendor profile (Fortanix) would suffice; cost / benefit favours
   v1.0 inclusion.

## Positioning notes (carried into PRD §11 + §16)

- **CyberArk PAM** is scored honestly but framed in PRD §11 / §16 as
  **"legacy / incumbent lane"** — strongest on its core (AD SAs, DB
  privileged accounts, network devices, break-glass quorum, session
  brokering); intentionally weaker on cloud-native / ephemeral /
  SPIFFE / K8s CSI lanes which belong to Conjur or cloud-native vaults.
  Recommending PAM displacement at XYZ is **out of scope** (Task 0
  §Q-I.03 procurement constraint); recommendations focus on **closing
  the gaps PAM does not cover**.

## References

- `task0/responses.md` §Q-A.04 (decision drivers), §C.00 (headline gap),
  §Q-I.03 (procurement constraint).
- `meta/workflow.md` (workflow plan).
- `notes/decisions.md` (2026-05-22 scope-expansion entry).
- `prompts/03-vendor-researcher-template.md` (parameterised template).
- `prompts/06-matrix-assembler.md` (per-vendor CSV concatenation
  pattern — to be updated at M3 to read `matrix/vendor-capabilities-*.csv`).

# PRD — Secrets-Management Positioning Across Machine Identities
## Financial-Industry v0.1 (XYZ Bank current-state assessment)

> **Status:** v0.1 — Milestone 3 deliverable (assembled 2026-05-23).
> **Stakeholder review target:** Mon 2026-05-25.
> **Deep-dive iteration:** v1.0, week of 2026-05-26.

---

## §0 Document control

- **Version:** v0.1 (Wave A — body sections 1–20 + ADRs 001/002/003/005/006; ADR-004 retained from M2; Appendices A–D in Wave B).
- **Owner:** Enterprise Solutions Architect / Security Architect (user).
- **Reviewers (proposed):** XYZ stakeholder TBC; independent PRD reviewer agent (prompt 09).
- **Date created:** 2026-05-20. **This iteration:** 2026-05-23.
- **Classification:** **Internal — for XYZ stakeholder review** (per [ADR-005](./adrs/ADR-005-anz-evidence-policy.md)).
- **Sensitivity policy:** real where publicly known; anonymised where internal/sensitive. XYZ-specific lived-experience signal is paraphrased and attributed to "a major AU Tier-1 FI" throughout. See [ADR-005](./adrs/ADR-005-anz-evidence-policy.md).
- **Source plan:** [`meta/workflow.md`](../meta/workflow.md).
- **Plan checkpoint of record:** `/Users/cnampalli/.claude/plans/wondrous-meandering-yao.md`.

---

## §1 Executive summary

Most large financial institutions overestimate how well they govern
machine identities. Vendor selections from the prior wave of secrets-
management investment — typically a single vault platform circa 2019 —
have not kept pace with two structural shifts: (a) **NHI sprawl** as
cloud-native, Kubernetes, AI-agent and Open Banking workloads
multiply faster than identity inventory; (b) an **outcomes-first
regulatory pressure** that, in Australia, blends ACSC Essential 8
maturity, ASD ISM controls and APRA CPS 234 / 230 expectations into a
single audit narrative. No single product fully satisfies that
narrative.

This PRD assembles a **universal buyer's framework** — 47 use cases ×
37 NHIs × 19 vendors = 1,596 capability cells — and applies it to a
major AU Tier-1 FI's current state. The headline finding is the
**absence of an NHI inventory layer above the vault tier**: capability
exists (Vault Enterprise was selected in 2019 and remains the system of
record), but adoption, observability and ownership-attestation lag
materially. Of 47 UCs, 0 are MET, 16 are PARTIAL, 11 are explicit GAP,
and 20 are PENDING for v1.0 deep-dive. The 2019 red-team finding —
plaintext secrets in source repositories — remains the dominant open
exposure and anchors the user-supplied seed UCs (UC-F-001, UC-N-001).

Cross-vendor, **HashiCorp Vault Enterprise** holds the broadest
functional NHI coverage (17/27 NATIVE UC-F rows) but cannot, alone,
close the inventory gap. **CyberArk PAM** is the entrenched legacy
lane for AD service accounts and is not displaceable inside v0.1
scope. **Fortanix DSM** sits below the vault tier as the post-Thales
crypto root. The **NHI-discovery tier** (Astrix, Entro, Oasis,
Aembit, Clutch) leads on inventory and AI-agent identity but is
disqualified as a primary platform by AU-residency / IRAP gaps for
APRA-regulated workloads. The **emerging tier** (Doppler, 1Password,
Infisical SaaS) is residency-disqualified for production.

The recommendations posture is therefore **conditional and pinned to
UC IDs**. Priority moves: (1) **close the NHI inventory gap** via a
discovery-and-attestation layer above existing vaults; (2) **demystify
ZT workload identity** as a first-class FI 27 deliverable, including
AI-agent identity; (3) **consolidate via control-plane pattern, not
vault displacement** — the 6-year drift to cloud-native vaults is real
and the FI 27 strategy must address it as such. All recommendations are
sequenced explicitly in §16 and back-mapped to E8 + NIST ZT outcomes in
§14 and Appendix A.

---

## §2 Stakeholders and audience

**Primary readers** (per Task 0 §A): **Head of IAM + Head of Platform
Security** at the FI. Both lenses are required because the dominant
findings sit at the intersection: an IAM-only read undercounts the
platform-engineering reality (Vault sprawl, K8s CSI, SPIFFE), while a
platform-only read undercounts the governance reality (CyberArk PAM
entrenchment, AD `svc_` accounts, exception-register pressure). The
PRD is written so a single reader from either side can land all 17
recommendations.

**Secondary readers:** (a) the 3-lines-of-defence cohort — internal
audit + Operational Risk + the CISO's control-attestation function;
(b) procurement, where any net-new vendor selection is constrained by
the existing Vault Enterprise + CyberArk PAM + Fortanix DSM footprint;
(c) Architecture Council, where FI 27 alignment will be litigated;
(d) — once the distribution surface is confirmed (PRD §17 O2) — vendor
SEs and / or the external regulator (APRA or ASD-aligned audit).

**Tertiary readers:** board sub-committee for risk + the Operational
Risk Committee. They consume §1 + §16 + §17.

Tone is therefore deliberately neutral: numbered, citation-bearing,
explicit about uncertainty, and free of vendor advocacy. Where
narrative judgement is required — the legacy-lane framing of CyberArk
PAM, the "crypto root below vaults" framing of Fortanix DSM, the
NHI-discovery-tier AU-residency disqualification — the judgement is
labelled and back-cited.

Distribution surface defaults to **Internal — for XYZ stakeholder
review** until the stakeholder confirms otherwise (PRD §17 O2;
[ADR-005](./adrs/ADR-005-anz-evidence-policy.md)).

---

## §3 Problem statement

Three threads, woven together, describe the problem the FI faces.

**(a) NHI sprawl is structurally underestimated.** The Cloud Security
Alliance NHI Working Group, Gartner MIM, GitGuardian State-of-Secrets
Sprawl, and Verizon DBIR all converge on a single observation: most
organisations recognise the familiar five identity types (cloud IAM,
K8s SAs, CI/CD pipelines, DB service accounts, third-party API keys)
and underweight the long tail (mainframe, RPA, branch peripherals,
code-signing, AI agents, backup agents, vault-internal). The
[identity taxonomy](../research/identity-taxonomy.md) catalogs 37 NHI
classes — 14 COMMON, 23 UNCOMMON — and the long tail is where breaches
land disproportionately. At a major AU Tier-1 FI, this manifests
operationally as **no NHI inventory / discovery layer above the vault
tier**: Vault Enterprise governs the auth methods and engines wired up
to it, but the organisation does not know how many machine identities
exist outside that scope ([INTERNAL paraphrased], Task 0 §C.00).

**(b) Outcome-first regulatory pressure exceeds any single product.**
ACSC Essential 8 (maturity-modelled), NIST SP 800-207 Zero Trust
(seven pillars + Federation / Workload-mTLS / CICD / Runtime / NHIDR /
PQC sub-pillars), APRA CPS 234 + CPS 230 + CPG 234, and ASD ISM
intersect on credential-handling outcomes — restrict administrative
privilege, MFA the privileged paths, prevent unauthorised cryptographic
operations, govern the lifecycle. The combined map is **47 UCs ×
multiple controls per UC**; all 47 UCs map to a PRIMARY-LENS
(E8 + ZT) framework cell and all 47 back-map to CPS 234 + ISM
([`matrix/regulatory-trace.csv`](../matrix/regulatory-trace.csv);
145 control rows). No vendor evaluated covers the full outcome map
natively. The MITRE T1552 family + 15 breach post-mortems
([`research/adversary/`](../research/adversary/)) sharpen the lens:
plaintext-in-files, IMDS abuse, container-API token theft, private-key
exfiltration and OAuth-app drift are reducible to specific UC gaps.

**(c) The FI's current state is shaped by a 2019 selection and a
2020-onwards drift.** Vault Enterprise was selected, deployed and
hardened — multi-region with on-prem master and edge clusters in
OpenShift, AWS, and GCP under Performance Replication. From 2020
onwards, **cloud-native vaults (AWS Secrets Manager, Azure Key Vault,
GCP Secret Manager) increasingly took application-team load**; Vault
Enterprise became a *system of record* rather than the day-to-day
operational vault ([INTERNAL paraphrased], Task 0 §F.03). HashiCorp
licensing churn (~2–3 model changes in six years; production AND
non-production licensing) compounds vendor risk. CyberArk PAM holds
the AD service-account rotation lane after an earlier Vault attempt
was rolled back (Task 0 §I.03). The Thales SafeNet Luna →
Fortanix DSM HSM migration is recent and material. The 2019 red-team
finding of plaintext secrets in source repositories **remains open
today**, with the strongest lived-experience evidence (Task 0 §F.02 /
§F.04).

Stated simply: the FI is well-served at the **vault tier** for the use
cases that were prominent in 2019, materially under-served at the
**discovery and AI-agent tier** that emerged 2024–2026, and carrying
unresolved exposure on the **plaintext-in-repos lane** that has been
known for six years.

---

## §4 Goals and non-goals

> **Intent:** Crisp list. Goals = the dual matrix exists + XYZ gap is
> visible + recommendations are prioritised. Non-goals (explicitly) =
> RFI/RFP derivation, vendor TCO modelling, implementation roadmap
> sequencing (those flow into FI 27 strategy or v1.0).

**Goals (v0.1):**

- **G1.** Publish the universal buyer's framework as a dual matrix
  (UC × NHI × Vendor + UC × NHI × XYZ-state).
- **G2.** Score the FI's current deployment against every UC × NHI
  pair with explicit Met / Partial / Gap / Pending (UC-level for v0.1;
  per-pair deferred to v1.0).
- **G3.** Back-map every UC to Essential 8 + NIST ZT (PRIMARY) and
  APRA CPS 234 + ASD ISM (BACK-MAP). NIST CSF 2.0 deferred to v1.0
  (per stakeholder direction, Task 0 §B.03).
- **G4.** Audit every UC against MITRE ATT&CK T1552-family TTPs +
  ≥ 12 named breach post-mortems (actual: 16 techniques + 15
  post-mortems).
- **G5.** Hand the stakeholder a numbered list of recommendations
  (each pinned to UCs + NHIs) by Mon 2026-05-25.

**Non-goals (v0.1):**

- **N1.** Industry-agnostic v2 PRD (deferred until v1.0 reviewed).
- **N2.** RFI / RFP source documents derived from the PRD.
- **N3.** Vendor TCO modelling.
- **N4.** Implementation sequencing roadmap for the FI.
- **N5.** Detailed FI 27 strategy alignment beyond §16 reserved subsection.

---

## §5 Scope and assumptions

**In scope:**

- **19 vendors across 5 tiers** (see [ADR-004](./adrs/ADR-004-vendor-shortlist.md)):
  core (Vault Enterprise, CyberArk Conjur, CyberArk PAM, Delinea
  Secret Server); cloud-native (AWS Secrets Manager, Azure Key Vault,
  GCP Secret Manager, AKEYLESS); emerging (Doppler, Infisical,
  1Password Secrets Automation); PKI / MIM (Venafi, Keyfactor);
  NHI-discovery (Astrix, Entro, Oasis, Aembit, Clutch); data-security
  (Fortanix DSM).
- **37 NHIs** ([ADR-002](./adrs/ADR-002-identity-taxonomy-source.md))
  across the COMMON / UNCOMMON split.
- **47 UCs** (27 functional + 20 non-functional —
  [`research/use-cases.md`](../research/use-cases.md)).
- **Outcomes-first regulatory lens** (E8 + ZT primary; CPS 234 + ISM
  back-map — [ADR-003](./adrs/ADR-003-regulatory-lens.md)).
- **Adversary lens** (MITRE ATT&CK T1552 family + 15 breach
  post-mortems —
  [`research/adversary/`](../research/adversary/)).

**Out of scope (v0.1):**

- Human-identity (workforce / consumer) IAM.
- Generic cloud KMS / HSM market beyond the 19 vendors listed.
- Detailed PKI architecture deep-dives (Venafi / Keyfactor at
  vendor-profile depth only).
- Specific FI remediation cost / FTE modelling.
- NIST CSF 2.0 mapping (deferred to v1.0).
- Per-NHI-per-UC XYZ scoring (deferred to v1.0; UC-level for v0.1).

**Assumptions (challengeable):**

- **A1.** The FI runs Vault Enterprise as the primary secrets platform
  (2019 selection still active) — confirmed via Task 0 §D.01.
- **A2.** The FI is multi-cloud (AWS + Azure + GCP); on-prem still
  material; mainframe workloads exist with embedded credentials at
  non-trivial scale.
- **A3.** Open Banking AU / CDR exposure creates B2B partner-token
  surface (FAPI 2.0).
- **A4.** Essential 8 maturity reporting is a real internal artifact.
- **A5.** Distribution surface defaults to internal (PRD §17 O2).
- **A6.** CyberArk PAM is the procurement-protected incumbent for AD
  service-account rotation; PAM displacement is **out of scope**
  (Task 0 §I.03).
- **A7.** Fortanix DSM is the post-Thales HSM root for Vault unseal
  and the BYOK control plane (Task 0 §D.04).

---

## §6 Machine-identity taxonomy

Full taxonomy: [`research/identity-taxonomy.md`](../research/identity-taxonomy.md).
Catalog CSV: [`matrix/identity-catalog.csv`](../matrix/identity-catalog.csv).
Sourcing decision: [ADR-002](./adrs/ADR-002-identity-taxonomy-source.md).

The taxonomy enumerates **37 NHIs (14 COMMON, 23 UNCOMMON)** anchored
to the Cloud Security Alliance NHI Working Group, Gartner MIM, SPIFFE
and NIST SP 800-204D, with OWASP Secrets Management Cheat Sheet as the
operational cross-check. Each NHI is classified along five axes:
lifecycle (EPHEMERAL / SHORT-LIVED / LONG-LIVED / STATIC), trust
anchor, authentication shape, governance-maturity (industry typical),
and pure-NHI vs human-shared.

**The COMMON 14** (NHI-001..014) cover the familiar majority that any
product owner recognises: cloud IAM principals, Kubernetes
ServiceAccounts, CI/CD pipeline identities, container / image-pull
credentials, database service accounts, application TLS / mTLS
workload identity, third-party SaaS API keys, Git platform
credentials, IaC agents, observability agents, message-broker clients,
AD / LDAP service accounts, API-gateway upstream identity, RPA bots.

**The UNCOMMON 23** (NHI-015..037) are the overlooked long tail that
materially expands blast radius and where most breach post-mortems
land. They include:

- **Code-signing identity** (Sigstore Fulcio, Authenticode, Apple
  Notary — NHI-015) and **SLSA / in-toto attestation identity**
  (NHI-016).
- **Service-mesh control-plane identity** (Istiod, Linkerd, Consul
  Connect — NHI-017).
- **Confidential-computing / TEE attestation identity** (Nitro, SEV-SNP,
  TDX, MAA — NHI-018).
- **AI-agent / autonomous-workflow identity** (NHI-019) — the
  fastest-growing class and the one with weakest tooling consensus.
- **Mainframe / midrange identity** (RACF, ACF2, Top Secret, IBM-i —
  NHI-022). Material at the FI.
- **HSM / KMS operator** (NHI-024) and **CA operator** (NHI-025) —
  quorum-protected, high-privilege.
- **Backup / DR agent identity** (NHI-026) — primary ransomware target.
- **Open Banking / FAPI 2.0 partner identity** (NHI-028) — AU-CDR
  scope, regulator-driven maturity.
- **PQC / hybrid-PKI rotation identity** (NHI-034).
- **Vault-internal identity** (NHI-035) — the vault's own NHIs;
  recursive risk surface.
- **Ephemeral SPIFFE / workload-broker identity** (NHI-036) — the ZT
  destination class.
- **Forgotten / orphaned legacy identity** (NHI-037) — most-abused
  class per Verizon DBIR.

Cross-cutting concerns ([taxonomy §5](../research/identity-taxonomy.md))
warn that ephemerality is not free (the trust anchor becomes a Tier-0
dependency; NHI-035 hardening required); federation moves blame, not
risk; blast radius scales with privilege × persistence × reachability;
vault sprawl is the predictable failure mode in regulated estates;
observability dashboards routinely ingest secrets; PQC migration is on
every Tier-1 bank's 2026–2028 roadmap; and AU sovereignty constrains
SaaS vault choices materially.

---

## §7 Use cases (functional + non-functional)

Full catalog: [`research/use-cases.md`](../research/use-cases.md).
CSV: [`matrix/use-cases.csv`](../matrix/use-cases.csv).

**47 UCs total**: 27 functional + 20 non-functional. Each carries (a)
≥ 1 NHI ID; (b) an outcome lens (E8 control area and / or NIST ZT
pillar); (c) a back-map to CPS 234 + ISM (and CSF 2.0 where the
mapping was authored before the deferral — retained for v1.0); (d)
FI priority (P0 / P1 / P2). 16 UCs are P0, 23 P1, 8 P2.

**Functional UCs (UC-F-001..027) are engineer-, SRE- and
DevSecOps-facing.** They include the two user-supplied seeds —
**UC-F-001 prevent plaintext secrets in source repositories** and
**UC-F-002 detect and remediate secrets already in history** — both
P0. The catalog then covers JIT short-lived cloud creds via OIDC
(UC-F-003), workload-attested ephemeral identity via SPIFFE / SPIRE
(UC-F-004), dynamic DB credentials with broker-issued leases
(UC-F-005), automated rotation of long-lived static secrets
(UC-F-006), immediate revocation on identity compromise (UC-F-007),
K8s secret consumption without on-disk plaintext (UC-F-008), per-
workload image-pull credentials (UC-F-009), IaC apply-time secrets
(UC-F-010), observability-agent credential hygiene (UC-F-011),
message-broker client hardening (UC-F-012), gMSA / Kerberos
modernisation (UC-F-013), API-gateway upstream identity (UC-F-014),
RPA-bot session-bound vaulting (UC-F-015), keyless code- and
artifact-signing in CI (UC-F-016), TEE-attestation-gated secret
release (UC-F-017), **AI-agent tool-credential brokering**
(UC-F-018), IoT / OT / branch device enrolment (UC-F-019),
mainframe / midrange credential rotation (UC-F-020), backup / DR
agent de-privileging (UC-F-021), webhook inbound identity
verification (UC-F-022), network-device credential modernisation
(UC-F-023), Open-Banking / FAPI 2.0 mTLS partner identity
(UC-F-024), OAuth-app / marketplace governance (UC-F-025),
vault-internal identity hardening (UC-F-026) and orphaned / dormant
NHI cleanup (UC-F-027).

**Non-functional UCs (UC-N-001..020) are product-owner-, auditor-,
regulator- and incident-responder-facing.** The user-supplied seed
is **UC-N-001 real-time secret-sprawl KPI dashboard** (P0). The
catalog covers **UC-N-002 NHI inventory and ownership attestation**
(the one that anchors the dominant FI finding — see §12), UC-N-003
rotation-coverage KPIs, UC-N-004 regulator audit evidence pack,
UC-N-005 E8 / ZT control-area scorecard, UC-N-006 vendor / SaaS
supply-chain risk attestation, UC-N-007 data-sovereignty / residency
assurance, UC-N-008 engineer training adoption KPI, UC-N-009
exception register and risk-acceptance governance, UC-N-010
break-glass and quorum-operator governance, UC-N-011 post-incident
RCA with NHI attribution + MITRE technique, UC-N-012 supply-chain /
SLSA-provenance assurance reporting, UC-N-013 crypto-agility / PQC
readiness, UC-N-014 vendor-evaluation matrix maintenance, UC-N-015
communications cadence, UC-N-016 IoT / OT / branch-fleet posture
reporting, UC-N-017 observability secret-leak governance, UC-N-018
TEE attestation assurance, **UC-N-019 AI-agent KPI suite**,
UC-N-020 mainframe / legacy posture and exception transparency.

**Three cross-cutting clusters** frame PRD §8 and §11 / §12:

- **Cluster A — Detect-and-remediate plaintext sprawl** (UC-F-001 +
  UC-F-002 + UC-N-001 + UC-N-008). The user-supplied entry point;
  the cluster where the FI has the strongest lived-experience
  evidence of unresolved exposure.
- **Cluster B — Ephemeral, attested, brokered identity** (UC-F-003 +
  UC-F-004 + UC-F-005 + UC-F-008 + UC-F-017 + UC-F-018 + UC-F-019 +
  UC-N-002 + UC-N-005). The strategic destination; vendor evaluation
  is most discriminating here.
- **Cluster C — Govern the long tail and the vault itself**
  (UC-F-013 + UC-F-015 + UC-F-020 + UC-F-021 + UC-F-023 +
  UC-F-025 + UC-F-026 + UC-F-027 + UC-N-007 + UC-N-009 +
  UC-N-010 + UC-N-020). Where audit, risk and ransomware-resilience
  concentrate.

---

## §8 Evaluation rubric

> **Intent:** Define the scoring scheme. See
> [ADR-006](./adrs/ADR-006-scoring-rubric.md).

**Coverage tier (per `(UC, NHI, Vendor)`):**

- `NATIVE` — vendor's first-class capability with documented support.
- `ADD-ON` — vendor supports it via paid add-on / module.
- `PARTNER` — vendor relies on a partner / 3rd-party integration.
- `GAP` — vendor does not address.
- `N/A` — not applicable to this NHI bucket.

**Maturity level (0–4):**

- 0 — none / not announced.
- 1 — announced / preview / unsupported.
- 2 — GA basic.
- 3 — GA mature with reference customers.
- 4 — industry-leading.

**XYZ current-state (per `(UC, NHI)` — applied at UC level for v0.1):**

- `MET` / `PARTIAL` / `GAP` / `N/A` / `PENDING` with confidence
  (HIGH / MEDIUM / LOW) + evidence quote (paraphrased per
  [ADR-005](./adrs/ADR-005-anz-evidence-policy.md)) + gap notes.

The two axes are **directly joinable**: PRD §16 recommendations name
the UC × NHI cells where the FI is `GAP` *and* the vendor matrix shows
a `NATIVE` + Maturity ≥ 3 option *and* AU-residency / IRAP filtering
admits the vendor as a primary platform for APRA-regulated workloads.
Where AU residency disqualifies the strongest candidate, the
recommendation explicitly names that constraint and proposes a
secondary path (e.g., self-host, sovereign-cloud, control-plane-only
deployment).

Full rubric: [ADR-006](./adrs/ADR-006-scoring-rubric.md).

### §8.1 Sourcing & confidence — how much to trust each number

**Be precise about what is verified versus claimed.** This matters for a
procurement decision. The honest posture (full policy: [ADR-007](./adrs/ADR-007-reading-model-and-confidence.md)):

- **Capability *existence*** is mostly cited to **vendor documentation** —
  primary, but vendor-self-reported. ~60-70 % of matrix cells carry a
  vendor primary-source URL; the rest are analyst/consensus judgments
  where the vendor is silent or the capability is out of scope.
- **Maturity scores (0-4)** are **our analyst judgment** against the
  ADR-006 rubric — they are **not** independently evidence-gated. A
  vendor's "GA basic" statement maps to Maturity 2 on a single citation;
  no third-party reference-customer corroboration is required for v0.1.
- **Rankings** (§9, §11) are **PRD-writer synthesis** of the CSV, not
  primary facts — recompute from the CSV if a number is load-bearing.
- **Forward-dated GA claims** are **unverified vendor roadmap** — see the
  register below.

**Source-type / confidence tags** (read every claim against these):

| Tag | Meaning | Trust |
|---|---|---|
| `VERIFIED-PRIMARY` | Vendor doc / spec / changelog cited | Med-High (vendor-authored) |
| `ANALYST` | Third-party (Gartner/Forrester/etc.) | Medium |
| `INDUSTRY-CONSENSUS` | Widely held, not single-source-verified | Low-Med |
| `FORWARD-DATED` | Future / unverified GA date | Low — confirm with vendor SE |

**Forward-dated / unverified claims register** (carry into any RFI; none
of these is asserted as present fact in the matrix scoring):

| Vendor | Claim | Stated date | Status |
|---|---|---|---|
| Aembit | Blended Identity + MCP Identity Gateway | "GA Apr 2026" | `FORWARD-DATED` — unverified |
| Oasis Security | AI Agent identity (AAM) | "GA Nov 2025" | `FORWARD-DATED` — near-term, unverified |
| Fortanix DSM | FX3400 FIPS 140-3 | "pending" | `FORWARD-DATED` — roadmap |
| Doppler | MCP Server | "experimental 2026" | `FORWARD-DATED` — pre-GA |

**Per-layer confidence summary** (independent reviewer estimates, M2/M3):

- **PRD body claims:** ~85-90 % carry a primary-source URL (regulator /
  NIST / MITRE / vendor) — highest confidence.
- **Layer 1 (secrets managers):** vendor profiles ~50-60 % primary-cited;
  capability *existence* solid, maturity is judgment.
- **Layer 2 (NHI-discovery / governance):** youngest market, highest
  `INDUSTRY-CONSENSUS` density and most forward-dated claims — treat
  maturity 3-4 scores here as provisional pending SE validation.
- **Layer-0 substrate dependency (Fortanix, §9.x):** evaluated as
  infrastructure, not ranked; its forward-dated FIPS 140-3 claim is in the
  register above — confirm crypto certifications directly with the vendor.

A v1.0 fact-check pass (deferred) would web-verify the maturity 3-4 claims
and the forward-dated register against third-party sources (PRD §17).

---

## §9 Vendor capability matrix

Inline summary: [`matrix/matrix.md`](../matrix/matrix.md). Interactive
stakeholder report: [`matrix/matrix-viewer.html`](../matrix/matrix-viewer.html)
— a self-contained offline report with an XYZ-posture dashboard,
per-use-case and per-identity decision cards, and a browse-all table over
the 18 ranked vendors (1,512 rows; Fortanix excluded as a Layer-0
dependency). Raw data:
[`matrix/vendor-capabilities.csv`](../matrix/vendor-capabilities.csv).

**Read this first — these are not one competitive set.** The **18 ranked
vendors** occupy **two comparison layers** of the machine-identity stack,
and a `NATIVE` score means a *different thing* in each. Beneath them sits a
**Layer-0 crypto-substrate dependency** (the HSM / key-root the vault
unseals against) — a *dependency, not a competitor*, so it is **not scored
in the ranking**. Rank **within** a layer; **compose** across layers.
(Full rationale: [ADR-007](./adrs/ADR-007-reading-model-and-confidence.md).)

```
 Layer 2  NHI DISCOVERY / GOVERNANCE      (above the vault — 5 vendors)
          Astrix · Entro · Oasis · Aembit · Clutch
          NATIVE = discovers / inventories / governs this identity
                         ▲  governs
 Layer 1  SECRETS MANAGEMENT              (the vault tier — THIS PRD, 13 vendors)
          Vault · Conjur · CyberArk PAM · Delinea · AWS · Azure ·
          GCP · AKEYLESS · Doppler · Infisical · 1Password
          PKI/MIM lane: Venafi · Keyfactor
          NATIVE = brokers / stores / rotates secrets for this identity
                         ▲  unseals / key-roots  (a DEPENDENCY, not a vendor choice)
 Layer 0  CRYPTO SUBSTRATE                (below the vault — NOT ranked)
          the HSM / key-root the vault needs (XYZ: Thales SafeNet → Fortanix)
          evaluated as infrastructure, NOT shortlisted against vaults — see §9.x
```

A discovery tool's `NATIVE` (it *finds* the identity) is not comparable to
a vault's `NATIVE` (it *brokers secrets* for the identity). The Layer-0
substrate is a separate infrastructure decision, handled in §9.x — not in
the vendor ranking. Read the matrix through this key, not as one league
table.

**Headline shape:** 18 ranked vendors × (37 NHI + 27 UC-F + 20 UC-N) =
**1,512 ranked capability rows**. Aggregate distribution: NATIVE = 492
(33 %), ADD-ON = 483 (32 %), PARTNER = 28 (2 %), GAP = 491 (32 %),
N/A = 18 (1 %). (The source CSV retains Fortanix DSM's 84 rows = 1,596
total, kept as Layer-0 substrate reference but excluded from rankings,
cards, and the dashboard per ADR-007.)

### Layer 1 — Secrets management (the like-for-like comparison)

This is the layer the PRD is actually about. Ranked by NHI NATIVE count
*within the secrets-management layer* — the only place a head-to-head
NATIVE count is apples-to-apples:

1. HashiCorp Vault Enterprise — 26 NATIVE / 4 GAP.
2. AKEYLESS — 21 NATIVE / 5 GAP (capability strong; AU-residency
   constrained — ranked by raw coverage, not a primary-use recommendation).
3. Azure Key Vault — 18 NATIVE / 4 GAP.
4. GCP Secret Manager — 17 NATIVE / 8 GAP.
5. AWS Secrets Manager — 16 NATIVE / 7 GAP.
6. Delinea Secret Server — 14 NATIVE / 8 GAP.
7. CyberArk Conjur — 13 NATIVE / 8 GAP · Infisical — 13 NATIVE / 5 GAP.
9. CyberArk PAM — 10 NATIVE / 14 GAP (privileged-access lane, not a
   general secrets broker — see §11 / §16 R3-R4).
10. Doppler — 9 NATIVE / 18 GAP · 1Password Secrets Automation —
   7 NATIVE / 16 GAP.

Top UC-F (functional) NATIVE in this layer: Vault (17), AKEYLESS (14),
AWS (13).

**PKI / machine-identity sub-lane — a distinct discipline (certificate &
key lifecycle, not secrets brokering):** Keyfactor — 9 NATIVE / 16 GAP ·
Venafi — 8 NATIVE / 20 GAP. Their high GAP counts are *expected*: scored
against the secrets-broker rubric they look sparse, but their job is
governing certificates and keys. Judge them on PKI/MIM rows, not vault
rows.

### §9.x Layer-0 crypto-substrate dependency (not a ranked vendor)

The secrets layer does not stand alone: the vault must be **unsealed and
key-rooted** by an HSM / key-management substrate beneath it. This is a
**dependency, not a vendor choice within this comparison** — you do not
shortlist a crypto substrate *against* Vault, you *pair* one with it.
Accordingly, **the substrate is excluded from the 18-vendor ranking,
cards, and dashboard** (ADR-007); scoring an HSM on a 37-NHI / 47-UC
*secrets-management* rubric would be a category error (it GAPs ~21/37
NHIs by design — it never brokers application secrets).

**Why it still matters here, and what to do:**
- It is the **trust root** of the whole secrets stack — weak unseal /
  key-management posture compromises every secret above it.
- XYZ has a **live decision**: the Thales SafeNet Luna → **Fortanix DSM**
  HSM migration (Task 0 §D; see §11 F-V-4). Fortanix's load-bearing
  capabilities are vault auto-unseal / seal-wrap (PKCS#11), cross-cloud
  BYOK / EKM, and PQC readiness (ML-KEM / ML-DSA).
- **Action:** evaluate the substrate as **crypto infrastructure** on its
  own criteria (FIPS 140-3 level, IRAP, AU region, PQC roadmap, vault
  integration), *not* on the secrets-broker rubric. Its detailed profile
  is retained for reference in [Appendix B §B.6](./appendices/B-vendor-profiles-index.md)
  and the source CSV, clearly marked as a dependency.

### Layer 2 — NHI discovery / governance — ranked among peers, not against vaults

These five tools **discover, inventory and govern** non-human identities;
they do **not** broker or rotate secrets. A `NATIVE` here means the tool
*finds and governs* that identity class — the opposite question from a
vault's `NATIVE`. Ranked by discovery/governance breadth *within the
tier*:

1. Entro Security — 16 NATIVE / 12 GAP.
2. Astrix Security — 13 NATIVE / 15 GAP · Clutch Security — 13 NATIVE / 17 GAP.
4. Oasis Security — 11 NATIVE / 13 GAP.
5. Aembit — 10 NATIVE / 21 GAP (workload-IAM brokering sub-niche).

They are a **control-plane above existing vaults** — positioned in §16 as
an inventory / observability layer, **not** as primary secrets platforms.
Tier-wide constraint: SaaS-only with **no AU region / IRAP across the
tier**, material for APRA-regulated production (see §11 F-V-5 + snapshot
below).

**AU residency / IRAP snapshot:** AWS Secrets Manager, Azure Key Vault,
GCP Secret Manager all hold IRAP PROTECTED assessment and AU regions;
Vault Enterprise and Infisical self-host (customer responsibility);
CyberArk PAM Privilege Cloud is in AWS Sydney (IRAP pending);
**Astrix / Entro / Oasis / Aembit / Clutch are SaaS-only with no AU
region across the tier**; Doppler and 1Password Secrets Automation are
similarly disqualified for APRA-regulated production workloads
without explicit residency contracts. See [`matrix/matrix.md`](../matrix/matrix.md)
§4 for the full table.

---

## §10 XYZ current-state gap matrix

Inline XYZ matrix: [`matrix/matrix.md`](../matrix/matrix.md) (XYZ
column where applicable). Raw data:
[`matrix/anz-current-state.csv`](../matrix/anz-current-state.csv) (47
rows, one per UC). Evidence file:
[`research/anz-current-state-evidence.md`](../research/anz-current-state-evidence.md).

**Headline distribution (47 UCs):**

| State | Count | Share |
|---|---|---|
| MET | 0 | 0 % |
| PARTIAL | 16 | 34 % |
| GAP | 11 | 23 % |
| N/A | 0 | 0 % |
| PENDING | 20 | 43 % |

**No UC is definitively MET** — consistent with the dominant finding
that without an inventory / discovery layer the FI cannot quantify
"working" as "met". The 16 PARTIAL UCs are those where Vault
Enterprise (or CyberArk PAM, or Fortanix DSM, or a cloud-native vault)
provides the capability but adoption / observability lags. The 11 GAP
UCs are anchored by the dominant findings in §12 — plaintext-in-repos
(UC-F-001 / UC-N-001), no inventory (UC-N-002 / UC-N-005 / UC-N-008),
ZT workload identity (UC-F-004), AI-agent governance
(UC-F-018 / UC-N-019). The 20 PENDING UCs reflect the 1-hour Task 0
pass — they are not gaps proven, but evidence-insufficient lanes that
v1.0 deep-dive must close (PRD §17 O4).

The XYZ matrix uses a **per-UC schema for v0.1** (47 rows, no NHI
dimension). The dispatch prompt specified a per-UC × per-NHI schema;
the simplification is a deliberate v0.1 scope decision (per
[`notes/decisions.md`](../notes/decisions.md) — Task 0 was a 1-hour
pass; per-pair scoring would have exceeded lived-experience evidence).
PRD §17 O5 carries the per-pair revisit explicitly for v1.0.

All 47 XYZ rows carry `[INTERNAL]` sensitivity. All evidence quotes in
the CSV are paraphrased per [ADR-005](./adrs/ADR-005-anz-evidence-policy.md);
no `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` content is reproduced.

---

## §11 Findings — vendor side

The 1,596-cell matrix surfaces six findings worth narrating into the
PRD body. Per-vendor narrative depth lives in
[`research/vendors/`](../research/vendors/) (19 profiles); per-tier
framing is in [`matrix/matrix.md`](../matrix/matrix.md) §3.

**F-V-1. Vault Enterprise holds the broadest functional-NHI coverage,
but cannot close the inventory gap.** With 26 NATIVE NHI rows and 17
NATIVE UC-F rows ([`research/vendors/hashicorp-vault-enterprise.md`](../research/vendors/hashicorp-vault-enterprise.md)),
Vault Enterprise covers dynamic DB credentials, JIT cloud creds via
OIDC, SPIFFE-adjacent K8s identity, gMSA / Kerberos modernisation,
keyless signing and HSM-backed unseal — the spine of Cluster B. It is
weak on **NHI inventory** (UC-N-002), **OAuth-app discovery**
(UC-F-025), **AI-agent identity** (UC-F-018) and **AU sovereignty
posture** (self-hosted; customer responsibility for IRAP). Combined
with the licensing model change history ([INTERNAL paraphrased],
Task 0 §G.01: production + non-prod licensing materially raises TCO),
Vault Enterprise remains a strong primary platform whose value depends
on the layers above and below it being added.

**F-V-2. CyberArk PAM is the entrenched legacy lane — not displaceable
inside v0.1.** PAM is uniquely strong on UC-N privileged-access
governance lanes (8 NATIVE UC-N rows) and weaker on developer-facing
UC-F lanes (9 NATIVE), consistent with its category as a privileged-
access platform rather than a secrets-management platform
([`research/vendors/cyberark-pam.md`](../research/vendors/cyberark-pam.md)).
At the FI it owns AD service-account rotation (after a prior Vault
attempt was rolled back — Task 0 §I.03). PRD §16 explicitly does **not**
recommend PAM displacement; it recommends closing the gaps PAM does
not cover (cloud-native ephemeral, SPIFFE, K8s CSI), routing those to
Vault / cloud-native / discovery-tier solutions. The "legacy lane"
framing is a feature, not a critique.

**F-V-3. Cloud-native vaults are AU-residency winners but multi-cloud
laggards.** AWS Secrets Manager, Azure Key Vault and GCP Secret
Manager all hold IRAP PROTECTED assessment and AU regions; all three
materially under-score on multi-cloud reach, mainframe, SPIFFE and
FAPI 2.0 ([`matrix/matrix.md`](../matrix/matrix.md) §3). AKEYLESS
scores **21 NATIVE NHIs** — competitive with the hyperscalers — but
**has no AU SaaS region**; Tier-1 AU FIs must self-host the
customer-Gateway component, with no publicly named AU FI customers
([`notes/decisions.md`](../notes/decisions.md) 2026-05-22). AKEYLESS
is therefore **not a like-for-like replacement for Vault Enterprise**
at the FI without a customer-controlled AU deployment.

**F-V-4. Fortanix DSM is the crypto root below the vault tier — not a
vault competitor.** The 5 NATIVE NHI rows (NHI-018 TEE, NHI-023 KMIP,
NHI-024 HSM operator, NHI-034 PQC, NHI-035 vault-internal) are
exactly the load-bearing rows for vault unseal, BYOK / EKM across
hyperscalers, and PQC readiness
([`research/vendors/fortanix-dsm.md`](../research/vendors/fortanix-dsm.md)).
The FI's Thales SafeNet Luna → Fortanix migration ([INTERNAL
paraphrased], Task 0 §D.04) makes Fortanix DSM load-bearing today;
v1.0 should confirm IRAP status (PRD §17 O9) and BYOK / EKM coverage
across the three clouds.

**F-V-5. The NHI-discovery tier leads on AI-agent identity and on the
inventory gap — but is AU-residency-disqualified for production
primary use.** Across Astrix, Entro, Oasis, Aembit and Clutch:
**Oasis** AAM™ (GA Nov 2025, Maturity 4) and **Aembit** Blended
Identity + MCP Gateway (GA Apr 2026, Maturity 4) lead on AI-agent
identity governance — a category that did not exist in 2019.
**Aembit** is the NHI-036 workload-attested-broker exemplar.
**Entro** carries the broadest NHI inventory NATIVE coverage in this
tier (16); **Clutch** carries the strongest Identity Lineage Graph
+ shadow-MCP-discovery posture; **Astrix** carries the OAuth-app risk
narrative. **All five are SaaS-only with no AU region across the tier.**
For APRA-regulated production primary use they require explicit
data-residency contractual commitments and / or are scoped to a
**control-plane / observability layer** above existing vaults rather
than as primary platforms. This is the recommendation lane in PRD §16.

**F-V-6. The emerging tier (Doppler, Infisical SaaS, 1Password Secrets
Automation) is residency-disqualified for production at this FI.**
Doppler is SaaS-only on GCP us-central1; 1Password Secrets Automation
SaaS Connect Server is self-host but with material enterprise-
governance gaps for an APRA-regulated estate; Infisical can be self-
hosted with strong developer DX but a thinner enterprise-governance
posture. None are recommended as primary platforms; Infisical
self-host is the only emerging-tier candidate worth a v1.0 pilot for
developer-tooling scope.

**F-V-7. PKI / MIM tier (Venafi, Keyfactor) is bounded to certificate
lifecycle.** Both score well on NHI-006 (TLS workload), NHI-025 (CA
operator) and NHI-028 (Open Banking / FAPI 2.0 partner). Keyfactor
leads on PQC readiness (NHI-034). Both are recommended as the
certificate-lifecycle lane (UC-F-024, UC-N-013, UC-F-019); they are
not secrets-vault candidates.

---

## §12 Findings — XYZ side

This section paraphrases lived-experience signals from
[`research/anz-current-state-evidence.md`](../research/anz-current-state-evidence.md)
per [ADR-005](./adrs/ADR-005-anz-evidence-policy.md). Each finding is
attributed to "a major AU Tier-1 FI" (the dispatch context) and
mapped to ZT pillars / E8 control areas in §14. Where a finding
generates a recommendation, the recommendation ID is named in §16.

**F-A-1. No NHI inventory / discovery layer above the vault tier.**
Vault Enterprise governs only the auth methods and secret engines
wired up to it; the FI **does not have a clear picture of how many
machine identities actually exist**. This is the dominant
non-functional finding and drives **UC-N-001, UC-N-002, UC-N-005,
UC-N-008 as GAP / HIGH confidence**. It is the primary anchor for
recommendations R1 + R2 (§16). [INTERNAL paraphrased, Task 0 §C.00.]

**F-A-2. Vault Enterprise is the system of record, not the day-to-day
operational vault.** From 2020 onwards, AWS Secrets Manager, Azure
Key Vault and GCP Secret Manager increasingly carried application-team
load. Vault is now used for very specific multi-cloud + on-prem use
cases. This **reframes the consolidation thesis** in FI 27 (Task 0
§A.05): the gap is not "one vault, many tools" but "many vaults, no
control plane". Recommendation R3 addresses this directly. [INTERNAL
paraphrased, Task 0 §F.03.]

**F-A-3. Multi-vendor stack confirmed.** Vault Enterprise (auth + secret
engines + Transform/FPE for PCI tokenisation), CyberArk PAM (AD
service-account rotation after Vault rollback), narrow "advanced
cryptographic platform" deployment on Vault Transform, cloud-native
vaults (AWS SM / Azure KV / GCP SM). This is the **actual
architecture**, not the aspirational one, and the PRD scores against
it. [INTERNAL paraphrased, Task 0 §D.01, §G.04.]

**F-A-4. HSM migration: Thales SafeNet Luna → Fortanix.** Recent and
material; Fortanix DSM is load-bearing for Vault unseal. Drives
**UC-F-016 PARTIAL** (HSM-sealed; awaiting runbook confirmation) and
**UC-N-013 PARTIAL** (PQC readiness signalled but not roadmapped).
PRD §17 O9 carries the Fortanix DSM IRAP-status confirmation as an
open question. [INTERNAL paraphrased, Task 0 §D.04.]

**F-A-5. Vault DB dynamic-credentials engine is shelf-ware.** The
engine is enabled but adoption is effectively zero. The classic
"capability exists, control objective not met" pattern. Drives
**UC-F-005 PARTIAL** with strong shelf-ware framing and informs
recommendation R5. [INTERNAL paraphrased, Task 0 §C.02, §D.06.]

**F-A-6. Absent auth methods in Vault.** No Azure AD / Entra auth
method enabled (despite Azure being one of three clouds; no Azure
edge cluster either). No TLS-cert auth method. No PKI / SPIRE
workload-identity auth method. Drives **UC-F-003 PARTIAL** (AWS-only
JIT today), **UC-F-004 GAP** (no SPIFFE), and reinforces the
recommendation in R6 to demystify ZT workload identity. [INTERNAL
paraphrased, Task 0 §D.03.]

**F-A-7. PKI is partial — SSL team uses Vault via ServiceNow + AppRole.**
Dedicated SSL team manages cert lifecycle; workflow is ServiceNow
request → Vault (AppRole auth) → static secrets fetch → SSL cert
generation → emailed to user. Issuance supported; revocation status
unclear. Drives **UC-F-007 PARTIAL** (issuance via shared workflow,
lifecycle external to Vault) and **UC-F-008 GAP / UC-F-009 PENDING**.
[INTERNAL paraphrased, Task 0 §G.06.]

**F-A-8. Vault Enterprise licensing churn is a material commercial
concern.** HashiCorp has changed the licensing model 2–3 times in six
years; current model treats Vault Enterprise as licensed in
production AND non-production, materially raising TCO. Drives
**UC-N-006 PARTIAL** (vendor-risk concern) and informs the FI 27
alignment subsection (§16). [INTERNAL paraphrased, Task 0 §G.01.]

**F-A-9. Plaintext secrets in repositories — still open from the 2019
red team.** The 2019 finding that secrets are visible on source-control
repositories remains the dominant gap with the strongest
lived-experience evidence. Drives **UC-F-001 GAP / HIGH** and
**UC-N-001 GAP / HIGH**. The user-supplied seed UCs are exactly the
lanes where the FI has the most catching up to do. Anchors
recommendation R7. [INTERNAL paraphrased, Task 0 §E.00 #1, §F.02,
§F.04.]

**F-A-10. ZT workload identity widely cited as strategy, poorly
understood operationally.** ZT is widely cited as strategy; ZT
*workload identity* is a niche topic that most people do not
understand well. There is a budget envelope for non-human identities.
Drives **UC-F-004 GAP** (no SPIFFE), **UC-F-018 GAP** (AI-agent
identity governance), **UC-N-019 GAP**. PRD §16 treats **demystify
ZT workload identity** (R6) as a first-class deliverable per Task 0
§J.01 and §K. [INTERNAL paraphrased, Task 0 §J.01, §K.]

**Architectural posture (paraphrased per ADR-005).** Master Vault
cluster on-premise with primary + DR sites on-prem (DR Replication
active-passive); edge clusters in OpenShift, AWS and GCP under
Performance Replication; no Azure edge cluster (consistent with no
Azure auth method); Vault auth methods enabled: AppRole, Kubernetes,
AWS IAM, AWS EC2, OIDC, JWT, LDAP, GCP IAM, Token. Scale: hundreds
of dev teams, multi-cloud across all three hyperscalers, Kubernetes-
heavy, mainframe still material. Drives **UC-F-026 PARTIAL** and
**UC-F-020 PENDING**. [INTERNAL paraphrased, Task 0 §D.05, §D.03,
§B.02.]

**Adversary chain (2019 red team).** External consultancy, ~1-week
engagement, achieved CEO email breach via phishing then pivoted to
privileged access. Top NHI-related findings: (1) plaintext in repos;
(2) UNIX/Linux PA-SAs with over-broad permissions and direct database
access — blast-radius violation; (3) CEO phishing → privileged-access
pivot. TTP chain: T1566 (Phishing) → T1078 (Valid Accounts) →
T1552-family (Credentials in Files / Cloud Instance Metadata /
Private Keys) → T1098 (Account Manipulation via over-permissioned
PA-SA); T1199 (Trusted Relationship) likely; T1556.006 unconfirmed.
[INTERNAL paraphrased, Task 0 §F.01, §F.02, §F.05.] The chain
narrates into PRD §13 and Appendix D.

---

## §13 Adversary context

Full detail: [`research/adversary/mitre-attack-t1552-family.md`](../research/adversary/mitre-attack-t1552-family.md)
+ [`research/adversary/breach-postmortems.md`](../research/adversary/breach-postmortems.md).
Appendix D consolidates the narrative. The
[`matrix/regulatory-trace.csv`](../matrix/regulatory-trace.csv) carries
31 ADVERSARY-LENS rows (16 MITRE techniques + 15 breach
post-mortems), each joined to ≥ 1 UC and ≥ 1 NHI.

**MITRE T1552 sub-techniques in scope** (8 + 8 adjacent):

- T1552.001 Credentials in Files — Uber 2022, Toyota 2022; mitigates
  via UC-F-001/002/005/006/010 + UC-N-001/002.
- T1552.002 Credentials in Registry — multiple ransomware crews,
  SolarWinds post-compromise; UC-F-006/013/015/027 + UC-N-002.
- T1552.003 Bash History — Sourcegraph Aug 2023; UC-F-001/005/006
  + UC-N-008/017.
- T1552.004 Private Keys — Storm-0558 Jul 2023, xz-utils Mar 2024;
  UC-F-004/006/016/017/026 + UC-N-010/013.
- T1552.005 Cloud Instance Metadata API — Capital One 2019, Sumo
  Logic Nov 2023; UC-F-003/004/008/009/017 + UC-N-002.
- T1552.006 Group Policy Preferences — persistent AD pen-test
  finding (mirrored in the FI's 2019 red team); UC-F-006/013/027 +
  UC-N-002.
- T1552.007 Container API — TeamTNT 2021–2023, SCARLETEEL 2023;
  UC-F-004/008/009/017 + UC-N-002.
- T1552.008 Chat Messages — Uber 2022; UC-F-001/007/025 +
  UC-N-008/017.

**Adjacent techniques mapped**: T1528 Steal Application Access Token,
T1078.004 Valid Cloud Accounts, T1606.002 Web Cookies, T1098.001
Account Manipulation, T1199 Trusted Relationship, T1539 Web Session
Cookie, T1556.006 MFA Modification, T1566 Phishing.

**15 named breach post-mortems**, each joined to UC mitigations: Okta
2023-10 (HAR file token theft), Okta 2022-01 LAPSUS$, Cloudflare
2023-11 (Okta-pivoted), CircleCI 2023-01 (engineer endpoint
compromise → 2FA token theft), Internet Archive 2024-10, Sourcegraph
2023-08, LastPass 2022 (DevOps engineer credential compromise),
xz-utils 2024-03 (multi-year supply-chain compromise), SolarWinds
2020, Storm-0558 2023-07, Uber 2022-09, Toyota 2022-10, Sumo Logic
2023-11, MOVEit 2023 (in which the FI was named in the victim
cohort — [PUBLIC]), Snowflake-related 2024-06.

**Reading for the FI:** every dominant XYZ finding in §12 maps to
≥ 1 TTP and ≥ 1 breach. F-A-9 (plaintext-in-repos) is T1552.001 +
the Uber 2022, Toyota 2022, and Internet Archive 2024-10 lessons.
F-A-6 (no SPIFFE, AWS-only JIT) is T1552.005 + Capital One 2019 +
Sumo Logic 2023. F-A-10 (ZT workload identity not understood) is
T1552.007 + TeamTNT / SCARLETEEL. F-A-2 (vault sprawl across cloud-
native) is T1552.004 + T1078.004 + LastPass 2022 + Storm-0558. The
recommendations in §16 are sized against the breach-impact evidence,
not against abstract control wishlists.

---

## §14 Regulatory traceability summary

Outcomes-first lens per [ADR-003](./adrs/ADR-003-regulatory-lens.md):
**E8 + NIST ZT primary**; **CPS 234 + ISM back-map**; **CSF 2.0
deferred** to v1.0. Full table:
[Appendix A](./appendices/A-compliance-traceability.md) (Wave B).
Raw join: [`matrix/regulatory-trace.csv`](../matrix/regulatory-trace.csv)
(145 control rows; all 47 UCs covered by both PRIMARY and BACK-MAP
frames).

**Essential 8 coverage** (8 mitigation strategies × ML1/2/3 = 24
control codes — see
[`research/regulatory/essential-8-mapping.md`](../research/regulatory/essential-8-mapping.md)).
The FI's secrets-management programme touches all 8 strategies but
concentrates on **Restrict Administrative Privileges (RAP)**, **Multi-
Factor Authentication (MFA — machine)**, **Application Control (AC)**
and **Patch Operating Systems (PA)**. Moving from ML2 → ML3 on RAP
alone closes UC-F-003, UC-F-004, UC-F-006, UC-F-013, UC-F-018,
UC-F-021 — the spine of Cluster B + the long-tail governance items in
Cluster C.

**NIST ZT pillar coverage**
([`research/regulatory/nist-sp-800-207-zt-mapping.md`](../research/regulatory/nist-sp-800-207-zt-mapping.md)):
all 7 pillars + Federation, Workload-mTLS, CICD, Runtime, NHIDR,
PQC sub-pillars are referenced. The **Identity** pillar (and the
**Federation** sub-pillar) carry the heaviest UC density; **Workload**
and **Visibility-Analytics** carry the next two. The PQC sub-pillar
maps to UC-N-013 (crypto-agility / PQC readiness) and is the v0.1
hook for the 2030-deadline obligations.

**APRA CPS 234 back-map**
([`research/regulatory/apra-cps-234-mapping.md`](../research/regulatory/apra-cps-234-mapping.md)).
Paragraph numbering normalised to **§21(a)-(d), §27(a)-(e),
§35(a)-(b)** (the dispatch prompt's earlier shorthand §28a-§28e /
§35a-§35c was corrected mid-project and is captured in
[meta/review-M2-2026-05-23.md](../meta/review-M2-2026-05-23.md) §B3).
**§22** (control implementation) anchors UC-F-003, UC-F-004,
UC-F-010, UC-N-002, UC-N-005, UC-N-009. **§28** (testing) anchors
UC-N-003, UC-N-004 and the back-map of UC-N-011 (post-incident RCA).
CPS 230 §39 (data residency / BCM) is the back-map for UC-N-007 and
the AU-residency framing of every SaaS-tier vendor.

**ASD ISM back-map**
([`research/regulatory/asd-ism-mapping.md`](../research/regulatory/asd-ism-mapping.md)).
41 ISM controls across 11 domains: Cryptography, Identification &
Authentication, System Hardening, Software Development, Database
Systems, Network & Gateways, Communications, Incidents, Personnel,
Governance, Backups. ISM-1619 (service-account credentials) carries the heaviest UC
density; ISM-1405 (centralised event logging) anchors UC-N-001 /
UC-N-011; ISM-1795 (credential length for service/admin accounts) carries the AD service-
account + mainframe lanes (UC-F-013, UC-F-020).

**Reading for the FI:** §14 is the audit-facing view of §9 + §10.
A regulator asking "show me your CPS 234 §22 evidence for NHI
governance" gets routed to UC-F-003 + UC-F-004 + UC-F-006 + UC-N-002
+ UC-N-005 with the current XYZ-state column joined in — a single
evidence pack per the UC-N-004 acceptance criteria. PRD §16
recommendations are sequenced to maximise E8-ML uplift per recommendation.

---

## §15 Risks and dependencies

Two halves: (a) risks to the report; (b) risks the FI inherits from
current-state gaps. Each carries an owner (in italics).

**(a) Risks to the report.**

- **R-rep-1. Data freshness.** The cross-vendor matrix and Task 0
  current-state read are accurate as of 2026-05-23. Vendor moves
  (Cisco→Astrix acquisition pending; Entro M&A unconfirmed; CyberArk
  PAM cloud regions evolving; Fortanix DSM IRAP status pending) will
  drift the matrix within 6–12 months. *Owner: PRD maintainer (v1.0
  refresh cadence).*
- **R-rep-2. Sensitivity leakage.** Two `[INTERNAL]` paraphrasing
  near-misses surfaced at M2 review
  ([`meta/review-M2-2026-05-23.md`](../meta/review-M2-2026-05-23.md) §C):
  Fortanix DSM XYZ migration attribution + Vault Enterprise
  `[USER-CONFIRMED EXPERIENCE]` rows. PRD body uses paraphrased
  attribution throughout; vendor profiles flagged for paraphrasing
  before any distribution beyond the M3 stakeholder review.
  *Owner: PRD maintainer + reviewer (gate enforcement).*
- **R-rep-3. FI 27 surprise.** The stakeholder briefing on FI 27 is
  not yet complete; PRD §16 reserves an FI 27 alignment subsection
  but the detail is conditional. v1.0 must reconcile §16-R3 (control-
  plane consolidation) against FI 27 specifics. *Owner: stakeholder +
  PRD maintainer.*
- **R-rep-4. NIST CSF 2.0 deferral.** Explicit and stakeholder-
  accepted (Task 0 §B.03 + M2 gate). Audience members expecting CSF
  2.0 will be redirected to v1.0. *Owner: PRD maintainer.*
- **R-rep-5. Per-pair XYZ scoring schema.** The v0.1 XYZ matrix uses
  a per-UC schema; per-pair (UC × NHI) deferred to v1.0
  ([`notes/decisions.md`](../notes/decisions.md)). *Owner: PRD
  maintainer + stakeholder for Task 0 v1.0 pass.*

**(b) Risks the FI inherits from current-state gaps.** Each is
mapped to a §16 recommendation.

- **R-fi-1. No inventory means no MET.** With 0 MET UCs, the FI
  cannot defensibly attest to control effectiveness even where
  capability exists. Drives R1. *Owner: Head IAM + Head Platform
  Security.*
- **R-fi-2. Plaintext-in-repos remains the dominant exposure.**
  T1552.001 is the most-cited initial-access pattern in the breach
  catalog. Drives R7. *Owner: DevSecOps + IAM.*
- **R-fi-3. Vault sprawl invisible to control plane.** Cloud-native
  vault drift since 2020 has no inventory or KPI coverage. Drives
  R3. *Owner: Platform Security.*
- **R-fi-4. ZT workload identity ambition ≠ operational reality.**
  No SPIFFE; no Azure / TLS-cert / PKI auth in Vault. Drives R6.
  *Owner: Platform Security + Architecture.*
- **R-fi-5. CyberArk PAM scope drift unclear post-2019 red team.**
  UNIX/Linux PA-SA over-permission status post-CyberArk-PAM is
  unconfirmed (PRD §17 O10). Drives R4 + R8. *Owner: PAM team +
  internal audit.*
- **R-fi-6. AI-agent NHI governance gap.** A 2024-2026 category
  largely unserved by the FI's incumbent stack. Drives R6. *Owner:
  Platform Security + AI / Data platform.*
- **R-fi-7. Vendor commercial risk on Vault Enterprise licensing.**
  Drives R3 commercial sequencing. *Owner: Procurement + Architecture.*

---

## §16 Recommendations

Recommendations are prioritised, each pinned to UC IDs + NHI IDs, with
explicit XYZ-state and vendor-matrix references. The order is
**outcome impact × adversary exposure × regulatory weight**, not
vendor preference.

**R1. Close the NHI inventory gap as a control-plane / observability
layer above the existing vaults.** Pinned to UC-N-001, UC-N-002,
UC-N-005, UC-N-008, UC-N-019. Anchors §12 F-A-1, §12 F-A-2. The
NHI-discovery tier (§11 F-V-5) leads on capability; AU-residency
disqualification means the deployment is **observability /
inventory only**, not a replacement for the vault tier, until / unless
a customer-controlled AU deployment is operationalised. Sequence:
(a) inventory pilot with 2–3 NHI-discovery vendors against a single
business unit; (b) tie discovered NHIs to UC-N-002 owner-attestation
workflow; (c) feed UC-N-001 KPI dashboard. **Adversary lens:** every
T1552 sub-technique benefits — you cannot defend what you cannot
count. **Regulatory lens:** CPS 234 §22 evidence pack + E8-RAP
ML2 → ML3.

**R2. Adopt the user-supplied seeds as the v0.1 demonstration
deliverable.** UC-F-001 (prevent plaintext secrets in source repos)
+ UC-F-002 (history sweep + rotate) + UC-N-001 (sprawl KPI dashboard)
+ UC-N-008 (training adoption). The 2019 red-team finding remains
open (§12 F-A-9); closing it produces the most tangible audit and
breach-narrative win. **Adversary lens:** T1552.001 + Uber 2022 +
Toyota 2022 + Internet Archive 2024-10. **Regulatory lens:** CPS 234
§17 + §28 + ISM-1619 + ISM-1690.

**R3. Consolidate via a control-plane pattern, not vault
displacement.** Pinned to UC-N-002, UC-N-005, UC-N-014, UC-F-026.
Anchors §12 F-A-2 + §15 R-fi-3. The post-2020 drift to cloud-native
vaults is not reversible at acceptable cost; the FI 27 consolidation
goal is best served by a **control-plane + inventory** pattern that
spans Vault Enterprise + cloud-native vaults + CyberArk PAM +
Fortanix DSM. This is the lane the NHI-discovery tier serves
(observability layer per R1) plus a federated-policy layer for
ownership, rotation policy and exception register. Avoid recommending
single-vault rebuild; the migration cost would exceed the value and
collides with the licensing-churn vendor-risk concern (§12 F-A-8).

**R4. Hold CyberArk PAM in its legacy lane; close adjacent gaps with
Vault + cloud-native + discovery.** Pinned to UC-F-013 (gMSA / AD),
UC-F-015 (RPA), UC-F-021 (backup agents), UC-F-023 (network device),
UC-N-010 (break-glass). PAM displacement is **out of scope** per
Task 0 §I.03; recommendations close the lanes PAM does not cover
(cloud-native ephemeral, SPIFFE, K8s CSI) rather than rebuilding its
core (AD SAs, DB privileged accounts, session brokering).

**R5. Move Vault's dynamic-DB engine off the shelf.** Pinned to
UC-F-005. Anchors §12 F-A-5. A scoped pilot in 1–2 business units
with a measurable adoption KPI in UC-N-003 (rotation-coverage). The
capability exists and is funded; the gap is adoption + telemetry.
**Adversary lens:** T1552.001 + T1552.003 (DB connection strings on
disk and in shell history).

**R6. Demystify ZT workload identity — as a first-class FI 27
deliverable.** Pinned to UC-F-003 (JIT cloud creds), UC-F-004
(SPIFFE / SPIRE), UC-F-008 (K8s CSI), UC-F-017 (TEE attestation),
**UC-F-018 (AI-agent tool-credential brokering)** and UC-N-019
(AI-agent KPI suite). Anchors §12 F-A-6 + §12 F-A-10. Per Task 0 §K,
**ZT workload identity is a niche topic that most people do not
understand well**; the recommendation is to **treat operator-grade
demystification as a discrete deliverable** — runbooks, reference
architectures, pilot stories — not as a side-effect of vendor
selection. AI-agent identity (NHI-019) is included as a first-class
sub-deliverable, **not** as a bolt-on, per the cross-vendor
finding that the NHI-discovery tier is leading this category (§11
F-V-5; matrix.md §5). **Adversary lens:** T1552.005 + T1552.007 +
Capital One 2019 + TeamTNT / SCARLETEEL.

**R7. Make plaintext-in-repos remediation visible at the board.**
Pinned to UC-F-001 + UC-F-002 + UC-N-001 + UC-N-008. Anchors §12
F-A-9. This is R2 expressed as a board-facing narrative: the 2019
red-team finding remains open; six years is a long window; the
combination of pre-commit + push-protection + history sweep +
rotation SLA + KPI dashboard is operationally cheap relative to its
risk reduction. The breach catalog narrates the consequence.

**R8. Audit-fix the post-2019 PA-SA over-permission status.** Pinned
to UC-F-014, UC-F-021, UC-N-002, UC-N-010. Anchors §12 F-A-3 +
§15 R-fi-5. The 2019 finding "UNIX/Linux PA-SAs with direct database
access and over-broad permissions" — status post-CyberArk-PAM is
unclear. PRD §17 O10 carries this as an explicit open question; R8
turns the open question into a remediation track.

**R9. Cert lifecycle: confirm revocation workflow and integrate.**
Pinned to UC-F-007, UC-F-008, UC-F-009, UC-F-024. Anchors §12 F-A-7.
The SSL team's issuance workflow is operating; revocation status is
unclear (PRD §17 O8). Integrating Venafi or Keyfactor as the cert
lifecycle lane (NHI-025 / NHI-028) closes the gap without disturbing
Vault's PKI engine for internal mTLS use.

**R10. Confirm Fortanix DSM IRAP status and BYOK / EKM coverage
across three clouds.** Pinned to UC-F-016, UC-F-017, UC-N-013,
UC-N-018. Anchors §12 F-A-4 + PRD §17 O9. v1.0 work; surfaced at
v0.1 because Fortanix DSM is load-bearing and the IRAP-status
uncertainty is a procurement / audit risk.

**R11. Maintain the vendor-evaluation matrix at release cadence.**
Pinned to UC-N-014. Vendor moves (Cisco → Astrix pending, Entro M&A,
CyberArk acquisition of Venafi, AKEYLESS AU posture, Fortanix
IRAP) require refresh; the matrix and PRD §11 must be refreshed at
each release cycle, with capability deltas highlighted and
independent reviewer sign-off (UC-N-014 acceptance criteria).

### FI 27 alignment (reserved subsection — per Task 0 §A.05 + §J.01 + §K)

FI 27 has two intertwined themes (Task 0 §A.05): (1) **cloud-native
+ Zero Trust + workload identity (SPIFFE / OIDC)** — attested
ephemeral identity, away from long-lived static secrets; (2)
**re-platform / consolidation** — fewer vaults, fewer integrations,
clearer ownership. The v0.1 recommendations align as follows:

- **Theme 1 (ZT workload identity):** R6 is the primary deliverable.
  R6 explicitly includes **demystify ZT workload identity for
  FI-grade operators** as a first-class deliverable (per Task 0 §K),
  with AI-agent identity (NHI-019) as a first-class sub-deliverable.
- **Theme 2 (consolidation):** R3 reframes consolidation as a
  control-plane / inventory layer (R1 + R3 paired) rather than
  vault displacement, given the 2020-onwards drift and the
  CyberArk PAM entrenchment.
- **Sequencing**: R1 + R2 + R7 in the first window (inventory +
  plaintext remediation visibility); R5 + R6 + R8 in the second
  (dynamic creds adoption + ZT demystification + PA-SA audit-fix);
  R3 + R4 + R9 + R10 + R11 in the third (control-plane integration,
  cert lifecycle, Fortanix IRAP confirmation, matrix maintenance).

This alignment is **conditional and revisitable** once the FI 27
detailed programme structure is briefed (PRD §17 O7).

---

## §17 Open questions

Surfaces from Task 0 lived-experience evidence + M2 reviewer findings,
deduplicated. Each is owned (stakeholder confirmation) and fed into
v1.0 deep-dive scope.

**Stakeholder / audience / distribution (carried from M1 + Task 0 §A):**

- **O1.** Confirm primary stakeholder role inside the FI — Task 0
  §A.01 confirmed Head IAM + Head Platform Security both lenses.
  v1.0 — confirm read-out plan.
- **O2.** Confirm distribution surface (Task 0 §A.03: internal-only
  for now; vendor SE binding may follow). Default: internal.

**Vendor / procurement (carried from Task 0 §I and M2 review §F):**

- **O3.** Confirm vendor procurement exclusions beyond CyberArk PAM
  AD lock-in (Task 0 §I.03).
- **O4.** Mainframe / RPA / AI / IoT-OT / B2B coverage — most marked
  PENDING in the XYZ matrix.
- **O5.** Per-pair (UC × NHI) XYZ scoring — accept v0.1
  simplification to per-UC and revisit at v1.0?
  ([`meta/review-M2-2026-05-23.md`](../meta/review-M2-2026-05-23.md) §F.2.)

**Adversary / IR (carried from Task 0 §F + §H):**

- **O6.** SSH access governance posture (Vault SSH OFF — Task 0
  §D.06; likely CyberArk PSM-brokered + static keys).
- **O7.** XYZ incident details withheld (Task 0 §H.01 / §H.02) —
  request stakeholder authorisation for anonymised inclusion in v1.0
  if it would sharpen §14.

**Regulatory / data:**

- **O8.** NIST CSF 2.0 deferral — explicit stakeholder accept that
  v0.1 ships with 4 frameworks (E8 + ZT + CPS 234 + ISM) and CSF is
  v1.0?
  ([`meta/review-M2-2026-05-23.md`](../meta/review-M2-2026-05-23.md) §F.1.)
- **O9.** Fortanix DSM IRAP status confirmation (drives R10 + the
  AU-residency map in §9).
- **O10.** 2019 PA-SA over-permission status today — confirm or
  reject post-CyberArk PAM (drives R8; Task 0 §F.04).

**Strategy / FI 27:**

- **O11.** FI 27 detailed programme structure / KPIs / timeline —
  full v1.0 alignment work.
- **O12.** Cert revocation workflow at SSL team (Task 0 §G.06; drives
  R9).

**Sensitivity / publication (from M2 review §F.3):**

- **O13.** Vendor-profile direct-XYZ-attribution lines (Fortanix HSM
  migration; Vault Azure auth not enabled) — confirm paraphrasing
  before any distribution beyond the M3 stakeholder review.
- **O14.** Astrix citation density — confirm tagging-convention
  difference vs real gap (M2 review §F.4).
- **O15.** Matrix-viewer browser sanity (M2 review §F.5).

---

## §18 Glossary

See [Appendix C](./appendices/C-glossary-and-NHI-definitions.md)
(Wave B). Every NHI ID (NHI-001..NHI-037) is expanded to its
full definition + primary citation; every acronym used in this PRD
(E8, ZT, CPS 234, ISM, NHI, MIM, SPIFFE, SPIRE, NHIDR, PQC,
IRAP, CDR, FAPI, gMSA, RACF, ACF2, BYOK, EKM, TEE, MCP) is
defined inline with source.

---

## §19 Appendices

- [Appendix A — Compliance traceability](./appendices/A-compliance-traceability.md)
  (Wave B) — full UC × framework table from
  [`matrix/regulatory-trace.csv`](../matrix/regulatory-trace.csv).
- [Appendix B — Vendor profiles index](./appendices/B-vendor-profiles-index.md)
  (Wave B) — one paragraph per vendor with link to
  [`research/vendors/`](../research/vendors/).
- [Appendix C — Glossary and NHI definitions](./appendices/C-glossary-and-NHI-definitions.md)
  (Wave B).
- [Appendix D — Adversary context](./appendices/D-adversary-context.md)
  (Wave B) — consolidated narrative from
  [`research/adversary/`](../research/adversary/), organised by
  NHI bucket.

---

## §20 ADR log

- [ADR-001 — Format choice](./adrs/ADR-001-format-choice.md) — Enterprise PRD + ADRs + dual matrix + compliance trace appendix.
- [ADR-002 — Identity taxonomy source](./adrs/ADR-002-identity-taxonomy-source.md) — CSA NHI WG + Gartner MIM + SPIFFE deltas; 37 NHIs.
- [ADR-003 — Regulatory lens (outcomes-first)](./adrs/ADR-003-regulatory-lens.md) — E8 + ZT primary; CPS 234 + ISM back-map; CSF 2.0 deferred.
- [ADR-004 — Vendor shortlist (19)](./adrs/ADR-004-vendor-shortlist.md) — 5-tier 19-vendor scope.
- [ADR-005 — XYZ evidence policy (sensitivity)](./adrs/ADR-005-anz-evidence-policy.md) — `[PUBLIC]` / `[INTERNAL]` / `[SENSITIVE]` / `[NOT-FOR-DISTRIBUTION]` with redaction rules; default attribution "a major AU Tier-1 FI".
- [ADR-006 — Scoring rubric](./adrs/ADR-006-scoring-rubric.md) — NATIVE / ADD-ON / PARTNER / GAP / N/A × Maturity 0–4; XYZ-axis MET / PARTIAL / GAP / N/A / PENDING.
- [ADR-007 — Reading model & confidence](./adrs/ADR-007-reading-model-and-confidence.md) — three-layer stack (L0 substrate / L1 secrets-mgmt / L2 governance), rank-within-layer, NATIVE-is-layer-relative; sourcing-confidence taxonomy + forward-dated register (§8.1).

---

> _End of v0.1 Wave A. Appendices A–D are Wave B (separate dispatch).
> Any `[TBD]` or `Deferred` reference resolves to PRD §17 Open
> Questions._

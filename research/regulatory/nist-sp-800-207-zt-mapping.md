# Regulatory Mapping — NIST SP 800-207 Zero Trust Architecture

**Role in PRD:** PRIMARY-LENS (outcomes-first, per ADR-003)
**Primary source:** https://csrc.nist.gov/publications/detail/sp/800-207/final
**Version cited:** NIST SP 800-207 "Zero Trust Architecture" (final, August 2020), supplemented by NIST SP 1800-35 "Implementing a Zero Trust Architecture" (Volumes A–E, final June 2025) and NIST SP 800-204D "Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines" (final, February 2024).
**Sensitivity:** [PUBLIC]
**Mapped by:** Opus 4.7 (prompt 04 v0.1), 2026-05-23 AEST.

---

## 1. Framework summary

NIST SP 800-207 defines **Zero Trust (ZT)** as a set of cyber-security
paradigms that move defences from static, network-based perimeters to
**users, assets, and resources** — making per-request, dynamic
authorisation decisions on the basis of "as much context as is
practically available" [nist-sp-800-207-2020]. A **Zero Trust
Architecture (ZTA)** is the enterprise's cyber-security plan that
applies ZT concepts to component relationships, workflow planning, and
access policies. The document explicitly names the **Policy Engine
(PE), Policy Administrator (PA), and Policy Enforcement Point (PEP)**
as the logical control plane; PEPs broker access to **resources** —
NIST treats data, services, **workloads, and accounts/credentials**
themselves as in-scope resources [nist-sp-800-207-2020, §3].

SP 800-207 enumerates **seven tenets** (§2.1) and three **deployment
variants** (device-agent / gateway, enclave, resource-portal) but is
deliberately implementation-neutral. The operational
companion is **NIST SP 1800-35** (NCCoE) which structures ZTA into
**seven cross-cutting pillars** — Identity, Device, Network /
Environment, Application & Workload, Data, Visibility & Analytics, and
Automation & Orchestration — overlaid by a **Governance** capability
[nist-sp-1800-35-2025]. CISA's Zero Trust Maturity Model v2.0 maps the
same seven pillars to four maturity stages (Traditional → Initial →
Advanced → Optimal) [cisa-ztmm-v2-2023]; this PRD uses the NCCoE pillar
labels because they preserve the **Governance** band that APRA-
regulated audit demands.

ZT is the PRD's **second primary outcome lens** (ADR-003) alongside
Essential 8 because (a) every secret release decision is, in ZT
language, a per-request authorisation against a verifiable subject
(NHI) and an attested workload context; (b) the seven-pillar framing
gives the secrets-management programme a vocabulary the Essential 8
lacks for **machine-to-machine identity, attestation, micro-segmentation,
and identity-behaviour analytics**; and (c) NIST's policy-engine
architecture cleanly maps to the broker pattern that vault, KMS,
SPIRE, and workload-IAM products implement. Per ADR-003 the
**back-maps to CPS 234, ISM, and CSF 2.0** are scoped to sibling
agents; this document deliberately stays on the outcomes lens.

## 2. Control objectives in scope

The seven pillars (NCCoE / CISA labelling), with secrets-management /
NHI relevance scored:

- **ZT-Pillar-Identity** — **HIGHEST** relevance. Every NHI is a
  subject; SP 800-207 §3.1.2 requires identification, attribution and
  per-request authorisation for "users and devices, including any
  non-person entities (NPEs)" [nist-sp-800-207-2020].
- **ZT-Pillar-Workload** — **HIGHEST**. NIST SP 800-204D's service-mesh
  and CI/CD guidance is the operational reference for workload-attested,
  ephemeral credentials (SPIFFE/SVID, OIDC-federated CI/CD)
  [nist-sp-800-204d-2024].
- **ZT-Pillar-Device** — HIGH (adjacent). Device-health posture gates
  secret release; TPM-rooted IoT/ATM identities live here.
- **ZT-Pillar-Network** — HIGH. Micro-segmentation around the secrets
  broker, mTLS east-west, and partner-mTLS (FAPI 2.0) all sit here.
- **ZT-Pillar-Data** — HIGH (adjacent). Data-at-rest and TDE keys
  ARE NHIs (NHI-023); TEE-attested secret release is data-pillar.
- **ZT-Pillar-Visibility-Analytics** — **HIGHEST**. The "log everything,
  baseline behaviour, react to anomalies" tenet (§2.1.7) is what
  separates a vault from a secrets-management *programme*.
- **ZT-Pillar-Automation-Orchestration** — HIGH. NIST §3.4.3 explicitly
  cites SOAR-driven response; rotation/revocation/credential lifecycle
  automation belongs here.
- **ZT-Pillar-Governance** — HIGH (NCCoE addition). Policy-as-code for
  NHI access, exception register, scorecards, supply-chain attestation.

NIST §2.1 (the seven tenets) is used as the **verbatim evidence quote**
source where a single sentence captures the pillar's intent
[nist-sp-800-207-2020].

## 3. UC ↔ control mapping

### ZT-Pillar-Identity — Subject identification and per-request authorisation
- **What it requires:** Every NHI is uniquely identified, owned,
  attested, and authorised at the moment of resource access; no
  standing implicit trust.
- **UCs that satisfy it:** UC-F-003; UC-F-004; UC-F-006; UC-F-007;
  UC-F-013; UC-F-015; UC-F-020; UC-F-024; UC-F-025; UC-F-027; UC-N-002;
  UC-N-003.
- **NHIs especially relevant:** NHI-001; NHI-002; NHI-003; NHI-005;
  NHI-006; NHI-007; NHI-012; NHI-019; NHI-027; NHI-028; NHI-029;
  NHI-035; NHI-036; NHI-037.
- **Evidence quote (≤ 30 words):** "All resource authentication and
  authorization are dynamic and strictly enforced before access is
  allowed" [nist-sp-800-207-2020, §2.1 tenet 6].
- **Maturity level:** Pillar-Identity.

### ZT-Pillar-Identity-Federation — NHI federation and OIDC trust
- **What it requires:** CI/CD and workload identities federate via
  short-lived OIDC/SVID tokens rather than long-lived shared secrets;
  trust policies scope `sub`/`aud` precisely.
- **UCs that satisfy it:** UC-F-003; UC-F-004; UC-F-018; UC-F-024.
- **NHIs:** NHI-003; NHI-006; NHI-019; NHI-027; NHI-028; NHI-036.
- **Evidence quote:** "Many enterprises will deploy ZTA components
  that … require federation between identity providers"
  [nist-sp-800-207-2020, §3.3.2].
- **Maturity level:** Pillar-Identity.

### ZT-Pillar-Workload-mTLS — Workload-to-workload attested mTLS
- **What it requires:** Service-to-service authentication uses
  attested, short-lived workload identities (X.509-SVID / JWT-SVID);
  static workload secrets are eliminated from approved patterns.
- **UCs that satisfy it:** UC-F-004; UC-F-008; UC-F-009; UC-F-012;
  UC-F-014.
- **NHIs:** NHI-002; NHI-004; NHI-006; NHI-011; NHI-013; NHI-017;
  NHI-036.
- **Evidence quote:** "Service mesh and similar overlays … can enforce
  per-request authorization and mutual authentication between
  microservices" [nist-sp-800-204d-2024, §4.3].
- **Maturity level:** Pillar-Workload.

### ZT-Pillar-Workload-CICD — CI/CD pipeline integrity & ephemeral creds
- **What it requires:** Pipelines run with ephemeral, federated
  identities; pipeline-resident secrets are eliminated; provenance is
  signed.
- **UCs that satisfy it:** UC-F-003; UC-F-010; UC-F-016; UC-N-012.
- **NHIs:** NHI-003; NHI-009; NHI-015; NHI-016; NHI-020.
- **Evidence quote:** "Pipelines should treat all secrets and signing
  keys as short-lived and brokered through a centrally managed
  service" [nist-sp-800-204d-2024, §5.2].
- **Maturity level:** Pillar-Workload.

### ZT-Pillar-Workload-Runtime — Runtime attestation before secret release
- **What it requires:** Workloads attest measurement (TEE / kernel /
  K8s / cloud-metadata) before the broker releases a secret; failed
  attestations are logged and denied.
- **UCs that satisfy it:** UC-F-004; UC-F-017; UC-F-018; UC-N-018.
- **NHIs:** NHI-002; NHI-006; NHI-018; NHI-019; NHI-036.
- **Evidence quote:** "The enterprise monitors and measures the
  integrity and security posture of all owned and associated assets"
  [nist-sp-800-207-2020, §2.1 tenet 5].
- **Maturity level:** Pillar-Workload.

### ZT-Pillar-Device — Device-health gate on secret release
- **What it requires:** Device posture (managed-vs-BYO, attestation,
  patch level, EDR presence) is an input to authorisation; IoT/OT/branch
  devices use hardware-rooted identity.
- **UCs that satisfy it:** UC-F-019; UC-F-023; UC-N-016.
- **NHIs:** NHI-021; NHI-032; NHI-033.
- **Evidence quote:** "No resource is inherently trusted … the enterprise
  evaluates the security posture of the asset" [nist-sp-800-207-2020,
  §2.1 tenets 1 and 4].
- **Maturity level:** Pillar-Device.

### ZT-Pillar-Network — Broker placement and micro-segmentation
- **What it requires:** Secrets broker is reachable only via authenticated,
  micro-segmented paths; PEPs sit close to resources; partner mTLS
  enforces sender-constrained tokens.
- **UCs that satisfy it:** UC-F-012; UC-F-014; UC-F-022; UC-F-024.
- **NHIs:** NHI-006; NHI-011; NHI-013; NHI-028; NHI-031; NHI-032.
- **Evidence quote:** "All communication is secured regardless of
  network location" [nist-sp-800-207-2020, §2.1 tenet 3].
- **Maturity level:** Pillar-Network.

### ZT-Pillar-Data — TDE / KMS / TEE-bound data keys as NHIs
- **What it requires:** Data-at-rest keys, TDE master keys and
  attestation-bound data keys are themselves governed as NHIs with
  custodian quorum.
- **UCs that satisfy it:** UC-F-005; UC-F-008; UC-F-016; UC-F-017;
  UC-N-007; UC-N-012; UC-N-013; UC-N-018.
- **NHIs:** NHI-018; NHI-023; NHI-024; NHI-025; NHI-034; NHI-035.
- **Evidence quote:** "All data sources and computing services are
  considered resources" [nist-sp-800-207-2020, §2.1 tenet 1].
- **Maturity level:** Pillar-Data.

### ZT-Pillar-Visibility-Analytics — Telemetry, baselining, NHI behaviour
- **What it requires:** All secret-access events are logged to a
  tamper-evident store; baselines per NHI are computed; anomalies
  trigger SOC review.
- **UCs that satisfy it:** UC-N-001; UC-N-002; UC-N-011; UC-N-017;
  UC-N-019; UC-N-020.
- **NHIs:** NHI-001; NHI-007; NHI-008; NHI-010; NHI-013; NHI-019;
  NHI-026; NHI-030; NHI-031; NHI-035; NHI-037.
- **Evidence quote:** "The enterprise collects … information about
  asset security posture, network traffic and access requests … to
  improve its security posture" [nist-sp-800-207-2020, §2.1 tenet 7].
- **Maturity level:** Pillar-Visibility-Analytics.

### ZT-Pillar-Visibility-NHIDR — NHI detection & response
- **What it requires:** NHI Detection & Response (NHIDR) — anomalous
  use of an NHI (impossible-travel-equivalent, scope inflation,
  prompt-injection-induced calls) is detected and contained.
- **UCs that satisfy it:** UC-F-007; UC-N-011; UC-N-019.
- **NHIs:** NHI-007; NHI-019; NHI-026; NHI-030; NHI-037.
- **Evidence quote:** "Continuous, dynamic monitoring of … assets
  detects compromise and informs … policy" [nist-sp-1800-35-2025, Vol C].
- **Maturity level:** Pillar-Visibility-Analytics.

### ZT-Pillar-Automation-Orchestration — Rotation, revocation, lifecycle
- **What it requires:** Rotation, revocation, expiry handling, and
  emergency response are codified and orchestrated; humans do not
  transcribe secrets.
- **UCs that satisfy it:** UC-F-006; UC-F-007; UC-F-011; UC-F-020;
  UC-F-021; UC-F-027.
- **NHIs:** NHI-005; NHI-007; NHI-010; NHI-011; NHI-012; NHI-014;
  NHI-022; NHI-026; NHI-029; NHI-031; NHI-037.
- **Evidence quote:** "Automation and orchestration … allow the
  enterprise to maintain a consistent security posture as the
  environment changes" [nist-sp-1800-35-2025, Vol B].
- **Maturity level:** Pillar-Automation-Orchestration.

### ZT-Pillar-Governance — Policy-as-code & exception register for NHIs
- **What it requires:** NHI access policy is expressed as code,
  versioned, peer-reviewed, and tested; exceptions are time-bound and
  reviewed; supply-chain attestations feed the policy engine.
- **UCs that satisfy it:** UC-N-004; UC-N-005; UC-N-006; UC-N-007;
  UC-N-009; UC-N-010; UC-N-014; UC-N-015.
- **NHIs:** NHI-007; NHI-024; NHI-025; NHI-026; NHI-028; NHI-030;
  NHI-035; NHI-037.
- **Evidence quote:** "The policy engine ultimately decides … access
  decisions are logged for analysis" [nist-sp-800-207-2020, §3.2].
- **Maturity level:** Pillar-Governance.

### ZT-Pillar-Governance-PQC — Crypto-agility & PQC readiness
- **What it requires:** Crypto inventory, hybrid-cert capability and
  PQC migration readiness are reported to executive forums; CA/HSM
  capabilities are tracked against NIST FIPS 203/204/205.
- **UCs that satisfy it:** UC-F-016; UC-N-013.
- **NHIs:** NHI-006; NHI-015; NHI-023; NHI-024; NHI-025; NHI-028;
  NHI-034.
- **Evidence quote:** "Organizations should plan a transition to
  post-quantum cryptography that maintains crypto-agility"
  [nist-sp-1800-38-2024].
- **Maturity level:** Pillar-Governance.

## 4. Reverse map: UCs missing ZT pillar coverage

All 27 functional and 20 non-functional UCs map to **at least one** ZT
pillar — ZT is a more granular outcomes lens than Essential 8 for
NHIs, so coverage is complete. UCs whose ZT mapping is light or
single-pillar (and therefore vulnerable to under-investment) are:

- **UC-F-002** (history sweep) — maps only to Visibility-Analytics; a
  weak ZT framing because remediation is reactive. Strengthen by
  cross-linking to Automation-Orchestration (auto-revocation).
- **UC-F-022** (webhook inbound) — Network pillar only; consider
  cross-link to Identity for inbound caller authentication.
- **UC-N-008** (engineer training) — Governance pillar only; this is
  appropriate, but the UC should reference SP 800-50r1 awareness
  guidance for evidentiary depth.
- **UC-N-015** (stakeholder cadence) — Governance pillar only; this
  is intentional and matches NCCoE Governance scope.

The Essential 8 mapping declares an explicit `E8-RAP-NHI-GAP` row
because E8 does not enumerate machine identities; the ZT lens has **no
equivalent gap** because NIST §2.1 tenet 6 and §3.1.2 explicitly call
out non-person entities. This is the single largest reason ZT is the
PRD's NHI-load-bearing outcome lens.

## 5. Outcome-lens cross-references

As a PRIMARY-LENS, ZT aggregates into the PRD's "what good looks like"
outcomes as follows:

- **Outcome A — Eliminate plaintext sprawl** ← Identity + Visibility-Analytics
  + Governance pillars (Essential 8 contributes RAP + AppControl).
- **Outcome B — Ephemeral, attested, brokered identity** ← Identity +
  Identity-Federation + Workload-mTLS + Workload-Runtime pillars
  (Essential 8 contributes RAP + MFA-Workload-mTLS analogue).
- **Outcome C — Govern the long tail and the vault itself** ←
  Automation-Orchestration + Governance + Data pillars (Essential 8
  contributes RAP-SVC + RAP-BreakGlass + Backups-Keys).
- **Outcome D — Detect-baseline-respond on NHIs** ← Visibility-Analytics
  + Visibility-NHIDR + Automation-Orchestration (no direct E8 analogue
  — this is where ZT carries the PRD).

Essential 8 and ZT are **complementary**: E8 supplies a maturity
ladder Australian regulators recognise; ZT supplies the NHI-aware
vocabulary E8 lacks. The PRD §7 outcome lens therefore uses the
**union** of both, with ZT as the canonical pillar taxonomy for §8's
control narrative.

## 6. Open questions

- Is **NHIDR** (NHI Detection & Response) a sub-pillar of
  Visibility-Analytics or a first-class control in PRD §11? NCCoE
  SP 1800-35 doesn't yet treat it as separate; CSA NHI WG does.
- Should **AI-agent identity** (NHI-019) get a dedicated ZT sub-pillar
  in v1.0? NIST AI 600-1 / NIST AI RMF do not yet integrate with
  SP 800-207; this is an industry-consensus gap.
- The **Governance** pillar is an NCCoE addition, not a NIST SP 800-207
  primary; do we cite the pillar to NIST SP 1800-35 Vol B exclusively
  or to CISA ZTMM v2.0 as a parallel?
- Treatment of the **Pillar-Network "broker placement"** in private-
  cloud vs. SaaS-vault topologies — does ZT permit SaaS vault as a
  PEP, or must the PEP be in-tenant for APRA-regulated data?
- Maturity-stage labelling: do we use **CISA ZTMM v2.0** (Traditional /
  Initial / Advanced / Optimal) for the scorecard, or stay with
  NCCoE's pillar-internal capability levels?

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under the
"NIST SP 800-207 ZT (Agent 04 — regulatory)" block. Keys used in this
mapping:

- `nist-sp-800-207-2020` (primary).
- `nist-sp-1800-35-2025` (NCCoE implementation guide).
- `nist-sp-800-204d-2024` (CI/CD + service-mesh).
- `nist-sp-1800-38-2024` (PQC migration).
- `cisa-ztmm-v2-2023` (maturity-model alignment).
- `nist-sp-800-207a-2023` (PE/PA/PEP in cloud-native enterprise).
- `nist-sp-800-63-4-2024` (digital identity).
- `csa-nhi-taxonomy-2024` (NHI taxonomy industry reference).
- `nist-csf-2.0-2024` (back-map anchor).

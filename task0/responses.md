# Task 0 — Responses (live capture)

> **Session:** live interactive (1-hour sweep).
> **Convention:** answers tagged inline with `[PUBLIC] / [INTERNAL] /
> [SENSITIVE] / [NOT-FOR-DISTRIBUTION]` (default `[INTERNAL]` if unstated).
> Unanswered = `(skipped — will surface as PRD §17 open question)`.

---

## Section A — Project context & stakeholders

### Q-A.01 — Primary stakeholder `[INTERNAL]`
**Compound primary stakeholder:** Head of IAM / Identity & Access **AND** Head of Platform Security / Cloud Security / DevSecOps. PRD must serve both lenses (NHI lifecycle + workload-identity outcomes for IAM; developer experience + control automation for Platform Sec).

### Q-A.02 — Secondary readers `[INTERNAL]`
- Internal: board sub-committee, internal audit, other engineering leaders.
- Vendor SEs (for RFP / RFI consumption) — implies PRD content must be reusable as RFP source; no internal-only narrative blocks.
- Distribution unknown for some downstream readers — default to internal-only sensitivity until confirmed.

### Q-A.03 — Distribution surface `[INTERNAL]`
**Internal to XYZ only** (current intent). Loose sensitivity policy applies for now — internal observations stay with light anonymisation. ADR-005 enforcement at "internal-only" level.

### Q-A.04 — Decision the report supports `[INTERNAL]`
**ALL FOUR** decision drivers in scope:
1. Re-validate XYZ's existing secrets-management choice (Vault Enterprise).
2. Identify gaps in current deployment for remediation.
3. Build buyer's framework for future selection / re-platform.
4. Audit defence vs APRA + ASD ISM + Essential 8 + NIST CSF.

> Implication: PRD §11 (vendor findings), §12 (XYZ findings), §14 (regulatory traceability), and §16 (recommendations) are all primary-value sections — not deferrable.

### Q-A.05 — FI 27 strategy preview `[INTERNAL]`
FI 27 has two intertwined themes:
1. **Cloud-native + Zero Trust + workload identity (SPIFFE/OIDC)** — push toward attested ephemeral identity, away from long-lived static secrets.
2. **Re-platform / consolidation** — rationalise secrets-management onto a smaller stack; fewer vaults, fewer integrations, clearer ownership.

> Implication: PRD §16 FI 27 alignment subsection should explicitly evaluate each vendor against (a) workload-identity maturity (SPIFFE/OIDC support, short-lived creds, ephemeral attestation) and (b) consolidation potential (breadth of native NHI coverage vs needing add-ons / partners).

---

## Section B — XYZ organisational context

### Q-B.01 — Public anchors we can cite `[PUBLIC]` + `[INTERNAL]`
Public anchors exist across three categories:
- HashiCorp / vendor case study referencing XYZ.
- Public conference talks (KubeCon AU / RSA APAC / HashiConf / AWS re:Invent / etc.).
- Public APRA notices / regulatory commentary on XYZ.

User cannot name specific URLs right now → **default to anonymised** in PRD body; M2 vendor researchers may surface citable URLs via web search and re-tag them `[PUBLIC]` with the user's confirmation at the M2 gate.

### Q-B.02 — Scale orientation `[INTERNAL]`
Tier-1 AU FI footprint:
- **Hundreds of dev teams.**
- **Multi-cloud across all three hyperscalers** (AWS + Azure + GCP).
- **Kubernetes-heavy** production footprint.
- **Mainframe still material** — embedded creds at non-trivial scale.

> Implication: NHI coverage must explicitly handle mainframe (NHI-022, NHI-027 from the taxonomy) and AI/ML serving (NHI-018, NHI-019) alongside the conventional cloud/K8s rows.

### Q-B.03 — Regulatory pressure observed `[INTERNAL]`
Most-cited in conversations during engagements:
- **APRA bundle: CPS 234 + CPS 230 + CPG 235** (information security + operational risk + data risk).
- **ASD Essential 8 maturity + ASD ISM.**
- **PCI-DSS + SOX + OAIC Privacy Act.**
- _NIST CSF / 800-series NOT specifically cited in conversations — supports our outcomes-first lens choice (use NIST as back-map, not primary). ADR-003 holds._

---

## Section C — XYZ identity inventory observed (NHI scope) `[INTERNAL]`

### C.00 — Headline finding (drives PRD §12, surfaces as P0 UC-N gap)

**Vault Enterprise at XYZ governs only the authentication methods and
secret engines that have been wired up.** There is **no NHI
inventory / discovery layer** above Vault. The organisation **does
not have a clear picture of how many machine identities actually exist**.

> Implication: this is the dominant non-functional gap. It maps directly
> to UC-N-001 (sprawl KPI dashboard), UC-N-005-class (inventory of
> orphaned / unused secrets), UC-N-008-class (secret usage analytics).
> XYZ current-state for those rows will be **GAP / HIGH confidence**.

### C.01 — Workload + Cloud IAM cluster

- **Cloud IAM (AWS) + EC2 instance metadata auth** — **ENABLED / governed
  by Vault Enterprise** (`MET` for UCs that depend on AWS IAM dynamic creds).
- Azure managed identity + GCP service account governance via Vault — _to
  confirm; likely partial_.
- Kubernetes ServiceAccount auth method — _to confirm; likely enabled at
  least for some clusters given multi-cloud + K8s-heavy footprint_.
- CI/CD pipeline identities (NHI-003) — _captured under §C.04 below_.

### C.02 — Database / OS service-account cluster

- **Vault database secrets engine is ENABLED but adoption is effectively
  zero — "no one is actually using it"**.
- AD service accounts (initially rotated by Vault) were handed back to
  **CyberArk PAM** (see §I.03 vendor decision below).
- Implication: XYZ current-state for DB-dynamic-creds UCs is
  **PARTIAL** — capability exists, control objective not met. Classic
  "shelf-ware" pattern.

### C.03 — PKI / Cryptographic identity cluster

- **Not governed by Vault.** Conventional TLS / mTLS / SSH / code-signing
  identity lifecycle is not managed through Vault's PKI / SSH engines.
- **EXCEPTION:** an "advanced cryptographic platform" exists that **uses
  HashiCorp Vault Enterprise (Transform / FPE engine) for credit-card
  tokenization** (PCI-DSS cardholder data scope). This is a narrow,
  vertical use — not general PKI governance.
- Implication: PKI-related UCs are largely **GAP**. Tokenization for PCI
  is a **MET** in a narrow lane. Surfaces as a finding in PRD §12.

### C.04 — DevOps + supply-chain cluster

- **Managed via Vault, but inconsistent adoption.** Not all engineering
  teams follow best practices. **No clear visibility on how many machine
  identities are present** across the pipeline / GitOps / IaC stack.
- Implication: **PARTIAL** for the cluster. Adoption + observability gap.

### C.05 — Mainframe / legacy

Tier-1 bank with mainframe still material (per §B.02). _Coverage pending
explicit confirmation — almost certainly **OUT OF VAULT SCOPE**, likely
RACF/Top Secret/ACF2 internal governance with no central NHI catalog._

### C.06 — RPA / AI agents

_Pending — high likelihood of being shadow / ungoverned given the
headline finding._

### C.07 — IoT / OT

_Pending — likely out of secrets-management scope; possibly governed
through device-management platform._

### C.08 — B2B / partner (Open Banking AU / SWIFT / NPP)

_Pending — typically PAM-style or bespoke vault; not the primary Vault
Enterprise lane._

### C.09 — Tooling identities (monitoring, SIEM/SOAR, ITSM, backup, network, browser ext)

_Pending — typically shadow; long tail of accounts._

---

## Section D — XYZ secrets-management stack (current state)

### Q-D.01 — Primary platform(s) `[INTERNAL]`
**Multi-vendor stack confirmed:**
- **HashiCorp Vault Enterprise** — primary; auth methods + secret engines + Transform/FPE for PCI tokenization.
- **CyberArk PAM** — owns AD service-account rotation (after initial Vault attempt was rolled back, see Q-I.03 below).
- **Vault-based "advanced cryptographic platform"** — narrow PCI-tokenization deployment leveraging Vault Transform engine.
- Cloud-native vaults (AWS Secrets Manager / Azure Key Vault / GCP Secret Manager) — _coverage to confirm; given multi-cloud footprint likely present at least for cloud-native workloads_.

### Q-D.02 — Coverage by NHI type `[INTERNAL]`
See Section C above. Headline: **patchwork — engines wired, but adoption
inconsistent and no inventory layer above Vault**.

### Q-D.03 — Auth methods enabled in Vault Enterprise `[INTERNAL]`
**Enabled at XYZ:**
- AppRole.
- Kubernetes auth method.
- AWS IAM auth method.
- AWS EC2 auth method.
- OIDC.
- JWT.
- LDAP.
- GCP IAM auth method.
- Token (static, for legacy / break-glass).

**Notable absences (worth flagging in PRD §12):**
- **No Azure AD / Entra auth method** enabled — yet §B.02 confirms Azure
  is one of three hyperscaler clouds in use. Implies Azure workloads
  authenticate to Vault via OIDC / JWT bridge or are out-of-Vault scope.
- **No TLS certificate auth method** enabled.
- **No PKI / SPIRE / workload-attestation auth method** enabled — this is
  a notable miss given the FI 27 SPIFFE / OIDC workload-identity ambition.

### Q-D.04 — HSM / Seal posture `[INTERNAL]`
- **Originally HSM-sealed via Thales SafeNet Luna** (transcribed as "Salt utility"; confirm at M2 review).
- **Migrated to Fortanix** (likely Fortanix DSM / Data Security Manager).
- Implication: HSM migration is recent and material. Likely affects the
  crypto-agility / PQC trajectory referenced in FI 27. PRD §12 to flag.

### Q-D.05 — DR / multi-region posture `[INTERNAL]`
**Topology:**
- **Master Vault cluster on-premise**, with **primary + DR** sites
  on-prem (Vault Enterprise **DR Replication** active-passive between
  the two on-prem sites).
- **Edge clusters in OpenShift, AWS, and GCP**, enabled with **Performance
  Replication** (read-scaling + low-latency local access).
- _No Azure edge cluster mentioned — consistent with no Azure auth method
  enabled (§Q-D.03)._

**Architecture note:** sophisticated multi-region topology — on-prem
primary+DR is the source of truth; PR clusters fan out to multi-cloud.
This is the canonical HashiCorp Vault Enterprise reference architecture.

### Q-D.06 — Secret rotation reality `[INTERNAL]`
- **DB dynamic credentials:** engine **enabled**, rotation reality
  **NO** — adoption is effectively zero. (→ PARTIAL with strong
  shelf-ware framing.)
- **PKI certificates:** **NOT managed by Vault at all.** Owned by a
  **dedicated SSL team**, presumed traditional cert ops (likely Venafi /
  Microsoft CA / DigiCert — to confirm at M2). Vault PKI engine off.
- **SSH OTPs / SSH CA signing:** **Vault SSH engine is OFF.**
  Implication: SSH access governance is out of Vault scope. Likely
  CyberArk PAM session broker + static SSH keys + ad-hoc.
- **Cloud IAM / STS:** **AWS only** (IAM auth + EC2 auth roles produce
  short-lived dynamic creds). Azure + GCP cloud-IAM rotation **NOT**
  via Vault dynamic engines.
- **AD service accounts:** **CyberArk-managed rotation** (per §Q-I.03).

> Aggregate implication: Vault is doing **dynamic-creds-for-AWS-only**
> + **PCI tokenization** + **secret KV storage** + **app-identity
> brokering via AppRole/OIDC/JWT**. The "dynamic credentials" promise
> is honoured only for AWS workloads. Everywhere else is static or
> external. This is a major finding for PRD §12.

---

## Section E — Control gaps observed at XYZ `[INTERNAL]`

### E.00 — Top observed control gaps (user-picked 8)

1. **Plaintext secrets in source code / CI logs / observability dashboards** — **dominant gap**, the one with the most lived-experience context. Maps directly to user-supplied seed UCs UC-F-001 + UC-N-001.
2. **Secret-scanning enforcement pre-merge** — gap present.
3. **JIT cloud / DB credentials** — confirmed shelf-ware DB engine; partial AWS-only JIT for cloud IAM.
4. **SSH-CA / OTP (Vault SSH engine OFF)** — gap; SSH access governance is external to Vault.
5. **Centralised + tamper-resistant audit log for every secret access** — gap (i.e., per-secret access logging may exist in Vault but not centralised tamper-resistant aggregation across vendors).
6. **Crypto-agility / PQC readiness** — gap; flagged in context of the SafeNet → Fortanix HSM migration.
7. **MTTR for an exposed secret** — gap; no measured rotation SLA.
8. **Orphaned / unused secrets inventory** — gap; aligns with the §C.00 headline finding (no NHI inventory layer).

User caveat: limited specific context behind 2–8; the **#1 gap is the
one with strongest lived-experience evidence**.

> Implication for PRD §12: gap #1 gets the most narrative weight, with
> citations to the user's red-team / engagement observations. Gaps 2–8
> get one-paragraph framings in PRD §12 + open-question entries in §17
> where evidence is thin.

### E.01 — Gaps NOT picked (treated as `MET` / `PARTIAL` / `N/A` until M2)

The user did **not** pick: mTLS/SPIFFE between services (#4),
cert-lifecycle automation (#5) — _but PKI is externally managed so this
should be marked `OUT-OF-VAULT-SCOPE`, not "Met"; M2 to clarify with the
SSL team's tooling_ —, break-glass governance (#8), AU sovereignty (#9),
vaultless detection (#11), secret usage analytics (#12), mainframe / RPA
/ AI / B2B / IoT-OT coverage (#15).

Status: tagged **PENDING** in `matrix/anz-current-state.csv` for those
rows; will surface as PRD §17 open questions.

---

## Section F — Red team findings (2019) and follow-ups

### Q-F.01 — Scope of the 2019 red team `[INTERNAL]`
- **Provider:** external consultancy (not named here — likely Big-4 / boutique; to confirm at M2 if needed).
- **Engagement length:** ~1 week.
- **Outcome (headline):** consultancy successfully **breached the CEO's email via phishing** and pivoted from there into **privileged access**.
- **Implicit scope:** end-to-end goal-oriented red team (no narrow technical scope); the privileged-access pivot suggests the brief allowed full enterprise traversal once initial access was obtained.

### Q-F.02 — Top findings related to secrets / NHIs `[INTERNAL]`
1. **Plaintext secrets visible on GitHub / code-management repositories.** _Surface area: developer-controlled repos; mitigation requires pre-merge scanning + push protection + historical sweep + rotation SLA._
2. **Privileged-access service accounts for UNIX / Linux had over-broad permissions** (a.k.a. **PA-SA scope sprawl**) — those SAs had **direct database access**, breaking blast-radius assumptions. _Surface area: privileged-access lifecycle ownership; mitigation requires JIT escalation + least-privilege baselines + access analytics._
3. Implied 3rd: the **CEO phishing → privileged-access pivot** itself, although that's a human-identity weakness as much as an NHI one — it amplifies the impact of the NHI findings because once you're privileged-as-CEO you can reach service accounts.

### Q-F.03 — Findings that drove the Vault Enterprise selection `[INTERNAL]`
Primary rationale: **Vault Enterprise was selected because it could
serve as a *centralised* secrets-management tool** — a single source of
truth and audit across heterogeneous workloads.

**Subsequent drift since 2020 (critical context for PRD §11 + §16):**
- With XYZ's adoption of **AWS and GCP from 2020 onwards**, Vault
  Enterprise effectively **became a *system of record*** rather than the
  primary day-to-day operational vault for cloud workloads.
- **Cloud-native vaults (AWS Secrets Manager, GCP Secret Manager, Azure
  Key Vault) became the de-facto choice** for cloud-specific use cases.
- Vault Enterprise is **now used only for very specific multi-cloud +
  on-prem use cases** — i.e., when an application team or a product
  needs the same secret accessible across multiple clouds AND on-prem,
  Vault is the broker. Otherwise teams reach for the cloud-native vault.

> Implication for PRD §16 recommendations: the FI 27 "consolidation"
> thesis has to reckon with this 6-year decentralisation drift.
> Recommending re-centralisation onto a single platform requires
> reversing a strong incumbent direction — needs a deliberate
> control-plane strategy (SPIFFE-based multi-vault, Vault as
> control-plane + cloud-native as data-plane, or vault-of-vaults
> overlay).

### Q-F.04 — Findings believed still open today (2026) `[INTERNAL]`
- **"Plaintext secrets in code repositories" — STILL OPEN.** Confirmed by §E.00 #1 (the dominant gap with strongest lived-experience evidence).
- **PA-SA over-permission for UNIX/Linux** — _status unclear_; the AD-joined slice is now under CyberArk PAM governance (per §Q-I.03), but non-AD UNIX/Linux SAs may remain a gap. Flag for PRD §17 open question.
- **The drift from "centralised Vault" to "cloud-native vaults dominant"** is itself a new open issue post-2019 that the original red-team didn't anticipate.

### Q-F.05 — Adversary TTPs observed or modelled `[INTERNAL]`
Implied from §F.01–F.02 narrative:
- **T1566 — Phishing** (initial access).
- **T1078 — Valid Accounts** (post-phish CEO account abuse).
- **T1552 family — Credentials in Files / Cloud Instance Metadata / Private Keys** (the "secrets in repos" findings).
- **T1098 — Account Manipulation** (over-permissioned PA-SA implies persistence / escalation via account modification).
- Possibly **T1556.006 — MFA-related bypass** if the CEO phish chained through SSO; to confirm.
- **T1199 — Trusted Relationship** (privileged SAs with cross-system access amplify lateral movement).

---

## Section G — Vendor deployment experience

### Q-G.01 — HashiCorp Vault Enterprise `[INTERNAL]`
**Biggest gripes:**
1. **Licensing model churn** — HashiCorp has changed the licensing model **2–3 times in the past 6 years**. The **current model treats Vault Enterprise as licensed in production AND non-production**. Most enterprises run non-prod for validation before promoting to prod, so this materially increases TCO. **This is a meaningful gripe to flag in PRD §11 (vendor findings)** and in PRD §16 recommendations when discussing consolidation feasibility.
2. **Plugin pain at enterprise scale** — plugins are numerous and have good online support, but **enterprise configuration / hardening of plugins is non-trivial**. (Likely includes namespace / mount-path coordination, ACL policy authoring, telemetry, upgrade compatibility.)

**Strengths (user-confirmed):**
- APIs are **fantastic**.
- Ease of access is **fantastic**.
- **Testing is easy** (clear non-prod story, good CI integration).
- **Stability is great**.

> Implication for PRD §11: Vault scores high on capability + DX + stability,
> with notable commercial-model concern + plugin-at-scale operational concern.

### Q-G.02 — CyberArk Conjur (and PAM context) `[INTERNAL]`
Last assessed by user in **2024**:
- Conjur is **not as good as Vault** (user's view).
- **API quality was appalling** — both PAM APIs and Conjur APIs reflected CyberArk's PAM-led API philosophy (not a modern REST/HCL ergonomic).
- **Community support is gated** by the CyberArk Partner Portal — a friction point that limits open knowledge-sharing and self-service troubleshooting.
- Likely improved by 2026 — **M2 vendor research must validate current state**, not rely on 2024 snapshot.

> Implication: PRD §11 to note "historical API + community concerns;
> M2 research to validate 2026 state." If CyberArk has materially
> improved the API surface and opened the community, that updates the
> scoring favourably.

### Q-G.03 — Delinea Secret Server `[INTERNAL]`
- User has **used it once or twice**.
- **UX is "seamless"** (comparable to Vault on that axis).
- BUT **not as mature as Vault** overall in user's opinion.
- Limited direct experience — M2 vendor research carries more weight here.

### Q-G.04 — Cloud-native vaults (AWS SM / Azure KV / GCP SM) `[INTERNAL]`
- User has **not worked extensively** with cloud-native secrets managers directly.
- **Observation**: at XYZ and other clients, **adoption by application teams of cloud-native secrets managers has been increasing** since 2020.
- **AWS and GCP have very large communities** — they're **evolving at a fast pace** comparable to HashiCorp Vault.
- _XYZ-specific cloud-vault lean: not explicitly stated; given AWS auth method depth in §D.03, AWS Secrets Manager is likely the most-used cloud-native vault at XYZ; Azure (no Vault auth method enabled) suggests Azure Key Vault picks up the Azure-side workloads as the only path._

> Implication: PRD §11 to credit cloud-native vaults for **velocity + community
> maturity**. PRD §12 (XYZ findings) to note that cloud-native vault adoption
> at XYZ is real and structural — the consolidation conversation must
> reckon with the strength of this trajectory.

### Q-G.05 — Emerging vaults (AKEYLESS / Doppler / Infisical / 1Password Secrets Auto) `[INTERNAL]`
- User's high-level view: **"great" — but DO NOT meet all enterprise use cases**, especially:
  - Multi-cloud,
  - Multi-region,
  - Multi-platform integrations and plugins.
- User explicitly **endorses the planned deep research** at M2 to validate this view against current 2026 capability.

> Implication: PRD §11 to handle the emerging-vault tier with explicit
> capability scoring (where they're strong: developer experience, modern
> APIs, opinionated workflows; where they thin out: enterprise multi-cloud
> / multi-region / regulated-deployment patterns).

### Q-G.06 — PKI / machine-identity platforms `[INTERNAL]`
**User's direct PKI-with-Vault experience (different client, not XYZ):**
- Worked at one FI-grade client with a **dedicated PKI plugin backend for HashiCorp Vault** (likely Vault PKI engine + signing intermediate).
- That implementation **worked seamlessly**.

**XYZ-specific PKI workflow (CORRECTS earlier characterisation):**
- XYZ has a **dedicated SSL team** that owns SSL/TLS cert lifecycle.
- The workflow:
  1. Application team submits a **ServiceNow request form** with cert details (CN / SANs / etc.).
  2. **ServiceNow integrates with Vault** (using **AppRole auth method**) to fetch **static secrets** required for cert generation.
  3. ServiceNow / SSL team generates the SSL certificate.
  4. Certificate is **emailed back** to the requesting team.
- **Issuance: supported.**
- **Revocation: status unclear** (user couldn't confirm).
- _So Vault IS involved in PKI at XYZ — as a static-secret backend for the SSL team's ServiceNow workflow — but the **cert lifecycle is owned outside Vault** by the SSL team's process. Vault PKI engine itself is **not** in active production use._

**Venafi / Keyfactor at XYZ:** **not confirmed by user.** The SSL team's
tooling beneath the ServiceNow workflow is unspecified. _M2 research to
probe whether XYZ uses Venafi / Keyfactor / Microsoft AD CS / DigiCert
CertCentral / etc._

> Implication for PRD §11 + §12: PKI is a **partial gap** — automated
> lifecycle (issuance + rotation + revocation + observability) is the
> opportunity; email-driven cert delivery is a 2025-vintage pattern
> worth modernising. PRD §16 to recommend SPIFFE / mTLS + ACME-driven
> automation as the FI 27 trajectory.

---

## Section H — Incidents

### Q-H.01 — Documented secrets-related incidents at XYZ `[INTERNAL]`
**User cannot share incident details at this time.** Treated as
`[NOT-FOR-DISTRIBUTION]` — not reproduced in any PRD output, not even
anonymised. Surfaces as PRD §17 open question for stakeholder discretion.

### Q-H.02 — Near-misses worth narrating `[NOT-FOR-DISTRIBUTION]`
Same as H.01 — withheld.

### Q-H.03 — Industry incidents to specifically address `[PUBLIC]`
User confirms: **yes, definitely address the default industry incident
catalog** in PRD §13/§14. Default set (per `prompts/05-adversary-ttp-mapper.md`):
Okta (Oct 2023, Jan 2022), Cloudflare (Nov 2023), CircleCI (Jan 2023),
Internet Archive (Oct 2024), Sourcegraph (Aug 2023), LastPass (Aug + Nov 2022),
xz-utils backdoor (Mar 2024), SolarWinds, Microsoft Storm-0558,
Uber 2022, Toyota source-leak, Sumo Logic (Nov 2023), MOVEit (2023),
Snowflake-related (2024).

No additional industry incidents requested beyond this default set.

---

## Section I — Prior decisions worth remembering

### Q-I.01 — Decisions XYZ has already made `[INTERNAL]`
- **Vault Enterprise selected (2019)** as the centralised secrets-management platform — driven by the red-team findings on plaintext-secrets-in-repos + over-permissioned PA-SAs.
- **Cloud-native vaults (AWS SM / GCP SM / Azure KV) adopted from ~2020 onwards** for cloud-specific workloads — effectively a strategic acceptance that Vault Enterprise would become a *system of record* rather than the primary cloud-workload vault.
- **CyberArk PAM retained for AD service-account governance** — attempted Vault migration was rolled back. CyberArk PAM is entrenched.
- **PCI cardholder-data tokenization** built on Vault Transform / FPE engine — narrow, specialised deployment of Vault for a regulated use case.
- **HSM migration from Thales SafeNet Luna → Fortanix** (likely Fortanix DSM) — recent.

> Implication: these decisions are durable. PRD §16 recommendations must
> assume the multi-vendor stack continues; the value-add of the
> universal framework is **what fills the gaps between** these vendors
> (NHI inventory, supply-chain signing, AI-agent identity, etc.).

### Q-I.02 — Decisions in flight that this report should inform `[INTERNAL]`
- **FI 27 strategy** itself — see §J. Cloud-native + ZT + workload identity + consolidation themes are open strategic decisions the report should illuminate.
- **NHI inventory / discovery layer** decision — gap surfaced in §C.00; resolving this is a P0 architectural decision the report should make recommendations on.
- **Whether to expand Vault PKI / SSH adoption** — currently off; FI 27 workload-identity ambition may force this question.
- **Whether to enable Azure auth method on Vault** — currently absent despite Azure being one of the three clouds.

### Q-I.03 — Procurement constraints / vendor exclusions `[INTERNAL]`
**CyberArk PAM is entrenched** for AD service-account governance. An
attempted migration of AD service accounts to Vault Enterprise was
rolled back — internal customer rationale: "we already use CyberArk PAM,
why would we manage our service accounts with Vault?" This is a hard
procurement / political constraint, not a technical capability gap on
either side.

> Implication: PRD §11 (vendor findings) and §16 (recommendations) must
> treat the **Vault + CyberArk coexistence** as a given. Recommendations
> that propose displacing CyberArk PAM will be DOA. Frame instead around
> "which vendor owns which NHI bucket" and "how to close the visibility
> gap above both vendors".

> Vendor list update: **CyberArk PAM joins the 12-vendor evaluation
> matrix** alongside CyberArk Conjur (they are distinct products with
> distinct architectures — PAM = Vaulted credentials + session brokering
> for human + AD service accounts; Conjur = secrets API for application
> identity). M2 vendor research will treat them as separate rows.

---

## Section J — FI 27 strategy

### Q-J.01 — What FI 27 expects from secrets-management `[INTERNAL]`
Per §A.05, FI 27 has two intertwined themes (cloud-native + ZT + workload
identity AND consolidation). Adding from this section:

- **Zero Trust is widely cited as strategy** at XYZ and other clients.
- **Zero Trust *workload identity* is a niche topic** that most people **do not understand well**. This is a real knowledge / framing gap — the report needs to demystify it (likely a sub-section in PRD §6 or §16).
- **There is a budget envelope for non-human identities** at XYZ — meaning NHI work is being funded, not just talked about.
- **Specific XYZ FI 27 detail / programme structure is unknown** to the user at the time of Task 0. PRD §16 FI 27 alignment subsection to be drafted at the **principle level** (workload identity + consolidation + AU sovereignty + crypto-agility) until XYZ-specific FI 27 detail is shared.

### Q-J.02 — Where FI 27 conflicts with anything in this PRD `[INTERNAL]`
- Potential conflict: the **2020-onwards drift to cloud-native vaults** (§F.03)
  may conflict with the **consolidation** theme in FI 27. If FI 27 wants
  fewer vaults, but XYZ has structurally favoured cloud-native vaults
  for cloud workloads, a re-consolidation push will encounter friction.
- Potential conflict: **CyberArk PAM entrenchment for AD SAs** (§I.03)
  conflicts with consolidation if FI 27 prefers a single vault.
- These conflicts become PRD §16 strategic recommendations rather than
  contradictions — the report's job is to make the trade-offs visible.

---

## Section K — Anything else `[INTERNAL]`

**Adoption-trajectory observation (carried into PRD):** the gap between
**Zero Trust as a stated strategy** and **Zero Trust workload identity as
a real operational practice** is wide industry-wide. Other clients of
the user are at the same place. PRD §16 should treat "demystify ZT
workload identity for FI-grade operators" as a first-class deliverable —
not just a recommendation but probably a short explainer in PRD §6 or §8.

**Funding signal:** budget envelope exists at XYZ for NHI work, which
means PRD recommendations are not aspirational — they can be sequenced
into a real programme. PRD §16 to produce a **prioritised numbered list
pinned to UC IDs**.

(No further open-mic content from user.)

---

## Live-session metadata

- Start time: 2026-05-22 (live).
- End time: 2026-05-22 (live, single session).
- Driver: Claude (orchestrator).
- Sections covered: A, B, C, D, E, F, G, H, I, J, K — **all 11 sections.**
- Sections with PENDING sub-fields: C.05 (mainframe), C.06 (RPA/AI), C.07 (IoT/OT), C.08 (B2B/partner), C.09 (tooling). These will surface as PRD §17 open questions and be confirmed at the M2 / M3 gates.
- Sensitivity audit:
  - `[PUBLIC]` content: parts of B.01 (public anchors exist but not URL-named).
  - `[INTERNAL]` (majority of content): paraphrased / anonymised for PRD use.
  - `[SENSITIVE]` content: none captured beyond H.
  - `[NOT-FOR-DISTRIBUTION]`: H.01 + H.02 (XYZ incident details withheld) — **not reproduced in any PRD output**.
- High-impact findings carried to PRD:
  1. **No NHI inventory / discovery layer** above Vault (§C.00).
  2. **Vault Enterprise became *system of record*** (not primary cloud-workload vault) post-2020 (§F.03).
  3. **Multi-vendor stack**: Vault Enterprise + CyberArk PAM + cloud-native vaults + Vault-Transform PCI tokenization (§D.01, §I.01).
  4. **HSM migration**: Thales SafeNet Luna → Fortanix (§D.04).
  5. **DB dynamic-creds engine = shelf-ware** (§C.02, §D.06).
  6. **No Azure auth method, no PKI/SPIRE auth method, no TLS-cert auth method** in Vault (§D.03).
  7. **SSL team uses Vault as static-secret backend via ServiceNow + AppRole** for cert generation; **lifecycle owned outside Vault**; revocation status unclear (§G.06).
  8. **Vault Enterprise licensing churn (non-prod also licensed)** is a material commercial concern (§G.01).
  9. **Plaintext secrets in repos** finding from 2019 red team **still open** today (§F.04).
  10. **ZT workload identity is widely cited as strategy but poorly understood operationally** — opportunity for PRD §16 to demystify (§J.01, §K).

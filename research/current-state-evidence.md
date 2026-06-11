# XYZ Current-State Evidence — Synthesis from Task 0

> **Source:** `task0/responses.md` (live session 2026-05-22).
> **Sensitivity policy (ADR-005):** `[PUBLIC]` content cited freely;
> `[INTERNAL]` content paraphrased / anonymised; `[SENSITIVE]` and
> `[NOT-FOR-DISTRIBUTION]` content not reproduced.
> **Scope:** captures the structured signal from Task 0 grouped by
> capability cluster. Companion CSV: `matrix/domains/secrets/current-state.csv` (47
> rows, one per UC).

---

## 0. Overview — XYZ current-state distribution

| Status | Count of UCs | Notes |
|---|---|---|
| MET | 0 | No UC is definitively MET — consistent with the headline finding (no inventory layer, so even working capabilities can't be quantified as MET) |
| PARTIAL | 16 | Capabilities exist but adoption is inconsistent / lacks observability / scoped narrowly |
| GAP | 11 | Material gaps with strong evidence — driven by the dominant XYZ findings |
| N/A | 0 | No UC is out-of-scope at XYZ |
| PENDING | 20 | Insufficient Task 0 signal to score; surfaces as PRD §17 open question |

The bias toward PARTIAL and PENDING reflects two realities:
(a) the lived-experience-vs-architecture gap (capabilities exist but
adoption / observability lags), and (b) Task 0 was a 1-hour pass — many
buckets need stakeholder-validated input for v1.0.

---

## 1. The dominant XYZ findings (cross-UC signals)

These are the 10 high-impact findings carried from `task0/responses.md`'s
live-session summary block. Each is referenced by the CSV cell that
matters most.

### 1.1 No NHI inventory / discovery layer above Vault `[INTERNAL]`

Vault Enterprise at XYZ governs only the authentication methods and
secret engines that have been wired up. There is **no NHI inventory /
discovery layer** above Vault. The organisation **does not have a clear
picture of how many machine identities actually exist**. (Q-C.00)

→ Dominant non-functional gap. Drives **UC-N-001, UC-N-002, UC-N-005,
UC-N-008 as GAP / HIGH confidence**.

### 1.2 Vault Enterprise became *system of record* post-2020 `[INTERNAL]`

XYZ adopted AWS and GCP cloud-native vaults from 2020 onwards. Vault
Enterprise effectively became a *system of record* rather than the
primary day-to-day operational vault for cloud workloads. Vault is now
used only for very specific multi-cloud + on-prem use cases. (Q-F.03)

→ Reframes the consolidation thesis in FI 27 (Q-A.05). PRD §16
recommendations must address this 6-year decentralisation drift
explicitly.

### 1.3 Multi-vendor stack confirmed `[INTERNAL]`

- HashiCorp Vault Enterprise — primary; auth methods + secret engines + Transform/FPE for PCI tokenization.
- CyberArk PAM — owns AD service-account rotation (after Vault attempt was rolled back).
- Vault-based "advanced cryptographic platform" — narrow PCI-tokenization deployment leveraging Vault Transform engine.
- Cloud-native vaults — AWS Secrets Manager / Azure Key Vault / GCP Secret Manager increasingly used by application teams since 2020. (Q-D.01, Q-G.04)

→ ADR-004 expanded matrix to include CyberArk PAM as a 13th vendor row
(separate from CyberArk Conjur), then to 19 with the NHI-discovery tier
+ Fortanix DSM.

### 1.4 HSM migration: Thales SafeNet Luna → Fortanix `[INTERNAL]`

Originally HSM-sealed via Thales SafeNet Luna; migrated to Fortanix
(likely Fortanix DSM / Data Security Manager). Recent and material.
(Q-D.04)

→ Fortanix DSM promoted from v1.0 to v0.1 scope (ADR-004 revision).
Drives **UC-F-016 PARTIAL** (HSM-sealed, awaiting runbook confirmation)
and **UC-N-013 PARTIAL** (PQC readiness signalled but not roadmapped).

### 1.5 DB dynamic-credentials engine = shelf-ware `[INTERNAL]`

Vault database secrets engine is enabled but adoption is effectively
zero — "no one is actually using it". (Q-C.02, Q-D.06)

→ Drives **UC-F-005 PARTIAL** with strong shelf-ware framing. Classic
"capability exists, control objective not met" pattern.

### 1.6 Absent auth methods in Vault `[INTERNAL]`

No Azure AD / Entra auth method enabled (despite Azure being one of the
three clouds). No TLS-cert auth method. No PKI / SPIRE workload-identity
auth method. (Q-D.03)

→ Drives **UC-F-003 PARTIAL (AWS-only JIT)**, **UC-F-004 GAP** (no
SPIFFE), and a notable finding in PRD §12 about workload-identity
ambition vs. operational reality.

### 1.7 PKI is partial — SSL team uses Vault via ServiceNow + AppRole `[INTERNAL]`

The dedicated SSL team manages SSL/TLS cert lifecycle. Workflow:
ServiceNow request → integrates with Vault (AppRole auth) → fetches
static secrets → generates SSL cert → emails to user. Issuance
supported; revocation status unclear. (Q-G.06)

→ Corrects the earlier "Vault not in PKI" framing. Drives **UC-F-007
PARTIAL** (issuance via shared workflow, lifecycle external to Vault) and
**UC-F-008 GAP / UC-F-009 PENDING**.

### 1.8 Vault Enterprise licensing churn = material commercial concern `[INTERNAL]`

HashiCorp has changed the licensing model 2–3 times in the past 6 years.
The current model treats Vault Enterprise as licensed in production AND
non-production. Most enterprises run non-prod for validation before
promoting to prod, so this materially increases TCO. (Q-G.01)

→ Drives **UC-N-006 PARTIAL** (vendor-risk concern) and PRD §11 + §16
findings on consolidation feasibility.

### 1.9 Plaintext secrets in repos — STILL OPEN from 2019 red team `[INTERNAL]`

The 2019 red-team finding that "secrets visible on GitHub / code
management repositories" remains the dominant gap at XYZ with strongest
lived-experience evidence. (Q-E.00 #1, Q-F.02, Q-F.04)

→ Drives **UC-F-001 GAP / HIGH confidence** and **UC-N-001 GAP / HIGH
confidence**. The user-supplied seed UCs are exactly the lanes where the
XYZ deployment has the most catching-up to do.

### 1.10 ZT workload identity widely cited as strategy, poorly understood operationally `[INTERNAL]`

ZT is widely cited as strategy at XYZ and other clients. ZT *workload
identity* is a niche topic that most people do not understand well.
There is a budget envelope for non-human identities at XYZ. (Q-J.01,
Q-K)

→ Drives **UC-F-004 GAP** (no SPIFFE), **UC-F-018 GAP** (AI agent
identity governance), **UC-N-019 GAP**. PRD §16 to treat "demystify ZT
workload identity" as a first-class deliverable.

---

## 2. The 2019 red team — adversary context `[INTERNAL]`

External consultancy, ~1 week engagement, achieved **CEO email breach
via phishing** then pivoted to privileged access. (Q-F.01)

Top NHI-related findings (Q-F.02):

1. **Plaintext secrets visible on GitHub / code-management repos** —
   the dominant finding. Still open today (Q-F.04).
2. **UNIX / Linux privileged-access service accounts had over-broad
   permissions** with direct database access — blast-radius violation
   (PA-SA scope sprawl). Status post-CyberArk-PAM unclear; AD slice now
   under PAM but non-AD UNIX/Linux unclear (Q-F.04, UC-F-014 PENDING).
3. **CEO phishing → privileged-access pivot** itself — human-identity
   weakness amplifying NHI impact.

TTPs exercised (Q-F.05): T1566 (Phishing) → T1078 (Valid Accounts) →
T1552-family (Credentials in Files / Cloud Instance Metadata / Private
Keys) → T1098 (Account Manipulation via over-permissioned PA-SA).
T1199 (Trusted Relationship) likely. T1556.006 if MFA bypass involved
(unconfirmed).

→ PRD §14 adversary context narrates this chain; matrix
`regulatory-trace.csv` already includes the MITRE T-codes as
`framework_role=ADVERSARY-LENS` rows.

---

## 3. Regulatory pressure at XYZ `[INTERNAL]`

Most-cited in engagement conversations (Q-B.03):

- **APRA bundle: CPS 234 + CPS 230 + CPG 234** (information security +
  operational risk + data risk).
- **ASD Essential 8 maturity + ASD ISM**.
- **PCI-DSS + SOX + OAIC Privacy Act** (downstream regulatory frames).
- _NIST CSF / 800-series NOT specifically cited in conversations —
  supports the outcomes-first lens choice in ADR-003._

→ PRD §14 leads with E8 + NIST ZT outcomes; back-maps to CPS 234 + ISM
in Appendix A (skipping CSF 2.0 per stakeholder direction for v0.1).

---

## 4. Architectural posture `[INTERNAL]`

### Multi-region topology (Q-D.05)

- Master Vault cluster **on-premise**, with primary + DR sites on-prem
  (Vault Enterprise DR Replication active-passive).
- **Edge clusters in OpenShift, AWS, and GCP**, enabled with **Performance
  Replication** (read-scaling + low-latency local access).
- _No Azure edge cluster — consistent with no Azure auth method enabled._

### Vault auth methods enabled (Q-D.03)

AppRole, Kubernetes, AWS IAM, AWS EC2, OIDC, JWT, LDAP, GCP IAM, Token.

### Scale (Q-B.02)

Hundreds of dev teams; multi-cloud across all three hyperscalers;
Kubernetes-heavy; mainframe still material.

→ Drives **UC-F-026 PARTIAL** (architecture documented; runbooks need
confirmation) and **UC-F-020 PENDING** (mainframe coverage).

---

## 5. FI 27 alignment hooks `[INTERNAL]`

FI 27 has two intertwined themes (Q-A.05):

1. **Cloud-native + Zero Trust + workload identity (SPIFFE/OIDC)** —
   attested ephemeral identity, away from long-lived static secrets.
2. **Re-platform / consolidation** — fewer vaults, fewer integrations,
   clearer ownership.

Potential conflicts with current state (Q-J.02):

- The 2020-onwards drift to cloud-native vaults conflicts with the
  consolidation theme.
- CyberArk PAM entrenchment for AD SAs conflicts with consolidation if
  FI 27 prefers a single vault.

→ PRD §16 reserves an FI 27 alignment subsection; recommendations
sequenced to:
(a) close NHI-inventory gap first (UC-N-001..005);
(b) demystify ZT workload identity (UC-F-004 + UC-N-019);
(c) consolidate via control-plane pattern, not vault displacement.

---

## 6. Sensitivity audit summary (ADR-005 enforcement)

| Sensitivity tag | Source coverage | Reproduced in PRD outputs? |
|---|---|---|
| `[PUBLIC]` | parts of §B.01 (public anchors exist but URLs not named) | YES — cite when M2 vendor researchers surface citable URLs |
| `[INTERNAL]` | majority of Task 0 responses | YES — paraphrased / anonymised as "observed at a major AU FI" |
| `[SENSITIVE]` | none observed in Task 0 | n/a |
| `[NOT-FOR-DISTRIBUTION]` | Q-H.01, Q-H.02 (XYZ incident details withheld) | **NO** — not reproduced in this file or anywhere else |

This file contains **no `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` content
verbatim**. The 10 high-impact findings are paraphrased from `[INTERNAL]`
content. Section 2 (red-team narrative) is `[INTERNAL]` paraphrased.

---

## 7. Open questions surfacing to PRD §17

- **O1.** Confirm primary stakeholder identity inside XYZ (Q-A.01: Head IAM + Head Platform Sec — both lenses).
- **O2.** Confirm distribution surface (Q-A.03: internal-only for now; vendor SE bound may follow).
- **O3.** Confirm any vendor procurement exclusions beyond the CyberArk-PAM-for-AD lock-in (Q-I.03).
- **O4.** Mainframe / RPA / AI / IoT-OT / B2B coverage — most marked PENDING.
- **O5.** SSH access governance posture (Vault SSH OFF — Q-D.06) — likely CyberArk PSM-brokered + static keys.
- **O6.** XYZ incident details withheld (Q-H.01 / Q-H.02) — request stakeholder authorisation for anonymised inclusion in v1.0 if it would sharpen §14.
- **O7.** FI 27 detailed programme structure / KPIs / timeline — full v1.0 alignment work.
- **O8.** Cert revocation workflow at SSL team (Q-G.06).
- **O9.** Fortanix DSM IRAP status confirmation (M2 research surfaced this as unconfirmed).
- **O10.** Confirm or reject the 2019 PA-SA over-permission finding's status today (Q-F.04).

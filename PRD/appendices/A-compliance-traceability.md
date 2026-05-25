# Appendix A — Compliance traceability

**Status:** v0.1 (Wave B — 2026-05-23).
**Parent document:** [`PRD-FI-v0.1.md`](../PRD-FI-v0.1.md) §14 + §19.
**Scope:** the full UC × framework cross-reference, joined from
[`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv) —
**145 control rows** (114 PRIMARY-LENS + BACK-MAP frames + 31
ADVERSARY-LENS rows enumerated in Appendix D). Frames follow
[ADR-003](../adrs/ADR-003-regulatory-lens.md): **E8 + CISA ZTMM v2.0
primary**; **CPS 234 + CPS 230 + CPG 234 + ASD ISM back-map**; **NIST
CSF 2.0 deferred to v1.0**.

> **Reading guide.** §A.2 carries the **PRIMARY-LENS** view per
> control code (E8 26 codes + ZTMM 13 pillar codes = 39 cells). §A.3
> carries the **BACK-MAP** view per Australian-regulator paragraph
> (APRA CPS 234 25 paragraph codes + CPS 230 6 paragraph codes + CPG
> 234 3 attachments + ASD ISM 41 controls = 75 cells). §A.4 cross-
> indexes the ADVERSARY-LENS rows from Appendix D (16 TTPs + 15
> breaches). §A.5 reverse-maps UC coverage and flags any UC missing
> PRIMARY-LENS coverage. §A.6 carries the NIST CSF 2.0 deferral note.

---

## A.1 Methodology

Per [ADR-003](../adrs/ADR-003-regulatory-lens.md), regulatory
intersections were enumerated **outcome-first**: every UC in
[`research/use-cases.md`](../../research/use-cases.md) was tagged
against (a) one or more **PRIMARY-LENS** control codes — the FI's
forward-looking maturity narrative (E8 + CISA ZTMM v2.0) — and (b) one or
more **BACK-MAP** controls — the Australian regulator narrative
(APRA CPS 234 + CPS 230 + CPG 234 + ASD ISM). The mapping is **many-
to-many in both directions**: a single UC typically resolves to
3–8 control cells across both frames; a single control typically
covers 4–10 UCs. The join lives in
[`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv) —
**145 rows × 10 columns** (`framework_slug, framework_role,
control_code, control_short_title, uc_ids, nhi_ids, maturity_level,
evidence_url, evidence_quote, citation_keys`). The CSV is the
authoritative source; the tables below are a compressed reading view.

Per [ADR-005](../adrs/ADR-005-anz-evidence-policy.md), all rows are
`[PUBLIC]` (regulator publications + NIST + MITRE primary URLs);
no `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` content appears.

NIST CSF 2.0 mapping is **deferred to v1.0** per the stakeholder-
accepted M2 gate decision (PRD §17 O8 + [ADR-003](../adrs/ADR-003-regulatory-lens.md)).
The 47 UCs were authored with `CSF-*` references for forward
compatibility; those tags remain in
[`research/use-cases.md`](../../research/use-cases.md) but are not
materialised in §A.2 / §A.3.

---

## A.2 PRIMARY-LENS controls — E8 + CISA ZTMM v2.0 (aligned to NIST SP 800-207)

PRIMARY-LENS = the **forward-looking outcomes narrative**. Each row
joins one control code to the UCs and NHIs it governs. The
`maturity_level` column is taken from the CSV (E8 ML1/ML2/ML3 where
applicable; "Pillar-*" for ZT pillars).

### A.2.1 Essential 8 (E8) — 26 control codes

> Sources: ACSC Essential Eight — <https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight>
> + Essential Eight Maturity Model — <https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model>.

| Code | Title | ML | UCs | NHIs |
|---|---|---|---|---|
| E8-RAP-ML1 | Restrict admin privileges — least-privilege baseline | ML1 | UC-F-003; UC-F-005; UC-F-013; UC-F-021; UC-N-002; UC-N-009; UC-N-010 | NHI-001; NHI-005; NHI-012; NHI-024; NHI-026; NHI-029; NHI-035 |
| E8-RAP-ML2 | Restrict admin privileges — separation + JIT | ML2 | UC-F-003; UC-F-005; UC-F-006; UC-F-007; UC-F-013; UC-F-015; UC-F-020; UC-F-021; UC-F-026; UC-N-002; UC-N-009; UC-N-010 | NHI-001; NHI-005; NHI-012; NHI-014; NHI-022; NHI-024; NHI-026; NHI-029; NHI-035 |
| E8-RAP-ML3 | Restrict admin privileges — SAWs + JIT | ML3 | UC-F-003; UC-F-007; UC-F-016; UC-F-020; UC-F-021; UC-F-026; UC-F-027; UC-N-009; UC-N-010; UC-N-011 | NHI-001; NHI-012; NHI-022; NHI-024; NHI-025; NHI-026; NHI-035; NHI-037 |
| E8-RAP-SVC | Restrict admin privileges — service-account credential hygiene | — | UC-F-006; UC-F-013; UC-F-020; UC-F-023; UC-F-026; UC-F-027; UC-N-002; UC-N-003; UC-N-009 | NHI-001; NHI-005; NHI-007; NHI-012; NHI-022; NHI-026; NHI-029; NHI-032; NHI-035; NHI-037 |
| E8-RAP-BREAKGLASS | Restrict admin privileges — break-glass account management | — | UC-F-007; UC-F-026; UC-N-009; UC-N-010 | NHI-024; NHI-025; NHI-026; NHI-035 |
| E8-RAP-LOG | Restrict admin privileges — central event logging | — | UC-F-007; UC-N-001; UC-N-011; UC-N-017; UC-N-019 | NHI-001; NHI-024; NHI-035; NHI-037 |
| E8-MFA-ML1 | MFA — internet-facing & online services | ML1 | UC-F-003; UC-F-015; UC-F-024; UC-F-025 | NHI-003; NHI-007; NHI-014; NHI-028; NHI-030 |
| E8-MFA-ML2 | MFA — privileged users + workload mTLS analogue | ML2 | UC-F-003; UC-F-004; UC-F-006; UC-F-013; UC-F-014; UC-F-015; UC-F-024; UC-F-026 | NHI-001; NHI-006; NHI-012; NHI-013; NHI-024; NHI-028; NHI-029; NHI-036 |
| E8-MFA-ML3 | MFA — phishing-resistant for high-value access | ML3 | UC-F-004; UC-F-007; UC-F-017; UC-F-018; UC-F-024; UC-F-026; UC-N-010 | NHI-006; NHI-018; NHI-019; NHI-024; NHI-028; NHI-035; NHI-036 |
| E8-MFA-WORKLOAD | MFA — machine-to-machine analogue (mTLS + attestation) | — | UC-F-003; UC-F-004; UC-F-014; UC-F-017; UC-F-018; UC-F-019; UC-F-024; UC-F-026 | NHI-002; NHI-006; NHI-017; NHI-018; NHI-021; NHI-028; NHI-036 |
| E8-AC-ML1 | Application control — executable allow-listing | ML1 | UC-F-001; UC-F-008; UC-F-009; UC-F-010; UC-F-016 | NHI-002; NHI-003; NHI-004; NHI-008; NHI-015; NHI-016 |
| E8-AC-ML2 | Application control — Microsoft blocklist + logging | ML2 | UC-F-016; UC-N-001; UC-N-011; UC-N-012 | NHI-015; NHI-016; NHI-020 |
| E8-AC-ML3 | Application control — signed admission + driver blocklist | ML3 | UC-F-008; UC-F-016; UC-N-012 | NHI-015; NHI-016; NHI-018; NHI-020; NHI-034 |
| E8-PA-ML1 | Patch applications — internet-facing (2 wk / 48 h) | ML1 | UC-N-001; UC-N-004; UC-N-011 | NHI-010; NHI-013; NHI-024; NHI-025; NHI-035 |
| E8-PA-ML2 | Patch applications — critical 48 h SLA on vault platform | ML2 | UC-F-026; UC-N-001; UC-N-004; UC-N-011 | NHI-010; NHI-013; NHI-024; NHI-025; NHI-035 |
| E8-POS-ML1 | Patch OS — vault/HSM/CA OS hygiene | ML1 | UC-F-026; UC-N-004; UC-N-011 | NHI-021; NHI-022; NHI-024; NHI-025; NHI-032; NHI-033; NHI-035 |
| E8-POS-ML2 | Patch OS — critical 48 h on internet-facing components | ML2 | UC-F-026; UC-N-004; UC-N-011 | NHI-013; NHI-024; NHI-025; NHI-032; NHI-035 |
| E8-POS-FIRMWARE | Patch OS — HSM / appliance firmware | — | UC-F-026; UC-N-004; UC-N-010; UC-N-013 | NHI-021; NHI-023; NHI-024; NHI-025; NHI-035 |
| E8-UAH | User application hardening | — | UC-F-001; UC-F-002; UC-N-008 | NHI-008 |
| E8-MAC | Restrict Microsoft Office macros | — | (no direct UC) | (no direct NHI) |
| E8-RB-ML1 | Regular backups — frequency + retention | ML1 | UC-F-021; UC-N-001; UC-N-003; UC-N-004 | NHI-023; NHI-024; NHI-026; NHI-035 |
| E8-RB-ML2 | Regular backups — backup-administrator separation | ML2 | UC-F-021; UC-N-003; UC-N-009; UC-N-010 | NHI-012; NHI-024; NHI-026; NHI-029; NHI-035 |
| E8-RB-ML3 | Regular backups — immutability + break-glass-only modification | ML3 | UC-F-021; UC-N-004; UC-N-010 | NHI-023; NHI-024; NHI-026; NHI-035 |
| E8-RB-KEYS | Regular backups — HSM/KMS key backup custody | — | UC-N-004; UC-N-007; UC-N-010; UC-N-013 | NHI-023; NHI-024; NHI-025; NHI-035 |
| E8-MATURITY-SCORECARD | Outcome scorecard — programme maturity reporting | — | UC-N-001; UC-N-003; UC-N-005; UC-N-009; UC-N-011; UC-N-014; UC-N-015; UC-N-020 | NHI-001; NHI-006; NHI-012; NHI-019; NHI-022; NHI-026; NHI-034; NHI-035; NHI-037 |
| E8-RAP-NHI-GAP | RAP — NHI-specific gap (no E8 dedicated NHI control) | — | (gap-flag row — see §A.5) | NHI-002; NHI-016; NHI-031; NHI-033; NHI-034 |

**Density read.** RAP (Restrict Admin Privileges) carries the heaviest
density (6 control codes, every UC cluster), followed by MFA (4),
Application Control (3), Patch (5) and Regular Backups (4). The
**E8-RAP-NHI-GAP** row is the deliberate flag that E8 itself has no
dedicated NHI control for NHI-002 / 016 / 031 / 033 / 034 — those
NHIs are governed in this PRD via ZT pillars (§A.2.2) and ISM
controls (§A.3.4). PRD §16 R6 (demystify ZT workload identity)
addresses this gap directly.

### A.2.2 CISA Zero Trust Maturity Model v2.0 — 13 pillar codes (aligned to NIST SP 800-207)

> Sources: NIST SP 800-207 — <https://csrc.nist.gov/pubs/sp/800/207/final>;
> NIST SP 1800-35 — <https://csrc.nist.gov/pubs/sp/1800/35/final>;
> CISA ZT Maturity Model v2 — <https://www.cisa.gov/zero-trust-maturity-model>;
> NIST SP 800-204D (workload-mTLS) — <https://csrc.nist.gov/pubs/sp/800/204/d/final>;
> NIST SP 1800-38 (PQC) — <https://csrc.nist.gov/publications/detail/sp/1800-38/draft>.

| Pillar | Title | UCs | NHIs |
|---|---|---|---|
| ZT-Pillar-Identity | Subject identification and per-request authorisation for NHIs | UC-F-003; UC-F-004; UC-F-006; UC-F-007; UC-F-013; UC-F-015; UC-F-020; UC-F-024; UC-F-025; UC-F-027; UC-N-002; UC-N-003 | NHI-001; NHI-002; NHI-003; NHI-005; NHI-006; NHI-007; NHI-012; NHI-019; NHI-027; NHI-028; NHI-029; NHI-035; NHI-036; NHI-037 |
| ZT-Pillar-Identity-Federation | Federated OIDC / SVID identity for CI/CD and partner clients | UC-F-003; UC-F-004; UC-F-018; UC-F-024 | NHI-003; NHI-006; NHI-019; NHI-027; NHI-028; NHI-036 |
| ZT-Pillar-Workload-mTLS | Workload-to-workload attested mTLS via service mesh | UC-F-004; UC-F-008; UC-F-009; UC-F-012; UC-F-014 | NHI-002; NHI-004; NHI-006; NHI-011; NHI-013; NHI-017; NHI-036 |
| ZT-Pillar-Workload-CICD | CI/CD pipeline integrity + ephemeral credentials | UC-F-003; UC-F-010; UC-F-016; UC-N-012 | NHI-003; NHI-009; NHI-015; NHI-016; NHI-020 |
| ZT-Pillar-Workload-Runtime | Runtime attestation gates secret release | UC-F-004; UC-F-017; UC-F-018; UC-N-018 | NHI-002; NHI-006; NHI-018; NHI-019; NHI-036 |
| ZT-Pillar-Device | Device health + hardware-rooted identity gating secret release | UC-F-019; UC-F-023; UC-N-016 | NHI-021; NHI-032; NHI-033 |
| ZT-Pillar-Network | Broker placement + micro-segmentation around secrets infrastructure | UC-F-012; UC-F-014; UC-F-022; UC-F-024 | NHI-006; NHI-011; NHI-013; NHI-028; NHI-031; NHI-032 |
| ZT-Pillar-Data | Data keys (TDE / TEE-bound) governed as NHIs with custodian quorum | UC-F-005; UC-F-008; UC-F-016; UC-F-017; UC-N-007; UC-N-012; UC-N-013; UC-N-018 | NHI-018; NHI-023; NHI-024; NHI-025; NHI-034; NHI-035 |
| ZT-Pillar-Visibility-Analytics | Tamper-evident logging of secret-access events with per-NHI baselining | UC-N-001; UC-N-002; UC-N-011; UC-N-017; UC-N-019; UC-N-020 | NHI-001; NHI-007; NHI-008; NHI-010; NHI-013; NHI-019; NHI-026; NHI-030; NHI-031; NHI-035; NHI-037 |
| ZT-Pillar-Visibility-NHIDR | NHI Detection and Response for anomalous credential use | UC-F-007; UC-N-011; UC-N-019 | NHI-007; NHI-019; NHI-026; NHI-030; NHI-037 |
| ZT-Pillar-Automation-Orchestration | Rotation, revocation, and lifecycle orchestration without human transcription | UC-F-006; UC-F-007; UC-F-011; UC-F-020; UC-F-021; UC-F-027 | NHI-005; NHI-007; NHI-010; NHI-011; NHI-012; NHI-014; NHI-022; NHI-026; NHI-029; NHI-031; NHI-037 |
| ZT-Pillar-Governance | Policy-as-code, exception register, and supply-chain attestation for NHIs | UC-N-004; UC-N-005; UC-N-006; UC-N-007; UC-N-009; UC-N-010; UC-N-014; UC-N-015 | NHI-007; NHI-024; NHI-025; NHI-026; NHI-028; NHI-030; NHI-035; NHI-037 |
| ZT-Pillar-Governance-PQC | Crypto-agility + PQC readiness reporting | UC-F-016; UC-N-013 | NHI-006; NHI-015; NHI-023; NHI-024; NHI-025; NHI-028; NHI-034 |

**Density read.** ZT-Pillar-Identity carries the heaviest UC density;
ZT-Pillar-Workload-mTLS and ZT-Pillar-Visibility-Analytics carry the
next two. Workload sub-pillars (mTLS / CICD / Runtime) together cover
the Cluster B spine (UC-F-004 + UC-F-008 + UC-F-016 + UC-F-017 +
UC-F-018). ZT-Pillar-Governance-PQC is the v0.1 hook for UC-N-013 and
the 2030-deadline obligations.

---

## A.3 BACK-MAP — APRA CPS 234 + CPS 230 + CPG 234 + ASD ISM

BACK-MAP = the **audit-facing narrative** an Australian regulator
expects. Per [ADR-003](../adrs/ADR-003-regulatory-lens.md), these
frames are not used as the primary maturity driver but as the
back-cite for any UC outcome.

### A.3.1 APRA CPS 234 — 25 paragraph codes

> Source: APRA CPS 234 (July 2019) — <https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf>.
> Paragraph numbering normalised at M2 to **§21(a)-(d), §27(a)-(e),
> §35** per [meta/review-M2-2026-05-23.md](../../meta/review-M2-2026-05-23.md)
> §B3.

| Code | Title | UCs | NHIs |
|---|---|---|---|
| CPS234-§13 | Board accountability for information security | UC-N-004; UC-N-005; UC-N-011; UC-N-015 | NHI-001; NHI-019; NHI-024; NHI-026; NHI-035 |
| CPS234-§14 | Clearly defined information-security roles | UC-N-002; UC-N-004; UC-N-009; UC-N-014; UC-N-015 | NHI-024; NHI-025; NHI-035; NHI-037 |
| CPS234-§15 | Information-security capability commensurate with threats | UC-F-004; UC-F-005; UC-F-006; UC-F-007; UC-F-026; UC-N-002; UC-N-003; UC-N-005 | NHI-001; NHI-002; NHI-005; NHI-006; NHI-008; NHI-012; NHI-019; NHI-022; NHI-035; NHI-037 |
| CPS234-§16 | Assess third-party information-security capability | UC-F-024; UC-F-025; UC-N-006; UC-N-007 | NHI-007; NHI-026; NHI-028; NHI-030; NHI-035 |
| CPS234-§17 | Active capability maintenance through change | UC-F-006; UC-F-027; UC-N-001; UC-N-003; UC-N-008; UC-N-013 | NHI-019; NHI-034; NHI-037 |
| CPS234-§18 | Information-security policy framework | UC-N-005; UC-N-008; UC-N-009; UC-N-015 | NHI-008; NHI-019; NHI-029 |
| CPS234-§19 | Policy framework — direction on responsibilities | UC-N-008; UC-N-015 | NHI-029; NHI-030 |
| CPS234-§20 | Asset classification by criticality and sensitivity | UC-F-005; UC-N-002; UC-N-007; UC-N-020 | NHI-005; NHI-008; NHI-022; NHI-023; NHI-026 |
| CPS234-§21 | Implementation of information-security controls (umbrella) | UC-F-001; UC-F-003; UC-F-004; UC-F-005; UC-F-006; UC-F-008; UC-F-009; UC-F-010; UC-F-012; UC-F-016; UC-F-018; UC-F-019; UC-F-020; UC-F-021; UC-F-022; UC-F-024 | NHI-001; NHI-002; NHI-005; NHI-006; NHI-007; NHI-008; NHI-011; NHI-015; NHI-017; NHI-018; NHI-022; NHI-023; NHI-024; NHI-026; NHI-028; NHI-031 |
| CPS234-§21(a) | Controls commensurate with vulnerabilities + threats | UC-F-001; UC-F-002; UC-F-007; UC-F-022; UC-N-011 | NHI-007; NHI-008; NHI-026; NHI-037 |
| CPS234-§21(b) | Controls commensurate with criticality and sensitivity | UC-F-005; UC-F-017; UC-F-021; UC-N-007; UC-N-018 | NHI-018; NHI-022; NHI-023; NHI-026 |
| CPS234-§21(c) | Controls commensurate with life-cycle stage | UC-F-006; UC-F-013; UC-F-016; UC-F-019; UC-F-027; UC-N-003 | NHI-015; NHI-016; NHI-021; NHI-029; NHI-034; NHI-037 |
| CPS234-§21(d) | Controls commensurate with incident consequences | UC-F-007; UC-F-021; UC-F-026; UC-N-010; UC-N-011 | NHI-019; NHI-024; NHI-026; NHI-035 |
| CPS234-§22 | Evaluate design of third-party controls | UC-F-024; UC-F-025; UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-026; NHI-028; NHI-030; NHI-035 |
| CPS234-§23 | Detect and respond mechanisms | UC-F-001; UC-F-002; UC-F-007; UC-N-001; UC-N-011; UC-N-017; UC-N-019 | NHI-007; NHI-008; NHI-010; NHI-019; NHI-030; NHI-037 |
| CPS234-§24 | Incident response plans for plausible incidents | UC-F-007; UC-N-010; UC-N-011 | NHI-024; NHI-035; NHI-037 |
| CPS234-§26 | Annual review and test of response plans | UC-F-007; UC-N-010; UC-N-011 | NHI-024; NHI-025; NHI-035 |
| CPS234-§27 | Systematic testing of control effectiveness | UC-F-006; UC-F-021; UC-F-026; UC-N-003; UC-N-005; UC-N-010 | NHI-001; NHI-006; NHI-012; NHI-022; NHI-024; NHI-026; NHI-035 |
| CPS234-§27(d) | Testing commensurate with untrusted-environment exposure | UC-F-018; UC-F-019; UC-F-024; UC-N-007; UC-N-016 | NHI-019; NHI-021; NHI-028; NHI-033 |
| CPS234-§28 | Assess sufficiency of third-party control testing | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-028; NHI-030; NHI-035 |
| CPS234-§30 | Independent specialist testers | UC-N-009; UC-N-010; UC-N-014 | NHI-024; NHI-025; NHI-035 |
| CPS234-§32 | Internal audit review of control effectiveness | UC-N-004; UC-N-009; UC-N-014; UC-N-020 | NHI-022; NHI-026; NHI-035 |
| CPS234-§34 | Internal audit assessment of third-party assurance | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-028; NHI-030; NHI-035 |
| CPS234-§35 | 72-hour APRA notification of material incident | UC-F-007; UC-N-001; UC-N-011; UC-N-019 | NHI-001; NHI-007; NHI-008; NHI-019; NHI-026; NHI-035; NHI-037 |
| CPS234-§36 | 10-business-day notification of material control weakness | UC-N-009; UC-N-011; UC-N-020 | NHI-012; NHI-022; NHI-029; NHI-037 |

**Density read.** **§21 (umbrella)** is the broadest cell — 16 UCs +
16 NHIs — because it is the implementation-controls clause. **§22**
+ **§28** carry the third-party / vendor lane; the FI's MOVEit-2023
victim-cohort exposure (Appendix D row 14) sits exactly here. **§35**
(72-hour notification) is the operational anchor for UC-N-001 +
UC-N-011 + UC-N-019.

### A.3.2 APRA CPS 230 — 6 paragraph codes (operational risk + BCM)

> Source: APRA CPS 230 (effective 1 July 2025) — <https://www.apra.gov.au/cps-230>.

| Code | Title | UCs | NHIs |
|---|---|---|---|
| CPS230-§15 | Service-provider prudential dependency gate | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-026; NHI-035 |
| CPS230-§25 | Sound IT capability + CPS 234 cross-reference | UC-F-026; UC-N-005; UC-N-013; UC-N-014 | NHI-022; NHI-034; NHI-035 |
| CPS230-§42 | 24-hour BCP-breach notification (vault / PKI outage) | UC-F-026; UC-N-007; UC-N-011 | NHI-023; NHI-024; NHI-025; NHI-035 |
| CPS230-§47 | Comprehensive service-provider management policy | UC-F-025; UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-026; NHI-030; NHI-035 |
| CPS230-§54 | Formal legally-binding agreement for material arrangements | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-026; NHI-030; NHI-035 |
| CPS230-§59(b) | Material-offshoring pre-notification to APRA | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-030; NHI-035 |

**Density read.** Five of six rows touch UC-N-007 (data-sovereignty /
residency); CPS 230 is the back-cite for every AU-residency
disqualification in PRD §11 (NHI-discovery tier; Doppler;
1Password SaaS; Infisical SaaS; AKEYLESS without self-hosted
Gateway).

### A.3.3 APRA CPG 234 — 3 attachments (practice guidance)

> Source: APRA CPG 234 — <https://www.apra.gov.au/sites/default/files/cpg_234_information_security.pdf>.

| Code | Title | UCs | NHIs |
|---|---|---|---|
| CPG234-Att-C | Identity and access management practice guidance | UC-F-006; UC-F-013; UC-F-020; UC-N-002 | NHI-006; NHI-012; NHI-022; NHI-029 |
| CPG234-Att-D | Cryptographic key management practice guidance | UC-F-016; UC-F-020; UC-N-010; UC-N-013 | NHI-023; NHI-024; NHI-025; NHI-034 |
| CPG234-Att-E | Third-party assurance practice guidance | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-028; NHI-030; NHI-035 |

### A.3.4 ASD ISM — 41 control codes across 11 domains

> Source: ASD Information Security Manual — <https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism>.
> The ISM is updated quarterly; control codes in this table are from
> the ISM March 2026 release as of 2026-05-23.

**Cryptography (8 controls).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-0471 | Using ASD Approved Cryptographic Algorithms | UC-F-016; UC-F-017; UC-N-013; UC-N-018 | NHI-018; NHI-023; NHI-024; NHI-034 |
| ISM-0507 | Cryptographic key management processes and procedures | UC-F-005; UC-F-016; UC-F-017; UC-F-026; UC-N-007; UC-N-010; UC-N-013 | NHI-023; NHI-024; NHI-025; NHI-034; NHI-035 |
| ISM-1324 | Issuing certificates — generated via evaluated CA or HSM | UC-F-016; UC-F-020; UC-F-026; UC-N-012; UC-N-013 | NHI-015; NHI-023; NHI-024; NHI-025; NHI-034 |
| ISM-0481 | Using ASD Approved Cryptographic Protocols | UC-F-004; UC-F-005; UC-F-008; UC-F-026 | NHI-006; NHI-023; NHI-024; NHI-035 |
| ISM-0457 | Encrypting data at rest | UC-F-005; UC-F-016; UC-F-017; UC-F-024; UC-F-026; UC-N-007; UC-N-010; UC-N-013 | NHI-023; NHI-024; NHI-025; NHI-028; NHI-035 |
| ISM-0469 | Encrypting data in transit | UC-F-004; UC-F-008; UC-F-012; UC-F-014; UC-F-022; UC-F-024 | NHI-006; NHI-011; NHI-013; NHI-028; NHI-031 |
| ISM-1139 | Configuring Transport Layer Security | UC-F-004; UC-F-008; UC-F-014; UC-F-024; UC-N-013 | NHI-006; NHI-013; NHI-028; NHI-034 |
| ISM-1323 | Issuing unique certificates for authentication | UC-F-004; UC-F-014; UC-F-019; UC-F-024; UC-N-013 | NHI-006; NHI-013; NHI-021; NHI-025; NHI-028; NHI-034 |
| ISM-1917 | Transitioning to post-quantum cryptography | UC-F-016; UC-N-013 | NHI-023; NHI-024; NHI-025; NHI-028; NHI-034 |

**Identification and Authentication (7 controls).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-1173 | Multi-factor authentication — privileged users | UC-F-001; UC-F-005; UC-F-015; UC-F-021; UC-N-010 | NHI-005; NHI-012; NHI-014; NHI-024; NHI-026; NHI-029 |
| ISM-1619 | Setting/resetting credentials for service accounts (gMSA) | UC-F-001; UC-F-003; UC-F-004; UC-F-005; UC-F-006; UC-F-008; UC-F-009; UC-F-010; UC-F-012; UC-F-013; UC-F-015; UC-F-018; UC-F-020; UC-F-024; UC-F-025; UC-N-002; UC-N-019 | NHI-001; NHI-002; NHI-003; NHI-005; NHI-006; NHI-007; NHI-009; NHI-012; NHI-019; NHI-022; NHI-028; NHI-029; NHI-035 |
| ISM-1504 | Multi-factor authentication — online services | UC-F-001; UC-F-003; UC-F-015; UC-N-008 | NHI-003; NHI-008; NHI-029 |
| ISM-1401 | Multi-factor authentication — approved factor types | UC-F-007; UC-F-015; UC-N-010 | NHI-014; NHI-024; NHI-025; NHI-029 |
| ISM-1795 | Credential length (>=30 chars) for service / break-glass / admin accounts | UC-F-006; UC-F-013; UC-F-020; UC-F-023; UC-N-003 | NHI-005; NHI-007; NHI-012; NHI-022; NHI-029; NHI-032; NHI-033 |
| ISM-1611 | Emergency (break-glass) access — restricted use | UC-F-007; UC-F-026; UC-N-010; UC-N-011 | NHI-024; NHI-025; NHI-026; NHI-035 |
| ISM-1613 | Emergency (break-glass) access — centralised logging | UC-F-007; UC-F-027; UC-N-002; UC-N-011; UC-N-019 | NHI-001; NHI-012; NHI-022; NHI-024; NHI-025; NHI-035; NHI-037 |

**System Hardening and Software Development (5).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-1690 | When to patch vulnerabilities | UC-F-002; UC-N-001 | NHI-008; NHI-010; NHI-037 |
| ISM-1656 | Application control | UC-F-008; UC-F-009; UC-F-016 | NHI-002; NHI-004; NHI-015; NHI-016 |
| ISM-1247 | Hardening server application configurations | UC-F-008; UC-F-019; UC-F-023 | NHI-002; NHI-021; NHI-032; NHI-033 |
| ISM-0401 | Secure software development — practices | UC-F-001; UC-F-002; UC-N-008; UC-N-015 | NHI-003; NHI-008 |
| ISM-1796 | Secure software development — code signing | UC-F-001; UC-F-002; UC-F-010; UC-N-001; UC-N-008; UC-N-015 | NHI-001; NHI-003; NHI-005; NHI-007; NHI-008; NHI-009; NHI-010; NHI-037 |
| ISM-1730 | Software bill of materials | UC-F-016; UC-N-012 | NHI-015; NHI-016; NHI-020; NHI-024; NHI-034 |

**Database Systems + Network and Gateways (5).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-1256 | Protecting databases | UC-F-005; UC-F-006 | NHI-005; NHI-023 |
| ISM-1275 | Software interaction with databases | UC-F-005; UC-F-006; UC-N-003 | NHI-005; NHI-023 |
| ISM-1181 | Network segmentation and segregation | UC-F-008; UC-F-012; UC-F-014; UC-F-022; UC-F-023 | NHI-002; NHI-011; NHI-013; NHI-031; NHI-032 |
| ISM-1211 | System administration processes and procedures | UC-F-023; UC-N-016 | NHI-032; NHI-033 |
| ISM-1437 | Cloud-based hosting of online services | UC-F-003; UC-F-007; UC-F-026; UC-N-010 | NHI-001; NHI-024; NHI-035 |

**Communications + IoT (3).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-1192 | Implementing gateways | UC-F-014; UC-F-022; UC-F-024 | NHI-006; NHI-013; NHI-028; NHI-031 |
| ISM-0421 | Single-factor authentication (where MFA not feasible) | UC-F-022; UC-N-006 | NHI-007; NHI-013; NHI-031 |
| ISM-1304 | Default user accounts and credentials for network/OT devices | UC-F-019; UC-N-016 | NHI-021; NHI-033 |

**Incidents + Backups + Personnel + Governance (8).**

| Code | Title | UCs | NHIs |
|---|---|---|---|
| ISM-1405 | Centralised event logging facility | UC-F-011; UC-F-018; UC-N-001; UC-N-011; UC-N-017; UC-N-019 | NHI-010; NHI-011; NHI-019; NHI-035 |
| ISM-0043 | Cybersecurity incident response plan | UC-F-007; UC-N-004; UC-N-011 | NHI-001; NHI-035; NHI-037 |
| ISM-0140 | Reporting cybersecurity incidents to ASD | UC-N-004; UC-N-011 | NHI-019; NHI-026; NHI-037 |
| ISM-1404 | Suspension of access to systems (credential revocation) | UC-F-007; UC-N-011 | NHI-001; NHI-003; NHI-007; NHI-008; NHI-019; NHI-027; NHI-035; NHI-037 |
| ISM-0252 | Providing cybersecurity awareness training | UC-N-008; UC-N-015 | NHI-003; NHI-008; NHI-019 |
| ISM-0027 | Authorisation to operate / risk acceptance | UC-N-009 | NHI-012; NHI-014; NHI-022; NHI-029; NHI-033; NHI-037 |
| ISM-1570 | Assessment of outsourced cloud service providers (IRAP) | UC-N-006; UC-N-007 | NHI-007; NHI-018; NHI-023; NHI-024; NHI-030; NHI-035 |
| ISM-0039 | Cybersecurity strategy | UC-N-004; UC-N-005; UC-N-009; UC-N-015 | — |
| ISM-0363 | Media destruction processes and procedures (secure decommissioning) | UC-F-027; UC-N-002 | NHI-021; NHI-024; NHI-026; NHI-037 |
| ISM-1452 | Cyber supply chain risk management activities | UC-N-006; UC-N-007; UC-N-014 | NHI-007; NHI-030; NHI-035 |
| ISM-1707 | Backup modification and deletion (immutability) | UC-F-021; UC-N-016 | NHI-024; NHI-026 |

**Density read.** **ISM-1619** (setting/resetting credentials for
service accounts — gMSA) is the heaviest cell — 17 UCs + 13 NHIs —
because it explicitly governs every service-account-class identity.
ISM-1796 (secure software development — code signing) is the back-cite
for UC-F-001 / UC-F-002 / UC-N-001. ISM-1404 (suspension of access /
credential revocation) is the back-cite for UC-F-007. ISM-1917 (PQC
transition) is the back-cite for UC-N-013.

---

## A.4 ADVERSARY-LENS — MITRE ATT&CK T1552 family + breach catalog

ADVERSARY-LENS = the **defensive narrative**: which TTPs and breaches
each UC has demonstrated impact against. **31 rows** total: 16 MITRE
techniques + 15 breach post-mortems. The full narrative for every row
is in [Appendix D](./D-adversary-context.md); this section provides
the per-row UC + NHI cross-reference for completeness.

### A.4.1 T1552 family + adjacent (16 techniques)

| Technique | UCs | NHIs |
|---|---|---|
| T1552.001 — Credentials in Files | UC-F-001; UC-F-002; UC-F-005; UC-F-006; UC-F-010; UC-N-001; UC-N-002 | NHI-001; NHI-003; NHI-005; NHI-007; NHI-008; NHI-009; NHI-012; NHI-029; NHI-037 |
| T1552.002 — Credentials in Registry | UC-F-006; UC-F-013; UC-F-015; UC-F-027; UC-N-002 | NHI-012; NHI-022; NHI-029; NHI-033; NHI-037 |
| T1552.003 — Shell History | UC-F-001; UC-F-005; UC-F-006; UC-N-008; UC-N-017 | NHI-005; NHI-008; NHI-009; NHI-029 |
| T1552.004 — Private Keys | UC-F-004; UC-F-006; UC-F-016; UC-F-017; UC-F-026; UC-N-010; UC-N-013 | NHI-006; NHI-008; NHI-015; NHI-016; NHI-024; NHI-025; NHI-034 |
| T1552.005 — Cloud Instance Metadata API | UC-F-003; UC-F-004; UC-F-008; UC-F-009; UC-F-017; UC-N-002 | NHI-001; NHI-002; NHI-003; NHI-004; NHI-006 |
| T1552.006 — Group Policy Preferences | UC-F-006; UC-F-013; UC-F-027; UC-N-002 | NHI-012; NHI-029; NHI-037 |
| T1552.007 — Container API | UC-F-004; UC-F-008; UC-F-009; UC-F-017; UC-N-002 | NHI-002; NHI-003; NHI-004; NHI-017; NHI-036 |
| T1552.008 — Chat Messages | UC-F-001; UC-F-007; UC-F-025; UC-N-008; UC-N-017 | NHI-007; NHI-008; NHI-029; NHI-030 |
| T1528 — Steal Application Access Token | UC-F-007; UC-F-018; UC-F-022; UC-F-024; UC-F-025; UC-N-006 | NHI-007; NHI-019; NHI-027; NHI-028; NHI-030 |
| T1078.004 — Valid Cloud Accounts | UC-F-003; UC-F-005; UC-F-006; UC-F-007; UC-N-002; UC-N-011 | NHI-001; NHI-005; NHI-007; NHI-029; NHI-037 |
| T1606.002 — Forge Web Credentials: SAML Tokens | UC-F-004; UC-F-006; UC-F-007; UC-F-014; UC-F-024; UC-F-026 | NHI-006; NHI-007; NHI-013; NHI-024; NHI-027 |
| T1098.001 — Additional Cloud Credentials | UC-F-006; UC-F-007; UC-F-027; UC-N-002; UC-N-009; UC-N-011 | NHI-001; NHI-007; NHI-008; NHI-012; NHI-027; NHI-028 |
| T1199 — Trusted Relationship | UC-F-016; UC-F-022; UC-F-024; UC-F-025; UC-N-006; UC-N-012; UC-N-014 | NHI-007; NHI-008; NHI-015; NHI-016; NHI-019; NHI-028; NHI-030 |
| T1539 — Steal Web Session Cookie | UC-F-007; UC-F-025; UC-N-008; UC-N-017 | NHI-007; NHI-008; NHI-027; NHI-030 |
| T1556.006 — MFA-related bypass | UC-F-007; UC-F-013; UC-F-025; UC-N-002; UC-N-009 | NHI-007; NHI-029; NHI-030 |
| T1566 — Phishing (initial-access feeder) | UC-F-007; UC-F-013; UC-N-008; UC-N-009 | NHI-007; NHI-008; NHI-029; NHI-030 |

### A.4.2 Breach catalog (15 incidents)

| Incident | UCs | NHIs |
|---|---|---|
| Okta 2023-10 (Customer Support) | UC-F-001; UC-F-006; UC-F-025; UC-F-027; UC-N-002; UC-N-006; UC-N-017 | NHI-007; NHI-029; NHI-030 |
| Okta 2022-01 (LAPSUS$ / Sitel) | UC-F-007; UC-F-025; UC-N-002; UC-N-006; UC-N-009; UC-N-011 | NHI-007; NHI-029; NHI-030 |
| Cloudflare 2023-11 (Thanksgiving) | UC-F-006; UC-F-007; UC-F-027; UC-N-002; UC-N-006; UC-N-011 | NHI-007; NHI-008; NHI-029; NHI-037 |
| CircleCI 2023-01 | UC-F-003; UC-F-004; UC-F-006; UC-F-007; UC-N-006; UC-N-017 | NHI-003; NHI-007; NHI-008; NHI-030 |
| Internet Archive 2024-10 | UC-F-001; UC-F-002; UC-F-006; UC-F-007; UC-N-002; UC-N-006 | NHI-007; NHI-008; NHI-029 |
| Sourcegraph 2023-08 | UC-F-001; UC-F-002; UC-F-006; UC-F-007; UC-N-001; UC-N-008 | NHI-007; NHI-008; NHI-029 |
| LastPass 2022 | UC-F-006; UC-F-007; UC-F-017; UC-F-026; UC-N-010; UC-N-011 | NHI-008; NHI-024; NHI-029; NHI-035 |
| xz-utils 2024-03 | UC-F-016; UC-F-025; UC-N-006; UC-N-012; UC-N-014 | NHI-008; NHI-015; NHI-016; NHI-019 |
| SolarWinds (SUNBURST) 2020 | UC-F-004; UC-F-016; UC-F-017; UC-F-026; UC-N-010; UC-N-011; UC-N-012; UC-N-013 | NHI-003; NHI-006; NHI-008; NHI-015; NHI-016; NHI-024; NHI-025 |
| Microsoft Storm-0558 2023-07 | UC-F-006; UC-F-016; UC-F-017; UC-F-026; UC-N-010; UC-N-011; UC-N-013 | NHI-006; NHI-015; NHI-024; NHI-025 |
| Uber 2022-09 | UC-F-001; UC-F-005; UC-F-007; UC-F-013; UC-F-015; UC-F-026; UC-N-002; UC-N-010 | NHI-001; NHI-005; NHI-012; NHI-024; NHI-029; NHI-037 |
| Toyota 2022-10 | UC-F-001; UC-F-002; UC-F-003; UC-F-006; UC-N-001; UC-N-002; UC-N-006 | NHI-001; NHI-008; NHI-029 |
| Sumo Logic 2023-11 | UC-F-003; UC-F-006; UC-F-007; UC-N-002; UC-N-017 | NHI-001; NHI-007; NHI-029 |
| MOVEit 2023-05/06 | UC-F-007; UC-F-014; UC-F-022; UC-N-006; UC-N-011; UC-N-014 | NHI-006; NHI-007; NHI-013; NHI-029; NHI-031 |
| Snowflake-related 2024-06 | UC-F-003; UC-F-005; UC-F-006; UC-F-007; UC-N-002; UC-N-006; UC-N-011 | NHI-001; NHI-005; NHI-007; NHI-029; NHI-037 |

See [Appendix D](./D-adversary-context.md) §D.3 for per-incident
vectors, primary URLs and direct quotes.

---

## A.5 Reverse map — PRIMARY-LENS coverage check

For each of the 47 UCs the team verified that **at least one
PRIMARY-LENS control cell** (E8 or CISA ZTMM) carries the UC ID.

**Result:** **47 of 47 UCs have direct PRIMARY-LENS coverage** — no
PRIMARY-LENS reverse-mapping gap. The two programme-management UCs that
once read as governance-only (UC-N-014 vendor-evaluation matrix
maintenance; UC-N-015 communications cadence) each carry a CISA ZTMM
PRIMARY-LENS row (`ZT-Pillar-Governance`) in addition to their
BACK-MAP coverage (CPS 234 / CPS 230 / ISM). They are operationally
governed end-to-end, not PRIMARY-LENS-orphaned.

The **E8-RAP-NHI-GAP** row in §A.2.1 also carries the explicit flag
that E8 itself has no dedicated NHI control for NHI-002 / NHI-016 /
NHI-031 / NHI-033 / NHI-034 — those NHIs are governed via ZT pillars
+ ISM controls (notably ZT-Pillar-Workload-mTLS, ZT-Pillar-
Governance-PQC, ISM-1917). **No PRIMARY-LENS reverse-mapping gap is
material**; the row is preserved so the regulator can read the
deliberate decision.

---

## A.6 NIST CSF 2.0 deferral

NIST CSF 2.0 is **deferred to v1.0** per stakeholder direction
(Task 0 §B.03) and reaffirmed at the M2 gate
([meta/review-M2-2026-05-23.md](../../meta/review-M2-2026-05-23.md)
§F.1). The 47 UCs in
[`research/use-cases.md`](../../research/use-cases.md) were authored
with `CSF-*` references retained for v1.0 forward compatibility;
those tags remain in the UC catalogue and the per-vendor profiles but
are not enumerated in §A.2 / §A.3 of this appendix. PRD §17 O8 carries
the deferral as a stakeholder-confirmation open question.

---

## A.7 Reading guide

- **For a regulator** ("show me CPS 234 §22 evidence for NHI
  governance"): start at §A.3.1 → join with §10 XYZ current-state →
  pull the UC-N-004 acceptance-criteria evidence pack.
- **For an architect** ("which UCs deliver E8-RAP-ML3 uplift?"):
  start at §A.2.1 → cross-reference with PRD §16 recommendations.
- **For a security engineer** ("which TTPs does UC-F-007 mitigate?"):
  start at §A.4.1 → cross-reference with [Appendix D](./D-adversary-context.md)
  §D.3 for breach-specific narrative.
- **For data lookup**: open
  [`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv)
  — the 145-row CSV is the authoritative source; this appendix is a
  compressed reading view.

---

> _End of Appendix A (Wave B v0.1)._

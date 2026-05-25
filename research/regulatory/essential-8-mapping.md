# Regulatory Mapping — ASD Essential 8 (Essential Eight Maturity Model)

**Role in PRD:** PRIMARY-LENS (outcomes-first, per ADR-003)
**Primary source:** https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model
**Version cited:** Essential Eight Maturity Model — November 2023 (last updated October 2024 FAQ; March 2025 "changes" PDF revision).
**Sensitivity:** [PUBLIC]
**Mapped by:** Opus 4.7 (prompt 04 v0.1), 2026-05-23 AEST.

---

## 1. Framework summary

The **Essential Eight (E8)** is the Australian Signals Directorate
(ASD) / Australian Cyber Security Centre (ACSC) baseline of eight
prioritised mitigation strategies for cyber-security incidents. It is
mandatory for Commonwealth non-corporate entities under PSPF Direction
002-2022 and is widely adopted by APRA-regulated financial institutions
as the operational lens for CPS 234 control implementation
[acsc-e8-2023][acsc-e8-mm-nov2023].

The model defines a **four-level maturity** scale — Maturity Level Zero
(weaknesses present), **ML1**, **ML2**, **ML3** — calibrated against
increasing adversary tradecraft (opportunistic, target-of-opportunity,
adaptive) [acsc-e8-mm-nov2023]. The November 2023 revision (effective
through 2025-03 changes PDF) materially tightened **Restrict
Administrative Privileges**, **Multi-Factor Authentication** and
**Patch Applications/OS** in ways directly relevant to non-human-
identity (NHI) governance: service-account credential hygiene moved
explicit, break-glass accounts became a first-class concept, and MFA
phishing-resistance became a ML3 requirement for both internal
privileged users and customers of online services
[acsc-e8-changes-nov2023].

E8 is the PRD's **primary outcome lens** (ADR-003) because (a) it is
the de facto Australian regulator-recognised baseline; (b) its maturity
model gives the secrets-management programme a defensible 3-step
roadmap from foundational to threat-adaptive; and (c) it back-maps
cleanly onto the ASD ISM control library
[acsc-e8-ism-mapping-2023]. The CPS 234, ISM, and NIST CSF 2.0 back-
maps are deliberately scoped to **separate agents** so that the PRD
narrative is anchored in outcomes, not in cross-framework citation
sprawl.

E8 is **deliberately narrow**: it focuses on user-driven cyber-hygiene
on Windows-centric estates. NHIs are not enumerated as a control
class — a gap that this mapping makes explicit and that the PRD must
close via the NIST SP 800-207 ZT pillars (Agent 04 sibling run).

## 2. Control objectives in scope

The eight mitigation strategies, with secrets-management / NHI
relevance scored:

- **E8-AC — Application control** — HIGH relevance (signed-artifact
  admission; image-pull governance; supply-chain trust)
  [acsc-e8-2023].
- **E8-PA — Patch applications** — MEDIUM (vault platform, agent
  patching; 48-hour critical SLA from November 2023 revision)
  [acsc-e8-changes-nov2023].
- **E8-MAC — Restrict Microsoft Office macros** — OUT OF SCOPE
  (irrelevant to NHIs).
- **E8-UAH — User application hardening** — LOW (browser hygiene only
  brushes UC-N-008 / UC-F-001).
- **E8-RAP — Restrict administrative privileges** — **PRIMARY**
  relevance: the single most-load-bearing E8 control for the secrets
  programme. Includes new service-account and break-glass credential
  clauses (November 2023) [acsc-e8-changes-nov2023].
- **E8-POS — Patch operating systems** — MEDIUM (vault appliances,
  HSM firmware, network-device OS).
- **E8-MFA — Multi-factor authentication** — HIGH (privileged-user
  MFA; ML3 phishing-resistance; workload-MFA analogue via mTLS +
  hardware-attested workload identity).
- **E8-RB — Regular backups** — HIGH (vault data + audit logs;
  HSM/KMS key backup custody; ransomware-resilience).

ML1 = mitigate opportunistic actors; ML2 = mitigate targeting actors
using publicly-available tradecraft; ML3 = mitigate adaptive actors
willing to invest in custom tradecraft [acsc-e8-mm-nov2023].

## 3. UC ↔ control mapping

### E8-RAP-ML1 — Restrict admin privileges (least-privilege baseline)
- **What it requires:** Validate privilege requests on first
  assignment; segregate privileged and unprivileged environments;
  re-validate annually.
- **UCs that satisfy it:** UC-F-003, UC-F-005, UC-F-013, UC-F-021,
  UC-N-002, UC-N-009, UC-N-010.
- **NHIs especially relevant:** NHI-001, NHI-005, NHI-012, NHI-024,
  NHI-026, NHI-029, NHI-035.
- **Evidence quote:** "Requests for privileged access to systems and
  applications are validated when first requested." [acsc-e8-2023]
- **Maturity level:** ML1.

### E8-RAP-ML2 — Restrict admin privileges (separation + JIT)
- **What it requires:** Privileged accounts prevented from internet /
  email / web; just-in-time elevation; separate privileged
  environments; central logging of privileged events.
- **UCs that satisfy it:** UC-F-003, UC-F-005, UC-F-006, UC-F-007,
  UC-F-013, UC-F-015, UC-F-020, UC-F-021, UC-F-026, UC-N-002,
  UC-N-009, UC-N-010.
- **NHIs especially relevant:** NHI-001, NHI-005, NHI-012, NHI-014,
  NHI-022, NHI-024, NHI-026, NHI-029, NHI-035.
- **Evidence quote:** "Privileged accounts (excluding privileged
  service accounts) are prevented from accessing the internet, email
  and web services." [acsc-e8-2023]
- **Maturity level:** ML2.

### E8-RAP-ML3 — Restrict admin privileges (Secure Admin Workstations)
- **What it requires:** Admin actions occur from dedicated, hardened
  workstations; memory isolation; LSA protection; reviewed
  semi-annually.
- **UCs that satisfy it:** UC-F-003, UC-F-007, UC-F-016, UC-F-020,
  UC-F-021, UC-F-026, UC-F-027, UC-N-009, UC-N-010, UC-N-011.
- **NHIs especially relevant:** NHI-001, NHI-012, NHI-022, NHI-024,
  NHI-025, NHI-026, NHI-035, NHI-037.
- **Evidence quote:** "Secure Admin Workstations are used in the
  performance of administrative activities." [acsc-e8-changes-nov2023]
- **Maturity level:** ML3.

### E8-RAP-SVC — Service-account credential hygiene (Nov-2023 add)
- **What it requires:** All service-account credentials are long,
  unique, unpredictable and managed by a controlled mechanism (i.e.,
  a vault, gMSA, or equivalent broker).
- **UCs that satisfy it:** UC-F-006, UC-F-013, UC-F-020, UC-F-023,
  UC-F-026, UC-F-027, UC-N-002, UC-N-003, UC-N-009.
- **NHIs especially relevant:** NHI-001, NHI-005, NHI-007, NHI-012,
  NHI-022, NHI-026, NHI-029, NHI-032, NHI-035, NHI-037.
- **Evidence quote:** "Credentials for local administrator accounts
  and service accounts are long, unique, unpredictable and managed."
  [acsc-e8-changes-nov2023]
- **Maturity level:** ML2.

### E8-RAP-BREAKGLASS — Break-glass identity management (Nov-2023 add)
- **What it requires:** Break-glass accounts (HSM CO, KMS root, vault
  recovery, backup break-glass) are inventoried, credentialled to the
  same standard as service accounts, and exempted only from backup-
  modification prohibitions.
- **UCs that satisfy it:** UC-F-007, UC-F-026, UC-N-009, UC-N-010.
- **NHIs especially relevant:** NHI-024, NHI-025, NHI-026, NHI-035.
- **Evidence quote:** "Credentials for break glass accounts are long,
  unique, unpredictable and managed." [acsc-e8-changes-nov2023]
- **Maturity level:** ML3.

### E8-RAP-LOG — Central event logging for privileged access
- **What it requires:** Privileged-account events centrally logged and
  tamper-resistant; ingestion path supports SOC + audit.
- **UCs that satisfy it:** UC-N-001, UC-N-011, UC-N-017, UC-F-007,
  UC-N-019.
- **NHIs especially relevant:** NHI-001, NHI-024, NHI-035, NHI-037.
- **Evidence quote:** "Privileged access events are centrally logged
  and protected from unauthorised modification and deletion."
  [acsc-e8-2023]
- **Maturity level:** ML2.

### E8-MFA-ML1 — Internet-facing & online-service MFA
- **What it requires:** MFA on internet-facing services that process
  sensitive data; customers offered MFA on online services.
- **UCs that satisfy it:** UC-F-003, UC-F-015, UC-F-024, UC-F-025.
- **NHIs especially relevant:** NHI-003, NHI-007, NHI-014, NHI-028,
  NHI-030.
- **Evidence quote:** "Multi-factor authentication is used by users
  when accessing internet-facing services that process, store or
  communicate sensitive data." [acsc-e8-2023]
- **Maturity level:** ML1.

### E8-MFA-ML2 — Privileged-user MFA + workload mTLS analogue
- **What it requires:** All privileged users (including ops, DB
  admins, vault admins) authenticate with MFA; machine-to-machine
  authentication should use the workload-MFA analogue (mTLS, hardware-
  attested workload identity).
- **UCs that satisfy it:** UC-F-003, UC-F-004, UC-F-006, UC-F-013,
  UC-F-014, UC-F-015, UC-F-024, UC-F-026.
- **NHIs especially relevant:** NHI-001, NHI-006, NHI-012, NHI-013,
  NHI-024, NHI-028, NHI-029, NHI-036.
- **Evidence quote:** "Multi-factor authentication is used to
  authenticate privileged users of systems." [acsc-e8-2023]
- **Maturity level:** ML2.

### E8-MFA-ML3 — Phishing-resistant MFA
- **What it requires:** ML3 mandates phishing-resistant MFA (FIDO2 /
  WebAuthn, smartcards, hardware-rooted passkeys) for privileged users
  and for users of high-value online services.
- **UCs that satisfy it:** UC-F-004, UC-F-007, UC-F-017, UC-F-018,
  UC-F-024, UC-F-026, UC-N-010.
- **NHIs especially relevant:** NHI-006, NHI-018, NHI-019, NHI-024,
  NHI-028, NHI-035, NHI-036.
- **Evidence quote:** "Multi-factor authentication used for
  authenticating users of systems is phishing-resistant."
  [acsc-e8-changes-nov2023]
- **Maturity level:** ML3.

### E8-MFA-WORKLOAD — Machine-to-machine workload-MFA analogue
- **What it requires:** Non-PRD-novel: the PRD applies the E8-MFA
  intent ("two factors, one phishing-resistant") to NHIs as
  mTLS + hardware-attested workload identity (TPM/TEE) — explicitly
  the SPIFFE/Aembit/Clutch pattern.
- **UCs that satisfy it:** UC-F-003, UC-F-004, UC-F-014, UC-F-017,
  UC-F-018, UC-F-019, UC-F-024, UC-F-026.
- **NHIs especially relevant:** NHI-002, NHI-006, NHI-017, NHI-018,
  NHI-021, NHI-028, NHI-036.
- **Evidence quote:** "Multi-factor authentication uses either:
  something users have and something users know, or something users
  have that is unlocked by something users know or are." [acsc-e8-2023]
- **Maturity level:** ML2 analogue.

### E8-AC-ML1 — Application control (executable allow-listing)
- **What it requires:** Allow-list executables, libraries, scripts,
  installers on workstations and internet-facing servers — the supply-
  chain control surface for signed-artifact admission.
- **UCs that satisfy it:** UC-F-001, UC-F-008, UC-F-009, UC-F-010,
  UC-F-016.
- **NHIs especially relevant:** NHI-002, NHI-003, NHI-004, NHI-008,
  NHI-015, NHI-016.
- **Evidence quote:** "Application control is implemented on
  workstations and internet-facing servers and restricts the
  execution of executables, software libraries, scripts and
  installers." [acsc-e8-2023]
- **Maturity level:** ML1.

### E8-AC-ML2 — Microsoft blocklist + central logging
- **What it requires:** Microsoft's recommended application blocklist
  enforced; rulesets reviewed annually; events centrally logged.
- **UCs that satisfy it:** UC-F-016, UC-N-012, UC-N-001, UC-N-011.
- **NHIs especially relevant:** NHI-015, NHI-016, NHI-020.
- **Evidence quote:** "Microsoft's recommended application blocklist
  is implemented; application control rulesets are validated on an
  annual or more frequent basis." [acsc-e8-changes-nov2023]
- **Maturity level:** ML2.

### E8-AC-ML3 — Driver blocklist + signed-artifact admission
- **What it requires:** Vulnerable-driver blocklist enforced;
  tamper-resistant logging; in the PRD context, SLSA-provenance
  verifier admission and TEE-attested execution gating.
- **UCs that satisfy it:** UC-F-008, UC-F-016, UC-N-012.
- **NHIs especially relevant:** NHI-015, NHI-016, NHI-018, NHI-020,
  NHI-034.
- **Evidence quote:** "Microsoft's vulnerable driver blocklist is
  implemented; application control events are centrally logged and
  protected from unauthorised modification." [acsc-e8-changes-nov2023]
- **Maturity level:** ML3.

### E8-PA-ML1 / E8-PA-ML2 — Patch applications (vault platform)
- **What it requires:** Two-week patch SLA for routine vulnerabilities
  in internet-facing applications (vault APIs, SaaS connectors); 48-
  hour SLA for critical vulnerabilities.
- **UCs that satisfy it:** UC-N-001, UC-N-004, UC-N-011, UC-F-026.
- **NHIs especially relevant:** NHI-010, NHI-013, NHI-024, NHI-025,
  NHI-035.
- **Evidence quote (ML2):** "Patches for critical vulnerabilities
  are applied within 48 hours of release when vendors assess
  vulnerabilities as critical or working exploits exist."
  [acsc-e8-changes-nov2023]
- **Maturity levels:** ML1 / ML2.

### E8-POS-ML1 / ML2 / FIRMWARE — Patch operating systems
- **What it requires:** Two-week routine / 48-hour critical OS-patch
  SLAs for internet-facing servers and network devices; firmware
  patching for HSM appliances and routers within one month.
- **UCs that satisfy it:** UC-N-004, UC-N-010, UC-N-011, UC-N-013,
  UC-F-026.
- **NHIs especially relevant:** NHI-021, NHI-022, NHI-023, NHI-024,
  NHI-025, NHI-032, NHI-033, NHI-035.
- **Evidence quote (FIRMWARE):** "Patches, updates or other vendor
  mitigations for vulnerabilities in network devices, firmware and
  operating systems are applied within one month." [acsc-e8-2023]
- **Maturity levels:** ML1 / ML2.

### E8-UAH — User application hardening
- **What it requires:** Browser / PDF / Office hardening; the only
  NHI brush is browser-extension / OAuth-app hygiene (UC-N-008
  training only).
- **UCs that satisfy it:** UC-F-001, UC-F-002, UC-N-008.
- **NHIs especially relevant:** NHI-008.
- **Evidence quote:** "User application hardening is configured to
  prevent execution of unneeded features such as Adobe Flash,
  advertisements and Java content." [acsc-e8-2023]
- **Maturity level:** N/A (low NHI relevance).

### E8-MAC — Restrict Microsoft Office macros
- **What it requires:** Macros blocked; Win32 API calls restricted.
- **UCs:** MISSING-UC. **NHIs:** MISSING-NHI. Not in PRD scope.
- **Evidence quote:** "Microsoft Office macros are blocked from
  making Win32 API calls." [acsc-e8-2023]
- **Maturity level:** N/A.

### E8-RB-ML1 — Regular backups (frequency + retention)
- **What it requires:** Backups of important data, software and
  configuration are performed and retained per business policy. For
  the secrets programme this is **vault data + audit log + HSM key
  backup**.
- **UCs that satisfy it:** UC-F-021, UC-N-001, UC-N-003, UC-N-004.
- **NHIs especially relevant:** NHI-023, NHI-024, NHI-026, NHI-035.
- **Evidence quote:** "Backups of important data, software and
  configuration settings are performed and retained with a frequency
  and retention timeframe in accordance with business requirements."
  [acsc-e8-2023]
- **Maturity level:** ML1.

### E8-RB-ML2 — Backup-administrator separation
- **What it requires:** Identified backup admins; unprivileged
  accounts cannot access others' backups; only backup admins can
  modify backup sets.
- **UCs that satisfy it:** UC-F-021, UC-N-003, UC-N-009, UC-N-010.
- **NHIs especially relevant:** NHI-012, NHI-024, NHI-026, NHI-029,
  NHI-035.
- **Evidence quote:** "Unprivileged accounts cannot access backups
  belonging to other accounts; only backup administrators can modify
  backup sets." [acsc-e8-2023]
- **Maturity level:** ML2.

### E8-RB-ML3 — Immutability + break-glass-only modification
- **What it requires:** Immutability (object-lock, tape-WORM, vault
  cold-storage); only break-glass accounts may modify or delete
  backups.
- **UCs that satisfy it:** UC-F-021, UC-N-004, UC-N-010.
- **NHIs especially relevant:** NHI-023, NHI-024, NHI-026, NHI-035.
- **Evidence quote:** "Unprivileged accounts and privileged accounts
  (excluding backup break glass accounts) are prevented from
  modifying or deleting any backups." [acsc-e8-changes-nov2023]
- **Maturity level:** ML3.

### E8-RB-KEYS — HSM / KMS key backup custody
- **What it requires:** Cryptographic key material is backed up under
  the same controls as data; backups tested and synchronised.
- **UCs that satisfy it:** UC-N-004, UC-N-007, UC-N-010, UC-N-013.
- **NHIs especially relevant:** NHI-023, NHI-024, NHI-025, NHI-035.
- **Evidence quote:** "Backups of important data, software and
  configuration settings are tested and synchronised in a coordinated
  manner." [acsc-e8-2023]
- **Maturity level:** ML2.

### E8-MATURITY-SCORECARD — Programme maturity reporting
- **What it requires:** Quarterly E8 ML1→ML2→ML3 scorecard at Risk
  Committee level (the UC-N-005 deliverable).
- **UCs that satisfy it:** UC-N-005, UC-N-001, UC-N-003, UC-N-009,
  UC-N-011, UC-N-014, UC-N-015, UC-N-020.
- **NHIs especially relevant:** NHI-001, NHI-006, NHI-012, NHI-019,
  NHI-022, NHI-026, NHI-034, NHI-035, NHI-037.
- **Evidence quote:** "Maturity levels One, Two and Three are intended
  to mitigate increasing levels of tradecraft (tools, tactics,
  techniques and procedures) and targeting." [acsc-e8-mm-nov2023]
- **Maturity level:** ML1 / ML2 / ML3.

### E8-RAP-NHI-GAP — Essential 8 has no NHI-specific control
- **What it requires:** GAP row — E8 framing assumes human privileged
  users. NHIs (NHI-002 K8s SA, NHI-016 SLSA attestation, NHI-031
  webhook, NHI-033 branch peripherals, NHI-034 PQC) are out-of-scope
  for E8 text and require NIST SP 800-207 pillars to cover.
- **UCs:** MISSING-UC.
- **NHIs:** NHI-002, NHI-016, NHI-031, NHI-033, NHI-034.
- **Evidence quote:** "Essential Eight controls focus on user accounts
  and do not enumerate machine identities; gap acknowledged by ASD
  ISM mapping document." [acsc-e8-ism-mapping-2023]
- **Maturity level:** N/A.

## 4. Reverse map: UCs not directly covered

UCs not directly satisfied by an E8 control because the framework is
silent on the underlying NHI class (not a UC gap, a framework scope
difference):

- **UC-F-011** (observability-agent credentials) — E8 has no SaaS-
  agent credential control; covered by NIST ZT Visibility & Analytics.
- **UC-F-012** (message-broker hardening) — E8 silent; ZT Network.
- **UC-F-018** (AI-agent tool brokering) — E8 silent on agentic
  NHIs; ZT Identity + governance lens applies.
- **UC-F-019** (IoT/branch enrolment) — E8 scoped to enterprise
  endpoints; NIST SP 800-213 / ZT Device covers.
- **UC-F-022** (webhook inbound verification) — silent in E8.
- **UC-F-024** (FAPI 2.0 partner mTLS) — touched by E8-MFA-WORKLOAD
  but partner-B2B is regulator territory (CDR / APRA).
- **UC-N-006** (vendor supply-chain attestation) — governance, not
  E8 control.
- **UC-N-007** (data-sovereignty) — CPS 230, not E8.
- **UC-N-013** (PQC readiness) — ASD PQC guidance is separate from
  E8 itself, though crypto-agility brushes E8-AC and E8-RB.
- **UC-N-016** (IoT posture reporting) — fleet posture is ZT Device.
- **UC-N-018** (TEE attestation assurance) — E8 silent on
  confidential-computing patterns.

None of the above are **UC gaps** — they are **framework-scope
differences** that justify the dual-lens design (E8 + NIST ZT).

## 5. Outcome-lens cross-references

E8 is the PRD's PRIMARY-LENS. Its eight strategies aggregate into
**four outcome columns** in the PRD §7 dual matrix:

- **Prevent** ⟵ E8-AC, E8-UAH, E8-MAC, E8-PA, E8-POS.
- **Restrict** ⟵ E8-RAP (all 6 rows), E8-MFA (all 4 rows).
- **Detect** ⟵ E8-RAP-LOG, E8-AC-ML3, and E8-MATURITY-SCORECARD.
- **Recover** ⟵ E8-RB (all 4 rows).

NIST ZT pillars provide the **NHI-shaped** complement covering NHI-002
(K8s SA), NHI-016 (SLSA attestation), NHI-031 (webhook), NHI-033
(branch device), NHI-034 (PQC) which E8 does not enumerate. The CPS
234 / ISM / CSF back-map agents will fold their controls under these
outcome columns; this mapping is the canonical anchor.

## 6. Open questions

1. **Workload-MFA analogue authority.** E8 text treats "users" as
   humans. Does XYZ accept the PRD's interpretation of E8-MFA-WORKLOAD
   (mTLS + hardware attestation ≡ workload-MFA), or must it stay an
   informal analogue pending ASD guidance?
2. **Service-account scope.** Does the Nov-2023 service-account
   credential clause cover all 37 NHI classes, or only those that
   share Windows / AD trust? CSA NHI taxonomy assumes the former;
   ASD ISM does not yet enumerate.
3. **Break-glass for vault recovery (Shamir).** Does ASD's
   "break-glass account" framing apply to M-of-N quorum shares, or
   only single-identity break-glass? Material to UC-F-026 / NHI-035.
4. **ML target for XYZ.** Is the FI target ML2 by FY27, ML3 by FY29
   for in-scope NHI classes (banking core, payments rails)? Required
   to populate the UC-N-005 scorecard.
5. **NHI gap acknowledgement.** Will ASD's 2026 model revision
   add NHI-specific controls (rumoured per industry briefings), or
   does the PRD permanently lean on NIST ZT for that surface?

## 7. Citations

See `meta/citations.bib`. BibTeX keys appended under
`## Essential 8 (Agent 04 — regulatory)`:

- `acsc-e8-2023` *(already present)*.
- `acsc-e8-mm-nov2023` — Essential Eight Maturity Model PDF (Nov 2023).
- `acsc-e8-changes-nov2023` — Essential Eight maturity model changes
  PDF (Nov 2023, March 2025 reprint).
- `acsc-e8-faq-oct2024` — Essential Eight Maturity Model FAQ (Oct 2024).
- `acsc-e8-ism-mapping-2023` — Essential Eight maturity model and ISM
  mapping (Dec 2023).
- `acsc-e8-changes-page` — landing page for the changes summary.
- `acsc-e8-explained` — Essential Eight explained (overview).
- `acsc-e8-assessment-2024` — Essential Eight assessment process guide.

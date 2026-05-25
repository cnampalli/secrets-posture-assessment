# Regulatory Mapping — APRA Prudential Standard CPS 234 Information Security

**Role in PRD:** BACK-MAP (per ADR-003, outcomes-first lens; CPS 234 back-mapped from Essential 8 + NIST SP 800-207 ZT).
**Primary source:** https://www.apra.gov.au/information-security
**Standard URL (PDF):** https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf
**Version cited:** CPS 234 dated July 2019, commenced 1 July 2019 (third-party assets from 1 July 2020). Adjacent: CPS 230 *Operational Risk Management* (July 2025, in force 1 July 2025) and CPG 234 *Information Security* (Practice Guide, June 2019).
**Sensitivity:** [PUBLIC]
**Mapped by:** Opus 4.7 (prompt 04 v0.1), 2026-05-23 AEST.

---

## 1. Framework summary

**APRA Prudential Standard CPS 234 Information Security** is the binding
information-security standard for all APRA-regulated entities — ADIs
(including foreign ADIs), general insurers, life companies, private
health insurers and RSE licensees — under the Banking Act 1959,
Insurance Act 1973, Life Insurance Act 1995, PHIPS Act and SIS Act
[apra-cps-234-2019]. It is enforceable: paragraph 11 reserves APRA's
power to adjust or exclude requirements in writing, and breaches expose
the entity's Australian banking / insurance / superannuation licence to
condition-setting and remediation directions [apra-cps-234-2019].

CPS 234 is **outcome-stated, not control-prescriptive**: it requires an
"information security capability commensurate with the size and extent
of threats" (§15), with controls "commensurate with the criticality and
sensitivity" of information assets (§21) [apra-cps-234-2019]. The
operational "what good looks like" detail sits in **Prudential Practice
Guide CPG 234 Information Security** (June 2019) [apra-cpg-234-2019].
**CPS 230 Operational Risk Management** (in force 1 July 2025) brings
binding service-provider, tolerance-level, BCP and 72-hour
operational-incident notification obligations that materially expand the
secrets-management programme's third-party and resilience perimeter —
notably the new 24-hour BCP-breach notification (CPS 230 §42) and the
material-offshoring pre-notification (CPS 230 §59(b)) [apra-cps-230-2025].

CPS 234 is the PRD's **BACK-MAP** framework (ADR-003). The PRD's primary
lens is outcomes-first via the ASD Essential 8 and NIST SP 800-207 ZT
pillars; CPS 234 paragraphs are then derived from those outcomes. This
preserves vendor-neutrality and avoids encoding a regulator's
non-prescriptive standard as if it were a control library — while
ensuring every E8/ZT control surfaces the §-codes a CPS-234 audit pack
must cite. The third-party-management spine of CPS 230 (§47–§60) is
included because secrets-vault, SaaS NHI-discovery and PKI/HSM SaaS
choices all fall under "material service provider" scope.

The standard's **NHI implications** are interpretive: CPS 234 never
mentions "non-human identity", but its definitions of *information
asset* ("information and information technology, including software,
hardware and data") and *information security control* (§12) clearly
encompass machine credentials, vault systems, certificates, keys and
the identity-broker infrastructure that issues them.

## 2. Control objectives in scope

CPS 234 paragraphs relevant to secrets-management and NHIs, plus
adjacent CPS 230 paragraphs (third-party + resilience) and CPG 234
guidance:

- **CPS234-§13** — Board ultimately responsible for information
  security commensurate with threat exposure [apra-cps-234-2019].
- **CPS234-§14** — clearly defined information-security roles and
  responsibilities across Board, senior management, governing bodies.
- **CPS234-§15** — maintain an information-security capability
  commensurate with threats. *(NHI lifecycle + vault platform
  capability.)*
- **CPS234-§16** — assess information-security capability of
  related/third parties (SaaS-vault and NHI-discovery vendors).
- **CPS234-§17** — actively maintain capability through change.
- **CPS234-§18 / §19** — information-security policy framework
  covering all parties (staff, contractors, third parties).
- **CPS234-§20** — classify information assets by criticality and
  sensitivity (data-classification underpins secret tiering).
- **CPS234-§21 / §21(a)–§21(d)** — implement controls **commensurate
  with vulnerabilities/threats, criticality/sensitivity, life-cycle
  stage, and incident consequences** — the load-bearing control clause
  for secrets-management.
- **CPS234-§22** — evaluate the design of related/third-party controls
  protecting the entity's information assets.
- **CPS234-§23 / §24 / §25 / §26** — detect/respond mechanisms,
  response plans, escalation, annual testing.
- **CPS234-§27 / §27(a)–§27(e)** — systematic testing of control
  effectiveness; commensurate with threat-change rate, criticality,
  consequences, untrusted-environment exposure and rate of change.
- **CPS234-§28** — where reliant on third-party testing, assess
  whether nature/frequency of that testing is commensurate.
- **CPS234-§29 / §30 / §31** — escalate test results, independent
  specialists, annual sufficiency review.
- **CPS234-§32 / §33 / §34** — internal-audit review of design and
  operating effectiveness; assess related/third-party assurance.
- **CPS234-§35 / §35(a) / §35(b)** — APRA notification within
  **72 hours** of a material incident.
- **CPS234-§36** — APRA notification within **10 business days** of a
  material control weakness not remediable in a timely manner.
- **CPS230-§15** — must not rely on a service provider unless
  prudential obligations are continuously met (vault-SaaS gating).
- **CPS230-§25** — sound IT capability; cross-reference to CPS 234.
- **CPS230-§42** — **24-hour** notification of a critical-operation
  disruption outside tolerance (secrets-broker outage in scope).
- **CPS230-§47–§54** — service-provider policy + formal agreement
  obligations (audit access, sub-contracting, termination, force
  majeure) [apra-cps-230-2025].
- **CPS230-§59(b)** — pre-notification of material offshoring (every
  US/EU SaaS vault and NHIDR vendor) [apra-cps-230-2025].
- **CPG234-Att-C/D/E (guidance)** — identity and access management,
  cryptographic key management, third-party recommendations
  [apra-cpg-234-2019].

## 3. UC ↔ control mapping

### CPS234-§13 — Board accountability for information security
- **What it requires:** The Board must ensure the entity maintains
  information security commensurate with the size and extent of threats
  to its information assets and continued sound operation.
- **UCs that satisfy it:** UC-N-004, UC-N-005, UC-N-011, UC-N-015.
- **NHIs especially relevant:** NHI-001, NHI-019, NHI-024, NHI-026,
  NHI-035 (vault-internal — most likely Board-level "critical
  information asset").
- **Evidence quote:** "The Board ... is ultimately responsible for the
  information security of the entity." [apra-cps-234-2019]
- **Paragraph:** §13.

### CPS234-§14 — Defined information-security roles
- **What it requires:** Roles and responsibilities of Board, senior
  management, governing bodies and individuals for decision-making,
  approval, oversight and operations must be clearly defined.
- **UCs:** UC-N-002, UC-N-004, UC-N-009, UC-N-014, UC-N-015.
- **NHIs:** NHI-024, NHI-025, NHI-035 (vault/HSM/CA operator roles
  with explicit RACI), NHI-037.
- **Evidence quote:** "An APRA-regulated entity must clearly define the
  information security-related roles and responsibilities of the Board,
  senior management, governing bodies and individuals." [apra-cps-234-2019]
- **Paragraph:** §14.

### CPS234-§15 — Information-security capability (proportionate)
- **What it requires:** Maintain a capability — totality of resources,
  skills and controls — commensurate with threats and continued sound
  operation. *NHI inventory + lifecycle controls form part of
  "capability".*
- **UCs:** UC-F-004, UC-F-005, UC-F-006, UC-F-007, UC-F-026, UC-N-002,
  UC-N-003, UC-N-005.
- **NHIs:** NHI-001..NHI-037 (entire inventory in scope).
- **Evidence quote:** "Maintain an information security capability
  commensurate with the size and extent of threats to its information
  assets." [apra-cps-234-2019]
- **Paragraph:** §15.

### CPS234-§16 — Assess third-party information-security capability
- **What it requires:** Where information assets are managed by a
  related or third party, assess that party's information-security
  capability commensurate with potential incident consequences.
- **UCs:** UC-N-006, UC-N-007, UC-F-024, UC-F-025.
- **NHIs:** NHI-007, NHI-028, NHI-030, NHI-035 (SaaS-vault control
  plane), NHI-026 (backup SaaS).
- **Evidence quote:** "The APRA-regulated entity must assess the
  information security capability of that party." [apra-cps-234-2019]
- **Paragraph:** §16.

### CPS234-§17 — Active capability maintenance through change
- **What it requires:** Actively maintain capability with respect to
  changes in vulnerabilities, threats, information assets or business
  environment — i.e., NHI sprawl and PQC migration.
- **UCs:** UC-F-006, UC-F-027, UC-N-001, UC-N-003, UC-N-008, UC-N-013.
- **NHIs:** NHI-034 (PQC roadmap), NHI-019 (AI agent emergence),
  NHI-037 (orphan drift).
- **Evidence quote:** "Actively maintain its information security
  capability with respect to changes in vulnerabilities and threats."
  [apra-cps-234-2019]
- **Paragraph:** §17.

### CPS234-§20 — Asset classification by criticality and sensitivity
- **What it requires:** Classify information assets (including those
  managed by third parties) by criticality and sensitivity. Secrets
  tiering inherits this classification.
- **UCs:** UC-F-005, UC-N-002, UC-N-007, UC-N-020.
- **NHIs:** NHI-005, NHI-008, NHI-022, NHI-023, NHI-026.
- **Evidence quote:** "Classify its information assets ... by
  criticality and sensitivity." [apra-cps-234-2019]
- **Paragraph:** §20.

### CPS234-§21 / §21(a)–§21(d) — Implementation of controls
- **What it requires:** Controls protecting information assets,
  implemented in a timely manner, commensurate with (a) vulnerabilities
  and threats, (b) criticality and sensitivity, (c) life-cycle stage,
  (d) incident consequences.
- **UCs:** UC-F-001, UC-F-003, UC-F-004, UC-F-005, UC-F-006, UC-F-008,
  UC-F-009, UC-F-010, UC-F-012, UC-F-016, UC-F-018, UC-F-019, UC-F-020,
  UC-F-021, UC-F-022, UC-F-024.
- **NHIs:** NHI-001, NHI-002, NHI-005, NHI-006, NHI-007, NHI-008,
  NHI-011, NHI-015, NHI-017, NHI-018, NHI-022, NHI-023, NHI-024,
  NHI-026, NHI-028, NHI-031.
- **Evidence quote:** "Information security controls ... implemented in
  a timely manner and ... commensurate with vulnerabilities and threats
  to the information assets." [apra-cps-234-2019]
- **Paragraph:** §21 (and §21(a)–(d)).

### CPS234-§22 — Evaluate design of third-party controls
- **What it requires:** Evaluate the design of related/third-party
  controls that protect the entity's information assets — applies to
  every SaaS vault, SaaS NHIDR/discovery tool, and emerging-vendor
  cloud-native broker the PRD evaluates.
- **UCs:** UC-N-006, UC-N-007, UC-N-014, UC-F-024, UC-F-025.
- **NHIs:** NHI-007, NHI-028, NHI-030, NHI-035, NHI-026.
- **Evidence quote:** "Evaluate the design of that party's information
  security controls that protects the information assets of the
  APRA-regulated entity." [apra-cps-234-2019]
- **Paragraph:** §22.

### CPS234-§23 — Detect and respond mechanisms
- **What it requires:** Robust detection and response mechanisms for
  information-security incidents in a timely manner. NHI-leak and
  anomalous-credential detection is in scope.
- **UCs:** UC-F-001, UC-F-002, UC-F-007, UC-N-001, UC-N-011, UC-N-017,
  UC-N-019.
- **NHIs:** NHI-007, NHI-008, NHI-010, NHI-019, NHI-030, NHI-037.
- **Evidence quote:** "Robust mechanisms in place to detect and respond
  to information security incidents in a timely manner."
  [apra-cps-234-2019]
- **Paragraph:** §23.

### CPS234-§24 / §25 / §26 — Response plans, escalation, annual testing
- **What it requires:** Maintain response plans for plausible incidents,
  with escalation to the Board, and annually review and test.
- **UCs:** UC-F-007, UC-N-010, UC-N-011, UC-N-019.
- **NHIs:** NHI-024, NHI-025, NHI-035, NHI-037.
- **Evidence quote:** "Annually review and test its information
  security response plans to ensure they remain effective and
  fit-for-purpose." [apra-cps-234-2019]
- **Paragraph:** §24–§26.

### CPS234-§27 / §27(a)–§27(e) — Systematic testing of control effectiveness
- **What it requires:** Test control effectiveness through a systematic
  programme commensurate with threat-change rate, criticality, incident
  consequences, untrusted-environment exposure, and rate of change to
  information assets.
- **UCs:** UC-N-003, UC-N-005, UC-N-010, UC-F-006, UC-F-007, UC-F-021,
  UC-F-026.
- **NHIs:** NHI-001, NHI-006, NHI-012, NHI-022, NHI-024, NHI-026,
  NHI-035.
- **Evidence quote:** "Test the effectiveness of its information
  security controls through a systematic testing program."
  [apra-cps-234-2019]
- **Paragraph:** §27.

### CPS234-§28 — Assess sufficiency of third-party control testing
- **What it requires:** Where reliant on third-party testing, assess
  whether nature and frequency are commensurate with §27(a)–(e).
- **UCs:** UC-N-006, UC-N-007, UC-N-014.
- **NHIs:** NHI-007, NHI-028, NHI-030, NHI-035.
- **Evidence quote:** "Assess whether the nature and frequency of
  testing of controls ... is commensurate with paragraphs 27(a) to
  27(e)." [apra-cps-234-2019]
- **Paragraph:** §28.

### CPS234-§29 / §30 / §31 — Escalation, independent specialists, sufficiency review
- **What it requires:** Escalate untimely-remediation results to the
  Board; ensure testing by appropriately skilled functionally
  independent specialists; review programme sufficiency at least
  annually.
- **UCs:** UC-N-009, UC-N-010, UC-N-011, UC-N-014.
- **NHIs:** NHI-024, NHI-025, NHI-035.
- **Evidence quote:** "Testing is conducted by appropriately skilled
  and functionally independent specialists." [apra-cps-234-2019]
- **Paragraph:** §30 (and §29 / §31).

### CPS234-§32 / §33 / §34 — Internal audit (incl. third-party assurance)
- **What it requires:** Internal audit must review design and operating
  effectiveness of controls (including third-party); reviewers must be
  appropriately skilled; internal audit must assess third-party
  assurance where material risk exists.
- **UCs:** UC-N-004, UC-N-009, UC-N-014, UC-N-020.
- **NHIs:** NHI-022, NHI-026, NHI-028, NHI-035.
- **Evidence quote:** "Internal audit activities must include a review
  of the design and operating effectiveness of information security
  controls." [apra-cps-234-2019]
- **Paragraph:** §32–§34.

### CPS234-§35 / §35(a) / §35(b) — 72-hour APRA notification of material incident
- **What it requires:** Notify APRA as soon as possible and no later
  than **72 hours** after becoming aware of a material incident or one
  notified to another regulator.
- **UCs:** UC-F-007, UC-N-001, UC-N-011, UC-N-019.
- **NHIs:** NHI-001, NHI-007, NHI-008, NHI-019, NHI-026, NHI-035,
  NHI-037.
- **Evidence quote:** "Notify APRA ... no later than 72 hours, after
  becoming aware of an information security incident that ... materially
  affected ... the entity." [apra-cps-234-2019]
- **Paragraph:** §35.

### CPS234-§36 — 10-business-day notification of material control weakness
- **What it requires:** Notify APRA within 10 business days of becoming
  aware of a material weakness that cannot be remediated in a timely
  manner — e.g., a vault root-token mis-management or unremediated
  long-lived secret class.
- **UCs:** UC-N-009, UC-N-011, UC-N-020.
- **NHIs:** NHI-012, NHI-022, NHI-029, NHI-037.
- **Evidence quote:** "Notify APRA ... no later than 10 business days,
  after it becomes aware of a material information security control
  weakness which the entity expects it will not be able to remediate in
  a timely manner." [apra-cps-234-2019]
- **Paragraph:** §36.

### CPS230-§15 — Service-provider prudential dependency gate
- **What it requires:** Entity must not rely on a service provider
  unless it can ensure prudential obligations are continuously met —
  gates SaaS-vault and SaaS NHIDR adoption.
- **UCs:** UC-N-006, UC-N-007, UC-N-014.
- **NHIs:** NHI-007, NHI-035, NHI-026.
- **Evidence quote:** "Must not rely on a service provider unless it
  can ensure that ... it can continue to meet its prudential obligations
  in full." [apra-cps-230-2025]
- **Paragraph:** §15.

### CPS230-§25 — Sound IT capability + cross-reference to CPS 234
- **What it requires:** Sound IT capability for current and projected
  business requirements; monitor age and health of information assets;
  meet CPS 234 information-security requirements.
- **UCs:** UC-N-005, UC-N-013, UC-N-014, UC-F-026.
- **NHIs:** NHI-022, NHI-034, NHI-035.
- **Evidence quote:** "Monitor the age and health of its information
  assets and meet the requirements for information security in
  Prudential Standard CPS 234." [apra-cps-230-2025]
- **Paragraph:** §25.

### CPS230-§42 — 24-hour BCP-breach notification (vault outage)
- **What it requires:** Notify APRA within 24 hours of a critical-
  operation disruption outside tolerance. A failed vault, KMS or PKI
  outage can cascade into payments/clearing critical-operation breach.
- **UCs:** UC-F-026, UC-N-007, UC-N-011.
- **NHIs:** NHI-023, NHI-024, NHI-025, NHI-035.
- **Evidence quote:** "Notify APRA ... not later than 24 hours after,
  if it has suffered a disruption to a critical operation outside
  tolerance." [apra-cps-230-2025]
- **Paragraph:** §42.

### CPS230-§47–§54 — Service-provider policy + formal agreement
- **What it requires:** Maintain a service-provider management policy;
  for every material arrangement maintain a formal legally-binding
  agreement covering audit access, sub-contracting, termination, force
  majeure, APRA access.
- **UCs:** UC-N-006, UC-N-007, UC-N-014, UC-F-025.
- **NHIs:** NHI-007, NHI-030, NHI-035, NHI-026.
- **Evidence quote:** "Maintain a comprehensive service provider
  management policy ... a formal legally binding agreement." [apra-cps-230-2025]
- **Paragraph:** §47 / §54.

### CPS230-§59(b) — Material offshoring pre-notification
- **What it requires:** Pre-notify APRA before entering a material
  offshoring arrangement — every US/EU-hosted SaaS vault or NHIDR
  vendor (Doppler, Infisical, 1Password, Astrix, Entro, Oasis, Aembit,
  Clutch) the PRD evaluates is in scope.
- **UCs:** UC-N-007, UC-N-014, UC-N-006.
- **NHIs:** NHI-007, NHI-030, NHI-035.
- **Evidence quote:** "Prior to entering into any material offshoring
  arrangement ... where data or personnel ... will be located offshore."
  [apra-cps-230-2025]
- **Paragraph:** §59(b).

### CPG234-Att-C/D/E — Identity/AM, crypto-key management, third-party guidance
- **What it requires:** Practice-guide expectations for identity and
  access management hygiene, cryptographic key management (lifecycle,
  separation, rotation), and third-party assurance.
- **UCs:** UC-F-006, UC-F-013, UC-F-020, UC-F-024, UC-N-002, UC-N-010,
  UC-N-013.
- **NHIs:** NHI-006, NHI-012, NHI-022, NHI-023, NHI-024, NHI-025,
  NHI-034.
- **Evidence quote (guidance):** "Robust identification and
  authentication ... cryptographic key management." [apra-cpg-234-2019]
- **Paragraph:** Attachments C–E (non-binding guidance).

## 4. Reverse map: UCs missing coverage

All 27 functional and 20 non-functional UCs back-map to at least one
CPS 234 / CPS 230 paragraph because the standard's outcome language
("information security capability ... commensurate ...") is broad enough
to cover every UC in the catalog. The following UCs sit only in CPS 234
*by inference* (no explicit paragraph names them) and are flagged for
PRD §6 evidence-quality review:

- **UC-F-016** (keyless signing) and **UC-N-012** (SLSA reporting) —
  covered only by §21 (life-cycle stage) + §17 (active maintenance);
  the standard predates Sigstore.
- **UC-F-017 / UC-F-018 / UC-N-018 / UC-N-019** (TEE attestation, AI
  agents) — covered only at the §15 capability and §17 active-
  maintenance level; no direct paragraph for confidential-computing or
  AI agent identity.
- **UC-F-019 / UC-N-016** (IoT/OT/branch) — covered by §20 (asset
  classification) but never explicitly enumerated.
- **UC-N-013** (PQC readiness) — covered only via §17 and §27(a)
  ("rate at which vulnerabilities and threats change").

This is a **scope difference**, not a research gap — CPS 234 is
intentionally technology-neutral.

## 5. Outcome-lens cross-references

CPS 234 is **back-mapped** onto the PRD's primary lens (Essential 8 +
NIST SP 800-207 ZT):

- §13–§14 (Board + roles) ↔ ZT-Pillar-Governance and the E8 maturity
  scorecard owner role (UC-N-005, UC-N-015).
- §15–§17 (capability) ↔ E8-RAP and E8-MFA service-account hygiene plus
  ZT-Pillar-Identity / ZT-Pillar-Automation-Orchestration.
- §21 (controls) ↔ all eight E8 mitigations and all seven ZT pillars
  (the load-bearing back-map).
- §16 / §22 / §28 / §34 (third party) ↔ ZT-Pillar-Governance and
  CPS230-§47–§59(b) — the material-offshoring spine that constrains
  SaaS-vault and emerging-vendor adoption.
- §27 (testing) ↔ E8 maturity assessment + ZT continuous-validation
  posture (UC-N-005, UC-N-010).
- §35–§36 (notification) ↔ ZT-Pillar-Visibility-Analytics and
  E8-RAP-LOG / E8-RB observability (UC-N-011).

The CPS 234 back-map is **necessary but not sufficient** for the FI
audience: the standard is outcome-language and an FI's regulator-audit
pack must cite both the paragraph (CPS 234) and the prescriptive
maturity item (E8 ML1/2/3 or ZT-Pillar-X) that evidences it. The
regulatory-trace CSV preserves both.

## 6. Open questions

- The Agent 04 dispatch prompt referenced **"§28a–§28e"** (security
  capability) and **"§35a–§35c"** (incident detection/response/
  assessment), but the published CPS 234 standard numbers its
  sub-paragraphs as **§21(a)–(d)** (implementation of controls) and
  **§27(a)–(e)** (testing); incident management lives at §23–§26, and
  §35 has only sub-paragraphs (a) and (b). This mapping uses the
  **actual** standard paragraph numbering. Confirm with the PRD owner
  whether downstream artefacts (matrix, PRD §5) should adopt the
  standard's numbering (recommended) or retain the original prompt
  shorthand for backwards-compatibility.
- **AI-agent NHIs (NHI-019, UC-F-018, UC-N-019)** — does the Board
  treat AI-agent prompt-injection-driven credential abuse as a §13
  Board-level risk in v0.1, or defer to v1.0 PRD?
- **CPG 234 weight** — is the practice-guide Attachment D
  cryptographic-key-management table evidence-quality enough to
  underpin UC-N-013 (PQC readiness), or must the PRD reference NIST
  FIPS 203/204/205 + ASD PQC guidance as primary?
- **CPS 230 §59(b) offshoring pre-notification** — confirm legal /
  compliance interpretation for *every* SaaS vault and NHIDR vendor
  evaluated. The 12-vendor matrix includes 6 SaaS-only US-hosted
  products with no AU region today.
- **CPS 234 §16 vs §22 distinction** for emerging-vendor risk — Agent 03
  flagged Astrix / Entro / Oasis / Aembit / Clutch as having *no AU
  data residency / IRAP* (material §22 + CPS230 §53 finding); confirm
  with vendor-risk owner whether v0.1 PRD accepts any of these as
  "evaluate-pilot-only" or all must be deferred until AU presence.
- **CPS 234 §35 72-hour clock** — define which secrets-management
  signals trigger the clock (token mass-revocation, vault seal failure,
  HSM quorum-loss). UC-F-007 + UC-N-011 acceptance criteria should
  reflect this.

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under section **"APRA CPS
234 (Agent 04 — regulatory)"**:

- `apra-cps-234-2019` — CPS 234 Information Security (July 2019).
- `apra-cps-230-2025` — CPS 230 Operational Risk Management (July 2025,
  in force 1 July 2025).
- `apra-cpg-234-2019` — CPG 234 Information Security Practice Guide
  (June 2019).
- `apra-info-sec-hub-2026` — APRA Information Security policy hub
  landing page.
- `apra-cps-230-2023-finalisation` — APRA media release / FAQ noting
  CPS 230's secrets-management interaction with CPS 234 §25.

Pre-existing keys reused: `apra-cps-234-2019`, `apra-cps-230-2023`,
`nist-csf-2.0-2024`, `csa-nhi-taxonomy-2024`, `nist-sp-800-204d-2024`.

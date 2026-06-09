# IGA Governed-Identity & Entitlement Taxonomy — ANZ Posture-Assessment Instrument (Phase 3, IGA domain)

**Sensitivity:** [PUBLIC] — independent of any client-specific evidence.
**Author:** IGA Identity Taxonomist sub-agent (Opus 4.8, 1M), 2026-06-09.
**Version:** v0.1 (Phase 3 IGA build input).
**Jurisdiction:** AU-primary (APRA CPS 234, ASD ISM / Essential Eight) + NIST SP 800-53r5 (AC family), ISO/IEC 27001:2022 Annex A.5, SOX §404 (SoD).
**Status of citations:** Every control quote below was fetched from a primary/authoritative source and verified verbatim during authoring (see §6). Where a control's *exact statutory wording* could not be machine-verified, it is flagged `[UNVERIFIED]` inline and **omitted** from the returned citations array.

---

## 1. Scope and how this differs from the PAM/NHI catalog

The PAM domain's identity catalog (`../identity-taxonomy.md`, NHI-001..037) enumerates **non-human / machine** identities and the *secrets* that authenticate them. The IGA domain governs a different population: **workforce (human) identities and the entitlements/roles assigned to them**, plus the **governance roles** (owners, approvers, certifiers) that the IGA process itself depends on, plus an **emerging machine-governance edge** where non-human actors (agentic-AI, OAuth apps) increasingly need *governance-grade* lifecycle, ownership, certification and revocation — not just a vaulted secret.

The instrument scores **process maturity, not tool deployment** (per the instrument-review methodology, dimension A1). So each class below is framed around the *governance question* it forces: who owns it, how is it provisioned/recertified/revoked, and what happens at the joiner/mover/leaver (JML) transitions.

### 1.1 Classification axes

Each class carries:

- **ID** — `IGID-001..` (stable; do not renumber).
- **bucket** — `COMMON` (every IGA programme must address it) or `EMERGING` (2026 frontier the review methodology, dimension B8, explicitly demands).
- **short_name** — label for CSV / rubric columns.
- **lifecycle** — dominant JML pattern: `JOINER` / `MOVER` / `LEAVER` / `STATIC` (governance-role or birthright objects that persist and are recertified rather than JML-driven). Most workforce identities traverse all of JOINER→MOVER→LEAVER; the tag marks the transition where *governance risk concentrates*.
- **governance_maturity** — industry-typical maturity (`LOW`/`MED`/`HIGH`) for how well ownership, entitlement assignment, recertification and revocation are *programmatically* controlled. Most regulated FIs sit LOW–MED outside the finance-SoD and privileged tiers.
- **typical_entitlements** — representative access this class holds.
- **citation keys** — control hooks (see §5/§6).

### 1.2 Control anchors common to almost every class

These recur, so they are stated once:

- **NIST AC-2 (Account Management)** binds the whole JML lifecycle: it requires the org to *"Create, enable, modify, disable, and remove accounts in accordance with [organization-defined] policy, procedures, prerequisites, and criteria"* and to notify account managers *"when accounts are no longer required"*, *"when users are terminated or transferred"*, and *"when system usage or need-to-know changes"* [nist-sp-800-53-ac2].
- **NIST AC-6 (Least Privilege)** governs entitlement *right-sizing*: *"Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks"* [nist-sp-800-53-ac6].
- **NIST AC-5 (Separation of Duties)** governs SoD design: *"Identify and document [organization-defined duties of individuals]; and Define system access authorizations to support separation of duties"* [nist-sp-800-53-ac5].
- **ISO/IEC 27001:2022 Annex A 5.18 (Access Rights)** governs the provision→review→revoke loop: access rights are to be *provisioned, reviewed, modified and removed in accordance with the organisation's policy and rules for access control* [iso-27001-a518].
- **APRA CPS 234 ¶21 (Implementation of controls)** is the binding AU prudential hook: *"An APRA-regulated entity must have information security controls to protect its information assets … that are implemented in a timely manner and that are commensurate with: (a) vulnerabilities and threats to the information assets; (b) the criticality and sensitivity …"* [apra-cps234].
- **SOX §404** is the binding driver for finance-relevant SoD/ICFR classes (see IGID-008): management must maintain *"an adequate internal control structure and procedures for financial reporting"* and assess its effectiveness [sox-404].

Per-class citation lists below add the *distinguishing* control(s); the anchors above are implied for every COMMON workforce class.

---

## 2. COMMON governed-identity classes (the workforce + governance-role core)

### IGID-001 — Workforce joiner (new starter) `[COMMON]`
- **short_name:** Joiner / new starter
- **description:** A newly hired employee whose identity is created and provisioned with *birthright* access at onboarding. The governance risk is the *correctness and timeliness* of initial entitlement grant — over-provisioning at the joiner stage is the seed of every later least-privilege drift finding.
- **typical_entitlements:** Birthright bundle (email, directory, VPN, collaboration suite, baseline business apps), department/role-based access requested via access-request workflow.
- **lifecycle:** `JOINER`
- **governance_maturity:** MED (HR-driven joiner is the most automated JML transition; birthright accuracy is the weak point).
- **citations:** [nist-sp-800-53-ac2], [iso-27001-a518], [apra-cps234].

### IGID-002 — Workforce mover (role/department change) `[COMMON]`
- **short_name:** Mover / transfer
- **description:** An existing identity changing role, team, manager, location or employment type. The governance risk is **access accretion / privilege creep**: movers accumulate entitlements from prior roles that are never removed — the single most common audit finding and the explicit harm ISO A.5.18 calls out (degraded/transferred staff retaining escalated rights).
- **typical_entitlements:** Old-role + new-role entitlements concurrently (the defect); should be net of removed prior-role access.
- **lifecycle:** `MOVER`
- **governance_maturity:** LOW (mover detection and prior-access removal is the least-automated JML transition in most FIs).
- **citations:** [nist-sp-800-53-ac6], [nist-sp-800-53-ac2], [iso-27001-a518].

### IGID-003 — Workforce leaver / terminated identity `[COMMON]`
- **short_name:** Leaver / terminated
- **description:** A departing employee (resignation, termination, end of contract). Governance risk is **timely, complete deprovisioning** across all systems — especially federated SaaS and standing tokens that survive directory disable. AC-2 explicitly requires notification *"when users are terminated or transferred"* within a defined time period.
- **typical_entitlements:** All access from the active lifecycle, pending revocation; residual risk in SaaS sessions, OAuth refresh tokens, cached creds.
- **lifecycle:** `LEAVER`
- **governance_maturity:** MED for directory disable; LOW for downstream/federated revocation completeness.
- **citations:** [nist-sp-800-53-ac2], [iso-27001-a518], [apra-cps234].

### IGID-004 — Contractor / third-party / vendor identity `[COMMON]`
- **short_name:** Contractor / third-party
- **description:** Non-employee workforce: contractors, consultants, outsourced run teams, partner/vendor staff with internal access. Governance risk is **sponsorship and time-bounding** — these identities lack an HR feed, so they default to no automatic leaver event; CPS 234 extends the entity's control obligation to *"information assets managed by related parties or third parties"* [apra-cps234].
- **typical_entitlements:** Scoped project access, often privileged remote access; frequently no defined expiry.
- **lifecycle:** `JOINER`→`LEAVER` (sponsor-driven, time-boxed).
- **governance_maturity:** LOW (no authoritative HR source; expiry and recertification frequently absent).
- **citations:** [apra-cps234], [nist-sp-800-53-ac2], [iso-27001-a518].

### IGID-005 — Privileged business user `[COMMON]`
- **short_name:** Privileged business user
- **description:** A workforce identity holding *high-impact business entitlements* (not infrastructure admin — that is PAM's domain) — e.g. payments approver, customer-data bulk-export, fraud-override, GL-posting, super-user roles in core banking / ERP. Governance risk is the **frequency and rigour of recertification** and SoD enforcement; ISO A.5.18 requires privileged access rights be reviewed *more frequently* given higher risk.
- **typical_entitlements:** Business super-user / maker-checker-override roles, bulk data access, financial transaction authority.
- **lifecycle:** `MOVER` (privilege most often acquired/changed via role moves; recertified on a cycle).
- **governance_maturity:** MED (privileged tier usually receives the most attention; depth of recert varies).
- **citations:** [nist-sp-800-53-ac6], [iso-27001-a518], [apra-cps234].

### IGID-006 — Application / system owner `[COMMON]`
- **short_name:** Application owner
- **description:** A governance *role*, not an end-user access pattern: the accountable owner of an application/system who must approve access requests to it and attest its entitlement model. Governance risk is **ownership coverage and currency** — orphaned applications with no owner cannot be governed, certified, or have access decisions made for them.
- **typical_entitlements:** Approval authority over the app's entitlements; data-classification accountability; recertification-campaign respondent.
- **lifecycle:** `STATIC` (a standing governance assignment, itself recertified).
- **governance_maturity:** MED (large estates routinely have a long tail of owner-less applications).
- **citations:** [nist-sp-800-53-ac2], [iso-27001-a518], [apra-cps234].

### IGID-007 — Role owner / entitlement owner `[COMMON]`
- **short_name:** Role owner
- **description:** The governance role accountable for a *business or technical role definition* (RBAC role) — its membership rules, contained entitlements, and SoD constraints. Governance risk is **role hygiene**: stale role definitions, role explosion, and roles that silently bundle toxic entitlement combinations. AC-2 requires *"prerequisites and criteria for group and role membership."*
- **typical_entitlements:** Authority to define/modify role contents and membership criteria; role-recertification respondent.
- **lifecycle:** `STATIC`
- **governance_maturity:** LOW–MED (role mining/cleanup and ongoing role governance are immature in most FIs).
- **citations:** [nist-sp-800-53-ac2], [nist-sp-800-53-ac5].

### IGID-008 — Segregation-sensitive finance role (SoD-controlled) `[COMMON]`
- **short_name:** SoD-sensitive finance role
- **description:** A workforce identity holding entitlements that are *individually legitimate but collectively toxic* under SoD — e.g. vendor-master maintenance + payment-run, or journal-entry + journal-approval. This is the **SOX/ICFR-critical** class: the assessment must detect SoD conflicts, not just provision access. AC-5 requires defining *"system access authorizations to support separation of duties"*; SOX §404 makes the financial-reporting control structure a board-level statutory obligation.
- **typical_entitlements:** Conflicting financial-process entitlements (P2P, O2C, R2R, treasury); mitigated by compensating controls where conflicts are accepted.
- **lifecycle:** `MOVER` (conflicts most often introduced by role moves; continuously monitored).
- **governance_maturity:** MED–HIGH where SOX-scoped (highest-governed business class); LOW outside SOX scope.
- **citations:** [nist-sp-800-53-ac5], [sox-404], [apra-cps234].

### IGID-009 — Service account under IGA governance `[COMMON]`
- **short_name:** Governed service account
- **description:** A non-human / functional account that IGA governs **as a first-class object** — with a named human owner, a defined purpose, recertification, and a deprovisioning trigger — rather than leaving it to PAM/secrets vaulting alone. This is the IGA-side complement to the PAM NHI catalog (cf. NHI-012/NHI-029): the governance defect is **ownerless, never-recertified, never-expiring** service accounts. AC-2 permits shared/group accounts only where they *"meet [organization-defined] conditions."*
- **typical_entitlements:** Application-to-application access, batch/integration privileges, often standing and over-scoped.
- **lifecycle:** `STATIC` (governed via ownership + recertification, not JML).
- **governance_maturity:** LOW (ownership attribution and recertification of service accounts is a near-universal gap).
- **citations:** [nist-sp-800-53-ac2], [nist-sp-800-53-ac6], [apra-cps234].

### IGID-010 — Birthright / role-based access holder `[COMMON]`
- **short_name:** Birthright / RBAC holder
- **description:** Any identity receiving access *automatically* by virtue of an attribute (department, job code, location) via birthright policy or RBAC assignment, with no per-request approval. Governance risk is **over-broad birthright scope** — automation that grants too much by default and is rarely re-examined. AC-2 frames this via *"prerequisites and criteria for group and role membership"* and access *"based on … intended system usage."*
- **typical_entitlements:** Attribute-driven default bundles; RBAC role memberships.
- **lifecycle:** `JOINER` (granted at onboarding/attribute change; recertified in campaigns).
- **governance_maturity:** MED (automation exists; *correctness* of the birthright model is under-reviewed).
- **citations:** [nist-sp-800-53-ac2], [nist-sp-800-53-ac6], [iso-27001-a518].

### IGID-011 — Dormant / orphan account `[COMMON]`
- **short_name:** Dormant / orphan account
- **description:** An account that is inactive (dormant — unused beyond a threshold) or has no valid owner/identity behind it (orphan — e.g. survived a leaver, or a service account whose owning app was decommissioned). The single highest-value *attestation finding* class and a prime lateral-movement target. AC-2 enhancement requires disabling accounts that *"Have expired; Are no longer associated with a user or individual; … or Have been inactive for [organization-defined time period]."*
- **typical_entitlements:** Whatever the account last held — rarely re-reviewed, often still privileged.
- **lifecycle:** `LEAVER` (the governance goal is detection→disable→remove).
- **governance_maturity:** LOW (surfaced only by periodic attestation/recon sweeps; remediation lags detection).
- **citations:** [nist-sp-800-53-ac2], [iso-27001-a518].

---

## 3. EMERGING governed-identity classes (the 2026 frontier the review methodology demands)

> These are the classes the instrument-review methodology (dimension **B8**, "2026 headline" red flags) requires the IGA domain to cover or be marked currency-deficient. Each is grounded in a current, dated source.

### IGID-012 — Agentic-AI / autonomous-agent identity `[EMERGING]`
- **short_name:** Agentic-AI / autonomous agent
- **description:** An LLM-driven autonomous agent that calls functions/tools and acts on systems with a *degree of delegated agency*, on behalf of a user or a business process. From an IGA seat this is a **new governed object**: it needs an owner, a scoped and recertified entitlement set, a "purpose", least-privilege tool access, human-in-the-loop gates on irreversible actions, and a deprovisioning trigger — i.e. JML-style governance applied to a non-human actor whose permissions can change dynamically. OWASP frames the core risk as **Excessive Agency**: *"An LLM-based system is often granted a degree of agency by its developer – the ability to call functions or interface with other systems via extensions … to undertake actions in response to a prompt"*, and *"Excessive Agency is the vulnerability that enables damaging actions to be performed in response to unexpected, ambiguous or manipulated outputs from an LLM"*, with root causes of *"excessive functionality; excessive permissions; excessive autonomy"* [owasp-llm06-2025]. NIST AC-6 already extends least privilege to *"processes acting on behalf of users"* — the standards hook exists; the governance practice is nascent [nist-sp-800-53-ac6].
- **typical_entitlements:** Tool/extension scopes, downstream API permissions, often inherited via an over-privileged service account or an OAuth session broader than the task requires (OWASP's recommended mitigation is a *read-only-scope OAuth session* and *human review of irreversible actions*) [owasp-llm06-2025].
- **lifecycle:** `STATIC` (deployed and owned; entitlements and autonomy bounds recertified) — but with dynamic permission change that defeats classic point-in-time recert.
- **governance_maturity:** LOW (most FIs have no agent inventory, owner model, or recertification for autonomous agents as of 2026).
- **citations:** [owasp-llm06-2025], [nist-sp-800-53-ac6], [apra-cps234].

### IGID-013 — OAuth app / over-scoped consent-grant identity (Midnight-Blizzard pattern) `[EMERGING]`
- **short_name:** OAuth app / consent-grant
- **description:** A registered OAuth application / service principal operating against tenant data under **delegated or admin-consented scopes** — and the standing **consent grants** themselves as governed objects. The governance risk is **over-scoped, un-owned, never-recertified consent** that confers durable, account-independent access. This is the explicit "Midnight-Blizzard pattern" the review methodology names: Microsoft reported the actor *"leveraged their initial access to identify and compromise a legacy test OAuth application that had elevated access to the Microsoft corporate environment. The actor created additional malicious OAuth applications. They created a new user account to grant consent … to the actor controlled malicious OAuth applications"*, and Microsoft notes *"The misuse of OAuth also enables threat actors to maintain access to applications, even if they lose access to the initially compromised account"* [ms-midnight-blizzard-2024]. IGA must inventory app registrations, attribute owners, certify consent grants, flag high-risk scopes (e.g. `full_access_as_app`), and revoke on leaver/decommission — AC-6 least privilege and AC-2 account/role criteria are the standards hooks.
- **typical_entitlements:** Delegated/application OAuth scopes (Graph, Exchange `full_access_as_app`, etc.), refresh tokens, app-role assignments — frequently far broader than function requires.
- **lifecycle:** `STATIC` (app registration + consent persist; must be owned, certified, and revoked on decommission) — survives the JML of any human who created it.
- **governance_maturity:** LOW (consent-grant inventory, ownership and recertification are rare; the class is largely invisible to traditional IGA).
- **citations:** [ms-midnight-blizzard-2024], [nist-sp-800-53-ac6], [nist-sp-800-53-ac2], [apra-cps234].

---

## 4. Cross-cutting governance notes

- **The MOVER transition is where least-privilege dies.** Joiner and leaver are HR-eventable; the mover (IGID-002) is the silent accumulator. Privilege-creep on movers (IGID-002 + IGID-005) and SoD conflicts introduced by moves (IGID-008) are the recurring high-consequence findings — weight them accordingly in the rubric (review methodology A4, scoring discrimination).
- **Ownership is the precondition for governance.** IGID-006/007 (app/role owners) are *enabling* governance roles: an owner-less application (IGID-006 gap) or role (IGID-007 gap) cannot be certified, so its end-user entitlements (IGID-005/008/010) are ungovernable by construction. Score ownership coverage as a gating control.
- **The emerging classes break point-in-time recertification.** Both IGID-012 (dynamic agent permissions) and IGID-013 (durable consent grants that outlive their creator) defeat the annual-campaign model. The instrument should treat *continuous* detection/attestation as the "good" end-state for these, not a yearly review — consistent with CPS 234 ¶21's *"implemented in a timely manner"* test [apra-cps234].
- **Dormant/orphan (IGID-011) is a maturity *outcome*, not just a class.** A low orphan/dormant population is evidence that JML (IGID-001/002/003), service-account governance (IGID-009) and consent-grant governance (IGID-013) are actually working. It is both a row and a KPI.
- **AU jurisdiction boundary.** Control hooks here are AU-binding (CPS 234) + internationally recognised (NIST/ISO/SOX). Other jurisdictions are data-swaps, not validated coverage (review methodology C15).

---

## 5. Class-to-control summary matrix

| ID | short_name | bucket | lifecycle | gov_maturity | primary control hooks |
|----|-----------|--------|-----------|--------------|------------------------|
| IGID-001 | Workforce joiner | COMMON | JOINER | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-002 | Workforce mover | COMMON | MOVER | LOW | AC-6, AC-2, ISO 5.18 |
| IGID-003 | Workforce leaver | COMMON | LEAVER | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-004 | Contractor / third-party | COMMON | JOINER→LEAVER | LOW | CPS 234, AC-2, ISO 5.18 |
| IGID-005 | Privileged business user | COMMON | MOVER | MED | AC-6, ISO 5.18, CPS 234 |
| IGID-006 | Application owner | COMMON | STATIC | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-007 | Role owner | COMMON | STATIC | LOW–MED | AC-2, AC-5 |
| IGID-008 | SoD-sensitive finance role | COMMON | MOVER | MED–HIGH (SOX) | AC-5, SOX 404, CPS 234 |
| IGID-009 | Governed service account | COMMON | STATIC | LOW | AC-2, AC-6, CPS 234 |
| IGID-010 | Birthright / RBAC holder | COMMON | JOINER | MED | AC-2, AC-6, ISO 5.18 |
| IGID-011 | Dormant / orphan account | COMMON | LEAVER | LOW | AC-2, ISO 5.18 |
| IGID-012 | Agentic-AI / autonomous agent | EMERGING | STATIC (dynamic) | LOW | OWASP LLM06, AC-6, CPS 234 |
| IGID-013 | OAuth app / consent-grant | EMERGING | STATIC | LOW | MS Midnight Blizzard, AC-6, AC-2, CPS 234 |

---

## 6. Citations (verified verbatim during authoring)

All quotes below were fetched and confirmed against the cited URL on 2026-06-09. Append these BibTeX keys to the project citation file.

- **[nist-sp-800-53-ac2]** — NIST SP 800-53 Rev. 5, AC-2 Account Management.
  URL: https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/
  Verbatim: *"Create, enable, modify, disable, and remove accounts in accordance with [Assignment: organization-defined policy, procedures, prerequisites, and criteria]"* and notify managers *"when accounts are no longer required … when users are terminated or transferred … when system usage or need-to-know changes for an individual."*

- **[nist-sp-800-53-ac5]** — NIST SP 800-53 Rev. 5, AC-5 Separation of Duties.
  URL: https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-5/
  Verbatim: *"Identify and document [Assignment: organization-defined duties of individuals]; and Define system access authorizations to support separation of duties."*

- **[nist-sp-800-53-ac6]** — NIST SP 800-53 Rev. 5, AC-6 Least Privilege.
  URL: https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/
  Verbatim: *"Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks."*

- **[iso-27001-a518]** — ISO/IEC 27001:2022 Annex A Control 5.18 Access Rights (control intent, as published).
  URL: https://www.isms.online/iso-27001/annex-a-2022/5-18-access-rights-2022/
  Verbatim (control intent): *"According to ISO 27001:2022, Annex A Control 5.18 addresses how access rights should be assigned, modified, and revoked based on business requirements"*; privileged access rights *"should be reviewed more frequently in light of the higher risk."*
  Note: the normative one-line wording of A.5.18 ("Access rights … shall be provisioned, reviewed, modified and removed …") is paywalled in the ISO standard itself; the published intent above is quoted from the cited secondary source. The exact standard sentence is treated as `[PARAPHRASE-OF-NORMATIVE]`, not represented as a verbatim ISO quote.

- **[apra-cps234]** — APRA Prudential Standard CPS 234 Information Security (July 2019), ¶21 Implementation of controls + Objectives.
  URL: https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf
  Verbatim (¶21): *"An APRA-regulated entity must have information security controls to protect its information assets, including those managed by related parties and third parties, that are implemented in a timely manner and that are commensurate with: (a) vulnerabilities and threats to the information assets; (b) the criticality and sensitivity …"*
  Verbatim (objective): *"… maintaining an information security capability commensurate with information security vulnerabilities and threats … including information assets managed by related parties or third parties."*

- **[sox-404]** — Sarbanes-Oxley Act of 2002, §404 Management Assessment of Internal Controls (statutory excerpt).
  URL: https://www.sarbanes-oxley-101.com/SOX-404.htm
  Verbatim: *"state the responsibility of management for establishing and maintaining an adequate internal control structure and procedures for financial reporting; and contain an assessment … of the effectiveness of the internal control structure and procedures of the issuer for financial reporting."*

- **[owasp-llm06-2025]** — OWASP Top 10 for LLM Applications (2025), LLM06:2025 Excessive Agency.
  URL: https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  Verbatim: *"An LLM-based system is often granted a degree of agency by its developer – the ability to call functions or interface with other systems via extensions … to undertake actions in response to a prompt."* and *"Excessive Agency is the vulnerability that enables damaging actions to be performed in response to unexpected, ambiguous or manipulated outputs from an LLM"*; root causes *"excessive functionality; excessive permissions; excessive autonomy."*

- **[ms-midnight-blizzard-2024]** — Microsoft Security Blog, "Midnight Blizzard: Guidance for responders on nation-state attack" (25 Jan 2024).
  URL: https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/
  Verbatim: *"Midnight Blizzard leveraged their initial access to identify and compromise a legacy test OAuth application that had elevated access to the Microsoft corporate environment. The actor created additional malicious OAuth applications. They created a new user account to grant consent in the Microsoft corporate environment to the actor controlled malicious OAuth applications."* and *"The misuse of OAuth also enables threat actors to maintain access to applications, even if they lose access to the initially compromised account."*

### Source-confidence notes
- NIST AC-2/AC-5/AC-6 quotes are from the csf.tools mirror, which reproduces SP 800-53r5 control text verbatim; for a primary citation the build agent may substitute the NIST OSCAL/PDF at csrc.nist.gov (control text is identical).
- ISO A.5.18 normative wording is paywalled; only the published *intent* is quoted verbatim, flagged above.
- All other quotes are from primary/authoritative publishers (APRA, Microsoft, OWASP, SOX statutory text).

---

## 7. Citation verification

Adversarial re-verification performed 2026-06-10 by an independent reviewer sub-agent. Each URL was fetched live; each quote was checked character-for-character against the fetched page. Verdicts:

| key | URL resolves | quote faithful | verdict | note |
|-----|--------------|----------------|---------|------|
| nist-sp-800-53-ac2 | yes (HTTP 200) | yes | VERIFIED | Control Statement item 6 matches verbatim, incl. the "Notify account managers … when accounts are no longer required / when users are terminated or transferred / when system usage or need-to-know changes" wording. csf.tools is a faithful SP 800-53r5 mirror; csrc.nist.gov is the primary substitute. |
| nist-sp-800-53-ac5 | yes (HTTP 200) | yes | VERIFIED | Control Statement matches: "Identify and document [Assignment: organization-defined duties of individuals] ; and Define system access authorizations to support separation of duties." (source renders a space before the semicolon; trivial whitespace only). |
| nist-sp-800-53-ac6 | yes (HTTP 200) | yes | VERIFIED | Control Statement matches verbatim, incl. "(or processes acting on behalf of users)". |
| iso-27001-a518 | yes (HTTP 200) | yes (as secondary-source intent, not normative ISO text) | VERIFIED | The sentence "According to ISO 27001:2022, Annex A Control 5.18 addresses how access rights should be assigned, modified, and revoked based on business requirements" appears verbatim on isms.online. The "reviewed more frequently in light of the higher risk" paraphrase is also supported on the page. Correctly flagged in §6 as published intent, NOT verbatim ISO normative wording (which is paywalled). |
| apra-cps234 | yes (HTTP 200 on the July-2019 PDF) | yes | VERIFIED | ¶21 "Implementation of controls" text matches verbatim against APRA's authoritative wording ("…controls to protect its information assets, including those managed by related parties and third parties, that are implemented in a timely manner and that are commensurate with: (a) vulnerabilities and threats…; (b) the criticality and sensitivity…"). Cross-checked against the APRA handbook (handbook.apra.gov.au/standard/cps-234); identical wording. |
| sox-404 | yes (HTTP 200) | yes | VERIFIED | The §404(a) statutory excerpt matches verbatim. sarbanes-oxley-101.com is a secondary host but reproduces the statutory text accurately; the U.S. Code (15 U.S.C. §7262) is the primary substitute. |
| owasp-llm06-2025 | yes (HTTP 200) | yes | VERIFIED | All three quoted fragments match verbatim (agency definition, "Excessive Agency is the vulnerability…", and the "excessive functionality; excessive permissions; excessive autonomy" root-cause list). |
| ms-midnight-blizzard-2024 | yes (HTTP 200) | yes | VERIFIED | Both quotes match verbatim on the Microsoft Security Blog, incl. "leveraged their initial access to identify and compromise a legacy test OAuth application…" and "The misuse of OAuth also enables threat actors to maintain access to applications, even if they lose access to the initially compromised account." |

**Outcome:** 8/8 VERIFIED. No SUSPECT or FABRICATED citations. No citations removed.

Residual caveats (do not block use, but note for primary-source upgrade):
- AC-2/AC-5/AC-6 cite the csf.tools mirror rather than csrc.nist.gov — substance is identical; upgrade to the NIST primary if a same-domain-as-register citation is required.
- iso-27001-a518 is a secondary-source intent quote, not normative ISO text — this is already disclosed in §6 and must remain disclosed wherever the quote is reused.
- apra-cps234 quote was confirmed against both the cited July-2019 PDF and the APRA handbook HTML; either is authoritative (apra.gov.au).
- sox-404 cites a secondary host (sarbanes-oxley-101.com); the quote is statutorily accurate but a build agent should prefer the U.S. Code / GovInfo primary for a regulated-FI deliverable.

# IGA Research — Joiner / Mover / Leaver (JML) Identity Lifecycle

> **⚠️ ERRATUM (2026-06-10):** the ISM-1591 and ISM-1648 citations below are WRONG controls
> (ISM-1591 = malicious-activity suspension; ISM-1648 = *privileged* 45-day inactivity). Correct
> controls: **ISM-0430** (same-day removal) and **ISM-1404** (unprivileged 45-day). Verified against
> the official cyber.gov.au ISM Dec-2024 PDF — see `docs/superpowers/plans/ws1-verification-notes.md`.
> The shipped trace and registry carry the corrected IDs.

> Domain: Identity Governance & Administration (IGA), Phase 3.
> Jurisdiction: AU-primary (APRA CPS 234, ASD ISM, Essential Eight) + NIST SP 800-53, ISO/IEC 27001:2022, SOX (SoD only).
> Instrument scores **process maturity**, not tool deployment.
> Citation policy: every citation below was fetched and the quote string-matched in the live source on 2026-06-09. Quotes that could not be verbatim-verified from a primary/authoritative source are marked **UNVERIFIED** inline and are excluded from the machine-readable citation array returned to the orchestrator.

---

## Scope and workforce identity populations

The JML area governs the lifecycle of **workforce (human) identities** — employees, contractors, secondees, and temporary staff — across in-scope applications and systems. Distinct in-scope populations used by the use cases below:

- **Joiners**: newly onboarded workforce identities (perm + contractor) requiring initial (birthright) access.
- **Movers**: existing workforce identities undergoing a role/department/manager/location change that should trigger access recalculation.
- **Leavers**: terminating workforce identities (resignation, dismissal, contract end, secondment end) requiring de-provisioning.
- **Orphan / dormant accounts**: existing accounts with no valid owner (orphan) or no recent authentication activity (dormant) across in-scope systems — includes accounts stranded by failed leaver/mover processes.

Privileged/NHI populations are governed by the PAM and Secrets domains; JML covers the *workforce-identity governance process* that feeds them.

---

## Archetype library (for reference)

| ID | Archetype | Shape |
|----|-----------|-------|
| A1 | Control-in-place | A discrete preventive/detective control is present and operating |
| A2 | Migration / threshold | Movement from a legacy pattern to a target pattern past a coverage threshold |
| A3 | Capability-config | A platform capability exists and is configured to a target state |
| A5 | Inventory & attestation | A population is inventoried and periodically attested |
| A7 | Process-maturity | A repeatable, owned, documented process |
| A8 | High-risk sign-off | Explicit accountable sign-off on high-risk items |

---

## Use cases

### UC-JML-01 — Automated joiner / birthright provisioning
- **uc_id mapping**: aligns to spike `UC-I-001` (JML / FUNCTIONAL).
- **Archetype**: **A2 (migration/threshold)** — moving from manual ticket-based account creation to automated, role/birthright-driven provisioning past a coverage threshold.
- **User story**: *As an identity-governance owner, I want new joiners to receive their birthright access automatically from an authoritative HR source based on their role/department, so that staff are productive on day one without manual ticket-based account creation and without over-provisioning.*
- **Workforce population in scope**: joiners (permanent + contractor) created from the authoritative HR/identity source.
- **Acceptance criteria (measurable)**:
  - An authoritative joiner feed (HR system / IdP) triggers provisioning; ≥ the agreed threshold (e.g. 90%) of joiner birthright access is granted via automated role/birthright policy rather than manual tickets.
  - Birthright entitlement sets are defined per role/department and version-controlled.
  - Median time-to-first-access from HR effective-start date is within the documented joiner SLA.
  - Every automated grant is attributable to a role/policy rule and recorded in an immutable audit log.
  - Exceptions (non-birthright access) route through the access-request workflow, not direct provisioning.
- **Outcome lens (risk reduced)**: eliminates ad-hoc manual grants and copy-a-colleague over-provisioning at onboarding; enforces least privilege from day one; removes the joiner backlog that drives shadow/standing access.

### UC-JML-02 — Mover access recalculation on transfer
- **uc_id mapping**: aligns to spike `UC-I-002` (JML / FUNCTIONAL).
- **Archetype**: **A7 (process-maturity)** — a repeatable, owned mover access-recalculation process.
- **User story**: *As an access-governance owner, I want a transferring employee's entitlements to be recalculated against their new role and prior access revoked where no longer justified, so that access does not accumulate (privilege creep) across role changes.*
- **Workforce population in scope**: movers — workforce identities with a detected change of role, department, manager, cost-centre, or location.
- **Acceptance criteria (measurable)**:
  - A documented, owned mover process is triggered by the authoritative HR change event.
  - New-role birthright access is added and prior-role access not justified by the new role is flagged for removal within the documented mover SLA.
  - Manager/owner reaffirmation is required for any retained cross-role access.
  - Privilege-creep is measured: residual access carried across the last N transfers is reported and trending down.
  - The process has a named owner, documented procedure, and exception handling.
- **Outcome lens (risk reduced)**: directly attacks privilege creep / access accretion — the dominant cause of toxic access combinations and excessive blast radius from a compromised account.

### UC-JML-03 — Timely leaver de-provisioning within SLA
- **uc_id mapping**: aligns to spike `UC-I-003` (JML / FUNCTIONAL).
- **Archetype**: **A2 (migration/threshold)** — moving from manual/delayed disablement to automated de-provisioning within SLA past a coverage threshold.
- **User story**: *As a security/IGA owner, I want leaver accounts disabled and access removed within a defined SLA of the termination event from the authoritative source, so that departed staff and contractors cannot retain access and standing credentials cannot be abused.*
- **Workforce population in scope**: leavers — resignations, dismissals, contract/secondment ends.
- **Acceptance criteria (measurable)**:
  - Termination events from the authoritative HR source trigger automated disable/revoke; ≥ the agreed threshold of leaver events are de-provisioned via the automated path.
  - Same-day (or tighter SLA) disablement is met for ≥ the agreed % of leaver events; SLA breaches are reported with root cause. (ASD ISM ISM-1591 sets a same-day expectation — see Regulatory mapping.)
  - High-risk/privileged leaver access is prioritised and disabled first.
  - A leaver SLA report shows distribution of termination-event-to-disable time and breach exceptions.
  - Federated/SaaS and on-prem targets are both covered (no de-provisioning gaps).
- **Outcome lens (risk reduced)**: removes standing valid credentials of departed identities — the prime enabler of Valid Accounts (T1078) abuse; closes the insider/ex-insider and credential-resale risk window.

### UC-JML-04 — Orphan / dormant account detection
- **uc_id mapping**: new (extends spike JML set; complements `UC-I-003`).
- **Archetype**: **A5 (inventory & attestation)** — inventory the account population and attest ownership/activity; detect orphans and dormant accounts and route to remediation.
- **User story**: *As an access-governance owner, I want all accounts across in-scope systems reconciled to a valid owner and recent activity, so that orphan (no owner) and dormant (inactive) accounts are detected and disabled before they become an unmonitored attack path.*
- **Workforce population in scope**: all accounts on in-scope systems (to find those with no valid workforce owner or no recent activity).
- **Acceptance criteria (measurable)**:
  - Periodic reconciliation runs (defined cadence) match every account to an authoritative identity; unmatched = orphan, flagged.
  - Accounts inactive beyond the inactivity threshold (e.g. 45 days unprivileged, per ASD ISM ISM-1648) are detected and disabled or attested.
  - Orphan and dormant findings are routed to a named owner with a remediation SLA; closure is tracked.
  - Coverage: % of in-scope systems included in the scan is measured and trending up.
  - Re-enable/exception of any flagged account requires recorded approval.
- **Outcome lens (risk reduced)**: removes unowned/unmonitored standing accounts (the residue of failed leaver/mover processes) that enable persistence (T1078) and account-manipulation persistence (T1098); supports NIST AC-2(3) inactive-account disablement.

---

## MITRE ATT&CK techniques (Enterprise)

Source: MITRE ATT&CK Enterprise (attack.mitre.org). IDs and first-line descriptions verified verbatim 2026-06-09.

| Technique | ID | Tactics (per MITRE page) | JML relevance |
|-----------|----|--------------------------|---------------|
| Valid Accounts | **T1078** | Initial Access, Persistence, Privilege Escalation, Defense Evasion | Standing credentials from failed leaver de-provisioning (UC-JML-03) and orphan/dormant accounts (UC-JML-04) are abused as valid accounts. |
| Account Manipulation | **T1098** | Persistence, Privilege Escalation | Privilege creep through movers (UC-JML-02) and unmanaged accounts (UC-JML-04) expand what manipulated/compromised accounts can reach. |

- **T1078 — Valid Accounts** verbatim: *"Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion."*
- **T1098 — Account Manipulation** verbatim: *"Adversaries may manipulate accounts to maintain and/or elevate access to victim systems."*

> Sub-technique note: T1078.004 (Cloud Accounts) and T1098.001/.003 (Additional Cloud Credentials / Additional Cloud Roles) are the most JML-relevant sub-techniques for federated SaaS de-provisioning gaps. Sub-technique exact text was not re-verified for this file; cite the parent techniques above, which were verified.

---

## Regulatory mapping

Each entry: control ID + verbatim quote + authoritative URL. All quotes string-matched in the live source on 2026-06-09.

### NIST SP 800-53 Rev. 5 — Access Control (AC)

**AC-2 Account Management (base)** — covers the full account lifecycle (joiner provisioning, mover changes, leaver disablement, monitoring).
> Verbatim (control statement, items a–b): *"Define and document the types of accounts allowed and specifically prohibited for use within the system; Assign account managers; Require [Assignment: organization-defined prerequisites and criteria] for group and role membership; ..."*
> Source: NIST SP 800-53 Rev. 5, AC-2 (CSF Tools mirror of NIST control text). https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/

**AC-2(3) Disable Accounts** — directly supports UC-JML-03 (leaver) and UC-JML-04 (orphan/dormant).
> Verbatim: *"Disable accounts within [Assignment: organization-defined time period] when the accounts: Have expired; Are no longer associated with a user or individual; Are in violation of organizational policy; or Have been inactive for [Assignment: organization-defined time period]."*
> Source: NIST SP 800-53 Rev. 5, AC-2(3). https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ac-2-3/
> Primary canonical text also in NIST OSCAL catalog: https://csrc.nist.gov/CSRC/media/Projects/risk-management/800-53%20Downloads/800-53r5/SP_800-53_v5_1-derived-OSCAL.pdf

### ASD Information Security Manual (cyber.gov.au) — Guidelines for Personnel Security

> Control statements appear immediately *before* their `Control: ISM-XXXX` identifier on the published guideline page; IDs below were confirmed against that pairing.

**ISM-1591 — same-day removal/suspension on loss of business requirement** (leaver SLA — UC-JML-03).
> Verbatim: *"Access to systems and their resources are removed or suspended the same day personnel no longer have a legitimate requirement for access."*
> Source: https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security

**ISM-1648 — unprivileged inactive-account disablement** (orphan/dormant — UC-JML-04).
> Verbatim: *"Unprivileged access to systems and their resources are disabled after 45 days of inactivity."*
> Source: https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security

**ISM-1647 — privileged inactive-account disablement** (orphan/dormant, privileged — UC-JML-04).
> Verbatim: *"Privileged access to systems and their resources are disabled after 45 days of inactivity."*
> Source: https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security

> Additional ISM context (verified verbatim on the same page, supporting privileged-access revalidation / mover): *"Privileged access to systems and their resources are disabled after 12 months unless revalidated."* — supports periodic revalidation feeding mover recalculation (UC-JML-02). (ID for this statement was adjacent to ISM-1647 on the page; treat the 45-day privileged statement as the primary cited control and this 12-month revalidation statement as supporting context.)

### APRA CPS 234 — Information Security

**Implementation of controls** (whole-of-lifecycle obligation; underpins timely leaver de-provisioning and access control maintenance).
> Verbatim: *"An APRA-regulated entity must have information security controls to protect its information assets, including those managed by related parties and third parties, that are implemented in a timely manner and that are commensurate with: vulnerabilities and threats to the information assets; the criticality and sensitivity of the information assets; the stage at which the information assets are within their life-cycle ..."*
> Source: APRA Prudential Handbook — CPS 234 Information Security. https://handbook.apra.gov.au/standard/cps-234
> Primary PDF (July 2019): https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf
> Relevance: CPS 234 is principles-based; it does not enumerate a discrete "JML" clause. The "Implementation of controls — timely manner / commensurate with life-cycle" obligation is the load-bearing hook for JML SLAs and access maintenance. The companion **CPG 234 Prudential Practice Guide** elaborates access-management practice (provisioning, review, removal) — see https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_0.pdf (CPG 234 specific paragraph text not re-verified verbatim for this file — **UNVERIFIED**, cite by reference only).

### ISO/IEC 27001:2022 — Annex A

**A.5.18 Access rights** — full lifecycle of access rights (provision/review/modify/remove) — covers all four JML use cases.
> Verbatim (control statement): *"Access rights to information and other associated assets should be provisioned, reviewed, modified and removed in accordance with the organisation's topic-specific policy on and rules for access control."*
> Source (authoritative-text mirror; full ISO standard is paywalled at iso.org): https://hightable.io/iso-27001-annex-a-5-18-access-rights/
> ISO catalogue entry (paywalled): https://www.iso.org/standard/27001

**A.5.16 Identity management** — full lifecycle of identities (supports joiner identity creation and leaver identity retirement).
> Purpose (paraphrase from authoritative mirror — exact ISO sentence is paywalled): A.5.16 requires the organisation to manage the **full life cycle of identities** for human and non-human entities. The verbatim normative sentence was **not** confirmed from a primary source (ISO text is paywalled), so A.5.16 is cited by control ID + purpose only and is **UNVERIFIED** for verbatim quoting.
> Source: https://hightable.io/iso-27001-annex-a-5-16-identity-management/ ; ISO catalogue https://www.iso.org/standard/27001

### SOX (Sarbanes–Oxley) — Segregation of Duties context
SOX SoD obligations are owned by the **SoD** area (spike UC-I-006/007/008), not JML. JML feeds SOX-relevant ITGC by ensuring leaver/mover de-provisioning is timely and evidenced (access-change ITGCs). No verbatim SOX statutory quote is included here; map JML evidence to the SoD/ITGC area instead.

---

## Evidence artifacts an auditor would accept

| Use case | Primary evidence artifact(s) | What it must show |
|----------|------------------------------|-------------------|
| UC-JML-01 Joiner | **Joiner provisioning audit log** + birthright role-policy register | Each joiner's grants tied to an HR effective-start event and a named role/birthright rule; time-to-first-access vs SLA; manual-vs-automated grant ratio. |
| UC-JML-02 Mover | **Mover recalculation report** + change-event trace | HR change event → recalculation → entitlements added/removed; manager reaffirmation records; residual cross-role access (privilege-creep metric). |
| UC-JML-03 Leaver | **Leaver SLA / de-provisioning report** | Termination-event timestamp → disable timestamp per account; % within SLA; breach list with root cause; coverage across SaaS + on-prem targets. |
| UC-JML-04 Orphan/dormant | **Orphan-account scan** + **dormant-account (inactivity) report** | Accounts with no valid owner; accounts past the inactivity threshold (e.g. 45 days); remediation/disable actions with approvals; scan coverage % of in-scope systems. |
| Cross-cutting | Process documentation with named owner; exception register; immutable audit logs; reconciliation between authoritative HR source and target systems. | Demonstrates process maturity (A7) and supports CPS 234 "timely manner" + NIST AC-2 account-management evidence. |

---

## Notes for build agents
- Use-case archetype assignments here are consistent with the spike `uc-archetype-map.csv` (UC-I-001→A2, UC-I-002→A7, UC-I-003→A2) and add UC-JML-04→A5 for orphan/dormant.
- The strongest, fully-verified citations for JML maturity ladders are: **NIST AC-2 / AC-2(3)**, **ASD ISM-1591 / ISM-1648 / ISM-1647**, **CPS 234 Implementation-of-controls**, **ISO A.5.18**. These four anchor the regulatory trace for the JML area.
- A.5.16, CPG 234 paragraph text, and ATT&CK sub-techniques are referenced but **UNVERIFIED for verbatim quoting** — do not present them as quoted controls without obtaining the primary text.

---

## Citation verification

Adversarial re-verification performed 2026-06-10. Each URL was fetched live (HTTP status checked) and each quote string-matched against the page after whitespace/HTML-entity normalization. Control IDs cross-checked against their authoritative registers.

| Key | URL resolves | Quote faithful | Verdict | Note |
|-----|:---:|:---:|---------|------|
| `mitre-t1078-valid-accounts` | yes (200) | yes | **VERIFIED** | Verbatim first-line description on the authoritative MITRE ATT&CK T1078 page; tactics (Initial Access, Persistence, Privilege Escalation, Defense Evasion) match. |
| `mitre-t1098-account-manipulation` | yes (200) | yes | **VERIFIED** | Verbatim first-line description on the authoritative MITRE ATT&CK T1098 page. |
| `nist-sp-800-53-ac2-3` | yes (200) | yes | **VERIFIED** | Verbatim AC-2(3) control statement. Source is csf.tools (a faithful NIST control-text mirror), not nist.gov primary; canonical OSCAL PDF also referenced in the AC-2(3) entry. Control ID AC-2(3) is real and correctly labelled "Disable Accounts". |
| `nist-sp-800-53-ac2` | yes (200) | yes | **VERIFIED** | Verbatim AC-2 control-statement items a–c. Same mirror caveat as AC-2(3). Control ID AC-2 "Account Management" is real and correctly labelled. |
| `asd-ism-1591-same-day-removal` | yes (200) | yes | **VERIFIED** | Primary source cyber.gov.au. Quote matches verbatim and the control statement is immediately paired with `Control: ISM-1591` on the live page (Revision 1, Updated Jun-25). Control ID confirmed in register. |
| `asd-ism-1648-unpriv-inactivity` | yes (200) | yes | **VERIFIED** | Primary source cyber.gov.au. Verbatim; paired with `Control: ISM-1648` (Rev 2, Jun-25, Essential 8 ML2/ML3). Control ID confirmed. |
| `asd-ism-1647-priv-inactivity` | yes (200) | yes | **VERIFIED** | Primary source cyber.gov.au. Verbatim; paired with `Control: ISM-1647` (Rev 2, Jun-25, Essential 8 ML2/ML3). Control ID confirmed. Note: ISM-1647 on the page concerns privileged inactivity (45 days); the adjacent "12 months unless revalidated" statement is a *separate* privileged-access control and must not be conflated with ISM-1647 — keep it as supporting context only, as already flagged inline. |
| `apra-cps-234-implementation-of-controls` | yes (200) | yes | **VERIFIED** | Primary source handbook.apra.gov.au. Quote matches verbatim (incl. "implemented in a timely manner", "commensurate with", "stage at which the information assets are within their life-cycle"). |
| `iso-27001-2022-a5-18-access-rights` | yes (200) | yes | **VERIFIED (secondary source)** | Quote matches verbatim. Source hightable.io is a third-party commercial mirror, NOT a primary authority — the ISO/IEC 27001:2022 standard text itself is paywalled at iso.org. Verdict VERIFIED on quote fidelity, but downgrade confidence: do not present as a primary citation; obtain licensed ISO text before any audit-facing use. Control ID A.5.18 "Access rights" is real and correct. |

**Outcome:** all 9 citations VERIFIED — none SUSPECT or FABRICATED. No citation removed. Two confidence caveats retained: (1) NIST AC-2 / AC-2(3) quotes are mirrored via csf.tools, not nist.gov primary; (2) ISO A.5.18 is mirrored via a third-party (hightable.io), with ISO primary paywalled.

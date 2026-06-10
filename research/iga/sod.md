# IGA Domain — Separation of Duties (SoD) / Toxic-Combination Management

> **⚠️ ERRATUM (2026-06-10):** `apra-cps234-roles` below is superseded — the verbatim roles quote is
> CPS 234 **paragraph 14** (official APRA PDF), shipped as control code **CPS234-§14** with citation
> key `apra-cps-234-para14`. See `docs/superpowers/plans/ws1-verification-notes.md`.

**Area:** Separation of Duties (SoD) / toxic-combination management
**Domain:** Identity Governance & Administration (IGA)
**Instrument intent:** Scores *process maturity*, not tool deployment. Questions probe whether the SoD lifecycle (define → prevent → detect → remediate → attest) is governed, repeatable, and evidenced — independent of any particular IGA/GRC vendor.
**Jurisdiction:** AU-primary (APRA CPS 234, ASD ISM, Essential Eight) + NIST SP 800-53 r5 AC family, ISO/IEC 27001:2022 Annex A.5, SOX s404 (SoD over ICFR).
**Date authored:** 2026-06-09

---

## 1. Framing: why SoD is a fraud-enablement control

Separation of Duties (SoD) is the control that ensures no single identity can complete a *toxic combination* of business or technical functions that, together, enable fraud, theft, or undetectable error. The canonical financial example is **create-vendor + approve-payment + release-payment** held by one person; the canonical technical example is **administer access-control + administer audit logs** held by one person (the latter is called out explicitly in NIST AC-5 guidance).

SoD failure is rarely a single exploit; it is a *standing condition* that an insider (or an adversary who has compromised one account) can exploit without collusion. The instrument therefore treats SoD as a continuous governance process with three reinforcing layers:

1. **Preventive** — block toxic grants at access-request time (before the conflict exists).
2. **Policy/governance** — a maintained ruleset (the "SoD register") and a managed process for handling violations and exceptions.
3. **Detective** — periodic scanning of *existing* access to find conflicts that slipped past prevention (legacy access, emergency grants, ruleset drift), tracking each with a mitigating control.

### ATT&CK / fraud-enablement framing

SoD is primarily an **insider-threat and post-compromise-abuse** control, so it maps to ATT&CK Enterprise tactics around *Privilege Escalation* and *abuse of legitimate access* rather than initial intrusion:

- **T1078 Valid Accounts** — once an adversary controls a legitimate account, the absence of SoD lets that single account perform the full attack/fraud chain. SoD constrains the *blast radius* of any one compromised identity.
- **T1098 Account Manipulation** — granting oneself (or an attacker granting a controlled identity) an additional entitlement that completes a toxic pair. Preventive SoD at request-time and detective scanning of entitlement changes are the countermeasures.
- **Fraud chain (non-ATT&CK, financial-crime lens):** initiate → approve → conceal. SoD breaks the chain by ensuring the *initiate*, *approve*, and *reconcile/audit* steps are held by distinct identities. This is the SOX/ICFR rationale and the ISO 27001 A.5.3 rationale ("prevent a single person from being able to commit, conceal, and justify improper actions").

The maturity lens: a low-maturity org *discovers* SoD conflicts during an annual audit; a high-maturity org *prevents* them at request time, maintains a versioned ruleset, and continuously detects residual conflicts with documented mitigating controls and an owner per violation.

---

## 2. Use Cases

> Archetype legend (instrument's existing maturity archetypes):
> **A1 = preventive/enforcing control** (stops the bad state from being created);
> **A3 = detective/monitoring capability** (finds the bad state after the fact);
> **A7 = governance/process discipline** (policy register, ownership, exception & violation management workflow).

---

### UC-SOD-1 — Preventive SoD checks at access-request time

**Archetype fit:** **A1** (preventive control — the request is evaluated and toxic grants are blocked or routed to risk-acceptance *before* the entitlement is provisioned).

**Story:**
As an access-governance owner, I want every access request (self-service, manager-initiated, role-assignment, or birthright) to be evaluated against the SoD ruleset *before* provisioning, so that a grant which would create a toxic combination with the requester's *existing* access is blocked — or forced through an explicit, logged risk-acceptance path — rather than silently provisioned and discovered months later.

**Acceptance criteria:**
- Access requests are evaluated against the active SoD ruleset at request time, considering the requester's **current** entitlements plus the **requested** entitlement (not the requested entitlement in isolation).
- A request that would create a defined toxic combination is **blocked by default**, or routed to a named risk-owner for explicit approval; "silent provisioning" of a conflicting grant is not possible without a recorded decision.
- The evaluation covers entitlements that span **multiple systems/applications** (cross-system toxic pairs), not just intra-application role conflicts — consistent with AC-5 guidance that "separation of duty violations can span systems and application domains."
- Every block/override decision is written to an immutable **request-time block log** (who requested, what conflict rule fired, decision, approver, justification, timestamp).
- The check is applied consistently to *all* provisioning channels (self-service portal, automated joiner/role-based birthright, manager grants, emergency/break-glass).

**Population (what the question is asked against):**
All access-granting events across in-scope systems — i.e., the population is *access requests / provisioning transactions* over a defined period (e.g., trailing 12 months), including birthright/automated grants. Sampling should include cross-system grants and break-glass grants, not only portal self-service.

**Outcome lens:**
*Toxic combinations are prevented at the source.* Maturity is demonstrated when conflicting grants cannot enter the environment without a recorded, owned risk-acceptance — measured by (a) coverage of provisioning channels, (b) cross-system rule evaluation, and (c) completeness of the block/override log. Low maturity = checks only in one portal, or advisory-only warnings that don't block; high maturity = enforced, cross-system, all-channels, fully logged.

---

### UC-SOD-2 — SoD policy register & violation-management process

**Archetype fit:** **A7** (governance/process — a maintained, owned policy ruleset plus a defined workflow for triaging violations, granting time-bound exceptions, and assigning mitigating controls).

**Story:**
As a risk/compliance owner, I want a maintained **SoD policy register** (the authoritative set of toxic-combination rules) with named business owners per rule, plus a documented **violation-management process** that defines how detected conflicts are triaged, who can approve a mitigating control or a time-bound exception, and how the register itself is reviewed and version-controlled — so that the ruleset reflects current business risk and every violation has an accountable disposition.

**Acceptance criteria:**
- An authoritative **SoD ruleset/register** exists, is version-controlled, and each rule has: a business rationale, a named owner, a risk rating, and the conflicting functions/entitlements it covers.
- The register is **reviewed on a defined cadence** (e.g., at least annually and on material business/process change), with review evidence retained — aligned with ISO 27001 A.5.3's expectation that segregation be considered "as part of the risk evaluation and treatment process."
- A documented **violation-management workflow** defines: intake of a detected/attempted conflict, triage and risk-rating, allowable dispositions (remediate, accept-with-mitigating-control, time-bound exception), required approver authority per disposition, and a re-review/expiry date for every exception.
- **Exceptions are time-bound and re-attested**; an exception cannot be open-ended. Each carries a documented mitigating control and an owner.
- Roles in the SoD process itself observe separation (the person who *defines/owns* a rule is not the sole person who can *waive* a violation of it) — reflecting AC-5's principle that those administering a control should not be the sole accountable party for overseeing it.

**Population:**
The SoD rule register (all rules) + the population of open and closed violations/exceptions over the review period. Evidence sampling targets: rules without owners, exceptions past expiry, and violations with no recorded disposition.

**Outcome lens:**
*Every SoD rule and every violation has an accountable owner and a current disposition.* Maturity is demonstrated by a living, reviewed register (not a stale spreadsheet), bounded exceptions with mitigating controls, and clear approval authority. This is the control that keeps UC-SOD-1 (prevention) and UC-SOD-3 (detection) *meaningful* — without a maintained ruleset, both degrade to checking against the wrong rules.

---

### UC-SOD-3 — Detective SoD scanning of existing access with mitigating-control tracking

**Archetype fit:** **A3** (detective/monitoring capability — periodic scan of the *installed base* of entitlements to surface conflicts that prevention missed, each tracked to a mitigating control).

**Story:**
As an access-governance owner, I want recurring detective scans of *existing* access across in-scope systems against the SoD ruleset, so that conflicts introduced before the ruleset existed, granted via break-glass, or created by entitlement/role drift are surfaced, risk-rated, and either remediated or formally tracked with a documented **mitigating control** and owner — closing the gap between point-in-time prevention and the standing reality of accumulated access.

**Acceptance criteria:**
- Existing entitlements are scanned against the active SoD ruleset on a **defined recurring cadence** (and ad hoc after major changes), covering **cross-system** combinations.
- Each detected conflict is risk-rated and assigned a disposition consistent with the UC-SOD-2 workflow: remediate (revoke one side), or retain with a **documented, owned mitigating control** (e.g., independent transaction review, dual-control on the conflicting activity, enhanced logging/alerting on the conflicted user).
- A **violation register** records, per conflict: the rule, the affected identity, affected systems, risk rating, disposition, the mitigating control (where retained), the owner, and the next review/expiry date.
- Detective findings feed back into prevention and policy: recurring conflict patterns trigger ruleset refinement (UC-SOD-2) and/or tightening of request-time blocks (UC-SOD-1).
- Scan results and dispositions are retained as audit evidence and are **traceable across review cycles** (you can show a given conflict's history: detected → mitigated → revalidated or remediated).

**Population:**
The full in-scope entitlement population (all users × all entitlements across covered systems) at scan time, plus the resulting violation register. Evidence sampling targets: high-risk-rated open conflicts, conflicts "mitigated" without a documented control, and conflicts re-appearing across consecutive scans (mitigation not working).

**Outcome lens:**
*The standing base of access is continuously reconciled to the SoD policy, and every residual conflict is consciously owned.* Maturity is demonstrated when scans are recurring + cross-system, when "mitigated" always means a real, documented, tested compensating control (not an unjustified accept), and when detective output measurably improves prevention. Low maturity = annual audit-driven spreadsheet; high maturity = scheduled scans with a living violation register, mitigating-control evidence, and feedback into the ruleset.

---

## 3. Regulatory mapping

> Citation rigor note: each quote below was retrieved from the cited primary/authoritative source and reproduced verbatim. NIST AC-5 is from the NIST OSCAL machine-readable catalog (primary). SOX s404 is from the U.S. statutory text on GovInfo (primary). APRA CPS 234 is from the official APRA Prudential Handbook (primary). ISO 27001:2022 A.5.3's normative one-line control statement is reproduced from a secondary publisher because ISO sells the standard text behind a paywall (iso.org) — this is flagged and the secondary source is cited; the verbatim ISO clause itself ("Conflicting duties and conflicting areas of responsibility shall be segregated") is the well-established normative wording but should be re-verified against a purchased copy of ISO/IEC 27001:2022 before any external attestation.

### 3.1 NIST SP 800-53 Rev 5 — AC-5 Separation of Duties *(primary)*

**Control statement (verbatim):**
> "a. Identify and document [Assignment: organization-defined duties of individuals requiring separation] ; and
> b. Define system access authorizations to support separation of duties."

**Discussion/guidance (verbatim):**
> "Separation of duties addresses the potential for abuse of authorized privileges and helps to reduce the risk of malevolent activity without collusion. Separation of duties includes dividing mission or business functions and support functions among different individuals or roles, conducting system support functions with different individuals, and ensuring that security personnel who administer access control functions do not also administer audit functions. Because separation of duty violations can span systems and application domains, organizations consider the entirety of systems and system components when developing policy on separation of duties. Separation of duties is enforced through the account management activities in AC-2 , access control mechanisms in AC-3 , and identity management activities in IA-2, IA-4 , and IA-12."

**Source:** NIST SP 800-53 Rev 5 OSCAL catalog (machine-readable, usnistgov/oscal-content), control `ac-5`. Authoritative landing: https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_1_1/home?element=AC-5 ; machine-readable JSON: https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json

**Maps to:** UC-SOD-1 (define + enforce access authorizations to support SoD; cross-system scope), UC-SOD-2 (identify and document duties requiring separation = the ruleset/register), UC-SOD-3 (cross-system violation detection). Note AC-5's own guidance ("span systems and application domains") is the direct authority for requiring *cross-system* evaluation in UC-SOD-1 and UC-SOD-3.

---

### 3.2 SOX — Section 404, Management Assessment of Internal Controls *(primary)*

SoD over Internal Control over Financial Reporting (ICFR) is a foundational SOX control. Section 404 itself does not use the phrase "segregation of duties"; it mandates that management establish, maintain, and assess an adequate internal control structure for financial reporting — and SoD is a core component of that structure under the COSO framework adopted by SEC/PCAOB. The statutory hooks:

**SOX §404 (verbatim):**
> "(a) Rules Required.--The Commission shall prescribe rules requiring each annual report required by section 13(a) or 15(d) of the Securities Exchange Act of 1934 (15 U.S.C. 78m or 78o(d)) to contain an internal control report, which shall-- (1) state the responsibility of management for establishing and maintaining an adequate internal control structure and procedures for financial reporting; and (2) contain an assessment, as of the end of the most recent fiscal year of the issuer, of the effectiveness of the internal control structure and procedures of the issuer for financial reporting."

**Supporting authorization-of-transactions hook — SOX §103(a)(2)(A)(iii)(II)(bb) auditor-evaluation criteria (verbatim):**
> "provide reasonable assurance that transactions are recorded as necessary to permit preparation of financial statements in accordance with generally accepted accounting principles, and that receipts and expenditures of the issuer are being made only in accordance with authorizations of management and directors of the issuer"

> **CORRECTION (citation verification 2026-06-10):** This quote was originally attributed to §404. It is verbatim-present in Public Law 107-204 but appears in **Section 103** (Auditing, Quality Control, and Independence Standards and Rules), at §103(a)(2)(A)(iii)(II)(bb) — the criteria the *auditor* must evaluate the internal control structure against — not in §404. The substantive mapping (authorization-of-transactions SoD hook) still holds; only the section label was wrong.

**Source:** Sarbanes-Oxley Act of 2002, Public Law 107-204, §103, U.S. Government Publishing Office (GovInfo): https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm

**Maps to:** UC-SOD-1 (transactions "only in accordance with authorizations" — preventive control over who can initiate vs approve), UC-SOD-2 (management's *adequate internal control structure* = a governed SoD ruleset and exception process), UC-SOD-3 (management's *assessment of effectiveness* requires detective scanning of standing access and tracked dispositions). Caveat for the instrument: SOX SoD applies specifically to **ICFR-relevant** systems and financially significant access — scope SOX-driven SoD questions to in-scope financial reporting applications, not the entire estate.

---

### 3.3 ISO/IEC 27001:2022 — Annex A 5.3 Segregation of Duties *(control statement via secondary publisher; verify against purchased standard)*

**Normative control statement (as reproduced by publisher; ISO text is paywalled):**
> "conflicting duties and conflicting areas of responsibility are separated."

**Purpose (as stated by publisher):**
> "In ISO 27001, Control 5.3 Segregation of Duties aims to separate conflicting duties. This reduces the risk of fraud and error and bypasses information security controls."

**Rationale (as stated by publisher):**
> "The control is designed to prevent a single person from being able to commit, conceal, and justify improper actions, thereby reducing the risk of fraud and error. It also prevents a single person from overriding information security controls."

**Source (secondary):** ISMS.online, "ISO 27001:2022 Annex A 5.3 – Segregation of Duties": https://www.isms.online/iso-27001/annex-a-2022/5-3-segregation-of-duties-2022/
**Primary (paywalled, for re-verification):** ISO/IEC 27001:2022, Annex A control 5.3 — https://www.iso.org/standard/27001 . The canonical ISO wording is "Conflicting duties and conflicting areas of responsibility shall be segregated"; confirm exact wording against a licensed copy before external attestation.

**Maps to:** UC-SOD-2 (A.5.3 expects segregation to be determined and implemented as part of risk treatment — the register and review cadence), UC-SOD-1 (separation enforced so no single person can act unchecked), UC-SOD-3 (where full separation is impractical, A.5.3 / ISO 27002 guidance accepts compensating controls such as monitoring, audit trails and supervision — this is the explicit basis for *mitigating-control tracking*).

---

### 3.4 APRA CPS 234 — Information Security (Implementation of controls) *(primary)*

CPS 234 does not name "segregation of duties" as a discrete clause, but its access/implementation-of-controls and roles-and-responsibilities obligations are the prudential authority for SoD as an information-security control in an APRA-regulated entity.

**Implementation of controls — para 22 (verbatim):**
> "An APRA-regulated entity must have information security controls to protect its information assets, including those managed by related parties and third parties, that are implemented in a timely manner and that are commensurate with: vulnerabilities and threats to the information assets; the criticality and sensitivity of the information assets; the stage at which the information assets are within their life-cycle; and the potential consequences of an information security incident."

**Roles and responsibilities (verbatim):**
> "An APRA-regulated entity must clearly define the information security-related roles and responsibilities of the Board, senior management, governing bodies and individuals with responsibility for decision-making, approval, oversight, operations and other information security functions."

**Source:** APRA Prudential Standard CPS 234 Information Security, APRA Prudential Handbook: https://handbook.apra.gov.au/standard/cps-234 (official PDF: https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf)

**Maps to:** UC-SOD-2 (clearly defined roles/responsibilities for *decision-making, approval, oversight, operations* = the basis for separating those functions and owning the SoD register), UC-SOD-1 + UC-SOD-3 (controls commensurate with criticality/sensitivity — high-value financial functions warrant enforced preventive SoD and recurring detective scanning).

---

## 4. Evidence artifacts

These are the durable artifacts an assessor requests to score each use case. The instrument scores *process maturity*, so artifacts must show a repeatable, owned, evidenced process — not a one-off export.

| Artifact | Primary UC | What it proves | Maturity tells |
|---|---|---|---|
| **SoD ruleset export** (versioned) | UC-SOD-2 | The authoritative toxic-combination rules exist, are version-controlled, each rule has an owner, risk rating, business rationale, and conflicting-function definition. | Version history + review dates present (living register) vs undated spreadsheet; rules with named owners vs orphaned rules; cross-system rules present vs intra-app only. |
| **Violation register with mitigating controls** | UC-SOD-3 (and UC-SOD-2 for exceptions) | Every detected conflict has a risk rating, disposition (remediate / accept-with-mitigation / time-bound exception), a documented mitigating control where retained, an owner, and a next-review/expiry date. | Mitigating controls are *documented and specific* (e.g., "independent monthly review of vendor-master changes by Finance Controller") vs "risk accepted" with no control; exceptions have expiry vs open-ended; conflict history traceable across scan cycles. |
| **Request-time block log** | UC-SOD-1 | The preventive check actually fired: records of access requests that triggered an SoD rule, the decision (blocked / overridden), the approver, justification, and timestamp — across all provisioning channels. | Log covers self-service + birthright + manager + break-glass (all channels) vs portal only; overrides carry named approver + justification vs silent overrides; cross-system conflicts represented. |
| *(supporting)* SoD policy & violation-management procedure document | UC-SOD-2 | The workflow, approval authorities per disposition, review cadence, and exception rules are defined and owned. | Approval authority separated from rule ownership; defined cadence; bounded exceptions. |
| *(supporting)* Detective scan schedule + completed scan reports across ≥2 cycles | UC-SOD-3 | Scans are recurring and cross-system, and findings feed back into the ruleset/prevention. | Recurring + dated vs single audit-time run; evidence that recurring-conflict patterns drove ruleset/prevention changes. |

**Cross-artifact integrity check (a maturity signal in itself):** a high-maturity program shows the three core artifacts *reconcile* — conflicts blocked at request time (block log) align with the ruleset (ruleset export), and residual standing conflicts found by scanning (violation register) feed ruleset refinement. If the detective scan keeps finding conflicts the preventive check should have blocked, prevention coverage is incomplete (a finding for UC-SOD-1).

---

## 5. Notes for build agents

- **Archetype anchoring is deliberate:** UC-SOD-1→A1 (preventive), UC-SOD-2→A7 (governance/process), UC-SOD-3→A3 (detective). Keep these distinct so the instrument can score an org that prevents-but-doesn't-detect differently from one that detects-but-doesn't-prevent (both are common, partial maturity states).
- **Cross-system scope** is the single most-cited differentiator across NIST AC-5, the fraud lens, and CPS 234 criticality-commensurate controls — questions for UC-SOD-1 and UC-SOD-3 should explicitly probe whether toxic-pair evaluation spans applications, not just intra-app role conflicts.
- **Mitigating controls are an ISO 27002 / A.5.3-sanctioned path**, not a loophole — but the maturity bar is that they are *documented, owned, time-bound, and tested*. "Risk accepted" with no compensating control is a low-maturity tell, not a valid disposition.
- **SOX scoping caveat:** apply SOX-driven SoD weighting only to ICFR-relevant/financially-significant systems; do not let SOX inflate SoD expectations on non-financial systems where CPS 234 / ISO criticality-commensurate scoping is the right lens.
- **Re-verify ISO A.5.3 verbatim wording** against a licensed ISO/IEC 27001:2022 copy before any external/attestation use — the iso.org text is paywalled and only the secondary reproduction was machine-verified here.

---

## Citation verification

Adversarial verification performed 2026-06-10. Each URL was fetched programmatically and each quote string-matched (whitespace-normalized) against the retrieved source text. Authoritative registers were used to confirm control IDs.

| Key | URL resolves | Quote faithful | Verdict | Note |
|---|---|---|---|---|
| `nist-sp-800-53-r5-ac-5` | Yes (200, OSCAL raw JSON) | Yes — verbatim | **VERIFIED** | AC-5 exists in the authoritative NIST OSCAL Rev 5 catalog; discussion text ("...abuse of authorized privileges...without collusion...can span systems and application domains...") matches word-for-word. |
| `nist-sp-800-53-r5-ac-5-statement` | Yes (csrc.nist.gov CPRT landing returns 200; `?element=AC-5` is a client-side SPA fragment) | Yes — verbatim | **VERIFIED** | Statement "Define system access authorizations to support separation of duties." confirmed verbatim against the OSCAL register (part b of AC-5). |
| `sox-pl107-204-s404` | Yes (200, GovInfo statutory HTML) | Yes — verbatim | **VERIFIED** | Both clauses confirmed verbatim in §404(a)(1) and §404(a)(2). |
| `sox-pl107-204-authorizations` | Yes (200, same page) | Yes — verbatim | **SUSPECT** | Quote IS verbatim in PL 107-204, but it appears in **§103(a)(2)(A)(iii)(II)(bb)** (auditor-evaluation criteria), NOT §404 as the sourceTitle claimed. Section attribution corrected in §3.2 above. Quote and URL are genuine; only the section label was wrong. |
| `apra-cps234-para22` | Yes (200, official APRA Prudential Handbook HTML) | Yes — verbatim | **VERIFIED** | Confirmed as paragraph 22 (footnote [10] on the live page explicitly references "paragraph 22 of this Prudential Standard"). Live-page rendering inserts footnote marker [9] + footnote text inline between "life-cycle;" and "and the potential consequences..."; the standard's prose itself matches the quote word-for-word. |
| `apra-cps234-roles` | Yes (200, same handbook page) | Yes — verbatim | **VERIFIED** | Roles-and-responsibilities sentence matches word-for-word. |

**Disposition:** No FABRICATED citations. One SUSPECT citation (`sox-pl107-204-authorizations`) — retained because the quote is genuine and verbatim on a resolving authoritative page, but its section attribution was corrected from §404 to §103. The ISO/IEC 27001:2022 A.5.3 material in §3.3 was already flagged in-document as secondary/unverified (paywalled primary) and was NOT part of the returned citations array; it remains flagged for re-verification against a licensed copy.

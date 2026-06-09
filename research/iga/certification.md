# IGA Research — Access Certification / Recertification Campaigns

**Domain:** Identity Governance & Administration (IGA)
**Area:** Access certification / recertification campaigns
**Jurisdiction:** AU-primary (APRA CPS 234, ASD ISM, Essential Eight) + NIST SP 800-53, ISO/IEC 27001:2022, SOX/ICFR
**Instrument lens:** scores *process maturity*, not tool deployment
**Author note:** Every citation below was fetched from its authoritative source and the quote string-matched against the live page/PDF before inclusion. Citations that could not be verbatim-verified are marked UNVERIFIED inline and excluded from the returned citations array.

---

## 1. Why this area matters (threat + governance framing)

Access certification (a.k.a. recertification, attestation, access review) is the periodic, accountable confirmation that each identity's standing entitlements are still warranted by a current business need. It is the principal *detective* control against **privilege accumulation** — the slow drift where movers, project access, break-glass grants, and stale role memberships pile up faster than they are removed.

The adversary relevance is direct. MITRE ATT&CK **T1078 Valid Accounts** is exactly the asset that accumulated, un-reviewed access creates: legitimate credentials and entitlements an adversary can ride without tripping malware controls. ATT&CK notes that "Compromised credentials may be used to bypass access controls placed on various resources on systems within the network and may even be used for persistent access to remote systems and externally available services" and that "The overlap of permissions for local, domain, and cloud accounts across a network of systems is of concern because the adversary may be able to pivot across accounts and systems to reach a high level of access (i.e., domain or enterprise administrator) to bypass access controls set within the enterprise." Certification campaigns shrink the standing entitlement surface that makes T1078 (and its sub-techniques .001 Local, .002 Domain, .003 Cloud) lucrative, and a privileged sign-off cycle directly attacks the "pivot to a high level of access" path. Because certification is detective rather than preventive, it is the natural complement to request-time SoD checks (UC-I-006) and JML de-provisioning (UC-I-003).

---

## 2. Use cases

Three use cases. UC-I-004 and UC-I-005 already exist in `spikes/iga/use-cases.csv`; this research deepens their stories/acceptance criteria and adds a third (micro-/event-driven certification) for build-time consideration.

### UC-I-004 — Periodic access certification campaigns
- **Archetype fit:** **A5** (inventory & attestation). Certification maps cleanly to A5: the campaign *inventories* in-scope entitlements and forces a *positive attestation* (keep / revoke) by an accountable reviewer.
- **Population:** in-scope workforce identities and their standing entitlements (application roles, group memberships, fine-grained entitlements) across systems within the certification scope.
- **Story:** As a control owner in a regulated bank, I run a recurring (typically quarterly for higher-risk apps, at least annually for the broad estate) certification campaign in which each line manager and/or application/entitlement owner reviews the access held by their reports/scope and explicitly affirms or revokes each item, so that standing access continues to reflect a current, validated business need and drift is caught and reversed.
- **Acceptance criteria (maturity signals, not tool features):**
  - A defined, scheduled cadence exists per risk tier (e.g. quarterly for high-risk apps, ≥ annual for the broad population) and campaigns actually launch on schedule.
  - **≥ 95% of in-scope items reviewed (decisioned) within the campaign window**; "no-decision" items are not silently auto-approved — they default to a defined safe outcome (escalation or revoke) per policy.
  - **Revocations are actioned within an agreed SLA** of the decision (e.g. high-risk within 24–72h; standard within the close window) and closure is evidenced, not just recorded as "approved for removal."
  - Reviewers are the *accountable* owners (manager and/or entitlement owner), not a central team rubber-stamping; rubber-stamp / bulk-approve behaviour is monitored and challenged.
  - Scope completeness is governed: the in-scope population is reconciled against an authoritative identity/entitlement inventory so the campaign is not blind to ungoverned systems.
- **Outcome lens:** the bulk of standing entitlements carry a current, owner-affirmed justification; revoke decisions complete within SLA; campaign completion is auditable end-to-end.

### UC-I-005 — High-risk / privileged access certification sign-off
- **Archetype fit:** **A8** (high-risk artifact sign-off). A named accountable owner signs off a defined high-risk artifact on a cadence within an agreed close window.
- **Population:** privileged and high-risk entitlements — admin roles, privileged groups, toxic/SoD-sensitive combinations, access to crown-jewel / financially-material systems, standing break-glass.
- **Story:** As the owner of privileged access risk, I run a separate, more frequent and more rigorous certification of privileged and high-risk entitlements in which an accountable senior owner signs off each privileged grant, so that the highest-impact access (the access an attacker most wants for T1078 privilege-escalation) is validated more often and removed faster than ordinary access.
- **Acceptance criteria:**
  - Privileged/high-risk entitlements are identified and certified on a **shorter cadence** than standard access (e.g. quarterly or more frequent) with a defined **campaign-close / sign-off window**.
  - A **named accountable owner** (not a delegate pool) provides explicit sign-off per privileged item; attestation is attributable and timestamped.
  - **Revocations of privileged access are actioned within a tight SLA** (materially shorter than standard, e.g. ≤ 24–72h).
  - Sign-off coverage approaches 100% of the privileged population within the window; exceptions carry a documented risk-acceptance with an owner and expiry.
  - Standing privileged access flagged for removal feeds JIT / least-privilege right-sizing (links to ISM-1649 JIT administration and UC-I-011).
- **Outcome lens:** every privileged/high-risk entitlement has a current, named sign-off; privileged revocations complete within the tight SLA; the privileged standing-access surface trends down.

### UC-I-006(cert) — Micro-certification on change / event-driven recertification
> Proposed new UC for build (suggest id e.g. `UC-I-012`; not yet in `use-cases.csv`). Naming kept distinct here to avoid clashing with the existing SoD `UC-I-006`.
- **Archetype fit:** **A5** (inventory & attestation) at the event grain — an event triggers a *targeted* attestation of just the affected entitlements, rather than a full periodic sweep.
- **Population:** the specific entitlements affected by a triggering event — e.g. on a mover/transfer, the retained pre-transfer access; on a role/entitlement definition change; on a high-risk-access grant; on detection of an SoD violation.
- **Story:** As a control owner, when a risk-relevant event occurs (job transfer, sensitive grant, role redefinition, SoD-violation detection), I trigger a small, fast "micro-certification" of just the impacted access so the affected reviewer confirms or revokes within a short SLA, so that risk is re-validated at the moment it changes instead of waiting for the next quarterly cycle.
- **Acceptance criteria:**
  - Defined trigger events exist (at minimum: mover/transfer, privileged/high-risk grant, SoD violation detected) and reliably initiate a scoped micro-certification.
  - Micro-certifications are **small (only impacted entitlements)** and carry a **short turnaround SLA** (e.g. ≤ 5 business days; tighter for privileged).
  - Completion + revocation actioning is evidenced per event; overdue micro-certs escalate.
  - Event-driven reviews are reconciled with periodic campaigns so nothing is double-counted or dropped.
- **Outcome lens:** mover-retained and newly-risky access is re-validated near the event, materially shortening the window in which stale/excess access persists between periodic campaigns.

---

## 3. Regulatory mapping (verified control IDs + verbatim quotes)

> Quotes are verbatim from the cited authoritative source as fetched. `[Assignment: ...]` placeholders are reproduced exactly as in NIST.

### NIST SP 800-53 Rev 5

**AC-2 Account Management — item (j): periodic account review.** This is the canonical periodic-certification hook.
> "Review accounts for compliance with account management requirements [Assignment: organization-defined frequency]"
Source: CSF Tools mirror of NIST SP 800-53 Rev 5 AC-2 — https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/

**AC-2(3) Disable Accounts** — supports the *revocation/actioning* half of certification (the outcome of a "revoke" decision).
> "Disable accounts within [Assignment: organization-defined time period] when the accounts: Have expired; Are no longer associated with a user or individual; Are in violation of organizational policy; or Have been inactive"
Source: https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/

**AC-6(7) Review of User Privileges** — the privileged-certification hook (maps to UC-I-005).
> "Review [Assignment: organization-defined frequency] the privileges assigned to [Assignment: organization-defined roles and classes] to validate the need for such privileges; and Reassign or remove privileges, if necessary, to correctly reflect organizational mission and business needs."
Source: https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/

### APRA CPS 234 — Information Security (Prudential Standard, July 2019)

**Paragraph 21 — Implementation of controls (commensurate, risk-tiered controls).** This is the basis for risk-tiered certification cadence (more frequent/rigorous for higher-criticality assets and privileged access).
> "An APRA-regulated entity must have information security controls to protect its information assets, including those managed by related parties and third parties, that are implemented in a timely manner and that are commensurate with: (a) vulnerabilities and threats to the information assets; (b) the criticality and sensitivity of the information assets; (c) the stage at which the information assets are within their life-cycle; and (d) the potential consequences of an information security incident."
Source: APRA, Prudential Standard CPS 234, July 2019 (official PDF), para 21 — https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf

**Paragraph 27 — Testing control effectiveness (systematic, risk-commensurate cadence).** Supports the requirement that certification (a control) be tested/run on a cadence commensurate with risk and change.
> "An APRA-regulated entity must test the effectiveness of its information security controls through a systematic testing program. The nature and frequency of the systematic testing must be commensurate with: (a) the rate at which the vulnerabilities and threats change; (b) the criticality and sensitivity of the information asset; (c) the consequences of an information security incident; (d) the risks associated with exposure to environments where the APRA-regulated entity is unable to enforce its information security policies; and (e) the materiality and frequency of change to information assets."
Source: APRA CPS 234, July 2019, para 27 — https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf

> Note: CPS 234 is principles-based and does not enumerate a discrete "access review" control ID. Access certification is the entity's implementation of paras 21/27 for access controls. Detailed how-to lives in the companion **CPG 234** practice guide (non-binding). Mapping certification to CPS 234 §21/§27 is defensible; do **not** invent a CPS 234 access-review clause number.

### ASD ISM (Information Security Manual, cyber.gov.au) — Essential Eight aligned

**ISM-1647 — privileged access revalidation (12-month disable unless revalidated).** Direct hook for privileged certification (UC-I-005); Essential Eight ML2/ML3.
> "Privileged access to systems and their resources are disabled after 12 months unless revalidated."
Source: ASD ISM, Guidelines for Personnel Security — Control ISM-1647 (Revision 2, Jun-25; Essential 8: ML2, ML3) — https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security

**ISM-0407 — secure access record incl. "when their access was last reviewed."** Supports the evidence/attestation-record requirement of certification.
> "A secure record is maintained for the life of systems and their resources that covers the following for each user: their user identification; their signed agreement to abide by system usage policies"
Source: ASD ISM, Guidelines for Personnel Security — Control ISM-0407 (Revision 6, Jun-25) — https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security
> Supporting (non-control) guidance on the same page: records "should include each user's user identification, their agreement to abide by system usage policies, who provided the authorisation for their access, when their authorisation was granted and **when their access was last reviewed**." (Records the *review* event — i.e. certification evidence.)

> Related controls on the same ISM page (verified present, available for finer mapping): **ISM-1648** "Privileged access to systems and their resources are disabled after 45 days of inactivity." (ML2/ML3) and **ISM-1649** just-in-time administration (ML3) — both reduce the standing privileged surface certification must police.

### ISO/IEC 27001:2022 — Annex A 5.18 Access rights

**A.5.18 Access rights** — the lifecycle review hook (provision/review/modify/remove).
> "Access rights to information and other associated assets should be provisioned, reviewed, modified and removed in accordance with the organisation's topic-specific policy on and rules for access control."
Source (quoting the standard's control statement verbatim): https://hightable.io/iso-27001-annex-a-5-18-access-rights/
> Note: iso.org sells the standard behind a paywall; the verbatim A.5.18 control statement is reproduced consistently across practitioner sources. The string above was verbatim-matched on the cited page. For an authoritative procurement reference, the standard is ISO/IEC 27001:2022, Annex A control 5.18 — https://www.iso.org/standard/27001

### SOX — ITGC access reviews (ICFR)

SOX itself (and the SEC's implementing rule) does not publish a numbered "access review" control. Periodic user-access reviews are an **IT General Control (ITGC)** that auditors test to support management's assertion on **internal control over financial reporting (ICFR)** under SOX §404, because access governs the "authorizations of management" clause of the ICFR definition.

**17 CFR 240.13a-15(f) — definition of ICFR (the SEC rule implementing SOX §302/§404).**
> "Provide reasonable assurance that transactions are recorded as necessary to permit preparation of financial statements in accordance with generally accepted accounting principles, and that receipts and expenditures of the issuer are being made only in accordance with authorizations of management and directors of the issuer"
Source: 17 CFR 240.13a-15(f), via Cornell Legal Information Institute — https://www.law.cornell.edu/cfr/text/17/240.13a-15

> Mapping rationale: access certification over financially-material systems demonstrates that access (and therefore the ability to initiate/record transactions) remains "only in accordance with authorizations of management" — the SoD and access-review backbone of SOX ITGC testing. Do **not** cite a fabricated "SOX 404 access-review control number"; the defensible anchor is the ICFR definition's "authorizations of management" clause plus the entity's own ITGC framework (commonly COBIT/COSO-aligned). The PCAOB auditing standard governing the ICFR audit is **AS 2201**; treat as supporting (not quoted here to avoid unverified text).

---

## 4. Evidence artifacts (what a mature campaign produces)

These are the artifacts an auditor / the instrument should expect; they double as the maturity evidence the questionnaire scores against.

1. **Campaign completion report** — per campaign: scope/population, item counts, % reviewed within window (target ≥ 95%), decision breakdown (kept / revoked / risk-accepted), no-decision handling, on-time vs. overdue, named reviewers and rubber-stamp/bulk-approve analytics. (Evidences AC-2(j); CPS 234 §27 systematic testing; A.5.18 review.)
2. **Revocation / remediation log** — every "revoke" decision with: decision timestamp, action timestamp, SLA met/missed, target system, and confirmation the entitlement was actually removed (closed-loop). Privileged revocations on the tight SLA broken out separately. (Evidences AC-2(3) disable, AC-6(7) reassign/remove, ISM-1647 revalidate-or-disable.)
3. **Reviewer attestation export** — per-item attestation records: reviewer identity, accountable owner, decision, justification, timestamp, and (for privileged) named sign-off. Immutable / tamper-evident retention. (Evidences ISM-0407 record incl. "when access was last reviewed"; SOX ITGC evidence of "authorizations of management"; A.5.18.)
4. **Scope/inventory reconciliation** — evidence the certified population was reconciled to an authoritative identity & entitlement inventory (no blind spots / ungoverned systems). (Evidences A5 archetype inventory; CPS 234 §21 commensurate, risk-tiered coverage.)
5. **Exception / risk-acceptance register** — for items kept despite flags or not decided in window: owner, rationale, expiry, re-review trigger. (Supports privileged sign-off exceptions and event-driven re-review.)

---

## 5. Archetype summary (for the questionnaire/archetype engine)

| UC | Title | Archetype | Key params |
|----|-------|-----------|------------|
| UC-I-004 | Periodic access certification campaigns | **A5** inventory & attestation | population=in-scope workforce entitlements; threshold=95% reviewed in window; cadence=risk-tiered (quarterly high-risk / ≥annual broad); revocation SLA tracked |
| UC-I-005 | High-risk / privileged access certification sign-off | **A8** high-risk artifact sign-off | artifact=privileged access sign-off; scope=privileged/high-risk entitlements; cadence=shorter (≥quarterly); named accountable owner; tight revocation SLA |
| UC-I-012 (proposed) | Micro-certification on change / event-driven | **A5** inventory & attestation (event grain) | trigger events=mover/grant/SoD-violation; scoped to impacted entitlements; short turnaround SLA |

Consistent with the existing `uc-archetype-map.csv` (certification → A5, high-risk sign-off → A8) and the spike finding that governance archetypes fit IGA cleanly with zero engine changes.

---

## 6. Citation key index

- `nist-sp-800-53-ac2j` — AC-2(j) account review
- `nist-sp-800-53-ac2-3` — AC-2(3) disable accounts
- `nist-sp-800-53-ac6-7` — AC-6(7) review of user privileges
- `apra-cps234-para21` — CPS 234 §21 implementation of controls (commensurate)
- `apra-cps234-para27` — CPS 234 §27 testing control effectiveness
- `asd-ism-1647` — ISM-1647 privileged access revalidate/disable at 12 months
- `asd-ism-0407` — ISM-0407 secure access record (incl. last-reviewed)
- `iso-27001-a5-18` — ISO/IEC 27001:2022 A.5.18 access rights lifecycle
- `sox-icfr-13a15f` — 17 CFR 240.13a-15(f) ICFR definition (SOX §404 anchor)
- `mitre-attack-t1078` — Valid Accounts (privilege accumulation / pivot)

---

## Citation verification

Adversarial re-verification performed 2026-06-10. Each URL was re-fetched from the live authoritative source and each quote string-matched (case-insensitive substring) against the fetched body. Control IDs were cross-checked against their authoritative register. **All 10 citations VERIFIED.** No SUSPECT or FABRICATED citations; nothing removed.

| Key | URL resolves | Quote faithful | Control ID valid | Verdict |
|-----|:---:|:---:|:---:|:--------|
| `nist-sp-800-53-ac2j` | yes (200) | yes | yes — AC-2 item present in NIST 800-53r5 AC family | VERIFIED |
| `nist-sp-800-53-ac2-3` | yes (200) | yes | yes — AC-2(3) "Disable Accounts" enhancement present | VERIFIED |
| `nist-sp-800-53-ac6-7` | yes (200) | yes | yes — AC-6(7) "Review of User Privileges" enhancement present | VERIFIED |
| `apra-cps234-para21` | yes (200, official APRA PDF) | yes — full (a)–(d) list matched verbatim | n/a (principles-based para, no control ID) | VERIFIED |
| `apra-cps234-para27` | yes (200, official APRA PDF) | yes — full (a)–(e) list matched verbatim | n/a (principles-based para) | VERIFIED |
| `asd-ism-1647` | yes (200, cyber.gov.au) | yes | yes — page shows "Control: ISM-1647; Revision: 2; Updated: Jun-25; Essential 8: ML2, ML3" immediately preceding the "disabled after 12 months unless revalidated" statement | VERIFIED |
| `asd-ism-0407` | yes (200, cyber.gov.au) | yes — both the control statement and the "when their access was last reviewed" supporting-guidance phrase matched verbatim | yes — "Control: ISM-0407; Revision: 6; Updated: Jun-25" present | VERIFIED (see note) |
| `iso-27001-a5-18` | yes (200) | yes — A.5.18 control statement matched verbatim | A.5.18 is a real ISO/IEC 27001:2022 Annex A control; cited source is a practitioner mirror (iso.org paywalled), already disclosed inline | VERIFIED |
| `sox-icfr-13a15f` | yes (200, Cornell LII) | yes — matched verbatim incl. full "Provide reasonable assurance that transactions are recorded…" prefix | yes — 17 CFR 240.13a-15(f) is the real SEC ICFR-definition rule | VERIFIED |
| `mitre-attack-t1078` | yes (200, attack.mitre.org) | yes — both the "overlap of permissions…" and "Compromised credentials may be used to bypass access controls…" passages matched verbatim | yes — T1078 "Valid Accounts" is a current ATT&CK Enterprise technique | VERIFIED |

**Note on `asd-ism-0407`:** The phrase "when their authorisation was granted and when their access was last reviewed" is drawn from the **supporting (non-control) guidance** paragraph that precedes the numbered ISM-0407 control statement on the cyber.gov.au page, not from the control statement text itself. Section 3 of this document already discloses this explicitly. The numbered ISM-0407 control statement ("A secure record is maintained for the life of systems and their resources that covers the following for each user: their user identification; their signed agreement to abide by system usage policies; …") is also present verbatim. Attribution is honest; verdict stands as VERIFIED.

**Note on `asd-ism-1647` page structure:** On cyber.gov.au the "Control: ISM-xxxx" marker is rendered *after* its control statement. The "disabled after 12 months unless revalidated" text follows the ISM-1647 marker (correct attribution). The "disabled after 45 days of inactivity" text *precedes* the ISM-1647 marker and belongs to the adjacent control (ISM-1648 per this document's Section 3 note) — the 12-month → ISM-1647 mapping in the citation is correct.

# IGA Domain — Role Management / Role Mining / Self-Service Access / Least-Privilege Right-Sizing

Research artifact for the regulated-FI (AU bank) posture-assessment instrument, Phase 3 (IGA domain).
**Scoring model:** process maturity, NOT tool deployment. All use cases are framed around the maturity of the *process*, with the tool/automation only as evidence of repeatability.

**Jurisdiction:** AU-primary — APRA CPS 234, ASD ISM / Essential Eight, plus NIST SP 800-53 Rev 5 (AC family), ISO/IEC 27001:2022 Annex A.5, SOX (SoD).

**Archetype legend (carried from Secrets/PAM domains):**
- **A2** — Migration / remediation / transition program (move from current state to target state).
- **A3** — Discovery / inventory / analytics capability (find what exists, model it).
- **A7** — Workflow / process / approval governance (repeatable request-decision-fulfil cycle).

---

## Area summary

This area covers the *governance of what access looks like* once an identity exists: how access is **modelled** (roles), how it is **requested and granted** (self-service + approval), and how it is **right-sized over time** (least-privilege reduction). It is distinct from the joiner/mover/leaver lifecycle (provisioning) and from access certification (recertification) — though it feeds both. The unifying control objective is **least privilege**: access is restricted to the minimum required to perform the assigned job function, and excess/standing entitlements are continuously driven down.

---

## Use Case 1 — Role Mining & RBAC Baseline (archetype: A3)

**Story.**
As a security/IAM architect at the bank, I want to analyse the actual entitlements held across the workforce and discover natural access patterns (candidate roles) so that I can establish an RBAC baseline that maps job functions to a curated set of business and technical roles, rather than granting entitlements ad hoc per individual. This converts an opaque, individually-managed access estate into a modelled, reviewable one.

**Acceptance criteria.**
- A documented role-mining exercise exists that ingests current entitlement assignments (from at least the in-scope critical systems) and clusters them into candidate roles.
- Candidate roles are reviewed and approved by business/application owners (not auto-promoted), producing an authoritative **role model document** (role name, owner, contained entitlements, eligible population, business justification).
- The role model distinguishes *business roles* (job-function level) from *technical/application roles* (system entitlement bundles), and records the mapping between them.
- Coverage metric is captured: % of users / % of entitlements explained by an approved role vs. remaining one-off ("outlier") assignments.
- A defined cadence exists for re-mining and refreshing the baseline (roles drift as the org changes).

**Population.** Workforce identities and their entitlement assignments across in-scope critical systems; secondarily, application/role owners who validate the model.

**Outcome lens.** *Visibility & model quality* — the org moves from "we grant entitlements individually and cannot explain them" to "X% of access is explained by an owned, approved role." Maturity is measured by coverage, owner accountability, and refresh discipline — not by whether a specific role-mining product is licensed.

**Archetype fit.** A3 — this is a discovery/analytics capability: mine the current state, surface candidate structure, produce an inventory (the role model) that downstream processes consume.

---

## Use Case 2 — Self-Service Access Request & Approval Workflow (archetype: A7)

**Story.**
As an employee (or their manager), I want to request access through a self-service catalogue of approved roles/entitlements and have that request routed through a defined approval chain, so that every grant is authorised, justified, recorded, and tied back to the role model — instead of access being granted via informal channels (email, tickets, verbal asks) with no consistent authorisation or audit trail.

**Acceptance criteria.**
- A request catalogue exposes requestable roles/entitlements with descriptions, owners, and (where applicable) risk ratings; high-risk items are flagged.
- Every request has a defined, enforced approval path (e.g., manager + resource/role owner; additional approver for high-risk or SoD-relevant items).
- Approvals are recorded with approver identity, decision, timestamp, and business justification — producing a **request/approval audit trail** that is queryable per user, per entitlement, and per time window.
- SoD-conflict checks run at request time for SOX-relevant entitlements; conflicting requests are blocked or escalated to a defined exception process.
- Time-bound / expiring access is supported for temporary needs (request need not create permanent standing access).
- A measurable proportion of grants flow through the catalogue/workflow vs. out-of-band; out-of-band grants are the exception and are themselves logged.

**Population.** All workforce identities requesting access; managers and resource/role owners acting as approvers; SoD/risk reviewers for flagged items.

**Outcome lens.** *Authorisation integrity & auditability* — every grant is attributable to an approved request with a recorded approver and justification. Maturity is the % of grants that are workflow-governed, the enforceability of the approval path, and the completeness of the audit trail — not the brand of the request portal.

**Archetype fit.** A7 — this is a workflow/process governance use case: a repeatable request → check → approve → fulfil → record cycle.

---

## Use Case 3 — Least-Privilege Entitlement Right-Sizing / Excess-Access Reduction (archetype: A2)

**Story.**
As an IAM/security owner, I want to identify and remove entitlements that users hold but do not need — based on usage telemetry, role-model deviation, and ownership review — and migrate the estate toward least privilege, so that standing excess access (a primary attack surface for credential abuse) is continuously reduced rather than only added to.

**Acceptance criteria.**
- An **entitlement right-sizing report** is produced periodically that flags excess access using defined signals: unused/dormant entitlements (no usage in N days), entitlements not explained by the user's approved role(s), over-broad/wildcard grants, and orphaned/standing privileged entitlements.
- A defined remediation/migration workflow exists to action flagged items: revoke, downscope, convert to time-bound/just-in-time, or formally accept-with-justification (exception register).
- Reduction is tracked as a trend (e.g., excess entitlements removed per cycle; standing-privilege count over time), demonstrating a *program*, not a one-off cleanup.
- Right-sizing decisions feed back into the role model (UC1) — persistent legitimate access patterns become role updates; removed access does not silently re-accumulate.
- The migration has owner sign-off and a rollback/appeal path so least-privilege enforcement does not break legitimate work.

**Population.** All identities holding in-scope entitlements (workforce + service/non-human where modelled); entitlement/resource owners who approve downscoping; privileged-account holders for standing-privilege reduction.

**Outcome lens.** *Attack-surface reduction* — the org demonstrably drives down standing and excess entitlements over successive cycles. Maturity is measured by the existence of a repeatable reduction program with trend evidence and feedback into the role model — not by a single audit-driven purge.

**Archetype fit.** A2 — this is a migration/remediation program: move the estate from current (over-provisioned) state to target (least-privilege) state, with tracking and feedback.

---

## ATT&CK relevance

These use cases reduce exposure to **excessive privilege abuse**, principally:

- **T1078 — Valid Accounts** (Tactics: Initial Access, Persistence, Privilege Escalation, Defense Evasion). Adversaries abuse the credentials of *existing, legitimate* accounts. The more entitlements an account carries (over-provisioning, standing privilege, role drift), the more an adversary gains the moment that one account is compromised, and the easier it is to blend in with normal activity. Least-privilege right-sizing (UC3), a governed request/approval trail (UC2), and an explainable role model (UC1) all shrink the blast radius and improve detectability of an abused valid account.
  - Verbatim (MITRE): *"Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion."* — https://attack.mitre.org/techniques/T1078/
  - Verbatim (MITRE): *"Compromised credentials may also grant an adversary increased privilege to specific systems or access to restricted areas of the network."* — https://attack.mitre.org/techniques/T1078/

**Mapping rationale:** RBAC baselining + right-sizing directly attack the "increased privilege" amplification described in T1078 — a tightly-scoped valid account is a far less valuable target. The request/approval audit trail (UC2) is the detection/attribution surface for anomalous grant patterns.

---

## Regulatory mapping (verified verbatim quotes)

> All quotes below were fetched from the cited authoritative URLs and confirmed verbatim at research time (2026-06-09). Control IDs are not invented.

### NIST SP 800-53 Rev 5 — AC-6 Least Privilege (base) — primary for UC1, UC3
- **Verbatim:** *"Employ the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks."*
- **Supplemental (verbatim):** *"The principle of least privilege is also applied to system processes, ensuring that the processes have access to systems and operate at privilege levels no higher than necessary to accomplish organizational missions or business functions."*
- **Source:** https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ (NIST SP 800-53 Rev 5 control reference)

### NIST SP 800-53 Rev 5 — AC-6(1) Authorize Access to Security Functions — supports UC2 approval scoping
- **Verbatim:** *"Authorize access for [Assignment: organization-defined individuals and roles] to: [Assignment: organization-defined security functions (deployed in hardware, software, and firmware)]; and [Assignment: organization-defined security-relevant information]."*
- **Supplemental (verbatim):** *"Security functions include establishing system accounts, configuring access authorizations (i.e., permissions, privileges), configuring settings for events to be audited, and establishing intrusion detection parameters."*
- **Source:** https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ac-6-1/

### NIST SP 800-53 Rev 5 — AC-6(5) Privileged Accounts — supports UC3 standing-privilege reduction
- **Verbatim:** *"Restrict privileged accounts on the system to [Assignment: organization-defined personnel or roles]."*
- **Source:** https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ (AC-6(5), Moderate/High baseline)

### NIST SP 800-53 Rev 5 — AC-3 Access Enforcement — primary for UC2 enforcement
- **Verbatim:** *"Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies."*
- **Source:** https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-3/

### ISO/IEC 27001:2022 Annex A — A.5.15 Access control & A.5.18 Access rights
- **A.5.15 (control statement):** *"Rules to control physical and logical access to information and other associated assets should be established and implemented based on business and information security requirements."*
- **A.5.18 (control statement):** *"Access rights to information and other associated assets should be provisioned, reviewed, modified and removed in accordance with the organization's topic-specific policy on and rules for access control."*
- **Note on source quality:** ISO/IEC 27001:2022 is a paywalled standard (iso.org/standard/27001). The control-statement wording above is widely reproduced (e.g., ISMS.online: https://www.isms.online/iso-27001/annex-a-2022/5-15-access-control-2022/ and https://www.isms.online/iso-27001/annex-a-2022/5-18-access-rights-2022/). For audit-grade citation, confirm against the licensed standard text. A.5.15 maps to UC1 (rules/role model), A.5.18 maps to UC2/UC3 (provisioning, review, modification, removal of access rights). **Treated as secondary-confidence** — see returned citations; the precise ISO wording is NOT included in the verified citations array because it was not confirmed against the primary (paywalled) source.

### APRA CPS 234 / CPG 234 — least privilege — primary AU mandate (UC1, UC3)
- **CPG 234 (verbatim):** *"access to, and configuration of, information assets is restricted to the minimum required to achieve business objectives. This is typically referred to as the principle"* [of least privilege].
- **CPG 234 Attachment G (verbatim, control objective):** *"Limit access to what has been authorised based on job role and principle of least privilege"*.
- **Source:** https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_1.pdf (CPG 234 Information Security, June 2019)
- **Note:** CPG 234 is the Prudential Practice *Guide* that elaborates the binding standard **CPS 234**. CPS 234 itself mandates information security controls commensurate with threats/vulnerabilities; CPG 234 articulates the least-privilege principle quoted above. The "job role + least privilege" objective directly underwrites UC1 (role model) and UC3 (right-sizing). CPS 234 standard: https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf

### SOX — Segregation of Duties (SoD) — supports UC2 approval checks
- SOX has no numbered "control IDs" in the NIST/ISO sense; SoD obligations derive from internal-control-over-financial-reporting requirements (SOX §404) and are operationalised via frameworks like COSO/COBIT. In this instrument, SOX is referenced as the *driver* for the SoD-conflict check at request time (UC2) and for the SoD lens on role design (UC1). No verbatim statutory quote is asserted here to avoid fabrication; map SOX to UC2's SoD acceptance criterion as a policy driver, not a quoted control.

---

## Evidence artifacts (what an assessor collects per use case)

| Use case | Primary evidence artifact | Supporting evidence |
|---|---|---|
| UC1 Role mining & RBAC baseline | **Role model document** — role catalogue with role name, owner, contained entitlements, eligible population, business justification; business-vs-technical role mapping | Role-mining run output; owner approval records; coverage metric (% users/entitlements explained); re-mining cadence/policy |
| UC2 Self-service request & approval | **Request/approval audit trail** — per-request record of requester, item, approver(s), decision, timestamp, justification | Request catalogue export; approval-path config; SoD-check results at request time; time-bound/expiry records; out-of-band-grant log |
| UC3 Least-privilege right-sizing | **Entitlement right-sizing report** — flagged excess/unused/unexplained/over-broad entitlements with disposition (revoke/downscope/JIT/accept) | Reduction trend metrics; remediation workflow records; exception register; feedback-to-role-model change log |

---

## Cross-references / notes for build agents

- UC1 (A3) feeds UC2 (A7): the role model is the catalogue source. UC3 (A2) closes the loop back to UC1. Sequence maturity scoring accordingly — a mature UC3 presupposes at least a partial UC1.
- Keep scoring on **process maturity**: presence of an owned role model, enforceability of the approval path, and a *trend* of excess-access reduction — not "do you own an IGA product."
- Strongest, audit-grade citations are the four NIST AC-family controls and CPG 234 (all verbatim-confirmed against primary/near-primary sources). ISO A.5.15/A.5.18 wording should be confirmed against the licensed standard before audit use.

---

## Citation verification

> Adversarial verification pass performed 2026-06-10. Each citation URL was fetched live and the verbatim quote was string-matched against the fetched source text. NIST AC-family control text was confirmed against the CSF Tools mirror of NIST SP 800-53 Rev 5; control IDs (AC-3, AC-6, AC-6(1), AC-6(5)) were confirmed to exist in the authoritative AC family. APRA CPG 234 quotes were confirmed by extracting and decompressing the actual PDF text stream (status 200, content-type application/pdf). MITRE T1078 quotes were confirmed against the live ATT&CK page (status 200).

| Key | URL resolves | Quote faithful | Verdict | Note |
|---|---|---|---|---|
| `nist-sp-800-53-r5-ac6` | yes | yes | VERIFIED | Exact match of AC-6 Control Statement. |
| `nist-sp-800-53-r5-ac6-supplemental` | yes | yes | VERIFIED | Exact match within AC-6 Supplemental Guidance. |
| `nist-sp-800-53-r5-ac6-1` | yes | yes | VERIFIED | Exact match of AC-6(1) Control Statement; URL points to the dedicated AC-6(1) page. |
| `nist-sp-800-53-r5-ac6-5` | yes | yes | VERIFIED | "Restrict privileged accounts on the system to [Assignment: organization-defined personnel or roles]." appears verbatim as the AC-6(5) enhancement on the AC-6 page. Control ID AC-6(5) confirmed in register. |
| `nist-sp-800-53-r5-ac3` | yes | yes | VERIFIED | Exact match of AC-3 Control Statement. |
| `apra-cpg-234-least-privilege` | yes | yes | VERIFIED | Verbatim in CPG 234 PDF: "...information assets is restricted to the minimum required to achieve business objectives. This is typically referred to as the principle [of least privilege]". |
| `apra-cpg-234-job-role` | yes | yes | VERIFIED | Verbatim in CPG 234 PDF, confirmed to fall under "Attachment G: Testing techniques" (nearest preceding heading). |
| `mitre-attack-t1078` | yes | yes | VERIFIED | Exact match of T1078 Valid Accounts description on live ATT&CK page. |
| `mitre-attack-t1078-priv` | yes | yes | VERIFIED | Exact match on live ATT&CK page. |

**Overall: PASS.** All 9 returned citations verified verbatim against resolving authoritative sources. No SUSPECT or FABRICATED citations found; no control IDs invented. No edits to the citation set were required.

> Note (not part of the returned citations array): the ISO/IEC 27001:2022 A.5.15 / A.5.18 control-statement wording in the Regulatory mapping section above remains UNVERIFIED against the primary (paywalled) ISO source — it is sourced only from a third-party reproduction (ISMS.online) and was correctly excluded from the returned citations array by the researcher. Confirm against the licensed standard before audit use. The SOX reference is a policy driver with no asserted verbatim quote, consistent with avoiding fabrication.

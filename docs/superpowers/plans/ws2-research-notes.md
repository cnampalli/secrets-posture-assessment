# WS-2 use-case gap-fill research notes — ready-to-paste content

Verified: 2026-06-11. Anti-fabrication protocol: every regulatory mapping below was checked
against an authoritative source via live fetch this session (or, for APRA/ISM, official PDFs
downloaded and text-extracted locally); verbatim quotes confirmed where stated. Anything not
confirmable is listed under UNVERIFIED at the bottom. **Do not paste trace rows before the
registry additions in §6 — `validate_data.py` gates on registry membership.**

Verification methods of note (mirrors WS1):
- ASD ISM: cyber.gov.au HTML guideline pages still time out; verified against the **official
  cyber.gov.au full ISM PDF (June 2025 release)** downloaded and text-extracted locally,
  cross-checked against ismcontrol.xyz per-control pages (Current, last updated 2025-05-21).
  Both sources agree verbatim on every control checked.
- APRA CPS 234 / CPG 234: official apra.gov.au PDFs (July 2019 / June 2019) downloaded and
  text-extracted locally; §14, §21 and Attachment A item (b) re-confirmed verbatim.
- NIST SP 800-53 R5: csf.tools mirror re-fetched for AC-2 (items f/j), AC-2(3), AC-3, AC-5,
  AC-6 — all verbatim (WS1 already confirmed these against the official OSCAL catalog).
- SOX/ICFR: law.cornell.edu 15 U.S.C. §7262(a) and 17 CFR 240.13a-15(f)(2) re-confirmed verbatim.
- ISO 27001:2022: titles only via isms.online secondary (A.5.3 / A.5.15 / A.5.16 / A.5.18
  confirmed); quotes withheld per the existing iso rows' convention.
- MITRE: attack.mitre.org T1078 opening sentence re-confirmed verbatim.

---

## 0. UC-I-007 vs UC-I-014 differentiation — VERDICT

**Defensible split — proceed.** The two are different control moments:

- **UC-I-007 (existing)** is **detective, post-grant, event-triggered**: a risk-relevant event
  (mover, new privileged grant, role redefinition, SoD violation) fires a scoped
  micro-certification of access the identity **already holds**. The reviewer reacts after the
  event; the access exists while the review runs.
- **UC-I-014 (new)** is **preventive, at-grant, request-triggered**: access is issued
  **time-bound with an expiry**, lapses automatically, and continuation requires a
  **re-request that is re-attested and re-approved at the request gate** before the access
  continues. Nothing is "reviewed later" — the re-validation *is* the grant decision.

Archetypes confirm the split: UC-I-007 maps to A5 (inventory & attestation of an impacted
population) while UC-I-014 maps to A1 (preventive guardrail at a gate), like UC-I-008.
To keep the boundary crisp, UC-I-014's acceptance_criteria explicitly carve out post-event
reviews as UC-I-007's scope, and UC-I-007 needs no change.

---

## 1. UC-I-014 — Request-time re-approval & time-bound access expiry (IGA, Certification)

Priority justification: **P1** — same exposure-shortening class as UC-I-007 (P1); the P0
certification baseline is carried by UC-I-005/006. Not itself a hard regulatory minimum, but
ISM-1647's revalidate-or-disable expectation and AC-2(3)'s expired-account disablement give it
a firm back-map.

### 1.1 use-cases.csv row (append after UC-I-013)

```csv
UC-I-014,FUNCTIONAL,Request-time re-approval & time-bound access expiry,"As an access-governance owner I want high-risk access granted with an explicit expiry and re-validated at the moment it is requested or re-requested — the continuing business need re-attested and re-approved at the request gate — so that continued access is a fresh owned decision at the point of grant rather than a standing entitlement waiting for the next periodic or event-driven review.","High-risk, SoD-relevant and contractor entitlements are granted time-bound with a defined expiry and no perpetual default; lapsed grants are removed automatically within the documented SLA (expired accounts disabled per AC-2(3)) and removal is evidenced; a re-request is evaluated as a fresh request — current business justification re-attested by the requester and re-approved by the accountable owner, never silently auto-renewed; renewal decisions are recorded with approver, timestamp and justification and are distinguishable from first grants; the share of high-risk access carrying an expiry is measured and trending up, and standing privileged access flagged by certification (UC-I-006) is migrated to expiring re-request grants; post-event reviews of already-held access remain in UC-I-007 scope.",IGID-004;IGID-005;IGID-006;IGID-008,Continued access becomes a fresh owned decision at the request gate; standing high-risk access converted to expiring re-approved grants,AC-2(3);AC-2j;ISM-1647;CPS234-§21,P1,nist-sp-800-53-ac2-3;nist-sp-800-53-ac2j;asd-ism-1647;apra-cps-234-para21
```

### 1.2 regulatory-trace.csv changes — ALL are appends to existing rows (no new rows)

All four anchors are already-registered codes with WS1-verified quotes (re-confirmed this
session — see ledger). Exact cell edits:

1. **AC-2(3) row** (line 3):
   - uc_ids: `UC-I-003;UC-I-004;UC-I-005` → `UC-I-003;UC-I-004;UC-I-005;UC-I-014`
   - nhi_ids: `IGID-003;IGID-004;IGID-011` → `IGID-003;IGID-004;IGID-011;IGID-005;IGID-008`
   - evidence_item_ids: `EV-IGA-ORPHAN-SCAN;EV-IGA-CERT-REVOCATION-LOG` → `EV-IGA-ORPHAN-SCAN;EV-IGA-CERT-REVOCATION-LOG;EV-IGA-EXPIRY-REGRANT-LOG`
2. **AC-2j row** (line 4):
   - uc_ids: `UC-I-005` → `UC-I-005;UC-I-007;UC-I-014`
     (NB: **UC-I-007 fold-in fixes pre-existing drift** — UC-I-007's backmap_codes already
     cite AC-2j but the trace row never listed UC-I-007; see §8 observations.)
   - nhi_ids: `IGID-005;IGID-010` → `IGID-005;IGID-010;IGID-004;IGID-006;IGID-008`
   - evidence_item_ids: `EV-IGA-CERT-COMPLETION-REPORT` → `EV-IGA-CERT-COMPLETION-REPORT;EV-IGA-TIMEBOUND-COVERAGE`
3. **ISM-1647 row** (line 12):
   - uc_ids: `UC-I-004;UC-I-006` → `UC-I-004;UC-I-006;UC-I-014`
   - nhi_ids: `IGID-005;IGID-011` → `IGID-005;IGID-011;IGID-004;IGID-008`
4. **CPS234-§21 row** (line 15):
   - uc_ids: `UC-I-001;UC-I-002;UC-I-003;UC-I-004;UC-I-005` → `UC-I-001;UC-I-002;UC-I-003;UC-I-004;UC-I-005;UC-I-014`
   - nhi_ids: `IGID-001;IGID-002;IGID-003;IGID-004;IGID-005` → `IGID-001;IGID-002;IGID-003;IGID-004;IGID-005;IGID-006;IGID-008`

### 1.3 uc-archetype-map.csv row

```csv
UC-I-014,A1,"control=request-time re-approval with time-bound expiry — high-risk access granted with an expiry, removed automatically at lapse and re-validated as a fresh owned decision on every re-request;nhi_population=high-risk, SoD-relevant and contractor entitlement grants;scope=all provisioning channels of the access-request workflow (self-service, manager, renewal / re-request), with post-event reviews of already-held access remaining UC-I-007's scope",Request-time re-approval & time-bound access expiry
```

### 1.4 evidence-catalog.csv rows

```csv
EV-IGA-EXPIRY-REGRANT-LOG,"An expiry / re-grant log: time-bound grants with their expiry, automatic removal at lapse with timestamp and SLA attainment, and re-request decisions recorded with approver, timestamp and justification, distinguishable from first grants and showing no silent auto-renewal.",enforcement,primary,"e.g., a request-workflow export of expired-and-removed grants plus the renewal-decision audit trail",[INTERNAL],nist-sp-800-53-ac2-3;asd-ism-1647
EV-IGA-TIMEBOUND-COVERAGE,"A time-bound coverage metric: the share of high-risk / SoD-relevant / contractor entitlements carrying a defined expiry versus perpetual grants, trended across cycles, with the migration backlog of standing access flagged by certification.",coverage,follow-up,"e.g., a periodic expiry-coverage dashboard with the perpetual-grant burn-down trend",[INTERNAL],nist-sp-800-53-ac2j;apra-cps-234-para21
```

### 1.5 current-state.csv row (illustrative — emerging-governance narrative)

```csv
UC-I-014,PARTIAL,MED,expiry-default-set;rerequest-fresh-approval,,"The request workflow supports time-bound access and some contractor grants carry an expiry, but high-risk entitlements default to perpetual and renewals are waved through without a fresh owner approval, so expiry-driven re-validation is not yet a working control.",PUBLIC,
```

assessment-record.mock.json snippet:

```json
"UC-I-014": {
  "archetype": "A1",
  "answers": {"expiry-default-set": "partial", "rerequest-fresh-approval": "no"},
  "proposed_state": "PARTIAL",
  "final_state": "PARTIAL",
  "overridden": false,
  "rationale": "The request workflow supports time-bound access and some contractor grants carry an expiry, but high-risk entitlements default to perpetual and renewals are waved through without a fresh owner approval, so expiry-driven re-validation is not yet a working control.",
  "confidence": "MED",
  "sensitivity_tag": "PUBLIC"
}
```

---

## 2. UC-I-015 — Requestor-approver separation / self-approval prevention (IGA, SoD)

Priority justification: **P0** — workflow-level preventive SoD control of the same class as
UC-I-008 (P0); self-approval is a classic SOX/ICFR material-weakness finding and CPS234-§14
requires clearly defined approval responsibilities.

### 2.1 use-cases.csv row

```csv
UC-I-015,FUNCTIONAL,Requestor-approver separation / self-approval prevention,"As a risk / compliance owner I want the access-request workflow to enforce that no identity can approve, modify or fulfil its own access request — including administrators editing their own entitlements and approvers appearing in their own approval chain — so that every grant reflects an independent authorisation and self-granted access is structurally impossible rather than merely discouraged.","The workflow engine rejects or re-routes any request where the requester and any approver in the chain resolve to the same identity, including alternate / linked accounts of the same person; delegation and out-of-office rules cannot route an approval back to the requester; direct entitlement edits outside the workflow (including admin-console changes to the editor's own access) are detected and alerted within a defined SLA with a recorded disposition; changes to approval-path rules by workflow administrators are dual-controlled; a periodic self-approval audit report across all grants shows zero unremediated self-approvals and is retained as evidence; break-glass self-grants are auto-flagged for independent post-hoc review.",IGID-005;IGID-006;IGID-007;IGID-008,No identity can author its own access; every grant carries an independent recorded approver,AC-5;A.5.3;CPS234-§14;PL 107-204 §404(a);17 CFR 240.13a-15(f),P0,nist-sp-800-53-ac5;iso-27001-a5-3-unverified;apra-cps-234-para14;sox-pl107-204-s404;sox-icfr-13a15f
```

### 2.2 regulatory-trace.csv changes — ALL appends (no new rows)

1. **AC-5 row** (line 6):
   - uc_ids: `UC-I-008;UC-I-009;UC-I-010` → `UC-I-008;UC-I-009;UC-I-010;UC-I-015`
   - nhi_ids: `IGID-007;IGID-008` → `IGID-007;IGID-008;IGID-005;IGID-006`
   - evidence_item_ids: `EV-IGA-SOD-RULESET;EV-IGA-SOD-VIOLATION-REGISTER;EV-IGA-SOD-BLOCK-LOG` → `EV-IGA-SOD-RULESET;EV-IGA-SOD-VIOLATION-REGISTER;EV-IGA-SOD-BLOCK-LOG;EV-IGA-SELF-APPROVAL-AUDIT`
2. **A.5.3 row** (line 23, framework_role stays INFORMATIVE):
   - uc_ids: `UC-I-008;UC-I-009;UC-I-010` → `UC-I-008;UC-I-009;UC-I-010;UC-I-015`
   - nhi_ids: `IGID-008` → `IGID-008;IGID-006;IGID-007`
3. **CPS234-§14 row** (line 18):
   - uc_ids: `UC-I-009` → `UC-I-009;UC-I-015`
   - nhi_ids: `IGID-007` → `IGID-007;IGID-006;IGID-008`
4. **PL 107-204 §404(a) row** (line 25):
   - uc_ids: `UC-I-008;UC-I-009;UC-I-010` → `UC-I-008;UC-I-009;UC-I-010;UC-I-015`
   - nhi_ids: `IGID-008` → `IGID-008;IGID-006`
5. **17 CFR 240.13a-15(f) row** (line 24):
   - uc_ids: `UC-I-005;UC-I-006;UC-I-008` → `UC-I-005;UC-I-006;UC-I-008;UC-I-015`
   - nhi_ids: `IGID-005;IGID-008` → `IGID-005;IGID-008;IGID-006`

(Note: AC-5's official discussion does not literally say "individuals may not approve their own
requests" — the verbatim control text is "Identify and document [duties]; and Define system
access authorizations to support separation of duties.", confirmed live. The mapping rests on
that control text plus the SOX/ICFR authorizations-of-management clauses, which is honest and
sufficient; do not invent a stronger AC-5 quote.)

### 2.3 uc-archetype-map.csv row

```csv
UC-I-015,A1,"control=requestor-approver separation enforced in the access-request workflow — no identity can approve, modify or fulfil its own access request;nhi_population=all access requests and direct entitlement edits across in-scope systems;scope=every approval chain including delegation and out-of-office routing, admin-console self-edits of the editor's own entitlements, and break-glass self-grants",Requestor-approver separation / self-approval prevention
```

### 2.4 evidence-catalog.csv rows

```csv
EV-IGA-SELF-APPROVAL-AUDIT,"The workflow configuration showing the requester-not-equal-approver rule (including delegation and out-of-office routing) plus a periodic self-approval audit report across all grants evidencing zero unremediated self-approvals, retained per evidence policy.",enforcement,primary,"e.g., the approval-policy configuration export plus the latest self-approval audit report",[INTERNAL],nist-sp-800-53-ac5;sox-icfr-13a15f
EV-IGA-ADMIN-SELF-EDIT-ALERT,"Evidence that out-of-band entitlement edits — including an administrator changing their own access in an application console — are detected and alerted within a defined SLA, with a sample alert and its recorded disposition (revert, justify or escalate).",exception,follow-up,"e.g., a detection rule for out-of-band self-edits plus a sample alert and disposition record",[INTERNAL],nist-sp-800-53-ac5;apra-cps-234-para14
```

### 2.5 current-state.csv row

```csv
UC-I-015,PARTIAL,MED,self-approval-blocked;admin-self-edit-alerted,,"The workflow blocks the trivial requester-equals-approver case, but delegation re-routing is not checked against the requester and application administrators can still edit their own entitlements in admin consoles without detection or alerting; no periodic self-approval audit report is produced.",PUBLIC,
```

assessment-record.mock.json snippet:

```json
"UC-I-015": {
  "archetype": "A1",
  "answers": {"self-approval-blocked": "partial", "admin-self-edit-alerted": "no"},
  "proposed_state": "PARTIAL",
  "final_state": "PARTIAL",
  "overridden": false,
  "rationale": "The workflow blocks the trivial requester-equals-approver case, but delegation re-routing is not checked against the requester and application administrators can still edit their own entitlements in admin consoles without detection or alerting; no periodic self-approval audit report is produced.",
  "confidence": "MED",
  "sensitivity_tag": "PUBLIC"
}
```

---

## 3. UC-I-016 — Unstructured-data / data-access entitlement governance (IGA, Role/Request)

Priority justification: **P1** — large real-world exposure (ownerless shares, anyone-links,
public buckets) but it builds on the P0 foundations (request workflow, certification engine);
typical FI sequencing lands data-access governance after application-access governance.

### 3.1 use-cases.csv row

```csv
UC-I-016,FUNCTIONAL,Unstructured-data / data-access entitlement governance,"As a data-access governance owner I want entitlements over unstructured data repositories — file shares, SharePoint / OneDrive / Teams sites and cloud object-storage buckets — governed like application access, with each repository mapped to a named business owner, its effective access resolvable and reviewed, and open access removed, so that least privilege covers the data estate and not only applications.","An inventory of in-scope unstructured-data repositories exists with a named business owner and data classification per repository, and inventory coverage is measured and trending up; effective access per repository is resolvable end-to-end including nested groups, sharing links and anonymous / org-wide grants; open access (Everyone-type groups, anyone-with-link sharing, public buckets) is detected on a defined scan cadence and removed or accepted via a recorded time-bound exception with owner; repository owners certify access on a risk-tiered cadence aligned to classification and revocations are actioned within SLA; provisioning of a new repository requires an owner and classification before access is granted; access to the highest-classification repositories routes through the access-request workflow rather than ad-hoc sharing.",IGID-005;IGID-006;IGID-010,Least privilege extended from applications to the unstructured-data estate; ownerless and open repositories eliminated,A.5.18;A.5.15;AC-3;AC-6;CPG234-Att-A,P1,iso-27001-a5-18-quote-withheld;iso-27001-a5-15-unverified;nist-sp-800-53-ac3;nist-sp-800-53-ac6;apra-cpg-234-least-privilege
```

### 3.2 regulatory-trace.csv changes — ALL appends (no new rows)

1. **A.5.18 row** (line 20, BACK-MAP, quote withheld):
   - uc_ids: `UC-I-001;UC-I-002;UC-I-003;UC-I-004;UC-I-005;UC-I-006;UC-I-012;UC-I-013` → `UC-I-001;UC-I-002;UC-I-003;UC-I-004;UC-I-005;UC-I-006;UC-I-012;UC-I-013;UC-I-016`
   - nhi_ids: `IGID-001;IGID-002;IGID-003;IGID-005` → `IGID-001;IGID-002;IGID-003;IGID-005;IGID-006;IGID-010`
   - evidence_item_ids: `EV-IGA-CERT-COMPLETION-REPORT` → `EV-IGA-CERT-COMPLETION-REPORT;EV-IGA-DATA-REPO-REGISTER`
2. **A.5.15 row** (line 22, INFORMATIVE):
   - uc_ids: `UC-I-011` → `UC-I-011;UC-I-016`
   - nhi_ids: `IGID-007;IGID-010` → `IGID-007;IGID-010;IGID-005;IGID-006`
3. **AC-3 row** (line 5):
   - uc_ids: `UC-I-012` → `UC-I-012;UC-I-016`
   - nhi_ids: `IGID-001;IGID-006;IGID-010` → `IGID-001;IGID-006;IGID-010;IGID-005`
4. **AC-6 row** (line 7):
   - uc_ids: `UC-I-011;UC-I-012;UC-I-013` → `UC-I-011;UC-I-012;UC-I-013;UC-I-016`
   - nhi_ids: `IGID-002;IGID-005;IGID-012` → `IGID-002;IGID-005;IGID-012;IGID-006;IGID-010`
5. **CPG234-Att-A row** (line 19):
   - uc_ids: `UC-I-011;UC-I-013` → `UC-I-011;UC-I-013;UC-I-016`
   - nhi_ids: `IGID-002;IGID-005` → `IGID-002;IGID-005;IGID-006;IGID-010`

### 3.3 uc-archetype-map.csv row

```csv
UC-I-016,A5,"nhi_population=unstructured-data repositories (file shares, SharePoint / OneDrive / Teams sites, cloud object-storage buckets) reconciled to a named business owner and a data classification, and the identities holding effective access to them;threshold=95%;cadence=risk-tiered owner certification aligned to data classification;system=the IGA certification module and data-access remediation queue",Unstructured-data / data-access entitlement governance
```

### 3.4 evidence-catalog.csv rows

```csv
EV-IGA-DATA-REPO-REGISTER,"An unstructured-data repository register: per repository the named business owner, data classification, effective-access resolution (including nested groups and sharing links) and last owner certification date, with a coverage metric of registered versus discovered repositories.",coverage,primary,"e.g., a repository inventory export with owner, classification and certification-status columns plus the coverage trend",[INTERNAL],nist-sp-800-53-ac3;apra-cpg-234-least-privilege
EV-IGA-DATA-OPEN-ACCESS-SCAN,"An open-access scan report over the unstructured-data estate detecting Everyone-type groups, anyone-with-link sharing and public buckets, with per-finding disposition (removed or accepted via a recorded time-bound exception with owner) traceable across scan cycles.",exception,follow-up,"e.g., a periodic open-access scan output with remediation / exception dispositions",[INTERNAL],nist-sp-800-53-ac6;apra-cpg-234-least-privilege
```

### 3.5 current-state.csv row

```csv
UC-I-016,GAP,MED,repo-owner-inventory;open-access-removed,,"Access governance covers applications only; file shares, SharePoint sites and cloud buckets have no owner inventory, sharing links and org-wide grants proliferate unreviewed, and there is no open-access scanning or repository-owner certification.",PUBLIC,
```

assessment-record.mock.json snippet:

```json
"UC-I-016": {
  "archetype": "A5",
  "answers": {"repo-owner-inventory": "no", "open-access-removed": "no"},
  "proposed_state": "GAP",
  "final_state": "GAP",
  "overridden": false,
  "rationale": "Access governance covers applications only; file shares, SharePoint sites and cloud buckets have no owner inventory, sharing links and org-wide grants proliferate unreviewed, and there is no open-access scanning or repository-owner certification.",
  "confidence": "MED",
  "sensitivity_tag": "PUBLIC"
}
```

---

## 4. UC-P-018 — Secure admin workstations (SAW/PAW) tier-0 isolation (PAM)

**New ISM codes found and fully verified** (official ISM June 2025 PDF + ismcontrol.xyz, both
verbatim-identical):

| code | verbatim current text | rev | E8 | guideline / section |
|---|---|---|---|---|
| ISM-1898 | "Secure Admin Workstations are used in the performance of administrative activities." | Rev 0, Dec-23 | ML3 | System management → Separate privileged operating environments |
| ISM-1380 | "Privileged users use separate privileged and unprivileged operating environments." | Rev 5, Sep-21 | ML1–ML3 | System management → Separate privileged operating environments |
| ISM-1175 | "Privileged user accounts (excluding those explicitly authorised to access online services) are prevented from accessing the internet, email and web services." | Rev 6, Sep-24 | ML1–ML3 | Personnel security → Privileged access to systems |

Also verified but deliberately NOT mapped/registered (kept lean; available if scope widens):
ISM-1687 ("Privileged operating environments are not virtualised within unprivileged operating
environments.", Rev 0, E8 ML2/ML3), ISM-1688 ("Unprivileged user accounts cannot logon to
privileged operating environments.", Rev 1), ISM-1689 ("Privileged user accounts (excluding
local administrator accounts) cannot logon to unprivileged operating environments.", Rev 1).
**ISM-1653 is REMOVED (Dec 2023, merged into ISM-1175) — do not use.**

Priority justification: **P1** — SAW usage is an Essential Eight **ML3** marker (E8-RAP-ML3)
and the mock profile is ML2-ish; tier-0 isolation is high-value but sequenced behind the P0
vault/proxy/MFA/JIT foundations (UC-P-001/002/004/007), matching how UC-P-003 (recording) and
UC-P-011 (vendor access) carry P1.

### 4.1 pam/use-cases.csv row (append after UC-P-017; PAM schema — outcome_lens is lens codes)

```csv
UC-P-018,FUNCTIONAL,Secure admin workstations (SAW/PAW) for tier-0 isolation,"As a security architect I want all tier-0 and high-impact administration performed from dedicated hardened Secure Admin Workstations isolated from email and web browsing so that credential theft on a standard endpoint can never reach a privileged session.","Tier-0 and in-scope privileged administration performed only from dedicated SAWs/PAWs hardened to a documented baseline (application control, no standing local admin for the operator, patched, monitored); the privileged operating environment is separated from any unprivileged environment and not virtualised inside one; privileged user accounts used from SAWs prevented from accessing internet, email and web services; non-SAW access to tier-0 targets technically blocked at the proxy / conditional-access layer with attempts alerted; SAW fleet inventory and baseline compliance tracked, with exceptions registered with owner and expiry.",PID-001;PID-003;PID-008;PID-009;PID-016,E8-RestrictAdminPriv;ZT-Pillar-Device;ZT-Pillar-Identity,CPS234-§21;ISM-1898;ISM-1380;ISM-1175;E8-RAP-ML2;E8-RAP-ML3,P1,ms-pth-mitigation-2014;gsa-privileged-identity-playbook-2024;acsc-e8-changes-nov2023
```

### 4.2 pam/regulatory-trace.csv changes

**NEW rows** (paste after the existing asd-ism block, i.e. after the ISM-1619 row; PAM URL
style mirrored from PAM's own rows). Registry additions in §6 MUST land first:

```csv
asd-ism,BACK-MAP,ISM-1898,Secure Admin Workstations for administrative activities,UC-P-018,PID-001;PID-003;PID-008;PID-009;PID-016,N/A,https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism/cyber-security-guidelines/guidelines-system-management,Secure Admin Workstations are used in the performance of administrative activities.,asd-ism-2024;asd-ism-sysmgmt-2025,EV-PAM-SAW-INVENTORY
asd-ism,BACK-MAP,ISM-1380,Separate privileged and unprivileged operating environments,UC-P-018,PID-001;PID-003;PID-008;PID-009;PID-016,N/A,https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism/cyber-security-guidelines/guidelines-system-management,Privileged users use separate privileged and unprivileged operating environments.,asd-ism-2024;asd-ism-sysmgmt-2025,EV-PAM-SAW-INVENTORY
asd-ism,BACK-MAP,ISM-1175,Privileged accounts prevented from internet/email/web access,UC-P-018,PID-001;PID-003;PID-008;PID-009;PID-016,N/A,https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism/cyber-security-guidelines/guidelines-personnel-security,"Privileged user accounts (excluding those explicitly authorised to access online services) are prevented from accessing the internet, email and web services.",asd-ism-2024;asd-ism-personnel-2025,EV-PAM-SAW-ACCESS-BLOCK
```

**NEW threat-context row** (PAM trace has no MITRE rows yet; mirrors the IGA T1078 row —
defensible: SAW isolation is the canonical mitigation for credential theft enabling
Valid-Accounts abuse, per Microsoft's PAW guidance already cited by this UC). Paste at the end:

```csv
mitre-attack,THREAT-CONTEXT,T1078,Valid Accounts,UC-P-018,PID-001;PID-016,N/A,https://attack.mitre.org/techniques/T1078/,"Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion.",mitre-t1078-valid-accounts,
```

**Appends to existing rows:**

1. **E8-RAP-ML3 row** (line 13) — quote IS the SAW expectation; this is the canonical reuse:
   - uc_ids: `UC-P-004` → `UC-P-004;UC-P-018`
   - nhi_ids: `PID-001;PID-003;PID-007;PID-010;PID-014;PID-019` → `PID-001;PID-003;PID-007;PID-010;PID-014;PID-019;PID-008;PID-009;PID-016`
   - evidence_item_ids: (empty) → `EV-PAM-SAW-INVENTORY`
2. **E8-RAP-ML2 row** (line 12) — quote is the internet/email/web prevention expectation:
   - uc_ids: `UC-P-001;UC-P-002;UC-P-009;UC-P-010;UC-P-011;UC-P-012;UC-P-014` → `UC-P-001;UC-P-002;UC-P-009;UC-P-010;UC-P-011;UC-P-012;UC-P-014;UC-P-018`
   - nhi_ids: unchanged (all five PIDs already present)
3. **CPS234-§21 row** (line 18):
   - uc_ids: `...;UC-P-017` → `...;UC-P-017;UC-P-018`
   - nhi_ids: unchanged (all five PIDs already present)

### 4.3 pam/uc-archetype-map.csv row

```csv
UC-P-018,A1,"control=privileged administration permitted only from dedicated hardened Secure Admin Workstations, with non-SAW access to tier-0 targets blocked at the proxy / conditional-access layer;nhi_population=tier-0 and in-scope privileged sessions and the administrators behind them;scope=all tier-0 administrative paths including directory, virtualization, network devices and the PAM platform itself",Secure admin workstations (SAW/PAW) for tier-0 isolation
```

### 4.4 pam/evidence-catalog.csv rows

```csv
EV-PAM-SAW-INVENTORY,"A SAW/PAW fleet inventory mapping each tier-0 / privileged administrator to a dedicated hardened admin workstation, with hardening-baseline compliance status (application control, no standing local admin, patch state) and exceptions registered with owner and expiry.",coverage,primary,"e.g., a SAW device inventory with per-device baseline-compliance status and the tier-0 operator mapping",[INTERNAL],acsc-e8-changes-nov2023;ms-pth-mitigation-2014
EV-PAM-SAW-ACCESS-BLOCK,"Evidence that access to tier-0 targets from non-SAW devices is technically blocked (proxy or conditional-access device filter) and that privileged accounts used from SAWs are prevented from reaching internet, email and web services, with a sample blocked-attempt alert.",enforcement,follow-up,"e.g., the conditional-access / proxy device-filter rule plus a sample blocked-attempt alert",[INTERNAL],acsc-e8-mm-nov2023;gartner-pam-mq-2024
```

### 4.5 pam/current-state.csv row (fits the ML2-ish mock profile)

```csv
UC-P-018,PARTIAL,MED,priv-env-separated;saw-dedicated;nonsaw-blocked,,"Administrators use separate privileged accounts and sessions are brokered through the PAM proxy, but administration is performed from standard SOE workstations rather than dedicated hardened SAWs, and tier-0 logon is not yet restricted to compliant devices, so a compromised daily-driver endpoint can still host a privileged session.",PUBLIC,
```

assessment-record.mock.json snippet:

```json
"UC-P-018": {
  "archetype": "A1",
  "answers": {"priv-env-separated": "yes", "saw-dedicated": "no", "nonsaw-blocked": "no"},
  "proposed_state": "PARTIAL",
  "final_state": "PARTIAL",
  "overridden": false,
  "rationale": "Administrators use separate privileged accounts and sessions are brokered through the PAM proxy, but administration is performed from standard SOE workstations rather than dedicated hardened SAWs, and tier-0 logon is not yet restricted to compliant devices, so a compromised daily-driver endpoint can still host a privileged session.",
  "confidence": "MED",
  "sensitivity_tag": "PUBLIC"
}
```

---

## 5. NOT used / negative findings

- **ISM-1653** — REMOVED from the ISM (Dec 2023; merged into ISM-1175). Excluded.
- **ISM-1687/1688/1689** — verified verbatim but not mapped (acceptance criteria already carry
  the separation requirement via ISM-1380; add later only if a dedicated virtualisation UC appears).
- **E8-PA-ML1/E8-PA-ML2** (registered) — not used: the PAM trace's established E8
  restrict-admin-privileges namespace is `E8-RAP-*`; introducing the parallel `E8-PA-*` codes
  into the PAM trace would split the lens. Left for the registry owner to reconcile.
- **AC-2(2) (temporary-account auto-disable)** — would fit UC-I-014 but is NOT registered;
  AC-2(3) "Have expired" covers the need, so no new NIST code was added (anti-fabrication: less
  surface). If wanted later, it must go through full WS1-style verification.

## 6. Registry + provenance + bibliography additions (required BEFORE pasting §4.2)

### 6.1 matrix/config/control-id-registry.yaml — asd-ism controls list

Replace the `asd-ism` controls list with (adds ISM-1175, ISM-1380, ISM-1898, kept sorted), and
add the comment line:

```yaml
  # ISM-1175 / ISM-1380 / ISM-1898 verified 2026-06-11 vs cyber.gov.au ISM June 2025 PDF
  # (downloaded + text-extracted) + ismcontrol.xyz (PAM SAW trace, WS2). NB: ISM-1653 is
  # REMOVED (merged into ISM-1175) — deliberately NOT registered.
  controls: [ISM-0027, ISM-0039, ISM-0043, ISM-0140, ISM-0252, ISM-0363, ISM-0401,
    ISM-0407, ISM-0421, ISM-0430, ISM-0457, ISM-0469, ISM-0471, ISM-0481, ISM-0507,
    ISM-1139, ISM-1173, ISM-1175, ISM-1181, ISM-1192, ISM-1211, ISM-1247, ISM-1256,
    ISM-1275, ISM-1304, ISM-1323, ISM-1324, ISM-1380, ISM-1401, ISM-1404, ISM-1405,
    ISM-1437, ISM-1452, ISM-1504, ISM-1570, ISM-1611, ISM-1613, ISM-1619, ISM-1647,
    ISM-1656, ISM-1690, ISM-1707, ISM-1730, ISM-1795, ISM-1796, ISM-1898, ISM-1917]
```

No new framework slug is introduced (asd-ism, essential-8, apra-cps-234 and mitre-attack all
exist), so **no new data-provenance.yaml entry is required**. Optional freshness touch-up to
the existing `asd-ism` provenance entry:

```yaml
  note: "Corrected mapping; SAW controls (ISM-1175/1380/1898) re-verified 2026-06-11 vs the June 2025 ISM release. Confirm against the current cyber.gov.au ISM release before publishing."
```

### 6.2 meta/citations.bib — new entry (PAM trace rows cite `asd-ism-sysmgmt-2025`)

```bibtex
@misc{asd-ism-sysmgmt-2025,
  title  = {ISM Cyber Security Guidelines — System Management},
  author = {{Australian Signals Directorate}},
  year   = {2025},
  url    = {https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism/cyber-security-guidelines/guidelines-system-management},
  note   = {[PUBLIC] Source guideline for ISM-1380, ISM-1687, ISM-1688, ISM-1689, ISM-1898 (Separate privileged operating environments / Secure Admin Workstations). Verified against the June 2025 ISM full PDF; E8 Restrict Admin Privileges ML3 anchor for SAW usage.}
}
```

(`asd-ism-personnel-2025` already exists in the bib and carries the right URL for ISM-1175's
guideline chapter.)

## 7. WS1-deferred fixes — exact old→new strings

### 7.1 (a) IGA use-cases.csv backmap_codes style alignment (verified against actual file)

Every change, one per cell (only the listed substrings change inside the cell):

| line | uc_id | old substring | new substring |
|---|---|---|---|
| 2 | UC-I-001 | `ISO-A.5.18` | `A.5.18` |
| 2 | UC-I-001 | `ISO-A.5.16` | `A.5.16` |
| 3 | UC-I-002 | `ISO-A.5.18` | `A.5.18` |
| 4 | UC-I-003 | `ISO-A.5.18` | `A.5.18` |
| 4 | UC-I-003 | `ISO-A.5.16` | `A.5.16` |
| 6 | UC-I-005 | `ISO-A.5.18` | `A.5.18` |
| 6 | UC-I-005 | `ICFR-13a15f` | `17 CFR 240.13a-15(f)` |
| 7 | UC-I-006 | `ICFR-13a15f` | `17 CFR 240.13a-15(f)` |
| 8 | UC-I-007 | `ISO-A.5.18` | `A.5.18` |
| 9 | UC-I-008 | `SOX-§404` | `PL 107-204 §404(a)` |
| 9 | UC-I-008 | `SOX-§103` | `PL 107-204 §103` |
| 9 | UC-I-008 | `ICFR-13a15f` | `17 CFR 240.13a-15(f)` |
| 10 | UC-I-009 | `SOX-§404` | `PL 107-204 §404(a)` |
| 10 | UC-I-009 | `SOX-§103` | `PL 107-204 §103` |
| 11 | UC-I-010 | `SOX-§404` | `PL 107-204 §404(a)` |
| 11 | UC-I-010 | `SOX-§103` | `PL 107-204 §103` |
| 12 | UC-I-011 | `ISO-A.5.15` | `A.5.15` |
| 13 | UC-I-012 | `ISO-A.5.18` | `A.5.18` |
| 14 | UC-I-013 | `ISO-A.5.18` | `A.5.18` |

Equivalent global replaces over `matrix/domains/iga/use-cases.csv` ONLY (safe — none of these
substrings appear outside backmap_codes cells in that file): `ISO-A.5.18`→`A.5.18`,
`ISO-A.5.16`→`A.5.16`, `ISO-A.5.15`→`A.5.15`, `SOX-§404`→`PL 107-204 §404(a)`,
`SOX-§103`→`PL 107-204 §103`, `ICFR-13a15f`→`17 CFR 240.13a-15(f)`. Do the `SOX-§404` replace
verbatim as written (the file has no `SOX-§404(a)` variant). Resulting cells remain unquoted —
the new codes contain spaces and `§` but no commas, so CSV stays valid.

### 7.2 (b) Dangling citation key `iso-27001-a5-18` → `iso-27001-a5-18-quote-withheld`

Global replace `iso-27001-a5-18` → `iso-27001-a5-18-quote-withheld` in exactly these two files
(verified: neither file contains the `-quote-withheld` form today, so the replace cannot
double-suffix):

- `matrix/domains/iga/use-cases.csv` — 7 occurrences: lines 2 (UC-I-001), 3 (UC-I-002),
  4 (UC-I-003), 6 (UC-I-005), 8 (UC-I-007), 13 (UC-I-012), 14 (UC-I-013).
- `matrix/domains/iga/identity-catalog.csv` — 8 occurrences: lines 2–7 (IGID-001…IGID-006),
  11 (IGID-010), 12 (IGID-011).

## 8. Observations logged while reading (not WS2 edits unless noted)

1. **UC-I-007 trace drift (FIXED via §1.2.2):** UC-I-007's backmap_codes cite `AC-2j` and
   `ISO-A.5.18` but neither trace row lists UC-I-007 in uc_ids. The AC-2j side is folded into
   the §1.2.2 append. For symmetry the A.5.18 row (line 20) uc_ids could also gain `UC-I-007`
   when applying §3.2.1 — recommended; if adopted the cell becomes
   `UC-I-001;UC-I-002;UC-I-003;UC-I-004;UC-I-005;UC-I-006;UC-I-007;UC-I-012;UC-I-013;UC-I-016`.
2. **Mock archetype vs map drift (pre-existing):** assessment-record.mock.json `archetype`
   fields (A1/A2 only) do not match uc-archetype-map.csv (e.g. UC-I-001 map=A2 mock=A1,
   UC-I-007 map=A5 mock=A2). The new snippets above use the map's archetypes; flag the
   existing drift to the instrument owner.
3. **Bib placement of ISM-1175:** `asd-ism-ia-2025` (citations.bib) lists ISM-1175 under the
   System Hardening guideline, but the June 2025 ISM places "Privileged access to systems"
   under Personnel Security (matches ismcontrol.xyz topic and the IGA trace's ISM-1647 row).
   The new ISM-1175 trace row therefore cites `asd-ism-personnel-2025`.
4. After pasting, run `validate_data.py` (registry membership + provenance gates) before commit.

---

## 9. Verification ledger (this session, 2026-06-11)

| # | URL / source | what was checked | verbatim confirmed? |
|---|---|---|---|
| 1 | https://ismcontrol.xyz/1898/ | ISM-1898 control text, Rev 0 Dec-23 | Y |
| 2 | https://ismcontrol.xyz/1380/ | ISM-1380 control text + revision history | Y |
| 3 | https://ismcontrol.xyz/1687/ | ISM-1687 control text | Y (not mapped) |
| 4 | https://ismcontrol.xyz/1653/ | ISM-1653 status | Y — REMOVED Dec 2023, merged into ISM-1175; excluded |
| 5 | https://ismcontrol.xyz/1175/ | ISM-1175 current text, Rev Sep-24 | Y |
| 6 | https://ismcontrol.xyz/1647/ | ISM-1647 current text (UC-I-014 reuse) | Y |
| 7 | https://www.cyber.gov.au/sites/default/files/2025-07/Information%20security%20manual%20(June%202025).pdf | full official ISM PDF downloaded + text-extracted; ISM-1898/1380/1687/1175/1688/1689 wording, revisions, E8 ML tags, chapter placement | Y (all six) |
| 8 | https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-system-management | HTML guideline page | N — fetch TIMED OUT (matches WS1); official PDF (#7) substituted |
| 9 | https://blueprint.asd.gov.au/security-and-governance/essential-eight/restrict-administrative-privileges/ | candidate second source | N — page carries no ISM control text; not used |
| 10 | https://attack.mitre.org/techniques/T1078/ | T1078 description sentence (PAM threat-context row) | Y |
| 11 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ac-2-3/ | AC-2(3) control text | Y |
| 12 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ | AC-2 items f and j | Y |
| 13 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-5/ | AC-5 control text + discussion (no self-approval sentence — noted in §2.2) | Y |
| 14 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-3/ | AC-3 control text | Y |
| 15 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ | AC-6 control text | Y |
| 16 | https://www.law.cornell.edu/cfr/text/17/240.13a-15 | 13a-15(f)(2) ICFR authorizations clause | Y |
| 17 | https://www.law.cornell.edu/uscode/text/15/7262 | §404(a) items (1)/(2) | Y |
| 18 | https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf | CPS 234 §14 and §21 (PDF downloaded + extracted) | Y |
| 19 | https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_1.pdf | CPG 234 Attachment A item (b) least privilege | Y |
| 20 | https://www.isms.online/iso-27001/annex-a/ | A.5.3 / A.5.15 / A.5.16 / A.5.18 titles (secondary) | Y (titles only) |

### UNVERIFIED / known limits

- **ISO/IEC 27001:2022 full control text** — licensed; titles verified via secondary mirror
  only, quotes withheld by design (existing convention; `A.5.3`/`A.5.15` rows remain
  INFORMATIVE with `-unverified` citation keys).
- **Essential Eight maturity-model quotes on E8-RAP-ML2 / E8-RAP-ML3 rows** — not re-fetched
  this session; rows are reused as-is (only uc_ids/nhi_ids appended), quotes were verified when
  the PAM trace was built. Re-verify on the next E8 refresh cycle.
- **cyber.gov.au HTML guideline pages** — consistently time out; evidence_url values keep the
  guideline-page convention of existing rows, but verification was performed against the
  official June 2025 ISM PDF + ismcontrol.xyz instead.
- Nothing else in this note is unverified; no quote or control ID above was reproduced from
  memory.

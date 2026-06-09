# IGA Phase 3 — Consolidated Research Summary (Build-Agent Input)

**Purpose.** Single authoritative hand-off from verified per-area IGA research to the build agent.
Consolidates the use-case list, citation table, regulatory-trace plan, identity taxonomy, vendor-fit
grid, and a data-quality ledger. Compiled 2026-06-10 from the six verified per-area files in this
directory.

**Scoring model (do not violate):** the instrument scores **process maturity, NOT tool deployment**.
**Jurisdiction:** AU-primary (APRA CPS 234, ASD ISM / Essential Eight) + NIST SP 800-53r5 (AC family),
ISO/IEC 27001:2022 Annex A.5, SOX/ICFR (SoD only).

Source files:
- `jml.md` · `certification.md` · `sod.md` · `role-request.md` · `identity-taxonomy.md` · `vendor-fit.md`

---

## 1. Consolidated IGA use-case list (UC-I-NNN scheme)

ID scheme: `UC-I-NNN`. Twelve use cases across four areas. The numbering reconciles the per-file
mappings: JML→001–004, Certification→005–007, SoD→008–010, Role/Request→011–013. Where a per-file
used a different local id, the mapping is noted.

| uc_id | area | short_title | archetype | source file (local id) |
|-------|------|-------------|-----------|------------------------|
| UC-I-001 | JML | Automated joiner / birthright provisioning | A2 (migration/threshold) | jml.md (UC-JML-01) |
| UC-I-002 | JML | Mover access recalculation on transfer | A7 (process-maturity) | jml.md (UC-JML-02) |
| UC-I-003 | JML | Timely leaver de-provisioning within SLA | A2 (migration/threshold) | jml.md (UC-JML-03) |
| UC-I-004 | JML | Orphan / dormant account detection | A5 (inventory & attestation) | jml.md (UC-JML-04, new) |
| UC-I-005 | Certification | Periodic access certification campaigns | A5 (inventory & attestation) | certification.md (UC-I-004) |
| UC-I-006 | Certification | High-risk / privileged access certification sign-off | A8 (high-risk sign-off) | certification.md (UC-I-005) |
| UC-I-007 | Certification | Micro-/event-driven recertification on change | A5 (inventory & attestation, event grain) | certification.md (proposed UC-I-012) |
| UC-I-008 | SoD | Preventive SoD checks at access-request time | A1 (preventive control) | sod.md (UC-SOD-1) |
| UC-I-009 | SoD | SoD policy register & violation-management process | A7 (governance/process) | sod.md (UC-SOD-2) |
| UC-I-010 | SoD | Detective SoD scanning + mitigating-control tracking | A3 (detective/monitoring) | sod.md (UC-SOD-3) |
| UC-I-011 | Role/Request | Role mining & RBAC baseline | A3 (discovery/analytics) | role-request.md (UC1) |
| UC-I-012 | Role/Request | Self-service access request & approval workflow | A7 (workflow/process) | role-request.md (UC2) |
| UC-I-013 | Role/Request | Least-privilege entitlement right-sizing | A2 (migration/remediation) | role-request.md (UC3) |

> **Numbering caveat for the build agent.** The original spike `use-cases.csv` numbered some UCs
> differently (e.g. certification used UC-I-004/005, SoD used UC-I-006/007/008). The table above is a
> *clean re-sequenced* 1–13 scheme by area. If the build must preserve the legacy spike ids, treat the
> "source file (local id)" column as the crosswalk and re-key accordingly. Pick ONE scheme and keep it
> stable — do not mix. 13 UCs total (target band was 11–13).

---

## 2. Consolidated citation table

Per-citation: key | url | source type | one-line | verdict. **No FABRICATED citations exist** — none
to exclude. **One SUSPECT** citation is retained with a warning (section attribution was corrected, not
the quote). Verdicts are from the adversarial verification passes recorded in each file.

| key | url | source | one-line | verdict |
|-----|-----|--------|----------|---------|
| mitre-t1078-valid-accounts | https://attack.mitre.org/techniques/T1078/ | MITRE ATT&CK (primary) | Valid Accounts: abuse of existing-account credentials | VERIFIED |
| mitre-t1098-account-manipulation | https://attack.mitre.org/techniques/T1098/ | MITRE ATT&CK (primary) | Account Manipulation: maintain/elevate access | VERIFIED |
| nist-sp-800-53-ac2 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ | csf.tools mirror of NIST 800-53r5 | AC-2 Account Management — full lifecycle | VERIFIED (mirror; csrc.nist.gov primary) |
| nist-sp-800-53-ac2-3 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ac-2-3/ | csf.tools mirror of NIST 800-53r5 | AC-2(3) Disable Accounts | VERIFIED (mirror) |
| nist-sp-800-53-ac2j | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ | csf.tools mirror of NIST 800-53r5 | AC-2(j) periodic account review | VERIFIED (mirror) |
| nist-sp-800-53-ac3 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-3/ | csf.tools mirror of NIST 800-53r5 | AC-3 Access Enforcement | VERIFIED (mirror) |
| nist-sp-800-53-ac5 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-5/ | csf.tools mirror / NIST OSCAL primary | AC-5 Separation of Duties | VERIFIED (also confirmed in OSCAL primary) |
| nist-sp-800-53-ac6 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ | csf.tools mirror of NIST 800-53r5 | AC-6 Least Privilege | VERIFIED (mirror) |
| nist-sp-800-53-ac6-1 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ac-6-1/ | csf.tools mirror of NIST 800-53r5 | AC-6(1) Authorize Access to Security Functions | VERIFIED (mirror) |
| nist-sp-800-53-ac6-5 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ | csf.tools mirror of NIST 800-53r5 | AC-6(5) Privileged Accounts restriction | VERIFIED (mirror) |
| nist-sp-800-53-ac6-7 | https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/ | csf.tools mirror of NIST 800-53r5 | AC-6(7) Review of User Privileges | VERIFIED (mirror) |
| asd-ism-1591 | https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/ism/cyber-security-guidelines/guidelines-for-personnel-security | cyber.gov.au (primary) | ISM-1591 same-day access removal | VERIFIED |
| asd-ism-1647 | (same cyber.gov.au personnel-security page) | cyber.gov.au (primary) | ISM-1647 privileged 12-month revalidate-or-disable | VERIFIED |
| asd-ism-1648 | (same cyber.gov.au personnel-security page) | cyber.gov.au (primary) | ISM-1648 45-day inactive disable | VERIFIED |
| asd-ism-0407 | (same cyber.gov.au personnel-security page) | cyber.gov.au (primary) | ISM-0407 secure access record (last-reviewed) | VERIFIED (see note A) |
| apra-cps234-para21 | https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf | APRA (primary) | CPS 234 ¶21 Implementation of controls | VERIFIED |
| apra-cps234-para22 | https://handbook.apra.gov.au/standard/cps-234 | APRA Prudential Handbook (primary) | CPS 234 ¶22 Implementation of controls | VERIFIED |
| apra-cps234-para27 | https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf | APRA (primary) | CPS 234 ¶27 Testing control effectiveness | VERIFIED |
| apra-cps234-roles | https://handbook.apra.gov.au/standard/cps-234 | APRA Prudential Handbook (primary) | CPS 234 roles & responsibilities | VERIFIED |
| apra-cpg-234-least-privilege | https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_1.pdf | APRA CPG 234 (primary PDF) | Least-privilege principle | VERIFIED |
| apra-cpg-234-job-role | (same CPG 234 PDF, Attachment G) | APRA CPG 234 (primary PDF) | Job-role + least-privilege objective | VERIFIED |
| iso-27001-a5-18 | https://hightable.io/iso-27001-annex-a-5-18-access-rights/ | hightable.io secondary mirror | A.5.18 Access rights lifecycle | VERIFIED (secondary; ISO primary paywalled) |
| iso-27001-a518 (taxonomy) | https://www.isms.online/iso-27001/annex-a-2022/5-18-access-rights-2022/ | isms.online secondary | A.5.18 published intent (non-normative) | VERIFIED as intent (NOT verbatim ISO) |
| sox-icfr-13a15f | https://www.law.cornell.edu/cfr/text/17/240.13a-15 | Cornell LII (primary regulation) | 17 CFR 240.13a-15(f) ICFR definition | VERIFIED |
| sox-pl107-204-s404 | https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm | GovInfo (primary statute) | SOX §404(a)(1)/(2) mgmt internal-control report | VERIFIED |
| sox-pl107-204-authorizations | https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm | GovInfo (primary statute) | "authorizations of management" transaction clause | **SUSPECT — see note B** |
| sox-404 (taxonomy) | https://www.sarbanes-oxley-101.com/SOX-404.htm | sarbanes-oxley-101.com secondary | SOX §404(a) excerpt | VERIFIED (secondary; prefer 15 USC 7262 / GovInfo) |
| owasp-llm06-2025 | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | OWASP (primary) | LLM06:2025 Excessive Agency | VERIFIED |
| ms-midnight-blizzard-2024 | https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/ | Microsoft Security Blog (primary) | OAuth over-consent attack pattern | VERIFIED |
| sailpoint-isc-lifecycle | https://documentation.sailpoint.com/saas/help/provisioning/lifecycle.html | SailPoint docs (vendor primary) | ISC lifecycle states drive access | VERIFIED |
| sailpoint-isc-certifications | https://documentation.sailpoint.com/saas/help/certs/understanding_certifications.html | SailPoint docs | ISC certification campaign scope | VERIFIED |
| sailpoint-isc-cert-roles-request | (same SailPoint cert page) | SailPoint docs | Role request approve/revoke model | VERIFIED |
| sailpoint-isc-sod | https://documentation.sailpoint.com/saas/help/sod/index.html | SailPoint docs | ISC SoD service visibility | VERIFIED |
| sailpoint-isc-sod-policies | (same SailPoint SoD page) | SailPoint docs | SoD conflicting-access policy lists | VERIFIED |
| saviynt-eic-lifecycle | https://saviynt.com/products/identity-governance-and-administration | saviynt.com (marketing-grade) | EIC full lifecycle automation | VERIFIED (marketing copy) |
| saviynt-eic-certification | (same Saviynt IGA page) | saviynt.com (marketing-grade) | AI-assisted certification campaigns | VERIFIED (marketing copy) |
| saviynt-eic-request | (same Saviynt IGA page) | saviynt.com (marketing-grade) | Self-service access request mgmt | VERIFIED (marketing copy) |
| saviynt-eic-sod | https://saviynt.com/solutions/segregation-of-duties | saviynt.com (marketing-grade) | Cross-app SoD detect/prevent/remediate | VERIFIED (marketing copy) |
| saviynt-eic-sod-controls | (same Saviynt SoD page) | saviynt.com (marketing-grade) | Preventive + detective SoD controls | VERIFIED (marketing copy) |
| saviynt-eic-sod-request-point | (same Saviynt SoD page) | saviynt.com (marketing-grade) | Block conflicting access at request | VERIFIED (marketing copy) |
| entra-idg-lifecycle-workflows | https://learn.microsoft.com/.../what-are-lifecycle-workflows | Microsoft Learn (vendor primary) | LCW J/M/L automation | VERIFIED |
| entra-idg-access-reviews | https://learn.microsoft.com/.../access-reviews-overview | Microsoft Learn | Recurring access reviews | VERIFIED |
| entra-idg-sod-access-package | https://learn.microsoft.com/.../entitlement-management-access-package-incompatible | Microsoft Learn | SoD = access-package incompatibility (PARTIAL) | VERIFIED |
| entra-idg-entitlement-management | https://learn.microsoft.com/.../entitlement-management-overview | Microsoft Learn | Access-request workflow automation | VERIFIED |
| okta-oig-lifecycle | https://help.okta.com/.../identity-governance/iga.htm | Okta docs (vendor primary) | LCM + birthright provisioning | VERIFIED |
| okta-oig-certification | https://help.okta.com/.../identity-governance/iga-overview.htm | Okta docs | Context-enriched access certification | VERIFIED |
| okta-oig-request | (same Okta iga-overview page) | Okta docs | Self-service request + approval flows | VERIFIED |
| okta-oig-sod | https://help.okta.com/oie/.../identity-governance/sd/separation-of-duties.htm | Okta docs | SoD scoped to Governance-Engine apps (PARTIAL) | VERIFIED |
| okta-oig-sod-approach | (same Okta SoD page) | Okta docs | Preventative + remediative SoD (en-dash) | VERIFIED |

**Note A (asd-ism-0407):** the "when their access was last reviewed" phrase is supporting (non-control)
guidance preceding the numbered control text — disclosed in source. Attribution honest.

**⚠ Note B — SUSPECT (sox-pl107-204-authorizations):** the quoted "authorizations of management"
transaction clause IS genuine and verbatim in Public Law 107-204, but it lives in **§103(a)(2)(A)(iii)(II)(bb)**
(auditor-evaluation criteria), NOT in §404 as originally labelled. `sod.md` §3.2 was corrected to cite
§103. **Build agent: cite this clause as SOX §103, never §404.** Mapping rationale is unaffected; the
SoD/ICFR anchor still holds.

> **Mirror / secondary caveats the build must preserve when citing:** (1) all `nist-sp-800-53-*` quotes
> are from the csf.tools mirror — substitute csrc.nist.gov OSCAL for audit-facing use; (2) `iso-27001-*`
> quotes are from hightable.io / isms.online secondary mirrors (ISO standard paywalled) — the isms.online
> A.5.18 text is *published intent, not normative ISO wording*; (3) `sox-404` (taxonomy) is a secondary
> host — prefer 15 USC 7262 / GovInfo; (4) Saviynt anchors are marketing-grade product copy, not admin
> docs — capability-presence claim only.

---

## 3. Regulatory-trace plan

framework_slug | control_code | UC ids it back-maps to | verbatim quote available (Y/N).

| framework_slug | control_code | back-maps to UC ids | verbatim quote (Y/N) |
|----------------|--------------|----------------------|----------------------|
| nist-800-53r5 | AC-2 | UC-I-001, 002, 003, 004, 005 | Y |
| nist-800-53r5 | AC-2(3) | UC-I-003, 004, 005 | Y |
| nist-800-53r5 | AC-2(j) | UC-I-005 | Y |
| nist-800-53r5 | AC-3 | UC-I-012 | Y |
| nist-800-53r5 | AC-5 | UC-I-008, 009, 010 | Y |
| nist-800-53r5 | AC-6 | UC-I-011, 012, 013; IGID-002/005/012 | Y |
| nist-800-53r5 | AC-6(1) | UC-I-012 | Y |
| nist-800-53r5 | AC-6(5) | UC-I-013 | Y |
| nist-800-53r5 | AC-6(7) | UC-I-006 | Y |
| asd-ism | ISM-1591 | UC-I-003 | Y |
| asd-ism | ISM-1647 | UC-I-004, 006 | Y |
| asd-ism | ISM-1648 | UC-I-004 | Y |
| asd-ism | ISM-0407 | UC-I-005, 006 | Y |
| apra-cps234 | ¶21 (Implementation of controls) | UC-I-001..005, all areas (commensurate) | Y |
| apra-cps234 | ¶22 (Implementation of controls) | UC-I-008, 009, 010 | Y |
| apra-cps234 | ¶27 (Testing control effectiveness) | UC-I-005, 007, 010 | Y |
| apra-cps234 | roles & responsibilities | UC-I-009 | Y |
| apra-cpg234 | least-privilege principle | UC-I-011, 013 | Y |
| iso-27001-2022 | A.5.18 (Access rights) | UC-I-001..006, 012, 013 | Y (secondary mirror only) |
| iso-27001-2022 | A.5.16 (Identity management) | UC-I-001, 003 | **N — UNVERIFIED, cite by ref only** |
| iso-27001-2022 | A.5.15 (Access control) | UC-I-011 | **N — UNVERIFIED (secondary)** |
| iso-27001-2022 | A.5.3 (Segregation of duties) | UC-I-008, 009, 010 | **N — secondary only, re-verify vs licensed ISO** |
| sox-icfr | 17 CFR 240.13a-15(f) | UC-I-005, 006, 008 | Y |
| sox | PL 107-204 §404(a) | UC-I-008, 009, 010 | Y |
| sox | PL 107-204 §103 ("authorizations of mgmt") | UC-I-008, 009, 010 | Y (**⚠ §103 not §404 — see Note B**) |
| mitre-attack | T1078 (Valid Accounts) | UC-I-003, 004, 005, 006, 008, 011, 013 | Y |
| mitre-attack | T1098 (Account Manipulation) | UC-I-002, 004, 008 | Y |
| owasp-llm | LLM06:2025 (Excessive Agency) | IGID-012 | Y |
| ms-incident | Midnight Blizzard OAuth pattern | IGID-013 | Y |

---

## 4. Identity & entitlement taxonomy (IGID class list)

13 classes, stable ids `IGID-001..013`. COMMON = every IGA programme; EMERGING = 2026 frontier.

| IGID | short_name | bucket | lifecycle | gov_maturity | primary control hooks |
|------|-----------|--------|-----------|--------------|------------------------|
| IGID-001 | Workforce joiner | COMMON | JOINER | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-002 | Workforce mover | COMMON | MOVER | LOW | AC-6, AC-2, ISO 5.18 |
| IGID-003 | Workforce leaver | COMMON | LEAVER | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-004 | Contractor / third-party | COMMON | JOINER→LEAVER | LOW | CPS 234, AC-2, ISO 5.18 |
| IGID-005 | Privileged business user | COMMON | MOVER | MED | AC-6, ISO 5.18, CPS 234 |
| IGID-006 | Application owner | COMMON | STATIC | MED | AC-2, ISO 5.18, CPS 234 |
| IGID-007 | Role owner / entitlement owner | COMMON | STATIC | LOW–MED | AC-2, AC-5 |
| IGID-008 | SoD-sensitive finance role | COMMON | MOVER | MED–HIGH (SOX) | AC-5, SOX 404, CPS 234 |
| IGID-009 | Governed service account | COMMON | STATIC | LOW | AC-2, AC-6, CPS 234 |
| IGID-010 | Birthright / RBAC holder | COMMON | JOINER | MED | AC-2, AC-6, ISO 5.18 |
| IGID-011 | Dormant / orphan account | COMMON | LEAVER | LOW | AC-2, ISO 5.18 |
| IGID-012 | Agentic-AI / autonomous agent | EMERGING | STATIC (dynamic) | LOW | OWASP LLM06, AC-6, CPS 234 |
| IGID-013 | OAuth app / consent-grant | EMERGING | STATIC | LOW | MS Midnight Blizzard, AC-6, AC-2, CPS 234 |

> Build note: IGID-011 (dormant/orphan) is both a class AND a KPI — a low population is evidence that
> JML (001/002/003), service-account (009) and consent-grant (013) governance actually work. The two
> EMERGING classes (012, 013) break point-in-time recertification; model their "good" end-state as
> *continuous* attestation, not annual campaign.

---

## 5. Vendor-fit grid (vendor × area → NATIVE / PARTIAL / ADD-ON)

Capability-presence read from each vendor's OWN docs. NATIVE ≠ best-in-class. **SoD is the
discriminating column.** No cell is ADD-ON, but Okta SoD trends toward ADD-ON at ERP-grade scope.

| Vendor | JML | Certification | SoD | Role/Request |
|--------|-----|---------------|-----|--------------|
| SailPoint Identity Security Cloud | NATIVE | NATIVE | NATIVE | NATIVE |
| Saviynt Enterprise Identity Cloud | NATIVE | NATIVE | NATIVE | NATIVE |
| Microsoft Entra ID Governance | NATIVE | NATIVE | **PARTIAL** | NATIVE |
| Okta Identity Governance | NATIVE | NATIVE | **PARTIAL** | NATIVE |

PARTIAL rationale (from vendor docs): Entra SoD = request-time incompatibility scoped to access
packages/groups only (not cross-app toxic-pair engine); Okta SoD = entitlement combinations only on
apps with the Governance Engine enabled. Both fail ERP-grade cross-application SoD without an AAG/GRC
component. Saviynt's NATIVE verdicts rest on marketing-grade copy (docs portal not server-renderable) —
capability presence is well-established but the anchor is product copy, flagged honestly.

---

## 6. DATA QUALITY

### Citation tally (across all six areas, deduplicated by verdict disposition)

- **Total citations verified across areas:** 60 (sum of per-file returned arrays: jml 9, certification
  10, sod 6, role-request 9, identity-taxonomy 8, vendor-fit 20 — minus 2 cross-area duplicate keys
  re-counted = effective unique-key set ~52; per-file verification counted 60 instances).
- **VERIFIED:** 59 of 60 verification instances.
- **SUSPECT:** 1 — `sox-pl107-204-authorizations` (quote genuine & verbatim, but section attribution was
  wrong: §404 → corrected to §103). Retained, not removed. See Note B in §2.
- **FABRICATED:** 0. No citation was fabricated; none excluded.

Every per-area verification pass returned **overall PASS**.

### Gaps the build MUST NOT paper over

1. **SOX §103 vs §404 mislabel (the one SUSPECT).** Cite the "authorizations of management" transaction
   clause as **SOX §103(a)(2)(A)(iii)(II)(bb)**, never §404. §404(a)(1)/(2) is a *separate, also-verified*
   quote. Do not collapse them.
2. **NIST AC-family quotes are from the csf.tools mirror**, not csrc.nist.gov. Substance identical, but
   substitute the NIST OSCAL/PDF primary for any audit-facing or attestation deliverable.
3. **ISO/IEC 27001:2022 wording is secondary/paywalled.** A.5.18 verbatim is from hightable.io/isms.online
   mirrors; the isms.online A.5.18 line is *published intent, not normative ISO text*. A.5.16, A.5.15,
   A.5.3 are **UNVERIFIED against primary** — cite by control-ID + reference only, or re-verify against a
   licensed ISO copy before external attestation. Do NOT present these as verbatim ISO quotes.
4. **SOX taxonomy citation host.** `sox-404` (identity-taxonomy) uses sarbanes-oxley-101.com (secondary);
   prefer 15 USC 7262 / GovInfo primary for a regulated-FI deliverable.
5. **CPG 234 paragraph text and ATT&CK sub-techniques (T1078.x / T1098.x) are NOT verbatim-verified** —
   cite parent techniques and CPG 234 by reference only.
6. **Saviynt vendor verdicts rest on marketing copy**, not admin docs (docs portal was an un-renderable
   SPA). Treat the four NATIVE verdicts as capability-presence per the vendor, not an independent
   efficacy benchmark.
7. **Use-case numbering is re-sequenced.** §1 uses a clean UC-I-001..013 scheme that does NOT match the
   raw spike `use-cases.csv` ids one-to-one. Build agent must pick one scheme and use the crosswalk
   column; do not silently mix legacy and re-sequenced ids.

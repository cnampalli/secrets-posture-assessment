# WS-1 control-ID verification notes — IGA regulatory-trace debt

Verified: 2026-06-10. Anti-fabrication protocol: every code below checked against an
authoritative source via live fetch; verbatim quotes confirmed where stated. Anything not
confirmable is listed under UNVERIFIED at the bottom. **Two fabrication-class errors found
in the CSV (ISM-1591 and ISM-1648 rows point at the wrong controls) — corrections below.**

Verification methods of note:
- ASD ISM: verified against the official **cyber.gov.au ISM PDF (December 2024 release)**
  downloaded and text-extracted locally (the cyber.gov.au HTML guideline page timed out
  repeatedly), cross-checked against ismcontrol.xyz per-control pages (`/NNNN/`, Current,
  last updated 2025-05-21). Both sources agree on every control checked.
- NIST SP 800-53 Rev 5: verified against the **official NIST OSCAL catalog**
  (github.com/usnistgov/oscal-content, `NIST_SP-800-53_rev5_catalog.json`) downloaded and
  parsed locally, cross-checked against csf.tools mirror pages.
- APRA CPS 234 / CPG 234: verified against the **official apra.gov.au PDFs** (July 2019 /
  June 2019), text-extracted locally; paragraph and attachment locations read directly.

---

## Task 1 — ASD ISM

| code | verified? | authoritative URL | official substance (Dec 2024 ISM) | CSV claim matches? | notes |
|---|---|---|---|---|---|
| ISM-1591 | YES (exists) — **but CSV claim NO** | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/1591/ | "Access to systems, applications and data repositories is removed or suspended **as soon as practicable when personnel are detected undertaking malicious activities**." (Rev 0, Aug-20) | **NO — wrong control.** CSV claims same-day removal on loss of business requirement; that is **ISM-0430** | Repoint row to ISM-0430 (see corrections) |
| ISM-0430 | YES | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/0430/ | "Access to systems, applications and data repositories is removed or suspended **on the same day personnel no longer have a legitimate requirement for access**." (Rev 7, Sep-19) | YES — this is the control the CSV row describes | Verified verbatim in both sources; not yet in registry |
| ISM-1647 | YES | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/1647/ | "Privileged access to systems, applications and data repositories is disabled after 12 months unless revalidated." (Rev 1, Dec-23; E8 ML2/ML3) | YES (substance) — **CSV quote uses outdated wording** "systems and their resources" | Update evidence_quote to current wording |
| ISM-1648 | YES (exists) — **but CSV claim NO** | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/1648/ | "**Privileged** access to systems and applications is disabled after 45 days of inactivity." (Rev 1, Dec-23; E8 ML2/ML3) | **NO — wrong control.** CSV claims *unprivileged* 45-day disablement; that is **ISM-1404** | Repoint row to ISM-1404 (already in registry) |
| ISM-1404 | YES | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/1404/ | "**Unprivileged** access to systems and applications is disabled after 45 days of inactivity." (Rev 4, Dec-23) | YES — this is the control the CSV ISM-1648 row describes | Already in registry controls list |
| ISM-0407 | YES | cyber.gov.au ISM Dec 2024 PDF; https://ismcontrol.xyz/0407/ | "A secure record is maintained for the life of each system covering the following for each user: their user identification; their signed agreement to abide by usage policies for the system and its resources; who provided authorisation for their access; when their access was granted; the level of access that they were granted; **when their access, and their level of access, was last reviewed**; when their level of access was changed, and to what extent (if applicable); when their access was withdrawn (if applicable)." (Rev 5, Sep-23) | YES (substance: includes "when access last reviewed") — CSV quote uses older wording ("life of systems and their resources", "system usage policies") and is truncated | Update evidence_quote to current Rev 5 wording |

## Task 2 — MITRE ATT&CK

| code | verified? | authoritative URL | official title/substance | CSV claim matches? | notes |
|---|---|---|---|---|---|
| T1078 | YES | https://attack.mitre.org/techniques/T1078/ | "Valid Accounts" — base technique, 4 sub-techniques (.001–.004) | YES — CSV quote verbatim: "Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion." | Add to registry (registry has only T1078.004) |
| T1098 | YES | https://attack.mitre.org/techniques/T1098/ | "Account Manipulation" — base technique, 7 sub-techniques (.001–.007) | YES — CSV quote verbatim: "Adversaries may manipulate accounts to maintain and/or elevate access to victim systems." | Add to registry (registry has only T1098.001) |

## Task 3 — NIST SP 800-53 Rev 5

Verified against the official NIST OSCAL Rev 5 catalog (usnistgov/oscal-content) and
csf.tools. Authoritative landing: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

| code | verified? | source | official title/substance | CSV claim matches? | notes |
|---|---|---|---|---|---|
| AC-2 | YES | OSCAL `ac-2`; https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-2/ | "Account Management" | YES — CSV quote is item f, verbatim | |
| AC-2(3) | YES | OSCAL `ac-2.3` | Enhancement "Disable Accounts" | YES — CSV quote verbatim | |
| AC-2(j) | **PARTIAL — item exists, citation style not defensible** | OSCAL `ac-2` statement part labeled `j.` | Item j verbatim: "Review accounts for compliance with account management requirements [Assignment: organization-defined frequency];" | Substance YES — quote verbatim | **Recommend recode to `AC-2j`.** In 800-53 notation, parenthesised suffixes are *numeric enhancements only* (AC-2(1)…AC-2(13)); "AC-2(j)" reads as a non-existent enhancement. NIST statement-item labels are letters (`a.`–`l.`), conventionally cited as AC-2j |
| AC-3 | YES | OSCAL `ac-3` | "Access Enforcement" | YES — CSV quote verbatim | |
| AC-5 | YES | OSCAL `ac-5` | "Separation of Duties" | YES — CSV quote verbatim (items a+b) | |
| AC-6 | YES | OSCAL `ac-6` | "Least Privilege" | YES — CSV quote verbatim | |
| AC-6(1) | YES | OSCAL `ac-6.1` | Enhancement "Authorize Access to Security Functions" | YES | |
| AC-6(5) | YES | OSCAL `ac-6.5` | Enhancement official title is **"Privileged Accounts"** (CSV short title "Privileged Accounts restriction" is a paraphrase — acceptable but flag) | YES — CSV quote verbatim | Consider tightening short title |
| AC-6(7) | YES | OSCAL `ac-6.7` | Enhancement "Review of User Privileges" | YES — CSV quote verbatim | |

Proposed `pattern` for the final code set {AC-2, AC-2(3), AC-2j, AC-3, AC-5, AC-6, AC-6(1), AC-6(5), AC-6(7)}:

```
^AC-\d{1,2}(\(\d{1,2}\)|[a-z])?$
```

## Task 4 — ISO/IEC 27001:2022 Annex A

Titles verified via ISMS.online Annex A reference (https://www.isms.online/iso-27001/annex-a/);
ISO text is licensed — titles only, no quotes (CSV correctly withholds quotes). Official
landing: https://www.iso.org/standard/27001

| code | verified? | official title | CSV claim matches? | notes |
|---|---|---|---|---|
| A.5.3 | YES (title, secondary source) | Segregation of duties | YES | |
| A.5.15 | YES (title, secondary source) | Access control | YES | |
| A.5.16 | YES (title, secondary source) | Identity management | YES | |
| A.5.18 | YES (title, secondary source) | Access rights | YES | |

## Task 5 — SOX

| code | verified? | authoritative URL | substance | CSV claim matches? | notes |
|---|---|---|---|---|---|
| PL 107-204 §404(a) | YES | https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm (ToC) + https://www.law.cornell.edu/uscode/text/15/7262 (codified, subsection (a) items (1)/(2) verbatim) | "Management assessment of internal controls" — internal control report must (1) state management responsibility for adequate ICFR structure/procedures and (2) contain an assessment of ICFR effectiveness | YES — CSV quote matches (1)/(2) | govinfo HTML fetch truncated before Title IV; full verbatim confirmed via 15 U.S.C. §7262(a) |
| PL 107-204 §103 | YES | https://www.govinfo.gov/content/pkg/PLAW-107publ204/html/PLAW-107publ204.htm | §103(a)(2)(A)(iii)(II)(bb) verbatim: "provide reasonable assurance that transactions are recorded as necessary to permit preparation of financial statements in accordance with generally accepted accounting principles, and that receipts and expenditures of the issuer are being made only in accordance with authorizations of management and directors" | YES — CSV quote verbatim; CSV maturity_level field correctly records the subsection path | |
| 17 CFR 240.13a-15(f) | YES | https://www.law.cornell.edu/cfr/text/17/240.13a-15 (eCFR geo-blocked at verification time — 302 to unblock.federalregister.gov) | §240.13a-15 paragraph (f) defines ICFR; sub-item (2) contains the "authorizations of management and directors of the issuer" clause | YES — CSV quote is (f)(2) substance | CSV evidence_url already points at Cornell LII; fine |

## Task 6 — OWASP LLM Top 10 2025

| code | verified? | authoritative URL | official title | CSV claim matches? | notes |
|---|---|---|---|---|---|
| LLM06:2025 | YES | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | "LLM06:2025 Excessive Agency" (OWASP Top 10 for LLM Applications 2025) | YES — CSV quote confirmed verbatim on page (full sentence ends "…regardless of what is causing the LLM to malfunction.") | |

## Task 7 — ms-incident

| code | verified? | authoritative URLs | substance | CSV claim matches? | notes |
|---|---|---|---|---|---|
| Midnight-Blizzard-OAuth | YES (incident-case ref) | MSRC canonical: https://www.microsoft.com/en-us/msrc/blog/2024/01/microsoft-actions-following-attack-by-nation-state-actor-midnight-blizzard/ (2024-01-19; the old msrc.microsoft.com URL now 301-redirects). CSV's evidence URL: https://www.microsoft.com/en-us/security/blog/2024/01/25/midnight-blizzard-guidance-for-responders-on-nation-state-attack/ (2024-01-25, Microsoft Threat Intelligence) | Midnight Blizzard (NOBELIUM) nation-state attack detected 2024-01-12: password spray on legacy test tenant → malicious OAuth applications → Exchange Online access | YES — CSV evidence_quote verified **verbatim** on the Jan 25 guidance post | Treat like BREACH-* case refs. Keep the Jan-25 guidance post as evidence_url (it carries the quote); record the MSRC post as the canonical incident disclosure |

## Task 8 — APRA CPS 234 (CPS234-roles)

| code | verified? | authoritative URL | substance | notes |
|---|---|---|---|---|
| CPS234-roles → **CPS234-§14** | YES | https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf (PDF text-extracted; "Roles and responsibilities" section) | §14 verbatim: "An APRA-regulated entity must clearly define the information security-related roles and responsibilities of the Board, senior management, governing bodies and individuals with responsibility for decision-making, approval, oversight, operations and other information security functions." (§13 = Board ultimate responsibility; §15 = capability) | CSV quote is **verbatim §14**. Repoint code to `CPS234-§14` — already in registry, no registry change needed. Note: a handbook.apra.gov.au fetch mislabeled this as §13/§14 shifted; the official PDF is definitive: roles = §14 |

## Task 9 — APRA CPG 234 (CPG234-LP)

| code | verified? | authoritative URL | substance | notes |
|---|---|---|---|---|
| CPG234-LP → **CPG234-Att-A** | YES | https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_1.pdf (PDF text-extracted) | The quoted text is **Attachment A: Security principles, item (b)**, verbatim: "access to, and configuration of, information assets is restricted to the minimum required to achieve business objectives. This is typically referred to as the principle of 'least privilege' and aims to reduce the number of attack vectors that can be used to compromise information security;" | CSV quote is a verbatim prefix of Att-A(b). **Recommend `CPG234-Att-A`** — fits the existing registry pattern `^CPG234-Att-[A-Z]$` exactly; no pattern extension needed. Record item (b) in the short title (e.g., "Least privilege — Attachment A principle (b)"). Add `CPG234-Att-A` to the registry controls list |

---

## READY-TO-PASTE YAML

### (a) Registry additions — existing frameworks

`asd-ism` controls list — ADD (after repointing rows; ISM-1404 already present; ISM-1591/ISM-1648 deliberately NOT added — wrong controls for these rows):

```yaml
# add to asd-ism.controls (verified 2026-06-10 vs cyber.gov.au ISM Dec 2024 PDF + ismcontrol.xyz):
#   ISM-0407, ISM-0430, ISM-1647
```

`mitre-attack` controls list — ADD base techniques (verified 2026-06-10):

```yaml
# add to mitre-attack.controls: T1078, T1098
```

### (b) New registry entries — matrix/config/control-id-registry.yaml

```yaml
nist-800-53r5:
  source: "csrc.nist.gov SP 800-53 Rev 5 (official NIST OSCAL catalog, usnistgov/oscal-content) + csf.tools mirror"
  verified: 2026-06-10
  # Parenthesised suffix = numeric enhancement; trailing letter = base-control statement item
  # (e.g. AC-2j). "AC-2(j)" is deliberately NOT registered — letter-in-parens fakes an enhancement.
  pattern: '^AC-\d{1,2}(\(\d{1,2}\)|[a-z])?$'
  controls: [AC-2, AC-2(3), AC-2j, AC-3, AC-5, AC-6, AC-6(1), AC-6(5), AC-6(7)]

iso-27001-2022:
  source: "iso.org/standard/27001 (licensed text — quotes withheld); control titles cross-checked via isms.online Annex A reference"
  verified: 2026-06-10
  pattern: '^A\.\d{1,2}\.\d{1,2}$'
  controls: [A.5.3, A.5.15, A.5.16, A.5.18]

sox:
  source: "govinfo.gov PLAW-107publ204 (Sarbanes-Oxley Act 2002) + law.cornell.edu 15 U.S.C. §7262"
  verified: 2026-06-10
  pattern: '^PL 107-204 §\d{3}(\([a-z]\))?$'
  controls: ["PL 107-204 §103", "PL 107-204 §404(a)"]

sox-icfr:
  source: "law.cornell.edu/cfr/text/17/240.13a-15 (eCFR geo-blocked at verification; re-verify against ecfr.gov when reachable)"
  verified: 2026-06-10
  pattern: '^17 CFR 240\.13a-15\([a-z]\)$'
  controls: ["17 CFR 240.13a-15(f)"]

owasp-llm:
  source: "genai.owasp.org OWASP Top 10 for LLM Applications 2025"
  verified: 2026-06-10
  pattern: '^LLM\d{2}:2025$'
  controls: ["LLM06:2025"]

ms-incident:
  source: "microsoft.com Security Blog (2024-01-25 Midnight Blizzard guidance) + MSRC blog (2024-01-19 disclosure) — incident-case refs, like BREACH-* under mitre-attack"
  verified: 2026-06-10
  pattern: '^[A-Z][A-Za-z0-9-]+$'
  controls: [Midnight-Blizzard-OAuth]
```

### (c) New provenance entries — matrix/config/data-provenance.yaml

```yaml
nist-800-53r5:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: annual
  owner: TBD
  source: "csrc.nist.gov SP 800-53 Rev 5 (official OSCAL catalog) + csf.tools mirror"

iso-27001-2022:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: annual
  owner: TBD
  source: "ISO/IEC 27001:2022 Annex A (licensed standard)"
  note: "Control titles verified via secondary mirror (isms.online); full text licensed — quotes withheld in trace rows by design."

sox:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: as-needed
  owner: TBD
  source: "govinfo.gov Public Law 107-204 + law.cornell.edu 15 U.S.C. §7262"

sox-icfr:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: as-needed
  owner: TBD
  source: "17 CFR 240.13a-15 via law.cornell.edu (eCFR geo-blocked at verification)"

owasp-llm:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: annual
  owner: TBD
  source: "genai.owasp.org OWASP Top 10 for LLM Applications 2025"

ms-incident:
  as_of: 2026-06-10
  source_tier: PRIMARY
  refresh: as-needed
  owner: TBD
  source: "Microsoft first-party incident disclosures (Security Blog + MSRC blog, Jan 2024)"
  note: "Threat-context incident-case reference (cf. BREACH-* refs under mitre-attack)."
```

---

## Recommended CSV corrections — matrix/domains/iga/regulatory-trace.csv

1. **Row `ISM-1591` (line 11) — WRONG CONTROL, repoint to `ISM-0430`.**
   - `control_code`: `ISM-1591` → `ISM-0430`
   - `evidence_quote` → current wording: `Access to systems, applications and data repositories is removed or suspended on the same day personnel no longer have a legitimate requirement for access.`
   - `citation_keys`: `asd-ism-1591` → `asd-ism-0430`
   - (ISM-1591 is "removed or suspended as soon as practicable when personnel are detected undertaking malicious activities" — a different control.)

2. **Row `ISM-1648` (line 13) — WRONG CONTROL, repoint to `ISM-1404`.**
   - `control_code`: `ISM-1648` → `ISM-1404` (already in registry)
   - `evidence_quote` → current wording: `Unprivileged access to systems and applications is disabled after 45 days of inactivity.`
   - `citation_keys`: `asd-ism-1648` → `asd-ism-1404`
   - (ISM-1648 is the *privileged* 45-day inactivity control. If a privileged-inactivity row is wanted later, ISM-1648 is verified and available.)

3. **Row `ISM-1647` (line 12) — keep code; refresh quote** to current wording:
   `Privileged access to systems, applications and data repositories is disabled after 12 months unless revalidated.`

4. **Row `ISM-0407` (line 14) — keep code; refresh quote** to current Rev 5 wording (at minimum replace "for the life of systems and their resources" with "for the life of each system" and "system usage policies" with "usage policies for the system and its resources"; ideally include "when their access, and their level of access, was last reviewed" since that is the clause the row leans on).

5. **Row `CPS234-roles` (line 18) — repoint to `CPS234-§14`.**
   - `control_code`: `CPS234-roles` → `CPS234-§14` (already in registry; quote verified verbatim against the official CPS 234 PDF)
   - Optionally set `maturity_level`/paragraph field to `Paragraph-14` for consistency with sibling rows, and prefer the official PDF URL used by the §21/§27 rows.

6. **Row `CPG234-LP` (line 19) — repoint to `CPG234-Att-A`.**
   - `control_code`: `CPG234-LP` → `CPG234-Att-A` (fits existing pattern `^CPG234-Att-[A-Z]$`; add `CPG234-Att-A` to the registry controls list)
   - `control_short_title` → e.g. `Least privilege — Attachment A security principle (b)`
   - Quote verified verbatim (it is a truncated prefix of Att-A item (b)); consider extending it to the full clause ending "…the principle of 'least privilege' and aims to reduce the number of attack vectors that can be used to compromise information security".

7. **Row `AC-2(j)` (line 4) — recode to `AC-2j`.**
   - `control_code`: `AC-2(j)` → `AC-2j`; `citation_keys` `nist-sp-800-53-ac2j` already matches. Quote verified verbatim against the official OSCAL catalog. Rationale: parenthesised suffixes in 800-53 denote numeric enhancements only; "AC-2(j)" misreads as a non-existent enhancement.

8. **Row `AC-6(5)` (line 9) — cosmetic:** official enhancement title is "Privileged Accounts"; CSV short title "Privileged Accounts restriction" is a paraphrase (acceptable, but tighten if standardising).

9. **Framework-slug mismatch (validator wiring, not a control-ID issue):** the CSV uses slugs `apra-cps234` / `apra-cpg234`, but the registry keys are `apra-cps-234` / `apra-cpg-234`. Either normalise the CSV slugs to the registry keys or alias in the validator — otherwise the membership gate cannot bind these rows to their registry entries.

---

## UNVERIFIED / verification caveats

Nothing is outright UNVERIFIED — every code resolved to a primary or acceptable secondary source. Caveats:

- **ISO/IEC 27001:2022 (A.5.3, A.5.15, A.5.16, A.5.18):** titles verified only via secondary (isms.online); full standard is licensed. Tried: iso.org landing (titles not enumerated publicly). Status: PARTIAL by design — matches the CSV's own "quote withheld / re-verify vs licensed ISO" posture. Re-verify against a licensed copy before client publication.
- **eCFR (17 CFR 240.13a-15):** ecfr.gov 302-redirected to unblock.federalregister.gov (geo/bot block). Verified via law.cornell.edu instead. Re-check ecfr.gov when reachable.
- **cyber.gov.au HTML guideline page** (personnel security) timed out twice; verification instead used the official cyber.gov.au ISM **December 2024 PDF** (downloaded from cyber.gov.au) — still the primary source. A newer ISM release may exist (ismcontrol.xyz shows "last updated May 21, 2025" with identical control texts for all six controls checked); confirm against the current cyber.gov.au release at next quarterly refresh.
- **SOX §404(a):** govinfo HTML fetch truncated before Title IV; §404(a) items (1)/(2) verified verbatim via the codified text at 15 U.S.C. §7262(a) (law.cornell.edu). §103 clause verified verbatim directly on govinfo.

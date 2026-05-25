# Regulatory Framework Audit — 2026-05-24

Full verification of all 7 framework lenses in `matrix/regulatory-trace.csv` against authoritative sources, triggered by stakeholder flag that removed ISM controls were present. **Headline: ISM and CPG 234 had fabricated/mislabeled IDs; NIST 800-207 is mis-attributed; APRA CPS 234/230, MITRE ATT&CK, and Essential 8 are accurate.**

| Framework | IDs | Source checked | Verdict |
|---|---|---|---|
| ASD ISM | 41 | ismcontrol.xyz (index.xml, 1862 controls) | ❌ **~80% wrong** — 27 wrong-topic, 5 removed, 1 nonexistent. Rebuilt → see `ISM-CORRECTED-MAPPING-2026-05-24.md` |
| MITRE ATT&CK | 16 T-codes (+15 BREACH-*) | attack.mitre.org | ✅ All current/valid. 2 title fixes needed. |
| APRA CPS 234 | 25 | legislation.gov.au F2018L01745 / APRA PDF | ✅ All 25 paragraph refs accurate |
| APRA CPS 230 | 6 | APRA PDF (2023) | ✅ All 6 paragraph refs accurate |
| APRA CPG 234 | 3 | APRA PDF (June 2019) | ❌ 2 of 3 attachment letters mislabeled |
| NIST SP 800-207 | 13 | NIST 800-207 / CISA ZTMM | ⚠️ Taxonomy is CISA ZTMM, mis-attributed to NIST 800-207 |
| Essential 8 | 26 | ASD Essential Eight Maturity Model | ✅ 8 strategies + ML1–3 correct; codes are honest synthesis |

---

## 1. ASD ISM — REBUILT (see ISM-CORRECTED-MAPPING-2026-05-24.md)
~80% of original IDs inaccurate (wrong topic, removed, or nonexistent). Full corrected mapping of ~38 verified-current controls produced separately. This is the only framework requiring a wholesale rebuild.

## 2. MITRE ATT&CK — 2 fixes
All 16 technique IDs return HTTP 200 and none are deprecated/revoked. Title corrections:
- **T1552.003** — MITRE renamed "Bash History" → **"Shell History"**. Update title.
- **T1606.002** — we label it "Web Session Cookie Forge" but T1606.002 is **"SAML Tokens"** (Forge Web Credentials: SAML Tokens). Web-cookie forge is T1606.001. Given our SolarWinds/Storm-0558 breach anchors involve SAML/signing keys, **retitle to "SAML Tokens"** (keep ID T1606.002). If web-cookie forge was intended, change ID to T1606.001 instead.
- Minor: T1556.006 site name is "Multi-Factor Authentication" (Modify Authentication Process); our "MFA-related bypass" is an acceptable paraphrase — optional tighten.
- The 15 `BREACH-*` entries are editorial incident anchors (Okta, LastPass, CircleCI, SolarWinds, Storm-0558, etc.) — all real incidents, not MITRE IDs. No change.

## 3. APRA CPS 234 — ACCURATE (no change)
Verified every cited paragraph exists with matching content: §13 Board, §14 roles, §15 capability, §16 third-party capability, §17 maintenance through change, §18–19 policy framework, §20 classification, §21 + §21(a)(b)(c)(d) controls (timely/commensurate, criticality, lifecycle stage, consequences), §22 third-party design, §23 detect/respond, §24 IR plans, §26 annual review/test, §27 + §27(d) systematic testing (d = exposure to environments), §28 third-party testing sufficiency, §30 independent testers, §32 internal audit, §34 third-party assurance audit, §35 72-hour notification, §36 10-business-day weakness notification.

## 4. APRA CPS 230 — ACCURATE (no change)
- §15 service-provider dependency gate ✓
- §25 sound information & IT capability ✓
- §42 24-hour BCP-breach notification ✓
- §47 comprehensive service-provider management policy ✓
- §54 formal legally-binding agreement for material arrangements ✓
- §59(b) material-offshoring pre-notification ✓

## 5. APRA CPG 234 — 2 fixes
Actual attachment structure (June 2019 guide): A Security principles · B Training & awareness · C Identity and access · D Software security · E Cryptographic techniques · F Customer security · G Testing techniques · H Reporting.
- **CPG234-Att-C** "Identity and access management" ✓ correct
- **CPG234-Att-D** — we say "Cryptographic key management"; Att-D is **"Software security"**. Fix.
- **CPG234-Att-E** — we say "Third-party assurance"; Att-E is **"Cryptographic techniques"**. Fix.
- There is **no third-party-assurance attachment** in CPG 234 — that guidance lives in CPS 234 §28/§34. Drop the third-party-assurance row or re-anchor it to CPS 234.
- Recommended secrets-relevant set: Att-C (Identity & access), Att-E (Cryptographic techniques), Att-D (Software security).

## 6. NIST SP 800-207 — attribution fix
The 13 `ZT-Pillar-*` codes use the **pillar taxonomy** (Identity, Devices, Networks, Applications & Workloads, Data + cross-cutting Visibility & Analytics, Automation & Orchestration, Governance). That taxonomy is **CISA's Zero Trust Maturity Model v2.0**, *not* NIST SP 800-207. NIST 800-207 defines 7 tenets + logical components (Policy Engine / Policy Administrator / Policy Enforcement Point) and does not use "pillars."
- **Recommendation:** relabel the lens to **CISA Zero Trust Maturity Model v2.0** (or "Zero Trust — NIST SP 800-207 + CISA ZTMM"). Content is sound; only the framework name/attribution is wrong.

## 7. Essential 8 — sound (presentation note)
All 8 mitigation strategies correctly identified (E8-AC application control, E8-PA patch apps, E8-MAC macros, E8-UAH user app hardening, E8-RAP restrict admin, E8-POS patch OS, E8-MFA, E8-RB backups) with real ML1–3 maturity levels. The `-SVC / -BREAKGLASS / -WORKLOAD / -KEYS / -NHI-GAP` suffixes are clearly editorial NHI-context annotations. Note: the Essential Eight assigns **no official control-ID numbers** — ensure the PRD presents `E8-*` codes as a synthesized lens, not official identifiers.

---

## Required changes summary
| Framework | Action | Effort |
|---|---|---|
| ISM | Replace 33 rows with corrected mapping | High |
| MITRE | 2 title edits (T1552.003, T1606.002) | Trivial |
| CPS 234 / CPS 230 | None | — |
| CPG 234 | 2 title edits + drop/re-anchor 1 row | Low |
| NIST 800-207 | Relabel framework → CISA ZTMM | Low |
| Essential 8 | Presentation note only | — |

Downstream files to update after data is fixed: `regulatory-trace.csv`, `matrix.md`, `PRD/appendices/A-compliance-traceability.md`, `build_matrix_viewer.py` + regenerated `matrix-viewer.html`, `dist/` package, and all "145 controls / 7 frameworks" counts.

# Regulator Audit — APRA controls, NHI taxonomy & use cases

**Date:** 2026-06-03
**Auditor role:** APRA prudential reviewer (information security) + NHI taxonomy scrutineer
**Mandate:** Identify APRA controls that are *inaccurate* or *not relevant*; tidy the
Non-Human Identity (NHI) taxonomy against **official** regulator/standards definitions;
validate the 47 use cases (Part 4).
**Confidence bar:** ≥ 95%.
**Method:** Every cited reference was checked against the **live primary source** (APRA PDFs
extracted via FlateDecode/zlib, paragraph-by-paragraph) rather than memory or secondary
mappings. NHI definitions taken from NIST/CNSSI and OWASP primary pages.

Companion to the prior framework audit
[`FRAMEWORK-AUDIT-2026-05-24.md`](./FRAMEWORK-AUDIT-2026-05-24.md).

---

## Part 1 — APRA controls: **ACCURATE (34/34). No inaccurate references found.**

Source files: `matrix/regulatory-trace.csv` rows where `framework_slug ∈
{apra-cps-234, apra-cps-230, apra-cpg-234}`.

### 1.1 CPS 234 (Prudential Standard, July 2019) — 25/25 verified

Source of truth: `cps_234_july_2019_for_public_release.pdf` (live extract).
Every cited paragraph number, evidence quote, and URL matches the standard verbatim,
including the four sub-clauses of §21 and §27(d), which were byte-checked:

- §21(a) "vulnerabilities and threats"; §21(b) "criticality and sensitivity";
  §21(c) "the stage at which the information assets are within their life-cycle";
  §21(d) "the potential consequences of an information security incident" — **all confirmed**.
- §27(d) "risks associated with exposure to environments where the APRA-regulated entity is
  unable to enforce its information security policies" — **confirmed** as item (d) of §27.

> **Self-correction note.** A pre-audit hypothesis held that the §34 quote ("internal audit
> function must assess the information security control assurance provided by a related party
> or third party") actually belonged to §33. **The live PDF disproves this** — paragraph 34
> reads exactly as cited; §33 covers internal-audit *skill* ("assurance is provided by
> personnel appropriately skilled"). The CSV is correct; the memory was wrong. Recorded here
> because it is the single highest-risk line in the APRA set and it is clean.

### 1.2 CPS 230 (Prudential Standard, Operational Risk Management) — 6/6 verified

Source of truth: 2023-07 CPS 230 PDF (live extract). All six paragraph numbers land exactly:

| Ref | Verified paragraph text (live) | Verdict |
|---|---|---|
| §15 | "must **not rely on a service provider** unless it can ensure that in doing so it can continue to meet its prudential obligations in full" | ✅ |
| §25 | IT-capability paragraph → "must **monitor the age and health** of its information assets and meet the requirements for information security in CPS 234" | ✅ |
| §42 | "must notify APRA … **not later than 24 hours** after, if it has suffered a disruption to a critical operation [outside tolerance]" | ✅ |
| §47 | "must maintain a **comprehensive service provider management policy**" | ✅ |
| §54 | "For all material arrangements … must maintain a **formal legally binding agreement**" | ✅ |
| §59(b) | "(b) **prior to entering into any material offshoring arrangement** …" (paragraph 59, sub-item b) | ✅ |

### 1.3 CPG 234 (Prudential Practice Guide, June 2019) — 3/3 verified

Source of truth: `cpg_234_information_security_june_2019_1.pdf` (live extract). The
attachment lettering exists and maps exactly: **Attachment C = Identity and access**;
**Attachment D = Software security**; **Attachment E = Cryptographic techniques** (full ToC:
A Security principles · B Training & awareness · C Identity & access · D Software security ·
E Cryptographic techniques · F Customer security · G Testing techniques · H Reporting).

### 1.4 Relevance — all APRA controls in scope are relevant

Each APRA reference maps to NHI/secrets-management risk via the `nhi_ids` column. The
service-provider / offshoring controls (CPS 230 §47/§54/§59) are relevant through third-party
NHIs (NHI-007, NHI-026, NHI-030, NHI-035). **No irrelevant APRA control was found.**

> **One data-modelling observation (not an accuracy defect):** the `maturity_level` column
> stores the paragraph pointer (e.g. `Paragraph-34`) rather than a maturity tier for APRA
> rows. This is a schema convention, not a regulatory inaccuracy. Flagged for tidiness only.

**APRA confidence: ≥ 98%** (primary-source, paragraph-level verification of every cited line).

---

## Part 2 — NHI taxonomy: **4 entries non-conformant, 1 needs reframing (of 37).**

### 2.1 The framing reality (important)

**APRA does not define "Non-Human Identity."** CPS 234/230 and CPG 234 govern *information
assets*, *access control*, and *service-provider* risk — they contain **no NHI taxonomy**.
The project's own `ADR-002` is honest about this: it anchors the 37-row taxonomy to the
**CSA NHI Working Group + Gartner MIM + SPIFFE + NIST**, "defensible to APRA/ASD review,"
not derived from APRA. Therefore the authoritative yardsticks for *tidying* are:

- **NIST / CNSSI 4009-2015 — Non-Person Entity (NPE):** *"An entity with a digital identity
  that acts in cyberspace, but is not a human actor. This can include organizations, hardware
  devices, software applications, and information artifacts."*
- **OWASP NHI (2025):** NHIs *"identify, authenticate, and authorize different software
  entities … not intrinsically tied to a human,"* and they **use** credentials — *"passwords,
  certificates, tokens, keys"* — i.e. **a key/token is a credential an NHI uses, not itself
  an NHI.** OWASP **NHI10:2025 "Human Use of NHI"** treats human use of an NHI as a risk.
- **NHIMG (Non-Human Identity Management Group)** — the body that originated the NHI Top-10
  OWASP later standardised. Its canonical **"three elements"** model independently corroborates
  this audit: *"a non-human identity usually has three elements: the **consumer** that performs
  the action, the **secret** that authenticates it, and the **entitlements** that define what it
  can access."* NHIMG's *consumers* are service accounts / workloads / bots / containers /
  pipelines / agents — **all non-human** — and the *secret* is explicitly **not** the identity.
  This validates the findings below from a third source: a human operator is not an NHI
  *consumer* (NHI-024/025); a key is a *secret*, not a *consumer* (NHI-023). Source:
  <https://nhimg.org/faq/what-are-the-three-elements-of-a-non-human-identity/>.

Three litmus tests follow: (T1) it must **act** and be **non-human**; (T2) it must be an
**identity**, not a **credential/secret**; (T3) it must be a **distinct entity**, not a
**programme or lifecycle attribute** spanning other identities.

### 2.2 Non-conformant entries

> **Referential constraint:** NHI IDs are foreign keys referenced 300–565× each across the
> vendor matrices, use-cases, regulatory trace and PRD. `validate_data.py` enforces unique
> IDs *and* cross-file referential integrity. **IDs must be preserved** — the correct remedy
> is to fix *meaning* (and/or add a conformance flag), never to delete or renumber.

| NHI | Current framing | Failing test | Regulator finding | Recommended disposition (ID preserved) |
|---|---|---|---|---|
| **NHI-023** Database TDE / encryption master-key identity | "The **key** (and custodian) used by TDE…" | **T2** | A TDE master key is a **cryptographic secret**, not an entity that acts. The entry conflates a credential with an identity. | Re-point to the **identity** — the KMS/key-custodian **principal** that controls the key — and state the key itself is a managed *secret*, not the NHI. |
| **NHI-024** HSM / KMS operator / break-glass identity | "high-privilege **identities that administer** the HSM … PED keys, smartcards, Shamir shares" | **T1** | PED-key/smartcard/quorum holders are **human operators**. This is a privileged **human** identity, not an NHI. The genuinely non-human KMS auto-unseal principal is already **NHI-035**. | Reclassify as **human-privileged / out-of-NHI-scope** (governance via UC-N-010), or narrow strictly to any *automated* break-glass principal. |
| **NHI-025** Certificate-authority operator identity | "Roles in private CA — RA, CA admin, auditor, enrolment agent … smartcard-bound admin certs" | **T1** | RA / CA-admin / auditor / enrolment-agent are **human PKI roles**. Not an NHI. The non-human **issuing-CA signing identity** is the real NHI (mesh case already = NHI-017). | Narrow to the **non-human issuing-CA signing identity**; move human operator roles to human-IAM scope. |
| **NHI-034** Quantum-resistant / hybrid-PKI rotation identity | "Identities involved in PQC … dual-signed certs, PQC-capable CAs and HSMs" | **T3** | Not an entity that acts — it is a **crypto-agility migration programme / attribute** applied across existing PKI identities (NHI-006, NHI-017, NHI-025). Dual-signed certs are credentials. Appendix C itself lists PQC under *cross-cutting concerns*. | Reframe as a **cross-cutting lifecycle attribute** of PKI identities, not a standalone NHI (governance via UC-N-013). |

### 2.3 Boundary entry — reframe, do not remove

| NHI | Issue | Finding |
|---|---|---|
| **NHI-029** Service-account-as-human (shared functional ID) | "AD/IdP account used by **multiple humans AND scripts**" | This **is** the OWASP **NHI10:2025 "Human Use of NHI"** anti-pattern. Legitimate NHI *governance* concern, but the wording conflates human and machine use. **Keep the ID; reframe** as a non-human service account whose **human use is the risk**, cross-referenced to OWASP NHI10. (ADR-002 already flagged it for v1.0 reclassification.) |

### 2.4 Conformant (no change) — 32/37

NHI-001…022, 026, 027, 028, 030, 031, 032, 033, 035, 036, 037 all satisfy T1–T3
(software/workload/device/bot entities that act, are non-human, and are identities rather
than secrets). NHI-014 (RPA bot) and NHI-037 (orphaned SA) are explicitly in-scope per OWASP
(bots; improper-offboarding NHI1:2025).

**NHI taxonomy confidence: ≥ 95%** (definitions from NIST/CNSSI + OWASP primary sources;
findings cross-checked against the entries' own self-descriptions and ADR-002).

---

## Part 3 — Remediation **APPLIED 2026-06-03** (preserves all IDs & referential integrity)

1. ✅ **Added `npe_conformance` column** to `identity-catalog.csv`:
   `CONFORMANT` (32) · `CREDENTIAL-NOT-IDENTITY` (NHI-023) · `HUMAN-IDENTITY` (NHI-024,
   NHI-025) · `CROSS-CUTTING-ATTRIBUTE` (NHI-034) · `HUMAN-USE-ANTIPATTERN` (NHI-029).
   Non-breaking (validator permits extra columns; verified).
2. ✅ **Corrected the five entries' `short_name`/`description`** in `identity-catalog.csv`,
   `PRD/appendices/C-glossary-and-NHI-definitions.md`, and `research/identity-taxonomy.md`
   per §2.2/§2.3 — **IDs unchanged**, so all foreign-key references stay valid. The
   "open questions for v1.0" entries in the taxonomy that raised exactly these
   classifications are now marked resolved.
3. ✅ **Verified zero breakage:** `matrix/validate_data.py` → *"All CSV data contracts
   valid."*; rebuilt `matrix-viewer.html` and refreshed `tests/fixtures/report.snapshot.html`;
   `pytest` → **111 passed**.

> **Not touched:** the frozen release copy under `dist/XYZ-Secrets-Management-PRD-v0.1/`
> is a versioned published package; it will pick up these corrections at the next release
> build rather than being edited in place.

## Part 4 — Use cases (47): valid; back-map layer rebuilt **APPLIED 2026-06-03**

**Question:** are the 47 UCs valid, ≥95% confidence? **Answer:** the use cases
*themselves* are valid; their *regulatory back-map column* was ~59% invalid and has
been rebuilt from the verified trace.

### 4.1 The use cases are valid (no UC removed or rescoped)
All 47 (UC-F-001..027 + UC-N-001..020) have coherent user stories, measurable
acceptance criteria, sensible `nhis_in_scope`, **full NHI coverage** (every NHI-001..037
referenced by ≥1 UC), no duplicate IDs/titles, and correct functional/non-functional
split. They are genuinely relevant to secrets/NHI management. The NHI-024/025 human
reclassification (Part 2) introduces **no inconsistency** — the UCs scoping them
(UC-N-010 break-glass/quorum-operator governance, UC-F-020 mainframe, UC-N-013 PQC) are
the correct homes for operator identities. **Confidence ≥98%.**

### 4.2 The `backmap_codes` column was ~59% invalid (now fixed)
The data validator never checked this column. Of 205 back-map references:

| Defect | Count | Evidence |
|---|---|---|
| `CSF-*` (NIST CSF) | 93 refs / 36 codes | NIST CSF 2.0 is **DEFERRED out of v0.1** per **ADR-003**; not a framework in the matrix. Codes are CSF **v1.1** IDs restructured in v2.0. |
| `CPS234-§28a/b/c` | 24 refs | **Fabricated** — live §28 is a single paragraph ("…commensurate with paragraphs 27(a) to 27(e)"); the (a)-(e) sub-items belong to **§27**. |
| `CPS234-§35c` (+`§35b`) | 2 refs | **Fabricated** — live §35 has only (a) and (b). |
| `CPS234-§33`, `CPS230-§39` | 2 refs | Real clauses but **not in the matrix** control set. |
| Reciprocity gaps | 27 pairs | Valid codes the trace's own `uc_ids` did not echo back. |

**Root cause (confirmed in ADR-003 §Neutral + the WS prompts):** the column kept the
pre-normalisation CPS 234 shorthand and the since-deferred CSF lens, and was never updated
after the 2026-05-24 ISM rebuild / CSF deferral. The same stale codes survive in
`research/use-cases.md` (now banner-superseded) and in `prompts/02-use-case-catalog-builder.md`
(**root generator — must be corrected before any UC regeneration**).

### 4.3 Remediation applied
- ✅ **Regenerated `backmap_codes` for all 47 UCs** from the **verified**
  `regulatory-trace.csv` (BACK-MAP tier = APRA CPS 234/230 + CPG 234 + ASD ISM, per
  ADR-003). Result: **0 CSF, 0 fabricated codes, 100% resolve, every UC ≥1 code, 0
  reciprocity gaps** (was 27). UC IDs unchanged (they are FKs). The rebuild also improved
  semantic fit (e.g. UC-F-007 "revocation" dropped the ill-fitting §34 internal-audit code
  and gained the incident-response cluster §23/§24/§26/§35).
- ✅ **Fixed UC-N-014 story** "12-vendor" → "19-vendor" (the matrix holds 19 vendors).
- ✅ **Banner-superseded** the stale inline back-maps in `research/use-cases.md`.
- ✅ Verified: only `backmap_codes` (+ that one story) changed vs `git HEAD`;
  `validate_data.py` valid; snapshot refreshed; **`pytest` → 111 passed**.
- ⚠️ **Residual (flagged, not changed):** `citation_keys` still cite `nist-csf-2.0-2024`
  on UC-N-001/004/005/015 (a real document, kept as background); and
  `prompts/02-use-case-catalog-builder.md` still encodes the old codes — fix before
  regenerating the catalog.

**Use-case back-map confidence after rebuild: ≥97%** (derived wholly from the
paragraph-verified trace).

## Part 5 — Generator hardening + stakeholder pack **APPLIED 2026-06-03**

To stop the defects re-appearing on any future regeneration, the upstream prompts were
corrected and the NPE/human-identity rules were encoded:

- **`prompts/02-use-case-catalog-builder.md`** — removed NIST CSF from the back-map
  sources; replaced the fabricated `§28a` example with valid normalised codes; added a
  **mandatory "Back-map integrity" guardrail**: `backmap_codes` must be reversed from
  `regulatory-trace.csv` (no invented codes, no CSF, no `§28a`/`§35c`), verified by
  `validate_data.py`.
- **`prompts/04-regulatory-mapper.md`** — marked **NIST CSF 2.0 as DEFERRED (ADR-003)**:
  do not dispatch a CSF mapper or emit `CSF-*` codes; refreshed the APRA/ISM source URLs.
- **`prompts/01-identity-taxonomist.md`** — added a **"What counts as an NHI" definition
  gate** (NIST NPE + OWASP NHI + the 3 litmus tests), fixed the stale CSV schema
  (`sources_at_anz_likely` → `sources_likely`, added `npe_conformance`), and the
  "preserve IDs, fix meaning" rule. This addresses the human-identity reclassification at
  the source (HSM/CA operators → `HUMAN-IDENTITY`).
- **Provenance note:** `PRD-FI-v0.1.md` and `research/regulatory/apra-cps-234-mapping.md`
  still mention `§28a–§28e` / CSF — these are **historical notes documenting the
  normalisation**, not current mappings, and are left as-is.

### Stakeholder deliverable
- **`stakeholder/Secrets-Mgmt-Stakeholder-Pack-2026-06-03.xlsx`** (generator:
  `matrix/build_stakeholder_pack.py`) — a shareable workbook with tabs **Read me · Use
  Cases (47) · NHI Taxonomy (37) · Regulatory back-map · Sources index**. **278 live
  hyperlinks** to primary sources (every UC and NHI row carries a clickable primary
  source; the back-map tab links each APRA/ISM control to its government evidence URL;
  the sources index resolves all cited keys to a URL). Colour-coded by
  priority and `npe_conformance`. Regenerable from the verified CSVs.
- **NHIMG citations added** to `meta/citations.bib` (`nhimg-three-elements-2025`,
  `nhimg-ultimate-guide-2025`, `nhimg-managing-nhi-risks-2025`) and **tagged onto the
  rows they support**: the three-elements definition on the five reclassified rows
  (NHI-023/024/025/029/034), the Ultimate Guide on NHI-019 (AI agent), and the risk
  white-paper on NHI-037 (orphaned legacy). 113/113 cited keys now resolve to a URL.

## Sources

- APRA CPS 234 (Jul 2019) — https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf
- APRA CPS 230 (2023-07) — https://www.apra.gov.au/sites/default/files/2023-07/Prudential%20Standard%20CPS%20230%20Operational%20Risk%20Management.pdf
- APRA CPG 234 (Jun 2019) — https://www.apra.gov.au/sites/default/files/cpg_234_information_security_june_2019_1.pdf
- NIST/CNSSI 4009-2015 NPE — https://csrc.nist.gov/glossary/term/non_person_entity
- OWASP NHI Top 10 (2025) — https://owasp.org/www-project-non-human-identities-top-10/2025/

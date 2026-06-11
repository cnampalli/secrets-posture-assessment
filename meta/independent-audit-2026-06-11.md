# Independent Audit — 2026-06-11

**Auditor:** independent (no prior exposure to this repository; all in-repo documents treated as claims-to-test, all external claims re-verified against live primary sources on 2026-06-11).
**Target:** `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/.claude/worktrees/ws4-report-naming` (branch `feat/ws4-report-naming`, head `8d20f07`, merge-base with `main` = `822833b`).

---

## 1. Executive summary

### 1.1 What this repository is (auditor's independent model)

This is a **multi-domain identity-security posture and vendor-selection assessment instrument**, built as a consulting product:

- **Data layer:** CSV "data contracts" per domain (`matrix/domains/{secrets,pam,iga}/` — use-cases, current-state, regulatory-trace, identity-catalog, per-vendor capability files) plus cross-domain YAML config (`matrix/config/` — control-ID registry, data provenance, vendor ownership/residency, domain descriptors, industry presets).
- **Engine layer:** ~3,400 lines of mostly-pure Python (`matrix/`, `questionnaire/`, `methodology/`, `presentation/`) that validates the data, scores posture, runs vendor-concentration/resilience analytics, and renders **one self-contained offline HTML report per domain** plus a cross-domain report, an exec summary, a roadmap generator, and an Excel stakeholder pack.
- **Front end:** a React/Vite questionnaire app (`app/`) sharing a scoring engine with the Python side via conformance vectors.
- **Narrative deliverable:** a PRD (`PRD/PRD-FI-v0.1.md`, 8 ADRs, 4 appendices) framing a secrets-management buyer's framework + current-state gap assessment for an anonymised AU Tier-1 financial institution ("XYZ"), under an APRA CPS 234/CPS 230, Essential 8, ASD ISM, CISA ZTMM, MITRE ATT&CK lens.

The repo's self-description (README, HANDOFF) matches this model **with one caveat**: the README is still written as if the repo were a single-engagement secrets PRD project, while the codebase has clearly evolved into a three-domain reusable product. The README's status lines, counts and dates are partially stale (see findings D-9).

The repo states an explicit core value: *"no invented numbers, no fabricated control mappings"* (HANDOFF.md:13–14), backed by anti-fabrication gates in `matrix/validate_data.py`. **This audit's central question was whether that promise holds.** Answer: it holds impressively well for regulatory control IDs, vendor capability evidence and the breach/ATT&CK corpus — and it **fails in the corporate-ownership layer**, where one acquisition claim is refuted and the single largest M&A event in the product's own market (Palo Alto Networks' completed acquisition of CyberArk) is missing entirely.

### 1.2 Verdict

**Overall: B — a genuinely well-engineered, unusually honest instrument with two material truthfulness defects in the vendor-ownership layer and a semantic gap in its anti-fabrication gating.** Fit for internal/illustrative use today; **not yet fit for client-facing use** until the ownership graph and the IGA CPS 234 §22 row are corrected (both are small fixes).

| Dimension | Score | Basis |
|---|---|---|
| Code quality | **A-** | Pure modules, dependency injection, descriptor pattern, deterministic builds; minor robustness nits |
| Correctness | **A-** | 308 pytest + 63 vitest pass; all 3 domain validators clean; all 4 HTML reports byte-stable on rebuild |
| Test adequacy | **B+** | Strong unit/parity/snapshot coverage; but the report SPA's JS is untested behaviorally and there is no CI |
| Data integrity | **B-** | 150/601 citation keys unresolvable; one wrong regulatory paragraph mapping; Essential 8 quote drift |
| Claim truthfulness | **B** | 42 external claims re-verified: 36 confirmed, 4 drifted, 2 refuted — both refutations in vendor ownership |
| Methodology | **B+** | Honest confidence taxonomy (PRD §8.1), illustrative-scenario banners, provenance gates; gates check ID membership, not semantics |
| Deliverable quality | **A-** | Self-contained, offline, navigable, deterministic, honestly bannered; some stale embedded metadata |

### 1.3 Top 10 issues at a glance

| # | Sev | Issue | Where |
|---|---|---|---|
| 1 | CRITICAL | "CyberArk acquired Entro Security (early 2025)" is **refuted** — Entro is independent (still independent at RSAC 2026). The ownership graph collapses an independent vendor under CyberArk and the cross-domain report displays it to readers | `matrix/config/vendor-ownership.yaml:36`; `matrix/cross-domain-report.html` |
| 2 | HIGH | Ownership graph misses **Palo Alto Networks' completed $25B acquisition of CyberArk (closed 2026-02-11)** — the "ultimate parent" of cyberark/conjur/venafi/zilla is wrong, and the WS3 ownership research (dated 2026-06) post-dates the close, so the "point-in-time" disclaimer does not cover it | `matrix/config/vendor-ownership.yaml` (whole cyberark cluster) |
| 3 | HIGH | IGA trace maps **CPS234-§22 to §21's content** ("implementation of controls"); actual §22 is third-party control-design evaluation. Fabrication-class per the project's own definition | `matrix/domains/iga/regulatory-trace.csv:16` |
| 4 | MEDIUM | **150 of 601 citation keys do not resolve** to `meta/citations.bib` (concentrated in PAM/IGA); no gate checks resolution | `meta/citations.bib`; `matrix/validate_data.py:271` |
| 5 | MEDIUM | Essential 8 `evidence_quote` text **drifts from the live cyber.gov.au source** (3 of 4 sampled quotes not verbatim-present) | `matrix/domains/secrets/regulatory-trace.csv` (E8 rows) |
| 6 | MEDIUM | The F3 anti-fabrication gate is **membership-only**: a registered control ID can carry the wrong title/quote/topic and still pass (root cause of #3) | `matrix/validate_data.py:245-263` |
| 7 | MEDIUM | **No CI** — every quality gate (pytest, validators, vitest) runs only when someone remembers to run it locally | repo root (no `.github/`) |
| 8 | MEDIUM | The consumer surface — the in-report 7-view SPA JavaScript — is tested only as a **byte snapshot**, never behaviorally | `tests/test_report_render.py`; `matrix/report-template.html` |
| 9 | LOW | Stale embedded metadata in deliverables: "111 tests pass" in the stakeholder pack, PRD "7,884 words" (actual ≈9,013), README references a non-existent `GEMINI.md`, HANDOFF claims a 15/16 IGA mapping gap that is actually fixed (16/16) | `matrix/build_stakeholder_pack.py:99`; `README.md:7,45`; `HANDOFF.md:54` |
| 10 | LOW | Citation provenance is fragmented across three stores (bib, WS3 ledgers in `docs/superpowers/plans/ws3-research/`, inline `evidence_url`); `iga-vendor-fit.csv` rows carry no `evidence_quote` at all | multiple |

---

## 2. Defects & bugs (severity-ranked)

### CRITICAL-1 — Fabricated-in-effect acquisition: Entro Security is not a CyberArk company

- **Where:** `matrix/config/vendor-ownership.yaml:36-43` (`entro-security: parent: cyberark, as_of: 2025-02, confidence: MEDIUM, note: "CyberArk announced acquisition of Entro Security … in early 2025"`).
- **Evidence:** Three independent web searches (2026-06-11) found **no announcement of any CyberArk–Entro acquisition**. Affirmative contradiction: Entro Security is profiled as an independent, VC-funded company ("most aggressively visible NHI startup at RSAC 2026") — see https://entro.security/ , https://www.securityweek.com/non-human-identity-lifecycle-firm-entro-security-raises-18-million/ , https://www.cremit.io/reports/rsac-2026-nhi . CyberArk's documented acquisitions in the period are Venafi (2024) and Zilla (2025) — neither is Entro.
- **Impact:** This is exactly the failure class the project promises to prevent. The CPS 230 service-provider-concentration analytics (`matrix/resilience.py`) collapse Entro under CyberArk, (a) overstating CyberArk-parent concentration and (b) telling a buyer that Entro is **not** an independent second-source when it is. The error is baked into the consumer-facing `matrix/cross-domain-report.html` (`"parents": [{"parent": "cyberark", … "brands": [... {"slug": "entro-security", ...}]`).
- **Mitigation in repo:** the entry is honestly marked `confidence: MEDIUM` with "verify close date and scope before client use" — which is why this isn't a worse finding — but the rendered reports do not surface that per-entry confidence to the reader.
- **Fix:** delete the `entro-security` entry from `vendor-ownership.yaml`, rebuild the cross-domain and secrets reports, and add a rule that `confidence: MEDIUM` ownership entries must either be verified to HIGH or excluded from concentration math (rendered as "unverified" instead).

### HIGH-1 — Ownership graph missing Palo Alto Networks' completed acquisition of CyberArk

- **Where:** `matrix/config/vendor-ownership.yaml` — `cyberark` is modeled as an ultimate parent (entries at lines 19, 24, 29, 67 point at it; nothing points above it). `grep -ri "palo alto networks"` across `matrix/config/`, `research/`, `docs/superpowers/plans/ws3-research/` returns nothing.
- **Evidence:** Palo Alto Networks **completed** its acquisition of CyberArk on **2026-02-11** (~$25B; $45.00 cash + 2.2005 PANW shares per share): https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-cyberark-to-secure-the-ai-era ; PANW 8-K: https://www.sec.gov/Archives/edgar/data/0001327567/000119312526045600/d40626dex991.htm ; announced 2025-07-30: https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-announces-agreement-to-acquire-cyberark--the-identity-security-leader .
- **Impact:** The schema's own definition ("`parent` = **ultimate** parent vendor_slug") is violated for the largest vendor cluster in the instrument (cyberark-conjur, cyberark-pam, venafi, zilla — and, per CRITICAL-1, entro). For an AU FI buyer, "your secrets vault, machine-identity PKI, PAM and modern IGA shortlist all roll up to **Palo Alto Networks**" is a materially different CPS 230 concentration story — especially if the institution already runs PANW firewalls/SASE/SOC tooling (a near-certainty for an AU Tier-1 FI). The "POINT-IN-TIME SNAPSHOT" disclaimer (line 16) does not excuse this: the WS3 ownership research is dated 2026-06-10/11, **four months after** the close, and the same research did correctly capture a 2026-03-05 event (Delinea–StrongDM). This is a research miss, not staleness.
- **Fix:** add `cyberark: {parent: palo-alto-networks, as_of: 2026-02-11, confidence: HIGH, source: paloaltonetworks.com press / SEC 8-K}`; `parent_of()` in `matrix/resilience.py:14-28` already follows multi-hop chains, so the engine needs no change. Rebuild reports; re-check the `test_cyberark_is_a_multi_brand_concentration_parent` pin in `tests/test_resilience_integration.py:64` (it asserts on the `cyberark` key and will need to follow the new root).

### HIGH-2 — IGA regulatory trace mislabels CPS 234 paragraph 22

- **Where:** `matrix/domains/iga/regulatory-trace.csv:16` — `CPS234-§22, "Implementation of controls (timely / commensurate)", uc_ids UC-I-008;UC-I-009;UC-I-010`, with an `evidence_quote` that reproduces **paragraph 21's** text ("An APRA-regulated entity must have information security controls to protect its information assets … implemented in a timely manner…").
- **Evidence:** Official CPS 234 PDF (July 2019, apra.gov.au), text-extracted by this audit: **¶21** = implementation of controls commensurate with (a)–(d); **¶22** = "Where an APRA-regulated entity's information assets are managed by a related party or third party, the APRA-regulated entity must evaluate the design of that party's information security controls…". Source: https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf . The secrets domain's own §22 row (`matrix/domains/secrets/regulatory-trace.csv`) has it **right**, so the two domains contradict each other in-repo.
- **Impact:** An audit/compliance reader cascading from CPS234-§22 in the IGA report gets the wrong obligation. By the project's own taxonomy (HANDOFF: "fabrication-class control-ID fixes") this is fabrication-class: right ID, wrong content. It passed the F3 gate because the gate checks only ID membership (see MEDIUM-3).
- **Fix:** either repoint the row to `CPS234-§21` (if the intent was implementation-of-controls) or rewrite title+quote to ¶22's third-party-evaluation content and re-map appropriate UCs (UC-I-008/009/010 — access reviews/SoD-type UCs — most plausibly belong under §21 or CPG 234). One-row change + report rebuild.

### MEDIUM-1 — 150 of 601 citation keys are unresolvable; no gate checks resolution

- **Where:** `meta/citations.bib` (538 entries) vs. `citation_keys` columns across `matrix/domains/*/*.csv` (601 distinct keys). Audit script result: **150 keys missing**, concentrated in PAM (92 missing in the aggregate `vendor-capabilities.csv` alone) and IGA (every key in `iga/regulatory-trace.csv`, `iga/use-cases.csv`, `iga/evidence-catalog.csv` is dangling); the secrets domain is nearly fully resolved (1–2 missing, incl. the HANDOFF-acknowledged `ms-pth-mitigation-2014`).
- **Why it matters:** `meta/citations.bib` is presented as the canonical citation store (README:76; `matrix/build_stakeholder_pack.py:29-46` resolves links from it, printing "(not in citations.bib)" on miss). The F2 gate (`matrix/validate_data.py:271-285`) only requires that a claim carry *some* key/URL/inference-tag — a typo'd or never-registered key passes forever. HANDOFF acknowledges exactly **two** dangling keys; the true count is 150, i.e., the provenance story is silently broken for two of three domains. (The underlying evidence mostly exists — WS3 ledgers under `docs/superpowers/plans/ws3-research/` and inline `evidence_url`s — but it is not resolvable from the data.)
- **Fix:** (a) backfill the bib from the WS3 ledgers (largely mechanical); (b) add a `check_citation_keys_resolve()` gate to `validate_data.py` that loads the bib and fails on unknown keys (allowlist sentinel tags).

### MEDIUM-2 — Essential 8 evidence quotes drift from the live primary source

- **Where:** `matrix/domains/secrets/regulatory-trace.csv`, E8 rows; registry claims source "cyber.gov.au Essential Eight Maturity Model (Nov 2023), verified 2026-05-24" (`matrix/config/control-id-registry.yaml:31-33`).
- **Evidence (live page fetched 2026-06-11, https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model ):**
  - `E8-MFA-ML1` quote *"Multi-factor authentication is used by users when accessing internet-facing services…"* — **absent** from the live model; this is the pre-Nov-2023 wording. Current wording: "Multi-factor authentication is used to authenticate users to their organisation's online services…". **DRIFT.**
  - `E8-RAP-ML1` quote *"Requests for privileged access to systems and applications are validated when first requested"* — live text reads "systems, **applications and data repositories**". **DRIFT** (truncated/older wording).
  - `E8-RAP-BREAKGLASS` quote *"Credentials for break glass accounts are long, unique, unpredictable and managed."* — live text: "Credentials for built-in Administrator accounts, break glass accounts, local administrator accounts and service accounts are long, unique, unpredictable and managed." The repo's version is a **condensation presented as a verbatim quote**. (Row cites the `-changes` page; even so it is not verbatim.)
  - `E8-RAP-LOG` quote "Privileged access events are centrally logged" — **CONFIRMED** verbatim.
- **Impact:** quotes are the instrument's evidence backbone; non-verbatim "quotes" undermine the ≥98%-verified assurance language embedded in the stakeholder pack (`matrix/build_stakeholder_pack.py:100`). Substantively the mappings remain correct — this is wording drift, not fabrication.
- **Fix:** re-verify all 26 E8 rows against the current model; either update quotes verbatim or relabel the column value as paraphrase (e.g., a `quote_type` flag).

### MEDIUM-3 — Anti-fabrication gate F3 binds IDs, not meaning

- **Where:** `matrix/validate_data.py:245-263` (`check_control_id_registry`) + `matrix/config/control-id-registry.yaml`.
- **Problem:** the gate freezes the *set* of permissible control codes, with an optional regex. Nothing binds a control code to its expected **topic/title/quote**, so HIGH-2 (right ID, wrong content) passes, and any future row can attach any prose to any registered ID. The registry comments themselves record that the original failure was wrong *content* mapping ("≈80% of the original ISM IDs were wrong").
- **Fix:** extend the registry to `ISM-1404: {title_contains: "45 days", topic: "Suspension of access"}`-style assertions (even a short `expect_substring` per control catches transposition errors), and have the gate check `control_short_title`/`evidence_quote` against them. Cheap, high leverage — it would have caught HIGH-2 mechanically.

### MEDIUM-4 — No CI pipeline

- **Where:** no `.github/`, no CI config anywhere in the worktree.
- **Problem:** the project's entire integrity posture (308 tests, 3 validators, byte-stable snapshots, vitest) is enforced only by operator discipline. The git history shows multi-PR, multi-worktree, multi-laptop development — precisely the workflow where an unrun gate slips through. The HANDOFF "Gates:" lines are self-reported.
- **Fix:** a ~20-line GitHub Actions workflow: `pytest -q`, `validate_data` ×3, `node questionnaire/scoring.test.mjs`, `cd app && npm ci && npx vitest run`, plus a rebuild-and-diff job asserting the four HTML reports are byte-identical to committed versions (this audit verified all four rebuild byte-stable, so the job will be green from day one).

### MEDIUM-5 — The report SPA is only snapshot-tested

- **Where:** `tests/test_report_render.py:9-16` (byte-identity vs `tests/fixtures/report.snapshot.html`); the actual UI logic lives as large inline JS in `matrix/report-template.html` / `matrix/cross-domain-template.html` (7 views, tab routing, filtering, "mark as MET" localStorage override, value-view banners).
- **Problem:** byte-snapshot testing proves determinism, not behavior. No test would catch a broken tab, a filter that drops rows, an override that mis-persists, or a regression in the gap→decision-card navigation that the README sells as the product's "fastest way in". The only JS under test is the 10-line scoring engine (vector parity) and the exec-summary script.
- **Fix:** extract the report JS into a testable module (built into the template at render time) and add a handful of DOM tests (jsdom/vitest — infrastructure already present in `app/`), prioritising: posture-count math, gap-link navigation targets, compliance-cascade filtering, MET-override persistence.

### LOW-1 — `derive_state` returns MET for an empty question list

- **Where:** `methodology/scoring.py:10-22` (mirrored in `questionnaire/scoring.js`).
- **Repro:** `derive_state([], {})` → `"MET"` (`all()` on empty is guarded by `vals and …`, but the subsequent `any()` checks are vacuously false and fall through to `return "MET"`). A UC accidentally mapped to an archetype with zero questions would silently score MET — the most favorable state — instead of erroring. Currently masked by `methodology/validate_rubric.py` coverage checks; the function itself should `raise ValueError` (and the JS mirror throw) on empty input, with a parity vector added.

### LOW-2 — Stale/self-inconsistent embedded metadata in deliverables and docs

- `matrix/build_stakeholder_pack.py:99`: "validate_data.py green; **111 tests pass**" — suite is 308; the claim is baked into a client-visible Excel tab.
- `README.md:45`: PRD "7,884 words" — `wc -w` gives ≈9,013 (the PRD grew; the claim didn't).
- `README.md:7-8`: directs readers regarding `GEMINI.md` "in this directory" — the file does not exist.
- `README.md:16-21` says "12+ vendor evaluations" naming 12; line 44 says 19 profiles; line 108 says 18 ranked vendors. All can be reconciled (18 ranked + 1 unranked L0 substrate = 19 profiles) but the README never reconciles them for the stakeholder it addresses.
- `HANDOFF.md:54`: "IGA 'REG-mapped UCs' off-by-one (15/16…)" — audit recomputation shows **16/16 mapped, zero unmapped**; the known-issues list is stale in the repo's favor.
- **Fix:** make embedded counts computed-at-build (test count, word count), and sweep README/HANDOFF claims at release time.

### LOW-3 — Anonymisation residue and aperture

- Content-level anonymisation to "XYZ" is systematic and even validator-enforced (`methodology/validate_rubric.py:17` `check_no_anz`, scoped to methodology CSVs), and no real-bank identifiers were found in any deliverable. However: the filenames `research/anz-current-state-evidence.md` and `PRD/adrs/ADR-005-anz-evidence-policy.md` survive (and are linked from README:102,150), and the report banner narrows the client to "a major AU Tier-1 FI" — filename + banner together substantially de-anonymise. If anonymity matters, rename the two files and genericise the banner; if it doesn't, drop the pretense in-repo.

### LOW-4 — `iga-vendor-fit.csv` evidence is URL-only

- **Where:** `matrix/domains/iga/iga-vendor-fit.csv` — sampled rows (conductorone, microsoft-entra-idg, lumos, sailpoint-isc) have an `evidence_url` but an **empty `evidence_quote`**, unlike the vendor-capabilities standard elsewhere. `check_vendor_fit` (validate_data.py:174) gates "sourced", not "quoted". URLs rot; quotes are the recoverable evidence. Backfill quotes (the WS3 ledgers likely already contain them).

---

## 3. Data-integrity & research-validation findings

### 3.1 Sampling strategy

Stratified, risk-weighted: (a) **exhaustive** re-verification of all 7 corporate-ownership/M&A claims (highest decision impact, highest churn); (b) random/coverage samples of ISM control IDs (10 of 47 registered), CPS 234 paragraph mappings (8 paragraphs incl. both domains' §21/§22), Essential 8 verbatim quotes (4), MITRE sub-technique IDs (3 of the less-common ones), and vendor capability evidence rows (9 rows across 8 vendors and all three domains, biased toward the newest WS3 vendors flagged "marketing-tier" in-repo); (c) nominal review of the 8 breach-case references against well-documented public incidents (names/dates checked, sources not re-fetched). Total: **42 externally checked claims**.

### 3.2 Ledger

| Claim (as stated in repo) | Verdict | Primary source | Note |
|---|---|---|---|
| CyberArk acquired Entro Security, early 2025 (`vendor-ownership.yaml:36`) | **REFUTED** | entro.security; securityweek.com (funding); cremit.io RSAC-2026 NHI report | No such acquisition found in 3 searches; Entro independent as of RSAC 2026 |
| CyberArk is ultimate parent of conjur/pam/venafi/zilla (`vendor-ownership.yaml`) | **REFUTED (by omission)** | paloaltonetworks.com/company/press/2026/…completes-acquisition-of-cyberark…; SEC 8-K | PANW closed $25B acquisition 2026-02-11; repo has zero PANW references |
| Delinea completed StrongDM acquisition 2026-03-05 | CONFIRMED | globenewswire.com/news-release/2026/03/05/3250113 | Date, "completed" status, and AI/ZSP framing all match |
| CyberArk acquired Zilla Security 2025-02-13, ~$165M + $10M earn-out | CONFIRMED | cyberark.com press; techcrunch.com/2025/02/13 | Exact figures match |
| CyberArk completed Venafi acquisition Oct 2024, ~$1.54B | CONFIRMED | cyberark.com press; SEC 6-K exhibit | Completed 2024-10-01; ~$1B cash + ~$540M shares |
| IBM completed HashiCorp acquisition 2025-02-27, ~$6.4B | CONFIRMED | techcrunch.com/2025/02/27; paulweiss.com | Exact date and value |
| BeyondTrust did NOT acquire Britive (WS3 "REFUTED" entry) | CONFIRMED | tracxn (BeyondTrust acquisitions list); crunchbase | Repo's own refutation independently confirmed |
| ISM-1898 = "Secure Admin Workstations are used in the performance of administrative activities" | CONFIRMED | cyber.gov.au ISM Guidelines for System Management PDF (Dec 2024) | Exact |
| ISM-0430 = same-day access removal | CONFIRMED | anao.gov.au insight citing ISM-0430; ismcontrol.xyz | Exact |
| ISM-1380 = separate privileged/unprivileged operating environments | CONFIRMED | ismcontrol.xyz/1380/ | Exact |
| ISM-1175 = privileged accounts prevented from internet/email/web | CONFIRMED | ismcontrol.xyz/1175/ | Exact incl. the "excluding those explicitly authorised" clause |
| ISM-1647 = privileged access disabled after 12 months unless revalidated | CONFIRMED | ismcontrol.xyz/1647/ | Exact |
| ISM-1619 = service accounts created as gMSA | CONFIRMED | ismcontrol.xyz/1619/ | Exact |
| ISM-0407 = secure per-user access record incl. review dates | CONFIRMED | ismcontrol.xyz/0407/ | Exact |
| ISM-1917 = PQC transition (ML-DSA-87/ML-KEM-1024/… by 2030) | CONFIRMED | ismcontrol.xyz/1917/ | Exact |
| ISM-1404 = unprivileged access disabled after 45 days inactivity | CONFIRMED | ismcontrol.xyz/1404/ | Exact |
| ISM-1795 = ≥30-char credentials for built-in admin/break-glass/local-admin/service accounts | CONFIRMED | ismcontrol.xyz/1795/ | Exact |
| CPS 234 ¶13 board responsibility | CONFIRMED | apra.gov.au CPS 234 PDF (extracted) | Verbatim match |
| CPS 234 ¶14 roles/responsibilities | CONFIRMED | same | Verbatim |
| CPS 234 ¶21 implement controls, commensurate (a)–(d) | CONFIRMED | same | Verbatim incl. sub-paras |
| CPS 234 ¶22 (secrets domain: third-party control design) | CONFIRMED | same | Secrets row correct |
| CPS 234 ¶22 (IGA domain: "implementation of controls") | **DRIFT/WRONG** | same | IGA row carries ¶21 text under §22 — see HIGH-2 |
| CPS 234 ¶26 annual review/test of response plans | CONFIRMED | same | Verbatim |
| CPS 234 ¶27 systematic testing, (d) untrusted-environment exposure | CONFIRMED | same | Verbatim |
| CPS 234 ¶35 72-hour incident notification | CONFIRMED | same | Verbatim |
| CPS 234 ¶36 10-business-day control-weakness notification | CONFIRMED | same | Verbatim |
| E8 quote "Privileged access events are centrally logged…" | CONFIRMED | cyber.gov.au E8 maturity model (live) | Verbatim present |
| E8-MFA-ML1 quote ("…internet-facing services…") | **DRIFT** | same | Pre-Nov-2023 wording; absent from live model |
| E8-RAP-ML1 quote ("systems and applications") | **DRIFT** | same | Live adds "and data repositories" |
| E8-RAP-BREAKGLASS quote | **DRIFT** | same | Condensed paraphrase presented as quote |
| MITRE T1552.008 exists (Chat Messages) | CONFIRMED | attack.mitre.org/techniques/T1552/008/ | |
| MITRE T1556.006 exists (Multi-Factor Authentication) | CONFIRMED | attack.mitre.org/techniques/T1556/006/ | |
| MITRE T1606.002 exists (SAML Tokens) | CONFIRMED | attack.mitre.org/techniques/T1606/002/ | |
| Apono Access Discovery quote (pam UC-P-005) | CONFIRMED | docs.apono.io/docs/getting-started/access-discovery.md | Verbatim |
| Netwrix agentless privileged-account discovery quote (UC-P-005) | CONFIRMED | netwrix.com/privilege_secure_for_discovery.html | Near-verbatim, claim accurate |
| Akeyless dynamic DB secrets target list (UC-F-005) | CONFIRMED | docs.akeyless.io/docs/agentic-runtime-authority.md | All 10 DBs listed |
| Aembit/Snowflake "85% … eliminated" (UC-F-005) | CONFIRMED | aembit.io/case-study/snowflake-uses-aembit-to-secure-workload-access/ | Verbatim; note it is a vendor case study (marketing-tier) |
| Britive "Account Discovery & Drift Detection" (UC-P-005) | CONFIRMED | britive.com/use-cases | Present; marketing-tier as repo itself flags |
| StrongDM "proxy that manages and audits access…" (UC-P-002) | CONFIRMED | strongdm.com/how-it-works | Verbatim |
| Lumos access-reviews product exists (iga fit grid) | CONFIRMED | lumos.com/products/access-reviews | Product real; claims match grid |
| Keyfactor SignServer CI/CD signing integration (UC-F-016) | CONFIRMED | keyfactor.com/products/signserver-enterprise/ | Verbatim |
| Astrix AI-agent discovery incl. OpenAI/Databricks (NHI-020) | CONFIRMED | astrix.security/product/ai-agent-discovery/ | Confirmed |
| 8 BREACH-* case refs (Okta ×2, Cloudflare 2023-11, CircleCI 2023-01, Internet Archive 2024-10, Sourcegraph 2023-08, LastPass 2022, xz-utils 2024-03) | CONFIRMED (nominal) | public reporting | Names/dates/mechanisms all match well-documented incidents; not re-fetched |

**Totals: 42 checked → 36 CONFIRMED, 4 DRIFT, 2 REFUTED.**

### 3.3 Implied confidence about unsampled claims

- **ISM / CPS 234 / MITRE strata:** 21/21 confirmed with exact-text matches. The post-remediation control registry (47 ISM + 25 CPS 234 + others) is very likely sound; residual risk concentrates in *content drift on unsampled rows* (the HIGH-2 pattern), not in invented IDs. Estimated error rate on unsampled control-ID rows: low single-digit percent.
- **Vendor-capability stratum:** 9/9 confirmed, including the WS3 vendors the repo itself flags as marketing-tier. The 1,596-row secrets matrix and PAM/IGA vendor files are likely accurate at the claim-existence level; maturity scores remain analyst judgment by design (disclosed in PRD §8.1).
- **Essential 8 quote stratum:** 3/4 drifted → drift is probably **systematic** across the ~26 E8 rows (captured from an older model revision). Treat every E8 quote as suspect until re-verified.
- **Ownership stratum:** exhaustively checked; no extrapolation needed — 2/7 wrong, both fixed by the recommendations above.

---

## 4. Gaps

1. **No CI / no enforced gate-on-merge** (MEDIUM-4). The strongest validator suite in the repo is only as good as the last human who ran it.
2. **No citation-resolution gate and no link-rot tooling.** `data-provenance.yaml` declares `refresh: quarterly` cadences, but nothing re-checks `evidence_url` liveness or quote presence. A trivial offline gate (bib resolution) and a periodic online job (HTTP 200 + quote-substring check) would convert the provenance manifest from documentation into enforcement.
3. **Semantic gap in the anti-fabrication design** (MEDIUM-3): IDs are frozen, meanings are not.
4. **Ownership-confidence not surfaced to readers.** `vendor-ownership.yaml` carries per-entry `confidence`, but the rendered concentration views present all parent collapses with equal authority.
5. **Behavioral test coverage of the consumer surface** (MEDIUM-5): the HTML report SPA — the thing stakeholders actually touch — has no functional tests.
6. **Domain asymmetry:** secrets lacks `evidence-catalog.csv`/`uc-archetype-map.csv` in its data dir (archetype map lives in `methodology/`), while PAM/IGA have evidence catalogs; `iga` has a fit grid, others don't. The descriptor pattern handles it, but consultants extending a domain must learn three slightly different shapes.
7. **Secrets current-state freshness:** the XYZ posture evidence leans on a 2026-05-22 interview and items as old as a 2019 red-team finding; there is no per-row capture date (acknowledged in `data-provenance.yaml` as deferred). Fine for v0.1, but a re-baselining mechanism is needed before any follow-up engagement.
8. **README is a time capsule:** it still narrates the May-2026 single-engagement PRD project (Monday stakeholder review, milestone gates) rather than the three-domain product the repo now is; HANDOFF.md is the real front door. A newcomer reading README first gets a materially outdated picture (PAM/IGA aren't mentioned at all).
9. **No automated consistency check between per-vendor CSVs and the aggregate** `vendor-capabilities.csv` was found in the validator (tests cover builds; the validator accepts both independently). If they drift, reports silently reflect whichever the loader prefers.

---

## 5. Recommendations (prioritized)

### Now (before any client-facing use; ~half a day total)

1. **Fix the ownership graph** — delete `entro-security` entry; add `cyberark → palo-alto-networks (closed 2026-02-11)`; re-verify the remaining entries' as-of dates; rebuild all four reports; adjust the `cyberark` pin in `tests/test_resilience_integration.py`. *Effort: 1–2 h. Payoff: removes both refuted claims; the headline CPS 230 feature becomes true again.*
2. **Fix IGA CPS234-§22** (one CSV row + rebuild). *Effort: 30 min. Payoff: regulatory trace correct in a compliance deliverable.*
3. **Re-verify the 26 E8 quote rows** against the live maturity model; update verbatim or mark paraphrase. *Effort: 2–3 h. Payoff: the "verbatim evidence quote" standard becomes true for the E8 stratum.*

### Next (1–2 weeks)

4. **Add CI** (GitHub Actions: pytest + 3 validators + scoring vectors + vitest + report rebuild-and-diff). *Effort: half a day. Payoff: every guarantee in HANDOFF becomes machine-enforced.*
5. **Citation-resolution gate + bib backfill** from WS3 ledgers (150 keys). *Effort: 1–2 days, mostly mechanical. Payoff: provenance claim true for all three domains; stakeholder-pack link resolution stops silently degrading.*
6. **Semantic registry**: add `expect_substring`/topic assertions per control to `control-id-registry.yaml` and enforce in F3. *Effort: 1 day. Payoff: the HIGH-2 class becomes mechanically impossible.*
7. **Surface ownership confidence** in the concentration views, and exclude (or visibly caveat) `MEDIUM`-confidence parent collapses. *Effort: half a day.*
8. **Stale-metadata sweep** (LOW-2 items) + compute embedded counts at build time. *Effort: 2 h.*

### Later

9. **Behavioral tests for the report SPA** (extract inline JS to a module; jsdom tests for posture math, navigation, cascade filtering, MET-override persistence). *Effort: 2–4 days. Payoff: the consumer surface gains real regression protection.*
10. **Link-rot / quote-presence checker** run on the `data-provenance.yaml` refresh cadence. *Effort: 1–2 days.*
11. **README rewrite** as the product's front door (three domains, engine architecture, HANDOFF for resume mechanics). *Effort: half a day.*
12. **Aggregate-vs-per-vendor consistency gate** in `validate_data.py`. *Effort: 2 h.*

---

## 6. Improvement roadmap (taking it to the next level)

The architecture is already deep in the right places — pure analytics modules (`report_logic`, `resilience`, `optimizer`, `compliance`) behind small interfaces, config injected (ownership/residency/presets), domains as data (descriptors), and a fully deterministic render pipeline (all four HTML artifacts rebuilt byte-identical during this audit). The next level is about turning *documented intentions into enforced invariants* and *one-off research into refreshable data*:

1. **Provenance as code.** Today provenance is three artifacts (bib, ledgers, YAML manifest) plus discipline. Unify on one citation store with a resolver gate, per-row `as_of` capture (schema column already anticipated), and a scheduled re-verification job. The product's differentiator is honesty; make the honesty machine-checkable end-to-end.
2. **Ownership graph as a first-class, dated, multi-hop entity graph** with mandatory primary-source URL per edge and a freshness SLA tied to `data-provenance.yaml` (`refresh: per-engagement`). M&A is the fastest-drifting data in this product (this audit found a four-month-old $25B event missing); it deserves the same gate rigor as control IDs.
3. **Seam-test the report SPA.** The inline-JS template is the shallowest seam in the codebase: a huge behavior surface reachable only through byte-snapshots. Extracting it into a real module (bundled at render time) creates a second adapter for the same interface (Python-rendered page ↔ tested JS module) and unlocks the React app and report to share view logic.
4. **Engagement workflow productisation** (the repo's own Phase 5 direction is right): client workspace, current-state import, benchmark deltas — all of which become safe only after (1) and (2), because reused data is data that silently ages.
5. **Domain symmetry:** converge the three domains on one canonical file set (evidence catalog + archetype map + fit grid all optional-but-uniform in the descriptor), so the fourth domain (Workforce IAM, parked) is a data exercise, not a code exercise.

---

## 7. Methodology appendix

### What was reviewed

- **Full structural sweep** of the worktree (426 git-tracked files; generated artifacts and `app/node_modules` excluded from review).
- **Executed gates:** `python3 -m pytest -q` (308 passed, 1.45 s); `matrix/validate_data.py` for secrets (no-arg default), PAM, IGA (all clean); `npx vitest run` in `app/` (63 passed); deterministic-rebuild check of all four HTML reports (`build_matrix_viewer.py` ×3 + `build_cross_domain.py` — all byte-identical to committed artifacts); working tree restored/clean throughout.
- **Code read in depth:** `matrix/validate_data.py`, `matrix/resilience.py`, `methodology/scoring.py`, `package.sh`, the full WS4 branch diff (`main...HEAD`, 51 files), spot reads of `report_io`/`report_logic`/`build_stakeholder_pack`/`roadmap_generator` interfaces, `questionnaire/scoring.js` parity harness.
- **Data analysis scripts (auditor-written, run locally):** citation-key ↔ bib cross-resolution (601 keys), control-ID census, IGA REG-mapping recomputation, per-domain CSV structure sampling.
- **Deliverables opened as a consumer:** secrets/pam/iga reports (banner, mock-posture disclosure, baked-data checks), cross-domain report (parent-concentration JSON), stakeholder pack builder, PRD §8.1, README/HANDOFF/STAKEHOLDER-START-HERE.
- **External verification:** 42 claims re-checked against live primary sources (ledger in §3.2), including text-extraction of the official APRA CPS 234 PDF and the live cyber.gov.au Essential Eight maturity model page.

### Fleet & skills

- No `Agent` tool was available in this session, so the planned sub-agent fan-out (mapping explorers, per-domain specialists, verifier fleet) was executed **inline by the auditor** in sequential/parallel tool batches. Effective "fleet size": 1 auditor performing ~10 distinct roles (mapper, code reviewer, data validator, regulatory SME, vendor-intel verifier ×2 strata, consumer reviewer, refute-tester, synthesist).
- **Skills invoked:** `code-review` (high) — angles applied inline over the WS4 diff (verdict: clean refactor; no findings above LOW); `deep-research` — phases executed inline with WebSearch/WebFetch (its `Workflow` runner was also unavailable); `improve-codebase-architecture` — its depth/seam/locality lens applied analytically to ground §6 (the skill's interactive HTML-report/grilling flow was inappropriate for an unattended audit and was not run). No memory/recall tooling was used; hook-injected "prior observation" banners on file reads were disregarded as audit input.
- **Independence note:** all in-repo verification records (`matrix/ISM-CONTROL-VERIFICATION-2026-05-24.md`, `REGULATOR-AUDIT-2026-06-03.md`, WS1–WS3 notes, dated reviews in `meta/`) were treated strictly as claims; every verdict in §3.2 rests on a source fetched or searched during this audit.

### Explicitly NOT covered

- The remaining 37 of 47 registered ISM controls, CPS 230/CPG 234 paragraph texts, and ~1,950 of the ~1,960 vendor-capability rows (sampled strata only; confidence statement in §3.3).
- Breach-case rows were name/date-checked against public knowledge, not re-fetched.
- The React app (`app/src/`) beyond running its test suite; the Brass Editorial design system; `spikes/`; the Excel pack's rendered output; PRD prose accuracy beyond §8.1 and structural claims; `docs/adr/` contents.
- Performance, accessibility (WCAG), and browser-matrix testing of the HTML reports.
- Any commit history forensics beyond branch-diff review and merge-base confirmation.

*Report generated 2026-06-11. The only working-tree change made by this audit is this file.*

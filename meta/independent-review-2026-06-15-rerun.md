# Independent Buyer-Grade Defensibility Review — Posture-Assessment Instrument (RE-RUN)

**Date:** 2026-06-15 (re-run; supersedes 2026-06-15 AM pass)
**Reviewer:** Independent multi-agent SME panel (buyer due-diligence lens)
**Methodology:** `/methodology/INSTRUMENT-REVIEW-METHODOLOGY.md` — 4 lenses × 20 dimensions, bands 0–3, verdict Buy / Buy-with-conditions / Not-yet
**Scope:** Secrets-management, PAM, IAM (cross-domain identity spine), and IGA governance control sets; data-integrity / anti-fabrication; regulatory defensibility (APRA CPS 234/230, ASD ISM, Essential Eight, NIST); output-correctness of the buyer-facing posture board; and the cross-cutting M3 agentic surface.
**Target:** worktree `m3-agentic-secrets-pam` HEAD, incl. M3.1 / M3.2 / M3.3 agentic work and the 6 MUST-FIX remediation (PR #39).
**Verification protocol:** Per-lens SME findings were independently re-derived against live data (CSV parses, `validate_data.py` runs, rendered HTML JSON, live-source quote spot-checks). All HIGH/CRITICAL findings were adversarially refute-tested before inclusion; MED/LOW pass through. Remediation closure was checked **in the data**, not from commit messages.

---

## 1. Executive Summary

### BOTTOM LINE UP FRONT

**Overall verdict: Buy-with-conditions** (unchanged label, materially improved posture).

The remediation **did move the needle** — but it did not clear the bar to an unconditional **Buy**, because two of the six MUST-FIX items did not fully land and the same fabrication-class defect they were meant to kill **re-surfaced in a sibling domain (PAM)** that was outside the original 6-item remit.

What genuinely improved:
- The 2026-06-09 **#1 buyer concern — the agentic-AI / OAuth-consent currency gap — is now CLOSED** with a coherent, privileged-aware identity spine (SPN-015 non-priv / SPN-016 priv), 9 agentic UCs across all three domains riding the same archetype-scored engine (A2/A3 templates, not bolt-ons), structured MITRE ATT&CK grounding (T1078/T1098 + OWASP LLM06), and a WS3-verified research base whose load-bearing OWASP quotes were confirmed **verbatim** against the live source.
- **4 of 6 MUST-FIX items are fully CLOSED in the data** (IAM-01, PAM-01, PAM-02, OC-01) with no new dangling references.
- **Anti-fabrication is now genuinely defensible**: independent recount found 4 dangling citation keys (all deliberate, allowlisted ISO-27001 sentinels) vs the prior audit's 150 unresolvable, and 0 orphan control_codes across 204 trace rows.

What still blocks an unconditional Buy:
- **REG-AGENTIC-01 is only PARTIALLY-CLOSED** — the regulatory-trace was fixed but the buyer-facing `use-cases.csv` backmap for UC-P-019 still self-declares the wrong control (ISM-1304), rendered into the stakeholder pack.
- **The IGA CPS234-§22 fix was half-applied** (trace fixed, `use-cases.csv` not) and the **identical right-ID-wrong-scope class re-appeared in PAM** (CPS234-§22 → four internal UCs). Both reach regulator-facing HTML/XLSX.

These are all **single-row, low-effort fixes** plus one **validator-rule** to stop the two files drifting again. None is a structural or content-coverage defect. A procurement DD team would make the PAM §22 re-map and the UC-P-019 backmap correction conditions of purchase — hence **Buy-with-conditions**, with a credible path to **Buy** on a one-day fix pass.

### Verdict trajectory

| Pass | Verdict | Driver |
|---|---|---|
| 2026-06-09 | Buy-with-conditions | Agentic currency gap (#1), no maturity roll-up, no benchmark, internal-only calibration |
| 2026-06-15 AM | Buy-with-conditions | 6 MUST-FIX list issued |
| **2026-06-15 (this re-run)** | **Buy-with-conditions** | 4/6 MUST-FIX closed; agentic gap closed; residual = 2 partial remediations + PAM §22 regression of a known class |

---

## 2. Remediation Regression Table (the 6 MUST-FIX items)

| # | MUST-FIX item | Status | Evidence (file:line) |
|---|---|---|---|
| IAM-01 | NHI-019 / IGID-009/012/013 `npe_conformance` NPE→CONFORMANT + closed-vocabulary enum gate | **CLOSED** | All 3 catalogs parse to exactly the 5 legal values, no bare `NPE`. `identity-catalog.csv:20` (NHI-019), iga `identity-catalog.csv:10,13,14` all CONFORMANT. `VALID_NPE_CONFORMANCE` at `validate_data.py:28`, gate wired at `:679`, verified rejecting `NPE`/`npe`. Validator clean; 61 tests pass. |
| PAM-01 | SPN-016 privileged-agent archetype added; PID-021 remapped SPN-015→SPN-016; no dangling refs | **CLOSED** | `identity-spine.yaml:141-148` defines SPN-016 (agentic/privileged); `pam/identity-catalog.csv:22` PID-021→SPN-016 is the sole referent; SPN-015 (`:136`) updated; rendered in `cross-domain-report.html` (span=1, PAM-only, by-design). `validate_data.py:645-649` enforces spine registration; clean. |
| AG-01 | Agentic citations re-pointed `csa-ai-agents-2024` → `csa-agentic-iam-2025` (ledger-verified) | **CLOSED** | grep finds zero `csa-ai-agents-2024` in any data CSV; old key only an unused bib def at `citations.bib:30`. New key `citations.bib:4157` (note "re-fetched live 2026-06-14"). Used by NHI-019, PID-021, IGID-012, and agentic UCs in secrets+PAM. |
| PAM-02 | MITRE ATT&CK grounding for agentic privileged ops; agent-session UC re-anchored | **CLOSED** | `pam/regulatory-trace.csv:29-31` add T1078 (Valid Accounts), T1098 (Account Manipulation), LLM06:2025 as THREAT-CONTEXT → UC-P-019/020/021 + PID-021, verbatim quotes + authoritative attack.mitre.org URLs. Defined `citations.bib:4129-4141`. Excluded from compliance % via `pam.yaml:48`. |
| REG-AGENTIC-01 | ISM-1405 + E8-RAP-LOG expanded to agentic session logging; ISM-1304 remapped without agentic UC/identity | **PARTIALLY-CLOSED** | Trace side CORRECT: `pam/regulatory-trace.csv:5` ISM-1405 lists UC-P-019 + PID-021; `:13` E8-RAP-LOG lists same; `:4` ISM-1304 excludes all agentic UCs/PID-021. **BUT** `pam/use-cases.csv:20` UC-P-019 `backmap_codes` still self-declares `ISM-1304` (not ISM-1405), rendered into the XLSX pack by `build_stakeholder_pack.py:143`. See **PAM-SME-01**. |
| OC-01 | Informative frameworks (owasp-llm) excluded from compliance % in secrets descriptor (and consistently) | **CLOSED** | `secrets.yaml:65`, `pam.yaml:48`, `iga.yaml:60` all list `['mitre-attack','owasp-llm','ms-incident']` in `informative_frameworks`. Defence-in-depth: `report_logic.py:90` `_EVIDENCE_COMPLIANCE_ROLES={PRIMARY-LENS,BACK-MAP}` excludes the THREAT-CONTEXT owasp-llm row by role independent of the descriptor. Rendered `secrets-report.html` COMPLIANCE JSON contains no owasp-llm. |

**Net: the 6 named items → 5 CLOSED / 1 PARTIALLY-CLOSED.**

### Re-test of the prior independent-audit-2026-06-11 CRITICALs (NOT in the 6 MUST-FIX list)

| Prior CRITICAL | Status this pass | Note |
|---|---|---|
| Entro / CyberArk false-acquisition claim | **NOT RE-TESTED this pass** — outside the agentic+remediation remit; vendor-layer collateral not in the worktree surface re-examined. **Flag as outstanding-unverified**; must be confirmed removed before any vendor-facing sale. |
| Palo Alto Networks acquisition of CyberArk missing | **NOT RE-TESTED this pass** — same vendor-layer scope exclusion. **Flag as outstanding-unverified.** |
| CPS234-§22 mapping defect (IGA) | **PARTIALLY-CLOSED / REGRESSED-IN-SIBLING** — IGA trace fixed (§22 merged into §21, correct quote), but IGA `use-cases.csv:9-11` still prints `CPS234-§22` for UC-I-008/009/010 (**IGA-F1, HIGH**), and the **same class re-appeared in PAM** `regulatory-trace.csv:24` (**REG-F1, HIGH**). |

> **Buyer caution:** the two vendor-acquisition CRITICALs from 2026-06-11 were **not in scope of this re-run** and have **not been re-verified closed**. Do not treat their absence from this report as closure.

---

## 3. 20-Dimension Scorecard

Bands: 0 Absent · 1 Emerging · 2 Sound · 3 Strong. Dimensions not exercised by this agentic+remediation-focused pass are marked **deferred (later pass)**.

| # | Dimension | Lens | Band | Confidence | Evidence |
|---|---|---|---|---|---|
| A1 | Construct validity | A | — | — | deferred (later pass) |
| A2 | Content coverage | A | **3** | HIGH | 9 agentic UCs span issuance/rotation/revocation (secrets), brokered-session/JIT-ZSP/anomaly (PAM), orphan-agent/consent-revocation (IGA); 5 sub-classes mapped to SPN anchors (`AGENTIC-RESEARCH.md`). |
| A3 | Reliability / inter-rater | A | — | — | deferred (later pass) |
| A4 | Scoring discrimination / sensitivity | A | **2–3** | HIGH/MED | Output-correctness lens: **3** — hand re-derivation of secrets board matches engine + HTML exactly; band thresholds correct at all boundaries (`report_logic.py:268-274`); P0 consequence-weighting applied. Agentic-regression lens: **2** (MED) — roll-up + priority_fi now exist but GAP-floor gating / priority weighting not re-verified in `scoring.ts`. **Reconciled: 2 (Sound), trending 3.** |
| A6 | Calibration to ground truth | A | **1** | HIGH | Agentic calibration remains internal/synthetic; no agent-incident back-test (AG-R-02). Honestly labelled. |
| B7 | Control-set canonicality (coverage) | B | **2–3** | HIGH | PAM: **3** — all 18 canonical controls incl. discrete SAW/PAW (UC-P-018), mainframe PID-018, backup/DR PID-017. Secrets: **2** — full lifecycle but agent-UC acceptance criteria thin on evidence (SEC-1/SEC-2). IGA: **2** — canonical lifecycle but held down by §22 mislabel reaching buyer HTML (IGA-F1). **Reconciled: 2 (Sound), PAM 3.** |
| B8 | Taxonomy / architecture currency | B | **3** | HIGH | Agentic-AI class first-class in all 3 domains + OAuth consent-grant (Midnight-Blizzard pattern); privileged-aware spine (`identity-spine.yaml:131-148`). The exact 2026-headline gap prior-scored Emerging(1), now comprehensively closed. |
| B9 | Threat-model grounding | B | **3** | HIGH | Structured ATT&CK technique IDs (T1078/T1098) + LLM06 on agentic privileged rows (`pam/regulatory-trace.csv:29-31`), verbatim + URLs. Slight ding: classic UCs (UC-P-016 PtH/Kerberoast/DCSync) carry techniques in prose only (PAM-SME-03). |
| B10 | Target-state / secretless currency | B | **3** | HIGH | SPN-016 good-state = zero-standing-privilege, broker-mediated JIT (`identity-spine.yaml:145`); PID-021 "(no standing privileged secret)"; continuous attestation modelled as agentic end-state (IGA). |
| C11 | Citation / control-ID soundness (anti-fabrication) | C | **2** | HIGH | Data-integrity lens: **3** — 4 allowlisted sentinel dangling keys, 0 orphan control_codes/204, 3/3 primary-source quotes faithful. Regulatory lens: **2** — residual right-ID-wrong-scope mappings survive (PAM §22 REG-F1, ISM-1404 drift REG-F3, IGA §22 IGA-F1). **Reconciled: 2 (Sound) — anti-fabrication *machinery* is Strong, but live mapping-scope defects in the regulator-facing surface cap the dimension at Sound.** |
| C12 | Evidence-model defensibility | C | — | — | deferred — note SEC-2: agentic current-state rows carry empty `evidence_q_ids` (`current-state.csv:49-51`), honestly tagged MEDIUM/GAP. |
| C13 | Bias / gaming resistance | C | — | — | deferred (later pass) |
| C14 | Framework-scope honesty | C | **3** | HIGH | Clean PRIMARY-LENS / BACK-MAP / THREAT-CONTEXT separation; APRA framed back-mapped not assessed-against; owasp-llm/MITRE excluded from compliance % (`secrets.yaml:65`). No logo-wall overreach. |
| C15 | Jurisdiction boundary honesty | C | **3** | MED | AU-only is a stated, locked decision; M3 work introduced no non-AU control claims; SOX/NIST/ISO appear only as BACK-MAP/INFORMATIVE. |
| D16–D18 | Commercial / vendor-fit / market | D | — | — | deferred (later pass) — note report_logic correctly refuses an empty agentic vendor-fit column (`test_agentic_area.py:18-19`). |
| D19 | Benchmarking | D | **2** | MED | Synthetic benchmark cohort + exec roll-up positioning now exist (`benchmark-cohort.json`), closing prior Emerging(1); honestly labelled SYNTHETIC / "not a peer comparison". Peer-position aspirational (M4). |
| D20 | Commercial defensibility | D | — | — | deferred (later pass) |

---

## 4. 2026-06-09 Original-Gap Regression

| # | Original gap (2026-06-09) | Status | Evidence |
|---|---|---|---|
| 1 | Agentic-AI / OAuth-consent **currency gap** (the #1 concern) | **CLOSED** | First-class agentic identity class in all 3 domains + OAuth consent-grant (IGID-013); privileged-aware spine SPN-015/016; 9 archetype-scored agentic UCs; structured ATT&CK grounding; verbatim-verified research base. B8/B9/B10 all band 3. |
| 2 | No **maturity roll-up** | **CLOSED** | `matrix/rollup.py` + `build_exec_rollup.py` compute ML1/2/3 overall band; secrets board re-derived by hand matches engine + HTML (A4). |
| 3 | Internal-vs-external **calibration** | **STILL-OPEN** | Calibration remains internal/synthetic; no agentic incident back-test; thresholds in archetype params not externally validated (AG-R-02, MED; A6 band 1). Honestly labelled. |
| 4 | No **benchmark** cohort | **PARTIALLY-CLOSED** | Synthetic cohort + benchmark.position now built (`benchmark-cohort.json`), but explicitly "not an external standard and not a peer comparison" — peer comparison deferred to M4 (D19 band 2). |

---

## 5. New / Remaining Findings by Severity

### CRITICAL
None. No CRITICAL finding survived adversarial verification this pass.

### HIGH

**IGA-F1 — IGA CPS234-§22 mislabel half-closed; wrong obligation reaches buyer HTML** *(pre-existing; remediation half-applied)*
- **Dim:** C11
- **Claim:** The §22 fix landed in `regulatory-trace.csv` but not in `use-cases.csv`, so `iga-report.html` still prints `CPS234-§22` against three SoD use cases with the wrong obligation.
- **Evidence:** `iga/regulatory-trace.csv:15` now carries §21 with correct ¶21 quote and lists UC-I-008/009/010 (no §22 row). But `iga/use-cases.csv:9-11` still carry `CPS234-§22` + `apra-cps-234-para22` for UC-I-008/009/010; `iga/iga-report.html:378` embeds these verbatim. Repo's own `secrets/regulatory-trace.csv:54` defines §22 = "Evaluate design of third-party controls" — wrong for SoD.
- **Framework:** APRA CPS 234 ¶22 (third-party control-design evaluation) vs ¶21; project's own right-ID-wrong-content fabrication class.
- **Recommendation:** In `use-cases.csv` replace `CPS234-§22`→`CPS234-§21` and `apra-cps-234-para22`→`apra-cps-234-para21` for UC-I-008/009/010, rebuild `iga-report.html`. Add validator cross-checking every `backmap_codes` CPS234-§N against a trace row covering that uc_id.

**REG-F1 — PAM CPS234-§22 maps third-party obligation to four internal UCs (same class re-appears in a sibling domain)** *(NEW instance of a known class)*
- **Dim:** C11
- **Claim:** CPS234-§22 (third-party control-design evaluation) is mapped to four purely-internal PAM UCs — the identical right-ID-wrong-scope defect fixed in IGA, now live in PAM.
- **Evidence:** `pam/regulatory-trace.csv:24` maps CPS234-§22 → UC-P-003 (session recording), UC-P-008 (break-glass), UC-P-015 (threat analytics), UC-P-016 (credential-theft detection); titles at `pam/use-cases.csv:4,9,16,17` are all internal controls. The §16 "assess third-party" row (`pam:20`) likewise maps non-third-party UC-P-005 discovery / UC-P-014 recertification.
- **Framework:** APRA CPS 234 ¶22; instrument's own anti-fabrication taxonomy (right-ID-wrong-content = fabrication-class).
- **Recommendation:** Re-map PAM §22 to genuine vendor/third-party privileged-access UCs, or move these internal UCs to §21. One-row class of fix, same as the IGA correction.

### MEDIUM

**PAM-SME-01 — REG-AGENTIC-01 half-applied: UC-P-019 backmap still tags ISM-1304, contradicting its own trace** *(remediation-introduced inconsistency)*
- **Dim:** B9 / C11
- **Claim:** UC-P-019's self-declared `backmap_codes` still tags ISM-1304, contradicting the authoritative trace which remapped UC-P-019 to ISM-1405 and stripped ISM-1304 of all agentic UCs. Stale tag is buyer-visible.
- **Evidence:** `pam/use-cases.csv:20` `backmap_codes = "CPS234-§21;ISM-1304;LLM06:2025"`; but `regulatory-trace.csv:4` ISM-1304 no longer lists UC-P-019, `:5` ISM-1405 now lists UC-P-019 + PID-021. `build_stakeholder_pack.py:143` renders `backmap_codes` into the XLSX, so the buyer sees UC-P-019 tagged ISM-1304 ("default user accounts/credentials for network/OT devices") — semantically wrong for agentic session brokering. `validate_data.py` cross-checks nothing (only header presence, line 33).
- **Framework:** C11 (highest-priority buyer check) + B9 grounding integrity.
- **Recommendation:** Change UC-P-019 `backmap_codes` to `CPS234-§21;ISM-1405;LLM06:2025`; add a validator rule cross-checking each UC's `backmap_codes` against the controls that list it in `regulatory-trace.csv`.

**REG-F2 — Semantic gate is structurally blind to UC-mapping scope** *(pre-existing structural gap; lets REG-F1/IGA-F1/PAM-SME-01 pass clean)*
- **Dim:** C11
- **Claim:** The H2 semantic-control gate verifies only that a control's title+quote match its registered topic (right-ID-wrong-TEXT), never that the mapped UCs/identities belong under that control. Hence REG-F1 passes "All CSV data contracts valid."
- **Evidence:** `validate_data.py:361-386` builds haystack from `control_short_title` + `evidence_quote` only; `control-semantics.yaml:86` registers §22 expect "evaluate design of third-party controls" which the row satisfies, so the wrong UC mapping is never gated.
- **Framework:** Methodology C11 — a mapping must be a genuine satisfies-relationship, not an aspirational stretch.
- **Recommendation:** Extend the gate with a UC/identity scope check for relationship-bearing controls (third-party controls require a UC tagged third-party/vendor), or add a reviewer-attestation column for §22/§16/§28/§34-class rows.

**REG-F3 — Secrets ISM-1404 title/scope drift; cross-domain inconsistency vs IGA** *(pre-existing)*
- **Dim:** C11
- **Claim:** Secrets ISM-1404 carries an editorialised title "Suspension of access… (credential revocation)" and maps to revocation UCs, but ISM-1404's actual control text (and its IGA use) is the 45-day unprivileged-inactivity disablement control.
- **Evidence:** `secrets/regulatory-trace.csv:108` title="Suspension of access…(credential revocation)", quote="…disabled after 45 days of inactivity", mapped UC-F-007/UC-N-011 (`secrets/use-cases.csv:7,11`). `iga:13` uses ISM-1404 correctly as 45-day inactivity disablement. Gate passes because expect-substring "45 days of inactivity" (`control-semantics.yaml:33`) is in the quote.
- **Framework:** ASD ISM-1404 is the 45-day inactivity disablement control; relabelling as "credential revocation" misrepresents the obligation.
- **Recommendation:** Restore ISM-1404 title to the 45-day inactivity meaning; re-map UC-F-007/UC-N-011 to a revocation-appropriate control. The secrets-vs-IGA inconsistency is itself a defensibility flag.

**F-03 — 37 of 199 "verbatim" quote rows contain internal ellipses** *(pre-existing)*
- **Dim:** C11
- **Claim:** Quote-label fidelity slightly overstated: 37/199 rows tagged `quote_type=verbatim` contain elisions (e.g. CPS234-§35). Meaning is preserved and elisions are visibly marked, but an elided excerpt is not character-for-character verbatim.
- **Evidence:** Independent scan of `*/regulatory-trace.csv`: 37/199 verbatim rows contain "…" (secrets §13/§20/§21/§28/§35/§36; CPS230 §15/§42). §35 elision faithful to apra.gov.au release text.
- **Recommendation:** Add a `verbatim-elided` quote_type (or column flag) so elided excerpts are distinguished. Low effort, raises defensibility.

**F-04 — Promised "H1d" verbatim-fidelity gate is unimplemented** *(pre-existing)*
- **Dim:** C11
- **Claim:** No stored source-text corpus exists and no function compares a verbatim quote to primary-source text; the only text gate is topic-level substring. So all 199 "verbatim" labels rest on manual analyst diligence, not an automated gate.
- **Evidence:** `validate_data.py:65` comments "verbatim rows are (later, H1d) held to source-quote presence/fidelity" but no H1d function exists; `check_control_semantics` (`:361`) only asserts a registered substring appears. No quote/source corpus under `matrix/config` or `meta/`.
- **Recommendation:** Either implement H1d against a small frozen source-quote fixture for the highest-stakes rows (APRA/E8/OWASP/ISM), or soften the line-65 comment to state fidelity is manually verified — so the code does not promise a gate it lacks.

**AG-R-02 — Agentic calibration still internal/synthetic** *(pre-existing; original gap #3)*
- **Dim:** A6
- **Claim:** No agentic verdict is back-tested against a real agent-compromise incident; archetype-param thresholds are unvalidated externally.
- **Evidence:** `matrix/rollup.py` consumes a synthetic cohort (`config/benchmark-cohort.json`); `AGENTIC-RESEARCH.md` verifies sources but not thresholds.
- **Recommendation:** Add even one agentic incident back-test or external-panel review before any "validated" claim in agentic collateral. Keep current honest "synthetic / not a peer comparison" labelling.

### LOW

| id | dim | claim | evidence (file:line) | recommendation | status |
|---|---|---|---|---|---|
| SEC-1 | B7 | UC-F-028/029/030 non-overlap with UC-F-018 is implicit, inviting "why two agent-broker UCs?" | `use-cases.csv:19` (UC-F-018) vs `:49` (UC-F-028) | Add a one-line relationship note (UC-F-028/029/030 decompose the lifecycle UC-F-018 frames). | pre-existing |
| SEC-2 | B7/C12 | Agent-UC current-state rows carry no evidence question-IDs | `current-state.csv:49-51` empty `evidence_q_ids`, [PUBLIC] | Attach ≥1 evidence-ID (even "not-yet-in-scope") on next pass. | pre-existing |
| SEC-3 | B8 | NHI-019 lists "static tool API keys" the agent UCs forbid; framing only | `identity-catalog.csv:20` vs UC-F-028 criteria | Annotate "(legacy/forbidden in new patterns)". | pre-existing |
| PAM-SME-02 | B7 | UC-P-019=A2 vs human analogue UC-P-002=A1 archetype asymmetry undocumented | `uc-archetype-map.csv` | One-line note: agent control assessed as migration off standing svc-accounts. | pre-existing |
| PAM-SME-03 | B9 | Classic UC-P-016 (PtH/Kerberoast/DCSync) names techniques in prose, no structured ATT&CK IDs | `use-cases.csv:17`, `regulatory-trace.csv:29-30` | Backfill T1550.002/T1558.003/T1003.006/T1528 to UC-P-015/016 trace rows. | pre-existing |
| IAM-F1 | B8 | SPN-016 span=1 (PAM-only) vs SPN-015 span=2 — could read as asymmetry | `cross-domain-report.html`; `identity-spine.yaml:145` | Do NOT fabricate a link; add a one-line "span=1 by-design" note. | pre-existing |
| IAM-F2 | B8 | SPN-015/016 carry empty archetype-level `citation_keys` | `identity-spine.yaml:139,148` | Optionally add csa-agentic-iam-2025;owasp-llm06-2025 to archetype rows. | pre-existing |
| IGA-F2 | C11 | No validator links `backmap_codes` to trace `control_codes` (the gap that let §22 half-apply) | `validate_data.py:33`; `citations.bib:4006` orphan para22 alias | Add backmap↔trace cross-check; retire orphaned `apra-cps-234-para22`. | pre-existing (structural) |
| F-01 | C11 | 4 dangling keys remain — all deliberate, allowlisted ISO sentinels | `validate_data.py:79-87`; `iga/regulatory-trace.csv:19-22` | No fix; optionally surface sentinel count to buyers. | pre-existing (non-defect) |
| F-02 | C11 | AG-01 fully closed; old key only an unused bib def | `citations.bib:30` | Optionally remove unused entry. | pre-existing (non-defect) |
| REG-F4 | C11 | Superseded csa-ai-agents-2024 still co-exists in bib + research notes | `citations.bib`; `research/*.md` | Annotate as superseded-by csa-agentic-iam-2025 or remove. | pre-existing |
| AG-R-01 | B8 | Two PRE-M3 agentic UCs cite owasp 2024 key while M3 UCs cite 2025 | `use-cases.csv:19,47` (2024) vs `:49-50` (2025) | Re-point UC-F-018/UC-N-019 to owasp-llm06-2025. | pre-existing |
| AG-R-03 | B8 | NIST AI RMF named in research base but wired into no UC/trace | `citations.bib:4164`; `AGENTIC-RESEARCH.md` | Cite on a relevant agentic UC or label informative-only. | pre-existing |
| OUT-01 | A4 | Secrets board all-ML1/0.0 — zero inter-group discrimination | `secrets-report.html` embedded JSON; PAM shows ML3/ML1 split | Correct behaviour (zero-MET fixture); add a "pre-implementation baseline" note. | pre-existing (non-defect) |
| OUT-02 | A4 | 18 of 50 secrets UCs are in no named board group | `report_logic.py:316-322`; `MATURITY_GROUPS['secrets']` (32 ids) | Add residual "Other" group or a footnote reconciling groups to headline. | pre-existing (intentional) |

---

## 6. Grades for the 6 User-Named Angles

| Angle | Grade | Basis |
|---|---|---|
| **Coding standards** | **B (spillover only; out of deep scope)** | Not a deep-reviewed axis this pass. Positive spillover: list-comprehension group construction avoids mutating `REC_UC_DOMAIN` (`report_logic.py:43-47`); data-driven exclude sets (`build_matrix_viewer.py:104-105`); enum/registry/semantic gates wired into `validate_all`. Negative spillover: validator checks `backmap_codes` presence but not consistency with the trace (`validate_data.py:33`) — the structural gap behind PAM-SME-01/IGA-F1; a comment promises an H1d gate that does not exist (F-04). |
| **Logic (scoring/output)** | **A− (out of deep scope; what surfaced is correct)** | Band logic correct at all boundaries (`report_logic.py:268-274`); P0 consequence-weighting genuinely applied; hand re-derivation of the secrets board matches engine + rendered HTML field-for-field; M3.2 double-count fix provably does not mutate `REC_UC_DOMAIN`. Minor: priority weighting acts on P0 only; GAP-floor gating in `scoring.ts` not re-verified this pass. |
| **PAM** | **A− (Strong coverage, one HIGH mapping defect)** | B7 band 3 (all 18 controls incl. discrete SAW/PAW, mainframe, backup/DR, agentic plane); B9 band 3 (structured ATT&CK on agentic rows). PAM-01/PAM-02 genuinely closed. Docked by **REG-F1 (HIGH** §22→internal UCs) and **PAM-SME-01 (MED** stale ISM-1304 backmap). |
| **IAM** | **A (cross-domain spine coherent and current)** | B8 band 3; agentic class first-class with privileged axis (SPN-015/016); IAM-01 enum gate real and fail-correct; npe_conformance taxonomically defensible; no dangling refs introduced. Only LOW nits (IAM-F1 span asymmetry by-design; IAM-F2 empty archetype citations). |
| **IGA** | **B+ (canonical control set, one HIGH display-layer defect)** | Agentic governance a genuine differentiator (A2/A5/A3 lifecycle, posture/vendor-fit decoupling correctly engineered); IAM-01 closed and semantically sound. Docked by **IGA-F1 (HIGH** §22 wrong obligation in regulator-facing HTML) + **IGA-F2** missing cross-check. |
| **Secrets management** | **A− (canonical and current; thin agentic evidence)** | Control set canonical and lifecycle-complete; B8 band 3 (NHI-019 + 2026-headline classes); AG-01/OC-01 closed with defence-in-depth. Docked by LOW items: REG-F3 ISM-1404 title drift, SEC-1/SEC-2 implicit UC boundary + empty agentic evidence-IDs, AG-R-01 mixed owasp citation years. |

---

## 7. Prioritised "Fix-Before-You-Sell-It" List

### MUST-FIX (conditions of purchase; block unconditional Buy)
1. **REG-F1 (HIGH)** — Re-map PAM `regulatory-trace.csv:24` CPS234-§22 off the four internal UCs onto genuine third-party/vendor privileged-access UCs (or §21). *(Also re-check the §16 row `pam:20`.)*
2. **IGA-F1 (HIGH)** — Fix IGA `use-cases.csv:9-11` `CPS234-§22`→`§21` and `apra-cps-234-para22`→`para21` for UC-I-008/009/010; rebuild `iga-report.html`.
3. **PAM-SME-01 (MED, but a MUST-FIX item)** — Correct UC-P-019 `backmap_codes` `ISM-1304`→`ISM-1405` in `pam/use-cases.csv:20` to finish REG-AGENTIC-01.
4. **IGA-F2 / REG-F2 (structural)** — Add the validator cross-check: every `backmap_codes` control must be covered by a `regulatory-trace.csv` row listing that uc_id, with a scope check for relationship-bearing (third-party) controls. This single gate stops items 1–3 from recurring and would have caught all three.
5. **Vendor-layer CRITICALs (carried, unverified)** — Before any vendor-facing sale, confirm the 2026-06-11 Entro/CyberArk false-acquisition and missing Palo Alto/CyberArk items are actually removed; **this re-run did not re-test them.**

### SHOULD
6. **REG-F3 (MED)** — Restore secrets ISM-1404 title to the 45-day inactivity meaning; re-map UC-F-007/UC-N-011 to a revocation-appropriate control (resolve the secrets-vs-IGA inconsistency).
7. **F-03 (MED)** — Introduce `verbatim-elided` quote_type for the 37 elided rows.
8. **F-04 (MED)** — Implement H1d against a frozen source-quote fixture for the highest-stakes rows, or soften the promising comment.
9. **AG-R-02 (MED)** — Add at least one agentic incident back-test / external-panel review before any "validated" claim; keep the honest synthetic labelling (calibration gap #3 remains open).

### COULD
10. **PAM-SME-03 (LOW)** — Backfill structured ATT&CK IDs (T1550.002/T1558.003/T1003.006/T1528) onto classic UC-P-015/016 trace rows.
11. **AG-R-01 / AG-R-03 / REG-F4 (LOW)** — Normalise agentic citation currency (re-point UC-F-018/UC-N-019 to owasp-llm06-2025; wire or label NIST AI RMF; annotate/remove superseded csa-ai-agents-2024).
12. **SEC-1/SEC-2/SEC-3, PAM-SME-02, IAM-F1/F2 (LOW)** — One-line provenance/relationship/by-design notes; attach agentic evidence-IDs; add archetype-level citations.
13. **OUT-01 / OUT-02 (LOW, non-defects)** — Add buyer-facing notes: secrets board is a pre-implementation baseline (0/50 MET, uniform ML1 expected); named groups are an illustrative subset of the 50-UC headline.

---

## 8. What This Pass Did NOT Cover

- **Lens A construct/reliability/calibration depth (A1, A3) and most of Lens D commercial (D16–D18, D20):** deferred to a later methodology pass; marked *deferred* in the scorecard.
- **Vendor-layer collateral:** the 2026-06-11 vendor-acquisition CRITICALs (Entro/CyberArk false acquisition; Palo Alto/CyberArk) were **outside this remediation+agentic remit and were not re-verified** — explicitly flagged as outstanding-unverified, not closed.
- **`scoring.ts` GAP-floor gating and priority weighting** were not re-traced end-to-end this pass (A4 held at Sound rather than Strong on that basis).
- **Verbatim character-level quote fidelity** was spot-checked on 3 primary sources (OWASP LLM06, Essential Eight, APRA CPS 234) only; there is no automated fidelity gate (F-04), so the remaining ~196 verbatim labels rest on manual diligence.
- **A live full rebuild / regression test suite run** beyond the validator (`validate_data.py` clean; 61 domain tests pass) — broader engineering CI, performance, and M4 productisation (peer benchmarking, external calibration, in-browser report generation) are out of scope for this defensibility re-run.

---

*Counts: 8 reviewers · 24 findings (2 HIGH, 6 MED, 16 LOW; 0 CRITICAL) · 2 HIGH adversarially verified, 0 dropped · remediation: 5 of 6 MUST-FIX CLOSED, 1 PARTIALLY-CLOSED.*

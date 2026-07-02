# Independent Buyer-Grade Defensibility Review — Posture-Assessment Instrument (DELTA RE-RUN)

**Date:** 2026-07-02
**Reviewer:** Independent buyer due-diligence reviewer (single-agent adversarial pass; all closure claims re-derived against live data and code, not commit messages)
**Methodology:** `/methodology/INSTRUMENT-REVIEW-METHODOLOGY.md` — 4 lenses × 20 dimensions, bands 0–3, per-verdict confidence tags, overcooked/undercooked read, verdict Buy / Buy-with-conditions / Not-yet
**Scope:** DELTA re-run against `meta/independent-review-2026-06-15-rerun.md` (prior verdict: **Buy-with-conditions**). Focus: are the conditions that blocked an unconditional Buy now closed? Unchanged dimensions carry forward with a `carried` marker.
**Commits reviewed:** worktree `wave0-validator-hardening` HEAD = `c169cc4` *(fix(validator): multi-domain default gate + H4 confidence + regression pins)*, on top of merge `9862796` (PR #39), whose in-branch tail contains the condition fixes `0d3ddfe` *(close REG-F1/IGA-F1/REG-F3 + structural gate)* and `5ca36c6` *(2 MED follow-ups: TST-01 negative test, SEC-REVERIFY-01 ISM-1404 evidence_url re-home)*. Delta surface since the 06-15-reviewed state: `matrix/validate_data.py`, `matrix/build_stakeholder_pack.py`, the domain CSVs touched by `0d3ddfe`, `tests/test_validate_data*.py`, both CI configs, regenerated stakeholder XLSX (verified via `git diff --name-only 9862796..HEAD` + PR #39 tail).
**Verification protocol:** Every condition was re-verified directly (CSV parses, code reads, live `validate_data.py` + full-pytest runs, XLSX zip inspection, rendered-HTML greps, one destructive fault-injection with byte-identical restore confirmed by `git diff --exit-code`). Historical defect states were reconstructed from `git show` at pre-fix commits to test whether the new gate would actually have caught them.

---

## 1. Bottom Line Up Front

**Overall verdict: BUY (unconditional).** Confidence: HIGH on condition closure; MED on the carried verbatim-fidelity axis.

All five conditions of purchase named by the 2026-06-15 re-run are **verified CLOSED in the data** — including the two vendor-layer CRITICALs that pass explicitly flagged as outstanding-unverified. The regulator-facing surface (all three domain trace files, both rendered HTML reports, the stakeholder XLSX) is clean of every defect instance the prior pass named, each closure is pinned by a dedicated regression test (48 pins pass; full suite 451/451), and the validator's bare CLI now gates **all three registered domains by default** — proven live by fault injection, not asserted.

One genuinely new finding survived this pass (NEW-01, MED): the "scope check for relationship-bearing controls" half of the prior MUST-FIX #4 was **not** implemented as a general validator rule, and I proved from the pre-fix git state that the forward gate that *was* implemented would **not** have caught the original REG-F1 (the defect was symmetric — both files agreed on the wrong scope). Protection against that specific class is regression-pins-only. However: a full live audit of every relationship-bearing control row (CPS234-§16/§22/§28/§34 + all CPS230 rows, all three domains) found **zero** wrong-scope mappings today, and the two historical instances are individually pinned. That makes NEW-01 a *forward-maintenance* risk on a currently-clean surface — a SHOULD, not a condition of purchase, by the methodology's own banding ("Sound: I'd buy it and note the caveats").

The remaining opens (F-04 fidelity gate, A6 synthetic calibration, a handful of LOWs) were SHOULD-not-MUST in the prior review's own framing, are honestly labelled in the artifacts, and none rose to a condition under re-examination.

### Verdict trajectory

| Pass | Verdict | Driver |
|---|---|---|
| 2026-06-09 | Buy-with-conditions | Agentic currency gap, no roll-up, no benchmark, internal calibration |
| 2026-06-15 AM | Buy-with-conditions | 6 MUST-FIX list issued |
| 2026-06-15 re-run | Buy-with-conditions | 2 partial remediations + PAM §22 regression + vendor CRITICALs unverified |
| **2026-07-02 (this delta)** | **Buy** | All 5 named conditions verified closed in data + pinned; residuals are SHOULD-class |

---

## 2. Per-Condition Verification Table

Every row below was verified by this reviewer in the worktree; evidence is file:line or command output.

| # | Condition (from 06-15 MUST-FIX) | Verdict | Evidence |
|---|---|---|---|
| 1 | **REG-F1** — PAM CPS234-§22 must map only third-party UC(s) | **CLOSED** (HIGH) | `matrix/domains/pam/regulatory-trace.csv:24` — §22 row `uc_ids = UC-P-011` only; UC-P-011 = "Privileged remote / third-party vendor access" (`pam/use-cases.csv:12`). The §16 row the prior review said to re-check (`regulatory-trace.csv:20`) is likewise UC-P-011-only. Identity list (PID-008/009/015/017) mirrors UC-P-011's own `nhis_in_scope` (vendor paths into network/hypervisor/backup layers + the vendor account itself) — consistent, not scope inflation. Rendered `pam-report.html`: §22 appears only in UC-P-011's backmap, UC-P-011's per-UC map, and the §22 trace entry (3 hits, all correct). Pin: `tests/test_validate_data_domains.py:256` asserts `ucs == {"UC-P-011"}`. |
| 2 | **IGA-F1** — zero §22 residue in IGA use-cases, trace, rendered HTML | **CLOSED** (HIGH) | `grep '§22\|para22'` over `iga/use-cases.csv`, `iga/regulatory-trace.csv`, `iga/iga-report.html` → **0 hits** in all three; HTML carries §21 ×48 (UC-I-008/009/010 re-homed). Pin: `test_iga_has_no_cps234_s22_residue` (`:266`) covers BOTH files. |
| 3 | **PAM-SME-01** — UC-P-019 backmap = ISM-1405, no ISM-1304; XLSX rebuilt from live data | **CLOSED** (HIGH) | Parsed `pam/use-cases.csv`: UC-P-019 `backmap_codes = CPS234-§21;ISM-1405;LLM06:2025` — ISM-1304 absent. Trace: ISM-1405 lists UC-P-019; ISM-1304 lists 12 UCs, none agentic; backmap↔trace sets match exactly for both codes. `pam-report.html` embedded JSON: `"UC-P-019": {"APRA": ["CPS234-§21"], "ISM": ["ISM-1405"]}` — clean. XLSX: `stakeholder/Secrets-Mgmt-Stakeholder-Pack-2026-06-03.xlsx` regenerated at `c169cc4` (binary 54274→55367 B; sheet counts now computed from live data — "Use Cases (50)", was hardcoded 47); zip-level grep of all sheet XML: no `ISM-1304;LLM06` string, no `para22`, and no UC-P rows at all. **Correction to the prior review:** the pack is secrets-only (`build_stakeholder_pack.py:17` hardwires the secrets dir); UC-P-019's stale tag never reached this XLSX — its buyer surface was `pam-report.html`, which is now clean. Closure status unaffected. Pin: `test_ucp019_backmap_is_ism_1405_not_1304` (`:273`). |
| 4 | **Structural gate** — (a) backmap↔trace consistency wired; (b) bare CLI validates ALL domains; (c) ownership edges need source_url + confidence | **CLOSED with residue → NEW-01** (HIGH) | (a) `check_backmap_trace_consistency` at `validate_data.py:339-367`, wired into `validate_all` at `:759`. (b) `main()` at `:810-836`: no `--data-dir` ⇒ iterates `iter_domain_data_dirs`, aggregates violations with `[slug]` prefix, never short-circuits; 3 domains registered (`matrix/config/domains/{secrets,pam,iga}.yaml`); both CIs run the bare call (`.github/workflows/ci.yml:27`, `.gitlab-ci.yml:21`). (c) `check_ownership_sources` at `:458-481`: dated acquisition edges MUST carry http(s) `source_url` AND closed-vocabulary HIGH/MEDIUM/LOW `confidence`; wired at `:771`. **Live run:** `python3 matrix/validate_data.py` → "All CSV data contracts valid.", exit 0. **Fault injection:** reverting UC-P-019's backmap to ISM-1304 in `pam/use-cases.csv` → `[pam] use-cases.csv: backmap_codes 'ISM-1304' (uc UC-P-019) is not mapped to UC-P-019 in regulatory-trace.csv — stale or mis-scoped control`, exit 1; restored, `git diff --exit-code` clean, re-run exit 0. **Residue:** the recommended *semantic scope check* for relationship-bearing controls was not implemented — see NEW-01 (§5). |
| 5 | **Vendor CRITICALs** (carried unverified from 06-15) — no Entro acquisition edge; CyberArk → Palo Alto Networks with primary sources | **CLOSED** (HIGH) | `matrix/config/vendor-ownership.yaml`: no `entro` key exists (Entro appears only in the header comment explaining the historical error; unlisted vendors are their own parent). `cyberark:` block (`:46-59`): `parent: palo-alto-networks`, `as_of: 2026-02-11`, `confidence: HIGH`, `source_url` = paloaltonetworks.com press release + PANW SEC 8-K noted. Pins: `tests/test_resilience_integration.py:23` (all CyberArk brands multi-hop to palo-alto-networks; `parent_of("entro-security") == "entro-security"` — the refuted-acquisition fix asserted by name) and `:36` (every acquisition edge carries provenance). |
| 6 | **Regression pins + suite** | **CLOSED** (HIGH) | `python3 -m pytest tests/test_validate_data_domains.py -q` → **48 passed**. Pins present for: PAM §22 third-party-only, IGA §22 zero-residue (both files), UC-P-019 ISM-1405-not-1304, the gate's negative case (`test_backmap_gate_catches_stale_control_scope`), multi-domain default CLI (`test_default_cli_run_covers_every_registered_domain`, `test_violation_in_non_secrets_domain_fails_default_run`). Full suite: `python3 -m pytest tests/ -q` → **451 passed**. |

---

## 3. Still-Open SHOULD Items — re-examined

| Item | Status this pass | Evidence | Rises to a condition? |
|---|---|---|---|
| **F-03** (37 elided "verbatim" rows) | **CLOSED** (not previously credited) | `VALID_QUOTE_TYPES` now includes `verbatim-elided` (`validate_data.py:74`); live counts: 162 `verbatim` / 37 `verbatim-elided` / 5 `analyst-note`; independent scan: **0** pure-`verbatim` rows contain `…`/`...` and **0** `verbatim-elided` rows lack one. Closed-set gate `check_quote_type` (`:289`) wired at `:735`. | — |
| **F-04** (verbatim-fidelity gate unimplemented) | **OPEN, honestly relabelled** | No fidelity/corpus gate exists (grep: only `:72-73`); the promising comment was softened to "Source-quote fidelity is currently verified by analyst diligence, not yet by an automated gate against a frozen source corpus" — the code no longer promises a gate it lacks (the prior review's accepted alternative remedy). The 162 verbatim labels still rest on manual diligence (3/3 prior spot-checks carried, MED confidence). | No — SHOULD, as framed on 06-15. Recommend the frozen-fixture variant for the ~20 highest-stakes APRA/ISM/E8/OWASP rows. |
| **A6 / AG-R-02** (calibration internal/synthetic) | **OPEN, honestly labelled** | `matrix/config/benchmark-cohort.json:2-3`: "illustrative synthetic baseline… Synthetic, designed-honest reference bands — NOT a measured cohort"; each band's `sources` self-declares "Synthetic estimate; calibrate against… when available". No agentic incident back-test. | No — disclosed limitation, not a defect. Blocks any *"validated"* marketing claim, which none of the artifacts make. |
| **LOW spot-checks (4 of 14)** | 1 closed, 3 open | **AG-R-01 CLOSED**: UC-F-018 and UC-N-019 now cite `owasp-llm06-2025` (parsed from `secrets/use-cases.csv`). **PAM-SME-03 OPEN**: no T1550.002/T1558.003/T1003.006/T1528 rows in `pam/regulatory-trace.csv` — classic UC-P-015/016 techniques still prose-only. **SEC-2 OPEN**: UC-F-028/029/030 `evidence_q_ids` still empty in `secrets/current-state.csv`. **REG-F4 partial**: no data CSV cites `csa-ai-agents-2024` or `apra-cps-234-para22`, but both linger as unannotated bib defs (`meta/citations.bib:30`, `:4007`). | No — cosmetic/roadmap; none reaches a verdict surface with wrong content. |

---

## 4. 20-Dimension Scorecard (delta; unchanged bands carried from 06-15 re-run)

| # | Dimension | Lens | Band | Confidence | Basis |
|---|---|---|---|---|---|
| A1 | Construct validity | A | — | — | carried (deferred; no engine/rubric change in delta surface) |
| A2 | Content coverage | A | **3** | HIGH | carried — no UC-set change in delta |
| A3 | Reliability / inter-rater | A | — | — | carried (deferred) |
| A4 | Scoring discrimination | A | **2** | HIGH/MED | carried — scoring engine untouched in delta; minor plus: XLSX counts now computed from live data (kills a hardcoded-47-vs-actual-50 drift, `c169cc4`) |
| A5 | Gaming / evidence-quality resistance | A | — | — | carried (deferred; note SEC-2 still open) |
| A6 | Calibration to ground truth | A | **1** | HIGH | carried — still internal/synthetic, still honestly labelled (§3) |
| B7 | PAM/control-set coverage | B | **2** | HIGH | carried overall; the IGA sub-score's §22-mislabel drag is gone (IGA-F1 closed), secrets still dinged by SEC-2 thin agentic evidence |
| B8 | NHI / taxonomy currency | B | **3** | HIGH | carried |
| B9 | Threat-model grounding | B | **3** | HIGH | carried — agentic rows structured; PAM-SME-03 (classic-UC ATT&CK backfill) verified still open, same "slight ding" as 06-15 |
| B10 | Target-state / secretless currency | B | **3** | HIGH | carried |
| C11 | Citation & control-ID soundness | C | **3** (was 2) | HIGH (mappings) / MED (verbatim fidelity, carried) | **CHANGED — rationale below** |
| C12 | Evidence-model defensibility | C | — | — | carried (deferred) |
| C13 | Override / confidence auditability | C | — | — | carried (deferred) |
| C14 | Framework-scope honesty | C | **3** | HIGH | carried — role separation intact; informative frameworks still excluded from compliance % |
| C15 | Jurisdiction boundary honesty | C | **3** | MED | carried |
| D16 | Proportionality | D | — | — | carried (deferred) |
| D17 | Actionability | D | — | — | carried (deferred) |
| D18 | Facilitator usability | D | — | — | carried (deferred) |
| D19 | Benchmarking | D | **2** | MED | carried — synthetic cohort, honest labels re-verified this pass |
| D20 | Independence / vendor-bias | D | **2** | HIGH | **CHANGED from deferred (partial):** the vendor-ownership layer — the only D20 axis this delta touches — is now verifiably honest: no fabricated Entro edge, PANW/CyberArk edge primary-sourced, provenance machine-enforced (`check_ownership_sources`) and test-pinned. Full D20 (recommendation SKU-neutrality etc.) remains deferred; band reflects the ownership axis only. |

**C11 rationale (2 → 3).** The 06-15 pass capped C11 at Sound *solely* because live right-ID-wrong-scope mappings survived in the regulator-facing surface (REG-F1, IGA-F1, PAM-SME-01, REG-F3). This pass verified all four closed in the data and rendered outputs, and independently audited **every** relationship-bearing control row (CPS234-§16/§22/§28/§34 + all CPS230 rows, three domains) — all genuinely scoped (secrets §22 → vendor-attestation / sovereignty / vendor-matrix / FAPI-partner / OAuth-marketplace UCs; PAM §16/§22 → UC-P-011 only; CPS230-§25/§42 quotes read and mappings judged defensible). REG-F3 also verified closed: ISM-1404 titled "Unprivileged inactive-account disablement at 45 days" in BOTH secrets (`regulatory-trace.csv:108`, now mapped to UC-F-027) and IGA (`:13`) — the cross-domain inconsistency is gone, and `5ca36c6` re-homed its evidence_url to the authoritative Personnel Security guideline. The anti-fabrication machinery is now four-layer (control-ID registry, semantic topic gate, backmap↔trace gate, quote-type closed set) plus instance pins. The dimension's question — *will these control mappings survive a regulator?* — is answered yes for the artifact as it stands; the residual risks (NEW-01 scope-gate gap, F-04 manual fidelity) are drift/maintenance risks, recorded as SHOULDs, not defects in the shipped mappings.

---

## 5. New Findings (this pass)

### MEDIUM

**NEW-01 — The "scope check for relationship-bearing controls" half of MUST-FIX #4 was not implemented; the forward gate is provably blind to the original REG-F1 class**
- **Dim:** C11 (drift protection)
- **Claim:** `check_backmap_trace_consistency` only verifies backmap→trace agreement. I reconstructed the pre-fix state (`git show 2488442`): the defective PAM §22 mapping was **symmetric** — the trace row listed UC-P-003/008/015/016 *and* those four UCs backmapped §22 — so the new gate would have passed it clean. The prior review's assertion that this gate "would have caught all three" is therefore false for REG-F1 (true for IGA-F1 and PAM-SME-01, which were file-drift defects). The reverse direction cannot simply be gated: backmap is a curated highlight subset by design (measured asymmetry: 389/11/9 trace-listed-but-not-backmapped pairs in secrets/pam/iga). The only automated defense against a *new* agreed-but-wrong-scope mapping is the pair of instance pins (PAM §22, IGA §22) — a new wrong-scope row on §16/§28/§34, CPS230, or any future domain would pass validator + pins silently.
- **Why not a condition:** the live surface is audited clean this pass (zero wrong-scope rows across all relationship-bearing controls, three domains), the two historical instances are pinned, and the class that actually recurred twice (stale backmaps) *is* class-gated. This is prevention debt on a clean artifact.
- **Recommendation:** implement the 06-15 recommendation as specified — extend `control-semantics.yaml` (which already registers the third-party topic strings at `:83,:86,:98,:101`) with an optional `expect_uc_tag: third-party` per control, and have a gate require every mapped UC to carry that tag (UC-P-011, UC-N-006/007/014, UC-F-024/025 would seed the tag set). Half a day; converts pins-only protection to class protection.

### LOW

**NEW-02 — Prior-review provenance imprecision: UC-P-019's stale backmap never reached the stakeholder XLSX**
- The 06-15 review cited `build_stakeholder_pack.py:143` rendering UC-P-019's ISM-1304 into "the XLSX pack"; the pack is secrets-only (`build_stakeholder_pack.py:17`) and contains no UC-P rows (zip-verified). The actual buyer surface was `pam-report.html`. No closure impact — both surfaces are now clean — but the erratum matters for anyone tracing the finding history.

**NEW-03 — Orphan bib definitions linger (REG-F4/IGA-F2 tails)**
- `apra-cps-234-para22` (`meta/citations.bib:4007`) and `csa-ai-agents-2024` (`:30`) remain as unused, unannotated entries; no data CSV cites either. Cosmetic; annotate as retired/superseded or delete.

---

## 6. Overcooked / Undercooked Read

**Placement: sweet spot, unchanged — "engineering ahead of the surface," and the delta work was correctly aimed at the highest-consequence axis.** The Wave-0 hardening added rigor exactly where the instrument's own incident history demanded it (mapping integrity + multi-domain gating + provenance enforcement), at low run-cost (validator + 451 tests execute in ~2 s) — that is right-sized, not overcooked. The gate's docstrings even encode the incident history (`validate_data.py:339-350`), which is the kind of institutional memory a buyer pays for. **Undercooked spots persist and are known:** calibration is synthetic (A6=1), agentic current-state rows carry no evidence question-IDs (SEC-2), quote fidelity and relationship-scope correctness rest on manual diligence plus pins rather than class gates (F-04, NEW-01). None of these is disguised — every one is either labelled in the artifact or comment-disclosed in the code, which is the difference between undercooked-and-honest and false confidence.

---

## 7. Final Verdict

**BUY (unconditional).** Confidence: **HIGH** on the closure of all five 06-15 purchase conditions (each verified in data/code/output by this reviewer, each regression-pinned, gate behaviour proven by live fault injection); **MED** on the carried verbatim-fidelity axis (162 verbatim labels, 3 prior spot-checks, no automated gate).

No `Inadequate` (0) dimension exists on any exercised axis; no finding of this pass reaches the methodology's condition bar ("a buyer would make this a condition of purchase or it undermines a verdict's defensibility"). The verdicts the instrument currently produces are defensible to a regulator on the surfaces examined.

### Prioritised should-fix list (not conditions)

1. **NEW-01 (MED)** — semantic scope gate for relationship-bearing controls (`expect_uc_tag` in control-semantics + validator rule). Converts pins-only protection for the twice-recurred §22 class into class protection. ~0.5 day.
2. **F-04 (MED)** — frozen source-quote fixture for the ~20 highest-stakes APRA/ISM/E8/OWASP verbatim rows; lifts the C11 fidelity axis from manual-diligence to gated.
3. **AG-R-02 / A6 (MED)** — one agentic incident back-test or external panel before any "validated" claim; keep the honest synthetic labels.
4. **SEC-2 / PAM-SME-03 / NEW-03 (LOW)** — agentic evidence_q_ids; ATT&CK backfill on UC-P-015/016; retire the two orphan bib defs.

*Counts: 6 conditions re-verified (6 CLOSED, 1 with recorded residue) · 3 new findings (1 MED, 2 LOW) · 4 of 14 prior LOWs spot-checked (1 closed, 3 open) · F-03 found closed, uncredited · validator exit 0 across 3 domains · fault-injection fired and restored byte-identical · tests 48/48 pinned, 451/451 full.*

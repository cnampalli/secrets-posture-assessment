# Main-thread checkpoint 003

**Stopped:** 2026-05-24 (Sun AEST) — after final M3 reviewer pass.

**Reason:** Optional Sunday work path #1 (final M3 reviewer pass) from
checkpoint 002 is complete. PRD v0.1 package now has an independent gate
review covering Wave A + Wave B. Awaiting user decision on whether to
apply the reviewer's pre-Monday fixes (v0.1 is otherwise frozen).

**Budget snapshot at stop:**
- Daily session: fresh allocation (Sunday), reviewer dispatch ~187k
  agent tokens consumed for the one pass.
- Weekly cloud: was ~80-85% at start of today; this single Opus 4.7
  reviewer dispatch pushes toward the upper end of that band. Remaining
  Sunday options below are all low-cost (main-thread only).

---

## What happened this session

- Dispatched prompt 09 reviewer (general-purpose, Opus 4.7) on the full
  PRD v0.1 package: body + 6 ADRs + 4 appendices + matrix.md +
  anz-current-state-evidence.md (+ underlying CSVs for consistency
  checks).
- Output: `meta/review-M3-2026-05-24.md` (Sections A–G, ≤3,500 w).
- Logged in `meta/agents.md` (row #09, 2026-05-24 08:00 AEST).

---

## M3 review result

**Gate verdict: PASS-with-comments** — 0 BLOCK-level items.
**Sensitivity LEAKAGE: none.** All three M2 "top-3" fixes confirmed
landed (CSVs RFC-4180-clean / 0 malformed rows; no
`[USER-CONFIRMED EXPERIENCE]` tag; Fortanix HSM line paraphrased).

The defects are **cross-wave numeric/narrative drift** — none structural,
none a leak, but all "embarrassment-risk in front of an architect reader".

### 7 Section E recommended actions (ordered by severity)

| # | Action | File / loc | Effort | Pre-Mon? |
|---|---|---|---|---|
| 1 | PRD §9 NHI vendor-ranking **omits AKEYLESS (21 NATIVE = true #2)**; contradicts §11 F-V-3 + matrix.md §1. Insert AKEYLESS #2, re-rank below. | `PRD-FI-v0.1.md:436-442` | ~3 lines | **Yes** |
| 2 | App A §A.5 "45 of 47" stale → **47/47** PRIMARY-LENS; delete the UC-N-014/UC-N-015 "governance-only" exception (both carry a PRIMARY-LENS row). | `A-compliance-traceability.md:362-371` | ~1 para | **Yes** |
| 3 | Control-row count **146 → 145** (CSV authoritative). | `matrix/matrix.md:144`, `B-vendor-profiles-index.md:402` | ~2 edits | **Yes** |
| 4 | ADR-004 internal **18 → 19** vendor count. | `ADR-004:35, :47, :54` | ~3 edits | **Yes** |
| 5 | CPS 234 paragraph cite **§35 → §35(a)-(b)** to match PRD §14/ADR-003. | `A-compliance-traceability.md` §A.3.1 | ~1 edit | nice-to-have |
| 6 | Confirm closure of §17 **O13** — `research/vendors/` source profiles (M2 leak site) paraphrased before any share beyond stakeholder. | (verification, not edit) | — | before external share |
| 7 | Reconcile ADR-004 tier labels ("Emerging + PKI/MIM (5)") with PRD §5/App B two-tier split (3+2). | `ADR-004` | cosmetic | defer v1.0 |

Items 1–4 ≈ 12 line-edits total; reviewer recommends all four before
Monday's stakeholder review.

### 5 Section F open questions
- **F1 (net-new):** §9-ranking-vs-§11 framing — "AKEYLESS #2" must not read
  as "recommended" given its AU-residency disqualification.
- **F5 (net-new):** forward-dated vendor GA claims (Aembit "GA Apr 2026",
  Oasis "GA Nov 2025") acceptable as `[INDUSTRY-CONSENSUS]`?
- 3 overlap existing PRD §17: **O5** (per-pair scoring), **O8** (CSF 2.0
  deferral), **O13** (vendor-profile paraphrasing).

---

## DECISION RESOLVED — E-items 1–4 applied (2026-05-24)

User chose **(a) apply all 4 now**. Six edits applied across 5 files
(one extra straggler caught by the post-edit consistency sweep that the
reviewer had not flagged):

| E# | File | Edit | Verified |
|---|---|---|---|
| 1 | `PRD/PRD-FI-v0.1.md` §9 | Inserted AKEYLESS (21 NATIVE / 5 GAP) as #2; re-ranked Azure/GCP/AWS/Entro to 3/4/5/5; added "ranked by raw coverage, not a primary-use recommendation" note (also closes open-question F1). | grep ✓ |
| 2 | `PRD/appendices/A-compliance-traceability.md` §A.5 | "45 of 47" → "47 of 47 PRIMARY-LENS"; removed UC-N-014/UC-N-015 governance-only exception (both confirmed carrying a `ZT-Pillar-Governance` PRIMARY-LENS row via CSV grep — 2 rows each). | CSV-verified ✓ |
| 2b | `PRD/PRD-FI-v0.1.md` §5 (line 131) | **Straggler** — same "45 of 47" claim duplicated in body; → "all 47". (Reviewer flagged only App A.) | grep ✓ |
| 3 | `matrix/matrix.md:144` + `B-vendor-profiles-index.md:402` | "146 control rows" → "145" (CSV authoritative = 145 data rows, verified `tail -n +2 \| grep -c`). | CSV-verified ✓ |
| 4 | `PRD/adrs/ADR-004-vendor-shortlist.md` :35/:47/:54 | "18" → "19" (×3). Master CSV unique vendor count = 19, verified. | CSV-verified ✓ |

**No CSV files were edited** → `matrix-viewer.html` does NOT need
regeneration. Post-edit consistency sweep clean: no residual
`45 of 47` / `146` / `18-vendor` strings in `PRD/` or `matrix/`.

**Not applied (deliberate):**
- E#5 (CPS 234 §35 → §35(a)-(b)) — cosmetic, left for v1.0.
- E#6 (§17 O13 vendor-profile paraphrasing) — verification item, not a
  body edit; remains a pre-external-share gate.
- E#7 (ADR-004 tier-label reconcile) — cosmetic, v1.0.

---

## Stakeholder-readiness reframing — DONE (2026-05-24)

After the M3 fixes, the user raised four substantive concerns. Addressed
as a **Monday-ready reframing on the frozen v0.1 data** (reading-layer
only; CSV not re-scored). Decision record: [ADR-007](../PRD/adrs/ADR-007-reading-model-and-confidence.md).

| Concern | Fix |
|---|---|
| Category coupling (NHI-discovery + Fortanix scored beside true secrets managers) | **Three-layer stack model** (L0 substrate / L1 secrets-mgmt + PKI-MIM lane / L2 governance), **rank within layer**. Reframed PRD §9 + matrix.md §0/§1/§3 + Appendix B tier banners. Fortanix now reads as substrate (not "rank 19"); discovery `NATIVE` ≠ vault `NATIVE`. |
| Fact-check vs hype | **PRD §8.1 sourcing & confidence** — honest posture (existence=vendor-cited, maturity=analyst judgment not verified, rankings=synthesis), 4-value taxonomy, **forward-dated register** (Aembit/Oasis/Fortanix/Doppler), per-layer confidence. No new research. |
| Jargon | Viewer **jargon tooltips** (94 terms: 37 NHI + 47 UC + coverage + maturity) sourced from catalog CSVs; hover any code. |
| Interactive viewer params | Viewer **layer toggles** (L0/L1/L2) + **how-to-read panel**, on top of existing filters. Regenerated 1,596 rows; `node --check` OK; layer split verified (L0=84/L1=1092/L2=420). |

Files touched: PRD §9/§8.1/§20, matrix.md, Appendix B, ADR-007 (new),
ADR-006 (footnote→ADR-007), build_matrix_viewer.py + matrix-viewer.html,
README, CHANGELOG, agents.md. **No CSV re-scored.** Morning M3 numeric
fixes (AKEYLESS #2, 47/47, 145 rows, 19 vendors) remain intact.

**Deferred to v1.0** (now in scope per ADR-007): sub-typing `NATIVE`
(broker/discover/keyroot), independent web verification of maturity 3-4 +
forward-dated claims, per-cell confidence column.

## Stakeholder report + Fortanix demotion — DONE (2026-05-24 pm)

Two further stakeholder asks after the reframing:

1. **"Drop Fortanix — convince me otherwise."** Agreed it doesn't belong in
   the *ranking* (scoring an HSM on a secrets rubric is a category error),
   but argued against deleting it (it's the vault's trust-root + XYZ has a
   live SafeNet→Fortanix migration). **Resolution: demote, don't delete** —
   removed from the ranked set (**19 → 18 ranked vendors**); surfaced as a
   Layer-0 crypto-substrate **dependency callout** (PRD §9.x, matrix §1.x,
   App B §B.6); excluded from rankings/cards/dashboard/viewer; CSV keeps its
   84 rows as reference. Recorded in [ADR-007](../PRD/adrs/ADR-007-reading-model-and-confidence.md) §A.1.
2. **"The scrolling table is painful — make it task-first + a dashboard +
   tell me how to email it."** Rebuilt `matrix-viewer.html` (via
   `build_matrix_viewer.py`) into a **self-contained 4-view report**:
   - **XYZ posture dashboard** (landing): KPI tiles, 0/16/11/20 posture bar,
     clickable top-gaps + partials, Layer-0 dependency note.
   - **By use case**: pick a UC → decision card (best-fit vendors by layer +
     XYZ state/confidence/evidence + recommended action).
   - **By identity**: pick an NHI → vendor coverage by layer.
   - **Browse all**: 1,512-row table, layer toggles, 94-term jargon tooltips.
   - **Sharing**: emailable single offline file; README "Sharing" section
     added; INTERNAL banner; O2 internal-only caveat.

Validation: `node --check` + a DOM-shim execution (all views render, no
runtime errors; 18 vendors / 1,512 rows). **Still no live browser
click-through** (O15) — recommend the user opens the file once before Monday.

### Report UX round 2 (2026-05-24, later) — DONE

Acting on further stakeholder feedback:
- **Vendors as columns** in the decision cards (coverage/maturity grid per
  layer: Satisfies + Maturity rows) + a **one-line best-fit recommendation**
  — UC and NHI views.
- **APRA CPS 234 + ASD ISM controls** now shown per use case (joined from
  `regulatory-trace.csv`; all 47 UCs mapped) — auditor's-eye view.
- **"Mark as MET" override** on dashboard + UC card — stakeholder ticks the
  PARTIALs they consider met; posture recomputes live, persists in browser
  (localStorage), baseline preserved.
- **Browse-all fixes**: `MAT` → `Maturity`, horizontal-scroll wrapper +
  min-width (columns + last column now render), dropped redundant
  vendor_slug column.

Validated: `node --check` + DOM-shim run (all views, 0 runtime errors;
UC-F-001 = 13 L1 vendor columns; APRA/ISM/MET-toggle present; override
recomputes posture). Generator: `matrix/build_matrix_viewer.py`.

### Compliance-trace tab + send package (2026-05-24, later still) — DONE

- **5th report tab "Compliance trace"** — ported the cascade from
  `.planning/sketches/003-regulatory-drilldown/` (Variant B): Framework →
  Control → Use case → Vendor evidence, click left-to-right, defaults to
  APRA CPS 234. All 7 frameworks / 145 controls; vendor evidence excludes
  Fortanix (ADR-007); control state-dot = worst XYZ state across its UCs.
- **Send package** — `package.sh` builds `dist/XYZ-Secrets-Management-PRD-v0.1.zip`
  (440K): single-file `XYZ-Secrets-Report.html` + full PRD package +
  matrices + `STAKEHOLDER-START-HERE.md` cover. The report alone is also
  emailable as one offline file. README "Sharing" section + START-HERE
  explain it. INTERNAL / O2 internal-only.

Report now has **5 tabs**: XYZ posture · By use case · By identity ·
Compliance trace · Browse all. Validated (node --check + DOM-shim +
cascade drill simulation). Generator: `matrix/build_matrix_viewer.py`.

## Remaining optional paths

- **Live browser click-through** of `matrix/matrix-viewer.html` (O15) — all
  5 tabs: dashboard gap → decision card; tick a PARTIAL as MET; cascade a
  CPS 234 control → vendor evidence; scroll the Browse-all table.
- Re-run `./package.sh` after any change to refresh the zip.
- **Executive briefing** — `PRD/EXEC-BRIEFING-v0.1.md` (2-page companion).
- **External-safe report variant** (XYZ panels stripped) if O2 surface widens.

---

## How to resume (cold-start protocol)

1. Read this checkpoint.
2. Read `meta/review-M3-2026-05-24.md` (the new gate review).
3. Read `meta/_main-checkpoint-002.md` (prior end-state + full inventory).
4. If applying fixes: open `PRD/PRD-FI-v0.1.md` §9 first (E-item 1).
5. Apply the 70% rule + session-budget rule throughout.

---

## Memory pointers

Unchanged from checkpoint 002 — see
`/Users/cnampalli/.claude/projects/-Users-cnampalli-Desktop-Projects-DE-AI-Reports-research-papers/memory/MEMORY.md`.

---

Session pauses here. M3 review complete, E-items 1–4 applied + verified.
PRD v0.1 is stakeholder-ready for Monday 2026-05-25. Remaining optional
paths (exec briefing / viewer sanity check / distribution prep) available
on request.

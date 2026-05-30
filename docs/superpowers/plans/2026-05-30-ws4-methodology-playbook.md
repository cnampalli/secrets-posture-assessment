# WS-4 Slice 1 — Methodology Playbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the WS-4 methodology — two markdown documents (`methodology/PLAYBOOK.md` consultant operating manual, then `methodology/METHODOLOGY.md` client-facing) — plus ADR-012 and a backlog update.

**Architecture:** Two prose documents sharing one 6-stage engagement-lifecycle skeleton. The playbook is the internal runbook (procedure + tooling + XYZ worked-example callouts); the client-facing doc is a distilled, trust-oriented retelling stripped of internal mechanics. No code changes this slice. "Verification" replaces "tests": cross-reference integrity, worked-example fidelity to real assessment data, two-doc consistency, self-review.

**Tech Stack:** Markdown only. Verification via shell (`ls`, `grep`, `awk`) against the existing repo.

**Source-of-truth data (verified 2026-05-30 — cite these exactly, do not paraphrase):**
- XYZ assessment, 47 UCs: **0 MET / 16 PARTIAL / 11 GAP / 20 PENDING** (`matrix/anz-current-state.csv`, column 2).
- Seed findings: **UC-F-001** — secret push-protection not deployed in blocking mode across repos (A1, GAP, HIGH; 2019 red-team finding still open). **UC-N-001** — plaintext-secret-sprawl KPI dashboard not in operational use (A6, GAP, HIGH).
- Headline gap: absence of an NHI **inventory layer above the vault tier** (Vault Enterprise selected 2019 = capability exists; adoption/observability/ownership-attestation lag).
- WS-2 presets (real filenames): `matrix/config/presets/{baseline,financial,government,retail}.yaml`. Frameworks: `matrix/config/frameworks.yaml`. Residency: `matrix/config/vendor-residency.yaml`.
- WS-1 rubric files: `methodology/{assessment-archetypes.csv,archetype-questions.csv,uc-archetype-map.csv,bespoke-criteria.csv,RUBRIC.md,scoring.py}`. Archetypes A0–A8.
- WS-3 questionnaire: `questionnaire/questionnaire.html` (built artifact), `questionnaire/build_questionnaire.py`, exports `assessment-record.json` (schema `posture-assessment-record/v1`).
- Report adapter: `questionnaire/report_adapter.py` → `matrix/build_matrix_viewer.py --current-state <csv>` (flag at `build_matrix_viewer.py:41`).

**Branch:** `ws4-methodology-playbook` (already created; spec already committed at `962a0f4`).

---

### Task 1: PLAYBOOK.md — header, spine, and stages 1–3 (Scope, Collect, Score)

**Files:**
- Create: `methodology/PLAYBOOK.md`

- [ ] **Step 1: Write the document header and the 6-stage overview**

Create `methodology/PLAYBOOK.md` starting with:

```markdown
# Posture Assessment — Consultant Operating Manual (Playbook)

**Status:** Draft
**Date:** 2026-05-30
**Audience:** Internal — the consultant running an engagement.
**Companion (client-facing):** `methodology/METHODOLOGY.md`
**Builds on:** WS-1 rubric (`RUBRIC.md`), WS-2 regulatory overlay (`matrix/config/`), WS-3 questionnaire (`questionnaire/`), report adapter (ADR-011).

This is the repeatable procedure for running a posture-assessment engagement end-to-end
for any AU client in any industry. The GAP/PARTIAL findings it produces are the engagement
menu — the consulting wedge. The procedure below is client-agnostic; **worked-example
callouts** (marked `> **XYZ example**`) ground each stage in the real XYZ secrets-management
assessment.

## The engagement lifecycle (6 stages)

1. **Scope** — pick the regulatory overlay(s) for the client/industry.
2. **Collect evidence** — run the questionnaire instrument (facilitated).
3. **Score** — rubric-assisted state, assessor confirms/overrides with rationale + confidence.
4. **Report current state** — project answers into the matrix gap report.
5. **Build the remediation roadmap** — turn GAP/PARTIAL into the prioritised engagement menu.
6. **Re-assess** — annual baseline + event-triggered + per-finding re-test.

Each stage below: **Purpose → Procedure → Tooling → Outputs → XYZ example.**
```

- [ ] **Step 2: Write Stage 1 (Scope)**

Append a `## Stage 1 — Scope` section. Required content:
- **Purpose:** select the binding framework(s) so the assessment scopes to what the client must satisfy.
- **Procedure (numbered):** (1) identify the client's industry and binding obligations; (2) choose the matching preset — `financial.yaml` (FI / APRA), `government.yaml` (PSPF/ISM), `retail.yaml`, or `baseline.yaml`; (3) add 1–2 comparison overlays; (4) confirm Essential 8 + Privacy Act remain always-on AU baseline.
- **Tooling:** `matrix/config/presets/*.yaml`, `matrix/config/frameworks.yaml`; the build consumes the selection (WS-2).
- **Outputs:** the scoped framework set for the engagement.
- **XYZ example callout:** AU Tier-1 FI → `financial.yaml` preset (APRA CPS 234/230 + ASD ISM), Essential 8 baseline always-on.

- [ ] **Step 3: Write Stage 2 (Collect evidence)**

Append `## Stage 2 — Collect evidence`. Required content:
- **Purpose:** gather the evidence that answers each use-case's diagnostic questions.
- **Procedure:** (1) open `questionnaire/questionnaire.html` (self-contained, no server); (2) facilitate live with the client — consultant drives; (3) answer each UC's items; (4) autosave/export progress.
- **Tooling:** `questionnaire/questionnaire.html` (built by `questionnaire/build_questionnaire.py` from the WS-1 rubric).
- **Outputs:** answered items per use-case, held in the questionnaire's working state.
- **XYZ example callout:** 47 UCs walked through; seed findings UC-F-001 and UC-N-001 answered against the 2019 red-team evidence.

- [ ] **Step 4: Write Stage 3 (Score)**

Append `## Stage 3 — Score`. Required content:
- **Purpose:** convert answers into a defensible MET/PARTIAL/GAP/PENDING state per UC.
- **Procedure:** (1) the rubric proposes a state from answers using the archetype model (A0–A8); (2) the assessor confirms or **overrides** with **rationale + confidence**; (3) export `assessment-record.json` (schema `posture-assessment-record/v1`).
- **Tooling:** `methodology/RUBRIC.md`, `methodology/assessment-archetypes.csv`, `methodology/scoring.py`; the questionnaire's export.
- **Outputs:** `assessment-record.json` (per-UC `final_state` / `proposed_state` / `confidence` / `rationale`).
- **XYZ example callout:** rubric dogfood reproduced 46/47 frozen expert verdicts; one principled override (UC-N-012 PENDING→GAP) logged with rationale.

- [ ] **Step 5: Verify cross-references for stages 1–3**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
for f in matrix/config/presets/financial.yaml matrix/config/presets/government.yaml \
         matrix/config/presets/retail.yaml matrix/config/presets/baseline.yaml \
         matrix/config/frameworks.yaml questionnaire/questionnaire.html \
         questionnaire/build_questionnaire.py methodology/RUBRIC.md \
         methodology/assessment-archetypes.csv methodology/scoring.py; do
  test -f "$f" && echo "OK  $f" || echo "MISSING  $f"; done
```
Expected: every line prints `OK` (no `MISSING`). If any reference in the prose names a file not on disk, fix the prose.

- [ ] **Step 6: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add methodology/PLAYBOOK.md
git commit -m "docs(ws4): playbook header + lifecycle stages 1-3 (scope, collect, score)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: PLAYBOOK.md — stages 4–6 and the prioritisation method

**Files:**
- Modify: `methodology/PLAYBOOK.md`

- [ ] **Step 1: Write Stage 4 (Report current state)**

Append `## Stage 4 — Report current state`. Required content:
- **Purpose:** render the scored record as the client-readable gap report.
- **Procedure:** (1) project the record to the report CSV: `python3 -m questionnaire.report_adapter <record.json> -o current-state.csv`; (2) build the report scoped to current state: `python3 matrix/build_matrix_viewer.py --current-state current-state.csv`; (3) read off MET/PARTIAL/GAP/PENDING per UC.
- **Tooling:** `questionnaire/report_adapter.py`, `matrix/build_matrix_viewer.py` (`--current-state` flag).
- **Outputs:** the matrix gap report.
- **XYZ example callout:** of 47 UCs — **0 MET, 16 PARTIAL, 11 GAP, 20 PENDING**; headline gap = absent NHI inventory layer above the vault tier (Vault Enterprise selected 2019, adoption/attestation lag).

- [ ] **Step 2: Write Stage 5 (Build the remediation roadmap) with the full prioritisation method**

Append `## Stage 5 — Build the remediation roadmap`. Required content:
- **Purpose:** turn GAP/PARTIAL findings into a sequenced, defensible engagement menu.
- **Procedure — the prioritisation method:**
  - **Axis 1 — Risk/exposure → High / Med / Low.** Band from qualitative anchors: residual exposure, blast radius (NHIs/systems touched), whether it is an *active* exposure (e.g. plaintext secrets in repos = High). No numeric score.
  - **Axis 2 — Remediation effort → High / Med / Low.** Band from anchors: dependency depth (needs the inventory layer first?), org/process change vs pure config, existing-tooling coverage (Vault selected → lower).
  - **Quadrants:** Quick wins (High risk / Low effort); Major projects (High / High); Fill-ins (Low / Low); Hard slogs (Low / High).
  - **Regulatory tie-breaker/escalator:** a binding obligation (APRA CPS 234/230, ASD ISM, selected overlay) breaks ties between equal cells and can escalate risk one band up — **always logged with the control reference, never silent.**
  - **Dependency note:** each row records sequencing constraints (e.g. inventory layer before ownership-attestation) so the roadmap is buildable.
- **Engagement-menu row shape (show as a literal code block in the doc):**
  ```
  UC-id · state · risk band · effort band · quadrant · regulatory driver · dependency · proposed engagement
  ```
- **Outputs:** the prioritised engagement menu (the wedge).
- **XYZ example callout:** walk UC-F-001 (push-protection, active plaintext-secret exposure → High risk; deployable as blocking-mode config on existing repos → Low effort → **Quick win**) and UC-N-001 (secret-sprawl KPI dashboard → High risk; depends on the inventory layer → High effort → **Major project**, dependency: inventory layer first).
- **Note in the doc:** this stage *documents* the method; the generator that auto-emits the menu from `assessment-record.json` is a later WS-4 slice.

- [ ] **Step 3: Write Stage 6 (Re-assess)**

Append `## Stage 6 — Re-assess`. Required content:
- **Purpose:** keep the posture current and measure remediation progress.
- **Procedure / cadence:** (1) **annual baseline** re-assessment; (2) **event-triggered** re-assessment on post-incident, major architecture change, or new regulatory obligation; (3) **per-finding re-test** after each remediation closes, to confirm the state moved (e.g. GAP→PARTIAL→MET).
- **Outputs:** cadence schedule + assessment deltas between runs.
- **XYZ example callout:** UC-F-001 re-tested after push-protection rollout to confirm GAP→MET.

- [ ] **Step 4: Verify Stage 4–6 references and worked-example fidelity**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
# tooling references exist
for f in questionnaire/report_adapter.py matrix/build_matrix_viewer.py; do
  test -f "$f" && echo "OK  $f" || echo "MISSING  $f"; done
# the --current-state flag exists
grep -q -- "--current-state" matrix/build_matrix_viewer.py && echo "OK  flag" || echo "MISSING flag"
# the cited XYZ counts match the real data
tail -n +2 matrix/anz-current-state.csv | awk -F',' '{print $2}' | sort | uniq -c
# the doc must state 16 PARTIAL / 11 GAP / 20 PENDING / 0 MET — confirm against the line above
grep -E "16 PARTIAL|11 GAP|20 PENDING|0 MET|0 .*MET" methodology/PLAYBOOK.md
```
Expected: `OK` lines; the `uniq -c` shows `11 GAP / 16 PARTIAL / 20 PENDING`; the doc's stated counts match. Fix any mismatch.

- [ ] **Step 5: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add methodology/PLAYBOOK.md
git commit -m "docs(ws4): playbook stages 4-6 + risk x effort prioritisation method

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: METHODOLOGY.md — the client-facing document

**Files:**
- Create: `methodology/METHODOLOGY.md`

- [ ] **Step 1: Write the client-facing doc from the shared 6-stage skeleton**

Create `methodology/METHODOLOGY.md`. It MUST reuse the identical 6-stage skeleton (Scope → Collect evidence → Score → Report current state → Build the remediation roadmap → Re-assess) but retell each stage for a buyer/exec. Header:

```markdown
# Posture Assessment — Methodology

**Status:** Draft
**Date:** 2026-05-30
**Audience:** Client — buyer / executive sponsor.
**Internal companion:** `methodology/PLAYBOOK.md`

Our posture assessment measures how well your organisation governs its machine identities
against the frameworks that bind you, and hands you a prioritised, defensible remediation
roadmap. The method is the same for every engagement; what changes is your evidence.
```

Then a `## What the method does` paragraph and one short subsection per stage. For each stage, state: **what we do** and **what you receive** — NOT the tooling commands or file paths. Required mappings:
- **Scope** → "we scope the assessment to the frameworks that bind your industry, plus comparison overlays." Receive: the scoped framework set.
- **Collect evidence** → "we facilitate a structured evidence-gathering session." Receive: a complete evidence record.
- **Score** → "each use-case is scored against a published rubric; our assessor confirms or overrides with documented rationale and a confidence level." Receive: a transparent, defensible scorecard.
- **Report current state** → "you receive a gap report across all use-cases (Met / Partial / Gap / Pending)." Receive: the current-state report.
- **Build the remediation roadmap** → "gaps become a prioritised engagement menu using a risk-versus-effort model, with regulatory obligations escalating priority." Receive: a sequenced remediation roadmap.
- **Re-assess** → "we re-assess annually, on significant change, and after each remediation." Receive: measured progress over time.

- [ ] **Step 2: Write the closing value framing (honest, no invented numbers)**

Append `## The value` section. Frame value as **cost-avoidance and exposure-reduction** (reduced likelihood/impact of credential exposure; audit-readiness against APRA/ISM/Essential 8). **Do NOT state any ROI percentages, dollar figures, or invented metrics.** Plain English only.

- [ ] **Step 3: Verify two-doc consistency, no internal mechanics, no invented numbers**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
# Both docs must contain all six stage names
for stage in "Scope" "Collect evidence" "Score" "Report current state" "remediation roadmap" "Re-assess"; do
  p=$(grep -c "$stage" methodology/PLAYBOOK.md); m=$(grep -c "$stage" methodology/METHODOLOGY.md)
  echo "stage='$stage' playbook=$p client=$m"; done
# Client doc must NOT leak internal mechanics: no file paths / CLI commands
grep -nE "python3|\.py|\.yaml|\.csv|\.html|--current-state|report_adapter|build_matrix_viewer" methodology/METHODOLOGY.md && echo "LEAK FOUND — remove" || echo "OK no internal mechanics"
# Client doc must NOT contain invented numbers (ROI %, $). Manual eyeball of any digit hits:
grep -nE "[0-9]+%|\\\$[0-9]|ROI" methodology/METHODOLOGY.md && echo "REVIEW numeric claims" || echo "OK no numeric claims"
```
Expected: every stage has `playbook>=1` and `client>=1`; `OK no internal mechanics`; `OK no numeric claims` (or, if any digit appears, confirm it is not an invented ROI/$ claim). Fix any leak or invented number.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add methodology/METHODOLOGY.md
git commit -m "docs(ws4): client-facing methodology doc (distilled from playbook)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: ADR-012 + backlog update + final self-review

**Files:**
- Create: `docs/adr/ADR-012-methodology-playbook.md`
- Modify: `meta/IMPROVEMENT-BACKLOG.md` (WS-4 section, lines ~94–100)

- [ ] **Step 1: Write ADR-012**

Create `docs/adr/ADR-012-methodology-playbook.md` following the style of `docs/adr/ADR-011-report-adapter.md`. Required content:
- **Status:** Accepted. **Date:** 2026-05-30.
- **Context:** WS-4 needs a repeatable written methodology so the assessment engagement (and its GAP/PARTIAL engagement menu — the wedge) is reproducible across clients, not ad-hoc.
- **Decision:** Two separate markdown docs in `methodology/` — `PLAYBOOK.md` (internal operating manual) and `METHODOLOGY.md` (client-facing) — sharing one 6-stage lifecycle skeleton. Prioritisation uses **risk × effort quadrants with regulation as tie-breaker/escalator**, qualitative bands (no invented numbers). Client-agnostic spine with XYZ worked-example callouts.
- **Alternatives rejected:** single layered doc (two audiences blur); single-source-generated views (premature machinery, YAGNI); client-facing HTML deck this slice (conflates runbook with presentation — deferred).
- **Consequences:** the roadmap *generator* and exec-summary print view remain later WS-4 slices; the prioritisation method is documented but not yet code.

- [ ] **Step 2: Update the backlog WS-4 section**

In `meta/IMPROVEMENT-BACKLOG.md`, under `### WS-4 — End-to-end process doc (playbook)`, mark slice 1 done. Change the heading to note progress and annotate the bullets, mirroring how WS-1/2/3 were marked. Add:
```
### WS-4 — End-to-end process doc (playbook) — **the consulting product** — ✅ DONE slice 1 (2026-05-30, branch ws4-methodology-playbook)

Delivered (slice 1): two methodology docs in `methodology/` — `PLAYBOOK.md` (consultant
operating manual: 6-stage lifecycle, risk×effort prioritisation, XYZ worked-example callouts)
and `METHODOLOGY.md` (client-facing, distilled). ADR-012. **Deferred:** the roadmap generator
(auto-emit the engagement menu from assessment-record.json) and the exec-summary print view.
```
Keep the original bullet list beneath it.

- [ ] **Step 3: Final self-review across all artifacts**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
# No placeholders anywhere in the new docs
grep -nE "TBD|TODO|FIXME|XXX|fill in|placeholder" methodology/PLAYBOOK.md methodology/METHODOLOGY.md docs/adr/ADR-012-methodology-playbook.md && echo "PLACEHOLDER FOUND" || echo "OK no placeholders"
# ADR sits in the right sequence
ls docs/adr/ADR-0{09,10,11,12}-*.md
# Backlog marks WS-4 slice 1
grep -n "WS-4" meta/IMPROVEMENT-BACKLOG.md | head
```
Expected: `OK no placeholders`; all four ADRs listed; WS-4 line shows the slice-1 done marker. Fix anything that fails.

- [ ] **Step 4: Commit**

```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers
git add docs/adr/ADR-012-methodology-playbook.md meta/IMPROVEMENT-BACKLOG.md
git commit -m "docs(ws4): ADR-012 + mark methodology playbook slice 1 done in backlog

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria (whole slice)

- `methodology/PLAYBOOK.md` exists: 6-stage lifecycle, full risk×effort prioritisation method, XYZ callouts with figures matching `matrix/anz-current-state.csv` (0/16/11/20).
- `methodology/METHODOLOGY.md` exists: same 6-stage skeleton, no internal mechanics, no invented numbers.
- `docs/adr/ADR-012-methodology-playbook.md` records the decision.
- `meta/IMPROVEMENT-BACKLOG.md` marks WS-4 slice 1 done.
- All four verification gates pass; four atomic commits on `ws4-methodology-playbook`.
- No code changed (generator + print view are later slices).

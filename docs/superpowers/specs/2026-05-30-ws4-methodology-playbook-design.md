# WS-4 Slice 1 — Methodology Playbook (Design Spec)

**Status:** Approved (brainstorming, 2026-05-30)
**Workstream:** WS-4 — End-to-end process doc (the consulting product)
**Slice:** 1 of N — the written methodology, two documents
**Builds on:** WS-1 rubric (archetypes A0–A8), WS-2 regulatory overlay, WS-3 questionnaire instrument, report adapter (ADR-011)
**Defers to later WS-4 slices:** the roadmap *generator* (auto-emits the engagement menu from `assessment-record.json`), the exec-summary print view.

---

## 1. Goal

Produce the **written methodology** that turns the reusable assessment instrument into a
repeatable consulting engagement. The GAP/PARTIAL/PENDING findings are the engagement
menu — the recurring-revenue wedge — so the methodology must make *producing that menu*
repeatable rather than ad-hoc.

This slice delivers **two separate documents**, sequenced:

1. **`methodology/PLAYBOOK.md`** — the consultant operating manual (internal runbook). Built first.
2. **`methodology/METHODOLOGY.md`** — the client-facing methodology (trust artifact), derived from the playbook. Built second.

Not one layered doc — two audiences, two files, sharing one skeleton.

## 2. Locked decisions (brainstorming, 2026-05-30)

| # | Decision | Outcome |
|---|----------|---------|
| 1 | Heart of this slice | The **written methodology playbook** (prose). Generator + print view = later slices. |
| 2 | Audience | **Operating manual first, then a separate client-facing doc.** Not layered into one file. |
| 3 | Prioritisation model | **Risk × effort quadrants, regulation as tie-breaker/escalator.** Qualitative bands, no invented numbers. |
| 4 | Worked example | **Client-agnostic spine + real XYZ worked-example callouts** at each stage. |
| 5 | Structure approach | **Two markdown docs in `methodology/`** (Approach A). Rejected: single-source-generated (premature), HTML deck this slice (conflates runbook with presentation). |

## 3. Document A — `methodology/PLAYBOOK.md` (operating manual)

### 3.1 Spine: the 6-stage engagement lifecycle

Each stage is written as: **purpose → procedure (numbered steps) → tooling it uses →
outputs → XYZ worked-example callout** (clearly marked, so the spine stays client-agnostic).

1. **Scope** — select the regulatory overlay(s) for the client/industry using the WS-2
   presets (financial / government / retail / baseline) plus 1–2 comparison overlays.
   Essential 8 + Privacy Act stay always-on AU baseline. *Output:* scoped framework set.
2. **Collect evidence** — run the WS-3 questionnaire instrument; facilitated-primary
   (consultant drives it live). *Output:* answered items per use-case.
3. **Score** — rubric-assisted state from answers (WS-1 archetypes A0–A8) → assessor
   confirms or overrides with **rationale + confidence**. *Output:* `assessment-record.json`.
4. **Report current state** — project the record into the matrix report
   (`questionnaire/report_adapter.py` → `matrix/build_matrix_viewer.py --current-state`).
   *Output:* the gap report (MET / PARTIAL / GAP / PENDING per UC).
5. **Build the remediation roadmap** — turn GAP/PARTIAL findings into the prioritised
   engagement menu via the risk × effort method (§3.2). *Output:* the engagement menu (the wedge).
6. **Re-assess** — cadence: **annual baseline + event-triggered** (post-incident, major
   architecture change, new regulatory obligation) **+ per-finding re-test after
   remediation**. *Output:* cadence schedule + assessment deltas.

### 3.2 The prioritisation method (how findings become the engagement menu)

A repeatable, no-invented-numbers procedure:

- **Axis 1 — Risk/exposure** → **High / Med / Low**, banded from qualitative anchors the
  rubric already surfaces: residual exposure, blast radius (how many NHIs/systems the gap
  touches), and whether it is an *active* exposure (e.g. plaintext secrets in repos = High).
  No numeric score — band by stated criteria.
- **Axis 2 — Remediation effort** → **High / Med / Low**, banded from anchors: dependency
  depth (does it need the inventory layer built first?), org/process change vs pure config,
  and whether existing tooling already covers it (Vault Enterprise selected → lower effort).
- **Quadrant placement:**
  - **Quick wins** — High risk / Low effort
  - **Major projects** — High risk / High effort
  - **Fill-ins** — Low risk / Low effort
  - **Hard slogs** — Low risk / High effort
- **Regulatory tie-breaker / escalator** — a binding obligation (APRA CPS 234/230, ASD ISM,
  the selected overlay) breaks ties between equal cells *and* can escalate a finding's risk
  band up one level. Always logged explicitly with the control reference — never silent.
- **Dependency note** — each menu row records sequencing constraints (e.g. inventory layer
  before ownership-attestation) so the roadmap is buildable, not merely ranked.

**Engagement-menu row shape:**

```
UC-id · state · risk band · effort band · quadrant · regulatory driver · dependency · proposed engagement
```

**XYZ callout for §3.2:** walk the seed findings UC-F-001 / UC-N-001 (plaintext secrets in
source repositories — the dominant open exposure from the 2019 red-team) through the method,
landing them in **Quick wins** and **Major project** respectively, with the dependency on the
inventory layer made explicit.

### 3.3 Worked-example callouts (XYZ)

Client-agnostic procedure is the spine; the real XYZ secrets-management assessment is the
worked example, in clearly-marked callout blocks at each stage. Headline figures used
must match the actual assessment data: **0 MET / 16 PARTIAL / 11 GAP / 20 PENDING** of 47
UCs; the inventory-layer-above-the-vault-tier finding as the headline gap; UC-F-001 /
UC-N-001 as the anchor seed findings.

## 4. Document B — `methodology/METHODOLOGY.md` (client-facing)

Derived from the playbook, **after** it is written. Same 6-stage skeleton, retold for a
buyer/exec:

- Why the method is rigorous (rubric-grounded, framework-scoped, evidence-based, override-with-rationale).
- What the client receives at each stage (scoped framework set → gap report → prioritised engagement menu → re-assessment cadence).
- What the engagement menu gives them (a sequenced, defensible remediation roadmap).

**Stripped of internal mechanics:** no step-by-step tooling commands, no consultant
checklists, no file paths. **Honest framing:** value expressed as cost-avoidance and
exposure-reduction; **no invented ROI numbers**.

**Relationship to Document A:** the playbook is the source of truth; the client-facing doc
is a distilled, trust-oriented retelling. Both share the identical 6-stage skeleton so they
cannot drift. Each doc carries a short header cross-linking the other.

## 5. Scope boundaries

**In scope (this slice):** the two markdown documents; ADR-012; backlog update.

**Out of scope (later WS-4 slices):**
- The roadmap **generator** — code that reads `assessment-record.json` and auto-emits the
  engagement menu. This slice only *documents* the method.
- The **exec-summary print view** — rendered/print-friendly client output.
- Promotion of the client-facing doc to a self-contained HTML deck (Approach C, later).

No code changes this slice.

## 6. Verification (replaces "tests" for a docs deliverable)

1. **Cross-reference integrity** — every tooling/file/UC reference in the playbook resolves
   to a real artifact (WS-2 presets, the questionnaire, the rubric files, `report_adapter.py`,
   the matrix report). Checked against the repo.
2. **Worked-example fidelity** — XYZ callout figures (0/16/11/20 counts, UC-F-001/UC-N-001
   seed findings, inventory-layer headline gap) match the actual assessment data, not
   paraphrased numbers.
3. **Two-doc consistency** — the 6-stage skeleton is identical across both documents; no
   contradictions between them.
4. **Self-review pass** — no TBD/placeholder; no invented numbers; prioritisation method
   internally consistent; client-facing doc free of internal mechanics.

## 7. Artifacts produced

- `methodology/PLAYBOOK.md`
- `methodology/METHODOLOGY.md`
- `docs/adr/ADR-012-methodology-playbook.md`
- `meta/IMPROVEMENT-BACKLOG.md` — WS-4 slice 1 marked.

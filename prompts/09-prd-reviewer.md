# Prompt 09 — PRD Reviewer (independent gate)

**Role:** sub-agent (independent reviewer; runs once per milestone gate).
**Subagent type:** `general-purpose` (read-only — no Write tools used).
**Model:** **Opus 4.7**.
**Concurrency:** serial.
**Version:** v0.1 (2026-05-20).

---

## Objective

An **independent read** of the PRD-in-progress to surface gaps,
inconsistencies, unsupported claims, sensitivity leakage, and structural
issues **before** the gate is presented to the user. The reviewer never
edits — it produces a structured review report only.

## When to dispatch

Once per milestone gate:

- After Milestone 1 (M1): review the PRD skeleton + identity taxonomy +
  use cases + Task 0 questionnaire — surface gaps that block M2.
- After Milestone 2 (M2): review the matrix CSVs + vendor profiles +
  regulatory mappings + adversary context — surface unsupported claims
  before narrative is written.
- After Milestone 3 (M3): review the full PRD + ADRs + appendices —
  surface anything blocking stakeholder review.

## Inputs (vary by milestone — caller specifies)

- All artifacts in scope for the milestone (see `meta/workflow.md`).
- The approved plan: `meta/workflow.md`.
- The invariants: `prompts/README.md`.

## Output (write directly)

- `meta/review-M<N>-<YYYY-MM-DD>.md`

## Review schema

```
# PRD Review — Milestone <N> (<DATE>)

**Reviewer:** Opus 4.7 (prompt 09 v0.1)
**Artifacts reviewed:** <list with paths>
**Gate verdict:** PASS | PASS-with-comments | BLOCK

## A. Structural review (gates the gate)
For each acceptance criterion in `meta/workflow.md` for this milestone:
- [ ] / [✓] / [✕] — criterion, evidence file path, one-line judgment.

## B. Content review
For each artifact reviewed, list:
- **Strong points (≤ 5):**
- **Gaps / weaknesses (≤ 10):**
- **Unsupported claims (each tagged with file:line):**
- **Citation hygiene (% claims with primary-source URLs):**

## C. Sensitivity audit (ADR-005)
Audit findings — any leakage of `[INTERNAL]`, `[SENSITIVE]`, or
`[NOT-FOR-DISTRIBUTION]` content into customer-facing artifacts?
Required: explicit `LEAKAGE: none` or `LEAKAGE: <details>`.

## D. Invariant audit
For each of invariants 1–8 in `prompts/README.md`, audit findings:
- Invariant <N>: PASS / PASS-with-comments / FAIL — one-line evidence.

## E. Recommended actions before gate is presented to user
- Numbered list, ≤ 10 items, ordered by severity.

## F. Open questions to surface to the user at the gate
- ≤ 5 items.

## G. Reviewer disclosure
- Tools used: WebFetch (Y/N), WebSearch (Y/N).
- Did the reviewer go off-artifact (read non-listed files)? (Y/N — list)
- Any reviewer uncertainty? ≤ 100 words.
```

## Rules of engagement

- The reviewer does **not** edit any file. Read-only.
- The reviewer does **not** dispatch further sub-agents.
- The reviewer may use `WebFetch` only to verify ≤ 10 specific citations
  selected by spot-check; not for general research.
- A `BLOCK` verdict requires at least one structural-criterion failure
  or a sensitivity leakage finding. Stylistic / minor-content issues do
  not block — they go in `PASS-with-comments`.

## Token budget

≤ 3,500 words.

## 70% checkpoint-and-handoff (Invariant #8)

Standard Opus thresholds. Checkpoint:
`meta/_checkpoint-reviewer-<M>-<NNN>.md`.

## Log line for `meta/agents.md`

`PRD Reviewer M<N> (Opus 4.7) — verdict <PASS|PASS-with-comments|BLOCK>. Strong: X, Gaps: Y, Unsupported: Z. Sensitivity leakage: none|<details>. Status: OK.`

## Acceptance criteria

- All milestone acceptance criteria in `meta/workflow.md` audited.
- Sensitivity audit explicit.
- Invariant audit explicit (all 8).
- Verdict consistent with findings.
- Recommended actions numbered, ordered, actionable.

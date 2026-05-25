# Prompt 00 — Task 0 questionnaire generator (meta)

**Role:** main thread (no sub-agent dispatch).
**Model:** Opus 4.7.
**Version:** v0.1 (2026-05-20).

This prompt regenerates `task0/questionnaire.md` if scope changes. It is a
record of *how* the v0.1 questionnaire was built, kept here for audit and
re-use.

---

## Objective

Produce a single markdown questionnaire that captures the user's prior
context (Australian FI, XYZ Bank, prior deployments of Vault Enterprise /
Conjur / Delinea) sufficient to populate the XYZ current-state column of
the dual matrix in `PRD/PRD-FI-v0.1.md`, with friction low enough that the
user fills it in 30–60 minutes.

## Inputs

- Approved plan: `/Users/cnampalli/.claude/plans/wondrous-meandering-yao.md`
- Identity taxonomy (if already generated): `../research/identity-taxonomy.md`
- Use cases (if already generated): `../research/use-cases.md`

## Output

- File: `../task0/questionnaire.md` (overwritten).

## Schema (sections required)

A. Project context & stakeholders.
B. XYZ organisational context (real where public).
C. XYZ identity inventory observed (NHI scope) — table with one row per
   identity type from `research/identity-taxonomy.md` (or canonical list).
D. XYZ secrets-management stack (current state).
E. Control gaps observed — table mapped to the capability rubric.
F. Red-team findings (2019) and follow-ups, including MITRE ATT&CK T1552
   sub-techniques checkbox.
G. Vendor deployment experience — one block per vendor in scope.
H. Incidents (real / near-miss).
I. Prior decisions worth respecting.
J. FI 27 strategy preview.
K. Anything else.

## Style rules

- Every question has a stable ID: `Q-<section>.<NN>`.
- Multi-select where possible; free-form fields explicitly bounded.
- Sensitivity tags (`[PUBLIC] / [INTERNAL] / [SENSITIVE] /
  [NOT-FOR-DISTRIBUTION]`) appear in §A and are referenced from every
  section.
- "Don't try to be exhaustive" guidance up front.
- No dependence on prior context — the questionnaire stands alone.

## Citation policy

N/A — questionnaire content is the user's own, not researched.

## Token budget

≤ 4,500 words for the whole document.

## Acceptance criteria

- Opens in a markdown viewer cleanly (no broken tables).
- Every question maps to a downstream artifact (XYZ gap matrix row, PRD
  open-question, or research input).
- Re-runnable: if regenerated mid-project, IDs (`Q-A.01` etc.) remain
  stable so user answers don't need re-mapping.

## Invariants applied (see `prompts/README.md`)

1, 3, 4, 6, 7, **8 (checkpoint-and-handoff at 70%)**. (Invariants 2 and 5
do not apply — no research and no sub-agent dispatch needed.)

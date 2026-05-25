# Prompt 07 — XYZ Current-State Synthesizer

**Role:** main thread (no sub-agent dispatch — handles sensitive content).
**Model:** Opus 4.7.
**Concurrency:** —
**Version:** v0.1 (2026-05-20).

---

## Why main-thread

`task0/responses.md` may contain `[INTERNAL] / [SENSITIVE] /
[NOT-FOR-DISTRIBUTION]` content. Sub-agents have their own context
windows and we do not want sensitive material crossing into a research
agent. The orchestrator (main thread) keeps this content in scope only
long enough to write `matrix/anz-current-state.csv` and the redacted PRD
§13 evidence cells.

## Objective

Translate the user's filled-in `task0/responses.md` into:

1. **`matrix/anz-current-state.csv`** — one row per `(UC, NHI)` pair
   declared compatible (mirrors `vendor-capabilities.csv` shape).
2. **Evidence excerpts for PRD §13** — written as a separate file
   `research/anz-current-state-evidence.md` with `[INTERNAL]` content
   stripped or anonymised per ADR-005.

## Inputs

- `task0/responses.md` (user-supplied).
- `task0/questionnaire.md` (for question ID resolution).
- `research/identity-taxonomy.md`.
- `research/use-cases.md`.
- `meta/workflow.md` for sensitivity policy.

## Output schema — `matrix/anz-current-state.csv`

Header row exactly:

```
uc_id,nhi_id,anz_state,confidence,evidence_q_ids,evidence_redacted,gap_notes,sensitivity_tag,citation_keys
```

- `anz_state` — `MET` | `PARTIAL` | `GAP` | `N/A` | `PENDING`.
- `confidence` — `HIGH` (user wrote a direct answer) /
  `MEDIUM` (inferred from related answers) / `LOW` (speculative) /
  `PENDING` (no user input yet).
- `evidence_q_ids` — semicolon-separated `Q-X.NN` IDs from the
  questionnaire that contributed.
- `evidence_redacted` — the **anonymised** version safe for PRD use
  (≤ 30 words). For `[SENSITIVE]` / `[NOT-FOR-DISTRIBUTION]` evidence,
  put `(redacted — see internal annex)`.
- `gap_notes` — what would close the gap (≤ 30 words).
- `sensitivity_tag` — highest tag from the contributing answers.
- `citation_keys` — any public references the user cited (e.g.,
  HashiCorp case study URLs, conference talks).

## Output schema — `research/anz-current-state-evidence.md`

Sectioned by NHI bucket (COMMON / UNCOMMON), then by UC, then bulleted
findings. Every finding carries its sensitivity tag. Sensitive content
is **not reproduced**; only the redacted summary appears.

## Redaction algorithm (ADR-005)

For each answer in `task0/responses.md`:

1. Read its sensitivity tag.
2. If `[PUBLIC]` — quote freely, cite the source the user named.
3. If `[INTERNAL]` — paraphrase, anonymise to "observed at a major AU
   FI", drop names of teams / tools / people / regions, retain the
   pattern.
4. If `[SENSITIVE]` — do not paraphrase into the PRD. Use only as
   `anz_state` signal in the CSV; evidence cell shows
   `(redacted — see internal annex)`.
5. If `[NOT-FOR-DISTRIBUTION]` — ignore for both PRD AND CSV (annex
   only — and even then, leave a one-line `<seen-but-not-reproduced>`
   marker in `research/anz-current-state-evidence.md`).

## Sensitivity policy (Invariant #7)

This prompt is the chief enforcement point for ADR-005. Be conservative:
when uncertain about a tag, treat the answer as `[SENSITIVE]`.

## 70% checkpoint-and-handoff (Invariant #8)

If `task0/responses.md` is very long: checkpoint at
`meta/_main-checkpoint-anz-<NNN>.md`. Resume by section.

## Log line for `meta/agents.md`

`XYZ Current-State Synthesizer (main, Opus 4.7) — wrote anz-current-state.csv (X rows: MET=A PARTIAL=B GAP=C N/A=D PENDING=E) + anz-current-state-evidence.md. Sensitivity audit: <summary>. Status: OK.`

## Acceptance criteria

- Every `(UC, NHI)` pair in `vendor-capabilities.csv` has a matching
  row in `anz-current-state.csv` (even if `PENDING`).
- Every `evidence_redacted` cell ≤ 30 words.
- Sensitivity-tag audit: no `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]`
  content reproduced verbatim in any output file.
- A short audit summary (`meta/anz-sensitivity-audit.md`) lists how many
  answers fell into each tag, and where any redactions were applied.

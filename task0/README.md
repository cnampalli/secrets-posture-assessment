# task0/ — your context (please fill async)

## What this is

This folder captures **your prior context** — XYZ Bank, the 2019 red-team
exercise that selected HashiCorp Vault Enterprise, and any other enterprise
deployments of CyberArk Conjur, Delinea Secret Server, or related products.

That context becomes:

- **The XYZ current-state column** in the dual matrix.
- **Evidence citations** in the PRD §13 (Findings — XYZ side).
- **Adversary realism** in PRD §14 (Adversary context) — what *actually*
  happened in your red-team exercise feeds into how the rubric is scored
  against adversary TTPs.

## Files

| File | Purpose |
|---|---|
| [`questionnaire.md`](./questionnaire.md) | The questionnaire itself. Read-only structure. |
| `responses.md` | **Where you write answers.** Create / edit this file. |

## How to fill it in

1. Open `questionnaire.md` and read through every section.
2. Copy or duplicate it as `responses.md` (or just start a fresh `responses.md`
   referencing question IDs — your choice).
3. Fill what you can. **Skip anything you don't have or can't share** — every
   blank becomes a PRD §18 Open Question for the stakeholder, which is
   acceptable.
4. Use the sensitivity tags in each section. Per ADR-005 (sensitivity
   policy):
   - `[PUBLIC]` — fact already in public record (Vault Ent at XYZ is in
     HashiCorp's published case studies, for example).
   - `[INTERNAL]` — observed during engagement; will be anonymised as
     "observed at a major AU FI" in the PRD.
   - `[SENSITIVE]` — keep in `responses.md` only; **will not** be reproduced
     in the PRD.
   - `[NOT-FOR-DISTRIBUTION]` — explicitly excluded from any PRD or
     supporting artifact, including footnotes.

## Bandwidth check

The questionnaire is structured to take **30–60 minutes** if you have the
context fresh. Skip the deep-dive sections (G–I) on first pass if you're
time-constrained — those mostly inform PRD v1.0, not v0.1.

## When you're done

Drop a line in the conversation ("Task 0 ready") and I'll fold the responses
into the dual matrix and PRD findings in the next session.

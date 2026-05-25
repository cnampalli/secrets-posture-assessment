# Main-thread checkpoint 001

**Stopped:** 2026-05-20 (Wed AEST) — voluntary stop to preserve daily +
weekly budget for the remainder of the week.

**Reason:** User-directed pacing. Reported session 7 % / weekly 23 % at
mid-session; explicit instruction: "make sure that we should be able to
work tomorrow as well. If not, save it until further instructions by me."

**Budget snapshot at stop (user-reported earlier in same session):**
- Daily session: ~7 % used, resets in ~4h15m from time of report.
- Weekly cloud: ~23 % used.
- After this turn estimated to be modestly higher — comfortably below
  any 70% threshold; we're stopping for **budget discipline across the
  week**, not because the context window is full.

---

## What is COMPLETE

### Workspace scaffold (M1.1) — DONE
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/README.md`
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/CHANGELOG.md`
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/meta/workflow.md` (incl. durable rules sub-section)
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/meta/agents.md` (empty log table)
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/meta/memory-index.md` (5 entries listed)
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/meta/citations.bib` (template)
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/notes/decisions.md`
- Full directory tree (`PRD/{adrs,appendices}`, `task0/`, `prompts/`,
  `research/{vendors,regulatory,adversary}`, `matrix/`, `meta/`, `notes/`).

### Task 0 questionnaire (M1.2) — DONE
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/task0/questionnaire.md`
  (sections A–K; ~50+ structured questions with stable `Q-X.NN` IDs).
- `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/task0/README.md`
  (instructions, sensitivity-tag policy, bandwidth guidance).
- **USER ACTION:** fill `task0/responses.md` (create the file) when ready.
  Partial fill is fine — blanks become PRD §18 open questions.

### Sub-agent prompts (M1.3) — PARTIAL (3 of 9 written)
- `prompts/README.md` (catalog + 8 invariants including the 70%
  checkpoint-and-handoff rule from this session).
- `prompts/00-task0-questionnaire-generator.md` — meta-prompt.
- `prompts/01-identity-taxonomist.md` — Opus 4.7, ready to dispatch tomorrow.
- `prompts/02-use-case-catalog-builder.md` — Opus 4.7, ready to dispatch tomorrow.

### Claude persistent memory (M1.4) — DONE
- `feedback-70-percent-checkpoint-rule.md`
- `feedback-session-budget-management.md`
- `user-role-architect-fi.md`
- `project-anz-secrets-prd.md`
- `reference-external-frameworks.md`
- `MEMORY.md` (index)

### Operational rules added mid-session
- **70 % context checkpoint-and-handoff** applies to every agent AND this
  main thread.
- **Session + weekly budget management** — pace across multi-day projects,
  preserve tomorrow.

---

## What is PENDING (tomorrow, Thu 2026-05-21)

In recommended order:

### 1. Finish the remaining 6 sub-agent prompts (cheap, ~30 min)
- `prompts/03-vendor-researcher-template.md` (Sonnet 4.6; parameterised over vendor; used in M2 waves of 4)
- `prompts/04-regulatory-mapper.md` (Opus 4.7; parameterised over framework: E8 / NIST-ZT / CPS-234 / ASD-ISM / NIST-CSF-2)
- `prompts/05-adversary-ttp-mapper.md` (Opus 4.7; MITRE ATT&CK T1552 family + breach post-mortems)
- `prompts/06-matrix-assembler.md` (main-thread deterministic join)
- `prompts/07-anz-current-state-synthesizer.md` (main-thread; reads `task0/responses.md`)
- `prompts/08-prd-writer.md` (main-thread; assembles PRD)
- `prompts/09-prd-reviewer.md` (independent reviewer; one pass per milestone)

### 2. Dispatch Identity Taxonomist (Opus 4.7) — sub-agent
- Prompt: `prompts/01-identity-taxonomist.md`.
- Output: `research/identity-taxonomy.md` + `matrix/identity-catalog.csv`.
- Concurrency: serial.

### 3. Dispatch Use Case Catalog Builder (Opus 4.7) — sub-agent
- Prompt: `prompts/02-use-case-catalog-builder.md`.
- Output: `research/use-cases.md` + `matrix/use-cases.csv`.
- Concurrency: can run in parallel with #2 (both Opus 4.7, but they don't
  share files — #2's `identity-taxonomy.md` is only an optional input to
  #3 and #3 falls back to canonical NHI buckets if absent).
- **Recommend:** sequence them (#2 first, then #3 with the taxonomy as
  input) for higher coherence; tomorrow's call.

### 4. Write PRD-FI-v0.1.md skeleton — main thread (cheap)
- File: `PRD/PRD-FI-v0.1.md` — 21 sections, intent lines only.

### 5. Update `meta/agents.md` with rows for the dispatched agents.

### 6. M1 gate review with the user.
- Present: identity taxonomy, use cases, PRD skeleton, sub-agent prompt
  catalog, Task 0 questionnaire.
- Confirm direction before M2 dispatch (12 vendor sub-agents — biggest
  spend of the week).

---

## What is DEFERRED beyond tomorrow

- **M2 (Fri 2026-05-22 → Sat 2026-05-23):** 12 vendor profile sub-agents
  in waves of 4 (Sonnet 4.6); 5 regulatory mappers in parallel (Opus 4.7);
  adversary TTP mapper (Opus 4.7); matrix assembly (CSV, MD, HTML viewer);
  XYZ current-state synthesis from `task0/responses.md`.
- **M3 (Sun 2026-05-24):** full PRD narrative + ADRs 001–006 + appendices
  A–D.
- **v1.0 (week of 2026-05-26):** post-stakeholder deep-dive iteration.

---

## How to resume tomorrow (cold-start protocol)

1. Read this checkpoint first.
2. Read `meta/workflow.md` for project context.
3. Read `prompts/README.md` for invariants (especially #7 and #8).
4. Check whether `task0/responses.md` exists. If yes, peek for completeness.
5. Pick up from "What is PENDING" #1 above (or jump to #2/#3 if the user
   says "skip the rest of the prompts, dispatch now").
6. Update task list: tasks #3, #5, #6, #7, #8, #9, #10 are still relevant
   (open IDs in the harness).
7. Apply the 70% rule for the rest of the session.

---

## Open questions still on the table (for user)

(Repeated from `meta/workflow.md` for visibility — user can answer
either via `task0/responses.md` Section A or directly in chat.)

1. Stakeholder identity inside XYZ (CISO / Head IAM / Head Platform Sec / other).
2. Distribution surface (internal XYZ only? external auditor? regulator?).
3. Existing XYZ artifacts to chain onto for Task 0 (any prior strategy / audit / IGA doc to reference?).
4. Vendor exclusions (any of the 12 ruled out by procurement / policy?).
5. FI 27 strategy preview (anything shareable now to avoid late re-tagging?).

---

## Memory pointers

- `feedback-70-percent-checkpoint-rule` — every agent + this thread checkpoint at ~70 %.
- `feedback-session-budget-management` — multi-day pacing rule.
- `project-anz-secrets-prd` — project facts + resume protocol.
- `user-role-architect-fi` — user expertise + working style.
- `reference-external-frameworks` — primary sources library.

Session ends here. Awaiting user's go-ahead to resume tomorrow.

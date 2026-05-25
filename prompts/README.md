# Sub-agent prompts — catalog

Versioned, first-class artifacts. Every sub-agent invocation references the
prompt file by path and logs the run in `../meta/agents.md`.

## Invariants (every prompt enforces these)

1. **Sub-agent writes its own output file directly** — no inline returns
   back to the orchestrator. The output path is supplied in the prompt.
2. **Citations are mandatory.** Every factual claim links to a primary-source
   URL or carries one of: `[SPECULATION]`, `[USER-SUPPLIED]`,
   `[BREACH-POST-MORTEM]`, `[INDUSTRY-CONSENSUS]`.
3. **Token budget per section** — declared explicitly (`≤N words`).
4. **Output schema is fixed** — CSV columns and markdown headings as
   specified.
5. **No cascade** — sub-agents must NOT spawn further sub-agents (avoid
   uncontrolled depth).
6. **Log to `meta/agents.md`** — one-line summary at completion.
7. **Sensitivity tags respected** — `[PUBLIC] / [INTERNAL] / [SENSITIVE] /
   [NOT-FOR-DISTRIBUTION]` (per ADR-005). Sub-agents touching `task0/responses.md`
   must treat `[SENSITIVE]` and `[NOT-FOR-DISTRIBUTION]` content as
   internal-only.
8. **70% checkpoint-and-handoff rule (MANDATORY for every agent, sub-agent
   AND main thread).** When the agent's own context window crosses **~70 %
   utilisation**, the agent MUST:

   a. **Save state** — write a structured checkpoint file at
      `<agent-output-dir>/_checkpoint-<NNN>.md` capturing:
      - completed work (with file paths and one-line summaries),
      - remaining work (concrete to-do list, in priority order),
      - intermediate findings not yet flushed to output files,
      - citations gathered so far (BibTeX keys + URLs),
      - sensitive tags applied,
      - explicit `## Continuation instructions` block for the successor
        (which prompt file, which output paths, which inputs to re-read).
   b. **Flush partial outputs** — anything that can be written to its final
      destination file safely (e.g., completed rows of a CSV, completed
      markdown sections) is written before handoff. Mark in-flight content
      with `<!-- CHECKPOINT-<NNN> partial; successor will continue -->`.
   c. **Hand off** — end the turn with a single-line orchestrator signal:
      `HANDOFF_NEEDED: <agent-output-dir>/_checkpoint-<NNN>.md`. Do not
      attempt to continue work past the threshold.
   d. **Log** — append the checkpoint event row to `meta/agents.md` with
      `status=PARTIAL — handoff`.

   The orchestrator (main thread or this prompt's caller) then dispatches a
   **fresh successor agent** with:
   - the same prompt file (e.g., `prompts/03-vendor-researcher-template.md`),
   - the same output paths,
   - the checkpoint file as a `--resume-from` input,
   - explicit instruction to read the checkpoint first, then continue.

   **Self-estimating 70%.** Sub-agents cannot directly read their own context
   meter. Estimate via these heuristics — checkpoint when ANY hits:
   - cumulative output written ≥ 6,000 words for an Opus 4.7 agent (or
     ≥ 4,000 words for Sonnet 4.6),
   - tool results consumed ≥ 25 (e.g., 25 WebFetch / Read calls),
   - elapsed turn count ≥ 12 distinct "tool call → reflect → tool call"
     loops,
   - any single completed sub-task whose continuation would push past the
     above bounds.

   When in doubt, **checkpoint early**. A two-checkpoint task is fine. A
   silently-truncated task is not.

   **This rule applies to the main thread too.** If the orchestrator senses
   it is approaching ~70 % during PRD writing or matrix assembly, it
   writes a `meta/_main-checkpoint-<NNN>.md` and ends its turn with the
   same `HANDOFF_NEEDED` signal so the next session resumes cleanly.

## Catalog

| # | Prompt file | Role | Subagent type | Model | Concurrency |
|---|---|---|---|---|---|
| 00 | [00-task0-questionnaire-generator.md](./00-task0-questionnaire-generator.md) | Meta-prompt to regenerate the questionnaire if scope changes | main thread (no agent) | Opus 4.7 | — |
| 01 | [01-identity-taxonomist.md](./01-identity-taxonomist.md) | Build comprehensive NHI taxonomy (common + uncommon) | general-purpose | Opus 4.7 | serial |
| 02 | [02-use-case-catalog-builder.md](./02-use-case-catalog-builder.md) | Build use-case catalog (functional + non-functional) | general-purpose | Opus 4.7 | serial |
| 03 | [03-vendor-researcher-template.md](./03-vendor-researcher-template.md) | Profile one vendor from public docs (parameterised template) | general-purpose w/ WebSearch + WebFetch | Sonnet 4.6 | 4-at-a-time waves |
| 04 | [04-regulatory-mapper.md](./04-regulatory-mapper.md) | Map UCs to a single regulatory framework (parameterised) | general-purpose w/ WebSearch | Opus 4.7 | 5-way parallel |
| 05 | [05-adversary-ttp-mapper.md](./05-adversary-ttp-mapper.md) | MITRE ATT&CK T1552 family + breach post-mortems | general-purpose w/ WebSearch | Opus 4.7 | serial |
| 06 | [06-matrix-assembler.md](./06-matrix-assembler.md) | Join CSVs into matrix.csv / matrix.md / matrix-viewer.html | main thread | Opus 4.7 | — |
| 07 | [07-anz-current-state-synthesizer.md](./07-anz-current-state-synthesizer.md) | Turn task0/responses.md into anz-current-state.csv | main thread | Opus 4.7 | — |
| 08 | [08-prd-writer.md](./08-prd-writer.md) | Assemble PRD-FI-v0.1.md from artifacts | main thread | Opus 4.7 | — |
| 09 | [09-prd-reviewer.md](./09-prd-reviewer.md) | Independent review pass on the PRD before each gate | adapted reviewer agent | Opus 4.7 | once per milestone |

## Versioning

Treat each prompt file as **append-only with revision blocks**. Prepend a
`## v0.2 (date)` block above the previous version, mark the older block as
`## v0.1 (date) [SUPERSEDED]`. Do not delete prior versions — the agent
catalog references the prompt-path at run time, and revision history is the
audit trail.

## How to dispatch one

```
Use the Agent tool with subagent_type="general-purpose" (or the type
specified in the prompt's header). Pass the contents of the prompt file
verbatim as the prompt parameter. The model is specified in the prompt
header — pass it via the model parameter of the Agent tool.
```

# Prompt 04 — Regulatory Mapper (parameterised template)

**Role:** sub-agent.
**Subagent type:** `general-purpose` (must have `WebSearch`).
**Model:** **Opus 4.7**.
**Concurrency:** 5-way parallel (one per framework).
**Version:** v0.1 (2026-05-20).

---

## Parameters (caller fills these in the Agent prompt header before dispatch)

- `FRAMEWORK_NAME` — one of: `Essential 8`, `NIST SP 800-207 Zero Trust`,
  `APRA CPS 234`, `ASD ISM`, `NIST CSF 2.0`.
- `FRAMEWORK_SLUG` — kebab-case (`essential-8` / `nist-sp-800-207-zt` /
  `apra-cps-234` / `asd-ism` / `nist-csf-2.0`).
- `FRAMEWORK_PRIMARY_URL` — official URL (from
  `reference-external-frameworks` memory entry).
- `FRAMEWORK_ROLE` — `PRIMARY-LENS` (Essential 8, NIST ZT) or
  `BACK-MAP` (CPS 234, ISM, CSF 2.0).

## Objective

Produce a **framework mapping document** for `FRAMEWORK_NAME` that:

1. Lists the framework's relevant control objectives / pillars /
   maturity levels in their canonical numbering.
2. Maps each control to the project's UCs (`UC-F-*` / `UC-N-*`) and NHIs
   (`NHI-*`) — i.e., which UCs / NHIs implement or satisfy this control.
3. Identifies controls the project's UC catalog does **not** yet address
   (gap rows for v1.0).

## Inputs

- `prompts/README.md` (invariants).
- `research/identity-taxonomy.md`.
- `research/use-cases.md`.
- `FRAMEWORK_PRIMARY_URL` and supporting primary sources.
- `meta/citations.bib` (append to).

## Outputs (write directly)

- `research/regulatory/<FRAMEWORK_SLUG>-mapping.md`
- Append rows to `matrix/regulatory-trace.csv`.

## Markdown schema

```
# Regulatory Mapping — <FRAMEWORK_NAME>

**Role in PRD:** <FRAMEWORK_ROLE>
**Primary source:** <FRAMEWORK_PRIMARY_URL>
**Version cited:** <e.g., "Essential 8 maturity model — November 2023">
**Mapped by:** Opus 4.7 (prompt 04 v0.1)

## 1. Framework summary (≤ 250 words)
What the framework is, its scope, its maturity model (if any), its
authority (AU government / NIST / APRA / etc.). Why it's in the PRD.

## 2. Control objectives in scope (≤ 400 words)
Bulleted with stable codes. Limit to controls relevant to secrets
management or machine identity.

## 3. UC ↔ control mapping (≤ 800 words)
For each control code:
### <Control code> — <Control short title>
- **What it requires:** ≤ 40 words.
- **UCs that satisfy it:** `UC-F-XXX, UC-N-XXX, …`.
- **NHIs especially relevant:** `NHI-XXX, …`.
- **Evidence quote (≤ 30 words):** verbatim from primary source.
- **Maturity level (if applicable):** ML1 / ML2 / ML3 for Essential 8;
  CSF tiers / NIST ZT pillars / CPS 234 paragraphs.

## 4. Reverse map: UCs missing coverage (≤ 200 words)
Which UCs in `research/use-cases.md` are not mapped to any control in
this framework — and is that a UC gap, a framework scope difference, or
a research gap?

## 5. Outcome-lens cross-references (≤ 200 words)
If `FRAMEWORK_ROLE = PRIMARY-LENS`, briefly state how this framework's
controls aggregate into the outcome lens the PRD uses. If
`BACK-MAP`, briefly state how this framework's controls **back-map**
onto the primary lens (Essential 8 + NIST ZT).

## 6. Open questions
What needs primary-source clarification or stakeholder input.

## 7. Citations
BibTeX keys appended to `meta/citations.bib`.
```

## CSV schema (`matrix/regulatory-trace.csv`)

Header row (write once if file empty):

```
framework_slug,framework_role,control_code,control_short_title,uc_ids,nhi_ids,maturity_level,evidence_url,evidence_quote,citation_keys
```

- `uc_ids` — semicolon-separated `UC-F-*` and `UC-N-*` IDs.
- `nhi_ids` — semicolon-separated `NHI-*` IDs.
- `maturity_level` — `ML1` / `ML2` / `ML3` / `Tier-1..4` / `Pillar-N` /
  `Paragraph-N` depending on framework, or `N/A`.

**Append**, don't overwrite.

## Sources policy

Primary sources only. Government / standards-body URLs.
- ASD Essential 8: `cyber.gov.au` (maturity model + ML1/2/3 detail pages).
- NIST SP 800-207: `csrc.nist.gov/publications/detail/sp/800-207/final`.
- APRA CPS 234: `apra.gov.au/prudential-standard-cps-234`.
- ASD ISM: `cyber.gov.au` (Information Security Manual).
- NIST CSF 2.0: `nist.gov/cyberframework` and `csrc.nist.gov`.

No vendor blog mappings, no consultancy-blog mappings.

## Token budget

≤ 3,500 words markdown + ~30–60 CSV rows.

## Sensitivity policy (Invariant #7)

`[PUBLIC]` only. Do not ingest `task0/responses.md`.

## 70% checkpoint-and-handoff (Invariant #8)

Standard Opus thresholds. Checkpoint file:
`research/regulatory/_checkpoint-<FRAMEWORK_SLUG>-<NNN>.md`.

## Log line for `meta/agents.md`

`Regulatory Mapper (Opus 4.7) — wrote <FRAMEWORK_SLUG>-mapping.md + N rows in regulatory-trace.csv. M citations. Status: OK.`

## Acceptance criteria

- Every control code in the framework's secrets-management-relevant
  subset has a row.
- ≥ 1 UC mapped to each control (or row tagged with `MISSING-UC` in
  notes if intentionally unmapped).
- ≥ 1 NHI mapped to each control where applicable.
- Every evidence quote ≤ 30 words.
- BibTeX entries appended to `meta/citations.bib`.

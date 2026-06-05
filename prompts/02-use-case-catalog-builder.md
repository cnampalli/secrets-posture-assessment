# Prompt 02 — Use Case Catalog Builder

**Role:** sub-agent.
**Subagent type:** `general-purpose`.
**Model:** **Opus 4.7**.
**Version:** v0.1 (2026-05-20).

---

## Objective

Produce a **comprehensive use-case catalog** for secrets management across
machine identities. Two categories:

1. **Functional use cases** — engineer-facing (e.g., "as an engineer I want
   to ensure no plain-text passwords sit in source-controlled code").
2. **Non-functional use cases** — product-owner / auditor-facing (e.g.,
   "as a product owner I need to know how many plain-text secrets remain
   in repos, with a trend line").

This catalog seeds rows of the dual matrix and §8 of the PRD.

## User-supplied seeds (must be in the output, refined)

- **Functional seed:** "As an engineer I want to make sure that there are
  no plain-text passwords in the code repository stored in source
  management software (e.g., GitLab, GitHub)."
- **Non-functional seed:** "As a product owner I need to know how many of
  those plain-text secrets are still present in the code repository."

These two seed examples define the *tone* of the catalog. Extend out from
them, then complete coverage across the NHI taxonomy in
`research/identity-taxonomy.md` (read it first; if absent, work from the
canonical NHI buckets and proceed).

## Inputs

- `prompts/README.md` (invariants).
- `research/identity-taxonomy.md` (NHI rows — every NHI bucket needs at
  least one UC touching it).
- `meta/workflow.md` for project context.

## Output (write directly)

- **File:** `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/research/use-cases.md`
- **Companion CSV (you populate):** `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/matrix/use-cases.csv`

## Markdown schema (use-cases.md)

```
# Use-Case Catalog — Secrets Management for Machine Identities

## 1. Methodology
[≤ 200 words; explain functional vs non-functional split, persona model
(engineer / SRE / platform-eng / DevSecOps / product-owner / auditor /
incident-responder), and how UCs cross-reference NHIs and frameworks.]

## 2. Personas
[Bulleted list with one-line role description for each persona referenced.]

## 3. Functional use cases (engineer-facing)
For each:
### UC-F-<NNN> — <Short title>
- **Story:** "As a <persona> I want <capability> so that <outcome>."
- **Acceptance criteria:** ≤ 3 bullets, testable.
- **NHIs in scope:** `NHI-001, NHI-007, …` (reference IDs).
- **Outcome lens (Essential 8 + ZT):** which E8 control area / ZT pillar.
- **Back-map (CPS 234 / CPS 230 / CPG 234 / ISM):** codes that **must already
  exist as a `control_code` in `matrix/regulatory-trace.csv`** — derive them from
  that file's `uc_ids` column, do **not** invent. **No NIST CSF** (deferred per ADR-003).
- **Priority (FI default):** P0 / P1 / P2.
- **Citations / inspiration:** primary source URLs.

[Aim for 18–24 functional UCs.]

## 4. Non-functional use cases (product-owner / auditor-facing)
[Same schema. Aim for 12–18 NF UCs. Include observability, KPIs, audit,
reporting, vendor-risk, training & comms, exception management,
break-glass governance, post-incident, supply-chain assurance,
crypto-agility.]

## 5. Cross-cutting use-case clusters
[≤ 300 words on clusters that span functional + non-functional, e.g.,
"detect-and-remediate-plaintext-secrets" cluster (F-detection +
N-reporting + N-trend + F-remediation pipeline).]

## 6. Open questions
[Bulleted, ≤ 10.]

## 7. Citations
[BibTeX keys appended into `meta/citations.bib`.]
```

## CSV schema (matrix/use-cases.csv)

```
uc_id,category,short_title,story,acceptance_criteria,nhis_in_scope,outcome_lens,backmap_codes,priority_fi,citation_keys
```

- `uc_id` — `UC-F-001` / `UC-N-001`, zero-padded.
- `category` — `FUNCTIONAL` | `NON_FUNCTIONAL`.
- `nhis_in_scope` — semicolon-separated NHI IDs.
- `outcome_lens` — semicolon-separated; values like `E8-AppControl` /
  `ZT-Pillar-Identity` / `ZT-Pillar-Device` / etc.
- `backmap_codes` — semicolon-separated; **every code MUST resolve to a
  `control_code` in `matrix/regulatory-trace.csv`**, e.g.
  `CPS234-§21;CPS234-§27(d);CPG234-Att-C;ISM-1619`. Note CPS 234 sub-clauses use
  the normalised paren form (`§21(a)`, `§27(d)`, `§35(a)`); the (a)–(e) items
  belong to **§27**, not §28 — **`§28a/b/c` and `§35c` do not exist**. **Do not
  emit `CSF-*` codes** (NIST CSF 2.0 is deferred per ADR-003).
- `priority_fi` — `P0` / `P1` / `P2`.

> **Back-map integrity (MANDATORY).** The `backmap_codes` column is a denormalised
> view of `matrix/regulatory-trace.csv`. Generate it **by reversing that file's
> `uc_ids` column** (BACK-MAP tier = `apra-cps-234` / `apra-cps-230` /
> `apra-cpg-234` / `asd-ism`). Never hand-author control codes from memory — the
> ISM IDs and CPS 234 clause numbers were corrected mid-project, and earlier drafts
> carried wrong ISM IDs (e.g. ISM-1546), fabricated APRA sub-clauses (`§28a`), and
> now-deferred CSF codes. After writing, run `python3 matrix/validate_data.py` and
> confirm every back-map code resolves. See `matrix/REGULATOR-AUDIT-2026-06-03.md` Part 4.

## Token budget

≤ 5,500 words total markdown.

## Sources to draw from (primary)

- CPS 234, CPS 230, CPG 234, ASD ISM, Essential 8 maturity (for back-mapping).
  **NIST CSF 2.0 is DEFERRED out of v0.1 per ADR-003 — do NOT emit `CSF-*` codes.**
- NIST SP 800-207 ZT pillars (for outcome lens).
- OWASP Secrets Management Cheat Sheet.
- CSA NHI Working Group risk catalog.
- GitGuardian "State of Secrets Sprawl" report (publicly available).
- Verizon DBIR — credential-related incident patterns.
- Vendor public docs (Vault, Conjur, AWS SM, etc.) for capability-shaped UCs.

## Sensitivity policy (Invariant #7)

`[PUBLIC]` everywhere. Do not ingest `task0/responses.md`.

## 70% checkpoint-and-handoff (Invariant #8)

Checkpoint to `research/_checkpoint-use-cases-<NNN>.md` per the standard
heuristics. Flush completed UC blocks and CSV rows first.

## Log line for `meta/agents.md`

`Use Case Catalog Builder (Opus 4.7) — wrote use-cases.md (X functional + Y non-functional) + use-cases.csv (Z rows). N citations. Status: OK.`

## Acceptance criteria

- ≥ 30 UCs total (18 functional minimum + 12 non-functional minimum).
- Both user-supplied seeds appear as UCs (e.g., `UC-F-001 / UC-N-001`).
- Every UC references ≥ 1 NHI ID.
- Every UC has an outcome-lens tag AND ≥1 back-map code, and **every back-map code
  resolves to a `control_code` in `matrix/regulatory-trace.csv`** (no `CSF-*`, no
  fabricated sub-clauses like `§28a`). Confirm via `python3 matrix/validate_data.py`.
- CSV parses cleanly.
- ≥ 1 functional + 1 non-functional UC per NHI bucket (no NHI orphans).

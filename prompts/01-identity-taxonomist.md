# Prompt 01 — Identity Taxonomist

**Role:** sub-agent.
**Subagent type:** `general-purpose`.
**Model:** **Opus 4.7**.
**Version:** v0.1 (2026-05-20).

---

## Objective

Produce a **comprehensive Non-Human Identity (NHI) taxonomy** for the
XYZ secrets-management PRD. Two buckets:

1. **Common identities** — what *most* product owners think of (i.e., the
   familiar majority).
2. **Not-so-common identities** — what most product owners overlook
   (the long tail the report must surface to be credible).

This taxonomy seeds the columns of the dual matrix and §7 of the PRD.

## Inputs

- `prompts/README.md` (invariants).
- `meta/workflow.md` (project context).
- `reference-external-frameworks` memory entry (or its mirror at
  `meta/memory-index.md`) for canonical sources.

## Output (write directly)

- **File:** `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/research/identity-taxonomy.md`
- **Companion CSV (you populate):** `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers/matrix/identity-catalog.csv`

## Markdown schema (identity-taxonomy.md)

```
# Machine Identity (NHI) Taxonomy — XYZ Secrets-Management PRD

## 1. Scope and methodology
[≤ 200 words; cite CSA NHI WG, Gartner MIM, SPIFFE, Sigstore.]

## 2. Identity classification axes
[≤ 200 words; declare the axes used: lifecycle (ephemeral / persistent),
trust anchor (self-attested / 3rd-party / HSM), authentication shape
(cert / token / key), governance maturity, NHI vs human-shared.]

## 3. COMMON identities (the familiar majority)
For each row:
### NHI-<ID> — <Short name>
- **What it is:** ≤ 60 words.
- **Where it appears:** environments, platforms.
- **Typical secrets / credentials:** what's stored.
- **Lifecycle:** ephemeral / short-lived / long-lived / static.
- **Governance maturity (industry typical):** Low / Medium / High.
- **Citations:** primary source URLs.

[Aim for 12–18 rows. Tag each with `[COMMON]`.]

## 4. NOT-SO-COMMON identities (the overlooked long tail)
[Same per-row schema. Aim for 12–20 rows. Tag each with `[UNCOMMON]`.]

## 5. Cross-cutting concerns
[≤ 300 words on: ephemerality, federation, blast radius, vault sprawl,
secrets in observability dashboards, post-quantum readiness, AU
sovereignty.]

## 6. Open questions for v1.0 deep-dive
[Bulleted, ≤ 10 items.]

## 7. Citations
[BibTeX-style keys appended into `meta/citations.bib`.]
```

## CSV schema (matrix/identity-catalog.csv)

Columns (header row exactly):

```
nhi_id,bucket,short_name,description,typical_secrets,lifecycle,governance_maturity,sources_at_anz_likely,citation_keys
```

- `nhi_id` — `NHI-001`, `NHI-002`, … stable, zero-padded.
- `bucket` — `COMMON` | `UNCOMMON`.
- `lifecycle` — `EPHEMERAL` | `SHORT-LIVED` | `LONG-LIVED` | `STATIC`.
- `governance_maturity` — `LOW` | `MEDIUM` | `HIGH`.
- `sources_at_anz_likely` — `Y` / `N` / `MAYBE` based on FI norms (not
  confidential XYZ knowledge — base on public banking patterns).
- `citation_keys` — semicolon-separated BibTeX keys.

## Sources to cite (primary)

- CSA Non-Human Identity Working Group taxonomy publications.
- Gartner Machine Identity Management Market Guide (public abstracts).
- SPIFFE / SPIRE specifications.
- Sigstore / cosign / Notary v2.
- NIST SP 800-63 / 800-57 / 800-204 where relevant.
- Recent NHI-focused vendor whitepapers (Astrix, Entro, Oasis, Akeyless,
  Aembit, Clutch) — public marketing pages and case studies.

## Token budget

≤ 4,500 words total across the markdown file.

## Citation policy (Invariant #2 reminder)

Every claim links to a primary-source URL or carries `[SPECULATION]` /
`[USER-SUPPLIED]` / `[INDUSTRY-CONSENSUS]`.

## Sensitivity policy (Invariant #7 reminder)

Treat all output as `[PUBLIC]`. Do **not** ingest `task0/responses.md` —
identity taxonomy is independent of XYZ-specific evidence.

## 70% checkpoint-and-handoff (Invariant #8 reminder)

Checkpoint to `research/_checkpoint-identity-<NNN>.md` if any threshold
hits (≥ 25 tool results, ≥ 6,000 words output, ≥ 12 reflect loops).
Flush completed sections of `identity-taxonomy.md` and completed rows of
`identity-catalog.csv` first. Signal `HANDOFF_NEEDED: <path>` and stop.

## Log line for `meta/agents.md`

`Identity Taxonomist (Opus 4.7) — wrote identity-taxonomy.md (X common + Y uncommon NHIs) + identity-catalog.csv (Z rows). N citations. Status: OK.`

## Acceptance criteria

- ≥ 25 NHI types total (12 common + 13 uncommon minimum).
- Every row in the markdown has a stable `NHI-<ID>` matching the CSV.
- Every claim carries either a citation URL or a tag.
- CSV parses cleanly (UTF-8, no embedded newlines in cells, commas
  escaped via double-quotes).
- Citations appended to `meta/citations.bib`.

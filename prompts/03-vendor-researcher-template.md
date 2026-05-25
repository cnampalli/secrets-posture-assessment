# Prompt 03 — Vendor Researcher (parameterised template)

**Role:** sub-agent.
**Subagent type:** `general-purpose` (must have `WebSearch` + `WebFetch`).
**Model:** **Sonnet 4.6** (volume work; well-bounded summarisation).
**Concurrency:** 4-at-a-time waves (dispatched in parallel from main thread).
**Version:** v0.1 (2026-05-20).

---

## Parameters (caller fills these in the Agent prompt header before dispatch)

- `VENDOR_NAME` — canonical vendor name (e.g., `HashiCorp Vault Enterprise`).
- `VENDOR_SLUG` — kebab-case slug (e.g., `hashicorp-vault-enterprise`).
- `VENDOR_DOC_ROOT` — primary docs URL (from
  `reference-external-frameworks` memory entry).
- `VENDOR_TIER` — `core` | `cloud-native` | `emerging` | `pki-mim`.

## Objective

Produce a **vendor profile** for `VENDOR_NAME` from public documentation,
scoring its capability against the use-case catalog and the NHI taxonomy.

## Inputs

- `prompts/README.md` (invariants — note #2, #7, #8).
- `research/identity-taxonomy.md` (NHI rows).
- `research/use-cases.md` (UC rows — score every UC).
- `meta/citations.bib` (append to).

## Outputs (write directly)

- `research/vendors/<VENDOR_SLUG>.md`
- One row per `(UC, NHI)` pair in
  `matrix/vendor-capabilities.csv` — see schema below. (Append rows; do
  NOT rewrite the file if it already has rows from other vendors.)

## Markdown schema (`research/vendors/<VENDOR_SLUG>.md`)

```
# Vendor Profile — <VENDOR_NAME>

**Tier:** <VENDOR_TIER>
**Primary docs:** <VENDOR_DOC_ROOT>
**Profile written:** <YYYY-MM-DD>
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

## 1. Vendor snapshot (≤ 150 words)
Ownership, deployment models, primary differentiator, AU/AUS presence.

## 2. Architecture (≤ 250 words)
Storage backend, auth methods, secrets engines / plugins, HSM/KMS
support, replication / DR posture, FedRAMP / IRAP / SOC 2 status if
declared.

## 3. NHI coverage map (≤ 600 words)
For every `NHI-<ID>` in `research/identity-taxonomy.md`:
- **Coverage:** `NATIVE` / `ADD-ON` / `PARTNER` / `GAP` / `N/A`.
- **Maturity:** 0–4 (0=none, 1=announced/preview, 2=GA-basic,
  3=GA-mature, 4=industry-leading).
- **Evidence:** one-line primary-source citation.

## 4. Use-case scoring (≤ 800 words)
For every `UC-<ID>` in `research/use-cases.md`:
- **Coverage:** as above.
- **Maturity:** 0–4.
- **Evidence:** one-line citation.

## 5. Strengths and gaps (≤ 300 words)
Top 3 strengths, top 3 gaps relative to the universal framework.

## 6. AU-specific notes (≤ 150 words)
Sovereignty / IRAP / Essential 8 alignment claims (verify each).

## 7. Citations
BibTeX keys appended to `meta/citations.bib`.

## 8. Open questions for v1.0
Where you couldn't find primary-source evidence; what an SE conversation
would answer.
```

## CSV schema (`matrix/vendor-capabilities.csv`)

If empty, write header row exactly:

```
vendor_slug,vendor_name,target_id,target_type,coverage,maturity,evidence_url,evidence_quote,citation_keys,notes
```

- `target_id` — either an `NHI-` ID or a `UC-` ID.
- `target_type` — `NHI` | `UC-F` | `UC-N`.
- `coverage` — `NATIVE` | `ADD-ON` | `PARTNER` | `GAP` | `N/A`.
- `maturity` — integer 0–4.
- `evidence_url` — the primary-source URL.
- `evidence_quote` — ≤ 30 words verbatim from the cited page.
- `citation_keys` — semicolon-separated BibTeX keys.
- `notes` — caveats / FY readiness / regional limits / etc.

**Append, don't overwrite.** If header already present, skip to row append.

## Sources policy

- **Primary** (required): vendor's own docs / specs / changelog / pricing
  page where capability is asserted.
- **Secondary** (corroborating): vendor blog posts, KB articles, GitHub
  repos, RFC documents.
- **Tertiary** (only if primary absent): analyst abstracts (Gartner /
  Forrester / KuppingerCole public summaries), peer-reviewed conference
  talks. Mark any tertiary-only claim with `[INDUSTRY-CONSENSUS]`.

If a capability is only mentioned in marketing without a docs page, mark
it `GAP` with maturity 0 and note in the `notes` column.

## Token budget

≤ 2,500 words of markdown + ~50–80 CSV rows.

## Sensitivity policy (Invariant #7)

`[PUBLIC]` only. Do not ingest `task0/responses.md`.

## 70% checkpoint-and-handoff (Invariant #8)

Sonnet 4.6 lower bound: checkpoint at ≥ 4,000 words output or ≥ 20 tool
results. Checkpoint file:
`research/vendors/_checkpoint-<VENDOR_SLUG>-<NNN>.md`. Flush rows to CSV
first, then markdown sections completed, then signal
`HANDOFF_NEEDED: <path>` and stop.

## Log line for `meta/agents.md`

`Vendor Researcher (Sonnet 4.6) — wrote vendors/<VENDOR_SLUG>.md + N rows appended to vendor-capabilities.csv. M citations. Status: OK.`

## Acceptance criteria

- Every NHI in the taxonomy has a row (or `N/A` if the vendor doesn't
  even claim to address that NHI bucket).
- Every UC has a row.
- ≥ 80 % of rows have a primary-source citation; the rest carry
  `[INDUSTRY-CONSENSUS]` tags.
- `evidence_quote` never exceeds 30 words (copyright caution).
- CSV header is present exactly once at the top of the file.

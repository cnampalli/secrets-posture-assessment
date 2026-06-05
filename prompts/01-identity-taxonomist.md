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

## What counts as an NHI (MANDATORY definition gate)

Anchor every row to the **official** definitions, not vendor marketing:

- **NIST / CNSSI 4009-2015 — Non-Person Entity (NPE):** "an entity with a digital
  identity that *acts in cyberspace, but is not a human actor*."
- **OWASP NHI (2025):** NHIs are software / workload / service identities **not
  intrinsically tied to a human**; they *use* credentials (passwords, certificates,
  tokens, **keys**) — a key/token is **a credential, not an identity**. Human use of
  an NHI is the OWASP **NHI10:2025** risk, not a separate identity class.

Apply three litmus tests to every candidate and record the verdict in `npe_conformance`:

1. **Acts AND non-human?** If the actor is a person (HSM/KMS operators, CA RA/admin,
   break-glass quorum holders), it is a **HUMAN** identity → tag `HUMAN-IDENTITY`; keep
   only for traceability and scope its governance to the human-IAM / PAM track. The
   non-human counterpart (e.g. the KMS auto-unseal principal, the issuing-CA signing
   identity) is the real NHI.
2. **Identity, not credential?** A cryptographic / TDE / master key is a **secret** —
   model the controlling *principal*, not the key. Tag a conflation `CREDENTIAL-NOT-IDENTITY`.
3. **A distinct entity, not a programme/attribute?** Crypto-agility / PQC migration
   spans existing PKI identities and is **not its own NHI** → tag `CROSS-CUTTING-ATTRIBUTE`.

Conforming rows are `CONFORMANT`; a non-human account whose defining risk is human use is
`HUMAN-USE-ANTIPATTERN`. Full worked findings: `matrix/REGULATOR-AUDIT-2026-06-03.md` Part 2.

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
nhi_id,bucket,short_name,description,typical_secrets,lifecycle,governance_maturity,sources_likely,citation_keys,npe_conformance
```

- `nhi_id` — `NHI-001`, `NHI-002`, … stable, zero-padded.
- `bucket` — `COMMON` | `UNCOMMON`.
- `lifecycle` — `EPHEMERAL` | `SHORT-LIVED` | `LONG-LIVED` | `STATIC`.
- `governance_maturity` — `LOW` | `MEDIUM` | `HIGH`.
- `sources_likely` — `Y` / `N` / `MAYBE` based on FI norms (not confidential
  XYZ knowledge — base on public banking patterns). **(Column was renamed from
  the legacy `sources_at_anz_likely`; the validator rejects the old name.)**
- `citation_keys` — semicolon-separated BibTeX keys.
- `npe_conformance` — verdict from the definition gate above: `CONFORMANT` |
  `HUMAN-IDENTITY` | `CREDENTIAL-NOT-IDENTITY` | `CROSS-CUTTING-ATTRIBUTE` |
  `HUMAN-USE-ANTIPATTERN`. **Do not delete or renumber existing `nhi_id`s — they
  are foreign keys referenced across the matrices, UCs and PRD; fix meaning, not IDs.**

## Sources to cite (primary)

- **NIST / CNSSI 4009 Non-Person Entity (NPE) definition** — `csrc.nist.gov/glossary/term/non_person_entity` (the definitional anchor).
- **OWASP Non-Human Identities Top 10 (2025)** — `owasp.org/www-project-non-human-identities-top-10/2025/`.
- **NHIMG (Non-Human Identity Management Group)** — leading independent NHI authority;
  originated the NHI Top-10 OWASP standardised. Its **three-elements** model (consumer =
  the identity · secret = the credential · entitlements = the permissions) is the litmus
  for "is this row a *consumer*, or just a secret/programme?". `nhimg.org`.
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
- **Every row carries an `npe_conformance` verdict** from the definition gate;
  human-operator, key-not-identity, and PQC-migration rows are tagged accordingly
  (not silently listed as clean NHIs).
- Every row in the markdown has a stable `NHI-<ID>` matching the CSV.
- Every claim carries either a citation URL or a tag.
- CSV parses cleanly (UTF-8, no embedded newlines in cells, commas
  escaped via double-quotes).
- Citations appended to `meta/citations.bib`.

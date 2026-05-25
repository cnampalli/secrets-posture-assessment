# Prompt 05 — Adversary TTP Mapper

**Role:** sub-agent.
**Subagent type:** `general-purpose` (must have `WebSearch`).
**Model:** **Opus 4.7**.
**Concurrency:** serial (one agent).
**Version:** v0.1 (2026-05-20).

---

## Objective

Produce the **adversary context** for the PRD:

1. **MITRE ATT&CK T1552 family** + adjacent techniques (T1528,
   T1078.004, T1606.002, T1098.001, T1199, T1539, T1556.006) detailed
   for secrets / machine-identity contexts.
2. **Recent breach post-mortems** where secrets / machine identities
   were the proximate or contributing cause.
3. **Mapping** of each TTP and each breach to the project's UCs and NHIs
   — so the PRD can claim "this UC mitigates this TTP" or "this NHI
   was the breach vector in incident X".

## Inputs

- `prompts/README.md` (invariants).
- `research/identity-taxonomy.md`.
- `research/use-cases.md`.
- `reference-external-frameworks` memory entry (breach list seed).
- `meta/citations.bib` (append to).

## Outputs (write directly)

- `research/adversary/mitre-attack-t1552-family.md`
- `research/adversary/breach-postmortems.md`
- Append rows to `matrix/regulatory-trace.csv` with
  `framework_slug=mitre-attack` (so adversary TTPs join the same trace
  table as regulatory controls).

## Markdown schema — `mitre-attack-t1552-family.md`

```
# MITRE ATT&CK — T1552 Credential Access and Related Techniques

Mapped by: Opus 4.7 (prompt 05 v0.1)

## 1. Why this lens (≤ 150 words)
Why secrets-management posture must be evaluated against adversary TTPs.

## 2. T1552 sub-techniques in scope
For each (.001 through .008, plus the adjacent techniques above):
### <Code> — <Title>
- **Definition:** ≤ 40 words from primary source.
- **Real-world examples (≤ 2):** breach references where this was used.
- **NHIs especially exposed:** `NHI-XXX, …`.
- **UCs that mitigate:** `UC-F-XXX, UC-N-XXX, …`.
- **Coverage maturity 0–4 needed to credibly mitigate.**
- **Citation:** primary-source URL.

## 3. Adjacent techniques (T1528, T1078.004, T1606.002, T1098.001, T1199, T1539, T1556.006)
Same schema as §2.

## 4. Cross-cutting observations (≤ 250 words)
What clusters of TTPs are mitigated by the same UCs (e.g., short-lived
creds mitigate T1552.001 + T1552.004 + T1078.004 simultaneously).

## 5. Open questions
≤ 8 bullets.

## 6. Citations
BibTeX keys appended to `meta/citations.bib`.
```

## Markdown schema — `breach-postmortems.md`

```
# Breach Post-Mortems Relevant to Secrets / Machine-Identity Management

Mapped by: Opus 4.7 (prompt 05 v0.1)

For each of (Okta Oct 2023, Okta Jan 2022, Cloudflare Nov 2023, CircleCI
Jan 2023, Internet Archive Oct 2024, Sourcegraph Aug 2023, LastPass Aug
2022 & Nov 2022, xz-utils Mar 2024, SolarWinds, Microsoft Storm-0558,
Uber 2022, Toyota source-leak, Sumo Logic Nov 2023, MOVEit 2023,
Snowflake-related 2024):

## <Breach short name> — <YYYY-MM>
- **Vector (≤ 30 words):** what happened.
- **Secrets / NHIs at root cause:** `NHI-XXX, …`.
- **MITRE ATT&CK techniques exercised:** `T1552.x, T1078.004, …`.
- **UCs that — if matured — would have detected or prevented:** `UC-XXX, …`.
- **Authoritative source (≤ 2 URLs):** vendor post-mortem, regulator
  filing, or industry-standard incident report.
- **Quote (≤ 30 words):** verbatim attribution.

[≥ 12 breaches required.]

## Cross-incident pattern observations (≤ 400 words)
- Which NHI types appear most often.
- Which UCs would have had the highest aggregate impact.
- AU-relevant breaches (any?).
```

## CSV rows to append (`matrix/regulatory-trace.csv`)

One row per MITRE TTP, with `framework_slug=mitre-attack`,
`framework_role=ADVERSARY-LENS`, `control_code=<T-code>`,
`control_short_title=<TTP title>`, etc. Same columns as the regulatory
mapper.

## Sources policy

- MITRE ATT&CK: `attack.mitre.org` (canonical).
- Breach post-mortems: vendor's own incident write-up first; only fall
  back to industry analysis if the vendor hasn't published.
- Mandiant, Unit 42, CrowdStrike write-ups are tertiary — mark as
  `[INDUSTRY-CONSENSUS]` if they're the only source.

## Token budget

≤ 4,500 words across both markdown files.

## Sensitivity policy (Invariant #7)

`[PUBLIC]` only. Cite incidents already in the public record.

## 70% checkpoint-and-handoff (Invariant #8)

Checkpoint file: `research/adversary/_checkpoint-<NNN>.md`.

## Log line for `meta/agents.md`

`Adversary TTP Mapper (Opus 4.7) — wrote mitre-attack-t1552-family.md + breach-postmortems.md + N CSV rows. M citations. Status: OK.`

## Acceptance criteria

- All 8 T1552 sub-techniques + 7 adjacent techniques covered.
- ≥ 12 breach post-mortems.
- Every TTP and every breach maps to ≥ 1 UC and ≥ 1 NHI.
- Every quote ≤ 30 words.
- CSV rows appended without disturbing existing rows.

# Secrets-Management-for-Machine-Identities — PRD Project (XYZ FI v0.1)

> **Status:** **PRD v0.1 ready** — Milestones 1, 2, 3 all complete (2026-05-23).
> **Stakeholder review:** **Mon 2026-05-25**.
> **Deep-dive v1.0:** week of **2026-05-26** (after stakeholder input).
>
> **Note:** `GEMINI.md` in this directory is a legacy stub from a prior
> session and is **superseded by this README**. Do not treat it as authoritative.

## What this project produces

A **Product Requirements Document (PRD)** whose "product" is a **Report** on
**secrets management positioning across all machine identities** for the
**XYZ Bank** stakeholder context, with two linked outputs:

1. **Universal buyer's framework** — comprehensive use cases (functional +
   non-functional) crossed with a comprehensive **non-human identity (NHI)
   taxonomy**, with **12+ vendor evaluations** (HashiCorp Vault Enterprise,
   CyberArk Conjur, Delinea Secret Server, AWS Secrets Manager, Azure Key
   Vault, GCP Secret Manager, AKEYLESS, Doppler, Infisical, 1Password Secrets
   Automation, Venafi, Keyfactor).
2. **XYZ current-state gap assessment** — does XYZ's existing deployment meet
   each use case? Evidence + gap notes for stakeholders.

**Primary regulatory lens:** Essential 8 maturity + CISA Zero Trust Maturity
Model v2.0 (aligned to NIST SP 800-207; outcomes-first), back-mapped to APRA
CPS 234 / CPS 230 / CPG 234, ASD ISM. NIST CSF 2.0 deferred to v1.0.

**Adversary lens:** MITRE ATT&CK T1552 family + recent secrets-related
breach post-mortems (Okta, Cloudflare, CircleCI, Internet Archive,
Sourcegraph, LastPass).

## Workflow plan

The approved plan lives at
[`/Users/cnampalli/.claude/plans/wondrous-meandering-yao.md`](file:///Users/cnampalli/.claude/plans/wondrous-meandering-yao.md)
and is mirrored project-locally at [`meta/workflow.md`](./meta/workflow.md).

## Three milestone gates

| # | Gate | Target | Status | Deliverables |
|---|---|---|---|---|
| M1 | Outline + scaffolding | Thu 2026-05-21 | ✓ done 2026-05-21 | Task 0 questionnaire, identity taxonomy (37 NHIs), use-case catalog (47 UCs), PRD skeleton, 10 sub-agent prompts |
| M2 | Matrices populated | Sat 2026-05-23 | ✓ done 2026-05-23 (PASS-with-comments → fixes applied) | **19** vendor profiles, 4 regulatory mappings (NIST CSF 2.0 deferred), adversary research, master CSV (1596 rows) + matrix.md + HTML viewer, XYZ current-state (47 UCs scored) |
| M3 | PRD v0.1 ready | Sun 2026-05-24 | ✓ done 2026-05-23 (one day ahead) | PRD-FI-v0.1.md (7,884 words, 20 sections) + ADR-001..006 + Appendices A-D (~20,500 words total package) |

## Directory map

```
research-papers/
├── README.md                          ← you are here
├── CHANGELOG.md                       version log per milestone
├── GEMINI.md                          (legacy stub; superseded)
│
├── PRD/                               main deliverable + ADRs + appendices
│   ├── PRD-FI-v0.1.md
│   ├── adrs/
│   └── appendices/
│
├── task0/                             user-supplied context (fill async)
│   ├── questionnaire.md               ★ fill this in
│   ├── responses.md                   ← your answers go here
│   └── README.md
│
├── prompts/                           documented sub-agent prompts (audit trail)
│
├── research/                          sub-agent research outputs
│   ├── identity-taxonomy.md
│   ├── use-cases.md
│   ├── vendors/
│   ├── regulatory/
│   └── adversary/
│
├── matrix/                            CSV + markdown + HTML matrices
│
├── meta/                              workflow + agent catalog + memory index + citations
│
└── notes/                             running working-notes (decisions flush into ADRs)
```

## Sub-agent strategy

Every sub-agent has a versioned prompt in `prompts/` and writes its own
output. Models assigned per role (Opus 4.7 for synthesis/taxonomy/regulatory
reasoning; Sonnet 4.6 for high-volume vendor doc summarisation). See
[`meta/agents.md`](./meta/agents.md) for the running invocation log.

## "Cloud save everything" — implementation

- **Local:** everything under this directory.
- **iCloud / Drive sync:** assumed configured at OS level for
  `Desktop/Projects/DE/`. (If not, will be flagged in `notes/decisions.md`.)
- **Claude persistent memory:** mirrored entries listed in
  [`meta/memory-index.md`](./meta/memory-index.md).

## Task 0 — context capture (complete)

[`task0/responses.md`](./task0/responses.md) captures the user's prior
context from the live 1-hour interactive session on 2026-05-22. All 11
sections (A-K) covered. Drives the XYZ-side narrative in PRD §12 and the
synthesised evidence file
[`research/anz-current-state-evidence.md`](./research/anz-current-state-evidence.md).

## Reading order for Monday stakeholder review

> **Read this first:** **18 ranked vendors** sit across **two comparison
> layers** — L1 secrets management (the vault tier) and L2 NHI governance
> (above the vault) — and a `NATIVE` score means a *different thing* in
> each (rank within a layer, compose across). Beneath them is a **Layer-0
> crypto-substrate dependency** (the HSM/key-root; XYZ's SafeNet→Fortanix
> migration) — a dependency you *pair* with the vault, **not ranked**
> against it. On confidence: capability existence is vendor-doc-cited,
> **maturity scores are analyst judgment (not independently verified)**,
> and some GA dates are unverified roadmap. See PRD §9 (stack model + §9.x
> substrate), §8.1 (sourcing & confidence), and
> [ADR-007](./PRD/adrs/ADR-007-reading-model-and-confidence.md).
>
> **Fastest way in:** open
> [`matrix/domains/secrets/secrets-report.html`](./matrix/domains/secrets/secrets-report.html) — it opens on
> an XYZ-posture dashboard; click any gap to jump to that use case's
> decision card (best-fit vendors + where XYZ stands + the recommended
> action).

For a **30-minute exec read**:

1. This README (~5 min).
2. [`PRD/PRD-FI-v0.1.md`](./PRD/PRD-FI-v0.1.md) §1 Executive summary + §8.1 sourcing & confidence (~5 min).
3. [`PRD/PRD-FI-v0.1.md`](./PRD/PRD-FI-v0.1.md) §9 (three-layer matrix) + §11 (vendor findings) + §12 (XYZ findings) + §16 (recommendations) (~13 min).
4. [`matrix/domains/secrets/secrets-report.html`](./matrix/domains/secrets/secrets-report.html) — the interactive report: **XYZ posture dashboard** → click a gap → **use-case decision card** (best-fit vendors by layer + XYZ state + recommended action); "By identity" and "Browse all" tabs for deeper digging; hover any NHI/UC/coverage code for its definition (~7 min).

For a **deeper architecture read** (≥ 2 hours):

1. Full [`PRD/PRD-FI-v0.1.md`](./PRD/PRD-FI-v0.1.md) (~45 min).
2. [`PRD/adrs/`](./PRD/adrs/) — 7 ADRs (007 = three-layer reading model + confidence policy) (~22 min).
3. [`PRD/appendices/`](./PRD/appendices/) — A (compliance trace), B (vendor index, now layer-tagged), C (glossary), D (adversary) (~30 min).
4. [`matrix/matrix.md`](./matrix/matrix.md) cross-vendor summary — §0 stack model + §1 layer-grouped coverage (~10 min).
5. [`research/anz-current-state-evidence.md`](./research/anz-current-state-evidence.md) (~15 min).

For **vendor procurement / RFP basis**:

1. [`PRD/appendices/B-vendor-profiles-index.md`](./PRD/appendices/B-vendor-profiles-index.md) — strengths + gaps per vendor.
2. [`research/vendors/`](./research/vendors/) — 19 detailed vendor profiles.
3. [`matrix/domains/secrets/vendor-capabilities.csv`](./matrix/domains/secrets/vendor-capabilities.csv) — 1596-row capability matrix for pivot-table analysis.
4. [`matrix/domains/secrets/regulatory-trace.csv`](./matrix/domains/secrets/regulatory-trace.csv) — UC ↔ control-framework back-map.

For **audit / compliance review**:

0. [`matrix/domains/secrets/secrets-report.html`](./matrix/domains/secrets/secrets-report.html) → **Compliance trace** tab — cascade from any APRA CPS 234 / ASD ISM / E8 / ZT control → the use cases it demands → vendor evidence, in three clicks. Each use-case card also shows its mapped APRA + ISM controls.
1. [`PRD/appendices/A-compliance-traceability.md`](./PRD/appendices/A-compliance-traceability.md) — full E8/ZT/CPS 234/ISM trace.
2. [`PRD/adrs/ADR-005-anz-evidence-policy.md`](./PRD/adrs/ADR-005-anz-evidence-policy.md) — sensitivity policy.
3. [`meta/review-M2-2026-05-23.md`](./meta/review-M2-2026-05-23.md) — independent reviewer's M2 verdict + recommended actions.

## Sharing this with the stakeholder

The interactive report is **one self-contained file** —
[`matrix/domains/secrets/secrets-report.html`](./matrix/domains/secrets/secrets-report.html) — with all data
baked in. No server, no internet, nothing to install.

- **Email:** attach `secrets-report.html` directly. The recipient saves it
  and **double-clicks to open in any browser** (Chrome / Edge / Safari),
  fully offline. That single file is the whole stakeholder experience —
  dashboard, decision cards, and the full matrix.
- **PRD narrative:** the prose lives in `PRD/PRD-FI-v0.1.md` (Markdown).
  Either share the repo/folder (zip `research-papers/`), view on an
  internal Git host, or render to **PDF** (e.g. `pandoc PRD/PRD-FI-v0.1.md
  -o PRD-FI-v0.1.pdf`, or VS Code "Markdown PDF") if a printable is wanted.
- **One-bundle option:** zip the whole `research-papers/` directory so all
  cross-links (PRD → ADRs → appendices → matrix → viewer) resolve locally.

> **Sensitivity (important):** the report carries an **INTERNAL** banner and
> includes `[INTERNAL]` XYZ current-state findings (ADR-005). The
> distribution surface is **internal-only** pending open question **O2** —
> share within XYZ, **not** with external vendors or third parties. If an
> external-safe version is needed, ask and we'll generate one with the
> XYZ panels stripped/paraphrased.

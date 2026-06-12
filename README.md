# Identity-Security Posture & Vendor-Selection Instrument

A **reusable, client-ready instrument** that assesses an organisation's
identity-security **posture** and turns the gaps into a **vendor-selection**
decision-support view — across **three domains** on one platform:

| Domain | What it covers | Scope |
|---|---|---|
| **Secrets** | Secrets management for machine / non-human identities (NHI) | 47 use cases · 19 vendors |
| **PAM** | Privileged access management | 18 use cases · 10 vendors |
| **IGA** | Identity governance & administration (process-shaped) | 16 use cases · 8 vendors (per-area fit) |

Each domain produces a **single, self-contained HTML report** (no server, no
internet, nothing to install) plus a **cross-domain consolidation** view. The
assessment is the wedge: its GAP / PARTIAL / PENDING findings are the engagement
menu, re-run over time for recurring value. **Not** a hosted multi-tenant SaaS —
self-hosted / local only (centralising multiple FIs' gap data is a liability).

> The demo data shipped in this repo is **illustrative** and labelled as such in
> every report; a real engagement supplies its own current-state inputs.

## Open a report (the fastest way in)

Double-click any of these in a browser (Chrome / Edge / Safari) — fully offline:

- `matrix/domains/secrets/secrets-report.html`
- `matrix/domains/pam/pam-report.html`
- `matrix/domains/iga/iga-report.html`
- `matrix/cross-domain-report.html` — concentration / ownership across domains

Each report opens on a **posture dashboard**; click any gap to jump to that use
case's **decision card** (best-fit vendors + where you stand + recommended
action). "By identity", "Compliance trace", and "Browse all" tabs go deeper;
hover any NHI / UC / control code for its definition.

**Reading model & confidence:** capability *existence* is vendor-doc-cited;
*maturity* scores are analyst judgment (not independently verified). Ownership /
M&A facts are point-in-time and carry per-edge confidence + a verify link. See
`PRD/adrs/ADR-007-reading-model-and-confidence.md`.

## Build the reports

```bash
pip install -r requirements.txt          # PyYAML
python3 matrix/build_matrix_viewer.py --domain secrets   # → matrix/domains/secrets/secrets-report.html
python3 matrix/build_matrix_viewer.py --domain pam
python3 matrix/build_matrix_viewer.py --domain iga
python3 matrix/build_cross_domain.py     # → matrix/cross-domain-report.html
```

The reports are **byte-deterministic** (a frozen snapshot test proves it). The
React questionnaire app (intake front door) lives in `app/` (`npm ci && npm run build`).

## Data integrity (the gates)

Everything is contract-checked. `python3 matrix/validate_data.py [--data-dir matrix/domains/<slug>]`
runs the build-failing gates:

- **Schema + referential** integrity across the five-table star schema.
- **Provenance (F1–F4):** source dating + tiering, control-ID registry (no fabricated
  control IDs), every capability claim cited, **citation keys resolve** to `meta/citations.bib`.
- **Data currency:** facts fail the build past a per-tier max age.
- **Semantic control registry:** a control's recorded text must match what the control
  is *about* (kills the right-ID-wrong-text class).
- **Ownership:** every acquisition edge cites a primary source; only HIGH-confidence
  ownership collapses sibling brands in the concentration math.
- **Aggregate ↔ per-vendor consistency:** the denormalised matrix can't drift from its
  per-vendor sources.

`matrix/check_links.py` is a report-only link-rot + quote-presence checker run on the
refresh cadence. CI (`.github/workflows/ci.yml`, mirrored in `.gitlab-ci.yml`) runs
all gates + the Python and app test suites + report byte-identity on every push.

## Methodology

A scoring **rubric** (archetype library A0–A8) under `methodology/` proposes each
use case's state; the assessor confirms / overrides with rationale + confidence.
The Python reference (`methodology/scoring.py`) and the two JS mirrors
(`questionnaire/scoring.js`, `app/src/assessment/scoring.ts`) are pinned in lockstep
by `questionnaire/scoring-vectors.json`. Regulatory coverage is a **selectable
overlay** — 13 frameworks registered (Essential 8, CISA ZTMM v2, APRA CPS 234 / 230,
ASD ISM, NIST 800-53, ISO 27001, SOX, MITRE ATT&CK, OWASP), scoped to the identity
slice; output is an **identity-control coverage indicator, not a compliance score**.

## Layout

```
matrix/            build engine, per-domain data (matrix/domains/<slug>/), config, gates
methodology/       archetype scoring rubric + validator
questionnaire/     intake → record → report adapter + JS scoring mirror
app/               React questionnaire SPA (domain-aware) + vitest suite
PRD/               narrative PRD + ADRs + appendices
research/          per-domain research outputs + citation ledgers
docs/              ADRs, the multi-domain roadmap, and the superpowers plans
meta/              citations.bib, audit + review records, agent log
```

## Resuming / contributing

- **`HANDOFF.md`** is the resume doc (source of truth across machines).
- **`docs/superpowers/MULTI-DOMAIN-ROADMAP.md`** is the status board + remaining phases.
- Plans and design specs live in `docs/superpowers/plans/` and `docs/adr/`.

## Sharing a report

The report is **one self-contained file** with all data baked in. Email it, or
**zip the whole repo** so cross-links (PRD → ADRs → appendices → matrix → report)
resolve locally. Reports carry an **INTERNAL** banner and may include current-state
findings (ADR-005 sensitivity policy) — keep distribution internal; ask for an
external-safe variant if needed.

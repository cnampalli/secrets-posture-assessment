# HANDOFF — resume here (cross-laptop)

**Last updated:** 2026-06-10. **Repo:** `cnampalli/secrets-posture-assessment`.
This file is the source of truth when resuming on another machine — the Claude session memory
(`~/.claude/.../memory/`) and the working plan (`~/.claude/plans/`) are **laptop-local and do NOT travel
via git**. Everything you need to resume is here + in `docs/superpowers/plans/`.

## What this project is
A multi-domain identity-security **posture + vendor-selection assessment instrument** (CSV-driven Python
→ one self-contained offline HTML report per domain). Domains: **secrets** (NHI/secrets-management),
**pam** (privileged access), **iga** (identity governance). Plus a React questionnaire app in `app/`.
Jurisdiction: AU-primary (APRA CPS 234 / ASD ISM / Essential 8) + NIST/ISO/SOX where relevant.
Honesty is core: **no invented numbers, no fabricated control mappings** (the project once shipped a
fabricated ISM mapping — anti-fabrication guards in `matrix/validate_data.py` exist because of it).

## Current state (2026-06-10)
- **`main`** = `b37b50e` — **IGA domain merged (PR #22)**. Three domains live: secrets (47 UCs, ~19
  vendors), pam (17 UCs, 6 vendors), iga (13 UCs, 4 vendors, bespoke per-area vendor-fit).
- **PR #23 OPEN** — branch **`feat/value-proposition-reporting`** (pushed to origin). Adds a curated
  in-report **Value Proposition** view (board ML1/2/3 maturity roll-up, top-priorities, defensibility/
  independence/currency callouts) to all 3 reports + illustrative mock posture for PAM/IGA. Gates passed:
  code-review approved; instrument-review Buy-with-conditions (all conditions closed); pytest 274 / app
  vitest 63 green. **→ Review & merge this first on resume.**

### ⚠️ Resume step 1 — re-establish the value-prop branch on the new laptop
The `../valueprop` git worktree is laptop-local; the **branch is on origin**. On the new machine:
```bash
git clone <repo>            # or: git fetch origin
git checkout feat/value-proposition-reporting   # the PR #23 branch
# review/merge PR #23 via GitHub, then on main:
git checkout main && git pull
```
(No need to recreate the worktree — just check out the branch. If you used a worktree before,
`git worktree remove ../valueprop` only matters on the old laptop.)

## Parked next work (approved, NOT started) → `docs/superpowers/plans/2026-06-10-vendor-accuracy-naming.md`
Four sequenced workstreams answering a buyer-DD review of the demos. **Start after PR #23 merges**, off
updated `main`, in an isolated worktree, agent-driven with the `code-review` + `instrument-review-methodology`
+ `grill-me` gate per phase:
1. **WS1 — IGA regulatory/validator debt.** Clear the 46 IGA `validate_data` violations (register IGA's
   7 frameworks in `control-id-registry.yaml` + `data-provenance.yaml`; whitelist `INFORMATIVE`/
   `THREAT-CONTEXT` roles + `scope` dimension in `validate_data.py`; fix the ISO A.5.18 secondary-quote).
   These are **schema-registration gaps, not fabrication**. Do NOT weaken the validator.
2. **WS2 — Use-case gap-fill.** IGA 13→16 (request-recert, self-approval-prevention, unstructured-data);
   PAM 17→18 (SAW/PAW tier-0). Watch the UC-count ripple (`test_iga_spike`, rubric JSON, app tests, mocks).
3. **WS3 — Vendor expansion to leader parity** (citation-backed, adversarially verified). PAM 6→~10
   (StrongDM, Britive, Apono, Netwrix); IGA 4→~8 (Omada, ConductorOne, Lumos, Zilla/CyberArk). Document
   CrowdStrike/Cisco as **adjacent** (ITDR/DSPM/CIEM), not core.
4. **WS4 — Report naming standardization.** Move all reports to `matrix/domains/<slug>/<slug>-report.html`
   (relocate secrets data + output too). Highest-coordination; do last.

Beyond this plan, the longer roadmap (`docs/superpowers/MULTI-DOMAIN-ROADMAP.md`) has: **Phase 5**
(consulting wrap: workspace/import/benchmark) + **WS-2 selectable-overlay engine** (Phase 4 Workforce IAM
PARKED).

## How to run / verify (from repo root)
```bash
python3 -m pytest -q                                  # full suite (274 on the value-prop branch)
python3 matrix/validate_data.py                       # data gate (IGA has 46 known violations → WS1)
python3 matrix/build_matrix_viewer.py --domain secrets|pam|iga   # build a domain report
python3 questionnaire/emit_rubric.py                  # regenerate app rubric JSON
cd app && npm install && npm test && npm run build     # React app (node_modules not committed)
```
Reports today: secrets `matrix/matrix-viewer.html`; pam `matrix/domains/pam/pam-report.html`; iga
`matrix/domains/iga/iga-report.html` (WS4 will standardize these names).

## Key references
- Roadmap/status: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`
- Review lens: `methodology/INSTRUMENT-REVIEW-METHODOLOGY.md`; dated reviews in `meta/`
- IGA research provenance: `research/iga/RESEARCH-SUMMARY.md`
- Parked plan: `docs/superpowers/plans/2026-06-10-vendor-accuracy-naming.md`

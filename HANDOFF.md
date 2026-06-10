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

## Current state (2026-06-11)
- **`main`** = `17c20f4` — PR #22 (IGA domain) and PR #23 (value-prop view) both **merged**. Three
  domains live: secrets (47 UCs, ~19 vendors), pam (17 UCs, 6 vendors), iga (13 UCs, 4 vendors,
  bespoke per-area vendor-fit).
- **WS1 DONE on this branch (`feat/ws1-iga-validator-debt` → PR #24).** All 46 IGA `validate_data`
  violations cleared WITHOUT weakening the gate. Source re-verification caught **two
  fabrication-class control-ID errors** (ISM-1591→ISM-0430 same-day removal; ISM-1648→ISM-1404
  unprivileged 45-day) — full evidence + deferred follow-ups in
  `docs/superpowers/plans/ws1-verification-notes.md`. Validator now: descriptor-declared matrix-less
  domains (`iga.yaml: vendor_fit`), citation-gated fit grid, cross-domain pytest gate over
  `domains.DOMAINS`. pytest 308 / vitest 63 green; validate_data clean ×3 domains.
  **→ If PR #24 is still open on resume, review & merge it first, then start WS2.**

## Workstream plan → `docs/superpowers/plans/2026-06-10-vendor-accuracy-naming.md`
Four sequenced workstreams answering a buyer-DD review of the demos. Each off updated `main`, in an
isolated worktree, agent-driven with the `code-review` + `instrument-review-methodology` + `grill-me`
gate per phase:
1. **WS1 — IGA regulatory/validator debt. ✅ DONE (PR #24, 2026-06-11).** Outcome differed from the
   original framing: mostly schema-registration gaps as expected, but verification found two
   genuinely wrong ISM control IDs (fixed) and the ISO A.5.18 fix had already landed via PR #23.
   WS2 inherits two small data follow-ups (backmap_codes style drift; dangling `iso-27001-a5-18`
   citation key) — see the deferred list in `ws1-verification-notes.md`.
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

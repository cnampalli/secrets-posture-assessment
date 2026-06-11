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

## Current state (2026-06-11) — **ALL FOUR WORKSTREAMS COMPLETE**
- **`main`** = `822833b` — PRs #22 (IGA), #23 (value-prop), #24 (WS1), #25 (WS2), **#26 (WS3)**
  all **merged**. Domains: secrets (47 UCs, ~19 vendors), pam (18 UCs, 10 vendors), iga (16 UCs,
  8 fit-grid vendors).
- **WS1 DONE (PR #24):** 46 IGA validator violations cleared; two fabrication-class control-ID
  fixes (ISM-1591→ISM-0430, ISM-1648→ISM-1404) — `docs/superpowers/plans/ws1-verification-notes.md`.
- **WS2 DONE (PR #25):** IGA 13→16, PAM 17→18 (UC-P-018 SAW/PAW; ISM-1898/1380/1175 registered) —
  `docs/superpowers/plans/ws2-research-notes.md`.
- **WS3 DONE (PR #26):** PAM 6→10 + IGA 4→8 vendors, adversarially citation-verified (8 ledgers in
  `docs/superpowers/plans/ws3-research/`); ownership graph strongdm→delinea (closed 2026-03-05) +
  zilla→cyberark (2025-02-13); Britive/BeyondTrust acquisition REFUTED. ⚠️ Britive evidence is
  marketing-tier — re-anchor to admin docs before client use.
- **WS4 DONE on this branch (`feat/ws4-report-naming`).** All three reports standardized at
  `matrix/domains/<slug>/<slug>-report.html`; secrets data relocated to `matrix/domains/secrets/`
  (25 CSVs, git-mv); `matrix-viewer.html` retired; `validate_data` no-arg default resolves secrets
  via the descriptor; consumers repathed (exec-summary, roadmap, stakeholder pack, package.sh,
  methodology validators); value-tab → vendor-tabs pointer added. Bonus: the old matrix-viewer
  rebuild nondeterminism does NOT reproduce at the new path (byte-stable across rebuilds).
  Gates: pytest 308 / validate_data ×3 clean / vitest 63 / package.sh produces the secrets report.
  **→ If the WS4 PR is open on resume, review & merge it. The buyer-DD plan is then fully shipped;
  next frontier per `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`: Phase 5 (consulting wrap:
  workspace/import/benchmark) + WS-2 selectable-overlay engine (Phase 4 Workforce IAM stays
  demand-pulled).**

## Workstream plan → `docs/superpowers/plans/2026-06-10-vendor-accuracy-naming.md`
Four sequenced workstreams answering a buyer-DD review of the demos. Each off updated `main`, in an
isolated worktree, agent-driven with the `code-review` + `instrument-review-methodology` + `grill-me`
gate per phase:
1. **WS1 — IGA regulatory/validator debt. ✅ DONE (PR #24, 2026-06-11).** Outcome differed from the
   original framing: mostly schema-registration gaps as expected, but verification found two
   genuinely wrong ISM control IDs (fixed) and the ISO A.5.18 fix had already landed via PR #23.
   WS2 inherits two small data follow-ups (backmap_codes style drift; dangling `iso-27001-a5-18`
   citation key) — see the deferred list in `ws1-verification-notes.md`.
2. **WS2 — Use-case gap-fill. ✅ DONE (this branch, 2026-06-11).** IGA 13→16 + PAM 17→18 landed with
   all ripples (test pins, rubric JSON, app tests, mocks, `_IGA_AREA_BY_NUM`, MATURITY_GROUPS,
   reports). Notes: `test_iga_spike` pins the spike dir, not production — no change needed; one
   extra pin found in `app/src/assessment/store.test.tsx`. Known pre-existing non-blockers:
   `ms-pth-mitigation-2014` cite key bib-undefined (3 PAM rows + UC-P-018); IGA "REG-mapped UCs"
   is 15/16 by design, not a bug — UC-I-012 carries NIST/ISO back-maps only, no APRA/ISM row
   (recomputed 2026-06-11 after the CPS234-§22→§21 merge; build output confirms 15).
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
Reports today: all standardized at `matrix/domains/<slug>/<slug>-report.html` — secrets
`matrix/domains/secrets/secrets-report.html`; pam `matrix/domains/pam/pam-report.html`; iga
`matrix/domains/iga/iga-report.html` (WS4 done).

## Key references
- Roadmap/status: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`
- Review lens: `methodology/INSTRUMENT-REVIEW-METHODOLOGY.md`; dated reviews in `meta/`
- IGA research provenance: `research/iga/RESEARCH-SUMMARY.md`
- Parked plan: `docs/superpowers/plans/2026-06-10-vendor-accuracy-naming.md`

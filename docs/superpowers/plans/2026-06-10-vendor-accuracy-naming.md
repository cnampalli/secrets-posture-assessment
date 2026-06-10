# Plan — Vendor coverage + accuracy + report standardization (Secrets · PAM · IGA)

> **⏸️ STATUS: PARKED (2026-06-10) — approved in scope, NOT started.** Resume after PR #23 merges.
> This is the durable, in-repo copy of the plan (the working copy lived in a laptop-local
> `~/.claude/plans/` file). See `/HANDOFF.md` for current branch/PR state and resume steps.

## Context
A buyer-DD pass over the three demo reports (Secrets/PAM/IGA value-proposition views) surfaced five
issues. Two are answered as findings (below); four became approved workstreams. Intent: make vendor
coverage credible at analyst-leader parity, make IGA's regulatory mapping audit-defensible, fill known
use-case gaps, and standardize report naming/structure — **without weakening the anti-fabrication
guards** this project depends on (it has a fabrication history).

**Prereq:** builds on the value-prop work (PR #23). Start from a fresh worktree off `main` **after PR #23
merges** (it touches `report-template.html`, the snapshot fixture, and `report_logic.py`, which this plan
also touches). Per the project rhythm, every phase is agent-driven and gated by `code-review` +
`instrument-review-methodology` + `grill-me`; use find-skills/superpowers throughout.

### Findings that are just answers (no build)
- **"Where are the vendors?"** Vendor comparison renders in **By use case / By identity / Compliance
  trace / Browse all**, plus **Vendor-mix + Vendor-intel** (secrets/PAM) and the **per-area fit grid**
  (IGA). The **Business value** tab intentionally has none — source of the "where are the vendors?"
  confusion. A small default polish adds a pointer from the value tab to the vendor tabs.
- **CrowdStrike / Cisco** are **ADJACENT, not core**: CrowdStrike = ITDR + DSPM (Flow), Cisco = MFA/ITDR
  (Duo/Oort). Document as adjacent categories (ITDR/DSPM/CIEM/NHI-lifecycle), **not** added to the 3 domains.
- **Use-case logic** is **sound** across all three (grounded in Gartner PAM Critical Capabilities, NIST,
  OWASP, IGA JML/Cert/SoD/Role) — only the WS2 gap-fill items are missing.
- **Regulatory mapping**: secrets + PAM **clean** (pass `validate_data`, verbatim quotes); IGA honest +
  verbatim-cited but in **validator debt** — 46 violations = schema-registration gaps, **not fabrication**
  → WS1.

### Locked scope (from the user)
- Vendor expansion: **IGA + PAM to leader parity** — IGA 4→~8 (Omada, ConductorOne, Lumos, Zilla/CyberArk);
  PAM 6→~10 (StrongDM, Britive, Apono, Netwrix). Secrets unchanged (already ~19, deep).
- Naming: **standardize all reports under `matrix/domains/<slug>/<slug>-report.html`** (move secrets too).
- Workstreams: all four below + the value-tab pointer polish.

## Honesty guardrails (non-negotiable, all phases)
- **No fabricated vendors, capabilities, control IDs, or quotes.** Every new vendor capability/fit cell
  carries an authoritative `evidence_url` + verbatim `evidence_quote` (or explicit inference tag),
  researched and **adversarially citation-verified** (the IGA-build Workflow pattern: fetch every URL,
  confirm every quote, reject unverifiable). `validate_data.check_provider_claims_cited` must pass.
- Honest source-confidence (layered, no flat "buy X" ranking; mark marketing-grade vs admin-doc).
- **Do not weaken the validator** to clear IGA debt — *register* the real frameworks and *whitelist the
  documented intentional roles*, don't bypass the gate.

---

## WS1 — IGA regulatory / validator debt (FIRST; foundational)
Clears the 46 IGA `validate_data` violations so IGA is audit-defensible before more IGA data is added.
- **Register IGA frameworks** in `matrix/config/control-id-registry.yaml`: `nist-800-53r5`,
  `iso-27001-2022`, `sox`, `sox-icfr`, `owasp-llm`, `ms-incident` (+ confirm `apra-cps234`/`apra-cpg234`
  slug spellings match the IGA trace) with verified control codes + format patterns.
- **Add provenance** for those frameworks in `matrix/config/data-provenance.yaml` (`as_of` + `source_tier`
  + owner).
- **Whitelist intentional tokens** in `matrix/validate_data.py`: add `INFORMATIVE` + `THREAT-CONTEXT` to
  the role enum and `scope` to the evidence-dimension enum (deliberate, documented IGA choices) — keep
  them EXCLUDED from evidence-pack binding (only PRIMARY-LENS/BACK-MAP bind).
- **MUST-FIX ISO A.5.18** in `matrix/domains/iga/regulatory-trace.csv`: secondary-mirror verbatim quote
  while labelled BACK-MAP → withhold quote, ISO landing-page URL, note "secondary; re-verify vs licensed
  ISO" (matching A.5.16/15/3). *(Verify against merged main — may already be addressed on PR #23.)*
- **Header-only `vendor-capabilities.csv`** (IGA matrix-less): keep the matrix-less handling; ensure
  `validate_data` treats header-only as intentional, not a violation.
- **Verify:** `python3 matrix/validate_data.py` → 0 IGA violations; secrets/PAM still clean; `pytest`
  green. Consider wiring `validate_data` into the test suite so this debt can't silently recur.

## WS2 — Use-case gap-fill (before WS3 — PAM vendor rows are per-UC)
- **IGA 13→16:** add request-time **recertification**, **requestor≠approver self-approval-prevention**,
  **unstructured-data / data-access entitlement governance** UCs (areas: Certification, SoD, Role/Request;
  extend `_IGA_AREA_BY_NUM` in `matrix/report_logic.py`).
- **PAM 17→18:** add discrete **SAW/PAW tier-0 isolation** UC.
- Each UC: rows in `use-cases.csv` + `uc-archetype-map.csv` + `regulatory-trace.csv` (cited) +
  `evidence-catalog.csv` + illustrative `current-state` entry.
- **Ripples (critical):** `tests/test_iga_spike.py` (pins `UC-I-001..013` → extend to 016); regenerate
  `app/src/data/rubric.{iga,pam}.json` via `emit_rubric.py`; `app/src/assessment/domains.test.ts` (iga
  13→16, pam 17→18); value-view mock records `matrix/domains/{iga,pam}/assessment-record.mock.json` +
  regenerated `current-state.csv`; `tests/fixtures/data-baseline.json` + secrets snapshot if affected.

## WS3 — Vendor expansion to leader parity (research-heavy; the big one)
Citation-backed, adversarially verified — mirror the IGA-build research Workflow.
- **PAM (+StrongDM, Britive, Apono, Netwrix Privilege Secure):** per-UC rows in
  `matrix/domains/pam/vendor-capabilities.csv` across all 18 PAM UCs (post-WS2); add to `pam.yaml`
  `vendor_layer`/`short` (StrongDM/Britive/Apono = L2 modern-access; Netwrix = L1) — **update the
  `test_domain_yaml` PAM anchor test** (pins those maps). Honest gaps (cloud-native won't be NATIVE on
  classic vaulting/session UCs).
- **IGA (+Omada, ConductorOne, Lumos, Zilla/CyberArk):** rows in `matrix/domains/iga/iga-vendor-fit.csv`
  (per-area NATIVE/PARTIAL/ADD-ON × {JML,Cert,SoD,Role/Request}, justification + cited evidence); add to
  `iga.yaml` `vendor_layer`/`short` + update the IGA anchor test + the vendor_slug⊆vendor_layer guard.
- **Adjacent-category note:** short honest "Adjacent categories (not assessed here)" callout naming
  CrowdStrike (ITDR/DSPM), Cisco (MFA/ITDR), Veza (CIEM), Astrix/Entro/Aembit (NHI-lifecycle).
- **Verify:** `validate_data` clean (all new claims cited); reports render expanded matrices/grids;
  `pytest` green.

## WS4 — Report naming / structure standardization (LAST — pure relocation)
All three at `matrix/domains/<slug>/<slug>-report.html`, including secrets.
- Relocate `matrix/{use-cases,current-state,regulatory-trace,vendor-capabilities,identity-catalog,evidence-catalog}.csv`
  → `matrix/domains/secrets/`; set `data_dir: "domains/secrets"` in `matrix/config/domains/secrets.yaml`;
  remove the secrets special-case output path in `matrix/build_matrix_viewer.py` (~lines 49-50).
- Update consumers of old secrets paths: `matrix/report_io.py`; `presentation/build_exec_summary.py`
  (hardcodes `matrix/use-cases.csv`/`regulatory-trace.csv`); `questionnaire/roadmap_generator.py`;
  `matrix/build_stakeholder_pack.py`; snapshot test path `tests/test_report_render.py` + regenerate
  `tests/fixtures/report.snapshot.html`; `package.sh`.
- Docs sweep: README, CHANGELOG, methodology/FACILITATOR-GUIDE, PRD, prompts, docs (~86 refs to
  `matrix-viewer.html`; functional ones = test, package.sh, build/exec/roadmap/stakeholder scripts).
- **Value-tab pointer polish (default):** in `report-template.html` `renderValue()` add a one-line
  pointer to the vendor tabs.
- **Verify:** all three build to new paths; `pytest` + `npm test` green; snapshot regenerated;
  `package.sh` produces the secrets report; grep shows no stale functional path refs.

## Execution model
- **Sequence WS1 → WS2 → WS3 → WS4**, each its own commit/PR on a feature branch off updated `main` in an
  isolated worktree, agent-driven (TDD) with the review gate per phase. WS3 research = adversarial
  citation-verification Workflow.
- **Per-phase gate:** `validate_data` clean; `pytest -q` green; `npm test` + `npm run build` green where
  the app changed; reports rebuilt; fixtures regenerated with intended-only diffs.

## Risks / ripples
- **UC-count ripple (WS2):** `test_iga_spike` pins 1..13; rubric JSON counts; app domain tests; mock
  records; maturity area map — move together or the suite/app breaks.
- **Anchor tests (WS3):** `test_domain_yaml` pins `vendor_layer`/`short` — adding vendors needs pin updates.
- **Secrets relocation (WS4):** highest-coordination; exec-summary/roadmap/stakeholder hardcode
  `matrix/*.csv`; do as an isolated final step with a full grep sweep.
- **Snapshot/baseline churn:** every content phase changes report output — regenerate fixtures per phase.
- **Don't weaken the validator** — register real data + whitelist documented tokens only.

# Multi-Domain Identity-Security Instrument — Roadmap & Resume

_Last updated: 2026-06-06. This is the durable resume doc — read it first in a new session._

## Vision (one paragraph)
The repo's "core database" is a generic, evidence-cited **compliance-and-vendor matrix engine**, not a
secrets-only artifact. The program turns it from a *posture assessment* into a *vendor-selection +
regulatory-coverage instrument*, then reuses the same engine across identity-security domains (secrets/NHI →
PAM → IGA → Workforce IAM). Architecture: **one platform, per-domain models, separate offerings**. Framed
as a consulting instrument; outputs are decision-support, not a buy list. Full strategic plan + Risks &
Guardrails: `~/.claude/plans/identify-every-possible-feature-synchronous-pinwheel.md` (local) — its content
is summarised here.

## Status board

| Phase | Scope | Status |
|---|---|---|
| **0** | Vendor-mix optimizer (C1–C4), parent-aware concentration + ownership graph (E1–E5), vendor intelligence (B2/B3/B4), identity-control coverage indicator + gap-to-target (D3/D4), provenance gate (F1–F4) | ✅ DONE — merged (PR #13) |
| **0.5** | PAM spike: validate "shared engine + per-domain model" abstraction | ✅ DONE — abstraction holds (see `spikes/pam/SPIKE-FINDINGS.md`) |
| **1** | Generalize the engine: per-domain `Domain` descriptor + config-driven report | ✅ DONE — slices 1–2, #1 body-prose, #3/#5, #4, #8, #1-residual all closed → **PR #17** (`feat/phase1`, off `main`; secrets byte-identical, suite 210 green) |
| **2** | Promote PAM to a real offering + cross-domain consolidation/concentration view (X1–X2) | ✅ DONE — PAM domain fully stood up; **cross-domain consolidation view built** (`build_cross_domain.py` → `cross-domain-report.html`; CyberArk flagged spanning 2/2; runtime-verified, suite 197 green) |
| **2.7** | **Both-domain demo parity** — app + questionnaires work seamlessly for BOTH PAM and Secrets posture assessment (gate before Phase 3) | ✅ DONE (2026-06-09) — PAM questionnaire depth (17 UCs), React app domain-aware (dropdown + per-domain isolation), both-domain smoke confirmed working. See "Phase 2.7" below |
| **3** | IGA / SailPoint as a *scoped* offering (process-shaped — own model, judgment-heavy) | ⬜ — **unblocked** (2.7 gate cleared) |
| **4** | Workforce IAM / CIAM — **demand-pulled only** (analyst-owned space) | ⬜ |
| **5** | Consulting-instrument wrap: multi-engagement workspace, current-state import, anonymized benchmark | ⬜ |

## Phase 2.7 — Both-domain demo parity (⬜ GATE before Phase 3)
**Goal:** the application demos *seamlessly* for both **PAM** and **Secrets** posture assessment — same
interactive UX, comparable depth, no domain looking like a stub. Added 2026-06-09 from a demo-readiness review.

**Findings that motivate this (current state):**
- The polished **React app** (`app/`, "Posture Assessment / Questionnaire") loads a **single bundled rubric**
  (`app/src/data/rubric.json` → `app/src/assessment/rubric.ts`) that is **Secrets-only** (47 UCs). It is
  **not domain-aware** — no PAM rubric, no domain switcher. The interactive demo currently can't show PAM.
- The **Python static questionnaires** (`questionnaire/build_questionnaire.py`) *are* domain-aware and both
  build clean, BUT **PAM renders only 3 of 17 use cases** — `matrix/domains/pam/uc-archetype-map.csv` maps
  just `UC-P-001..003`. The PAM *matrix report* covers all 17; only the *questionnaire* archetype map lags.
- Matrix reports are at parity already: `matrix-viewer.html` (Secrets), `matrix/domains/pam/pam-report.html`
  (PAM, 17 UCs), `cross-domain-report.html`.

**To-do (do these before starting Phase 3):**
1. ✅ **[PAM questionnaire depth] DONE** (commit `b48d3d8`) — all 17 PAM UCs (`UC-P-001..017`) mapped across 7
   archetypes (A1×4, A2×4, A3×4, A4, A5×2, A7, A8) in `matrix/domains/pam/uc-archetype-map.csv`;
   `pam-questionnaire.html` rebuilt (3 → 17 UCs); suite + PAM data gate green.
2. ✅ **[React app → domain-aware] DONE** (commits `b6afcfa`→`f9d2aa0`) — `emit_rubric.py` now emits one JSON
   per domain (`rubric.secrets.json` 47 / `rubric.pam.json` 17); `domains.ts` registry + `makeRubric(domainId)`
   factory replace the single static import; the store carries the active `domainId` + `setDomain`; a header
   **dropdown** switches domains at runtime; responses + evidence are **namespaced per domain** (localStorage
   key suffix + IndexedDB id prefix) with one-shot legacy migration into the `secrets` namespace; export is
   domain-tagged (`assessment-<domain>.json`) and import warns on a cross-domain file. `UseCaseView` prev/next
   now follows the active rubric. App suite 57 green; offline single-file `build:check` passes (both rubrics
   inlined). PAM regulatory evidence packs in the React UI remain out of scope (separate follow-up).
3. ✅ **[Parity check] DONE** (2026-06-09) — both-domain demo smoke-tested live in the React app
   (`npm run dev`): Secrets⇄PAM switch, score + evidence + export/import confirmed working in each, no
   cross-domain contamination. Confirmed working by the user.
4. ✅ **[Regression] DONE** — app suite 57 green; Python suite 234 green; PAM data gate clean
   (`validate_data.py --data-dir matrix/domains/pam`); offline `build:check` passes.

**Acceptance:** a reviewer can pick "PAM" or "Secrets" in the live app and run a full posture assessment
end-to-end in either, with the questionnaire depth and report both complete.

**Deferred follow-ups (logged 2026-06-09; full detail under WS-3 in `meta/IMPROVEMENT-BACKLOG.md`):**
- **Unscored-use-case navigation** — the last-use-case completion affordance (commit `9f8fe20`) shows
  "X of N scored" but not *which* UCs are unscored, and offers no jump-to-finish link. Add clickable links
  to the remaining unscored UCs.
- **In-browser report generation** (roadmap option #3) — render the scored report from live answers in-app,
  replacing the offline `report_adapter.py` → `build_matrix_viewer.py --current-state` CLI.
- **PAM regulatory evidence packs in the React UI** — surface the per-question "what artifact proves this
  control" hints (already in the PAM data) in the interactive app.

## What exists now (on `main`)
- Engine: `matrix/optimizer.py`, `resilience.py`, `vendor_intel.py`, `compliance.py`, `matrix_vocab.py`,
  `report_logic.py` (build_vendormix / build_vendor_intel / build_compliance + legacy build_recdata).
- Per-domain config: `matrix/domains.py` (`Domain` dataclass, `SECRETS`, `DOMAINS` registry).
- Provenance gate: `matrix/validate_data.py` + `matrix/config/{control-id-registry,data-provenance,
  vendor-ownership}.yaml`.
- Report: `matrix/build_matrix_viewer.py` → `report_render.py` + `report-template.html` (domain labels
  tokenized; **body prose still secrets-specific** — see #1 below).
- Worked example for the next domain: `spikes/pam/` (illustrative PAM data + `run_pam_spike.py` proving the
  engine runs on a new domain unchanged).
- **Real PAM data layer (Phase 2)**: `matrix/domains/pam/` — five gate-clean CSVs: 20 privileged-identity
  types (`PID-001..020`), 17 use cases (`UC-P-001..017`), 6 vendors × 17 UCs = 102 cited capability rows
  (CyberArk, Delinea, BeyondTrust, One Identity, WALLIX, Teleport), 24-control regulatory-trace
  (registry-verified), PENDING current-state template. `validate_data.py --data-dir matrix/domains/pam`
  ⇒ all contracts valid.
- Tests: full suite green (187). Data gate clean (both domains).

## Phase 1 work — ✅ ALL CLOSED (PR #17, branch `feat/phase1` off `main`)
Originally tracked in `docs/superpowers/phase1-code-review-2026-06-05.md`:
- **#1 Body prose → per-domain content blocks ✅** — posture noun, identity picker, L0 substrate card,
  compliance-trace note, and the whole business-value tab moved to `Domain.report_content()`. Secrets
  byte-identical; PAM has no visible secrets vocabulary.
- **#1-residual ✅** — the gated secrets *source* (Fortanix L0 card + legacy `renderRecommendations`
  block/`recChip`/`recVendorRow`) is now *removed* (not just `display:none`) for non-secrets domains via
  `__SUBSTRATE_CARD__`/`__LEGACY_REC__` template regions resolved in `render()`. `pam-report.html` sheds 52
  lines of residue.
- **#3/#5 ✅** — `render()` consumes `Domain.report_meta()`; dict-drift + secrets-vocab fallbacks gone.
- **#4 ✅** — single-pass regex token substitution; a domain label containing a `__RV__`-style token can no
  longer be mangled by a later replace.
- **#8 ✅** — `Domain` loads from `matrix/config/domains/*.yaml` (`load_domain`/`load_domains`); ~150 lines of
  Python data literals deleted; adding a domain = dropping a YAML.
- **(new) provenance gate is now domain-aware** — `validate_data.py --data-dir <dir>`.

## Phase 2 — DONE (merged to `main`)
Merged via **PR #15** (merge commit `42a1e75`, 2026-06-05). Work below is on `main`; suite 198 green.

**DONE — real PAM data layer** (`matrix/domains/pam/`, all gate-clean, committed):
- `identity-catalog.csv` (20 `PID-*` privileged-identity types), `use-cases.csv` (17 `UC-P-*`),
  `vendor-capabilities.csv` + 6 per-vendor files (102 cited rows), `regulatory-trace.csv` (24
  registry-verified controls), `current-state.csv` (PENDING template — no client PAM assessment).
- `validate_data.py --data-dir matrix/domains/pam` ⇒ **All CSV data contracts valid.**

**DONE — PAM report builds correctly (#6 + #7):**
- `PAM` `Domain` descriptor (L1 = 5 established suites, L2 = Teleport, `substrate_slug=""`, PAM labels +
  per-domain `value_content`) registered; `--domain` flag on `build_matrix_viewer.py` (default secrets)
  → writes `matrix/domains/pam/pam-report.html`.
- Legacy secrets-specific RECDATA **gated** to secrets (`legacy_recdata` flag) — `renderRecommendations`
  restructured so the domain-agnostic VENDORMIX/COMPLIANCE/VENDORINTEL sections always render.
- Body prose → per-domain **content blocks** (`Domain.report_content()`): posture noun, identity picker,
  L0 substrate card (hidden when no substrate), compliance-trace vendor-count note, and the whole
  business-value tab (outcomes / KPIs / ROI). Secrets report **byte-identical**; PAM report has **no
  visible secrets vocabulary**; suite 191 green; both data gates clean.
- ⚠️ Minor residual (not visible, source-cleanliness): the runtime-gated legacy `renderRecommendations`
  JS still contains secrets string literals, and the `display:none` L0 card keeps Fortanix text in PAM
  source. Optional follow-up: extract the legacy block / L0 card to a per-domain content block so they're
  absent (not just hidden) for non-secrets domains. **Recommend a browser open of `pam-report.html` to
  eyeball all tabs** (static greps pass; no live render done).

**DONE — the moat (X1–X2):** cross-domain consolidation/concentration view, built via subagent-driven
development (spec + plan in `docs/superpowers/`). New: `matrix/crossdomain.py` (pure rollup-by-parent +
concentration/consolidation panels), `cross_render.py` + `cross-domain-template.html`,
`build_cross_domain.py` → `matrix/cross-domain-report.html`. Generic over `domains.DOMAINS` (new domains
appear automatically). Today's signal: **CyberArk spans 2/2** (Conjur/PAM/Venafi/Entro in secrets + CyberArk
PAM). Runtime-verified (0 JS errors); suite 197 green.

**Still open (Phase 1 minors + PR #15 follow-ups):** #4 single-pass token escaping, #8 load `Domain` from
YAML; plus the code-review follow-ups recorded below (PARTIAL coverage state, `</script>`-hardening sweep,
evidence-URL HTTP-200 sweep, etc.).

## Code-review follow-ups (PR #15 — 3 parallel reviewers, no Critical/blocking issues)
Fixed in-PR: visible secrets prose in `recommend()`/uc-card note/posture-legend (Important #2,
re-verified). Tracked (non-blocking):
- **Important** — vendor coverage has no `PARTIAL` state, so genuine partial gaps (esp. One Identity /
  WALLIX) sit as `ADD-ON` + low maturity + caveat. Mitigated (grid shows maturity beside coverage);
  consider adding a `PARTIAL` coverage value or guaranteeing maturity+caveat render prominently.
- **Minor** — `value_content`/`card_copy` dicts aren't `_FrozenDict`-protected (no active bug);
  external per-vendor `vendor-capabilities-*.csv` glob lacks an automated test; L0 card is
  `display:none`-hidden rather than omitted from non-substrate source; `json.dumps` injections aren't
  `</script>`-escaped (first-party, defense-in-depth); run an HTTP-200 sweep over all 102 evidence_urls
  before client delivery; `maturity_level` in regulatory-trace is free-text (not enum-validated);
  `pam-report.html` lives in the data dir (generated-artifact layering smell).

## Hazards to respect (from Risks & Guardrails)
- **Data decay** — vendor/framework data is point-in-time; the provenance gate + as-of dating exist for this.
  Re-verify before client use.
- **Ownership graph** — count concentration by ultimate parent, not brand (already implemented).
- **Decision-support, not recommendation** — never present optimizer output as a buy list.
- **Coverage indicator, not compliance score** — identity-scoped control slice only.
- **IGA is process-shaped** — don't force it into the capability matrix; scope it, sequence it last.
- Anything client-facing/outward: confirm before publishing.

## Branch / PR history
- PR #13 → Phase 0 (merged, `351589f`). PR #14 → Phase 1 slices 1–2 (merged, `655f87e`).
- `main` also carries the secrets data refresh (`bf2b812`) + audit/stakeholder/questionnaire artifacts
  (`97efae3`).
- Merged feature branches pruned 2026-06-05. `spike/pam-domain` content preserved under `spikes/pam/`.

## Other outstanding
- **WS-2 overlay engine** (selectable regulatory overlay) — carried over from an earlier milestone; see
  `meta/IMPROVEMENT-BACKLOG.md` if present.

# Multi-Domain Identity-Security Instrument — Roadmap & Resume

_Last updated: 2026-06-05. This is the durable resume doc — read it first in a new session._

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
| **1** | Generalize the engine: per-domain `Domain` descriptor + config-driven report | 🟡 slices 1–2 + #3/#5 DONE; **#1 body-prose + #4/#8 open** (below) |
| **2** | Promote PAM to a real offering + cross-domain consolidation/concentration view (X1–X2) | 🟡 IN PROGRESS — real PAM **data layer complete + gate-clean**; descriptor+wiring+body-prose next |
| **3** | IGA / SailPoint as a *scoped* offering (process-shaped — own model, judgment-heavy) | ⬜ |
| **4** | Workforce IAM / CIAM — **demand-pulled only** (analyst-owned space) | ⬜ |
| **5** | Consulting-instrument wrap: multi-engagement workspace, current-state import, anonymized benchmark | ⬜ |

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

## Remaining Phase 1 work (do these first / alongside Phase 2)
Tracked in `docs/superpowers/phase1-code-review-2026-06-05.md`:
- **#1 (big, OPEN) Body prose still secrets-specific** — `report-template.html` JS still hardcodes "L1 Secrets
  management / L2 NHI governance", "secrets-mgmt use cases NATIVE", the L0 substrate card, "Pick a machine
  identity", APRA-L2 caveat (~85 strings / ~25 JS functions — see the inventory in the body-prose task). Move
  to **per-domain content blocks** (`__DOMAIN_CONFIG__` JSON injected from the `Domain` descriptor; secrets
  values = exact current strings so the secrets report stays byte-identical). Now has a real PAM domain to
  validate against. This is the gate to a correct non-secrets report.
- **#3/#5 ✅ DONE** — `render()` consumes `Domain.report_meta()`; dict-drift + secrets-vocab fallbacks gone
  (commit `2cecd07`).
- **#4** single-pass / escaped token substitution (label tokens currently replaced before count tokens).
- **#8** load `Domain` from YAML (project convention) instead of a Python descriptor.
- **(new) provenance gate is now domain-aware** — `validate_data.py --data-dir <dir>` (commit `875cd1d`).

## Phase 2 — IN PROGRESS (resume here)
Branch: **`feat/phase1-remainder`** (not yet pushed/PR'd).

**DONE — real PAM data layer** (`matrix/domains/pam/`, all gate-clean, committed):
- `identity-catalog.csv` (20 `PID-*` privileged-identity types), `use-cases.csv` (17 `UC-P-*`),
  `vendor-capabilities.csv` + 6 per-vendor files (102 cited rows), `regulatory-trace.csv` (24
  registry-verified controls), `current-state.csv` (PENDING template — no client PAM assessment).
- `validate_data.py --data-dir matrix/domains/pam` ⇒ **All CSV data contracts valid.**

**NEXT — make the PAM report build correctly (2 intertwined slices):**
1. **#6 — `PAM` `Domain` descriptor + `--domain` build wiring.** Add `PAM` to `matrix/domains.py`
   (data_dir=`matrix/domains/pam`; `short` map; `vendor_layer` — propose L1=established suites
   {cyberark-pam, delinea, beyondtrust, one-identity-safeguard, wallix-bastion}, L2=modern access
   {teleport}; `substrate_slug=""` (PAM has **no** L0 crypto substrate — handle empty-substrate path in
   `build_recdata`); `anchors_tier`; PAM `layer_label`; report labels). Register in `DOMAINS`. Add a
   `--domain` flag to `build_matrix_viewer.py` (default secrets) writing a PAM-specific output file.
   ⚠️ Watch: `build_recdata` substrate handling with empty `substrate_slug`; `informative_frameworks=∅`
   (PAM trace has no mitre-attack).
2. **#7 — Phase 1 #1 body-prose generalization** (the gate). ~85 secrets-specific strings across ~25 JS
   functions in `report-template.html` → `__DOMAIN_CONFIG__` JSON injected from the descriptor; secrets
   values = exact current strings (secrets report stays **byte-identical**); PAM report has no secrets
   vocabulary below the fold. Hotspots: L0 crypto-substrate card, the L1/L2 layer cards + caveats, the
   business-value loop + KPIs, the concentration note. Validate by building the PAM report and confirming
   no "vault / NHI / Fortanix / machine identity / APRA-L2" leaks.

**THEN — the moat:** cross-domain consolidation/concentration view (CyberArk spans secrets+PAM; one parent
= concentration *across* domains — the spike already confirmed `cyberark-pam` rolls up to the same
`cyberark` parent that dominates secrets).

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

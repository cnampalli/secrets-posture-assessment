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
| **1** | Generalize the engine: per-domain `Domain` descriptor + config-driven report | 🟡 slices 1–2 DONE (merged PR #14); **remainder open** (below) |
| **2** | Promote PAM to a real offering + cross-domain consolidation/concentration view (X1–X2) | ⬜ next |
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
- Tests: full suite green (181). Data gate clean.

## Remaining Phase 1 work (do these first / alongside Phase 2)
Tracked in `docs/superpowers/phase1-code-review-2026-06-05.md`:
- **#1 (big) Body prose still secrets-specific** — `report-template.html` JS still hardcodes "L1 Secrets
  management / L2 NHI governance", "secrets-mgmt use cases NATIVE", the L0 substrate card, "Pick a machine
  identity", APRA-L2 caveat. Move to **per-domain content blocks**. Best done WITH a real non-secrets domain
  in hand. This is the gate to a correct non-secrets report.
- **#3/#5** render() should take the `Domain` (or `Domain.report_meta()`) instead of a hand-built
  `domain_meta` dict; drop secrets-flavoured per-key fallbacks.
- **#4** single-pass / escaped token substitution (label tokens currently replaced before count tokens).
- **#8** load `Domain` from YAML (project convention) instead of a Python descriptor.

## Phase 2 — recommended next milestone
Stand up a **real PAM domain** (replace `spikes/pam` illustrative data with verified, pipeline-generated
data): run `prompts/01→06` with a PAM seed → produce the five CSVs → apply the provenance gate
(control-id-registry + data-provenance + citations). Add a `PAM` `Domain` + register it. Build the
**cross-domain consolidation/concentration view** (the moat: e.g. CyberArk spans secrets+PAM; one parent =
concentration across domains). Do Phase-1 #1/#3 as part of this so the PAM report body is correct.

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

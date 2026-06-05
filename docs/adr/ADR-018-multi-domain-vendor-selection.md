# ADR-018 — Multi-domain vendor-selection instrument

**Status:** Accepted (2026-06-05) · **Supersedes/extends:** ADR-009 (regulatory overlay), ADR-017 (report modularization)

## Context
The matrix engine was treated as a secrets/NHI-only artifact, but its data model (identity catalog →
use cases → posture → regulatory trace → vendor capabilities, keyed on generic
`target_type`/`target_id`/`framework_slug`) is domain-agnostic. We want to (a) go beyond posture
assessment into vendor selection + regulatory coverage, and (b) reuse the engine across identity-security
domains (secrets/NHI → PAM → IGA → Workforce IAM) as a consulting instrument.

## Decisions
1. **One platform, per-domain models, separate offerings.** Not separate tools per domain, not one
   schema forced on every domain. Shared engine + a per-domain `Domain` descriptor (`matrix/domains.py`);
   each domain is data + config, not new code. Validated by the PAM spike (engine ran on PAM with an empty
   `matrix/` diff — see `spikes/pam/SPIKE-FINDINGS.md`).
2. **Vendor selection is decision-support, not a recommendation engine.** The optimizer (greedy set-cover)
   and analytics surface candidate portfolios; price/contracts/stack-fit are consultant inputs. Never a buy list.
3. **Concentration counted by ultimate corporate parent, not brand** (`resilience.py` +
   `config/vendor-ownership.yaml`) — sibling brands under one owner are not independent second-sources
   (APRA CPS 230). This cross-domain parent view is the moat.
4. **Coverage indicator, not compliance score** (`compliance.py`) — against the identity-scoped control
   slice only; a control is MET only when every mapped use case is MET.
5. **Provenance is enforceable** (`validate_data.py` + `config/control-id-registry.yaml`,
   `data-provenance.yaml`) — anti-fabrication control-ID gate, no-uncited-claims, as-of/source-tier
   manifest. Driven by this project's history of a fabricated ISM mapping.
6. **IGA is process-shaped** — it gets its own model, scoped narrowly, sequenced last; do not force it into
   the capability matrix.

## Consequences
- Adding a domain = a `Domain` descriptor + gated data, validated against the secrets regression anchor.
- Engine, report model-builders, and provenance gate are domain-neutral; remaining secrets-specificity is
  the report **body prose** (tracked, Phase-1 remainder).
- Phases: 0 (done), 0.5 spike (done), 1 slices 1–2 (done); remaining 1 (prose/render/YAML), 2 (real PAM +
  cross-domain view), 3 (IGA), 4 (Workforce, demand-pulled), 5 (consulting wrap).

## References
- Design: `docs/superpowers/specs/2026-06-05-multi-domain-vendor-selection-design.md`
- Roadmap/resume: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`
- Reviews: `docs/superpowers/phase0-code-review-2026-06-05.md`, `phase1-code-review-2026-06-05.md`

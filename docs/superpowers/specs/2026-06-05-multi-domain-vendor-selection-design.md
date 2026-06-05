# Design — Multi-domain vendor-selection instrument (Phases 0, 0.5, 1)

Date: 2026-06-05 · ADR: ADR-018 · Roadmap: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`

## Scope
The decision-support layer over the matrix engine + the per-domain generalization. Built across Phase 0
(analytics), Phase 0.5 (PAM spike), Phase 1 slices 1–2 (domain descriptor + report labels). All merged to
`main`; full suite green; report snapshot byte-identical for the secrets domain.

## Modules (all pure, dependency-injected; `matrix/`)
- **`optimizer.py`** — resilience-first greedy set-cover (C1–C3): `greedy_cover` (ties diversify parent),
  `complement` (C4, "have X → add Y"), `portfolio_concentration`, white-space detection.
- **`resilience.py`** — parent-aware concentration (E1–E5): `parent_of`, `coverage_by_parent`,
  `single_source`, `concentration` (blast radius + sole-source).
- **`vendor_intel.py`** — B2/B3/B4: `best_for` (leading provider + cited differentiator), `head_to_head`.
- **`compliance.py`** — D3/D4: `coverage_indicator`, `gap_to_target` (worst-state aggregation; UNKNOWN
  ranks below MET so unassessed UCs don't inflate coverage).
- **`matrix_vocab.py`** — single-source domain vocabulary (STATE_RANK, COVERAGE_ORDER, UC_TYPES).
- **`report_logic.py`** — model builders `build_vendormix` / `build_vendor_intel` / `build_compliance`
  (additive sections; legacy `build_recdata` unchanged / RECDATA frozen).
- **`domains.py`** — `Domain` dataclass + `SECRETS` + `DOMAINS` registry; read-only `_FrozenDict` maps.
- **`validate_data.py`** — provenance gate: control-ID registry (anti-fabrication), no-uncited-claims,
  data-provenance manifest.

## Config (data, not code)
`matrix/config/`: `control-id-registry.yaml`, `data-provenance.yaml`, `vendor-ownership.yaml`
(+ existing `frameworks.yaml`, `vendor-residency.yaml`, presets).

## Report integration
`build_matrix_viewer.py` drives the build from `DOMAIN = domains.SECRETS`; `report_render.py` injects
additive model sections (VENDORMIX / COMPLIANCE / VENDORINTEL) + domain-label tokens
(`__DOMAIN_TITLE__`/`__OBJECT_*__`/…) into `report-template.html`.

## How to add a domain (per ADR-018)
1. Run `prompts/01→06` with the domain seed → five CSVs; apply the provenance gate.
2. Add a `Domain` descriptor (filenames, vendor maps, anchors tier, informative frameworks, report labels).
3. Build via the existing engine — validated end-to-end by `spikes/pam/run_pam_spike.py`.

## Known remaining (Phase 1 remainder) — see `docs/superpowers/phase1-code-review-2026-06-05.md`
Body prose still secrets-specific (#1, the gate to a correct non-secrets report); render-via-Domain
(#3/#5); single-pass token escaping (#4); load `Domain` from YAML (#8).

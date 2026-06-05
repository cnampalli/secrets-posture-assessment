# Phase 1 — Defects & follow-ups (code review of PR #14)

Date: 2026-06-05 · Branch: `feat/phase1-domain-config` · Review: high-effort multi-angle.

8 findings, none active regressions (behaviour byte-identical, suite 181 green). They're
about *finishing* the multi-domain generalisation safely.

## Fixed (commit e214196)
- **#2 🟠 shared-mutable maps** — Domain maps are now a read-only `_FrozenDict`; a new domain
  built by copy-edit can't silently corrupt the source.
- **#6 🟡 informative-frameworks single source** — removed hardcoded
  `report_logic.INFORMATIVE_FRAMEWORKS`; `build_compliance(exclude=frozenset())`, caller passes
  `domain.informative_frameworks`.
- **#7 🔵 dead back-compat aliases** — deleted unused `VENDOR_LAYER`/`SHORT`/`LAYER_LABEL`/
  `SUBSTRATE_SLUG` aliases + the `report_io` re-export (verified zero consumers).

## Open follow-ups

### #1 — 🟠 Body prose still secrets-specific (the defining remaining work)
- **Where:** `matrix/report-template.html` JS render functions — "Pick a machine identity",
  "L1 Secrets management / L2 NHI governance", "secrets-mgmt use cases NATIVE", the L0
  crypto-substrate card, the APRA-L2 SaaS caveat, "best fit vault" copy, etc.
- **Problem:** slice 2 parameterised only title/heading/nav/subtitle. Point `DOMAIN` at a
  non-secrets domain → correct chrome over a secrets body = an internally contradictory,
  factually-wrong-below-the-fold report (worse than an obviously-untouched template).
- **Fix direction:** move domain copy into per-domain **content blocks** (a content map/file the
  template consumes), not hardcoded strings. Do this WITH a real non-secrets domain in hand to
  validate against — it is the bulk of remaining Phase 1.
- **Effort:** L.

### #3 / #5 — 🟡 `render()` should take the `Domain`; kills dict-drift + secrets-vocab fallback
- **Where:** `matrix/build_matrix_viewer.py` (hand-built `domain_meta` dict) + `matrix/report_render.py`
  (per-key `dm.get(..., "identities"/"identity")` fallbacks).
- **Problem:** every new label needs edits in 3 places (Domain field, the dict, a `.replace()`);
  a missing key silently renders blank title/heading OR secrets vocabulary in a non-secrets report.
- **Fix direction:** pass the `Domain` (or a `Domain.report_meta()` mapping) into `render()`; read
  fields off it; drop the secrets-flavoured per-key defaults (fail fast on a missing key).
- **Effort:** S.

### #4 — 🟡 Unescaped token substitution (labels before counts)
- **Where:** `matrix/report_render.py` — `__DOMAIN_*__`/`__SUBSTRATE_NOTE__` substituted before
  `__RV__`/`__NHI__`/`__UC__`/`__OBJECT_*__`.
- **Problem:** a future domain whose heading/substrate_note legitimately contains a `__…__`
  sequence gets mangled by a later replace.
- **Fix direction:** single-pass substitution over a token→value map, or a non-colliding
  placeholder syntax.
- **Effort:** S. (No current trigger — secrets values contain no tokens.)

### #8 — 🔵 `Domain` is Python, not YAML
- **Where:** `matrix/domains.py`.
- **Problem:** project convention keeps config in YAML (`frameworks.yaml`, `vendor-residency.yaml`,
  `vendor-ownership.yaml`); a Python descriptor means analysts can't add a domain without code, and
  the vendor maps are pure data.
- **Fix direction:** load `Domain` from a per-domain YAML (maps can stay as data files); keep the
  dataclass as the in-memory shape.
- **Effort:** M. (Noted as a planned Phase-1 follow-up.)

## Dropped (verified non-issues)
- "Make `load_inputs` domain required" — the `domain=SECRETS` default is relied on by 4 integration
  tests; keep it.
- `.replace()`-chain efficiency — negligible for a one-off build; do not optimise.

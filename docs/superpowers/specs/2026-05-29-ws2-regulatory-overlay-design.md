# WS-2 — Selectable Regulatory Overlay (engine) — Design Spec

**Date:** 2026-05-29
**Branch:** `ws2-regulatory-overlay` (off `main`)
**Status:** Approved design — awaiting spec review before planning
**Source:** `meta/IMPROVEMENT-BACKLOG.md` WS-2; brainstorming session 2026-05-29

---

## 1. Purpose

Make the vendor/compliance report **industry-agnostic** by replacing hardcoded,
FI/APRA-flavoured framework and residency logic in `matrix/build_matrix_viewer.py`
with declarative config. A client (or the consultant driving the engagement) selects
which regulatory framework(s) the report scopes to, plus comparison overlays, and tunes
how heavily AU data-residency / IRAP weighs on vendor ordering.

This is an **engine-filtering change, not new research** — it operates entirely on the
7 frameworks already mapped in `matrix/regulatory-trace.csv`. No new control→UC mappings
are authored in WS-2.

## 2. Non-goals (explicit scope boundary)

- **No new framework research.** Privacy Act, My Health Record, PSPF, and SOCI have **zero**
  control→UC rows in `regulatory-trace.csv` today; they are out of scope and deferred to a
  future new-research workstream (IMPROVEMENT-BACKLOG follow-up).
- **No in-report live toggle.** WS-2 scopes at build time. The data structure is made
  forward-compatible (§7) so a WS-3 JS toggle drops in later, but embedding all-framework
  data for live filtering is a WS-3 concern.
- **No current-state file format change.** That is a WS-3 question.
- **No ANZ tokens introduced** (locked naming constraint). Existing data values are untouched.

## 3. Frameworks actually available (ground truth)

Distinct `framework_slug` values in `matrix/regulatory-trace.csv`, with row counts:

| slug | rows | role |
|---|---|---|
| `essential-8` | 26 | ACSC maturity baseline (always-on) |
| `cisa-ztmm-v2` | 13 | Zero Trust overlay (cross-cutting) |
| `apra-cps-234` | 25 | Prudential — information security |
| `apra-cps-230` | 6 | Prudential — operational risk |
| `apra-cpg-234` | 3 | Prudential — practice guide |
| `asd-ism` | 41 | Australian Govt baseline |
| `mitre-attack` | 31 | Adversary TTPs (informative overlay) |

Any config referencing a slug outside this set is **warned and skipped**, never silently scoped to empty.

## 4. Architecture

A **config resolution layer** sits in front of the existing build. Three pieces of
hardcoded state become declarative; one new behaviour layers on top.

```
engagement.yaml ──┐
--preset / --frameworks (CLI) ──┤
presets/<name>.yaml ──┤──> engagement_config.resolve() ──> EngagementConfig
built-in default ──┘                                          │
                                                              ▼
config/frameworks.yaml ───────> build_matrix_viewer.py (scopes frameworks,
config/vendor-residency.yaml ──>   applies residency weighting, emits metadata)
                                                              │
                                                              ▼
                                                  scoped report HTML + REGDATA
```

**Regression anchor (non-negotiable):** with **no engagement config**, the engine reproduces
today's report exactly — all 7 frameworks shown, residency-first ordering, IRAP-gated primary.
A golden-output test enforces this. Presets are strictly opt-in.

## 5. Components

| File | Status | Role |
|---|---|---|
| `matrix/engagement_config.py` | NEW | Loads YAML, resolves `preset + inline overrides + CLI`, validates slugs against the 7 available frameworks, returns a resolved `EngagementConfig`. Sole owner of YAML parsing. |
| `matrix/config/frameworks.yaml` | NEW | Externalized `FRAMEWORK_LABELS` (label + subtitle) for the 7 slugs. |
| `matrix/config/vendor-residency.yaml` | NEW | Externalized `VENDOR_RESIDENCY` (residency / irap / note per vendor slug). |
| `matrix/config/presets/financial.yaml` | NEW | APRA (×3) primary + E8 baseline + ZTMM overlay; residency `high`, IRAP required. |
| `matrix/config/presets/government.yaml` | NEW | ISM primary + E8 baseline; residency `high`, IRAP required. |
| `matrix/config/presets/retail.yaml` | NEW | E8 only; residency `low`, IRAP not required. |
| `matrix/config/presets/baseline.yaml` | NEW | E8 only; residency `medium`, IRAP not required. |
| `matrix/config/engagement.example.yaml` | NEW | Documented engagement template. |
| `requirements.txt` | NEW | `PyYAML`. |
| `matrix/build_matrix_viewer.py` | MODIFY | Consume resolved config: filter `fw_order` / `framework_controls`, apply residency weighting, emit selection metadata. Source `FRAMEWORK_LABELS` and `VENDOR_RESIDENCY` from config files. |
| `tests/test_engagement_config.py` | NEW | Config resolution + scoping + weighting tests (§8). |
| `docs/adr/ADR-009-regulatory-overlay-config.md` | NEW | Records the externalization decision + PyYAML-dependency tradeoff. |

## 6. Config schema & precedence

```yaml
# engagement.yaml
preset: financial            # optional base; loads presets/financial.yaml
primary:   [apra-cps-234]    # optional inline override of the preset's primary
overlays:  [cisa-ztmm-v2]    # comparison frameworks shown alongside primary
baseline:  [essential-8]     # always-on; union'd into the scope regardless of selection
residency:
  weight: high               # high | medium | low | off
  irap_required: true
```

**Resolution precedence (highest wins):**
1. CLI flag (`--frameworks a,b,c`, `--preset <name>`, `--config <path>`)
2. inline `engagement.yaml` key
3. named preset's value
4. built-in default = today's all-frameworks behaviour (the regression anchor)

`baseline` is always union'd into the final framework set even if the user omits it.

## 7. Residency weighting

`weight` and `irap_required` are **independent knobs**. `weight` controls only where
residency sits in the vendor sort key (the `RES_ORDER`-keyed sorts at L290–295);
`irap_required` independently controls the IRAP gate on primary-vendor selection
(the "AU-RESIDENT **and** IRAP=YES" filter at L297–299).

`weight` — position of residency in the vendor sort key:

| `weight` | Vendor sort behaviour |
|---|---|
| `high` | residency = primary sort key (today's `RES_ORDER` behaviour) |
| `medium` | residency applied after capability as a strong tiebreaker |
| `low` | residency as a final tiebreaker only |
| `off` | residency removed from sort key; rank by capability only |

`irap_required` — primary-vendor IRAP gate:

- `true` → primary must be AU-RESIDENT **and** IRAP=YES (today's behaviour).
- `false` → gate disabled; a vendor can be primary on capability alone.

Presets pin concrete values (financial/government: `high` + `true`; retail: `low` + `false`;
baseline: `medium` + `false`) so no value is left to the implementer's judgement.

## 8. Selection-aware data structure (WS-3-ready)

`REGDATA` gains a `framework_selection` block:

```python
"framework_selection": {
  "selected":  [...primary slugs...],
  "overlays":  [...overlay slugs...],
  "baseline":  ["essential-8"],
  "available": [all 7 slugs in regulatory-trace.csv],
}
```

WS-2 scopes `frameworks` / `controls` at build time (smaller, scoped output). `available`
documents the full menu so a WS-3 in-report toggle knows the complete option set without
re-architecting the engine.

## 9. Error handling

| Condition | Behaviour |
|---|---|
| PyYAML not installed | `ERROR: PyYAML required — pip install -r requirements.txt`, exit non-zero |
| Unknown preset name | Error listing available preset names |
| Config slug absent from `regulatory-trace.csv` | **Warn + skip** that slug; continue |
| `weight` value not in {high,medium,low,off} | Error naming valid values |
| Empty resulting framework scope | Error (a report with no frameworks is invalid) |

## 10. Testing (TDD)

Extends existing `tests/`. Tests are written RED before implementation.

1. **Golden regression** — no-config build reproduces frozen current output (structural compare of `REGDATA` frameworks + vendor order).
2. `financial` preset → `REGDATA` frameworks = {apra-cps-234, apra-cps-230, apra-cpg-234, essential-8, cisa-ztmm-v2} only.
3. `government` preset → {asd-ism, essential-8}; `retail` → {essential-8}.
4. `weight: off` → residency removed from sort; deterministic order change vs `high`.
5. `irap_required: false` → primary-vendor selection changes.
6. Unknown framework slug → warn + skip (not in output, no crash); unknown preset → error.
7. `baseline` always present even when omitted from config.
8. Precedence: CLI > inline > preset > default.

## 11. Tradeoffs recorded

- **PyYAML dependency** (user choice): gains human-friendly, commentable config for the
  consultant hand-editing engagement files; costs bare-`python3` portability. Mitigated by
  `requirements.txt` + a clear install error message. Recorded in ADR-009.
- **Build-time scoping over embed-all** keeps WS-2 output small and the engine simple; the
  `available` metadata preserves the WS-3 upgrade path.

## 12. Process

- Branch `ws2-regulatory-overlay` off `main` (independent of WS-1 PR #1).
- TDD discipline (RED → GREEN → REFACTOR), atomic commits.
- `requesting-code-review` before PR; `code-review` on the diff.
- On completion: mark WS-2 ✅ in `meta/IMPROVEMENT-BACKLOG.md`; note the health-preset /
  Privacy-Act / PSPF / SOCI / MyHR data gap as a deferred follow-up.

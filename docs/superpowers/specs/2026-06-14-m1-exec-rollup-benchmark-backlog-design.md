# M1 — Exec roll-up + benchmark + backlog export (design)

**Date:** 2026-06-14
**Track:** M (market leadership) — first item, per `docs/superpowers/plans/2026-06-11-a-plus-hardening.md`
**Status:** approved, ready for implementation plan

## Purpose

Close the first market-leadership gap the IAM-specialist review named: there is no
board-grade cross-domain output and no benchmark mechanism. Today every output is an
analyst-grade tab. M1 adds three first-class deliverables that move the instrument from
"comprehensive analysis" to "consumable by CEO/CIO/CTO/Product-Owner personas":

1. A board-grade exec roll-up (standalone one-pager).
2. A synthetic, clearly-labelled benchmark layer ("you vs AU-FI peers").
3. A GAP/PARTIAL → Jira/ADO-importable backlog CSV (Product Owner's missing hook).

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Roll-up form | **Standalone one-pager HTML** (own generator) | Plan says "first-class output, not a tab". |
| Trend element | **Baseline marker, no arrow** | No prior dated assessment exists; `as_of`/history is M4. No fabricated direction. Slot reserved for M4. |
| Benchmark basis | **Config file with cited rationale**, synthetic + illustrative | Auditable, evolvable to real cohort. Honest labelling required. |
| Cohort scope | **AU-FI default, configurable** via `engagement_config` | Matches existing engagement-config pattern; retarget without code change. |
| Backlog format | **One neutral CSV, both-importable** (Jira + ADO) | Single schema to maintain/test; documented per-tool import mapping. |
| Backlog scope | **GAP + PARTIAL, all priorities** | Matches plan wording; priority carried from risk band so P0s sort to top. |

## Architecture

Follows the established `matrix/` separation: **pure model builders** (no I/O) +
**pure renderers** + **build entrypoints** (I/O) + **config/data**. Mirrors the existing
`crossdomain.py` / `cross_render.py` / `build_cross_domain.py` triplet.

### 1. Exec roll-up

- **`matrix/rollup.py`** (pure) — `build_exec_rollup(domains_posture, benchmark, crossmap) -> model`
  - Per domain: `{slug, label, overall_band, met_pct, counts, top_3_risks, benchmark, trend}`.
  - `top_3_risks`: the three highest **risk-band** open `GAP`/`PARTIAL` UCs for the domain,
    each `{uc_id, short_title, regulatory_driver, risk_band, state}`. Ranking reuses the same
    risk-band ordering used elsewhere in `report_logic`. Fewer than three open gaps → return
    what exists (no padding).
  - `trend`: `{state: "baseline", note: "First assessment — trend activates at next dated re-baseline."}`.
    No directional glyph.
  - One cross-domain headline derived from `crossmap`: the top spanning corporate parent
    (concentration signal) or an explicit "no parent spans >1 domain" statement.
  - Overall posture line: lowest band across domains + total open P0 count.
- **`matrix/rollup_render.py`** (pure) — `render(model) -> html`. Self-contained, offline,
  Brass-Editorial styled, `@media print` one-page CSS. Mirrors `cross_render.py` structure.
- **`matrix/build_exec_rollup.py`** (I/O) — mirrors `build_cross_domain.py`:
  loads every registered domain via `report_io.load_inputs`, computes
  `build_posture_maturity` per domain, loads the benchmark cohort, calls `crossdomain.build_crossmap`
  for the headline, builds the model, writes `matrix/exec-rollup.html`. Prints a summary line.
- **Linking:** each domain report header and the cross-domain report gain a link to
  `exec-rollup.html` (small template additions in `report_render` / `cross_render`).

### 2. Benchmark layer

- **`matrix/config/benchmark-cohort.json`** — versioned, auditable:
  ```
  {
    "cohort_label": "Australian financial institutions (illustrative synthetic baseline)",
    "basis": "Synthetic, designed-honest. Not a measured cohort. Evolves to real percentiles as engagements accumulate.",
    "domains": {
      "secrets": { "p25": <int>, "p50": <int>, "p75": <int>, "rationale": "...", "sources": ["..."] },
      "pam":     { "p25": <int>, "p50": <int>, "p75": <int>, "rationale": "...", "sources": ["..."] },
      "iga":     { "p25": <int>, "p50": <int>, "p75": <int>, "rationale": "...", "sources": ["..."] }
    }
  }
  ```
  Every band carries a `rationale`. Percentiles are met-% bands (0–100).
- **`matrix/benchmark.py`** (pure):
  - `load_cohort(cfgdir, engagement) -> cohort` — reads the JSON; applies an optional
    `engagement_config.benchmark_cohort` override (label and/or alternate cohort file/key).
    Validation: raise if any present domain band lacks a `rationale` (honesty gate).
  - `position(met_pct, domain, cohort) -> {percentile_band, cohort_label, basis_note}` —
    maps a domain's met-% onto `below p25 / p25–p50 / p50–p75 / above p75`. Missing domain →
    `{percentile_band: "no cohort baseline", ...}` (never silently invents a band).
- **Honesty guardrails:** the rendered roll-up must carry the literal cohort label string
  (asserted by a render test); the basis note must state "synthetic"/"illustrative".

### 3. Backlog export

- **`matrix/backlog.py`** (pure):
  - `build_backlog_rows(anz, ucs, domain) -> [row]` — every UC whose state is `GAP` or
    `PARTIAL` becomes one row. `MET` and `PENDING` are excluded. Columns, chosen to import
    cleanly into **both** Jira and Azure DevOps:
    `Summary, Work Item Type, Description, Priority, Labels, UC-ID, Domain, Regulatory-Driver, State`.
    - `Work Item Type` = fixed (e.g. `Task`) — both tools accept it.
    - `Priority` derived from the UC risk band (P0 → highest), so P0s sort to the top.
    - `Labels` = space/semicolon convention that both tools accept; includes domain + driver tag.
  - `to_csv(rows) -> str` — RFC-4180 escaping (quote fields containing comma/quote/newline).
- **`matrix/build_backlog.py`** (I/O) — writes `<domain>-backlog.csv` next to the domain
  reports for every registered domain. A short README note documents the Jira and ADO
  import-column mapping.

## Data flow

```
domains.DOMAINS ─┐
                 ├─ report_io.load_inputs ─ build_posture_maturity ─┐
benchmark-cohort.json ─ benchmark.load_cohort ────────────────────┤
crossdomain.build_crossmap ───────────────────────────────────────┤
                                                                   └─ rollup.build_exec_rollup
                                                                         └─ rollup_render.render ─ exec-rollup.html

report_io.load_inputs ─ backlog.build_backlog_rows ─ backlog.to_csv ─ <domain>-backlog.csv
```

## Error handling / edge cases

- Domain with zero open gaps → `top_3_risks: []`, roll-up states "no open gaps".
- Domain absent from cohort config → benchmark band "no cohort baseline" (explicit, not invented).
- Benchmark band missing `rationale` → `load_cohort` raises (honesty gate, fails CI).
- Matrix-less domain (IGA) → still gets posture/maturity and a backlog (it has UCs); the
  cross-domain **headline** continues to skip matrix-less domains exactly as `build_cross_domain.py`
  does today (parent-disjoint precondition unchanged).
- Empty UC set → builders return empty structures, never a fabricated band or arrow.

## Testing (TDD)

- **`tests/test_rollup.py`** — band selection, top-3 risk ranking + truncation, baseline trend
  shape (no arrow), cross-domain headline present/absent, empty-domain.
- **`tests/test_benchmark.py`** — boundary percentiles (exactly p25/p50/p75), missing-domain band,
  cohort-label override via engagement, rationale-required raise.
- **`tests/test_backlog.py`** — only GAP+PARTIAL exported, MET/PENDING excluded, priority-from-risk-band
  mapping, CSV escaping of comma/quote/newline, all both-tool columns present.
- **`tests/test_rollup_render.py`** — three domains render, literal synthetic-cohort label present,
  baseline note present, **no** directional trend glyph, self-contained (no external refs).

## CI / gates

Add `build_exec_rollup` and `build_backlog` to the existing machine-verified gate pipeline
(alongside the report byte-identity / build-clean gates), so the new artifacts are produced
and validated on every push. The benchmark `rationale`-required check runs as part of
`build_exec_rollup` and therefore in CI.

## Out of scope (deliberate, YAGNI)

- Real measured cohort percentiles (requires accumulated engagements — evolves later).
- `as_of` / per-row freshness capture and re-baselining (M4).
- Live directional trend (M4, once a second dated assessment exists).
- Two tailored per-tool CSV schemas (one neutral CSV chosen instead).

## Acceptance

1. `exec-rollup.html` builds: three domains × ML band × top-3 risks × baseline-trend marker +
   benchmark position + one cross-domain headline, on one printed page.
2. Benchmark renders with the explicit synthetic/illustrative AU-FI cohort label; no band
   lacks a documented rationale.
3. `<domain>-backlog.csv` imports into both Jira and ADO per the documented mapping; contains
   exactly the GAP+PARTIAL rows with P0s sorted first.
4. All new tests pass; exec-rollup + backlog builds run green in CI.

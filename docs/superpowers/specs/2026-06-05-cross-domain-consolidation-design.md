# Design — Cross-domain consolidation/concentration view (Phase 2, the moat)

Date: 2026-06-05 · Roadmap: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md` (Phase 2, X1–X2) · ADR: ADR-018

## Context
The instrument now models two real domains (secrets/NHI, PAM) on one shared engine, with a parent-aware
ownership graph (`vendor-ownership.yaml`) already collapsing sibling brands to their ultimate parent. Each
per-domain report shows concentration *within* its domain. The cross-cutting insight that single-domain
analysis misses: a corporate parent that spans **multiple** domains. Today **CyberArk** is the one such
parent — it owns Conjur, CyberArk PAM, Venafi and Entro in secrets **and** CyberArk PAM in the PAM domain.
A buyer who picks "a second source" in secrets and "a PAM platform" can land on the *same parent* without
realising it. This view surfaces that — as neutral decision-support that reads two ways at once.

## Goal
A **standalone** cross-domain report that loads every registered domain's vendor data, rolls up by ultimate
parent, and renders: (1) a parent × domain footprint **map**, (2) a **concentration** panel (risk reading),
and (3) a **consolidation** panel (opportunity reading). Generic over the `domains.DOMAINS` registry so
future domains (IGA, …) appear automatically. The current real signal (CyberArk spans 2/2) must land clearly
and stay correct as domains are added.

## Non-goals (YAGNI)
- No full coverage heatmap — a per-cell brand list + one-line coverage hint is enough for v1.
- No new interactivity beyond the report chrome.
- No changes to the per-domain reports or the engine's existing modules (additive only).
- Not a buy list / ranking — both panels are framed as decision-support.

## Architecture — 4 layers, reusing the engine
**Data** — for each `domain` in `domains.DOMAINS`, call the existing
`report_io.load_inputs(domain.data_dir, None, domain)` to get its `ranked` vendor rows; load
`vendor-ownership.yaml` once via `report_io.load_vendor_ownership`. (No new I/O code; substrate vendors are
already excluded from `ranked`.)

**Logic — NEW `matrix/crossdomain.py` (pure, dependency-injected).**
`build_crossmap(domains_data, ownership) -> model`, where `domains_data` is an ordered list of
`{slug, label, ranked}` (one per domain) and `ownership` is the parent map. Uses `resilience.parent_of`.
Model shape:
```
{
  "domains": [{"slug": "secrets", "label": "Secrets management / NHI"},
              {"slug": "pam",     "label": "Privileged Access Management"}],
  "parents": [
    {"parent": "cyberark",
     "by_domain": {"secrets": {"brands": [{"slug": "cyberark-conjur", "name": "Conjur"}, …],
                               "native_ucs": 12},
                   "pam":     {"brands": [{"slug": "cyberark-pam", "name": "CyberArk PAM"}],
                               "native_ucs": 14}},
     "spans": 2,
     "domains_present": ["secrets", "pam"]},
    {"parent": "ibm", "by_domain": {"secrets": {"brands": [{"slug": "hashicorp-vault-enterprise", …}],
                                                "native_ucs": 17}},
     "spans": 1, "domains_present": ["secrets"]},
    …
  ],                              # sorted: spans desc, then parent name
  "concentration": [             # only parents with spans >= 2
    {"parent": "cyberark", "spans": 2, "domains_present": ["secrets","pam"],
     "brands_total": 5,
     "note": "Spans 2/2 assessed domains. A 'second source' in Secrets (e.g. Conjur) and the PAM platform "
             "can be the same ultimate parent — not independent (CPS 230 service-provider concentration)."}
  ],
  "consolidation": [             # same spanning parents, ranked by breadth (domains, then native_ucs total)
    {"parent": "cyberark", "domains": 2, "native_ucs_total": 26,
     "note": "One parent covers Secrets L1 + PAM → fewer vendors / contracts to manage."}
  ]
}
```
- **One definition of `native_ucs`**: per (parent, domain) it is the count of **distinct** UC `target_id`s
  for which **any** of that parent's brands in that domain has `coverage == "NATIVE"` (computed from the
  `ranked` rows). It lives on each `by_domain.<slug>` entry; the cell hint renders "NATIVE on N UCs".
  `consolidation.native_ucs_total` = sum of a parent's per-domain `native_ucs` across its present domains.
  (Illustrative numbers above; actuals derive from the CSVs.)
- `by_domain.<slug>.brands` = the parent's vendor brands present in that domain (chips); a parent absent
  from a domain has no key for that slug (renders an em-dash cell).
- `spans` = number of domains where the parent has ≥1 ranked vendor.
- Concentration listed only for `spans >= 2`. Consolidation lists the same parents (breadth framing).
- Determinism: stable sort, no `Date.now()`/random.

**Render — NEW `matrix/cross_render.py` + `matrix/cross-domain-template.html`.**
`render(model)` loads the template, injects `brand_fonts`/`brand_tokens` (reused) and the model JSON
(`/*__CROSSMAP__*/{}`), and substitutes a small set of label tokens. The template is a self-contained
offline HTML page in the existing visual language with three sections: the parent × domain matrix
(parents as rows, domains as columns, cells = brand chips + "NATIVE on N UCs"; spanning parents marked ★),
then the Concentration panel, then the Consolidation panel. JSON injected via `json.dumps(..., ensure_ascii
=False)`; apply `</`→`<\/` escaping (defense-in-depth, addressing the PR #15 review note).

**Present — NEW `matrix/build_cross_domain.py`.** Orchestrator: iterate `domains.DOMAINS`, load each via
`report_io.load_inputs`, call `crossdomain.build_crossmap`, `cross_render.render`, write
`matrix/cross-domain-report.html`. Print a one-line summary (parents, spanning count).

## Guardrails (from the project's Risks & Guardrails)
- Count concentration by **ultimate parent**, not brand (reuse `parent_of`).
- **Decision-support, not a recommendation** — neutral framing; never present as a buy list.
- Ownership data is **point-in-time** — the report carries an as-of / re-verify note (ownership YAML has
  `as_of`/`confidence`; surface that a parent's spanning claim depends on M&A facts that drift).
- No invented numbers — every count derives from the CSV `ranked` rows.

## Testing (TDD)
**`tests/test_crossdomain.py`** (pure-logic, synthetic data — no file I/O):
- two domains, a parent with a brand in each → `spans == 2`, appears in `concentration` + `consolidation`.
- a parent in only one domain → `spans == 1`, absent from both panels.
- `native_ucs` counts distinct NATIVE UC target_ids per (parent, domain); ADD-ON/PARTNER/GAP excluded.
- parents sorted spans-desc then name; deterministic.
- empty domain (no ranked rows) handled without error.
**Build smoke test** (`tests/test_cross_build.py`): run `build_cross_domain.py`; assert it writes valid
HTML containing the spanning parent and both panel headings; assert `cyberark` flagged `spans 2`.
**Runtime verify** (Playwright, manual gate): report opens, 0 JS errors, CyberArk row shows ★/2, both
panels render. (Not a pytest; a verification step.)

## Files
- New: `matrix/crossdomain.py`, `matrix/cross_render.py`, `matrix/cross-domain-template.html`,
  `matrix/build_cross_domain.py`, `tests/test_crossdomain.py`, `tests/test_cross_build.py`.
- Reused unchanged: `report_io.py`, `resilience.py`, `domains.py`, `brand_fonts.py`, `brand_tokens.py`,
  `vendor-ownership.yaml`. No edits to existing modules.

## Adding a domain later (recipe addendum)
Once a new domain is registered in `DOMAINS` with gate-clean data, it appears in the cross-domain map
automatically — no cross-domain code change. Overlaps grow (e.g. SailPoint/One Identity across PAM+IGA),
which is exactly when this view earns its keep.

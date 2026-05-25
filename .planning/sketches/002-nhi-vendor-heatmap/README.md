---
sketch: 002
name: nhi-vendor-heatmap
question: "Can 703 coverage cells (37 NHI × 19 vendors) remain readable and drill-able on a single screen, and what's the right ordering / grouping?"
audience: Enterprise Architect / Platform Engineering
winner: null
tags: [heatmap, density, vendor-comparison, stage-1]
---

# Sketch 002 — NHI × Vendor Coverage Heatmap

## Design Question

Can 703 coverage cells (37 NHI × 19 vendors) remain visually readable and drill-able
on a single screen, and what's the right ordering / grouping for an architect to
*see* the gaps?

## How to View

From the repo root:

```sh
open .planning/sketches/002-nhi-vendor-heatmap/index.html
```

## Variants

- **A: Full density** — All 37 NHIs (rows) × 19 vendors (columns). Vertical column headers,
  vendor slugs in monospace, cells show maturity 0–5 with color = coverage tier. Row totals
  on the right ("any-coverage / vendor-count"). Hover any cell for evidence quote + URL.
- **B: Bucketed** — Same matrix, but with a divider between COMMON identities (14 — cloud IAM,
  K8s SAs, AD service accounts) and UNCOMMON / emerging (23 — agentic AI, RPA, mainframe,
  PQC). Rows where XYZ has a confirmed UC-level GAP are highlighted in red, so the architect
  sees vendor coverage *and* XYZ relevance at once.
- **C: Vendor leaderboard** — Pivots to vendor as primary axis. 19 vendors ranked by NHI
  coverage score (NATIVE × maturity + ADD-ON ÷ 2 + PARTNER ÷ 4), with NATIVE/ADD-ON/PARTNER/GAP
  composition as a stacked bar per row. Bottom half: top-5 vendors heatmap drill for direct
  comparison.

## Headline Numbers

- 703 cells total: **249 NATIVE · 208 ADD-ON · 14 PARTNER · 232 GAP**
- Top vendor by NHI score: **HashiCorp Vault Enterprise (191)**
- Bottom vendor by NHI score: **Fortanix DSM (62)**
- 22 of 37 NHIs flagged as XYZ-confirmed GAP (joined via UC-level GAP states from
  `anz-current-state.csv`)

## Coverage Score Formula

`score(vendor) = Σ over NHIs of: SCORE[coverage] × (1 + 0.2 × maturity)`
where `SCORE = {NATIVE: 4, ADD-ON: 2, PARTNER: 1, GAP: 0, N/A: 0}`.

This rewards NATIVE depth twice as heavily as ADD-ON, and slightly amplifies maturity.
Worth confirming with the user — if procurement weights ADD-ON more (e.g., because
"add-on" implies extensibility), the ranking re-shuffles. The formula is one Python
line in `build.py` and is the most opinionated piece of this sketch.

## What to Look For When Comparing Variants

| Question | A | B | C |
|---|---|---|---|
| Can you see ALL gaps at once? | ★ yes (every cell visible) | ★ yes (with XYZ context) | ▽ no (only top 5 drilled) |
| Decision support — "which vendor first?" | ▽ requires scanning columns | ▲ same as A with context | ★ explicit ranking |
| Survives B&W print? | ▽ relies on color | ▲ color + bucket dividers | ★ bars survive B&W |
| Architect reading time on first open? | ▲ ~60 sec to orient | ★ ~30 sec (bucketed) | ★ ~15 sec (ranked) |
| Useful for procurement defensibility? | ▲ raw evidence | ▲ raw evidence | ★ explicit ranking + score breakdown |

## Open Questions for the User Review

1. The coverage score formula (above) is opinionated — does it match how XYZ weights
   NATIVE vs ADD-ON? Should PARTNER be excluded entirely (since it implies vendor lock-in)?
2. Variant B highlights rows where XYZ has a confirmed UC-level GAP. Is that the right
   XYZ-relevance signal, or should we use a different join (e.g., NHIs known to exist
   in the XYZ estate)?
3. Variant C ranks vendors purely on NHI coverage. Should the leaderboard also reflect
   UC coverage (47 UCs × 19 vendors = 894 more cells)? Combined score?
4. The maturity numeric (0–5) is rendered inside cells. Useful, or visual noise?
   Toggle option?

## Files

- `build.py` — regenerates `index.html` from CSVs. Run from this directory.
- `index.html` — generated artifact, ~225 KB (data inlined).

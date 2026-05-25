---
sketch: 001
name: risk-posture-one-pager
question: "Can a single page communicate 'are we covered?' to a board in under 30 seconds, then survive print to A3?"
audience: CISO / Board / Executive
winner: null
tags: [board, dashboard, rag, print, stage-1]
---

# Sketch 001 — Risk Posture One-Pager

## Design Question

Can a single page communicate *"are we covered, and what's our regulatory exposure?"*
to a non-technical executive audience in under 30 seconds, and survive the
print-to-PDF board-pack distribution path?

## How to View

From the repo root:

```sh
open .planning/sketches/001-risk-posture-one-pager/index.html
```

Print test:

```sh
# In the browser tab: Cmd-P (mac) / Ctrl-P. Layout: portrait, fit-to-page.
```

## Variants

- **A: Classic dashboard** — Headline KPI tiles (5 numbers) → RAG heatmap by NHI bucket
  (COMMON vs UNCOMMON, 37 NHIs as click-chips) → APRA CPS-234 25-cell exposure strip.
  Enterprise-familiar pattern. Highest information density.
- **B: Narrative one-liner** — Serif headline that *speaks the finding* in one sentence,
  followed by one focal stacked bar (state distribution) and three APRA roll-up cards.
  Optimised for executive retention; lowest cognitive load.
- **C: Risk register table** — Looks like an internal-audit register. All 47 UCs in a
  sorted table by priority+state, with NHIs in scope and APRA back-map columns.
  Optimised for risk committees and audit teams who want defensibility, not a story.

## Headline Numbers (2026-Q2 baseline)

- 47 controlled outcomes (UCs); states: **11 GAP / 16 PARTIAL / 20 PENDING / 0 MET**
- 12 P0 outcomes; **4 P0 outcomes confirmed as GAPs** (highest residual risk)
- 37 NHI types; **22 NHIs touch at least one GAP UC** (red)
- APRA CPS-234 (25 controls): **14 RED (any GAP), 11 AMBER (PARTIAL), 0 GREEN**

## What to Look For When Comparing Variants

| Question | A | B | C |
|---|---|---|---|
| 30-second comprehension? | ▲ moderate (5 numbers to scan) | ★ high (one sentence) | ▽ low (table — needs reading) |
| Defensibility for audit? | ▲ moderate | ▽ low (story only) | ★ high (per-UC row) |
| Survives B&W print? | ▲ uses color heavily | ★ text-driven, prints clean | ★ table prints clean |
| Density on one A3 page? | ▲ tight but fits | ★ generous | ▽ may overflow at 47 rows |
| Honest about PENDING state? | ★ shows it as separate tier | ★ shows it in the sentence | ★ explicit column |

## Rollup Semantics (used in A and B)

For each NHI bucket and each APRA control, the visual state rolls up from the worst
touching UC, using order: `GAP > PARTIAL > PENDING > MET`. Rationale: a known GAP is
a stronger board signal than a not-yet-assessed PENDING — the latter is uncertainty,
the former is a confirmed issue. Toggling the rollup priority would re-paint the page;
worth confirming with the CISO before lock-in.

## Open Questions for the User Review

1. Does the rollup semantic (`GAP > PARTIAL > PENDING > MET`) match how XYZ leadership
   reads risk? Or should PENDING be treated as worse-than-PARTIAL ("we don't know" is
   itself a finding)?
2. Variant A's 5-KPI tile set — are these the right 5 headlines? Specifically:
   should "PENDING NHIs" be replaced with something more actionable?
3. Should Variant C include a "next action" / "remediation owner" column, or keep
   it as a pure state snapshot?
4. Does the neutral palette read as credible, or does it need brand mirror retrofit
   (deferred per Stage-1 plan)?

## Files

- `build.py` — regenerates `index.html` from CSVs. Run from this directory.
- `index.html` — generated artifact (do not edit by hand).

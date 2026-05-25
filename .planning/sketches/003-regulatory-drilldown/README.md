---
sketch: 003
name: regulatory-drilldown
question: "Can a Risk & Compliance reader trace one regulatory paragraph all the way to vendor evidence — in three clicks or fewer — and still print clean for an APRA audit pack?"
audience: Risk & Compliance (APRA-facing)
winner: null
tags: [traceability, drill-down, compliance, apra, stage-1]
---

# Sketch 003 — Regulatory Traceability Drill-down

## Design Question

Can a Risk & Compliance reader trace **one regulatory paragraph → UCs that satisfy it →
NHIs in scope → vendor evidence with citations** in three clicks or fewer, and still print
clean enough to ship in an APRA audit pack?

## How to View

From the repo root:

```sh
open .planning/sketches/003-regulatory-drilldown/index.html
```

## Variants

- **A: Master/detail** — Left rail = all 145 controls grouped by framework, with state-dot +
  UC count. Right pane shows the selected control's full chain: UCs (with state + priority +
  acceptance criteria), NHIs in scope (as pills), and top vendor evidence per UC with
  evidence quote + URL. Default selection: APRA CPS-234 first control.
- **B: Cascading columns** — Four side-by-side columns (Framework → Control → UC → Vendor
  evidence). Click left-to-right; each selection populates the next column. Optimised for
  exploratory navigation; weakest for print.
- **C: Tree (print-ready)** — Fully expanded indented tree: framework header → control →
  uc rows → top-3 vendor evidence rows. Framework filter dropdown to narrow scope.
  Default = APRA CPS-234. Survives print-to-PDF as a single document; closest to how
  an audit pack appendix would look.

## Headline Numbers

- **7 frameworks** mapped: Essential 8 (26), NIST ZTA (13), **APRA CPS 234 (25)**,
  APRA CPS 230 (6), APRA CPG 234 (3), ASD ISM (41), MITRE ATT&CK (31).
- **145 control rows** total in `regulatory-trace.csv`
- **47 UCs** indexed with state, priority, acceptance criteria
- **893 vendor-UC evidence rows** = 47 UCs × 19 vendors, ranked by coverage tier then maturity
- **37 NHIs** linked by `nhi_ids` per control row

## Per-Control Rollups (computed at build time)

Each control row carries three derived properties:

| Property | How computed | Used in |
|---|---|---|
| `anz_state` | Worst XYZ-state across all UCs the control demands (GAP > PARTIAL > PENDING > MET) | State-dot in rail + tree |
| `vendor_strength` | Mean of best-per-UC coverage scores (NATIVE=4 / ADD-ON=2 / PARTNER=1 / GAP=0) | Available in data; not yet surfaced visually |
| `best_vendors` | Top-5 vendors by count of NATIVE coverage across the control's UCs | "Top NATIVE vendors" line in Variant C |

## What to Look For When Comparing Variants

| Question | A | B | C |
|---|---|---|---|
| Three-click trace (control → vendor)? | ★ ~2 clicks (rail + control) | ★ exactly 3 clicks | ★ 0 clicks (all expanded) |
| Density on one screen? | ★ rail + detail | ▲ four columns; can feel cramped | ▽ scrolls — many pages |
| Print to PDF (audit appendix)? | ▽ master-detail loses left rail content | ▽ cascading columns don't reflow | ★ tree prints as a linear document |
| Quickly switch between frameworks? | ▲ scroll rail | ★ first column | ★ filter dropdown |
| Audit defensibility (sources?) | ▲ shows evidence quote per vendor row | ▲ same on demand | ★ evidence shown inline always |

## Open Questions for the User Review

1. The **state rollup priority** (`GAP > PARTIAL > PENDING > MET`) matches Sketch 001;
   confirm it's the right reading for compliance audiences specifically.
2. Variant A only displays the **top-4 vendors per UC**. Should it show all 19 with a
   "show more" toggle, or is 4 the right ceiling for executive reading?
3. APRA CPS-234 is the implicit default everywhere — is that right, or should the
   landing default rotate based on a "today's focus framework" setting?
4. The **`best_vendors`** computation (count of UCs where vendor is NATIVE) is one of
   several possible "vendor leaders per control" formulas. Should the count be
   maturity-weighted? Use a weighted score instead of raw NATIVE count?
5. Variant C currently shows top-3 vendor evidence per UC. For a 25-control APRA pack
   this generates ~75 vendor rows. Is that the right tradeoff between defensibility
   and reading load?
6. Should evidence URLs be **resolved to citation keys** (from `meta/citations.bib`,
   485 entries) instead of raw URLs? More credible for audit; more build complexity.

## Files

- `build.py` — regenerates `index.html` from CSVs. Run from this directory.
- `index.html` — generated artifact, ~365 KB (data inlined).

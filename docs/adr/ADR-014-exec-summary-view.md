# ADR-014: Exec-Summary View (client-facing deliverable)

**Status:** Accepted
**Date:** 2026-05-31
**Workstream:** WS-4 slice 3

## Context
WS-4 slices 1–2 produced the methodology (`methodology/PLAYBOOK.md` + `METHODOLOGY.md`) and the
`engagement-menu/v1` generator (`questionnaire/roadmap_generator.py`). What was still missing was the
client-facing rendering of that output. This slice renders the deliverable — the exec summary the
client actually reads — completing WS-4.

## Decision
A self-contained interactive `exec-summary.html` built by `presentation/build_exec_summary.py`,
mirroring the questionnaire build:

- The posture snapshot is computed in Python via `record_state.resolve_state`, and the prioritised
  engagement menu via `roadmap_generator` (generator-as-library). The resulting data plus
  `exec-summary.css` and `exec-summary.js` are inlined into `exec-summary-template.html`, so the
  output is one portable file with no asset fetches.
- JS is dual-mode plain-script: pure helpers are Node-tested while the DOM wiring runs in the
  browser, so the same file is unit-tested and shipped.
- The brand is dark signal-lime on screen; `@media print` flips to white/ink with page breaks for a
  clean printed appendix. The snapshot counters carry their true final in `data-value`, and a
  `beforeprint` handler forces finals so the printed numbers are always correct (no half-animated
  counters on paper).
- `client` and `as_of` are optional build inputs so the build stays byte-stable — there is no
  auto-injected timestamp.
- The on-screen aesthetic was produced with the `frontend-design` skill.

## Alternatives rejected
- **Server-side static (no JS):** dropped once an interactive microsite (filterable/sortable
  quadrant board, animated snapshot) was the chosen experience.
- **Embedding a summary block into `engagement-menu/v1`:** avoided to keep the v1 schema frozen; the
  view is a pure consumer of the generator output.
- **Server-side PDF:** rejected in favour of browser Print → Save as PDF, which is why the print
  stylesheet and `beforeprint` handler carry the burden.

## Consequences
- (+) WS-4 is complete: methodology → engagement-menu generator → client-facing exec summary.
- (−) The view depends on the generator + `record_state`; a change to either ripples here — covered
  by the exec-summary tests so the breakage surfaces immediately.
- Fonts load via CDN — the only external dependency, matching the existing decks
  (`value-proposition.html`, `educational-overview.html`).

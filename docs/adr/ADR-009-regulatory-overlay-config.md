# ADR-009: Selectable Regulatory Overlay via Externalized YAML Config

**Status:** Accepted
**Date:** 2026-05-29
**Workstream:** WS-2

## Context
The report engine (`matrix/build_matrix_viewer.py`) hardcoded framework labels,
per-vendor AU residency/IRAP data, and an implicit all-frameworks scope with
FI/APRA-flavoured, residency-first vendor ordering. This blocked reuse for
non-FI, non-APRA clients.

## Decision
Externalize framework labels and vendor residency to `matrix/config/*.yaml`.
Add an engagement config (preset + inline override + CLI) that scopes the report
to selected framework(s) + overlays over an always-on Essential 8 baseline, and a
residency `weight` (high|medium|low|off) + independent `irap_required` gate. A
no-config run reproduces the previous output exactly (golden regression test).
Ship 4 presets: financial, government, retail, baseline.

## Consequences
- (+) Industry-agnostic scoping with zero new research; WS-3 JS toggle enabled via
  `framework_selection.available` metadata.
- (−) Adds a PyYAML runtime dependency (`requirements.txt`), trading away
  bare-`python3` portability for human-editable config. Mitigated by a clear
  install-error message.
- Scope limited to the 7 frameworks in `regulatory-trace.csv`. Privacy Act,
  My Health Record, PSPF, SOCI (and a health preset) are deferred to a future
  new-research workstream; configs referencing them are warned and skipped.
- A YAML gotcha: a bare `weight: off` is parsed by PyYAML as the boolean `False`;
  the resolver normalizes it back to the string `"off"`.

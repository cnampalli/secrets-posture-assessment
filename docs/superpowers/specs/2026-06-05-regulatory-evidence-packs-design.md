# Regulatory-Driven Evidence Packs for PAM — Design

**Date:** 2026-06-05
**Status:** Approved (brainstorm + grilling), implementing vertical slice
**Domain:** PAM first; framework designed domain-agnostic

## Problem

The assessment questionnaire's evidence requirements are open-ended. A non-technical workshop
facilitator can't drive the session because nothing tells them *what evidence to ask the client
for* against each question. Separately, regulatory controls are currently **back-mapped**
(derived) from use cases — the regulatory lens is an output, not a driver.

## What we're building

**Invert the flow.** The regulatory control becomes the authoring entry point. Per control we
author an **evidence pack** — concrete, vendor-neutral artifacts the client must produce — and
that evidence flows *down* into the use-case questions via the existing control→use-case join.
For every question a facilitator asks, the instrument shows exactly which artifacts to request,
traceable to the regulator's own words.

This pass delivers a **runnable vertical slice**: full machinery + one fully-worked control family
(credential vaulting / rotation), end-to-end in the questionnaire. It proves the schema before we
author the remaining ~60 PAM control packs.

## Design decisions (locked)

| Decision | Choice |
|---|---|
| Domain | PAM first |
| Architecture | Regulatory packs drive *what evidence*; archetypes (A1–A8) drive *question shape + scoring ladder*. Composed, not either/or. |
| Grain | Per control, tiered **primary + follow-up**, vendor-neutral requirement first, optional non-authoritative `example_artifact` hint |
| Dedup | Canonical **evidence catalog** of stable-ID'd items (`EV-PAM-*`); controls reference item IDs; a UC's evidence = deduped union across its controls → "one artifact → many controls" reverse view |
| Binding | Evidence items attach to a UC's archetype questions **by shared `dimension`**; primary→`GAP_PARTIAL` rung, follow-up→`PARTIAL_MET` rungs. Scoring engine unchanged — evidence *decorates* questions, adds no scored items |
| Provenance | Each `EV-*` carries `citation_keys`, anchored to its control's existing `evidence_quote`/`evidence_url`. New F-gate enforces resolution + citation. `example_artifact` marked non-authoritative |
| UI | Progressive drill-down — primary shown on the question; follow-ups behind an expander |
| Mapping location | New optional `evidence_item_ids` column on `regulatory-trace.csv` (co-located with the control) |
| Surfaces | Questionnaire now (workshop driver); report compliance-trace evidence view is the immediate follow-on |
| SECRETS future-proofing | A0 bespoke UCs attach packs at UC-level (no dimension); pack authoring skips `ADVERSARY-LENS` frameworks (e.g. MITRE) |

## Data model

**New — `matrix/domains/pam/evidence-catalog.csv`:**
`ev_id, requirement, dimension, tier, example_artifact, sensitivity_tag, citation_keys`
- `ev_id`: stable, e.g. `EV-PAM-VAULT-REGISTER`
- `requirement`: vendor-neutral ("a register showing which privileged accounts are vaulted and their rotation policy")
- `dimension`: one of coverage/enforcement/depth/cadence/governance/exception (archetype vocabulary)
- `tier`: `primary` | `follow-up`
- `example_artifact`: non-authoritative hint ("e.g., CyberArk AD-group config export")
- `sensitivity_tag`: ADR-005 vocab; warns facilitator when the collected artifact is e.g. `[SENSITIVE]`
- `citation_keys`: ≥1 required

**New — `matrix/domains/pam/uc-archetype-map.csv`:** `uc_id, archetype_id, params, notes`
(slice: UC-P-001=A4, UC-P-002=A1, UC-P-003=A3)

**Modified — `matrix/domains/pam/regulatory-trace.csv`:** add optional `evidence_item_ids` column
(`;`-list of `ev_id`) on the credential-vaulting/rotation + session control rows.

## Binding algorithm (per UC)

1. Resolve UC's archetype questions (dimensions) from `uc-archetype-map.csv` + shared templates.
2. Find controls backing the UC: `regulatory-trace.csv` rows whose `uc_ids` contains the UC and
   whose `framework_role` is a compliance role (`PRIMARY-LENS`/`BACK-MAP`), excluding `ADVERSARY-LENS`.
3. Union those controls' `evidence_item_ids`; dedup; resolve to catalog items; annotate each item
   with the set of backing controls it satisfies (for this UC).
4. Attach each item to questions sharing its `dimension`; within a question, `primary` shown,
   `follow-up` behind drill-down.
5. Items whose dimension matches no question → per-UC "additional evidence for compliance" list.
6. (Future SECRETS) A0 bespoke UC → attach all items at UC level; keep existing inline evidence.

## Components

- `questionnaire/rubric_loader.py` — `load_rubric(meth_dir, data_dir=None)`; shared templates from
  `meth_dir`, domain map/catalog/trace from `data_dir`; evidence binding helper. Backward compatible.
- `questionnaire/build_questionnaire.py` — `build(out_path=None, data_dir=None)`; builds a PAM
  questionnaire when given the PAM data dir.
- `questionnaire/template.html` + `app.js` — render primary/follow-up drill-down per question;
  `scoring.js` unchanged.
- `matrix/validate_data.py` — `check_evidence_packs(trace, catalog)`: every referenced `ev_id`
  resolves; every referenced item has ≥1 `citation_keys`; `dimension`/`tier` enums; skip
  `ADVERSARY-LENS` rows; only runs when `evidence-catalog.csv` exists.

## Verification

- `python matrix/validate_data.py --data-dir matrix/domains/pam` passes; **fails** on a broken
  `evidence_item_ids` ref or an uncited referenced item (prove the gate).
- `pytest` green (new + existing suite).
- Build PAM questionnaire, open with the Playwright harness: UC-P-001 shows A4 maturity questions,
  each with a primary evidence ask visible + follow-ups behind drill-down; an artifact shared
  across controls appears once and lists the controls it satisfies; scoring still resolves.

## Out of scope (immediate follow-on)

- Report compliance-trace evidence view + reverse card.
- Authoring the remaining ~60 PAM control packs.
- SECRETS evidence packs (rules designed; authoring later).

# IGA Scoping Spike — Design Spec

_2026-06-09. Phase 3 kickoff. A throwaway-ish **scoping spike** that validates a hybrid
model for the IGA (Identity Governance & Administration) offering before any
citation-backed data authoring._

## Problem / why a spike

Phase 3 is "IGA / SailPoint as a scoped offering." The roadmap flags the crux:
**"IGA is process-shaped — don't force it into the capability matrix."** Secrets and PAM
both fit a vendor × use-case capability matrix (NATIVE/ADD-ON coverage). IGA's real
differentiator is *process maturity* (joiner/mover/leaver, certification, segregation of
duties, role/request governance) — the major suites mostly all "have" the features, so a
capability matrix misrepresents the domain.

We chose a **hybrid model**: a process-maturity assessment core **plus** a *light* vendor-fit
overlay. That model is unproven, and real IGA data needs citation-backed research (fabrication
is a known project hazard). So we de-risk exactly as PAM was de-risked (Phase 0.5 spike →
Phase 2 real data): a thin, **illustrative** end-to-end slice that proves the model and
surfaces where the existing engine reuses vs. needs a new view.

## Goal

Prove (or disprove) two hypotheses with illustrative data, and produce a findings doc that
green-lights (or reshapes) full Phase 3:

1. **Questionnaire/archetype reuse** — the domain-agnostic `rubric_loader` + the existing
   archetypes (A1/A2/A3/A5/A7/A8) cleanly express IGA process-maturity use cases, with **no
   engine changes**. *Expected: holds.*
2. **Vendor-overlay seam** — the capability-matrix report engine
   (`report_logic.build_vendormix` etc., via `build_matrix_viewer.py`) either accommodates a
   *light* vendor-fit overlay or reveals the seam where IGA needs its own lighter view.
   *Expected: the matrix wants fine-grained per-UC NATIVE/ADD-ON; the hybrid overlay is coarser
   → documents the need for a dedicated IGA vendor-fit view in full Phase 3.*

**Acceptance:** `run_iga_spike.py` runs clean; `iga-questionnaire.html` builds with all
illustrative IGA use cases and no unresolved `{slots}`; `SPIKE-FINDINGS.md` states a clear
verdict + recommendation for full Phase 3.

## Non-goals (YAGNI — explicitly deferred to full Phase 3)

- **No citation-backed real data.** All CSVs are ILLUSTRATIVE and labelled as such.
- **No production domain registration** (`matrix/config/domains/iga.yaml`, `matrix/domains/iga/`).
- **No React-app IGA wiring** (the domain-aware app already supports adding a domain later).
- **No new report renderer.** The spike *identifies* whether one is needed; building it is
  Phase 3 proper.

## Location & isolation

Everything lives under **`spikes/iga/`** (mirrors `spikes/pam/`), isolated from production
`matrix/domains/`. Nothing in `matrix/` changes. Like the PAM spike, files carry an
ILLUSTRATIVE banner.

## Components

### 1. Illustrative IGA use cases — `spikes/iga/iga-use-cases.csv` + `iga-uc-archetype-map.csv`
~11 use cases across the four chosen process areas, each mapped to an existing archetype with
every question-template slot filled (same authoring rules as the PAM `uc-archetype-map.csv`):

| uc_id | Area | Title | Archetype |
|---|---|---|---|
| UC-I-001 | JML | Automated joiner / birthright provisioning | A2 (migration) |
| UC-I-002 | JML | Mover access recalculation on transfer | A7 (governance process) |
| UC-I-003 | JML | Timely leaver de-provisioning | A2 (migration) |
| UC-I-004 | Certification | Periodic access certification campaigns | A5 (inventory & attestation) |
| UC-I-005 | Certification | High-risk access certification sign-off | A8 (periodic assurance artifact) |
| UC-I-006 | SoD | Preventive SoD checks at request time | A1 (preventive guardrail) |
| UC-I-007 | SoD | SoD policy register & violation management | A7 (governance process) |
| UC-I-008 | SoD | Detective SoD scanning of existing access | A3 (capability adoption) |
| UC-I-009 | Role/Request | Role mining & RBAC baseline | A3 (capability adoption) |
| UC-I-010 | Role/Request | Self-service access request & approval | A7 (governance process) |
| UC-I-011 | Role/Request | Least-privilege entitlement right-sizing | A2 (migration) |

This spread deliberately exercises **A1, A2, A3, A5, A7, A8** — proving the archetype library
covers IGA's process shape. (`uc_id` prefix `UC-I-*`; categories FUNCTIONAL except detective
analytics UC-I-008 → NON_FUNCTIONAL.)

### 2. IGA questionnaire — `spikes/iga/iga-questionnaire.html`
Built with the existing domain-aware loader — no new code:
`python3 questionnaire/build_questionnaire.py --data-dir spikes/iga --out spikes/iga/iga-questionnaire.html`.
Proves the process-maturity instrument works end-to-end on IGA with zero engine changes.

### 3. Light vendor-fit overlay — `spikes/iga/iga-vendor-fit.csv`
Illustrative, coarse-grained: vendors **SailPoint, Saviynt, Microsoft Entra ID Governance,
Okta Identity Governance** × the **four process areas**, each cell a coarse fit
(`supports` / `partial` / `add-on`). Deliberately **not** a per-UC NATIVE/ADD-ON matrix —
this is the artifact the spike feeds (adapted) toward the existing engine to expose the seam.

### 4. Spike runner — `spikes/iga/run_iga_spike.py`
Mirrors `run_pam_spike.py`. Two probes:
- **Probe A (questionnaire/archetype):** load the IGA rubric via `questionnaire.rubric_loader`
  against `spikes/iga/`; assert it resolves all ~11 UCs as ladder questions with no leftover
  `{slots}`; print the count. (Should pass clean → hypothesis 1 holds.)
- **Probe B (vendor overlay):** attempt to shape `iga-vendor-fit.csv` toward the capability-
  matrix engine and record what fits vs. what leaks (e.g. the engine expects per-UC
  vendor-capability rows + identity-catalog; the coarse per-area overlay doesn't map 1:1).
  The runner **documents** the mismatch rather than forcing a render.
- Prints an ILLUSTRATIVE-DATA banner. Exits non-zero only on an *unexpected* failure of Probe A
  (Probe B's mismatch is an expected, recorded finding, not a crash).

### 5. Findings — `spikes/iga/SPIKE-FINDINGS.md`
Sections mirroring `spikes/pam/SPIKE-FINDINGS.md`: **Hypothesis · Method · Result · What reuses
cleanly · What needs a new view · Verdict & recommendation (for full Phase 3) · Status.** The
verdict states whether the hybrid model holds and what full Phase 3 must build (expected: a
dedicated lightweight IGA vendor-fit view + citation-backed data authoring).

## Data flow

```
iga-use-cases.csv + iga-uc-archetype-map.csv
        │  (existing, unchanged) questionnaire/rubric_loader + build_questionnaire.py --data-dir
        ▼
iga-questionnaire.html         ← Probe A: process-maturity instrument (expected: clean reuse)

iga-vendor-fit.csv  ──shape──▶ existing capability-matrix engine?  ← Probe B: records the seam
        ▼
SPIKE-FINDINGS.md  (verdict + recommendation for full Phase 3)
```

## Error handling

- Probe A failure (unresolved slot / unmapped archetype) = a real finding → runner exits
  non-zero with the offending uc_id/qid. This is the engine-reuse hypothesis breaking.
- Probe B mismatch = expected; captured as prose in the findings, not a crash.
- All illustrative CSVs validated only for archetype-map well-formedness (params parse, slots
  fill) — **not** through the production provenance gate (no citation data in a spike).

## Testing

Spikes in this repo are runner-driven, not pytest-gated (see `spikes/pam/`). Mirror that:
- `run_iga_spike.py` carries inline assertions (Probe A resolves all UCs, no leftover slots).
- One lightweight pytest is justified to keep the archetype mapping honest:
  `tests/test_iga_spike.py` — load `spikes/iga` via `rubric_loader`, assert all ~11 `UC-I-*`
  resolve as ladders with no `{` in any question text. (Cheap regression guard; mirrors the
  PAM rubric-loader assertions.)
- Full existing suite must stay green (nothing in `matrix/`, `questionnaire/`, or `app/`
  changes, so it should be untouched).

## Verification / rollout

1. `python3 spikes/iga/run_iga_spike.py` → Probe A clean, Probe B mismatch recorded, ILLUSTRATIVE banner.
2. `python3 questionnaire/build_questionnaire.py --data-dir spikes/iga --out spikes/iga/iga-questionnaire.html` → 11 use cases.
3. `python3 -m pytest tests/test_iga_spike.py -q` and full `python3 -m pytest -q` → green.
4. `SPIKE-FINDINGS.md` verdict written → green-lights / reshapes full Phase 3.

## Assumption (stated in the spike banner)

Same AU FI regulatory context as Secrets/PAM (APRA CPS 234 / CPS 230, ISM, Essential 8) plus
IGA-relevant SoD / SOX-style ITGC framing — all illustrative, to be replaced with
citation-backed mappings in full Phase 3.

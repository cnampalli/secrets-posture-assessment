# Phase 3 — IGA scoping spike: findings

_ILLUSTRATIVE spike. Data in `spikes/iga/` is placeholder, not a verified IGA/vendor assessment._

## Hypotheses
A) The questionnaire/archetype engine expresses IGA process-maturity use cases with no engine changes.
B) The capability-matrix engine does not fit a light per-area vendor-fit overlay (IGA is process-shaped).

## Method
- Authored 11 illustrative IGA use cases (`use-cases.csv` + `uc-archetype-map.csv`) across JML,
  Certification, SoD, and Role/Request, mapped to archetypes A1/A2/A3/A5/A7/A8.
- Probe A: loaded them through the unchanged `questionnaire.rubric_loader`; built `iga-questionnaire.html`.
- Probe B: shaped a coarse per-area vendor-fit overlay (`iga-vendor-fit.csv`) toward the capability-matrix engine.

## Result: ✅ HYBRID MODEL HOLDS
- **Probe A:** all 11 use cases resolved as ladder questions; archetypes exercised = [A1, A2, A3, A5, A7, A8];
  `iga-questionnaire.html` built with 11 use cases (28,903 bytes); zero engine changes. The governance
  archetypes fit IGA especially cleanly — certification → A5 (inventory & attestation), JML mover /
  SoD policy / access-request governance → A7, high-risk certification sign-off → A8.
- **Probe B:** the per-area coarse overlay (4 vendors × 4 areas) does NOT map 1:1 onto the capability
  matrix, which expects per-USE-CASE NATIVE/ADD-ON coverage plus an identity-catalog scored against a
  current-state. Confirmed the predicted seam.

## What reuses cleanly
- `questionnaire/rubric_loader.py`, `build_questionnaire.py`, and the archetype library — unchanged.
- The process-maturity instrument is fully functional for IGA today.

## What needs a new view (full Phase 3 build)
- A dedicated **lightweight IGA vendor-fit view** (per-area / per-process support), separate from the
  NATIVE/ADD-ON capability matrix used by Secrets/PAM.
- Citation-backed replacement of all illustrative data (use cases, regulatory trace, vendor fit).
- Production domain registration + React-app wiring (deferred).

## Verdict & recommendation
Green-light full Phase 3 on the hybrid model: reuse the questionnaire/archetype engine as-is for the
process-maturity core; build a small bespoke vendor-fit renderer rather than forcing IGA into the
capability matrix. Sequence: data research → questionnaire (works now) → vendor-fit view → cross-domain.

## Status
Spike complete; illustrative artifacts in `spikes/iga/`. No production code touched.

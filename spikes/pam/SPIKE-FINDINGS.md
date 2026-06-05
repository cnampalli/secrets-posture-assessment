# Phase 0.5 — PAM domain spike: findings

Date: 2026-06-05 · Branch: `spike/pam-domain` (off `feat/phase0-vendor-mix-optimizer`)

## Hypothesis
The Phase 0 analytic core and report model-builders are **domain-agnostic** — a PAM
dataset should run through `report_logic.build_vendormix / build_vendor_intel /
build_compliance` (and the optimizer/resilience/vendor_intel/compliance modules) with
**zero changes to any `matrix/*.py` file**, requiring only new data + light config.
This is the decision gate before investing in Phase 1 (engine generalisation).

## Method
- Hand-built a minimal, **illustrative** PAM domain: 11 use cases, 3 vendors
  (CyberArk PAM, Delinea, BeyondTrust), 33 capability rows, 4 control mappings, a
  sample posture. (`spikes/pam/pam-*.csv` — coverage/maturity are spike values, not a
  verified vendor assessment.)
- Wrote `run_pam_spike.py` that imports the **unchanged** Phase 0 modules and runs the
  same model functions the secrets report uses, against the PAM data.
- Reused the existing `vendor-ownership.yaml` and `frameworks.yaml` configs as-is.

## Result: ✅ ABSTRACTION HOLDS
`git diff feat/phase0-vendor-mix-optimizer...spike/pam-domain -- matrix/` is **empty** —
the entire spike is additive under `spikes/`. The Phase 0 core produced correct,
sensible PAM output with no module edits:

- **Vendor mix:** BeyondTrust + CyberArk PAM cover 10/11 UCs NATIVE across 2 parents.
- **White-space:** `UC-P-011` (secretless workload attestation) correctly flagged — PAM
  has no NATIVE coverage. *Cross-domain insight: this capability lives in the secrets/
  NHI domain, not PAM.*
- **Single-source:** EPM (`UC-P-009`) flagged as single-parent (BeyondTrust only).
- **Concentration / ownership graph carried over:** `cyberark-pam` rolled up to parent
  `cyberark` (90% of UCs) — the **same parent that dominated the secrets domain**. The
  cross-domain concentration thesis is real and the ownership graph is reusable.
- **Best-vendor-per-UC, head-to-head, coverage indicator, gap-to-target, complement**
  all ran unchanged; coverage indicator surfaced MET for the assessed MFA control.

All 5 spike assertions PASS.

## What was NOT reusable (the expected Phase 1 seams — no surprises)
The leaks are exactly the secrets-specific seams the roadmap already names; none are
deep/structural:

1. **I/O loader** — `report_io.load_inputs` hardwires the secrets filenames + the
   substrate exclusion; the spike bypassed it with `read_csv`. → per-domain data paths.
2. **`VENDOR_LAYER` / `SHORT`** — secrets-specific maps in `report_io`. The *new* Phase 0
   functions don't depend on `VENDOR_LAYER` (only the legacy `build_recdata` does), but
   `SHORT` (display names) had to be supplied in the runner. → per-domain config.
3. **`anchors`** (which incumbents seed the complement view) — supplied in the runner.
   → per-domain config / policy.
4. **Report template** — not exercised (spike used the model layer, not the HTML build).
   → per-domain rendering is the remaining Phase 1 work.

Notably, `frameworks.yaml` and `vendor-ownership.yaml` were **reused unchanged** —
regulatory frameworks and corporate ownership are genuinely cross-domain.

## Verdict & recommendation
**Green-light Phase 1.** PAM (capability-shaped, like secrets) fit the existing
`target_type`/`coverage`/`maturity` schema with no model changes — confirming the
"shared engine + per-domain model" architecture for capability-shaped domains. Phase 1
should generalise the four seams above (loader, layer/short maps, anchors, template)
into per-domain config, then re-express secrets through it as the regression anchor.

**Caveat for IGA (later):** PAM validated the *capability-shaped* case. IGA is
process-shaped (JML, recertification, SoD) and remains the real test of whether the
schema generalises beyond capability coverage — keep it scoped and sequenced last, per
the roadmap.

## Status
Throwaway spike (illustrative data). Keep for reference; do not ship the PAM CSVs as a
real assessment. Real PAM data would be manufactured via the prompt pipeline with the
provenance gate applied.

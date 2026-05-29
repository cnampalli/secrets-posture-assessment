# Design Spec — WS-1: Assessment Scoring Rubric (Archetype Library)

**Date:** 2026-05-29
**Status:** Approved (brainstorming complete) — ready for implementation planning
**Workstream:** WS-1 of `meta/IMPROVEMENT-BACKLOG.md`
**Builds on:** ADR-006 (scoring vocabulary), ADR-007 (sourcing-confidence posture)

---

## 1. Purpose

Formalise the methodology by which a client's secrets-management posture is scored, so the
assessment is **defensible, repeatable, and reusable across any AU client in any industry**.
Today, each of the 47 use-cases is scored MET/PARTIAL/GAP/PENDING by expert judgment with no
documented per-UC criteria and no explicit confidence rule. WS-1 makes that connective tissue
explicit and portable.

This spec is the substance ("the rubric"). The interactive instrument (WS-3) and the
regulatory-overlay engine (WS-2) consume it but are out of scope here.

## 2. Decisions locked (grill + brainstorming)

| # | Decision | Outcome |
|---|----------|---------|
| G1 | De-target model | Universal core + selectable regulatory overlay (WS-2). Rubric is industry-agnostic. |
| G2 | Methodology output | 3-state verdict (MET/PARTIAL/GAP, +N/A, +PENDING) as the atomic output, defined via decomposed criteria; maturity roll-up is a future derived view, not a rewrite. |
| G3 | Scoring autonomy | **Rubric-assisted + override** — rubric proposes a state; assessor confirms or overrides with recorded rationale + confidence. |
| G4 | Front door | Facilitated-primary, architected as "both"; current-state file = single source of truth. |
| B1 | Authoring approach | **Archetype library + A0 bespoke fallback.** Archetypes built bottom-up from existing `acceptance_criteria` (grounded, not invented). |
| B2 | File location | New `methodology/` directory = the reusable Library layer, separate from client data and vendor data. |
| B3 | Naming constraint | **No new `anz`/`ANZ` references.** All WS-1 artifacts use client-generic names (`current_state`, not `anz_state`). The frozen `matrix/anz-current-state.csv` is a read-only *input* to the dogfood only; its rename to a client-generic name is WS-5, not WS-1. |

## 3. The archetype model

An **archetype** is a reusable scoring pattern. Every use-case maps to one (occasionally two)
archetypes; each archetype defines *generically* what MET/PARTIAL/GAP mean for that *kind* of
control, then is parametrised per UC. A genuinely unique UC maps to **A0 (Bespoke)** and carries
its own criteria instead of inheriting a template.

Initial archetype set (derived from reading all 47 UCs — to be verified/adjusted during build):

| # | Archetype | Measures | Seed UCs |
|---|-----------|----------|----------|
| A0 | **Bespoke** | Long-tail UCs that resist patterning | UC-F-017, UC-F-026 (candidates) |
| A1 | **Preventive Guardrail** | Control enforced at a gate (block/deny) + coverage + exception path | UC-F-001, F-008, F-022 |
| A2 | **Population Migration / Coverage** | % of an identity population on a target pattern + legacy burn-down + registered exceptions | UC-F-003, F-006, F-013, F-019, F-023 |
| A3 | **Capability Adoption** | Capability deployed *and adopted* to depth + config thresholds | UC-F-004, F-005, F-010, F-017 |
| A4 | **Lifecycle Automation** | Issuance / rotation / revocation automated within SLA | UC-F-007, F-016, F-020, F-021 |
| A5 | **Inventory & Attestation** | Complete owner-attested register + coverage % + cadence + export | UC-N-002, F-027, N-010 |
| A6 | **Telemetry / KPI** | Metric published at cadence + drill-down + freshness | UC-N-001, N-003, N-019 |
| A7 | **Governance Process & Register** | Documented process; entries carry owner + expiry; escalation | UC-N-006, N-009, N-011 |
| A8 | **Periodic Assurance Artifact** | Scorecard / evidence-pack at cadence with sign-off | UC-N-004, N-005, N-013 |

Each archetype carries: generic MET / PARTIAL / GAP / N/A definitions (prose templates with
`{slots}`), a set of parametrised diagnostic questions (one per dimension), and an evidence
expectation that drives the confidence rule.

### Worked example — A2 (Population Migration / Coverage), UC-F-003

Parameters: `nhi_population = cloud IAM pipeline credentials; target_pattern = OIDC federation
(sub/aud-scoped); legacy_pattern = static cloud access keys; threshold = 95%; detection_dim =
mis-scoped trust-policy detection`.

- **MET:** target pattern is enforced default for new identities AND ≥threshold% of existing
  population migrated AND legacy inventory with active burn-down AND exceptions registered with
  owner + expiry.
- **PARTIAL:** target pattern available and used for some population; no complete inventory/burn-down;
  exceptions ad hoc.
- **GAP:** target pattern not in use; population on legacy/static credentials; no inventory.
- **N/A:** that identity population does not exist in client scope.
- **Diagnostic questions:** "Is `{target_pattern}` the enforced default for new `{nhi_population}`?" ·
  "What % of existing `{nhi_population}` has migrated off `{legacy_pattern}`?" · "Is there an
  inventory + burn-down for the legacy remainder?" · "Are exceptions registered with owner + expiry?"

Validated against a known-good scenario (AWS-only OIDC, Azure static, no burn-down, no detection):
rubric proposes **PARTIAL / HIGH**, reproducing the existing expert verdict for UC-F-003.

## 4. Data model

New `methodology/` directory:

```
methodology/
  assessment-archetypes.csv   # archetype_id, name, intent, met_def, partial_def, gap_def, na_def, evidence_expectation
  archetype-questions.csv     # archetype_id, q_id, question_template, dimension, informs_state
  uc-archetype-map.csv        # uc_id, archetype_id, params, notes
  bespoke-criteria.csv        # A0 only: uc_id, sub_id, sub_criterion, question, evidence
  RUBRIC.md                   # canonical prose reference for the rules in §5
```

Conventions:
- State definitions are prose templates with `{slot}` placeholders.
- `params` uses the existing `;`-delimited `key=value` convention (matches `nhis_in_scope`).
- A0 UCs appear in `uc-archetype-map.csv` (archetype_id = A0); their criteria live in
  `bespoke-criteria.csv`.
- A UC may map to more than one archetype (multiple rows in `uc-archetype-map.csv`).

Recorded as **ADR-008 — Assessment archetype rubric** in `PRD/adrs/`.

## 5. The rules

### 5.1 State-derivation
Each archetype question informs a **dimension** (coverage / enforcement / exception-handling /
cadence / depth …). The archetype's MET/PARTIAL/GAP definition specifies which dimensions must
hold for each state. The rubric **proposes** a state — it never finalises it.

### 5.2 Confidence rule (replaces pure judgment)
- **HIGH** — direct artifact / demonstrated / lived-experience evidence answers the questions.
- **MEDIUM** — attested but not independently evidenced, or mixed-evidence dimensions.
- **LOW** — inferred from indirect or single weak signal.
- **PENDING** — a *state* (not a confidence): no Task-0 signal gathered for the UC at all.

### 5.3 Override protocol (rubric-assisted + override)
The current-state record gains:
- `proposed_state` — what the rubric proposes from the answers.
- `final_state` — the assessor's recorded verdict.
- `override_reason` — **required** whenever `final_state` differs from `proposed_state`.

`confidence`, `evidence_redacted`, `gap_notes`, `sensitivity_tag` already exist on
`matrix/anz-current-state.csv` and are retained unchanged.

## 6. Validation & acceptance

- **Dogfood re-score (acceptance test):** apply the rubric by hand to all 47 client UCs and record
  `proposed_state` in a new **client-generic** file `methodology/posture-rescore.csv` (columns:
  `uc_id, archetype_id, proposed_state, confidence, override_reason, notes` — no `anz` naming). It
  reads the frozen `matrix/anz-current-state.csv` only as the known-good baseline to compare against,
  and must reproduce that baseline's verdict for the large majority; every divergence is documented
  as either a rubric refinement or a legitimately-better verdict.
- **Coverage checks:** every UC maps to ≥1 archetype (or A0); every archetype is used by ≥1 UC;
  every archetype question informs a state distinction; every `{slot}` in a used template is
  filled by the UC's `params`.

## 7. Scope boundaries

**In scope (WS-1):** the 5 `methodology/` files; ADR-008; the dogfood re-score demonstrating the
rubric reproduces known-good verdicts. Scoring is applied by hand — the goal is to prove the rubric
is well-defined enough to be mechanised later.

**Explicitly deferred:**
- Interactive instrument UI that captures answers and auto-proposes states — WS-3.
- Engine reading the rubric at build time to auto-propose — WS-2/WS-3.
- Maturity-level (ML1/2/3) roll-up view.
- Regulatory-overlay scoping (client picks frameworks) — WS-2.
- Restructuring `task0/questionnaire.md` into a keyed question bank — WS-3 (WS-1 defines only the
  question *templates* inside `archetype-questions.csv`).

## 8. Open items to resolve during build
- Confirm the A0 long-tail set (UC-F-017 TEE attestation, UC-F-026 vault-internal hardening are
  candidates; verify against the full catalog).
- Confirm no UC needs a 9th archetype once all 48 are mapped.
- The dogfood writes to the new client-generic `methodology/posture-rescore.csv`; the frozen
  `matrix/anz-current-state.csv` is not modified in WS-1 (its rename + the `proposed_state`/
  `override_reason` columns landing on the live current-state file happen in WS-5/WS-2).

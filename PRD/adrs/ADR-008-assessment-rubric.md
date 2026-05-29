# ADR-008 — Assessment Archetype Rubric

**Status:** Accepted  
**Date:** 2026-05-29  
**Authors:** Project architect.

## Context

The posture assessment scored each use-case MET / PARTIAL / GAP / PENDING by expert judgment. No
documented per-UC criteria existed: the assessor held the rubric in their head, and each verdict
was defensible only while that assessor was available. For the methodology to be reusable across
any client or industry, the scoring logic must be made explicit and portable — so a second
assessor, a different industry context, or a future client engagement can reproduce verdicts
consistently without re-inventing the criteria from scratch.

ADR-006 locked the MET / PARTIAL / GAP vocabulary and the confidence (HIGH / MEDIUM / LOW) axis.
ADR-007 formalised the sourcing-confidence posture and the evidence-quality distinctions. Neither
ADR specified *per-use-case* criteria — that gap is what this decision closes.

## Decision

Adopt an **archetype library** as the canonical scoring methodology:

- **8 reusable scoring patterns (A1–A8)** — each archetype defines, in parametrised prose
  templates, what MET / PARTIAL / GAP / N/A means for a *kind* of control (preventive guardrail,
  population migration, capability adoption, lifecycle automation, inventory & attestation,
  telemetry/KPI, governance process & register, periodic assurance artifact).
- **A0 Bespoke fallback** — a genuinely unique use-case that resists any of the eight patterns
  maps to A0 and carries its own criteria in `bespoke-criteria.csv`.
- **State-derivation rule** — each archetype question informs a named dimension (coverage /
  enforcement / exception / cadence / depth / governance); the archetype's MET / PARTIAL / GAP
  definition specifies which dimensions must hold. The rubric proposes a state; it does not
  finalise it.
- **Confidence rule** — HIGH = direct artifact / demonstrated / lived-experience evidence; MEDIUM
  = attested but not independently evidenced, or mixed-evidence dimensions; LOW = inferred from
  indirect or single weak signal; PENDING = a state (not a confidence), no signal gathered.
- **Override protocol** — the current-state record carries `proposed_state` (rubric output),
  `final_state` (assessor verdict), and `override_reason` (required whenever they differ).

The archetypes were built **bottom-up** from the existing `acceptance_criteria` columns across all
48 use-cases, ensuring the library is grounded in real control patterns rather than invented
taxonomy. The full prose rules live in `methodology/RUBRIC.md`.

This decision **builds on** ADR-006's MET / PARTIAL / GAP vocabulary and ADR-007's
sourcing-confidence posture. It does not replace them: ADR-006's state definitions are the
vocabulary; ADR-007's evidence-quality distinctions inform the confidence label; this ADR adds the
per-archetype criteria that connect the two.

## Consequences

**Positive:**

- **Cross-client reuse** — a new client's use-cases map onto the existing eight archetypes without
  rewriting scoring criteria. Only `uc-archetype-map.csv` rows and `params` values change.
- **Consistent scoring semantics** — two assessors working independently on the same UC will
  start from the same archetype definition and reach structurally comparable conclusions.
- **Validation-enforced completeness** — `methodology/validate_rubric.py` enforces that every UC
  is mapped, every `{slot}` is filled, and no archetype is left unused. Gaps surface as CI
  failures, not silent omissions.
- **Traceable overrides** — when assessor expertise diverges from the rubric output, the
  `override_reason` field makes the divergence explicit and auditable.

**Negative:**

- **One-time authoring cost** — defining 8 archetypes, their question sets, and the per-UC
  `params` mapping required a non-trivial up-front investment. The payoff accrues across clients.
- **A0 escape hatch** — genuinely unique use-cases still require bespoke criteria, authored
  per-client. If the long-tail grows, the library may need a 9th archetype in a future revision.

**Neutral:**

- **Maturity-level roll-up deferred** — the archetype library produces per-UC MET / PARTIAL / GAP
  verdicts. A derived maturity-level view (ML1 / ML2 / ML3) is out of scope for WS-1 and is not
  blocked by this decision.

## Alternatives considered

**(a) Derive-then-refine per-UC sub-criteria** — author bespoke MET / PARTIAL / GAP criteria for
each of the 48 use-cases independently. Rejected: produces 48 disconnected island-rubrics with no
structural reuse; two assessors comparing verdicts across clients have no common reference point.

**(b) Bespoke prose rubric per UC** — write a free-text rationale per UC describing what each
state means. Rejected: creates a second source of truth competing with the existing
`acceptance_criteria` column; any change to the control's intent must be updated in two places;
no machine-checkable completeness.

## References

- [`methodology/RUBRIC.md`](../../methodology/RUBRIC.md) — canonical prose reference for the
  state-derivation, confidence, and override rules.
- [`docs/superpowers/specs/2026-05-29-assessment-rubric-design.md`](../../docs/superpowers/specs/2026-05-29-assessment-rubric-design.md)
  — the approved design spec (brainstorming + grill complete) that this ADR records.
- Companion ADRs: [ADR-006](./ADR-006-scoring-rubric.md) (scoring vocabulary),
  [ADR-007](./ADR-007-reading-model-and-confidence.md) (sourcing-confidence posture).

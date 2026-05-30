# Assessment Rubric — Archetype Library Reference

**Status:** Accepted  
**Date:** 2026-05-29  
**Applies to:** WS-1 methodology files in `methodology/`  
**Builds on:** ADR-006 (scoring vocabulary), ADR-007 (sourcing-confidence posture)

---

## 1. The Archetype Model

An **archetype** is a reusable scoring pattern that captures what MET / PARTIAL / GAP means for a *kind* of control — independently of which specific credential type, population, or system is in scope.

Every use-case in the catalog maps to **one (occasionally two) archetypes** from the library (A1–A8). A genuinely unique use-case that does not fit any reusable pattern maps to **A0 (Bespoke)** and carries its own per-UC criteria in `bespoke-criteria.csv` instead of inheriting a template.

Archetypes are **parametrised per use-case** via the `params` column in `uc-archetype-map.csv`. Each archetype's state definitions and question templates contain `{slot}` placeholders; the UC's `params` entry supplies the concrete values (e.g. `nhi_population=cloud IAM pipeline credentials; threshold=95%`). The rubric therefore remains generic at the library level and concrete at the use-case level — without duplicating prose.

The `uc-archetype-map.csv` is the single join point between the use-case catalog and the archetype library. A UC may appear in more than one row if it genuinely spans two patterns (e.g. coverage *and* lifecycle automation).

---

## 2. The Nine Archetypes (A0–A8)

| ID | Name | Intent |
|----|------|--------|
| A0 | Bespoke | Long-tail use-case that does not fit a reusable pattern; criteria authored per-UC in `bespoke-criteria.csv`. |
| A1 | Preventive Guardrail | A control enforced at a gate that blocks a bad action for the target population. |
| A2 | Population Migration / Coverage | Share of an identity population moved from a legacy pattern to a target pattern. |
| A3 | Capability Adoption | A capability is deployed *and* adopted to depth for a target population at a configuration threshold. |
| A4 | Lifecycle Automation | Issuance, rotation, and revocation of a credential type automated within an SLA for a target population. |
| A5 | Inventory & Attestation | A complete owner-attested register of a population re-attested every cadence and exported to a target system. |
| A6 | Telemetry / KPI | A metric published every cadence with drill-down by dimension and freshness within a bound. |
| A7 | Governance Process & Register | A documented process whose entries carry owner+expiry and auto-escalate. |
| A8 | Periodic Assurance Artifact | An artifact assembled every cadence with sign-off covering a defined scope. |

### State definitions per archetype (summarised)

**A1 — Preventive Guardrail**

| State | Definition |
|-------|-----------|
| MET | Control enforced in blocking mode across the full scope; bypasses require a registered exception with owner+expiry; violations alerted. |
| PARTIAL | Control deployed in detect/monitor mode or over partial scope; enforcement not blocking everywhere; exceptions ad hoc. |
| GAP | Control not deployed or trivially bypassed; no meaningful coverage. |
| N/A | Control or population not applicable to client scope. |

**A2 — Population Migration / Coverage**

| State | Definition |
|-------|-----------|
| MET | Target pattern is the enforced default for new identities AND >= threshold of existing population migrated AND legacy inventory with active burn-down AND exceptions registered with owner+expiry. |
| PARTIAL | Target pattern available and used for some population; no complete inventory or burn-down; exceptions ad hoc. |
| GAP | Target pattern not in use; population remains on legacy credentials; no inventory. |
| N/A | Population does not exist in client scope. |

**A3 — Capability Adoption**

| State | Definition |
|-------|-----------|
| MET | Capability in production AND adopted by >= threshold of target population AND configuration meets the config target. |
| PARTIAL | Capability available but adoption is low (shelf-ware) OR configuration below threshold. |
| GAP | Capability not available or not used for the population. |
| N/A | Capability or population not applicable to client scope. |

**A4 — Lifecycle Automation**

| State | Definition |
|-------|-----------|
| MET | Full lifecycle (issue + rotate + revoke) automated for the population within SLA; failures alerted on-call. |
| PARTIAL | Some lifecycle phases automated (e.g. rotation but not revocation) or partial population coverage; manual steps remain. |
| GAP | Lifecycle is manual or managed out-of-band for the credential type. |
| N/A | Credential type or population not applicable to client scope. |

**A5 — Inventory & Attestation**

| State | Definition |
|-------|-----------|
| MET | Register covers >= threshold of population; entries owner-attested; re-attested every cadence; exported to the target system. |
| PARTIAL | Partial inventory; attestation ad hoc or stale; no export to target system. |
| GAP | No inventory of the population exists. |
| N/A | Population not applicable to client scope. |

**A6 — Telemetry / KPI**

| State | Definition |
|-------|-----------|
| MET | Metric published every cadence; drill-down by dimension; freshness within bound; reviewed at the designated forum. |
| PARTIAL | Metric exists but cadence is irregular, lacks drill-down, or is stale beyond the freshness bound. |
| GAP | Metric is not produced. |
| N/A | Metric not applicable to client scope. |

**A7 — Governance Process & Register**

| State | Definition |
|-------|-----------|
| MET | Process documented and operating; every entry has owner+expiry; expired entries auto-escalate; reviewed every cadence. |
| PARTIAL | Process exists but entries lack owner/expiry or escalation is manual. |
| GAP | No process or register exists. |
| N/A | Process not applicable to client scope. |

**A8 — Periodic Assurance Artifact**

| State | Definition |
|-------|-----------|
| MET | Artifact assembled every cadence; signed and timestamped; covers defined scope; generated within SLA. |
| PARTIAL | Artifact produced ad hoc or with incomplete scope; no formal sign-off. |
| GAP | Artifact is not produced. |
| N/A | Artifact not applicable to client scope. |

---

## 3. State-Derivation Rule

Each archetype question targets a **dimension** of the control:

| Dimension | What it measures |
|-----------|-----------------|
| `coverage` | What fraction of the relevant population or scope the control reaches. |
| `enforcement` | Whether the control blocks bad outcomes or only detects/monitors them. |
| `exception` | Whether out-of-policy cases are registered, owned, and time-bounded. |
| `cadence` | Whether periodic activities (attestation, reporting, sign-off) occur on schedule. |
| `depth` | Whether adoption goes beyond deployment to meaningful use at the right configuration. |
| `governance` | Whether ownership, expiry, and escalation paths are documented and functioning. |

The archetype's MET / PARTIAL / GAP prose definition specifies *which combination of dimensions must hold* for each state. Concretely:

- **MET** requires all load-bearing dimensions to be satisfied.
- **PARTIAL** means one or more dimensions are present but incomplete (e.g. coverage exists but enforcement is monitoring-only, or cadence is irregular).
- **GAP** means the primary dimension is absent or trivially unmet.

The rubric **proposes** a state based on the answers gathered. It never finalises the record — the assessor confirms or overrides (see §5).

---

## 4. Confidence Rule

Confidence is an independent axis from state. It reflects the quality of evidence behind the proposed state, not the state itself.

| Confidence | Meaning |
|------------|---------|
| HIGH | Direct artifact, demonstrated capability, or lived-experience evidence answers all key dimension questions. |
| MEDIUM | Evidence is attested but not independently verified, or some dimensions have strong evidence while others are inferred. |
| LOW | State is inferred from indirect signals or a single weak data point. |
| PENDING | **A state, not a confidence level.** No signal has been gathered for this use-case at all. Surfaces as an open question, not a scored row. |

`PENDING` rows are not given a confidence label — the field is left blank until signal is collected.

---

## 5. Override Protocol

The current-state record carries three fields governing the rubric's interaction with assessor judgment:

| Field | Purpose |
|-------|---------|
| `proposed_state` | The state the rubric proposes, derived mechanically from the archetype definition and the answers to its diagnostic questions. |
| `final_state` | The assessor's recorded verdict. May match or differ from `proposed_state`. |
| `rationale` | **Required whenever `final_state` differs from `proposed_state`.** Must cite the dimension(s) where the rubric's answer differed from the assessor's read and why. |

The intent: the rubric is a forcing function for explicit documentation, not an authority that overrides domain expertise. An assessor who knows more than the rubric should record that knowledge as an override rather than silently diverging.

Existing fields `confidence`, `evidence_redacted`, `gap_notes`, and `sensitivity_tag` are retained unchanged from the frozen v0.1 current-state baseline (renamed to a client-generic name in WS-5).

---

## 6. How to Add a New Client, Industry, or Regulatory Framework

The archetype library (A0–A8) and the question templates in `archetype-questions.csv` are **client-agnostic and reusable without modification**. Onboarding a new client or overlaying a new regulatory framework requires only:

1. **Define the in-scope use-case set** — draw from the catalog or extend it.
2. **Map each UC to an archetype** — add rows to `uc-archetype-map.csv` with the client-specific `params` values.
3. **Author bespoke criteria** for any UCs that land on A0 (add rows to `bespoke-criteria.csv`).
4. **Run the validator** — `python3 methodology/validate_rubric.py` — to confirm every UC is mapped, every slot is filled, and no forbidden tokens are present.

No archetype definitions change. No question templates change. The scoring semantics (MET / PARTIAL / GAP / PENDING, HIGH / MEDIUM / LOW confidence, override protocol) carry over verbatim. This is the reusability payoff of the bottom-up archetype design.

---

## 7. Cross-Reference

See `PRD/adrs/ADR-008-assessment-rubric.md` for the architectural decision record that adopted this archetype library, its rationale, and the alternatives considered.

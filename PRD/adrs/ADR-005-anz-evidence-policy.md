# ADR-005 — XYZ evidence policy (sensitivity)

**Status:** Accepted
**Date:** 2026-05-20 (re-confirmed 2026-05-23 with the M2 reviewer audit
in [`meta/review-M2-2026-05-23.md`](../../meta/review-M2-2026-05-23.md) §C)
**Authors:** Project architect.

## Context

Task 0 elicited a mix of **publicly attestable signals** (vendor
selections, regulator citations) and **internal lived-experience
signals** (operational adoption, internal incidents, licensing
observations). The PRD must be defensible if shared with: (a) XYZ
internal review; (b) an external auditor; (c) — potentially — vendor
SEs in an RFI context. The same artifact may surface to all three
audiences, so a clear sensitivity policy is required up front.

There is also a known risk pattern from
[`meta/review-M2-2026-05-23.md`](../../meta/review-M2-2026-05-23.md) §C:
**vendor profiles drift into direct XYZ attribution** because the
researcher saw the lived-experience evidence. The policy below is the
authoritative guard against that drift.

## Decision

Adopt the **four-tier sensitivity tagging policy** below, applied to
every input artifact and enforced in every output artifact (PRD body,
appendices, ADRs, vendor profiles, regulatory mappings, matrices).

| Tag | Meaning | Reproduction rule |
|---|---|---|
| `[PUBLIC]` | Information independently published (vendor docs, regulator publications, breach post-mortems, peer-reviewed research). | Cite freely with primary URL. |
| `[INTERNAL]` | Lived-experience signal from Task 0 about XYZ that is not separately public. | **Paraphrase. Attribute to "a major AU Tier-1 FI"**, not XYZ by name. Quote ≤ 30 words. |
| `[SENSITIVE]` | XYZ internal detail that, if reproduced, would create concrete operational exposure. | **Do not reproduce verbatim.** Summarise at the category level only if absolutely required for the narrative; otherwise omit. |
| `[NOT-FOR-DISTRIBUTION]` | XYZ incident details, regulator interactions, or material withheld by the stakeholder during Task 0. | **Do not reproduce in any output artifact.** Reference by tag only. |

Additionally:

- Every claim about a vendor must cite a primary URL **or** carry a
  canonical tag from `prompts/README.md` invariant #2
  (`[INDUSTRY-CONSENSUS]`, `[SPECULATION]`, `[USER-SUPPLIED]`,
  `[BREACH-POST-MORTEM]`).
- The non-canonical tag `[USER-CONFIRMED EXPERIENCE]` (found in
  hashicorp-vault-enterprise.md at M2 review) **must be normalised to
  `[USER-SUPPLIED]`** before PRD body assembly.
- Default attribution for `[INTERNAL]` XYZ content is exactly
  **"a major AU Tier-1 FI"**, used in PRD §3, §10, §12, §15, §16.

## Consequences

**Positive:**

- The PRD is shareable to auditor / vendor SE without re-redaction.
- Reviewers have a single bright-line test (is the source `[INTERNAL]`
  or stronger? then paraphrase / omit).
- The two profile leakages flagged at M2 (Fortanix DSM XYZ migration
  attribution; Vault Enterprise `[USER-CONFIRMED EXPERIENCE]` rows) have
  a deterministic fix.

**Negative:**

- Some narrative punch is lost where direct attribution would be
  rhetorically stronger. Accepted as the cost of shareability.
- Reviewers must spot-check tagging at every milestone; PRD review
  prompt 09 includes a §C "Sensitivity audit" gate.

**Neutral:**

- Distribution-surface decisions (vendor SE? regulator?) are deferred to
  PRD §17 open question O2; until decided, classification defaults to
  "Internal — for XYZ stakeholder review".

## Alternatives considered

- **No tagging; redact at publish time** — rejected; redaction at
  publish time produces inconsistent artifacts and is hard to audit.
- **Tag everything `[SENSITIVE]` by default** — rejected; over-redaction
  would gut PRD §12 and §16 evidentiary weight.
- **Allow `[INTERNAL]` with named XYZ attribution** — rejected;
  inconsistent with the stakeholder distribution-surface uncertainty.

## References

- [`prompts/README.md`](../../prompts/README.md) invariant #7 (sensitivity
  enforcement) + invariant #2 (citations).
- [`research/anz-current-state-evidence.md`](../../research/anz-current-state-evidence.md)
  §6 (Sensitivity audit summary).
- [`meta/review-M2-2026-05-23.md`](../../meta/review-M2-2026-05-23.md) §C
  (M2 sensitivity audit; two profile leakages identified for
  paraphrasing).
- Companion ADRs: [ADR-001](./ADR-001-format-choice.md) (format trace),
  [ADR-004](./ADR-004-vendor-shortlist.md) (vendor shortlist scoring).

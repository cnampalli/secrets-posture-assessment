# Critical Action Plan — IAM-Specialist Review × A+ Hardening Alignment

> **Status: APPROVED 2026-06-11.** Addendum to `docs/superpowers/plans/2026-06-11-a-plus-hardening.md`.
> Source inputs: `meta/iam-specialist-review-2026-06-11.md` (verdict *"invest"*) and the approved A+
> hardening plan. This document does **not** rewrite the A+ plan — it **closes coverage gaps** the
> A+ plan softened or dropped, and **re-sequences** the two highest-urgency items. The A+ plan stays
> immutable; this addendum is the execution driver.

## Why this addendum exists

The A+ hardening plan was authored from the cold-start audit (grade B) **and** the IAM-specialist
review. Cross-referencing every specialist action item against the A+ plan shows: most items map
cleanly, but **two high-urgency items were softened** and **four asks were dropped entirely**. Two of
those — data-currency enforcement and anonymisation — are the specialist's *existential risk* and a
*pre-external-release blocker*, yet the A+ plan schedules them 4th and last respectively. This plan
corrects coverage and sequencing.

## Locked decisions (grill-me, 2026-06-11)

1. **Form** — standalone addendum, cross-linked from A+ (A+ unchanged).
2. **Data-currency** — re-hardened to a **CI build-gate**, overriding A+ H4's checklist softening; the
   per-engagement checklist is retained as a human backstop.
3. **Scope** — **all four** dropped specialist items promoted in-scope, including the "non-fatal"
   Platform/integration NFRs. Nothing deferred silently.
4. **Sequencing** — release-blockers (anonymisation + currency gate) **front-loaded to Wave 0**, ahead
   of the H1→H2→H3 engineering chain.
5. **Scoring** — **capture the number + keep the hard-gate for the binding verdict**; the captured %
   drives a separate trend view. Defensibility preserved, movement-between-assessments gained.

---

## Coverage matrix (the alignment assessment)

### Cleanly covered ✅
| Specialist item | A+ item |
|---|---|
| Vendor-ownership fabrication (Entro / PANW→CyberArk) | Fixed on WS4 + **H4** ownership graph first-class |
| No maturity roll-up | **M1** exec roll-up |
| No peer benchmark | **M1** benchmark layer |
| Cross-domain identity registry (specialist's #1 structural ask) | **M2** identity spine |
| Evidence capture not enforced | **M4** |
| PAM agentic + IGA agent-lifecycle (core) | **M3** |
| Calibration / inter-rater reliability | **M4** calibration workbook |
| Anonymisation leakage | **H6** + **M4** — *but mis-sequenced (see Wave 0)* |
| CPS 230 overlay | **M4** |

### Softened / partial ⚠️ → corrected here
| Specialist ask | A+ treatment | Correction |
|---|---|---|
| Data-currency **build-failing** gate (the "existential risk") | H4 → per-engagement checklist | **A1** — CI build-gate, max-age per provenance tier |
| Quantitative **%-capture**; hard-gating compresses signal (20%→80% scores identically) | M4 enforces evidence, not the number | **A2** — capture number + trend view; verdict gate unchanged |
| IGA SaaS-to-SaaS OAuth-grant cert + machine-ID-cert campaign type | M3 generic agentic only | **A4** — named explicitly in M3 IGA scope |
| Rapid-scan tier (~25Q wedge) vs plan's tier names | tier taxonomies diverge | **A6** — reconcile tiers in M4 |

### Dropped entirely ❌ → all promoted
| Specialist ask | Promotion |
|---|---|
| Britive evidence re-anchor ("do it, don't ship the caveat") | **A3** — Wave 0, pre-client blocker |
| PAM ITDR adjacency (CrowdStrike/Microsoft/Silverfort, "like CIEM got") | **A4** — into M3 PAM slice |
| IGA OAuth-grant + machine-ID campaign type | **A4** — into M3 IGA slice |
| Platform/integration NFRs (vault RTO/RPO, ServiceNow/CMDB, operating model, CPS 230 exit/portability, risk-appetite params, migration sequencing) | **A5** — new requirement-modeling task |
| OWASP NHI Top 10 mapping + NIS2 overlay | **A7** — into M3 NHI extension / M4 overlays |

### Sequencing tension → corrected
- Anonymisation = specialist **pre-external-release blocker**, A+ scheduled it **last (H6)**.
- Data-currency = specialist **existential risk**, A+ scheduled it **4th (H4)**.
- **Both move to Wave 0**, ahead of the H-chain.

---

## Execution waves

### Wave 0 — Release blockers (before the H-chain)

**A1 — Data-currency CI build-gate.**
Add a max-age assertion per provenance tier to `matrix/validate_data.py`, reading thresholds from
`matrix/config/data-provenance.yaml`. The build **fails** when any HIGH-impact fact exceeds its
tier's age threshold. Retain the per-engagement currency checklist (A+ H4) as the human backstop.
Wires into the H3 CI pipeline once it exists. *Rationale: specialist found two ownership errors in
one config in one afternoon; M&A decays facts on a ~monthly cycle — credibility rests on currency.*

**A3 — Britive evidence re-anchor.**
Replace marketing-tier Britive citations in the PAM evidence catalog with primary-source quotes;
enforce via the existing `check_vendor_fit` / evidence-quote logic in `validate_data.py`.
*Rationale: repo already flags Britive marketing-tier — fix it, don't ship the caveat to a client.*

**Anonymisation (H6 subset, pulled forward).**
Rename `research/anz-current-state-evidence.md` and `PRD/adrs/ADR-005-anz-evidence-policy.md`;
genericize the report banner aperture; scrub client identity from `task0/responses.md`. Closes the
"real client name in filenames vs zip-the-repo sharing instruction" exposure before any external
distribution.

### Engineering chain (A+ as-is)
- **H1 → H2 → H3** unchanged (provenance-as-code → semantic control registry → CI). A1's gate lands
  inside H3's pipeline.
- **H4** retained but **reduced** — its currency element becomes A1; H4 keeps ownership-edge
  `confidence`/`as_of` surfacing + MEDIUM-confidence exclusion from concentration math.
- **H5, H6 (remainder)** unchanged.

### Market chain (A+ M-items + promotions)
- **M1** exec roll-up + benchmark — unchanged.
- **M2** identity spine — unchanged (specialist's #1 ask; already well-mapped).
- **A2 — Scoring trend (pairs with M4).** In `app/src/assessment/scoring.ts`: capture the
  quantitative answer's actual percentage; the rubric applies the threshold; the **binding MET/GAP
  verdict keeps the hard-gate** (defensibility preserved); the captured number feeds a separate
  trend/progress view keyed to M4's per-row `as_of`.
- **M3 + A4 — Agentic slice, expanded.** PAM (agent privileged-session brokering + JIT **+ ITDR
  adjacency** treatment); IGA (agent lifecycle **+ SaaS-to-SaaS OAuth-grant certification +
  machine-identity-certification as a first-class campaign type**); Secrets (agent credential
  issuance/rotation). NHI taxonomy extension **+ A7** explicit OWASP NHI Top 10 mapping. Each with
  regulatory trace and evidence at the WS2/WS3 verification bar.
- **A5 — Platform/integration NFR catalog (new).** Requirement-modeling UCs: vault availability /
  RTO / RPO, latency budgets, DR & break-glass *of the vault*, ServiceNow/CMDB + SIEM + HR-feed
  integration constraints, operating model (platform vs managed service), commercials & exit /
  portability (CPS 230 material-service-provider), risk-appetite parametrisation, migration-sequencing
  constraints. Framing stays at *"requirements-shaped findings catalog,"* not *"your requirement set."*
- **M4 + A6 — Productisation.** Per-row `as_of`, evidence enforcement, calibration workbook,
  **tier taxonomy reconciled** to the specialist's rapid-scan / full / posture-retainer, CPS 230
  **+ A7 NIS2** overlay presets.

---

## Files

**Modify:**
| File | Change |
|---|---|
| `matrix/validate_data.py` | A1 max-age gate; A3 Britive evidence enforcement (reuse gate helpers) |
| `matrix/config/data-provenance.yaml` | per-tier age thresholds |
| `app/src/assessment/scoring.ts` | A2 number capture + trend (verdict gate untouched) |
| `research/anz-current-state-evidence.md`, `PRD/adrs/ADR-005-anz-evidence-policy.md` | anonymisation rename |
| `docs/superpowers/plans/2026-06-11-a-plus-hardening.md` | cross-link pointer (done) |

**Reuse (don't reinvent):** `validate_data.py` gate helpers (`check_vendor_fit`, the H1 citation-key
resolver), the `data-provenance.yaml` tier scaffolding (exists — operationalise), the H3 CI pipeline
as the host for A1's gate.

---

## Verification

1. **Alignment complete** — every action item in `meta/iam-specialist-review-2026-06-11.md` appears in
   the coverage matrix as covered / corrected / promoted; zero unaccounted items.
2. **A1 gate works** — backdate a HIGH-impact fact's `as_of` in `data-provenance.yaml` →
   `python matrix/validate_data.py` fails with a currency error; restore → passes.
3. **A2 preserves defensibility** — scoring parity vectors stay green; 20% vs 80% on a quantitative
   answer yields the **same MET/GAP verdict** but a **different trend value**.
4. **Anonymisation closed** — `grep -ri "<real-client-name>" research/ PRD/ task0/` returns nothing;
   renamed files resolve in all references.
5. **Sequence consistent** — Wave 0 → H-chain → M-chain has no broken dependencies; A+ plan carries
   the cross-link.

---

## Execution model

Isolated worktree per wave; agent-driven TDD; adversarial citation verification for all new external
claims (A3 / A4 / A5 / A7); code-review + grill-me gates. Wave 0 ships first as the release-blocker PR;
the H-chain and M-chain follow. Checkpoint at ~70% context per the standing handoff rule.

## A+ re-audit success bar (unchanged)
1. Cold-start audit re-run → ≥A on all seven dimensions, zero CRITICAL/HIGH, refuted-claim count 0.
2. IAM-specialist review re-run → benchmarks / roll-up / identity-spine / agentic move from "gap" to
   "differentiator"; stakeholder matrix shows CEO/CIO consumable outputs.
3. All gates in CI; provenance machine-checked end-to-end; ownership graph dated + confidence-surfaced;
   **currency build-gate green (A1)**.

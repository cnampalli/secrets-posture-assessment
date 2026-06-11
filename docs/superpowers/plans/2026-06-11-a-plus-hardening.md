# A+ Hardening Plan — from "B / top-decile instrument" to "A+ / best available in the market"

> **⮕ Execution driver:** see `docs/superpowers/plans/2026-06-11-critical-action-plan.md` — the
> gap-closure + re-sequencing addendum that corrects two softened items (currency gate, scoring trend),
> promotes four dropped specialist asks (A3–A5, A7), and front-loads release-blockers as Wave 0.

> **Status: APPROVED 2026-06-11, not started.** Source inputs: the independent cold-start audit
> (`meta/independent-audit-2026-06-11.md`, verdict **B**) and the independent IAM-specialist review
> (`meta/iam-specialist-review-2026-06-11.md`, "top-decile instrument, held back by missing
> benchmarks/roll-up"). The audit's CRITICAL/HIGH/quote-drift findings are already FIXED on the WS4
> branch (Entro removal, PANW→CyberArk, IGA §22→§21 merge, 26 E8 rows re-verified, metadata sweep).
> This plan covers everything else needed to re-audit at **≥A on every dimension** AND to clear the
> specialist's market-leadership bar.

## Why two tracks
The audit grades engineering truth (gates, tests, provenance). The specialist grades market value
(who buys it, what's differentiated). A+ = both. Phases H1–H6 close the audit; M1–M4 close the market
gap. Sequence: H1→H2→H3 first (they make every later phase machine-verified), then interleave.

---

## Track H — engineering hardening (audit dimensions → A)

### H1 — Provenance as code (data integrity B- → A)
- `check_citation_keys_resolve()` gate in `matrix/validate_data.py`: every `citation_keys` token must
  resolve to `meta/citations.bib` (allowlist sentinel tags); backfill the ~150 dangling keys from the
  WS3 ledgers (`docs/superpowers/plans/ws3-research/*.md`) — mostly mechanical.
- Backfill `evidence_quote` for `matrix/domains/iga/iga-vendor-fit.csv` (quotes exist in the ledgers);
  extend `check_vendor_fit` to require it.
- Add a `quote_type` column/flag (verbatim | paraphrase | analyst-note) so entries like
  `E8-RAP-NHI-GAP` (an analyst gap-note in a quote field) are honestly labelled — gate verbatim rows.
- Link-rot + quote-presence checker (HTTP 200 + contiguous-substring) runnable on the
  `data-provenance.yaml` refresh cadence; report drift, never auto-rewrite.

### H2 — Semantic control registry (claim truthfulness B → A)
- Per-control `expect_substring` (or topic) assertions in `matrix/config/control-id-registry.yaml`;
  F3 gate checks `control_short_title`/`evidence_quote` against them. Makes the right-ID-wrong-text
  class (the audit's HIGH-2, caught only by a human re-read) mechanically impossible.
- Seed from the already-verified strata (47 ISM, 25 CPS 234, E8, MITRE) — the texts were fetched
  during WS1/WS2 and the 2026-06-11 fixes; this is transcription, not research.

### H3 — CI (test adequacy B+ → A)
- GitHub Actions (~20 lines): `pytest -q` · `validate_data` ×3 · scoring parity vectors ·
  `app` vitest + build · rebuild-and-diff byte-identity for all four HTML reports.
  Everything is already green and deterministic, so the pipeline is green from day one; the point is
  that HANDOFF's "Gates:" lines stop being self-reported.

### H4 — Ownership graph first-class (truthfulness, CPS 230 feature)
- Per-edge primary-source URL mandatory; per-edge `confidence` + `as_of` SURFACED in the rendered
  concentration views; MEDIUM-confidence collapses excluded from concentration math (rendered as
  "unverified") — the rule that would have stopped the Entro error from reaching a reader.
- Freshness SLA: ownership re-verification is a per-engagement checklist item (M&A was the
  fastest-drifting data in both independent reviews — a 4-month-old $25B event was missed).

### H5 — Report SPA behavioral tests (deliverable quality A- → A+)
- Extract the inline template JS into a module bundled at render time; jsdom/vitest tests (infra in
  `app/` already) for: posture-count math, gap-link navigation targets, compliance-cascade filtering,
  MET-override persistence. Byte-snapshots keep proving determinism; these prove behavior.

### H6 — Symmetry & polish
- One canonical optional-but-uniform per-domain file set (evidence catalog + archetype map + fit grid
  declared in the descriptor) so domain #4 is a data exercise.
- README rewritten as the three-domain product front door (HANDOFF stays the resume doc).
- `derive_state([])` → raise (+ JS parity vector); aggregate-vs-per-vendor consistency gate;
- Anonymisation: rename `research/anz-current-state-evidence.md` + `PRD/adrs/ADR-005-anz-evidence-policy.md`
  (filename leak vs the "zip the repo" sharing instruction) and genericise the report banner aperture.

---

## Track M — market leadership (specialist findings → "best available")

### M1 — Exec roll-up + benchmark layer (unblocks CEO/CIO/CTO personas)
- One-page cross-domain maturity roll-up (board-grade: 3 domains × ML band × top-3 risks × trend) as
  a first-class output, not a tab.
- Benchmark mechanism: anonymised cohort percentiles ("you vs AU-FI peers") — start with a
  designed-honest synthetic/published-data baseline clearly labelled, evolve to real cohort as
  engagements accumulate. The specialist names benchmarking as THE gap vs Gartner/KC/Big-4.
- Backlog export: GAP/PARTIAL → Jira/ADO-importable CSV (Product Owner persona's missing hook).

### M2 — Cross-domain identity spine (the specialist's #1 structural ask)
- Single identity taxonomy (human | NPE | agentic-AI × privileged flag) keyed once, with per-domain
  lenses — today the same service account exists three times (secrets IGID/PAM PID/IGA IGID) with no
  linkage. This is also the technical foundation of the IAM → NHI → Agentic-AI story.

### M3 — Agentic-AI from aspiration to instrument (~5% of artifact mass today)
- Agentic identity UCs in all three domains (agent credential issuance/rotation in secrets; agent
  privileged-session brokering + JIT in PAM; agent lifecycle/ownership/certification in IGA), each
  with regulatory trace (OWASP LLM, ISM PQC/MFA where applicable) and evidence items — same
  verification bar as WS2/WS3.
- Extend the NHI taxonomy (already CSA/SPIFFE-anchored, the repo's most valuable asset per the
  specialist) with the agentic sub-tree and quarterly currency review.

### M4 — Engagement productisation (Phase 5, re-scoped by the reviews)
- Client workspace + current-state import + re-baselining (per-row `as_of` capture — closes the
  audit's freshness gap and enables the benchmark layer).
- Calibration workbook + evidence-capture enforcement in the questionnaire (specialist Q7: questions
  are accurate but quantitative answers flatten to yes/no and evidence is optional).
- Packaging: 3-tier offer (self-serve questionnaire / facilitated assessment / full vendor-selection
  engagement) + CPS 230 / DORA overlay presets.

---

## Acceptance (the A+ bar)
1. Re-run the independent cold-start audit (same protocol): **≥A on all seven dimensions**, zero
   CRITICAL/HIGH, refuted-claim count 0.
2. Re-run the independent IAM-specialist review: benchmarks/roll-up/identity-spine/agentic items move
   from "gap" to "differentiator"; stakeholder matrix shows CEO/CIO consumable outputs.
3. All gates in CI; provenance machine-checked end-to-end; ownership graph dated + confidence-surfaced.

## Sequencing & effort (rough)
H1+H2 (~3 days) → H3 (½ day) → H4 (1 day) → M1 (2-4 days) → M2 (3-5 days, schema work) →
H5 (2-4 days) → M3 (research-heavy, WS3-style verification fleet) → H6 + M4 (ongoing/productisation).
Per project rhythm: isolated worktree per phase, agent-driven TDD, code-review + instrument-review +
grill-me gates, adversarial citation verification for all new external claims.

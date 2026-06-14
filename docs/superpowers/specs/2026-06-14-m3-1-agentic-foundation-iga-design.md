# M3.1 — Agentic foundation + IGA pilot (design)

**Date:** 2026-06-14
**Track:** M (market leadership) — M3 sub-project 1 of 3, per `docs/superpowers/plans/2026-06-11-a-plus-hardening.md` (M3) + the critical-action-plan A4 fold-in.
**Status:** approved, ready for implementation plan
**Mock:** `docs/superpowers/sketches/2026-06-14-m3-agentic-iga-mock.html`

## Purpose

M3 turns agentic-AI from aspiration (~5% of artifact mass, per the IAM-specialist review) into a
first-class instrument. M3 is too large for one spec, so it is decomposed into three sub-projects;
**this is M3.1**, the foundation plus a single validated pilot domain. It delivers (a) the shared
agentic substrate every later slice depends on — a verified external-source research base and an
agentic sub-tree extending the NHI taxonomy — and (b) IGA taken end-to-end with three agentic
governance use cases, at the WS2/WS3 verification bar. Secrets and PAM generalize in M3.2/M3.3.

## Decomposition (M3 → 3 sub-projects)

| Sub-project | Scope |
|---|---|
| **M3.1 (this spec)** | Agentic foundation (sub-tree taxonomy + verified research base) + **IGA pilot**: 3 agentic governance UCs end-to-end. |
| M3.2 | Generalize to **secrets**: agent credential issuance/rotation UCs + identities, reusing the foundation. |
| M3.3 | Generalize to **PAM**: agent privileged-session brokering + JIT + ITDR adjacency (A4) UCs + identities (closes the PAM agentic-identity gap). |

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Decomposition | **Foundation + pilot domain first**, then generalize | Matches the project's proven spike-then-generalize rhythm (PAM spike → generalize). |
| Pilot domain | **IGA** | Most agentic-ready: existing `IGID-012` (agentic agent) + `IGID-013` (OAuth consent-grant) + `owasp-llm` already in its reg-trace; richest agentic-governance standards coverage. |
| Foundation breadth | **Taxonomy + research + IGA only** | No orphan identities; secrets/PAM agentic identities are authored with their own UCs in M3.2/M3.3. |
| IGA UC count | **3 focused UCs** | High-signal, proves the pattern without over-investing pre-generalization. |
| Verification bar | **WS3-style adversarial** | Re-fetch every source, REFUTE posture, verbatim-only quotes, citation keys resolve through the H1 gate. Matches the M3 acceptance + the repo's anti-fabrication history. |
| Identities | **Govern existing `IGID-012`/`IGID-013`; no new identity rows** | The pilot governs agents that already exist in the catalog. |
| Report area | **New "Agentic governance" area** | The specialist frames agentic as its own emerging governance area; cleaner than scattering across JML/Certification. |
| Sub-tree home | **Research/taxonomy artifact mapping to existing spine `SPN-015`** | No new spine rows; the agentic archetype already exists from M2. |

## Architecture

Adds **data + research artifacts** to the existing IGA domain and one small **report-logic** seam,
reusing the WS2/WS3 data-authoring pipeline end-to-end. No new engine modules.

### 1. Foundation — research base + agentic sub-tree

- **`research/agentic/AGENTIC-RESEARCH.md`** — WS3-verified external-source base: OWASP LLM Top 10
  2025 (esp. **LLM06 Excessive Agency**), CSA agentic-AI guidance, NIST AI RMF / SP 800-53 AC family
  as applied to agents. Each source re-fetched, REFUTE posture, verbatim quotes only, with a
  per-source verification ledger (mirrors `research/iga/RESEARCH-SUMMARY.md`). Honesty caveats
  recorded inline (mirror status, withheld quotes, etc.).
- **Agentic sub-tree** — a structured section (in the research artifact and/or
  `research/identity-taxonomy.md`) defining agentic sub-classes — autonomous task agent, tool-using
  (function-calling) agent, agent-delegated NPE (OBO / consent-grant), human-gated agent (HITL on
  irreversible actions), multi-agent orchestrator — each anchored to CSA/OWASP/NIST and **mapped to
  the existing spine `SPN-015`**. No change to `identity-spine.yaml`.

### 2. IGA pilot — 3 agentic governance UCs

Append to `matrix/domains/iga/use-cases.csv`:
- **UC-I-017 — Agent registration & ownership** (P0): every autonomous agent is a governed object
  with a named human owner, declared purpose and scoped tool entitlements before acting.
- **UC-I-018 — Agent entitlement certification / continuous attestation** (P0): agent tool-scopes are
  recertified; dynamic permission change defeats point-in-time recert, so continuous attestation is
  the modelled good end-state.
- **UC-I-019 — Agent deprovisioning / orphan-agent detection** (P1): decommissioned/owner-less agents
  and their standing consent grants are detected and revoked (the agentic analogue of dormant/orphan).

Each carries `story`, `acceptance_criteria`, `nhis_in_scope` (IGID-012/013), `outcome_lens`,
`backmap_codes`, `priority_fi`, `citation_keys`. Plus illustrative rows in
`matrix/domains/iga/current-state.csv` (states as in the mock: 017 GAP, 018 PARTIAL, 019 GAP).

### 3. Regulatory trace (WS3-verified)

Append rows to `matrix/domains/iga/regulatory-trace.csv` mapping the 3 UCs to OWASP LLM (LLM06 and
any other applicable items), NIST 800-53 AC-2/AC-6, ASD ISM (where applicable), APRA CPS 234. Every
new control:
- registered in `matrix/config/control-id-registry.yaml` (allow-list + format),
- given an `expect_substring` in `matrix/config/control-semantics.yaml` (H2 semantic gate),
- given source provenance in `matrix/config/data-provenance.yaml`,
- with new bib keys in `meta/citations.bib` resolving through the H1 citation-resolution gate,
- and `quote_type` set honestly (verbatim/paraphrase/analyst-note per H1c).

### 4. Questionnaire + report integration

- **`matrix/domains/iga/uc-archetype-map.csv`** — map UC-I-017/018/019 to assessment archetypes.
  Reuse existing IGA archetypes (A1/A2/A5/A7/A8 express governance lifecycle) where they fit; add one
  agentic archetype **only if** none fit cleanly. Regenerate the rubric (`emit_rubric.py`) and the IGA
  questionnaire.
- **`matrix/report_logic.py` `_IGA_AREA_BY_NUM`** — extend the id-range map so UC-I-017..019 →
  **"Agentic governance"** (a new area in `IGA_AREAS`). Regenerate the IGA report; the cross-domain
  report already surfaces `SPN-015` via the M2 spine (no change needed there beyond rebuild).

### Data flow

```
research (WS3-verified) ─ author ─→ use-cases.csv (+3) ─┐
                                    current-state.csv (+3)├─ build_matrix_viewer (IGA) ─ iga-report.html
                         ─ author ─→ regulatory-trace.csv ┘   (new "Agentic governance" posture area)
new controls ─→ control-id-registry + control-semantics + data-provenance ─ validate_data (gates ×3)
new bib keys ─→ meta/citations.bib ─ H1 citation-resolution gate
UC-I-017..019 ─→ uc-archetype-map.csv ─ emit_rubric ─ rubric.iga.json + iga-questionnaire.html
```

## Error handling / edge cases

- A new control whose verbatim quote can't be verified → it is **not** added (honest gap), not
  fabricated; the UC keeps the controls that do verify.
- `_IGA_AREA_BY_NUM` must stay exhaustive — UC ids outside any range fall to "Other"; the 3 new ids
  are added explicitly so they land in "Agentic governance", not "Other".
- Rubric/questionnaire embed sync: regenerate both `rubric.iga.json` and `iga-questionnaire.html`
  after the archetype-map change (the embed-sync gap noted in H6).
- `REG-mapped` count: if a UC is NIST/ISO back-map only (no regulator obligation), record it the same
  honest way IGA already does (e.g. the UC-I-012 precedent), so the compliance count stays truthful.

## Testing (TDD + gates)

- **Data contracts:** `validate_data` ×3 stays clean (new controls registered + semantically gated +
  cited + current); the IGA run exercises all new rows.
- **`tests/` additions:** area-mapping test (`_IGA_AREA_BY_NUM` returns "Agentic governance" for
  UC-I-017..019 and the area appears in `build_posture_maturity`); UC-count/archetype-coverage guard
  (every new UC maps to an archetype); citation-resolution holds for the new keys.
- **Adversarial verification** (WS3-style): a verification ledger proving each external quote was
  re-fetched and verbatim-matched; refuted claims dropped, not softened.
- **Byte-identity:** IGA report + cross-domain report + rubric + questionnaire regenerate
  deterministically; `git diff --exit-code` clean after a fresh rebuild.

## Out of scope (M3.2 / M3.3, deliberate)

- Secrets agentic UCs/identities (M3.2); PAM agentic UCs/identities + ITDR adjacency / A4 (M3.3).
- New spine archetypes or `identity-spine.yaml` changes (the agentic class `SPN-015` already exists).
- React/`app/` changes beyond the regenerated IGA rubric/questionnaire the existing pipeline emits.
- A standalone agentic report/view (the cross-domain spine section already carries the cross-domain
  agentic signal).

## Acceptance

1. `research/agentic/AGENTIC-RESEARCH.md` exists with a WS3-verified source base and the agentic
   sub-tree (sub-classes mapped to `SPN-015`); 0 fabricated, refuted claims dropped.
2. IGA has 3 new agentic governance UCs (UC-I-017/018/019) with verified regulatory trace, illustrative
   current-state, and archetype mappings; rubric + questionnaire regenerated.
3. The IGA report shows a new **"Agentic governance"** posture-maturity area covering the 3 UCs.
4. All gates green ×3 (control-id / semantics / citation-resolve / currency / spine); pytest green;
   rubric parity holds; IGA + cross-domain reports rebuild byte-identical.

# M3.3 — Generalize agentic to PAM (design)

**Date:** 2026-06-15
**Track:** M (market leadership) — M3 sub-project 3 of 3, per `docs/superpowers/specs/2026-06-14-m3-1-agentic-foundation-iga-design.md` (decomposition table).
**Status:** approved, ready for implementation plan
**Foundation:** `research/agentic/AGENTIC-RESEARCH.md` (M3.1, WS3-verified, agentic sub-tree → spine `SPN-015`)

## Purpose

M3.3 closes the M3 generalization: it takes the agentic foundation into the **PAM** domain with
agent **privileged-session brokering**, **JIT elevation / zero standing privilege**, and an
**ITDR-adjacency** detection use case for anomalous agent privileged behaviour. Critically, it
**adds the first agentic privileged identity** to the PAM catalog (no such identity exists today),
closing the PAM agentic-identity gap the M3.1 decomposition called out.

## Decomposition position

| Sub-project | Scope | Status |
|---|---|---|
| M3.1 | Agentic foundation + IGA pilot (3 UCs) | ✅ merged (PR #38) |
| M3.2 | Generalize to secrets (agent credential issuance/rotation) | spec written |
| **M3.3 (this spec)** | Generalize to **PAM**: agent privileged-session brokering + JIT + ITDR adjacency. | this spec |

## Decisions (locked during brainstorming + verified)

| Decision | Choice | Rationale |
|---|---|---|
| Identities | **Add one new identity row** `PID-021` (agentic privileged operator) → `SPN-015` | PAM has no agentic privileged identity today; this closes the gap. No orphan: it is referenced by the new UCs. |
| UC count | **3 focused new UCs** (`UC-P-019/020/021`) | Mirrors M3.1/M3.2 minimalism; covers session-brokering, JIT/ZSP, ITDR-adjacency. |
| Archetypes (PAM is data-driven) | `UC-P-019→A2`, `UC-P-020→A2`, **`UC-P-021→A3`** | Fit by analogy to existing PAM UCs: A2 *Population Migration/Coverage* matches brokering (UC-P-006) and JIT (UC-P-004); **A3 *Capability Adoption*** matches the existing PAM threat-analytics/ITDR UCs (UC-P-015/016→A3). **Correction:** the M3.1 note's "(A4)" referenced a critical-action-plan item, not the assessment archetype — archetype `A4` is *Lifecycle Automation* and does **not** fit a detection UC. No new archetype. |
| Posture area | **New "Agentic privileged access" group in `MATURITY_GROUPS["pam"]`** = `[UC-P-019,UC-P-020,UC-P-021]` | Net-new ids → no double-count subtraction needed (unlike secrets). |
| Verification bar | **WS3-style adversarial** | Reuse already-verified controls; new sources re-fetched, REFUTE posture, verbatim-only, keys resolve through H1. |
| Evidence-catalog | **+3 agentic PAM evidence items** | PAM *has* an `evidence-catalog.csv` (unlike secrets); the evidence-packs gate binds reg-trace `evidence_item_ids` → catalog `ev_id`. |
| Spine | **No change to `identity-spine.yaml`** | `SPN-015` already exists; `PID-021` anchors to it. |

## Architecture

Adds **data** across the full PAM data-driven pipeline (identity-catalog → use-cases → current-state
→ regulatory-trace → evidence-catalog → uc-archetype-map → rubric → report) plus one **report-logic
seam** (a new `MATURITY_GROUPS["pam"]` posture group). Reuses the WS2/WS3 PAM pipeline end-to-end.
No new engine modules.

### 1. New agentic privileged identity

Append to `matrix/domains/pam/identity-catalog.csv` (schema:
`nhi_id,bucket,short_name,description,typical_secrets,lifecycle,governance_maturity,sources_likely,citation_keys,npe_conformance,spine_id`):

- **`PID-021,UNCOMMON,Autonomous / agentic privileged operator`** — an LLM/agent (or agent-delegated
  NPE) that performs privileged actions: requesting JIT elevation, opening brokered privileged
  sessions, running privileged tools on behalf of a human owner. `typical_secrets` = brokered
  short-lived session tokens / OBO tokens (no standing privileged creds in good state).
  `lifecycle=SHORT-LIVED`, `governance_maturity=LOW`, `npe_conformance=CONFORMANT`,
  `spine_id=SPN-015`. `citation_keys` reuse verified agentic source keys (`owasp-llm06-2025`,
  `csa-ai-agents-2024`, etc.).

### 2. Three new agentic PAM UCs

Append to `matrix/domains/pam/use-cases.csv`:

- **UC-P-019 — Agent privileged-session brokering** (P0): autonomous agents obtain privileged
  sessions only through the broker/proxy, fully recorded; the agent holds no standing privileged
  credential. `nhis_in_scope=PID-021`.
- **UC-P-020 — Agent JIT elevation / zero standing privilege** (P0): agent privilege is just-in-time,
  time-boxed and purpose-bound; no standing agent admin; elevation requires owner + purpose.
  `nhis_in_scope=PID-021`.
- **UC-P-021 — Agentic privileged-behaviour detection (ITDR adjacency)** (P1): anomalous or
  compromised agent privileged sessions (excessive autonomy, off-purpose tool use, abnormal
  velocity) are detected and contained — the agent analogue of privileged-access threat analytics.
  `nhis_in_scope=PID-021`.

Plus 3 illustrative rows in `matrix/domains/pam/current-state.csv`: 019 GAP, 020 PARTIAL, 021 GAP.

### 3. Regulatory trace + evidence (framework-lens schema, reuse verified controls)

The PAM reg-trace uses the same **framework-lens** schema as secrets, **plus** an `evidence_item_ids`
column. Header:
`framework_slug,framework_role,control_code,control_short_title,uc_ids,nhi_ids,maturity_level,evidence_url,evidence_quote,citation_keys,evidence_item_ids,quote_type`.
Framework slugs in use: `essential-8`, `apra-cps-234`, `apra-cps-230`, `asd-ism`, `mitre-attack`.

Two moves, both reuse-only on quotes:

1. **Append the 3 new UC ids to existing verified framework-lens rows** whose control applies — copy
   the precedent set by the PAM session/JIT/brokering UCs (`UC-P-002` session isolation, `UC-P-004`
   JIT, `UC-P-006` app-to-app brokering): add `UC-P-019/020/021` to the `uc_ids` of the rows that fit.
   No quote changes — those rows are already WS-verified. Add `PID-021` to the `nhi_ids` of the
   agentic rows.
2. **Add `owasp-llm` `LLM06:2025` rows** for the agentic UCs (excessive-agency control). `owasp-llm`
   is registered + semantically gated but **not yet used in the PAM reg-trace**; reuse the identical
   verified LLM06 quote + URL + `quote_type` proven in the IGA reg-trace (M3.1). Bind these rows'
   `evidence_item_ids` to the new `ev_id`s below.

Append 3 items to `matrix/domains/pam/evidence-catalog.csv` (schema:
`ev_id,requirement,dimension,tier,example_artifact,sensitivity_tag,citation_keys`):
- `EV-PAM-AGENT-SESSION-LOG` — brokered agent privileged-session recording.
- `EV-PAM-AGENT-JIT-GRANT` — agent JIT elevation grant/expiry log.
- `EV-PAM-AGENT-ANOMALY-ALERT` — agent privileged-behaviour anomaly detection output.
Bind these `ev_id`s in the matching reg-trace rows' `evidence_item_ids` (evidence-packs gate).

**No new control registration** unless a genuinely new control's verbatim quote verifies (then
register in `control-id-registry.yaml` + `control-semantics.yaml` + `data-provenance.yaml` same
commit). Prefer reuse.

Append 3 items to `matrix/domains/pam/evidence-catalog.csv` (schema:
`ev_id,requirement,dimension,tier,example_artifact,sensitivity_tag,citation_keys`):
- `EV-PAM-AGENT-SESSION-LOG` — brokered agent privileged-session recording.
- `EV-PAM-AGENT-JIT-GRANT` — agent JIT elevation grant/expiry log.
- `EV-PAM-AGENT-ANOMALY-ALERT` — agent privileged-behaviour anomaly detection output.
Bind these `ev_id`s in the matching reg-trace rows' `evidence_item_ids` (evidence-packs gate).

### 4. Archetype mapping + rubric/questionnaire regen

Append to `matrix/domains/pam/uc-archetype-map.csv` (schema: `uc_id,archetype_id,params,notes`):
`UC-P-019→A2`, `UC-P-020→A2`, `UC-P-021→A3` (params authored per the existing PAM rows' style).
Regenerate `app/src/data/rubric.pam.json` (`emit_rubric.py`) and `questionnaire/pam-questionnaire.html`
(`build_questionnaire.py`), matching the WS2/H6 regeneration invocation.

### 5. "Agentic privileged access" posture area (report-logic seam)

Add a group to `MATURITY_GROUPS["pam"]`:
```python
"Agentic privileged access": ["UC-P-019", "UC-P-020", "UC-P-021"],
```
These ids appear in no other PAM group, so no subtraction/double-count handling is required.

### Data flow

```
identity-catalog.csv (+PID-021) ─┐
use-cases.csv (+UC-P-019..021)   ├─ build_matrix_viewer(pam) ─ pam-report.html
current-state.csv (+3)           │     (new "Agentic privileged access" posture area)
regulatory-trace.csv (+rows, reused verified controls)  │
evidence-catalog.csv (+3) ───────┘
uc-archetype-map.csv (+3) ─ emit_rubric ─ rubric.pam.json + pam-questionnaire.html
report_logic MATURITY_GROUPS["pam"] += "Agentic privileged access" ─ build_posture_maturity
PID-021 → SPN-015 flows to cross-domain via the M2 spine ─ build_cross_domain (rebuild)
```

## Error handling / edge cases

- A new control whose verbatim quote cannot be re-verified → **not added** (honest gap), never
  fabricated.
- `PID-021` must be referenced by at least one UC (it is — all three) so the referential gate and the
  spine view stay coherent; no orphan identity.
- Evidence-packs gate: every `evidence_item_ids` value in the new reg-trace rows must resolve to a new
  `ev_id` in `evidence-catalog.csv`.
- Rubric/questionnaire embed sync: regenerate both `rubric.pam.json` and `pam-questionnaire.html`
  after the archetype-map change (the embed-sync gap noted in H6).
- `REG-mapped` count: NIST/ISO back-map-only UCs recorded the honest way PAM already does.

## Testing (TDD + gates)

- **Data contracts:** `python3 matrix/validate_data.py --data-dir matrix/domains/pam` exits 0
  (control-id / semantics / citation-resolve / evidence-packs / currency / referential / spine).
- **`tests/` additions:** PAM posture-area test (`MATURITY_GROUPS["pam"]` contains "Agentic
  privileged access"; the 3 UCs group there); UC-coverage guard (each new UC has an archetype row);
  identity-referential guard (`PID-021` referenced by UCs and anchored to `SPN-015`). Update any
  golden PAM UC-count / identity-count assertion.
- **Adversarial verification:** any genuinely new source → ledger row in
  `research/agentic/AGENTIC-RESEARCH.md`; refuted claims dropped.
- **Byte-identity:** PAM report + rubric + questionnaire + cross-domain + exec-rollup + backlog
  regenerate deterministically; `git diff --exit-code` clean after a fresh rebuild.

## Out of scope (deliberate)

- New spine archetypes / `identity-spine.yaml` changes (`SPN-015` already exists).
- A standalone agentic report/view (cross-domain spine already carries the cross-domain agentic
  signal; PID-021 surfaces there via `SPN-015`).
- Re-opening M3.1 (IGA) or M3.2 (secrets) scope.

## Acceptance

1. PAM has one new agentic privileged identity (`PID-021` → `SPN-015`) referenced by the new UCs.
2. PAM has 3 new agentic UCs (`UC-P-019/020/021`) with verified regulatory trace, illustrative
   current-state, evidence items, and archetype mappings (`A2/A2/A3`); rubric + questionnaire
   regenerated.
3. The PAM report shows a new **"Agentic privileged access"** posture-maturity area covering the 3 UCs.
4. All gates green (control-id / semantics / citation-resolve / evidence-packs / currency /
   referential / spine); pytest green; rubric parity holds; PAM + cross-domain + exec-rollup +
   backlog rebuild byte-identical.

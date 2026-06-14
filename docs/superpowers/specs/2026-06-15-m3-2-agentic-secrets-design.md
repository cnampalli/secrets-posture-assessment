# M3.2 — Generalize agentic to Secrets (design)

**Date:** 2026-06-15
**Track:** M (market leadership) — M3 sub-project 2 of 3, per `docs/superpowers/specs/2026-06-14-m3-1-agentic-foundation-iga-design.md` (decomposition table).
**Status:** approved, ready for implementation plan
**Foundation:** `research/agentic/AGENTIC-RESEARCH.md` (M3.1, WS3-verified, agentic sub-tree → spine `SPN-015`)

## Purpose

M3.1 delivered the shared agentic foundation (verified research base + agentic sub-tree taxonomy
anchored to spine `SPN-015`) and took **IGA** end-to-end with three agentic governance use cases.
**M3.2 generalizes that foundation to the Secrets domain**: agent **credential issuance / rotation**
use cases surfaced in a new "Agentic" posture-maturity area, at the WS2/WS3 verification bar. PAM
follows in M3.3.

## Decomposition position

| Sub-project | Scope | Status |
|---|---|---|
| M3.1 | Agentic foundation + IGA pilot (3 UCs) | ✅ merged (PR #38) |
| **M3.2 (this spec)** | Generalize to **secrets**: agent credential issuance/rotation UCs, reusing the foundation. | this spec |
| M3.3 | Generalize to **PAM**: agent privileged-session brokering + JIT + ITDR adjacency (A4). | next |

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Identities | **Govern existing — no new identity row** | Secrets already carries rich agentic identities: `NHI-019` (AI agent / autonomous workflow → `SPN-015`), `NHI-010` (observability agent), `NHI-009` (IaC agent). No real gap to fill; the agentic-identity *gap* is in PAM and is closed in M3.3. No orphan rows. |
| UC count | **3 focused new UCs** (`UC-F-028/029/030`) | Mirrors M3.1's high-signal minimalism; covers issuance, rotation/revocation, scope-confinement. |
| Posture area | **New "Agentic" group in `MATURITY_GROUPS["secrets"]`** + **retrofit existing agentic UCs** | The board posture view should reflect *true* agentic coverage, not split it across lifecycle/governance. |
| Verification bar | **WS3-style adversarial** | Reuse already-verified controls; any genuinely new source re-fetched, REFUTE posture, verbatim-only, keys resolve through the H1 gate. |
| Rubric / archetypes | **None — secrets is methodology-only** | `emit_rubric.py` registers secrets with `data_dir=None`; there is **no** `uc-archetype-map.csv` and **no** `evidence-catalog.csv` for secrets. M3.2 therefore has no archetype-map or evidence-catalog work (simpler than M3.1). |
| Spine | **No change to `identity-spine.yaml`** | `SPN-015` already exists; `NHI-019` already anchors to it. |

## Architecture

Adds **data** to the existing secrets domain (use-cases + current-state + regulatory-trace) and one
**report-logic seam** (a new `MATURITY_GROUPS["secrets"]` posture group, with double-count avoidance).
Reuses the WS2/WS3 secrets data-authoring pipeline end-to-end. No new engine modules.

### 1. Three new agent-credential UCs

Append to `matrix/domains/secrets/use-cases.csv` (schema:
`uc_id,category,short_title,story,acceptance_criteria,nhis_in_scope,outcome_lens,backmap_codes,priority_fi,citation_keys`):

- **UC-F-028 — Agent credential issuance via broker** (P0): per-session, per-tool, scoped,
  short-lived credentials brokered to autonomous agents; static long-lived agent keys forbidden in
  new patterns. `nhis_in_scope=NHI-019;NHI-010`.
- **UC-F-029 — Agent credential rotation & revocation** (P0): agent-held credentials rotate
  automatically on a risk cadence and are revoked immediately on agent decommission or compromise;
  no agent credential outlives the agent's purpose. `nhis_in_scope=NHI-019;NHI-009;NHI-010`.
- **UC-F-030 — Agent secret-scope confinement (least-privilege)** (P1): agent credentials are scoped
  per task / per tool; over-broad secret scope (the excessive-agency analogue in the credential
  plane) is detected and flagged. `nhis_in_scope=NHI-019`.

Plus 3 illustrative rows in `matrix/domains/secrets/current-state.csv` (schema:
`uc_id,current_state,confidence,evidence_q_ids,evidence_redacted,gap_notes,sensitivity_tag,citation_keys`):
028 GAP, 029 PARTIAL, 030 GAP — authored honestly as `PUBLIC` illustrative states.

### 2. Regulatory trace (framework-lens schema, reuse verified controls)

The secrets reg-trace uses a **framework-lens** schema, not NIST control-IDs. Header:
`framework_slug,framework_role,control_code,control_short_title,uc_ids,nhi_ids,maturity_level,evidence_url,evidence_quote,citation_keys,quote_type`.
Framework slugs in use: `essential-8`, `cisa-ztmm-v2`, `apra-cps-234`, `apra-cps-230`, `apra-cpg-234`,
`asd-ism`, `mitre-attack`. Rows are keyed by `framework_slug`/`control_code`; the `uc_ids` field is a
multi-value (`;`-separated) list of the UCs that map to that control.

Two moves, both reuse-only on quotes:

1. **Append the 3 new UC ids to existing verified framework-lens rows** whose control applies —
   copy the precedent set by `UC-F-018` (the existing AI-agent brokering UC already maps to
   `essential-8:E8-MFA-WORKLOAD`, `cisa-ztmm-v2:ZT-Pillar-Workload-Runtime`, `apra-cps-234:CPS234-§21/§27(d)`,
   `asd-ism:ISM-1619/1405`, `mitre-attack:T1528`). Add `UC-F-028/029/030` to the `uc_ids` of the rows
   that fit (issuance/rotation/scope). No quote changes — the rows are already WS-verified.
2. **Add `owasp-llm` `LLM06:2025` rows** for the agentic UCs (the excessive-agency control). The
   `owasp-llm` framework is registered in `control-id-registry.yaml` (`LLM06:2025`) and gated in
   `control-semantics.yaml` (`"excessive agency"`) but is **not yet used in the secrets reg-trace**.
   Reuse the **identical verified LLM06 quote + URL + `quote_type`** already proven in the IGA
   reg-trace (M3.1); set `framework_role` consistent with how IGA classes it.

**No new control registration** unless a genuinely new control's verbatim quote verifies; if it does,
register it in `control-id-registry.yaml` + `control-semantics.yaml` + `data-provenance.yaml` in the
same commit. Prefer reuse.

### 3. "Agentic" posture area (report-logic seam)

`build_posture_maturity` groups secrets by `MATURITY_GROUPS["secrets"]`. Today:

```python
"secrets": {
    "Secrets lifecycle": REC_UC_DOMAIN["secrets"],
    "Governance":        REC_UC_DOMAIN["governance"],
},
```

Add a third group **"Agentic"** containing the agentic UCs (retrofit decision):
`[UC-F-011, UC-F-015, UC-F-018, UC-F-028, UC-F-029, UC-F-030, UC-N-019]`.

**Critical seam — double-count avoidance.** The MATURITY_GROUPS branch of `build_posture_maturity`
iterates every group and appends a UC to *each* group whose id-set contains it (there is **no
`break`**). If a retrofitted UC remains in both "Secrets lifecycle"/"Governance" *and* "Agentic", it
is counted twice in the board roll-up. Therefore the agentic ids must be **subtracted** from the
other groups for secrets. Constraint: `REC_UC_DOMAIN` is shared with the recommendations engine and
**must not be mutated**. Implementation: build the secrets group map from explicit, agentic-subtracted
id-lists (e.g. a module-level `_SECRETS_AGENTIC_UCS` set, with lifecycle/governance computed as
`[id for id in REC_UC_DOMAIN[...] if id not in _SECRETS_AGENTIC_UCS]`). This keeps `REC_UC_DOMAIN`
intact and guarantees each UC lands in exactly one posture group.

### Data flow

```
research (M3.1, reused) ─────────────────────────────────────┐
use-cases.csv (+3 UC-F-028..030) ─┐                           │
current-state.csv (+3)            ├─ build_matrix_viewer(secrets) ─ secrets-report.html
regulatory-trace.csv (+rows, reused verified controls) ┘        (new "Agentic" posture area)
report_logic MATURITY_GROUPS["secrets"] += "Agentic" (subtracted) ─ build_posture_maturity
secrets agentic signal already flows to cross-domain via SPN-015 (NHI-019) — rebuild only
```

## Error handling / edge cases

- A new control whose verbatim quote cannot be re-verified → **not added** (honest gap), never
  fabricated; the UC keeps the controls that do verify.
- Double-counting: covered by the subtraction seam above; a unit test asserts each agentic UC appears
  in exactly one posture group and the group totals sum to the domain total.
- `REC_UC_DOMAIN` immutability: the subtraction must be non-mutating (list comprehension / new set),
  asserted by a test that `REC_UC_DOMAIN["secrets"]` still contains its original ids.
- `REG-mapped` count: if a UC is NIST/ISO back-map only (no regulator obligation), record it the same
  honest way the domain already does, so the compliance count stays truthful.

## Testing (TDD + gates)

- **Data contracts:** `python3 matrix/validate_data.py --data-dir matrix/domains/secrets` exits 0
  (new controls reused/registered, semantics, citations resolve, currency); referential gates hold.
- **`tests/` additions:** a secrets posture-area test (`MATURITY_GROUPS["secrets"]` contains
  "Agentic"; the 7 agentic UCs group there and nowhere else; `REC_UC_DOMAIN["secrets"]` unmutated;
  group totals sum to domain total). Update any golden UC-count assertion for secrets.
- **Adversarial verification:** any genuinely new source gets a ledger row appended to
  `research/agentic/AGENTIC-RESEARCH.md` (re-fetched, verbatim, verdict); refuted claims dropped.
- **Byte-identity:** secrets report + cross-domain + exec-rollup + backlog regenerate
  deterministically; `git diff --exit-code` clean after a fresh rebuild.

## Out of scope (M3.3, deliberate)

- PAM agentic UCs/identities + ITDR adjacency / A4 (M3.3).
- New spine archetypes or `identity-spine.yaml` changes (`SPN-015` already exists).
- New secrets identity rows (existing `NHI-019/010/009` coverage is sufficient).
- React/`app/` changes beyond what the existing secrets pipeline regenerates (secrets rubric is
  methodology-only and unaffected by these data rows).

## Acceptance

1. Secrets has 3 new agent-credential UCs (`UC-F-028/029/030`) with verified regulatory trace and
   illustrative current-state; 0 fabricated, refuted claims dropped.
2. The secrets report shows a new **"Agentic"** posture-maturity area covering the agentic UCs
   (the 3 new + the retrofitted UC-F-011/015/018 + UC-N-019), each counted exactly once.
3. All gates green (control-id / semantics / citation-resolve / currency / spine); pytest green;
   secrets + cross-domain + exec-rollup + backlog rebuild byte-identical.
4. `REC_UC_DOMAIN` is unmutated; the vendor-fit / recommendations paths are unaffected.

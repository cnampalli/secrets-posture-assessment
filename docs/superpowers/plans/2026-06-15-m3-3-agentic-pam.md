# M3.3 — Generalize agentic to PAM Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take the PAM domain agentic by adding the first agentic privileged identity (`PID-021`→`SPN-015`) and 3 use cases (agent privileged-session brokering, JIT/ZSP, ITDR-adjacency detection), surfaced in a new "Agentic privileged access" posture area, reusing the M3.1 verified foundation.

**Architecture:** Data-authoring through the full PAM data-driven pipeline (identity-catalog → use-cases → current-state → regulatory-trace → evidence-catalog → uc-archetype-map → rubric → report) plus one report-logic seam (`MATURITY_GROUPS["pam"]` += "Agentic privileged access" — net-new ids, no subtraction needed). Reg-trace REUSES verified controls (append UC ids to existing verbatim rows) + adds one `owasp-llm` `LLM06:2025` row (reuse IGA quote; 12-col PAM schema with `evidence_item_ids`). Adding a new identity changes the cross-domain spine view, so cross-domain + rollup regenerate.

**Tech Stack:** Python 3.12, CSV data contracts, YAML config, pytest.

**Spec:** `docs/superpowers/specs/2026-06-15-m3-3-agentic-pam-design.md` · **Foundation:** `research/agentic/AGENTIC-RESEARCH.md` (M3.1)

---

## File structure

| File | Change | Responsibility |
|---|---|---|
| `matrix/domains/pam/identity-catalog.csv` | modify | +1 row `PID-021` agentic privileged operator → `SPN-015` |
| `matrix/domains/pam/use-cases.csv` | modify | +3 rows UC-P-019/020/021 |
| `matrix/domains/pam/current-state.csv` | modify | +3 illustrative rows (019 GAP, 020 PARTIAL, 021 GAP) |
| `matrix/domains/pam/regulatory-trace.csv` | modify | append UC ids to verified rows + 1 `owasp-llm`/`LLM06:2025` row (12-col, evidence_item_ids) |
| `matrix/domains/pam/evidence-catalog.csv` | modify | +3 agentic evidence items |
| `matrix/domains/pam/uc-archetype-map.csv` | modify | UC-P-019→A2, UC-P-020→A2, UC-P-021→A3 |
| `matrix/report_logic.py` | modify | `MATURITY_GROUPS["pam"]` += "Agentic privileged access" |
| `tests/test_agentic_area.py` | modify | +PAM posture-area test |
| `tests/test_validate_data_domains.py` | modify | PAM agentic UC + identity presence guard |
| `tests/test_emit_rubric.py` | modify | golden: `len(pam)` 18→21, UC-P range→22 |
| generated: `pam-report.html`, `cross-domain-report.html`, `exec-rollup.html`, `pam-backlog.csv`, `rubric.pam.json`, `pam-questionnaire.html` | regenerate | byte-identity artifacts |

**Reused (do not reimplement):** the PAM WS2/WS3 pipeline; `validate_data` gates (incl. evidence-packs); `build_matrix_viewer.py --domain pam`; `build_cross_domain.py`; `build_exec_rollup.py`; `build_backlog.py`; `emit_rubric.py`; `build_questionnaire.py`; the verified IGA `owasp-llm`/`LLM06:2025` quote (`matrix/domains/iga/regulatory-trace.csv:28`); archetypes A2 (Population Migration/Coverage, like UC-P-004/006) and A3 (Capability Adoption, like UC-P-015/016).

**Key integration facts (verified):**
- `PID-020` is the last identity; `UC-P-018` the last UC. New: `PID-021`, `UC-P-019/020/021`.
- PAM reg-trace schema is 12-col **with** `evidence_item_ids`: `framework_slug,framework_role,control_code,control_short_title,uc_ids,nhi_ids,maturity_level,evidence_url,evidence_quote,citation_keys,evidence_item_ids,quote_type`.
- PAM evidence-catalog uses `tier` ∈ {primary, follow-up} and `dimension` ∈ {coverage, enforcement, …}; `sensitivity_tag` `[INTERNAL]`.
- No PAM report snapshot test exists (the frozen snapshot in `test_report_render.py` is secrets-only), and the engine `data-baseline.json` is the secrets default — so neither needs regenerating for M3.3. **But** `build_cross_domain` changes (new identity in the `SPN-015` spine view) — verify no cross-domain frozen fixture trips; if one does, regenerate it deliberately.
- `test_emit_rubric.py` asserts `len(pam) == 18` and `{UC-P-001..018}`; update to 21 and `range(1, 22)`.
- `owasp-llm` is registered (`control-id-registry.yaml`), semantically gated (`control-semantics.yaml`), and provenanced (`data-provenance.yaml:122`) — usable in PAM with no new registration.

---

## Task 1: New agentic privileged identity (PID-021)

**Files:** Modify `matrix/domains/pam/identity-catalog.csv`

- [ ] **Step 1: Append `PID-021`** (schema: `nhi_id,bucket,short_name,description,typical_secrets,lifecycle,governance_maturity,sources_likely,citation_keys,npe_conformance,spine_id`):
  ```
  PID-021,UNCOMMON,Autonomous / agentic privileged operator,"An LLM-driven or agent-delegated identity that performs privileged actions on behalf of a human owner — requesting just-in-time elevation, opening brokered privileged sessions, and running privileged tools. The agentic analogue of a privileged operator; in the good state it holds no standing privileged credential and acts only through the broker.","Brokered short-lived privileged-session tokens; OAuth on-behalf-of tokens; JIT-issued ephemeral credentials (no standing privileged secret)",SHORT-LIVED,LOW,Y,owasp-llm06-2025;csa-ai-agents-2024,CONFORMANT,SPN-015
  ```

- [ ] **Step 2: Validate.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/pam`
  Expected: exit 0 (the identity is self-contained; it becomes referenced by UCs in Task 2/3). If the spine gate flags `SPN-015`, confirm it exists in `identity-spine.yaml` (it does, from M2).

- [ ] **Step 3: Commit.**
  ```bash
  git add matrix/domains/pam/identity-catalog.csv
  git commit -m "feat(m3.3): new agentic privileged identity PID-021 (-> SPN-015)"
  ```

---

## Task 2: Author the 3 PAM agentic UCs

**Files:** Modify `matrix/domains/pam/use-cases.csv`, `matrix/domains/pam/current-state.csv`

- [ ] **Step 1: Append 3 rows to `use-cases.csv`** (schema: `uc_id,category,short_title,story,acceptance_criteria,nhis_in_scope,outcome_lens,backmap_codes,priority_fi,citation_keys`):
  - `UC-P-019,FUNCTIONAL,Agent privileged-session brokering,"As a PAM owner I want autonomous agents to obtain privileged sessions only through the session broker/proxy — fully recorded and with no standing privileged credential held by the agent — so that a compromised or prompt-injected agent cannot open an unbrokered privileged session or retain privileged access.","Autonomous agents reach privileged targets only via the broker/proxy; every agent privileged session is recorded and attributable to the agent identity and its human owner; agents hold no standing privileged credential (broker-issued, short-lived only); unbrokered privileged access paths for agents are blocked.",PID-021,ZT-Pillar-Identity;ZT-Pillar-Workload;E8-RestrictAdminPriv,CPS234-§21;ISM-1304;LLM06:2025,P0,owasp-llm06-2025;csa-ai-agents-2024`
  - `UC-P-020,FUNCTIONAL,Agent JIT elevation / zero standing privilege,"As a risk owner I want any privilege an autonomous agent uses to be just-in-time, time-boxed and bound to a declared purpose and owner, so that no agent carries standing administrative rights between tasks.","Agent privilege is granted just-in-time, time-boxed and purpose-bound; no standing agent admin role membership exists; each elevation records the requesting agent, owner and purpose and auto-expires; standing agent privilege is detected and removed.",PID-021,ZT-Pillar-Identity;E8-RestrictAdminPriv,CPS234-§21;LLM06:2025,P0,owasp-llm06-2025;csa-ai-agents-2024`
  - `UC-P-021,NON_FUNCTIONAL,Agentic privileged-behaviour detection,"As a SOC lead I want anomalous or compromised agent privileged sessions — excessive autonomy, off-purpose tool use, abnormal velocity — to be detected and contained, so that an agent operating beyond its declared purpose in the privileged plane is caught (the agent analogue of privileged-access threat analytics; ITDR adjacency).","Agent privileged sessions are baselined and deviations (off-purpose tool use, scope inflation, abnormal velocity) are alerted to the SOC in near real time; alerts are attributable to the agent identity and owner and mapped to a containment runbook; suspected agent compromise triggers session termination and credential revocation.",PID-021,ZT-Pillar-Visibility-Analytics;ZT-Pillar-Identity,CPS234-§21;LLM06:2025,P1,owasp-llm06-2025;csa-ai-agents-2024`

- [ ] **Step 2: Append 3 rows to `current-state.csv`** (schema: `uc_id,current_state,confidence,evidence_q_ids,evidence_redacted,gap_notes,sensitivity_tag,citation_keys`):
  - `UC-P-019,GAP,MEDIUM,,No agent-aware privileged-session brokering; agents (where present) use standing privileged service accounts,Broker all agent privileged sessions through the PAM proxy with recording and no standing agent credential,[PUBLIC],`
  - `UC-P-020,PARTIAL,MEDIUM,,JIT elevation exists for humans but is not extended to agent identities; agents may hold standing privilege,Extend JIT / zero-standing-privilege to agent identities with purpose-bound time-boxed elevation,[PUBLIC],`
  - `UC-P-021,GAP,MEDIUM,,Privileged-access analytics do not model agent behaviour; off-purpose or anomalous agent sessions are undetected,Baseline agent privileged behaviour and alert deviations to the SOC with a containment runbook,[PUBLIC],`

- [ ] **Step 3: Validate.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/pam`
  Expected: exit 0 (one-directional referential gate; trace/archetype added next). If `PID-021` referential errors appear, they resolve in Task 3/4.

- [ ] **Step 4: Commit.**
  ```bash
  git add matrix/domains/pam/use-cases.csv matrix/domains/pam/current-state.csv
  git commit -m "feat(m3.3): 3 PAM agentic UCs (UC-P-019/020/021)"
  ```

---

## Task 3: Regulatory trace + evidence (reuse verified controls + owasp-llm)

**Files:** Modify `matrix/domains/pam/regulatory-trace.csv`, `matrix/domains/pam/evidence-catalog.csv`

- [ ] **Step 1: Add 3 evidence items to `evidence-catalog.csv`** (schema: `ev_id,requirement,dimension,tier,example_artifact,sensitivity_tag,citation_keys`). Match the existing `dimension`/`tier` vocabulary (`coverage`/`enforcement`; `primary`/`follow-up`) — confirm valid values against existing rows before writing:
  - `EV-PAM-AGENT-SESSION-LOG,"A recording/log of agent-initiated privileged sessions brokered through the PAM proxy, each attributable to the agent identity and its human owner, demonstrating no standing privileged credential is held by the agent.",coverage,primary,"e.g., a brokered agent privileged-session recording with agent+owner attribution",[INTERNAL],owasp-llm06-2025`
  - `EV-PAM-AGENT-JIT-GRANT,"Evidence that agent privilege is granted just-in-time, time-boxed and purpose-bound, with each grant recording the requesting agent, owner and purpose and an auto-expiry.",enforcement,follow-up,"e.g., an agent JIT elevation grant/expiry record",[INTERNAL],owasp-llm06-2025`
  - `EV-PAM-AGENT-ANOMALY-ALERT,"A sample alert showing an anomalous agent privileged session (off-purpose tool use, scope inflation or abnormal velocity) detected, attributed to the agent identity and mapped to a containment runbook.",enforcement,follow-up,"e.g., an agent privileged-behaviour anomaly alert with runbook mapping",[INTERNAL],owasp-llm06-2025`

- [ ] **Step 2: Append the new UC ids to existing verified framework-lens rows** (edit `uc_ids`; do NOT change quotes). Suggested mapping from the precedents:
  - `asd-ism,ISM-1304` (privileged session controls) → add `UC-P-019`
  - `essential-8,E8-RAP-ML3` (restrict admin / JIT, holds UC-P-004) → add `UC-P-020`
  - `apra-cps-234,CPS234-§21` (umbrella, holds most UC-P) → add `UC-P-019;UC-P-020;UC-P-021`
  Add `PID-021` to the `nhi_ids` of those rows.

- [ ] **Step 3: Add one `owasp-llm` / `LLM06:2025` row** (12-col PAM schema, reuse IGA-verified quote, bind the new evidence ids):
  ```
  owasp-llm,THREAT-CONTEXT,LLM06:2025,Excessive Agency,UC-P-019;UC-P-020;UC-P-021,PID-021,N/A,https://genai.owasp.org/llmrisk/llm062025-excessive-agency/,"Excessive Agency is the vulnerability that enables damaging actions to be performed in response to unexpected, ambiguous or manipulated outputs from an LLM",owasp-llm06-2025,EV-PAM-AGENT-SESSION-LOG;EV-PAM-AGENT-JIT-GRANT;EV-PAM-AGENT-ANOMALY-ALERT,verbatim
  ```

- [ ] **Step 4: Validate the data contracts.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/pam`
  Expected: **exit 0** (control-id / semantics / citation-resolve / evidence-packs / currency all pass). The evidence-packs gate binds the reg-trace `evidence_item_ids` to the new catalog `ev_id`s. If the evidence-packs gate fails, confirm the `ev_id`s match exactly and the `dimension`/`tier` values are in the allowed set.

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/domains/pam/regulatory-trace.csv matrix/domains/pam/evidence-catalog.csv
  git commit -m "feat(m3.3): agentic PAM reg-trace (reused verified controls + owasp-llm) + evidence"
  ```

---

## Task 4: Archetype map + "Agentic privileged access" posture area

**Files:** Modify `matrix/domains/pam/uc-archetype-map.csv`, `matrix/report_logic.py`, `tests/test_agentic_area.py`

- [ ] **Step 1: Append 3 rows to `uc-archetype-map.csv`** (schema: `uc_id,archetype_id,params,notes`), matching the PAM A2/A3 param-key style:
  - `UC-P-019,A2,"target_pattern=brokered, recorded agent privileged sessions with no standing agent credential;nhi_population=autonomous/agentic privileged operators (PID-021);legacy_pattern=agents using standing privileged service accounts or unbrokered access;threshold=all agent privileged access paths",Agent privileged-session brokering`
  - `UC-P-020,A2,"target_pattern=just-in-time, time-boxed, purpose-bound agent privilege (zero standing privilege);nhi_population=autonomous/agentic privileged operators (PID-021);legacy_pattern=agents holding standing administrative rights between tasks;threshold=the bulk of agent privilege grants",Agent JIT elevation / zero standing privilege`
  - `UC-P-021,A3,"capability=behavioural detection of anomalous agent privileged sessions (off-purpose tool use, scope inflation, abnormal velocity);nhi_population=agent privileged sessions (PID-021);config_target=deviations alerted to the SOC in near real time, attributed to the agent and owner, and mapped to a containment runbook",Agentic privileged-behaviour detection`

- [ ] **Step 2: Write the failing PAM posture-area test** (append to `tests/test_agentic_area.py`):
```python
def test_pam_has_agentic_posture_group():
    g = rl.MATURITY_GROUPS["pam"]
    assert "Agentic privileged access" in g
    assert set(g["Agentic privileged access"]) == {"UC-P-019", "UC-P-020", "UC-P-021"}
```

- [ ] **Step 3: Run it — expect FAIL.**
  Run: `python3 -m pytest tests/test_agentic_area.py::test_pam_has_agentic_posture_group -v`

- [ ] **Step 4: Edit `report_logic.py`** — add the group to `MATURITY_GROUPS["pam"]` (after "Endpoint & threat analytics"):
  ```python
      "pam": {
          "Credential & session control":
              ["UC-P-001", "UC-P-002", "UC-P-003", "UC-P-007", "UC-P-008"],
          "Privilege governance":
              ["UC-P-004", "UC-P-005", "UC-P-010", "UC-P-014"],
          "Workload & cloud access":
              ["UC-P-006", "UC-P-011", "UC-P-012", "UC-P-013"],
          "Endpoint & threat analytics":
              ["UC-P-009", "UC-P-015", "UC-P-016", "UC-P-017", "UC-P-018"],
          "Agentic privileged access":
              ["UC-P-019", "UC-P-020", "UC-P-021"],
      },
  ```

- [ ] **Step 5: Run the test — expect PASS.**
  Run: `python3 -m pytest tests/test_agentic_area.py -v`

- [ ] **Step 6: Commit.**
  ```bash
  git add matrix/domains/pam/uc-archetype-map.csv matrix/report_logic.py tests/test_agentic_area.py
  git commit -m "feat(m3.3): PAM agentic archetypes (A2/A2/A3) + Agentic-privileged-access posture area"
  ```

---

## Task 5: Guards, golden updates, regenerate artifacts

**Files:** Modify `tests/test_validate_data_domains.py`, `tests/test_emit_rubric.py`; regenerate reports/rubric/questionnaire

- [ ] **Step 1: Add a PAM presence guard** (append to `tests/test_validate_data_domains.py`):
```python
def test_pam_agentic_ucs_and_identity_present():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "pam")
    ucs = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    mapped = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "uc-archetype-map.csv"), encoding="utf-8"))}
    ids = {r["nhi_id"] for r in csv.DictReader(open(os.path.join(base, "identity-catalog.csv"), encoding="utf-8"))}
    for uc in ("UC-P-019", "UC-P-020", "UC-P-021"):
        assert uc in ucs and uc in mapped, f"{uc} missing UC row or archetype mapping"
    assert "PID-021" in ids, "PID-021 missing from PAM identity-catalog"
```

- [ ] **Step 2: Update the emit-rubric goldens** in `tests/test_emit_rubric.py`:
  ```python
  assert len(pam) == 21          # M3.3: +3 agentic UCs (UC-P-019/020/021)
  ```
  and
  ```python
  assert {u["uc_id"] for u in pam} == {f"UC-P-{i:03d}" for i in range(1, 22)}
  ```

- [ ] **Step 3: Regenerate rubric + questionnaire + reports.**
  ```bash
  python3 questionnaire/emit_rubric.py
  python3 questionnaire/build_questionnaire.py --data-dir matrix/domains/pam --out questionnaire/pam-questionnaire.html
  python3 matrix/build_matrix_viewer.py --domain pam
  python3 matrix/build_cross_domain.py
  python3 matrix/build_exec_rollup.py
  python3 matrix/build_backlog.py
  ```
  (Confirm the exact `build_questionnaire.py` invocation against how PAM was regenerated in WS2/M3.1 if flags differ.)

- [ ] **Step 4: Confirm the area renders.**
  Run: `grep -c "Agentic privileged access" matrix/domains/pam/pam-report.html`
  Expected: ≥ 1.

- [ ] **Step 5: Commit.**
  ```bash
  git add -A
  git commit -m "build(m3.3): PAM presence guard + rubric goldens (18->21) + regenerate artifacts"
  ```

---

## Task 6: Full verification + byte-identity

- [ ] **Step 1: Full gate + test run.**
  ```bash
  python3 matrix/validate_data.py
  python3 matrix/validate_data.py --data-dir matrix/domains/secrets
  python3 matrix/validate_data.py --data-dir matrix/domains/pam
  python3 matrix/validate_data.py --data-dir matrix/domains/iga
  python3 -m pytest tests/ -q
  ```
  Expected: validate_data ×4 exit 0; pytest all green. If a cross-domain frozen fixture trips (new identity in the spine view), regenerate it deliberately and note it in the commit.

- [ ] **Step 2: Byte-identity — clean rebuild confirms determinism.**
  ```bash
  python3 matrix/build_matrix_viewer.py --domain secrets
  python3 matrix/build_matrix_viewer.py --domain pam
  python3 matrix/build_matrix_viewer.py --domain iga
  python3 matrix/build_cross_domain.py
  python3 matrix/build_exec_rollup.py
  python3 matrix/build_backlog.py
  python3 questionnaire/emit_rubric.py
  git diff --exit-code
  ```
  Expected: clean.

- [ ] **Step 3: Commit any regenerated artifacts** (if Step 2 produced uncommitted changes).
  ```bash
  git add -A && git commit -m "build(m3.3): regenerate PAM + cross-domain artifacts with agentic identity/area"
  ```

---

## Final verification

- [ ] `python3 -m pytest tests/ -q` → all pass (incl. PAM posture-area + presence guards + updated rubric goldens).
- [ ] `validate_data` ×4 exit 0 (control-id / semantics / citation-resolve / evidence-packs / currency / referential / spine).
- [ ] `grep -c "Agentic privileged access" matrix/domains/pam/pam-report.html` ≥ 1.
- [ ] `PID-021` present and anchored to `SPN-015`; referenced by UC-P-019/020/021.
- [ ] Clean rebuild → `git diff --exit-code` clean.
- [ ] Finish the branch with `superpowers:finishing-a-development-branch` (M3.2 + M3.3 together).

---

## Self-review notes (author)

- **Spec coverage:** new identity PID-021→SPN-015 (Task 1) ✓; 3 UCs (Task 2) ✓; framework-lens reg-trace reuse + owasp-llm LLM06 w/ evidence_item_ids (Task 3) ✓; +3 evidence items (Task 3) ✓; archetypes A2/A2/A3 (Task 4) ✓; "Agentic privileged access" posture area (Task 4) ✓; rubric/questionnaire regen (Task 5) ✓; gates + byte-identity + cross-domain regen (Task 6) ✓.
- **No-fabrication discipline:** reg-trace REUSES verified quotes (existing PAM rows + IGA-verified LLM06); UC stories/acceptance and the PID-021 description are our own authored content. No external quote invented.
- **Type/seam consistency:** archetype ids A2/A2/A3 match the analogous PAM UCs (004/006→A2, 015/016→A3); the methodology-level map is NOT touched (PAM is data-driven, uses its own domain `uc-archetype-map.csv`). The new posture group uses net-new ids, so no double-count subtraction (unlike M3.2 secrets). `data-baseline.json` and the secrets `report.snapshot.html` are NOT affected (engine default is secrets); only cross-domain/rollup change from the new identity.
- **Confirm-at-execution:** exact `build_questionnaire.py` flags (Task 5 Step 3); valid `dimension`/`tier` vocabulary for evidence rows (Task 3 Step 1); whether any cross-domain frozen fixture needs deliberate regeneration (Task 6 Step 1).

# M3.2 — Generalize agentic to Secrets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take the Secrets domain agentic by adding 3 agent credential issuance/rotation use cases and surfacing them — with the existing scattered agentic UCs — in a new "Agentic" posture-maturity area, reusing the M3.1 verified foundation.

**Architecture:** Pure data-authoring through the existing secrets WS2/WS3 pipeline (use-cases → current-state → regulatory-trace → report) plus one report-logic seam (`MATURITY_GROUPS["secrets"]` += "Agentic" with non-mutating double-count subtraction). Secrets is **methodology-only** in `emit_rubric.py` — there is NO `uc-archetype-map.csv` and NO `evidence-catalog.csv`, so there is no archetype/evidence/rubric work. Reg-trace REUSES already-verified controls: append the new UC ids to existing verbatim-verified framework-lens rows, and add one `owasp-llm` `LLM06:2025` row reusing the IGA-verified quote.

**Tech Stack:** Python 3.12, CSV data contracts, YAML config, pytest.

**Spec:** `docs/superpowers/specs/2026-06-15-m3-2-agentic-secrets-design.md` · **Foundation:** `research/agentic/AGENTIC-RESEARCH.md` (M3.1)

---

## File structure

| File | Change | Responsibility |
|---|---|---|
| `matrix/domains/secrets/use-cases.csv` | modify | +3 rows UC-F-028/029/030 |
| `matrix/domains/secrets/current-state.csv` | modify | +3 illustrative assessment rows |
| `matrix/domains/secrets/regulatory-trace.csv` | modify | append UC ids to existing verified rows + 1 new `owasp-llm`/`LLM06:2025` row (reuse IGA quote) |
| `matrix/report_logic.py` | modify | `MATURITY_GROUPS["secrets"]` += "Agentic"; non-mutating subtraction of agentic UCs from lifecycle/governance |
| `tests/test_agentic_area.py` | modify | +secrets posture-area + double-count + REC_UC_DOMAIN-immutability tests |
| `tests/test_validate_data_domains.py` | modify | secrets agentic UC presence guard |
| `tests/fixtures/report.snapshot.html` | regenerate | frozen secrets-report snapshot (legitimately changes) |
| generated: `matrix/domains/secrets/secrets-report.html`, `matrix/cross-domain-report.html`, exec-rollup, backlog | regenerate | byte-identity artifacts |

**Reused (do not reimplement):** the secrets WS2/WS3 pipeline; `validate_data` gates; `build_matrix_viewer.py`; `build_cross_domain.py`; `build_exec_rollup.py`; `build_backlog.py`; the verified IGA `owasp-llm`/`LLM06:2025` row (`matrix/domains/iga/regulatory-trace.csv:28` — copy its `evidence_url`, `evidence_quote`, `owasp-llm06-2025` key, `quote_type=verbatim`); the existing verified secrets framework-lens rows.

**Key integration facts (verified):**
- `REC_UC_DOMAIN["secrets"]` (report_logic.py:20) contains `UC-F-015` and `UC-F-018`; `UC-F-011` and `UC-N-019` are in NO maturity group today. Retrofitting all agentic UCs into "Agentic" therefore requires subtracting `UC-F-015`/`UC-F-018` from "Secrets lifecycle" (the MATURITY_GROUPS branch of `build_posture_maturity` has NO `break`, so a UC in two groups double-counts).
- `REC_UC_DOMAIN` is shared with the recommendations engine — it must NOT be mutated; use list comprehensions to build the subtracted lists.
- Secrets reg-trace schema (11 cols, NO `evidence_item_ids`): `framework_slug,framework_role,control_code,control_short_title,uc_ids,nhi_ids,maturity_level,evidence_url,evidence_quote,citation_keys,quote_type`.
- `tests/test_report_render.py::test_default_report_is_byte_identical` md5-compares the built secrets report to `tests/fixtures/report.snapshot.html`; M3.2 changes the secrets report, so this fixture is regenerated in Task 4.

---

## Task 1: Author the 3 secrets agentic UCs

**Files:** Modify `matrix/domains/secrets/use-cases.csv`, `matrix/domains/secrets/current-state.csv`

- [ ] **Step 1: Append 3 rows to `use-cases.csv`** (schema: `uc_id,category,short_title,story,acceptance_criteria,nhis_in_scope,outcome_lens,backmap_codes,priority_fi,citation_keys`). Author concretely (our own content):

  - `UC-F-028,FUNCTIONAL,Agent credential issuance via broker,"As a platform engineer I want autonomous AI agents to receive tool and API credentials only from a broker that mints per-session, per-tool, scoped, short-lived credentials, so that a compromised or prompt-injected agent cannot obtain or exfiltrate a long-lived secret.","Static long-lived API keys for agents are forbidden in new patterns; agent credentials are broker-minted, scoped per tool and per session, and short-lived; every issuance is logged with the agent identity, owner and requesting purpose; issuance is denied to unregistered or unowned agents.",NHI-019;NHI-010,ZT-Pillar-Identity;ZT-Pillar-Workload;E8-RestrictAdminPriv,CPS234-§21;ISM-1619;LLM06:2025,P0,owasp-llm06-2025;csa-ai-agents-2024`
  - `UC-F-029,FUNCTIONAL,Agent credential rotation & revocation,"As a secrets owner I want credentials held by autonomous agents to rotate automatically on a risk cadence and to be revoked immediately when an agent is decommissioned or shows signs of compromise, so that no agent credential outlives the agent's purpose or a containment event.","Agent-held credentials rotate automatically on a risk-tiered cadence with no service interruption; decommissioning or compromise of an agent triggers immediate revocation of its issued credentials and active sessions; rotation/revocation coverage for agent identities is a tracked KPI and trends up; no long-lived static agent secret persists past its rotation window.",NHI-019;NHI-009;NHI-010,ZT-Pillar-Identity;ZT-Pillar-Workload,CPS234-§21;ISM-1619;LLM06:2025,P0,owasp-llm06-2025;csa-ai-agents-2024`
  - `UC-F-030,FUNCTIONAL,Agent secret-scope confinement,"As a risk owner I want every credential issued to an autonomous agent to be scoped to the minimum tools and data its declared task needs, and for over-broad agent secret-scope to be detected and flagged, so that excessive agency in the credential plane cannot translate a single agent compromise into broad lateral access.","Agent credentials are scoped per task and per tool by default; over-broad or unused scopes on agent credentials are detected and flagged for right-sizing; scope grants are tied to the agent's declared purpose and owner; excessive-agency conditions (credential scope beyond declared purpose) are surfaced to the owner.",NHI-019,ZT-Pillar-Identity;E8-RestrictAdminPriv,CPS234-§21;LLM06:2025,P1,owasp-llm06-2025`

- [ ] **Step 2: Append 3 illustrative rows to `current-state.csv`** (schema: `uc_id,current_state,confidence,evidence_q_ids,evidence_redacted,gap_notes,sensitivity_tag,citation_keys`). States per design (028 GAP, 029 PARTIAL, 030 GAP), authored as PUBLIC illustrative:
  - `UC-F-028,GAP,MEDIUM,,No agent credential broker in operational scope; agents use static long-lived tool API keys,Adopt a per-session agent credential broker (Aembit / Oasis AAM / native workload broker) tied to the agent registry,[PUBLIC],`
  - `UC-F-029,PARTIAL,MEDIUM,,Some agent credentials are rotated on the generic secret-rotation cadence but there is no agent-aware revocation on decommission/compromise,Extend automated rotation and immediate revocation to agent identities; track agent rotation/revocation coverage as a KPI,[PUBLIC],`
  - `UC-F-030,GAP,MEDIUM,,Agent credential scopes are not right-sized; over-broad agent tokens are not detected,Introduce per-task scope confinement and over-broad-scope detection for agent credentials,[PUBLIC],`

- [ ] **Step 3: Validate.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/secrets`
  Expected: **FAIL** — the new `uc_ids` are referenced in use-cases but not yet in regulatory-trace (referential gate). Expected; Task 2 closes it. If a `backmap_codes` value (`LLM06:2025`) is rejected by the control-id gate, that is also expected to resolve once the `owasp-llm` row is added in Task 2; if it persists, confirm `LLM06:2025` is in `control-id-registry.yaml` (it is) and that backmap_codes are gated against the registry.

- [ ] **Step 4: Commit.**
  ```bash
  git add matrix/domains/secrets/use-cases.csv matrix/domains/secrets/current-state.csv
  git commit -m "feat(m3.2): 3 secrets agent-credential UCs (UC-F-028/029/030)"
  ```

---

## Task 2: Regulatory trace (reuse verified controls + owasp-llm)

**Files:** Modify `matrix/domains/secrets/regulatory-trace.csv`

- [ ] **Step 1: Append the new UC ids to existing verified framework-lens rows.** Edit the `uc_ids` field (semicolon list) of these already-verbatim-verified rows to add the agentic UCs where the control applies. Do NOT change any `evidence_quote`/`evidence_url`/`quote_type`. Suggested mapping (mirrors the UC-F-018 precedent):
  - `essential-8,E8-MFA-WORKLOAD` (machine-to-machine MFA / attestation) → add `UC-F-028`
  - `cisa-ztmm-v2,ZT-Pillar-Workload-Runtime` (runtime attestation gates secret release) → add `UC-F-028;UC-F-030`
  - `apra-cps-234,CPS234-§21` (implementation of controls, umbrella) → add `UC-F-028;UC-F-029;UC-F-030`
  - `asd-ism,ISM-1619` (setting/resetting service-account credentials) → add `UC-F-028;UC-F-029`
  - `asd-ism,ISM-1405` (centralised event logging) → add `UC-F-029`
  - `mitre-attack,T1528` (steal application access token) → add `UC-F-028;UC-F-029`
  Add `NHI-019` to the `nhi_ids` of any row above that does not already list it (most already do).

- [ ] **Step 2: Add one new `owasp-llm` / `LLM06:2025` row** reusing the IGA-verified quote. Copy the verified values from `matrix/domains/iga/regulatory-trace.csv:28` (URL `https://genai.owasp.org/llmrisk/llm062025-excessive-agency/`, the verbatim quote, key `owasp-llm06-2025`, `quote_type=verbatim`). The secrets schema has 11 columns (NO `evidence_item_ids`):
  ```
  owasp-llm,THREAT-CONTEXT,LLM06:2025,Excessive Agency,UC-F-018;UC-F-028;UC-F-029;UC-F-030,NHI-019;NHI-010,N/A,https://genai.owasp.org/llmrisk/llm062025-excessive-agency/,"Excessive Agency is the vulnerability that enables damaging actions to be performed in response to unexpected, ambiguous or manipulated outputs from an LLM",owasp-llm06-2025,verbatim
  ```
  (Including `UC-F-018` here brings the pre-existing agent-brokering UC under the excessive-agency control too — honest and harmless.)

- [ ] **Step 3: Confirm no new control registration is needed.** `LLM06:2025` is in `control-id-registry.yaml` (framework `owasp-llm`) and gated in `control-semantics.yaml` (`"excessive agency"`); all other codes touched are pre-registered. If `owasp-llm` provenance is required, confirm it is present in `data-provenance.yaml` (it was added for IGA in M3.1); if absent for the secrets data-dir, add it in this commit.

- [ ] **Step 4: Validate the data contracts.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/secrets`
  Expected: **exit 0** — referential gap closed; control-id / semantics / citation-resolve / currency all pass for the new rows. If a semantic or citation error appears, fix the quote/key (do NOT weaken the gate).

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/domains/secrets/regulatory-trace.csv matrix/config/data-provenance.yaml
  git commit -m "feat(m3.2): agentic secrets reg-trace (reused verified controls + owasp-llm LLM06)"
  ```

---

## Task 3: "Agentic" posture area (report-logic seam)

**Files:** Modify `matrix/report_logic.py`; Modify `tests/test_agentic_area.py`

- [ ] **Step 1: Write the failing tests** (append to `tests/test_agentic_area.py`):

```python
def test_secrets_has_agentic_posture_group():
    g = rl.MATURITY_GROUPS["secrets"]
    assert "Agentic" in g
    agentic = set(g["Agentic"])
    assert {"UC-F-011", "UC-F-015", "UC-F-018",
            "UC-F-028", "UC-F-029", "UC-F-030", "UC-N-019"} <= agentic


def test_secrets_agentic_ucs_counted_once():
    g = rl.MATURITY_GROUPS["secrets"]
    seen = {}
    for ids in g.values():
        for uc in ids:
            seen[uc] = seen.get(uc, 0) + 1
    for uc in ("UC-F-015", "UC-F-018"):  # these were in REC_UC_DOMAIN["secrets"]
        assert seen.get(uc) == 1, f"{uc} appears in more than one posture group"


def test_rec_uc_domain_not_mutated():
    # REC_UC_DOMAIN is shared with the recommendations engine; subtraction must be non-mutating.
    assert "UC-F-015" in rl.REC_UC_DOMAIN["secrets"]
    assert "UC-F-018" in rl.REC_UC_DOMAIN["secrets"]
```

- [ ] **Step 2: Run them — expect FAIL** (`"Agentic"` not a key; `UC-F-015`/`UC-F-018` double-count or absent).
  Run: `python3 -m pytest tests/test_agentic_area.py -v`

- [ ] **Step 3: Edit `report_logic.py`.** Immediately ABOVE `MATURITY_GROUPS = {` (line 33), add:
  ```python
  # M3.2: agentic UCs surfaced as their own emerging posture area. They are subtracted
  # from the lifecycle/governance lists below so each UC is counted in exactly one
  # posture group. REC_UC_DOMAIN is shared with the recommendations engine and is NOT
  # mutated — the subtraction uses list comprehensions over copies.
  _SECRETS_AGENTIC_UCS = ["UC-F-011", "UC-F-015", "UC-F-018", "UC-F-028",
                          "UC-F-029", "UC-F-030", "UC-N-019"]
  _SECRETS_AGENTIC_SET = set(_SECRETS_AGENTIC_UCS)
  ```
  Then change the `"secrets"` entry of `MATURITY_GROUPS` from:
  ```python
      "secrets": {
          "Secrets lifecycle": REC_UC_DOMAIN["secrets"],
          "Governance": REC_UC_DOMAIN["governance"],
      },
  ```
  to:
  ```python
      "secrets": {
          "Secrets lifecycle": [u for u in REC_UC_DOMAIN["secrets"]
                                if u not in _SECRETS_AGENTIC_SET],
          "Governance": [u for u in REC_UC_DOMAIN["governance"]
                         if u not in _SECRETS_AGENTIC_SET],
          "Agentic": list(_SECRETS_AGENTIC_UCS),
      },
  ```

- [ ] **Step 4: Run the tests — expect PASS.**
  Run: `python3 -m pytest tests/test_agentic_area.py -v`

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/report_logic.py tests/test_agentic_area.py
  git commit -m "feat(m3.2): Agentic secrets posture area (non-mutating double-count subtraction)"
  ```

---

## Task 4: UC guard, regenerate artifacts + full verification

**Files:** Modify `tests/test_validate_data_domains.py`; regenerate reports + frozen snapshot

- [ ] **Step 1: Add a secrets UC-presence guard** (append to `tests/test_validate_data_domains.py`; `ROOT` is already defined there):

```python
def test_secrets_agentic_ucs_present():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "secrets")
    ucs = {r["uc_id"] for r in csv.DictReader(
        open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    for uc in ("UC-F-028", "UC-F-029", "UC-F-030"):
        assert uc in ucs, f"{uc} missing from secrets use-cases.csv"
```

- [ ] **Step 2: Rebuild the secrets + cross-domain + roll-up + backlog artifacts.**
  ```bash
  python3 matrix/build_matrix_viewer.py --domain secrets
  python3 matrix/build_cross_domain.py
  python3 matrix/build_exec_rollup.py
  python3 matrix/build_backlog.py
  ```

- [ ] **Step 3: Confirm the Agentic area renders.**
  Run: `grep -c "Agentic" matrix/domains/secrets/secrets-report.html`
  Expected: ≥ 1.

- [ ] **Step 4: Regenerate the frozen secrets-report snapshot** (it legitimately changed).
  ```bash
  cp matrix/domains/secrets/secrets-report.html tests/fixtures/report.snapshot.html
  ```

- [ ] **Step 5: Full gate + test run.**
  ```bash
  python3 matrix/validate_data.py
  python3 matrix/validate_data.py --data-dir matrix/domains/secrets
  python3 matrix/validate_data.py --data-dir matrix/domains/pam
  python3 -m pytest tests/ -q
  ```
  Expected: validate_data ×3 exit 0; pytest all green (incl. the regenerated snapshot test and the new guards). If another frozen snapshot (e.g. cross-domain/roll-up) legitimately changed because secrets posture shifted, regenerate that fixture the same deliberate way and note it in the commit.

- [ ] **Step 6: Byte-identity — clean rebuild confirms determinism.**
  ```bash
  python3 matrix/build_matrix_viewer.py --domain secrets
  python3 matrix/build_matrix_viewer.py --domain pam
  python3 matrix/build_matrix_viewer.py --domain iga
  python3 matrix/build_cross_domain.py
  python3 matrix/build_exec_rollup.py
  python3 matrix/build_backlog.py
  git diff --exit-code
  ```
  Expected: clean (all report/CSV byte-changes already committed in their tasks).

- [ ] **Step 7: Commit regenerated artifacts.**
  ```bash
  git add matrix/domains/secrets/secrets-report.html matrix/cross-domain-report.html tests/fixtures/report.snapshot.html tests/test_validate_data_domains.py
  git add -A
  git commit -m "build(m3.2): regenerate secrets + cross-domain reports with Agentic area; refresh snapshot"
  ```

---

## Final verification

- [ ] `python3 -m pytest tests/ -q` → all pass (incl. secrets posture-area + double-count + immutability + UC-presence guards).
- [ ] `validate_data` ×3 exit 0 (agentic controls reused, semantics, citations resolve, currency).
- [ ] `grep -c "Agentic" matrix/domains/secrets/secrets-report.html` ≥ 1.
- [ ] `REC_UC_DOMAIN["secrets"]` still contains UC-F-015/UC-F-018 (immutability test green).
- [ ] Clean rebuild → `git diff --exit-code` clean.
- [ ] Proceed to M3.3 (PAM) in this same worktree, then finish the branch with `superpowers:finishing-a-development-branch`.

---

## Self-review notes (author)

- **Spec coverage:** 3 agent-credential UCs (Task 1) ✓; framework-lens reg-trace reuse + owasp-llm LLM06 (Task 2) ✓; "Agentic" posture area with double-count subtraction (Task 3) ✓; retrofit of existing agentic UCs into the area (Task 3 `_SECRETS_AGENTIC_UCS`) ✓; govern existing identities / no new identity / no spine change (Tasks 1-2, explicit) ✓; gates + byte-identity + snapshot refresh (Task 4) ✓; methodology-only (no archetype/evidence work) honored ✓.
- **No-fabrication discipline:** reg-trace REUSES already-verified quotes (copy from existing secrets rows + the IGA-verified LLM06 row); UC stories/acceptance are our own authored content. No external quote is invented.
- **Type/seam consistency:** `_SECRETS_AGENTIC_UCS`/`_SECRETS_AGENTIC_SET` defined in Task 3 before `MATURITY_GROUPS` and asserted by the same task's tests; `REC_UC_DOMAIN` left unmutated (recommendations path unaffected), asserted by `test_rec_uc_domain_not_mutated`. Snapshot fixture regenerated deliberately (Task 4) because the secrets report legitimately changes.
- **Confirm-at-execution:** whether `backmap_codes=LLM06:2025` passes the control-id gate without the owasp-llm row present (Task 1 Step 3 flags this; resolves in Task 2); whether any second frozen snapshot (cross-domain/roll-up) also needs deliberate regeneration (Task 4 Step 5).

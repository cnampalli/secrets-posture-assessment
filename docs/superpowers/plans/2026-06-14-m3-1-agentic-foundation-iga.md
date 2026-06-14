# M3.1 — Agentic foundation + IGA pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the shared agentic foundation (WS3-verified research base + agentic sub-tree taxonomy mapping to spine `SPN-015`) and take IGA end-to-end with 3 agentic governance use cases surfaced in a new "Agentic governance" report area.

**Architecture:** Pure data-authoring through the existing WS2/WS3 IGA pipeline (use-cases → current-state → regulatory-trace → evidence-catalog → uc-archetype-map → rubric → report) plus one surgical `report_logic.py` seam for the new posture area. No new engine modules. Reg-trace **reuses already-registered, already-verified controls** (`LLM06:2025`, `AC-2`, `AC-6`, `CPS234-§14/§21`); new external-claim verification is concentrated in the research artifact.

**Tech Stack:** Python 3.12, CSV data contracts, YAML config, pytest; WS3-style adversarial source verification.

**Spec:** `docs/superpowers/specs/2026-06-14-m3-1-agentic-foundation-iga-design.md` · **Mock:** `docs/superpowers/sketches/2026-06-14-m3-agentic-iga-mock.html`

---

## File structure

| File | Change | Responsibility |
|---|---|---|
| `research/agentic/AGENTIC-RESEARCH.md` | create | WS3-verified source base (OWASP LLM06 2025, CSA agentic, NIST AI) + agentic sub-tree taxonomy → `SPN-015` + verification ledger |
| `matrix/domains/iga/use-cases.csv` | modify | +3 rows UC-I-017/018/019 |
| `matrix/domains/iga/current-state.csv` | modify | +3 illustrative assessment rows |
| `matrix/domains/iga/regulatory-trace.csv` | modify | +rows mapping the 3 UCs to LLM06:2025 / AC-2 / AC-6 / CPS234 (reused verified quotes) |
| `matrix/domains/iga/evidence-catalog.csv` | modify | +3 agentic evidence items |
| `matrix/domains/iga/uc-archetype-map.csv` | modify | UC-I-017→A2, UC-I-018→A5, UC-I-019→A3 |
| `matrix/report_logic.py` | modify | `_IGA_AREA_BY_NUM` += (17,19,"Agentic governance"); decouple posture areas from vendor-fit `IGA_AREAS` |
| `meta/citations.bib` | modify | new bib keys for any new AGENTIC-RESEARCH sources (resolve through H1 gate) |
| `tests/test_report_logic.py` (or new `tests/test_agentic_area.py`) | modify/create | area-mapping + posture-area unit tests |
| `tests/test_validate_data_domains.py` | modify | UC-count / archetype-coverage guard for the new UCs |
| generated: `iga-report.html`, `cross-domain-report.html`, `rubric.iga.json`, `iga-questionnaire.html` | regenerate | byte-identity artifacts |

**Reused (do not reimplement):** the WS2/WS3 IGA data pipeline; `validate_data` gates (control-id, semantics, citation-resolve, evidence-packs, currency); `build_matrix_viewer.py --domain iga`; `build_cross_domain.py`; `emit_rubric.py`; the already-verified control rows for `LLM06:2025` / `AC-2` / `AC-6` / `CPS234-§14` / `CPS234-§21` (copy their verbatim `evidence_quote`/`evidence_url`/`citation_keys`); archetypes A2 (Population/Coverage), A5 (Inventory & Attestation), A3 (Capability Adoption).

**Key integration fact (verified):** `IGA_AREAS = ["JML","Certification","SoD","Role/Request"]` (report_logic.py:534) drives BOTH posture grouping (line 314) AND the vendor-fit grid (lines 562/582). Adding "Agentic governance" to `IGA_AREAS` would inject an empty agentic column into the vendor-fit view. So Task 4 **decouples**: posture grouping uses a new `_IGA_POSTURE_AREAS = IGA_AREAS + ["Agentic governance"]`; `IGA_AREAS` (vendor-fit) is unchanged.

---

## Task 1: Agentic research base + sub-tree taxonomy (WS3-verified)

**Files:** Create `research/agentic/AGENTIC-RESEARCH.md`; Modify `meta/citations.bib`

- [ ] **Step 1: Fetch + verify the source base (adversarial, REFUTE posture).**
  Re-fetch each source live and capture a verbatim quote + canonical URL + access date:
  - OWASP Top 10 for LLM Applications 2025 — **LLM06:2025 Excessive Agency** (genai.owasp.org). Confirm the existing bib key `owasp-llm06-2025` URL still resolves; capture the verbatim "excessive functionality, permissions, or autonomy" framing.
  - CSA agentic-AI guidance (cloudsecurityalliance.org) — agentic identity governance.
  - NIST AI RMF / SP 800-53 AC family as applied to autonomous agents.
  Drop any claim that does not verify verbatim (do NOT soften). Record a per-source ledger row: `source | url | access_date | verbatim_quote | verdict(CONFIRMED/DRIFT/REFUTED)`.

- [ ] **Step 2: Write `research/agentic/AGENTIC-RESEARCH.md`** with two sections:
  1. **Verification ledger** (the table from Step 1; mirrors `research/iga/RESEARCH-SUMMARY.md` style, honesty caveats inline).
  2. **Agentic sub-tree** — a table of sub-classes, each mapping to spine `SPN-015`:

  | Sub-class | Maps to | Anchor |
  |---|---|---|
  | Autonomous task agent | SPN-015 | OWASP LLM06; CSA agentic |
  | Tool-using (function-calling) agent | SPN-015 | OWASP LLM06; NIST AI RMF |
  | Agent-delegated NPE (OBO / consent-grant) | SPN-015 / SPN-010 | OAuth; IGID-013 pattern |
  | Human-gated agent (HITL on irreversible) | SPN-015 | OWASP LLM06; NIST AC-6 |
  | Multi-agent orchestrator | SPN-015 | CSA agentic |

  State explicitly: this extends the NHI taxonomy; **no change to `identity-spine.yaml`** (the `SPN-015` archetype already exists from M2).

- [ ] **Step 3: Add bib keys** to `meta/citations.bib` for any NEW source not already present (e.g. a CSA agentic guidance key, a NIST AI RMF key). Reuse existing `owasp-llm06-2025` / `owasp-llm-top10-2024` where they apply. Every new key needs a real resolvable URL (no fabricated URLs).

- [ ] **Step 4: Verify the citation gate.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/iga`
  Expected: exit 0 (no dangling keys — note new keys aren't cited by data rows yet, so they won't be flagged until used in Task 3; this run just confirms nothing broke).

- [ ] **Step 5: Commit.**
  ```bash
  git add research/agentic/AGENTIC-RESEARCH.md meta/citations.bib
  git commit -m "research(m3.1): WS3-verified agentic source base + sub-tree taxonomy (-> SPN-015)"
  ```

---

## Task 2: Author the 3 IGA agentic UCs

**Files:** Modify `matrix/domains/iga/use-cases.csv`, `matrix/domains/iga/current-state.csv`

- [ ] **Step 1: Append 3 rows to `use-cases.csv`** (schema: `uc_id,category,short_title,story,acceptance_criteria,nhis_in_scope,outcome_lens,backmap_codes,priority_fi,citation_keys`). Author concretely (this is our content, not external claims):

  - `UC-I-017,FUNCTIONAL,Agent registration & ownership,"As an identity-governance owner I want every autonomous AI agent operating against enterprise systems to be a registered, governed object — with a named human owner, a declared purpose and a scoped, least-privilege set of tool entitlements recorded before the agent is allowed to act — so that no unowned or undeclared agent holds standing access.","An inventory of autonomous agents exists with a named human owner, declared purpose and recorded tool-scope per agent, and inventory coverage is measured and trending up; an agent cannot obtain or retain access without a registered owner and purpose; agent tool-scopes are least-privilege by default and over-broad scopes are flagged; registration is required before first action, not retrofitted.",IGID-012;IGID-013,Every autonomous agent is owned, declared and least-privilege before it acts,AC-2;LLM06:2025;CPS234-§14,P0,nist-sp-800-53-ac2;owasp-llm06-2025;apra-cps-234-para14`
  - `UC-I-018,FUNCTIONAL,Agent entitlement certification / continuous attestation,"As a risk owner I want an agent's tool-scopes and downstream permissions to be recertified on a risk cadence and — because an agent's effective permissions change dynamically as it is re-prompted and re-tooled — for point-in-time recertification to be augmented by continuous attestation, so that an agent's live authority never silently exceeds what was certified.","Agent entitlements are recertified by the owner on a risk-tiered cadence and revocations are actioned within SLA; effective agent authority (granted tool-scopes plus inherited service-account / OAuth scopes) is resolvable; drift between certified and live agent authority is detected continuously and alerted, with continuous attestation modelled as the good end-state rather than periodic-only recert; excessive-agency conditions (autonomy or permissions beyond purpose) are surfaced.",IGID-012;IGID-013,Agent authority is recertified and continuously attested against its declared purpose,AC-6;LLM06:2025,P0,nist-sp-800-53-ac6;owasp-llm06-2025`
  - `UC-I-019,FUNCTIONAL,Agent deprovisioning / orphan-agent detection,"As a governance owner I want decommissioned or owner-less autonomous agents — and the standing consent grants and credentials they leave behind — to be detected and revoked, so that orphaned agents do not persist as durable account-independent access (the agentic analogue of the dormant/orphan finding).","Agents whose owner has left or whose purpose has ended are detected within a defined window and deprovisioned, including revocation of their OAuth consent grants, tool-scopes and issued credentials; orphan-agent population is a tracked KPI and trends down; a decommissioned agent leaves no residual standing access surviving its removal.",IGID-012;IGID-013,No decommissioned or owner-less agent retains standing access,AC-2;LLM06:2025;CPS234-§21,P1,nist-sp-800-53-ac2;owasp-llm06-2025;apra-cps-234-para21`

- [ ] **Step 2: Append 3 illustrative rows to `current-state.csv`** (schema: `uc_id,current_state,confidence,evidence_q_ids,evidence_redacted,gap_notes,sensitivity_tag,citation_keys`). States per the mock (017 GAP, 018 PARTIAL, 019 GAP):
  - `UC-I-017,GAP,MED,,,"No agent registry exists; autonomous agents run under shared or over-privileged service accounts with no declared owner or purpose.",PUBLIC,`
  - `UC-I-018,PARTIAL,MED,,,"Some agent tool-scopes are reviewed during periodic access certification, but there is no continuous attestation and effective agent authority is not resolvable end-to-end.",PUBLIC,`
  - `UC-I-019,GAP,MED,,,"Decommissioned agents and their consent grants are not systematically detected; orphan-agent population is unmeasured.",PUBLIC,`

- [ ] **Step 3: Validate.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/iga`
  Expected: **FAIL** — the new `uc_ids` are referenced but not yet in regulatory-trace / archetype-map (referential gate). This is expected; Tasks 3 & 5 close it. (If it unexpectedly passes, re-check the referential gate covers UC↔trace.)

- [ ] **Step 4: Commit.**
  ```bash
  git add matrix/domains/iga/use-cases.csv matrix/domains/iga/current-state.csv
  git commit -m "feat(m3.1): 3 IGA agentic governance UCs (UC-I-017/018/019)"
  ```

---

## Task 3: Regulatory trace + evidence (reuse verified controls)

**Files:** Modify `matrix/domains/iga/regulatory-trace.csv`, `matrix/domains/iga/evidence-catalog.csv`

- [ ] **Step 1: Copy verified control rows.** For each control the UCs cite (`AC-2`, `AC-6`, `LLM06:2025`, `CPS234-§14`, `CPS234-§21`), find the existing IGA regulatory-trace row that already carries its verbatim `evidence_quote` + `evidence_url` + `citation_keys` + `quote_type` (these were WS1/WS2/H-chain verified). Add UC-I-017/018/019 to the `uc_ids` of those rows where the control applies, OR add new rows reusing the identical verified quote — whichever keeps one control_code coherent. Mapping:
  - `AC-2` → add UC-I-017, UC-I-019
  - `AC-6` → add UC-I-018
  - `LLM06:2025` (owasp-llm) → all three (017/018/019); copy the verified LLM06 quote (the `excessive agency` row; if no data row exists yet, fetch genai.owasp.org and capture verbatim, `quote_type=verbatim`)
  - `CPS234-§14` → UC-I-017; `CPS234-§21` → UC-I-019
  - `nhi_ids` on agentic rows: include `IGID-012;IGID-013`.

- [ ] **Step 2: Add 3 evidence items to `evidence-catalog.csv`** (schema: `ev_id,requirement,dimension,tier,example_artifact,sensitivity_tag,citation_keys`):
  - `EV-IGA-AGENT-REGISTRY,Inventory of autonomous agents with owner+purpose+tool-scope,coverage,1,Agent registry export,PUBLIC,owasp-llm06-2025`
  - `EV-IGA-AGENT-CERT-LOG,Agent entitlement recertification + drift-attestation log,attestation,2,Certification campaign + drift report,PUBLIC,owasp-llm06-2025`
  - `EV-IGA-ORPHAN-AGENT-SCAN,Orphan/owner-less agent detection + revocation report,detection,2,Orphan-agent scan output,PUBLIC,`
  Reference these `ev_id`s in the matching reg-trace rows' `evidence_item_ids` where the schema uses them (the `evidence-packs` gate binds reg-trace `evidence_item_ids` to catalog `ev_id`).

- [ ] **Step 3: Confirm no new control registration is needed.** `LLM06:2025` is in `control-id-registry.yaml` (pattern `^LLM\d{2}:2025$`) and `control-semantics.yaml` (`"excessive agency"`); `AC-2`/`AC-6`/`CPS234-§14`/`CPS234-§21` are registered + semantically gated. **If** you introduce any control NOT already registered, add it to `control-id-registry.yaml` + `control-semantics.yaml` (distinctive `expect_substring`) + `data-provenance.yaml` in the same commit. Prefer reuse to avoid new registration.

- [ ] **Step 4: Validate the data contracts.**
  Run: `python3 matrix/validate_data.py --data-dir matrix/domains/iga`
  Expected: still FAIL only on the archetype-map referential gap (Task 5); all of control-id / semantics / citation-resolve / evidence-packs / currency now pass for the new rows. If a semantic or citation error appears, fix the quote/key (do not weaken the gate).

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/domains/iga/regulatory-trace.csv matrix/domains/iga/evidence-catalog.csv
  git commit -m "feat(m3.1): agentic reg-trace (reused verified controls) + evidence items"
  ```

---

## Task 4: "Agentic governance" posture area (report-logic seam)

**Files:** Modify `matrix/report_logic.py`; Create `tests/test_agentic_area.py`

- [ ] **Step 1: Write the failing test** (`tests/test_agentic_area.py`):

```python
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "matrix"))
import report_logic as rl  # noqa: E402


def test_agentic_ucs_map_to_agentic_area():
    assert rl._iga_area_for("UC-I-017") == "Agentic governance"
    assert rl._iga_area_for("UC-I-018") == "Agentic governance"
    assert rl._iga_area_for("UC-I-019") == "Agentic governance"


def test_existing_areas_unchanged():
    assert rl._iga_area_for("UC-I-001") == "JML"
    assert rl._iga_area_for("UC-I-005") == "Certification"


def test_agentic_area_in_posture_order_not_in_vendor_fit():
    # posture grouping includes the new area; vendor-fit IGA_AREAS does NOT
    assert "Agentic governance" in rl._IGA_POSTURE_AREAS
    assert "Agentic governance" not in rl.IGA_AREAS
```

- [ ] **Step 2: Run it — expect FAIL** (`_IGA_POSTURE_AREAS` undefined; UC-I-017 → "Other").
  Run: `python3 -m pytest tests/test_agentic_area.py -v`

- [ ] **Step 3: Edit `report_logic.py`.**
  Extend the id-range map (currently ends `(16, 16, "Role/Request")`):
  ```python
  _IGA_AREA_BY_NUM = (
      (1, 4, "JML"), (5, 7, "Certification"), (8, 10, "SoD"), (11, 13, "Role/Request"),
      (14, 14, "Certification"), (15, 15, "SoD"), (16, 16, "Role/Request"),
      (17, 19, "Agentic governance"))
  ```
  Add the decoupled posture-area list near `IGA_AREAS = ["JML", "Certification", "SoD", "Role/Request"]` (line 534):
  ```python
  # Posture grouping shows an emerging agentic area; the vendor-fit grid (IGA_AREAS) does
  # NOT — there is no agentic IGA vendor rating yet, so it must not get an empty column.
  _IGA_POSTURE_AREAS = IGA_AREAS + ["Agentic governance"]
  ```
  In `build_posture_maturity`, change the IGA branch (line ~314) from `labels_order = list(IGA_AREAS) + ["Other"]` to:
  ```python
  labels_order = list(_IGA_POSTURE_AREAS) + ["Other"]
  ```

- [ ] **Step 4: Run the test — expect PASS.**
  Run: `python3 -m pytest tests/test_agentic_area.py -v`

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/report_logic.py tests/test_agentic_area.py
  git commit -m "feat(m3.1): Agentic-governance posture area (decoupled from vendor-fit IGA_AREAS)"
  ```

---

## Task 5: Archetype mapping + rubric/questionnaire regen

**Files:** Modify `matrix/domains/iga/uc-archetype-map.csv`; Modify `tests/test_validate_data_domains.py`; regenerate rubric + questionnaire

- [ ] **Step 1: Append 3 rows to `uc-archetype-map.csv`** (schema: `uc_id,archetype_id,params,notes`). Reuse existing archetypes (no new agentic archetype):
  - `UC-I-017,A2,"target_pattern=registered autonomous agents with a named owner, declared purpose and recorded least-privilege tool-scope;nhi_population=autonomous AI agents and their delegated OAuth/consent identities;legacy_pattern=agents running under shared or over-privileged service accounts with no owner;threshold=the agreed coverage threshold of agents registered and owned",Agent registration & ownership coverage`
  - `UC-I-018,A5,"process=risk-cadence recertification of agent tool-scopes augmented by continuous attestation of drift between certified and live agent authority",Agent entitlement certification / continuous attestation`
  - `UC-I-019,A3,"process=detection and deprovisioning of decommissioned or owner-less agents including revocation of standing consent grants and credentials;legacy_pattern=orphaned agents persisting with standing access",Agent deprovisioning / orphan-agent detection`

- [ ] **Step 2: Write the UC-coverage guard** in `tests/test_validate_data_domains.py` (append):

```python
def test_iga_agentic_ucs_have_archetypes():
    import csv, os
    base = os.path.join(ROOT, "matrix", "domains", "iga")
    ucs = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "use-cases.csv"), encoding="utf-8"))}
    mapped = {r["uc_id"] for r in csv.DictReader(open(os.path.join(base, "uc-archetype-map.csv"), encoding="utf-8"))}
    for uc in ("UC-I-017", "UC-I-018", "UC-I-019"):
        assert uc in ucs and uc in mapped, f"{uc} missing UC row or archetype mapping"
```
(`ROOT` is already defined in this test module.)

- [ ] **Step 3: Run the guard + the full IGA validation — expect PASS now.**
  ```bash
  python3 -m pytest tests/test_validate_data_domains.py -q
  python3 matrix/validate_data.py --data-dir matrix/domains/iga
  ```
  Expected: tests pass; `validate_data` IGA exits 0 (referential gap from Tasks 2/3 now closed).

- [ ] **Step 4: Regenerate the rubric + questionnaire.**
  ```bash
  python3 questionnaire/emit_rubric.py          # emits rubric.iga.json (per-domain)
  python3 questionnaire/build_questionnaire.py --data-dir matrix/domains/iga --out matrix/domains/iga/iga-questionnaire.html
  ```
  (Confirm the exact emit/build invocation against `questionnaire/` README if flags differ; match how PAM/IGA were regenerated in WS2/H6.)

- [ ] **Step 5: Commit.**
  ```bash
  git add matrix/domains/iga/uc-archetype-map.csv tests/test_validate_data_domains.py questionnaire/rubric.iga.json matrix/domains/iga/iga-questionnaire.html
  git commit -m "feat(m3.1): map agentic UCs to archetypes + regenerate IGA rubric/questionnaire"
  ```

---

## Task 6: Rebuild artifacts + full verification

**Files:** regenerate reports; final gates

- [ ] **Step 1: Rebuild the IGA + cross-domain reports.**
  ```bash
  python3 matrix/build_matrix_viewer.py --domain iga
  python3 matrix/build_cross_domain.py
  ```

- [ ] **Step 2: Confirm the agentic area renders.**
  Run: `grep -c "Agentic governance" matrix/domains/iga/iga-report.html`
  Expected: ≥ 1.

- [ ] **Step 3: Full gate run.**
  ```bash
  python3 matrix/validate_data.py
  python3 matrix/validate_data.py --data-dir matrix/domains/iga
  python3 matrix/validate_data.py --data-dir matrix/domains/pam
  python3 -m pytest tests/ -q
  ```
  Expected: validate_data ×3 exit 0; pytest all green.

- [ ] **Step 4: Byte-identity — rebuild everything and confirm determinism.**
  ```bash
  python3 matrix/build_matrix_viewer.py --domain secrets
  python3 matrix/build_matrix_viewer.py --domain pam
  python3 matrix/build_matrix_viewer.py --domain iga
  python3 matrix/build_cross_domain.py
  python3 matrix/build_exec_rollup.py
  python3 matrix/build_backlog.py
  git diff --exit-code
  ```
  Expected: clean (any report/CSV byte-changes already committed in their tasks). If the secrets snapshot test trips, the secrets report did not change here — investigate before regenerating.

- [ ] **Step 5: Commit any regenerated artifacts.**
  ```bash
  git add matrix/domains/iga/iga-report.html matrix/cross-domain-report.html
  git commit -m "build(m3.1): regenerate IGA + cross-domain reports with agentic area"
  ```

---

## Final verification

- [ ] `python3 -m pytest tests/ -q` → all pass (incl. `test_agentic_area.py` + the UC-coverage guard).
- [ ] `validate_data` ×3 exit 0 (agentic controls registered/reused, semantics, citations resolve, evidence packs bind, currency).
- [ ] `grep -c "Agentic governance" matrix/domains/iga/iga-report.html` ≥ 1 (new posture area renders).
- [ ] `research/agentic/AGENTIC-RESEARCH.md` ledger shows 0 fabricated, refuted claims dropped.
- [ ] Clean rebuild → `git diff --exit-code` clean.
- [ ] Finish the branch with `superpowers:finishing-a-development-branch`.

---

## Self-review notes (author)

- **Spec coverage:** foundation research + sub-tree (Task 1) ✓; 3 IGA UCs (Task 2) ✓; reg-trace WS3-verified, reused controls (Task 3) ✓; evidence items (Task 3) ✓; archetype map + rubric/questionnaire (Task 5) ✓; new "Agentic governance" area (Task 4) ✓; govern existing IGID-012/013, no new identities / no spine change (Tasks 2-3, explicit) ✓; gates + byte-identity (Task 6) ✓.
- **No-fabrication discipline:** the plan does NOT pre-write external quotes — reg-trace REUSES already-verified control quotes (copy from existing rows) and Task 1 specifies the fetch-and-verify procedure for genuinely new sources. UC stories/acceptance are our own authored content (not external claims), so they are written in full here.
- **Type/seam consistency:** `_IGA_POSTURE_AREAS` is defined in Task 4 and asserted in the same task's tests; `IGA_AREAS` left untouched (vendor-fit unaffected). Archetype ids A2/A5/A3 match the analogous existing UCs (001→A2, 005/007→A5, 011→A3). Controls AC-2/AC-6/LLM06:2025/CPS234-§14/§21 confirmed already registered.
- **Confirmed:** IGA `regulatory-trace.csv` already binds `evidence_item_ids` (existing row uses `EV-IGA-JOINER-LOG;EV-IGA-LEAVER-SLA-REPORT`), so Task 3 Step 2's evidence binding is correct.
- **Confirm-at-execution:** the exact `emit_rubric.py` / `build_questionnaire.py` invocation (Task 5 Step 4) — match the WS2/H6 regeneration commands if flags differ.

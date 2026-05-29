# WS-1 Assessment Rubric (Archetype Library) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author a reusable, archetype-based posture-scoring rubric (8 archetypes + bespoke fallback) and a validation harness that enforces full coverage of all 48 use-cases, then dogfood it against the existing XYZ assessment.

**Architecture:** Five data/doc artifacts in a new `methodology/` Library-layer directory, guarded by a Python validator (`methodology/validate_rubric.py`) built test-first with pytest. The validator enforces structural invariants (schema, coverage, slot-fill, no-ANZ). A final dogfood task re-scores all 48 UCs through the rubric and compares to the frozen baseline.

**Tech Stack:** Python 3 stdlib (`csv`, `re`, `pathlib`), pytest for tests. No changes to `build_matrix_viewer.py` (that is WS-2).

**Spec:** `docs/superpowers/specs/2026-05-29-assessment-rubric-design.md`

---

## File Structure

- Create: `methodology/assessment-archetypes.csv` — A0–A8, state definitions with `{slots}`.
- Create: `methodology/archetype-questions.csv` — diagnostic question templates per archetype.
- Create: `methodology/uc-archetype-map.csv` — all 48 UCs → archetype + params.
- Create: `methodology/bespoke-criteria.csv` — A0 long-tail criteria.
- Create: `methodology/RUBRIC.md` — canonical prose for the rules.
- Create: `methodology/posture-rescore.csv` — dogfood output (client-generic naming).
- Create: `methodology/validate_rubric.py` — validation harness.
- Create: `methodology/compare_dogfood.py` — baseline comparison report.
- Create: `tests/test_rubric.py` — pytest tests for the validator.
- Create: `requirements-dev.txt` — pins pytest.
- Create: `PRD/adrs/ADR-008-assessment-rubric.md` — the ADR.

**Naming constraint (spec B3):** no new `anz`/`ANZ` token in any created file. The frozen
`matrix/anz-current-state.csv` is read-only input to the dogfood only.

---

## Task 1: Scaffold + CSV loader + no-ANZ guard

**Files:**
- Create: `requirements-dev.txt`
- Create: `methodology/validate_rubric.py`
- Create: `tests/test_rubric.py`
- Create: `methodology/assessment-archetypes.csv` (header-only stub)

- [ ] **Step 1: Create the dev dependency file**

`requirements-dev.txt`:
```
pytest==8.3.3
```

- [ ] **Step 2: Write the failing test**

`tests/test_rubric.py`:
```python
from pathlib import Path
import methodology.validate_rubric as vr

ROOT = Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"

def test_load_csv_reads_header_and_rows(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("a,b\n1,2\n", encoding="utf-8")
    rows = vr.load_csv(f)
    assert rows == [{"a": "1", "b": "2"}]

def test_no_anz_passes_clean_text(tmp_path):
    f = tmp_path / "clean.csv"
    f.write_text("uc_id,note\nUC-F-001,client-generic\n", encoding="utf-8")
    assert vr.check_no_anz([f]) == []

def test_no_anz_flags_anz_token(tmp_path):
    f = tmp_path / "dirty.csv"
    f.write_text("uc_id,note\nUC-F-001,anz_state here\n", encoding="utf-8")
    assert f.name in " ".join(vr.check_no_anz([f]))
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'methodology.validate_rubric'`

- [ ] **Step 4: Create package markers + minimal implementation**

Create empty `methodology/__init__.py` and empty `tests/__init__.py`.

`methodology/validate_rubric.py`:
```python
"""Validation harness for the WS-1 assessment rubric (archetype library)."""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
ANZ_RE = re.compile(r"anz", re.IGNORECASE)


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_no_anz(paths):
    """Return a list of human-readable violations (empty = clean)."""
    violations = []
    for p in paths:
        text = Path(p).read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if ANZ_RE.search(line):
                violations.append(f"{Path(p).name}:{i}: contains 'anz' token")
    return violations
```

- [ ] **Step 5: Create the archetypes header-only stub**

`methodology/assessment-archetypes.csv`:
```
archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (3 passed)

- [ ] **Step 7: Commit**

```bash
git add requirements-dev.txt methodology/ tests/
git commit -m "feat(methodology): scaffold rubric validator + no-ANZ guard"
```

---

## Task 2: Author the 8 archetypes + A0, validate schema

**Files:**
- Modify: `methodology/assessment-archetypes.csv`
- Modify: `methodology/validate_rubric.py`
- Modify: `tests/test_rubric.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
REQUIRED_ARCH_COLS = {
    "archetype_id", "name", "intent", "met_def",
    "partial_def", "gap_def", "na_def", "evidence_expectation",
}
EXPECTED_IDS = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"}

def test_archetypes_have_all_ids_and_filled_cells():
    rows = vr.load_csv(METH / "assessment-archetypes.csv")
    ids = {r["archetype_id"] for r in rows}
    assert ids == EXPECTED_IDS
    errors = vr.validate_archetypes(rows)
    assert errors == [], errors

def test_archetypes_file_has_no_anz():
    assert vr.check_no_anz([METH / "assessment-archetypes.csv"]) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_archetypes_have_all_ids_and_filled_cells -v`
Expected: FAIL — `AttributeError: module ... has no attribute 'validate_archetypes'`

- [ ] **Step 3: Add the validator function**

Append to `methodology/validate_rubric.py`:
```python
REQUIRED_ARCH_COLS = (
    "archetype_id", "name", "intent", "met_def",
    "partial_def", "gap_def", "na_def", "evidence_expectation",
)


def validate_archetypes(rows):
    errors = []
    seen = set()
    for r in rows:
        aid = r.get("archetype_id", "")
        if aid in seen:
            errors.append(f"duplicate archetype_id {aid}")
        seen.add(aid)
        # A0 carries definitions per-UC in bespoke-criteria.csv; only id/name/intent required.
        cols = ("archetype_id", "name", "intent") if aid == "A0" else REQUIRED_ARCH_COLS
        for c in cols:
            if not (r.get(c) or "").strip():
                errors.append(f"{aid}: empty required column '{c}'")
    return errors
```

- [ ] **Step 4: Author the archetype data**

Replace `methodology/assessment-archetypes.csv` with (quote every field containing commas):
```
archetype_id,name,intent,met_def,partial_def,gap_def,na_def,evidence_expectation
A0,Bespoke,"Long-tail use-case that does not fit a reusable pattern; criteria authored per-UC.","See bespoke-criteria.csv for this uc_id.","See bespoke-criteria.csv for this uc_id.","See bespoke-criteria.csv for this uc_id.","Capability not in client scope.","Per the uc_id row(s) in bespoke-criteria.csv."
A1,Preventive Guardrail,"A control enforced at a gate that blocks a bad action for {nhi_population}.","{control} enforced in blocking mode across {scope}; bypasses require a registered exception with owner+expiry; violations alerted.","{control} deployed in detect/monitor mode or over partial {scope}; enforcement not blocking everywhere; exceptions ad hoc.","{control} not deployed or trivially bypassed; no meaningful coverage.","{control}/{nhi_population} not applicable to client scope.","Gate/policy config showing blocking mode plus the covered {scope} list."
A2,Population Migration / Coverage,"Share of an identity population {nhi_population} moved from {legacy_pattern} to {target_pattern}.","{target_pattern} is the enforced default for new {nhi_population} AND >= {threshold} of existing population migrated AND legacy inventory with active burn-down AND exceptions registered with owner+expiry.","{target_pattern} available and used for some {nhi_population}; no complete inventory or burn-down; exceptions ad hoc.","{target_pattern} not in use; {nhi_population} remains on {legacy_pattern}; no inventory.","{nhi_population} does not exist in client scope.","Migration metric (% on {target_pattern}) plus legacy burn-down inventory."
A3,Capability Adoption,"{capability} is deployed AND adopted to depth for {nhi_population} meeting {config_target}.","{capability} in production AND adopted by >= {threshold} of {nhi_population} AND configuration meets {config_target}.","{capability} available but adoption is low (shelf-ware) OR configuration below {config_target}.","{capability} not available or not used for {nhi_population}.","{capability}/{nhi_population} not applicable to client scope.","Adoption metric plus a configuration sample evidencing {config_target}."
A4,Lifecycle Automation,"Issuance, rotation and revocation of {credential_type} automated within {sla} for {nhi_population}.","Full lifecycle (issue+rotate+revoke) automated for {nhi_population} within {sla}; failures alerted on-call.","Some lifecycle phases automated (e.g. rotation but not revocation) or partial {nhi_population}; manual steps remain.","Lifecycle is manual or managed out-of-band for {credential_type}.","{credential_type}/{nhi_population} not applicable to client scope.","Pipeline/runbook plus an SLA-attainment metric for {credential_type}."
A5,Inventory & Attestation,"A complete owner-attested register of {nhi_population} re-attested every {cadence} and exported to {system}.","Register covers >= {threshold} of {nhi_population}; entries owner-attested; re-attested every {cadence}; exported to {system}.","Partial inventory; attestation ad hoc or stale; no export to {system}.","No inventory of {nhi_population} exists.","{nhi_population} not applicable to client scope.","The register plus attestation records and an export to {system}."
A6,Telemetry / KPI,"{metric} published every {cadence} with drill-down by {dimension} and freshness <= {freshness}.","{metric} published every {cadence}; drill-down by {dimension}; freshness <= {freshness}; reviewed at {forum}.","{metric} exists but cadence is irregular, lacks drill-down, or is stale beyond {freshness}.","{metric} is not produced.","{metric} not applicable to client scope.","The dashboard/report instance plus evidence of {cadence} and {freshness}."
A7,Governance Process & Register,"A documented {process} whose entries carry owner+expiry and auto-escalate.","{process} documented and operating; every entry has owner+expiry; expired entries auto-escalate; reviewed every {cadence}.","{process} exists but entries lack owner/expiry or escalation is manual.","No {process} or register exists.","{process} not applicable to client scope.","A register sample plus evidence of an escalation having fired."
A8,Periodic Assurance Artifact,"A {artifact} assembled every {cadence} with sign-off covering {scope}.","{artifact} assembled every {cadence}; signed and timestamped; covers {scope}; generated within {sla}.","{artifact} produced ad hoc or with incomplete {scope}; no formal sign-off.","{artifact} is not produced.","{artifact} not applicable to client scope.","An artifact instance plus its sign-off/timestamp record."
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (all)

- [ ] **Step 6: Commit**

```bash
git add methodology/assessment-archetypes.csv methodology/validate_rubric.py tests/test_rubric.py
git commit -m "feat(methodology): author 8 archetypes + A0 with schema validation"
```

---

## Task 3: Author diagnostic questions + validate

**Files:**
- Create: `methodology/archetype-questions.csv`
- Modify: `methodology/validate_rubric.py`
- Modify: `tests/test_rubric.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
ALLOWED_BOUNDARY = {"GAP_PARTIAL", "PARTIAL_MET"}

def test_questions_valid_and_cover_each_non_a0_archetype():
    archs = vr.load_csv(METH / "assessment-archetypes.csv")
    qs = vr.load_csv(METH / "archetype-questions.csv")
    errors = vr.validate_questions(archs, qs)
    assert errors == [], errors

def test_questions_file_has_no_anz():
    assert vr.check_no_anz([METH / "archetype-questions.csv"]) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_questions_valid_and_cover_each_non_a0_archetype -v`
Expected: FAIL — `AttributeError: ... 'validate_questions'`

- [ ] **Step 3: Add the validator function**

Append to `methodology/validate_rubric.py`:
```python
ALLOWED_BOUNDARY = {"GAP_PARTIAL", "PARTIAL_MET"}


def validate_questions(archetype_rows, question_rows):
    errors = []
    arch_ids = {r["archetype_id"] for r in archetype_rows}
    non_a0 = arch_ids - {"A0"}
    covered = set()
    for q in question_rows:
        aid = q.get("archetype_id", "")
        if aid not in arch_ids:
            errors.append(f"question {q.get('q_id')}: unknown archetype_id {aid}")
        covered.add(aid)
        for c in ("q_id", "question_template", "dimension", "informs_state"):
            if not (q.get(c) or "").strip():
                errors.append(f"question {q.get('q_id')}: empty '{c}'")
        if q.get("informs_state") not in ALLOWED_BOUNDARY:
            errors.append(
                f"question {q.get('q_id')}: informs_state must be one of {ALLOWED_BOUNDARY}"
            )
    for aid in sorted(non_a0 - covered):
        errors.append(f"archetype {aid}: has no diagnostic questions")
    return errors
```

- [ ] **Step 4: Author the questions data**

`methodology/archetype-questions.csv` (one+ question per non-A0 archetype; `informs_state` is the
state boundary the answer discriminates):
```
archetype_id,q_id,question_template,dimension,informs_state
A1,A1-Q1,"Is {control} deployed at all relevant gates for {nhi_population}?",coverage,GAP_PARTIAL
A1,A1-Q2,"Is {control} enforced in blocking mode (not detect-only) across {scope}?",enforcement,PARTIAL_MET
A1,A1-Q3,"Are bypasses controlled by a registered exception with owner and expiry?",exception,PARTIAL_MET
A2,A2-Q1,"Is {target_pattern} the enforced default for new {nhi_population}?",enforcement,GAP_PARTIAL
A2,A2-Q2,"What share of existing {nhi_population} has migrated off {legacy_pattern}?",coverage,PARTIAL_MET
A2,A2-Q3,"Is there an inventory plus active burn-down for the legacy remainder?",governance,PARTIAL_MET
A2,A2-Q4,"Are exceptions registered with owner and expiry?",exception,PARTIAL_MET
A3,A3-Q1,"Is {capability} available in production for {nhi_population}?",coverage,GAP_PARTIAL
A3,A3-Q2,"What share of {nhi_population} actually uses {capability} (vs shelf-ware)?",depth,PARTIAL_MET
A3,A3-Q3,"Does the configuration meet {config_target}?",depth,PARTIAL_MET
A4,A4-Q1,"Is any lifecycle phase for {credential_type} automated?",coverage,GAP_PARTIAL
A4,A4-Q2,"Are issuance, rotation AND revocation all automated within {sla}?",depth,PARTIAL_MET
A4,A4-Q3,"Are automation failures alerted to on-call?",enforcement,PARTIAL_MET
A5,A5-Q1,"Does a register of {nhi_population} exist?",coverage,GAP_PARTIAL
A5,A5-Q2,"Does it cover >= {threshold} of {nhi_population} with owner attestation?",depth,PARTIAL_MET
A5,A5-Q3,"Is it re-attested every {cadence} and exported to {system}?",cadence,PARTIAL_MET
A6,A6-Q1,"Is {metric} produced at all?",coverage,GAP_PARTIAL
A6,A6-Q2,"Is it published every {cadence} with drill-down by {dimension}?",cadence,PARTIAL_MET
A6,A6-Q3,"Is data freshness within {freshness}?",depth,PARTIAL_MET
A7,A7-Q1,"Is {process} documented and operating?",coverage,GAP_PARTIAL
A7,A7-Q2,"Does every entry carry owner and expiry?",governance,PARTIAL_MET
A7,A7-Q3,"Do expired entries auto-escalate?",enforcement,PARTIAL_MET
A8,A8-Q1,"Is {artifact} produced at all?",coverage,GAP_PARTIAL
A8,A8-Q2,"Is it assembled every {cadence} covering {scope} with sign-off?",cadence,PARTIAL_MET
A8,A8-Q3,"Is it generated within {sla}?",depth,PARTIAL_MET
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (all)

- [ ] **Step 6: Commit**

```bash
git add methodology/archetype-questions.csv methodology/validate_rubric.py tests/test_rubric.py
git commit -m "feat(methodology): author archetype diagnostic questions + validation"
```

---

## Task 4: Map all 48 use-cases + validate coverage and slot-fill

**Files:**
- Create: `methodology/uc-archetype-map.csv`
- Modify: `methodology/validate_rubric.py`
- Modify: `tests/test_rubric.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
USE_CASES = ROOT / "matrix" / "use-cases.csv"

def test_every_uc_is_mapped_with_valid_archetype_and_slots():
    ucs = vr.load_csv(USE_CASES)
    archs = vr.load_csv(METH / "assessment-archetypes.csv")
    qs = vr.load_csv(METH / "archetype-questions.csv")
    mapping = vr.load_csv(METH / "uc-archetype-map.csv")
    errors = vr.validate_mapping(ucs, archs, qs, mapping)
    assert errors == [], errors

def test_mapping_file_has_no_anz():
    assert vr.check_no_anz([METH / "uc-archetype-map.csv"]) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_every_uc_is_mapped_with_valid_archetype_and_slots -v`
Expected: FAIL — `AttributeError: ... 'validate_mapping'`

- [ ] **Step 3: Add the validator function**

Append to `methodology/validate_rubric.py`:
```python
SLOT_RE = re.compile(r"\{([a-zA-Z_]+)\}")


def _slots_for_archetype(aid, archetype_rows, question_rows):
    """All {slot} names referenced by an archetype's defs + its questions."""
    slots = set()
    for r in archetype_rows:
        if r["archetype_id"] == aid:
            for col in ("met_def", "partial_def", "gap_def", "na_def", "intent"):
                slots |= set(SLOT_RE.findall(r.get(col, "")))
    for q in question_rows:
        if q["archetype_id"] == aid:
            slots |= set(SLOT_RE.findall(q.get("question_template", "")))
    return slots


def _parse_params(raw):
    out = {}
    for pair in (raw or "").split(";"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            return None  # malformed
        k, v = pair.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def validate_mapping(use_case_rows, archetype_rows, question_rows, mapping_rows):
    errors = []
    arch_ids = {r["archetype_id"] for r in archetype_rows}
    uc_ids = {r["uc_id"] for r in use_case_rows}
    mapped = set()
    used_archetypes = set()
    for m in mapping_rows:
        uc = m.get("uc_id", "")
        aid = m.get("archetype_id", "")
        if uc not in uc_ids:
            errors.append(f"mapping: unknown uc_id {uc}")
        if aid not in arch_ids:
            errors.append(f"mapping {uc}: unknown archetype_id {aid}")
            continue
        mapped.add(uc)
        used_archetypes.add(aid)
        if aid == "A0":
            continue  # slots not required; criteria live in bespoke-criteria.csv
        params = _parse_params(m.get("params", ""))
        if params is None:
            errors.append(f"mapping {uc}: malformed params (need key=value;key=value)")
            continue
        needed = _slots_for_archetype(aid, archetype_rows, question_rows)
        missing = needed - set(params)
        if missing:
            errors.append(f"mapping {uc} ({aid}): params missing slots {sorted(missing)}")
    for uc in sorted(uc_ids - mapped):
        errors.append(f"use-case {uc}: not mapped to any archetype")
    for aid in sorted((arch_ids - {"A0"}) - used_archetypes):
        errors.append(f"archetype {aid}: never used by any UC (dead archetype)")
    return errors
```

- [ ] **Step 4: Author the mapping data**

Read `matrix/use-cases.csv`. For each of the 48 `uc_id`s, choose the archetype whose intent best
matches the UC's `acceptance_criteria`, then fill EVERY slot that archetype requires (see
`_slots_for_archetype` — e.g. A2 needs `nhi_population, legacy_pattern, target_pattern, threshold`).
Derive slot values from the UC's `story` + `acceptance_criteria` + `nhis_in_scope`. Use the seed
table below for the first rows and the same procedure for the remainder; the test in Step 5 fails
until all 48 are present with every slot filled.

`methodology/uc-archetype-map.csv` (header + worked rows shown; complete all 48):
```
uc_id,archetype_id,params,notes
UC-F-001,A1,"control=secret push-protection;nhi_population=repo-committed secrets;scope=all source repos",Prevent plaintext secrets in repos
UC-F-002,A2,"nhi_population=historical repo/CI secrets;legacy_pattern=unscanned history;target_pattern=full-history scanning+rotation;threshold=all branches quarterly",Detect/remediate secrets in history
UC-F-003,A2,"nhi_population=cloud IAM pipeline credentials;legacy_pattern=static cloud access keys;target_pattern=OIDC federation (sub/aud-scoped);threshold=95%",JIT cloud creds via OIDC
UC-F-004,A3,"capability=SPIFFE/SPIRE attested workload identity;nhi_population=production workloads;config_target=SVID TTL<=1h with auto-rotation;threshold=in-scope workloads",Workload-attested ephemeral identity
UC-F-005,A3,"capability=dynamic database credentials (broker leases);nhi_population=in-scope DB engines;config_target=per-data-class max TTL;threshold=in-scope DB estate",Dynamic DB credentials
UC-F-006,A4,"credential_type=long-lived static secrets;nhi_population=rotatable secret buckets;sla=policy interval (>95% in-window); failures alert <15m",Automated rotation
UC-F-007,A4,"credential_type=any NHI active credentials/sessions;nhi_population=in-scope NHIs;sla=revoke<1m via SOAR; introspection<5m",Immediate revocation
UC-N-001,A6,"metric=plaintext-secret sprawl (total/P0/MTTR);cadence=weekly;dimension=team/repo/NHI bucket;freshness=24h;forum=remediation review",Sprawl KPI dashboard
UC-N-002,A5,"nhi_population=all in-scope NHI buckets;threshold=95%;cadence=annual;system=GRC",NHI inventory + attestation
UC-F-017,A0,,TEE attestation-gated release — bespoke (see bespoke-criteria.csv)
UC-F-026,A0,,Vault-internal identity hardening — bespoke (see bespoke-criteria.csv)
```

Mapping guidance for the remaining UCs (apply the same archetype-intent match):
- Gate/block controls (deny plaintext, deny insecure default) → **A1**.
- "% of a population on a better pattern / migrate off legacy" → **A2** (UC-F-013, F-019, F-023).
- "capability exists and must be adopted to depth / TTL" → **A3** (UC-F-008, F-009, F-010, F-012, F-014).
- "issue/rotate/revoke automated" → **A4** (UC-F-016, F-020, F-021, F-024).
- "complete attested register / inventory / cleanup sweep" → **A5** (UC-F-027, N-010).
- "a KPI/metric published at cadence" → **A6** (UC-N-003, N-016, N-019, N-020).
- "a documented governance process/register with owner+expiry" → **A7** (UC-N-006, N-007, N-009, N-011, N-014, N-015).
- "a periodic scorecard/evidence-pack/report with sign-off" → **A8** (UC-N-004, N-005, N-012, N-013, N-017, N-018).
- UC-F-011, F-015, F-018, F-022, F-025, N-008 → choose by closest acceptance_criteria match; if a UC
  genuinely fits none, assign **A0** and add it to `bespoke-criteria.csv` in Task 5.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS — failures name the exact UC and missing slots until all 48 are mapped and filled.

- [ ] **Step 6: Commit**

```bash
git add methodology/uc-archetype-map.csv methodology/validate_rubric.py tests/test_rubric.py
git commit -m "feat(methodology): map all 48 use-cases to archetypes with slot-fill validation"
```

---

## Task 5: Author A0 bespoke criteria + validate

**Files:**
- Create: `methodology/bespoke-criteria.csv`
- Modify: `methodology/validate_rubric.py`
- Modify: `tests/test_rubric.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
def test_every_a0_uc_has_bespoke_criteria_and_vice_versa():
    mapping = vr.load_csv(METH / "uc-archetype-map.csv")
    bespoke = vr.load_csv(METH / "bespoke-criteria.csv")
    errors = vr.validate_bespoke(mapping, bespoke)
    assert errors == [], errors

def test_bespoke_file_has_no_anz():
    assert vr.check_no_anz([METH / "bespoke-criteria.csv"]) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_every_a0_uc_has_bespoke_criteria_and_vice_versa -v`
Expected: FAIL — `AttributeError: ... 'validate_bespoke'`

- [ ] **Step 3: Add the validator function**

Append to `methodology/validate_rubric.py`:
```python
def validate_bespoke(mapping_rows, bespoke_rows):
    errors = []
    a0_ucs = {m["uc_id"] for m in mapping_rows if m.get("archetype_id") == "A0"}
    bespoke_ucs = {b["uc_id"] for b in bespoke_rows}
    for uc in sorted(a0_ucs - bespoke_ucs):
        errors.append(f"A0 use-case {uc}: no bespoke criteria authored")
    for uc in sorted(bespoke_ucs - a0_ucs):
        errors.append(f"bespoke criteria for {uc}: but {uc} is not mapped to A0")
    for b in bespoke_rows:
        for c in ("uc_id", "sub_id", "sub_criterion", "question", "evidence"):
            if not (b.get(c) or "").strip():
                errors.append(f"bespoke {b.get('uc_id')}/{b.get('sub_id')}: empty '{c}'")
    return errors
```

- [ ] **Step 4: Author the bespoke data**

For every UC assigned A0 in Task 4, decompose its `acceptance_criteria` into 2–4 atomic sub-criteria.
Worked example for the two seed A0 UCs:

`methodology/bespoke-criteria.csv`:
```
uc_id,sub_id,sub_criterion,question,evidence
UC-F-017,UC-F-017.1,Attestation-gated release is documented for a regulated workload class,"Is high-value secret release gated on TEE attestation for any workload class?",Broker policy + attestation flow doc
UC-F-017.2,UC-F-017.2,The broker supports at least one TEE attestation flow,"Does the secrets broker support a TEE attestation flow (Nitro/MAA/Confidential Space)?",Broker config evidencing a TEE flow
UC-F-017.3,UC-F-017.3,A pilot exists for a regulated workload and revocation/stale-quote handling is defined,"Is there a live pilot, and does policy handle revocation and stale quotes?",Pilot record + revocation policy
UC-F-026,UC-F-026.1,The secrets manager root is sealed offline (Shamir/KMS unseal),"Is the vault root token sealed offline via Shamir or KMS auto-unseal?",Seal config
UC-F-026,UC-F-026.2,Replication tokens are rotated and scoped,"Are replication tokens rotated and least-scoped?",Replication token policy
UC-F-026,UC-F-026.3,Auto-unseal KMS keys are governed as strictly as customer keys,"Are auto-unseal KMS keys under the same controls as customer keys?",KMS key policy
```

> NOTE: if Task 4 assigned additional UCs to A0, add their rows here too — the test fails until every
> A0 UC has criteria and no orphan bespoke rows exist.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (all)

- [ ] **Step 6: Commit**

```bash
git add methodology/bespoke-criteria.csv methodology/validate_rubric.py tests/test_rubric.py
git commit -m "feat(methodology): author A0 bespoke criteria + validation"
```

---

## Task 6: Wire the CLI entrypoint + author RUBRIC.md and ADR-008

**Files:**
- Modify: `methodology/validate_rubric.py`
- Modify: `tests/test_rubric.py`
- Create: `methodology/RUBRIC.md`
- Create: `PRD/adrs/ADR-008-assessment-rubric.md`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
def test_run_all_returns_no_errors_on_real_data():
    errors = vr.run_all()
    assert errors == [], errors
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_run_all_returns_no_errors_on_real_data -v`
Expected: FAIL — `AttributeError: ... 'run_all'`

- [ ] **Step 3: Add the orchestrator + CLI**

Append to `methodology/validate_rubric.py`:
```python
def run_all():
    archs = load_csv(METH / "assessment-archetypes.csv")
    qs = load_csv(METH / "archetype-questions.csv")
    mapping = load_csv(METH / "uc-archetype-map.csv")
    bespoke = load_csv(METH / "bespoke-criteria.csv")
    ucs = load_csv(ROOT / "matrix" / "use-cases.csv")
    files = [
        METH / "assessment-archetypes.csv",
        METH / "archetype-questions.csv",
        METH / "uc-archetype-map.csv",
        METH / "bespoke-criteria.csv",
    ]
    errors = []
    errors += validate_archetypes(archs)
    errors += validate_questions(archs, qs)
    errors += validate_mapping(ucs, archs, qs, mapping)
    errors += validate_bespoke(mapping, bespoke)
    errors += check_no_anz(files)
    return errors


if __name__ == "__main__":
    problems = run_all()
    if problems:
        print("RUBRIC VALIDATION FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Rubric validation passed.")
```

- [ ] **Step 4: Run tests + the CLI to verify they pass**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (all)
Run: `python3 methodology/validate_rubric.py`
Expected: `Rubric validation passed.`

- [ ] **Step 5: Author RUBRIC.md**

`methodology/RUBRIC.md` — document, in prose: the archetype model; the 9 archetypes with their
state definitions; the state-derivation rule (questions → dimensions → state per archetype def);
the confidence rule (HIGH/MEDIUM/LOW, PENDING-as-state) verbatim from spec §5.2; the override
protocol (`proposed_state`/`final_state`/`override_reason`, required when differing) from spec §5.3;
and a "how to add a new client/industry/framework" section (reuse archetypes; only the
`uc-archetype-map.csv` params and the in-scope UC set change). Cross-reference ADR-008.

- [ ] **Step 6: Author ADR-008**

`PRD/adrs/ADR-008-assessment-rubric.md` — Status: Accepted; Date: 2026-05-29. Follow the existing
ADR format (Context / Decision / Consequences / Alternatives considered / References). Decision =
adopt the archetype library + A0 fallback as the posture-scoring methodology, building on ADR-006's
vocabulary and ADR-007's confidence posture. Alternatives = derive-then-refine per-UC (rejected:
48 islands, no reuse) and bespoke-per-UC (rejected: two sources of truth vs acceptance_criteria).
Reference `methodology/RUBRIC.md` and `docs/superpowers/specs/2026-05-29-assessment-rubric-design.md`.

- [ ] **Step 7: Commit**

```bash
git add methodology/validate_rubric.py tests/test_rubric.py methodology/RUBRIC.md PRD/adrs/ADR-008-assessment-rubric.md
git commit -m "feat(methodology): add validator CLI, RUBRIC.md rules doc, and ADR-008"
```

---

## Task 7: Dogfood re-score + baseline comparison

**Files:**
- Create: `methodology/posture-rescore.csv`
- Create: `methodology/compare_dogfood.py`
- Modify: `tests/test_rubric.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_rubric.py`:
```python
def test_rescore_covers_all_ucs_and_no_anz():
    ucs = vr.load_csv(USE_CASES)
    rescore = vr.load_csv(METH / "posture-rescore.csv")
    rescored_ids = {r["uc_id"] for r in rescore}
    assert rescored_ids == {u["uc_id"] for u in ucs}
    for r in rescore:
        assert r["proposed_state"] in {"MET", "PARTIAL", "GAP", "N/A", "PENDING"}, r
    assert vr.check_no_anz([METH / "posture-rescore.csv"]) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_rubric.py::test_rescore_covers_all_ucs_and_no_anz -v`
Expected: FAIL — file `methodology/posture-rescore.csv` does not exist.

- [ ] **Step 3: Produce the dogfood re-score**

For each of the 48 UCs: apply its mapped archetype's diagnostic questions against the evidence in
`research/anz-current-state-evidence.md` + `task0/responses.md`, derive `proposed_state` per the
archetype's state definition, set `confidence` per the rule, and write the row. This is the manual
application that proves the rubric is mechanisable. Columns are client-generic (no `anz`).

`methodology/posture-rescore.csv` (header + first rows; complete all 48):
```
uc_id,archetype_id,proposed_state,confidence,override_reason,notes
UC-F-001,A1,GAP,HIGH,,Push-protection not enforced estate-wide; 2019 finding open
UC-F-003,A2,PARTIAL,HIGH,,OIDC for AWS only; Azure/GCP not covered
UC-F-005,A3,PARTIAL,HIGH,,Dynamic DB engine enabled but adoption ~zero (shelf-ware)
```

- [ ] **Step 4: Write the comparison script**

`methodology/compare_dogfood.py`:
```python
"""Compare the rubric dogfood re-score against the frozen baseline verdicts."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]


def _load(path, key, val):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r[key]: r[val] for r in csv.DictReader(fh)}


def main():
    proposed = _load(ROOT / "methodology" / "posture-rescore.csv", "uc_id", "proposed_state")
    baseline = _load(ROOT / "matrix" / "anz-current-state.csv", "uc_id", "anz_state")
    matches, diffs = 0, []
    for uc, base in baseline.items():
        prop = proposed.get(uc, "MISSING")
        if prop == base:
            matches += 1
        else:
            diffs.append((uc, base, prop))
    total = len(baseline)
    print(f"Reproduction: {matches}/{total} = {matches/total:.0%}")
    print("Divergences (uc_id: baseline -> proposed):")
    for uc, base, prop in sorted(diffs):
        print(f"  {uc}: {base} -> {prop}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the comparison + the full suite**

Run: `python3 -m pytest tests/test_rubric.py -v`
Expected: PASS (all)
Run: `python3 methodology/compare_dogfood.py`
Expected: prints reproduction rate + a divergence list. Review each divergence: either tighten the
mapping/params (rubric refinement) or record it in the `notes`/`override_reason` column as a
legitimately-better verdict. Re-run until every divergence is explained.

- [ ] **Step 6: Commit**

```bash
git add methodology/posture-rescore.csv methodology/compare_dogfood.py tests/test_rubric.py
git commit -m "feat(methodology): dogfood re-score all 48 UCs + baseline comparison"
```

---

## Self-Review (completed by author)

**Spec coverage:** §3 archetype model → Tasks 2,3; §4 data model (5 files) → Tasks 2–6; §5 rules
(state/confidence/override) → RUBRIC.md in Task 6; §6 validation (dogfood + coverage checks) →
Tasks 4,7; §7 scope (no engine/instrument changes) → respected (no `build_matrix_viewer.py` edits);
B3 no-ANZ → enforced by `check_no_anz` in every task. ADR-008 (§4) → Task 6.

**Placeholder scan:** Tasks 4, 5, 7 require the engineer to complete the full 48-row / all-A0 /
all-48-rescore data sets; this is irreducible content work, but it is bounded by a deterministic
procedure AND a failing test that names the exact missing item — not an open-ended "TBD." All code
steps contain complete, runnable code.

**Type/name consistency:** `load_csv`, `check_no_anz`, `validate_archetypes`, `validate_questions`,
`validate_mapping`, `validate_bespoke`, `run_all` are defined once and referenced consistently;
column names (`archetype_id`, `proposed_state`, `informs_state`, `params`) match across data files,
validators, and tests.

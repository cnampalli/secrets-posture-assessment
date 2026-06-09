# IGA Scoping Spike Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an isolated, ILLUSTRATIVE `spikes/iga/` slice that validates the hybrid IGA model — proving the questionnaire/archetype engine expresses IGA process-maturity use cases with zero engine changes, and documenting where the vendor capability-matrix engine does *not* fit — ending in a `SPIKE-FINDINGS.md` verdict for full Phase 3.

**Architecture:** New files only, all under `spikes/iga/` (mirrors `spikes/pam/`) plus one pytest guard. Reuses the existing domain-aware `questionnaire/rubric_loader.py` + `build_questionnaire.py` unchanged. Nothing in `matrix/`, `questionnaire/`, or `app/` is modified.

**Tech Stack:** Python 3, the existing rubric loader + archetype library (`methodology/archetype-questions.csv`, `assessment-archetypes.csv`). Run from repo root.

**Spec:** `docs/superpowers/specs/2026-06-09-iga-scoping-spike-design.md`

**Key constraints carried from the spec:**
- All data is ILLUSTRATIVE (banner in every authored file). Not a vendor assessment, not citation-backed.
- No production domain registration, no `matrix/` changes, no React-app changes, no new report renderer.
- `rubric_loader` reads exactly `use-cases.csv` + `uc-archetype-map.csv` from the data dir — use those names.

**Archetype slot reference** (slots each archetype's questions require — every one MUST be present in `params`, else the loader raises):
- A1: `control`, `nhi_population`, `scope`
- A2: `target_pattern`, `nhi_population`, `legacy_pattern`
- A3: `capability`, `nhi_population`, `config_target`
- A5: `nhi_population`, `threshold`, `cadence`, `system`
- A7: `process`
- A8: `artifact`, `cadence`, `scope`, `sla`

(`params` use `;` as separator and `key=value`; values must not contain `;`. `cadence` values omit a leading article — house style renders `every {cadence}`.)

---

### Task 1: Illustrative IGA rubric data + pytest guard

**Files:**
- Create: `spikes/iga/use-cases.csv`
- Create: `spikes/iga/uc-archetype-map.csv`
- Test: `tests/test_iga_spike.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_iga_spike.py`:

```python
import pathlib
import questionnaire.rubric_loader as rl

ROOT = pathlib.Path(__file__).resolve().parents[1]
METH = ROOT / "methodology"
SPIKE = ROOT / "spikes" / "iga"

UCS = rl.load_rubric(METH, data_dir=SPIKE)
BY_ID = {u["uc_id"]: u for u in UCS}


def test_all_11_iga_use_cases_resolve():
    assert {u["uc_id"] for u in UCS} == {f"UC-I-{i:03d}" for i in range(1, 12)}


def test_every_iga_uc_is_a_ladder_with_questions():
    for uc in UCS:
        assert uc["kind"] == "ladder", f"{uc['uc_id']} is not a ladder"
        assert uc["questions"], f"{uc['uc_id']} has no questions"


def test_no_unfilled_slots_in_iga_questions():
    for uc in UCS:
        for q in uc["questions"]:
            assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled: {q['text']}"


def test_archetype_spread_exercises_the_governance_library():
    # the spike must prove A1/A2/A3/A5/A7/A8 all express IGA use cases
    used = {u["archetype"] for u in UCS}
    assert {"A1", "A2", "A3", "A5", "A7", "A8"} <= used


def test_category_mapping():
    assert BY_ID["UC-I-008"]["category"] == "Non-functional"   # detective analytics
    assert BY_ID["UC-I-001"]["category"] == "Functional"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_iga_spike.py -q`
Expected: FAIL/ERROR — `spikes/iga/` and its CSVs don't exist (the module-level `load_rubric` raises on the missing dir/files).

- [ ] **Step 3: Create `spikes/iga/use-cases.csv`**

`rubric_loader` only needs `uc_id` + `category`; `short_title`/`area` are included for readability and the vendor-fit join.

```csv
uc_id,category,short_title,area
UC-I-001,FUNCTIONAL,Automated joiner / birthright provisioning,JML
UC-I-002,FUNCTIONAL,Mover access recalculation on transfer,JML
UC-I-003,FUNCTIONAL,Timely leaver de-provisioning,JML
UC-I-004,FUNCTIONAL,Periodic access certification campaigns,Certification
UC-I-005,FUNCTIONAL,High-risk access certification sign-off,Certification
UC-I-006,FUNCTIONAL,Preventive SoD checks at request time,SoD
UC-I-007,FUNCTIONAL,SoD policy register & violation management,SoD
UC-I-008,NON_FUNCTIONAL,Detective SoD scanning of existing access,SoD
UC-I-009,FUNCTIONAL,Role mining & RBAC baseline,Role/Request
UC-I-010,FUNCTIONAL,Self-service access request & approval,Role/Request
UC-I-011,FUNCTIONAL,Least-privilege entitlement right-sizing,Role/Request
```

- [ ] **Step 4: Create `spikes/iga/uc-archetype-map.csv`**

Every row's `params` fills exactly the slots its archetype's questions reference (see the slot reference above). `notes` is the rendered title.

```csv
uc_id,archetype_id,params,notes
UC-I-001,A2,"target_pattern=automated birthright and role-based provisioning;nhi_population=workforce joiners;legacy_pattern=manual ticket-based account creation;threshold=the bulk of joiner provisioning",Automated joiner / birthright provisioning
UC-I-002,A7,"process=the mover access-recalculation process for workforce transfers",Mover access recalculation on transfer
UC-I-003,A2,"target_pattern=automated de-provisioning within SLA on termination;nhi_population=workforce leavers;legacy_pattern=manual and delayed account disablement;threshold=the bulk of leaver events",Timely leaver de-provisioning
UC-I-004,A5,"nhi_population=in-scope workforce entitlements;threshold=95%;cadence=quarterly certification campaign;system=the IGA certification module",Periodic access certification campaigns
UC-I-005,A8,"artifact=a high-risk access certification sign-off;cadence=quarterly cycle;scope=privileged and high-risk entitlements;sla=the agreed campaign-close window",High-risk access certification sign-off
UC-I-006,A1,"control=preventive segregation-of-duties checks at access-request time;nhi_population=all access requests;scope=all in-scope applications with defined SoD rules",Preventive SoD checks at request time
UC-I-007,A7,"process=the segregation-of-duties policy and violation-management process",SoD policy register & violation management
UC-I-008,A3,"capability=detective SoD violation scanning of existing access;nhi_population=in-scope workforce entitlements;config_target=toxic combinations detected and routed to remediation with mitigating-control tracking",Detective SoD scanning of existing access
UC-I-009,A3,"capability=role mining and RBAC role engineering;nhi_population=in-scope workforce populations;config_target=a maintained role model covering the bulk of access with periodic role review",Role mining & RBAC baseline
UC-I-010,A7,"process=the self-service access request and approval workflow",Self-service access request & approval
UC-I-011,A2,"target_pattern=right-sized least-privilege entitlements;nhi_population=in-scope workforce identities;legacy_pattern=accumulated over-provisioned access from role changes;threshold=the bulk of identified excess entitlements",Least-privilege entitlement right-sizing
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest tests/test_iga_spike.py -q`
Expected: PASS (5 tests). If any question shows a leftover `{slot}`, a `params` value is missing that slot — fix the offending row.

- [ ] **Step 6: Sanity-check rendered questions read cleanly**

Run:
```bash
cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -c "
import questionnaire.rubric_loader as rl
for u in rl.load_rubric('methodology', data_dir='spikes/iga'):
    print(u['uc_id'], u['archetype'], '|', u['questions'][0]['text'])
"
```
Expected: each first-question line reads as grammatical English (no `{}`; no `every a ...`). If a `cadence`/`threshold` reads awkwardly, adjust the value (house style: bare noun phrases).

- [ ] **Step 7: Commit**

```bash
git add spikes/iga/use-cases.csv spikes/iga/uc-archetype-map.csv tests/test_iga_spike.py
git commit -m "spike(iga): illustrative IGA rubric data + archetype-resolve guard

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Vendor-fit overlay + spike runner + questionnaire build

**Files:**
- Create: `spikes/iga/iga-vendor-fit.csv`
- Create: `spikes/iga/run_iga_spike.py`
- Generated: `spikes/iga/iga-questionnaire.html`

- [ ] **Step 1: Create the illustrative vendor-fit overlay `spikes/iga/iga-vendor-fit.csv`**

Coarse per-area fit (`supports` / `partial` / `add-on`). **Illustrative placeholders — not a vendor assessment.**

```csv
vendor,area,fit
SailPoint,JML,supports
SailPoint,Certification,supports
SailPoint,SoD,supports
SailPoint,Role/Request,supports
Saviynt,JML,supports
Saviynt,Certification,supports
Saviynt,SoD,supports
Saviynt,Role/Request,supports
Microsoft Entra ID Governance,JML,supports
Microsoft Entra ID Governance,Certification,supports
Microsoft Entra ID Governance,SoD,partial
Microsoft Entra ID Governance,Role/Request,supports
Okta Identity Governance,JML,partial
Okta Identity Governance,Certification,supports
Okta Identity Governance,SoD,add-on
Okta Identity Governance,Role/Request,supports
```

- [ ] **Step 2: Create the spike runner `spikes/iga/run_iga_spike.py`**

```python
#!/usr/bin/env python3
"""Phase 3 — IGA scoping spike.

HYPOTHESES:
  A) The domain-agnostic questionnaire engine (questionnaire.rubric_loader + the
     archetype library) expresses IGA *process-maturity* use cases with ZERO engine
     changes — only new data.
  B) The vendor capability-matrix engine wants fine-grained per-UC NATIVE/ADD-ON
     coverage; the hybrid model's *light* per-area vendor-fit overlay does not map 1:1.
     That mismatch is the finding, not a bug.

Run: python3 spikes/iga/run_iga_spike.py
NOTE: spikes/iga/*.csv are ILLUSTRATIVE (spike only) — not a verified IGA assessment.
"""
import csv
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from questionnaire import rubric_loader  # noqa: E402

METH = os.path.join(ROOT, "methodology")
AREAS = ["JML", "Certification", "SoD", "Role/Request"]


def banner():
    print("=" * 72)
    print("IGA SCOPING SPIKE — ILLUSTRATIVE DATA ONLY (not a vendor assessment)")
    print("=" * 72)


def probe_a():
    """Questionnaire/archetype reuse — must run clean."""
    print("\n[Probe A] questionnaire/archetype reuse")
    ucs = rubric_loader.load_rubric(METH, data_dir=HERE)
    assert len(ucs) == 11, f"expected 11 IGA use cases, got {len(ucs)}"
    for uc in ucs:
        assert uc["kind"] == "ladder", f"{uc['uc_id']} not a ladder"
        for q in uc["questions"]:
            assert "{" not in q["text"], f"{uc['uc_id']} {q['qid']} unfilled slot"
    spread = sorted({u["archetype"] for u in ucs})
    print(f"  ✓ {len(ucs)} IGA use cases resolved; archetypes exercised: {spread}")
    print("  ✓ no engine changes required — rubric_loader is domain-agnostic")
    return ucs


def probe_b():
    """Vendor overlay vs the capability-matrix engine — record the seam."""
    print("\n[Probe B] light vendor-fit overlay vs capability-matrix engine")
    rows = list(csv.DictReader(open(os.path.join(HERE, "iga-vendor-fit.csv"), encoding="utf-8")))
    by_vendor = defaultdict(dict)
    for r in rows:
        by_vendor[r["vendor"]][r["area"]] = r["fit"]
    print(f"  overlay shape: {len(by_vendor)} vendors x {len(AREAS)} process areas (coarse fit)")
    for v, areas in by_vendor.items():
        print(f"    {v}: " + ", ".join(f"{a}={areas.get(a, '-')}" for a in AREAS))
    # The matrix engine (report_logic.build_vendormix) expects per-USE-CASE vendor rows
    # with NATIVE/ADD-ON coverage + an identity-catalog, scored against a current-state.
    # This overlay is per-AREA and coarse by design (the suites mostly 'support' everything;
    # IGA's differentiator is process maturity, captured by Probe A — not capability presence).
    print("  ⚠ SEAM: capability-matrix wants per-UC NATIVE/ADD-ON + identity-catalog;")
    print("    the hybrid overlay is per-area + coarse and does NOT map 1:1.")
    print("    → full Phase 3 needs a dedicated lightweight IGA vendor-fit view (recorded in findings).")


if __name__ == "__main__":
    banner()
    probe_a()
    probe_b()
    print("\nDONE — see spikes/iga/SPIKE-FINDINGS.md for the verdict.")
```

- [ ] **Step 3: Run the spike runner**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 spikes/iga/run_iga_spike.py`
Expected: banner prints; Probe A prints "11 IGA use cases resolved" + the archetype spread `['A1','A2','A3','A5','A7','A8']`; Probe B prints the overlay table + the SEAM note; exits 0.

- [ ] **Step 4: Build the IGA questionnaire (existing tool, unchanged)**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 questionnaire/build_questionnaire.py --data-dir spikes/iga --out spikes/iga/iga-questionnaire.html`
Expected: `Wrote .../spikes/iga/iga-questionnaire.html (... bytes; 11 use cases)`.

- [ ] **Step 5: Confirm no raw slots leaked into the built HTML**

Run: `grep -oE '\{[a-z_]+\}' spikes/iga/iga-questionnaire.html | sort -u | head` 
Expected: no output (no unresolved `{slot}` tokens).

- [ ] **Step 6: Commit**

```bash
git add spikes/iga/iga-vendor-fit.csv spikes/iga/run_iga_spike.py spikes/iga/iga-questionnaire.html
git commit -m "spike(iga): vendor-fit overlay + runner; build IGA questionnaire (11 UCs)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Findings doc + roadmap update

**Files:**
- Create: `spikes/iga/SPIKE-FINDINGS.md`
- Modify: `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`

- [ ] **Step 1: Write `spikes/iga/SPIKE-FINDINGS.md` from the ACTUAL runner output**

Run `python3 spikes/iga/run_iga_spike.py` again and write the findings reflecting what it actually printed (do not invent results). Use this structure (mirrors `spikes/pam/SPIKE-FINDINGS.md`):

```markdown
# Phase 3 — IGA scoping spike: findings

_ILLUSTRATIVE spike. Data in `spikes/iga/` is placeholder, not a verified IGA/vendor assessment._

## Hypotheses
A) The questionnaire/archetype engine expresses IGA process-maturity use cases with no engine changes.
B) The capability-matrix engine does not fit a light per-area vendor-fit overlay (IGA is process-shaped).

## Method
- Authored 11 illustrative IGA use cases (`use-cases.csv` + `uc-archetype-map.csv`) across JML,
  Certification, SoD, and Role/Request, mapped to archetypes A1/A2/A3/A5/A7/A8.
- Probe A: loaded them through the unchanged `questionnaire.rubric_loader`; built `iga-questionnaire.html`.
- Probe B: shaped a coarse per-area vendor-fit overlay (`iga-vendor-fit.csv`) toward the capability-matrix engine.

## Result: ✅ HYBRID MODEL HOLDS
- Probe A: all 11 UCs resolved as ladder questions; archetypes exercised = [A1, A2, A3, A5, A7, A8];
  questionnaire built with 11 use cases; zero engine changes. The governance archetypes (A5/A7/A8)
  fit IGA process maturity especially cleanly (certification → A5, SoD/JML/request governance → A7,
  high-risk cert sign-off → A8).
- Probe B: the per-area coarse overlay does NOT map 1:1 onto the capability matrix (which wants
  per-UC NATIVE/ADD-ON + identity-catalog scored against current-state). Confirmed the predicted seam.

## What reuses cleanly
- `questionnaire/rubric_loader.py`, `build_questionnaire.py`, the archetype library — unchanged.
- The process-maturity instrument is fully functional for IGA today.

## What needs a new view (full Phase 3 build)
- A dedicated **lightweight IGA vendor-fit view** (per-area / per-process support), separate from the
  NATIVE/ADD-ON capability matrix used by Secrets/PAM.
- Citation-backed replacement of all illustrative data (use cases, regulatory trace, vendor fit).
- Production domain registration + React-app wiring (deferred).

## Verdict & recommendation
Green-light full Phase 3 on the hybrid model: reuse the questionnaire/archetype engine as-is for the
process-maturity core; build a small bespoke vendor-fit renderer rather than forcing IGA into the
capability matrix. Sequence: data research → questionnaire (works now) → vendor-fit view → cross-domain.

## Status
Spike complete; illustrative artifacts in `spikes/iga/`. No production code touched.
```
Adjust any bullet that doesn't match the actual runner output.

- [ ] **Step 2: Update the roadmap status board + Phase 3 note**

In `docs/superpowers/MULTI-DOMAIN-ROADMAP.md`, change the Phase 3 status-board row from `⬜ — **unblocked**` to note the spike outcome, e.g.:
`🟦 SCOPING DONE — IGA scoping spike validates the hybrid model (process-maturity reuses the engine; needs a bespoke light vendor-fit view). See spikes/iga/SPIKE-FINDINGS.md. Next: full Phase 3 (citation-backed data + vendor-fit view).`
Add a one-line pointer under the roadmap's deferred/follow-ups area if appropriate. Keep edits minimal and factual.

- [ ] **Step 3: Full regression (nothing production changed)**

Run: `cd /Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers && python3 -m pytest -q`
Expected: all pass (prior 234 + 5 new IGA spike tests = 239).

- [ ] **Step 4: Commit**

```bash
git add spikes/iga/SPIKE-FINDINGS.md docs/superpowers/MULTI-DOMAIN-ROADMAP.md
git commit -m "spike(iga): findings (hybrid model holds) + roadmap Phase 3 scoping note

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Notes for the executor
- Run all commands from the repo root: `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/research-papers`.
- Use native Write tools for files; do not edit anything under `matrix/`, `questionnaire/`, or `app/`.
- Every authored file is ILLUSTRATIVE — keep the banner/labelling honest; do not present the vendor-fit values as real.
- The findings doc must reflect the ACTUAL runner output, not the template's assumed results.

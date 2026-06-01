# WS-5 Slice 1 — Cleanup + CSV Schema Validation (Design Spec)

**Status:** Approved (brainstorming, 2026-06-01)
**Workstream:** WS-5 — codebase hygiene (opportunistic enabler). Slice 1 of an agreed sequence.
**Agreed WS-5 sequence:** **5a cleanup → 5c validation** (this slice) → 5b legacy `anz` rename → 5d monolith split.

---

## 1. Goal

Two hygiene wins in one slice:
- **5a:** remove a stale file and archive research checkpoints (low-risk warm-up).
- **5c:** add the project's first **CSV schema validator** — required columns, structural checks, value enums, and cross-file referential integrity over the core data contracts + all vendor CSVs. Currently there are **zero** data guards.

## 2. Locked decisions (brainstorming, 2026-06-01)

| # | Decision |
|---|----------|
| 1 | Slice = 5a cleanup + 5c validation. Excludes the `anz` rename (5b) and monolith split (5d). |
| 2 | Coverage: **core 4 + all 19 vendor CSVs + the aggregate** `vendor-capabilities.csv`. |
| 3 | Integration: **standalone `matrix/validate_data.py` (CLI + importable) + pytest.** NOT wired into builds (keeps builds byte-stable, no new failure modes). |
| 4 | `RUBRIC.md` `override_reason`→`rationale` already done (WS-4 slice 2) — not in scope. |
| 5 | `matrix/` stays a non-package; the validator is a self-contained stdlib script; tests load it via a `sys.path` insert + run the CLI via `subprocess` (the `test_report_adapter` pattern). No `matrix/__init__.py` added (avoids any risk to the byte-stable build). |

## 3. Part 5a — Cleanup

- `git rm GEMINI.md` (stale; superseded).
- Move the **12** `research/vendors/_checkpoint-*.md` files into `research/vendors/_archive/` (move, not delete — research provenance). Use `git mv`.
- No other files touched.

## 4. Part 5c — `matrix/validate_data.py`

Read-only validator, mirrors `methodology/validate_rubric.py`:
- `load_csv(path) -> list[dict]` (DictReader).
- `REQUIRED_COLS` — dict: contract file → required-column tuple.
- Per-check **pure functions** taking loaded row-lists → returning **lists of violation strings** (empty = clean). They **collect, never raise** on data problems.
- `validate_all(root) -> list[str]` — runs every check, concatenates violations.
- **CLI** (`python3 matrix/validate_data.py [--root .]`): prints each violation + a summary; exits **1** if any, else **0**.

### 4.1 Required columns (verified headers)
- `use-cases.csv`: uc_id, category, short_title, story, acceptance_criteria, nhis_in_scope, outcome_lens, backmap_codes, priority_fi, citation_keys
- `anz-current-state.csv`: uc_id, anz_state, confidence, evidence_q_ids, evidence_redacted, gap_notes, sensitivity_tag, citation_keys
- `regulatory-trace.csv`: framework_slug, framework_role, control_code, control_short_title, uc_ids, nhi_ids, maturity_level, evidence_url, evidence_quote, citation_keys
- `identity-catalog.csv`: nhi_id, bucket, short_name, description, typical_secrets, lifecycle, governance_maturity, sources_at_anz_likely, citation_keys
- `vendor-capabilities.csv` + 19 `vendor-capabilities-*.csv`: vendor_slug, vendor_name, target_id, target_type, coverage, maturity, evidence_url, evidence_quote, citation_keys, notes

### 4.2 Structural
- Each contract file non-empty.
- `uc_id` unique in use-cases; `nhi_id` unique in identity-catalog; `uc_id` unique in current-state.
- use-cases and current-state have the **same `uc_id` set**.

### 4.3 Value enums (high-confidence only, to avoid false positives)
- `anz_state ∈ {MET, PARTIAL, GAP, PENDING, NA}` (real data uses GAP/PARTIAL/PENDING — superset is fine)
- `framework_role ∈ {PRIMARY-LENS, BACK-MAP, ADVERSARY-LENS}`
- vendor `maturity` parses as an integer in **0–5** (real data ranges 0–4)
- vendor `coverage` is **non-empty** (real values: NATIVE/PARTNER/ADD-ON/GAP/N-A — no hardcoded enum, deferred)

### 4.3.1 Intentional sentinels (allowlisted, NOT violations)
`regulatory-trace.csv` deliberately uses `MISSING-UC` / `MISSING-NHI` as "no known mapping"
placeholders (3 rows: E8-MAC, E8-RAP-NHI-GAP, ISM-0039). The referential checks **skip** these
two sentinel tokens — they are documented markers, not dangling refs. `SENTINELS = {"MISSING-UC",
"MISSING-NHI"}`.

### 4.4 Referential integrity (the high-value class)
- `current-state.uc_id` ⊆ `use-cases.uc_id`
- `regulatory-trace.uc_ids` (`;`-split, ignoring blanks **and sentinels**) ⊆ `use-cases.uc_id`
- `regulatory-trace.nhi_ids` (`;`-split, ignoring sentinels) ⊆ `identity-catalog.nhi_id`
- `use-cases.nhis_in_scope` (`;`-split) ⊆ `identity-catalog.nhi_id`
- vendor `target_id`: rows with `target_type == "NHI"` ⊆ identity-catalog `nhi_id`; rows with `target_type` starting `"UC"` (real values `UC-F`/`UC-N`) ⊆ use-cases `uc_id`; other target_types ignored
- each per-vendor `vendor-capabilities-<slug>.csv`: a single consistent `vendor_slug`; same `target_id` integrity as the aggregate

**Note:** if `validate_all` against the real data surfaces genuine violations, that is a real data-quality finding — record it in the slice report; fix only obvious typos, otherwise flag for the user. (Goal: the real data should validate clean and become the golden baseline.)

## 5. Testing / verification

- **Unit (pytest, in-memory fixtures):** every check fed a clean fixture (→ no violations) and a deliberately-broken one (→ the exact expected violation). Covers required-columns, the three uniqueness checks, same-uc-set, each enum, and each referential link.
- **Integration:** `validate_all(REPO_ROOT)` against the real data returns **zero violations** (data certified as the golden baseline).
- **CLI:** exit 0 on clean data; on a broken tmp copy, exit 1 + the violation printed.
- **5a:** `GEMINI.md` absent; the 12 checkpoints relocated under `research/vendors/_archive/`; nothing else moved.
- Full suite stays green (90 + new validator tests).

## 6. Scope boundaries

**In scope:** `matrix/validate_data.py`, `tests/test_validate_data.py`, the 5a file moves, ADR-015, backlog update.
**Out of scope:** the `anz` rename (5b — including the `anz_state` column, `anz-current-state.csv`, `sources_at_anz_likely`); the monolith split (5d); wiring validation into the builds; vendor `coverage` enum strictness; aggregate-vs-per-vendor superset checks.

## 7. Artifacts produced

- `matrix/validate_data.py`
- `tests/test_validate_data.py`
- `research/vendors/_archive/` (12 relocated checkpoints); `GEMINI.md` removed
- `docs/adr/ADR-015-csv-validation.md`
- `meta/IMPROVEMENT-BACKLOG.md` (WS-5 slice 1 marked)

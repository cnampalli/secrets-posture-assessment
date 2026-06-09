# IGA domain build map (Phase 3) — code paths

Worktree: `/Users/cnampalli/Desktop/Projects/DE/AI-Reports/iga-phase3` (branch `feat/iga-domain-phase3`, anchor tag `pre-iga-phase3`).
Engine is fully decoupled: adding a domain = YAML + data CSVs + a few small edits. **No questionnaire/report engine logic changes** (domain passed as arg).

## Files to CREATE
- `matrix/config/domains/iga.yaml` — domain descriptor (mirror `pam.yaml`).
- `matrix/domains/iga/` CSVs: `use-cases.csv` (full 10-col schema), `uc-archetype-map.csv`, `identity-catalog.csv`, `regulatory-trace.csv`, `current-state.csv`, `evidence-catalog.csv`, and bespoke `iga-vendor-fit.csv`.
- `matrix/domains/iga/iga-report.html` — generated output.
- `app/src/data/rubric.iga.json` — **auto-generated** by `questionnaire/emit_rubric.py` (do NOT hand-write).

## Files to EDIT
- `matrix/domains.py:153` — `_DOMAIN_ORDER = ("secrets","pam")` → add `"iga"`.
- `questionnaire/emit_rubric.py:17-20` — add `{"id":"iga","data_dir": ROOT/matrix/domains/iga}` to DOMAINS list (ONLY after CSVs exist, else test_emit_rubric fails).
- `app/src/assessment/domains.ts` — add `'iga'` to `DomainId` union (line 5), import `rubric.iga.json`, add DOMAINS entry.
- `app/src/assessment/domains.test.ts:7,13-15` — expected id list + IGA rubric length.
- `tests/test_domain_yaml.py` (after line 60) — add `test_iga_round_trips_through_registry` + `test_iga_yaml_anchors_to_historical_values`.
- `tests/test_domains.py` — add IGA registry/field tests.
- `tests/test_iga_spike.py` — currently points at `spikes/iga/`; on production move, add/repoint a production test for `matrix/domains/iga/`.

## Key facts / gotchas
- `load_domains()` auto-discovers `config/domains/*.yaml`. **Merely creating iga.yaml adds DOMAINS["iga"] immediately** → any "build all domains" test will try to read `matrix/domains/iga/*.csv`. ⇒ CSVs must land WITH the yaml (data task before/with config).
- `Domain` dataclass (matrix/domains.py:30-104) REQUIRES field `vendor_capabilities` (a filename). IGA uses a bespoke per-area view, NOT the NATIVE/ADD-ON matrix. Plan: ship a valid `vendor-capabilities.csv` (header-only or minimal) to satisfy loader + gate the matrix region OFF for IGA + render bespoke view from `iga-vendor-fit.csv`.
- `test_domain_yaml` loads YAML only (does NOT open CSVs) — passes without data files.
- No Python descriptor object needed; YAML is source of truth (auto-discovered). Anchor test pins literal field values.

## Vendor-fit renderer seam
- `matrix/report_logic.py` `build_vendormix(...)` builds the NATIVE/ADD-ON matrix; called at `matrix/build_matrix_viewer.py:85-86`, injected as model key `"vendormix"` (line 101).
- Plan: add `build_iga_vendor_fit(...)` in report_logic.py; in build_matrix_viewer.py inject `model["igavfit"]` when `DOMAIN.slug=="iga"`; gate template regions via `_apply_region(template,"IGA_VENDOR_FIT",keep=DOMAIN.slug=="iga")` and turn the matrix region off for IGA in `matrix/report_render.py` (regions at lines 54-55) + `matrix/report-template.html`.

## Test/build commands (from worktree root)
- `pytest` (full), `pytest -k iga`.
- `python3 questionnaire/emit_rubric.py` → regenerates rubric.*.json.
- `python3 matrix/build_matrix_viewer.py --domain iga` → builds iga-report.html.
- `app/`: `npm test`, `npm run build`.

# M2 — Cross-domain identity spine: implementation plan

> Mirrors the approved plan-mode plan (`~/.claude/plans/csa-nhi-categories-focus-distributed-puzzle.md`).
> Spec: `docs/superpowers/specs/2026-06-14-m2-cross-domain-identity-spine-design.md`.

## Context

The IAM-specialist review's #1 structural ask: the same logical identity is modelled three times with no
linkage — secrets `NHI-*` (37), PAM `PID-*` (20), IGA `IGID-*` (13). M2 adds a **canonical identity spine**
(a registry of identity archetypes keyed once that every domain catalog maps onto) and surfaces it as an
"Identity spine" section in the cross-domain report. Foundation of the IAM → NHI → Agentic story (M3).

**Anchoring:** CSA NHI primary (governance) for NPE + IAM-governance citations (NIST AC / ISM / CPS 234)
for human classes; one **optional** `spiffe_ref` on genuine workload archetypes only. SPIFFE never required,
never the framing (its technical angle lives in the orthogonal `npe_conformance` field + M3).

## Decisions

| Decision | Choice |
|---|---|
| Spine shape | Anchored archetype registry (~10–15 archetypes, `identity_class` × `privileged`) |
| Anchoring | CSA NHI primary + governance citations for human; optional `spiffe_ref` on workload only |
| Agentic | Establish `agentic` class + tag existing EMERGING (IGID-012-class); no new agentic identities (M3) |
| Surfacing | "Identity spine" section in `cross-domain-report.html` (archetype × domain lens; `span≥2` highlighted) |
| `npe_conformance` | Untouched; add `spine_id`; non-identity rows → `NOT-AN-IDENTITY` sentinel, exempt |

## File structure

| File | Change | Responsibility |
|---|---|---|
| `matrix/config/identity-spine.yaml` | create | Archetype registry (class × privileged, `csa_nhi_anchor`, optional `spiffe_ref`, citations) |
| `matrix/domains/{secrets,pam,iga}/identity-catalog.csv` | modify | Append `spine_id` to all 70 rows (sentinel for non-identities) |
| `matrix/identity_spine.py` | create | Pure `load_spine(cfgdir)`, `build_spine_view(domains_identities, spine)`, lens map |
| `matrix/validate_data.py` | modify | `check_identity_spine_registry` + `check_identity_spine_mapping`; load yaml; wire into `validate_all` |
| `matrix/report_io.py` | modify | Carry `spine_id` through the `nhis` projection (line 87-88) |
| `matrix/build_cross_domain.py` | modify | Collect every domain's identities (incl. IGA, before the matrix-less skip); build + pass spine |
| `matrix/cross_render.py` | modify | `render(model, spine=None)` — substitute `/*__SPINE__*/{}` |
| `matrix/cross-domain-template.html` | modify | "Identity spine" section + token + JS renderer (parallel to `renderMap`) |
| `tests/test_identity_spine.py` | create | Loader + builder unit tests |
| `tests/test_validate_data_domains.py` | modify | Registry + mapping injection tests |

**Reused:** `validate_data.load_yaml`/`load_csv`/`validate_all(root, data_dir)` (checks RETURN violation
strings, empty = clean — they do NOT raise); `report_io.load_inputs` (`nhis`); `cross_render.render` token
pattern (`</`-escaped JSON); `domains.DOMAINS`; the parametrized domain-validation + mangle→assert injection
test pattern (`test_vendor_fit_unsourced_claim_rejected`).

## Tasks (TDD)

1. **Registry + loader + registry validation.** Author `identity-spine.yaml` (~10–15 archetypes, clustered
   from the 70 existing entries, anchored). `identity_spine.load_spine`. `check_identity_spine_registry`
   (dup id / bad enum / non-bool privileged / empty label|description|csa_nhi_anchor). Tests parse + bad-registry.
2. **`spine_id` mapping.** Append column to 3 catalogs (real → archetype, non-identity → `NOT-AN-IDENTITY`).
   `report_io` projection += `spine_id`. `check_identity_spine_mapping` (empty / unknown id). Wire both into
   `validate_all`. Tests: domain-zero-violations stays green ×3; injection (bogus `spine_id` → 1 violation).
3. **`build_spine_view`.** Pure model: archetypes with `by_domain` lens + `span`; `cross_domain` (span≥2);
   `classes` roll-up; `unmapped`; sentinel skipped. Lens map secrets/pam/iga. Tests for each.
4. **Render section.** `cross_render.render(model, spine=None)` + `/*__SPINE__*/{}`. Template "Identity spine"
   section (archetype × domain, lens headers, class/priv, span≥2 highlighted, honest caption). `build_cross_domain`
   collects all domains' identities before the matrix-less skip; loads spine; passes model. Test: section + a
   span≥2 archetype + IGA identity present. Regenerate `cross-domain-report.html`.
5. **Final verification.** `validate_data` ×3 clean; `pytest -q` green; rebuild → `git diff --exit-code` clean.
   No new CI wiring (gates inside `validate_data` ×3; section inside the byte-identity-gated cross-domain report).

## Verification

```bash
python3 matrix/validate_data.py && python3 matrix/validate_data.py --data-dir matrix/domains/iga && python3 matrix/validate_data.py --data-dir matrix/domains/pam
python3 -m pytest tests/ -q
python3 matrix/build_cross_domain.py && git diff --exit-code
grep -c "Identity spine" matrix/cross-domain-report.html   # >= 1
```

## Out of scope
React/`app/` (demand-pulled); new agentic UCs/identities (M3); instance-level keys (needs client data);
rewriting `npe_conformance`; co-equal SPIFFE anchoring.

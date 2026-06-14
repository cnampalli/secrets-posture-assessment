# M2 — Cross-domain identity spine (design)

**Date:** 2026-06-14
**Track:** M (market leadership) — item 2, per `docs/superpowers/plans/2026-06-11-a-plus-hardening.md`
**Status:** approved, ready for implementation plan

## Purpose

Close the IAM-specialist review's **#1 structural ask**: today the same logical identity
(e.g. a service account) is modelled three times with no linkage — secrets `NHI-*`, PAM
`PID-*`, IGA `IGID-*` — each in its own ID space. There is no single identity taxonomy and
no way to see one identity through every domain's lens. M2 introduces a **canonical identity
spine**: a registry of identity archetypes, keyed once, that every domain catalog maps onto.
This is also the technical foundation of the IAM → NHI → Agentic-AI story (M3 builds on it).

## Current state (verified)

Three siloed `identity-catalog.csv` files, **70 identities total**, identical schema, no linkage:

| Domain | Rows | ID prefix |
|---|---|---|
| secrets | 37 | `NHI-*` |
| pam | 20 | `PID-*` |
| iga | 13 | `IGID-*` |

Schema today: `nhi_id, bucket, short_name, description, typical_secrets, lifecycle,
governance_maturity, sources_likely, citation_keys, npe_conformance`.

`npe_conformance` is a **separate axis** (SPIFFE/NPE-conformance) with values incl.
`CONFORMANT`, `HUMAN-IDENTITY`, `NPE`, and non-identity markers `CREDENTIAL-NOT-IDENTITY`,
`CROSS-CUTTING-ATTRIBUTE`, `HUMAN-USE-ANTIPATTERN`. It is **not** a clean class×privileged
taxonomy and is left untouched by M2.

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|---|---|---|
| Spine shape | **Anchored archetype registry** (~10–15 named archetypes, class × privileged, CSA-NHI/SPIFFE-anchored) | Links precisely; builds on the repo's most valuable asset (the NHI taxonomy). |
| Agentic scope | **Establish the agentic class + tag existing EMERGING entries only** | Clean M2/M3 boundary; M3 authors new agentic identities/UCs. Spine is ready for M3 to populate. |
| Surfacing | **"Identity spine" section in the cross-domain report** | A cross-platform artifact belongs in the only-possible-on-one-platform view. |
| `npe_conformance` | **Keep as orthogonal axis; add `spine_id`; non-identity rows get a sentinel, exempt from mapping** | Don't rewrite a verified field; a credential isn't an identity. |

## Architecture

Follows the established `matrix/` separation: **config/data** + **pure model builder** +
**pure renderer (section)** + **validation gates**. Mirrors how the vendor cross-domain map
(`crossdomain.py` / `cross_render.py` / `build_cross_domain.py`) is structured.

### 1. Canonical registry (data)

- **`matrix/config/identity-spine.yaml`** — the archetype registry. Each archetype:
  ```yaml
  - spine_id: SPN-001
    label: Privileged human administrator
    identity_class: human          # human | npe | agentic
    privileged: true
    description: "<one line — what this archetype is>"
    anchor: "<CSA NHI category / SPIFFE concept it maps to>"
    citation_keys: "<bib key(s) anchoring the archetype; may be empty for self-evident classes>"
  ```
  ~10–15 entries spanning the three classes × privileged flag, sized to cover the 70
  existing identities. The concrete list is derived during execution from the existing
  catalogs and citation-anchored (see "Data authoring" below).

- **`spine_id` column** appended to all three `identity-catalog.csv` (70 rows). Each real
  identity references one archetype. Non-identity rows (`CREDENTIAL-NOT-IDENTITY`,
  `CROSS-CUTTING-ATTRIBUTE`, and any future non-identity marker) use the sentinel
  `NOT-AN-IDENTITY` and are exempt from archetype mapping.

### 2. Validation (`matrix/validate_data.py`, gated ×3 domains)

- **`check_identity_spine_registry(spine)`** — `spine_id` unique; `identity_class` in
  `{human, npe, agentic}`; `privileged` is a real bool; every archetype has a non-empty
  `label`, `description`, and `anchor`. Fail-closed on a malformed registry file.
- **`check_identity_spine_mapping(identity_rows, spine)`** — every catalog row has a
  non-empty `spine_id`; each value is either `NOT-AN-IDENTITY` or resolves to a registered
  archetype. Raises on an unmapped row or an unknown `spine_id`. Injection-tested (a bogus
  `spine_id` must fail the build).

Both wired into `validate_all` so they run in the existing CI `validate_data` ×3 step.

### 3. Model builder (pure, no I/O)

- **`matrix/identity_spine.py`**
  - `load_spine(cfgdir) -> spine` — reads `identity-spine.yaml`; returns a list of archetype
    dicts keyed by `spine_id`.
  - `build_spine_view(domains_identities, spine) -> model` — `domains_identities` is
    `[{slug, label, identities:[{spine_id, short_name, ...}]}]` for **all** domains (IGA
    included; identity catalogs exist for every domain, so the matrix-less vendor skip does
    NOT apply here). Returns:
    ```
    {
      archetypes: [
        { spine_id, label, identity_class, privileged, anchor,
          by_domain: { secrets: [short_name...], pam: [...], iga: [...] },
          span: <count of domains that map ≥1 identity to this archetype> }
      ],
      cross_domain: [ archetypes with span >= 2 ],   # the payoff
      classes: { human: n, npe: n, agentic: n },      # roll-up counts
      unmapped: [ ... ]                                # archetypes with span 0 (e.g. baseline agentic)
    }
    ```
  - Per-domain **lens** descriptor is a small constant map:
    `secrets = "credential issuance & rotation"`, `pam = "privileged session brokering"`,
    `iga = "lifecycle & certification"`. Surfaced so the matrix reads as "this identity, seen
    as X in secrets / Y in PAM / Z in IGA".

### 4. Render (section in the cross-domain report)

- `build_cross_domain.py` additionally: loads each domain's identity catalog (via
  `report_io.load_inputs`, which already returns `nhis` — the identity rows — but **needs the
  new `spine_id` field carried through**; see Data flow), `load_spine`, calls
  `build_spine_view`, and passes a `spine` model to `cross_render.render`.
- **`cross_render.py`** substitutes a new `/*__SPINE__*/{}` JSON payload token (same
  `</script>`-safe pattern as `/*__CROSSMAP__*/`).
- **`cross-domain-template.html`** gains an **"Identity spine"** section: a table of
  archetype × domain, cross-domain (`span ≥ 2`) rows visually highlighted, with class and
  privileged flag shown and the per-domain lens in the column headers. Honest caption: the
  spine is a designed taxonomy; archetype anchors are point-in-time.

### Data flow

```
identity-spine.yaml ─ identity_spine.load_spine ──────────────┐
matrix/domains/<slug>/identity-catalog.csv (incl. spine_id) ──┤
  via report_io.load_inputs -> nhis (spine_id carried)        ├─ identity_spine.build_spine_view
                                                              └─ cross_render.render (/*__SPINE__*/) ─ cross-domain-report.html

identity rows + spine ─ validate_data.check_identity_spine_{registry,mapping} ─ (CI gate ×3)
```

`report_io.load_inputs` currently projects `nhis` as
`{nhi_id, bucket, short_name, description}`. M2 adds `spine_id` to that projection so the
field reaches the builder. This is the one touch to existing I/O.

## Error handling / edge cases

- Catalog row missing `spine_id` → `check_identity_spine_mapping` raises (fail-closed).
- Unknown `spine_id` (typo / injection) → raises, names the offending row.
- `NOT-AN-IDENTITY` sentinel → row skipped in `build_spine_view` (never appears under an archetype).
- Archetype with `span 0` (e.g. a baseline agentic archetype no domain maps yet — though M2
  only tags existing, so expected `span 0` set is empty) → listed under `unmapped`, not an error.
- All domains have identity catalogs, so the spine view never silently drops a domain; a
  domain contributing zero mapped identities still appears (empty column), surfaced honestly.

## Testing (TDD)

- **`tests/test_identity_spine.py`** — `load_spine` parse; `build_spine_view` archetype
  grouping, `by_domain` lens population, `span` computation, `cross_domain` filter (span ≥ 2),
  class roll-up counts, sentinel exemption (NOT-AN-IDENTITY never appears), `unmapped` capture.
- **`tests/test_identity_spine_validate.py`** (or extend `test_validate_data_domains.py`) —
  every catalog row mapped; sentinel allowed; unknown `spine_id` raises (injection); registry
  enum/uniqueness/anchor-required raise on malformed input.
- **Render** — cross-domain report contains the "Identity spine" section; a cross-domain
  (span ≥ 2) archetype is present; IGA identities appear (proving IGA is included).

## CI / gates

No new CI wiring needed: `check_identity_spine_*` run inside `validate_data` (already gated
×3), and the "Identity spine" section ships inside `cross-domain-report.html` (already in the
byte-identity rebuild gate). The cross-domain report is regenerated and must stay
byte-identical to the committed artifact.

## Data authoring (execution note, not a placeholder)

The archetype set and the 70 per-row mappings are authored during execution:
1. Derive candidate archetypes by clustering the existing 70 `short_name`/`description`
   entries across domains (e.g. cloud-workload NPE, CI/CD NPE, privileged human admin,
   workforce human, agentic-AI agent).
2. Anchor each archetype to a CSA-NHI category or SPIFFE concept; cite where a real source
   exists, mark designed/illustrative where it doesn't (same honesty bar as prior phases).
3. Map every real identity to exactly one archetype; assign the sentinel to non-identity rows.
4. Tag existing EMERGING agentic entries (e.g. IGA `IGID-012`) to an agentic archetype; author
   no new agentic identities (M3).

## Out of scope (deliberate, YAGNI)

- React/`app/` changes (demand-pulled, as in M1).
- New agentic UCs or identities (M3).
- Instance-level identity keys (requires real client data).
- Rewriting / collapsing `npe_conformance` (kept as an orthogonal conformance axis).

## Acceptance

1. `identity-spine.yaml` exists with a class×privileged archetype registry, all archetypes
   anchored; registry validation passes.
2. All 70 identity-catalog rows carry a `spine_id`; real identities map to a registered
   archetype, non-identities to the sentinel; mapping validation passes ×3 domains.
3. The cross-domain report shows an "Identity spine" section with archetype × domain lenses
   and the cross-domain (span ≥ 2) identities highlighted; IGA is included.
4. All new tests pass; `validate_data` ×3 clean; cross-domain report rebuilds byte-identical.

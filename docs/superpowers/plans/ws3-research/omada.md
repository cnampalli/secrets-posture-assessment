# Omada Identity — IGA vendor-fit research (ws3)

Vendor: **Omada Identity** · slug `omada` · full-suite IGA (Omada Identity / Omada Identity Cloud).
All four areas graded honestly from first-party docs (documentation.omadaidentity.com + omadaidentity.com product pages). Quotes confirmed verbatim by live fetch.

---

## (1) Ready-to-paste fit rows (mirror existing CSV header exactly)

`vendor,vendor_slug,area,fit,justification,evidence_url,citation_keys`

```csv
Omada Identity,omada,JML,NATIVE,"First-party joiner-mover-leaver lifecycle drives onboard/change/offboard provisioning from authoritative sources; vendor docs: ""The processes under the Identity Lifecycle Management process area are known as the joiner-mover-leaver processes.""",https://omadaidentity.com/products/functionality/lifecycle-management/,omada-lifecycle-management
Omada Identity,omada,Certification,NATIVE,"Scheduled certification campaigns periodically re-validate access, policies, roles and master data; vendor docs: ""Certification campaigns (also known as review, attestation, and recertification) are used to periodically verify that access rights, policies, role definitions and Master Data in the system are valid.""",https://documentation.omadaidentity.com/docs/identityprocess/governance/,omada-certification-campaigns
Omada Identity,omada,SoD,NATIVE,"First-party SoD module defines toxic-combination policies and detects violations, with violation approval requiring a justification and a compensating control; vendor docs: ""The Segregation of Duties (SoD) module is used to define policies for toxic combinations of access rights.""",https://documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/,omada-sod-module;omada-sod-violation
Omada Identity,omada,Role/Request,NATIVE,"Role model assigns birthright/organizational/functional roles, with self-service access request layered on top and SoD policies checked at request time; vendor docs: ""Special entitlements and roles can also be added using the self-service access request process.""",https://documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/,omada-role-management;omada-access-request
```

---

## (2) iga.yaml lines

```yaml
vendor_layer:
  omada: ["L1", "suite"]

short:
  omada: "Omada"
```

**Layer rationale:** Omada Identity is a full-spectrum IGA platform (lifecycle, certification, SoD, role/request unified in one policy-driven framework) — identical footprint to SailPoint ISC / Saviynt EIC / Entra IDG / Okta OIG. It belongs in the single `L1`/`suite` class the descriptor defines for all IGA suites; no new layer required.

---

## (3) Verification ledger

| Area | Evidence URL | Verbatim Y/N | Source grade |
|---|---|---|---|
| JML | omadaidentity.com/products/functionality/lifecycle-management/ | Y — "...are known as the joiner-mover-leaver processes." | First-party product page (capability-presence, not efficacy) |
| Certification | documentation.omadaidentity.com/docs/identityprocess/governance/ | Y — full sentence confirmed verbatim | First-party technical documentation (strongest grade) |
| SoD | documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/ | Y — "The Segregation of Duties (SoD) module is used to define policies for toxic combinations of access rights." | First-party product walkthrough docs |
| Role/Request | documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/ | Y — "Special entitlements and roles can also be added using the self-service access request process." | First-party product walkthrough docs |

Supporting verbatim (also confirmed, used as secondary context, not the embedded quote):
- SoD violation handling (governance doc): "Manager gets a task to approve or resolve the violation. Approving a violation requires a justification and selection of a compensating control."
- Role/Request SoD-at-request (business-alignment page): "These policies are checked each time a user submits a self-service access request, or an automated assignment is made."

---

## (4) UNVERIFIED list

- `documentation.omadaidentity.com/docs/identityprocess/lifecyclemanagement/` returned HTTP 404 — the JML evidence URL therefore uses the product functionality page (omadaidentity.com/products/functionality/lifecycle-management/) whose verbatim quote IS confirmed. No quote is sourced from the dead doc URL.
- No efficacy/benchmark claims made — all four rows assert capability presence only, consistent with the existing CSV convention.
- Privileged-access / micro-recertification and request-time SoD-block granularity (UC-level depth) were NOT separately verified; the per-area NATIVE grade reflects area presence, not per-UC coverage (per the per-area, not per-UC, grid design).

---

## (5) Ownership verdict

**Independent.** Omada Identity is a standalone, IDP-agnostic IGA vendor (Omada A/S) — not an add-on to or reseller of another vendor's IGA engine. It operates its own lifecycle, certification, SoD and role/request engine (RoPE policy engine referenced in its governance docs) and connects to external IdPs/target systems rather than depending on one. Grading all four areas NATIVE is defensible: each capability is first-party and the embedded quotes are verbatim from Omada-owned domains.

---

## Adversarial verification (PASS 2)

Re-fetched 2026-06-11. Posture: REFUTE-by-default; a row survives only if its `evidence_url` re-fetches live AND the embedded verbatim quote appears as an exact contiguous substring.

| # | Area | evidence_url | Quote re-fetch | Verdict |
|---|------|--------------|----------------|---------|
| 1 | JML | omadaidentity.com/products/functionality/lifecycle-management/ | "The processes under the Identity Lifecycle Management process area are known as the joiner-mover-leaver processes." — exact | **CONFIRMED** |
| 2 | Certification | documentation.omadaidentity.com/docs/identityprocess/governance/ | "Certification campaigns (also known as review, attestation, and recertification) are used to periodically verify that access rights, policies, role definitions and Master Data in the system are valid." — exact | **CONFIRMED** |
| 3 | SoD | documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/ | Embedded quote is the leading clause of a longer live sentence; "The Segregation of Duties (SoD) module is used to define policies for toxic combinations of access rights" appears verbatim as a contiguous substring (full live sentence continues "…assigned to the same person, detect any violations…") | **CONFIRMED** |
| 4 | Role/Request | documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/ | "Special entitlements and roles can also be added using the self-service access request process." — exact | **CONFIRMED** |

**Schema sanity:** 7 cols present; fit = NATIVE×4 ∈ {NATIVE,PARTIAL,ADD-ON}; justification/url/keys non-empty. PASS.

**NATIVE-overclaim hunt:** All four NATIVE grades are supported by first-party Omada-domain documentation (capability-presence, not efficacy). SoD NATIVE is well-supported (dedicated first-party SoD module + violation-approval/compensating-control evidence). No overclaim found — Omada is the strongest of the four vendors.

### Final LANDABLE rows (unchanged — all CONFIRMED)
```csv
Omada Identity,omada,JML,NATIVE,"First-party joiner-mover-leaver lifecycle drives onboard/change/offboard provisioning from authoritative sources; vendor docs: ""The processes under the Identity Lifecycle Management process area are known as the joiner-mover-leaver processes.""",https://omadaidentity.com/products/functionality/lifecycle-management/,omada-lifecycle-management
Omada Identity,omada,Certification,NATIVE,"Scheduled certification campaigns periodically re-validate access, policies, roles and master data; vendor docs: ""Certification campaigns (also known as review, attestation, and recertification) are used to periodically verify that access rights, policies, role definitions and Master Data in the system are valid.""",https://documentation.omadaidentity.com/docs/identityprocess/governance/,omada-certification-campaigns
Omada Identity,omada,SoD,NATIVE,"First-party SoD module defines toxic-combination policies and detects violations, with violation approval requiring a justification and a compensating control; vendor docs: ""The Segregation of Duties (SoD) module is used to define policies for toxic combinations of access rights.""",https://documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/,omada-sod-module;omada-sod-violation
Omada Identity,omada,Role/Request,NATIVE,"Role model assigns birthright/organizational/functional roles, with self-service access request layered on top and SoD policies checked at request time; vendor docs: ""Special entitlements and roles can also be added using the self-service access request process.""",https://documentation.omadaidentity.com/productwalkthrough/IGA-scenarios/policy-and-role-management/,omada-role-management;omada-access-request
```

### Layer recommendation
`["L1","suite"]` — CORRECT and unchanged. iga.yaml (lines 8-10, 26-27) defines a single `suite` layer for all IGA platforms, fit assessed per governance AREA (not the L1/L2 model). Omada is a full-suite IGA, identical class to SailPoint/Saviynt/Entra/Okta. No new layer.

**Verdict counts:** CONFIRMED 4 · QUOTE-DRIFT 0 · UNREACHABLE 0 · REFUTED 0. Lands fully.

# Lumos — IGA vendor-fit research (ws3 vendor expansion)

**Vendor:** Lumos · slug `lumos` · modern IGA / app-governance platform ("Autonomous Identity Platform", Albus AI).
**Policy:** STRICT anti-fabrication. Every row carries a verbatim vendor-doc quote + evidence_url + citation_keys. All grades live-fetched 2026-06 against lumos.com.
**Net verdict on grades:** JML NATIVE · Certification NATIVE · SoD PARTIAL (honest — detective/AI-flagged, not a dedicated cross-app SoD policy engine) · Role/Request NATIVE.

---

## (1) Four ready-to-paste fit rows

Paste into `matrix/domains/iga/iga-vendor-fit.csv` (header: `vendor,vendor_slug,area,fit,justification,evidence_url,citation_keys`).

```
Lumos,lumos,JML,NATIVE,"Policy- and event-driven joiner/mover/leaver workflows provision and deprovision across IdP, SaaS, cloud and on-prem from a continuous HRIS sync; vendor copy: ""Reduce manual work with end-to-end workflows that provision and deprovision access across your stack."" (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.lumos.com/products/lifecycle-management,lumos-lifecycle
Lumos,lumos,Certification,NATIVE,"Automated user access review (UAR) campaigns with one-click approve/deny/delegate, full action logging and Albus AI recommendations; vendor copy: ""Reviewers can approve, deny, or delegate with one click, while Lumos logs all actions for compliance and future audits to save hours of manual work for IT and security teams."" (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.lumos.com/products/access-reviews,lumos-access-reviews
Lumos,lumos,SoD,PARTIAL,"SoD exists as AI-driven detective flagging inside reviews / the lifecycle (Albus surfaces risk-prone access combinations and SoD violations) rather than a dedicated first-party cross-app toxic-combination policy register with rule owners; vendor copy: ""Flag changes, anomalies, SoD violations, and privileged access."" Coverage is SaaS-first (300+ integrations) and will not satisfy ERP-grade fine-grained SoX/ERP SoD without a dedicated GRC capability. (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.lumos.com/products/access-reviews,lumos-sod;lumos-sod-topic
Lumos,lumos,Role/Request,NATIVE,"Self-service access requests via AppStore/Slack/Teams/CLI/ITSM with configurable requester/approver/duration and time-bound auto-revocation; vendor copy: ""define who can request, who approves, and how long access lasts."" (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.lumos.com/products/appstore,lumos-appstore
```

> Note: marketing-grade-source caveat mirrors the Saviynt rows (`saviynt-eic`) — lumos.com product pages are JS/marketing pages, not a server-renderable docs portal. The same honesty disclaimer is carried verbatim.

---

## (2) iga.yaml lines + layer rationale

Lumos is the **same vendor class** as ConductorOne (modern SaaS-first IGA / app-governance). Per `iga.yaml`, **all** IGA vendors share the single `["L1", "suite"]` layer — IGA fit is assessed per governance area, not per-product NATIVE/ADD-ON. Lumos follows that convention exactly (no new layer). Add:

```yaml
# vendor_layer: (add under existing entries)
  lumos: ["L1", "suite"]

# short: (add under existing entries)
  lumos: "Lumos"
```

**Layer rationale:** `L1 / suite` is correct and consistent. Lumos delivers all four governance areas as one platform (lifecycle, UAR, requests, SoD-flagging), so it belongs in the same L1 IGA-platforms band as SailPoint/Saviynt/Entra/Okta. The honest differentiator is *grade within areas* (SoD = PARTIAL, SaaS-first coverage), not a different layer. Whatever label ConductorOne-class vendors receive, Lumos must match it — do not invent a separate "modern/lightweight IGA" layer unless ConductorOne also gets one.

---

## (3) Verification ledger (live-fetched 2026-06)

| Area | URL | Verbatim evidence (Y = capability present) | Grade |
|------|-----|--------------------------------------------|-------|
| JML | https://www.lumos.com/products/lifecycle-management | Y — "Reduce manual work with end-to-end workflows that provision and deprovision access across your stack."; "Automate joiner, mover, leaver workflows."; "Unify lifecycle workflows with continuous HRIS sync." | NATIVE |
| Certification | https://www.lumos.com/products/access-reviews | Y — "Automate user access reviews."; "Reviewers can approve, deny, or delegate with one click, while Lumos logs all actions for compliance and future audits…" | NATIVE |
| SoD | https://www.lumos.com/products/access-reviews + https://www.lumos.com/topic/separation-of-duties-definition-best-practices | Partial-Y — "Flag changes, anomalies, SoD violations, and privileged access."; topic page: "Lumos embeds SoD controls directly into the identity lifecycle: enforcing least privilege"; "detecting entitlement conflicts in real time". No dedicated cross-app SoD policy-register/request-time engine evidenced; SaaS-first ("300+ integrations"). | PARTIAL |
| Role/Request | https://www.lumos.com/products/appstore | Y — "Self-service app requests in one place."; "define who can request, who approves, and how long access lasts."; "Lumos enforces time-bound approvals, tracks activity, and auto-revokes access after the set duration." | NATIVE |

Suggested `citation_keys` → URL bindings for the bib:
- `lumos-lifecycle` → https://www.lumos.com/products/lifecycle-management
- `lumos-access-reviews` → https://www.lumos.com/products/access-reviews
- `lumos-sod` → https://www.lumos.com/products/access-reviews (SoD-flag quote)
- `lumos-sod-topic` → https://www.lumos.com/topic/separation-of-duties-definition-best-practices
- `lumos-appstore` → https://www.lumos.com/products/appstore

---

## (4) UNVERIFIED list (claimed but NOT confirmed to fit-row evidentiary standard — do NOT cite as NATIVE)

- **Dedicated preventive request-time SoD engine.** Topic page says "Lumos doesn't just audit SoD conflicts; it prevents them" and "dynamic provisioning rules" — but no product-page evidence of a request-time toxic-combination *block* with a rule register + rule owners (the UC-I-008 / UC-I-009 standard). Treated as detective ⇒ SoD held at PARTIAL, not NATIVE. Do not upgrade without a verbatim request-time-block quote.
- **ERP-grade / fine-grained cross-app SoD (SoX/ERP).** No evidence; coverage is SaaS-first (300+ integrations). Out of scope.
- **Role mining / RBAC baseline (UC-I-011).** Not separately verified on a Lumos page; not claimed in any fit row.
- **Unstructured-data entitlement governance (UC-I-016).** Not verified; not claimed.
- **Agentic UAR efficacy ("6x faster", "industry-first").** Marketing/PR claim — recorded as presence framing only, never as an efficacy benchmark.
- **Docs portal (developers.lumos.com / docs.lumos.com / support.lumos.com).** Exist but not used for fit quotes; product marketing pages used instead (same as Saviynt precedent). If a stricter docs-grade source is later required, re-fetch these.

---

## (5) Ownership verdict

**OWN** — Lumos is a clean fit for the IGA instrument and I take ownership of these four rows. Three areas (JML, Certification, Role/Request) verify NATIVE on first-party product pages with verbatim quotes; SoD is honestly graded PARTIAL (AI-flagged/detective inside reviews and lifecycle, SaaS-first, no dedicated cross-app SoD policy engine — matching the realistic enterprise verdict applied to Okta OIG). Layer = `L1 / suite`, consistent with the ConductorOne-class convention; no new layer invented. No data files edited (per task). Ready to paste pending: (a) confirmation of the exact label ConductorOne receives, (b) bib entries for the five citation_keys, (c) validator run (`validate_data.py`) after the rows land.

---

## Adversarial verification (PASS 2)

Re-fetched 2026-06-11. Posture: REFUTE-by-default. Each row's embedded verbatim quote must appear as an exact contiguous substring on the live `evidence_url`.

| # | Area | evidence_url | Quote re-fetch | Verdict |
|---|------|--------------|----------------|---------|
| 1 | JML | https://www.lumos.com/products/lifecycle-management | "Reduce manual work with end-to-end workflows that provision and deprovision access across your stack." — exact | **CONFIRMED** |
| 2 | Certification | https://www.lumos.com/products/access-reviews | "Reviewers can approve, deny, or delegate with one click, while Lumos logs all actions for compliance and future audits to save hours of manual work for IT and security teams." — exact | **CONFIRMED** |
| 3 | SoD | https://www.lumos.com/products/access-reviews | "Flag changes, anomalies, SoD violations, and privileged access." — exact | **CONFIRMED** |
| 4 | Role/Request | https://www.lumos.com/products/appstore | "define who can request, who approves, and how long access lasts." — exact | **CONFIRMED** |

**Schema sanity:** 7 cols; fit = NATIVE/NATIVE/PARTIAL/NATIVE ∈ {NATIVE,PARTIAL,ADD-ON}; non-empty justification/url/keys. Note the SoD row carries two citation_keys (`lumos-sod;lumos-sod-topic`); the row's EMBEDDED verbatim ("Flag changes, anomalies, SoD violations, and privileged access.") is on the primary `evidence_url` (access-reviews) and CONFIRMED — the `-topic` page is supporting context only, not the embedded quote, so the row stands. PASS.

**SoD overclaim check (special scrutiny):** PASS. SoD is graded PARTIAL (AI-driven detective flagging, SaaS-first). The preventive request-time-block claim ("Lumos doesn't just audit SoD conflicts; it prevents them") is correctly quarantined in §4 UNVERIFIED and NOT embedded in the landable row. No overclaim.

**NATIVE-overclaim hunt:** JML/Certification/Role-Request NATIVE each rest on first-party product-page verbatim (capability presence). No NATIVE exceeds its evidence. Marketing-grade caveat is carried in every justification.

### Final LANDABLE rows (unchanged — all CONFIRMED)
Rows in §1 stand as written; no quote or URL correction required.

### Layer recommendation
`["L1","suite"]` — CORRECT and unchanged. Matches iga.yaml's single-suite contract and the file's own reasoning. Lumos is the same SaaS-first IGA class as ConductorOne/Zilla; all three land at L1 suite (NOT ConductorOne's proposed L2 `modern-iga`, which is overridden — see conductorone.md PASS 2). Per-area grades carry the modern/SaaS-first nuance.

**Verdict counts:** CONFIRMED 4 · QUOTE-DRIFT 0 · UNREACHABLE 0 · REFUTED 0. Lands fully.

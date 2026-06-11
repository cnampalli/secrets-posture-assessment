# ConductorOne — IGA vendor-fit research (WS-3)

Vendor: **ConductorOne** · slug `conductorone` · modern / next-gen IGA.
Live-fetched 2026-06-11. Primary domain `conductorone.com` 301-redirects to `c1.ai`; cite the
resolved `c1.ai` URLs (the host the live page actually serves). Anti-fabrication: every quote below
was returned verbatim by a live fetch of the cited URL.

---

## 1. Four ready-to-paste fit rows

Append to `matrix/domains/iga/iga-vendor-fit.csv` (same column order:
`vendor,vendor_slug,area,fit,justification,evidence_url,citation_keys`):

```csv
ConductorOne,conductorone,JML,PARTIAL,"Newer ILM module automates joiner/mover/leaver and birthright provisioning off HRIS, but lifecycle is a recent addition built on its access-control core rather than a mature first-party JML engine — graded PARTIAL honestly; vendor copy: ""When roles and attributes change, access changes. Automatically revoke unneeded access and provision new entitlements in response to transfers, promotions, and leave.""",https://www.c1.ai/solutions/identity-lifecycle-management/,conductorone-ilm
ConductorOne,conductorone,Certification,NATIVE,"Access Reviews is a core first-party product: scopes campaigns by app/role/department/risk, auto-routes reviewers, executes revocations and provisions changes in real time; vendor copy: ""Approved changes provision automatically. Revocations execute in real time.""",https://www.c1.ai/products/access-reviews/,conductorone-access-reviews
ConductorOne,conductorone,SoD,PARTIAL,"First-party SoD exists as the Access Conflicts policy add-on (not pure ADD-ON) but vendor frames it as an extension to the platform and as entitlement-set toxic-combination detection/notification, not an ERP-grade fine-grained SoX engine; realistic enterprise verdict trends ADD-ON where deep ERP SoD is in scope; vendor copy: ""C1 automatically and continuously tracks, detects, and notifies users of SoD policy violations.""",https://www.c1.ai/news/press-release/conductorone-extends-next-gen-iga-platform-with-separation-of-duties-policy-automation/,conductorone-sod-access-conflicts
ConductorOne,conductorone,Role/Request,NATIVE,"Self-service access requests with policy-driven approval, JIT and time-bound access are the platform's flagship capability; vendor copy: ""Replace standing privileged access with automated just-in-time (JIT) access to any app or permission.""",https://www.c1.ai/products/access-requests/,conductorone-access-requests;conductorone-jit
```

---

## 2. iga.yaml lines + layer rationale

The IGA yaml today uses **one flat `suite` layer (L1)** for all four incumbents — there is no
`modern-iga` / L2 label yet. ConductorOne is a next-gen / modern IGA whose centre of gravity is
JIT access-requests, not the lifecycle+cert+SoD breadth of a legacy suite. Recommend a **new L2
label** to keep the honest distinction visible rather than flattening it into `suite`.

Proposed edits (do NOT apply here — data-file changes are out of scope for this researcher):

```yaml
# vendor_layer:  add
  conductorone: ["L2", "modern-iga"]

# short:  add
  conductorone: "ConductorOne"

# layer_label:  add
  L2: "L2 · Modern / next-gen IGA (access-request & JIT-led; lifecycle, certification & SoD assessed per governance area) — fit assessed per governance area, not per-product NATIVE/ADD-ON"

# layer_groups:  add
  - ["L2", "Modern IGA"]
```

**Rationale:** ConductorOne self-describes (press release title) as a "Next-Gen IGA Platform";
its strengths (access requests, JIT, certification) are NATIVE while breadth areas (full JML,
ERP-grade SoD) are PARTIAL/add-on. A distinct L2 preserves that shape. If the team prefers to keep
a single layer, drop it into existing `suite`/L1 with the per-area grades carrying the nuance — but
the L2 split is the more honest representation. Decision is the owner's call (see §5).

---

## 3. Verification ledger (URL · verbatim Y/N · grade)

| Area | Evidence URL (live, resolved host) | Verbatim quote returned? | Grade |
|------|-----------|--------------------------|-------|
| JML | https://www.c1.ai/solutions/identity-lifecycle-management/ | Y — "When roles and attributes change, access changes. Automatically revoke unneeded access and provision new entitlements in response to transfers, promotions, and leave." Also "Give new hires the right access on day one, no manual intervention needed." | PARTIAL |
| Certification | https://www.c1.ai/products/access-reviews/ | Y — "Approved changes provision automatically. Revocations execute in real time." + "Scope reviews by application, role, department, risk level, and more." + "Schedule regular reviews to trigger and run automatically." | NATIVE |
| SoD | https://www.c1.ai/news/press-release/conductorone-extends-next-gen-iga-platform-with-separation-of-duties-policy-automation/ | Y — "C1 automatically and continuously tracks, detects, and notifies users of SoD policy violations." + "To create an Access Conflicts policy, users begin by selecting a group of entitlements as well as the conflicting set of entitlements." | PARTIAL (trends ADD-ON for ERP-grade) |
| Role/Request | https://www.c1.ai/products/access-requests/ | Y — "Replace standing privileged access with automated just-in-time (JIT) access to any app or permission." + "Configure policies to auto-approve routine requests and route sensitive requests to the right approvers with full context." | NATIVE |

Cross-supporting fetch: access-request SoD enforcement at request time —
"ConductorOne enforces separation of duties (SoD) policies by ensuring that the person requesting
access cannot be the same person approving it" (WebSearch surfacing c1.ai access-request guide) —
supports UC-I-008 / UC-I-015 fit but quoted from a guide, not the product page, so used only as
corroboration, not as a row's primary verbatim source.

---

## 4. UNVERIFIED list (do not assert without further live confirmation)

- **Docs portal pages 404 on live fetch.** `c1.ai/docs/product/access-reviews/review-tasks/`
  returned HTTP 404; `conductorone.com/docs/...` 301s but the resolved docs path was not
  server-rendered. All rows therefore cite product/solution/press pages (marketing-grade), not the
  docs portal. Flag: capability *presence* per vendor, not an efficacy benchmark — same caveat the
  Saviynt rows already carry.
- **Shadow-IT / app discovery / orphaned-account scanning** — lifecycle page says "Continuously
  scan for orphaned accounts … and remediate automatically," but this maps to UC-I-004 (account
  hygiene), not one of the four grid areas; not turned into a row. Discovery breadth unverified.
- **Cross-application / ERP-grade fine-grained SoD** — Access Conflicts is entitlement-set toxic-
  combination detection; no live evidence of SAP/Oracle ruleset-grade SoD. SoD graded PARTIAL on
  that basis; do not upgrade to NATIVE without ERP-connector evidence.
- **Request-time SoD blocking** (preventive, UC-I-008) vs detect-and-notify — press release wording
  is detective ("tracks, detects, notifies … can remediate or exempt"); preventive-at-request-gate
  not verbatim-confirmed on a first-party product page. Do not claim hard request-time block.
- **Citation-key registration** — the five proposed citation keys are not yet in the bib/citation
  store; validator will reject the rows until the keys + sources are registered (not done here —
  no data-file edits).

---

## 5. Ownership verdict

**Own ConductorOne in the IGA domain — recommend OWN, with two NATIVE (Certification,
Role/Request) and two PARTIAL (JML, SoD).** Evidence is live-verified with verbatim quotes for all
four areas, so the grid is defensible under the anti-fabrication policy. Two caveats for the owner
to clear before merging the data rows: (a) decide L2 `modern-iga` vs folding into `suite` (§2);
(b) register the five citation keys + accept the marketing-grade source caveat (docs portal not
fetchable). Honest grades favored over generosity: JML and SoD are real but recent/add-on, hence
PARTIAL not NATIVE.

---

## Adversarial verification (PASS 2)

Re-fetched 2026-06-11. Posture: REFUTE-by-default. `conductorone.com` 301→`c1.ai`; the cited `c1.ai` URLs are the live resolved hosts. Docs portal was unreachable in PASS 1 — re-anchor target was the product/solution/press pages (stabler than the 404'ing `/docs/` paths), and all four re-fetched live with their quotes intact.

| # | Area | evidence_url (resolved live host) | Quote re-fetch | Verdict |
|---|------|-----------------------------------|----------------|---------|
| 1 | JML | https://www.c1.ai/solutions/identity-lifecycle-management/ | "When roles and attributes change, access changes. Automatically revoke unneeded access and provision new entitlements in response to transfers, promotions, and leave." — exact | **CONFIRMED** |
| 2 | Certification | https://www.c1.ai/products/access-reviews/ | "Approved changes provision automatically. Revocations execute in real time." — exact | **CONFIRMED** |
| 3 | SoD | https://www.c1.ai/news/press-release/conductorone-extends-next-gen-iga-platform-with-separation-of-duties-policy-automation/ | "C1 automatically and continuously tracks, detects, and notifies users of SoD policy violations." — exact; re-fetch also confirms wording is **detective** ("tracks, detects, notifies … can remediate or exempt"), no request-time block | **CONFIRMED** |
| 4 | Role/Request | https://www.c1.ai/products/access-requests/ | "Replace standing privileged access with automated just-in-time (JIT) access to any app or permission." — exact (page resolved; note the live page also serves the same copy under `/products/access-controls/` — both reach the quote) | **CONFIRMED** |

**Schema sanity:** 7 cols; fit = PARTIAL/NATIVE/PARTIAL/NATIVE ∈ {NATIVE,PARTIAL,ADD-ON}; non-empty justification/url/keys. PASS.

**SoD overclaim check (special scrutiny):** PASS. The SoD row is graded PARTIAL (trending ADD-ON for ERP-grade) and the justification does NOT claim preventive request-time SoD. Re-fetch confirms the press-release wording is detective only. The unverified preventive/request-time-block claim correctly remains in the §4 UNVERIFIED list and is NOT embedded in any landable row. No overclaim.

**NATIVE-overclaim hunt:** Certification NATIVE and Role/Request NATIVE are both supported by first-party product-page verbatim. JML PARTIAL and SoD PARTIAL are appropriately conservative given the marketing-grade sourcing and recency. No NATIVE is over-stated relative to its evidence.

**Source-grade caveat:** All four rows cite marketing/solution/press pages (docs portal 404s). This is the same capability-presence (not efficacy) caveat the Saviynt rows carry — acceptable, but the rows must carry that hedge when landed.

### Final LANDABLE rows (unchanged quotes — all CONFIRMED)
```csv
ConductorOne,conductorone,JML,PARTIAL,"Newer ILM module automates joiner/mover/leaver and birthright provisioning off HRIS, but lifecycle is a recent addition built on its access-control core rather than a mature first-party JML engine — graded PARTIAL honestly; vendor copy: ""When roles and attributes change, access changes. Automatically revoke unneeded access and provision new entitlements in response to transfers, promotions, and leave.""",https://www.c1.ai/solutions/identity-lifecycle-management/,conductorone-ilm
ConductorOne,conductorone,Certification,NATIVE,"Access Reviews is a core first-party product: scopes campaigns by app/role/department/risk, auto-routes reviewers, executes revocations and provisions changes in real time; vendor copy: ""Approved changes provision automatically. Revocations execute in real time.""",https://www.c1.ai/products/access-reviews/,conductorone-access-reviews
ConductorOne,conductorone,SoD,PARTIAL,"First-party SoD exists as the Access Conflicts policy (detect-and-notify), framed as a platform extension and entitlement-set toxic-combination detection — not an ERP-grade fine-grained SoX engine; trends ADD-ON where deep ERP SoD is in scope; vendor copy: ""C1 automatically and continuously tracks, detects, and notifies users of SoD policy violations.""",https://www.c1.ai/news/press-release/conductorone-extends-next-gen-iga-platform-with-separation-of-duties-policy-automation/,conductorone-sod-access-conflicts
ConductorOne,conductorone,Role/Request,NATIVE,"Self-service access requests with policy-driven approval, JIT and time-bound access are the platform's flagship capability; vendor copy: ""Replace standing privileged access with automated just-in-time (JIT) access to any app or permission.""",https://www.c1.ai/products/access-requests/,conductorone-access-requests;conductorone-jit
```
(SoD justification trimmed to drop the "preventive" ambiguity and keep only the detective verbatim — defensible under anti-fabrication.)

### Layer recommendation — RESOLVE THE CONFLICT
**Use `["L1","suite"]`, NOT the proposed L2 `modern-iga`.** Decisive grounds: `iga.yaml` (lines 8-10, 26-27) hard-codes a SINGLE `suite` layer for ALL IGA vendors and states fit is "assessed per governance AREA, not the layered L1/L2 model used by secrets/PAM." The honest modern-vs-legacy distinction ConductorOne wants to preserve is ALREADY carried by its per-area grades (JML PARTIAL, SoD PARTIAL vs SailPoint NATIVE) — it does not need a layer. Adding L2 `modern-iga` would require new `layer_label`/`layer_groups` keys and break the descriptor's stated contract. The PAM domain's L2 `modern-access` (Teleport) is NOT a precedent here: there L2 marks a genuinely different *access model* (ephemeral certificate-based vs vaulting); ConductorOne/Lumos/Zilla deliver the same four governance areas as the incumbents, just SaaS-first — same class, not a different model. **Override §2's L2 proposal → L1 suite.**

**Verdict counts:** CONFIRMED 4 · QUOTE-DRIFT 0 · UNREACHABLE 0 · REFUTED 0. Lands fully (quotes verbatim); SoD stays PARTIAL with no preventive overclaim; layer corrected to L1 suite.

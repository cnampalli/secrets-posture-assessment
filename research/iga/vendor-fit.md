# IGA Vendor-Fit Overlay (Phase 3)

**Scope.** A LIGHTWEIGHT per-AREA vendor-fit view for the IGA domain, distinct
from the per-use-case NATIVE / ADD-ON matrix used for the Secrets-management and
PAM domains. This overlay is informational context for assessors interpreting an
organisation's process-maturity scores; it is **NOT** a tool-deployment scorecard
and it deliberately avoids a flat "buy this one" ranking.

**Areas (4):**
- **JML** — Joiner / Mover / Leaver lifecycle (automated provisioning, mover
  re-evaluation, leaver de-provisioning).
- **Certification** — periodic access reviews / certification campaigns.
- **SoD** — Separation of Duties (toxic-combination prevention + detection).
- **Role/Request** — role modelling + self-service access request / approval.

**Verdict vocabulary (per vendor x area):**
- **NATIVE** — first-party, in-platform capability documented as a core function
  of the product, no separate product or third-party integration required.
- **PARTIAL** — capability exists but is meaningfully scoped/constrained
  (e.g. limited to the vendor's own resource model, narrow object types, or
  requires a higher-tier SKU), so it does not generalise to cross-application
  enterprise scope without help.
- **ADD-ON** — capability typically depends on a separate SKU, a connected
  governance engine that must be enabled per-app, or an external
  integration/GRC product to be usable at enterprise scope.

> **Source-confidence framing (project rule).** Every verdict below is anchored to
> the vendor's OWN official documentation with a verbatim quote. Marketing
> solution-pages are used only where product docs were not server-renderable
> (noted per cell). This is a *capability-presence* read, not an independent
> efficacy benchmark — vendors describe their own strengths. Treat NATIVE as
> "the vendor documents this as core," not as "best-in-class." Where a vendor's
> own docs reveal a constraint (e.g. Entra SoD is access-package-scoped; Okta SoD
> requires Governance Engine enabled per app), the verdict reflects that
> constraint honestly rather than the marketing headline.

---

## Vendor-fit matrix (at a glance)

| Vendor | JML | Certification | SoD | Role/Request |
|---|---|---|---|---|
| SailPoint Identity Security Cloud | NATIVE | NATIVE | NATIVE | NATIVE |
| Saviynt Enterprise Identity Cloud | NATIVE | NATIVE | NATIVE | NATIVE |
| Microsoft Entra ID Governance | NATIVE | NATIVE | **PARTIAL** | NATIVE |
| Okta Identity Governance | NATIVE | NATIVE | **PARTIAL** | NATIVE |

The two purpose-built enterprise IGA suites (SailPoint, Saviynt) document
first-party SoD analysis with cross-application reach. The two
IdP-anchored governance products (Entra, Okta) document SoD only as a
constrained capability — Entra scoped to access-package incompatibility, Okta
scoped to entitlement combinations on apps that have the Governance Engine
enabled — hence **PARTIAL** in both cases. This split is the single most
decision-relevant finding in the overlay and should be surfaced to assessors.

---

## SailPoint Identity Security Cloud (ISC)

| Area | Verdict | One-line justification |
|---|---|---|
| JML | NATIVE | Lifecycle states drive access changes per identity profile (pre-hire/active/leave/terminated/archived). |
| Certification | NATIVE | Certification campaigns review entitlement, access-profile, and role data, with revocation through connectors. |
| SoD | NATIVE | First-party SoD service builds conflicting-access policy lists and generates violation reports across governance data. |
| Role/Request | NATIVE | Roles obtained via access request can be approved or revoked; role model governs assignment. |

**JML — NATIVE.** SailPoint docs: *"Lifecycle states describe a user's status in
the organization, which you can use to drive access changes for your users. For
example, when a new employee joins your company, Identity Security Cloud can grant
them the required access for active employees. When someone leaves the
organization, their access can be automatically revoked or their source accounts
disabled."* (`saas/help/provisioning/lifecycle.html`)

**Certification — NATIVE.** SailPoint docs: *"Certifications may include
entitlement, access profile, and role data."* and *"Roles obtained through an
access request can be approved or revoked."* (`saas/help/certs/understanding_certifications.html`)

**SoD — NATIVE.** SailPoint docs: *"Identity Security Cloud's Separation of Duties
(SoD) service provides visibility into the access everyone in your organization
has so you can easily track violations of your internal policies and see where
your greatest risks lie."* and *"Create Separation of Duties policies to build
lists of conflicting access. Identities in your org with access in one list aren't
allowed to have access within the other list."* (`saas/help/sod/index.html`)

**Role/Request — NATIVE.** Same certification doc establishes the request+role
model: *"Roles obtained through an access request can be approved or revoked.
Roles assigned to users through automated assignment criteria can only be
acknowledged since the role model controls the role assignment."*
(`saas/help/certs/understanding_certifications.html`)

*Source confidence: HIGH.* All four anchored to product documentation
(documentation.sailpoint.com), server-rendered, verbatim quotes confirmed.

---

## Saviynt Enterprise Identity Cloud (EIC)

| Area | Verdict | One-line justification |
|---|---|---|
| JML | NATIVE | Automates the complete identity lifecycle from onboarding access assignment to departure revocation. |
| Certification | NATIVE | AI-assisted certification campaigns; campaigns can certify accounts, entitlements, enterprise/app roles. |
| SoD | NATIVE | First-party preventive + detective SoD controls, within and across applications. |
| Role/Request | NATIVE | Self-service access-request management with SoD evaluated at the point of request. |

**JML — NATIVE.** Saviynt IGA product page: *"Automate the complete identity
lifecycle, from rapidly assigning access during onboarding to automatically
revoking it upon departure."* (`saviynt.com/products/identity-governance-and-administration`)

**Certification — NATIVE.** Saviynt IGA product page: *"Use AI-powered
recommendations and automation to streamline access requests, simplify
certification campaigns, and ensure continuous compliance while reducing the total
cost of ownership."* (`saviynt.com/products/identity-governance-and-administration`)

**SoD — NATIVE.** Saviynt SoD solution page: *"Detect, prevent, and remediate
segregation-of-duties (SoD) conflicts across your entire application ecosystem
with intelligent, automated controls."* and *"Saviynt provides segregation of
duties preventive and detective controls."* (`saviynt.com/solutions/segregation-of-duties`)

**Role/Request — NATIVE.** Saviynt IGA product page: *"Access Request Management:
IGA software streamlines the process of requesting access privileges, making it a
seamless, self-service experience that reduces the administrative burden."*;
SoD solution page confirms request-stage enforcement: *"Block conflicting access
at the point of request with intelligent workflows that evaluate policies, prevent
violations, and guide approvers with clear risk insights."*
(`saviynt.com/products/identity-governance-and-administration`, `saviynt.com/solutions/segregation-of-duties`)

*Source confidence: MEDIUM-HIGH.* Saviynt's product documentation portal
(docs.saviyntcloud.com) is a client-rendered Zoomin SPA and was NOT
server-renderable from this environment, so its topic text could not be quoted
verbatim. Quotes above are taken from Saviynt's OWN official saviynt.com product
and solution pages (server-rendered, verbatim confirmed). Capability presence is
well-established (Saviynt is a recognised enterprise IGA + AAG/SoD suite), but the
anchor is marketing-grade product copy rather than admin docs — flagged honestly.
Docs-portal topics that corroborate (not quoted): `EIC-Admin` Chapter 16
"Segregation of Duties" (Detective-SOD) and Chapter 15 "Campaigns and
Certifications".

---

## Microsoft Entra ID Governance

| Area | Verdict | One-line justification |
|---|---|---|
| JML | NATIVE | Lifecycle Workflows automate Joiner/Mover/Leaver tasks across the three lifecycle phases. |
| Certification | NATIVE | Access reviews recur (weekly/monthly/quarterly/annually) over groups, apps, and role assignments. |
| SoD | **PARTIAL** | SoD exists only as access-package incompatibility (block a request based on existing group/package membership) — not a general cross-app SoD policy engine. |
| Role/Request | NATIVE | Entitlement management automates access-request workflows, assignments, reviews, and expiration via access packages. |

**JML — NATIVE.** Microsoft Learn: *"Lifecycle workflows (LCW) are identity
governance capabilities that enable organizations to manage Microsoft Entra users
across the three phases of a user's lifecycle with an organization: Joiner ... Mover
... Leaver ..."* (`learn.microsoft.com/.../what-are-lifecycle-workflows`)

**Certification — NATIVE.** Microsoft Learn: *"Access reviews in Microsoft Entra
ID, part of Microsoft Entra, enable organizations to efficiently manage group
memberships, access to enterprise applications, and role assignments. User access
can be reviewed regularly to make sure only the right people have continued
access."* (`learn.microsoft.com/.../access-reviews-overview`)

**SoD — PARTIAL.** Microsoft Learn: *"With the separation of duties settings on an
access package, you can configure that a user who is a member of a security group
or who already has an assignment to one access package can't request another
access package."* (`learn.microsoft.com/.../entitlement-management-access-package-incompatible`)
→ This is **request-time incompatibility scoped to Entra access packages and
groups**, not a general toxic-combination policy engine spanning arbitrary
downstream application entitlements. It will not, on its own, satisfy fine-grained
cross-application SoD of the kind SOX/ERP auditors expect (e.g. create-vendor vs
pay-invoice inside an ERP). Hence PARTIAL, not NATIVE. Closing that gap typically
requires a dedicated AAG/GRC capability or integration.

**Role/Request — NATIVE.** Microsoft Learn: *"Entitlement management is an identity
governance feature that enables organizations to manage identity and access
lifecycle at scale, by automating access request workflows, access assignments,
reviews, and expiration."* (`learn.microsoft.com/.../entitlement-management-overview`)

*Source confidence: HIGH.* All anchored to Microsoft Learn (learn.microsoft.com),
server-rendered, verbatim quotes confirmed. Note also a licensing caveat: these
are Entra ID Governance (premium) features, not base Entra ID — relevant if the
assessed org assumes "we already have Entra."

---

## Okta Identity Governance (OIG)

| Area | Verdict | One-line justification |
|---|---|---|
| JML | NATIVE | Built on Lifecycle Management + Workflows; auto-provisions new hires to birthright apps and automates lifecycle tasks. |
| Certification | NATIVE | Access certifications (reviews) confirm users still need access, enriched with usage context. |
| SoD | **PARTIAL** | SoD rules only apply to entitlement combinations on apps with the Governance Engine enabled, and enforce via Access Requests / Certifications rather than a standalone cross-app SoD engine. |
| Role/Request | NATIVE | Self-service access requests evaluate who receives access; approval flows protect sensitive resources. |

**JML — NATIVE.** Okta docs: *"Lifecycle Management helps you manage users, groups
(and group owners), apps, rules, assignments, and other attributes associated with
these."* and *"Automatically provision new employees to birthright apps based on
their user profile attributes."* (`help.okta.com/.../identity-governance/iga.htm`,
`.../iga-overview.htm`)

**Certification — NATIVE.** Okta docs: *"Make access certification more meaningful
with the contextual information, such as sign-in frequency, a resource's last
accessed date, and more."* (`help.okta.com/.../identity-governance/iga-overview.htm`)

**SoD — PARTIAL.** Okta docs: *"Use separation of duties (SOD) to define rules that
allow (with or without additional oversight) or block specific entitlement
combinations for apps with Governance Engine enabled."* and *"With SOD rules, you
can adopt a two-pronged approach to manage conflicting entitlement assignments –
preventative and remediative. Use Access Requests and Access Certifications to
control which combinations of entitlements users are allowed to possess."*
(`help.okta.com/oie/.../identity-governance/sd/separation-of-duties.htm`)
→ Okta DOES have a first-party SoD feature (so this is NOT a pure ADD-ON), but its
own docs constrain it to **entitlement combinations on apps that have the
Governance Engine enabled**, enforced through the Access Request / Certification
paths. For the deep, cross-application / ERP-grade SoD a regulated FI usually
needs, this commonly requires the entitlement model to be onboarded per app and/or
an external/integration approach — so the realistic enterprise verdict is PARTIAL,
trending toward ADD-ON where ERP-level fine-grained SoD is in scope. Be honest with
assessors: the headline "Okta has SoD" is true but narrower than SailPoint/Saviynt.

**Role/Request — NATIVE.** Okta docs: *"Okta Identity Governance uses automated,
self-service requests to evaluate who receives access to resources. Approval flows
provide security for your most sensitive data and tools."*
(`help.okta.com/.../identity-governance/iga-overview.htm`)

*Source confidence: HIGH.* All anchored to Okta official help docs (help.okta.com),
server-rendered, verbatim quotes confirmed.

---

## Assessor guidance (how to use this overlay)

1. **Do not convert this into a score.** The instrument scores PROCESS MATURITY,
   not tool capability. This overlay only helps an assessor interpret *why* a
   given org may find certain IGA areas easier or harder to mature given its
   incumbent platform.
2. **SoD is the discriminating area.** If the org's IGA platform is Entra ID
   Governance or Okta IG and the assessment scope includes cross-application or
   ERP-grade SoD (common under SOX SoD expectations), expect a capability gap that
   process maturity alone cannot close — the org likely needs an AAG/GRC component
   or integration. Flag this rather than assuming the IdP "covers SoD."
3. **NATIVE != superior.** Two vendors can both be NATIVE in an area with very
   different depth. Use the verbatim quotes, not the verdict label, when the
   distinction matters.
4. **Licensing reality.** Entra capabilities here require Entra ID Governance
   (premium), and Okta SoD requires the Governance Engine enabled per app — neither
   is "free with the IdP you already own."

## Regulatory anchors (context, not vendor claims)

These frameworks motivate WHY each area is assessed; they are NOT vendor citations
and are listed for the build agent's cross-mapping convenience only:
- **SoD** → SOX (segregation of duties over financial processes); NIST SP 800-53
  **AC-5** (Separation of Duties); ISO/IEC 27001:2022 Annex A **5.3**.
- **Certification** → NIST SP 800-53 **AC-2** (Account Management — periodic
  review); APRA CPS 234 (access provisioning/review).
- **JML / Role/Request** → NIST SP 800-53 **AC-2 / AC-6** (least privilege);
  ASD ISM access-control guidance; APRA CPS 234.

(Control-ID mappings above are indicative cross-references for the IGA-domain
control authors to VERIFY against authoritative sources — they are not asserted
here as verified citations.)

---

## Citation verification

Adversarial verification performed 2026-06-10. Method: each URL was fetched
directly (HTTP, redirects followed), the HTML stripped to text and whitespace/
quote-character normalised, then the verbatim quote was searched for as a
substring. URL resolution and quote presence were both confirmed. All cited
URLs returned HTTP 200 from their stated authoritative hosts
(documentation.sailpoint.com, saviynt.com, learn.microsoft.com, help.okta.com).

No control IDs (NIST AC-x, ASD ISM, ISO A.x) are asserted as verified citations
in this file — the regulatory anchors in the section above are explicitly marked
as indicative cross-references to be verified separately, so they are out of
scope for this vendor-quote verification pass.

| Key | URL resolves | Quote faithful | Verdict |
|---|---|---|---|
| sailpoint-isc-lifecycle | yes (200) | yes | VERIFIED |
| sailpoint-isc-certifications | yes (200) | yes | VERIFIED |
| sailpoint-isc-cert-roles-request | yes (200) | yes | VERIFIED |
| sailpoint-isc-sod | yes (200) | yes | VERIFIED |
| sailpoint-isc-sod-policies | yes (200) | yes | VERIFIED |
| saviynt-eic-lifecycle | yes (200) | yes | VERIFIED |
| saviynt-eic-certification | yes (200) | yes | VERIFIED |
| saviynt-eic-request | yes (200) | yes | VERIFIED |
| saviynt-eic-sod | yes (200) | yes | VERIFIED |
| saviynt-eic-sod-controls | yes (200) | yes | VERIFIED |
| saviynt-eic-sod-request-point | yes (200) | yes | VERIFIED |
| entra-idg-lifecycle-workflows | yes (200) | yes | VERIFIED |
| entra-idg-access-reviews | yes (200) | yes | VERIFIED |
| entra-idg-sod-access-package | yes (200) | yes | VERIFIED |
| entra-idg-entitlement-management | yes (200) | yes | VERIFIED |
| okta-oig-lifecycle | yes (200) | yes | VERIFIED |
| okta-oig-certification | yes (200) | yes | VERIFIED |
| okta-oig-request | yes (200) | yes | VERIFIED |
| okta-oig-sod | yes (200) | yes | VERIFIED |
| okta-oig-sod-approach | yes (200) | yes | VERIFIED |

**Notes.**
- The `okta-oig-sod-approach` quote contains an en-dash ("approach –
  preventative and remediative"); this matches the source verbatim (the source
  uses an en-dash, not a hyphen). Preserve the en-dash if this quote is
  re-typed.
- `okta-oig-lifecycle` is anchored to two Okta help pages in the prose
  (`iga.htm` plus the "birthright apps" sentence on `iga-overview.htm`); only
  the `iga.htm` "Lifecycle Management helps you manage users..." sentence is the
  registered citation quote and it verified on `iga.htm`.
- Saviynt anchors (`saviynt.com` product/solution pages) are marketing-grade
  product copy, not admin docs — already flagged honestly in the Saviynt source-
  confidence note above. They are VERIFIED as faithful quotes from those pages,
  which is the claim being made (capability presence per the vendor), not an
  independent efficacy benchmark.

**Overall: PASS.** All 20 citations VERIFIED. No SUSPECT or FABRICATED entries;
nothing removed.

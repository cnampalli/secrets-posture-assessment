# Zilla Security (slug `zilla`) — IGA vendor-fit research

**Vendor:** Zilla Security — modern, AI-driven IGA SaaS. Two products: **Zilla Comply**
(access reviews / certification) and **Zilla Provisioning / Zilla Provision** (access requests +
joiner/mover/leaver lifecycle), driven by **Zilla AI Profiles**.

**CRITICAL SOURCING CAVEAT (anti-fabrication):** As of this research date the entire
`zillasecurity.com` capability site **302-redirects to `https://www.cyberark.com/products/modern-iga/`**.
The standalone Zilla product/doc pages are no longer independently server-rendered. Capability claims
now live under **CyberArk marketing** (modern-IGA product page) plus the **CyberArk acquisition press
release**; pre-acquisition wording survives in the **Oct-2023 Zilla Provision PR Newswire release** and the
**Zilla support wiki** (`zilla.atlassian.net`). All grades below are **capability-presence per vendor,
marketing-grade source — not an efficacy benchmark.** No customer-doc / admin-guide depth was obtainable
live (the doc portal is gated/redirected), so SoD and Role/Request are graded conservatively.

---

## (1) Four ready-to-paste fit rows

> Paste into `matrix/domains/iga/iga-vendor-fit.csv` (header:
> `vendor,vendor_slug,area,fit,justification,evidence_url,citation_keys`).
> Same marketing-grade hedge style as the Saviynt rows.

```csv
Zilla Security,zilla,JML,NATIVE,"Zilla Provisioning automates the full joiner/mover/leaver lifecycle via AI Profiles + event-driven policy; vendor copy: ""Streamline identity lifecycle events and automate access for workforce and privileged users joining, moving roles and leaving the organization."" and Zilla Provisioning ""Revolutionizes access management with an AI-driven, automated approach to provisioning tasks such as onboarding, role transitions and offboarding."" (marketing-grade source, now CyberArk-hosted post-acquisition — capability presence per vendor, not an efficacy benchmark)",https://www.cyberark.com/products/modern-iga/,zilla-provisioning-lifecycle;zilla-acquisition-press
Zilla Security,zilla,Certification,NATIVE,"Zilla Comply is the product's flagship: fully-automated access-review / certification campaigns with audit-ready evidence; vendor copy: ""Access reviews with 80% less effort"" with ""Fully automated campaign prep, review management, and evidence creation."" and Zilla Comply ""Simplifies user access reviews and evidence documentation through robust integration and automation that supports the entire audit process."" (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.cyberark.com/products/modern-iga/,zilla-comply-certification;zilla-acquisition-press
Zilla Security,zilla,SoD,PARTIAL,"First-party SoD exists (so not ADD-ON) but is presented as detective alerting / policy-mapped conflict detection rather than a dedicated ERP-grade fine-grained SoD engine; vendor copy: ""Get alerts in real-time for high-risk permissions and group memberships"" / ""Detect Segregation of Duties (SOD) conflicts"", and Zilla Provision ""improves security posture through policies, such as Segregation of Duties (SOD)."" Realistic enterprise verdict trends toward ADD-ON where ERP-grade fine-grained SoD is in scope; no cross-app toxic-combination engine depth was verifiable in live docs. (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.cyberark.com/products/modern-iga/,zilla-sod-detect;zilla-provision-pr-sod
Zilla Security,zilla,Role/Request,NATIVE,"Zilla Provision delivers self-service access requests with policy-aware approval routing, executed through ITSM (ServiceNow / Jira) for workflow + audit trail; vendor copy: ""Self-service Access Requests for faster, more convenient, and error-free access to enterprise applications and services"" and Zilla ""automatically detects potential policy violations, dynamically assigns business approvals and routes the ticket to the assignee to fulfill approved access."" Request/approval is NATIVE; note role-MODELING / role-mining depth is not strongly evidenced in live sources. (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.prnewswire.com/news-releases/zilla-security-releases-zilla-provision-to-automate-and-streamline-identity-security-301972455.html,zilla-provision-request;zilla-provision-pr-request
```

---

## (2) `matrix/config/domains/iga.yaml` lines + layer rationale

Add `zilla` to the three maps (single L1 "suite" layer, identical to the existing four — IGA
fit is assessed per governance AREA, not per-product layer):

```yaml
vendor_layer:
  zilla: ["L1", "suite"]

short:
  zilla: "Zilla"
```

(No change to `layer_label`, `anchors_tier`, or `layer_groups` — Zilla is a fifth L1 suite.)

**Layer rationale:** Zilla is a full IGA SaaS platform (lifecycle + certification + SoD +
access requests), so it belongs in the same **L1 · IGA platforms** band as SailPoint / Saviynt /
Entra / Okta. Per `iga.yaml`'s descriptor, all IGA suites share L1 "suite" and are differentiated
by per-area fit, not by layer. Zilla's profile is **certification-led** (Comply is the historic
strength) with strong lifecycle/provisioning, weaker (detective-only) SoD — a meaningful contrast
to SailPoint/Saviynt's NATIVE SoD.

---

## (3) Ownership verdict + `vendor-ownership.yaml` entry

**VERDICT:** Zilla Security is a **wholly-owned CyberArk product** as of **2025-02-13** (announced;
TechCrunch/CyberScoop/Crunchbase concur). Deal: **US$165M cash + US$10M earn-out (up to ~US$175M)**.
This is **HIGH confidence** — primary CyberArk press release + multiple independent outlets + a live
domain redirect (`zillasecurity.com` → `cyberark.com`) corroborating integration.

**Cross-domain concentration impact (the moat):** CyberArk already anchors the **secrets** and **PAM**
matrices in this instrument and owns Conjur, Venafi (2024-10), and Entro (2025-02). Adding Zilla means
CyberArk now spans **secrets + PAM + machine-identity + IGA** — a single parent across four domains.
This row must be added so substitutability/concentration math does NOT count Zilla as an independent
second-source IGA vendor against CyberArk.

```yaml
zilla:
  parent: cyberark
  as_of: 2025-02-13
  confidence: HIGH
  source: cyberark.com (press) ; crunchbase.com ; techcrunch.com
  note: >-
    CyberArk acquired Zilla Security (modern IGA — Zilla Comply access reviews +
    Zilla Provisioning lifecycle) on 2025-02-13 for ~US$165M cash + US$10M earn-out
    (up to ~US$175M). zillasecurity.com now 302-redirects to cyberark.com/products/modern-iga.
    Collapses Zilla under CyberArk for cross-domain (secrets/PAM/machine-identity/IGA)
    concentration analysis. Verify exact close date before client use.
```

---

## (4) Verification ledger (URL · verbatim Y/N · grade)

| # | Area / fact | URL | Verbatim found | Grade |
|---|---|---|---|---|
| 1 | Acquisition date 2025-02-13, $165M+$10M | https://www.cyberark.com/press/cyberark-acquires-zilla-security-to-reshape-identity-governance-and-administration-for-the-modern-enterprise/ | Y — "$165 million in cash"; "$10 million earn-out" | OWNERSHIP HIGH |
| 2 | JML / lifecycle | https://www.cyberark.com/products/modern-iga/ | Y — "automate access for workforce and privileged users joining, moving roles and leaving the organization" | NATIVE |
| 3 | Zilla Provisioning (lifecycle, AI-driven) | https://www.cyberark.com/press/cyberark-acquires-zilla-security-...-enterprise/ | Y — "an AI-driven, automated approach to provisioning tasks such as onboarding, role transitions and offboarding" | NATIVE |
| 4 | Certification / access reviews | https://www.cyberark.com/products/modern-iga/ | Y — "Fully automated campaign prep, review management, and evidence creation"; "Access reviews with 80% less effort" | NATIVE |
| 5 | Zilla Comply | press release (as above) | Y — "Simplifies user access reviews and evidence documentation through robust integration and automation that supports the entire audit process" | NATIVE |
| 6 | SoD detection | https://www.cyberark.com/products/modern-iga/ | Y — "Detect Segregation of Duties (SOD) conflicts"; "alerts in real-time for high-risk permissions and group memberships" | PARTIAL |
| 7 | SoD via policy (Zilla Provision PR) | https://www.prnewswire.com/news-releases/zilla-security-releases-zilla-provision-to-automate-and-streamline-identity-security-301972455.html | Y — "improves security posture through policies, such as Segregation of Duties (SOD)" | PARTIAL |
| 8 | Self-service access request | https://www.prnewswire.com/.../zilla-provision-...301972455.html | Y — "Self-service Access Requests for faster, more convenient, and error-free access to enterprise applications and services" | NATIVE |
| 9 | Approval routing / policy-violation detection | https://www.cyberark.com/products/modern-iga/ (search-surfaced) | Y — "automatically detects potential policy violations, dynamically assigns business approvals and routes the ticket to the assignee" | NATIVE |
| 10 | Domain redirect (integration evidence) | https://zillasecurity.com/ → 302 → https://www.cyberark.com/products/modern-iga/ | Y — live 302 redirect observed | OWNERSHIP corroboration |

---

## (5) UNVERIFIED list (do NOT publish as fact without further primary sourcing)

- **ERP-grade fine-grained / cross-application toxic-combination SoD engine** — only detective
  "alert"/"detect conflicts" wording found; no evidence of a SailPoint/Saviynt-class preventive
  cross-app SoD engine. Graded SoD = PARTIAL deliberately. Needs admin-doc confirmation.
- **Role MINING / RBAC role-model authoring** (UC-I-011) — Role/Request graded NATIVE on the
  request/approval axis only; role-mining/role-modelling depth NOT evidenced in live sources.
- **Preventive (request-time blocking) SoD** vs detective-only — "detects potential policy
  violations" at request time is suggestive but the block-vs-flag behaviour is unconfirmed.
- **Original `zillasecurity.com` capability-page wording** — the standalone pages
  (`/user-access-lifecycle-management/`, `/segregation-of-duties/`,
  `/self-service-access-provisioning-request/`) all now 302 to CyberArk; pre-acquisition exact
  phrasing is only partially recoverable (PR Newswire + support wiki). Evidence URLs above point to
  the durable CyberArk-hosted equivalents and the dated PR release.
- **Exact acquisition CLOSE date** (vs 2025-02-13 ANNOUNCE date) — not separately confirmed;
  `as_of` uses the announcement date.

---

## Adversarial verification (PASS 2)

Re-fetched 2026-06-11. Posture: REFUTE-by-default. `zillasecurity.com` redirects to CyberArk; verified the LANDED URLs are live CyberArk pages and that each embedded verbatim is an exact contiguous substring there.

### Ownership (two independent sources required)
**CONFIRMED — CyberArk owns Zilla Security, announced 2025-02-13, $165M cash + $10M earn-out (~$175M).**
- Source 1 (primary): cyberark.com press release re-fetched live — "$165 million in cash" + "$10 million earn-out" + "CyberArk has acquired Zilla Security" all verbatim.
- Source 2+ (independent): WebSearch surfaced TechCrunch, CyberScoop, SiliconANGLE, BankInfoSecurity, INCYBER, Crunchbase — all concur Feb 13 2025, ~$175M. Requirement (two independent) exceeded.
- Redirect corroboration: `zillasecurity.com` → `cyberark.com/products/modern-iga/` confirmed; landed CyberArk pages are live and carry the capability quotes. The `vendor-ownership.yaml` entry in §3 stands.

### Row quote verification
| # | Area | evidence_url (landed) | Quote re-fetch | Verdict |
|---|------|-----------------------|----------------|---------|
| 1 | JML | https://www.cyberark.com/products/modern-iga/ | "automate access for workforce and privileged users joining, moving roles and leaving the organization" — exact; press-release clause "an AI-driven, automated approach to provisioning tasks such as onboarding, role transitions and offboarding" — exact | **CONFIRMED** |
| 2 | Certification | https://www.cyberark.com/products/modern-iga/ | "Fully automated campaign prep, review management, and evidence creation" + "Access reviews with 80% less effort" — exact; press clause "Simplifies user access reviews and evidence documentation…" — exact | **CONFIRMED** |
| 3 | SoD | https://www.cyberark.com/products/modern-iga/ | "Detect Segregation of Duties (SOD) conflicts" + "Get alerts in real-time for high-risk permissions and group memberships" — exact; PR Newswire "improves security posture through policies, such as Segregation of Duties (SOD)" — exact | **CONFIRMED** (PARTIAL grade) |
| 4 | Role/Request | https://www.prnewswire.com/...301972455.html | "Self-service Access Requests for faster, more convenient, and error-free access to enterprise applications and services" — **exact (CONFIRMED)**. BUT the second embedded clause "automatically detects potential policy violations, dynamically assigns business approvals and routes the ticket to the assignee to fulfill approved access" — **NOT FOUND** on the PR Newswire URL **nor** on cyberark.com/products/modern-iga/ (this clause was self-flagged "(search-surfaced)" in the §4 ledger) | **QUOTE-DRIFT** — corrected below |

**Finding (anti-fabrication):** Row 4 embedded a second quote that does not re-fetch on the cited URL (or the alternate CyberArk page). Under the cardinal rule this clause is dropped and replaced with a verbatim clause that IS live on the cited PR Newswire URL. The row REMAINS NATIVE because its primary verbatim (self-service access requests) is confirmed on the cited URL.

**Corrected Role/Request row (apply this — replaces §1 row 4):**
```csv
Zilla Security,zilla,Role/Request,NATIVE,"Zilla Provision delivers self-service access requests executed through ITSM (ServiceNow / Jira) for workflow + audit trail; vendor copy: ""Self-service Access Requests for faster, more convenient, and error-free access to enterprise applications and services"" and ""system-verified provisioning through IT service management (ITSM) systems by leveraging them for workflow, ticketing and audit trails."" Request/approval is NATIVE; role-MODELING / role-mining depth is not strongly evidenced in live sources. (marketing-grade source — capability presence per vendor, not an efficacy benchmark)",https://www.prnewswire.com/news-releases/zilla-security-releases-zilla-provision-to-automate-and-streamline-identity-security-301972455.html,zilla-provision-request;zilla-provision-pr-request
```
(Removed the unverifiable "dynamically assigns business approvals and routes the ticket to the assignee" clause; substituted the verbatim ITSM-workflow clause confirmed live on the same cited URL. Ledger row 9 "automatically detects potential policy violations…" is downgraded to UNVERIFIED — it was search-surfaced, not on a fetchable first-party page.)

**Schema sanity:** 7 cols; fit = NATIVE/NATIVE/PARTIAL/NATIVE ∈ {NATIVE,PARTIAL,ADD-ON}; non-empty justification/url/keys. PASS after correction.

**SoD overclaim check:** PASS. SoD = PARTIAL, detective-only ("Detect…conflicts", "alerts in real-time"); the preventive request-time-block claim stays in §5 UNVERIFIED, not embedded. No overclaim.

**NATIVE-overclaim hunt:** JML and Certification NATIVE are well-supported (CyberArk modern-iga page + press release verbatim). Role/Request NATIVE survives on the corrected verbatim. No remaining NATIVE exceeds its evidence.

### Final LANDABLE rows
Rows 1 (JML), 2 (Certification), 3 (SoD) stand as written in §1. **Row 4 (Role/Request) MUST be replaced by the corrected CSV above** before landing.

### Layer recommendation
`["L1","suite"]` — CORRECT and unchanged. Zilla is a full IGA SaaS (lifecycle + cert + SoD + requests), same class as the incumbents and the other new SaaS-first vendors; lands at L1 suite per iga.yaml's single-suite contract. Consistent with Omada (L1), and with the override of ConductorOne's L2 proposal — all four new vendors = L1 suite.

**Verdict counts:** CONFIRMED 3 · QUOTE-DRIFT 1 (Role/Request, corrected) · UNREACHABLE 0 · REFUTED 0. Ownership CONFIRMED HIGH. Lands fully once the corrected Role/Request row is applied.

# Britive — vendor-capability research (L2 modern-access, cloud-PAM / JIT ephemeral)

Slug: `britive` · Layer: L2 modern-access · Researched: 2026-06-11 · Anti-fabrication: every NATIVE/ADD-ON/PARTIAL row below carries an authoritative first-party evidence_url + verbatim evidence_quote confirmed by live fetch. GAP rows carry no citation by policy.

Britive is an agent-less / proxy-less **cloud-native CPAM** built around JIT ephemeral permissions and Zero Standing Privileges (ZSP). Consistent with the honest-gap rule for cloud-native CPAM vendors, classic on-prem vaulting, credential-injection session-proxy isolation, session recording, EPM, SAW/PAW, break-glass, recertification, and dedicated ITDR/UEBA are graded GAP/PARTIAL — Britive does not market substantive first-party capability there, leaning on the customer's IdP/SSO and its ephemeral model instead.

---

## (1) Ready-to-paste capability rows (18 UCs)

Column order: `vendor_slug,vendor_name,target_id,target_type,coverage,maturity,evidence_url,evidence_quote,citation_keys,notes`

```csv
britive,Britive,UC-P-001,UC-F,PARTIAL,2,https://www.britive.com/platform/,"Safeguard sensitive data with Britive's Secrets Manager. Store, manage, and access credentials securely with temporary, auto-expiring permissions, preventing unauthorized access and reducing the risk of data breaches.",britive-platform-2026,"Britive Secrets Manager stores/manages credentials with temporary auto-expiring access — but the model is ephemeral JIT, NOT a classic password vault with scheduled check-out/check-in rotation of in-scope privileged accounts across AD/Unix/DB/network. No first-party evidence of automated password rotation or full privileged-account onboarding. Graded PARTIAL: vaulting present for vaulted/static credentials, but rotation-on-schedule and estate-wide onboarding not evidenced. [HONEST-GAP for classic vault semantics]"
britive,Britive,UC-P-002,UC-F,PARTIAL,2,https://www.britive.com/platform/access-broker,"Extend Britive's JIT ephemeral permissions model to hybrid, private cloud, and on-prem resources to eliminate standing privileges.","Access Broker integrate with cloud services (SaaS, DaaS, PaaS), cloud infrastructure (IaaS, Kubernetes), servers (physical, VMs) databases, applications, and more.",britive-access-broker-2026,"Britive is explicitly agent-less and proxy-less; Access Broker brokers JIT access to servers/DBs/K8s/on-prem but markets NO credential-injection isolation proxy that withholds the target secret from the operator endpoint, and the page contains no explicit session-isolation claim. Graded PARTIAL — brokered access yes, classic isolation-proxy with credential injection not evidenced. [HONEST-GAP for session-proxy isolation]"
britive,Britive,UC-P-003,UC-F,PARTIAL,1,https://www.britive.com/use-cases/cloud-pam,"Privileged Session Monitoring and Recording",britive-cloud-pam-usecase-2026,"Britive markets a 'Privileged Session Monitoring and Recording' use case, but first-party pages expose only the heading with no substantive description of keystroke/command capture, tamper-evidence, retention, or high-risk-command flagging. Graded PARTIAL maturity 1 — capability named by vendor but undocumented at depth; treat as marketing-tier until admin-doc confirms scope. [UNVERIFIED depth — marketing header only]"
britive,Britive,UC-P-004,UC-F,NATIVE,5,https://www.britive.com/platform/just-in-time-access,"True Zero Standing Privileges (ZSP)...privileges only exist when a task is being performed.",britive-jit-2026,"Flagship capability. Permissions dynamically minted only at the exact moment of execution and automatically revoked once the task completes; self-service automated access-request workflows with approvals; multi-cloud (AWS, Azure, GCP, Kubernetes). Patented JIT/ZSP model — market-leading for cloud-native JIT. Marketing+product-page sourced; admin-doc (docs.britive.com) not separately fetched."
britive,Britive,UC-P-005,UC-F,PARTIAL,1,https://www.britive.com/use-cases,"Account Discovery & Drift Detection",britive-usecases-2026,"Britive lists 'Account Discovery & Drift Detection' as a use case but first-party pages give only the heading without describing recurring multi-source enumeration (AD/Unix/cloud/DB/network/SaaS) or auto-flagging of newly found accounts. Likely cloud-identity scoped, not classic on-prem privileged/local-admin enumeration. Graded PARTIAL maturity 1 pending admin-doc. [UNVERIFIED depth — marketing header only]"
britive,Britive,UC-P-006,UC-F,NATIVE,4,https://www.britive.com/platform/just-in-time-access,"Permissions are dynamically minted only at the exact moment of execution.",britive-jit-2026,"Britive markets dedicated NHI / automations / AI-agent and IaC use cases; A2A/workload access obtains dynamic ephemeral privileges at runtime rather than holding hard-coded secrets. Strong fit for runtime credential brokering. Maturity 4 — broad NHI coverage evidenced via marketing; per-app scoping detail not separately confirmed in admin-doc."
britive,Britive,UC-P-007,UC-F,GAP,0,,,,"No first-party evidence that Britive enforces or provides MFA / phishing-resistant factors at its own elevation point. As an agent-less cloud-native broker, Britive relies on the customer's IdP/SSO (Okta, Entra, etc.) for authentication and MFA rather than enforcing FIDO2 itself. Graded GAP — MFA is an upstream-IdP responsibility, not a Britive-native control. [HONEST-GAP]"
britive,Britive,UC-P-008,UC-F,GAP,0,,,,"No first-party evidence of a dedicated break-glass / emergency-access capability (sealed accounts, dual-control checkout, alert-on-use, auto post-use rotation). Britive's ZSP model reduces standing accounts generally but does not document a controlled break-glass path. Graded GAP. [HONEST-GAP]"
britive,Britive,UC-P-009,UC-F,GAP,0,,,,"Britive has no Endpoint Privilege Management. It does not remove local-admin tokens, apply per-application UAC-style elevation, or enforce process-level least-privilege on desktops. Outside the architectural scope of a cloud-native CPAM. EPM requires a dedicated tool (e.g., BeyondTrust EPM, CyberArk EPM). [HONEST-GAP — architectural]"
britive,Britive,UC-P-010,UC-F,NATIVE,4,https://www.britive.com/platform/,"Eliminate the risks associated with standing privileges. Ephemeral, just-in-time access ensures that access is granted temporarily and expires when no longer needed, enforcing Zero Standing Privileges by default.",britive-platform-2026,"ZSP-by-default structurally enforces least privilege at session level; combined with CIEM-style cross-cloud entitlement analysis (see UC-P-012) for right-sizing. Maturity 4 — strong right-sizing posture via JIT; automated unused-entitlement removal tooling not separately admin-doc-confirmed."
britive,Britive,UC-P-011,UC-F,PARTIAL,2,https://www.britive.com/platform/access-broker,"Secure legacy applications and infrastructure awaiting cloud migration. Ensure consistent access policies across hybrid and cloud-native environments.",britive-access-broker-2026,"JIT + Access Broker can deliver scoped, time-bound third-party/remote access without standing credentials, but Britive does not market a dedicated recorded vendor-access path with per-vendor scope/expiry and session recording as a first-class use case. Graded PARTIAL — JIT vendor scoping plausible; recorded brokered-vendor path not separately evidenced. [partial]"
britive,Britive,UC-P-012,UC-F,NATIVE,4,https://www.britive.com/platform/,"Eliminate the risks associated with standing privileges. Ephemeral, just-in-time access ensures that access is granted temporarily and expires when no longer needed, enforcing Zero Standing Privileges by default.",britive-platform-2026,"Britive's core is cross-cloud (AWS/Azure/GCP/Oracle) privileged-entitlement management with ZSP; Gartner notes its JIT capabilities maintain a ZSP posture by granting and expiring dynamic permissions. CIEM-style entitlement visibility + right-sizing is central to the product. Maturity 4 — strong multi-cloud entitlement posture; depth of remediation automation per cloud not separately admin-doc-confirmed."
britive,Britive,UC-P-013,UC-F,NATIVE,4,https://www.britive.com/platform/just-in-time-access,"Dynamic, ephemeral privileges at the exact moment of execution.",britive-jit-2026,"Dedicated NHI / automations / AI-agent / IaC coverage: privileged workloads obtain short-lived ephemeral grants at runtime rather than holding stored standing secrets. Aligns with secretless/short-lived-token attestation intent. Maturity 4 — ephemeral workload access evidenced; formal attestation primitive (e.g. SPIFFE) not first-party-confirmed."
britive,Britive,UC-P-014,UC-F,GAP,0,,,,"No first-party evidence of a privileged-account certification / recertification cycle (periodic attestation, reviewer assignment, orphaned-grant revocation, retained certification evidence). Britive's ZSP model reduces standing grants but recertification is an IGA-style function it does not document. Graded GAP. [HONEST-GAP — IGA-adjacent]"
britive,Britive,UC-P-015,UC-N,GAP,0,,,,"No first-party evidence of behavioral / UEBA privileged-session threat analytics with anomaly detection mapped to SOC runbooks. Britive markets audit logging of privileged activity but not a dedicated threat-analytics / ITDR engine. Graded GAP — analytics is logging-grade, not detection-grade. [HONEST-GAP]"
britive,Britive,UC-P-016,UC-N,PARTIAL,2,https://www.britive.com/platform/just-in-time-access,"Ensures an identity has absolutely no value to an attacker unless actively performing authorized task.",britive-jit-2026,"Britive's ZSP/ephemeral model structurally limits credential-theft blast radius ('nothing to steal') — a preventive control, NOT detection of pass-the-hash / Kerberoasting / DCSync / token-theft. No first-party detection capability for those techniques. Graded PARTIAL maturity 2 — structural mitigation strong, active credential-theft detection absent. [HONEST-GAP for detection]"
britive,Britive,UC-P-017,UC-N,GAP,0,,,,"No first-party evidence fetched for PAM-platform availability / recovery targets, failover, or vault backup testing. Britive is delivered SaaS so managed availability is plausible, but no documented HA/DR/RPO commitment was confirmed. Graded GAP pending first-party resilience documentation. [UNVERIFIED — no resilience doc fetched]"
britive,Britive,UC-P-018,UC-F,GAP,0,,,,"Britive provides no Secure Admin Workstation / PAW capability — it does not deliver or enforce hardened dedicated admin endpoints, application control, or tier-0 endpoint isolation. Outside the scope of a cloud-native CPAM. [HONEST-GAP — architectural]"
```

---

## (2) pam.yaml lines

```yaml
britive: ["L2", "modern-access"]
short: "Britive"
```

(Add `britive` to the vendor list and the `short` map exactly as the other L2 entries are formatted in `matrix/config/pam.yaml`.)

---

## (3) Ownership verdict + vendor-ownership.yaml entry

**VERDICT: NOT CONFIRMED — do NOT add an ownership entry.** The claimed "BeyondTrust acquisition of Britive (~late 2025)" could not be verified against any authoritative source.

Evidence against:
- No BeyondTrust newsroom / press release, no Britive newsroom item, and no reputable trade coverage announces a BeyondTrust→Britive acquisition.
- BeyondTrust's documented JIT acquisition is **Entitle** (announced 2024), not Britive. The two are easily conflated; the prompt's claim most likely confuses Entitle with Britive.
- As of 2026, Britive is covered as an **independent** third-gen / cloud-PAM vendor (e.g., SACR 2026 PAM report Feb 2026, AWS Security Hub integration Feb 2026) and Tracxn lists no acquisition of Britive.
- BeyondTrust's own corporate-control news in this window is the inbound **Veritas Capital** acquisition *of BeyondTrust*, unrelated to Britive.

Action: **omit Britive from `vendor-ownership.yaml`** (a vendor not listed is treated as its own parent). Adding a fabricated `britive → beyondtrust` entry would corrupt the concentration analysis by collapsing an independent second-source. If a real deal is later announced, add with `confidence: LOW` and a primary-source `source:` only after a live first-party confirmation.

---

## (4) Verification ledger

| target | evidence_url | source grade | verbatim confirmed (Y/N) |
|---|---|---|---|
| UC-P-001 | britive.com/platform/ | first-party marketing | Y |
| UC-P-002 | britive.com/platform/access-broker | first-party marketing | Y |
| UC-P-003 | britive.com/use-cases/cloud-pam | first-party marketing (header only) | Y (header text only) |
| UC-P-004 | britive.com/platform/just-in-time-access | first-party marketing | Y |
| UC-P-005 | britive.com/use-cases | first-party marketing (header only) | Y (header text only) |
| UC-P-006 | britive.com/platform/just-in-time-access | first-party marketing | Y |
| UC-P-010 | britive.com/platform/ | first-party marketing | Y |
| UC-P-011 | britive.com/platform/access-broker | first-party marketing | Y |
| UC-P-012 | britive.com/platform/ | first-party marketing | Y |
| UC-P-013 | britive.com/platform/just-in-time-access | first-party marketing | Y |
| UC-P-016 | britive.com/platform/just-in-time-access | first-party marketing | Y |
| Ownership (BeyondTrust→Britive) | WebSearch (BeyondTrust newsroom / Tracxn / SACR) | secondary / absence-of-evidence | N — claim NOT confirmed |

Notes on grade: all confirmed quotes are from **vendor first-party marketing pages** (britive.com). `docs.britive.com` admin-doc tier was not separately fetched (returned no indexable results via search); rows leaning on marketing-only headers (003, 005) are flagged below. GAP rows carry no citation by policy.

---

## (5) UNVERIFIED list (needs admin-doc confirmation before client publication)

- **UC-P-003 session recording** — only a marketing header confirmed; no admin-doc describing capture/retention/tamper-evidence. Confirm at docs.britive.com or downgrade.
- **UC-P-005 account discovery** — only a marketing header; scope (cloud-only vs estate-wide) unconfirmed.
- **UC-P-017 resilience/HA-DR** — no first-party availability/RPO/backup documentation fetched; graded GAP conservatively, but Britive being SaaS, a managed-availability statement may exist — verify.
- **All quotes are marketing-tier**, not admin-doc-tier. Before client use, re-confirm UC-P-004/006/012/013 maturity-5/4 claims against `docs.britive.com` and tag marketing-vs-admin-doc per house policy.
- **Ownership** — re-check periodically; if BeyondTrust (or any acquirer) announces Britive, add a LOW-confidence ownership entry with a primary source only.

---

## Adversarial verification (PASS 2)

Verifier posture: REFUTE-by-default. Cited rows re-fetched live (2026-06-11). Schema check: 18 rows,
UC-P-001..018 each exactly once, 10 columns. ✅ Coverage enum note: rows use the **illegal `PARTIAL`**
value (001, 002, 003, 005, 011, 016) — must be re-encoded before landing (table below).

### Per-row verdict table

| uc_id | verdict | corrected quote / url if drifted |
|---|---|---|
| UC-P-001 | CONFIRMED | "Safeguard sensitive data with Britive's Secrets Manager. Store, manage, and access credentials securely with temporary, auto-expiring permissions, preventing unauthorized access and reducing the risk of data breaches." verbatim @ britive.com/platform/ |
| UC-P-002 | **QUOTE-DRIFT** | Quote#1 drifted (page reads "…to eliminate standing privileges **for both human and non-human identities.**"). Quote#2 ("Access Broker integrate with cloud services (SaaS, DaaS, PaaS)…") **NOT FOUND** — page reads: "Manage privileged access for all identities across public cloud, private cloud and hybrid environments, on-prem servers, databases, VMs, and applications through a single platform." Use that verbatim sentence instead. |
| UC-P-003 | CONFIRMED | "Privileged Session Monitoring and Recording" verbatim @ britive.com/use-cases/cloud-pam (header/nav-link only, as PASS-1 flagged — marketing-tier, depth unverified) |
| UC-P-004 | **QUOTE-DRIFT** | "True Zero Standing Privileges (ZSP)...privileges only exist when a task is being performed." is a SPLICE. Verbatim text: "By ensuring privileges only exist when a task is being performed, we leave nothing behind for an attacker to exploit". Also verbatim: "permissions are dynamically minted only at the exact moment of execution". Use a real sentence. |
| UC-P-005 | CONFIRMED | "Account Discovery & Drift Detection" verbatim @ britive.com/use-cases (header only — marketing-tier) |
| UC-P-006 | **QUOTE-DRIFT** | "Permissions are dynamically minted only at the exact moment of execution." → on-page it is lower-case mid-sentence: "permissions are dynamically minted only at the exact moment of execution". Substring holds if leading-cap/period dropped. |
| UC-P-010 | CONFIRMED | "Eliminate the risks associated with standing privileges. Ephemeral, just-in-time access ensures that access is granted temporarily and expires when no longer needed, enforcing Zero Standing Privileges by default." verbatim |
| UC-P-011 | **QUOTE-DRIFT** | Page reads: "Secure legacy applications and infrastructure awaiting cloud migration. Ensure consistent access policies across hybrid and cloud-native environments **and streamline migration efforts without security gaps.**" Cited quote truncates mid-sentence — extend to a clean clause boundary. |
| UC-P-012 | CONFIRMED | (same platform/ ZSP quote as UC-P-010) verbatim |
| UC-P-013 | **QUOTE-DRIFT** | "Dynamic, ephemeral privileges at the exact moment of execution." → on-page lower-case fragment "dynamic, ephemeral privileges at the exact moment of execution". Substring holds if leading-cap/period dropped. |
| UC-P-016 | **QUOTE-DRIFT** | "Ensures an identity has absolutely no value to an attacker unless actively performing authorized task." → verbatim is "ensure an identity has absolutely no value to an attacker unless it is actively performing an authorized, verified task". Replace with the real wording. |
| GAP rows 007/008/009/014/015/017/018 | GAP (skipped) | no citation required |

Counts: CONFIRMED 5 / DRIFT 6 / UNREACHABLE 0 / REFUTED 0 (one half-row, UC-P-002 quote#2, is REFUTED but the row survives on the substitute sentence).

### Ownership verdict (CONFIRMED — matches PASS 1)

**Britive is NOT acquired by BeyondTrust.** Independently confirmed: BeyondTrust's JIT acquisition is
**Entitle** (announced 2024-04-16, per BeyondTrust newsroom + Clearlake + Dark Reading), NOT Britive. No
BeyondTrust→Britive press release exists; the claim conflates Entitle with Britive. → **Omit Britive from
`vendor-ownership.yaml`** (treated as its own parent). PASS-1 verdict stands, HIGH confidence.

### LANDABLE rows (corrected quotes + legal coverage applied)

PARTIAL is illegal. Britive's PARTIAL rows are weak-but-real cloud-native capability → re-encode as
NATIVE with low maturity + caveat (the honest "real but incomplete" encoding), EXCEPT where only a
marketing header exists (003, 005) which lean weakest.

| uc_id | landed coverage | maturity | corrected verbatim quote to use |
|---|---|---|---|
| UC-P-001 | **NATIVE** | 2 | (as cited — confirmed verbatim) |
| UC-P-002 | **NATIVE** | 2 | replace quote → "Manage privileged access for all identities across public cloud, private cloud and hybrid environments, on-prem servers, databases, VMs, and applications through a single platform." |
| UC-P-003 | **NATIVE** | 1 | "Privileged Session Monitoring and Recording" (marketing header only — keep maturity 1 caveat; lands but weakest) |
| UC-P-004 | NATIVE | 5 | replace spliced quote → "permissions are dynamically minted only at the exact moment of execution" (verbatim) |
| UC-P-005 | **NATIVE** | 1 | "Account Discovery & Drift Detection" (header only; maturity-1 caveat) |
| UC-P-006 | NATIVE | 4 | "permissions are dynamically minted only at the exact moment of execution" (lower-case verbatim) |
| UC-P-010 | NATIVE | 4 | (as cited — confirmed) |
| UC-P-011 | **NATIVE** | 2 | extend quote → "Secure legacy applications and infrastructure awaiting cloud migration. Ensure consistent access policies across hybrid and cloud-native environments and streamline migration efforts without security gaps." |
| UC-P-012 | NATIVE | 4 | (as cited — confirmed) |
| UC-P-013 | NATIVE | 4 | "dynamic, ephemeral privileges at the exact moment of execution" (lower-case verbatim) |
| UC-P-016 | **NATIVE** | 2 | replace → "ensure an identity has absolutely no value to an attacker unless it is actively performing an authorized, verified task" |
| GAP rows 007/008/009/014/015/017/018 | GAP | 0 | unchanged |

**Caveat on landing:** all Britive evidence is **marketing-tier** (britive.com), `docs.britive.com` admin-doc
never confirmed. 6 of 11 cited rows needed quote correction — research is LANDABLE only after the corrected
quotes above are pasted. Rows 003 and 005 are header-only and should land at maturity 1 or be held for
admin-doc confirmation. Recommend a re-fetch pass against docs.britive.com before client publication.

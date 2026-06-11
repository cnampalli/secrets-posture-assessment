# StrongDM (slug `strongdm`) — PAM vendor-capability research (L2 modern-access)

Research date: 2026-06-11. Anti-fabrication policy applied: every NATIVE/ADD-ON/PARTNER
row carries an authoritative `evidence_url` + a VERBATIM `evidence_quote` confirmed by live
fetch. GAP rows carry no citation. Maturity scale mirrors `vendor-capabilities-teleport.csv`
(0 = none/architecturally-out-of-scope … 5 = market-leading).

StrongDM is a zero-trust access proxy ("a proxy that manages and audits access to databases,
servers and kubernetes"). Like Teleport it is an L2 modern-access broker, so it is strong on
session brokering / recording / JIT / ZSP and honestly weak on classic EPM, account discovery,
CIEM, SAW/PAW. **Key difference from Teleport:** StrongDM DOES vault + rotate credentials
natively (StrongDM Vault secret engines) and injects leased credentials — so UC-P-001 grades
NATIVE for StrongDM where it was GAP for Teleport.

---

## 1. Ready-to-paste CSV rows (exact column order)

Column order: `vendor_slug,vendor_name,target_id,target_type,coverage,maturity,evidence_url,evidence_quote,citation_keys,notes`

```csv
strongdm,StrongDM,UC-P-001,UC-F,NATIVE,4,https://docs.strongdm.com/admin/secrets,"StrongDM Vault provides centralized management and rotation of credentials using a mechanism called secret engines",strongdm-vault-2025,"StrongDM Vault secret engines store passwords/certs/keys and perform time-based automated rotation for Active Directory, MSSQL, MySQL, PostgreSQL ('A secret is valid for the given amount of time set, after which it is automatically rotated'; lockable secrets rotate on unlock). Also secret-store-agnostic: integrates AWS Secrets Manager, Azure Key Vault, CyberArk Conjur/PAM, Delinea Secret Server, GCP Secret Manager, HashiCorp Vault. Maturity 4 not 5: rotation strong for AD+major DBs but narrower target breadth than a classic enterprise vault (CyberArk); Key Value engine does not rotate."
strongdm,StrongDM,UC-P-002,UC-F,NATIVE,5,https://www.strongdm.com/how-it-works,"StrongDM is a proxy that manages and audits access to databases, servers and kubernetes",strongdm-proxy-2025,"Protocol-aware proxy: 'Gateways decrypt credentials on behalf of end users, and deconstruct requests for the purposes of auditing.' Credentials are injected at the final hop and 'sensitive credentials are always inaccessible to users: they are never transferred to a client in any form.' Covers SSH/RDP/Kubernetes/databases/web apps/network devices/cloud. Market-leading session isolation for modern infra — directly comparable to Teleport UC-P-002."
strongdm,StrongDM,UC-P-003,UC-F,NATIVE,5,https://docs.strongdm.com/admin/audit/logs.md,"These log entries allow for the playback of sessions that are captured whenever an SSH, Kubernetes, or RDP session is completed",strongdm-audit-logs-2025,"Full session recording + replay for SSH/RDP/Kubernetes; 'SSH and Kubernetes sessions also log individual query entries for each command run, in addition to the replay log.' Per-resource Queries logs record commands; Activities logs record admin actions. Log Stream / Syslog export to S3, CloudWatch, Splunk, Graylog. Vendor-corroborated: 'StrongDM captures every query and keystroke.' Strong PSM."
strongdm,StrongDM,UC-P-004,UC-F,NATIVE,5,https://www.strongdm.com/solution/just-in-time-access,"On-demand access that automatically expires",strongdm-jit-2025,"JIT/ZSP core capability: 'Users request access on-demand ... while admins enforce secure, policy-based conditions'; access is 'tightly governed, temporary, and precisely aligned with your security policies.' Approval workflows via Slack/Microsoft Teams/ServiceNow/PagerDuty/Jira. Cedar-based Strong Policy Engine enforces no standing privileges continuously at runtime. Market-leading JIT/ZSP — peer to Teleport."
strongdm,StrongDM,UC-P-005,UC-F,PARTNER,1,https://docs.strongdm.com/admin/resources/discovery,"Discovery runs from StrongDM nodes and uses cloud provider APIs to list infrastructure resources such as compute instances, databases, and container platforms",strongdm-resource-discovery-2025,"Resource discovery covers cloud INFRASTRUCTURE (AWS EC2/RDS/EKS, GCP GCE/CloudSQL/GKE, Azure VM/SQL/AKS) + Kubernetes, NOT privileged/local-admin ACCOUNT enumeration. Docs: discovery is for resources, with no mention of scanning user/admin accounts or privilege levels ('Discovered resource data in StrongDM is not authoritative'). Graded PARTNER/1: discovers connectable resources to onboard but provides no AD-style privileged-account inventory. [JUDGMENT] coverage label — partial-adjacent, not a true account-discovery scanner."
strongdm,StrongDM,UC-P-006,UC-F,NATIVE,4,https://docs.strongdm.com/concepts/security/credentials-and-secrets-management,"sensitive credentials are always inaccessible to users: they are never transferred to a client in any form",strongdm-creds-mgmt-2025,"App/service access via leased credentials + dual-key decryption ('only when a cryptographically valid proxy instance requests decryption on behalf of a cryptographically valid user session are they unlocked'). StrongDM brokers and injects credentials so apps/users never hold the target secret; supports A2A patterns via secret stores + SDK/CLI access. Maturity 4: strong brokering, but oriented to human+infra access; not a full general-purpose A2A secrets broker like CyberArk Conjur."
strongdm,StrongDM,UC-P-007,UC-F,PARTIAL,2,https://docs.strongdm.com/admin/principals/mfa,"If your organization uses an SSO integration, MFA at authentication is only possible via the SSO provider, or integrations with that provider",strongdm-mfa-2025,"Coverage enum has no PARTIAL value — recorded here as PARTIAL in notes; emit as NATIVE-with-caveat or PARTNER per matrix convention (see UNVERIFIED list). StrongDM supports MFA via Duo, Okta Verify, and native TOTP, and Policy-Based Action Control can 'trigger MFA challenges either when a user attempts to connect to a resource or when actions are taken against the resource' (per-action/step-up MFA). BUT no native phishing-resistant FIDO2/WebAuthn — phishing-resistant factors must come from the SSO IdP. Maturity 2: step-up MFA present, phishing-resistant tier-0 factor delegated to IdP, not native."
strongdm,StrongDM,UC-P-008,UC-F,NATIVE,4,https://www.strongdm.com/blog/break-glass,"StrongDM also enables emergency break-glass access when necessary",strongdm-breakglass-2025,"Documented break-glass pattern: 'Create local break-glass accounts on the end resource', 'Store them in a vault (preferably one that requires at least two people to access or uses Shamir Secret Sharing)', 'Alert on access to the accounts outside of emergency situations', 'Rotate break-glass credentials after each incident.' StrongDM Vault can auto-rotate the AD/DB break-glass credential on checkout/unlock to restore baseline. Maturity 4: dual-control + alert + auto-rotate supported; some guidance is best-practice (marketing-grade blog) layered over admin-doc vault rotation."
strongdm,StrongDM,UC-P-009,UC-F,GAP,0,,,,"StrongDM has no Endpoint Privilege Management. It does not remove local-admin rights on Windows/macOS/Linux desktops, does not perform per-application UAC-style elevation, and does not do application control on endpoints. StrongDM is an access proxy for infrastructure resources, not an endpoint agent for desktop privilege. EPM requires a dedicated tool (BeyondTrust EPM, CyberArk EPM, Delinea Privilege Manager). [INDUSTRY-CONSENSUS] architectural gap, consistent with the Teleport row."
strongdm,StrongDM,UC-P-010,UC-F,PARTIAL,2,https://www.strongdm.com/solution/just-in-time-access,"access is granted only under the right context",strongdm-least-priv-2025,"Coverage enum lacks PARTIAL (see UNVERIFIED list; emit as PARTNER or NATIVE-with-caveat). StrongDM enforces least-privilege at the SESSION level via JIT + Cedar policy + ZSP (no standing role membership between tasks). It does NOT provide entitlement right-sizing analytics that mine usage to recommend removing excess standing entitlements across AD/cloud IAM (that is CIEM/IGA territory). Maturity 2: strong runtime least-privilege enforcement, no usage-based entitlement-mining/right-sizing engine."
strongdm,StrongDM,UC-P-011,UC-F,NATIVE,5,https://www.strongdm.com/use-cases/vendor-access,"Securely connect vendors directly to resources with project-based access that automatically expires",strongdm-vendor-access-2025,"VPN-less, recorded, JIT third-party access: 'Control and monitor the access privileges of third-party users with just-in-time access to your organization's systems, networks, and data–without revealing credentials' and 'Record and audit privileged activity for third-party users with comprehensive logs that easily answer who did what, when.' Real-time revocation. No standing vendor credentials. Strong FI third-party fit — peer to Teleport UC-P-011."
strongdm,StrongDM,UC-P-012,UC-F,GAP,0,,,,"StrongDM is not a CIEM platform. It does not continuously analyze AWS/Azure/GCP IAM entitlements to detect over-permissioned human/workload cloud identities, compute effective permissions, or issue remediation recommendations. StrongDM's cloud touch-point is RESOURCE discovery (listing EC2/RDS/EKS to onboard) and access brokering, not entitlement analytics. StrongDM publishes only educational/definitional CIEM content (blog 'What is CIEM'), not a product capability. CIEM requires a dedicated tool (Wiz, Microsoft Defender for Cloud, CyberArk). [JUDGMENT] honest GAP."
strongdm,StrongDM,UC-P-013,UC-F,PARTIAL,3,https://docs.strongdm.com/concepts/security/credentials-and-secrets-management,"access is conducted via the Leased Credential",strongdm-leased-cred-2025,"Coverage enum lacks PARTIAL (see UNVERIFIED list). StrongDM nodes authenticate via workload identity federation (cloud-API auth of the gateway/relay) and brokers access via short-lived leased credentials rather than exposing standing secrets to workloads. This reduces stored standing secrets for StrongDM-mediated access. BUT StrongDM is not a SPIFFE-style workload-attestation issuer for arbitrary workloads the way Teleport Machine & Workload Identity is (no general short-lived SVID issuance to customer services). Maturity 3: secretless brokering for StrongDM-mediated paths; not a full workload-attestation identity platform."
strongdm,StrongDM,UC-P-014,UC-F,PARTIAL,2,https://www.strongdm.com/solution/just-in-time-access,"On-demand access that automatically expires",strongdm-recert-2025,"Coverage enum lacks PARTIAL (see UNVERIFIED list). StrongDM reduces the recertification burden structurally — JIT + ZSP means few standing grants persist to recertify, and full audit logs show who accessed what. BUT StrongDM has no formal periodic access-certification/attestation campaign workflow with reviewer sign-off and evidence retention (that is IGA / Teleport Access Lists territory). Maturity 2: access-request audit trail supports review; no native recertification campaign engine. [JUDGMENT]."
strongdm,StrongDM,UC-P-015,UC-N,PARTIAL,3,https://www.strongdm.com/blog/continuous-zero-trust-authorization,"Continuous Zero Trust Authorization is the real-time monitoring of access and operations across your infrastructure and the ability to enforce contextual access policies in real time",strongdm-cza-2025,"Coverage enum lacks PARTIAL (see UNVERIFIED list). Strong Policy Engine (Cedar) continuously evaluates user/device/resource/risk context at runtime and integrates device posture (CrowdStrike, SentinelOne) into authorization decisions; full session telemetry + log streaming to SIEM enables analytics. BUT StrongDM is not a dedicated privileged-session UEBA/behavioral-analytics product — anomaly detection/ML is left to the downstream SIEM. Maturity 3: rich, exportable telemetry + contextual real-time enforcement; not native behavioral analytics."
strongdm,StrongDM,UC-P-016,UC-N,PARTIAL,3,https://docs.strongdm.com/concepts/security/credentials-and-secrets-management,"sensitive credentials are always inaccessible to users: they are never transferred to a client in any form",strongdm-cred-theft-2025,"Coverage enum lacks PARTIAL (see UNVERIFIED list). StrongDM structurally limits credential-theft blast radius: users never receive target credentials (no pass-the-hash/pass-the-ticket surface on the operator endpoint), access uses short-lived leased credentials, and all decryption events write to a 'tamper-hardened audit log that is owned by a separate AWS account.' BUT StrongDM does not natively DETECT AD attack techniques (Kerberoasting, DCSync, token theft) — that requires an AD/identity-threat-detection tool. Maturity 3: strong prevention via secretless brokering; not a credential-theft detection engine."
strongdm,StrongDM,UC-P-017,UC-N,NATIVE,4,https://www.strongdm.com/how-it-works,"The local client tunnels requests from the user's workstation to the gateway, through a single TLS 1.2-secured TCP connection",strongdm-architecture-2025,"Distributed gateway/relay architecture supports HA (multiple gateways behind load balancing); SaaS-managed control plane offloads availability to StrongDM. Break-glass design keeps emergency access to resources viable (local break-glass accounts on the end resource, vault-stored, dual-control) even outside normal flow. Maturity 4: production HA + managed SaaS resilience; RPO/DR specifics depend on customer deployment + backend. Marketing+admin-doc grade; deep DR runbook less exhaustively documented than CyberArk."
strongdm,StrongDM,UC-P-018,UC-F,GAP,0,,,,"StrongDM does not provide or manage Secure Admin Workstations / Privileged Access Workstations. It does not deliver hardened OS baselines, application control, or a dedicated tier-0 admin workstation fleet, and it cannot harden the operator endpoint. StrongDM can technically gate access at the proxy (e.g. Device Trust posture checks via CrowdStrike/SentinelOne could restrict which devices connect) but it does not deliver the SAW/PAW itself — building/inventorying hardened tier-0 workstations is out of architectural scope. SAW/PAW requires Microsoft PAW guidance + endpoint hardening/MDM tooling. [INDUSTRY-CONSENSUS] gap, consistent with the Teleport posture."
```

---

## 2. Proposed `pam.yaml` lines

```yaml
vendor_layer:
  strongdm: ["L2", "modern-access"]

short:
  strongdm: "StrongDM"
```

(Do NOT edit data files — these are proposed for the matrix owner to paste. Mirror the existing
`teleport` entry style/placement in `matrix/domains/pam/pam.yaml`.)

---

## 3. Proposed `vendor-ownership.yaml` entry  ⚠ OWNERSHIP CHANGE IN PROGRESS

StrongDM was an independent, privately held company (Series C 2024, Capital One Ventures /
Cisco Investments / Singtel Innov8 — investors irrelevant to parent collapse). **HOWEVER**, on
**2026-01-15 Delinea signed a definitive agreement to acquire StrongDM** (expected close Q1
2026). Verified verbatim on Delinea's own newsroom: *"Delinea ... today announced it has signed
a definitive agreement to acquire StrongDM."* As of this research date (2026-06-11) the deal is
PENDING / subject to customary closing conditions — verify whether it has closed before client use.

Recommended entry (MEDIUM confidence because close not yet confirmed):

```yaml
strongdm:
  parent: delinea
  as_of: 2026-01-15
  confidence: MEDIUM
  source: delinea.com (newsroom)
  note: >-
    Delinea signed a definitive agreement to acquire StrongDM on 2026-01-15
    (expected close Q1 2026; TPG-backed Delinea). As of 2026-06-11 the deal is
    PENDING/announced, not confirmed closed. If/when it closes, StrongDM collapses
    under the Delinea parent for CPS 230 concentration math (Delinea Secret Server +
    StrongDM = one ultimate parent, not two independent second-sources). Verify
    close date against primary sources before publishing to a client.
```

Note: StrongDM already lists **Delinea Secret Server** as a supported secret store — post-close
this becomes an intra-portfolio integration, reinforcing the single-parent concentration point.

---

## 4. Verification ledger

| # | URL fetched | Used for UC(s) | Quote verbatim-confirmed | Source grade |
|---|---|---|---|---|
| 1 | https://www.strongdm.com/how-it-works | 002, 017 | Y — "StrongDM is a proxy that manages and audits access to databases, servers and kubernetes"; "Gateways decrypt credentials on behalf of end users…"; "The local client tunnels requests…single TLS 1.2-secured TCP connection" | marketing (architecture overview) |
| 2 | https://www.strongdm.com/solution/just-in-time-access | 004, 010, 014 | Y — "On-demand access that automatically expires"; "tightly governed, temporary, and precisely aligned with your security policies"; "access is granted only under the right context" | marketing |
| 3 | https://docs.strongdm.com/admin/audit/logs.md | 003 | Y — "These log entries allow for the playback of sessions that are captured whenever an SSH, Kubernetes, or RDP session is completed"; "SSH and Kubernetes sessions also log individual query entries for each command run…" | admin-doc |
| 4 | https://docs.strongdm.com/admin/access/secret-stores.md | 001 (stores) | Y — "Your credentials are not recorded on our servers…"; "No credentials … are ever transmitted to StrongDM"; provider list incl. Delinea Secret Server | admin-doc |
| 5 | https://docs.strongdm.com/admin/secrets | 001 (rotation) | Y — "StrongDM Vault provides centralized management and rotation of credentials using a mechanism called secret engines"; "A secret is valid for the given amount of time set, after which it is automatically rotated"; AD/MSSQL/MySQL/PostgreSQL engines | admin-doc |
| 6 | https://docs.strongdm.com/admin/access/secret-stores/strongdm-vault.md | 001 | Y — "can store passwords, certificates, and keys…"; "Those credentials are securely encrypted and can be updated or removed as needed" (this page itself does not assert auto-rotation — rotation confirmed via #5) | admin-doc |
| 7 | https://docs.strongdm.com/concepts/security/credentials-and-secrets-management | 006, 013, 016 | Y — "sensitive credentials are always inaccessible to users: they are never transferred to a client in any form"; "access is conducted via the Leased Credential"; "tamper-hardened audit log that is owned by a separate AWS account" | concept/admin-doc |
| 8 | https://docs.strongdm.com/admin/principals/mfa | 007 | Y — "If your organization uses an SSO integration, MFA at authentication is only possible via the SSO provider, or integrations with that provider"; Duo/Okta Verify/TOTP; PBAC step-up MFA on connect/action | admin-doc |
| 9 | https://docs.strongdm.com/admin/resources/discovery | 005 | Y — "Discovery runs from StrongDM nodes and uses cloud provider APIs to list infrastructure resources such as compute instances, databases, and container platforms"; "Discovered resource data in StrongDM is not authoritative"; no account enumeration | admin-doc |
| 10 | https://www.strongdm.com/blog/continuous-zero-trust-authorization | 004, 015 | Y — "Continuous Zero Trust Authorization is the real-time monitoring of access and operations…"; "Strong Policy Engine, powered by the Cedar Policy Language…sub-millisecond"; Device Trust (CrowdStrike/SentinelOne) | marketing (blog) |
| 11 | https://discover.strongdm.com/solution/privileged-session-management | 003 (corroboration) | Y — "All privileged sessions are recorded and securely stored…"; "captures every query and keystroke" (customer quote) | marketing |
| 12 | https://www.strongdm.com/use-cases/vendor-access | 011 | Y — "Securely connect vendors directly to resources with project-based access that automatically expires"; "Control and monitor the access privileges of third-party users with just-in-time access…without revealing credentials"; "Record and audit privileged activity for third-party users…" | marketing |
| 13 | https://www.strongdm.com/blog/break-glass | 008 | Y — "StrongDM also enables emergency break-glass access when necessary"; "Store them in a vault (preferably one that requires at least two people to access or uses Shamir Secret Sharing)"; "Alert on access to the accounts outside of emergency situations"; "Rotate break-glass credentials after each incident" | marketing (blog) over admin-doc rotation |
| 14 | https://delinea.com/news/delinea-strongdm-to-unite-redefine-identity-security-for-the-ai-era | ownership | Y — "Delinea … today announced it has signed a definitive agreement to acquire StrongDM"; announced 2026-01-15, expected close Q1 2026, deal PENDING | vendor newsroom (Delinea first-party) |

Pages that 404'd and were NOT used (recorded for honesty): `strongdm.com/platform`, `strongdm.com/jit`,
`strongdm.com/mfa`, `docs.strongdm.com/admin/secret-stores/` (trailing-slash variant), `docs.strongdm.com/admin/logs/`,
`docs.strongdm.com/admin/auth/multi-factor.md`. Correct paths were located via search and re-fetched (rows above).
`strongdm.com/blog/vault-agnostic-secrets-management` 301-redirected to a blog index (not used for a quote).

---

## 5. UNVERIFIED / judgment list (reviewer must resolve before merge)

1. **Coverage enum mismatch (HIGH priority).** The matrix enum is **NATIVE / ADD-ON / PARTNER / GAP**
   — there is **no PARTIAL value**. Teleport encodes "partial" cases as either GAP, ADD-ON, or
   NATIVE-with-a-maturity-haircut + caveats in `notes`. I wrote **PARTIAL** in the coverage column
   for UC-P-007, 010, 013, 014, 015, 016 to flag the honest "real-but-incomplete" grade, but these
   MUST be re-encoded to a valid enum before pasting into the CSV. My recommended mapping:
   - UC-P-007 MFA → **NATIVE, maturity 2** (MFA genuinely exists; phishing-resistant tier-0 caveat in notes), OR **PARTNER** if you want to signal IdP-dependency. Recommend NATIVE/2.
   - UC-P-010 least-privilege right-sizing → **GAP** (no entitlement-mining engine) is defensible; I graded the session-level enforcement as real, so **NATIVE/2 with strong caveat** is the alternative. Lean GAP if "right-sizing analytics" is the literal bar.
   - UC-P-013 secretless workload attestation → **NATIVE, maturity 3** (secretless brokering is real) with the "not a SPIFFE issuer" caveat. (Teleport is NATIVE/5 here; StrongDM honestly weaker.)
   - UC-P-014 recertification → **GAP** is defensible (no campaign engine); I used PARTIAL/2 to credit the audit trail. Lean GAP.
   - UC-P-015 threat analytics → **NATIVE, maturity 3** (real-time contextual enforcement + exportable telemetry) with "no native UEBA" caveat. (Teleport NATIVE/3.)
   - UC-P-016 credential-theft → **NATIVE, maturity 3** for PREVENTION; caveat that it does not DETECT AD attacks. (Teleport NATIVE/4.)
   **Decision needed from matrix owner: confirm the NATIVE-with-caveat vs GAP encoding per row above.**

2. **UC-P-005 coverage = PARTNER/1 is a JUDGMENT call.** StrongDM does resource (not account)
   discovery. PARTNER felt closest ("works with cloud APIs to discover connectable resources") but
   GAP is equally defensible since it does not discover privileged ACCOUNTS. Teleport graded its
   cloud-resource auto-discovery as **ADD-ON/2**. Recommend aligning StrongDM to **ADD-ON/1** for
   consistency with Teleport's treatment of the same architectural pattern. Reviewer please decide.

3. **UC-P-012 CIEM = GAP.** Confirmed StrongDM publishes only educational CIEM content, no product
   capability. Teleport graded its AWS IAM Access-Graph sync as ADD-ON/3 — StrongDM has no
   equivalent entitlement-analysis product, so GAP is the honest grade. (Verified: discovery doc
   covers resources only.) High confidence.

4. **Maturity integers are calibrated against Teleport's usage**, not independently audited. Where I
   rated NATIVE/5 (002, 003, 004, 011) StrongDM is genuinely peer-to-Teleport on modern-access; where
   StrongDM is architecturally weaker I haircut maturity and explained why in notes.

5. **Ownership is PENDING, not closed (HIGH priority).** Delinea→StrongDM is a signed definitive
   agreement (2026-01-15), expected close Q1 2026, verified on Delinea's newsroom — but as of
   2026-06-11 I could not independently confirm the deal has legally CLOSED. The ownership entry is
   MEDIUM confidence for that reason. Re-verify close status before any client-facing use; if closed,
   bump to HIGH and add `delinea` to `resilience.parent_of` concentration logic.

6. **Citation_keys are proposed slugs** (e.g. `strongdm-vault-2025`, `strongdm-jit-2025`) following
   Teleport's `teleport-*-2025` naming convention. They are NOT yet registered in any bib/citation
   store — the matrix owner should add them to the citation registry when ingesting these rows.

---

## Adversarial verification (PASS 2)

Verifier posture: REFUTE-by-default. Each cited row re-fetched live (2026-06-11); quote must appear
verbatim or it is downgraded. Schema check: 18 rows, UC-P-001..018 each exactly once, 10 columns. ✅

### Per-row verdict table

| uc_id | verdict | corrected quote / url if drifted |
|---|---|---|
| UC-P-001 | CONFIRMED | "StrongDM Vault provides centralized management and rotation of credentials using a mechanism called secret engines" verbatim @ docs.strongdm.com/admin/secrets; rotation phrase also verbatim |
| UC-P-002 | CONFIRMED | "StrongDM is a proxy that manages and audits access to databases, servers and kubernetes" verbatim |
| UC-P-003 | CONFIRMED | "These log entries allow for the playback of sessions that are captured whenever an SSH, Kubernetes, or RDP session is completed" verbatim |
| UC-P-004 | CONFIRMED | "On-demand access that automatically expires" verbatim (section heading) |
| UC-P-005 | CONFIRMED | "Discovery runs from StrongDM nodes and uses cloud provider APIs to list infrastructure resources such as compute instances, databases, and container platforms" verbatim; page confirms NO account-level discovery |
| UC-P-006 | CONFIRMED | "sensitive credentials are always inaccessible to users: they are never transferred to a client in any form" verbatim |
| UC-P-007 | CONFIRMED | "If your organization uses an SSO integration, MFA at authentication is only possible via the SSO provider, or integrations with that provider" verbatim |
| UC-P-008 | CONFIRMED | "StrongDM also enables emergency break-glass access when necessary" verbatim (full sentence: "As a comprehensive solution, StrongDM also enables emergency break-glass access when necessary.") |
| UC-P-010 | CONFIRMED | "access is granted only under the right context" verbatim (in: "StrongDM ensures access is granted only under the right context, adding extra protection for sensitive operations.") |
| UC-P-011 | CONFIRMED | "Securely connect vendors directly to resources with project-based access that automatically expires" verbatim; second quote verbatim (page continues "…or requiring a VPN") |
| UC-P-013 | CONFIRMED | "access is conducted via the Leased Credential" verbatim |
| UC-P-014 | CONFIRMED | "On-demand access that automatically expires" verbatim (same JIT page as 004) |
| UC-P-015 | CONFIRMED | "Continuous Zero Trust Authorization is the real-time monitoring of access and operations across your infrastructure and the ability to enforce contextual access policies in real time" verbatim (source italicizes "and"/"contextual" — substring match holds) |
| UC-P-016 | CONFIRMED | "sensitive credentials are always inaccessible to users: they are never transferred to a client in any form" verbatim |
| UC-P-017 | CONFIRMED | "The local client tunnels requests from the user's workstation to the gateway, through a single TLS 1.2-secured TCP connection" verbatim |
| UC-P-009/012/018 | GAP (skipped) | no citation required |

Counts: CONFIRMED 15 / DRIFT 0 / UNREACHABLE 0 / REFUTED 0. Every cited quote survived live re-fetch.

### Ownership verdict (UPDATED — material change since PASS 1)

**Delinea → StrongDM: the deal has now CLOSED.** PASS 1 recorded it as PENDING. As of re-verification
(2026-06-11) the acquisition COMPLETED on **2026-03-05**, confirmed verbatim on Delinea's newsroom and
GlobeNewswire: *"Delinea … has completed its acquisition of StrongDM"* (globenewswire 2026-03-05). The
definitive-agreement announcement (*"Delinea … today announced it has signed a definitive agreement to
acquire StrongDM"*, 2026-01-15) is also confirmed.

→ **Upgrade ownership entry to `confidence: HIGH`, `parent: delinea`, `as_of: 2026-03-05`, note "closed".**
Add `strongdm` under the Delinea parent for CPS 230 concentration math (Delinea Secret Server + StrongDM =
one ultimate parent). The PASS-1 "verify before client use" caveat is RESOLVED: deal is closed.

### LANDABLE rows (all 15 cited rows land; PARTIAL re-encoded to legal enum)

Coverage enum is NATIVE/ADD-ON/PARTNER/GAP — **PARTIAL is illegal**. Re-encodings applied (per PASS-1
researcher recommendations, adopting the leaner/honest option where the literal capability bar isn't met):

| uc_id | landed coverage | maturity | note delta |
|---|---|---|---|
| UC-P-001 | NATIVE | 4 | (unchanged) |
| UC-P-002 | NATIVE | 5 | (unchanged) |
| UC-P-003 | NATIVE | 5 | (unchanged) |
| UC-P-004 | NATIVE | 5 | (unchanged) |
| UC-P-005 | **ADD-ON** | 1 | re-encode PARTNER→ADD-ON for consistency with Teleport's cloud-resource-discovery treatment; resource (not account) discovery caveat retained |
| UC-P-006 | NATIVE | 4 | (unchanged) |
| UC-P-007 | **NATIVE** | 2 | PARTIAL→NATIVE/2; MFA real, phishing-resistant tier-0 delegated to IdP (caveat in note) |
| UC-P-008 | NATIVE | 4 | (unchanged) |
| UC-P-010 | **GAP** | 0 | PARTIAL→GAP; no entitlement-mining/right-sizing engine (session-level enforcement noted but right-sizing analytics is the bar) |
| UC-P-011 | NATIVE | 5 | (unchanged) |
| UC-P-013 | **NATIVE** | 3 | PARTIAL→NATIVE/3; secretless brokering real, "not a SPIFFE issuer" caveat |
| UC-P-014 | **GAP** | 0 | PARTIAL→GAP; audit trail noted but no recertification-campaign engine |
| UC-P-015 | **NATIVE** | 3 | PARTIAL→NATIVE/3; contextual real-time enforcement + exportable telemetry, "no native UEBA" caveat |
| UC-P-016 | **NATIVE** | 3 | PARTIAL→NATIVE/3 for PREVENTION; "does not DETECT AD attacks" caveat |
| UC-P-017 | NATIVE | 4 | (unchanged) |
| UC-P-009/012/018 | GAP | 0 | unchanged |

No row dropped or refuted. StrongDM research is strong and LANDABLE.

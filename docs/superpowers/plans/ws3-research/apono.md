# Apono (slug `apono`) — L2 modern-access — PAM vendor-capability research

Layer L2 (cloud-native JIT / cloud privilege governance). Modern cloud-access vendor: dynamic, just-in-time + just-enough permissions created at request time in the cloud's native policy language, auto-revoked on expiry. Classic vaulting / session-proxy / endpoint / SAW use-cases graded GAP or PARTIAL honestly. Anti-fabrication: every NATIVE/ADD-ON/PARTIAL row below carries a live-fetched first-party `evidence_url` + verbatim `evidence_quote`. GAP rows carry no citation.

---

## (1) Ready-to-paste rows — all 18 UCs
Column order: `vendor_slug,vendor_name,target_id,target_type,coverage,maturity,evidence_url,evidence_quote,citation_keys,notes`

```csv
apono,Apono,UC-P-001,UC-F,GAP,0,,,,"Apono is NOT a credential vault. It creates dynamic JIT permissions in the cloud's native policy language at request time rather than storing/rotating static privileged passwords or keys. Its connector explicitly avoids holding secrets — 'The Connector does not read, cache or store any secrets, nor does Apono need an account with admin privileges to function.' (docs.apono.io). Classical vaulting / check-in-check-out / scheduled password rotation requires a dedicated vault (e.g. CyberArk, HashiCorp Vault). Note: Apono does enforce password reset / credential rotation for managed DB-user grants, but this is per-grant cleanup, not an enterprise vault — insufficient for UC-P-001."
apono,Apono,UC-P-002,UC-F,GAP,0,,,,"Apono is not a session-isolation proxy. It grants/revokes native cloud and DB entitlements just-in-time but does not broker privileged sessions through a credential-injecting isolation proxy that hides the target secret from the operator endpoint; users connect with their own tooling once access is granted. Session brokering/isolation requires a proxy-architecture PAM (e.g. CyberArk, BeyondTrust, Teleport). [INDUSTRY-CONSENSUS] gap for proxy-based isolation."
apono,Apono,UC-P-003,UC-F,PARTIAL,2,https://docs.apono.io/docs/audits-and-reports/session-audit.md,"Session Audit records activity performed during privileged access sessions. When enabled, it captures text-based session activity","apono-session-audit-2025","PARTIAL — text-based session audit only, NOT full session recording. Captures SSH 'Commands, outputs, and session lifecycle events' and Kubernetes 'kubectl get, kubectl apply, kubectl delete' incl. kubectl exec; explicitly 'does not support... Session replay or video'. Database query capture not listed. No tamper-evident video playback, so falls short of UC-P-003 keystroke/command-recording-with-review expectations for SSH/k8s coverage only. Maturity 2."
apono,Apono,UC-P-004,UC-F,NATIVE,5,https://docs.apono.io/docs/getting-started/how-apono-works.md,"Three easy steps are what it takes to create Just-In-Time and Just Enough permissions","apono-jit-2025","Core differentiator. Access Flows answer 'Who should get access? What can they gain access to? What Actions? How Long? Who must Approve?' Access 'begins and ends according to Access Flow definition' and is 'automatically revoked when no longer needed', eliminating standing privilege. Market-leading cloud-native JIT / zero-standing-privilege. Maturity 5."
apono,Apono,UC-P-005,UC-F,PARTIAL,2,https://docs.apono.io/llms-full.txt,"Access Discovery helps you identify and remediate standing access","apono-access-discovery-2025","PARTIAL — Apono discovers cloud/DB/IAM principals and standing access ('tracking whether principals are active or dormant', flagging 'overprivileged principals for targeted remediation') across its 35+ integrated cloud/DB/k8s resource types. It does NOT perform classic AD/Unix/network/local-admin privileged-account enumeration across the on-prem estate. Cloud-scoped discovery only. Maturity 2. [verbatim quote drawn from docs llms-full.txt export]"
apono,Apono,UC-P-006,UC-F,GAP,0,,,,"Apono brokers human (and AI-agent) JIT access to cloud/DB resources; it is not an application-to-application credential broker / secrets API for hard-coded app credentials. Its connector 'does not read, cache or store any secrets'. A2A secret brokering requires a secrets manager (e.g. Conjur, HashiCorp Vault, AWS Secrets Manager). GAP."
apono,Apono,UC-P-007,UC-F,PARTIAL,3,https://docs.apono.io/docs/access-flows/access-flows/what-are-access-flows.md,"Identify users who can request access, and whether MFA is required to verify identities","apono-mfa-2025","PARTIAL — Apono can require MFA to verify the requester's identity at the access-request step and integrates with IdPs (Okta, Entra ID) that carry phishing-resistant factors. MFA is enforced at Apono's request/approval gate, not as a session-proxy challenge to every target, and phishing-resistant (FIDO2) enforcement depends on the upstream IdP rather than Apono natively. Functional for request-time MFA; relies on IdP for factor strength. Maturity 3."
apono,Apono,UC-P-008,UC-F,PARTIAL,3,https://docs.apono.io/llms-full.txt,"Apono's Access Flows prepare for contingencies, emergency access and regular maintenance","apono-breakglass-2025","PARTIAL — Apono supports emergency/break-glass access via dedicated Access Flows (auto-approval or expedited approval, time-bound, fully logged). It does not provide sealed dual-control break-glass vault accounts with mandatory post-use credential rotation in the classic PAM sense; controls are JIT-grant-based. Adequate for cloud emergency access, lighter than vault break-glass. Maturity 3. [verbatim quote from docs llms-full.txt export]"
apono,Apono,UC-P-009,UC-F,GAP,0,,,,"Apono has no Endpoint Privilege Management. It does not remove local-admin rights from workstations, perform per-application elevation (UAC/sudo control), or enforce process-level least privilege on endpoints. Outside architectural scope — EPM requires a dedicated tool (BeyondTrust EPM, CyberArk EPM). GAP."
apono,Apono,UC-P-010,UC-F,NATIVE,4,https://docs.apono.io/llms-full.txt,"flagging overprivileged principals for targeted remediation","apono-least-privilege-2025","Apono enforces least privilege structurally via just-enough JIT grants (no standing privilege) and surfaces excess/dormant entitlements through Access Discovery ('tracking whether principals are active or dormant'). Right-sizing recommendations + JIT enforcement together give strong least-privilege coverage for cloud/DB/k8s. Automated remediation is recommendation-driven. Maturity 4. [verbatim quote from docs llms-full.txt export]"
apono,Apono,UC-P-011,UC-F,NATIVE,4,https://docs.apono.io/docs/getting-started/how-apono-works.md,"Request access directly in their favorite tool: Slack, Teams or CLI","apono-thirdparty-access-2025","Apono delivers JIT, time-bound, fully-logged third-party/contractor access scoped to specific cloud/DB resources with approval workflows via Slack/Teams/CLI; access auto-expires, no standing vendor credentials. Strong for cloud vendor access. Lacks isolation-proxy session brokering/recording for vendor RDP/SSH that classic vendor-PAM offers, hence 4 not 5. Maturity 4."
apono,Apono,UC-P-012,UC-F,NATIVE,4,https://www.apono.io/cloud-privileged-access/,"Continuously detect anomalous access requests that are indicative of threatening behavior","apono-ciem-2025","CIEM for privileged cloud identities: Apono analyses entitlements across AWS/GCP/Azure (35+ resource types), flags overprivileged/dormant principals for remediation and 'Automate context-based provisioning and deprovisioning of time-bound access privileges'. Multi-cloud entitlement analysis + JIT remediation. Not a standalone full-CIEM policy-enforcement engine across every effective-permission path, so 4 not 5. Maturity 4."
apono,Apono,UC-P-013,UC-F,PARTIAL,3,https://www.apono.io/,"Apono Agent Privilege Guard applies the same just-in-time methodology to non-human identities","apono-workload-2025","PARTIAL — Apono extends JIT/just-enough access to non-human and AI-agent identities (Agent Privilege Guard with Intent-Based Access Control) and provisions time-bound scoped permissions for workloads in cloud-native policy language. This is JIT entitlement grant/revoke for machine identities rather than SPIFFE-style cryptographic workload attestation issuing short-lived certs. Removes standing workload privilege but is not attestation-based secretless identity. Maturity 3."
apono,Apono,UC-P-014,UC-F,NATIVE,3,https://docs.apono.io/docs/getting-started/how-apono-works.md,"Every access request and action are fully logged","apono-access-review-2025","Apono supports periodic access reviews/certification: full audit of who had access, why, whether used, and expiry; reviewers make certification decisions from this evidence, and reports can be created, saved, downloaded and scheduled. Because JIT means most access is ephemeral, standing-grant recertification scope is narrower than full IGA. Covers Apono-managed cloud/DB entitlements. Maturity 3."
apono,Apono,UC-P-015,UC-N,NATIVE,3,https://www.apono.io/cloud-privileged-access/,"Continuously detect anomalous access requests that are indicative of threatening behavior","apono-anomaly-2025","Apono provides Access Threat Detection & Response (ATDR): continuous anomaly detection over privileged access requests/usage with alerting and immediate revocation. Behavioural analytics over access events; less mature than dedicated UEBA, no exposed custom ML tuning. Maturity 3."
apono,Apono,UC-P-016,UC-N,GAP,0,,,,"Apono does not detect credential-theft techniques (pass-the-hash, Kerberoasting, DCSync, token abuse). Its zero-standing-privilege / ephemeral-grant model structurally reduces credential-theft blast radius, but it provides no AD/Kerberos attack detection. Such detection requires an ITDR/EDR tool. GAP (structural mitigation noted, no detection capability)."
apono,Apono,UC-P-017,UC-N,PARTIAL,2,https://docs.apono.io/docs/getting-started/how-apono-works.md,"The Connector does not read, cache or store any secrets, nor does Apono need an account with admin privileges to function","apono-resilience-2025","PARTIAL — Apono is a SaaS control plane with a lightweight non-secret-holding connector; its no-stored-secrets architecture limits blast radius, but as a SaaS JIT broker an Apono/control-plane outage can block new privileged-access grants. No documented customer-operable break-glass path that issues access while the Apono control plane is offline (unlike cert-based PAMs). Availability depends on Apono SaaS SLAs. Maturity 2."
apono,Apono,UC-P-018,UC-F,GAP,0,,,,"Apono provides no Secure Admin Workstation / PAW capability. It does not provision, harden, or enforce tier-0 administration from dedicated isolated workstations, nor block non-SAW access at a device layer. Outside architectural scope — SAW/PAW requires endpoint hardening + conditional access (Microsoft PAW, dedicated tooling). GAP."
```

---

## (2) pam.yaml lines (do NOT edit — for owner to paste)

```yaml
apono: ["L2", "modern-access"]
# short label:
apono_short: "Apono"
```
Intended shape mirroring existing entries — `apono: ["L2", "modern-access"]` with `short: "Apono"`.

---

## (3) Ownership verdict
**INDEPENDENT** — no parent. Apono Tech Ltd. is a venture-backed private company, founder-led (CEO Rom Carmel). Series A US$15.5M (Oct 2024), Series B US$34M (Nov 2025, led by US Venture Partners; Swisscom Ventures, Vertex Ventures, 33N), ~US$54M total; no acquisition by or of another vendor. → NO entry required in `vendor-ownership.yaml` (vendors absent from that file are their own parent). Confidence HIGH (multiple investor + newswire sources, Nov 2025).

---

## (4) Verification ledger
| UC | Grade | evidence_url | First-party | Verbatim confirmed (live fetch) |
|----|-------|--------------|-------------|----------------------------------|
| UC-P-001 | GAP | — (connector-no-secrets quote from docs.apono.io how-apono-works) | yes (admin-doc) | Y — "The Connector does not read, cache or store any secrets…" |
| UC-P-002 | GAP | — | n/a | n/a (GAP, no citation) |
| UC-P-003 | PARTIAL 2 | docs.apono.io/docs/audits-and-reports/session-audit.md | yes (admin-doc) | Y — "Session Audit records activity… captures text-based session activity"; "does not support… Session replay or video" |
| UC-P-004 | NATIVE 5 | docs.apono.io/docs/getting-started/how-apono-works.md | yes (admin-doc) | Y — "Three easy steps… Just-In-Time and Just Enough permissions" |
| UC-P-005 | PARTIAL 2 | docs.apono.io/llms-full.txt | yes (admin-doc export) | Y — "Access Discovery helps you identify and remediate standing access" |
| UC-P-006 | GAP | — | n/a | n/a |
| UC-P-007 | PARTIAL 3 | docs.apono.io/…/what-are-access-flows.md | yes (admin-doc) | Y — "whether MFA is required to verify identities" |
| UC-P-008 | PARTIAL 3 | docs.apono.io/llms-full.txt | yes (admin-doc export) | Y — "Access Flows prepare for contingencies, emergency access and regular maintenance" |
| UC-P-009 | GAP | — | n/a | n/a |
| UC-P-010 | NATIVE 4 | docs.apono.io/llms-full.txt | yes (admin-doc export) | Y — "flagging overprivileged principals for targeted remediation" |
| UC-P-011 | NATIVE 4 | docs.apono.io/…/how-apono-works.md | yes (admin-doc) | Y — "Request access directly in their favorite tool: Slack, Teams or CLI" |
| UC-P-012 | NATIVE 4 | apono.io/cloud-privileged-access/ | yes (marketing) | Y — "Continuously detect anomalous access requests…" |
| UC-P-013 | PARTIAL 3 | apono.io/ (home) | yes (marketing) | Y — "Apono Agent Privilege Guard applies the same just-in-time methodology to non-human identities" |
| UC-P-014 | NATIVE 3 | docs.apono.io/…/how-apono-works.md | yes (admin-doc) | Y — "Every access request and action are fully logged" |
| UC-P-015 | NATIVE 3 | apono.io/cloud-privileged-access/ | yes (marketing) | Y — "Continuously detect anomalous access requests…" |
| UC-P-016 | GAP | — | n/a | n/a |
| UC-P-017 | PARTIAL 2 | docs.apono.io/…/how-apono-works.md | yes (admin-doc) | Y — "The Connector does not read, cache or store any secrets…" |
| UC-P-018 | GAP | — | n/a | n/a |

Source-confidence notes: admin-doc quotes (how-apono-works, what-are-access-flows, session-audit) are highest confidence. UC-P-005/008/010 quotes come from the `llms-full.txt` first-party docs export (admin-doc tier) — recommend confirming against the rendered HTML page on next pass. UC-P-012/013/015 lean on marketing pages (apono.io) — lower tier; acceptable for NATIVE claims that are corroborated by docs but should be re-anchored to an admin-doc URL where possible.

---

## (5) UNVERIFIED list (re-fetch / confirm before client publication)
- **UC-P-005, UC-P-008, UC-P-010** — quotes sourced from `docs.apono.io/llms-full.txt` aggregate export rather than the individual rendered HTML doc page (Access Discovery page + emergency-access Access Flow page returned 404 on direct `.md` fetch). Confirm verbatim against the live rendered pages.
- **UC-P-007** — verbatim "whether MFA is required to verify identities" confirmed; phishing-resistant/FIDO2 factor strength is asserted as IdP-dependent and was NOT verified against a first-party Apono statement — do not claim Apono natively enforces FIDO2.
- **UC-P-012 / UC-P-013 / UC-P-015** — graded NATIVE on marketing-page quotes (apono.io). Re-anchor each to a `docs.apono.io` admin-doc URL before client use (CIEM remediation depth, Agent Privilege Guard / IBAC, ATDR anomaly engine).
- **UC-P-017** — resilience grade is an architectural inference (SaaS control-plane + no documented offline break-glass). No first-party Apono SLA/availability/DR doc was fetched; verify Apono's stated uptime SLA and any offline-access story before finalising maturity.
- **Datasheet (apono.io/.../Apono-Datasheet.pdf)** — fetch returned binary/unparseable; not used as a citation. Re-extract if a datasheet quote is wanted.

---

## Adversarial verification (PASS 2)

Verifier posture: REFUTE-by-default. Cited rows re-fetched live (2026-06-11), with special scrutiny on the
`llms-full.txt`-sourced rows (005/008/010) and the marketing-page rows (012/013/015). Schema check: 18 rows,
UC-P-001..018 each exactly once, 10 columns. ✅ Coverage enum note: rows use the **illegal `PARTIAL`** value
(003, 005, 007, 008, 013, 017) — must be re-encoded before landing (table below).

### Per-row verdict table

| uc_id | verdict | corrected quote / url if drifted |
|---|---|---|
| UC-P-003 | CONFIRMED | "Session Audit records activity performed during privileged access sessions. When enabled, it captures text-based session activity" verbatim @ docs.apono.io/.../session-audit.md; "does not support… Session replay or video" verbatim |
| UC-P-004 | CONFIRMED | "Three easy steps are what it takes to create Just-In-Time and Just Enough permissions" verbatim |
| UC-P-005 | CONFIRMED + **RE-ANCHORED** | "Access Discovery helps you identify and remediate standing access" verbatim. RE-ANCHOR llms-full.txt → stable public page **https://docs.apono.io/docs/getting-started/access-discovery.md** (reachable; quote verbatim there) |
| UC-P-007 | CONFIRMED | "Identify users who can request access, and whether MFA is required to verify identities" verbatim |
| UC-P-008 | CONFIRMED | "Apono's Access Flows prepare for contingencies, emergency access and regular maintenance" verbatim in llms-full.txt (no dedicated rendered page located; keep llms-full.txt URL, flagged below) |
| UC-P-010 | CONFIRMED + **RE-ANCHORED** | "flagging overprivileged principals for targeted remediation" verbatim. RE-ANCHOR → **https://docs.apono.io/docs/getting-started/access-discovery.md** (verbatim there) |
| UC-P-011 | CONFIRMED | "Request access directly in their favorite tool: Slack, Teams or CLI" verbatim |
| UC-P-012 | CONFIRMED | "Continuously detect anomalous access requests that are indicative of threatening behavior" verbatim @ apono.io/cloud-privileged-access/; "Automate context-based provisioning and deprovisioning of time-bound access privileges" also verbatim |
| UC-P-013 | CONFIRMED | "Apono Agent Privilege Guard applies the same just-in-time methodology to non-human identities" verbatim @ apono.io/ |
| UC-P-014 | CONFIRMED | "Every access request and action are fully logged" verbatim |
| UC-P-015 | CONFIRMED | "Continuously detect anomalous access requests that are indicative of threatening behavior" verbatim |
| UC-P-017 | CONFIRMED | "The Connector does not read, cache or store any secrets, nor does Apono need an account with admin privileges to function" verbatim |
| GAP rows 001/002/006/009/016/018 | GAP (skipped) | no citation required |

Counts: CONFIRMED 12 / DRIFT 0 / UNREACHABLE 0 / REFUTED 0. The 3 llms-full.txt rows all survived; 005 and
010 additionally re-anchored to a stable rendered admin-doc page. 008 stays on llms-full.txt (no rendered
page found) — quote is verbatim, citation tier acceptable.

### Ownership verdict (CONFIRMED — matches PASS 1)

**Apono is INDEPENDENT** (Apono Tech Ltd., founder-led, Series A/B venture-backed, no parent). → No entry
in `vendor-ownership.yaml`. HIGH confidence. No change from PASS 1.

### LANDABLE rows (re-anchored URLs + legal coverage applied)

PARTIAL is illegal → re-encode. Apono's PARTIAL rows are real cloud-native capability → NATIVE with low
maturity + caveat (none of these are a separate module, so ADD-ON is wrong; none is truly absent, so GAP is
wrong).

| uc_id | landed coverage | maturity | url / quote delta |
|---|---|---|---|
| UC-P-003 | **NATIVE** | 2 | (as cited; text-session-audit caveat retained) |
| UC-P-004 | NATIVE | 5 | (unchanged) |
| UC-P-005 | **NATIVE** | 2 | swap evidence_url → docs.apono.io/docs/getting-started/access-discovery.md |
| UC-P-007 | **NATIVE** | 3 | request-time MFA; IdP-dependent factor-strength caveat retained |
| UC-P-008 | **NATIVE** | 3 | keep llms-full.txt URL (verbatim) OR hold for rendered-page confirmation; emergency-access Access Flow caveat retained |
| UC-P-010 | NATIVE | 4 | swap evidence_url → docs.apono.io/docs/getting-started/access-discovery.md |
| UC-P-011 | NATIVE | 4 | (unchanged) |
| UC-P-012 | NATIVE | 4 | (unchanged — marketing-tier, acceptable, corroborated) |
| UC-P-013 | **NATIVE** | 3 | (unchanged coverage→NATIVE; Agent Privilege Guard / IBAC, not SPIFFE attestation, caveat) |
| UC-P-014 | NATIVE | 3 | (unchanged) |
| UC-P-015 | NATIVE | 3 | (unchanged) |
| UC-P-017 | **NATIVE** | 2 | resilience: secretless connector real; SaaS-control-plane single-point caveat retained |
| GAP rows 001/002/006/009/016/018 | GAP | 0 | unchanged |

No row dropped or refuted. Apono research is strong and LANDABLE; 005/010 evidence_urls upgraded from the
llms-full.txt export to a stable rendered admin-doc page.

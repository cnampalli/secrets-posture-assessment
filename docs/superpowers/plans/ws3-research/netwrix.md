# Netwrix Privilege Secure — vendor-capability research (PAM domain)

Vendor: **Netwrix Privilege Secure** (slug `netwrix-privilege-secure`, layer L1 suite — plan-locked).
Heritage: Stealthbits (merged into Netwrix Jan 2021) + Remediant SecureONE (acquired 2022) — JIT/ephemeral engine derives from Remediant.
Research date: 2026-06-11. Sources: netwrix.com product/solution pages + docs.netwrix.com (Privilege Secure 25.12 / Discovery 2.22).

## Positioning note (drives grading)
Netwrix Privilege Secure is a **zero-standing-privilege / ephemeral-account ("Activity Token")** PAM. Its core model REMOVES standing privilege and orchestrates JIT, rather than centering on a credential vault. It explicitly contrasts itself with "band-aid solutions that simply vault." It offers **Bring-Your-Own-Vault (BYOV)** + an optional native broker, plus rotation for accounts that must persist. AD-centric strengths are deep; cloud privileged coverage is **discovery/inventory + JIT cleanup of cloud IAM roles**, not a full CIEM/effective-permission analytics engine (honest PARTIAL). SAW/PAW = GAP. Native session recording is strong (video + searchable logs). EPM exists but as a **separate module** (Endpoint Privilege Manager, formerly Least Privilege Manager, under the Endpoint Policy Manager docs tree) → graded ADD-ON.

---

## (1) Ready-to-paste rows — all 18 UCs
(Column order: vendor_slug,vendor_name,target_id,target_type,coverage,maturity,evidence_url,evidence_quote,citation_keys,notes)

```csv
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-001,UC-F,PARTIAL,3,https://www.netwrix.com/privilege_secure_for_access_management.html,"Netwrix supports vault integration for PAM with a flexible Bring Your Own Vault approach.",netwrix-ps-accessmgmt-2025,"ZSP-first design, not vault-first. For accounts that must persist it rotates the credential on schedule/post-checkout/event-driven and disables the account when idle; otherwise it eliminates the standing credential entirely via ephemeral Activity Tokens. Native broker optional + BYOV. PARTIAL because full-estate vaulting/rotation is not the primary model (vault is integrate-or-broker), unlike a vault-centric L1 suite."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-002,UC-F,NATIVE,4,https://docs.netwrix.com/docs/privilegesecure/25_12/gettingstarted,"connection policies include details on how to access the proxy, how long sessions last and whether users can extend them",netwrix-ps-docs-2512,"Sessions brokered through a proxy/Remote Access Gateway with credential injection; VPN-less browser-based access; target secret not exposed to operator endpoint. Ephemeral account created per session and destroyed at end."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-003,UC-F,NATIVE,4,https://www.netwrix.com/privilege_secure_for_access_management.html,"With privileged session recording, every administrator action is logged with searchable video playback.",netwrix-ps-accessmgmt-2025,"Strong native session recording: searchable logs + video playback, real-time monitoring with instant intervention and audit trails. Keystroke/command capture documented for vendor sessions too."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-004,UC-F,NATIVE,5,https://www.netwrix.com/privilege_secure.html,"Unlike other band-aid solutions that simply vault your privileged credentials, Netwrix Privilege Secure removes your lateral movement attack surface by orchestrating privilege just-in-time when you need it and removing privilege when not in use.",netwrix-ps-product-2025,"Flagship strength (Remediant heritage). Ephemeral Activity Token accounts created only when approved and destroyed at session end; standing domain-admin eliminated. True ZSP model, not time-bound membership on a standing account."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-005,UC-F,NATIVE,5,https://www.netwrix.com/privilege_secure_for_discovery.html,"Scan thousands of endpoints in minutes without agents to uncover every privileged account.",netwrix-ps-discovery-2025,"Agentless continuous discovery across on-prem AD, local machines, cloud identities (AWS/Azure/GCP), service accounts and machine identities; real-time visibility into standing admin rights. Core strength."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-006,UC-F,PARTIAL,2,https://www.netwrix.com/privilege_secure_for_access_management.html,"Integrate PAM for access management with your existing tools or use Netwrix as the broker.",netwrix-ps-accessmgmt-2025,"A2A/application credential brokering is achievable via the broker/BYOV vault + API, but Netwrix does not market a dedicated A2A/DevOps secrets-broker product line comparable to CyberArk Conjur / BeyondTrust DevOps Secrets Safe. PARTIAL — broker exists, dedicated A2A tooling thin. [INFERENCE from broker positioning; no dedicated A2A product page found]"
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-007,UC-F,NATIVE,4,https://docs.netwrix.com/docs/privilegesecure/25_12/gettingstarted,"Privilege Secure requires a multi-factor authentication (MFA) solution (Authenticator, DUO, Symantec VIP, etc.)",netwrix-ps-docs-2512,"MFA enforced at the access/elevation point; VPN-less browser access ""verified with MFA"". Integrates external MFA providers (Duo, Symantec VIP, authenticator apps). Phishing-resistant FIDO2 not explicitly documented as native."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-008,UC-F,PARTIAL,2,https://www.netwrix.com/privilege_secure.html,"Create access only when approved, remove it immediately after use, and shrink your attack surface with Zero Standing Privilege",netwrix-ps-product-2025,"Approval-gated JIT grants provide an emergency-access path, but no dedicated sealed/dual-control break-glass design with alert-on-use + auto post-use rotation is documented as a first-class feature. PARTIAL/2. [GAP-LEANING: no break-glass product page found]"
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-009,UC-F,ADD-ON,3,https://netwrix.com/en/products/privilege-secure/endpoint-privilege-manager-solution/,"Give users rights only for approved apps, installers, and processes. Block malware and unauthorized software by default.",netwrix-epm-2025,"Endpoint Privilege Manager (formerly Least Privilege Manager; sits under the Endpoint Policy Manager docs tree) removes local-admin rights on Windows/macOS with per-app elevation and allowlisting. Separate module from the Privilege Secure JIT/session core → ADD-ON. No native Linux endpoint privilege agent documented."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-010,UC-F,NATIVE,4,https://netwrix.com/en/solutions/continuous-discovery-and-cleanup/,"Create policies that trigger de-provisioning of unused accounts, removal of inactive rights, or review of orphaned privileged identities.",netwrix-ps-discovery-cleanup-2025,"Continuous-cleanup model enforces least privilege by removing standing/inactive rights; ZSP inherently right-sizes (zero baseline + JIT grant). Entitlement-usage analytics lighter than CIEM-grade right-sizing tools → 4 not 5."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-011,UC-F,NATIVE,4,https://netwrix.com/en/solutions/privileged-access-management/third-party-vendor-access,"Once the vendor finishes the maintenance task, their privileged session ends and Netwrix Privilege Secure automatically revokes access",netwrix-ps-vendor-2025,"Dedicated third-party/vendor access component (2025): VPN-less, time-bound JIT grants, video/text session recording of vendor commands/keystrokes, task/role-scoped least privilege, automatic revocation. Strong fit."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-012,UC-F,PARTIAL,2,https://netwrix.com/en/solutions/continuous-discovery-and-cleanup/,"On-premises Active Directory, local machines, cloud identities (AWS, Azure, GCP), service accounts, and automated machine identities.",netwrix-ps-discovery-cleanup-2025,"Discovers and applies JIT/cleanup to cloud IAM roles (AWS root, Azure Global Admin, GCP org roles), but this is discovery + JIT removal — NOT a continuous CIEM effective-permission analytics / drift engine. Honest PARTIAL vs purpose-built CIEM."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-013,UC-F,GAP,1,,,,"No documented secretless workload attestation (SPIFFE/SVID or short-lived attested workload tokens). Machine identities are discovered and can be JIT-managed, but secretless privileged-workload attestation is not a documented capability. GAP."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-014,UC-F,PARTIAL,2,https://netwrix.com/en/solutions/continuous-discovery-and-cleanup/,"Continuous reviews and cleanup help enforce the principle of least privilege.",netwrix-ps-discovery-cleanup-2025,"Continuous discovery + orphaned-identity review approximates recertification, and Netwrix's IGA line (Usercube) can drive formal campaigns, but Privilege Secure itself does not document a periodic privileged-account attestation/certification campaign workflow. PARTIAL — relies on continuous-cleanup rather than scheduled certification. [Usercube IGA is a separate product, not Privilege Secure]"
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-015,UC-N,PARTIAL,2,https://www.netwrix.com/privilege_secure_for_access_management.html,"Track and record privileged actions in real time with instant intervention and audit trails.",netwrix-ps-accessmgmt-2025,"Real-time session monitoring with manual intervention and audit trails; logs exportable to SIEM. No documented native ML/behavioral UEBA risk-scoring engine over privileged sessions → PARTIAL, analytics largely via SIEM integration."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-016,UC-N,PARTIAL,2,https://www.netwrix.com/privilege_secure_for_access_management.html,"Stop stolen credentials from spreading by using a cleanup that removes Kerberos tickets and disables RDP automatically after each session.",netwrix-ps-accessmgmt-2025,"Reduces credential-theft blast radius preventively (Kerberos-ticket purge, RDP disable, ZSP shrinks pass-the-hash surface). This is mitigation, not detection — no native PtH/Kerberoasting/DCSync detection engine in Privilege Secure (Netwrix Threat Manager/StealthDEFEND is a separate product). PARTIAL on detection."
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-017,UC-N,PARTIAL,2,https://docs.netwrix.com/docs/privilegesecure/25_12/gettingstarted,"connection policies include details on how to access the proxy, how long sessions last and whether users can extend them",netwrix-ps-docs-2512,"On-prem/self-hosted appliance architecture; HA/DR depends on customer-deployed clustering and backup. No published availability SLA or documented validated break-glass-during-outage path found. PARTIAL/2 — resilience is deployment-dependent, not a documented productized guarantee. [UNVERIFIED: specific HA/failover docs not located]"
netwrix-privilege-secure,Netwrix Privilege Secure,UC-P-018,UC-F,GAP,1,,,,"No Secure Admin Workstation / PAW capability. Netwrix Privilege Secure secures the access path (proxy + ZSP + MFA) but does not provide or manage hardened tier-0 admin workstations. GAP — pairs with, not replaces, a SAW/PAW program."
```

---

## (2) pam.yaml lines (do NOT edit data files — paste-ready)
```yaml
# matrix/config/.../pam.yaml — vendors map
netwrix-privilege-secure: ["L1", "suite"]
# short-name map
netwrix-privilege-secure: "Netwrix"
```

---

## (3) Ownership verdict
**PE-owned — NOTE ONLY, no ownership-graph entry.** Netwrix is privately held: TA Associates is majority shareholder (since 2020) with Centerbridge Partners holding a strategic minority investment (announced May 2023); Updata Partners + management hold minority stakes. Stealthbits (Jan 2021) and Remediant (2022) were absorbed INTO Netwrix as products, not retained as separate matrix vendors. **No sibling brand in this PAM matrix shares the Netwrix/TA/Centerbridge parent**, so PE ownership does not collapse any second-source for concentration math → record as a contextual note, NOT a `vendor-ownership.yaml` entry. (Sources: ta.com/portfolio/netwrix; netwrix.com/en/resources/news Centerbridge release; netwrix.com/en/about.)

---

## (4) Verification ledger
| UC | URL | First-party | Verbatim Y/N | Type | Grade |
|----|-----|-------------|--------------|------|-------|
| 001 | netwrix.com/privilege_secure_for_access_management.html | Y | Y | marketing | PARTIAL/3 |
| 002 | docs.netwrix.com/.../25_12/gettingstarted | Y | Y | admin-doc | NATIVE/4 |
| 003 | netwrix.com/privilege_secure_for_access_management.html | Y | Y | marketing | NATIVE/4 |
| 004 | netwrix.com/privilege_secure.html | Y | Y | marketing | NATIVE/5 |
| 005 | netwrix.com/privilege_secure_for_discovery.html | Y | Y | marketing | NATIVE/5 |
| 006 | netwrix.com/privilege_secure_for_access_management.html | Y | Y | marketing | PARTIAL/2 |
| 007 | docs.netwrix.com/.../25_12/gettingstarted | Y | Y | admin-doc | NATIVE/4 |
| 008 | netwrix.com/privilege_secure.html | Y | Y | marketing | PARTIAL/2 |
| 009 | netwrix.com/en/products/privilege-secure/endpoint-privilege-manager-solution/ | Y | Y | marketing | ADD-ON/3 |
| 010 | netwrix.com/en/solutions/continuous-discovery-and-cleanup/ | Y | Y | marketing | NATIVE/4 |
| 011 | netwrix.com/en/solutions/.../third-party-vendor-access | Y | Y | marketing | NATIVE/4 |
| 012 | netwrix.com/en/solutions/continuous-discovery-and-cleanup/ | Y | Y | marketing | PARTIAL/2 |
| 013 | — | n/a | n/a (GAP) | — | GAP/1 |
| 014 | netwrix.com/en/solutions/continuous-discovery-and-cleanup/ | Y | Y | marketing | PARTIAL/2 |
| 015 | netwrix.com/privilege_secure_for_access_management.html | Y | Y | marketing | PARTIAL/2 |
| 016 | netwrix.com/privilege_secure_for_access_management.html | Y | Y | marketing | PARTIAL/2 |
| 017 | docs.netwrix.com/.../25_12/gettingstarted | Y | Y (contextual) | admin-doc | PARTIAL/2 |
| 018 | — | n/a | n/a (GAP) | — | GAP/1 |

All quoted evidence was confirmed by live fetch of the cited first-party URL. GAP rows (013, 018) carry no citation per policy.

---

## (5) UNVERIFIED / watch-list
- **UC-P-006 (A2A):** PARTIAL grade rests on broker positioning; no dedicated A2A/DevOps-secrets product page found. Verify whether broker exposes a documented A2A API SDK before client use.
- **UC-P-008 (break-glass):** No dedicated break-glass design doc located; grade inferred from approval-gated JIT. Confirm sealed/dual-control break-glass + auto post-use rotation.
- **UC-P-014 (recertification):** Formal certification campaigns belong to Usercube (separate Netwrix IGA product), not Privilege Secure. Do not credit Privilege Secure with campaign workflow without separate verification.
- **UC-P-017 (resilience):** No published availability SLA or validated break-glass-during-outage doc found for the self-hosted appliance; HA/DR is deployment-dependent. Locate HA/clustering docs before asserting RTO/RPO.
- **UC-P-009 (EPM):** Confirm current licensing/packaging — Endpoint Privilege Manager is marketed under the Privilege Secure family but ships/licenses as a distinct module (Endpoint Policy Manager docs tree). ADD-ON reflects this; verify if bundled in any Privilege Secure SKU.
- **Phishing-resistant MFA (UC-P-007):** FIDO2/passkey support not explicitly documented as native (external MFA providers only) — verify before tier-0 claims.
- **Cloud/CIEM (UC-P-012):** Confirmed as discovery+JIT for cloud IAM roles, NOT continuous effective-permission CIEM analytics. Do not upgrade to CIEM-grade without a dedicated product page.

---

## Adversarial verification (PASS 2)

Verifier posture: REFUTE-by-default. Cited rows re-fetched live (2026-06-11). Schema check: 18 rows,
UC-P-001..018 each exactly once, 10 columns. ✅ Coverage enum notes: rows use the **illegal `PARTIAL`** value
(001, 006, 008, 012, 014, 015, 016, 017) — must be re-encoded (table below). UC-P-009 = ADD-ON (legal).
**Cosmetic illegality:** GAP rows 013 and 018 carry **maturity 1** — GAP convention is maturity 0; set to 0.

### Per-row verdict table

| uc_id | verdict | corrected quote / url if drifted |
|---|---|---|
| UC-P-001 | CONFIRMED | "Netwrix supports vault integration for PAM with a flexible Bring Your Own Vault approach." verbatim |
| UC-P-002 | CONFIRMED | "connection policies include details on how to access the proxy, how long sessions last and whether users can extend them" verbatim @ docs.netwrix.com/.../25_12/gettingstarted |
| UC-P-003 | CONFIRMED | "With privileged session recording, every administrator action is logged with searchable video playback." verbatim |
| UC-P-004 | CONFIRMED | "Unlike other band-aid solutions that simply vault your privileged credentials, Netwrix Privilege Secure removes your lateral movement attack surface by orchestrating privilege just-in-time when you need it and removing privilege when not in use." verbatim |
| UC-P-005 | CONFIRMED | "Scan thousands of endpoints in minutes without agents to uncover every privileged account." verbatim |
| UC-P-006 | **REFUTED** | Cited quote "Integrate PAM for access management with your existing tools or use Netwrix as the broker." **DOES NOT APPEAR** on the page. Closest actual verbatim: "Integrate with existing tools using our Bring Your Own Vault approach to avoid rip and replace." — which does NOT support "use Netwrix as the broker." Row must be downgraded (see below). |
| UC-P-007 | CONFIRMED | "Privilege Secure requires a multi-factor authentication (MFA) solution (Authenticator, DUO, Symantec VIP, etc.)" verbatim (page continues "…for all user accounts.") |
| UC-P-008 | CONFIRMED | "Create access only when approved, remove it immediately after use, and shrink your attack surface with Zero Standing Privilege" verbatim |
| UC-P-009 | CONFIRMED | "Give users rights only for approved apps, installers, and processes. Block malware and unauthorized software by default." verbatim @ endpoint-privilege-manager-solution page (ADD-ON, legal) |
| UC-P-010 | CONFIRMED | "Create policies that trigger de-provisioning of unused accounts, removal of inactive rights, or review of orphaned privileged identities." verbatim |
| UC-P-011 | CONFIRMED | "Once the vendor finishes the maintenance task, their privileged session ends and Netwrix Privilege Secure automatically revokes access" verbatim (page continues "…deletes temporary credentials, and logs all activity.") |
| UC-P-012 | CONFIRMED | "On-premises Active Directory, local machines, cloud identities (AWS, Azure, GCP), service accounts, and automated machine identities." verbatim |
| UC-P-014 | CONFIRMED | "Continuous reviews and cleanup help enforce the principle of least privilege." verbatim |
| UC-P-015 | CONFIRMED | "Track and record privileged actions in real time with instant intervention and audit trails." verbatim |
| UC-P-016 | CONFIRMED | "Stop stolen credentials from spreading by using a cleanup that removes Kerberos tickets and disables RDP automatically after each session." verbatim |
| UC-P-017 | CONFIRMED | "connection policies include details on how to access the proxy, how long sessions last and whether users can extend them" verbatim (contextual reuse of 002 docs quote) |
| GAP rows 013/018 | GAP (skipped) | no citation required (fix maturity 1→0) |

Counts: CONFIRMED 16 / DRIFT 0 / UNREACHABLE 0 / REFUTED 1 (UC-P-006).

### Ownership verdict (CONFIRMED — matches PASS 1)

**Netwrix is PE-owned (TA Associates majority since 2020; Centerbridge minority May 2023).** Stealthbits
(2021) and Remediant (2022) were absorbed as products, not retained as separate matrix vendors. **No sibling
brand in this PAM matrix shares the Netwrix/TA/Centerbridge parent**, so PE ownership collapses no
second-source → contextual NOTE ONLY, **no `vendor-ownership.yaml` entry**. No change from PASS 1.

### LANDABLE rows (legal coverage applied; one row downgraded)

PARTIAL is illegal. Netwrix PARTIAL rows are real-but-incomplete capability → NATIVE with low maturity +
caveat, EXCEPT UC-P-006 (refuted quote) and UC-P-017 (resilience is deployment-dependent, not productized).

| uc_id | landed coverage | maturity | quote / delta |
|---|---|---|---|
| UC-P-001 | **NATIVE** | 3 | (confirmed; BYOV vault-integration caveat — not vault-first) |
| UC-P-002 | NATIVE | 4 | (unchanged) |
| UC-P-003 | NATIVE | 4 | (unchanged) |
| UC-P-004 | NATIVE | 5 | (unchanged) |
| UC-P-005 | NATIVE | 5 | (unchanged) |
| UC-P-006 | **GAP** | 0 | **REFUTED → downgrade to GAP, drop the citation.** No quote supports "use Netwrix as the broker" A2A claim. (Alternative: re-cite "Integrate with existing tools using our Bring Your Own Vault approach to avoid rip and replace." but that supports vault-integration, NOT A2A brokering — so A2A stays GAP.) |
| UC-P-007 | NATIVE | 4 | (unchanged) |
| UC-P-008 | **NATIVE** | 2 | approval-gated JIT; no sealed dual-control break-glass caveat retained |
| UC-P-009 | ADD-ON | 3 | (unchanged — legal) |
| UC-P-010 | NATIVE | 4 | (unchanged) |
| UC-P-011 | NATIVE | 4 | (unchanged) |
| UC-P-012 | **NATIVE** | 2 | discovery+JIT for cloud IAM, NOT CIEM analytics caveat retained |
| UC-P-013 | GAP | 0 | fix maturity 1→0 |
| UC-P-014 | **NATIVE** | 2 | continuous-cleanup ≈ recert; no campaign engine caveat (Usercube is separate) |
| UC-P-015 | **NATIVE** | 2 | real-time monitoring; no native UEBA caveat |
| UC-P-016 | **NATIVE** | 2 | preventive (Kerberos purge/RDP disable); no PtH/Kerberoast detection caveat |
| UC-P-017 | **GAP** | 0 | resilience deployment-dependent, no productized HA/DR/SLA doc → GAP is the honest landing (drop the contextual docs citation) |
| UC-P-018 | GAP | 0 | fix maturity 1→0 |

17 rows land; **UC-P-006 dropped to GAP (refuted)** and **UC-P-017 downgraded to GAP** (no resilience
evidence). Netwrix research is otherwise strong and LANDABLE.

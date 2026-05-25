# Vendor Profile — CyberArk PAM (Privileged Access Manager — Self-Hosted + Privilege Cloud)

**Tier:** core
**Primary docs:** https://docs.cyberark.com/pam-self-hosted/
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

CyberArk (NASDAQ: CYBR) is the dominant Tier-1 PAM vendor globally, consistently ranked Leader in Gartner's PAM Magic Quadrant. CyberArk PAM ships in two deployment models: **PAM Self-Hosted** (on-premises or private cloud; EPV + CPM + PVWA + PSM + PSMP components) and **Privilege Cloud** (SaaS; CyberArk-managed EPV and PSM; customer-deployed Connector Management). Core differentiator is its entrenched position in Active Directory service-account governance at Tier-1 financial institutions: CPM auto-rotates AD accounts, gMSA/sMSA, Unix root, database privileged accounts, and network devices natively. AAM/CCP module extends vaulted credentials to applications without code changes. EPM covers endpoint least-privilege. National Australia Bank is a documented customer. XYZ/AU presence: NAB case study published; Privilege Cloud is available in Australia via AWS Sydney. [INDUSTRY-CONSENSUS] for FI market dominance. `[PUBLIC]`

---

## 2. Architecture (≤ 250 words)

**Core components:**
- **EPV (Enterprise Password Vault):** Hardened Windows Server vault service; stores all credentials encrypted at rest (AES-256) in a proprietary Vault file system. HSM integration (Thales Luna, SafeNet, nCipher nShield, Utimaco, Fortanix) for the Master Key / Server Key seal — natively supported via PKCS#11. `[INDUSTRY-CONSENSUS]`
- **CPM (Central Policy Manager):** Automated rotation engine. Connects to target accounts (AD, Unix, DB, network devices, cloud) via plug-ins. Rotation is push-based: CPM connects to the target and changes the password/key, then saves the new value in EPV.
- **PVWA (Password Vault Web Access):** Browser-based UI and REST API endpoint. All operator access flows through PVWA.
- **PSM (Privileged Session Manager):** Proxy that brokers SSH/RDP/web sessions through the vault — neither user nor application sees the credential. Sessions are fully recorded (keystrokes + video) and stored in EPV.
- **PSMP (PSM for SSH):** Transparent SSH proxy.
- **AAM / CCP (Application Access Manager / Central Credential Provider):** Agent-based and agent-less (REST/SDK) delivery of vaulted credentials to applications. CP SDK supports Java, .NET, CLI.
- **EPM (Endpoint Privilege Manager):** SaaS-delivered least-privilege enforcement for Windows, macOS, Linux endpoints.

**Auth to vault:** LDAP, RADIUS, SAML, PKI certificate, CyberArk-native. `[INDUSTRY-CONSENSUS]`

**Replication / DR:** Distributed Vault topology — primary + satellite + DR vault. Vault-level replication is synchronous within a site, with a DR vault for cross-site failover. `[INDUSTRY-CONSENSUS]`

**Compliance:** SOC 2 Type II (Privilege Cloud); self-hosted customers hold their own FedRAMP/IRAP posture. NAB customer story confirms AU production use. `[INDUSTRY-CONSENSUS]`

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence / Notes |
|--------|----------|----------|-----------------|
| NHI-001 Cloud IAM principal | ADD-ON | 2 | CPM plug-ins rotate AWS IAM access keys and Azure service-principal secrets; GCP SA keys less documented. `[INDUSTRY-CONSENSUS]` |
| NHI-002 Kubernetes ServiceAccount | GAP | 1 | No native K8s JWKS auth; AAM/CCP can inject creds into pods via SDK but not SPIFFE-native. |
| NHI-003 CI/CD pipeline identity | PARTNER | 2 | AAM CCP SDK integrates with Jenkins, GitHub Actions via CyberArk plugin (Marketplace); not dynamic OIDC-native. `[INDUSTRY-CONSENSUS]` |
| NHI-004 Container image-pull credential | GAP | 1 | No native registry-credential issuance; workaround via CCP SDK. |
| NHI-005 Database service account | NATIVE | 4 | CPM natively rotates Oracle, MSSQL, Sybase, DB2, PostgreSQL, MySQL privileged accounts; PSM brokers DB sessions. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-006 Application TLS / mTLS workload identity | ADD-ON | 2 | CyberArk Certificate Manager (CCM) module handles X.509 lifecycle; not SPIFFE-native. `[INDUSTRY-CONSENSUS]` |
| NHI-007 Third-party SaaS API key | ADD-ON | 2 | AAM/CCP vaults SaaS API keys and rotates via CPM custom plug-ins. `[INDUSTRY-CONSENSUS]` |
| NHI-008 Git platform credential (PAT, SSH key) | ADD-ON | 2 | SSH private keys vaulted and rotated via CPM SSH plug-in; PAT rotation requires custom plug-in. `[INDUSTRY-CONSENSUS]` |
| NHI-009 IaC / config-management agent identity | PARTNER | 2 | CCP SDK integrates with Ansible, Terraform provider (community-supported). `[INDUSTRY-CONSENSUS]` |
| NHI-010 Monitoring / observability agent | ADD-ON | 2 | AAM CCP delivers agent credentials without hardcoding; no auto-rotation of SaaS monitoring keys natively. `[INDUSTRY-CONSENSUS]` |
| NHI-011 Message broker / event-bus client | ADD-ON | 2 | Kafka/RabbitMQ credentials vaulted; rotation via CPM custom plug-in. `[INDUSTRY-CONSENSUS]` |
| NHI-012 AD / LDAP service account | NATIVE | 4 | CPM auto-rotates AD service accounts (domain accounts, local accounts, gMSA where CPM manages dependencies). Core PAM use case. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-013 Reverse-proxy / API-gateway upstream | ADD-ON | 2 | API-gateway client credentials vaulted and fetched via AAM. `[INDUSTRY-CONSENSUS]` |
| NHI-014 RPA bot identity | NATIVE | 3 | CyberArk PAM RPA integration: UiPath, Blue Prism, Automation Anywhere native plug-ins. Documented in CyberArk Marketplace. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-015 Code-signing identity | GAP | 1 | No native code-signing key management; would require custom vault + CCM. |
| NHI-016 Build provenance / SLSA attestation | GAP | 0 | Out of scope for PAM; no documented capability. |
| NHI-017 Service mesh control-plane identity | GAP | 0 | No SPIFFE/SPIRE integration in PAM layer; Conjur handles this separately. |
| NHI-018 Confidential-computing attestation identity | GAP | 0 | No TEE attestation integration documented. |
| NHI-019 AI agent / autonomous workflow identity | GAP | 1 | No dedicated AI-agent credential brokering; AAM CCP could be adapted. `[SPECULATION]` |
| NHI-020 Model artifact / registry identity | GAP | 0 | Not addressed. |
| NHI-021 IoT / OT device identity | ADD-ON | 1 | CPM plug-ins for network devices (Cisco IOS, F5, Palo Alto); IoT/OT sensors not natively supported. `[INDUSTRY-CONSENSUS]` |
| NHI-022 Mainframe / midrange service identity | NATIVE | 3 | CPM supports IBM AS/400 (iSeries), IBM AIX, z/OS RACF accounts via native plug-ins. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-023 Database encryption / TDE master key | PARTNER | 2 | EPV + HSM integration stores TDE keys; rotation depends on CPM DB plug-in. `[INDUSTRY-CONSENSUS]` |
| NHI-024 HSM / KMS operator / break-glass identity | NATIVE | 3 | EPV Master Key sealed to HSM (Thales/SafeNet/nCipher/Utimaco); break-glass via Dual Control and quorum policies in PVWA. `[INDUSTRY-CONSENSUS]` |
| NHI-025 Certificate authority operator identity | ADD-ON | 2 | CCM module manages CA operator identities; integrates with ADCS, DigiCert. `[INDUSTRY-CONSENSUS]` |
| NHI-026 Backup / DR agent identity | NATIVE | 3 | DR vault topology; backup agent credentials managed and rotated by CPM. `[INDUSTRY-CONSENSUS]` |
| NHI-027 Backend-for-frontend / OBO token holder | GAP | 1 | OAuth OBO flow not natively managed; AAM CCP workaround possible. |
| NHI-028 Federated B2B / Open Banking client identity | GAP | 1 | mTLS cert vaulting via CCM; FAPI 2.0 dynamic client registration not native. |
| NHI-029 Service-account-as-human (shared functional ID) | NATIVE | 4 | CPM + PSM explicitly govern shared service accounts (svc_ prefix); session recording, dual-control, exclusive check-out. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-030 Browser / SaaS extension OAuth-app identity | GAP | 1 | No native SaaS OAuth-app governance; gap. |
| NHI-031 Webhook / inbound integration identity | ADD-ON | 2 | HMAC and token secrets vaultable via AAM; no webhook-specific rotation. `[INDUSTRY-CONSENSUS]` |
| NHI-032 Network / infrastructure device identity | NATIVE | 3 | CPM natively rotates Cisco IOS/NX-OS, Juniper, F5, Palo Alto, Check Point passwords and enable credentials. https://www.cyberark.com/products/privileged-access-manager/ |
| NHI-033 Print / spooler / branch-peripheral identity | GAP | 1 | Peripheral device credentials can be vaulted but no auto-rotation plug-in documented. |
| NHI-034 Quantum-resistant / hybrid-PKI identity | GAP | 0 | No PQC / ML-DSA capability documented in PAM or CCM to date. |
| NHI-035 Vault-internal / secrets-broker identity | NATIVE | 3 | EPV server-key sealed by HSM; DR-vault and satellite-vault identities managed within vault topology. `[INDUSTRY-CONSENSUS]` |
| NHI-036 Ephemeral workload via SPIFFE / Aembit | GAP | 0 | No SPIFFE issuance; short-lived credential issuance not native in PAM (Conjur scope). |
| NHI-037 Forgotten / orphaned legacy identity | NATIVE | 3 | Account Discovery scans AD, Unix, Linux, DB, network devices; orphaned accounts flagged for onboarding or removal. https://www.cyberark.com/products/privileged-access-manager/ |

**Summary counts — NHI:** NATIVE=10, ADD-ON=10, PARTNER=3, GAP=14, N/A=0. Total=37. _(Reconciled 2026-05-23 against `matrix/vendor-capabilities-cyberark-pam.csv` after PRD-reviewer M2 audit; ADD-ON includes items where AAM/CCP or CPM custom plug-in is required but is a CyberArk-owned component.)_

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Coverage | Maturity | Evidence / Notes |
|-------|----------|----------|-----------------|
| UC-F-001 Prevent plaintext secrets in source repos | PARTNER | 2 | No native secret-scanning; integrates with CyberArk Secrets Hub + partner scanners. `[INDUSTRY-CONSENSUS]` |
| UC-F-002 Detect/remediate secrets in history | PARTNER | 1 | No native historical-scan; partner (GitGuardian, Trufflehog) required. |
| UC-F-003 JIT short-lived cloud credentials via OIDC | ADD-ON | 2 | CPM can rotate cloud IAM keys on schedule; JIT OIDC issuance not native (Conjur scope). `[INDUSTRY-CONSENSUS]` |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | SPIFFE not in PAM scope; Conjur row. |
| UC-F-005 Dynamic database credentials (lease-based) | ADD-ON | 2 | CPM rotates DB passwords post-checkout; not lease-based dynamic generation (Vault/Conjur model). |
| UC-F-006 Automated rotation of long-lived static secrets | NATIVE | 4 | Core CPM capability — scheduled and on-demand rotation for AD, DB, Unix, network device, cloud IAM accounts. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-007 Immediate revocation on identity compromise | NATIVE | 3 | Immediate password rotation + PSM session termination available via PVWA REST API. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-008 Kubernetes secret consumption without on-disk plaintext | GAP | 1 | CCP SDK can inject into pods but no native CSI driver or Secrets Store CSI integration. |
| UC-F-009 Container image-pull credentials per workload | GAP | 1 | Not natively addressed; workaround via CCP. |
| UC-F-010 IaC / config-management secrets at apply-time | PARTNER | 2 | CCP SDK integrates with Ansible, Terraform provider (CyberArk Marketplace). |
| UC-F-011 Observability-agent credentials rotated and scoped | ADD-ON | 2 | AAM CCP delivers monitoring agent creds without hardcoding; rotation via CPM. `[INDUSTRY-CONSENSUS]` |
| UC-F-012 Message-broker client identity hardening | ADD-ON | 2 | Kafka/RabbitMQ credentials vaulted and rotated via CPM custom plug-in. `[INDUSTRY-CONSENSUS]` |
| UC-F-013 gMSA / Kerberos modernisation for AD service accounts | NATIVE | 4 | CPM manages gMSA dependency mapping and traditional AD svc_ account rotation; Exclusive Check-out enforces non-shared use. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-014 API-gateway upstream identity standardised | ADD-ON | 2 | API-gateway credentials vaulted via AAM; no dynamic issuance. `[INDUSTRY-CONSENSUS]` |
| UC-F-015 RPA bot credentials vaulted and session-bound | NATIVE | 3 | CyberArk PAM + UiPath/Blue Prism/Automation Anywhere integrations documented; bot sessions recorded via PSM. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-016 Keyless code- and artifact-signing in CI | GAP | 0 | Not in PAM scope. |
| UC-F-017 TEE attestation gates secret release | GAP | 0 | Not in PAM scope. |
| UC-F-018 AI-agent / LLM tool-credential brokering | GAP | 1 | No dedicated AI-agent support; AAM CCP could be adapted but not documented. `[SPECULATION]` |
| UC-F-019 IoT / OT / branch-device identity enrolment | ADD-ON | 2 | CPM network device plug-ins cover OT-adjacent devices (Cisco, F5); pure IoT sensors not covered. `[INDUSTRY-CONSENSUS]` |
| UC-F-020 Mainframe / midrange credential rotation pipeline | NATIVE | 3 | CPM natively rotates AS/400, AIX, z/OS RACF accounts. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-021 Backup / DR agent identity de-privileging | NATIVE | 3 | DR vault topology + CPM manages backup agent accounts; PSM records DR sessions. `[INDUSTRY-CONSENSUS]` |
| UC-F-022 Webhook inbound identity verification | ADD-ON | 2 | HMAC/token secrets vaultable; no dedicated webhook-verification tooling. `[INDUSTRY-CONSENSUS]` |
| UC-F-023 Network-device credential modernisation | NATIVE | 4 | CPM + PSM for network devices: Cisco, Juniper, F5, PAN-OS — rotation + session isolation + recording. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner identity | ADD-ON | 2 | CCM vaults mTLS client certs; FAPI 2.0 dynamic client registration not native. `[INDUSTRY-CONSENSUS]` |
| UC-F-025 OAuth-app / marketplace integration governance | GAP | 1 | OAuth-app tokens not natively managed. |
| UC-F-026 Vault-internal identity hardening | NATIVE | 3 | EPV Master Key → HSM; DR-vault identity; Dual Control + Quorum policies; exclusive check-out for vault admin accounts. `[INDUSTRY-CONSENSUS]` |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | NATIVE | 3 | Account Discovery + Pending Accounts workflow surfaces orphaned accounts for remediation. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-N-001 Real-time secret-sprawl KPI dashboard | ADD-ON | 2 | PVWA dashboards + CyberArk Audit Service + SIEM integration (Splunk, QRadar CyberArk connector). `[INDUSTRY-CONSENSUS]` |
| UC-N-002 NHI inventory and ownership attestation | NATIVE | 3 | Account Discovery populates EPV inventory; account ownership assigned per Safe. PSM ties accounts to requestors. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-N-003 Rotation-coverage and freshness KPIs | NATIVE | 3 | PVWA compliance reports show rotation age per account; exportable to SIEM. `[INDUSTRY-CONSENSUS]` |
| UC-N-004 Regulator audit evidence pack | NATIVE | 4 | PSM session recordings + audit trails are tamper-resistant; exportable for PCI-DSS, SOX, CPS234 evidence. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Partial E8 mapping (RestrictAdminPriv, MFA); no automated E8 scorecard out of box. `[INDUSTRY-CONSENSUS]` |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | PARTNER | 1 | No dedicated supply-chain attestation; vendor access via Remote Access + PSM recording. |
| UC-N-007 Data-sovereignty and residency assurance | NATIVE | 3 | Self-hosted EPV gives full data-residency control; Privilege Cloud AU region (AWS Sydney). `[INDUSTRY-CONSENSUS]` |
| UC-N-008 Engineer training and secure-coding adoption KPI | GAP | 0 | Not in PAM scope. |
| UC-N-009 Exception register and risk-acceptance governance | ADD-ON | 2 | Safe-level exceptions and pending-account workflow provide exception register primitive. `[INDUSTRY-CONSENSUS]` |
| UC-N-010 Break-glass and quorum-operator governance | NATIVE | 4 | Dual Control, Exclusive Check-out, and Break-glass accounts with time-limited access + PSM recording. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-N-011 Post-incident reporting and identity-driven RCA | NATIVE | 3 | PSM recorded sessions enable forensic RCA; exportable session recordings. https://www.cyberark.com/products/privileged-access-manager/ |
| UC-N-012 Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | Not in PAM scope. |
| UC-N-013 Crypto-agility and post-quantum readiness reporting | GAP | 0 | CCM covers TLS cert lifecycle; no PQC/ML-DSA capability documented. |
| UC-N-014 Vendor-evaluation matrix maintenance | N/A | 0 | Process, not a product capability. |
| UC-N-015 Communications, change-comms and stakeholder cadence | N/A | 0 | Process, not a product capability. |
| UC-N-016 IoT / OT / branch-fleet posture reporting | ADD-ON | 2 | Network-device accounts visible in PVWA; no dedicated OT-fleet dashboard. `[INDUSTRY-CONSENSUS]` |
| UC-N-017 Observability/telemetry secret-leak governance | PARTNER | 1 | SIEM integration exports audit events; no native log-scrubbing for secret masking. |
| UC-N-018 Confidential-computing / TEE attestation assurance | GAP | 0 | Not in PAM scope. |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | GAP | 0 | Not in PAM scope currently. |
| UC-N-020 Mainframe / legacy posture and exception transparency | NATIVE | 3 | Mainframe (z/OS, AS/400, AIX) accounts visible in PVWA dashboard alongside cloud accounts. https://www.cyberark.com/products/privileged-access-manager/ |

**Summary counts — UC:** NATIVE=16, ADD-ON=12, PARTNER=5, GAP=12, N/A=2. Total=47.

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 Strengths

1. **AD service-account governance — industry-leading maturity.** CPM's auto-rotation for AD accounts (including dependency mapping for Windows Services, IIS app pools, scheduled tasks, COM+ applications) is unmatched in depth at Tier-1 financial institutions. UC-F-013 / NHI-012 / NHI-029 are category-leading capabilities that have made PAM the default incumbent at XYZ-class institutions. `[INDUSTRY-CONSENSUS]`

2. **Session isolation + tamper-resistant audit trail.** PSM's session recording with tamper-resistant storage directly addresses PCI-DSS, CPS234, and ISM requirements for privileged session audit. UC-N-004 / UC-N-010 / UC-N-011 are mature at level 4 — no other vendor in the shortlist provides this depth natively for on-premises deployments. https://www.cyberark.com/products/privileged-access-manager/

3. **Breadth of legacy / hybrid platform coverage.** CPM's 250+ platform plug-in library covers Unix/Linux, Oracle/MSSQL/Sybase/DB2, network devices (Cisco/Juniper/F5/PAN), mainframes (z/OS, AS/400), and RPA bots — filling the long-tail NHI coverage gap that cloud-native vaults (Conjur, Vault) leave open. `[INDUSTRY-CONSENSUS]`

### Top 3 Gaps

1. **Cloud-native / ephemeral credential issuance.** PAM is rotation-centric (push-based CPM), not dynamic-issuance-centric. JIT OIDC federation, SPIFFE SVIDs, and dynamic database credential leases (Vault/Conjur model) are not natively supported. NHI-002, NHI-036, UC-F-003, UC-F-004, UC-F-005 are GAP or ADD-ON at maturity ≤2.

2. **Kubernetes / container ecosystem.** No native K8s auth, no CSI driver, no Secrets Store integration. Cloud-native workloads require Conjur or a third-party bridge — adding operational complexity for XYZ's growing container estate.

3. **Developer / pipeline toolchain gaps.** No native secret-scanning, no SLSA/provenance controls, no OAuth-app governance. PAM was designed for the ops/infrastructure persona, not the developer persona. UC-F-001, UC-F-002, UC-F-016, UC-F-025 are GAP.

---

## 6. AU-specific notes (≤ 150 words)

- **National Australia Bank** is a documented CyberArk Privilege Cloud customer (case study published at https://www.cyberark.com/customer-stories/national-australia-bank/), confirming production AU deployment.
- **Privilege Cloud** is available on AWS Sydney (ap-southeast-2), satisfying APRA CPS234 data-residency requirements for the SaaS deployment model.
- **Self-Hosted** deployment within XYZ's on-premises or sovereign-cloud datacentre satisfies full data-residency control with no third-party data egress.
- **IRAP assessment status:** Not publicly declared for PAM Self-Hosted as of 2026-05; SE confirmation required. `[OPEN-QUESTION]`
- **Essential 8 alignment:** RestrictAdminPriv (CPM + PSM), MFA (PVWA RADIUS/SAML), Application Control (EPM). Automated E8 scorecard output not native — requires SIEM integration + custom reporting. `[INDUSTRY-CONSENSUS]`
- **APRA CPS 234 §28:** PSM session recordings + PVWA audit exports constitute evidence for §28(b) and §28(c) controls. `[INDUSTRY-CONSENSUS]`

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## CyberArk PAM (Agent 03 wave 1)`:

- `cyberark-pam-product-2025` — https://www.cyberark.com/products/privileged-access-manager/
- `cyberark-privcloud-2025` — https://www.cyberark.com/products/privilege-cloud/
- `cyberark-epm-2025` — https://www.cyberark.com/products/endpoint-privilege-manager/
- `cyberark-pam-solutions-2025` — https://www.cyberark.com/solutions/
- `cyberark-nab-casestudy-2025` — https://www.cyberark.com/customer-stories/national-australia-bank/
- `cyberark-pam-discovery-2025` — https://www.cyberark.com/products/ (identity discovery and onboarding)
- `cyberark-priv-access-2025` — https://www.cyberark.com/products/privileged-access/
- `gartner-mq-pam-2025` — https://lp.cyberark.com/gartner-mq-pam-2025.html

---

## 8. Open questions for v1.0

1. **IRAP status:** Is PAM Self-Hosted or Privilege Cloud (AU region) currently IRAP-assessed? ASD ISM compliance requires this for PROTECTED data environments.
2. **CPM gMSA dependency mapping depth:** Does CPM v14.x natively resolve all dependent Windows Services, IIS app pools, and COM+ application pools before rotating gMSA? Or is dependency mapping only for traditional domain accounts?
3. **CCM (Certificate Manager) module scope:** Is the CyberArk Certificate Manager (CCM) a separate licence add-on to PAM, or bundled with Privilege Cloud Enterprise tier? What CAs does it natively integrate with (ADCS, DigiCert, Entrust, ACME)?
4. **HSM key-wrap ceremony:** What is the official documented procedure for initial EPV Master Key generation / sealing to Thales Luna or nCipher nShield in a multi-region AU deployment?
5. **Privilege Cloud AU multi-AZ:** Is Privilege Cloud on AWS Sydney deployed in multi-AZ / multi-region configuration for XYZ HA/DR requirements?
6. **Cloud IAM rotation depth:** Does CPM rotate GCP Service Account JSON keys natively, or only AWS IAM access keys and Azure SP secrets?
7. **PQC roadmap:** Has CyberArk published a post-quantum cryptography roadmap for EPV encryption and CCM certificate lifecycle (ML-KEM/ML-DSA)?

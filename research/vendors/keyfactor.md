# Vendor Profile — Keyfactor Machine Identity Security

**Tier:** pki-mim
**Primary docs:** https://docs.keyfactor.com (also https://www.keyfactor.com/products/)
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Keyfactor is a privately held machine identity and PKI security company (US HQ, offices in EU and APAC). Its product suite comprises **Keyfactor Command** (certificate lifecycle orchestration), **EJBCA Enterprise** (PKI platform — root/issuing/sub-CAs), **SignServer Enterprise** (server-side code- and document-signing), and **Bouncy Castle** (FIPS-certified Java/.NET crypto library, acquired 2022). Together these form the most vertically integrated PKI-plus-lifecycle stack on the market — a direct Venafi competitor with the differentiator of owning the full CA. Deployment options span on-premises software appliance, hardware appliance, containers (Kubernetes Helm), SaaS (Command SaaS Lite via Azure Marketplace; EJBCA SaaS on AWS and Azure), and PKI-as-a-Service (managed service). No publicly confirmed AU-sovereign data-residency region. Customers include EQ Bank (CA), M&T Bank (US), RSA Security, and ServiceNow.

[PUBLIC] [keyfactor-command-2024] [keyfactor-ejbca-2024] [keyfactor-platform-2024]

---

## 2. Architecture (≤ 250 words)

**Keyfactor Command** is the orchestration layer. It performs continuous certificate discovery across networks, cloud accounts, and keystores; tracks expiry; enforces policy; triggers automated renewal via ACME, REST API, or CA connectors (EJBCA, Microsoft ADCS, AWS Private CA, DigiCert, etc.); and provides RBAC-governed audit logs. It integrates with HSMs and cloud key vaults to ensure private keys are generated and stored securely. Deployment: on-prem Windows/Linux server, SaaS Lite (Azure Marketplace), or Kubernetes containers.

**EJBCA Enterprise** is the CA engine. Built on the world's most widely deployed open-source PKI codebase, it supports full root + issuing + sub-CA hierarchies. Enrollment protocols: ACME, EST, CMP, SCEP, Microsoft Autoenrollment (DCOM), SOAP, and REST API. CRL and OCSP for revocation. HSM-backed CA private keys (PKCS#11). **PQC-ready:** composite certificate issuance (ML-DSA combined with RSA/ECDSA/EdDSA) using Bouncy Castle algorithms; NIST FIPS 203/204/205 aligned. SaaS available on AWS and Azure.

**SignServer Enterprise** is a server-side signing engine. Supports code signing, PDF/XML/document signing, timestamp authority. Integrates with on-prem and cloud HSMs (or built-in hardware appliance). API-driven; CI/CD pipeline integration. Detailed signed audit logs per transaction.

**Bouncy Castle** underpins the cryptographic layer for EJBCA and SignServer. FIPS 140-2/3 certified Java module. Includes ML-DSA, ML-KEM, SLH-DSA (NIST PQC algorithms). Crypto-agility baked in.

No public IRAP or FedRAMP declaration found. SOC 2 compliance resources published; specific attestation scope requires vendor confirmation.

[keyfactor-command-2024] [keyfactor-ejbca-2024] [keyfactor-signserver-2024] [ejbca-docs-intro-2024] [ejbca-pqc-guide-2024]

---

## 3. NHI coverage map (≤ 600 words)

**NHI-001 — Cloud IAM principal**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Keyfactor is a PKI/cert platform; no cloud IAM role/SA management. [INDUSTRY-CONSENSUS]

**NHI-002 — Kubernetes ServiceAccount**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** EJBCA ACME + cert-manager integration issues TLS certs to K8s workloads; Command tracks K8s cert stores. Direct K8s SA token management is out of scope. [keyfactor-integrations-2024]

**NHI-003 — CI/CD pipeline identity**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** SignServer integrates with CI/CD tools for code signing; Command automates cert renewal in pipelines. Static-secret rotation not in scope. [keyfactor-signserver-2024]

**NHI-004 — Container / image-pull credential**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No container registry credential management; PKI scope only. [INDUSTRY-CONSENSUS]

**NHI-005 — Database service account**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No database dynamic credential engine. [INDUSTRY-CONSENSUS]

**NHI-006 — Application TLS server / mTLS workload identity**
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** Core value proposition: "discovers, protects, and automates every certificate, everywhere." EJBCA issues TLS and mTLS certs at scale. [keyfactor-command-2024]

**NHI-007 — Third-party SaaS API key / OAuth client**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Outside PKI/cert scope. [INDUSTRY-CONSENSUS]

**NHI-008 — Git platform credential**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No git credential management capability. [INDUSTRY-CONSENSUS]

**NHI-009 — Configuration-management / IaC agent identity**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Ansible + Terraform integrations for cert issuance from EJBCA/Command. [keyfactor-integrations-2024]

**NHI-010 — Monitoring / observability agent**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Cert-based auth can be issued to monitoring agents via EJBCA SCEP/ACME; lifecycle managed by Command. [keyfactor-ejbca-2024]

**NHI-011 — Message broker / event-bus client**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** TLS/mTLS cert issuance to broker clients; no dynamic secret engine for broker credentials. [INDUSTRY-CONSENSUS]

**NHI-012 — Active Directory / LDAP service account**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** EJBCA supports Microsoft Autoenrollment (DCOM/SCEP); Command discovers ADCS-issued certs. gMSA management is out of scope. [ejbca-docs-intro-2024]

**NHI-013 — Reverse-proxy / API-gateway upstream identity**
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** TLS/mTLS cert lifecycle for gateways; integrations with Akamai, F5, Nginx documented. [keyfactor-integrations-2024]

**NHI-014 — RPA bot identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No RPA bot credential management feature. [INDUSTRY-CONSENSUS]

**NHI-015 — Code-signing identity**
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** SignServer Enterprise provides centralised server-side code signing with HSM key custody, detailed audit logs. [keyfactor-signserver-2024]

**NHI-016 — Build provenance / SLSA attestation identity**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** SignServer signs build artifacts in CI/CD; SLSA-specific attestation metadata not natively generated. [keyfactor-signserver-2024]

**NHI-017 — Service mesh control-plane identity**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** EJBCA can serve as external CA for Istio/Consul Connect via ACME/REST; no native mesh control-plane agent. [INDUSTRY-CONSENSUS]

**NHI-018 — Confidential-computing attestation identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TEE/confidential compute attestation capability. [INDUSTRY-CONSENSUS]

**NHI-019 — AI agent / autonomous workflow identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No AI agent identity management. [INDUSTRY-CONSENSUS]

**NHI-020 — Model artifact / registry identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No model registry signing capability currently documented. [INDUSTRY-CONSENSUS]

**NHI-021 — IoT / OT device identity**
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** EJBCA is a leading IoT identity platform; EST, SCEP, CMP for device enrollment; scales to millions of devices. [keyfactor-ejbca-2024]

**NHI-022 — Mainframe / midrange service identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No mainframe cert management stated; requires custom integration. [INDUSTRY-CONSENSUS]

**NHI-023 — Database encryption / TDE master key identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Not a KMS/TDE key management platform. [INDUSTRY-CONSENSUS]

**NHI-024 — HSM / KMS operator / break-glass identity**
- **Coverage:** ADD-ON
- **Maturity:** 3
- **Evidence:** EJBCA uses PKCS#11 HSMs for CA key storage; SignServer supports cloud and on-prem HSMs. Break-glass quorum not natively managed. [keyfactor-ejbca-2024] [keyfactor-signserver-2024]

**NHI-025 — Certificate authority operator identity**
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** EJBCA provides full CA admin roles, RA roles, audit roles; Command RBAC governs enrollment and management. [ejbca-docs-intro-2024]

**NHI-026 — Backup / DR agent identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No backup agent credential management; cert issuance to backup agents possible but not a stated use case. [INDUSTRY-CONSENSUS]

**NHI-027 — Backend-for-frontend / OBO token holder**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** OAuth/OIDC token delegation is outside PKI platform scope. [INDUSTRY-CONSENSUS]

**NHI-028 — Federated B2B / Open Banking client identity**
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** EJBCA issues mTLS client certs for FAPI 2.0/Open Banking; financial services page references compliance use cases. [keyfactor-finserv-2024]

**NHI-029 — Service-account-as-human (shared functional ID)**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** PAM/shared account management not in scope. [INDUSTRY-CONSENSUS]

**NHI-030 — Browser / SaaS extension OAuth-app identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No OAuth app governance capability. [INDUSTRY-CONSENSUS]

**NHI-031 — Webhook / inbound integration identity**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** EJBCA can issue TLS client certs for webhook callers; no dedicated webhook signing/verification product. [INDUSTRY-CONSENSUS]

**NHI-032 — Network / infrastructure device identity**
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** EJBCA SCEP is standard for network device certificate enrollment (Cisco IOS/NX-OS, Juniper); Command discovers and rotates. [keyfactor-ejbca-2024]

**NHI-033 — Print / spooler / branch-peripheral identity**
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** EJBCA SCEP/EST can issue certs to branch peripherals; no dedicated peripheral management. [INDUSTRY-CONSENSUS]

**NHI-034 — Quantum-resistant / hybrid-PKI rotation identity**
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** EJBCA issues composite certs (ML-DSA + classical) using Bouncy Castle FIPS; PQC Lab Test Drive available. [ejbca-pqc-guide-2024]

**NHI-035 — Vault-internal / secrets-broker identity**
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Keyfactor is not a general-purpose secrets vault; no broker identity management. [INDUSTRY-CONSENSUS]

**NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch**
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** EJBCA can issue X.509 SVIDs (SPIFFE-compatible format) via ACME/REST; no native SPIRE server/agent. [INDUSTRY-CONSENSUS]

**NHI-037 — Forgotten / orphaned legacy identity**
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Command continuous discovery finds unknown/orphaned certs; expiry tracking and policy enforcement. [keyfactor-command-2024]

---

## 4. Use-case scoring (≤ 800 words)

**UC-F-001 — Prevent plaintext secrets in source repos**
- **Coverage:** GAP | **Maturity:** 0 | EJBCA/Command do not address secret sprawl in repos. [INDUSTRY-CONSENSUS]

**UC-F-002 — Detect and remediate secrets already in history**
- **Coverage:** GAP | **Maturity:** 0 | No git-history scanning capability. [INDUSTRY-CONSENSUS]

**UC-F-003 — JIT short-lived cloud credentials via OIDC**
- **Coverage:** GAP | **Maturity:** 0 | Cloud credential brokering not in scope. [INDUSTRY-CONSENSUS]

**UC-F-004 — Workload-attested ephemeral identity (SPIFFE/SPIRE)**
- **Coverage:** ADD-ON | **Maturity:** 2 | EJBCA issues X.509 SVIDs; no SPIRE server/agent. [INDUSTRY-CONSENSUS]

**UC-F-005 — Dynamic database credentials**
- **Coverage:** GAP | **Maturity:** 0 | No database secrets engine. [INDUSTRY-CONSENSUS]

**UC-F-006 — Automated rotation of long-lived static secrets**
- **Coverage:** GAP | **Maturity:** 0 | Command rotates certs; generic static secret rotation not in scope. [INDUSTRY-CONSENSUS]

**UC-F-007 — Immediate revocation on identity compromise**
- **Coverage:** NATIVE | **Maturity:** 4 | Command provides immediate cert revocation + CRL/OCSP propagation via EJBCA. [keyfactor-command-2024]

**UC-F-008 — Kubernetes secret consumption without on-disk plaintext**
- **Coverage:** ADD-ON | **Maturity:** 2 | cert-manager/ACME integration via EJBCA issues TLS certs to K8s pods; no secrets injection for non-cert secrets. [keyfactor-integrations-2024]

**UC-F-009 — Container image-pull credentials issued per workload**
- **Coverage:** GAP | **Maturity:** 0 | Registry credential management not in scope. [INDUSTRY-CONSENSUS]

**UC-F-010 — IaC / config-management secrets injected at apply-time**
- **Coverage:** ADD-ON | **Maturity:** 2 | Ansible/Terraform integrations issue certs at apply-time; general secrets injection not in scope. [keyfactor-integrations-2024]

**UC-F-011 — Observability-agent credentials rotated and scoped**
- **Coverage:** ADD-ON | **Maturity:** 2 | Cert-based auth for observability agents; Command tracks and rotates. [keyfactor-command-2024]

**UC-F-012 — Message-broker client identity hardening**
- **Coverage:** ADD-ON | **Maturity:** 2 | mTLS cert issuance for broker clients; no dynamic broker credentials. [keyfactor-ejbca-2024]

**UC-F-013 — gMSA / Kerberos modernisation for AD service accounts**
- **Coverage:** ADD-ON | **Maturity:** 2 | EJBCA Microsoft Autoenrollment; Command discovers ADCS certs. gMSA provisioning not native. [ejbca-docs-intro-2024]

**UC-F-014 — API-gateway upstream identity standardised**
- **Coverage:** NATIVE | **Maturity:** 3 | Command/EJBCA automates TLS/mTLS cert lifecycle for API gateways; Akamai integration. [keyfactor-integrations-2024]

**UC-F-015 — RPA bot credentials vaulted and session-bound**
- **Coverage:** GAP | **Maturity:** 0 | RPA credential management not in scope. [INDUSTRY-CONSENSUS]

**UC-F-016 — Keyless code- and artifact-signing in CI**
- **Coverage:** NATIVE | **Maturity:** 4 | SignServer provides server-side code signing integrated with CI/CD tools via API. [keyfactor-signserver-2024]

**UC-F-017 — TEE attestation gates secret release**
- **Coverage:** GAP | **Maturity:** 0 | No TEE/confidential compute attestation. [INDUSTRY-CONSENSUS]

**UC-F-018 — AI-agent / LLM tool-credential brokering**
- **Coverage:** GAP | **Maturity:** 0 | No AI agent credential management. [INDUSTRY-CONSENSUS]

**UC-F-019 — IoT / OT / branch-device identity enrolment**
- **Coverage:** NATIVE | **Maturity:** 4 | EJBCA EST/SCEP/CMP for IoT device enrollment at scale; industry-leading for connected devices. [keyfactor-ejbca-2024]

**UC-F-020 — Mainframe / midrange credential rotation pipeline**
- **Coverage:** GAP | **Maturity:** 0 | No mainframe credential management. [INDUSTRY-CONSENSUS]

**UC-F-021 — Backup / DR agent identity de-privileging**
- **Coverage:** GAP | **Maturity:** 0 | Not in scope. [INDUSTRY-CONSENSUS]

**UC-F-022 — Webhook inbound identity verification**
- **Coverage:** ADD-ON | **Maturity:** 2 | TLS client certs for webhook callers via EJBCA; no dedicated webhook signing. [INDUSTRY-CONSENSUS]

**UC-F-023 — Network-device credential modernisation**
- **Coverage:** NATIVE | **Maturity:** 3 | EJBCA SCEP is the standard for network device cert enrollment; Command lifecycle management. [keyfactor-ejbca-2024]

**UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity**
- **Coverage:** NATIVE | **Maturity:** 3 | EJBCA issues mTLS client certs for FAPI/Open Banking; financial services track record. [keyfactor-finserv-2024]

**UC-F-025 — OAuth-app / marketplace integration governance**
- **Coverage:** GAP | **Maturity:** 0 | OAuth app governance not in scope. [INDUSTRY-CONSENSUS]

**UC-F-026 — Vault-internal identity hardening**
- **Coverage:** GAP | **Maturity:** 0 | Not a secrets vault platform. [INDUSTRY-CONSENSUS]

**UC-F-027 — Orphaned / dormant NHI cleanup pipeline**
- **Coverage:** NATIVE | **Maturity:** 3 | Command continuous discovery identifies unknown/expired certs for remediation. [keyfactor-command-2024]

**UC-N-001 — Real-time secret-sprawl KPI dashboard**
- **Coverage:** ADD-ON | **Maturity:** 2 | Command provides cert inventory dashboards; non-cert secret sprawl not covered. [keyfactor-command-2024]

**UC-N-002 — NHI inventory and ownership attestation**
- **Coverage:** NATIVE | **Maturity:** 3 | Command tracks cert owners, metadata, expiry across enterprise. [keyfactor-command-2024]

**UC-N-003 — Rotation-coverage and freshness KPIs**
- **Coverage:** NATIVE | **Maturity:** 3 | Command expiry tracking, renewal coverage metrics, compliance reporting. [keyfactor-command-2024]

**UC-N-004 — Regulator audit evidence pack**
- **Coverage:** NATIVE | **Maturity:** 3 | Complete audit logs of cert/config changes; RBAC governance; compliance reports. [keyfactor-command-2024]

**UC-N-005 — Essential 8 / ZT control-area scorecard**
- **Coverage:** ADD-ON | **Maturity:** 2 | PKI/cert posture contributes to ZT but does not produce full E8 scorecard. [INDUSTRY-CONSENSUS]

**UC-N-006 — Vendor / SaaS supply-chain risk attestation**
- **Coverage:** GAP | **Maturity:** 0 | No vendor risk attestation workflow. [INDUSTRY-CONSENSUS]

**UC-N-007 — Data-sovereignty and residency assurance**
- **Coverage:** ADD-ON | **Maturity:** 1 | Self-hosted deployment possible; no AU sovereign cloud region confirmed. [INDUSTRY-CONSENSUS]

**UC-N-008 — Engineer training and secure-coding adoption KPI**
- **Coverage:** GAP | **Maturity:** 0 | Not in scope. [INDUSTRY-CONSENSUS]

**UC-N-009 — Exception register and risk-acceptance governance**
- **Coverage:** ADD-ON | **Maturity:** 2 | Command policy exceptions trackable; dedicated risk register not native. [INDUSTRY-CONSENSUS]

**UC-N-010 — Break-glass and quorum-operator governance**
- **Coverage:** ADD-ON | **Maturity:** 2 | EJBCA HSM key ceremonies; RBAC break-glass accounts manageable but no native quorum workflow. [keyfactor-ejbca-2024]

**UC-N-011 — Post-incident reporting and identity-driven RCA**
- **Coverage:** ADD-ON | **Maturity:** 2 | Command audit logs support RCA; dedicated incident reporting module not native. [keyfactor-command-2024]

**UC-N-012 — Supply-chain / SLSA-provenance assurance reporting**
- **Coverage:** ADD-ON | **Maturity:** 2 | SignServer signs artifacts; SLSA attestation records not natively generated. [keyfactor-signserver-2024]

**UC-N-013 — Crypto-agility and post-quantum readiness reporting**
- **Coverage:** NATIVE | **Maturity:** 4 | EJBCA composite cert support; Bouncy Castle PQC algorithms; PQC Lab Test Drive; "State of Quantum Readiness" report. [ejbca-pqc-guide-2024] [keyfactor-crypto-agility-2024]

**UC-N-014 — Vendor-evaluation matrix maintenance**
- **Coverage:** GAP | **Maturity:** 0 | No vendor matrix tooling. [INDUSTRY-CONSENSUS]

**UC-N-015 — Communications, change-comms and stakeholder cadence**
- **Coverage:** GAP | **Maturity:** 0 | Not in scope. [INDUSTRY-CONSENSUS]

**UC-N-016 — IoT / OT / branch-fleet posture reporting**
- **Coverage:** NATIVE | **Maturity:** 3 | Command tracks device cert posture across fleet; EJBCA enrollment protocols. [keyfactor-ejbca-2024] [keyfactor-command-2024]

**UC-N-017 — Observability/telemetry secret-leak governance**
- **Coverage:** GAP | **Maturity:** 0 | No telemetry secret scanning. [INDUSTRY-CONSENSUS]

**UC-N-018 — Confidential-computing / TEE attestation assurance**
- **Coverage:** GAP | **Maturity:** 0 | No TEE attestation posture reporting. [INDUSTRY-CONSENSUS]

**UC-N-019 — AI-agent / autonomous-workflow KPI suite**
- **Coverage:** GAP | **Maturity:** 0 | Not in scope. [INDUSTRY-CONSENSUS]

**UC-N-020 — Mainframe / legacy posture and exception transparency**
- **Coverage:** GAP | **Maturity:** 0 | Not in scope. [INDUSTRY-CONSENSUS]

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **Full PKI stack ownership.** Keyfactor uniquely combines EJBCA (CA), Command (lifecycle), SignServer (signing), and Bouncy Castle (crypto library) under one vendor. XYZ's SSL team could run EJBCA as the underlying CA engine with Command providing lifecycle governance — no separate CA vendor needed. Deep IoT/device identity (SCEP/EST/CMP) is industry-leading.

2. **Post-quantum cryptography leadership.** EJBCA composite certificate issuance (ML-DSA + classical hybrid) powered by Bouncy Castle is GA today with a PQC Lab Test Drive. This is the most complete, production-ready PQC migration path of any vendor in this matrix, directly addressing NHI-034 and UC-N-013. Keyfactor was an early NIST PQC adopter via its Bouncy Castle acquisition.

3. **Certificate lifecycle automation at scale.** Command's continuous discovery, policy-driven auto-renewal, ACME orchestration, and audit log capability directly address the certificate outage and compliance audit pain points (NHI-006, NHI-009–013, NHI-021, NHI-025, NHI-032, NHI-037) that motivated this PRD.

### Top 3 gaps

1. **Not a general-purpose secrets vault.** NHI-001 through NHI-008 (cloud IAM, K8s SA, CI/CD, container, database, API keys, git creds) are all GAP. Keyfactor must be paired with a vault platform (HashiCorp Vault, Akeyless, AWS/Azure) to cover the full XYZ secrets estate.

2. **No SPIFFE/SPIRE native integration.** Ephemeral workload identity (NHI-036, UC-F-004) requires EJBCA as an external CA via ACME/REST — functional but not a first-class SPIFFE-native product. Venafi (post-CyberArk) has a dedicated Workload Identity Manager.

3. **AU data residency / IRAP unclear.** EJBCA SaaS is on AWS and Azure but no AU region confirmation found publicly. For an XYZ bank regulated under CPS 234, unconfirmed residency is a procurement risk.

---

## 6. AU-specific notes (≤ 150 words)

**APRA CPS 234 alignment:** Keyfactor's cert lifecycle automation, RBAC audit logs, and revocation capabilities map to CPS 234 §22 (encryption key management), §28 (testing), and §36 (audit) requirements. Financial services page explicitly references compliance demonstrations.

**Essential 8:** Certificate-based authentication (Restrict Admin Privileges, Patch Applications) is enabled by Command/EJBCA; code signing (Application Control) by SignServer — but Keyfactor does not produce an E8 scorecard natively.

**IRAP:** No IRAP assessment found in public documentation. Self-hosted deployment avoids cloud residency concerns.

**AU customer references:** EQ Bank (Canadian), M&T Bank (US). No publicly cited AU bank reference found.

**Data residency:** EJBCA SaaS on AWS/Azure; no explicit AU region confirmation. Self-hosted on XYZ-owned infrastructure is the sovereignty-safe path. Requires vendor confirmation for SaaS AU region availability.

[keyfactor-finserv-2024] [INDUSTRY-CONSENSUS]

---

## 7. Citations

See BibTeX keys appended to `meta/citations.bib` under `## Keyfactor (Agent 03 wave 3)`:

- `keyfactor-command-2024`
- `keyfactor-ejbca-2024`
- `keyfactor-signserver-2024`
- `keyfactor-platform-2024`
- `ejbca-docs-intro-2024`
- `ejbca-pqc-guide-2024`
- `keyfactor-finserv-2024`
- `keyfactor-integrations-2024`
- `signserver-docs-2024`
- `keyfactor-crypto-agility-2024`
- `keyfactor-pki-automation-2024`
- `keyfactor-customers-2024`

---

## 8. Open questions for v1.0

1. **HSM vendor list:** Which specific HSMs (Thales Luna, Entrust nShield, nCipher, Fortanix) are qualified with EJBCA Enterprise and SignServer? Requires SE conversation or EJBCA HSM compatibility matrix.
2. **AU data residency:** Is EJBCA SaaS available in an Australian AWS/Azure region? What is the SLA for AU data sovereignty?
3. **IRAP assessment:** Has Keyfactor undergone or is planning an IRAP assessment for the XYZ government/regulated market?
4. **SPIFFE/SPIRE integration:** Is there a productised EJBCA-as-SPIRE-upstream-CA solution, or does this require custom integration?
5. **XYZ bank references:** Are there AU-based financial services customers (big-4 banks, regional banks) not publicly cited?
6. **SOC 2 Type II scope:** What services are in scope? Is EJBCA SaaS covered?
7. **FedRAMP:** Any US government authorization underway that would signal compliance maturity for AU regulated sectors?
8. **Bouncy Castle FIPS status:** Is BC FIPS Java 1.x in scope for APRA cryptographic controls, or does EJBCA use a different validated module?

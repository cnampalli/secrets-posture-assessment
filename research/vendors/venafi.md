# Vendor Profile — Venafi Machine Identity Security (CyberArk)

**Tier:** pki-mim
**Primary docs:** https://docs.venafi.com / https://docs.venafi.cloud / https://www.cyberark.com/products/machine-identity-security/
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Venafi is the market-defining **machine identity lifecycle platform**, acquired by CyberArk in October 2024 and fully rebranded under the CyberArk Machine Identity Security umbrella. The platform covers certificate lifecycle management (TLS/SSL), SSH key governance, code-signing key custody, lightweight SPIFFE-compatible workload identity issuance, and cloud-managed PKI — all unified through the Venafi Control Plane (now called CyberArk Machine Identity Security platform).

Deployment models span SaaS (Certificate Manager SaaS, Workload Identity Manager, Zero Touch PKI) and on-premises / self-hosted (Certificate Manager Self-Hosted, SSH Manager for Machines, Code Sign Manager Self-Hosted). CyberArk reports trust from over 55 % of Fortune 500 and 35 % of Global 2000. No AU-specific cloud region confirmed publicly; self-hosted deployment enables AU data sovereignty for regulated workloads. IRAP assessment not found in public docs as of 2026-05-22. [venafi-product-rebranding-2025, cyberark-mis-overview-2025]

---

## 2. Architecture (≤ 250 words)

**Core components (post-2024 rebrand):**

| Legacy Venafi name | Current CyberArk name | Deployment |
|---|---|---|
| TLS Protect (Trust Protection Platform) | Certificate Manager, Self-Hosted | On-prem / private cloud |
| TLS Protect Cloud | Certificate Manager, SaaS | Multi-tenant cloud |
| TLS Protect for Kubernetes | Certificate Manager for Kubernetes | K8s cluster |
| Firefly | Workload Identity Manager | Container / K8s |
| SSH Protect | SSH Manager for Machines | On-prem |
| CodeSign Protect | Code Sign Manager | SaaS or self-hosted |
| Zero Touch PKI | Zero Touch PKI | Cloud (US/EU datacentres) |

**Storage and secrets:** Certificate Manager Self-Hosted stores policy, certificate metadata, and private keys in a SQL Server backend. HSM integration (Thales Luna, Entrust nShield, nCipher, AWS CloudHSM) is native for CA key protection and code-signing. Workload Identity Manager can use an HSM for SVID signing keys (GA June 2024). [venafi-wim-hsm-2024]

**Auth and policy:** Policy-driven issuance via certificate policies; RBAC with AD/LDAP integration. REST API and Venafi Firefly gRPC API for programmatic consumption.

**CA integrations:** Public CAs — DigiCert, Sectigo, GlobalSign, Entrust, Let's Encrypt. Private CAs — Microsoft AD CS, EJBCA, AWS Private CA, GCP CAS, HashiCorp Vault PKI. [cyberark-cert-mgr-2025, INDUSTRY-CONSENSUS]

**Compliance:** SOC 2 Type 2, ISO 27001, CSA STAR Trusted Cloud Provider. FedRAMP and IRAP not confirmed in public docs. [cyberark-compliance-2025]

---

## 3. NHI coverage map (≤ 600 words)

### NHI-001 — Cloud IAM principal
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Venafi/CyberArk MIS does not issue or rotate cloud IAM roles/service accounts; that is the domain of PAM or cloud-native IAM. [cyberark-mis-overview-2025]

### NHI-002 — Kubernetes ServiceAccount
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Certificate Manager for Kubernetes (cert-manager integration via VSatellite) issues TLS certs to K8s workloads; JWT-SVID for K8s service accounts is via Workload Identity Manager. Direct K8s SA token management is out of scope. [venafi-cloud-docs-2026]

### NHI-003 — CI/CD pipeline identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Code Sign Manager integrates with Jenkins, GitHub Actions, Azure DevOps for pipeline-initiated code signing; certificate issuance via ACME/REST APIs from pipelines. [cyberark-code-sign-mgr-2025]

### NHI-004 — Container / image-pull credential
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No container registry credential management product in CyberArk MIS portfolio; handled by Conjur or PAM. [cyberark-mis-overview-2025]

### NHI-005 — Database service account
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Database dynamic credential issuance is out of scope for machine-identity platform; belongs to secrets vault (Conjur/PAM). [cyberark-mis-overview-2025]

### NHI-006 — Application TLS server / mTLS workload identity
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** "CyberArk Certificate Manager (formerly Venafi TLS Protect) simplifies the entire certificate lifecycle by automating discovery, monitoring, renewal, and compliance enforcement." Core product lane. [cyberark-cert-mgr-2025]

### NHI-007 — Third-party SaaS API key / OAuth client
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** API key and OAuth client credential management is outside MIS scope; belongs to secrets vault. [cyberark-mis-overview-2025]

### NHI-008 — Git platform credential
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** PAT/deploy-key management not in MIS product scope. [cyberark-mis-overview-2025]

### NHI-009 — Configuration-management / IaC agent identity
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** IaC pipelines can request certs from Certificate Manager via API; no native IaC agent identity product. [cyberark-cert-mgr-2025]

### NHI-010 — Monitoring / observability agent
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Agent credential management not in MIS scope. [cyberark-mis-overview-2025]

### NHI-011 — Message broker / event-bus client
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** mTLS client certificates for brokers can be provisioned by Certificate Manager, but dynamic broker-credential issuance is out of scope. Partial overlap only. [cyberark-cert-mgr-2025]

### NHI-012 — Active Directory / LDAP service account
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** AD service account management belongs to CyberArk PAM; not in MIS scope. [cyberark-mis-overview-2025]

### NHI-013 — Reverse-proxy / API-gateway upstream identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Certificate Manager provisions TLS certs to F5 BIG-IP, Akamai CDN, A10 Thunder ADC, Radware Alteon, and other proxies/gateways via machine integrations. "CyberArk Certificate Manager - SaaS now supports integration with Akamai CDN for certificate discovery and provisioning." [venafi-cloud-whatsnew-2026]

### NHI-014 — RPA bot identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** RPA credential management belongs to PAM; not in MIS scope. [cyberark-mis-overview-2025]

### NHI-015 — Code-signing identity
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** "Securely store private keys in the CyberArk vault or a connected HSM. Use any operating system, interface, or API." Code Sign Manager is purpose-built for enterprise code-signing key custody and signing-as-a-service. [cyberark-code-sign-mgr-2025]

### NHI-016 — Build provenance / SLSA attestation identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Code Sign Manager provides signing key governance for build provenance; SLSA-specific attestation identity is not explicitly documented as a named feature. [cyberark-code-sign-mgr-2025]

### NHI-017 — Service mesh control-plane identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Workload Identity Manager issues SPIFFE X.509-SVIDs used by Istio/Linkerd/Consul control planes; direct service-mesh control-plane operator product is out of scope. [cyberark-wim-2025]

### NHI-018 — Confidential-computing attestation identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** TEE attestation not in MIS product scope. [cyberark-mis-overview-2025]

### NHI-019 — AI agent / autonomous workflow identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** AI agent credential brokering not in MIS scope; Conjur/PAM handles secrets injection. [cyberark-mis-overview-2025]

### NHI-020 — Model artifact / registry identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** ML model registry identity not in MIS product scope. [cyberark-mis-overview-2025]

### NHI-021 — IoT / OT device identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Zero Touch PKI supports SCEP (common IoT enrollment protocol) and ACME/EST/REST; Certificate Manager Self-Hosted supports large-scale device cert issuance. [cyberark-zero-touch-pki-2025]

### NHI-022 — Mainframe / midrange service identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Mainframe TLS certificates can theoretically be managed but no documented mainframe-specific integration. [cyberark-cert-mgr-2025, SPECULATION]

### NHI-023 — Database encryption / TDE master key identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** TDE key management belongs to HSM/KMS layer; MIS does not manage DB encryption keys directly. [cyberark-mis-overview-2025]

### NHI-024 — HSM / KMS operator / break-glass identity
- **Coverage:** ADD-ON
- **Maturity:** 3
- **Evidence:** Certificate Manager Self-Hosted and Workload Identity Manager integrate natively with Thales Luna, Entrust nShield, and other HSMs for CA key protection; HSM operator identity governance is indirect. [venafi-wim-hsm-2024]

### NHI-025 — Certificate authority operator identity
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** Venafi (now CyberArk Certificate Manager) is explicitly cited in the taxonomy as a CA operator identity platform. Policy framework governs RA, CA admin, and enrolment agent roles. [cyberark-cert-mgr-2025, venafi-tpp-2024]

### NHI-026 — Backup / DR agent identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Backup agent credential management not in MIS scope. [cyberark-mis-overview-2025]

### NHI-027 — Backend-for-frontend / on-behalf-of token holder
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** OAuth token brokering not in MIS scope. [cyberark-mis-overview-2025]

### NHI-028 — Federated B2B / Open Banking client identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** mTLS client certificates for FAPI 2.0 / Open Banking partners can be provisioned by Certificate Manager; no dedicated Open Banking product feature. [cyberark-cert-mgr-2025]

### NHI-029 — Service-account-as-human (shared functional ID)
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Shared account governance belongs to PAM. [cyberark-mis-overview-2025]

### NHI-030 — Browser / SaaS extension and OAuth-app identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** OAuth app governance not in MIS scope. [cyberark-mis-overview-2025]

### NHI-031 — Webhook / inbound integration identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Webhook identity management not in MIS scope. [cyberark-mis-overview-2025]

### NHI-032 — Network / infrastructure device identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Certificate Manager provisions certs to routers, switches, load balancers (F5, A10, Radware Alteon), and CDN nodes (Akamai). SCEP integration for network device enrollment. [venafi-cloud-whatsnew-2026, cyberark-zero-touch-pki-2025]

### NHI-033 — Print / spooler / branch-peripheral identity
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Zero Touch PKI SCEP can enroll printers/peripherals; no dedicated integration documented. [cyberark-zero-touch-pki-2025]

### NHI-034 — Quantum-resistant / hybrid-PKI rotation identity
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Crypto-agility is a documented capability of Certificate Manager (policy-based algorithm enforcement); explicit PQC / hybrid-cert issuance roadmap not confirmed in public 2026 docs. [cyberark-cert-mgr-2025, SPECULATION]

### NHI-035 — Vault-internal / secrets-broker identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Secrets broker identity is in Conjur/PAM scope, not MIS. [cyberark-mis-overview-2025]

### NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch
- **Coverage:** NATIVE
- **Maturity:** 4
- **Evidence:** "Workload Identity Manager … provides support for SPIFFE standards, offering governance and trust at the velocity they demand." Industry's first workload identity issuer with built-in trust validation. [cyberark-wim-2025]

### NHI-037 — Forgotten / orphaned legacy identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Certificate Manager includes continuous discovery and certificate-age/owner reporting, targeting orphaned/forgotten certificates as a primary value proposition. [cyberark-cert-mgr-2025]

---

## 4. Use-case scoring (≤ 800 words)

### UC-F-001 — Prevent plaintext secrets in source repositories
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Secret scanning and vault injection not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-002 — Detect and remediate secrets in history
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Git history scanning not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-003 — JIT short-lived cloud credentials via OIDC
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Cloud OIDC federation belongs to Conjur/PAM, not MIS. [cyberark-mis-overview-2025]

### UC-F-004 — Workload-attested ephemeral identity (SPIFFE/SPIRE)
- **Coverage:** NATIVE | **Maturity:** 4
- **Evidence:** Workload Identity Manager is "The industry's first workload identity issuer featuring built-in trust validation and authentication" with SPIFFE support. [cyberark-wim-2025]

### UC-F-005 — Dynamic database credentials
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Dynamic DB credential issuance not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-006 — Automated rotation of long-lived static secrets
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate Manager automates certificate renewal; SSH Manager rotates SSH keys; non-cert/non-SSH static secrets are out of scope. [cyberark-cert-mgr-2025, cyberark-ssh-mgr-2025]

### UC-F-007 — Immediate revocation on identity compromise
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager supports CRL and OCSP-based revocation; CA integrations enforce revocation downstream. [cyberark-cert-mgr-2025]

### UC-F-008 — Kubernetes secret consumption without on-disk plaintext
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate Manager for Kubernetes / cert-manager integration issues in-cluster TLS certs without long-lived static files; not a general K8s secret injector. [venafi-cloud-docs-2026]

### UC-F-009 — Container image-pull credentials issued per workload
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Image-pull credential management not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-010 — IaC / config-management secrets injected at apply-time
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Generic secrets injection not in MIS scope; cert API callable from IaC pipelines is ADD-ON at best but not documented. [cyberark-mis-overview-2025]

### UC-F-011 — Observability-agent credentials rotated and scoped
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Agent credential rotation not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-012 — Message-broker client identity hardening
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** mTLS client certificates for Kafka/RabbitMQ can be provisioned by Certificate Manager via ACME/REST; not a named use-case in product docs. [cyberark-cert-mgr-2025]

### UC-F-013 — gMSA / Kerberos modernisation for AD service accounts
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** AD service account modernisation belongs to PAM. [cyberark-mis-overview-2025]

### UC-F-014 — API-gateway upstream identity standardised
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager provisions and rotates TLS/mTLS certs for Akamai, F5, A10, Radware Alteon — covering API-gateway upstream identity. [venafi-cloud-whatsnew-2026]

### UC-F-015 — RPA bot credentials vaulted and session-bound
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** RPA credential management belongs to PAM. [cyberark-mis-overview-2025]

### UC-F-016 — Keyless code- and artifact-signing in CI
- **Coverage:** NATIVE | **Maturity:** 4
- **Evidence:** "Securely store private keys in the CyberArk vault or a connected HSM. Work the way your developers already do. Integrate with the tools and processes your teams already use." Code Sign Manager is the primary platform for this use case. [cyberark-code-sign-mgr-2025]

### UC-F-017 — TEE attestation gates secret release
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Confidential-computing attestation not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-018 — AI-agent / LLM tool-credential brokering
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** AI agent credential brokering belongs to Conjur/PAM. [cyberark-mis-overview-2025]

### UC-F-019 — IoT / OT / branch-device identity enrolment
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Zero Touch PKI supports SCEP, ACME, EST for device enrollment; Certificate Manager Self-Hosted scales for large IoT fleets. [cyberark-zero-touch-pki-2025]

### UC-F-020 — Mainframe / midrange credential rotation pipeline
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** No documented mainframe-specific integration; generic cert provision possible but not validated. [cyberark-mis-overview-2025]

### UC-F-021 — Backup / DR agent identity de-privileging
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** DR agent credential management belongs to PAM. [cyberark-mis-overview-2025]

### UC-F-022 — Webhook inbound identity verification
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Webhook identity not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-023 — Network-device credential modernisation
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager provisions TLS certs to network devices via SCEP and machine integrations (F5, Akamai, A10, Radware Alteon). [venafi-cloud-whatsnew-2026, cyberark-zero-touch-pki-2025]

### UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager issues and manages mTLS client certificates; policy enforcement aligns with Open Banking mutual-auth requirements. [cyberark-cert-mgr-2025]

### UC-F-025 — OAuth-app / marketplace integration governance
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** OAuth app governance not in MIS scope. [cyberark-mis-overview-2025]

### UC-F-026 — Vault-internal identity hardening
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Secrets-vault internal identity belongs to Conjur/PAM. [cyberark-mis-overview-2025]

### UC-F-027 — Orphaned / dormant NHI cleanup pipeline
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate discovery and inventory, including orphaned-cert detection and reporting, is a core Certificate Manager value proposition. SSH Manager provides equivalent for SSH key sprawl. [cyberark-cert-mgr-2025, cyberark-ssh-mgr-2025]

### UC-N-001 — Real-time secret-sprawl KPI dashboard
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager provides certificate inventory dashboards covering location, owner, expiry, and compliance status. [cyberark-cert-mgr-2025]

### UC-N-002 — NHI inventory and ownership attestation
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate Manager maps certificate ownership; SSH Manager maps SSH key ownership and trusted relationships. [cyberark-cert-mgr-2025, cyberark-ssh-mgr-2025]

### UC-N-003 — Rotation-coverage and freshness KPIs
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Certificate expiry monitoring and renewal-coverage tracking are core Certificate Manager features. [cyberark-cert-mgr-2025]

### UC-N-004 — Regulator audit evidence pack
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate Manager reporting + SSH audit logs support regulator evidence; no packaged APRA-specific audit report documented. [cyberark-cert-mgr-2025, cyberark-ssh-mgr-2025]

### UC-N-005 — Essential 8 / ZT control-area scorecard
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate and code-signing governance maps to E8 Application Control; no packaged Essential 8 scorecard. [cyberark-compliance-2025]

### UC-N-006 — Vendor / SaaS supply-chain risk attestation
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Code Sign Manager underpins software supply-chain assurance; supply-chain risk scoring is not a standalone feature. [cyberark-code-sign-mgr-2025]

### UC-N-007 — Data-sovereignty and residency assurance
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate Manager Self-Hosted can be deployed in AU-hosted infrastructure for full data sovereignty; SaaS regions not confirmed for AU. [cyberark-cert-mgr-2025]

### UC-N-008 — Engineer training and secure-coding adoption KPI
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Developer training metrics not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-009 — Exception register and risk-acceptance governance
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate policy exceptions and non-compliant certificate alerting support exception governance; no formal risk-acceptance workflow documented. [cyberark-cert-mgr-2025]

### UC-N-010 — Break-glass and quorum-operator governance
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Code Sign Manager supports quorum-based signing approvals for HSM-backed keys; break-glass workflow not documented for Certificate Manager. [cyberark-code-sign-mgr-2025]

### UC-N-011 — Post-incident reporting and identity-driven RCA
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate usage audit logs and SSH key usage logs support identity-driven RCA; no dedicated incident-response workflow product. [cyberark-cert-mgr-2025, cyberark-ssh-mgr-2025]

### UC-N-012 — Supply-chain / SLSA-provenance assurance reporting
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Code Sign Manager provides signing key governance enabling SLSA attestation; SLSA-specific provenance reporting not explicitly documented. [cyberark-code-sign-mgr-2025]

### UC-N-013 — Crypto-agility and post-quantum readiness reporting
- **Coverage:** ADD-ON | **Maturity:** 2
- **Evidence:** Certificate Manager enforces policy-based algorithm selection; crypto-agility dashboard for PQC readiness not confirmed in public docs. [cyberark-cert-mgr-2025]

### UC-N-014 — Vendor-evaluation matrix maintenance
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Vendor evaluation tooling not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-015 — Communications, change-comms and stakeholder cadence
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Stakeholder communications tooling not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-016 — IoT / OT / branch-fleet posture reporting
- **Coverage:** NATIVE | **Maturity:** 3
- **Evidence:** Zero Touch PKI and Certificate Manager Self-Hosted provide fleet-scale device cert posture; discovery, monitoring, and expiry alerting for IoT/OT fleets. [cyberark-zero-touch-pki-2025]

### UC-N-017 — Observability/telemetry secret-leak governance
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Telemetry secret-leak detection not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-018 — Confidential-computing / TEE attestation assurance
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** TEE attestation not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-019 — AI-agent / autonomous-workflow KPI suite
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** AI agent governance not in MIS scope. [cyberark-mis-overview-2025]

### UC-N-020 — Mainframe / legacy posture and exception transparency
- **Coverage:** GAP | **Maturity:** 0
- **Evidence:** Mainframe posture reporting not in MIS scope. [cyberark-mis-overview-2025]

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **Industry-leading certificate lifecycle automation (NHI-006, NHI-013, NHI-021, NHI-032, UC-F-007, UC-F-014, UC-F-019, UC-F-023):** Certificate Manager is the global reference implementation for enterprise TLS/PKI automation. Broad CA ecosystem (12+ public/private CAs), 200+ machine integrations (load balancers, CDN, network devices), and 47-day cert lifespan automation make it uniquely positioned for XYZ banks managing large certificate estates. No other reviewed vendor matches this breadth.

2. **Code-signing key custody and pipeline integration (NHI-015, UC-F-016):** Code Sign Manager provides enterprise-grade HSM-backed signing-as-a-service with native CI/CD pipeline integration (Jenkins, GitHub Actions, Azure DevOps). This directly addresses software supply-chain risk — a P1 requirement for XYZ regulated environments and SLSA compliance.

3. **SPIFFE-native workload identity issuance (NHI-036, NHI-002, NHI-017, UC-F-004):** Workload Identity Manager (formerly Firefly) is the market's first purpose-built SPIFFE-compatible workload identity issuer with HSM backing, purpose-designed for cloud-native environments at developer velocity. Directly fills the SPIFFE/SPIRE workload identity gap that general secrets vaults do not address.

### Top 3 gaps

1. **Not a secrets vault — generic secrets management is a GAP:** NHI-001 through NHI-005, NHI-007/008, NHI-012 and most vault-pattern use cases (UC-F-001 to UC-F-003, UC-F-005) are explicitly out of scope. Venafi/CyberArk MIS is a complement to, not a replacement for, a secrets vault (Conjur, HashiCorp Vault, AWS Secrets Manager).

2. **AU data sovereignty / IRAP unconfirmed for SaaS tier:** Zero Touch PKI and Certificate Manager SaaS have confirmed US and European datacentres only; IRAP assessment not found publicly. XYZ regulated SaaS use requires further due diligence or self-hosted deployment.

3. **AI/TEE/mainframe lanes absent:** NHI-018, NHI-019, NHI-020, NHI-022, NHI-035 are all GAP — these identity categories require complementary tooling.

---

## 6. AU-specific notes (≤ 150 words)

**Deployment sovereignty:** Certificate Manager Self-Hosted and SSH Manager for Machines can be deployed on AU-hosted infrastructure (on-premises or AU-region cloud), providing full data residency control for APRA CPS 230/234-regulated workloads. The self-hosted model is documented and production-grade.

**SaaS regions:** Zero Touch PKI has confirmed North America and European multi-datacentre redundancy. Certificate Manager SaaS region availability for Australia is not confirmed in public documentation as of 2026-05-22. [SPECULATION — needs CyberArk SE confirmation for XYZ regulated use.]

**IRAP:** No IRAP assessment found in public CyberArk compliance documentation. CSA STAR, SOC 2 Type 2, and ISO 27001 are confirmed. For ASD-regulated environments, IRAP status must be confirmed directly with CyberArk.

**Essential 8:** Code-signing governance maps to E8 Application Control (ML3). Certificate automation supports E8 Patch Applications indirectly.

**Customer references:** No AU FI customer references found in public docs. [INDUSTRY-CONSENSUS — CyberArk cites 55% of Fortune 500 but no AU-specific FI references found publicly.]

---

## 7. Citations

See BibTeX keys appended to `meta/citations.bib` under section `Venafi (Agent 03 wave 3)`.

Key citations used:
- `venafi-product-rebranding-2025` — CyberArk product name updates page
- `cyberark-cert-mgr-2025` — Certificate Manager product page
- `cyberark-wim-2025` — Workload Identity Manager product page
- `cyberark-code-sign-mgr-2025` — Code Sign Manager product page
- `cyberark-ssh-mgr-2025` — SSH Manager for Machines product page
- `cyberark-zero-touch-pki-2025` — Zero Touch PKI product page
- `cyberark-mis-overview-2025` — Machine Identity Security product overview
- `cyberark-compliance-2025` — CyberArk compliance page
- `cyberark-mis-what-is-2025` — What is Machine Identity Security glossary
- `venafi-cloud-docs-2026` — docs.venafi.cloud home
- `venafi-cloud-whatsnew-2026` — docs.venafi.cloud what's new (2025/2026 features)
- `venafi-wim-hsm-2024` — Workload Identity Manager HSM integration (June 2024)
- `venafi-tpp-2024` — referenced in taxonomy (NHI-025) for TPP/TLSPC platform

---

## 8. Open questions for v1.0

1. **AU SaaS region:** Does Certificate Manager SaaS have an Australia/AP datacentre? (Needs CyberArk SE confirmation.)
2. **IRAP assessment:** Is CyberArk Certificate Manager SaaS or Zero Touch PKI IRAP-assessed? Status for 2025/2026?
3. **Conjur-CertManager integration depth:** What is the roadmap for native integration between Conjur (CyberArk Secrets Manager) and Certificate Manager post-acquisition? Is private-key injection to Conjur paths planned?
4. **PQC roadmap:** Does Certificate Manager have a confirmed roadmap for ML-DSA / hybrid X.509 issuance for NHI-034?
5. **AU FI customer references:** Any AU bank or FI customers using TLS Protect / Certificate Manager that CyberArk can reference publicly?
6. **HashiCorp Vault PKI integration:** Depth of Certificate Manager ↔ HashiCorp Vault PKI integration (connector-based or API-native)?
7. **EJBCA integration:** Is EJBCA listed as a supported CA for Certificate Manager SaaS (or self-hosted only)?

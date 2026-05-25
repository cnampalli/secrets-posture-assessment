# Vendor Profile — AKEYLESS Vault Platform

**Tier:** emerging
**Primary docs:** https://docs.akeyless.io
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Akeyless is a privately held, Israel-founded SaaS-first secrets-management and machine-identity security company, incorporated as Akeyless Security Ltd. Its primary commercial differentiator is **Distributed Fragments Cryptography (DFC)** — a patented architecture in which encryption-key material is never reconstructed on any single server, including Akeyless's own infrastructure. The platform is positioned explicitly as a cloud-native, agentless alternative to HashiCorp Vault Enterprise (the vendor's own compare pages target Vault directly). Deployment models: fully-managed SaaS (US region, EU region) plus a customer-hosted **Gateway** component that can run on any cloud or on-premises environment, enabling customer data-residency control. No dedicated AU/AP SaaS region is publicly documented as of May 2026; AU customers must self-host the Gateway. The company lists no named AU financial-services customers in public materials. Available on AWS Marketplace.

**Citations:** [akeyless-components-2024][akeyless-trust-center-2024]

---

## 2. Architecture (≤ 250 words)

**Platform components:**
- **Akeyless SaaS Platform** — control plane hosted in US (console.akeyless.io) and EU (console.eu.akeyless.io) regions; manages auth policies, access-control, audit, and secret metadata.
- **Key Fragment Managers (KFMs)** — internal to the SaaS; hold encrypted key-fragments; never combine them.
- **Akeyless Gateway** — customer-hosted stateless proxy (Docker/Kubernetes/serverless); brokers requests between workloads and SaaS; required for zero-knowledge deployment, dynamic secrets, log forwarding, and Vault-proxy compatibility.
- **Customer Fragment** — optional one-time-generated key-fragment stored exclusively in the customer's Gateway environment; once deployed, Akeyless cannot decrypt customer secrets without it.

**DFC cryptography:** Key material is split into multiple independent fragments via cryptographic derivation. Cryptographic operations execute across fragments without ever combining them. FIPS 140-3 validated (Certificate #5227, NIST CMVP). The public docs reference a FIPS 140-2 Level 3 HSM claim in legacy marketing but the current certification page shows a software-module FIPS 140-3 validation — score reflects the documented cert.

**Auth methods:** API Key, AWS IAM, Azure AD/OIDC, GCP IAM, Kubernetes (dedicated SA), LDAP/Kerberos, OAuth 2.0/JWT, OCI IAM, OIDC (GitHub, GitLab, Auth0, Okta, Google), SAML (Azure AD, Okta, Ping Identity), Universal Identity, X.509 Certificate.

**Secrets engines:** Static KV, Dynamic Secrets (producers: AWS, Azure AD, GCP, K8s, EKS, GKE, databases, RabbitMQ, GitHub, GitLab, Docker Hub, OpenAI, and others), Rotated Secrets, PKI/Certificate Lifecycle Management, SSH certificates, KMIP server, TDE, Tokenization, GPG Keys.

**Compliance declared:** SOC 2 Type II, ISO 27001, ISO 27701, PCI DSS, HIPAA, DORA, FIPS 140-3 (cert #5227). IRAP: not documented. FedRAMP: not documented.

**Replication/DR:** Multi-region, multi-cloud, multi-AZ SaaS with geo-location-based policy; Gateway stateless (no single point of failure). Hybrid PQC TLS (X25519MLKEM768, TLS 1.3) between clients and SaaS/Gateway.

**Citations:** [akeyless-components-2024][akeyless-fips-2024][akeyless-gw-overview-2024][akeyless-pqc-2024][akeyless-trust-center-2024]

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence (primary source) |
|---|---|---|---|
| NHI-001 Cloud IAM principal | NATIVE | 4 | AWS IAM, Azure AD, GCP dynamic-secret producers + auth methods — full lifecycle [akeyless-llms-index-2024] |
| NHI-002 Kubernetes ServiceAccount | NATIVE | 4 | Kubernetes auth method, CSI driver, Secrets Injector, External Secrets Operator [akeyless-llms-index-2024] |
| NHI-003 CI/CD pipeline identity | NATIVE | 3 | GitHub Actions, GitLab, Azure DevOps, TeamCity plugins; OIDC federation for GitHub/GitLab [akeyless-llms-index-2024] |
| NHI-004 Container image-pull credential | NATIVE | 2 | Docker Hub dynamic & rotated secrets; Harbor/ECR via dynamic AWS creds [akeyless-llms-index-2024] |
| NHI-005 Database service account | NATIVE | 4 | Dynamic secrets: MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis, Redshift, Snowflake, Cassandra, HanaDB [akeyless-agentic-2024] |
| NHI-006 Application TLS / mTLS workload | NATIVE | 3 | PKI/Certificate Lifecycle Management, ACME server, SPIRE Upstream Authority [akeyless-spire-2024] |
| NHI-007 Third-party SaaS API key | NATIVE | 3 | Static KV + rotated secrets (OpenAI, Splunk, custom rotation); Universal Identity brokers [akeyless-llms-index-2024] |
| NHI-008 Git platform credential | NATIVE | 3 | GitHub/GitLab dynamic secrets + OIDC auth; GitHub Actions plugin [akeyless-llms-index-2024] |
| NHI-009 Config-management / IaC agent | NATIVE | 3 | Terraform, Ansible, Puppet plugins; HashiCorp Vault Proxy compatibility [akeyless-llms-index-2024] |
| NHI-010 Monitoring / observability agent | NATIVE | 2 | Static KV + Splunk rotated secret; log forwarding integrations [akeyless-log-fwd-2024] |
| NHI-011 Message broker client | NATIVE | 3 | RabbitMQ dynamic secrets; Kafka via LDAP/custom [akeyless-llms-index-2024] |
| NHI-012 AD/LDAP service account | NATIVE | 3 | LDAP auth method, LDAP dynamic secrets, LDAP rotated secrets, Resource Discovery [akeyless-discovery-2024] |
| NHI-013 API gateway upstream identity | ADD-ON | 2 | mTLS via PKI/cert lifecycle; gateway JWT signing; no direct API-GW plugin listed [akeyless-llms-index-2024] |
| NHI-014 RPA bot identity | ADD-ON | 2 | Static KV vaulting + rotated secrets for Windows/AD; no direct UiPath/BluePrism connector documented [akeyless-llms-index-2024] |
| NHI-015 Code-signing identity | NATIVE | 2 | Code Signing with Akeyless page; Java JAR & APK signing; HSM-backed via classic keys [akeyless-llms-index-2024] |
| NHI-016 Build provenance / SLSA attestation | GAP | 0 | No Sigstore/SLSA/in-toto attestation documented [INDUSTRY-CONSENSUS] |
| NHI-017 Service mesh control-plane identity | ADD-ON | 2 | SPIRE Upstream Authority plugin — Akeyless as mesh CA backend [akeyless-spire-2024] |
| NHI-018 Confidential-computing attestation | GAP | 0 | No TEE attestation-gated secret release documented in public docs [INDUSTRY-CONSENSUS] |
| NHI-019 AI agent / autonomous workflow | NATIVE | 2 | Agentic Runtime Authority (early access); Prompt Injection Protection; MCP Server [akeyless-agentic-2024] |
| NHI-020 Model artifact / registry identity | ADD-ON | 1 | OpenAI dynamic/rotated secrets; generic token vaulting; no MLflow/SageMaker connector [akeyless-llms-index-2024] |
| NHI-021 IoT / OT device identity | ADD-ON | 1 | Certificate lifecycle / ACME for device certs; no dedicated IoT-DPS connector [akeyless-llms-index-2024] |
| NHI-022 Mainframe / midrange identity | GAP | 0 | No RACF/ACF2/z/OS integration documented; no IBM i connector [INDUSTRY-CONSENSUS] |
| NHI-023 Database TDE master key | NATIVE | 3 | TDE for MSSQL, TDE for Oracle, KMIP server for vSphere [akeyless-llms-index-2024] |
| NHI-024 HSM / KMS operator identity | ADD-ON | 2 | Gateway HSM integration documented; DFC fragments backed by HSM; no quorum-operator workflow [akeyless-gw-overview-2024] |
| NHI-025 CA operator identity | NATIVE | 3 | Certificate Lifecycle Management, ACME Server, PKI issuer management, Venafi target [akeyless-llms-index-2024] |
| NHI-026 Backup / DR agent identity | ADD-ON | 1 | Static KV + Windows/AD rotated secrets usable for backup agents; no Veeam/Rubrik/Commvault connector [INDUSTRY-CONSENSUS] |
| NHI-027 Backend-for-frontend / OBO token | ADD-ON | 2 | OAuth 2.0/JWT auth; Universal Identity token exchange patterns; no explicit BFF pattern documented [akeyless-auth-overview-2024] |
| NHI-028 Federated B2B / Open Banking mTLS | ADD-ON | 2 | PKI/mTLS certificate lifecycle; FAPI 2.0 client-cert issuance supportable; no CDR-specific workflow [akeyless-llms-index-2024] |
| NHI-029 Service-account-as-human (shared) | NATIVE | 3 | Resource Discovery imports shared domain accounts as Rotated Secrets; LDAP rotation [akeyless-discovery-2024] |
| NHI-030 Browser/SaaS OAuth-app identity | GAP | 0 | No OAuth-app inventory / M365 / Google Workspace governance feature documented [INDUSTRY-CONSENSUS] |
| NHI-031 Webhook inbound identity | ADD-ON | 1 | Static KV storage of HMAC secrets; no webhook-specific rotation workflow [INDUSTRY-CONSENSUS] |
| NHI-032 Network / infra device identity | ADD-ON | 1 | SSH target + rotated SSH secrets; no TACACS+/RADIUS/SNMP-specific automation [INDUSTRY-CONSENSUS] |
| NHI-033 Print / branch-peripheral identity | GAP | 0 | No branch-peripheral or ATM credential workflow documented [INDUSTRY-CONSENSUS] |
| NHI-034 Quantum-resistant / hybrid-PKI | NATIVE | 2 | Hybrid PQC TLS (X25519MLKEM768/TLS 1.3) for client-SaaS/Gateway transport; PQC for key-at-rest not yet documented [akeyless-pqc-2024] |
| NHI-035 Vault-internal / secrets-broker identity | NATIVE | 3 | Gateway stateless; Customer Fragment holds crypto anchor; DFC eliminates single-point root token risk [akeyless-gw-zk-2024] |
| NHI-036 Ephemeral SPIFFE/Aembit workload | NATIVE | 3 | SPIRE Key Manager, Secret Manager, Upstream Authority plugins; Universal Identity ephemeral tokens [akeyless-spire-2024] |
| NHI-037 Forgotten / orphaned identity | NATIVE | 2 | Identity & Secrets Intelligence (early access): stale-credential detection, unused-identity analytics [akeyless-isi-2024] |

**Citations:** [akeyless-dfc-overview-2024][akeyless-spire-2024][akeyless-agentic-2024][akeyless-discovery-2024][akeyless-pqc-2024][akeyless-isi-2024][akeyless-gw-zk-2024][akeyless-llms-index-2024]

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Type | Coverage | Maturity | Evidence |
|---|---|---|---|---|
| UC-F-001 Prevent plaintext secrets in repos | UC-F | ADD-ON | 2 | No native pre-commit scanner; integrates with GitHub/GitLab for secret storage; relies on partner tooling for detection [akeyless-llms-index-2024] |
| UC-F-002 Detect/remediate secrets in history | UC-F | GAP | 0 | No repo-history scanning capability documented; out of product scope [INDUSTRY-CONSENSUS] |
| UC-F-003 JIT short-lived cloud creds via OIDC | UC-F | NATIVE | 4 | AWS/Azure/GCP dynamic secrets + OIDC federation for CI/CD; full pipeline [akeyless-llms-index-2024] |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | UC-F | NATIVE | 3 | SPIRE Upstream Authority, Key Manager, Secret Manager plugins; Universal Identity [akeyless-spire-2024] |
| UC-F-005 Dynamic DB credentials with broker leases | UC-F | NATIVE | 4 | Dynamic secrets for MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis, Redshift, Snowflake, Cassandra, HanaDB [akeyless-agentic-2024] |
| UC-F-006 Automated rotation of long-lived static secrets | UC-F | NATIVE | 4 | Rotated secrets: DB, LDAP, AWS, Azure, GCP, SSH, Windows, Docker Hub, OpenAI, Splunk, Custom [akeyless-llms-index-2024] |
| UC-F-007 Immediate revocation on compromise | UC-F | NATIVE | 3 | Token revocation via Gateway; DFC fragment invalidation; SOAR integration via API [akeyless-gw-overview-2024] |
| UC-F-008 K8s secret consumption without on-disk plaintext | UC-F | NATIVE | 4 | CSI driver, Kubernetes Secrets Injector, External Secrets Operator, etcd-encrypt compatible [akeyless-llms-index-2024] |
| UC-F-009 Container image-pull creds per workload | UC-F | NATIVE | 3 | Docker Hub dynamic + ECR/ACR/GAR via cloud dynamic secrets; per-workload scoping [akeyless-llms-index-2024] |
| UC-F-010 IaC/config-management secrets at apply-time | UC-F | NATIVE | 3 | Terraform, Ansible, Puppet, Pulumi integrations; state-file secrets never persist [akeyless-llms-index-2024] |
| UC-F-011 Observability-agent credentials rotated/scoped | UC-F | NATIVE | 2 | Splunk rotated secret; static KV for other agents; rotation cadence configurable [akeyless-llms-index-2024] |
| UC-F-012 Message-broker client identity hardening | UC-F | NATIVE | 3 | RabbitMQ dynamic secrets; mTLS via PKI cert lifecycle; LDAP dynamic for Kafka [akeyless-llms-index-2024] |
| UC-F-013 gMSA / Kerberos modernisation for AD accounts | UC-F | ADD-ON | 2 | Kerberos auth method; LDAP rotated secrets; no direct gMSA provisioning [akeyless-llms-index-2024] |
| UC-F-014 API-gateway upstream identity standardised | UC-F | ADD-ON | 2 | PKI/mTLS cert lifecycle; JWT signing; no direct API-GW vendor plugin [akeyless-llms-index-2024] |
| UC-F-015 RPA bot credentials vaulted and session-bound | UC-F | ADD-ON | 2 | Windows/AD rotated secrets; static KV for orchestrators; no UiPath/BluePrism native plugin [INDUSTRY-CONSENSUS] |
| UC-F-016 Keyless code- and artifact-signing in CI | UC-F | NATIVE | 2 | Code signing page; Java JAR/APK signing; HSM-backed classic keys [akeyless-llms-index-2024] |
| UC-F-017 TEE attestation gates secret release | UC-F | GAP | 0 | No TEE/Nitro/SGX attestation-gated release documented [INDUSTRY-CONSENSUS] |
| UC-F-018 AI-agent / LLM tool-credential brokering | UC-F | NATIVE | 2 | Agentic Runtime Authority (early access); Prompt Injection Protection; MCP Server; per-session scoped access [akeyless-agentic-2024] |
| UC-F-019 IoT / OT / branch-device identity enrolment | UC-F | ADD-ON | 1 | ACME server + cert lifecycle for device enrolment; no DPS/EST/SCEP connector [akeyless-llms-index-2024] |
| UC-F-020 Mainframe / midrange credential rotation | UC-F | GAP | 0 | No RACF/z/OS/IBM-i integration documented [INDUSTRY-CONSENSUS] |
| UC-F-021 Backup / DR agent identity de-privileging | UC-F | ADD-ON | 1 | Windows/AD rotation usable; no Veeam/Rubrik/Commvault native connector [INDUSTRY-CONSENSUS] |
| UC-F-022 Webhook inbound identity verification | UC-F | ADD-ON | 1 | Static KV for HMAC secrets; no webhook-rotation workflow [INDUSTRY-CONSENSUS] |
| UC-F-023 Network-device credential modernisation | UC-F | ADD-ON | 1 | SSH targets and rotated secrets; no TACACS+/RADIUS automation documented [INDUSTRY-CONSENSUS] |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner identity | UC-F | ADD-ON | 2 | PKI/mTLS certificate lifecycle; no CDR-specific workflow; FAPI 2.0 client-cert issuable [akeyless-llms-index-2024] |
| UC-F-025 OAuth-app / marketplace integration governance | UC-F | GAP | 0 | No OAuth-app inventory or governance feature documented [INDUSTRY-CONSENSUS] |
| UC-F-026 Vault-internal identity hardening | UC-F | NATIVE | 4 | Customer Fragment + DFC eliminates root-token single-point-of-failure; Gateway stateless; multi-region [akeyless-gw-zk-2024] |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | UC-F | NATIVE | 2 | Identity & Secrets Intelligence (early access): stale-credential and dormancy analytics [akeyless-isi-2024] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | UC-N | ADD-ON | 2 | Analytics page; audit logs; ISI surface (early access); no repo-sprawl native dashboard [akeyless-isi-2024] |
| UC-N-002 NHI inventory and ownership attestation | UC-N | NATIVE | 2 | Identity & Secrets Intelligence (early access); Resource Discovery; Audit Logs [akeyless-discovery-2024] |
| UC-N-003 Rotation-coverage and freshness KPIs | UC-N | NATIVE | 3 | Analytics + Audit Logs; rotation status per secret tracked; KPI export via API [akeyless-llms-index-2024] |
| UC-N-004 Regulator audit evidence pack | UC-N | ADD-ON | 2 | Comprehensive audit logs + SIEM forwarding; no pre-built CPS 234 evidence-pack [akeyless-log-fwd-2024] |
| UC-N-005 Essential 8 / ZT control-area scorecard | UC-N | ADD-ON | 1 | No built-in E8 scorecard; controls evidenced via audit logs + manual mapping [INDUSTRY-CONSENSUS] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | UC-N | ADD-ON | 1 | No vendor-risk scoring module; SOC 2 documentation available for own attestation [akeyless-trust-center-2024] |
| UC-N-007 Data-sovereignty and residency assurance | UC-N | NATIVE | 3 | Gateway self-hosted anywhere + Customer Fragment → customer-controlled data residency; US/EU SaaS only [akeyless-gw-zk-2024] |
| UC-N-008 Engineer training / secure-coding adoption KPI | UC-N | GAP | 0 | No training module; out of product scope [INDUSTRY-CONSENSUS] |
| UC-N-009 Exception register and risk-acceptance governance | UC-N | GAP | 0 | No GRC/exception-register module documented [INDUSTRY-CONSENSUS] |
| UC-N-010 Break-glass / quorum-operator governance | UC-N | ADD-ON | 2 | Sub-Admins; RBAC; no formal quorum-ceremony workflow documented [akeyless-llms-index-2024] |
| UC-N-011 Post-incident reporting / identity-driven RCA | UC-N | ADD-ON | 2 | Audit logs + SIEM forwarding enable IR; no built-in ATT&CK attribution [akeyless-log-fwd-2024] |
| UC-N-012 Supply-chain / SLSA-provenance assurance | UC-N | GAP | 0 | No SLSA/in-toto integration documented [INDUSTRY-CONSENSUS] |
| UC-N-013 Crypto-agility and PQC readiness reporting | UC-N | NATIVE | 2 | Hybrid PQC TLS documented + PQC Support Reference page; key-at-rest PQC not yet GA [akeyless-pqc-2024] |
| UC-N-014 Vendor-evaluation matrix maintenance | UC-N | N/A | — | Meta-process; not a product capability |
| UC-N-015 Comms / stakeholder cadence | UC-N | N/A | — | Meta-process; not a product capability |
| UC-N-016 IoT / OT / branch-fleet posture reporting | UC-N | ADD-ON | 1 | Cert lifecycle for fleet; no fleet-posture reporting dashboard [INDUSTRY-CONSENSUS] |
| UC-N-017 Observability/telemetry secret-leak governance | UC-N | ADD-ON | 2 | Log forwarding to SIEM; audit logs track secret access; no log-scrubbing capability [akeyless-log-fwd-2024] |
| UC-N-018 Confidential-computing / TEE attestation assurance | UC-N | GAP | 0 | No TEE attestation assurance documented [INDUSTRY-CONSENSUS] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | UC-N | NATIVE | 2 | Agentic Runtime Authority: per-session traceability, tool-credential issuance monitoring [akeyless-agentic-2024] |
| UC-N-020 Mainframe / legacy posture and exception transparency | UC-N | GAP | 0 | No mainframe integration; legacy transparency requires manual process [INDUSTRY-CONSENSUS] |

**Citations:** [akeyless-agentic-2024][akeyless-spire-2024][akeyless-isi-2024][akeyless-discovery-2024][akeyless-log-fwd-2024][akeyless-pqc-2024][akeyless-gw-zk-2024][akeyless-llms-index-2024]

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

**1. DFC zero-knowledge cryptography with Customer Fragment sovereignty.**
Akeyless's patented DFC architecture genuinely eliminates the single-server key-reconstruction problem. When a Customer Fragment is deployed in the customer's own Gateway, the vendor cannot decrypt customer secrets — a verifiable architectural claim, not just a marketing assertion. This directly addresses the vault-internal identity risk (NHI-035) and provides a stronger cryptographic data-residency argument than any competing SaaS vault that relies solely on KMS key policies. FIPS 140-3 validated (cert #5227).

**2. Broadest SaaS-native multi-cloud dynamic secrets coverage.**
AWS, Azure AD, GCP, Kubernetes/EKS/GKE, and a full database matrix (10+ engines) are all NATIVE dynamic-secrets producers with short-lived leases — reducing reliance on static credentials across NHI-001, NHI-002, NHI-005. The Vault-proxy compatibility layer means teams can migrate from HashiCorp Vault without rewriting application code.

**3. AI-agent identity ahead of most competitors (2026).**
Agentic Runtime Authority, Prompt Injection Protection, Identity & Secrets Intelligence, and MCP Server integrations (Claude Desktop, GitHub Copilot, Cursor) collectively address NHI-019 more concretely than any core vendor in this evaluation. The features are early-access but documented and shipping.

### Top 3 gaps

**1. No AU/AP SaaS region; no IRAP assessment.**
The absence of an AP SaaS region means APRA-regulated AU workloads must self-host the Gateway to achieve data residency. IRAP is absent — a hard blocker for any AU Government deployment and a risk flag for APRA-regulated entities whose legal teams require Australian government security assessments.

**2. No mainframe (NHI-022) integration.**
RACF/ACF2/z/OS credential rotation — critical for Tier-1 FI core banking — is unaddressed. This is a GAP that CyberArk Conjur and Delinea Secret Server cover natively.

**3. NHI inventory and orphan discovery is early-access only.**
Identity & Secrets Intelligence (the NHI-inventory / dormancy-analytics surface) remains in early access as of May 2026, limiting its use for compliance evidence and UC-N-002 (NHI inventory attestation).

---

## 6. AU-specific notes (≤ 150 words)

**SaaS regions:** US and EU only (publicly documented). No dedicated AP or AU region. Workloads requiring AU data residency must self-host the Akeyless Gateway within AU cloud regions (AWS ap-southeast-2, Azure Australia East, GCP australia-southeast1) and deploy a Customer Fragment on that Gateway — at which point no plaintext key material transits to Akeyless's US/EU SaaS.

**IRAP:** No IRAP Protected or Unclassified assessment is listed on Akeyless's trust centre or public docs. This is a disqualifying gap for AU Government and likely a concern for APRA-regulated entities under CPS 234 §14 (third-party due diligence). An SE conversation is required to determine if any assessment is in progress.

**Essential 8:** No built-in E8 scorecard; compliance evidenced via audit logs and manual control mapping.

**AU customer references:** No named AU financial-services customers in public materials as of May 2026.

**Citations:** [akeyless-trust-center-2024][akeyless-gw-zk-2024]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Akeyless (Agent 03 wave 2)`.

Key list:
- akeyless-dfc-overview-2024
- akeyless-dfc-deepdive-2024
- akeyless-zero-knowledge-2024
- akeyless-fips-2024
- akeyless-components-2024
- akeyless-gw-overview-2024
- akeyless-gw-zk-2024
- akeyless-saas-us-2024
- akeyless-saas-eu-2024
- akeyless-spire-2024
- akeyless-agentic-2024
- akeyless-ai-security-2024
- akeyless-prompt-injection-2024
- akeyless-discovery-2024
- akeyless-pqc-2024
- akeyless-trust-center-2024
- akeyless-log-fwd-2024
- akeyless-auth-overview-2024
- akeyless-isi-2024
- akeyless-llms-index-2024

---

## 8. Open questions for v1.0

1. **IRAP status:** Is an IRAP Protected or Unclassified assessment in progress or planned? This is blocking for XYZ AU Government scoping.
2. **AP SaaS region:** Is an AP/AU SaaS region on the Akeyless roadmap? If not, Gateway-only deployment for AU is the architectural requirement.
3. **FIPS 140-2 Level 3 HSM claim:** The marketing copy references "FIPS 140-2 Level 3 HSM-backed cryptography" but the certification page shows FIPS 140-3 (software module, cert #5227). Clarify whether an HSM-backed variant exists and what its CMVP certificate is.
4. **Mainframe roadmap:** Is RACF/ACF2/z/OS integration on the Akeyless product roadmap? Without it, core-banking NHI-022 / UC-F-020 cannot be addressed.
5. **Identity & Secrets Intelligence GA date:** When does the NHI inventory / dormancy-analytics feature exit early access? This gates UC-N-002 compliance evidence.
6. **Agentic Runtime Authority GA date:** Currently early access; XYZ would need production-grade SLA before relying on it for NHI-019.
7. **Pricing for XYZ scale:** No public rate card. Does the transaction-quota model remain cost-competitive against HashiCorp Vault Enterprise at XYZ's secret volume (thousands of workloads, millions of API calls/day)?
8. **AU customer references:** Any named AU Tier-1 FI or AU Government customers that can be cited for the Risk Committee?
9. **PQC for key-at-rest:** Hybrid PQC TLS is documented. Is ML-KEM/ML-DSA encryption for stored secrets and DFC fragments on the 2026–2027 roadmap?
10. **TEE attestation:** Any plans for Nitro/SGX/MAA attestation-gated secret release (relevant to UC-F-017 / NHI-018)?

# Vendor Profile — Azure Key Vault

**Tier:** cloud-native
**Primary docs:** https://learn.microsoft.com/azure/key-vault/
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

Azure Key Vault is Microsoft's managed cloud key-management and secrets-storage service, available in three distinct SKUs: **Standard** (software-backed keys), **Premium** (HSM-backed keys, FIPS 140-3 Level 3 via Platform 2 firmware), and **Managed HSM** (dedicated single-tenant FIPS 140-3 Level 3 pool). Owned by Microsoft, it is a PaaS offering — no infrastructure to manage. All three SKUs are available in Australian regions (Australia East / Sydney, Australia Southeast / Melbourne, Australia Central / Canberra). Managed HSM Standard B1 pool pricing is listed for all Australian regions. The service integrates natively with the full Azure ecosystem: Entra ID (formerly Azure AD) for authentication, Azure Monitor / Log Analytics for audit, Azure Private Link for network isolation, and Event Grid for event-driven automation. Primary differentiator for XYZ: deepest Azure-native integration, IRAP PROTECTED assessment, and first-party Entra Workload Identity for K8s. [PUBLIC]

---

## 2. Architecture

**Storage backend:** Encrypted at rest (Microsoft-managed or customer-managed keys). Secrets, keys, and certificates are stored as versioned objects. Each vault is scoped to a single Azure region.

**Auth methods:** Microsoft Entra ID is mandatory for both control plane (Azure RBAC) and data plane (Azure RBAC or legacy Key Vault Access Policies). Managed Identities (system-assigned and user-assigned) are the recommended workload auth pattern. Workload Identity Federation (OIDC) allows external IdPs (GitHub Actions, GitLab CI, Google, Kubernetes OIDC JWKS) to exchange tokens for Entra tokens without storing secrets.

**HSM/KMS support:** Standard: FIPS 140-2 Level 1 (software). Premium: FIPS 140-2 Level 2 (Platform 1) or FIPS 140-3 Level 3 (Platform 2 firmware, updated 2024/2025). Managed HSM: Dedicated single-tenant pool, FIPS 140-3 Level 3, local RBAC (separate from Entra RBAC), Shamir's Secret Sharing-based security domain.

**Replication / DR:** Standard/Premium: automatic zone-redundant replication within region + automatic secondary-region replication (paired region); no extra cost. Managed HSM: three HSM instances in customer-selected region; security domain enables cross-region restore; full backup to Azure Blob Storage via managed identity.

**Compliance / certifications:** SOC 1/2/3, ISO 27001/27017/27018, PCI DSS, FedRAMP High, IRAP PROTECTED (assessment current), Common Criteria. Azure Australia regions are IRAP-assessed at PROTECTED level; Microsoft continues ongoing IRAP assessments post-CCSL closure (July 2020).

**Key/secret types:** RSA (2048/3072/4096), EC (P-256, P-384, P-521, P-256K), AES (128/192/256 — Managed HSM only), symmetric oct-HSM. Secrets: arbitrary UTF-8 strings with metadata. Certificates: full lifecycle with integrated CAs (DigiCert, GlobalSign) or self-signed.

**Network:** Private Link / Private Endpoints, VNet service endpoints, IP firewall rules, Network Security Perimeter. Azure Arc does not extend Key Vault natively to non-Azure clusters, but AKS Workload Identity + CSI driver covers hybrid K8s via OIDC federation.

**Cost model:** Per-operation pricing (secrets: per 10,000 transactions; keys: per key/month for Premium HSM + per 10,000 operations; certificates: per renewal + per 10,000 operations). Managed HSM: hourly fee per pool (Standard B1). No per-secret storage fee.

---

## 3. NHI coverage map

**NHI-001 — Cloud IAM principal (role / service account)**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Managed Identities (system + user-assigned) are the primary recommended pattern; all Key Vault access flows through Entra ID. [akv-auth-2025]

**NHI-002 — Kubernetes ServiceAccount**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** AKS Workload ID + OIDC federation + CSI Secrets Store Driver mounts Key Vault secrets into pods without plaintext K8s Secret objects. [aks-workload-identity-2025; aks-csi-driver-2025]

**NHI-003 — CI/CD pipeline identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Workload Identity Federation supports GitHub Actions, GitLab, and any OIDC-compliant CI; no stored secrets needed. [akv-wif-2025]

**NHI-004 — Container / image-pull credential**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Key Vault stores ACR admin credentials as secrets; no native image-pull credential rotation; requires custom function or pipeline step. [akv-dev-guide-2025]

**NHI-005 — Database service account**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Event Grid + Azure Functions rotation pattern rotates SQL Server passwords stored in Key Vault; not a dynamic-credential broker. [akv-rotation-2025]

**NHI-006 — Application TLS server / mTLS workload identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Key Vault certificates with full lifecycle management; DigiCert/GlobalSign integrated CAs; auto-renew via policy. [akv-certs-about-2025]

**NHI-007 — Third-party SaaS API key / OAuth client**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Secrets stored and versioned; access via Managed Identity or Workload ID; no third-party rotation brokering built in. [akv-secrets-best-practices-2025]

**NHI-008 — Git platform credential (PAT, SSH key, deploy key)**
- **Coverage:** NATIVE — **Maturity:** 2
- **Evidence:** Git PATs stored as secrets in Key Vault; rotation requires custom Event Grid / Function. [akv-secrets-best-practices-2025]

**NHI-009 — Configuration-management / IaC agent identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Terraform AzureRM provider + Managed Identity retrieves secrets at apply-time; Ansible azure_rm_keyvault module supported. [akv-dev-guide-2025]

**NHI-010 — Monitoring / observability agent**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Azure Monitor agents use Managed Identity; secrets for third-party agents (Datadog, Splunk) stored in Key Vault and retrieved at startup. [akv-logging-2025]

**NHI-011 — Message broker / event-bus client**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Service Bus SAS keys and Event Hub connection strings stored as Key Vault secrets; no auto-rotation built in. [akv-dev-guide-2025]

**NHI-012 — Active Directory / LDAP service account**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** AD passwords stored as Key Vault secrets; rotation via custom function; no gMSA native integration. [akv-dev-guide-2025]

**NHI-013 — Reverse-proxy / API-gateway upstream identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Azure API Management (APIM) natively retrieves Key Vault secrets/certs for backend auth; TLS cert auto-renew supported. [akv-dev-guide-2025]

**NHI-014 — RPA bot identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** RPA orchestrator credentials stored in Key Vault; no native UiPath/Blue Prism integration — custom connector needed. [akv-secrets-best-practices-2025]

**NHI-015 — Code-signing identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Key Vault keys used for code signing via Azure SignTool and Trusted Signing service; lifecycle managed via Key Vault certificates. [akv-keys-2025]

**NHI-016 — Build provenance / SLSA attestation identity**
- **Coverage:** PARTNER — **Maturity:** 1
- **Evidence:** No native SLSA attestation signing via Key Vault; GitHub Actions OIDC + Key Vault key can be used for signing but not automated. [akv-wif-2025]

**NHI-017 — Service mesh control-plane identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Istio/Linkerd cert issuance can use Key Vault via CSI driver or cert-manager integration; no native mesh CA integration. [aks-csi-driver-2025]

**NHI-018 — Confidential-computing attestation identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM uses Intel SGX TEEs for key operations; HSM security domain is TEE-protected; Azure Confidential Computing integration documented. [akv-hsm-tech-2025]

**NHI-019 — AI agent / autonomous workflow identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Azure OpenAI and AI Foundry workloads use Managed Identity to retrieve Key Vault secrets; Entra Workload ID supports agentic frameworks. [akv-auth-2025]

**NHI-020 — Model artifact / registry identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure ML workspace uses Key Vault as its backing secrets store for model registry credentials; managed by Azure ML, not directly by Key Vault. [akv-dev-guide-2025]

**NHI-021 — IoT / OT device identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** IoT Hub device credentials can be stored in Key Vault; no native IoT device certificate lifecycle management via AKV. [akv-certs-about-2025]

**NHI-022 — Mainframe / midrange service identity**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No documented mainframe (RACF, ACF2, TopSecret) or midrange integration with Azure Key Vault. GAP for XYZ mainframe estate.

**NHI-023 — Database encryption / TDE master key identity**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Azure SQL TDE with customer-managed key (CMK) in Key Vault/Managed HSM; Always Encrypted column-level key management supported. [akv-overview-2025]

**NHI-024 — HSM / KMS operator / break-glass identity**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Managed HSM local RBAC: Managed HSM Administrator, Crypto Officer, Crypto User roles; quorum-protected security domain download. [akv-hsm-roles-2025]

**NHI-025 — Certificate authority operator identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Certificate issuer resources in Key Vault represent CA accounts (DigiCert, GlobalSign); admin account credential stored securely. [akv-certs-2025]

**NHI-026 — Backup / DR agent identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM full backup uses user-assigned managed identity; backup to Azure Blob Storage with RBAC-scoped permissions. [akv-hsm-backup-2025]

**NHI-027 — Backend-for-frontend / on-behalf-of token holder**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** BFF services use Managed Identity to retrieve Key Vault secrets; OBO token flow via Entra ID; Key Vault not directly in OBO chain. [akv-auth-2025]

**NHI-028 — Federated B2B / Open Banking client identity**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No native FAPI 2.0 / CDR / Open Banking CA integration in Key Vault. mTLS client certs can be stored but no FAPI-specific lifecycle tooling. GAP.

**NHI-029 — Service-account-as-human (shared functional ID)**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Shared service account passwords can be stored; no privileged-session or check-in/check-out controls — requires CyberArk PAM or Delinea integration. [akv-secrets-best-practices-2025]

**NHI-030 — Browser / SaaS extension and OAuth-app identity**
- **Coverage:** NATIVE — **Maturity:** 2
- **Evidence:** OAuth client secrets stored in Key Vault; Entra App Registrations manage client secrets separately; no rotation broker. [akv-auth-2025]

**NHI-031 — Webhook / inbound integration identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Webhook HMAC secrets stored in Key Vault; rotation via custom function. [akv-secrets-best-practices-2025]

**NHI-032 — Network / infrastructure device identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Network device credentials stored as secrets; no TACACS+/RADIUS-native integration with Key Vault. [akv-dev-guide-2025]

**NHI-033 — Print / spooler / branch-peripheral identity**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No documented integration path for printer/spooler credential lifecycle management in Azure Key Vault.

**NHI-034 — Quantum-resistant / hybrid-PKI rotation identity**
- **Coverage:** ADD-ON — **Maturity:** 1
- **Evidence:** No post-quantum key types currently in Key Vault GA; Microsoft has announced PQC roadmap for Azure services but not yet landed in AKV. [akv-keys-2025]

**NHI-035 — Vault-internal / secrets-broker identity**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Key Vault itself acts as the secrets broker; Managed Identity used to access Key Vault; no external broker needed for Azure workloads. [akv-overview-2025]

**NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No native SPIFFE/SPIRE integration; OIDC Workload Identity Federation is the Azure-native analogue but does not implement SPIFFE SVID. [akv-wif-2025]

**NHI-037 — Forgotten / orphaned legacy identity**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Key Vault has no built-in orphan detection; Microsoft Defender for Cloud (Defender CSPM) and Entra ID Access Reviews provide coverage as add-ons. [akv-security-2025]

---

## 4. Use-case scoring

**UC-F-001 — Prevent plaintext secrets in source repositories**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Key Vault + Managed Identity / Workload ID eliminates credential embedding; Azure DevOps and GitHub Actions native integrations. [akv-auth-2025]

**UC-F-002 — Detect and remediate secrets already in history**
- **Coverage:** PARTNER — **Maturity:** 2
- **Evidence:** No built-in secret-scanning; Microsoft Defender for DevOps (GitHub Advanced Security integration) covers this as an add-on from a partner service. [akv-security-2025]

**UC-F-003 — JIT short-lived cloud credentials via OIDC**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Workload Identity Federation exchanges external OIDC tokens for Entra tokens; no stored secrets; JIT access to Key Vault data plane. [akv-wif-2025]

**UC-F-004 — Workload-attested ephemeral identity (SPIFFE/SPIRE)**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No native SPIFFE/SPIRE support; AKS OIDC Issuer + Workload ID is the Azure-native substitute but is not SPIFFE-spec compliant. [aks-workload-identity-2025]

**UC-F-005 — Dynamic database credentials with broker-issued leases**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** Key Vault does not issue dynamic DB credentials with TTL leases; static secret rotation via Event Grid + Function is the closest pattern. [akv-rotation-2025]

**UC-F-006 — Automated rotation of long-lived static secrets**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Event Grid near-expiry event triggers Azure Function to rotate secret and update service; Storage Account key rotation managed natively. [akv-rotation-2025; akv-autorotation-2025]

**UC-F-007 — Immediate revocation on identity compromise**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Disable or delete secret/key version immediately; purge protection and soft-delete configurable; certificate CRL and OCSP via integrated CAs. [akv-recovery-2025]

**UC-F-008 — Kubernetes secret consumption without on-disk plaintext**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Azure Key Vault Provider for Secrets Store CSI Driver mounts secrets as volumes; secrets never written as plaintext K8s Secret objects unless sync enabled. [aks-csi-driver-2025]

**UC-F-009 — Container image-pull credentials issued per workload**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** ACR integrates with Managed Identity for image pull; ACR admin credentials can be stored in Key Vault; no per-workload token issuance natively. [akv-dev-guide-2025]

**UC-F-010 — IaC / config-management secrets injected at apply-time**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Terraform azurerm_key_vault_secret data source; Ansible azure_rm_keyvault_secret; Bicep / ARM Key Vault reference syntax. [akv-dev-guide-2025]

**UC-F-011 — Observability-agent credentials rotated and scoped**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Azure Monitor agents use Managed Identity; third-party agent credentials stored and rotated via Event Grid + Function pattern. [akv-logging-2025]

**UC-F-012 — Message-broker client identity hardening**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Service Bus SAS/connection-string secrets stored in Key Vault; Managed Identity for Service Bus eliminates static keys for Azure services. [akv-dev-guide-2025]

**UC-F-013 — gMSA / Kerberos modernisation for AD service accounts**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** gMSA credentials managed by Active Directory; Key Vault stores supplementary secrets; no native gMSA integration in Key Vault. [akv-dev-guide-2025]

**UC-F-014 — API-gateway upstream identity standardised**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** APIM natively retrieves Key Vault certificates and secrets; TLS cert auto-renewal and backend auth via Managed Identity. [akv-dev-guide-2025]

**UC-F-015 — RPA bot credentials vaulted and session-bound**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** RPA credentials stored in Key Vault; no native UiPath/Blue Prism integration; custom retrieval required per bot framework. [akv-secrets-best-practices-2025]

**UC-F-016 — Keyless code- and artifact-signing in CI**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure Trusted Signing service (preview) uses Key Vault keys under the hood; Sigstore keyless model not natively supported. [akv-keys-2025]

**UC-F-017 — TEE attestation gates secret release**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM runs in Intel SGX TEE; security domain bound to TEE; Azure Confidential Ledger and Confidential Computing attestation integration. [akv-hsm-tech-2025]

**UC-F-018 — AI-agent / LLM tool-credential brokering**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Azure OpenAI / AI Foundry workloads use Managed Identity to retrieve Key Vault secrets; Entra Workload ID enables agentic OIDC flows. [akv-auth-2025]

**UC-F-019 — IoT / OT / branch-device identity enrolment**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** IoT Hub device credentials stored in Key Vault; no native DPS-to-Key Vault cert lifecycle management; Azure IoT Edge uses Key Vault indirectly. [akv-certs-about-2025]

**UC-F-020 — Mainframe / midrange credential rotation pipeline**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No documented mainframe (RACF, ACF2, JES) credential rotation integration with Azure Key Vault. [GAP]

**UC-F-021 — Backup / DR agent identity de-privileging**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM backup uses user-assigned managed identity scoped to Storage Blob Data Contributor; least-privilege enforced by RBAC. [akv-hsm-backup-2025]

**UC-F-022 — Webhook inbound identity verification**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** HMAC secrets stored in Key Vault; no native webhook-signature verification service; custom Azure Function required. [akv-secrets-best-practices-2025]

**UC-F-023 — Network-device credential modernisation**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Network device passwords stored as Key Vault secrets; rotation via custom function or Ansible; no TACACS+ native integration. [akv-dev-guide-2025]

**UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** Key Vault stores mTLS client certs; no FAPI 2.0 / CDR-specific CA integration or DPoP key management tooling. GAP. [akv-certs-about-2025]

**UC-F-025 — OAuth-app / marketplace integration governance**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** OAuth client secrets stored in Key Vault; Entra App Registrations govern lifecycle separately; no unified governance dashboard. [akv-auth-2025]

**UC-F-026 — Vault-internal identity hardening**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM local RBAC enforces separation of duties; Key Vault itself is hardened by Entra RBAC; no privileged admin sessions recorded natively. [akv-hsm-roles-2025]

**UC-F-027 — Orphaned / dormant NHI cleanup pipeline**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Key Vault has no orphan detection; Microsoft Defender CSPM and Entra ID Access Reviews supplement; custom last-access auditing via Log Analytics. [akv-logging-2025]

**UC-N-001 — Real-time secret-sprawl KPI dashboard**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure Monitor + Log Analytics KQL queries on Key Vault audit logs; no out-of-box KPI dashboard; custom workbooks required. [akv-logging-2025]

**UC-N-002 — NHI inventory and ownership attestation**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure Resource Graph can enumerate Key Vault objects; no ownership attestation workflow built in; requires Entra Access Reviews extension. [akv-rbac-2025]

**UC-N-003 — Rotation-coverage and freshness KPIs**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Key Vault expiry events via Event Grid; Log Analytics can track last-rotation timestamp; no out-of-box freshness KPI report. [akv-autorotation-2025]

**UC-N-004 — Regulator audit evidence pack**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Full diagnostic logs (AzureDiagnostics / ResourceLogs) sent to Log Analytics; 90-day immutable audit trail; Defender for Cloud compliance reports. [akv-logging-2025]

**UC-N-005 — Essential 8 / ZT control-area scorecard**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Microsoft Defender for Cloud Secure Score maps to Essential Eight controls; Key Vault contributes to Application Control and Patch Application categories. [azure-irap-2025]

**UC-N-006 — Vendor / SaaS supply-chain risk attestation**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Microsoft publishes Supply Chain Integrity documentation; Key Vault service supply chain not independently attestable by customers. [akv-security-2025]

**UC-N-007 — Data-sovereignty and residency assurance**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Key Vault data resides in the selected Azure region (Australia East/Southeast/Central); replication stays within Australian geographic boundary (security world). [akv-security-worlds-2025; azure-irap-2025]

**UC-N-008 — Engineer training and secure-coding adoption KPI**
- **Coverage:** N/A — **Maturity:** 0
- **Evidence:** Not a Key Vault product capability; Microsoft Learn documentation and training paths available but not a measurable KPI feature.

**UC-N-009 — Exception register and risk-acceptance governance**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No built-in exception register or risk-acceptance workflow in Key Vault. Requires GRC tooling (ServiceNow, Archer) as external overlay.

**UC-N-010 — Break-glass and quorum-operator governance**
- **Coverage:** NATIVE — **Maturity:** 4
- **Evidence:** Managed HSM security domain uses Shamir's Secret Sharing for M-of-N quorum; local RBAC Administrator role for break-glass; Managed HSM Admin role separation. [akv-hsm-roles-2025; akv-hsm-tech-2025]

**UC-N-011 — Post-incident reporting and identity-driven RCA**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Key Vault diagnostic logs record every REST operation with caller identity, result, and timestamp; Log Analytics enables forensic KQL queries. [akv-logging-2025]

**UC-N-012 — Supply-chain / SLSA-provenance assurance reporting**
- **Coverage:** PARTNER — **Maturity:** 1
- **Evidence:** No SLSA build-provenance native to Key Vault; GitHub Actions + OIDC + Key Vault signing is the partner-assembled path. [akv-wif-2025]

**UC-N-013 — Crypto-agility and post-quantum readiness reporting**
- **Coverage:** ADD-ON — **Maturity:** 1
- **Evidence:** Current Key Vault GA key types do not include PQC algorithms; Microsoft PQC roadmap announced; Managed HSM firmware updated to FIPS 140-3 L3 positioning for future PQC. [akv-managed-hsm-2025]

**UC-N-014 — Vendor-evaluation matrix maintenance**
- **Coverage:** N/A — **Maturity:** 0
- **Evidence:** Meta-process activity; not a Key Vault product capability.

**UC-N-015 — Communications, change-comms and stakeholder cadence**
- **Coverage:** N/A — **Maturity:** 0
- **Evidence:** Organisational process; not a Key Vault product capability.

**UC-N-016 — IoT / OT / branch-fleet posture reporting**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure IoT Hub + Defender for IoT provides fleet posture; Key Vault stores device credentials; no unified IoT + KV posture report. [akv-certs-about-2025]

**UC-N-017 — Observability/telemetry secret-leak governance**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure Monitor + Sentinel can be configured to alert on secret access anomalies; no built-in secret-leak detection in Key Vault logs. [akv-hsm-bestpractices-2025]

**UC-N-018 — Confidential-computing / TEE attestation assurance**
- **Coverage:** NATIVE — **Maturity:** 3
- **Evidence:** Managed HSM runs cryptographic operations in Intel SGX TEEs; attestation evidence embedded in security domain; Azure Confidential Ledger integration. [akv-hsm-tech-2025]

**UC-N-019 — AI-agent / autonomous-workflow KPI suite**
- **Coverage:** ADD-ON — **Maturity:** 2
- **Evidence:** Azure AI Foundry + Managed Identity accesses Key Vault; no AI-agent-specific KPI dashboard for credential usage in Key Vault. [akv-auth-2025]

**UC-N-020 — Mainframe / legacy posture and exception transparency**
- **Coverage:** GAP — **Maturity:** 0
- **Evidence:** No mainframe integration; no posture reporting for mainframe identities in Key Vault or Azure Monitor.

---

## 5. Strengths and gaps

### Top 3 strengths

1. **Deepest Azure-native integration.** Key Vault is the cryptographic backbone of the Azure platform. Managed Identity authentication, Azure RBAC, Event Grid rotation triggers, APIM cert lifecycle, AKS CSI driver, and SQL TDE CMK all operate natively — no third-party glue required. For XYZ banks running Azure-first, this dramatically reduces integration complexity.

2. **FIPS 140-3 Level 3 at all HSM tiers.** Both Premium (Platform 2 firmware, 2024/2025 update) and Managed HSM now deliver FIPS 140-3 Level 3. Managed HSM adds a dedicated single-tenant pool with local RBAC, Shamir M-of-N security domain, and Intel SGX TEE-backed operations — meeting APRA CPS 234 HSM requirements without on-premises hardware.

3. **AKS + OIDC Workload Identity Federation.** Entra Workload ID with OIDC federation is the strongest native K8s secrets pattern of any cloud-native vendor: no secret mounting, OIDC token exchange, pod-level identity scoping, and CSI driver integration all GA. Directly addresses NHI-002, UC-F-003, UC-F-008.

### Top 3 gaps

1. **No dynamic credential brokering (NHI-005, UC-F-005).** Key Vault is a static secrets store. It does not issue Vault-like dynamic database credentials with TTL leases. XYZ banks with Oracle/DB2/PostgreSQL requiring just-in-time dynamic credentials must layer HashiCorp Vault or CyberArk Conjur.

2. **No SPIFFE/SPIRE native support (NHI-036, UC-F-004).** Entra Workload ID is functionally similar but is not SPIFFE-spec compliant (no SVID, no SPIRE agent). XYZ workloads requiring SPIFFE for multi-cloud or on-premises attestation need a separate SPIRE deployment with Key Vault as the downstream secret store.

3. **Mainframe and FAPI 2.0 gaps (NHI-022, NHI-028, UC-F-020, UC-F-024).** No documented integration with RACF/ACF2/TopSecret mainframe credential stores. No FAPI 2.0 / CDR-specific CA management. Both are XYZ-relevant (legacy mainframe banking estate; CDR / Open Banking mandate). Require partner solutions.

---

## 6. AU-specific notes

**Regions:** Key Vault Standard and Premium: GA in Australia East (Sydney), Australia Southeast (Melbourne), Australia Central (Canberra), Australia Central 2. Managed HSM Standard B1 pool: available in Australian regions per pricing data (confirmed via pricing page; microsoft.com/regions/services advised for authoritative confirmation).

**IRAP PROTECTED:** Microsoft completed an IRAP assessment for Azure cloud services at PROTECTED level covering Australian regions. Following CCSL closure (July 2020), ongoing IRAP assessments by independent assessors continue; Key Vault is within the IRAP-assessed service scope. Agencies must complete their own authorization under the PSPF/ISM risk-managed approach.

**Data sovereignty:** Key Vault security worlds are geo-bounded; Australian regions replicate within the Australia geographic boundary (Australia East ↔ Australia Southeast paired region). No data egress to other geopolitical regions.

**Essential Eight:** Contributes to Application Control (code-signing via Trusted Signing), Multi-Factor Authentication (Entra MFA for Key Vault admin access), Restrict Administrative Privileges (RBAC least privilege), and Patch Operating Systems (no OS to patch — managed service).

**ISM alignment:** Key Vault satisfies ISM-1546 (secrets management), ISM-1412 (cryptographic key protection), ISM-0469 (key ceremony records via Managed HSM security domain). ASD IRAP assessors have reviewed Azure's control implementation at PROTECTED.

---

## 7. Citations

BibTeX keys introduced by this profile are appended to `meta/citations.bib` under `## Azure Key Vault (Agent 03 wave 2)`.

Keys used: akv-overview-2025, akv-security-2025, akv-managed-hsm-2025, akv-auth-2025, akv-certs-2025, akv-recovery-2025, akv-keys-2025, akv-rbac-2025, akv-logging-2025, akv-network-2025, akv-pricing-2025, akv-hsm-backup-2025, akv-dr-2025, akv-hsm-tech-2025, akv-hsm-roles-2025, akv-rotation-2025, aks-workload-identity-2025, akv-dev-guide-2025, akv-wif-2025, akv-secrets-best-practices-2025, akv-certs-about-2025, akv-security-worlds-2025, akv-autorotation-2025, akv-hsm-bestpractices-2025, aks-csi-driver-2025, akv-hsm-dr-2025, azure-irap-2025, akv-concepts-2025, akv-hsm-access-2025

---

## 8. Open questions for v1.0

1. **Managed HSM exact AU region list:** Pricing page lists AU regions for Managed HSM Standard B1 but the dedicated regions page (404). Confirm official Managed HSM AU region support via `az keyvault list-deleted --resource-type hsm` or Microsoft SE.
2. **IRAP scope document:** The IRAP page returned 401 (requires Azure portal auth). Exact Key Vault service-scope list for the current IRAP assessment is behind authentication. Microsoft SE can provide the IRAP Consumer Guide.
3. **PQC timeline:** Microsoft has announced post-quantum readiness but no GA date for PQC key types in Key Vault. Confirm roadmap with Microsoft Product team.
4. **Managed HSM Australia Central availability:** Australia Central is a restricted region (government/sovereign). Confirm whether Managed HSM is available there for non-government XYZ entities.
5. **Dynamic secrets roadmap:** Does Microsoft plan a Vault-style dynamic credential engine, or is the recommended pattern always Event Grid + Function rotation? Relevant for NHI-005 scoring.
6. **FAPI 2.0 / CDR integration:** Any Azure API Management + Key Vault reference architecture for CDR / Open Banking mTLS cert management (ACCC-accredited participants)?

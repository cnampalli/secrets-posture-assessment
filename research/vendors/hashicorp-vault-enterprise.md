# Vendor Profile — HashiCorp Vault Enterprise

**Tier:** core
**Primary docs:** https://developer.hashicorp.com/vault
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

HashiCorp Vault Enterprise is an IBM-owned (post-2023 acquisition) self-managed secrets-management and identity broker, available as on-premises packages, cloud-provider marketplace AMIs, or HCP Vault Dedicated (operator-managed SaaS variant). The primary differentiator is its **API-first, plugin-modular architecture**: every auth method and secrets engine is a separately mountable plugin, producing extraordinary breadth across cloud IAM, PKI, dynamic credentials, and encryption-as-a-service. The Community edition is OSS (MPL 2.0); Enterprise adds namespaces, performance/DR replication, HSM/PKCS11 unseal, Transform (FPE/tokenisation), Sentinel policy, FIPS 140-3 builds, and Secrets Sync. A major AU Tier-1 FI already runs Vault Enterprise at scale `[USER-SUPPLIED]`. Australian presence: HashiCorp lists Sydney as a support location; AWS ap-southeast-2 and Azure australiaeast regions are supported for HCP Vault Dedicated data residency.

**Citations:** [hashicorp-vault-what-is-2024] [hashicorp-hcp-vault-2024]

---

## 2. Architecture

**Storage backends:** Integrated Storage (Raft-based, built-in HA and replication — recommended) or third-party (Consul, PostgreSQL, etc.). Integrated Storage encrypts and replicates data across the cluster natively. [hashicorp-vault-what-is-2024]

**Auth methods:** 17+ GA methods (Community): AppRole, Kubernetes, AWS (IAM + EC2), Azure, GCP, JWT/OIDC, LDAP, TLS Certificates, Token, Kerberos, Okta, RADIUS, GitHub, OCI, AliCloud, Cloud Foundry, Username/Password. Enterprise adds SAML, SCEP, SPIFFE. [hashicorp-vault-auth-2024]

**Secrets engines:** KV v1/v2, PKI (X.509/ACME), Database (13+ DB plugins), SSH (OTP + CA), Transit (encryption-as-a-service), AWS/Azure/GCP dynamic creds, LDAP, RabbitMQ, Consul, TOTP, Kubernetes. Enterprise adds Transform (FPE/tokenisation), Key Management (KMIP), SPIFFE engine, Secrets Sync, Secrets Import. [hashicorp-vault-secrets-2024]

**HSM/KMS auto-unseal:** AWS KMS, Azure Key Vault, GCP Cloud KMS, OCI KMS, Transit (unseal chaining), and HSM via PKCS#11 (Enterprise only). Seal Wrap is enabled by default in Enterprise for an additional encryption layer. FIPS 140-3 inside builds available since v1.19.4 (Leidos attestation). [hashicorp-vault-seal-2024] [hashicorp-vault-pkcs11-2024] [hashicorp-vault-fips-2024]

**Replication:** Performance Replication (horizontal read-scale; secondaries manage own tokens/leases) and DR Replication (shared token/lease infrastructure for catastrophic failure protection). Path filters enable selective namespace/mount replication. [hashicorp-vault-replication-2024]

**Compliance posture:** SOC 2 Type II (self-declared), FIPS 140-3 (v1.19.4+ Leidos attestation). No public IRAP declaration found as of 2026-05-22. FedRAMP not applicable for self-managed; HCP Vault Dedicated FedRAMP High planned [INDUSTRY-CONSENSUS].

**Licensing model:** Enterprise is module-gated. Core Enterprise modules include Governance/Policy (Sentinel, namespaces, MFA) and Advanced Data Protection (ADP-Transform for FPE/tokenisation; ADP-KM for KMIP/Key Management). Non-production environments are separately licensed alongside production — this is a notable commercial consideration for any FI running lab/dev/staging clusters at scale `[USER-SUPPLIED]`. Pricing is negotiated per-node/per-cluster; HashiCorp does not publish list prices publicly. [hashicorp-vault-enterprise-2024]

---

## 3. NHI coverage map

| NHI ID | Name | Coverage | Maturity | Evidence |
|--------|------|----------|----------|---------|
| NHI-001 | Cloud IAM principal (AWS/Azure/GCP) | NATIVE | 4 | AWS IAM, Azure, GCP auth methods + dynamic creds engines [hashicorp-vault-auth-2024] |
| NHI-002 | Kubernetes ServiceAccount | NATIVE | 4 | Kubernetes auth method + Agent Injector + CSI driver [hashicorp-vault-k8s-2024] |
| NHI-003 | CI/CD pipeline identity | NATIVE | 4 | JWT/OIDC auth supports GitHub Actions, GitLab OIDC, Azure DevOps OIDC [hashicorp-vault-jwt-2024] |
| NHI-004 | Container image-pull credential | ADD-ON | 2 | KV secrets + Agent Injector can deliver registry creds; no native ECR/ACR dynamic engine [hashicorp-vault-agent-injector-2024] |
| NHI-005 | Database service account | NATIVE | 4 | Database secrets engine with 13+ plugins (Oracle, MSSQL, PostgreSQL, MySQL, Snowflake, MongoDB, Cassandra, Redis, Elasticsearch, etc.) [hashicorp-vault-db-2024] |
| NHI-006 | Application TLS / mTLS workload identity | NATIVE | 4 | PKI secrets engine (ACME, X.509, SPIFFE SVIDs in ENT) + TLS cert auth [hashicorp-vault-pki-2024] |
| NHI-007 | Third-party SaaS API key / OAuth client | NATIVE | 3 | KV v2 storage + rotation policies; no native SaaS-specific dynamic engines [hashicorp-vault-kv-2024] |
| NHI-008 | Git platform credential (PAT, SSH key) | NATIVE | 3 | KV v2 + SSH secrets engine for SSH key signing; no native GitHub PAT dynamic engine [hashicorp-vault-ssh-2024] |
| NHI-009 | IaC / config-management agent identity | NATIVE | 4 | AppRole + Terraform Vault Provider + HCP Terraform integration [hashicorp-vault-approle-2024] |
| NHI-010 | Monitoring / observability agent | NATIVE | 3 | KV v2 + dynamic secret rotation; no native Datadog/Splunk dynamic engines [hashicorp-vault-kv-2024] |
| NHI-011 | Message broker / event-bus client | NATIVE | 3 | RabbitMQ secrets engine GA; Kafka via KV rotation; Azure SB via Azure secrets engine [hashicorp-vault-secrets-2024] |
| NHI-012 | Active Directory / LDAP service account | NATIVE | 4 | LDAP secrets engine for dynamic AD/LDAP creds + LDAP auth method [hashicorp-vault-secrets-2024] |
| NHI-013 | Reverse-proxy / API-gateway upstream identity | NATIVE | 3 | PKI engine for mTLS cert issuance; JWT/TLS cert auth for gateway-to-upstream [hashicorp-vault-pki-2024] |
| NHI-014 | RPA bot identity | NATIVE | 3 | AppRole or KV v2 vault integration; no native UiPath/Blue Prism plugin [hashicorp-vault-approle-2024] |
| NHI-015 | Code-signing identity (Sigstore / Authenticode) | ADD-ON | 2 | PKI engine issues code-signing certs; Sigstore Fulcio integration via OIDC; no native keyless signing workflow [hashicorp-vault-pki-2024] |
| NHI-016 | Build provenance / SLSA attestation identity | GAP | 1 | No native SLSA/in-toto attestation engine; JWT/OIDC auth can provide identity for Sigstore [INDUSTRY-CONSENSUS] |
| NHI-017 | Service mesh control-plane identity | NATIVE | 3 | Consul Connect CA integration; PKI engine as Vault-backed mesh CA for Istio/Linkerd [hashicorp-vault-pki-2024] |
| NHI-018 | Confidential-computing attestation identity | GAP | 1 | No native TEE attestation (Nitro/SEV-SNP/TDX) gated secret release; community plugins exist [INDUSTRY-CONSENSUS] |
| NHI-019 | AI agent / autonomous workflow identity | NATIVE | 3 | AppRole + JWT/OIDC auth + per-session dynamic creds; no AI-native policy primitives yet [hashicorp-vault-approle-2024] |
| NHI-020 | Model artifact / registry identity | NATIVE | 2 | KV v2 storage for registry tokens; no native ML registry integration [hashicorp-vault-kv-2024] |
| NHI-021 | IoT / OT device identity | ADD-ON | 2 | PKI engine with ACME/EST/SCEP (ENT) for device cert enrolment; no DPS/IoT Hub integration [hashicorp-vault-pki-2024] |
| NHI-022 | Mainframe / midrange service identity | PARTNER | 2 | No native RACF/ACF2 plugin; partner integrations (CyberArk Conjur z/OS bridge) required [INDUSTRY-CONSENSUS] |
| NHI-023 | Database encryption / TDE master key | NATIVE | 3 | Transit secrets engine for bring-your-own-key; Key Management engine (ENT) for KMS wrapping [hashicorp-vault-secrets-2024] |
| NHI-024 | HSM / KMS operator / break-glass identity | NATIVE | 4 | PKCS11 auto-unseal (ENT); seal wrap; root token rekeying with M-of-N Shamir; quorum unseal [hashicorp-vault-pkcs11-2024] |
| NHI-025 | Certificate authority operator identity | NATIVE | 4 | PKI engine with full CA operator roles; ACME; SCEP/EST (ENT); external CA delegation [hashicorp-vault-pki-2024] |
| NHI-026 | Backup / DR agent identity | NATIVE | 3 | KV v2 + LDAP secrets engine for AD backup accounts; DR Replication for vault itself [hashicorp-vault-replication-2024] |
| NHI-027 | Backend-for-frontend / OBO token holder | NATIVE | 3 | JWT/OIDC auth + token exchange pattern; private_key_jwt support via JWT auth [hashicorp-vault-jwt-2024] |
| NHI-028 | Federated B2B / Open Banking client identity | NATIVE | 3 | PKI engine for mTLS client certs; TLS cert auth for FAPI 2.0 client validation [hashicorp-vault-pki-2024] |
| NHI-029 | Service-account-as-human (shared functional ID) | NATIVE | 3 | LDAP secrets engine + AppRole enforce per-machine identity; audit logging distinguishes callers [hashicorp-vault-secrets-2024] |
| NHI-030 | Browser / SaaS extension / OAuth-app identity | GAP | 1 | No native OAuth-app inventory or SaaS marketplace token management [INDUSTRY-CONSENSUS] |
| NHI-031 | Webhook / inbound integration identity | NATIVE | 2 | KV v2 for HMAC signing secret storage and rotation; no native webhook secret broker [hashicorp-vault-kv-2024] |
| NHI-032 | Network / infrastructure device identity | ADD-ON | 2 | SSH engine (CA signing) for network device SSH; TACACS+ secrets via KV + rotation [hashicorp-vault-ssh-2024] |
| NHI-033 | Print / spooler / branch-peripheral identity | ADD-ON | 2 | PKI engine issues 802.1X EAP-TLS certs; no branch-peripheral-specific workflow [hashicorp-vault-pki-2024] |
| NHI-034 | Quantum-resistant / hybrid-PKI rotation identity | GAP | 1 | No PQC / ML-DSA algorithm support in current PKI or Transit engines; on HashiCorp roadmap [INDUSTRY-CONSENSUS] |
| NHI-035 | Vault-internal / secrets-broker identity | NATIVE | 4 | Root token sealed offline; Shamir/M-of-N rekeying; auto-unseal KMS; DR replication tokens scoped [hashicorp-vault-seal-2024] |
| NHI-036 | Ephemeral workload via SPIFFE / Aembit | NATIVE | 3 | SPIFFE auth method (ENT) + PKI SVID issuance (ENT); JWT-SVID via JWT auth (Community) [hashicorp-vault-auth-2024] |
| NHI-037 | Forgotten / orphaned legacy identity | ADD-ON | 2 | Vault audit logs + token TTL enforcement limit orphans; no native dormancy-detection sweep [hashicorp-vault-enterprise-2024] |

**NHI coverage summary:** NATIVE=28, ADD-ON=6, PARTNER=1, GAP=4 (NHI-016, NHI-018, NHI-030, NHI-034), N/A=0.

---

## 4. Use-case scoring

| UC ID | Description (short) | Coverage | Maturity | Evidence |
|-------|---------------------|----------|----------|---------|
| UC-F-001 | Prevent plaintext secrets in repos | ADD-ON | 2 | No native pre-commit/push-protection; HCP Sentinel policies can gate Vault access but not scan repos [INDUSTRY-CONSENSUS] |
| UC-F-002 | Detect & remediate historical secrets | GAP | 0 | Vault does not provide repo scanning; complement with GitGuardian or Trufflehog [INDUSTRY-CONSENSUS] |
| UC-F-003 | JIT short-lived cloud creds via OIDC | NATIVE | 4 | JWT/OIDC auth + AWS/Azure/GCP dynamic creds engines provide full JIT federation [hashicorp-vault-jwt-2024] |
| UC-F-004 | SPIFFE/SPIRE workload-attested identity | NATIVE | 3 | SPIFFE auth method (ENT) + PKI SVID issuance; Community uses JWT-SVID pattern [hashicorp-vault-auth-2024] |
| UC-F-005 | Dynamic DB credentials with broker leases | NATIVE | 4 | Database secrets engine with 13+ plugins, TTL-bound leases, static/dynamic roles [hashicorp-vault-db-2024] |
| UC-F-006 | Automated rotation of long-lived static secrets | NATIVE | 4 | LDAP engine, DB engine static roles, scheduled root rotation (ENT), lease renewal [hashicorp-vault-db-2024] |
| UC-F-007 | Immediate revocation on compromise | NATIVE | 4 | Vault token revocation + lease revocation tree + PKI CRL immediate issuance [hashicorp-vault-pki-2024] |
| UC-F-008 | K8s secret consumption without on-disk plaintext | NATIVE | 4 | Agent Injector (sidecar/init) + Vault Secrets Store CSI Provider + etcd encryption [hashicorp-vault-k8s-2024] |
| UC-F-009 | Container image-pull creds issued per workload | ADD-ON | 2 | KV v2 + Agent Injector can deliver ECR tokens; no native per-workload image-pull dynamic engine [hashicorp-vault-agent-injector-2024] |
| UC-F-010 | IaC/config-mgmt secrets injected at apply-time | NATIVE | 4 | Vault Terraform Provider + HCP Terraform secrets sync; Ansible lookup plugin [hashicorp-vault-approle-2024] |
| UC-F-011 | Observability-agent credentials rotated | NATIVE | 3 | KV v2 + scheduled rotation; no native Datadog/Splunk dynamic engines [hashicorp-vault-kv-2024] |
| UC-F-012 | Message-broker client identity hardening | NATIVE | 3 | RabbitMQ secrets engine GA; mTLS via PKI; Kafka via KV + rotation [hashicorp-vault-secrets-2024] |
| UC-F-013 | gMSA/Kerberos modernisation for AD SAs | NATIVE | 3 | LDAP secrets engine generates dynamic AD creds; Kerberos auth method supported [hashicorp-vault-secrets-2024] |
| UC-F-014 | API-gateway upstream identity standardised | NATIVE | 3 | PKI engine for gateway mTLS certs; TLS cert auth for upstream [hashicorp-vault-pki-2024] |
| UC-F-015 | RPA bot credentials vaulted + session-bound | NATIVE | 3 | AppRole per-bot RoleID/SecretID pattern; response-wrapped SecretID delivery [hashicorp-vault-approle-2024] |
| UC-F-016 | Keyless code/artifact signing in CI | ADD-ON | 2 | PKI issues code-signing certs; Transit for signing operations; no native Sigstore Fulcio integration [hashicorp-vault-pki-2024] |
| UC-F-017 | TEE attestation gates secret release | GAP | 1 | No native Nitro/SEV-SNP/TDX attestation engine; community workarounds via JWT auth [INDUSTRY-CONSENSUS] |
| UC-F-018 | AI-agent / LLM tool-credential brokering | NATIVE | 3 | AppRole + JWT/OIDC + per-session dynamic creds; no AI-native policy primitives [hashicorp-vault-approle-2024] |
| UC-F-019 | IoT/OT/branch-device identity enrolment | ADD-ON | 2 | PKI engine ACME/EST/SCEP (ENT) for device certs; no DPS/IoT Hub native integration [hashicorp-vault-pki-2024] |
| UC-F-020 | Mainframe/midrange credential rotation | PARTNER | 2 | No native RACF/ACF2 plugin; requires partner bridge (e.g., CyberArk Conjur z/OS) [INDUSTRY-CONSENSUS] |
| UC-F-021 | Backup/DR agent identity de-privileging | NATIVE | 3 | LDAP engine + KV v2 for backup SA creds; DR Replication for vault resiliency [hashicorp-vault-replication-2024] |
| UC-F-022 | Webhook inbound identity verification | NATIVE | 2 | KV v2 stores HMAC secrets; rotation possible; no native webhook-broker workflow [hashicorp-vault-kv-2024] |
| UC-F-023 | Network-device credential modernisation | ADD-ON | 2 | SSH engine CA signing for device SSH; TACACS+ secrets via KV; no native TACACS+ integration [hashicorp-vault-ssh-2024] |
| UC-F-024 | Open-Banking / FAPI 2.0 mTLS partner identity | NATIVE | 3 | PKI engine for mTLS client cert lifecycle; TLS cert auth for partner validation [hashicorp-vault-pki-2024] |
| UC-F-025 | OAuth-app / marketplace integration governance | GAP | 0 | No native OAuth-app inventory or governance capability [INDUSTRY-CONSENSUS] |
| UC-F-026 | Vault-internal identity hardening | NATIVE | 4 | Root token sealed offline; Shamir M-of-N rekeying; auto-unseal KMS; replication token scoping [hashicorp-vault-seal-2024] |
| UC-F-027 | Orphaned/dormant NHI cleanup pipeline | ADD-ON | 2 | Vault audit logs + token TTL help limit orphans; no native dormancy-detection/sweep [hashicorp-vault-enterprise-2024] |
| UC-N-001 | Real-time secret-sprawl KPI dashboard | GAP | 1 | Vault UI shows lease/token counts; no cross-repo sprawl KPI dashboard [INDUSTRY-CONSENSUS] |
| UC-N-002 | NHI inventory and ownership attestation | ADD-ON | 2 | Vault entity/group model + namespaces; no unified cross-system NHI inventory [hashicorp-vault-enterprise-2024] |
| UC-N-003 | Rotation-coverage and freshness KPIs | ADD-ON | 2 | Audit log exports + Vault Sentinel can enforce policies; no built-in KPI dashboard [hashicorp-vault-enterprise-2024] |
| UC-N-004 | Regulator audit evidence pack | NATIVE | 3 | Immutable audit log (file/syslog); Sentinel policy-as-code; namespace-level audit isolation [hashicorp-vault-enterprise-2024] |
| UC-N-005 | Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Vault meets several E8/ZT pillars; no native E8 scorecard generation [INDUSTRY-CONSENSUS] |
| UC-N-006 | Vendor/SaaS supply-chain risk attestation | GAP | 0 | Not in Vault's scope; complement with TPRM tooling [INDUSTRY-CONSENSUS] |
| UC-N-007 | Data-sovereignty and residency assurance | NATIVE | 3 | Integrated Storage + self-managed deployment enables AU data residency; HCP Vault Dedicated ap-southeast-2 [hashicorp-hcp-vault-2024] |
| UC-N-008 | Engineer training and secure-coding KPI | GAP | 0 | Not in Vault's scope [INDUSTRY-CONSENSUS] |
| UC-N-009 | Exception register and risk-acceptance governance | ADD-ON | 2 | Sentinel EGP/RGP policies enforce exceptions; no native risk-register integration [hashicorp-vault-enterprise-2024] |
| UC-N-010 | Break-glass and quorum-operator governance | NATIVE | 4 | M-of-N Shamir unseal; root token rekeying; PKCS11 HSM; audit log of all break-glass events [hashicorp-vault-seal-2024] |
| UC-N-011 | Post-incident RCA and identity-driven reporting | NATIVE | 3 | Immutable audit log with full NHI attribution; revocation audit trail [hashicorp-vault-enterprise-2024] |
| UC-N-012 | Supply-chain / SLSA-provenance assurance | GAP | 1 | PKI engine supports signing cert issuance; no SLSA/in-toto native reporting [INDUSTRY-CONSENSUS] |
| UC-N-013 | Crypto-agility and PQC readiness reporting | ADD-ON | 1 | Transit + PKI support algorithm agility; no PQC/ML-DSA algorithms yet [INDUSTRY-CONSENSUS] |
| UC-N-014 | Vendor-evaluation matrix maintenance | N/A | 0 | Process/governance UC; not a product capability [INDUSTRY-CONSENSUS] |
| UC-N-015 | Communications and stakeholder cadence | N/A | 0 | Process/governance UC; not a product capability [INDUSTRY-CONSENSUS] |
| UC-N-016 | IoT / OT / branch-fleet posture reporting | ADD-ON | 2 | PKI engine cert inventory; no dedicated IoT fleet posture dashboard [hashicorp-vault-pki-2024] |
| UC-N-017 | Observability/telemetry secret-leak governance | ADD-ON | 2 | Audit log helps detect anomalous reads; no native log-scrubbing governance [hashicorp-vault-enterprise-2024] |
| UC-N-018 | Confidential-computing / TEE attestation assurance | GAP | 1 | No native TEE attestation reporting [INDUSTRY-CONSENSUS] |
| UC-N-019 | AI-agent / autonomous-workflow KPI suite | ADD-ON | 2 | Audit logs track per-tool credential issuance; no AI-agent-native KPI dashboard [hashicorp-vault-enterprise-2024] |
| UC-N-020 | Mainframe / legacy posture and exception transparency | PARTNER | 1 | Requires partner bridge for mainframe visibility; no native mainframe reporting [INDUSTRY-CONSENSUS] |

**UC coverage summary:** NATIVE=21, ADD-ON=14, PARTNER=2, GAP=8 (UC-F-002, UC-F-017, UC-F-025, UC-N-001, UC-N-006, UC-N-008, UC-N-012, UC-N-018), N/A=2.

---

## 5. Strengths and gaps

### Top 3 strengths

1. **Breadth and API maturity** [USER-SUPPLIED]: Vault's API-first design means every capability is equally accessible via CLI, HTTP API, or Terraform. Auth methods and secrets engines are uniformly pluggable. AppRole, Kubernetes auth, AWS IAM auth, and dynamic database credentials are the most mature and well-tested capabilities in any secrets broker in the market. The developer experience (SDKs, Vault Agent, CSI driver, injector) is class-leading. [hashicorp-vault-auth-2024] [hashicorp-vault-k8s-2024]

2. **PKI and workload identity ecosystem** [USER-SUPPLIED]: The PKI engine supports full CA lifecycle (root/intermediate/ACME/SCEP/EST in Enterprise), SPIFFE SVID issuance (Enterprise), and auto-rotation primitives. Integration with Consul Connect and service mesh CAs is native. This makes Vault the de-facto internal PKI and mTLS broker for cloud-native estates. [hashicorp-vault-pki-2024]

3. **Replication + HSM + FIPS posture**: Performance and DR Replication (with path-filter selectivity) provide enterprise-grade multi-region HA without custom tooling. PKCS#11 auto-unseal and seal wrap satisfy PCI HSM requirements. FIPS 140-3 builds (Leidos-attested v1.19.4+) meet government and regulated-sector cryptographic mandates. [hashicorp-vault-replication-2024] [hashicorp-vault-fips-2024]

### Top 3 gaps

1. **Azure auth method under-adoption observed in a major AU Tier-1 FI** `[USER-SUPPLIED]`: Despite Azure being one of three primary hyperscalers in scope, Azure auth has not been enabled. The Azure auth method has a documented 24-hour non-configurable token TTL and AKS-specific OIDC provider mismatch issues that create friction; these are known but require SE-level resolution. [hashicorp-vault-azure-2024]

2. **No native secret-scanning / sprawl detection**: Vault does not detect plaintext secrets in repos, CI variables, or Terraform state (UC-F-001, UC-F-002, UC-N-001). These P0 use cases require separate tooling (GitGuardian, Trufflehog). This is a structural gap — Vault is a broker, not a scanner. [INDUSTRY-CONSENSUS]

3. **Licensing complexity at enterprise scale** [USER-SUPPLIED]: Module-gated licensing (ADP-Transform, ADP-KM, Governance/Policy) adds commercial and operational complexity. Non-production clusters require separate licenses — a meaningful cost driver for regulated banks running dev/test/staging/prod lifecycle environments. The licensing model has evolved significantly post-IBM acquisition and requires active SE engagement. [hashicorp-vault-enterprise-2024]

---

## 6. AU-specific notes

**Data residency:** Self-managed Vault with Integrated Storage can be deployed entirely in AWS ap-southeast-2 or Azure australiaeast, satisfying APRA CPS 230 data residency. HCP Vault Dedicated also supports ap-southeast-2. [hashicorp-hcp-vault-2024]

**IRAP:** No public IRAP (Information Security Registered Assessors Program) assessment declaration found as of 2026-05-22. XYZ would need to independently assess or obtain a customer-managed IRAP assessment for Vault as a platform component. Suitable for PROTECTED workloads if deployed in an IRAP-assessed environment (e.g., AWS GovCloud AU or Vault self-managed in-region). [INDUSTRY-CONSENSUS]

**Essential 8 alignment:** Vault Enterprise directly addresses E8 controls: Restrict Admin Privileges (namespaces + Sentinel), Patch Applications (version upgrade paths), Multi-factor Authentication (MFA step-up in Enterprise). The FIPS 140-3 build satisfies ASD ISM cryptographic algorithm requirements. [hashicorp-vault-fips-2024]

**APRA CPS 234:** Vault's immutable audit log, namespace isolation, and Sentinel policy-as-code support CPS 234 §22 (information security capabilities), §28 (controls testing evidence), and §35 (incident notification audit trail). No explicit CPS 234 mapping is published by HashiCorp as of 2026-05-22 — XYZ would need to produce the control mapping. [INDUSTRY-CONSENSUS]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` — see `## HashiCorp Vault Enterprise (Agent 03 wave 1)` block.

---

## 8. Open questions for v1.0

1. **Azure auth enablement path** — What specific blockers (AKS OIDC provider mismatch, 24hr token TTL) prevent FI deployers from enabling Azure auth in practice? SE-level Vault Professional Services engagement recommended `[USER-SUPPLIED]`.
2. **Licensing model post-IBM acquisition** — Has the module/tier structure changed since IBM closed the HashiCorp acquisition? Verify current ADP-Transform and ADP-KM commercial terms with IBM/HashiCorp sales.
3. **IRAP assessment** — Does HashiCorp / IBM publish an IRAP assessment letter for Vault Enterprise or HCP Vault Dedicated? If not, XYZ's CISO team needs to commission one for any PROTECTED workload deployment.
4. **Plugin configuration at scale** — Vault's plugin model is powerful but operationally complex at XYZ scale (multiple namespaces, 100s of mounts). What is the operational runbook for mount lifecycle management? [USER-SUPPLIED]
5. **PQC roadmap** — When does HashiCorp plan to add ML-DSA (FIPS 204) to Transit and PKI engines? Needed for NHI-034 / UC-N-013 by APRA's implied 2030 deadline.
6. **Mainframe bridge** — What is the recommended partner integration path for RACF/ACF2 credential rotation (NHI-022 / UC-F-020) given the lack of a native plugin?
7. **TEE attestation** — Is HashiCorp planning native Nitro Enclave or AMD SEV-SNP attestation gating in Vault (NHI-018 / UC-F-017)?
8. **DR Replication token security** — Secondary activation tokens are compared to root tokens in the docs; what is XYZ's current handling of these tokens across DR clusters?

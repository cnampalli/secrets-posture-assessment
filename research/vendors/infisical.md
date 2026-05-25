# Vendor Profile — Infisical

**Tier:** emerging
**Primary docs:** https://infisical.com/docs
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Infisical is an open-source-first, all-in-one platform for secrets management, certificate management (PKI), KMS, and SSH certificate-based access. Founded 2022; the core repository is MIT-licensed on GitHub (6.95M+ downloads) with enterprise features in a separate `/ee` directory under a commercial licence. Three deployment modes: Infisical Cloud (SaaS — US and EU regions only; **no confirmed AU SaaS region as of 2026-05-22**), self-hosted (Docker Compose, Kubernetes/Helm, bare-metal Linux), and Enterprise self-hosted with HSM support. Primary differentiator is breadth: secrets + dynamic secrets + secret rotation + PKI + SSH CA + KMS + PAM, all from a single platform and single codebase. No confirmed AU customer references in public docs. Self-hosting is the recommended AU-sovereignty path for APRA-regulated entities.

**Citations:** [infisical-intro-2024][infisical-github-2024][infisical-pricing-2024]

---

## 2. Architecture (≤ 250 words)

**Storage backend:** PostgreSQL (primary data store) + Redis (caching, session, queue). Both can be externally managed for production HA. Self-hosted Helm chart supports external managed services (RDS, ElastiCache, etc.).

**Auth methods (machine identities):** Universal Auth (client ID + secret, platform-agnostic), AWS Auth (IAM/STS), Azure Auth (Managed Identity), GCP Auth (service account), Kubernetes Auth (projected SA token), OIDC Auth (generic OIDC provider), JWT Auth. LDAP authentication is Enterprise-tier only.

**Secrets engines / capabilities:**
- Secret Manager: versioned secrets, folders, environments, point-in-time recovery, secret syncs to AWS SM, GitHub, Vercel, and 50+ integrations.
- Secret Rotation (v2): PostgreSQL, MySQL, AWS IAM; scheduled interval-based with auto-rotation toggle.
- Dynamic Secrets: AWS IAM, AWS ElastiCache, AWS MemoryDB, PostgreSQL, Oracle (confirmed); additional templates in UI navigation (Redis, Cassandra, MongoDB, Kubernetes).
- KMS: internal AES-256-GCM per-org/per-project keys; external KMS (AWS KMS, GCP KMS, Azure KMS); HSM via PKCS#11 (Thales Luna, Fortanix, AWS CloudHSM) — Enterprise self-hosted only.
- PKI / Certificate Manager: internal CA hierarchy, external CA (ACME/Let's Encrypt/DigiCert/MS ADCS), ACME and EST enrollment, CRL, lifecycle management, certificate syncs, code-signing support, post-quantum algorithms referenced.
- SSH CA: signed SSH certificates for ephemeral infrastructure access (confirmed in GitHub README; docs path 404 at time of profile — likely doc reorganisation).
- PAM: listed as product tier on pricing page.

**Compliance:** SOC 2 reports available at Enterprise tier; FIPS 140-3 alignment claimed for self-hosted deployments via HSM integration. No confirmed ISO 27001 primary-source certification found. FedRAMP: not claimed.

**Citations:** [infisical-selfhost-2024][infisical-security-2024][infisical-kms-hsm-2024][infisical-helm-2024][infisical-rotation-2024][infisical-dynamic-secrets-2024][infisical-pki-2024][infisical-github-2024]

---

## 3. NHI coverage map (≤ 600 words)

| NHI ID | Coverage | Maturity | Evidence |
|--------|----------|----------|---------|
| NHI-001 Cloud IAM principal | NATIVE | 3 | AWS/Azure/GCP Auth methods + dynamic AWS IAM secrets [infisical-aws-auth-2024][infisical-dynamic-aws-iam-2024] |
| NHI-002 Kubernetes ServiceAccount | NATIVE | 3 | Kubernetes Auth (projected SA token) + K8s Operator [infisical-k8s-auth-2024][infisical-k8s-operator-2024] |
| NHI-003 CI/CD pipeline identity | NATIVE | 3 | OIDC Auth supports GitHub Actions/GitLab; 50+ integrations [infisical-oidc-auth-2024] |
| NHI-004 Container / image-pull credential | ADD-ON | 2 | Secret syncs to registries; no dedicated image-pull credential engine [infisical-github-2024] |
| NHI-005 Database service account | NATIVE | 3 | Dynamic secrets (PostgreSQL, Oracle) + rotation (PostgreSQL, MySQL) [infisical-dynamic-pg-2024][infisical-rotation-pg-2024] |
| NHI-006 Application TLS / mTLS workload identity | NATIVE | 3 | Internal PKI CA, ACME/EST enrollment, certificate lifecycle, CRL [infisical-pki-2024] |
| NHI-007 Third-party SaaS API key / OAuth client | ADD-ON | 2 | Secret rotation v2 supports generic secrets; no dedicated OAuth-client rotation [infisical-rotation-2024] |
| NHI-008 Git platform credential (PAT, deploy key) | NATIVE | 3 | Secret scanning CLI (140+ types), pre-commit hooks, git history scan [infisical-scanning-2024] |
| NHI-009 IaC / config-management agent identity | NATIVE | 2 | Terraform provider, Ansible integration, Infisical Agent [infisical-github-2024] |
| NHI-010 Monitoring / observability agent | ADD-ON | 2 | Secrets stored and synced; no dedicated observability-agent rotation engine [infisical-pricing-2024] |
| NHI-011 Message broker / event-bus client | ADD-ON | 1 | No confirmed native message-broker credential type; secrets manager path only [INDUSTRY-CONSENSUS] |
| NHI-012 Active Directory / LDAP service account | ADD-ON | 2 | LDAP auth (Enterprise); no native AD/gMSA rotation [infisical-pricing-2024] |
| NHI-013 Reverse-proxy / API-gateway identity | ADD-ON | 2 | PKI cert issuance for mTLS; no gateway-specific integration confirmed [infisical-pki-2024] |
| NHI-014 RPA bot identity | ADD-ON | 1 | Generic secret storage; no RPA orchestrator integration confirmed [INDUSTRY-CONSENSUS] |
| NHI-015 Code-signing identity | NATIVE | 2 | PKI code-signing support mentioned in certificate management [infisical-pki-2024] |
| NHI-016 Build provenance / SLSA attestation | GAP | 0 | No Sigstore/SLSA/in-toto integration found in docs [INDUSTRY-CONSENSUS] |
| NHI-017 Service mesh control-plane identity | ADD-ON | 1 | PKI CA can back Istio/Linkerd intermediate CA; no native mesh integration [infisical-pki-2024] |
| NHI-018 Confidential-computing attestation | GAP | 0 | No TEE attestation-gated secret release found [INDUSTRY-CONSENSUS] |
| NHI-019 AI agent / autonomous workflow identity | ADD-ON | 2 | AI Security Advisor (Enterprise), MCP server referenced but docs 404 [infisical-pricing-2024] |
| NHI-020 Model artifact / registry identity | GAP | 0 | No ML registry credential type found [INDUSTRY-CONSENSUS] |
| NHI-021 IoT / OT device identity | ADD-ON | 1 | PKI cert enrollment (ACME/EST/SCEP) applicable; no IoT fleet integration [infisical-pki-2024] |
| NHI-022 Mainframe / midrange service identity | GAP | 0 | No RACF/ACF2/IBM i integration found [INDUSTRY-CONSENSUS] |
| NHI-023 Database encryption / TDE master key | NATIVE | 2 | KMS per-project keys; external KMS integration for CMK control [infisical-kms-2024] |
| NHI-024 HSM / KMS operator identity | NATIVE | 3 | HSM PKCS#11 integration (Thales Luna, Fortanix, AWS CloudHSM); Enterprise self-hosted [infisical-kms-hsm-2024] |
| NHI-025 Certificate authority operator identity | NATIVE | 3 | Full internal CA hierarchy, admin roles, policies, profiles [infisical-pki-2024] |
| NHI-026 Backup / DR agent identity | ADD-ON | 1 | Generic secret storage; no backup-agent-specific credential rotation [INDUSTRY-CONSENSUS] |
| NHI-027 Backend-for-frontend / OBO token holder | ADD-ON | 2 | OIDC/JWT Auth for service identities; no dedicated OBO engine [infisical-oidc-auth-2024] |
| NHI-028 Federated B2B / Open Banking client identity | ADD-ON | 2 | PKI cert lifecycle for mTLS; no FAPI 2.0 / CDR-specific integration [infisical-pki-2024] |
| NHI-029 Service-account-as-human (shared functional ID) | ADD-ON | 1 | Secret storage; no IGA-style shared-account governance [INDUSTRY-CONSENSUS] |
| NHI-030 Browser / SaaS extension / OAuth-app identity | GAP | 0 | No OAuth-app inventory or governance feature found [INDUSTRY-CONSENSUS] |
| NHI-031 Webhook / inbound integration identity | ADD-ON | 1 | Secrets can store webhook signing secrets; no webhook-specific rotation [INDUSTRY-CONSENSUS] |
| NHI-032 Network / infrastructure device identity | ADD-ON | 1 | PKI cert enrollment for network devices; no TACACS+/RADIUS integration [infisical-pki-2024] |
| NHI-033 Print / spooler / branch-peripheral identity | ADD-ON | 1 | PKI 802.1X-capable certs; no peripheral-specific integration [infisical-pki-2024] |
| NHI-034 Quantum-resistant / hybrid-PKI rotation identity | NATIVE | 2 | Post-Quantum Algorithms reference page in PKI docs [infisical-pqc-2024] |
| NHI-035 Vault-internal / secrets-broker identity | NATIVE | 2 | Self-hosted root token management; auto-unseal via external KMS [infisical-kms-2024] |
| NHI-036 Ephemeral workload via SPIFFE / Aembit | ADD-ON | 1 | No native SPIFFE/SPIRE implementation; short-lived JWT via OIDC/Universal Auth [infisical-oidc-auth-2024] |
| NHI-037 Forgotten / orphaned legacy identity | ADD-ON | 1 | Audit logs + secret versioning; no dedicated dormancy sweep/orphan cleanup pipeline [infisical-audit-2024] |

---

## 4. Use-case scoring (≤ 800 words)

| UC ID | Coverage | Maturity | Evidence |
|-------|----------|----------|---------|
| UC-F-001 Prevent plaintext secrets in repos | NATIVE | 3 | CLI scanning 140+ types, pre-commit hook, git history scan [infisical-scanning-2024] |
| UC-F-002 Detect and remediate secrets in history | NATIVE | 3 | `infisical scan --verbose` full git history; pre-commit install [infisical-scanning-2024] |
| UC-F-003 JIT short-lived cloud credentials via OIDC | NATIVE | 3 | OIDC Auth, AWS/Azure/GCP Auth; dynamic AWS IAM credentials [infisical-oidc-auth-2024][infisical-dynamic-aws-iam-2024] |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | ADD-ON | 1 | No native SPIFFE/SPIRE; OIDC/JWT Auth provides short-lived tokens only [infisical-oidc-auth-2024] |
| UC-F-005 Dynamic DB credentials with broker leases | NATIVE | 3 | Dynamic secrets for PostgreSQL, Oracle, AWS ElastiCache, AWS MemoryDB [infisical-dynamic-pg-2024][infisical-dynamic-oracle-2024] |
| UC-F-006 Automated rotation of long-lived static secrets | NATIVE | 3 | Secret Rotation v2 (PostgreSQL, MySQL, AWS IAM) with scheduled intervals [infisical-rotation-2024] |
| UC-F-007 Immediate revocation on identity compromise | NATIVE | 2 | Secret versioning, point-in-time recovery, access revocation via machine identity management [infisical-security-2024] |
| UC-F-008 K8s secret consumption without on-disk plaintext | NATIVE | 3 | Kubernetes Operator syncs to K8s native secrets; Infisical Agent for injection [infisical-k8s-operator-2024] |
| UC-F-009 Container image-pull credentials per workload | ADD-ON | 2 | K8s Operator can populate imagePullSecrets; no dedicated per-workload image-pull engine [infisical-k8s-operator-2024] |
| UC-F-010 IaC / config-management secrets at apply-time | NATIVE | 2 | Terraform provider, Ansible integration, dynamic secret fetch at run time [infisical-github-2024] |
| UC-F-011 Observability-agent credentials rotated and scoped | ADD-ON | 2 | Secrets Manager stores agent tokens; rotation v2 can target API-key secrets [infisical-rotation-2024] |
| UC-F-012 Message-broker client identity hardening | ADD-ON | 1 | No native Kafka/RabbitMQ/SQS mTLS engine; PKI for mTLS only [infisical-pki-2024] |
| UC-F-013 gMSA / Kerberos modernisation for AD accounts | ADD-ON | 1 | LDAP auth (Enterprise); no gMSA/Kerberos rotation native [infisical-pricing-2024] |
| UC-F-014 API-gateway upstream identity standardised | ADD-ON | 2 | PKI cert lifecycle for gateway mTLS; no gateway-specific integration [infisical-pki-2024] |
| UC-F-015 RPA bot credentials vaulted and session-bound | ADD-ON | 1 | Generic secret storage; no RPA orchestrator native integration [INDUSTRY-CONSENSUS] |
| UC-F-016 Keyless code- and artifact-signing in CI | NATIVE | 2 | PKI code-signing support; PKI reference includes PQC algorithms [infisical-pki-2024][infisical-pqc-2024] |
| UC-F-017 TEE attestation gates secret release | GAP | 0 | No TEE/confidential-computing attestation flow found in docs [INDUSTRY-CONSENSUS] |
| UC-F-018 AI-agent / LLM tool-credential brokering | ADD-ON | 2 | AI Security Advisor (Enterprise), MCP server referenced but not confirmed in docs [infisical-pricing-2024] |
| UC-F-019 IoT / OT / branch-device identity enrolment | ADD-ON | 2 | PKI supports ACME/EST enrollment applicable to IoT; no fleet integration [infisical-pki-2024] |
| UC-F-020 Mainframe / midrange credential rotation pipeline | GAP | 0 | No RACF/ACF2/IBM-i integration found [INDUSTRY-CONSENSUS] |
| UC-F-021 Backup / DR agent identity de-privileging | ADD-ON | 1 | Generic secret storage for backup agent creds; no native backup integration [INDUSTRY-CONSENSUS] |
| UC-F-022 Webhook inbound identity verification | ADD-ON | 1 | Secrets Manager can store HMAC webhook secrets; no rotation native [infisical-rotation-2024] |
| UC-F-023 Network-device credential modernisation | ADD-ON | 1 | PKI cert enrollment for network devices; no TACACS+/RADIUS rotation [infisical-pki-2024] |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner identity | ADD-ON | 2 | PKI lifecycle management for mTLS client certs; no FAPI-specific feature [infisical-pki-2024] |
| UC-F-025 OAuth-app / marketplace integration governance | GAP | 0 | No OAuth-app inventory or shadow-integration governance [INDUSTRY-CONSENSUS] |
| UC-F-026 Vault-internal identity hardening | NATIVE | 2 | External KMS for auto-unseal, machine identity for vault agent, audit logs [infisical-kms-2024][infisical-audit-2024] |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | ADD-ON | 1 | Audit logs show access history; no automated dormancy sweep or owner-attestation pipeline [infisical-audit-2024] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | ADD-ON | 2 | Insights feature in Secrets Manager; no cross-repo KPI dashboard [infisical-github-2024] |
| UC-N-002 NHI inventory and ownership attestation | ADD-ON | 2 | Machine identity management UI; no enterprise-grade IGA attestation workflow [infisical-machine-identities-2024] |
| UC-N-003 Rotation-coverage and freshness KPIs | ADD-ON | 2 | Rotation v2 scheduling; no KPI reporting/dashboard for rotation coverage [infisical-rotation-2024] |
| UC-N-004 Regulator audit evidence pack | ADD-ON | 2 | Audit logs with custom retention (Enterprise); no one-click evidence-pack generation [infisical-audit-2024] |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 1 | No E8/ZT scorecard feature; self-hosted enables controls alignment [INDUSTRY-CONSENSUS] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | ADD-ON | 1 | No vendor risk scoring or supply-chain attestation feature [INDUSTRY-CONSENSUS] |
| UC-N-007 Data-sovereignty and residency assurance | NATIVE | 3 | Self-hosted on any infrastructure; no AU SaaS region — self-host required for APRA CPS 230 [infisical-selfhost-2024] |
| UC-N-008 Engineer training and secure-coding adoption KPI | GAP | 0 | No training module or adoption KPI feature found [INDUSTRY-CONSENSUS] |
| UC-N-009 Exception register and risk-acceptance governance | GAP | 0 | No exception register or GRC integration found [INDUSTRY-CONSENSUS] |
| UC-N-010 Break-glass and quorum-operator governance | ADD-ON | 2 | HSM quorum via PKCS#11 (Enterprise); no vault-level Shamir quorum UI [infisical-kms-hsm-2024] |
| UC-N-011 Post-incident reporting and identity-driven RCA | ADD-ON | 2 | Audit logs with streaming (Enterprise); no SOAR/MITRE-mapped RCA tooling [infisical-audit-2024] |
| UC-N-012 Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA/in-toto/Sigstore integration or reporting [INDUSTRY-CONSENSUS] |
| UC-N-013 Crypto-agility and post-quantum readiness reporting | NATIVE | 2 | PQC algorithms in PKI CA; dedicated PQC reference page [infisical-pqc-2024] |
| UC-N-014 Vendor-evaluation matrix maintenance | N/A | 0 | This is a process UC; vendor does not address it natively [N/A] |
| UC-N-015 Communications, change-comms and stakeholder cadence | N/A | 0 | Process UC; out of scope for vendor tooling [N/A] |
| UC-N-016 IoT / OT / branch-fleet posture reporting | ADD-ON | 1 | PKI enrollment for IoT; no fleet posture dashboard [infisical-pki-2024] |
| UC-N-017 Observability/telemetry secret-leak governance | ADD-ON | 1 | CLI scanning covers log files; no ingest-tier log-scrubbing integration [infisical-scanning-2024] |
| UC-N-018 Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE attestation evidence or reporting [INDUSTRY-CONSENSUS] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | ADD-ON | 1 | AI Security Advisor in Enterprise; no per-tool credential issuance KPIs confirmed [infisical-pricing-2024] |
| UC-N-020 Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe/RPA posture reporting [INDUSTRY-CONSENSUS] |

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

**1. Broadest built-in scope of any emerging vendor.** Infisical combines secrets management, dynamic secrets, secret rotation, internal PKI/CA, SSH certificate authority, KMS, and HSM integration in a single platform. No other emerging-tier vendor matches this breadth from a single codebase, reducing integration complexity for platform engineering teams.

**2. Open-source-first with genuine self-host parity.** MIT licence (core) means XYZ can self-host on-premises or in AU-sovereign cloud (e.g., AWS ap-southeast-2) with no dependency on Infisical SaaS. The Helm chart supports external PostgreSQL/Redis (RDS/ElastiCache), enabling high-availability deployments within APRA CPS 230 data-residency boundaries. HSM integration (Thales Luna, Fortanix, AWS CloudHSM) is available for PCI/APRA CPS 234 key-custody requirements.

**3. Post-quantum readiness ahead of peers.** A dedicated PQC algorithms reference exists in the PKI CA documentation, placing Infisical ahead of most emerging vendors on NHI-034 and UC-N-013. Certificate policies/profiles with PQC algorithm selection support XYZ's 2026–2028 hybrid-cert roadmap.

### Top 3 gaps

**1. No AU SaaS region.** For teams that prefer managed SaaS, Infisical Cloud offers only US and EU regions. APRA-regulated workloads cannot use Infisical Cloud without an explicit data-residency risk acceptance; self-hosting is the only compliant path.

**2. Weak enterprise governance layer.** No orphan/dormancy cleanup pipeline (UC-F-027), no exception register (UC-N-009), no SLSA/supply-chain attestation (UC-N-012), and no SOAR integration for identity-driven RCA. Compared to Delinea or CyberArk, the governance and audit story is immature.

**3. No mainframe or SPIFFE native.** NHI-022 (mainframe/RACF) and NHI-036 (SPIFFE/SPIRE) are both gaps. For XYZ's core-banking estate and zero-trust workload-identity roadmap, complementary tools (Conjur z/OS, SPIRE) would be required.

---

## 6. AU-specific notes (≤ 150 words)

**Data residency:** Infisical Cloud operates from US/EU regions only — no confirmed AU SaaS region. Self-hosting in AWS `ap-southeast-2` (Sydney) or Azure `australiaeast` is the only path to APRA CPS 230 §39 data-residency compliance. Self-hosted deployments keep all secret data under XYZ control, satisfying CPS 234 §22 and §28 governance requirements.

**IRAP:** No IRAP assessment found in public documentation. Self-hosted on an IRAP-assessed cloud platform (AWS/Azure/GCP in AU regions) would partially satisfy ASD ISM controls; Infisical itself is not assessed.

**Essential 8:** Secret scanning CLI addresses E8-AppControl (restrict script execution / malicious code); dynamic secrets + rotation address E8-RestrictAdminPriv. No built-in E8 maturity scorecard.

**APRA CPS 234:** HSM integration and external KMS support address CPS 234 §28b cryptographic key custody requirements when self-hosted.

**Citations:** [infisical-selfhost-2024][infisical-security-2024]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Infisical (Agent 03 wave 3)`.

---

## 8. Open questions for v1.0

1. **SSH CA docs path:** The `/docs/documentation/platform/ssh` page returned 404 at profile time. Confirm current URL and SSH CA capabilities (user vs. host certs, TTL, hostnames).
2. **AU SaaS region:** Is an AU Infisical Cloud region on the roadmap? Timeline?
3. **MCP server:** The MCP server is referenced in the GitHub README and pricing ("AI Security Advisor") but docs path 404. Confirm GA status, scope of AI agent identity features.
4. **ISO 27001:** No public ISO 27001 certification found. Does Infisical hold or plan one?
5. **Dynamic secrets full list:** The UI navigation suggests Redis, Cassandra, MongoDB, Kubernetes templates — confirm GA status and enumerate all supported engines.
6. **SPIFFE roadmap:** Is a native SPIFFE Workload API planned?
7. **FAPI 2.0 / CDR:** Any plans to support CDR/Open Banking specific enrolment workflows?
8. **Rotation v2 full target list:** Are SendGrid, Twilio, LDAP, and other non-DB rotation targets on the roadmap?
9. **IRAP / Essential 8 self-assessment:** Any plans to publish an IRAP-equivalent assessment?

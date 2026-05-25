# Vendor Profile — Delinea Secret Server

**Tier:** core  
**Primary docs:** https://docs.delinea.com/online-help/secret-server/start.htm  
**Profile written:** 2026-05-22  
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

Delinea (formed 2021 from the merger of Thycotic and Centrify) is a US-headquartered PAM vendor. Secret Server is its flagship privileged-account vault, available as **Self-Hosted** (Windows Server + MS SQL) and **Secret Server Cloud** (SaaS). Delinea positions Secret Server between Vault's developer/cloud-native focus and CyberArk's enterprise PAM depth, emphasising **ease of use, fast time-to-value, and lower total-cost-of-ownership**. Related products — DevOps Secrets Vault (DSV, developer-facing), Privilege Manager (endpoint EPM), and the newly acquired StrongDM (JIT runtime authorisation) — extend the platform. Delinea is actively used in AU financial services (community evidence) but no dedicated AU data-residency region has been confirmed in public documentation as of May 2026. Delinea is privately held. [delinea-ss-product-2025; delinea-home-2025]

---

## 2. Architecture

**Storage backend:** Microsoft SQL Server (self-hosted). Secrets encrypted AES-256 CBC at rest; all web and API traffic requires TLS 1.2+. [delinea-ss-security-2025]

**Auth methods:** Windows Authentication (Kerberos/NTLM), SAML 2.0 SSO, LDAP/Active Directory sync, MFA at login and optionally per-secret. [delinea-ss-auth-2025]

**Distributed Engine (DE):** Lightweight Windows service agents deployed in network segments, DMZs, or remote sites. DEs relay RPC (Remote Password Changing), heartbeat, and discovery traffic to the central Secret Server; traffic is outbound from DE to SS, reducing firewall requirements. Multiple DEs per site for HA. [delinea-ss-security-2025]

**Secrets engines:** No secrets-engine plugin model (unlike Vault). Capability is delivered via built-in Secret Templates (150+ out of box), remote password changers, and the REST API. Custom password changers via PowerShell extend coverage to non-standard targets.

**HSM/KMS support:** Secret Server supports an HSM to protect its master encryption key. Public docs reference Thales/SafeNet nShield (community). Specific certified vendor list not confirmed in primary public docs. [delinea-ss-security-2025]

**Replication / HA / DR:** Active/passive SQL Server mirroring or AlwaysOn AG for database HA; multiple web nodes behind a load balancer; multiple DEs per site for workload distribution. No multi-region active-active replication documented publicly (unlike Vault Enterprise). [delinea-ss-security-2025]

**Compliance posture:** SOC 2 Type II (Delinea cloud products); FedRAMP authorisation not confirmed for Secret Server Cloud as of May 2026; IRAP assessment not confirmed publicly. [delinea-ss-product-2025]

**Cloud:** Secret Server Cloud runs in US and EU regions; AU (AWS Sydney) region availability is not confirmed in current public documentation.

---

## 3. NHI Coverage Map

| NHI ID | Name | Coverage | Maturity | Evidence |
|--------|------|----------|----------|----------|
| NHI-001 | Cloud IAM principal | ADD-ON | 2 | Discovery supports AWS/GCP IAM accounts; static rotation only, no dynamic short-lived creds. [delinea-ss-discovery-2025] |
| NHI-002 | Kubernetes ServiceAccount | ADD-ON | 1 | No native K8s controller; REST API can be scripted; DSV (separate product) adds K8s integration. [delinea-ss-api-2025] |
| NHI-003 | CI/CD pipeline identity | ADD-ON | 2 | REST API + token auth; no native OIDC federation for CI/CD pipelines (unlike Vault). [delinea-ss-api-2025] |
| NHI-004 | Container / image-pull credential | ADD-ON | 1 | Storable via custom template; no native registry integration; REST API retrieval. [delinea-ss-features-2025] |
| NHI-005 | Database service account | NATIVE | 3 | Built-in RPC for SQL Server, Oracle, MySQL, PostgreSQL; heartbeat; auto-rotation. [delinea-ss-features-2025] |
| NHI-006 | Application TLS / mTLS workload identity | ADD-ON | 2 | Certificate management feature (later versions); limited scope; no full CLM. [delinea-ss-admin-2025] |
| NHI-007 | SaaS API key / OAuth client | NATIVE | 2 | Generic secret template + manual rotation; no OAuth client credential engine. [delinea-ss-features-2025] |
| NHI-008 | Git platform credential (PAT / SSH) | NATIVE | 2 | Storable; custom RPC scripts can rotate; no native GitHub/GitLab integration. [delinea-ss-features-2025] |
| NHI-009 | Config-mgmt / IaC agent identity | ADD-ON | 2 | REST API + scripted retrieval; Ansible/Terraform community modules exist. [delinea-ss-api-2025] |
| NHI-010 | Monitoring / observability agent | NATIVE | 2 | Generic secret storage + rotation via RPC; no deep SIEM/observability native integration. [delinea-ss-features-2025] |
| NHI-011 | Message-broker / event-bus client | NATIVE | 2 | Generic credential storage; RabbitMQ/Kafka passwords via custom RPC. [delinea-ss-features-2025] |
| NHI-012 | Active Directory / LDAP service account | NATIVE | 4 | Core PAM use-case; discovery, rotation, heartbeat, dependency mapping for AD SAs. [delinea-ss-discovery-2025] |
| NHI-013 | Reverse-proxy / API-gateway upstream identity | NATIVE | 2 | Generic credential template; no native APIM integration. [delinea-ss-features-2025] |
| NHI-014 | RPA bot identity | NATIVE | 3 | RPA integrations documented (UiPath, Blue Prism); session-bound checkout; audit trail. [delinea-ss-product-2025] |
| NHI-015 | Code-signing identity | PARTNER | 1 | Not natively supported; storable but no PKI/HSM-backed signing workflow. [delinea-ss-features-2025] |
| NHI-016 | Build provenance / SLSA attestation | GAP | 0 | No documented SLSA or supply-chain attestation capability. [INDUSTRY-CONSENSUS] |
| NHI-017 | Service mesh control-plane identity | GAP | 0 | No Istio/Envoy/Consul service mesh integration documented. [INDUSTRY-CONSENSUS] |
| NHI-018 | Confidential-computing attestation | GAP | 0 | No TEE / confidential computing attestation support documented. [INDUSTRY-CONSENSUS] |
| NHI-019 | AI agent / autonomous workflow identity | ADD-ON | 1 | Delinea platform roadmap (StrongDM JIT) addresses agentic identity; Secret Server alone lacks native AI-agent credential brokering. [delinea-home-2025] |
| NHI-020 | Model artifact / registry identity | GAP | 0 | No model registry credential management documented. [INDUSTRY-CONSENSUS] |
| NHI-021 | IoT / OT device identity | ADD-ON | 1 | Custom secret templates; no native OT/SCADA protocols; extensible via PowerShell. [delinea-ss-features-2025] |
| NHI-022 | Mainframe / midrange service identity | GAP | 0 | No documented RACF / Top Secret / ACF2 support. [INDUSTRY-CONSENSUS] |
| NHI-023 | Database encryption / TDE master key | ADD-ON | 1 | Can store TDE passwords; no KMS integration or key lifecycle management. [delinea-ss-features-2025] |
| NHI-024 | HSM / KMS operator / break-glass identity | ADD-ON | 2 | HSM master key support; break-glass via Unlimited Admin mode; quorum not documented. [delinea-ss-security-2025] |
| NHI-025 | Certificate authority operator identity | ADD-ON | 2 | Certificate management add-on; limited CA operator workflow vs. Venafi/Keyfactor. [delinea-ss-admin-2025] |
| NHI-026 | Backup / DR agent identity | NATIVE | 2 | Generic credential management; DE multi-site supports DR contexts. [delinea-ss-security-2025] |
| NHI-027 | Backend-for-frontend / on-behalf-of token | ADD-ON | 1 | Generic secret storage; no OAuth token delegation engine. [delinea-ss-features-2025] |
| NHI-028 | Federated B2B / Open Banking client identity | GAP | 0 | No FAPI 2.0 / CDR-specific support documented. [INDUSTRY-CONSENSUS] |
| NHI-029 | Service-account-as-human (shared functional ID) | NATIVE | 3 | Core Secret Server use-case; checkout/check-in, session recording, dual-approval. [delinea-ss-product-2025] |
| NHI-030 | Browser / SaaS extension / OAuth-app identity | ADD-ON | 2 | Delinea Credential Manager browser extension; OAuth app secrets storable. [delinea-ss-features-2025] |
| NHI-031 | Webhook / inbound integration identity | NATIVE | 2 | Generic credential storage; webhook signing secrets managed manually. [delinea-ss-features-2025] |
| NHI-032 | Network / infrastructure device identity | NATIVE | 3 | Cisco, Juniper, F5, network device RPC templates; discovery for network accounts. [delinea-ss-discovery-2025] |
| NHI-033 | Print / spooler / branch-peripheral identity | ADD-ON | 1 | Custom template; no native SNMP v3 or 802.1X workflow. [delinea-ss-features-2025] |
| NHI-034 | Quantum-resistant / hybrid-PKI rotation identity | GAP | 0 | No PQC roadmap documented publicly for Secret Server. [INDUSTRY-CONSENSUS] |
| NHI-035 | Vault-internal / secrets-broker identity | NATIVE | 2 | DE identity, SQL service account password management, admin role separation. [delinea-ss-security-2025] |
| NHI-036 | Ephemeral workload via SPIFFE/Aembit/Clutch | GAP | 0 | No SPIFFE/SPIRE integration documented; StrongDM acquisition may address. [delinea-home-2025] |
| NHI-037 | Forgotten / orphaned legacy identity | NATIVE | 3 | Discovery pipeline identifies unmanaged accounts; heartbeat detects drift; dependency mapping. [delinea-ss-discovery-2025] |

**NHI Summary:** NATIVE=19, ADD-ON=12, PARTNER=1, GAP=6, N/A=0

---

## 4. Use-Case Scoring

| UC ID | Title (abbrev.) | Coverage | Maturity | Evidence |
|-------|-----------------|----------|----------|----------|
| UC-F-001 | Prevent plaintext secrets in source repos | ADD-ON | 2 | REST API pull pattern prevents embedding; no native pre-commit hook scanner. [delinea-ss-api-2025] |
| UC-F-002 | Detect and remediate secrets in history | PARTNER | 1 | No native repo-scanning; partner/integration required (e.g., GitGuardian). [INDUSTRY-CONSENSUS] |
| UC-F-003 | JIT short-lived cloud creds via OIDC | GAP | 0 | No OIDC federation for dynamic cloud creds; static IAM key rotation only. [delinea-ss-discovery-2025] |
| UC-F-004 | Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No SPIFFE/SPIRE support. [INDUSTRY-CONSENSUS] |
| UC-F-005 | Dynamic DB credentials with broker leases | ADD-ON | 2 | Password rotation on schedule/checkout; no true dynamic lease/TTL model like Vault. [delinea-ss-features-2025] |
| UC-F-006 | Automated rotation of long-lived static secrets | NATIVE | 4 | Core capability; 150+ built-in RPC templates; heartbeat; scheduled rotation. [delinea-ss-features-2025] |
| UC-F-007 | Immediate revocation on identity compromise | NATIVE | 3 | Disable secret, immediate RPC rotation, dependency notification; limited broadcast revocation. [delinea-ss-product-2025] |
| UC-F-008 | K8s secret consumption without on-disk plaintext | ADD-ON | 1 | No native K8s CSI driver; REST API retrieval at pod startup via init containers. [delinea-ss-api-2025] |
| UC-F-009 | Container image-pull creds per workload | ADD-ON | 1 | Storable; no native registry webhook; scripted retrieval. [delinea-ss-features-2025] |
| UC-F-010 | IaC / config-mgmt secrets injected at apply-time | ADD-ON | 2 | REST API + Ansible/Terraform community plugins; no official provider. [delinea-ss-api-2025] |
| UC-F-011 | Observability-agent creds rotated and scoped | NATIVE | 2 | Generic credential rotation; no deep observability-platform integration. [delinea-ss-features-2025] |
| UC-F-012 | Message-broker client identity hardening | NATIVE | 2 | Password-based credential storage + rotation for Kafka/RabbitMQ. [delinea-ss-features-2025] |
| UC-F-013 | gMSA / Kerberos modernisation for AD SAs | NATIVE | 4 | Deep AD discovery, gMSA support, dependency mapping, scheduled rotation — industry-leading PAM core. [delinea-ss-discovery-2025] |
| UC-F-014 | API-gateway upstream identity standardised | NATIVE | 2 | Generic secret storage + rotation; no native APIM/Kong/NGINX integration. [delinea-ss-features-2025] |
| UC-F-015 | RPA bot creds vaulted and session-bound | NATIVE | 3 | UiPath/Blue Prism integrations; checkout with session recording; dual-approval. [delinea-ss-product-2025] |
| UC-F-016 | Keyless code/artifact signing in CI | PARTNER | 1 | Not native; cert storage possible; requires partner (Sigstore/Venafi). [INDUSTRY-CONSENSUS] |
| UC-F-017 | TEE attestation gates secret release | GAP | 0 | No confidential computing attestation documented. [INDUSTRY-CONSENSUS] |
| UC-F-018 | AI-agent / LLM tool-credential brokering | ADD-ON | 1 | Platform direction (StrongDM JIT); Secret Server alone lacks native AI-agent context. [delinea-home-2025] |
| UC-F-019 | IoT / OT / branch-device identity enrolment | ADD-ON | 1 | Custom templates; no OT/SCADA protocol support natively. [delinea-ss-features-2025] |
| UC-F-020 | Mainframe / midrange credential rotation | GAP | 0 | No RACF/TSS/ACF2 support. [INDUSTRY-CONSENSUS] |
| UC-F-021 | Backup / DR agent identity de-privileging | NATIVE | 2 | Generic managed credentials for backup agents; DE multi-site DR. [delinea-ss-security-2025] |
| UC-F-022 | Webhook inbound identity verification | NATIVE | 2 | Webhook signing secrets storable; manual rotation via RPC. [delinea-ss-features-2025] |
| UC-F-023 | Network-device credential modernisation | NATIVE | 3 | Cisco IOS, Juniper, F5, network device RPC templates; SSH key management. [delinea-ss-discovery-2025] |
| UC-F-024 | Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | No FAPI 2.0 or CDR-specific workflow documented. [INDUSTRY-CONSENSUS] |
| UC-F-025 | OAuth-app / marketplace integration governance | ADD-ON | 1 | Generic secret storage; no OAuth app lifecycle management. [delinea-ss-features-2025] |
| UC-F-026 | Vault-internal identity hardening | NATIVE | 2 | DE identity protection; admin role separation; SQL SA password management. [delinea-ss-security-2025] |
| UC-F-027 | Orphaned / dormant NHI cleanup pipeline | NATIVE | 3 | Discovery identifies unmanaged; heartbeat detects drift; dependency map for cleanup. [delinea-ss-discovery-2025] |
| UC-N-001 | Real-time secret-sprawl KPI dashboard | NATIVE | 3 | Built-in reports and dashboards; audit logs; secret inventory metrics. [delinea-ss-features-2025] |
| UC-N-002 | NHI inventory and ownership attestation | NATIVE | 3 | Discovery-driven inventory; secret ownership assignment; access reviews. [delinea-ss-discovery-2025] |
| UC-N-003 | Rotation-coverage and freshness KPIs | NATIVE | 3 | Heartbeat + rotation schedule reports; stale-secret dashboards. [delinea-ss-features-2025] |
| UC-N-004 | Regulator audit evidence pack | NATIVE | 3 | Full audit trail; session recording (with PSM); exportable reports for regulators. [delinea-ss-product-2025] |
| UC-N-005 | Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Built-in controls map to E8 restrict-admin-privs; no automated E8 scorecard export. [delinea-ss-features-2025] |
| UC-N-006 | Vendor / SaaS supply-chain risk attestation | ADD-ON | 1 | Generic secret storage; no supply-chain risk scoring workflow natively. [delinea-ss-features-2025] |
| UC-N-007 | Data-sovereignty and residency assurance | ADD-ON | 2 | Self-hosted option enables on-prem AU deployment; Cloud edition US/EU regions only. [delinea-ss-security-2025] |
| UC-N-008 | Engineer training and secure-coding adoption KPI | ADD-ON | 1 | No built-in training or adoption KPI capability; reports show API usage. [delinea-ss-features-2025] |
| UC-N-009 | Exception register and risk-acceptance governance | NATIVE | 2 | Ticketing system integration (ServiceNow etc.); exception workflows via approval. [delinea-ss-admin-2025] |
| UC-N-010 | Break-glass and quorum-operator governance | NATIVE | 3 | Unlimited admin mode; dual-control workflow; emergency access with full audit. [delinea-ss-security-2025] |
| UC-N-011 | Post-incident reporting and identity-driven RCA | NATIVE | 3 | Session recording; audit trail; exportable event logs for forensic RCA. [delinea-ss-product-2025] |
| UC-N-012 | Supply-chain / SLSA-provenance assurance | GAP | 0 | No SLSA attestation or provenance reporting. [INDUSTRY-CONSENSUS] |
| UC-N-013 | Crypto-agility and post-quantum readiness | GAP | 0 | No PQC roadmap confirmed; AES-256 at rest. [INDUSTRY-CONSENSUS] |
| UC-N-014 | Vendor-evaluation matrix maintenance | N/A | 0 | Governance process; not a product capability. [N/A] |
| UC-N-015 | Communications / change-comms / stakeholder cadence | N/A | 0 | Governance process; not a product capability. [N/A] |
| UC-N-016 | IoT / OT / branch-fleet posture reporting | ADD-ON | 1 | Limited; custom templates for IoT; no fleet-posture reporting. [delinea-ss-features-2025] |
| UC-N-017 | Observability/telemetry secret-leak governance | NATIVE | 2 | Audit logs detect secret access anomalies; PBA (Privileged Behaviour Analytics) add-on. [delinea-ss-product-2025] |
| UC-N-018 | Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE capability. [INDUSTRY-CONSENSUS] |
| UC-N-019 | AI-agent / autonomous-workflow KPI suite | ADD-ON | 1 | No native AI-agent KPI; platform roadmap direction. [delinea-home-2025] |
| UC-N-020 | Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe credential management. [INDUSTRY-CONSENSUS] |

**UC Summary:** NATIVE=20, ADD-ON=15, PARTNER=2, GAP=8, N/A=2

---

## 5. Strengths and Gaps

### Top 3 Strengths

1. **AD / Windows service account PAM depth (NHI-012, UC-F-013):** Delinea Secret Server leads the market in AD service account lifecycle management — discovery, gMSA, dependency mapping, scheduled rotation, and heartbeat are all GA-mature and well-documented. For XYZ banks with large AD footprints, this is the strongest out-of-box capability vs. Vault (ADD-ON) and CyberArk PAM (comparable).

2. **Ease-of-use and time-to-value:** 150+ built-in secret templates, a GUI-driven discovery wizard, and role-based access control make Secret Server deployable by teams without deep PAM engineering expertise. The UX claim is well-supported by the features documentation and market positioning — substantially simpler than CyberArk PAM's CPM/PSM/PVWA stack or Vault's CLI-first model.

3. **Static/long-lived secret rotation coverage (UC-F-006, UC-F-027):** Heartbeat-based drift detection, PowerShell-extensible RPC, and dependency mapping address the XYZ "never-rotated service account" risk better than most cloud-native tools. Network device coverage (Cisco, F5, Juniper) is NATIVE and mature, filling gaps left by Vault-centric approaches.

### Top 3 Gaps

1. **Dynamic / ephemeral credential generation (UC-F-003, UC-F-004, UC-F-005):** Secret Server has no native dynamic-secrets engine comparable to Vault's database/cloud/PKI engines. Cloud IAM JIT creds, SPIFFE workload attestation, and short-lived DB leases are all gaps or require DevOps Secrets Vault (separate product + licensing).

2. **Cloud-native / Kubernetes / CI-CD integration (NHI-002, NHI-003, UC-F-008):** No native Kubernetes CSI driver, no OIDC federation for CI/CD pipelines, no official Terraform provider. These gaps matter significantly for XYZ's cloud-native workloads and are the primary areas where Vault Enterprise leads Delinea.

3. **Mainframe + FAPI/CDR + PQC (NHI-022, UC-F-020, UC-F-024, UC-N-013):** No RACF/TSS/ACF2 credential management, no FAPI 2.0/CDR workflow, and no post-quantum cryptography roadmap confirmed. For an XYZ bank with mainframe systems and Open Banking obligations, these are significant capability gaps requiring supplementary tooling.

---

## 6. AU-Specific Notes

**Data residency:** Secret Server Self-Hosted can be deployed entirely within Australian infrastructure (XYZ-managed datacentres or AWS Sydney), satisfying CPS 230/234 data-sovereignty requirements. Secret Server Cloud regions are documented as US and EU only — no Sydney/AP region confirmed in public docs as of May 2026. XYZ would need to use self-hosted for AU data-residency compliance if Cloud edition is selected.

**IRAP:** No IRAP (Information Security Registered Assessors Program) assessment confirmed for Delinea Secret Server in public sources. [SPECULATION — SE conversation required]

**Essential 8:** Secret Server's core capabilities (restrict admin privileges, application control via Privilege Manager integration, multi-factor authentication) align strongly with Essential 8 maturity levels 1–2. No automated E8 scorecard export is documented.

**AU customers:** Delinea is cited in the broader AU financial services and government sectors (community), but no named AU Tier-1 bank case study is publicly available. CyberArk's NAB case study gives CyberArk an edge in AU reference-customer positioning. [delinea-home-2025; INDUSTRY-CONSENSUS]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Delinea Secret Server (Agent 03 wave 1)`:

- delinea-ss-docs-2025
- delinea-ss-discovery-2025
- delinea-ss-auth-2025
- delinea-ss-security-2025
- delinea-ss-api-2025
- delinea-ss-features-2025
- delinea-ss-product-2025
- delinea-pm-product-2025
- delinea-home-2025
- delinea-ss-admin-2025

---

## 8. Open Questions for v1.0

1. **HSM certified partners:** Does Delinea publish a certified HSM interoperability list (Thales/SafeNet nShield, Entrust, Fortanix)? Not confirmed from public docs — SE conversation required.
2. **Secret Server Cloud AU region:** Is an AWS Sydney region planned or available under enterprise agreements? Critical for CPS 230/234 cloud edition deployments.
3. **IRAP assessment status:** Has Delinea completed or initiated an IRAP assessment for Secret Server Cloud or self-hosted? No public evidence found.
4. **Dynamic credentials roadmap:** Does the Delinea Platform roadmap (post-StrongDM acquisition) bring dynamic ephemeral cred generation into Secret Server, or only into DSV/StrongDM?
5. **FedRAMP / StateRAMP:** Secret Server Cloud FedRAMP authorisation status — not confirmed; relevant for XYZ government-adjacent workloads.
6. **Mainframe roadmap:** Any RACF/TSS integration planned or available via Professional Services? Not documented publicly.
7. **FAPI 2.0 / CDR alignment:** Any Open Banking credential workflow or CDR-specific template available? Not documented.
8. **PBA licensing:** Privileged Behaviour Analytics is referenced as an add-on — is it included in standard licensing or separately priced?
9. **Delinea Platform pricing model post-StrongDM:** How does the combined Delinea+StrongDM licensing affect XYZ's TCO for dynamic-access use cases?
10. **Session recording scope:** Does Session Recording (equivalent to CyberArk PSM) require a separate module license for Secret Server self-hosted?

# Vendor Profile — CyberArk Conjur

**Tier:** core
**Primary docs:** https://docs.cyberark.com/conjur-enterprise/
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

CyberArk (NASDAQ: CYBR) is a publicly listed identity-security company headquartered in Newton, MA and Petah Tikva, Israel. Conjur is its machine-secrets platform, distinct from the CyberArk PAM (Privileged Access Manager / Vault) product line. Three deployment options coexist as of May 2026: **Conjur Open Source** (LGPL v3, free, community-supported), **Conjur Enterprise / Secrets Manager Self-Hosted** (v13.7 as of Nov 2025, containerised on Docker/Podman, enterprise licence), and **Conjur Cloud / Secrets Manager SaaS** (multi-tenant SaaS with optional on-premises Followers). CyberArk has a significant XYZ presence (local pre-sales, post-sales, reseller channel) and completed IRAP assessment at Protected level for its Identity Security Platform. Primary differentiator: deep PAM ecosystem integration via Secrets Hub and Vault Synchronizer; strong Kubernetes/cloud-native authenticator breadth. [cyberark-conjur-overview-2025] [cyberark-irap-2025]

---

## 2. Architecture

**Storage backend:** PostgreSQL (streaming replication between Leader and Standbys). Secrets encrypted at rest using a master key; PKCS#11 HSM support for master-key protection (validated with Entrust nShield nShield 5c, FIPS 140-3). [entrust-conjur-hsm-2025]

**Deployment topology (Enterprise):** Leader → Standbys (synchronous replication, ≥2 for auto-failover) → Followers (asynchronous, read-only, deployed per region/cluster). Selective replication allows Followers to hold a subset of secrets, enabling data-segregation across geographies. Throughput scales linearly with Follower count ("shared-nothing" read tier). [cyberark-conjur-arch-2025]

**Auth methods (native):** authn (API key), authn-k8s (mTLS SPIFFE-aligned), authn-jwt (generic JWT/OIDC), authn-iam (AWS IAM), authn-azure, authn-gcp, authn-ldap, authn-oidc. Cloud variant also supports SPIFFE JWT-SVIDs for AI-agent workloads. [cyberark-conjur-authn-2025]

**Secrets types:** static variables (key/value), dynamic rotation via policy-annotated variables with ISO-8601 TTL, AWS dynamic secrets (GA in Cloud UI as of 2025). No dedicated PKI/cert issuance engine native to Conjur; PKI/TLS lifecycle is handled by the separate **CyberArk Certificate Manager** and **Zero Touch PKI** products. [cyberark-cert-mgr-2025]

**HSM/KMS:** PKCS#11 HSM for master-key encryption (Enterprise). Conjur Cloud uses cloud-managed KMS; no public BYOK/HYOK detail found. [entrust-conjur-hsm-2025]

**Replication/DR:** WAN Standbys supported for geographic DR; Follower auto-rebase via cluster load balancer. Regular evoke backup provides point-in-time recovery. [cyberark-conjur-ha-2025]

**Compliance posture:** FIPS 140-2 Level 1 (CyberArk Cryptographic Module, NIST CMVP cert 4377). SOC 2 Type II for SaaS products. FedRAMP High for select Identity Security Platform services (GovCloud region only). IRAP Protected (Workforce Identity; broader platform scope confirmed; specific Conjur Cloud AU region IRAP scope not separately published as of profile date). [cyberark-compliance-2025] [cyberark-fedramp-2025] [cyberark-irap-2025]

---

## 3. NHI coverage map

| NHI-ID | Description | Coverage | Maturity | Evidence |
|--------|-------------|----------|----------|----------|
| NHI-001 | Cloud IAM principal | NATIVE | 4 | authn-iam (AWS), authn-azure, authn-gcp GA authenticators [cyberark-conjur-authn-2025] |
| NHI-002 | Kubernetes ServiceAccount | NATIVE | 4 | authn-k8s (mTLS, SPIFFE-aligned) + authn-jwt K8s variant; Secrets Provider sidecar/init container [cyberark-k8s-authn-2025] |
| NHI-003 | CI/CD pipeline identity | NATIVE | 3 | authn-jwt supports GitHub Actions, GitLab CI, Jenkins OIDC tokens natively [cyberark-conjur-authn-2025] |
| NHI-004 | Container image-pull credential | ADD-ON | 2 | Secrets stored as variables; no dedicated ECR/ACR/GAR dynamic-token engine; requires application-side SDK fetch [INDUSTRY-CONSENSUS] |
| NHI-005 | Database service account | NATIVE | 3 | Policy-based rotation with TTL; Dual Accounts feature for zero-downtime rotation; AWS dynamic secrets GA [cyberark-rotation-2025] |
| NHI-006 | Application TLS / mTLS identity | PARTNER | 2 | No native X.509 issuance in Conjur; CyberArk Certificate Manager (separate product) covers TLS lifecycle [cyberark-cert-mgr-2025] |
| NHI-007 | Third-party SaaS API key | NATIVE | 3 | Static secret storage + rotation policy; no native OAuth token exchange engine [cyberark-rotation-2025] |
| NHI-008 | Git platform credential | NATIVE | 2 | Static variable storage + rotation; no native GitHub/GitLab-specific dynamic-token engine [INDUSTRY-CONSENSUS] |
| NHI-009 | IaC / config-mgmt agent | NATIVE | 3 | Terraform provider, Ansible integration, Summon CLI all documented [cyberark-conjur-overview-2025] |
| NHI-010 | Monitoring / observability agent | NATIVE | 2 | Static key vaulting + rotation; no vendor-specific Datadog/Splunk dynamic-token engines [INDUSTRY-CONSENSUS] |
| NHI-011 | Message broker / event-bus client | NATIVE | 2 | Static credential storage; rotation policy applicable; no native Kafka/RabbitMQ dynamic engine [INDUSTRY-CONSENSUS] |
| NHI-012 | AD / LDAP service account | NATIVE | 3 | authn-ldap GA; LDAP sync for policy population; password rotation via rotators [cyberark-ldap-2025] |
| NHI-013 | Reverse-proxy / API-gateway | ADD-ON | 2 | Secrets consumable via SDK/Summon; no native gateway-identity plugin [INDUSTRY-CONSENSUS] |
| NHI-014 | RPA bot identity | ADD-ON | 2 | PAM integration (Vault Synchronizer) covers RPA credential vaulting; Conjur alone: static storage [cyberark-secretshub-2025] |
| NHI-015 | Code-signing identity | GAP | 0 | No native code-signing or Sigstore integration documented [INDUSTRY-CONSENSUS] |
| NHI-016 | Build provenance / SLSA identity | GAP | 0 | No SLSA / in-toto integration documented [INDUSTRY-CONSENSUS] |
| NHI-017 | Service mesh control-plane identity | ADD-ON | 1 | authn-k8s aligns with SPIFFE; no native Istio/Linkerd CA integration documented [INDUSTRY-CONSENSUS] |
| NHI-018 | Confidential-computing / TEE identity | GAP | 0 | No TEE attestation-gated secret release documented for Conjur [INDUSTRY-CONSENSUS] |
| NHI-019 | AI agent / autonomous workflow | NATIVE | 3 | GA Nov 2025: CyberArk Secure AI Agents Solution; JWT-SVID SPIFFE auth for AI agent workloads [cyberark-ai-agents-2025] |
| NHI-020 | Model artifact / registry identity | GAP | 0 | No ML registry or model-signing integration documented [INDUSTRY-CONSENSUS] |
| NHI-021 | IoT / OT device identity | GAP | 1 | Generic secret storage possible; no EST/SCEP/DPS enrollment integration documented [INDUSTRY-CONSENSUS] |
| NHI-022 | Mainframe / midrange service identity | ADD-ON | 2 | Conjur described as capable of securing mainframe secrets; PAM integration covers RACF via CyberArk EPV; Conjur-direct z/OS docs thin [cyberark-mainframe-2025] |
| NHI-023 | Database encryption / TDE master key | ADD-ON | 2 | Variable storage for KMS CMK ARN / HSM partition creds; no native TDE-key lifecycle engine [INDUSTRY-CONSENSUS] |
| NHI-024 | HSM / KMS operator / break-glass | ADD-ON | 2 | PKCS#11 HSM integration for Conjur master key; break-glass via PAM integration; no standalone quorum-operator workflow in Conjur alone [entrust-conjur-hsm-2025] |
| NHI-025 | CA operator identity | PARTNER | 2 | CyberArk Certificate Manager + Zero Touch PKI (separate products) cover CA operator identity; not Conjur-native [cyberark-cert-mgr-2025] |
| NHI-026 | Backup / DR agent identity | ADD-ON | 2 | Credential storage + rotation applicable; no native Veeam/Commvault/Rubrik plugin documented for Conjur [INDUSTRY-CONSENSUS] |
| NHI-027 | Backend-for-frontend / OBO token | ADD-ON | 2 | authn-jwt covers client-credentials pattern; OBO/token-exchange requires app-layer logic [INDUSTRY-CONSENSUS] |
| NHI-028 | Federated B2B / Open Banking mTLS | PARTNER | 1 | FAPI 2.0 / CDR mTLS certs depend on CyberArk Certificate Manager; no Conjur-native CDR client-cert issuance [INDUSTRY-CONSENSUS] |
| NHI-029 | Service-account-as-human (shared ID) | ADD-ON | 2 | Static credential vaulting + rotation; access controls via policy RBAC; requires PAM for session recording [INDUSTRY-CONSENSUS] |
| NHI-030 | Browser / SaaS OAuth-app identity | GAP | 0 | No OAuth-app inventory or governance capability in Conjur [INDUSTRY-CONSENSUS] |
| NHI-031 | Webhook / inbound integration identity | ADD-ON | 1 | HMAC signing-secret storage only; no webhook-signature verification middleware [INDUSTRY-CONSENSUS] |
| NHI-032 | Network / infrastructure device identity | ADD-ON | 1 | Generic credential vaulting; no native TACACS+/RADIUS integration in Conjur (that lives in PAM) [INDUSTRY-CONSENSUS] |
| NHI-033 | Print / spooler / branch-peripheral | GAP | 0 | No documented integration for branch-peripheral credential management [INDUSTRY-CONSENSUS] |
| NHI-034 | Quantum-resistant / hybrid-PKI identity | GAP | 1 | CyberArk Certificate Manager roadmap mentions PQC; no Conjur-native PQC key-management documented [cyberark-cert-mgr-2025] |
| NHI-035 | Vault-internal / secrets-broker identity | NATIVE | 3 | Leader/Standby/Follower identities documented; replication tokens; auto-unseal via HSM PKCS#11 [cyberark-conjur-arch-2025] |
| NHI-036 | Ephemeral workload via SPIFFE/Aembit | NATIVE | 3 | JWT-SVID SPIFFE authentication GA for SaaS; authn-k8s mTLS SPIFFE-aligned for Enterprise [cyberark-ai-agents-2025] |
| NHI-037 | Forgotten / orphaned legacy identity | ADD-ON | 2 | Policy-based RBAC + audit trail; no dedicated dormancy-sweep / discovery engine native to Conjur [INDUSTRY-CONSENSUS] |

**NHI split:** NATIVE=17, ADD-ON=13, PARTNER=3, GAP=7, N/A=0

---

## 4. Use-case scoring

| UC-ID | Title | Coverage | Maturity | Evidence |
|-------|-------|----------|----------|----------|
| UC-F-001 | Prevent plaintext secrets in source repos | ADD-ON | 2 | No native scanner; Conjur stores secrets retrieved at runtime; pre-commit tooling is third-party [INDUSTRY-CONSENSUS] |
| UC-F-002 | Detect and remediate secrets in history | GAP | 0 | No historical-scan capability; requires GitGuardian/TruffleHog alongside Conjur [INDUSTRY-CONSENSUS] |
| UC-F-003 | JIT short-lived cloud credentials via OIDC | NATIVE | 4 | authn-iam, authn-azure, authn-gcp + authn-jwt/OIDC; JIT credential patterns supported [cyberark-conjur-authn-2025] |
| UC-F-004 | Workload-attested ephemeral identity (SPIFFE) | NATIVE | 3 | authn-k8s (SPIFFE-aligned mTLS) + JWT-SVID for AI agents (Nov 2025 GA) [cyberark-ai-agents-2025] |
| UC-F-005 | Dynamic database credentials with leases | NATIVE | 3 | Policy-based rotation with TTL; Dual Accounts zero-downtime rotation; AWS dynamic secrets GA [cyberark-rotation-2025] |
| UC-F-006 | Automated rotation of long-lived static secrets | NATIVE | 3 | ISO-8601 TTL rotation with retry logic; rotation failure alerting; Dual Accounts [cyberark-rotation-2025] |
| UC-F-007 | Immediate revocation on identity compromise | NATIVE | 3 | Policy revocation removes host access immediately; API-driven revocation; audit trail [cyberark-conjur-arch-2025] |
| UC-F-008 | Kubernetes secret consumption without on-disk plaintext | NATIVE | 4 | Secrets Provider (init container / sidecar), CSI driver, Summon; K8s Secrets mode documented [cyberark-k8s-authn-2025] |
| UC-F-009 | Container image-pull credentials per workload | ADD-ON | 2 | Pull-credential storage possible; no dynamic ECR/ACR/GAR short-lived-token engine native to Conjur [INDUSTRY-CONSENSUS] |
| UC-F-010 | IaC / config-mgmt secrets injected at apply-time | NATIVE | 3 | Terraform provider, Ansible lookup, Summon; tested with TFC/Enterprise [cyberark-conjur-overview-2025] |
| UC-F-011 | Observability-agent credentials rotated and scoped | NATIVE | 2 | Static key vaulting + rotation policy; no vendor-native Datadog/Splunk dynamic-token engine [INDUSTRY-CONSENSUS] |
| UC-F-012 | Message-broker client identity hardening | ADD-ON | 2 | Credential storage + rotation applicable; no native Kafka mTLS cert-issuance or SAS rotation engine [INDUSTRY-CONSENSUS] |
| UC-F-013 | gMSA / Kerberos modernisation for AD service accounts | ADD-ON | 2 | authn-ldap + LDAP sync covers AD credentials; no gMSA native integration [cyberark-ldap-2025] |
| UC-F-014 | API-gateway upstream identity standardised | ADD-ON | 2 | Credential storage for gateway secrets; no native Kong/Apigee plugin [INDUSTRY-CONSENSUS] |
| UC-F-015 | RPA bot credentials vaulted and session-bound | ADD-ON | 2 | Vault Synchronizer links PAM and Conjur for RPA workflows; Conjur alone: static vaulting [cyberark-secretshub-2025] |
| UC-F-016 | Keyless code- and artifact-signing in CI | GAP | 0 | No Sigstore/HSM code-signing integration in Conjur; CyberArk Certificate Manager required [cyberark-cert-mgr-2025] |
| UC-F-017 | TEE attestation gates secret release | GAP | 0 | No TEE attestation-gated pattern documented for Conjur as of May 2026 [INDUSTRY-CONSENSUS] |
| UC-F-018 | AI-agent / LLM tool-credential brokering | NATIVE | 3 | Secure AI Agents Solution GA Nov 2025; JWT-SVID SPIFFE auth; MCP Server connector [cyberark-ai-agents-2025] |
| UC-F-019 | IoT / OT / branch-device identity enrolment | GAP | 1 | Generic credential storage; no EST/SCEP/DPS enrollment module [INDUSTRY-CONSENSUS] |
| UC-F-020 | Mainframe / midrange credential rotation pipeline | ADD-ON | 2 | Conjur described for mainframe secrets; PAM integration for RACF; Conjur-direct z/OS pipeline thin [cyberark-mainframe-2025] |
| UC-F-021 | Backup / DR agent identity de-privileging | ADD-ON | 2 | Credential vaulting + rotation applicable; no native Veeam/Rubrik connector for Conjur [INDUSTRY-CONSENSUS] |
| UC-F-022 | Webhook inbound identity verification | GAP | 0 | HMAC-secret storage only; no webhook-signature middleware [INDUSTRY-CONSENSUS] |
| UC-F-023 | Network-device credential modernisation | ADD-ON | 1 | Generic vaulting possible; TACACS+/RADIUS integration lives in CyberArk PAM, not Conjur [INDUSTRY-CONSENSUS] |
| UC-F-024 | Open-Banking / FAPI 2.0 mTLS partner identity | PARTNER | 1 | Partner mTLS certs depend on Certificate Manager; Conjur stores client-cert private keys; no CDR-native workflow [INDUSTRY-CONSENSUS] |
| UC-F-025 | OAuth-app / marketplace integration governance | GAP | 0 | No OAuth-app inventory or governance capability native to Conjur [INDUSTRY-CONSENSUS] |
| UC-F-026 | Vault-internal identity hardening | NATIVE | 3 | Leader/Standby/Follower topology; PKCS#11 HSM unseal; replication tokens; backup/recovery documented [cyberark-conjur-ha-2025] |
| UC-F-027 | Orphaned / dormant NHI cleanup pipeline | ADD-ON | 2 | Policy RBAC audit trail; no native dormancy-detection or discovery sweep [INDUSTRY-CONSENSUS] |
| UC-N-001 | Real-time secret-sprawl KPI dashboard | ADD-ON | 2 | Audit + Reports service provides event stream; no dedicated secrets-sprawl-KPI dashboard in Conjur [cyberark-audit-siem-2025] |
| UC-N-002 | NHI inventory and ownership attestation | ADD-ON | 2 | Policy-as-code defines all hosts/groups; inventory derives from policy; no automated attestation workflow [cyberark-conjur-arch-2025] |
| UC-N-003 | Rotation-coverage and freshness KPIs | ADD-ON | 2 | Rotation events auditable; no out-of-box KPI dashboard for rotation coverage [INDUSTRY-CONSENSUS] |
| UC-N-004 | Regulator audit evidence pack | ADD-ON | 2 | Audit service exports events; SIEM integration (Splunk, QRadar, etc.); no one-click CPS 234 evidence pack [cyberark-audit-siem-2025] |
| UC-N-005 | Essential 8 / ZT control-area scorecard | ADD-ON | 1 | No native E8 / NIST ZT scorecard; requires GRC tooling integration [INDUSTRY-CONSENSUS] |
| UC-N-006 | Vendor / SaaS supply-chain risk attestation | GAP | 0 | No supply-chain risk scoring capability in Conjur [INDUSTRY-CONSENSUS] |
| UC-N-007 | Data-sovereignty and residency assurance | NATIVE | 3 | Selective Follower replication limits secrets per region; Conjur Cloud India region available; IRAP Protected (platform) [cyberark-conjur-ha-2025] [cyberark-irap-2025] |
| UC-N-008 | Engineer training and secure-coding adoption KPI | GAP | 0 | Training products exist (CyberArk University) but no training-completion KPI within Conjur product [INDUSTRY-CONSENSUS] |
| UC-N-009 | Exception register and risk-acceptance governance | GAP | 0 | No exception-register module in Conjur; requires GRC tooling [INDUSTRY-CONSENSUS] |
| UC-N-010 | Break-glass and quorum-operator governance | ADD-ON | 2 | Policy-based break-glass role with audit; PKCS#11 HSM quorum via hardware; no software M-of-N quorum native to Conjur [cyberark-conjur-arch-2025] |
| UC-N-011 | Post-incident reporting and identity-driven RCA | ADD-ON | 2 | Audit service + SIEM exports support IR; no native ATT&CK-mapped RCA template [cyberark-audit-siem-2025] |
| UC-N-012 | Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA or artifact-signing reporting capability [INDUSTRY-CONSENSUS] |
| UC-N-013 | Crypto-agility and post-quantum readiness reporting | GAP | 1 | CyberArk Certificate Manager mentions PQC roadmap; no Conjur-native crypto-inventory or PQC reporting [cyberark-cert-mgr-2025] |
| UC-N-014 | Vendor-evaluation matrix maintenance | N/A | 0 | Governance process, not a product capability [INDUSTRY-CONSENSUS] |
| UC-N-015 | Communications, change-comms and stakeholder cadence | N/A | 0 | Governance process, not a product capability [INDUSTRY-CONSENSUS] |
| UC-N-016 | IoT / OT / branch-fleet posture reporting | GAP | 0 | No IoT/OT fleet-posture reporting in Conjur [INDUSTRY-CONSENSUS] |
| UC-N-017 | Observability/telemetry secret-leak governance | ADD-ON | 1 | Audit stream monitors Conjur secret access; no log-scrubbing or telemetry-scanning capability [INDUSTRY-CONSENSUS] |
| UC-N-018 | Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE attestation assurance reporting [INDUSTRY-CONSENSUS] |
| UC-N-019 | AI-agent / autonomous-workflow KPI suite | NATIVE | 2 | Secure AI Agents Solution provides workload identity; KPI suite not yet at mature level as of Nov 2025 GA [cyberark-ai-agents-2025] |
| UC-N-020 | Mainframe / legacy posture and exception transparency | ADD-ON | 1 | Audit events available; no mainframe-posture dashboard native to Conjur [INDUSTRY-CONSENSUS] |

**UC split (functional):** NATIVE=9, ADD-ON=10, PARTNER=1, GAP=7, N/A=0
**UC split (non-functional):** NATIVE=2, ADD-ON=9, PARTNER=0, GAP=7, N/A=2
**UC total:** NATIVE=11, ADD-ON=19, PARTNER=1, GAP=14, N/A=2

---

## 5. Strengths and gaps

### Top 3 strengths

1. **Cloud-native authenticator breadth (NHI-001/002/003, UC-F-003/004/008).** Conjur ships GA authenticators for AWS IAM, Azure, GCP, Kubernetes (SPIFFE-aligned mTLS + JWT), generic OIDC/JWT, and LDAP. The authn-k8s Secrets Provider (init-container and sidecar) is a mature, widely-deployed pattern for secretless Kubernetes workloads. No comparable vendor has this breadth at parity maturity.

2. **PAM ecosystem integration via Secrets Hub and Vault Synchronizer (NHI-014/022/026, UC-F-015/020).** CyberArk's unique advantage is the ability to sync secrets from PAM Self-Hosted (EPV) to Conjur, or from Conjur to native cloud vaults (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), enabling hybrid-estate coverage without rip-and-replace. For an XYZ bank with legacy PAM estates, this is a decisive differentiator.

3. **Horizontal Follower scale + selective replication (NHI-035, UC-N-007, UC-F-026).** The Leader-Standby-Follower architecture scales read throughput linearly, supports geographic data-segregation via selective replication, and enables APRA CPS 230 data-residency controls. Conjur Cloud's India region (2025) and selective Follower deployment patterns address multi-cloud and sovereignty requirements.

### Top 3 gaps

1. **No native PKI / X.509 / cert-lifecycle engine in Conjur (NHI-006/015/025/034, UC-F-016/024, UC-N-013).** CyberArk's PKI capability (Certificate Manager, Zero Touch PKI) is a separate licensed product. Evaluators must budget for and integrate both products for NHI-006/025 coverage. This is a notable structural gap versus HashiCorp Vault (native PKI secrets engine).

2. **No secrets-sprawl detection or discovery (UC-F-001/002, UC-N-001/002).** Conjur has no pre-commit scanning, historical repo sweep, or CI-secret-detection capability. Organisations need a parallel tool (GitGuardian, TruffleHog, GitHub Advanced Security) for Cluster A use cases. The Secure AI Agents expansion does not address this gap.

3. **Thin non-functional / audit dashboarding (UC-N-003/004/005/009, UC-N-010).** The Audit & Reports service provides event streaming and SIEM integration but lacks out-of-box KPI dashboards, rotation-coverage reports, CPS 234 evidence packs, or exception registers. Customers build these on top of SIEM/GRC tooling, adding integration complexity. Vault Enterprise's native reporting is more comprehensive.

---

## 6. AU-specific notes

**IRAP Protected:** CyberArk has completed IRAP assessment at the Protected level for its Identity Security Platform. The specific product scope (whether Conjur Cloud SaaS is in scope for the AU IRAP report) was not separately published as of May 2026; evaluation teams should request the IRAP assessment report directly from CyberArk. [cyberark-irap-2025]

**APRA CPS 230 / CPS 234:** Selective Follower replication enables in-AU data residency for Conjur Enterprise. For Conjur Cloud, the AUS region availability should be confirmed with CyberArk pre-sales; India region is confirmed (2025 What's New). No explicit Sydney/Melbourne region announcement found as of profile date. [cyberark-conjur-whatsnew-2025]

**Essential 8:** Conjur supports E8 RestrictAdminPrivilege (machine identity scope) via RBAC policy, just-in-time secret issuance (authn-k8s, authn-jwt), and automated rotation. No native E8 maturity scorecard. Integration with ASD ISM controls is customer-built on top of audit stream.

**XYZ presence:** CyberArk has local offices (Sydney, Melbourne), active BFSI customer base in AU/NZ, and participation in AISA/ACSe forums. IRAP assessment signals government-sector readiness. [cyberark-irap-2025]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## CyberArk Conjur (Agent 03 wave 1)`.

Keys used: `cyberark-conjur-overview-2025`, `cyberark-conjur-arch-2025`, `cyberark-conjur-authn-2025`, `cyberark-k8s-authn-2025`, `cyberark-rotation-2025`, `cyberark-conjur-ha-2025`, `cyberark-cert-mgr-2025`, `cyberark-ai-agents-2025`, `cyberark-audit-siem-2025`, `cyberark-secretshub-2025`, `cyberark-ldap-2025`, `cyberark-mainframe-2025`, `cyberark-compliance-2025`, `cyberark-fedramp-2025`, `cyberark-irap-2025`, `cyberark-conjur-whatsnew-2025`, `entrust-conjur-hsm-2025`

---

## 8. Open questions for v1.0

1. **Conjur Cloud AU region:** Is there a Sydney/Melbourne region for Conjur Cloud SaaS? CyberArk What's New (2025) only confirms India expansion. Confirm with CyberArk AU pre-sales.
2. **IRAP scope:** Does the IRAP Protected assessment specifically cover Conjur Cloud SaaS, or only Workforce Identity components? Request the IRAP assessment report from CyberArk.
3. **Dynamic DB engine breadth:** AWS dynamic secrets are GA in Conjur Cloud; is Azure SQL / GCP Cloud SQL / PostgreSQL dynamic-credential issuance also available, or is this AWS-only? Primary-source URL not found.
4. **API quality 2026:** The user's 2024 assessment of "appalling, PAM-led philosophy" is partially rebutted: OpenAPI spec now published for both Conjur Cloud and OSS; authn API is REST-idiomatic. However, the policy DSL (YAML-based) retains complexity. An SE / demo session is needed to validate ergonomics for modern DevSecOps toolchains.
5. **Community access 2024→2026:** GitHub repos (cyberark/conjur, ~5k stars) are public; docs at docs.cyberark.com are open without login. Conjur Commons (Discourse) is open-registration. The Partner Portal friction noted in 2024 appears to have eased for OSS/community paths; Enterprise pricing and advanced docs still require a CyberArk sales engagement.
6. **Conjur OSS maintenance status 2026:** OSS v1.21.1 last tagged June 2024; Enterprise v13.7 Nov 2025. OSS release cadence has slowed relative to Enterprise — confirm whether OSS is in maintenance mode or still receiving feature parity.
7. **PKI integration depth:** What is the licensing and integration complexity for pairing Conjur Enterprise with CyberArk Certificate Manager + Zero Touch PKI for NHI-006/025 coverage? SE conversation required.
8. **Mainframe z/OS direct pipeline:** Is there a supported Conjur REST API integration from z/OS (CICS, batch) without routing through PAM EPV? Community forum references exist but primary-source docs are thin.

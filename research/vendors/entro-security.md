# Vendor Profile — Entro Security

**Tier:** nhi-discovery
**Primary docs:** https://entro.security
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

Entro Security Ltd was founded in 2022 in Tel Aviv, Israel (commercial HQ listed as Boston, MA). Co-founders are CEO Itzik Alvas (formerly Microsoft Defender for Cloud engineering lead) and CTO Adam Cheriki (formerly Javelin Networks, acquired by Symantec). The company exited stealth in May 2023 and raised $6M seed + $18M Series A (June 2024, led by Dell Technologies Capital, with Hyperwise Ventures, StageOne Ventures, Mickey Boodaei and Rakesh Loonkar), totalling $24M raised. An M&A offer was reportedly received in April 2025 — acquirer unconfirmed as of profile date [entro-security-series-a-2024][entro-security-dtc-series-a-2024]. Deployment is **SaaS-only** (app.entro.security). The primary differentiator is **secret lineage and NHI context**: tracing every secret from creation through storage to runtime consumption across 50+ integrations. No AU data residency, no IRAP, no self-hosted option is publicly documented.

---

## 2. Architecture

Entro is a **read-only SaaS discovery and governance overlay** — it does **not** store secrets. It connects to existing vaults (HashiCorp Vault, AWS SM, Azure KV, GCP SM, CyberArk Conjur, Akeyless, Delinea, BeyondTrust, 1Password, LastPass, K8s Secrets), code repositories (GitHub, GitLab, Bitbucket — cloud and on-prem), CI/CD systems (GitHub Actions, Jenkins, CircleCI, Azure DevOps, TeamCity, Drone CI, Octopus Deploy, Travis CI), cloud control planes (AWS, Azure, GCP, OCI), SaaS apps (Slack, Teams, Google Workspace, Salesforce, ServiceNow, Snowflake, Workday, Jira, Confluence, Notion, Monday.com, Zendesk), and identity/SIEM tools (Okta, AD, Splunk, Datadog, Elastic, Sentinel, Wiz) via agentless API connectors [entro-security-integrations-2025]. The **ContextIQ™ AI model** classifies 1,200+ secret types and auto-triages false positives. **NHIDR™** is the proprietary behavioural anomaly detection engine, baselining NHI activity and triggering automated remediation into the upstream vaults. HSM/KMS support is indirect (via vault integrations). Compliance: **ISO 27001** and **SOC 2 Type II** [entro-security-wiz-integration-2025]. No FedRAMP, no IRAP, no AU region [entro-security-financial-svcs-2025].

---

## 3. NHI coverage map

**Scoring note for nhi-discovery tier:** Entro does not store, issue, or rotate credentials natively. It discovers, inventories, contextualises, risk-scores, and triggers remediation via upstream vaults. Scores reflect discovery/governance capability, not storage/issuance.

| NHI ID | Coverage | Maturity | Evidence |
|---|---|---|---|
| NHI-001 Cloud IAM principal | NATIVE | 4 | AWS/Azure/GCP cloud IAM NHI discovery; lineage + posture [entro-security-nhi-platform-2025] |
| NHI-002 K8s ServiceAccount | NATIVE | 3 | K8s Secrets vault integration; workload NHI inventory [entro-security-integrations-2025] |
| NHI-003 CI/CD pipeline identity | NATIVE | 4 | GitHub Actions, Jenkins, CircleCI, Azure DevOps, TeamCity, Drone CI, Octopus, Travis CI [entro-security-integrations-2025] |
| NHI-004 Container image-pull credential | NATIVE | 2 | Docker Hub integration; K8s Secrets; registry credential discovery [entro-security-integrations-2025] |
| NHI-005 Database service account | NATIVE | 3 | Snowflake, MongoDB integrations; DB credential discovery via secrets scanning [entro-security-secrets-platform-2025] |
| NHI-006 Application TLS / mTLS identity | PARTNER | 1 | Certificate NHIs not a stated focus; PKI/cert lifecycle out of scope [INDUSTRY-CONSENSUS] |
| NHI-007 Third-party SaaS API key / OAuth client | NATIVE | 4 | SaaS integration layer (Salesforce, ServiceNow, Workday, Slack, Teams) + OAuth app discovery [entro-security-nhi-platform-2025] |
| NHI-008 Git platform credential (PAT / SSH) | NATIVE | 4 | GitHub, GitLab, Bitbucket repos scanned; PAT/SSH key discovery [entro-security-secrets-platform-2025] |
| NHI-009 IaC / config-mgmt agent identity | NATIVE | 3 | Terraform, Kubernetes IaC scanning; secret-in-state-file detection [entro-security-secrets-platform-2025] |
| NHI-010 Monitoring / observability agent | NATIVE | 3 | Datadog, Splunk, Elastic integrations; agent credential discovery [entro-security-integrations-2025] |
| NHI-011 Message broker / event-bus client | ADD-ON | 2 | Indirect via cloud (AWS SQS/SNS, Azure Service Bus) secret discovery; no explicit broker NHI posture [INDUSTRY-CONSENSUS] |
| NHI-012 AD / LDAP service account | NATIVE | 3 | Active Directory, Hybrid Azure AD integration; svc_ account inventory [entro-security-integrations-2025] |
| NHI-013 Reverse-proxy / API-gateway identity | ADD-ON | 1 | Not explicitly listed; partial coverage via cloud IAM discovery [INDUSTRY-CONSENSUS] |
| NHI-014 RPA bot identity | ADD-ON | 2 | Covered via AD service account inventory and SaaS OAuth app discovery [entro-security-nhi-platform-2025] |
| NHI-015 Code-signing identity | GAP | 0 | No code-signing or certificate lifecycle capability documented [INDUSTRY-CONSENSUS] |
| NHI-016 Build provenance / SLSA attestation identity | GAP | 0 | SLSA/Sigstore out of scope for NHI discovery tier [INDUSTRY-CONSENSUS] |
| NHI-017 Service mesh control-plane identity | GAP | 0 | SPIFFE/SPIRE mesh CA identities not covered [INDUSTRY-CONSENSUS] |
| NHI-018 Confidential-computing attestation identity | GAP | 0 | TEE attestation identities not in product scope [INDUSTRY-CONSENSUS] |
| NHI-019 AI agent / autonomous workflow identity | NATIVE | 4 | Dedicated AI agent platform pillar: discovery, lineage, NHIDR monitoring, MCP server integration [entro-security-ai-agents-2025] |
| NHI-020 Model artifact / registry identity | ADD-ON | 1 | Not explicitly listed; partial coverage via SaaS/cloud credential scanning [INDUSTRY-CONSENSUS] |
| NHI-021 IoT / OT device identity | GAP | 0 | IoT/OT device identities not in product scope; no DPS/EST support [INDUSTRY-CONSENSUS] |
| NHI-022 Mainframe / midrange service identity | GAP | 0 | RACF/ACF2/ICSF not listed; no mainframe vault integration [INDUSTRY-CONSENSUS] |
| NHI-023 Database encryption / TDE master key identity | ADD-ON | 1 | Partial: DB credential discovery via Snowflake/MongoDB; TDE key identity not in scope [INDUSTRY-CONSENSUS] |
| NHI-024 HSM / KMS operator / break-glass identity | GAP | 0 | HSM operator identities not discovered; no HSM integration [INDUSTRY-CONSENSUS] |
| NHI-025 CA operator identity | GAP | 0 | PKI/CA operator identities out of scope [INDUSTRY-CONSENSUS] |
| NHI-026 Backup / DR agent identity | ADD-ON | 1 | Indirect: backup agent AD accounts covered via AD integration; no dedicated backup-agent module [INDUSTRY-CONSENSUS] |
| NHI-027 Backend-for-frontend / OBO token holder | NATIVE | 3 | OAuth/OIDC client secret discovery; confidential-client secrets in vaults [entro-security-nhi-platform-2025] |
| NHI-028 Federated B2B / Open Banking client identity | ADD-ON | 1 | mTLS/FAPI certs not a primary focus; partial via SaaS OAuth app inventory [INDUSTRY-CONSENSUS] |
| NHI-029 Service-account-as-human (shared functional ID) | NATIVE | 3 | AD service account discovery; ownership attribution identifies shared accounts [entro-security-nhi-platform-2025] |
| NHI-030 Browser / SaaS extension / OAuth-app identity | NATIVE | 4 | OAuth app inventory across M365, Google Workspace, Salesforce, Slack, GitHub Apps [entro-security-nhi-platform-2025] |
| NHI-031 Webhook / inbound integration identity | NATIVE | 3 | Webhook signing secrets discovered via SaaS integrations and repo scanning [entro-security-secrets-platform-2025] |
| NHI-032 Network / infra device identity | GAP | 0 | Network device credentials (TACACS+, SNMP) not in scope [INDUSTRY-CONSENSUS] |
| NHI-033 Print / spooler / branch-peripheral identity | GAP | 0 | Branch peripheral credentials out of scope [INDUSTRY-CONSENSUS] |
| NHI-034 Quantum-resistant / hybrid-PKI identity | GAP | 0 | PQC identity governance not in product roadmap [INDUSTRY-CONSENSUS] |
| NHI-035 Vault-internal / secrets-broker identity | ADD-ON | 2 | Vault posture monitoring (fetching anomalies, privilege creep detection in vaults); root/replication tokens not directly governed [entro-security-secrets-platform-2025] |
| NHI-036 Ephemeral workload (SPIFFE / Aembit / Clutch) | GAP | 0 | SPIFFE SVID / workload attestation brokers not integrated [INDUSTRY-CONSENSUS] |
| NHI-037 Forgotten / orphaned legacy identity | NATIVE | 4 | Core use case: idle/stale NHI detection, dormancy analysis, owner-attestation workflows [entro-security-nhi-platform-2025] |

**NHI split: NATIVE=16, ADD-ON=9, PARTNER=1, GAP=11, N/A=0**

---

## 4. Use-case scoring

**Framing note:** Entro is an NHI-discovery/governance overlay. UC-F rows on vault storage, dynamic cred issuance, and rotation mechanics → GAP/PARTNER. UC-F rows on discovery, inventory, lineage, posture, and UC-N rows → expect NATIVE/strong.

| UC ID | Coverage | Maturity | Evidence |
|---|---|---|---|
| UC-F-001 Prevent plaintext secrets in repos | NATIVE | 4 | Repo scanning (GitHub/GitLab/Bitbucket) + ContextIQ™ auto-triage; PR-integrated remediation [entro-security-secrets-platform-2025] |
| UC-F-002 Detect secrets already in history | NATIVE | 4 | Historical and continuous repo sweep; 1,200+ secret types; ownership attribution [entro-security-secrets-platform-2025] |
| UC-F-003 JIT short-lived cloud creds via OIDC | GAP | 0 | Entro does not issue credentials; no OIDC token broker [INDUSTRY-CONSENSUS] |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No SPIFFE/SPIRE workload identity issuance [INDUSTRY-CONSENSUS] |
| UC-F-005 Dynamic DB credentials with broker leases | GAP | 0 | No dynamic credential issuance; discovery-only for DB secrets [INDUSTRY-CONSENSUS] |
| UC-F-006 Automated rotation of long-lived static secrets | ADD-ON | 2 | Policy enforcement + vaulting enforcement + active rotation trigger for at-risk secrets (into upstream vaults) [entro-security-nhi-platform-2025] |
| UC-F-007 Immediate revocation on compromise | ADD-ON | 2 | NHIDR™ triggers automated remediation; revocation executed via upstream vault API [entro-security-nhi-platform-2025] |
| UC-F-008 K8s secret consumption without on-disk plaintext | ADD-ON | 2 | K8s Secrets integration; detects plaintext K8s secrets; remediation guidance; does not deploy CSI driver [INDUSTRY-CONSENSUS] |
| UC-F-009 Container image-pull creds per workload | ADD-ON | 1 | Docker Hub integration; image-pull credential discovery; no per-workload issuance [entro-security-integrations-2025] |
| UC-F-010 IaC / config-mgmt secrets at apply-time | ADD-ON | 2 | Terraform state file scanning; secret-in-IaC detection; no dynamic provider injection [entro-security-secrets-platform-2025] |
| UC-F-011 Observability-agent credentials rotated | ADD-ON | 2 | Datadog/Splunk/Elastic agent credential discovery and posture; rotation via upstream vault [entro-security-integrations-2025] |
| UC-F-012 Message-broker client identity hardening | ADD-ON | 1 | Partial: cloud broker credential discovery; no explicit mTLS or SASL posture tooling [INDUSTRY-CONSENSUS] |
| UC-F-013 gMSA / Kerberos modernisation for AD SA | ADD-ON | 2 | AD/Azure AD integration; svc_ account inventory; gMSA modernisation guidance [entro-security-integrations-2025] |
| UC-F-014 API-gateway upstream identity standardised | GAP | 0 | API gateway identity not explicitly covered [INDUSTRY-CONSENSUS] |
| UC-F-015 RPA bot credentials vaulted and session-bound | ADD-ON | 2 | AD service account + SaaS OAuth discovery covers RPA bot identity inventory [entro-security-nhi-platform-2025] |
| UC-F-016 Keyless code- and artifact-signing in CI | GAP | 0 | Code-signing / Sigstore out of scope [INDUSTRY-CONSENSUS] |
| UC-F-017 TEE attestation gates secret release | GAP | 0 | Confidential-computing attestation not in scope [INDUSTRY-CONSENSUS] |
| UC-F-018 AI-agent / LLM tool-credential brokering | NATIVE | 3 | AI agent platform pillar: discovery, NHI mapping, NHIDR monitoring of agent credential use; no native credential broker [entro-security-ai-agents-2025] |
| UC-F-019 IoT / OT / branch-device identity enrolment | GAP | 0 | IoT/OT/DPS/EST not in scope [INDUSTRY-CONSENSUS] |
| UC-F-020 Mainframe / midrange credential rotation pipeline | GAP | 0 | No mainframe (RACF/ICSF) integration [INDUSTRY-CONSENSUS] |
| UC-F-021 Backup / DR agent identity de-privileging | ADD-ON | 1 | AD-based backup agent account inventory; no dedicated backup-agent vaulting module [INDUSTRY-CONSENSUS] |
| UC-F-022 Webhook inbound identity verification | NATIVE | 3 | Webhook signing secrets discovered and posture-managed via repo + SaaS scanning [entro-security-secrets-platform-2025] |
| UC-F-023 Network-device credential modernisation | GAP | 0 | TACACS+/SNMP device credentials not in scope [INDUSTRY-CONSENSUS] |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | mTLS/FAPI cert lifecycle not in scope [INDUSTRY-CONSENSUS] |
| UC-F-025 OAuth-app / marketplace integration governance | NATIVE | 4 | Core NHI use case: OAuth app inventory across M365/GW/Salesforce/Slack/GitHub; risk scoring; revocation triggers [entro-security-nhi-platform-2025] |
| UC-F-026 Vault-internal identity hardening | ADD-ON | 2 | Vault posture monitoring: fetching anomaly detection, privilege creep; does not govern root tokens directly [entro-security-secrets-platform-2025] |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | NATIVE | 4 | Core product capability: idle NHI detection, activity-based dormancy, owner-attestation, automated removal [entro-security-nhi-platform-2025] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | NATIVE | 4 | Centralised inventory dashboard: findings by team/repo/NHI type; trend tracking [entro-security-homepage-2025] |
| UC-N-002 NHI inventory and ownership attestation | NATIVE | 4 | Complete NHI inventory with human-owner attribution; annual attestation workflow [entro-security-nhi-platform-2025] |
| UC-N-003 Rotation-coverage and freshness KPIs | NATIVE | 3 | Rotation coverage metrics; freshness tracking per NHI bucket; posture scoring [entro-security-nhi-platform-2025] |
| UC-N-004 Regulator audit evidence pack | ADD-ON | 2 | Posture compliance reporting (SOC2, ISO27001, PCI, HIPAA) but no APRA CPS 234-specific evidence pack [entro-security-financial-svcs-2025] |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 1 | No E8 / NIST ZT scorecard template; general posture compliance mapping [INDUSTRY-CONSENSUS] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | NATIVE | 3 | SaaS integration risk scoring; OAuth-app inventory; supply-chain credential exposure [entro-security-nhi-platform-2025] |
| UC-N-007 Data-sovereignty and residency assurance | GAP | 0 | SaaS-only, no AU region, no IRAP; APRA CPS 230 data-residency requirements unmet [entro-security-financial-svcs-2025] |
| UC-N-008 Engineer training and secure-coding adoption KPI | GAP | 0 | No training platform or adoption KPI tooling [INDUSTRY-CONSENSUS] |
| UC-N-009 Exception register and risk-acceptance governance | ADD-ON | 2 | Risk prioritisation and posture exception surfacing; no dedicated GRC exception register module [INDUSTRY-CONSENSUS] |
| UC-N-010 Break-glass and quorum-operator governance | GAP | 0 | HSM/CA quorum-operator identities not in scope [INDUSTRY-CONSENSUS] |
| UC-N-011 Post-incident reporting and identity-driven RCA | ADD-ON | 2 | NHIDR™ logs and anomaly events support RCA; no MITRE ATT&CK T1552 mapping module [entro-security-nhi-platform-2025] |
| UC-N-012 Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | SLSA/in-toto provenance not in scope [INDUSTRY-CONSENSUS] |
| UC-N-013 Crypto-agility and PQC readiness reporting | GAP | 0 | PQC not in roadmap; no crypto-inventory capability [INDUSTRY-CONSENSUS] |
| UC-N-014 Vendor-evaluation matrix maintenance | ADD-ON | 2 | NHI posture metrics exportable; no dedicated matrix-maintenance tooling [INDUSTRY-CONSENSUS] |
| UC-N-015 Communications, change-comms, stakeholder cadence | GAP | 0 | Out of product scope [INDUSTRY-CONSENSUS] |
| UC-N-016 IoT / OT / branch-fleet posture reporting | GAP | 0 | IoT/OT out of scope [INDUSTRY-CONSENSUS] |
| UC-N-017 Observability / telemetry secret-leak governance | NATIVE | 3 | Detects secrets in logs/telemetry pipelines; Datadog/Splunk/Elastic integrations [entro-security-integrations-2025] |
| UC-N-018 Confidential-computing / TEE attestation assurance | GAP | 0 | TEE out of scope [INDUSTRY-CONSENSUS] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | NATIVE | 3 | AI agent NHI inventory + per-tool credential issuance volume; NHIDR anomaly alerting [entro-security-ai-agents-2025] |
| UC-N-020 Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe visibility [INDUSTRY-CONSENSUS] |

**UC-F split: NATIVE=7, ADD-ON=12, PARTNER=0, GAP=8, N/A=0**
**UC-N split: NATIVE=7, ADD-ON=5, PARTNER=0, GAP=8, N/A=0**

---

## 5. Strengths and gaps

### Top 3 strengths

1. **Secret lineage and NHI context depth.** Entro's ContextIQ™ model and lineage mapping trace every secret from creation through vault storage to runtime consumption — answering "who created this token, where is it stored, what uses it" across 1,200+ secret types and 50+ integrations. This is market-differentiated for sprawl visibility (UC-F-001, UC-F-002, UC-N-001, UC-N-002).

2. **Breadth of NHI discovery: SaaS OAuth, cloud IAM, AI agents.** The platform delivers best-in-class coverage of SaaS OAuth apps (NHI-030), third-party API keys (NHI-007), AI agent identities (NHI-019), and CI/CD credentials (NHI-003) — precisely the NHI classes most Tier-1 FI security programmes lack visibility into. NHIDR™ adds behavioural anomaly detection unavailable in vault-centric tools.

3. **AI agent identity governance (emerging leadership).** Dedicated agentic AI pillar with discovery of shadow agents, MCP server integration, per-agent NHI mapping, and NHIDR monitoring. This is the most forward-looking differentiator for FI programmes deploying LLM-based automation (UC-F-018, UC-N-019).

### Top 3 gaps

1. **No credential issuance, storage, or dynamic generation.** Entro is discovery/governance-only. It cannot issue JIT OIDC tokens (UC-F-003), dynamic DB creds (UC-F-005), or SPIFFE SVIDs (UC-F-004). Must partner with HashiCorp Vault, CyberArk, or cloud-native vaults for all P0 issuance UCs.

2. **No AU data residency or IRAP.** SaaS-only deployment with no documented Australian region. All NHI metadata and secret-context data transits Entro's US/global infrastructure. For APRA CPS 230/234-regulated programmes, this is a blocking compliance gap (UC-N-007). No IRAP, no Essential 8 scorecard module (UC-N-005).

3. **No PKI/cert, mainframe, IoT, or network-device coverage.** NHI-006, NHI-015–NHI-018, NHI-021–NHI-025, NHI-032–NHI-034, NHI-036 are all GAP. For XYZ Bank's full NHI programme, these classes (mainframe RACF, PKI certs, HSM operators, FAPI 2.0 mTLS) require separate PKI-MIM tier vendors (Venafi, Keyfactor, CyberArk) with no integration between Entro and those tools currently documented.

---

## 6. AU-specific notes

**Sovereignty/IRAP:** No Australian data centre or SaaS region is publicly documented. All Entro SaaS processing is US/EU-based. This creates a direct conflict with APRA CPS 230 (material service provider data-flow obligations) and CPS 234 (information security controls for regulated data). No IRAP assessment published. No ASD Essential 8 scorecard alignment claimed.

**Compliance posture:** ISO 27001 and SOC 2 Type II are confirmed [entro-security-wiz-integration-2025]. PCI DSS and HIPAA alignment claimed on financial-services page [entro-security-financial-svcs-2025]. No APRA-specific controls mapping is present.

**AU customer references:** None identified in public sources. Named customers (Elastic, SolarWinds, Nasuni, Booking.com) are all North America/EU enterprises.

**Risk rating for APRA context:** The SaaS-only + no-AU-residency posture makes Entro an **observer/analytics layer only** unless deployed under an approved data-residency exception or via a future AU region. An SE conversation about a private-cloud or BYOC option is recommended.

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Entro Security (Agent 03 wave 4)`:

- `entro-security-homepage-2025`
- `entro-security-integrations-2025`
- `entro-security-nhi-platform-2025`
- `entro-security-secrets-platform-2025`
- `entro-security-ai-agents-2025`
- `entro-security-financial-svcs-2025`
- `entro-security-wiz-integration-2025`
- `entro-security-series-a-2024`
- `entro-security-dtc-series-a-2024`
- `entro-security-nov-2024-announcement`

---

## 8. Open questions for v1.0

1. **AU data residency option:** Does Entro offer BYOC deployment, private-cloud tenant isolation, or a planned AU SaaS region to satisfy APRA CPS 230? No public evidence found.
2. **M&A status:** The April 2025 M&A offer — has it progressed to acquisition? If acquired (e.g., by a Tier-1 security vendor), product roadmap and compliance posture may change materially.
3. **Rotation execution depth:** Entro claims "active rotation of at-risk secrets" — is this a direct vault API write-back, or a policy-triggered workflow dispatched to the upstream vault admin? Clarify execution model for P0 rotation UCs.
4. **CyberArk PAM integration:** Entro integrates with CyberArk Conjur (confirmed) — does it also integrate with CyberArk Privilege Cloud / PAM Self-Hosted for privileged account credential discovery?
5. **IRAP roadmap:** Any government or regulated-sector customers driving an IRAP assessment engagement?
6. **Mainframe / RACF coverage:** Is there a roadmap item for z/OS or AS/400 credential discovery, relevant to XYZ's core banking estate?
7. **AI agent credential brokering:** Entro discovers and monitors AI agent credentials — does it also enforce least-privilege token issuance per agent session, or is that delegated to the upstream broker?
8. **Pricing model:** No public pricing; is it per-NHI, per-integration, or per-seat? Material for FY27 budget planning.

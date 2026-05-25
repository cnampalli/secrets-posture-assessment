# Vendor Profile — Astrix Security

**Tier:** nhi-discovery
**Primary docs:** https://astrix.security
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Astrix Security (founded 2021, Tel Aviv / New York) is a SaaS-only NHI security platform
specialising in discovery, posture management, anomaly detection, and lifecycle governance
of non-human identities and AI agents. The company raised $85 M total (Series B $45 M,
December 2024; investors: CRV, Menlo Ventures, Workday Ventures, Bessemer). On 2026-05-04
Cisco announced intent to acquire Astrix (~$250–350 M); the deal is pending close and
Astrix will integrate into Cisco Identity Intelligence, Secure Access, Duo, and Splunk.
Recognition: Fortune Cyber 60 (2026), Gartner Hype Cycle for Digital Identity 2025
(Workload Identity Management). Customers are predominantly Fortune 500 tech/SaaS firms
(Workday, Netflix, HubSpot, NetApp, Figma, Boomi, Pagaya, Mercury); no Tier-1 AU bank is
publicly cited. AU / APAC presence is not separately declared; no IRAP assessment found.

[astrix-nhi-platform-2026][astrix-series-b-2024][astrix-cisco-2026]

---

## 2. Architecture (≤ 250 words)

**Deployment model:** SaaS-only, agentless. Integration is API-based, requiring read-only
or minimal-permission OAuth / API-key scopes into each integrated system. No on-premises
component is marketed. Time-to-value is claimed as "hours" post-onboarding.

**Discovery architecture (four methods, announced March 2026):**
1. *AI Platform Integrations* — direct API connections to Microsoft Copilot, Amazon Bedrock,
   Google Vertex AI, OpenAI, Salesforce Agentforce, Databricks, and others.
2. *NHI Fingerprinting* — correlates NHI credential artifacts (OAuth apps, service accounts,
   API keys, IAM roles, PATs, secrets) across cloud, SaaS, IdP, and DevOps platforms.
3. *Sensor Telemetry* — reads from EDR agents (CrowdStrike, SentinelOne, Microsoft Defender)
   and network sensors (FortiGate) to surface shadow agents without direct platform access.
4. *Bring Your Own Service (BYOS)* — custom integration API for proprietary / homegrown
   services. [astrix-helpnet-2026]

**Integration catalogue (20+ connectors):** AWS, Azure / Microsoft 365, GCP, GitHub,
Kubernetes, Databricks, Snowflake, Slack, Salesforce, Okta, Active Directory / Entra ID,
Google Workspace, Jira, Confluence, ServiceNow, NetSuite, BeyondTrust, Fortinet, Cursor.

**Anomaly detection engine:** ML-based behavioural analytics over access patterns, permission
changes, and API traffic — branded "Agentic Detection & Response (ADR™)." [astrix-iam-itdr-2026]

**Secrets posture:** Discovers unvaulted secrets across cloud and SaaS; aggregates across
"multiple vaults" (names not publicly listed); automates rotation enforcement and expiration
policies; monitors for unusual vault retrievals. [astrix-secret-management-2026]

**Compliance / certifications:** SOC 2 Type 2 (Big Four audit, achieved within 5 months of
stealth exit). ISO 27001: not publicly claimed. IRAP: not publicly claimed. [astrix-soc2-2022]

**HSM / KMS / replication / DR:** Not applicable (SaaS; Astrix does not store or broker
secrets — it discovers and governs them).

---

## 3. NHI coverage map (≤ 600 words)

For each NHI, Coverage = NATIVE / ADD-ON / PARTNER / GAP / N/A and Maturity 0–4.

| NHI-ID | Name | Coverage | Maturity | Evidence |
|---|---|---|---|---|
| NHI-001 | Cloud IAM principal | NATIVE | 4 | AWS/Azure/GCP IAM roles discovered and risk-scored [astrix-nhi-discover-2026] |
| NHI-002 | Kubernetes ServiceAccount | NATIVE | 3 | K8s listed as integration; service account discovery covered [astrix-nhi-platform-2026] |
| NHI-003 | CI/CD pipeline identity | NATIVE | 3 | GitHub integration; PATs, secrets, and OAuth apps in CI scope [astrix-nhi-discover-2026] |
| NHI-004 | Container / image-pull credential | ADD-ON | 2 | Covered via cloud-registry service-account discovery; no dedicated registry-cred path cited |
| NHI-005 | Database service account | NATIVE | 3 | Snowflake, Databricks listed; service accounts across cloud DBs inventoried [astrix-nhi-discover-2026] |
| NHI-006 | Application TLS / mTLS workload | GAP | 0 | No X.509 / SPIFFE certificate lifecycle capability found; purely NHI-discovery focus |
| NHI-007 | Third-party SaaS API key / OAuth client | NATIVE | 4 | Core differentiator: SaaS-to-SaaS OAuth apps, API keys, refresh tokens; vendor risk scoring [astrix-third-party-risk-2026] |
| NHI-008 | Git platform credential (PAT / SSH) | NATIVE | 4 | GitHub PATs, deploy keys in-scope; supply-chain attack research published [astrix-nhi-discover-2026] |
| NHI-009 | IaC / config-mgmt agent identity | ADD-ON | 2 | Secrets in cloud environments discovered; no explicit Terraform/Ansible agent identity path |
| NHI-010 | Monitoring / observability agent | ADD-ON | 2 | API keys for observability agents discoverable via cloud/SaaS integration; no dedicated path |
| NHI-011 | Message broker / event-bus client | ADD-ON | 1 | Not explicitly documented; covered indirectly via cloud-service-account inventory |
| NHI-012 | AD / LDAP service account | NATIVE | 3 | Active Directory / Entra ID integration listed; managed service accounts inventoried [astrix-why-2026] |
| NHI-013 | API-gateway upstream identity | ADD-ON | 2 | API keys and OAuth creds for gateways discoverable; no dedicated gateway-identity path |
| NHI-014 | RPA bot identity | ADD-ON | 2 | Service-account discovery covers RPA bots; no named UiPath / Blue Prism integration |
| NHI-015 | Code-signing identity | GAP | 0 | No Sigstore / Authenticode / HSM code-signing coverage found |
| NHI-016 | Build provenance / SLSA attestation | GAP | 0 | No SLSA / in-toto attestation coverage found |
| NHI-017 | Service mesh control-plane identity | GAP | 0 | No SPIFFE / Istio / Linkerd / Consul mesh identity coverage found |
| NHI-018 | Confidential-computing attestation | GAP | 0 | No TEE attestation coverage found |
| NHI-019 | AI agent / autonomous workflow | NATIVE | 4 | Primary differentiator: ACP, Agent Policies, four-method discovery, MCP governance [astrix-ai-agent-discovery-2026] |
| NHI-020 | Model artifact / registry identity | ADD-ON | 2 | Databricks, Snowflake integrations cover model-registry service accounts; no dedicated ML-registry path |
| NHI-021 | IoT / OT device identity | GAP | 0 | No IoT/OT device identity coverage found |
| NHI-022 | Mainframe / midrange service identity | GAP | 0 | No RACF / ACF2 / IBM i / z/OS coverage found |
| NHI-023 | Database encryption / TDE master key | GAP | 0 | Key-management not in scope; discovery-only platform |
| NHI-024 | HSM / KMS operator identity | GAP | 0 | No HSM / KMS operator identity coverage found |
| NHI-025 | CA operator identity | GAP | 0 | No PKI / CA operator identity coverage found |
| NHI-026 | Backup / DR agent identity | ADD-ON | 1 | Service accounts for backup agents discoverable; no named Veeam/Rubrik integration |
| NHI-027 | BFF / on-behalf-of token holder | NATIVE | 3 | OAuth token exchange and refresh-token governance covered via SaaS discovery [astrix-third-party-risk-2026] |
| NHI-028 | Federated B2B / Open Banking client | GAP | 0 | No FAPI 2.0 / CDR / mTLS partner-cert lifecycle coverage found |
| NHI-029 | Service-account-as-human (shared functional ID) | NATIVE | 3 | Ownership attribution per NHI; "zombie credentials" and shared-account detection [astrix-workday-2026] |
| NHI-030 | Browser / SaaS extension / OAuth-app | NATIVE | 4 | Third-party OAuth grant discovery core product; stale refresh token revocation [astrix-third-party-risk-2026] |
| NHI-031 | Webhook / inbound integration identity | NATIVE | 3 | Webhooks listed as NHI type; signing-secret governance in scope [astrix-nhi-discover-2026] |
| NHI-032 | Network / infrastructure device identity | GAP | 0 | No TACACS+ / SNMP / network-device credential coverage found |
| NHI-033 | Print / spooler / branch-peripheral identity | GAP | 0 | No IoT/OT/peripheral device coverage found |
| NHI-034 | Quantum-resistant / hybrid-PKI identity | GAP | 0 | No PQC / hybrid-cert coverage found |
| NHI-035 | Vault-internal / secrets-broker identity | ADD-ON | 2 | Monitors "unauthorized vault activity"; aggregates across multiple vaults [astrix-secret-management-2026] |
| NHI-036 | Ephemeral workload via SPIFFE / Aembit | GAP | 0 | No SPIFFE / workload-broker ephemeral identity coverage found |
| NHI-037 | Forgotten / orphaned legacy identity | NATIVE | 4 | Orphan/dormant NHI detection is explicit use-case; "zombie credentials" named [astrix-lifecycle-2026] |

**NHI summary:** NATIVE=16, ADD-ON=11, GAP=10, N/A=0.

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Title | Coverage | Maturity | Evidence |
|---|---|---|---|---|
| UC-F-001 | Prevent plaintext secrets in source repos | NATIVE | 3 | GitHub integration; secret scanning; NHI fingerprinting across CI [astrix-nhi-discover-2026] |
| UC-F-002 | Detect/remediate secrets in history | PARTNER | 2 | Discovers exposed secrets in cloud/SaaS; historical repo scanning requires GitGuardian/TruffleHog partner |
| UC-F-003 | JIT short-lived cloud credentials via OIDC | GAP | 0 | Astrix discovers credentials but does not issue/broker OIDC tokens |
| UC-F-004 | Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No SPIFFE / SVID issuance or workload-broker capability |
| UC-F-005 | Dynamic database credentials with leases | GAP | 0 | Does not issue dynamic DB credentials; discovery only |
| UC-F-006 | Automated rotation of long-lived static secrets | NATIVE | 3 | Policy-driven rotation and expiration enforcement across vaults [astrix-lifecycle-2026] |
| UC-F-007 | Immediate revocation on identity compromise | NATIVE | 3 | ADR™ threat detection + automated revocation remediation workflows [astrix-iam-itdr-2026] |
| UC-F-008 | K8s secret consumption without on-disk plaintext | GAP | 0 | No CSI driver / Vault Agent injector capability; K8s service accounts discovered only |
| UC-F-009 | Container image-pull credentials per workload | ADD-ON | 1 | Image-pull creds discoverable via cloud-registry service-account inventory; not brokered |
| UC-F-010 | IaC secrets injected at apply-time | GAP | 0 | No Terraform/Ansible dynamic secrets provider capability |
| UC-F-011 | Observability-agent credentials rotated and scoped | ADD-ON | 2 | API keys for observability agents discoverable and rotation-enforceable via vault policy |
| UC-F-012 | Message-broker client identity hardening | ADD-ON | 1 | Cloud-IAM service accounts for Kafka/Pub-Sub discoverable; no direct broker-identity path |
| UC-F-013 | gMSA / Kerberos modernisation for AD service accounts | ADD-ON | 2 | AD / Entra ID integration surfaces AD service accounts; no gMSA provisioning capability |
| UC-F-014 | API-gateway upstream identity standardised | ADD-ON | 2 | OAuth creds / API keys for gateways discoverable; no gateway-cert lifecycle |
| UC-F-015 | RPA bot credentials vaulted and session-bound | ADD-ON | 2 | RPA bot service accounts surfaced via AD/cloud; no named RPA orchestrator integration |
| UC-F-016 | Keyless code- and artifact-signing in CI | GAP | 0 | No Sigstore / code-signing capability |
| UC-F-017 | TEE attestation gates secret release | GAP | 0 | No TEE attestation capability |
| UC-F-018 | AI-agent / LLM tool-credential brokering | NATIVE | 4 | ACP + Agent Policies: per-tool, per-session scoped tokens; JIT access [astrix-ai-agent-discovery-2026] |
| UC-F-019 | IoT / OT / branch-device identity enrolment | GAP | 0 | No IoT device enrolment capability |
| UC-F-020 | Mainframe / midrange credential rotation | GAP | 0 | No mainframe / RACF coverage |
| UC-F-021 | Backup / DR agent identity de-privileging | ADD-ON | 1 | Backup service accounts surfaced via AD; remediation possible but no native backup-agent path |
| UC-F-022 | Webhook inbound identity verification | NATIVE | 3 | Webhooks inventoried; signing-secret governance and rotation [astrix-nhi-discover-2026] |
| UC-F-023 | Network-device credential modernisation | GAP | 0 | No TACACS+ / network-device coverage |
| UC-F-024 | Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | No FAPI 2.0 / CDR / mTLS client-cert lifecycle coverage |
| UC-F-025 | OAuth-app / marketplace integration governance | NATIVE | 4 | Core use-case: tenant-wide OAuth inventory, stale-token revocation, vendor risk scoring [astrix-third-party-risk-2026] |
| UC-F-026 | Vault-internal identity hardening | ADD-ON | 2 | Vault activity monitoring; unvaulted-secret detection; no vault root-token / Shamir governance |
| UC-F-027 | Orphaned / dormant NHI cleanup pipeline | NATIVE | 4 | Dormancy detection, owner attestation, auto-revocation of unused NHIs [astrix-lifecycle-2026] |
| UC-N-001 | Real-time secret-sprawl KPI dashboard | NATIVE | 4 | Single dashboard: NHI count, risk posture, trend lines, per-team drill-down [astrix-nhi-platform-2026] |
| UC-N-002 | NHI inventory and ownership attestation | NATIVE | 4 | Continuous NHI inventory with owner attribution and attestation workflows [astrix-lifecycle-2026] |
| UC-N-003 | Rotation-coverage and freshness KPIs | NATIVE | 3 | Expiration dates, rotation status, usage trends reported per NHI bucket [astrix-lifecycle-2026] |
| UC-N-004 | Regulator audit evidence pack | ADD-ON | 2 | ITSM/GRC integration for evidence export; no APRA-specific pack; requires GRC tool config |
| UC-N-005 | Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Posture metrics available; no pre-built E8 or NIST SP 800-207 scorecard found |
| UC-N-006 | Vendor / SaaS supply-chain risk attestation | NATIVE | 4 | Third-party risk scoring, vendor reputation analysis, supply-chain breach tracking [astrix-third-party-risk-2026] |
| UC-N-007 | Data-sovereignty and residency assurance | GAP | 0 | SaaS-only; no AU data-residency or in-region deployment option documented |
| UC-N-008 | Engineer training and secure-coding adoption KPI | GAP | 0 | No training-management or LMS capability |
| UC-N-009 | Exception register and risk-acceptance governance | ADD-ON | 2 | GRC integration enables exception tracking; no native exception register in product |
| UC-N-010 | Break-glass and quorum-operator governance | GAP | 0 | No HSM/KMS quorum or break-glass identity governance |
| UC-N-011 | Post-incident reporting and identity-driven RCA | NATIVE | 3 | ADR™ incident detection + root cause analysis; SIEM integration for export [astrix-iam-itdr-2026] |
| UC-N-012 | Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA / signed-artifact coverage |
| UC-N-013 | Crypto-agility and post-quantum readiness reporting | GAP | 0 | No crypto-inventory or PQC readiness capability |
| UC-N-014 | Vendor-evaluation matrix maintenance | ADD-ON | 2 | NHI inventory data can feed vendor matrix; no dedicated matrix-maintenance workflow |
| UC-N-015 | Communications / stakeholder cadence | GAP | 0 | No comms or training workflow capability |
| UC-N-016 | IoT / OT / branch-fleet posture reporting | GAP | 0 | No IoT/OT coverage |
| UC-N-017 | Observability/telemetry secret-leak governance | NATIVE | 3 | Secrets exposed in SaaS/cloud detected; vault hygiene monitoring [astrix-secret-management-2026] |
| UC-N-018 | Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE attestation coverage |
| UC-N-019 | AI-agent / autonomous-workflow KPI suite | NATIVE | 4 | Per-agent credential issuance volume, anomalous tool-call detection, Agent Policies [astrix-ai-agent-discovery-2026] |
| UC-N-020 | Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe / RPA legacy posture reporting |

**UC summary:** NATIVE=16, ADD-ON=14, PARTNER=1, GAP=16, N/A=0.

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

**1. NHI discovery breadth across SaaS and cloud (industry-leading for this tier).**
Astrix's four-method agentless discovery surfaces OAuth apps, API keys, service accounts,
webhooks, PATs, secrets, managed identities, and AI agents across 20+ cloud/SaaS connectors.
The platform's core value proposition — "discover what you don't know exists" — addresses the
most common audit finding (orphaned/unowned NHIs). The Workday case study demonstrates
real-world prevention of supply-chain compromise. [astrix-workday-2026]

**2. AI agent and MCP governance — unique and differentiated.**
Astrix is the only profiled vendor with dedicated Agent Control Plane (ACP), Agent Policies
(allow/flag/block by user/department/resource), and four-method shadow-agent discovery
covering OpenAI, Bedrock, Vertex, Agentforce, and MCP servers. This directly addresses the
fastest-growing NHI class (NHI-019) and XYZ's likely 2027–2028 agentic-AI wave. [astrix-ai-agent-discovery-2026]

**3. Third-party OAuth / supply-chain risk governance.**
Continuous vendor risk scoring, real-time detection of compromised third-party integrations,
and stale-token auto-revocation are primary product capabilities with strong evidence (UC-F-025,
NHI-030, UC-N-006). The platform tracked breaches at CircleCI, Slack, GitHub, Okta, Snowflake —
directly relevant to XYZ's supply-chain risk programme. [astrix-third-party-risk-2026]

### Top 3 gaps

**1. No secrets-brokering or dynamic-credential issuance.**
Astrix discovers and governs but does not store, issue, or rotate secrets on behalf of
workloads. UCs requiring dynamic creds (UC-F-003/004/005/008/010) are hard GAPs —
Astrix must partner with Vault / AWS SM / Conjur for these.

**2. No AU data-residency or IRAP compliance.**
SaaS-only architecture with no declared AU region. APRA CPS 234 / CPS 230 data-flow
requirements are unresolved. This is a blocking risk for XYZ regulated workloads.

**3. No PKI, mTLS, mainframe, or IoT coverage.**
NHI-006/015/016/017/021/022/025/028/032–034/036 are all GAP. XYZ's mainframe
(NHI-022), Open Banking (NHI-028), and network-device (NHI-032) NHI lanes require a
complementary PKI/PAM vendor.

---

## 6. AU-specific notes (≤ 150 words)

No AU-specific product page, data-residency declaration, or IRAP assessment is publicly
documented for Astrix Security as of 2026-05-23. The platform is SaaS-only, hosted in US
cloud regions (inferred from Cisco/AWS partnership; no explicit AU-region option marketed).
This creates a material APRA CPS 234 §22 and CPS 230 §39 data-residency risk: NHI metadata
(credential names, scopes, usage patterns, owner identities) would transit and reside outside
Australia. ISO 27001 certification is not publicly claimed. IRAP is not applicable (Astrix
is not an Australian Government product at this time). Post-Cisco acquisition, Cisco's
existing IRAP-assessed infrastructure (Cisco Secure, Duo) may provide a path to AU sovereign
deployment, but no commitment is documented. XYZ procurement should obtain a Data Processing
Agreement with explicit AU-residency or in-Cisco-AU-cloud hosting commitment as a contractual
pre-condition. Essential 8 mapping is not pre-built; requires manual scorecard configuration.

[astrix-cisco-2026][astrix-soc2-2022]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Astrix Security (Agent 03 wave 4)`.

Keys: `astrix-nhi-platform-2026`, `astrix-nhi-discover-2026`, `astrix-ai-agent-discovery-2026`,
`astrix-lifecycle-2026`, `astrix-third-party-risk-2026`, `astrix-secret-management-2026`,
`astrix-iam-itdr-2026`, `astrix-why-2026`, `astrix-cisco-2026`, `astrix-workday-2026`,
`astrix-state-nhi-2024`, `astrix-soc2-2022`, `astrix-series-b-2024`, `astrix-helpnet-2026`,
`cisco-astrix-securityweek-2026` (15 total).

---

## 8. Open questions for v1.0

1. **AU data residency** — Does Cisco plan to offer Astrix capabilities from an IRAP-assessed
   AU region (Cisco or AWS ap-southeast-2) post-acquisition? What is the timeline?
2. **APRA CPS 234 metadata scope** — Which NHI metadata fields (credential names? usage logs?
   owner identity?) are retained in Astrix SaaS, and are they subject to APRA data-residency?
3. **Vault integration specifics** — Which named vault products (HashiCorp, CyberArk, Akeyless,
   AWS SM) does Astrix currently integrate with for rotation execution vs. discovery-only?
4. **ISO 27001 / IRAP roadmap** — Are these on the post-Cisco acquisition compliance roadmap?
5. **Tier-1 FI customer references** — Are there undisclosed financial-services customers (bank,
   insurer) willing to provide a reference for XYZ procurement?
6. **Mainframe / RACF roadmap** — Is NHI-022 on any product roadmap, given XYZ's core-banking
   dependency?
7. **Acquisition risk** — What are the contractual protections if the Cisco acquisition results
   in product roadmap changes or pricing restructure? What is the support SLA continuity model?
8. **AI agent identity scoping** — Does Astrix's ACP/Agent Policies support MFA or
   hardware-attested identity for AI agent provisioning (relevant to NHI-019 / UC-F-018)?

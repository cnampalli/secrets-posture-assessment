# Vendor Profile — Clutch Security

**Tier:** nhi-discovery
**Primary docs:** https://clutch.security
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Clutch Security is an Israeli-founded, US-headquartered NHI security start-up founded circa 2023. CEO and co-founder Ofir Har-Chen has a background at Sygnia and Hunters. Total funding: $28.5M — $8.5M Seed (July 2024, Lightspeed Venture Partners + Merlin Ventures) and $20M Series A (January 2025, SignalFire lead, Lightspeed, Merlin Ventures, Cyber Club London). Deployment model: agentless SaaS with Zero-Knowledge Architecture — sensitive data never leaves the customer network; no credentials stored or transmitted to Clutch. AWS Marketplace listed ($50k/year Starter Pack). Positions as "the industry's first Universal Non-Human Identity Security Platform" built on the Identity Lineage® Graph. Primary differentiator: holistic NHI discovery + AI agent governance + secret scanning in a single agentless SaaS, challenging vault vendors on posture and observability. No announced AU data-residency region or IRAP certification as of May 2026. [clutch-series-a-2025] [clutch-aws-marketplace-2025]

---

## 2. Architecture (≤ 250 words)

**Deployment:** Agentless, API-based. One-click connection to cloud providers, SaaS apps, vaults, code repos, and endpoints. No agents, no infrastructure changes required. [clutch-platform-2025]

**Data handling:** Zero-Knowledge Architecture. All sensitive data stays within the customer's network boundary. Clutch processes metadata and enrichment signals; raw credentials are never transmitted to Clutch infrastructure. [clutch-homepage-2025]

**Discovery engine:** Identity Lineage® Graph — a contextual identity graph mapping every NHI and secret to: (a) origin, (b) human owner, (c) storage location, (d) consumers, (e) downstream resources. Continuously refreshed via 100+ API integrations across cloud, SaaS, vaults, repos, CI/CD, endpoints, and AI platforms. [clutch-homepage-2025]

**Risk scoring:** Blast-radius-driven prioritisation. Findings ranked by what each identity can access and the business-damage of compromise, not severity labels alone. [clutch-platform-2025]

**Threat detection:** Behavioural baseline monitoring across identities and AI agents; alerts on deviation from baselines. [clutch-platform-2025]

**Vault integrations (read-only augmentation):** HashiCorp Vault, CyberArk, Delinea, 1Password, AWS Secrets Manager, Bravura Security. Clutch does not store or broker credentials; it reads vault metadata to augment inventory and surface missing secrets or copied credentials. [clutch-integrations-2025]

**Compliance certifications:** SOC 2 (AICPA), ISO 27001. Linux Foundation member. [clutch-homepage-2025]

**Rotation philosophy:** Clutch explicitly positions itself as an alternative to rotation cycles — advocating Zero Trust validation + ephemeral credentials over reactive rotation. Rotation orchestration is out-of-scope by design. [clutch-principles-2025]

**HSM / KMS:** No native HSM/KMS integration declared; not a secrets-brokering or secrets-storage product.

**FedRAMP / IRAP / AU sovereignty:** Not declared. SaaS control plane region not publicly disclosed.

---

## 3. NHI coverage map (≤ 600 words)

### NHI-001 — Cloud IAM principal (role / service account)
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Platform discovers and inventories AWS/Azure/GCP IAM roles and service accounts via cloud provider APIs. [clutch-homepage-2025]

### NHI-002 — Kubernetes ServiceAccount
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** Kubernetes listed as an integration source for identity discovery. [clutch-integrations-2025]

### NHI-003 — CI/CD pipeline identity
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** CI/CD platforms (Jenkins, CircleCI, Azure DevOps) in discovery source list; PATs/pipeline secrets scanned. [clutch-integrations-2025]

### NHI-004 — Container / image-pull credential
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** No dedicated image-pull credential feature; likely surfaced via repo/registry scanning as part of secret scan. [clutch-homepage-2025]

### NHI-005 — Database service account
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** Snowflake and Databricks in integration list; database credentials surfaced via vault augmentation. [clutch-integrations-2025]

### NHI-006 — Application TLS server / mTLS workload identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No certificate lifecycle management or PKI/mTLS features found in public docs. [clutch-platform-2025]

### NHI-007 — Third-party SaaS API key / OAuth client
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** SaaS OAuth app discovery and API key inventory are core use cases (Salesforce, Workday, SAP, Oracle, 100+ SaaS integrations). [clutch-homepage-2025]

### NHI-008 — Git platform credential (PAT, SSH key, deploy key)
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** GitHub/GitLab/Bitbucket in discovery sources; contextual secret scanning in repos; VSCode extension for workspace scanning. [clutch-integrations-2025]

### NHI-009 — Configuration-management / IaC agent identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Terraform listed as integration; IaC secrets surfaced via code scanning. [clutch-integrations-2025]

### NHI-010 — Monitoring / observability agent
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** Datadog, Splunk in integration list; observability agent API keys in discovery scope. [clutch-integrations-2025]

### NHI-011 — Message broker / event-bus client
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No Kafka/RabbitMQ/Service Bus integration or credential lifecycle feature found. [clutch-integrations-2025]

### NHI-012 — Active Directory / LDAP service account
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Windows listed as infrastructure integration; AD service account inventory not explicitly documented as native capability. [clutch-integrations-2025]

### NHI-013 — Reverse-proxy / API-gateway upstream identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No API gateway credential management or mTLS key inventory found in public docs. [clutch-platform-2025]

### NHI-014 — RPA bot identity
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** RPA listed as a discovery source category on the platform page. [clutch-platform-2025]

### NHI-015 — Code-signing identity (Sigstore / Authenticode / Apple)
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No code-signing or Sigstore features found. [clutch-platform-2025]

### NHI-016 — Build provenance / SLSA attestation identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No SLSA/in-toto provenance features declared. [clutch-platform-2025]

### NHI-017 — Service mesh control-plane identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No Istio/Linkerd/Consul control-plane identity management found. [clutch-platform-2025]

### NHI-018 — Confidential-computing attestation identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TEE/enclave attestation features declared. [clutch-platform-2025]

### NHI-019 — AI agent / autonomous workflow identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Dedicated Agentic AI Governance module: discovery (sanctioned + shadow AI), guardrails, risk scoring, threat detection. Shadow AI/MCP discovery GA Aug 2025. [clutch-agentic-ai-2025] [clutch-mcp-server-2025]

### NHI-020 — Model artifact / registry identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No model registry or ML pipeline identity features found. [clutch-platform-2025]

### NHI-021 — IoT / OT device identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No IoT/OT/device certificate or PSK management features found. [clutch-platform-2025]

### NHI-022 — Mainframe / midrange service identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No RACF/ACF2/IBM-i integration or mainframe credential management found. [clutch-platform-2025]

### NHI-023 — Database encryption / TDE master key identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No KMS/TDE key-management features declared. [clutch-platform-2025]

### NHI-024 — HSM / KMS operator / break-glass identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No HSM/KMS operator or quorum identity management found. [clutch-platform-2025]

### NHI-025 — Certificate authority operator identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No CA operator or PKI admin identity management found. [clutch-platform-2025]

### NHI-026 — Backup / DR agent identity
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Backup agent credentials likely surfaced via secret scanning / vault augmentation; no dedicated backup-agent feature. [clutch-platform-2025]

### NHI-027 — Backend-for-frontend / on-behalf-of token holder
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** OAuth client secrets and token credentials discoverable via SaaS and code scanning, but no OBO-specific workflow. [clutch-integrations-2025]

### NHI-028 — Federated B2B / Open Banking client identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No FAPI 2.0/CDR/Open Banking partner certificate lifecycle management found. [clutch-platform-2025]

### NHI-029 — Service-account-as-human (shared functional ID)
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** "Workforce Attribution" use case maps human-to-NHI relationships; Identity Lineage® identifies shared-account patterns. [clutch-homepage-2025]

### NHI-030 — Browser / SaaS extension and OAuth-app identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** OAuth app discovery across M365/Google Workspace/Salesforce/Slack/GitHub explicitly in discovery scope. "Shadow integration" use case addressed. [clutch-homepage-2025]

### NHI-031 — Webhook / inbound integration identity
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Webhook signing secrets likely surfaced via contextual secret scanning; no dedicated webhook-identity feature. [clutch-platform-2025]

### NHI-032 — Network / infrastructure device identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TACACS+/RADIUS/network-device credential management found. [clutch-platform-2025]

### NHI-033 — Print / spooler / branch-peripheral identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No branch peripheral / ATM credential management declared. [clutch-platform-2025]

### NHI-034 — Quantum-resistant / hybrid-PKI rotation identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No PQC or hybrid-cert features declared. [clutch-platform-2025]

### NHI-035 — Vault-internal / secrets-broker identity
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Vault augmentation surfaces vault-internal gaps (missing secrets, copied credentials); does not govern vault root tokens or replication credentials. [clutch-homepage-2025]

### NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Clutch explicitly advocates ephemeral credentials as core ZT philosophy; platform lifecycle features support transition to ephemeral identities; ZT-for-NHIs is the primary product narrative. [clutch-principles-2025]

### NHI-037 — Forgotten / orphaned legacy identity
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** "Identity Hygiene Automation" use case: clean up stale and orphaned identities. Dormancy detection and owner attestation are declared capabilities. [clutch-homepage-2025]

---

## 4. Use-case scoring (≤ 800 words)

### UC-F-001 — Prevent plaintext secrets in source repositories
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Contextual Secret Scanning in repos (GitHub/GitLab/Bitbucket) with blast-radius context; VSCode extension for workspace scanning. [clutch-integrations-2025]

### UC-F-002 — Detect and remediate secrets already in history
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Continuous and historical sweep with contextual remediation; "Vault Augmentation" surfaces secrets outside vaults. [clutch-homepage-2025]

### UC-F-003 — Just-in-time short-lived cloud credentials via OIDC
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Clutch discovers and inventories OIDC-federated pipelines; advocates ephemeral credentials; does not issue OIDC tokens itself — partner with IdP or CI platform. [clutch-principles-2025]

### UC-F-004 — Workload-attested ephemeral identity (SPIFFE/SPIRE)
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Clutch advocates and tracks ephemeral NHIs but does not operate a SPIFFE workload API itself. [clutch-principles-2025]

### UC-F-005 — Dynamic database credentials with broker-issued leases
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Clutch does not broker database credentials; no dynamic-secret engine found. [clutch-platform-2025]

### UC-F-006 — Automated rotation of long-lived static secrets
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Clutch explicitly does NOT position rotation as a core feature — anti-rotation philosophy; advocates ZT + ephemeral instead. [clutch-principles-2025]

### UC-F-007 — Immediate revocation on identity compromise
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** AWS Key Lockdown open-source tool for revoking exposed AWS access keys; platform integrates with SOAR/SIEM for response. [clutch-homepage-2025]

### UC-F-008 — Kubernetes secret consumption without on-disk plaintext
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No K8s CSI driver, secret-store integration, or etcd encryption capability found. [clutch-platform-2025]

### UC-F-009 — Container image-pull credentials issued per workload
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No per-workload image-pull credential issuance feature found. [clutch-platform-2025]

### UC-F-010 — IaC / config-management secrets injected at apply-time
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** Clutch does not inject secrets at apply-time; Terraform integration is discovery-only. [clutch-integrations-2025]

### UC-F-011 — Observability-agent credentials rotated and scoped
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Datadog/Splunk agent credentials in discovery scope; lifecycle hygiene flagged; rotation itself requires vault partner. [clutch-integrations-2025]

### UC-F-012 — Message-broker client identity hardening
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No Kafka/Service Bus/RabbitMQ integration found. [clutch-integrations-2025]

### UC-F-013 — gMSA / Kerberos modernisation for AD service accounts
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Windows/AD integration listed; AD service account inventory possible; gMSA migration orchestration not found. [clutch-integrations-2025]

### UC-F-014 — API-gateway upstream identity standardised
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No API gateway identity lifecycle or mTLS certificate management found. [clutch-platform-2025]

### UC-F-015 — RPA bot credentials vaulted and session-bound
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** RPA listed as discovery source; bot identity mapping via Identity Lineage®; vault integration for bot credential storage not native. [clutch-platform-2025]

### UC-F-016 — Keyless code- and artifact-signing in CI
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No code-signing or Sigstore integration found. [clutch-platform-2025]

### UC-F-017 — TEE attestation gates secret release
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TEE/enclave attestation features declared. [clutch-platform-2025]

### UC-F-018 — AI-agent / LLM tool-credential brokering
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Agentic AI Governance: agent credential mapping, guardrails on tool permissions, shadow AI/MCP discovery (Claude/Copilot/Cursor). [clutch-agentic-ai-2025] [clutch-shadow-ai-2025]

### UC-F-019 — IoT / OT / branch-device identity enrolment
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No IoT/OT/ATM device enrolment or certificate lifecycle found. [clutch-platform-2025]

### UC-F-020 — Mainframe / midrange credential rotation pipeline
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No mainframe/RACF integration or credential rotation pipeline found. [clutch-platform-2025]

### UC-F-021 — Backup / DR agent identity de-privileging
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Backup agent credentials surfaced via secret scanning; no dedicated de-privilege or vault-integration workflow for backup agents. [clutch-platform-2025]

### UC-F-022 — Webhook inbound identity verification
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Webhook signing secrets surfaced via contextual scanning; no dedicated verification middleware or replay-protection feature. [clutch-platform-2025]

### UC-F-023 — Network-device credential modernisation
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TACACS+/RADIUS/network-device integration found. [clutch-integrations-2025]

### UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No CDR/FAPI 2.0 partner certificate lifecycle found. [clutch-platform-2025]

### UC-F-025 — OAuth-app / marketplace integration governance
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** OAuth app discovery and risk scoring across M365/Google Workspace/Salesforce/GitHub/Slack is a stated use case; stale-token detection. [clutch-homepage-2025]

### UC-F-026 — Vault-internal identity hardening
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Vault Augmentation: surfaces missing secrets, copied credentials, gaps in vault coverage. Does not manage root tokens or replication identities natively. [clutch-homepage-2025]

### UC-F-027 — Orphaned / dormant NHI cleanup pipeline
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** "Identity Hygiene Automation" explicitly addresses stale/orphaned NHIs; owner attestation and dormancy detection declared. [clutch-homepage-2025]

---

### UC-N-001 — Real-time secret-sprawl KPI dashboard
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Full inventory and risk scoring within minutes; contextual findings dashboard with remediation prioritisation. [clutch-platform-2025]

### UC-N-002 — NHI inventory and ownership attestation
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Identity Lineage® maps every NHI to human owner; lifecycle ownership tracking; workforce attribution use case. [clutch-homepage-2025]

### UC-N-003 — Rotation-coverage and freshness KPIs
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Clutch tracks secret age and hygiene KPIs; rotation-specific KPIs depend on vault partner integrations for coverage. [clutch-platform-2025]

### UC-N-004 — Regulator audit evidence pack
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** SOC 2 + ISO 27001 certified; no APRA CPS 234 mapping or one-click evidence pack feature found publicly. [clutch-homepage-2025]

### UC-N-005 — Essential 8 / ZT control-area scorecard
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** ZT-for-NHIs is the product narrative; no explicit E8/NIST CSF scorecard feature found. [clutch-principles-2025]

### UC-N-006 — Vendor / SaaS supply-chain risk attestation
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** SaaS OAuth app risk scoring; supply-chain secret exposure via repo scanning; no formal vendor-risk register feature found. [clutch-homepage-2025]

### UC-N-007 — Data-sovereignty and residency assurance
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No AU data residency region, IRAP certification, or APRA CPS 230 data-flow documentation found publicly. SaaS control plane region undisclosed. [clutch-platform-2025]

### UC-N-008 — Engineer training and secure-coding adoption KPI
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** NHI Masterclass and Agentic AI Masterclass training content offered; no LMS integration or training-completion KPI feature found. [clutch-homepage-2025]

### UC-N-009 — Exception register and risk-acceptance governance
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** Risk-scoring and remediation context provided; no formal GRC exception register integration found publicly. [clutch-platform-2025]

### UC-N-010 — Break-glass and quorum-operator governance
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No HSM/KMS quorum or break-glass identity governance found. [clutch-platform-2025]

### UC-N-011 — Post-incident reporting and identity-driven RCA
- **Coverage:** ADD-ON
- **Maturity:** 2
- **Evidence:** Threat detection + SOAR integration (PagerDuty, CrowdStrike) enables incident response; no NHI-attributed RCA schema or MITRE T1552 tagging found. [clutch-integrations-2025]

### UC-N-012 — Supply-chain / SLSA-provenance assurance reporting
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No SLSA/in-toto provenance reporting found. [clutch-platform-2025]

### UC-N-013 — Crypto-agility and post-quantum readiness reporting
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No PQC crypto-inventory or hybrid-cert features declared. [clutch-platform-2025]

### UC-N-014 — Vendor-evaluation matrix maintenance
- **Coverage:** ADD-ON
- **Maturity:** 1
- **Evidence:** NHI Index (nonhuman.id) industry mapping published; no automated vendor-matrix delta feature found. [clutch-homepage-2025]

### UC-N-015 — Communications, change-comms and stakeholder cadence
- **Coverage:** N/A
- **Maturity:** 0
- **Evidence:** Not a product capability; out of scope for a vendor platform. [INDUSTRY-CONSENSUS]

### UC-N-016 — IoT / OT / branch-fleet posture reporting
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No IoT/OT fleet posture or default-credential reporting found. [clutch-platform-2025]

### UC-N-017 — Observability/telemetry secret-leak governance
- **Coverage:** NATIVE
- **Maturity:** 2
- **Evidence:** Datadog/Splunk integration; secret scanning surfaces credentials in observability configs; no dedicated log-scrubbing middleware. [clutch-integrations-2025]

### UC-N-018 — Confidential-computing / TEE attestation assurance
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No TEE attestation audit or reporting features found. [clutch-platform-2025]

### UC-N-019 — AI-agent / autonomous-workflow KPI suite
- **Coverage:** NATIVE
- **Maturity:** 3
- **Evidence:** Agentic AI Governance: per-agent credential inventory, tool-access tracking, behavioural anomaly detection, shadow AI KPIs. [clutch-agentic-ai-2025]

### UC-N-020 — Mainframe / legacy posture and exception transparency
- **Coverage:** GAP
- **Maturity:** 0
- **Evidence:** No mainframe/RPA legacy posture reporting found; RPA is a discovery source but reporting depth unconfirmed. [clutch-platform-2025]

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

**1. Identity Lineage® Graph — contextual NHI inventory at scale.**
Clutch's graph approach — mapping every NHI to origin, owner, storage, consumers, and resources — is a genuine differentiator over point-scanners. The agentless, API-driven model means deployment in minutes across 100+ platforms with no infrastructure overhead, yielding rapid time-to-value for UC-N-002 (inventory) and UC-F-027 (orphan cleanup). [clutch-homepage-2025]

**2. AI agent / shadow AI governance — first-mover advantage.**
The Agentic AI Governance module (Shadow AI/MCP discovery GA Aug 2025, Universal NHI MCP Server Aug 2025) positions Clutch as the most purpose-built vendor for NHI-019 (AI agent identity) and UC-F-018/UC-N-019 in this evaluation. The ability to discover unsanctioned MCP servers (Claude/Copilot/Cursor) and map their credential access is currently unique at this maturity level. [clutch-agentic-ai-2025]

**3. Zero Trust NHI philosophy — ephemeral credentials + behaviour analytics.**
Clutch's explicit anti-rotation stance and ZT-for-NHIs narrative (continuous validation, least privilege, ephemeral identity lifecycle) aligns well with a Tier-1 bank's ZT transformation goals, particularly for cloud-native NHI classes (NHI-001/003/007/030). Blast-radius-driven risk scoring is more actionable for incident response than severity-only labels. [clutch-principles-2025]

### Top 3 gaps

**1. AU sovereignty — critical blocker.**
No AU data-residency region, IRAP certification, or APRA CPS 230/234 data-flow documentation found. SaaS control plane region undisclosed. For an APRA-regulated entity, this is a material deployment blocker for production use of the cloud-connected discovery features.

**2. Secrets brokering and rotation — by design absent.**
Clutch explicitly does not offer secrets injection (UC-F-005/008/009/010), rotation orchestration (UC-F-006), or dynamic credential issuance. These gaps require HashiCorp Vault, CyberArk, or AWS Secrets Manager as partners.

**3. Legacy/infrastructure long tail — out of scope.**
Mainframe (NHI-022), network devices (NHI-032), IoT/OT (NHI-021), PKI/HSM (NHI-024/025), message brokers (NHI-011), and code-signing (NHI-015/016) are all GAP. For a bank with a broad NHI estate, Clutch covers the modern cloud/SaaS/AI tier but not the deep legacy and infrastructure tier.

---

## 6. AU-specific notes (≤ 150 words)

**Data residency:** No publicly disclosed AU/APAC SaaS region. Zero-Knowledge Architecture (data stays in customer network) partially mitigates sovereignty risk for discovery metadata, but the Clutch SaaS control plane processes enrichment signals whose residency is unconfirmed. [clutch-platform-2025]

**IRAP:** No IRAP Protected assessment declared. Not listed on ASD's IRAP-assessed products register as of May 2026. [INDUSTRY-CONSENSUS]

**APRA CPS 234 / CPS 230:** No published mapping to CPS 234 §22/28/33/35 controls. No BCM or data-residency documentation for CPS 230 §39. Material gap for APRA-regulated adoption.

**Essential 8:** ZT-for-NHIs narrative aligns with E8 Restrict Admin Privileges and Multi-Factor Auth (machine) controls, but no formal E8 maturity mapping published.

**Customer references — AU/NZ:** None found publicly. NTT Data (global), Fluidra, OpenWeb, Cedar are named references; no AU Tier-1 FI reference disclosed.

**Recommendation:** Engage Clutch pre-sales on AU region roadmap, IRAP intent, and CPS 234 evidence capability before production consideration.

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Clutch Security (Agent 03 wave 4)`.

Key references: [clutch-homepage-2025], [clutch-platform-2025], [clutch-principles-2025], [clutch-series-a-2025], [clutch-mcp-server-2025], [clutch-shadow-ai-2025], [clutch-agentic-ai-2025], [clutch-aws-marketplace-2025], [clutch-integrations-2025], [signalfire-clutch-2025].

---

## 8. Open questions for v1.0

1. **AU data residency:** Does Clutch plan an AU/APAC SaaS region or on-premises deployment option? What is the control-plane data flow for the Zero-Knowledge Architecture?
2. **IRAP roadmap:** Is Clutch pursuing IRAP Protected assessment for ASD/APRA-regulated customers?
3. **Rotation orchestration:** Is Clutch building rotation orchestration (via vault API calls) or deliberately maintaining the anti-rotation positioning?
4. **Vault brokering partnership:** What is the recommended Clutch + HashiCorp Vault / CyberArk integration pattern for UC-F-005/008/010?
5. **Tier-1 FI reference:** Any named banking or financial-services customer in APAC willing to provide a public reference?
6. **Mainframe coverage:** Any roadmap for RACF/IBM-i credential inventory (NHI-022)?
7. **Dynamic credential lifecycle:** Does the ephemeral-credentials philosophy include integration with cloud provider STS or SPIFFE for issuance, or is it a posture-tracking function only?
8. **Risk scoring methodology:** Is blast-radius scoring based on graph-traversal (reachability) or heuristic? What data does it use for business-damage estimation?

# Vendor Profile — Oasis Security

**Tier:** nhi-discovery
**Primary docs:** https://www.oasis.security
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Oasis Security is a privately-held, New York-based NHI Management and Agentic Access Management vendor founded in 2022. It raised a $35M seed round (Cyberstarts, 2023), $40M Series A (Sequoia, Accel, Cyberstarts, Jan 2024), and $120M Series B (Craft Ventures lead, Sequoia, Accel, Cyberstarts, March 2026), totalling $195M. ARR grew 5× year-on-year; the majority of new ARR comes from Fortune 500 multi-year agreements. The platform is delivered as SaaS (no self-hosted option publicly declared). The primary differentiator is full NHI lifecycle governance — discovery, ownership attribution, posture management, rotation orchestration, provisioning, decommissioning, and ITDR — combined with a dedicated Agentic Access Management (AAM) layer for AI agent credential brokering. No AU/APAC data-centre, IRAP, or APRA-specific certifications found in public sources. SOC 2 and ISO/IEC 27001 achieved; ISO/IEC 27018 certification also reported.

---

## 2. Architecture (≤ 250 words)

**Deployment model:** SaaS only (agentless-first, with an optional agent for on-prem Active Directory discovery). No self-hosted or private-cloud deployment option has been announced publicly.

**Discovery mechanism:** Oasis connects to cloud control planes (AWS, Azure, GCP), identity providers (Okta, Entra ID, Ping), secrets vaults (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), SaaS platforms (Salesforce, GitHub, Snowflake, Databricks, OpenAI, Copilot, Glean), and on-prem Active Directory via a read-only agentless connector or an agent for environments not synced to Entra. Oasis does not store secrets — it stores metadata about NHIs and their credential relationships.

**AuthPrint™ technology:** Proprietary behavioral fingerprinting engine inside Oasis Scout (launched GA January 2025) that maps observed credential-usage patterns to known threat-actor signatures, reducing false-positive rates.

**Agentic Access Management (AAM™):** Announced November 2025. Issues ephemeral, per-session, least-privilege identities to AI agents after intent analysis; full audit chain (Human → Agent → Prompt → Intent → Policy → Identity → Actions → Results). No standing permissions or long-lived secrets in agent workflows.

**Secrets integration posture:** Oasis positions itself as complementary to vaults — vaults store secrets; Oasis maps who owns them, who uses them, and what they access. Rotation is orchestrated by Oasis, executed via the target vault or system.

**Compliance certifications (confirmed):** SOC 2, ISO/IEC 27001. No IRAP, FedRAMP, or AU-sovereign region declared.

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence |
|--------|----------|----------|---------|
| NHI-001 Cloud IAM principal | NATIVE | 4 | Platform discovers AWS IAM roles, Azure managed identities, GCP service accounts natively [oasis-product-2025] |
| NHI-002 Kubernetes ServiceAccount | ADD-ON | 2 | Workload identity discovery referenced in glossary; no dedicated K8s connector published [oasis-glossary-2025] |
| NHI-003 CI/CD pipeline identity | NATIVE | 3 | GitHub integration GA; OIDC-federated identities and PATs discovered and lifecycle-managed [oasis-github-2025] |
| NHI-004 Container image-pull credential | ADD-ON | 2 | Covered via cloud IAM (ECR/ACR/GAR) discovery; no dedicated pull-secret connector [oasis-product-2025] |
| NHI-005 Database service account | NATIVE | 3 | AWS RDS users and Snowflake/Databricks service accounts in scope; rotation orchestrated [oasis-databricks-2025] |
| NHI-006 App TLS/mTLS workload identity | PARTNER | 1 | Not a certificate lifecycle tool; certificates discovered contextually via vault integrations [oasis-vault-collab-2025] |
| NHI-007 Third-party SaaS API key / OAuth client | NATIVE | 4 | Core discovery use-case — API keys, OAuth tokens across Salesforce, Slack, GitHub, Office 365 inventoried [oasis-product-2025] |
| NHI-008 Git platform credential (PAT, SSH, deploy key) | NATIVE | 3 | GitHub integration detects PATs, SSH keys, deploy keys; scope-inflation detection [oasis-github-2025] |
| NHI-009 IaC / config-mgmt agent identity | ADD-ON | 2 | Terraform-based provisioning workflows supported; IaC agent NHIs discovered via cloud IAM [oasis-provisioning-2025] |
| NHI-010 Monitoring/observability agent | ADD-ON | 2 | Agent API keys surfaced via SaaS discovery (Datadog, Splunk not confirmed explicitly); [INDUSTRY-CONSENSUS] |
| NHI-011 Message broker / event-bus client | GAP | 0 | No Kafka, RabbitMQ, or Azure Service Bus connector found in public docs [oasis-product-2025] |
| NHI-012 Active Directory / LDAP service account | NATIVE | 3 | GA AD integration (Dec 2024) — agentless (Entra-synced) and agent-based (on-prem) [oasis-ad-2024] |
| NHI-013 API-gateway upstream identity | ADD-ON | 1 | Covered indirectly via cloud IAM / SaaS discovery; no API-GW-specific connector [oasis-product-2025] |
| NHI-014 RPA bot identity | ADD-ON | 2 | RPA listed as NHI type in glossary; discovered via AD and SaaS connectors [oasis-glossary-2025] |
| NHI-015 Code-signing identity | GAP | 0 | Not in scope — NHI discovery tool, not PKI/signing lifecycle [oasis-product-2025] |
| NHI-016 Build provenance / SLSA attestation | GAP | 0 | Supply-chain attestation not a platform capability [oasis-product-2025] |
| NHI-017 Service mesh control-plane identity | GAP | 0 | SPIFFE/SPIRE and mesh CA identities not discoverable; no connector found [oasis-product-2025] |
| NHI-018 Confidential-computing attestation | GAP | 0 | TEE attestation identities not in scope [oasis-product-2025] |
| NHI-019 AI agent / autonomous workflow identity | NATIVE | 4 | AAM™ core product — ephemeral per-session identities, intent-based access, full audit trail (Nov 2025 GA) [oasis-aam-2025] |
| NHI-020 Model artifact / registry identity | ADD-ON | 1 | Partially covered via SaaS discovery (OpenAI, Hugging Face not confirmed); [INDUSTRY-CONSENSUS] |
| NHI-021 IoT / OT device identity | GAP | 0 | Device identity in glossary but no IoT/OT connector or lifecycle tooling found [oasis-glossary-2025] |
| NHI-022 Mainframe / midrange service identity | GAP | 0 | No RACF, ACF2, or z/OS connector found [oasis-product-2025] |
| NHI-023 Database encryption / TDE master key | GAP | 0 | KMS keys in glossary (metadata-level); TDE lifecycle not a platform capability [oasis-glossary-2025] |
| NHI-024 HSM / KMS operator / break-glass identity | ADD-ON | 2 | Break-glass accounts in glossary with AWS/Azure/GCP/Okta support; HSM-operator class not addressed [oasis-glossary-2025] |
| NHI-025 CA operator identity | GAP | 0 | PKI/CA operator identities not in scope [oasis-product-2025] |
| NHI-026 Backup / DR agent identity | ADD-ON | 1 | AD-connected backup service accounts discoverable; no Veeam/Rubrik direct connector [oasis-ad-2024] |
| NHI-027 Backend-for-frontend / OBO token holder | ADD-ON | 2 | Confidential-client and OAuth refresh tokens discoverable via SaaS connectors [oasis-product-2025] |
| NHI-028 Federated B2B / Open Banking client | GAP | 0 | FAPI 2.0 / CDR client certs and mTLS identities not addressed [oasis-product-2025] |
| NHI-029 Service-account-as-human (shared functional ID) | NATIVE | 3 | AD integration distinguishes human vs NHI accounts; stale/shared account detection [oasis-ad-2024] |
| NHI-030 Browser / SaaS extension and OAuth-app | NATIVE | 3 | OAuth app discovery across M365, Google Workspace, Salesforce, GitHub is a core platform capability [oasis-product-2025] |
| NHI-031 Webhook / inbound integration identity | NATIVE | 2 | Webhooks listed in NHI type glossary; discovered via SaaS connectors [oasis-glossary-2025] |
| NHI-032 Network / infrastructure device identity | GAP | 0 | Network device credentials (TACACS, SNMP) not in scope [oasis-product-2025] |
| NHI-033 Print / spooler / branch-peripheral | GAP | 0 | Branch peripheral identities not addressed [oasis-product-2025] |
| NHI-034 Quantum-resistant / hybrid-PKI rotation | GAP | 0 | PQC out of scope for NHI discovery tier [oasis-product-2025] |
| NHI-035 Vault-internal / secrets-broker identity | PARTNER | 2 | Vault connectors read metadata; vault-internal identities (root tokens, replication tokens) not governed by Oasis [oasis-vault-collab-2025] |
| NHI-036 Ephemeral workload via SPIFFE/Aembit | PARTNER | 1 | Federated OIDC identities discovered; SPIFFE SVIDs and Aembit workload tokens not a native connector [oasis-glossary-2025] |
| NHI-037 Forgotten / orphaned legacy identity | NATIVE | 4 | Stale identity detection, dormancy-based decommissioning, ownership attestation campaigns are core platform capabilities [oasis-governance-2025] |

---

## 4. Use-case scoring (≤ 800 words)

**Framing note:** Oasis is an NHI discovery/posture/lifecycle/ITDR SaaS platform — not a secrets vault. Score vault-storage UCs (F-003, F-004, F-005, F-008, F-009, F-016, F-017) as GAP or PARTNER where Oasis provides no native storage or brokering beyond metadata/orchestration. Score NHI inventory/observability/governance UCs highly where Oasis is the primary product.

| UC-ID | Type | Coverage | Maturity | Evidence |
|-------|------|----------|----------|---------|
| UC-F-001 Prevent plaintext secrets in repos | UC-F | ADD-ON | 2 | GitHub integration detects secrets in repos; Oasis is not a dedicated secrets scanner but surfaces NHI credential exposure [oasis-github-2025] |
| UC-F-002 Detect/remediate secrets in history | UC-F | ADD-ON | 1 | Discovery surfaces exposed credentials; full historical repo scanning is out-of-scope for NHI platform [oasis-product-2025] |
| UC-F-003 JIT short-lived cloud creds via OIDC | UC-F | PARTNER | 2 | Federated identity provisioning (OIDC) supported in NHI Provisioning; JIT issuance is via cloud IAM not Oasis itself [oasis-provisioning-2025] |
| UC-F-004 SPIFFE/SPIRE workload identity | UC-F | GAP | 0 | No SPIFFE/SPIRE connector or SVID issuance capability [oasis-product-2025] |
| UC-F-005 Dynamic DB credentials | UC-F | GAP | 0 | Vault-class DB dynamic-credential issuance not a platform capability; Oasis orchestrates rotation only [oasis-vault-collab-2025] |
| UC-F-006 Automated rotation of long-lived secrets | UC-F | NATIVE | 3 | Rotation orchestration (schedule + on-incident) via vault integrations is core — HashiCorp Vault, AWS SM, Azure KV, GCP SM [oasis-provisioning-2025] |
| UC-F-007 Immediate revocation on compromise | UC-F | NATIVE | 3 | Oasis Scout ITDR triggers revocation workflows; integration with SOAR playbooks not explicitly documented [oasis-scout-2025] |
| UC-F-008 K8s secret consumption without plaintext | UC-F | GAP | 0 | CSI driver / agent-injector deployment not a platform capability [oasis-product-2025] |
| UC-F-009 Container image-pull creds per workload | UC-F | GAP | 0 | Pull-credential issuance not in scope [oasis-product-2025] |
| UC-F-010 IaC/config secrets at apply-time | UC-F | ADD-ON | 2 | Terraform-based provisioning and approval workflows exist; state-file scanning not native [oasis-provisioning-2025] |
| UC-F-011 Observability-agent creds rotated/scoped | UC-F | ADD-ON | 2 | Monitoring agent API keys inventoried and rotation orchestrated via vault connectors [oasis-product-2025] |
| UC-F-012 Message-broker client hardening | UC-F | GAP | 0 | No Kafka/RabbitMQ/Service Bus connector [oasis-product-2025] |
| UC-F-013 gMSA / Kerberos modernisation | UC-F | NATIVE | 3 | AD integration with service-account lifecycle management (ownership, rotation, decommission); gMSA-specific migration not explicitly confirmed [oasis-ad-2024] |
| UC-F-014 API-gateway upstream identity | UC-F | GAP | 0 | API-gateway cert lifecycle not in scope [oasis-product-2025] |
| UC-F-015 RPA bot credentials vaulted | UC-F | ADD-ON | 2 | RPA identities discovered and lifecycle-managed via AD and SaaS connectors; vault integration orchestrates rotation [oasis-governance-2025] |
| UC-F-016 Keyless code/artifact signing | UC-F | GAP | 0 | Code-signing not in scope [oasis-product-2025] |
| UC-F-017 TEE attestation gates secret release | UC-F | GAP | 0 | Confidential-computing attestation not in scope [oasis-product-2025] |
| UC-F-018 AI-agent / LLM tool-credential brokering | UC-F | NATIVE | 4 | AAM™ core capability: per-session ephemeral identity, intent analysis, deterministic policy, full audit chain; integrations with Claude, OpenAI, Cursor confirmed [oasis-aam-2025] |
| UC-F-019 IoT / OT / branch device enrolment | UC-F | GAP | 0 | No IoT/OT device connector or enrolment lifecycle [oasis-product-2025] |
| UC-F-020 Mainframe credential rotation pipeline | UC-F | GAP | 0 | No RACF/ACF2/z/OS connector [oasis-product-2025] |
| UC-F-021 Backup / DR agent de-privileging | UC-F | ADD-ON | 1 | Backup service accounts discoverable via AD; no Veeam/Rubrik direct integration [oasis-ad-2024] |
| UC-F-022 Webhook inbound identity verification | UC-F | ADD-ON | 2 | Webhooks discovered and inventoried; verification enforcement not native [oasis-glossary-2025] |
| UC-F-023 Network-device credential modernisation | UC-F | GAP | 0 | TACACS+/SNMP credentials not in scope [oasis-product-2025] |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner | UC-F | GAP | 0 | FAPI 2.0 / CDR client identity management not a platform capability [oasis-product-2025] |
| UC-F-025 OAuth-app / marketplace integration governance | UC-F | NATIVE | 4 | Shadow-integration discovery and governance across M365, Google Workspace, Salesforce, GitHub, Slack is a core product use-case; stale token revocation [oasis-product-2025] |
| UC-F-026 Vault-internal identity hardening | UC-F | PARTNER | 1 | Vault connectors read metadata; root token / replication token governance out of scope [oasis-vault-collab-2025] |
| UC-F-027 Orphaned / dormant NHI cleanup | UC-F | NATIVE | 4 | Stale/orphaned NHI detection, owner-attestation campaigns, decommission automation are flagship capabilities [oasis-governance-2025] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | UC-N | NATIVE | 3 | Built-in dashboard with 15 NHI KPIs, risk scoring, trend lines, board-level communication support [oasis-kpis-2025] |
| UC-N-002 NHI inventory and ownership attestation | UC-N | NATIVE | 4 | Core platform: auto-discovery, AI-powered owner attribution, recertification campaigns, GRC export [oasis-governance-2025] |
| UC-N-003 Rotation-coverage and freshness KPIs | UC-N | NATIVE | 3 | Rotation frequency, stale credential rate, orphan-reduction rate all tracked in dashboard [oasis-kpis-2025] |
| UC-N-004 Regulator audit evidence pack | UC-N | ADD-ON | 2 | Compliance dashboards per framework; PCI DSS 4.0, SOC 2, GDPR named; APRA CPS 234 not explicitly mapped [oasis-governance-2025] |
| UC-N-005 Essential 8 / ZT control-area scorecard | UC-N | ADD-ON | 1 | Five-dimension posture framework exists; Essential 8 and NIST ZT pillars not explicitly mapped [oasis-kpis-2025] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | UC-N | NATIVE | 3 | Third-party NHI exposure assessment and OAuth-app risk scoring in dashboard [oasis-kpis-2025] |
| UC-N-007 Data-sovereignty and residency assurance | UC-N | GAP | 0 | SaaS-only; no AU data-residency region, IRAP, or sovereignty commitment found publicly [oasis-iso-2024] |
| UC-N-008 Engineer training / secure-coding KPI | UC-N | GAP | 0 | NHI certification programme launched (education); not an enterprise training KPI tool [oasis-cert-2025] |
| UC-N-009 Exception register and risk-acceptance governance | UC-N | ADD-ON | 2 | Policy violation tracking and stale exception escalation partially addressed via posture management; dedicated exception-register workflow not confirmed [oasis-governance-2025] |
| UC-N-010 Break-glass and quorum-operator governance | UC-N | ADD-ON | 2 | Break-glass account discovery and monitoring across AWS/Azure/GCP/Okta in glossary; quorum-operator governance not addressed [oasis-glossary-2025] |
| UC-N-011 Post-incident reporting / identity-driven RCA | UC-N | NATIVE | 3 | Oasis Scout + NHI Threat Center provide ITDR incident attribution; audit trail supports RCA; MITRE ATT&CK tagging not confirmed [oasis-scout-2025] |
| UC-N-012 Supply-chain / SLSA provenance reporting | UC-N | GAP | 0 | SLSA/in-toto attestation not in scope [oasis-product-2025] |
| UC-N-013 Crypto-agility and PQC readiness reporting | UC-N | GAP | 0 | Crypto-inventory and PQC roadmap not a platform capability [oasis-product-2025] |
| UC-N-014 Vendor-evaluation matrix maintenance | UC-N | ADD-ON | 1 | Platform data could populate matrix inputs; no automated vendor-matrix tooling [oasis-product-2025] |
| UC-N-015 Communications / stakeholder cadence | UC-N | GAP | 0 | Out of scope [oasis-product-2025] |
| UC-N-016 IoT / OT / branch fleet posture reporting | UC-N | GAP | 0 | No IoT/OT fleet visibility [oasis-product-2025] |
| UC-N-017 Observability/telemetry secret-leak governance | UC-N | ADD-ON | 2 | NHI discovery surfaces observability agent credentials; telemetry secret-scrubbing not native [oasis-product-2025] |
| UC-N-018 Confidential-computing / TEE attestation assurance | UC-N | GAP | 0 | TEE out of scope [oasis-product-2025] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | UC-N | NATIVE | 3 | AAM audit chain provides per-session agent identity, tool calls, policy, expiration; weekly reporting KPIs referenced [oasis-aam-2025] |
| UC-N-020 Mainframe / legacy posture reporting | UC-N | GAP | 0 | No mainframe or RPA posture visibility beyond AD-connected accounts [oasis-product-2025] |

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **AI agent identity (NHI-019 / UC-F-018 / UC-N-019) — industry-leading.** Oasis is uniquely positioned among NHI vendors with a dedicated Agentic Access Management (AAM™) layer. Per-session ephemeral identity issuance, intent-based access, deterministic policy enforcement, and a complete audit chain (Human → Agent → Prompt → Intent → Policy → Identity → Actions → Results) represent Maturity 4 in a space where every other evaluated vendor scores GAP or ADD-ON. The $120M Series B (March 2026) is explicitly positioned around this capability, and integrations with Claude, OpenAI, and Cursor are confirmed.

2. **NHI discovery breadth + ownership attribution.** Oasis's automated discovery across cloud IAM, Active Directory (agentless and agent-based, GA December 2024), SaaS platforms, git repos, secrets vaults, and data platforms, combined with AI-powered owner attribution and recertification campaigns, is Maturity 3–4 across NHI-001, NHI-007, NHI-012, NHI-029, NHI-030, NHI-037. The "who owns it, who uses it, what it can access" framing directly serves UC-N-002 (NHI inventory) and UC-F-027 (orphan cleanup) at enterprise scale.

3. **NHI ITDR — Oasis Scout.** GA January 2025, AuthPrint™ behavioral fingerprinting provides high-fidelity threat detection, reducing the ~90% false-positive rate typical in NHI monitoring. The NHI Threat Center (public threat-intel DB for NHI-targeting actors) is an industry first. Directly addresses UC-F-007 (revocation on compromise) and UC-N-011 (post-incident RCA).

### Top 3 gaps

1. **AU data sovereignty / IRAP — critical gap for APRA-regulated deployments.** SaaS-only with no declared AU/APAC region, no IRAP assessment, and no APRA CPS 230/234 mapping. For XYZ Bank this is a material blocker for production adoption without a vendor commitment.

2. **Vault-class secrets brokering absent.** Oasis does not issue dynamic credentials, SPIFFE SVIDs, or database leases — it orchestrates rotation against existing vaults. UCs F-003 through F-010 (JIT cloud creds, SPIFFE, dynamic DB, K8s CSI, image-pull) are GAP or PARTNER. Oasis must pair with HashiCorp Vault, AWS Secrets Manager, or a PAM platform.

3. **Infrastructure perimeter NHIs — mainframe, network, IoT, PKI.** NHI-011 (message brokers), NHI-015–018 (code-signing, SLSA, mesh, TEE), NHI-021–022 (IoT, mainframe), NHI-025 (CA operator), NHI-032–034 (network, peripherals, PQC) are all GAP. This limits coverage for XYZ's core-banking and branch-network NHI classes without a complementary toolchain.

---

## 6. AU-specific notes (≤ 150 words)

**AU data residency:** No AU or APAC SaaS region declared in public documentation. This is a material risk under APRA CPS 230 (§39) and CPS 234 (§22) for any APRA-regulated entity processing or brokering credentials for Australian regulated data.

**IRAP status:** No IRAP assessment found. Not listed on ASD IRAP marketplace or equivalent AU-government cloud marketplace.

**SOC 2 / ISO 27001:** Confirmed. ISO/IEC 27018 (cloud privacy) also confirmed via PRNewswire announcement.

**APRA CPS 234 alignment:** The governance dashboard references PCI DSS 4.0, SOC 2, and GDPR as compliance frameworks but does not explicitly map to CPS 234 §22, §28, §33, or §35. Evidence packs for APRA examination are not described.

**Essential 8:** No direct Essential 8 mapping in product documentation. Could be constructed from NHI KPI data but requires custom mapping effort.

**Recommendation:** Oasis would require a Data Processing Agreement with explicit AU-residency commitment and a roadmap to an AP-region SaaS deployment before XYZ production use.

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Oasis Security (Agent 03 wave 4)`.

Key citation references used:
- `oasis-product-2025` — https://www.oasis.security/product
- `oasis-aam-2025` — https://www.oasis.security/agentic-access-management
- `oasis-scout-2025` — https://www.prnewswire.com/news-releases/oasis-security-launches-oasis-scout-the-first-itdr-solution-for-non-human-identities-with-authprint-technology-302362762.html
- `oasis-provisioning-2025` — https://www.oasis.security/blog/introducing-oasis-nhi-provisioning-transforming-nhi-security-from-day-1
- `oasis-governance-2025` — https://www.oasis.security/solutions/governance
- `oasis-ad-2024` — https://www.oasis.security/blog/oasis-security-integration-with-microsoft-active-directory
- `oasis-github-2025` — https://www.oasis.security/blog/enhancing-github-security-with-oasis
- `oasis-vault-collab-2025` — https://www.oasis.security/resources/the-collaborative-approach-of-secret-managers-and-oasis
- `oasis-kpis-2025` — https://www.oasis.security/blog/nhi-security-metrics-15-kpis-your-board-needs-in-2025
- `oasis-glossary-2025` — https://www.oasis.security/non-human-identity-management-glossary-identity-tyeps-oasis-security
- `oasis-databricks-2025` — https://www.oasis.security/blog/new-oasis-integration-for-databricks-secures-access-to-data-and-ai
- `oasis-iso-2024` — https://oasis.security/resources/oasis-has-achieved-iso-iec-27001-certification
- `oasis-series-b-2026` — https://fintech.global/2026/03/20/oasis-security-lands-120m-to-govern-enterprise-ai-agents/
- `oasis-cert-2025` — https://www.oasis.security/blog/nhi-certification
- `oasis-finance-2025` — https://www.oasis.security/solutions/finance

---

## 8. Open questions for v1.0

1. **AU data-residency commitment:** Does Oasis have a contractual AU-region SaaS option or a private-cloud deployment pathway for APRA-regulated customers? No public evidence found.
2. **IRAP roadmap:** Is Oasis Security planning an IRAP assessment? Relevant for AU government and APRA-adjacent clients.
3. **APRA CPS 234 mapping:** Does Oasis have a controls-mapping document for CPS 234 §22, §28, §33, §35?
4. **Kubernetes native connector:** Is a dedicated K8s ServiceAccount / projected-token connector on the roadmap, beyond the current Entra/cloud-IAM path?
5. **SOAR integration for revocation:** Is there a documented Palo Alto XSOAR / Splunk SOAR / ServiceNow SecOps playbook for one-click NHI revocation via Oasis Scout?
6. **Mainframe / RACF integration:** Any partnerships with IBM, BetaSoft, or Broadcom to address z/OS NHIs?
7. **AAM™ GA status / supported agent frameworks:** Is AAM™ in GA or preview? Which agent frameworks (LangChain, Agentforce, MS Copilot Studio) are natively supported vs. generic API?
8. **Tier-1 FI customer references:** Any Tier-1 bank or AU/APAC financial institution prepared to provide a reference?
9. **Pricing model:** Per-NHI, per-user, or platform licence? Key for XYZ business case modelling.
10. **CyberArk relationship:** Oasis lists CyberArk as an IAM integration; is there a formal technology partnership or competing positioning?

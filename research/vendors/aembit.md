# Vendor Profile — Aembit

**Tier:** nhi-discovery (workload-IAM / access-management sub-niche)
**Primary docs:** https://docs.aembit.io
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Aembit is a US-based (Silver Spring, MD) **Workload Identity and Access Management (WIAM)** platform founded in 2021. It raised $25M Series A in September 2024 (led by Acrew Capital; co-investors: Ballistic Ventures, Ten Eleven Ventures, Okta Ventures, CrowdStrike Falcon Fund), totalling ~$45M raised. The company employs ~45 staff. Aembit is a broker-centric platform: its Aembit Edge component intercepts outbound workload calls, attests the caller's identity via cloud/K8s/Kerberos metadata, and injects a short-lived just-in-time credential — eliminating static secrets from application code. The control plane (Aembit Cloud) is SaaS-only; no self-hosted control-plane option is documented. Aembit holds SOC 2 Type II (Feb 2024, recertified Feb 2025) and ISO 27001:2022 (March 2025) certifications. No AU data-residency region, IRAP assessment, or FedRAMP status has been declared. [aembit-series-a-2024][aembit-soc2-recert-2025][aembit-iso27001-2025]

---

## 2. Architecture (≤ 250 words)

Aembit operates a **hybrid control / data plane** architecture:

- **Aembit Cloud (control plane):** Centralised SaaS service that hosts the identity policy engine, audit log store, dashboard, and credential-provider integrations. Policy decisions are evaluated here; no secret values are stored at rest in Aembit.
- **Aembit Edge (data plane / broker):** A lightweight auth proxy deployed in the customer's environment (Kubernetes via Helm chart, AWS ECS Fargate, AWS Lambda, or VMs). Edge intercepts outbound workload requests, presents the workload's identity attestation to Aembit Cloud for policy evaluation, and — if approved — injects a short-lived credential into the request before forwarding to the target. Credentials are never returned to application memory.

**Trust anchor / attestation:** Edge reads cryptographically signed workload metadata from the host environment (cloud instance identity documents, Kubernetes projected service-account tokens, Kerberos tickets, OIDC tokens from CI systems) and forwards attested claims to the policy engine. Thirteen trust-provider types are documented (AWS Metadata Service, AWS Role, Azure Instance Metadata, Azure Entra WIF, GCP Identity Token, GitHub Actions OIDC, GitLab OIDC, Kubernetes Service Account, Kerberos, OIDC ID Token, SAMLv2, Terraform Cloud Token, Certificate Signed Attestation). [aembit-arch-2024][aembit-trust-providers-2024]

**Credential issuance:** Aembit issues API keys, Username/Password, JWT, OAuth 2.0 (client credentials and auth-code flows), AWS STS tokens, Azure Entra WIF tokens, GCP WIF tokens, SPIFFE JWT-SVIDs, X.509-SVIDs, and MCP access tokens. It can also fetch credentials from HashiCorp Vault, AWS Secrets Manager, and Azure Key Vault as upstream sources. [aembit-credential-providers-2024]

**SOC 2 Type II** (Sensiba LLP, Feb 2025 recertification) and **ISO 27001:2022** (Sensiba LLP / ANAB, March 2025). No FedRAMP or IRAP. [aembit-soc2-recert-2025][aembit-iso27001-2025]

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence |
|--------|----------|----------|---------- |
| NHI-001 Cloud IAM principal | NATIVE | 4 | AWS STS, Azure Entra WIF, GCP WIF trust providers + credential issuance natively [aembit-trust-providers-2024] |
| NHI-002 Kubernetes ServiceAccount | NATIVE | 4 | K8s SA Trust Provider supports EKS/AKS/GKE/self-hosted; namespace/pod/SA match rules [aembit-trust-providers-2024] |
| NHI-003 CI/CD pipeline identity | NATIVE | 3 | GitHub Actions OIDC and GitLab Job OIDC trust providers documented [aembit-trust-providers-2024] |
| NHI-004 Container image-pull credential | GAP | 0 | No image-pull credential provider documented; not core use case [aembit-arch-2024] |
| NHI-005 Database service account | NATIVE | 3 | PostgreSQL, MySQL, Snowflake documented as target workloads; credential injected JIT [aembit-snowflake-case-study-2024] |
| NHI-006 Application TLS / mTLS workload identity | NATIVE | 3 | X.509-SVID credential provider issued; mTLS broker patterns supported [aembit-credential-providers-2024] |
| NHI-007 Third-party SaaS API key / OAuth client | NATIVE | 3 | OAuth 2.0 client credentials + API Key credential providers; Atlassian, Slack, Datadog, PagerDuty named [aembit-credential-providers-2024] |
| NHI-008 Git platform credential (PAT, SSH) | ADD-ON | 2 | GitLab managed-account credential provider available; GitHub PAT not natively managed [aembit-credential-providers-2024] |
| NHI-009 IaC / config-mgmt agent identity | NATIVE | 3 | Terraform Cloud Identity Token trust provider; Terraform provider for policy-as-code [aembit-trust-providers-2024] |
| NHI-010 Monitoring / observability agent | GAP | 0 | No dedicated observability-agent credential rotation; API key issuance possible but unspecific [aembit-arch-2024] |
| NHI-011 Message broker / event-bus client | GAP | 1 | No Kafka/RabbitMQ/Service-Bus specific integration documented [INDUSTRY-CONSENSUS] |
| NHI-012 Active Directory / LDAP service account | ADD-ON | 2 | Kerberos trust provider attests Windows/AD-joined workloads; does not manage AD account passwords [aembit-ms-environments-2025] |
| NHI-013 Reverse-proxy / API gateway upstream | ADD-ON | 2 | JWT/OAuth injection into HTTP(S) upstream; no dedicated API-GW connector [aembit-arch-2024] |
| NHI-014 RPA bot identity | GAP | 0 | No UiPath/Blue Prism/AA connector documented [INDUSTRY-CONSENSUS] |
| NHI-015 Code-signing identity | GAP | 0 | Not in scope for Aembit [INDUSTRY-CONSENSUS] |
| NHI-016 Build provenance / SLSA attestation identity | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| NHI-017 Service mesh control-plane identity | ADD-ON | 2 | Issues X.509-SVIDs; can serve as SPIFFE-compatible issuance layer; integrates with SPIRE [aembit-spiffe-2025] |
| NHI-018 Confidential-computing / TEE attestation | GAP | 0 | No TEE attestation integration documented [INDUSTRY-CONSENSUS] |
| NHI-019 AI agent / autonomous workflow identity | NATIVE | 4 | Blended Identity + MCP Identity Gateway GA April 2026; cryptographic agent identity + human binding + token exchange [aembit-agentic-ai-ga-2026] |
| NHI-020 Model artifact / registry identity | GAP | 0 | No model registry integration documented [INDUSTRY-CONSENSUS] |
| NHI-021 IoT / OT device identity | GAP | 0 | Not in documented scope [INDUSTRY-CONSENSUS] |
| NHI-022 Mainframe / midrange service identity | GAP | 0 | No RACF/ACF2/IBM-i integration documented [INDUSTRY-CONSENSUS] |
| NHI-023 Database encryption / TDE master key | GAP | 0 | Not in scope; no KMS/HSM key-management capability [INDUSTRY-CONSENSUS] |
| NHI-024 HSM / KMS operator / break-glass identity | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| NHI-025 Certificate authority operator identity | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| NHI-026 Backup / DR agent identity | GAP | 0 | No backup-agent integration documented [INDUSTRY-CONSENSUS] |
| NHI-027 Backend-for-frontend / OBO token holder | NATIVE | 3 | OAuth 2.0 token-exchange patterns supported; MCP User-Based Access Token for human-in-loop [aembit-credential-providers-2024] |
| NHI-028 Federated B2B / Open Banking client identity | ADD-ON | 1 | mTLS / X.509-SVID issuance available but no FAPI 2.0 or CDR-specific integration documented [aembit-credential-providers-2024] |
| NHI-029 Service-account-as-human (shared functional ID) | GAP | 0 | No detection or governance of shared-account patterns [INDUSTRY-CONSENSUS] |
| NHI-030 Browser / SaaS extension / OAuth-app identity | GAP | 0 | No OAuth-app inventory or discovery capability [INDUSTRY-CONSENSUS] |
| NHI-031 Webhook / inbound integration identity | GAP | 0 | Aembit brokers outbound; no inbound webhook verification feature [INDUSTRY-CONSENSUS] |
| NHI-032 Network / infrastructure device identity | GAP | 0 | No TACACS+/RADIUS/SNMPv3 integration documented [INDUSTRY-CONSENSUS] |
| NHI-033 Print / spooler / branch-peripheral identity | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| NHI-034 Quantum-resistant / hybrid-PKI identity | GAP | 0 | No PQC / hybrid-cert capability documented [INDUSTRY-CONSENSUS] |
| NHI-035 Vault-internal / secrets-broker identity | ADD-ON | 2 | Aembit can use Vault as upstream credential source; Aembit's own Edge/Cloud identities not self-governed [aembit-credential-providers-2024] |
| NHI-036 Ephemeral workload via SPIFFE / Aembit / Clutch | NATIVE | 4 | This is Aembit's primary identity model; SPIFFE SVID issuance + attestation-gated JIT brokering [aembit-arch-2024][aembit-spiffe-2025] |
| NHI-037 Forgotten / orphaned legacy identity | GAP | 0 | No NHI discovery, orphan sweep, or dormancy detection capability [INDUSTRY-CONSENSUS] |

**NHI summary:** NATIVE=12, ADD-ON=8, GAP=17, N/A=0.

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Coverage | Maturity | Evidence |
|-------|----------|----------|---------- |
| UC-F-001 Prevent plaintext secrets in repos | GAP | 0 | Aembit does not scan repos or enforce pre-commit hooks [INDUSTRY-CONSENSUS] |
| UC-F-002 Detect/remediate secrets in history | GAP | 0 | No secrets-scanning capability [INDUSTRY-CONSENSUS] |
| UC-F-003 JIT short-lived cloud credentials (OIDC) | NATIVE | 4 | Core capability: AWS/Azure/GCP WIF trust providers + STS/WIF credential issuance at runtime [aembit-trust-providers-2024] |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | NATIVE | 4 | Attestation-based identity foundation; JWT-SVID and X.509-SVID issuance; integrates with SPIRE [aembit-spiffe-2025] |
| UC-F-005 Dynamic database credentials | NATIVE | 3 | PostgreSQL, MySQL, Snowflake JIT credential injection via Edge proxy [aembit-snowflake-case-study-2024] |
| UC-F-006 Automated rotation of long-lived static secrets | ADD-ON | 2 | JIT brokering replaces rotation for supported targets; no bulk rotation pipeline for unmanaged legacy secrets [aembit-arch-2024] |
| UC-F-007 Immediate revocation on compromise | NATIVE | 3 | Policy-based immediate revocation; short-lived tokens expire naturally; no long-lived tokens to revoke [aembit-agentic-ai-ga-2026] |
| UC-F-008 K8s secret consumption without on-disk plaintext | NATIVE | 3 | Edge proxy injects credentials at request-time; K8s SA trust provider for pod attestation [aembit-trust-providers-2024] |
| UC-F-009 Container image-pull credentials per workload | GAP | 0 | No image registry credential management [INDUSTRY-CONSENSUS] |
| UC-F-010 IaC / config-mgmt secrets at apply-time | NATIVE | 3 | Terraform Cloud trust provider + Terraform provider for policy-as-code; credential injected at apply time [aembit-trust-providers-2024] |
| UC-F-011 Observability-agent credentials rotated | GAP | 1 | API-key credential type available but no observability-agent-specific rotation pipeline [INDUSTRY-CONSENSUS] |
| UC-F-012 Message-broker client identity hardening | GAP | 1 | No Kafka/RabbitMQ/Service Bus integration; OAuth/JWT injection generically possible [INDUSTRY-CONSENSUS] |
| UC-F-013 gMSA / Kerberos modernisation for AD accounts | ADD-ON | 2 | Kerberos trust provider attests Windows workloads; does not directly manage AD passwords or gMSA [aembit-ms-environments-2025] |
| UC-F-014 API-gateway upstream identity standardised | ADD-ON | 2 | JWT/OAuth injection into upstream HTTP; no dedicated API-gateway connector [aembit-credential-providers-2024] |
| UC-F-015 RPA bot credentials vaulted, session-bound | GAP | 0 | No RPA orchestrator integration documented [INDUSTRY-CONSENSUS] |
| UC-F-016 Keyless code/artifact signing in CI | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| UC-F-017 TEE attestation gates secret release | GAP | 0 | No TEE/enclave attestation integration documented [INDUSTRY-CONSENSUS] |
| UC-F-018 AI-agent / LLM tool-credential brokering | NATIVE | 4 | Blended Identity + MCP Identity Gateway GA April 2026; per-task JIT token exchange without exposing creds [aembit-agentic-ai-ga-2026] |
| UC-F-019 IoT / OT / branch device identity enrolment | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| UC-F-020 Mainframe / midrange credential rotation | GAP | 0 | No mainframe integration documented [INDUSTRY-CONSENSUS] |
| UC-F-021 Backup / DR agent identity de-privileging | GAP | 0 | No backup-agent integration [INDUSTRY-CONSENSUS] |
| UC-F-022 Webhook inbound identity verification | GAP | 0 | Aembit is outbound-broker only; no inbound webhook verification [INDUSTRY-CONSENSUS] |
| UC-F-023 Network-device credential modernisation | GAP | 0 | No TACACS+/RADIUS/SNMPv3 integration [INDUSTRY-CONSENSUS] |
| UC-F-024 Open Banking / FAPI 2.0 mTLS partner identity | ADD-ON | 1 | X.509-SVID issuance available; no FAPI 2.0 / CDR-specific workflow documented [aembit-credential-providers-2024] |
| UC-F-025 OAuth-app / marketplace integration governance | GAP | 0 | No OAuth-app inventory or governance capability [INDUSTRY-CONSENSUS] |
| UC-F-026 Vault-internal identity hardening | ADD-ON | 2 | Aembit Edge/Cloud have their own identity model; Vault used as upstream; no self-hardening tooling documented [aembit-credential-providers-2024] |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | GAP | 0 | No NHI discovery or dormancy sweep capability [INDUSTRY-CONSENSUS] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | GAP | 0 | No secrets-scanning or sprawl-detection analytics [INDUSTRY-CONSENSUS] |
| UC-N-002 NHI inventory and ownership attestation | ADD-ON | 2 | Access audit logs provide workload-level activity; no full NHI discovery/ownership inventory [aembit-arch-2024] |
| UC-N-003 Rotation-coverage and freshness KPIs | ADD-ON | 2 | Authorization event logs track credential issuance; no rotation-coverage reporting for unmanaged secrets [aembit-arch-2024] |
| UC-N-004 Regulator audit evidence pack | ADD-ON | 2 | Structured audit logs; no one-click APRA CPS 234 evidence-pack builder [aembit-arch-2024] |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Zero-trust access policy model aligns with ZT pillars; no E8 scorecard tooling [aembit-wiam-guide-2024] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | GAP | 0 | No supply-chain risk scoring capability [INDUSTRY-CONSENSUS] |
| UC-N-007 Data-sovereignty and residency assurance | GAP | 1 | SaaS-only; no AU/APAC region documented; SOC 2 + ISO 27001 help but no data-residency election [aembit-soc2-recert-2025] |
| UC-N-008 Engineer training and secure-coding adoption KPI | GAP | 0 | No training platform [INDUSTRY-CONSENSUS] |
| UC-N-009 Exception register and risk-acceptance governance | GAP | 0 | No GRC-integrated exception register [INDUSTRY-CONSENSUS] |
| UC-N-010 Break-glass and quorum-operator governance | GAP | 0 | No PAM-style break-glass workflow [INDUSTRY-CONSENSUS] |
| UC-N-011 Post-incident reporting and identity-driven RCA | ADD-ON | 2 | Authorization audit logs and workload activity tracking support RCA; no SOAR integration documented [aembit-arch-2024] |
| UC-N-012 Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| UC-N-013 Crypto-agility and PQC readiness reporting | GAP | 0 | No PQC capability [INDUSTRY-CONSENSUS] |
| UC-N-014 Vendor-evaluation matrix maintenance | GAP | 0 | Not a platform-level capability [INDUSTRY-CONSENSUS] |
| UC-N-015 Communications / stakeholder cadence | GAP | 0 | Not a platform-level capability [INDUSTRY-CONSENSUS] |
| UC-N-016 IoT / OT / branch-fleet posture reporting | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| UC-N-017 Observability / telemetry secret-leak governance | GAP | 0 | No telemetry-scrubbing or log-audit capability [INDUSTRY-CONSENSUS] |
| UC-N-018 Confidential-computing / TEE attestation assurance | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | NATIVE | 3 | Blended Identity audit logs, per-tool credential issuance volume, attribution across human/agent actions [aembit-agentic-ai-ga-2026] |
| UC-N-020 Mainframe / legacy posture and exception transparency | GAP | 0 | Not in scope [INDUSTRY-CONSENSUS] |

**UC summary:** NATIVE=8, ADD-ON=13, GAP=26, N/A=0.

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **Industry-leading workload attestation and JIT brokering (NHI-036, UC-F-003/004/005).** Aembit's core WIAM architecture is purpose-built for NHI-036: it attests workloads via 13 trust-provider types and injects short-lived credentials at the moment of access without any secrets stored in application code or environment variables. The Snowflake case study demonstrates 85% reduction in credential workload. This is a Maturity 4 capability for modern cloud/K8s estates.

2. **AI agent identity — most differentiated capability in the evaluation pool (NHI-019, UC-F-018, UC-N-019).** Blended Identity (cryptographic agent-plus-human binding) and the MCP Identity Gateway (OAuth 2.1 + token exchange without agent-side secret exposure) reached GA at RSA Conference April 2026. Aembit is explicitly named in NHI-036 taxonomy entry as an exemplar. With pricing starting at $20/agent/month this is market-ready. No other single vendor in this evaluation combines workload attestation with agentic identity at this maturity level.

3. **Conditional access with real-time posture signals.** Geo-IP, time-based, CrowdStrike Falcon posture, and Wiz security-findings conditions are all NATIVE. This MFA-strength, policy-driven access model for NHIs closes a gap that static-credential vaults leave open. CrowdStrike co-investment (via Falcon Fund) provides a tight integration pathway.

### Top 3 gaps

1. **No secrets discovery, scanning, or NHI inventory (UC-F-001/002/027, UC-N-001/002).** Aembit does not scan repositories, detect plaintext secrets, sweep for orphans, or produce a full NHI inventory. Pairing with a discovery-led NHI platform (Oasis, Entro, Astrix) is required for full coverage.

2. **AU sovereignty — critical blocker for APRA-regulated deployment.** SaaS-only control plane, no AU data residency region, no IRAP assessment. Control-plane traffic and audit logs transit US-hosted infrastructure. APRA CPS 234 §22 requires demonstrable data-flow control.

3. **Narrow target coverage for enterprise long-tail.** Mainframe (NHI-022), IoT/OT (NHI-021), backup agents (NHI-026), network devices (NHI-032), RPA bots (NHI-014), and message brokers (NHI-011) are all GAP. Aembit is purpose-built for modern cloud/K8s/AI workloads and does not address the legacy long-tail central to Cluster C use cases.

---

## 6. AU-specific notes (≤ 150 words)

Aembit has **no documented Australian presence** as at profile date (May 2026). The Aembit Cloud control plane is a US-hosted SaaS service; no AU/APAC region option is listed on the website or in documentation. No IRAP assessment (PROTECTED or OFFICIAL) has been announced. No APRA CPS 234 or Essential 8 mapping is published. The Trust Center (trust.aembit.io) exposes SOC 2 Type II and ISO 27001:2022 reports but does not reference Australian regulatory frameworks.

**XYZ relevance:** Aembit Edge runs on-premise / in-cloud inside the customer's own AWS/Azure/GCP tenancy (no Australian VPC constraint), meaning the data-plane broker itself could be AU-hosted. However, the control plane (policy evaluation, audit logs) transits Aembit's US SaaS — a material APRA CPS 234 §22 and CPS 230 §39 gap. An AU sovereign-cloud deployment or private-plane offering would be required for production adoption by an APRA-regulated entity. [aembit-soc2-recert-2025][aembit-iso27001-2025]

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Aembit (Agent 03 wave 4)`.

---

## 8. Open questions for v1.0

1. **AU data residency roadmap:** Does Aembit have plans for an APAC/AU control-plane region? IRAP assessment timeline?
2. **Private / dedicated control plane:** Is an isolated Aembit Cloud tenancy available for regulated customers (analogous to CyberArk SaaS private-cloud)?
3. **SPIRE co-deployment specifics:** What exactly does Aembit integrate with in an existing SPIRE deployment — does it federate trust domains or replace SPIRE server entirely?
4. **Mainframe/legacy roadmap:** Any plans to extend trust providers to IBM z/OS or RACF, or to RPA orchestrators?
5. **Message-broker support:** Is Kafka mTLS credential injection on the roadmap given the K8s workload coverage?
6. **Conflict/complement with HashiCorp Vault Enterprise:** When a customer already has Vault Enterprise, is Aembit a layer-above broker or a replacement for the dynamic secrets engine?
7. **Aembit's own NHI hardening (NHI-035):** How is the Aembit Edge agent identity itself managed, rotated, and monitored?
8. **FAPI 2.0 / CDR alignment:** Can the OAuth 2.0 authorization-code flow support FAPI 2.0 sender-constrained token requirements for CDR Open Banking?

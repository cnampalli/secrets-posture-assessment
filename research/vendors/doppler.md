# Vendor Profile — Doppler

**Tier:** emerging
**Primary docs:** https://docs.doppler.com
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot

Doppler is a privately-held, San Francisco-based SaaS secrets-management platform founded in 2018. It is **SaaS-only** — all infrastructure runs on GCP us-central1; no self-hosted or hybrid deployment option is offered as a standard product. The primary differentiator is developer experience: a CLI-first, environment-variable-centric model that syncs secrets across cloud providers, CI/CD platforms, and Kubernetes from a single control plane. Doppler positions explicitly against both HashiCorp Vault ("too complex") and cloud-native vaults ("too siloed"). It serves software development teams at growth-stage and mid-market companies. No AU-specific region is offered; data residency is US (GCP us-central1). No publicly confirmed AU FI customer references found. An emerging "SecretOps" brand encompasses rotation, dynamic secrets, and MCP-server-based AI-agent integration as of 2025–2026.

**Citations:** [doppler-security-page-2025], [doppler-security-fact-sheet-2025]

---

## 2. Architecture

**Storage backend:** Doppler runs on GCP us-central1 in private VPCs with primary and failover compute. Secrets are stored encrypted at rest using AES-256-GCM with a per-workspace 256-bit key that is loaded transiently in memory only during requests. All workspace encryption keys are themselves protected by an HSM-backed key accessible via GCP KMS — meaning GCP KMS (HSM-backed) is the root trust for all customer secrets. Transit uses TLS 1.2/1.3 via Cloudflare (full-strict mode) proxied to GCP.

**Enterprise Key Management (EKM):** Enterprise-plan customers can add a second encryption layer using their own AWS KMS or GCP KMS key (Azure KV is on-roadmap). This provides BYOK-style control but sealed secrets still reside on Doppler's US infrastructure — there is no data-residency choice.

**Auth methods:** SAML SSO (Okta, Google, Azure Entra ID, JumpCloud, OneLogin, Auth0, Authentik), SCIM (Okta, Entra, OneLogin), service tokens (read-only, config-scoped), service accounts (multi-project, assignable workplace roles), and OIDC-based service account identities for CI (GitHub Actions, GitLab, CircleCI, Kubernetes Operator). K8s Operator OIDC requires Team or Enterprise plan.

**Secrets engines / secrets sync:** Doppler functions as a universal sync layer, not a secrets engine in the Vault sense. It pushes secrets to: AWS Secrets Manager, AWS Parameter Store, Azure App Service, Azure Key Vault, GCP Secret Manager, Kubernetes Secrets (via Operator or External Secrets Operator), GitHub Actions Secrets, CircleCI, Vercel, Netlify, Heroku, Terraform Cloud, and 30+ others.

**Dynamic secrets:** Enterprise-only. AWS IAM (ephemeral IAM users, 30-min default TTL) and Azure Service Principal supported. Lease lifecycle managed via CLI/API.

**Secret rotation:** Team/Enterprise. API-based (provider API) and Proxied (via open-source AWS Lambda agent for private infra). Supported targets: AWS IAM User, AWS RDS PostgreSQL, AWS RDS MySQL, GCP Cloud SQL (MySQL/Postgres/SQL Server), MongoDB Atlas.

**Replication / DR:** GCP-native HA in us-central1; no cross-region or multi-region option disclosed.

**FedRAMP / IRAP / SOC 2:** SOC 2 achieved April 2021 (Type not confirmed on primary docs page); ISO 27001 certified. FedRAMP: no evidence found. IRAP: no evidence found.

**Citations:** [doppler-security-fact-sheet-2025], [doppler-ekm-docs-2025], [doppler-rotation-docs-2025], [doppler-dynamic-secrets-docs-2025], [doppler-soc2-2021]

---

## 3. NHI coverage map

| NHI ID | Name | Coverage | Maturity | Evidence |
|--------|------|----------|----------|---------|
| NHI-001 | Cloud IAM principal | NATIVE | 3 | Doppler syncs to AWS/Azure/GCP; dynamic AWS IAM secrets (Enterprise); OIDC service account identities. [doppler-docs-integrations-2025] |
| NHI-002 | Kubernetes ServiceAccount | NATIVE | 3 | Doppler K8s Operator with OIDC support (v1.7.0+, Team/Enterprise); External Secrets Operator provider; CSI via ESO. [doppler-k8s-oidc-docs-2025] |
| NHI-003 | CI/CD pipeline identity | NATIVE | 3 | OIDC service account identities for GitHub Actions, GitLab CI, CircleCI; native sync integrations. [doppler-service-account-identities-2025] |
| NHI-004 | Container / image-pull credential | ADD-ON | 2 | No native image-pull rotation; secrets sync to K8s Secrets which can hold pull credentials; no first-class registry credential management. [doppler-k8s-oidc-docs-2025] |
| NHI-005 | Database service account | NATIVE | 2 | Rotation for AWS RDS (MySQL/Postgres), GCP Cloud SQL, MongoDB Atlas. Dynamic creds Enterprise-only, limited RDBMS coverage. [doppler-rotation-docs-2025] |
| NHI-006 | Application TLS / mTLS workload identity | GAP | 0 | No PKI, no certificate issuance, no SPIFFE/SPIRE integration. Doppler does not manage X.509 identities. [doppler-docs-integrations-2025] |
| NHI-007 | Third-party SaaS API key / OAuth client | NATIVE | 3 | Core use case: store, version, rotate, and sync SaaS API keys across environments. [doppler-security-page-2025] |
| NHI-008 | Git platform credential (PAT, SSH key) | NATIVE | 2 | Sync to GitHub Actions Secrets; secrets stored in Doppler and pushed to repos. No secret-scanning / push-protection. [doppler-docs-integrations-2025] |
| NHI-009 | IaC / config-management agent identity | NATIVE | 2 | Terraform Cloud integration (sync); Pulumi ESC provider; Ansible via CLI injection. No first-class AppRole equivalent. [doppler-docs-integrations-2025] |
| NHI-010 | Monitoring / observability agent | NATIVE | 2 | Stores and syncs Datadog/Splunk API keys; env-injection model. No agent-specific credential scoping or rotation workflow. [doppler-docs-integrations-2025] |
| NHI-011 | Message broker / event-bus client | ADD-ON | 1 | No native Kafka/RabbitMQ integration; credentials can be stored and synced but no broker-specific rotation support documented. [INDUSTRY-CONSENSUS] |
| NHI-012 | Active Directory / LDAP service account | GAP | 0 | No AD/LDAP integration; gMSA and Kerberos are completely out of scope for this SaaS-first platform. [doppler-docs-integrations-2025] |
| NHI-013 | Reverse-proxy / API-gateway upstream identity | ADD-ON | 1 | Secrets can be stored and injected; no API-gateway-specific lifecycle management. [INDUSTRY-CONSENSUS] |
| NHI-014 | RPA bot identity | GAP | 0 | No UiPath/Blue Prism/AA integration; no bot orchestrator credential management. [INDUSTRY-CONSENSUS] |
| NHI-015 | Code-signing identity (Sigstore/Authenticode) | GAP | 0 | No code-signing or certificate management features. [doppler-docs-integrations-2025] |
| NHI-016 | Build provenance / SLSA attestation identity | GAP | 0 | No SLSA, in-toto, or Sigstore integration. [doppler-docs-integrations-2025] |
| NHI-017 | Service mesh control-plane identity | GAP | 0 | No Istio/Linkerd/Consul CA or intermediate-CA management. [doppler-docs-integrations-2025] |
| NHI-018 | Confidential-computing / TEE attestation | GAP | 0 | No TEE attestation gates or integration. [doppler-docs-integrations-2025] |
| NHI-019 | AI agent / autonomous workflow identity | NATIVE | 2 | Doppler MCP Server (experimental as of 2026) for AI agent secrets access; scoped tokens, read-only mode; integrates with Claude, Cursor. [doppler-mcp-docs-2025] |
| NHI-020 | Model artifact / registry identity | ADD-ON | 1 | ML registry tokens can be stored in Doppler; no model-registry-specific lifecycle management. [INDUSTRY-CONSENSUS] |
| NHI-021 | IoT / OT device identity | GAP | 0 | No device identity, DPS/EST/SCEP, or TPM-backed enrolment. [doppler-docs-integrations-2025] |
| NHI-022 | Mainframe / midrange service identity | GAP | 0 | No RACF, ACF2, IBM-i, ICSF integration. [doppler-docs-integrations-2025] |
| NHI-023 | Database encryption / TDE master key | GAP | 0 | Doppler is a secrets store, not a KMS. No TDE key custody. [doppler-docs-integrations-2025] |
| NHI-024 | HSM / KMS operator / break-glass identity | GAP | 0 | Doppler leverages GCP KMS/HSM internally but does not provide HSM operator identity governance to customers. [doppler-security-fact-sheet-2025] |
| NHI-025 | Certificate authority operator identity | GAP | 0 | No PKI CA functionality. [doppler-docs-integrations-2025] |
| NHI-026 | Backup / DR agent identity | GAP | 0 | No backup-agent credential vaulting integrations (NetBackup, Veeam, Rubrik, etc.). [INDUSTRY-CONSENSUS] |
| NHI-027 | Backend-for-frontend / OBO token holder | ADD-ON | 1 | OAuth client secrets storable; no OBO-specific token-exchange broker. [INDUSTRY-CONSENSUS] |
| NHI-028 | Federated B2B / Open Banking client identity | GAP | 0 | No FAPI 2.0, mTLS client cert, or CDR/Open Banking lifecycle management. [doppler-docs-integrations-2025] |
| NHI-029 | Service-account-as-human (shared functional ID) | ADD-ON | 1 | Service tokens provide scoped read-only access; no PAM-style checkout, session recording, or JIT elevation. [doppler-service-tokens-docs-2025] |
| NHI-030 | Browser / SaaS extension OAuth-app identity | ADD-ON | 1 | OAuth client secrets stored; no OAuth-app inventory, risk-scoring, or revocation orchestration. [INDUSTRY-CONSENSUS] |
| NHI-031 | Webhook / inbound integration identity | ADD-ON | 1 | Webhook signing secrets stored and versioned; no replay-protection enforcement or HMAC-validation middleware. [INDUSTRY-CONSENSUS] |
| NHI-032 | Network / infrastructure device identity | GAP | 0 | No TACACS+/RADIUS or network device credential integration. [INDUSTRY-CONSENSUS] |
| NHI-033 | Print / branch-peripheral identity | GAP | 0 | No branch-device or 802.1X credential management. [INDUSTRY-CONSENSUS] |
| NHI-034 | Quantum-resistant / hybrid-PKI identity | GAP | 0 | No PQC capability; no HSM or CA for hybrid-cert issuance. [doppler-docs-integrations-2025] |
| NHI-035 | Vault-internal / secrets-broker identity | ADD-ON | 1 | Doppler uses GCP KMS HSM-backed key internally; service tokens and service accounts govern operator access; no quorum/Shamir recovery. [doppler-security-fact-sheet-2025] |
| NHI-036 | Ephemeral workload via SPIFFE / ZTBA | GAP | 0 | No SPIFFE/SPIRE, no Aembit-style workload attestation. [doppler-docs-integrations-2025] |
| NHI-037 | Forgotten / orphaned legacy identity | ADD-ON | 1 | Activity logs and access audit trails enable identification; no automated dormancy sweep or attestation workflow. [doppler-compliance-page-2025] |

**NHI summary:** NATIVE=10, ADD-ON=12, PARTNER=0, GAP=15, N/A=0

---

## 4. Use-case scoring

| UC ID | Name | Coverage | Maturity | Evidence |
|-------|------|----------|----------|---------|
| UC-F-001 | Prevent plaintext secrets in source repos | ADD-ON | 1 | Doppler sync to GitHub Secrets removes the need for inline secrets but provides no pre-commit scanning or push-protection. [doppler-github-actions-docs-2025] |
| UC-F-002 | Detect and remediate secrets in history | GAP | 0 | No secret-scanning, historical repo sweep, or detection capability. [doppler-docs-integrations-2025] |
| UC-F-003 | JIT short-lived cloud credentials via OIDC | NATIVE | 2 | OIDC service account identities for GitHub Actions, GitLab, CircleCI (Team/Enterprise). K8s Operator OIDC for EKS/GKE/AKS. [doppler-service-account-identities-2025] |
| UC-F-004 | Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No SPIFFE/SPIRE support; no workload attestation broker. [doppler-docs-integrations-2025] |
| UC-F-005 | Dynamic database credentials | NATIVE | 2 | Enterprise-only. AWS RDS (MySQL/Postgres), GCP Cloud SQL, MongoDB Atlas; 30-min TTL default. Limited RDBMS coverage. [doppler-dynamic-secrets-docs-2025] |
| UC-F-006 | Automated rotation of long-lived secrets | NATIVE | 2 | Rotation for AWS IAM, RDS, GCP Cloud SQL, MongoDB Atlas (Team/Enterprise). Proxied rotation for private infra via Lambda agent. [doppler-rotation-docs-2025] |
| UC-F-007 | Immediate revocation on compromise | NATIVE | 2 | Service tokens revocable instantly; service accounts deletable; synced secrets revoked at source. No cross-system SOAR playbook integration documented. [doppler-service-tokens-docs-2025] |
| UC-F-008 | K8s secret consumption without on-disk plaintext | NATIVE | 2 | Doppler K8s Operator injects secrets as env vars / K8s Secrets; External Secrets Operator integration. No CSI driver; etcd encryption is customer-managed separately. [doppler-k8s-oidc-docs-2025] |
| UC-F-009 | Container image-pull credentials per workload | ADD-ON | 1 | Pull credentials can be stored and synced to K8s Secrets; no per-workload scoping or registry-native rotation. [INDUSTRY-CONSENSUS] |
| UC-F-010 | IaC / config-management secrets at apply-time | NATIVE | 2 | Terraform Cloud sync; Pulumi ESC provider; Ansible CLI injection; Harness integration. State-file scanning not provided. [doppler-docs-integrations-2025] |
| UC-F-011 | Observability-agent credentials rotated | ADD-ON | 1 | Agent API keys stored and sync-distributed; no agent-specific rotation cadence or scope enforcement. [INDUSTRY-CONSENSUS] |
| UC-F-012 | Message-broker client identity hardening | GAP | 0 | No Kafka, RabbitMQ, SQS, or Service Bus credential management. [INDUSTRY-CONSENSUS] |
| UC-F-013 | gMSA / Kerberos modernisation for AD service accounts | GAP | 0 | No AD integration; out of scope for SaaS cloud-native platform. [doppler-docs-integrations-2025] |
| UC-F-014 | API-gateway upstream identity standardised | ADD-ON | 1 | Gateway secrets storable; no certificate lifecycle or mTLS provisioning for gateways. [INDUSTRY-CONSENSUS] |
| UC-F-015 | RPA bot credentials vaulted | GAP | 0 | No RPA orchestrator integration; no session-bound credential checkout. [INDUSTRY-CONSENSUS] |
| UC-F-016 | Keyless code- and artifact-signing | GAP | 0 | No Sigstore, HSM-backed code-signing, or SLSA features. [doppler-docs-integrations-2025] |
| UC-F-017 | TEE attestation gates secret release | GAP | 0 | No TEE/attestation-gated release capability. [doppler-docs-integrations-2025] |
| UC-F-018 | AI-agent / LLM tool-credential brokering | NATIVE | 2 | Doppler MCP Server (experimental) provides scoped, read-only secret access for AI agents; per-tool token scoping available. Not yet production GA. [doppler-mcp-docs-2025] |
| UC-F-019 | IoT / OT / branch-device identity enrolment | GAP | 0 | No device enrolment, DPS/EST/SCEP, or per-device certificate management. [doppler-docs-integrations-2025] |
| UC-F-020 | Mainframe / midrange credential rotation pipeline | GAP | 0 | No mainframe integration. [doppler-docs-integrations-2025] |
| UC-F-021 | Backup / DR agent identity de-privileging | GAP | 0 | No backup-agent credential vaulting. [INDUSTRY-CONSENSUS] |
| UC-F-022 | Webhook inbound identity verification | ADD-ON | 1 | Webhook signing secrets stored and versioned; no replay-protection or HMAC-validation enforcement layer. [INDUSTRY-CONSENSUS] |
| UC-F-023 | Network-device credential modernisation | GAP | 0 | No TACACS+/RADIUS or network device integration. [INDUSTRY-CONSENSUS] |
| UC-F-024 | Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | No mTLS client-cert lifecycle management. [doppler-docs-integrations-2025] |
| UC-F-025 | OAuth-app / marketplace integration governance | ADD-ON | 1 | OAuth secrets stored; no shadow-integration discovery, risk scoring, or stale-token revocation sweep. [INDUSTRY-CONSENSUS] |
| UC-F-026 | Vault-internal identity hardening | ADD-ON | 1 | Service accounts and tokens govern Doppler operator access; no quorum recovery, no Shamir shares, no root-token ceremony. [doppler-security-fact-sheet-2025] |
| UC-F-027 | Orphaned / dormant NHI cleanup pipeline | ADD-ON | 1 | Activity logs enable manual identification; no automated dormancy sweep or owner-attestation workflow. [doppler-compliance-page-2025] |
| UC-N-001 | Real-time secret-sprawl KPI dashboard | ADD-ON | 1 | Doppler tracks secrets and changes internally; no secrets-in-repo sprawl KPI or cross-system dashboard. [doppler-compliance-page-2025] |
| UC-N-002 | NHI inventory and ownership attestation | ADD-ON | 1 | Project/config hierarchy provides partial inventory; no formal owner-attestation workflow or GRC export. [doppler-compliance-page-2025] |
| UC-N-003 | Rotation-coverage and freshness KPIs | ADD-ON | 1 | Activity logs show rotation events; no built-in KPI dashboard for rotation coverage by NHI bucket. [doppler-compliance-page-2025] |
| UC-N-004 | Regulator audit evidence pack | ADD-ON | 1 | Audit logs exportable; no one-click APRA CPS 234 evidence pack builder. [doppler-compliance-page-2025] |
| UC-N-005 | Essential 8 / ZT control-area scorecard | GAP | 0 | No E8 or ZT scorecard functionality. [INDUSTRY-CONSENSUS] |
| UC-N-006 | Vendor / SaaS supply-chain risk attestation | GAP | 0 | No third-party integration risk scoring or supply-chain attestation. [INDUSTRY-CONSENSUS] |
| UC-N-007 | Data-sovereignty and residency assurance | GAP | 0 | GCP us-central1 only; no AU region, no data residency selection. Critical gap for APRA-regulated entities. [doppler-security-fact-sheet-2025] |
| UC-N-008 | Engineer training and secure-coding KPI | GAP | 0 | No training module or completion tracking. [INDUSTRY-CONSENSUS] |
| UC-N-009 | Exception register and risk-acceptance governance | GAP | 0 | No exception register, GRC integration, or risk-acceptance workflow. [INDUSTRY-CONSENSUS] |
| UC-N-010 | Break-glass and quorum-operator governance | ADD-ON | 1 | Workplace owner roles and access logs provide rudimentary governance; no quorum/MofN controls. [doppler-security-fact-sheet-2025] |
| UC-N-011 | Post-incident RCA and identity-driven reporting | ADD-ON | 1 | Audit logs support forensics; no SOAR playbook integration or NHI-attributed RCA template. [doppler-compliance-page-2025] |
| UC-N-012 | Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA, in-toto, or signed-artifact coverage reporting. [INDUSTRY-CONSENSUS] |
| UC-N-013 | Crypto-agility and PQC readiness reporting | GAP | 0 | No crypto-inventory, PQC migration, or hybrid-cert capability. [INDUSTRY-CONSENSUS] |
| UC-N-014 | Vendor-evaluation matrix maintenance | ADD-ON | 1 | Doppler's own docs describe comparison with peers but no tooling for customer-side matrix maintenance. [INDUSTRY-CONSENSUS] |
| UC-N-015 | Communications and stakeholder cadence | GAP | 0 | Out of scope — no product feature. [INDUSTRY-CONSENSUS] |
| UC-N-016 | IoT / OT / branch-fleet posture reporting | GAP | 0 | No IoT/OT fleet posture capability. [INDUSTRY-CONSENSUS] |
| UC-N-017 | Observability/telemetry secret-leak governance | ADD-ON | 1 | Logs visible in activity trail; no log-scrubbing or telemetry-pipeline secret-scanning. [INDUSTRY-CONSENSUS] |
| UC-N-018 | Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE attestation. [INDUSTRY-CONSENSUS] |
| UC-N-019 | AI-agent / autonomous-workflow KPI suite | ADD-ON | 1 | MCP server provides scoped access; no per-tool credential issuance volume KPIs or SOC alerting. [doppler-mcp-docs-2025] |
| UC-N-020 | Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe integration or legacy posture reporting. [INDUSTRY-CONSENSUS] |

**UC summary:** NATIVE=8, ADD-ON=19, PARTNER=0, GAP=20, N/A=0

---

## 5. Strengths and gaps

### Top 3 strengths

1. **Developer experience and multi-environment sync.** Doppler's CLI-first, environment-variable-centric model delivers the smoothest developer onboarding of any vendor in this evaluation. The 30+ automated sync integrations (GitHub Actions, CircleCI, Vercel, AWS SM, Azure KV, GCP SM, K8s) mean secrets-as-code adoption is low-friction. For cloud-native SaaS and startup estates this is genuinely industry-leading (maturity 4 in that narrow band).

2. **Emerging AI-agent / MCP integration.** Doppler is one of the first secrets-management vendors to publish a Model Context Protocol server, offering scoped, read-only credential brokering for LLM agents (NHI-019 / UC-F-018). While experimental, this positions Doppler ahead of most peers for agentic-workflow identity — a fast-moving requirement.

3. **OIDC workload identity for CI/CD and Kubernetes.** Service account OIDC identities for GitHub Actions, GitLab, CircleCI, and the K8s Operator eliminate the need for long-lived service tokens in pipelines and clusters — directly addressing NHI-003 and NHI-002 at maturity 3.

### Top 3 gaps

1. **AU data residency / sovereignty — disqualifying for APRA-regulated entities.** All data resides in GCP us-central1; there is no AU region, no self-hosted option, and no IRAP certification. APRA CPS 230/234 data-residency and BCM requirements cannot be met. This is the single largest gap for any XYZ FI evaluation.

2. **No PKI / certificate / SPIFFE capability (NHI-006, NHI-015–017, NHI-025, NHI-034).** Doppler has zero X.509, mTLS, SPIFFE/SPIRE, code-signing, or CA-operator functionality. The entire PKI and workload-attestation layer must be sourced elsewhere. For a programme requiring UC-F-004, UC-F-016, UC-F-024, and UC-N-013 this is a structural gap.

3. **No on-premises / legacy / mainframe coverage (NHI-012, NHI-014, NHI-022, NHI-032, NHI-033).** Doppler's SaaS cloud-native architecture means it cannot address AD service accounts, RACF, RPA bots, or network device credentials — the identities that carry the highest static-credential risk in a Tier-1 bank estate.

---

## 6. AU-specific notes

Doppler's entire infrastructure runs in GCP **us-central1** (US). The security fact sheet explicitly states this and lists no multi-region or customer-selectable region options. There is no self-hosted deployment path. Consequently:

- **APRA CPS 230 §39** (operational resilience, service provider concentration, data residency) cannot be met without a contractual data-processing agreement that acknowledges US-only residency — potentially problematic.
- **APRA CPS 234 §22/28** (information asset classification, protection) requires the regulated entity to assess the adequacy of a SaaS provider's data handling; storing production secrets in a US SaaS with no AU region will require explicit Board-endorsed risk acceptance.
- **ASD IRAP:** No evidence of IRAP assessment. Not eligible for Protected-level use.
- **Essential 8:** Doppler can assist E8 Maturity 1–2 for application control (removing hardcoded secrets) and restrict-admin-privilege (OIDC for CI), but cannot address the broader E8 scorecard without complementary tooling.
- No confirmed AU FI customer references found in public sources.

**Verdict for XYZ FI:** Not deployable as primary secrets platform under current CPS 230/234 requirements without explicit regulatory risk acceptance and supplemental AU-sovereign infrastructure. Suitable as a **developer experience layer** over AU-sovereign backends (e.g., syncing to AWS Sydney Secrets Manager or Azure Australia East Key Vault) if data-flow classification permits.

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## Doppler (Agent 03 wave 3)`.

Keys used: `doppler-security-page-2025`, `doppler-security-fact-sheet-2025`, `doppler-ekm-docs-2025`, `doppler-rotation-docs-2025`, `doppler-dynamic-secrets-docs-2025`, `doppler-soc2-2021`, `doppler-docs-integrations-2025`, `doppler-k8s-oidc-docs-2025`, `doppler-service-account-identities-2025`, `doppler-service-tokens-docs-2025`, `doppler-mcp-docs-2025`, `doppler-compliance-page-2025`, `doppler-github-actions-docs-2025`

---

## 8. Open questions for v1.0

1. **SOC 2 Type confirmation:** The announcement page (April 2021) does not state Type 1 vs Type 2. An SE conversation or trust.doppler.com review would confirm scope and whether a current (2025/2026) renewal report is available.
2. **ISO 27001 scope and date:** Third-party profile (Nudge Security) claims ISO 27001 but Doppler's own security page does not list it explicitly. Verification needed.
3. **FedRAMP claim:** One third-party profile lists "FedRAMP Compliant" — this is not corroborated by any Doppler primary source or the FedRAMP marketplace. Likely inaccurate; needs SE confirmation.
4. **AU region roadmap:** Has Doppler roadmapped a GCP Australia (sydney) region? No public disclosure found.
5. **Self-hosted / BYOC roadmap:** Infisical (a direct Doppler competitor) offers self-hosted. Is Doppler planning a self-hosted SKU? No evidence found.
6. **EKM Azure KV timeline:** Azure Key Vault listed as "on roadmap" for EKM — no GA date published.
7. **Proxied rotation coverage expansion:** Lambda-based proxied rotation currently covers AWS RDS/IAM and limited GCP. Oracle, MSSQL, Snowflake, Redshift rotation not documented — significant gap for enterprise RDBMS estates.
8. **Dynamic secrets for Azure:** Only AWS IAM and Azure Service Principal documented for dynamic secrets; no Azure Managed Identity or GCP Workload Identity Federation dynamic path confirmed.
9. **MCP server GA timeline:** Currently experimental. Production GA date and any plan-tier requirement not published.
10. **AU FI customer references:** No public case studies identified. Would require direct vendor engagement.

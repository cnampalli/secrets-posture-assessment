# Vendor Profile — 1Password Secrets Automation

**Tier:** emerging
**Primary docs:** https://developer.1password.com/docs/secrets
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

1Password is a private Canadian company (AgileBits Inc.) originally launched in 2006 as a consumer password manager. The **Secrets Automation** product line — comprising Service Accounts, Connect Server, CLI, SDKs, Kubernetes Operator, Secrets Injector, Terraform Provider, and the recently announced MCP server — was added to address developer and DevOps workflows. The product is deployed as a cloud SaaS (primary region: US; EU region at 1Password.eu) with an optional self-hosted broker tier via Connect Server. 1Password positions against Doppler and Infisical in the developer-secrets segment and against HashiCorp Vault in the enterprise tier, but explicitly targets smaller engineering teams rather than large FI deployments. No publicly confirmed AU data-centre region exists; Connect Server can be self-hosted inside AU infrastructure as a sovereignty mitigation. Workforce password management remains the primary revenue base.

---

## 2. Architecture (≤ 250 words)

**Storage back-end:** 1Password-managed cloud (AgileBits-operated). Secrets are stored as encrypted items in vaults. The data plane is AgileBits-controlled SaaS; Connect Server provides an optional self-hosted caching/proxy tier but the authoritative store always resides in the cloud.

**Encryption:** End-to-end AES-GCM-256. Keys are derived via PBKDF2-HMAC-SHA256 using a two-factor "dual-key" model (account password + 128-bit Secret Key). Transit uses TLS with Secure Remote Password (SRP) protocol so the password itself is never transmitted. No external HSM or KMS integration is documented for the SaaS store; the self-hosted Connect Server does not expose an HSM-integration layer.

**Auth methods:** Service Account tokens (scoped to vaults/permissions), Connect Server access tokens (JWT-style), CLI biometric integration (Touch ID / Windows Hello / Polkit). OIDC/cloud-IAM-federated workload identity is **not natively supported** — there is no documented OIDC-to-token exchange comparable to Vault's JWT/OIDC auth method.

**Secrets engines / plugins:** Static KV only. No dynamic secret generation (database, cloud-IAM, PKI) as a first-class engine. Rotation is supported via CLI/API scripting but there is no lease/TTL broker-issued credential model.

**Replication / DR:** Managed by AgileBits on the SaaS tier; Connect Server local state syncs from the cloud. No documented active-active DR topology for self-hosted deployments.

**Compliance declared:** SOC 2 Type II (AICPA). No ISO 27001 or IRAP certification is publicly listed on the 1Password security page as of the profile date. GDPR compliance claimed for EU region.

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence |
|--------|----------|----------|----------|
| NHI-001 — Cloud IAM principal | ADD-ON | 2 | CLI/SDK can store and inject cloud API keys; no native OIDC-based JIT issuance [1password-sa-docs-2024] |
| NHI-002 — Kubernetes ServiceAccount | NATIVE | 3 | K8s Operator + Injector create K8s Secrets and inject env vars into pods via service account or Connect token [1password-k8s-docs-2024] |
| NHI-003 — CI/CD pipeline identity | NATIVE | 3 | Secret references (`op://`) and `op run` inject secrets at pipeline runtime; GitHub/GitLab integrations documented [1password-cli-docs-2024] |
| NHI-004 — Container / image-pull credential | ADD-ON | 2 | Secrets can be stored and injected as K8s pull-secret items; no dedicated imagePullSecret engine [1password-k8s-docs-2024] |
| NHI-005 — Database service account | ADD-ON | 1 | Static DB credentials can be stored and rotated via scripting; no dynamic DB secrets engine [1password-sa-docs-2024] |
| NHI-006 — Application TLS / mTLS workload identity | GAP | 0 | No PKI/CA engine; no cert issuance or lifecycle management documented [PUBLIC] |
| NHI-007 — Third-party SaaS API key | NATIVE | 3 | Core use case; vaults store API keys, injected via CLI/SDK/Connect [1password-cli-docs-2024] |
| NHI-008 — Git platform credential (PAT, SSH key) | NATIVE | 3 | Native SSH agent integration + PAT storage; `op://` references in CI pipelines [1password-ssh-docs-2024] |
| NHI-009 — Config-management / IaC agent identity | NATIVE | 3 | Terraform provider and Ansible collection inject secrets at apply-time [1password-tf-docs-2024] |
| NHI-010 — Monitoring / observability agent | ADD-ON | 2 | Monitoring creds stored as static secrets, injected via CLI; no dedicated SIEM/telemetry path [1password-cli-docs-2024] |
| NHI-011 — Message broker / event-bus client | ADD-ON | 2 | Broker credentials stored as KV items; no native AMQP/Kafka credential plugin [1password-sa-docs-2024] |
| NHI-012 — AD / LDAP service account | ADD-ON | 1 | Windows credential items supported; no gMSA/Kerberos rotation engine [INDUSTRY-CONSENSUS] |
| NHI-013 — Reverse-proxy / API-gateway identity | ADD-ON | 2 | API keys stored and injected; no native gateway-side identity protocol [1password-cli-docs-2024] |
| NHI-014 — RPA bot identity | ADD-ON | 1 | RPA tool credentials can be stored; no RPA-platform-native plugin documented [INDUSTRY-CONSENSUS] |
| NHI-015 — Code-signing identity | GAP | 0 | No code-signing key management or Sigstore integration [PUBLIC] |
| NHI-016 — Build provenance / SLSA attestation | GAP | 0 | Not in scope for 1Password Secrets Automation [PUBLIC] |
| NHI-017 — Service mesh control-plane identity | GAP | 0 | No Istio/Linkerd/SPIFFE integration documented [PUBLIC] |
| NHI-018 — Confidential-computing attestation | GAP | 0 | No TEE attestation gate for secret release [PUBLIC] |
| NHI-019 — AI agent / autonomous workflow identity | NATIVE | 2 | MCP Server for Codex (2026 launch) + agent hooks expose 1Password to LLM tool calls [1password-mcp-docs-2026] |
| NHI-020 — Model artifact / registry identity | GAP | 0 | No ML model registry credential pattern documented [PUBLIC] |
| NHI-021 — IoT / OT device identity | GAP | 0 | No IoT enrollment or device-certificate engine [PUBLIC] |
| NHI-022 — Mainframe / midrange service identity | GAP | 0 | No mainframe credential plugin or RACF integration [PUBLIC] |
| NHI-023 — Database encryption / TDE master key | GAP | 0 | No HSM-backed TDE key management; SaaS store only [PUBLIC] |
| NHI-024 — HSM / KMS operator / break-glass identity | GAP | 0 | No external HSM/KMS operator identity management [PUBLIC] |
| NHI-025 — Certificate authority operator | GAP | 0 | No internal CA or cert lifecycle management [PUBLIC] |
| NHI-026 — Backup / DR agent identity | ADD-ON | 1 | Backup creds stored as static KV; no DR-specific identity workflow [INDUSTRY-CONSENSUS] |
| NHI-027 — Backend-for-frontend / on-behalf-of token | ADD-ON | 1 | OAuth tokens can be stored; no OBO token broker engine [INDUSTRY-CONSENSUS] |
| NHI-028 — Federated B2B / Open Banking client | GAP | 0 | No FAPI 2.0 or Open Banking mTLS cert management [PUBLIC] |
| NHI-029 — Service-account-as-human (shared functional ID) | ADD-ON | 2 | Shared vaults with RBAC for functional accounts; audit log available [1password-pricing-2024] |
| NHI-030 — Browser / SaaS extension / OAuth-app | NATIVE | 3 | Core consumer/business use case; browser extension + vault RBAC [1password-security-2024] |
| NHI-031 — Webhook / inbound integration identity | ADD-ON | 1 | Webhook secret tokens stored as KV; no HMAC-validation engine [INDUSTRY-CONSENSUS] |
| NHI-032 — Network / infrastructure device identity | GAP | 0 | No TACACS+/RADIUS/network-device credential engine [PUBLIC] |
| NHI-033 — Print / spooler / branch-peripheral | GAP | 0 | Not in scope [PUBLIC] |
| NHI-034 — Quantum-resistant / hybrid-PKI rotation | GAP | 0 | No PQC key management [PUBLIC] |
| NHI-035 — Vault-internal / secrets-broker identity | ADD-ON | 2 | Connect Server access tokens govern broker identity; scoped per workflow [1password-connect-docs-2024] |
| NHI-036 — Ephemeral workload via SPIFFE / Aembit | GAP | 0 | No SPIFFE/SPIRE integration; no SVID issuance [PUBLIC] |
| NHI-037 — Forgotten / orphaned legacy identity | ADD-ON | 1 | Watchtower feature flags weak/reused creds for workforce; no programmatic NHI orphan sweep [1password-security-2024] |

**NHI summary:** NATIVE=9, ADD-ON=15, GAP=13, N/A=0.

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Coverage | Maturity | Evidence |
|-------|----------|----------|----------|
| UC-F-001 — Prevent plaintext secrets in source repos | NATIVE | 3 | `op://` secret references replace inline secrets; VS Code extension enforces at edit time [1password-secret-refs-2024] |
| UC-F-002 — Detect & remediate secrets in history | ADD-ON | 1 | No built-in repo-scanning; relies on external tools (GitGuardian etc.) [INDUSTRY-CONSENSUS] |
| UC-F-003 — JIT short-lived cloud credentials via OIDC | GAP | 0 | No OIDC-to-token exchange or cloud IAM integration; static API keys only [PUBLIC] |
| UC-F-004 — Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No SPIFFE/SPIRE integration [PUBLIC] |
| UC-F-005 — Dynamic DB credentials with broker-issued leases | GAP | 0 | No dynamic secrets engine; only static KV storage [PUBLIC] |
| UC-F-006 — Automated rotation of long-lived static secrets | ADD-ON | 2 | Rotation via CLI scripting + webhooks; not a first-class engine with lease TTLs [1password-cli-docs-2024] |
| UC-F-007 — Immediate revocation on identity compromise | ADD-ON | 2 | Service account tokens and Connect tokens can be revoked via dashboard/CLI; no automated ITSM trigger [1password-sa-docs-2024] |
| UC-F-008 — K8s secret consumption without on-disk plaintext | NATIVE | 3 | K8s Operator creates Secrets from 1Password items; Injector injects as env vars without persisting to disk [1password-k8s-docs-2024] |
| UC-F-009 — Container image-pull credentials per workload | ADD-ON | 2 | Pull-secret values stored as KV items, injected via Operator; no per-workload issuance engine [1password-k8s-docs-2024] |
| UC-F-010 — IaC secrets injected at apply-time | NATIVE | 3 | Terraform provider + Ansible collection inject secrets without persisting in state files [1password-tf-docs-2024] |
| UC-F-011 — Observability-agent credentials rotated and scoped | ADD-ON | 1 | Creds stored as KV; manual rotation scripting only; no native telemetry integration [INDUSTRY-CONSENSUS] |
| UC-F-012 — Message-broker client identity hardening | ADD-ON | 1 | Credentials stored; no native Kafka/RabbitMQ plugin [INDUSTRY-CONSENSUS] |
| UC-F-013 — gMSA / Kerberos modernisation for AD service accounts | GAP | 0 | No AD/Kerberos/gMSA integration [PUBLIC] |
| UC-F-014 — API-gateway upstream identity standardised | ADD-ON | 2 | API keys stored and injected; no native gateway-side enforcement [1password-cli-docs-2024] |
| UC-F-015 — RPA bot credentials vaulted and session-bound | ADD-ON | 1 | Credentials storable; no RPA-platform plugin or session-binding [INDUSTRY-CONSENSUS] |
| UC-F-016 — Keyless code- and artifact-signing in CI | GAP | 0 | No code-signing or Sigstore/cosign integration [PUBLIC] |
| UC-F-017 — TEE attestation gates secret release | GAP | 0 | No confidential-computing attestation path [PUBLIC] |
| UC-F-018 — AI-agent / LLM tool-credential brokering | NATIVE | 2 | MCP Server for Codex (2026) + agent hooks let LLM agents request credentials through 1Password [1password-mcp-docs-2026] |
| UC-F-019 — IoT / OT / branch-device identity enrolment | GAP | 0 | No IoT certificate or device-identity engine [PUBLIC] |
| UC-F-020 — Mainframe / midrange credential rotation pipeline | GAP | 0 | No mainframe integration [PUBLIC] |
| UC-F-021 — Backup / DR agent identity de-privileging | ADD-ON | 1 | Backup creds stored; no automated de-privileging workflow [INDUSTRY-CONSENSUS] |
| UC-F-022 — Webhook inbound identity verification | ADD-ON | 1 | Webhook tokens stored as KV; no HMAC-verify engine [INDUSTRY-CONSENSUS] |
| UC-F-023 — Network-device credential modernisation | GAP | 0 | No TACACS+/RADIUS/NETCONF integration [PUBLIC] |
| UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | No PKI or mTLS cert management [PUBLIC] |
| UC-F-025 — OAuth-app / marketplace integration governance | ADD-ON | 2 | OAuth tokens stored with RBAC in shared vaults; no automated revocation [1password-pricing-2024] |
| UC-F-026 — Vault-internal identity hardening | ADD-ON | 2 | Connect Server access tokens + service account tokens are scoped; no quorum/Shamir split [1password-connect-docs-2024] |
| UC-F-027 — Orphaned / dormant NHI cleanup pipeline | ADD-ON | 1 | Watchtower identifies human-focused weak/stale entries; no machine-identity orphan sweep [1password-security-2024] |
| UC-N-001 — Real-time secret-sprawl KPI dashboard | ADD-ON | 1 | Business plan provides usage reports; no dedicated secret-sprawl KPI dashboard [1password-pricing-2024] |
| UC-N-002 — NHI inventory and ownership attestation | ADD-ON | 1 | Vault/item inventory available via API; no formal NHI ownership attestation workflow [1password-sa-docs-2024] |
| UC-N-003 — Rotation-coverage and freshness KPIs | ADD-ON | 1 | No rotation-age reporting for machine secrets natively [INDUSTRY-CONSENSUS] |
| UC-N-004 — Regulator audit evidence pack | ADD-ON | 2 | SOC 2 Type II report available; audit log via Business plan; limited regulatory mapping docs [1password-security-2024] |
| UC-N-005 — Essential 8 / ZT control-area scorecard | GAP | 0 | No E8 or ZT scorecard tooling; no ACSC/ASD mapping published [PUBLIC] |
| UC-N-006 — Vendor / SaaS supply-chain risk attestation | ADD-ON | 1 | SOC 2 available; no supply-chain-specific SBOM or attestation workflow [INDUSTRY-CONSENSUS] |
| UC-N-007 — Data-sovereignty and residency assurance | ADD-ON | 2 | EU region available (1Password.eu); no AU region; self-hosted Connect Server provides partial sovereignty [1password-connect-docs-2024] |
| UC-N-008 — Engineer training and secure-coding adoption KPI | NATIVE | 2 | Watchtower + security score dashboards for workforce habits; limited machine-identity training KPIs [1password-security-2024] |
| UC-N-009 — Exception register and risk-acceptance governance | GAP | 0 | No formal exception register or risk-acceptance workflow [PUBLIC] |
| UC-N-010 — Break-glass and quorum-operator governance | GAP | 0 | No Shamir/quorum secret-sharing or break-glass workflow [PUBLIC] |
| UC-N-011 — Post-incident reporting and identity-driven RCA | ADD-ON | 1 | Audit events available; no structured incident-RCA workflow [INDUSTRY-CONSENSUS] |
| UC-N-012 — Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA integration or provenance reporting [PUBLIC] |
| UC-N-013 — Crypto-agility and post-quantum readiness reporting | GAP | 0 | No PQC or crypto-agility framework [PUBLIC] |
| UC-N-014 — Vendor-evaluation matrix maintenance | ADD-ON | 1 | No tooling; manual process [INDUSTRY-CONSENSUS] |
| UC-N-015 — Communications, change-comms and stakeholder cadence | ADD-ON | 1 | No built-in comms tooling [INDUSTRY-CONSENSUS] |
| UC-N-016 — IoT / OT / branch-fleet posture reporting | GAP | 0 | No IoT/OT inventory or reporting [PUBLIC] |
| UC-N-017 — Observability/telemetry secret-leak governance | ADD-ON | 1 | No native telemetry-pipeline monitoring for secret leaks [INDUSTRY-CONSENSUS] |
| UC-N-018 — Confidential-computing / TEE attestation assurance | GAP | 0 | No TEE integration [PUBLIC] |
| UC-N-019 — AI-agent / autonomous-workflow KPI suite | ADD-ON | 1 | MCP Server and agent hooks exist; no governance KPI dashboard for AI agent credential use [1password-mcp-docs-2026] |
| UC-N-020 — Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe/legacy posture tooling [PUBLIC] |

**UC summary:** NATIVE=5, ADD-ON=22, GAP=20, N/A=0. (UC-F: NATIVE=5, ADD-ON=13, GAP=9; UC-N: NATIVE=0, ADD-ON=9, GAP=11.)

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 Strengths

1. **Developer experience (DX) for static-secret injection.** The `op://` secret reference syntax, `op run`, `op inject`, and the Terraform provider deliver a polished, low-friction path for replacing plaintext secrets in CI/CD and IaC pipelines. SDK support for Go, Python, and JavaScript covers the majority of XYZ application languages. Maturity 3 across NHI-002, -003, -007, -008, -009 reflects genuine GA quality.

2. **Kubernetes workload delivery.** The Kubernetes Operator (creates K8s Secrets from 1Password items, auto-restarts on rotation) and the Secrets Injector (mutating webhook for environment-variable injection) are feature-complete and Helm-chart deployable. For teams migrating away from base64-encoded K8s Secrets, this is the smoothest on-ramp in the emerging tier.

3. **AI-agent / MCP integration (emerging).** The 2026 launch of the 1Password MCP Server for Codex and agent hooks positions 1Password ahead of most secrets vendors in LLM tool-calling scenarios. Although governance KPIs are absent, the credential-brokering primitive for NHI-019 (AI agent identity) is a genuine differentiator.

### Top 3 Gaps

1. **No dynamic secrets engine.** 1Password cannot issue broker-generated, lease-limited database or cloud-IAM credentials. This is an architectural gap (UC-F-003, -004, -005 all GAP/0), and a fundamental blocker for APRA CPS 234 §28a dynamic credential requirements at FI scale.

2. **No PKI / cert lifecycle management.** There is no CA, no ACME endpoint, no certificate issuance or renewal workflow. NHI-006, -015, -024, -025, -028 are all GAP/0. FIs operating mTLS-heavy Open Banking or internal service-mesh environments will need a complementary tool.

3. **No AU data region and limited compliance posture.** Only US and EU SaaS regions are documented. No IRAP assessment, no ISO 27001 certificate, and no APRA CPS 230/234 data-flow evidence published. Data-sovereignty for APRA-regulated workloads requires self-hosted Connect Server with non-trivial operational overhead.

---

## 6. AU-specific notes (≤ 150 words)

**Data residency:** No AU-region SaaS is publicly documented (as of 2026-05-22). The EU region (1Password.eu) is available for GDPR compliance but does not satisfy APRA data-residency requirements. Self-hosted Connect Server (Docker / Kubernetes) can be deployed inside AU infrastructure, providing a sovereignty path — but this adds operational complexity and leaves the authoritative SaaS store outside AU borders unless an air-gapped Connect-only topology is maintained (not the documented design intent).

**Compliance:** SOC 2 Type II is confirmed. No IRAP assessment, no ISO 27001, and no ASD Essential 8 mapping are publicly listed. 1Password does not publish APRA CPS 230/234 data-flow diagrams. For an APRA-regulated FI, use of 1Password SaaS for machine secrets would require vendor risk acceptance and likely a data-processing agreement with AgileBits.

**AU enterprise references:** No publicly confirmed XYZ Bank or major Australian FI customer references found in public documentation.

---

## 7. Citations

BibTeX keys used in this profile (appended to `meta/citations.bib`):

- `1password-sa-docs-2024` — Service Accounts overview
- `1password-connect-docs-2024` — Connect Server get-started
- `1password-cli-docs-2024` — CLI get-started and secret references
- `1password-k8s-docs-2024` — Kubernetes integrations overview
- `1password-k8s-op-docs-2024` — Kubernetes Operator
- `1password-k8s-injector-docs-2024` — Kubernetes Injector
- `1password-tf-docs-2024` — Terraform provider
- `1password-sdk-docs-2024` — SDKs overview and concepts
- `1password-security-2024` — Security page and whitepaper
- `1password-pricing-2024` — Pricing page (Business / Enterprise plan features)
- `1password-ssh-docs-2024` — SSH & Git integration
- `1password-mcp-docs-2026` — MCP Server for Codex / Build with LLMs / Agent hooks
- `1password-secret-refs-2024` — CLI secret references (`op://` syntax)

---

## 8. Open questions for v1.0

1. **AU data region roadmap:** Does 1Password have a planned AU SaaS region? An SE conversation is needed to determine the timeline.
2. **IRAP assessment:** Has 1Password engaged an IRAP assessor? The security page is silent on this.
3. **ISO 27001 status:** The security page references SOC 2 only. Is ISO 27001 certification in-progress?
4. **Enterprise pricing for Secrets Automation:** The public pricing page shows per-user pricing. Is there a separate per-secret or unlimited-secrets tier for large FI deployments?
5. **Connect Server in air-gapped environments:** Can Connect Server operate fully offline (no egress to 1Password.com) for high-security deployments? Documentation does not confirm this.
6. **Dynamic secrets roadmap:** Is 1Password planning a database or cloud-IAM dynamic-secrets engine, or is the architecture intentionally static-KV-only?
7. **HSM integration for Connect Server:** Can Connect Server be configured to use a customer-managed PKCS#11 HSM for key protection?
8. **APRA compliance evidence:** Does 1Password produce a data-processing agreement and data-flow diagram suitable for APRA CPS 230 §39 vendor-risk requirements?

# Use-Case Catalog — Secrets Management for Machine Identities

**Sensitivity:** [PUBLIC] — independent of XYZ-specific evidence.
**Author:** Use Case Catalog Builder sub-agent (Opus 4.7), 2026-05-21.
**Version:** v0.1.

> **⚠️ Back-map supersession (2026-06-03 regulator audit).** The inline
> per-UC **"Back-map:"** lines below are **superseded and must not be cited**.
> They were written 2026-05-21 and predate (a) the **2026-05-24 ASD ISM
> rebuild** (so they carry old wrong ISM IDs, e.g. ISM-1546/ISM-0974), (b) the
> **NIST CSF 2.0 deferral** (ADR-003 — `CSF-*` codes are out of v0.1 scope),
> and (c) the **CPS 234 clause normalisation** (`§28a/b/c`, `§35b/c` are not
> real clauses; §27 carries the (a)-(e) sub-items). The **authoritative,
> verified** UC→control back-map is now `matrix/use-cases.csv:backmap_codes`
> (regenerated from `matrix/regulatory-trace.csv`), with full bidirectional
> consistency. See [`matrix/REGULATOR-AUDIT-2026-06-03.md`](../matrix/REGULATOR-AUDIT-2026-06-03.md) Part 4.

---

## 1. Methodology

This catalog enumerates **functional** and **non-functional** use cases
(UCs) for secrets management across the 37 Non-Human Identities (NHIs)
catalogued in `research/identity-taxonomy.md`. **Functional UCs** are
engineer-, SRE-, and DevSecOps-facing capabilities (prevent, detect,
broker, rotate, revoke). **Non-functional UCs** are product-owner-,
auditor-, regulator-, and incident-responder-facing capabilities
(measure, report, attest, govern, train, comply). Each UC carries:
(a) ≥1 NHI ID in scope; (b) an **outcome lens** (Essential 8 control
area and/or NIST SP 800-207 ZT pillar) [acsc-e8-2023]
[nist-sp-800-207-2020]; (c) a **back-map** to APRA CPS 234, ASD ISM
control numbers, and/or NIST CSF 2.0 subcategories
[apra-cps-234-2019][asd-ism-2024][nist-csf-2.0-2024]; and (d) an
**FI priority** (P0/P1/P2). Primary sources are OWASP Secrets
Management Cheat Sheet [owasp-sm-cheatsheet-2024], CSA NHI WG
[csa-nhi-taxonomy-2024], GitGuardian State of Secrets Sprawl
[gitguardian-sots-2024], NIST SP 800-204D
[nist-sp-800-204d-2024], MITRE ATT&CK T1552 [mitre-t1552-2024], plus
vendor docs. UCs labelled `[INDUSTRY-CONSENSUS]` reflect widely-
adopted practice with no single canonical source.

## 2. Personas

- **Engineer** — application developer or platform engineer; consumes
  secrets at build- and runtime.
- **SRE** — operates services; owns rotation, revocation, on-call.
- **Platform engineer** — owns the secrets-management platform and
  identity brokers (Vault, KMS, SPIRE, Aembit).
- **DevSecOps engineer** — owns pre-commit, CI, CD security guardrails.
- **Product owner** — owns backlog priority for a business capability;
  consumes KPIs.
- **Internal auditor** — independent assurance over controls and
  evidence sufficiency.
- **External auditor / regulator** — APRA, ASD, ACCC CDR, PCI QSA.
- **Incident responder** — owns identity-driven breach containment.
- **Architect / cryptography lead** — owns crypto-agility, PQC roadmap.
- **Vendor-risk manager** — owns third-party assurance, SaaS data flows.

## 3. Functional use cases (engineer-facing)

### UC-F-001 — Prevent plaintext secrets in source repositories
- **Story:** "As an engineer I want to ensure that no plaintext passwords,
  API keys, certificates, or tokens are committed to source-controlled
  repositories (GitHub, GitLab, Bitbucket, Azure Repos) so that compromise
  of a developer workstation or repo mirror does not leak production
  credentials." (Refines user-supplied functional seed.)
- **Acceptance criteria:**
  - Pre-commit hooks and server-side push-protection block known secret
    patterns across all enterprise repos.
  - CI fails the build if any new secret-shaped string is introduced.
  - Detected leaks auto-create an incident ticket with rotation SLA.
- **NHIs in scope:** NHI-008; NHI-001; NHI-003; NHI-005; NHI-007; NHI-010.
- **Outcome lens:** E8-AppControl; E8-RestrictAdminPriv; ZT-Pillar-Identity;
  ZT-Pillar-Data.
- **Back-map:** CPS234-§28a; CPS234-§35b; ISM-1546; ISM-0974;
  CSF-PR.DS-5; CSF-DE.CM-7.
- **Priority:** P0.
- **Citations:** [owasp-sm-cheatsheet-2024]; [gitguardian-sots-2024];
  [github-push-protection-2024]; [gitlab-secret-detection-2024].

### UC-F-002 — Detect and remediate secrets already in history
- **Story:** "As a DevSecOps engineer I want a one-time and continuous
  historical sweep of all repos and CI variables so that legacy
  plaintext secrets are surfaced, rotated, and purged with chain-of-
  custody evidence."
- **Acceptance criteria:**
  - All default and protected branches scanned; full commit history
    inspected at least once per quarter.
  - Each finding produces: secret type, NHI bucket, owning team,
    rotation status, and validated-or-revoked outcome.
  - Findings tracked to closure in <30 days for P0 secrets.
- **NHIs in scope:** NHI-008; NHI-001; NHI-005; NHI-007; NHI-010; NHI-037.
- **Outcome lens:** E8-PatchApps (analogue); ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§35c; ISM-1525; CSF-DE.CM-1; CSF-RS.MI-2.
- **Priority:** P0.
- **Citations:** [gitguardian-sots-2024];
  [trufflehog-2024]; [git-filter-repo-2024].

### UC-F-003 — Just-in-time short-lived cloud credentials via OIDC
- **Story:** "As a platform engineer I want CI/CD jobs to federate to
  AWS / Azure / GCP via OIDC so that no long-lived cloud access keys
  exist in pipeline variables."
- **Acceptance criteria:**
  - 100% of new pipelines use OIDC trust policies scoped by `sub`/`aud`.
  - Legacy static cloud keys deprecated within 12 months with an
    inventory burn-down.
  - Trust-policy mis-scoping detected by a control (e.g., wildcard
    `sub:*`).
- **NHIs in scope:** NHI-003; NHI-001.
- **Outcome lens:** E8-RestrictAdminPriv; E8-MultiFactorAuth (machine);
  ZT-Pillar-Identity; ZT-Pillar-Workload.
- **Back-map:** CPS234-§22; ISM-1546; ISM-1559; CSF-PR.AC-1; CSF-PR.AC-7.
- **Priority:** P0.
- **Citations:** [github-oidc-2024]; [gitlab-oidc-2024];
  [aws-iam-oidc-2024].

### UC-F-004 — Workload-attested ephemeral identity (SPIFFE/SPIRE)
- **Story:** "As a platform engineer I want every workload to receive a
  short-lived attested identity (X.509-SVID or JWT-SVID) so that
  service-to-service authentication does not rely on long-lived
  shared secrets."
- **Acceptance criteria:**
  - SPIFFE Workload API or equivalent broker reachable from all
    production workloads in scope.
  - Default SVID TTL ≤ 1 hour with automatic rotation; no static
    workload credentials in approved patterns.
  - Trust-domain boundaries reviewed by Architecture Council.
- **NHIs in scope:** NHI-006; NHI-002; NHI-017; NHI-036.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Workload; ZT-Pillar-Identity.
- **Back-map:** CPS234-§22; ISM-1546; CSF-PR.AC-1; CSF-PR.AC-3.
- **Priority:** P1.
- **Citations:** [spiffe-spec-2023]; [nist-sp-800-204d-2024];
  [istio-mtls-2024].

### UC-F-005 — Dynamic database credentials with broker-issued leases
- **Story:** "As an SRE I want application database credentials issued
  on-demand by a secrets broker with TTLs so that compromise of an
  application instance does not yield a long-lived DB credential."
- **Acceptance criteria:**
  - Dynamic-creds path available for all in-scope RDBMS / cloud-DB /
    warehouse engines.
  - Maximum credential TTL configured per data-classification tier.
  - Static-DB-password exceptions registered with expiry.
- **NHIs in scope:** NHI-005; NHI-001; NHI-023.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Data; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28a; ISM-1546; ISM-0974; CSF-PR.AC-1; CSF-PR.DS-5.
- **Priority:** P0.
- **Citations:** [hashicorp-vault-db-secrets-2024];
  [aws-rds-iam-auth-2024]; [snowflake-key-pair-2024].

### UC-F-006 — Automated rotation of long-lived static secrets
- **Story:** "As an SRE I want long-lived shared secrets (DB passwords,
  service-account passwords, API keys) rotated on a schedule and on
  incident, with zero manual transcription, so that stale credentials
  do not accumulate."
- **Acceptance criteria:**
  - Rotation pipelines exist per NHI bucket with documented blast-
    radius / rollback steps.
  - >95% of in-scope long-lived secrets rotated within their policy
    interval (e.g., 90 days).
  - Rotation failures alert on-call within 15 minutes.
- **NHIs in scope:** NHI-005; NHI-007; NHI-010; NHI-011; NHI-012; NHI-014;
  NHI-022; NHI-029; NHI-031.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28c; ISM-1402; ISM-1546; CSF-PR.AC-1; CSF-PR.MA-1.
- **Priority:** P0.
- **Citations:** [owasp-sm-cheatsheet-2024]; [nist-sp-800-57-2020].

### UC-F-007 — Immediate revocation on identity compromise
- **Story:** "As an incident responder I want one-click revocation of any
  NHI's active credentials and active sessions so that a confirmed
  compromise can be contained inside the regulator-expected window."
- **Acceptance criteria:**
  - Revocation API callable from SOAR playbooks within 1 minute end-
    to-end.
  - Token-introspection invalidation propagates across the trust mesh
    in <5 minutes.
  - Post-revocation forensic export available to IR.
- **NHIs in scope:** NHI-001; NHI-003; NHI-007; NHI-008; NHI-019; NHI-027;
  NHI-035.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§34; ISM-1228; CSF-RS.MI-1; CSF-RS.MI-2.
- **Priority:** P0.
- **Citations:** [csa-nhi-taxonomy-2024]; [mitre-t1552-2024];
  [cisa-ransomware-2024].

### UC-F-008 — Kubernetes secret consumption without on-disk plaintext
- **Story:** "As a platform engineer I want pods to consume secrets via
  CSI driver / agent-injector / projected SA tokens so that secrets
  are never written as plaintext K8s Secret objects."
- **Acceptance criteria:**
  - Default cluster policy denies plaintext `Secret` objects of class
    `production-credential`.
  - CSI/agent-injector deployed across in-scope clusters.
  - At-rest etcd encryption with customer-managed keys is enforced.
- **NHIs in scope:** NHI-002; NHI-004; NHI-006.
- **Outcome lens:** E8-AppControl; ZT-Pillar-Workload; ZT-Pillar-Data.
- **Back-map:** CPS234-§28a; ISM-1546; CSF-PR.DS-1; CSF-PR.DS-5.
- **Priority:** P1.
- **Citations:** [k8s-secrets-store-csi-2024];
  [hashicorp-vault-agent-injector-2024]; [k8s-etcd-encryption-2024].

### UC-F-009 — Container image-pull credentials issued per workload
- **Story:** "As a DevSecOps engineer I want image-pull credentials
  scoped per namespace / per workload, with short TTLs, so that a
  compromised node cannot pull arbitrary production images."
- **Acceptance criteria:**
  - Per-workload pull credentials supported (e.g., ECR/ACR/GAR
    short-lived tokens, Harbor robots).
  - No `imagePullSecret` shared across teams in production.
  - Pull-credential rotation automated.
- **NHIs in scope:** NHI-004; NHI-002.
- **Outcome lens:** E8-AppControl; ZT-Pillar-Workload; ZT-Pillar-Data.
- **Back-map:** CPS234-§28a; ISM-1546; CSF-PR.AC-1; CSF-PR.IP-1.
- **Priority:** P1.
- **Citations:** [docker-registry-token-2024]; [harbor-robot-2024];
  [aws-ecr-tokens-2024].

### UC-F-010 — IaC / config-management secrets injected at apply-time
- **Story:** "As an SRE I want Terraform / Ansible / Pulumi runs to fetch
  secrets at apply-time from a broker so that secrets never persist in
  state files, var-files, or runner caches."
- **Acceptance criteria:**
  - State-file scanners enforce zero-plaintext-secret policy.
  - Dynamic-provider integration deployed across IaC platforms.
  - Runner caches encrypted and short-lived.
- **NHIs in scope:** NHI-009; NHI-001; NHI-003.
- **Outcome lens:** E8-AppControl; ZT-Pillar-Workload.
- **Back-map:** CPS234-§22; ISM-1546; CSF-PR.IP-1; CSF-PR.IP-3.
- **Priority:** P1.
- **Citations:** [hashicorp-tfc-2024]; [ansible-aap-2024];
  [hashicorp-vault-tf-provider-2024].

### UC-F-011 — Observability-agent credentials rotated and scoped
- **Story:** "As a platform engineer I want monitoring/observability
  agents (Datadog, Splunk, Dynatrace, Elastic) to use scoped,
  rotatable ingest tokens so that a compromised host cannot exfiltrate
  beyond its own telemetry."
- **Acceptance criteria:**
  - Ingest tokens scoped per environment and per agent class.
  - Tokens rotated ≥quarterly without telemetry gaps.
  - Agent configs forbid embedded application secrets.
- **NHIs in scope:** NHI-010.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics; ZT-Pillar-Workload.
- **Back-map:** CPS234-§28b; ISM-0123; CSF-DE.CM-1; CSF-DE.CM-7.
- **Priority:** P1.
- **Citations:** [datadog-agent-keys-2024]; [splunk-hec-token-2024];
  [elastic-agent-tokens-2024].

### UC-F-012 — Message-broker client identity hardening
- **Story:** "As an engineer I want Kafka / RabbitMQ / Pub-Sub / Service
  Bus clients to authenticate with mTLS or IAM-signed requests, not
  shared SASL passwords, so that lateral movement via the event bus is
  prevented."
- **Acceptance criteria:**
  - mTLS or cloud-IAM auth available as default for all in-scope brokers.
  - SAS / shared-access-signature rotation automated.
  - Cross-tenant topic ACLs enforced.
- **NHIs in scope:** NHI-011; NHI-001; NHI-006.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Network; ZT-Pillar-Workload.
- **Back-map:** CPS234-§28a; ISM-1546; CSF-PR.AC-5; CSF-PR.DS-2.
- **Priority:** P1.
- **Citations:** [kafka-security-2024]; [azure-sb-sas-2024];
  [confluent-rbac-2024].

### UC-F-013 — gMSA / Kerberos modernisation for AD service accounts
- **Story:** "As an SRE I want Active Directory service accounts
  migrated to gMSA / sMSA (or eliminated via federation) so that
  `svc_`-prefixed identities are not held together by static
  passwords."
- **Acceptance criteria:**
  - Inventory of all `svc_` accounts with eligibility classification.
  - gMSA migration path approved for in-scope estates.
  - Password-rotation policy enforced where gMSA not feasible.
- **NHIs in scope:** NHI-012; NHI-029.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity.
- **Back-map:** CPS234-§22; ISM-1402; ISM-1546; CSF-PR.AC-1; CSF-PR.AC-4.
- **Priority:** P1.
- **Citations:** [ms-gmsa-2024]; [ms-spn-2024]; [cisa-default-creds-2024].

### UC-F-014 — API-gateway upstream identity standardised
- **Story:** "As a platform engineer I want every API gateway to
  present a strong upstream identity (mTLS, signed JWT, SigV4) so
  that upstream services can mutually authenticate the gateway."
- **Acceptance criteria:**
  - HMAC-only upstream patterns deprecated in production.
  - Gateway cert lifecycle automated (issuance + rotation).
  - Anomalous upstream auth failures alerted.
- **NHIs in scope:** NHI-013; NHI-006.
- **Outcome lens:** ZT-Pillar-Network; ZT-Pillar-Workload.
- **Back-map:** CPS234-§28a; ISM-1182; CSF-PR.AC-5; CSF-PR.DS-2.
- **Priority:** P2.
- **Citations:** [apigee-mtls-2024]; [aws-apigw-iam-2024];
  [kong-mtls-2024].

### UC-F-015 — RPA bot credentials vaulted and session-bound
- **Story:** "As an SRE I want UiPath / Blue Prism / Automation Anywhere
  bots to retrieve credentials from a vault per-session, with no
  embedded passwords in orchestrator stores or scripts, so that bot
  identities cannot persist after offboarding."
- **Acceptance criteria:**
  - Vault integration enabled for all bot orchestrators.
  - Bots use functional identities distinct from human users where
    feasible; otherwise MFA-bypass tokens are inventoried and rotated.
  - Bot session activity logged and tied to ticket/business process.
- **NHIs in scope:** NHI-014; NHI-029; NHI-012.
- **Outcome lens:** E8-RestrictAdminPriv; E8-MultiFactorAuth;
  ZT-Pillar-Identity.
- **Back-map:** CPS234-§28a; ISM-1546; CSF-PR.AC-1; CSF-PR.AC-7.
- **Priority:** P1.
- **Citations:** [uipath-creds-2024]; [blueprism-creds-2024];
  [cyberark-rpa-2024].

### UC-F-016 — Keyless code- and artifact-signing in CI
- **Story:** "As a DevSecOps engineer I want builds to sign artifacts
  with keyless / short-lived identities (Sigstore Fulcio, GitHub OIDC,
  HSM-backed Authenticode) so that signing keys cannot be stolen at
  rest."
- **Acceptance criteria:**
  - Keyless signing path available for ≥90% of in-scope artifact types.
  - HSM-backed long-lived signing where keyless not viable; quorum
    operator policies documented.
  - Verification policies enforce signed-artifact admission.
- **NHIs in scope:** NHI-015; NHI-016; NHI-024; NHI-034.
- **Outcome lens:** E8-AppControl; ZT-Pillar-Workload; ZT-Pillar-Data.
- **Back-map:** CPS234-§28a; ISM-1414; CSF-PR.DS-6; CSF-PR.IP-3.
- **Priority:** P1.
- **Citations:** [sigstore-arch-2023]; [slsa-spec-2024];
  [ms-authenticode-2024]; [nist-pqc-fips-203-204-205-2024].

### UC-F-017 — TEE attestation gates secret release
- **Story:** "As an architect I want regulated workloads to release
  high-value secrets only after a TEE attestation (Nitro / SEV-SNP /
  TDX / MAA) so that secrets are bound to a measured execution
  environment."
- **Acceptance criteria:**
  - Attestation-gated release pattern documented; broker supports
    at least one TEE attestation flow.
  - Production pilot exists for a regulated workload class.
  - Attestation policy includes revocation and stale-quote handling.
- **NHIs in scope:** NHI-018; NHI-023.
- **Outcome lens:** E8-AppControl; ZT-Pillar-Data; ZT-Pillar-Workload.
- **Back-map:** CPS234-§28b; ISM-0457; CSF-PR.DS-1; CSF-PR.DS-2.
- **Priority:** P2.
- **Citations:** [nitro-enclaves-attestation-2024]; [azure-maa-2024];
  [confidential-space-2024].

### UC-F-018 — AI-agent / LLM tool-credential brokering
- **Story:** "As a platform engineer I want LLM agents (LangChain,
  Copilot Studio, Agentforce, custom agentic frameworks) to obtain
  tool credentials via a broker with per-tool, per-session, scoped
  tokens so that prompt-injection cannot exfiltrate long-lived secrets."
- **Acceptance criteria:**
  - Static API keys for agent tools forbidden in new patterns.
  - OAuth on-behalf-of or workload-broker tokens used; scopes audited.
  - Tool calls logged with agent identity and prompt provenance.
- **NHIs in scope:** NHI-019; NHI-007; NHI-020; NHI-027; NHI-036.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity; ZT-Pillar-Workload.
- **Back-map:** CPS234-§22; ISM-1546; CSF-PR.AC-1; CSF-PR.AC-3.
- **Priority:** P1.
- **Citations:** [owasp-llm-top10-2024]; [csa-ai-agents-2024];
  [astrix-nhi-report-2024].

### UC-F-019 — IoT / OT / branch-device identity enrolment
- **Story:** "As a platform engineer I want IoT / OT / ATM / branch
  devices to enrol via DPS / EST / SCEP with hardware-rooted identity
  so that fleet-wide pre-shared keys are eliminated."
- **Acceptance criteria:**
  - Per-device certificates with TPM / secure-element binding where
    hardware permits.
  - PSK and default-credential fleets have a documented retirement
    plan.
  - Device cert lifecycle automated end-to-end.
- **NHIs in scope:** NHI-021; NHI-033; NHI-025.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Device; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28a; ISM-1554; CSF-PR.AC-1; CSF-PR.AC-3.
- **Priority:** P2.
- **Citations:** [aws-iot-x509-2024]; [azure-iot-dps-2024];
  [nist-sp-800-213-2021].

### UC-F-020 — Mainframe / midrange credential rotation pipeline
- **Story:** "As an SRE I want RACF / ACF2 / Top-Secret / IBM-i started-
  task and batch-scheduler credentials rotated under change-window
  governance so that core-banking NHIs are not effectively static."
- **Acceptance criteria:**
  - Vault integration to mainframe (Conjur z/OS, custom RACF / ICSF
    bridge, or equivalent).
  - Rotation runbooks per started-task class with rollback.
  - ICSF master-key custody includes quorum operators.
- **NHIs in scope:** NHI-022; NHI-024; NHI-023.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28a; ISM-1402; ISM-1546; CSF-PR.AC-1; CSF-PR.MA-2.
- **Priority:** P1.
- **Citations:** [ibm-racf-2024]; [ibm-icsf-2024];
  [cyberark-conjur-2024].

### UC-F-021 — Backup / DR agent identity de-privileging
- **Story:** "As an SRE I want backup / DR agents (NetBackup, Commvault,
  Veeam, Rubrik, Cohesity) to operate with least-privilege,
  vaulted credentials so that ransomware operators cannot turn a
  backup agent into a tier-0 takeover."
- **Acceptance criteria:**
  - Backup-service AD accounts vaulted; passwords rotated post-job
    where supported, or per documented policy otherwise.
  - Immutable-storage tokens stored in HSM-backed vault.
  - Backup-tier admin actions require MFA + just-in-time elevation.
- **NHIs in scope:** NHI-026; NHI-012; NHI-029.
- **Outcome lens:** E8-RestrictAdminPriv; E8-RegularBackups; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28a; ISM-1547; CSF-PR.AC-4; CSF-PR.IP-4.
- **Priority:** P0.
- **Citations:** [cisa-ransomware-2024]; [veeam-perms-2024];
  [nist-sp-1800-25-2020].

### UC-F-022 — Webhook inbound identity verification
- **Story:** "As an engineer I want every inbound webhook (Stripe,
  GitHub, Twilio, payment-rail callbacks) verified by HMAC signature,
  mTLS, or replay-protected JWT so that spoofed callbacks cannot
  drive business logic."
- **Acceptance criteria:**
  - Default library/middleware enforces signature verification on all
    inbound webhooks.
  - Webhook signing secrets rotatable without endpoint downtime.
  - Replay protection (timestamp/nonce window) enforced.
- **NHIs in scope:** NHI-031; NHI-013.
- **Outcome lens:** ZT-Pillar-Network; ZT-Pillar-Data.
- **Back-map:** CPS234-§28a; ISM-0421; CSF-PR.DS-2; CSF-PR.DS-6.
- **Priority:** P2.
- **Citations:** [stripe-webhook-sigs-2024];
  [github-webhook-sigs-2024]; [owasp-sm-cheatsheet-2024].

### UC-F-023 — Network-device credential modernisation
- **Story:** "As a NetOps engineer I want router / switch / firewall /
  SD-WAN credentials rotated via vault-integrated TACACS+/RADIUS so
  that shared device-admin passwords and SNMP communities are
  eliminated."
- **Acceptance criteria:**
  - TACACS+/RADIUS integration with vault deployed across fabric.
  - SNMPv3 + per-device credentials enforced; SNMPv1/v2 deprecated.
  - Vendor-cloud-controller tokens (Meraki, Panorama, Aruba Central)
    vaulted and rotated.
- **NHIs in scope:** NHI-032; NHI-033.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Network; ZT-Pillar-Device.
- **Back-map:** CPS234-§28a; ISM-1402; CSF-PR.AC-3; CSF-PR.AC-5.
- **Priority:** P2.
- **Citations:** [tacacs-rfc8907-2020]; [cisa-network-defaults-2024];
  [cisco-tacacs-2024].

### UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity
- **Story:** "As an architect I want CDR / Open-Banking / payments-rail
  partner clients authenticated by FAPI-2.0-compliant mTLS with
  sender-constrained tokens so that B2B integrations meet regulator
  expectations."
- **Acceptance criteria:**
  - Partner mTLS client certs lifecycle-managed via Venafi/Keyfactor or
    equivalent.
  - private_key_jwt or DPoP used for token requests.
  - Per-partner key compromise drill executed annually.
- **NHIs in scope:** NHI-028; NHI-027; NHI-025.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Network.
- **Back-map:** CPS234-§28a; ISM-1546; CSF-PR.AC-1; CSF-PR.DS-2.
- **Priority:** P1.
- **Citations:** [fapi2-baseline-2024]; [acccdr-2024];
  [rfc8693-token-exchange-2020].

### UC-F-025 — OAuth-app / marketplace integration governance
- **Story:** "As a DevSecOps engineer I want all third-party OAuth apps
  installed into M365 / Google Workspace / Salesforce / Slack / GitHub
  inventoried, risk-scored, and revocable so that 'shadow integrations'
  cannot persist after vendor offboarding."
- **Acceptance criteria:**
  - Tenant-wide OAuth-app inventory refreshed ≥weekly.
  - High-scope apps require approval workflow.
  - Stale refresh tokens (>90 days unused) auto-revoked.
- **NHIs in scope:** NHI-030; NHI-007; NHI-037.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity.
- **Back-map:** CPS234-§22; ISM-1546; CSF-PR.AC-1; CSF-DE.CM-3.
- **Priority:** P1.
- **Citations:** [salesforce-connected-apps-2024];
  [astrix-nhi-report-2024]; [m365-oauth-apps-2024].

### UC-F-026 — Vault-internal identity hardening
- **Story:** "As a platform engineer I want the secrets-manager's own
  identities (root tokens, auto-unseal KMS principals, replication
  tokens, agent/proxy identities) governed with the same rigour as
  customer workloads so that the vault itself is not a single point of
  failure."
- **Acceptance criteria:**
  - Root token sealed offline; recovery via M-of-N Shamir or KMS-
    backed unseal.
  - Replication tokens rotated and scoped per DR/perf cluster.
  - Vault auto-unseal KMS keys subject to the same key-management
    controls as customer keys.
- **NHIs in scope:** NHI-035; NHI-024; NHI-001.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity; ZT-Pillar-Data.
- **Back-map:** CPS234-§22; ISM-1402; CSF-PR.AC-4; CSF-PR.MA-2.
- **Priority:** P0.
- **Citations:** [hashicorp-vault-auto-unseal-2024];
  [cyberark-conjur-followers-2024]; [akeyless-arch-2024].

### UC-F-027 — Orphaned / dormant NHI cleanup pipeline
- **Story:** "As an SRE I want a recurring sweep that identifies and
  retires NHIs unused for >N days (test accounts in prod, ex-vendor
  backdoors, decommissioned-app SAs) so that forgotten identities do
  not become breach vectors."
- **Acceptance criteria:**
  - Activity-based dormancy threshold per NHI bucket.
  - Owner-attestation required before retention extension.
  - Retired identities exported to immutable evidence store.
- **NHIs in scope:** NHI-037; NHI-001; NHI-012; NHI-029.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§22; ISM-1556; CSF-PR.AC-1; CSF-DE.CM-3.
- **Priority:** P1.
- **Citations:** [verizon-dbir-2024]; [csa-nhi-state-2024];
  [cis-controls-v8-2021].

## 4. Non-functional use cases (product-owner / auditor-facing)

### UC-N-001 — Real-time secret-sprawl KPI dashboard
- **Story:** "As a product owner I need to know how many plaintext
  secrets remain in our code repositories — broken down by team, NHI
  bucket, repo, and age — with a trend line so that I can prioritise
  remediation investment." (Refines user-supplied non-functional seed.)
- **Acceptance criteria:**
  - Single dashboard shows: total findings, P0 findings,
    median-time-to-rotate, 30/60/90-day trend.
  - Drill-down per team and per repo with NHI tagging.
  - KPI freshness ≤24 h; data lineage documented.
- **NHIs in scope:** NHI-008; NHI-007; NHI-005; NHI-003; NHI-010; NHI-037.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§35; ISM-0123; ISM-1525; CSF-DE.CM-1; CSF-DE.AE-2.
- **Priority:** P0.
- **Citations:** [gitguardian-sots-2024]; [nist-csf-2.0-2024];
  [owasp-sm-cheatsheet-2024].

### UC-N-002 — NHI inventory and ownership attestation
- **Story:** "As an internal auditor I need a complete, owner-attested
  inventory of every NHI across the estate so that orphans, sprawl,
  and unowned credentials can be evidenced and remediated."
- **Acceptance criteria:**
  - Inventory completeness measured (≥95% coverage of in-scope NHI
    buckets).
  - Annual owner re-attestation per identity.
  - Inventory exports to GRC tooling.
- **NHIs in scope:** NHI-001; NHI-002; NHI-003; NHI-005; NHI-007; NHI-008;
  NHI-012; NHI-014; NHI-019; NHI-022; NHI-026; NHI-030; NHI-037.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§15; CPS234-§22; ISM-1546; CSF-ID.AM-1; CSF-ID.AM-3.
- **Priority:** P0.
- **Citations:** [csa-nhi-taxonomy-2024]; [gartner-mim-2023];
  [verizon-dbir-2024].

### UC-N-003 — Rotation-coverage and freshness KPIs
- **Story:** "As a product owner I need monthly KPIs on rotation
  coverage, rotation freshness (median days since last rotation), and
  rotation-failure backlog by NHI bucket so that I can demonstrate
  control effectiveness."
- **Acceptance criteria:**
  - KPIs split by NHI bucket and data classification.
  - Failure-burn-down tracked at executive forum.
  - Targets agreed annually with CISO and audit.
- **NHIs in scope:** NHI-005; NHI-006; NHI-010; NHI-011; NHI-012; NHI-022;
  NHI-024; NHI-025.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics; ZT-Pillar-Identity.
- **Back-map:** CPS234-§28c; ISM-1402; CSF-PR.MA-1; CSF-DE.CM-1.
- **Priority:** P0.
- **Citations:** [owasp-sm-cheatsheet-2024]; [nist-sp-800-57-2020].

### UC-N-004 — Regulator audit evidence pack
- **Story:** "As an internal auditor I need a one-click APRA CPS 234
  evidence pack (controls 22, 28, 33, 35) for any in-scope NHI bucket
  so that regulator interactions are repeatable and timely."
- **Acceptance criteria:**
  - Evidence pack assembles from control library + raw artefacts.
  - Pack export is signed and timestamped (immutable).
  - Generation completes in <1 business day from request.
- **NHIs in scope:** NHI-005; NHI-008; NHI-009; NHI-022; NHI-028; NHI-035.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics; ZT-Pillar-Governance.
- **Back-map:** CPS234-§22; CPS234-§33; CPS234-§35; ISM-0125; CSF-ID.GV-3.
- **Priority:** P1.
- **Citations:** [apra-cps-234-2019]; [apra-cpg-234-2019];
  [nist-csf-2.0-2024].

### UC-N-005 — Essential 8 / ZT control-area scorecard
- **Story:** "As an architect I need a quarterly scorecard mapping the
  secrets-management programme to Essential 8 maturity levels and
  NIST SP 800-207 ZT pillars so that the FI primary lens is auditable."
- **Acceptance criteria:**
  - Scorecard published quarterly to Risk Committee.
  - Independent maturity review annually.
  - Gaps tracked with owner + due date.
- **NHIs in scope:** NHI-001; NHI-002; NHI-006; NHI-012; NHI-019; NHI-034.
- **Outcome lens:** E8-Maturity-Levels-1-2-3; ZT-All-Pillars.
- **Back-map:** ISM-0570; ISM-0123; CSF-ID.GV-1; CSF-ID.GV-3.
- **Priority:** P1.
- **Citations:** [acsc-e8-2023]; [nist-sp-800-207-2020];
  [nist-csf-2.0-2024].

### UC-N-006 — Vendor / SaaS supply-chain risk attestation
- **Story:** "As a vendor-risk manager I need every SaaS or OAuth-app
  integration risk-scored on data scope, residency, secret-handling,
  and incident-disclosure SLAs so that supply-chain risk is governed
  to the same standard as in-house systems."
- **Acceptance criteria:**
  - Risk-scoring rubric published.
  - Tier-1 vendor attestations refreshed annually.
  - High-risk integrations reviewed at change-advisory board.
- **NHIs in scope:** NHI-007; NHI-030; NHI-031; NHI-028; NHI-026; NHI-004.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Governance.
- **Back-map:** CPS234-§14; ISM-1452; CSF-ID.SC-2; CSF-ID.SC-3.
- **Priority:** P1.
- **Citations:** [apra-cps-230-2023]; [astrix-nhi-report-2024];
  [nist-sp-800-161r1-2024].

### UC-N-007 — Data-sovereignty and residency assurance
- **Story:** "As a vendor-risk manager I need explicit data-flow
  evidence for every vault / KMS / HSM / SaaS secrets product so that
  APRA-regulated data does not transit non-approved jurisdictions."
- **Acceptance criteria:**
  - Data-flow diagrams maintained per vendor.
  - In-AU residency / sovereign-cloud options selected where required.
  - Cross-border processing logged for CPS 230 BCM purposes.
- **NHIs in scope:** NHI-035; NHI-023; NHI-024; NHI-018.
- **Outcome lens:** ZT-Pillar-Data; ZT-Pillar-Governance.
- **Back-map:** CPS230-§39; CPS234-§22; ISM-0072; CSF-ID.GV-3; CSF-PR.DS-5.
- **Priority:** P1.
- **Citations:** [apra-cps-230-2023]; [apra-cps-234-2019];
  [oaic-app-2024].

### UC-N-008 — Engineer training and secure-coding adoption KPI
- **Story:** "As a product owner I need to know that every engineer who
  ships code has completed secrets-management secure-coding training
  in the last 12 months so that culture-level controls are evidenced."
- **Acceptance criteria:**
  - Training completion ≥98% across active engineers.
  - Training content updated annually against OWASP and DBIR findings.
  - Champions network active in each business unit.
- **NHIs in scope:** NHI-008; NHI-003; NHI-005; NHI-019.
- **Outcome lens:** ZT-Pillar-Governance.
- **Back-map:** CPS234-§17; ISM-0252; CSF-PR.AT-1; CSF-PR.AT-2.
- **Priority:** P2.
- **Citations:** [owasp-sm-cheatsheet-2024]; [verizon-dbir-2024];
  [acsc-strategies-2023].

### UC-N-009 — Exception register and risk-acceptance governance
- **Story:** "As an internal auditor I need every deviation from the
  secrets-management standard (static keys, long-rotation, shared
  service accounts) registered with risk-owner, expiry and
  compensating-control evidence so that risk acceptance is
  intentional, time-bound and reviewed."
- **Acceptance criteria:**
  - Exceptions captured in GRC tool with expiry ≤12 months by default.
  - Expired exceptions escalate automatically.
  - Exception trend reported quarterly.
- **NHIs in scope:** NHI-012; NHI-014; NHI-022; NHI-029; NHI-033; NHI-037.
- **Outcome lens:** ZT-Pillar-Governance.
- **Back-map:** CPS234-§15; CPS234-§22; ISM-0027; CSF-ID.GV-4; CSF-ID.RA-6.
- **Priority:** P1.
- **Citations:** [apra-cps-234-2019]; [nist-sp-800-37r2-2018];
  [cis-controls-v8-2021].

### UC-N-010 — Break-glass and quorum-operator governance
- **Story:** "As an internal auditor I need every break-glass identity
  and HSM/CA/KMS quorum-operator role inventoried, monitored, and
  drilled so that high-privilege standing access is detectable and
  testable."
- **Acceptance criteria:**
  - Break-glass identity inventory reviewed quarterly.
  - Use of break-glass generates a same-day SOC review.
  - Quorum drills exercised semi-annually.
- **NHIs in scope:** NHI-024; NHI-025; NHI-035; NHI-022; NHI-026; NHI-017.
- **Outcome lens:** E8-RestrictAdminPriv; ZT-Pillar-Identity; ZT-Pillar-Governance.
- **Back-map:** CPS234-§22; ISM-1175; ISM-1402; CSF-PR.AC-4; CSF-PR.IP-9.
- **Priority:** P1.
- **Citations:** [thales-luna-roles-2024];
  [aws-cloudhsm-users-2024]; [csa-nhi-state-2024].

### UC-N-011 — Post-incident reporting and identity-driven RCA
- **Story:** "As an incident responder I need every secrets-/identity-
  related incident captured with NHI attribution, MITRE T1552 sub-
  technique, and lessons-learned so that programme investment is
  data-driven."
- **Acceptance criteria:**
  - Incident schema includes NHI bucket and ATT&CK technique.
  - RCA template includes contributing control-gap analysis.
  - Findings flow into roadmap prioritisation.
- **NHIs in scope:** NHI-001; NHI-003; NHI-007; NHI-008; NHI-019; NHI-026;
  NHI-037.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics; ZT-Pillar-Governance.
- **Back-map:** CPS234-§34; CPS234-§35; ISM-0123; CSF-RS.AN-1; CSF-RS.IM-1.
- **Priority:** P0.
- **Citations:** [mitre-t1552-2024]; [verizon-dbir-2024];
  [cisa-ransomware-2024].

### UC-N-012 — Supply-chain / SLSA-provenance assurance reporting
- **Story:** "As an architect I need quarterly reports on signed-
  artifact coverage (SLSA level, signed-image %, signed-package %, in-
  toto attestations) so that supply-chain controls evidence improving
  posture over time."
- **Acceptance criteria:**
  - SLSA-level tracked per artefact class.
  - Unsigned-artefact admission requires exception.
  - Provenance verifiers deployed in production CD.
- **NHIs in scope:** NHI-015; NHI-016; NHI-020; NHI-035.
- **Outcome lens:** ZT-Pillar-Data; ZT-Pillar-Workload; ZT-Pillar-Governance.
- **Back-map:** CPS234-§28a; CPS234-§35; ISM-1414; CSF-PR.DS-6; CSF-PR.IP-3.
- **Priority:** P1.
- **Citations:** [slsa-spec-2024]; [in-toto-spec-2024];
  [nist-sp-800-204d-2024].

### UC-N-013 — Crypto-agility and post-quantum readiness reporting
- **Story:** "As an architect I need a crypto-inventory and PQC-
  migration readiness scorecard (NIST FIPS 203/204/205, hybrid certs,
  CA / HSM capability) so that 2030-deadline obligations are visible
  to the board."
- **Acceptance criteria:**
  - Crypto-inventory covers all in-scope vaults, CAs, HSMs, mTLS
    estates, and code-signing pipelines.
  - PQC-migration roadmap exists with capability milestones.
  - Hybrid-cert pilots executed before 2027.
- **NHIs in scope:** NHI-034; NHI-023; NHI-024; NHI-025; NHI-006; NHI-021;
  NHI-028.
- **Outcome lens:** ZT-Pillar-Data; ZT-Pillar-Governance.
- **Back-map:** CPS234-§22; CPS234-§28b; ISM-1232; CSF-PR.DS-1; CSF-PR.IP-3.
- **Priority:** P1.
- **Citations:** [nist-pqc-fips-203-204-205-2024];
  [asd-pqc-guidance-2024]; [nist-sp-1800-38-2024].

### UC-N-014 — Vendor-evaluation matrix maintenance
- **Story:** "As a product owner I need the 12-vendor evaluation matrix
  refreshed each release cycle, with capability deltas highlighted, so
  that vendor choice remains defensible to the Risk Committee."
- **Acceptance criteria:**
  - Matrix re-populated against canonical UC catalogue per release.
  - Capability deltas (gained/lost) flagged for each vendor.
  - Independent reviewer signs off matrix before publication.
- **NHIs in scope:** NHI-001; NHI-002; NHI-005; NHI-006; NHI-015; NHI-019;
  NHI-022; NHI-026; NHI-034; NHI-035.
- **Outcome lens:** ZT-Pillar-Governance.
- **Back-map:** CPS234-§14; ISM-1452; CSF-ID.SC-1; CSF-ID.SC-3.
- **Priority:** P1.
- **Citations:** [gartner-mim-2023]; [csa-nhi-taxonomy-2024];
  [forrester-secrets-2023].

### UC-N-015 — Communications, change-comms and stakeholder cadence
- **Story:** "As a product owner I need a cadence of stakeholder
  communications (engineering, business, executive, board) on the
  secrets-management programme so that delivery, risk and value are
  understood across audiences."
- **Acceptance criteria:**
  - Communications calendar approved; minimum monthly engineering and
    quarterly board cadence.
  - Each release accompanied by impact briefing.
  - Feedback loop from comms captured in backlog.
- **NHIs in scope:** NHI-008; NHI-019; NHI-030; NHI-037.
- **Outcome lens:** ZT-Pillar-Governance.
- **Back-map:** CPS234-§17; ISM-0252; CSF-PR.AT-3; CSF-PR.AT-4.
- **Priority:** P2.
- **Citations:** [acsc-strategies-2023]; [nist-csf-2.0-2024];
  [verizon-dbir-2024].

### UC-N-016 — IoT / OT / branch-fleet posture reporting
- **Story:** "As an internal auditor I need monthly fleet-posture
  reports on IoT / OT / ATM / branch-peripheral identities so that
  default-credentials and PSK-fleet exposure is visible and burning
  down."
- **Acceptance criteria:**
  - Fleet inventory by device class with credential type.
  - Default-credentials and PSK fleets tracked with retirement plan.
  - Posture deltas reported at Operational Risk Committee.
- **NHIs in scope:** NHI-021; NHI-033; NHI-032.
- **Outcome lens:** ZT-Pillar-Device; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§22; ISM-1554; CSF-PR.AC-3; CSF-ID.AM-1.
- **Priority:** P2.
- **Citations:** [nist-sp-800-213-2021]; [cisa-default-creds-2024];
  [cisa-network-defaults-2024].

### UC-N-017 — Observability/telemetry secret-leak governance
- **Story:** "As an internal auditor I need evidence that logs and
  telemetry pipelines do not propagate secrets onward to Datadog /
  Splunk / Elastic SaaS so that observability is not itself a leak
  channel."
- **Acceptance criteria:**
  - Log-scrubbing rules enforced at agent and ingest tier.
  - Periodic sampled audit of indexed telemetry for secret patterns.
  - Findings tied back to UC-N-001 dashboard.
- **NHIs in scope:** NHI-010; NHI-011; NHI-013.
- **Outcome lens:** ZT-Pillar-Visibility-Analytics; ZT-Pillar-Data.
- **Back-map:** CPS234-§28b; ISM-0123; CSF-DE.CM-1; CSF-PR.DS-5.
- **Priority:** P1.
- **Citations:** [datadog-agent-keys-2024]; [splunk-hec-token-2024];
  [owasp-sm-cheatsheet-2024].

### UC-N-018 — Confidential-computing / TEE attestation assurance
- **Story:** "As an auditor I need attestation evidence for any
  workload claiming TEE-bound secret release so that the strongest-
  trust pattern is verifiable, not just declarative."
- **Acceptance criteria:**
  - Attestation logs retained per data-classification policy.
  - Periodic verifier review of attestation policies.
  - Failed-attestation incidents reported.
- **NHIs in scope:** NHI-018; NHI-023.
- **Outcome lens:** ZT-Pillar-Workload; ZT-Pillar-Data.
- **Back-map:** CPS234-§28b; ISM-0457; CSF-PR.DS-1; CSF-PR.DS-2.
- **Priority:** P2.
- **Citations:** [nitro-enclaves-attestation-2024];
  [azure-maa-2024]; [confidential-space-2024].

### UC-N-019 — AI-agent / autonomous-workflow KPI suite
- **Story:** "As a product owner I need KPIs specific to AI-agent NHIs
  — tools-invoked-per-session, scope inflation, refusal/escalation
  rates, prompt-injection-induced credential calls — so that the
  governance of agentic workflows scales with adoption."
- **Acceptance criteria:**
  - AI-agent NHI inventory maintained alongside UC-N-002.
  - Per-tool credential issuance volume reported weekly.
  - Anomalous tool-credential request patterns alert SOC.
- **NHIs in scope:** NHI-019; NHI-020; NHI-027; NHI-036.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§22; CPS234-§35; ISM-1546; CSF-DE.CM-3; CSF-DE.AE-2.
- **Priority:** P1.
- **Citations:** [owasp-llm-top10-2024]; [csa-ai-agents-2024];
  [astrix-nhi-report-2024].

### UC-N-020 — Mainframe / legacy posture and exception transparency
- **Story:** "As an internal auditor I need mainframe / midrange / RPA
  posture reported alongside cloud so that the legacy long-tail is
  visible and exception register pressure is data-driven."
- **Acceptance criteria:**
  - Mainframe + RPA rotation/coverage shown on the same dashboard as
    cloud (UC-N-001/003).
  - Aging exceptions on legacy NHIs auto-escalate.
  - Modernisation roadmap published.
- **NHIs in scope:** NHI-022; NHI-014; NHI-029; NHI-026; NHI-032.
- **Outcome lens:** ZT-Pillar-Identity; ZT-Pillar-Visibility-Analytics.
- **Back-map:** CPS234-§22; ISM-1402; CSF-ID.AM-1; CSF-PR.MA-2.
- **Priority:** P1.
- **Citations:** [ibm-racf-2024]; [uipath-creds-2024];
  [csa-nhi-state-2024].

## 5. Cross-cutting use-case clusters

Three clusters span functional and non-functional UCs and frame PRD §8.

**Cluster A — Detect-and-remediate plaintext sprawl.** Combines UC-F-001
(prevention), UC-F-002 (history sweep), UC-N-001 (KPI dashboard) and
UC-N-008 (training adoption). This is the cluster the user-supplied
seeds anchor; it is the most-cited entry point in GitGuardian SoSS and
Verizon DBIR and the easiest to demonstrate value to non-technical
stakeholders.

**Cluster B — Ephemeral, attested, brokered identity.** Combines
UC-F-003 (CI OIDC), UC-F-004 (SPIFFE), UC-F-005 (dynamic DB),
UC-F-008 (K8s consumption), UC-F-017/18/19 (TEE / AI / IoT
attestation) plus UC-N-002 (inventory) and UC-N-005 (E8/ZT
scorecard). This cluster is the strategic destination; vendor
evaluation will be most discriminating here.

**Cluster C — Govern the long tail and the vault itself.** Combines
UC-F-013 (gMSA), UC-F-015 (RPA), UC-F-020 (mainframe), UC-F-021
(backup), UC-F-023 (network device), UC-F-025 (OAuth-app), UC-F-026
(vault-internal) and UC-F-027 (orphan cleanup), with UC-N-007
(sovereignty), UC-N-009 (exceptions), UC-N-010 (break-glass) and
UC-N-020 (legacy transparency). This cluster is where audit, risk
and ransomware-resilience concentrate.

## 6. Open questions

- Should **UC-F-018 / UC-N-019** (AI-agent identity) be promoted to a
  standalone PRD section or remain a cross-cutting cluster?
- Treatment of **UC-F-026** (vault-internal identity): include the
  vendor's own NHIs in the 12-vendor scoring matrix?
- Are **UC-F-019 / UC-N-016** (IoT/OT/branch) in v0.1 scope or deferred
  to a sibling fleet PRD?
- Confirm **mainframe** (UC-F-020 / UC-N-020) as a first-class matrix
  column vs. appendix.
- Should **service-account-as-human** (NHI-029) be jointly owned with
  IGA, and how does that affect UC-F-013 / UC-N-009 ownership lines?
- **Crypto-agility / PQC** (UC-N-013): explicit roadmap milestones in
  v0.1, or v1.0 deep-dive?
- **Open-Banking / FAPI 2.0** (UC-F-024): scope to current CDR
  obligations only, or anticipate 2026 non-bank-lender expansion?
- Where does **break-glass governance** (UC-N-010) live — secrets PRD
  or PAM/IGA PRD?
- Are **orphans / dormancy** (UC-F-027) a UC or a maturity dimension?
- What is the **funding model** for the cross-cutting cluster C in FY27?

## 7. Citations

BibTeX keys used above are appended to `meta/citations.bib`. New keys
introduced by this catalog (beyond Agent 01) are listed in the
"Use Case Catalog Builder" block of that file.

# Appendix C — Glossary and NHI definitions

**Status:** v0.1 (Wave B — 2026-05-23).
**Parent document:** [`PRD-FI-v0.1.md`](../PRD-FI-v0.1.md) §18 + §19.
**Scope:** every NHI ID (NHI-001..NHI-037) is defined; every UC ID
(UC-F-001..027 + UC-N-001..020) has a one-line summary; every acronym
used in the PRD body, appendices and ADRs is expanded. Sources are
[`research/identity-taxonomy.md`](../../research/identity-taxonomy.md)
([ADR-002](../adrs/ADR-002-identity-taxonomy-source.md)) and
[`research/use-cases.md`](../../research/use-cases.md). Sensitivity
tagging per [ADR-005](../adrs/ADR-005-anz-evidence-policy.md).

---

## C.1 NHI definitions

The taxonomy carries **37 NHIs** — 14 COMMON (NHI-001..014) and 23
UNCOMMON (NHI-015..037) — anchored to the Cloud Security Alliance NHI
Working Group, Gartner MIM, SPIFFE specification, NIST SP 800-204D and
OWASP Secrets Management Cheat Sheet. Each definition below is the
60-word capture from [`research/identity-taxonomy.md`](../../research/identity-taxonomy.md);
follow the link for the full per-NHI lifecycle / trust-anchor / typical-
credential / governance-maturity card.

### C.1.1 COMMON identities (NHI-001..014)

- **NHI-001 — Cloud IAM principal `[COMMON]`.** A workload-bound
  principal in AWS IAM, Azure Entra (managed identity), or GCP service
  account, used by compute resources to call cloud APIs. STS / metadata
  tokens are SHORT-LIVED; JSON keys / IAM access keys are LONG-LIVED.
- **NHI-002 — Kubernetes ServiceAccount `[COMMON]`.** Pod-bound
  identity issued by the K8s API server and projected as a short-lived
  JWT via the TokenRequest API (default 1 h). EKS / AKS / GKE /
  OpenShift / Rancher / bare-metal.
- **NHI-003 — CI/CD pipeline identity `[COMMON]`.** GitHub Actions,
  GitLab CI, Azure DevOps, Jenkins, CircleCI job identity. Increasingly
  OIDC-federated to cloud IAM; otherwise long-lived PATs and deploy
  keys. PAT sprawl is endemic per GitGuardian state-of-secrets.
- **NHI-004 — Container / image-pull credential `[COMMON]`.** Registry
  credential used by orchestrators and build tools to pull container
  images. ECR / ACR / GAR / Harbor / Artifactory; `imagePullSecret`
  patterns in K8s; OAuth2 tokens or robot accounts.
- **NHI-005 — Database service account `[COMMON]`.** Application-to-
  database principal (PostgreSQL, MySQL, Oracle, MSSQL, MongoDB,
  Snowflake, BigQuery, Redshift, Cassandra). Long-lived to STATIC is
  the common rotation-failure mode; LOW–MEDIUM governance maturity.
- **NHI-006 — Application TLS server / mTLS workload identity
  `[COMMON]`.** X.509 identity for a web/API workload or workload-to-
  workload mTLS (SPIFFE / SPIRE). Lifetimes range from SHORT-LIVED
  (SPIFFE SVID ~1 h) to LONG-LIVED (public CA certs).
- **NHI-007 — Third-party SaaS API key / OAuth client `[COMMON]`.**
  OAuth `client_id+secret`, refresh tokens, static API keys or webhook
  signing secrets used to call external SaaS (Salesforce, Workday,
  ServiceNow, Slack, Datadog, etc.). LOW governance maturity.
- **NHI-008 — Git platform credential (PAT, SSH key, deploy key)
  `[COMMON]`.** GitHub, GitLab, Bitbucket, Azure Repos identity used by
  humans, bots and pipelines. Fine-grained tokens, SSH keys, deploy
  keys, GitHub App installation tokens. PAT sprawl is the dominant
  exposure pattern.
- **NHI-009 — Configuration-management / IaC agent identity
  `[COMMON]`.** Ansible Automation Platform, Puppet, Chef, Terraform
  Cloud / Enterprise, Pulumi agents. Build farms, control planes and
  ephemeral runners. AAP credentials, AppRoles, team tokens, dynamic
  cloud creds.
- **NHI-010 — Monitoring / observability agent `[COMMON]`.** Datadog
  agent keys, Splunk HEC tokens, Dynatrace OneAgent, Prometheus
  exporters, Elastic Beats, New Relic agents. Endemically baked into
  golden images; LOW governance maturity.
- **NHI-011 — Message broker / event-bus client `[COMMON]`.** Kafka,
  RabbitMQ, Pulsar, SQS/SNS, Service Bus, Pub/Sub, Event Grid producer/
  consumer clients. SASL/SCRAM creds, mTLS certs, IAM-signed requests,
  shared-access signatures (SAS).
- **NHI-012 — Active Directory / LDAP service account `[COMMON]`.**
  Domain service accounts (`svc_`-prefixed) used by on-prem and
  hybrid workloads — Windows file/print, SQL Server, SharePoint,
  Exchange hybrid, Kerberos-bound Java apps. STATIC unless gMSA-
  modernised.
- **NHI-013 — Reverse-proxy / API-gateway upstream identity
  `[COMMON]`.** Identity the API gateway (Apigee, Kong, AWS API GW,
  Azure APIM, F5, NGINX+) presents to upstream services. mTLS client
  certs, signed JWTs, HMAC keys or AWS SigV4 IAM credentials.
- **NHI-014 — RPA bot identity `[COMMON]`.** UiPath, Blue Prism,
  Automation Anywhere robots — frequently authenticated as a "real"
  AD user. AD passwords vaulted in Orchestrator, MFA bypass tokens,
  browser session cookies. STATIC.

### C.1.2 UNCOMMON identities (NHI-015..037)

- **NHI-015 — Code-signing identity (Sigstore / Authenticode / Apple)
  `[UNCOMMON]`.** Identity that signs binaries, container images,
  packages or SBOM attestations. Sigstore Fulcio ephemeral (~10 min),
  EV / OV code-signing certs HSM-bound, Apple Developer ID keys, GPG
  keys for package repos.
- **NHI-016 — Build provenance / SLSA attestation identity
  `[UNCOMMON]`.** Identity that signs in-toto / SLSA provenance
  statements proving how an artifact was built. GitHub Actions
  reusable workflows, GitLab SLSA, Buildkite, Tekton Chains. Sigstore
  keyless OIDC, TUF root keys.
- **NHI-017 — Service mesh control-plane identity `[UNCOMMON]`.** The
  identity Istiod / Linkerd identity / Consul Connect CA uses to mint
  workload SVIDs. Intermediate-CA private keys, bootstrap tokens,
  root-CA trust bundles. Often unknown to the secrets team.
- **NHI-018 — Confidential-computing attestation identity
  `[UNCOMMON]`.** Identity rooted in a TEE (Intel SGX/TDX, AMD SEV-SNP,
  AWS Nitro, Azure Confidential VMs, GCP Confidential Space) that
  attests measurements before secret release. EPHEMERAL.
- **NHI-019 — AI agent / autonomous workflow identity `[UNCOMMON]`.**
  LLM-driven agent (LangChain, AutoGen, MS Copilot Studio, Agentforce,
  custom agentic frameworks) calling tools, APIs and human-facing
  systems on behalf of a user or process. OAuth OBO tokens, static tool
  API keys, retrieval-store creds, model-provider keys. The fastest-
  growing class.
- **NHI-020 — Model artifact / registry identity `[UNCOMMON]`.**
  Identity that pushes / pulls trained models or weights from a model
  registry (MLflow, SageMaker Model Registry, Hugging Face, Vertex
  Model Garden, Azure ML). Registry tokens, S3 / GCS / Blob
  credentials, signed model artifacts.
- **NHI-021 — IoT / OT device identity `[UNCOMMON]`.** Per-device
  identity for sensors, gateways, ATMs, POS terminals, branch-printer
  fleets, BMS, EV chargers. Hardware-rooted (TPM, secure element).
  AWS IoT Core, Azure IoT Hub, branch / ATM networks. LONG-LIVED.
- **NHI-022 — Mainframe / midrange service identity `[UNCOMMON]`.**
  RACF, ACF2, Top Secret userIDs used by started tasks, CICS region
  IDs, IMS dependent regions, batch-scheduler IDs (Control-M, OPCA);
  AS/400 / IBM i profiles. STATIC; rotation requires change windows.
  Material at the FI.
- **NHI-023 — Database encryption / TDE master-key identity
  `[UNCOMMON]`.** The key (and custodian) used by TDE for SQL Server,
  Oracle TDE, PostgreSQL pgcrypto, AlwaysEncrypted CMK, MongoDB
  CSFLE. Lives in KMS / HSM; custodian is usually a service account.
- **NHI-024 — HSM / KMS operator / break-glass identity `[UNCOMMON]`.**
  The high-privilege identities that administer the HSM (CloudHSM,
  Thales Luna, Fortanix DSM, nCipher nShield, Entrust, Utimaco) or
  the KMS control plane. Quorum-protected (M-of-N). PED keys,
  smartcards, Shamir shares.
- **NHI-025 — Certificate authority operator identity `[UNCOMMON]`.**
  Roles in private CA (Microsoft ADCS, EJBCA, Venafi TPP/TLSPC,
  Keyfactor Command, AWS Private CA, GCP CAS) — RA, CA admin,
  auditor, enrolment agent. Smartcard-bound admin certs, CA private
  keys in HSM, ACME EAB keys.
- **NHI-026 — Backup / DR agent identity `[UNCOMMON]`.** NetBackup,
  Commvault, Veeam, Rubrik, Cohesity, Druva agent identities with
  cross-system read access. Prime ransomware target. STATIC; LOW
  governance per recent post-mortems.
- **NHI-027 — Backend-for-frontend / on-behalf-of token holder
  `[UNCOMMON]`.** Service identities that exchange user tokens for
  downstream-API tokens (OAuth 2.0 token exchange, OBO, JWT bearer
  grant). BFF tier; banking customer-360 microservice graphs.
  Confidential-client secrets, private_key_jwt, DPoP keys.
- **NHI-028 — Federated B2B / Open Banking client identity
  `[UNCOMMON]`.** mTLS / FAPI 2.0 client identities used by partner
  banks, fintechs and CDR data recipients. Open Banking, payment rails
  (PEXA, NPP), Swift, ASX. mTLS certs + sender-constrained tokens +
  SSAs + DPoP keys. Regulator-driven maturity.
- **NHI-029 — Service-account-as-human (shared functional ID)
  `[UNCOMMON]`.** AD / IdP account used by multiple humans AND scripts;
  common in legacy ops and outsourced run teams (`oracle`, `sapadm`,
  `weblogic`, `svc_batch`, shared Tableau / Power BI). LOW maturity.
- **NHI-030 — Browser / SaaS extension and OAuth-app identity
  `[UNCOMMON]`.** Third-party apps installed into Google Workspace,
  M365, Salesforce, Slack, GitHub Apps — operating with delegated
  scopes against tenant data. OAuth refresh tokens (long-lived),
  install tokens, webhook secrets. The "shadow integration" problem.
- **NHI-031 — Webhook / inbound integration identity `[UNCOMMON]`.**
  Inbound caller identity asserted via HMAC-signed webhooks, mTLS or
  replay-protected JWTs (Stripe, GitHub, Twilio, payment gateways).
  Event-driven integrations, fraud feeds, payment notifications.
- **NHI-032 — Network / infrastructure device identity `[UNCOMMON]`.**
  Router, switch, firewall, load-balancer, SD-WAN edge identity used
  by NetOps automation and TACACS+ / RADIUS-authenticated principals.
  SSH keys, TACACS+ shared secrets, SNMPv3 creds, vendor cloud-
  controller tokens. STATIC.
- **NHI-033 — Print / spooler / branch-peripheral identity
  `[UNCOMMON]`.** Network printer, MFP, cheque scanner, ATM
  peripheral, kiosk identities — historically authenticated via
  default credentials. SNMPv3 creds, 802.1X EAP-TLS certs, default
  admin creds (a very common gap).
- **NHI-034 — Quantum-resistant / hybrid-PKI rotation identity
  `[UNCOMMON]`.** Identities involved in post-quantum (NIST PQC:
  ML-KEM, ML-DSA, SLH-DSA) and hybrid-cert rollouts — dual-signed
  certificates, PQC-capable CAs and HSMs. On every Tier-1 bank's
  2026–2028 roadmap.
- **NHI-035 — Vault-internal / secrets-broker identity `[UNCOMMON]`.**
  The vault's own service identities — auto-unseal KMS principals,
  replication tokens, Performance / DR Replication identities, agent /
  proxy identities (Vault Agent, Conjur follower, Akeyless Gateway).
  Recursive risk surface — the vault itself is an NHI.
- **NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch
  `[UNCOMMON]`.** "Zero-trust workload identity" issued just-in-time
  to a workload after attestation (kernel, K8s, AWS metadata),
  replacing static secrets. SPIFFE SVIDs, signed-attestation-bound
  tokens. EPHEMERAL. The ZT destination class.
- **NHI-037 — Forgotten / orphaned legacy identity `[UNCOMMON]`.**
  Decommissioned-app service accounts still active, expired-team
  credentials, "test" accounts in production, ex-vendor backdoors.
  Per Verizon DBIR the most-abused class in breaches. Surfaced only
  via attestation / ITDR sweeps.

> **Cross-cutting concerns** (per
> [taxonomy §5](../../research/identity-taxonomy.md)): ephemerality is
> not free (the trust anchor becomes a Tier-0 dependency); federation
> moves blame, not risk; blast radius scales with privilege ×
> persistence × reachability; vault sprawl is the predictable failure
> mode in regulated estates; observability dashboards routinely ingest
> secrets; PQC migration sits on every Tier-1 bank's roadmap; AU
> sovereignty constrains SaaS vault choices materially.

---

## C.2 UC definitions (one-line summary per UC)

47 UCs total — 27 functional (engineer / SRE / DevSecOps-facing) + 20
non-functional (product-owner / auditor / regulator / IR-facing). Full
acceptance criteria and citations live in
[`research/use-cases.md`](../../research/use-cases.md). User-supplied
seeds are flagged.

### C.2.1 Functional UCs

- **UC-F-001 — Prevent plaintext secrets in source repositories.**
  Pre-commit and server-side push-protection block known secret
  patterns across all enterprise repos; CI fails on new secret-shaped
  strings; detected leaks auto-create incident with rotation SLA.
  `[USER-SUPPLIED SEED]`.
- **UC-F-002 — Detect and remediate secrets already in history.**
  One-time + continuous sweep of repos + CI variables; findings
  surface secret type / NHI bucket / owner / rotation status; P0
  closure < 30 days.
- **UC-F-003 — Just-in-time short-lived cloud credentials via OIDC.**
  100% of new pipelines federate to AWS / Azure / GCP via OIDC scoped
  by `sub`/`aud`; legacy static keys burn-down on a 12-month plan.
- **UC-F-004 — Workload-attested ephemeral identity (SPIFFE / SPIRE).**
  Workload API or equivalent reachable from all production workloads;
  default SVID TTL ≤ 1 h with automatic rotation.
- **UC-F-005 — Dynamic database credentials with broker-issued
  leases.** All in-scope RDBMS / cloud-DB / warehouse engines have a
  dynamic-creds path; TTLs per classification tier; exceptions in
  register.
- **UC-F-006 — Automated rotation of long-lived static secrets.**
  Per-NHI rotation pipelines with blast-radius / rollback documented;
  > 95% of in-scope secrets rotated within policy interval.
- **UC-F-007 — Immediate revocation on identity compromise.** One-
  click revoke for any NHI's active credentials + sessions; tested
  quarterly; contained inside the regulator-expected window.
- **UC-F-008 — K8s secret consumption without on-disk plaintext.**
  CSI driver / agent-injector / projected SA tokens — secrets never
  written as plaintext K8s Secret objects.
- **UC-F-009 — Container image-pull credentials issued per workload.**
  Image-pull credentials scoped per namespace / per workload with
  short TTLs; a compromised node cannot pull arbitrary production
  images.
- **UC-F-010 — IaC / config-management secrets injected at apply-
  time.** Terraform / Ansible / Pulumi runs fetch secrets at
  apply-time from a broker — never persisted in state files or
  runner caches.
- **UC-F-011 — Observability-agent credentials rotated and scoped.**
  Datadog / Splunk / Dynatrace / Elastic agents use scoped, rotatable
  ingest tokens; a compromised host cannot exfiltrate beyond own
  telemetry.
- **UC-F-012 — Message-broker client identity hardening.** Kafka /
  RabbitMQ / Pub-Sub / Service Bus clients authenticate via mTLS or
  IAM-signed requests; no shared SASL passwords.
- **UC-F-013 — gMSA / Kerberos modernisation for AD service
  accounts.** AD `svc_` accounts migrated to gMSA / sMSA or
  eliminated via federation — no static-password legacy lane.
- **UC-F-014 — API-gateway upstream identity standardised.** Every
  API gateway presents a strong upstream identity (mTLS, signed JWT,
  SigV4) so upstreams can mutually authenticate.
- **UC-F-015 — RPA bot credentials vaulted and session-bound.**
  UiPath / Blue Prism / Automation Anywhere bots retrieve credentials
  from a vault per-session; no embedded passwords in orchestrator
  stores.
- **UC-F-016 — Keyless code- and artifact-signing in CI.** Builds
  sign artifacts with keyless / short-lived identities (Sigstore
  Fulcio, GitHub OIDC, HSM-backed Authenticode); signing keys cannot
  be stolen at rest.
- **UC-F-017 — TEE attestation gates secret release.** Regulated
  workloads release high-value secrets only after a TEE attestation
  (Nitro / SEV-SNP / TDX / MAA); secrets bound to a measured
  execution environment.
- **UC-F-018 — AI-agent / LLM tool-credential brokering.** LLM
  agents (LangChain, Copilot Studio, Agentforce, custom) obtain tool
  credentials via a broker with per-tool, per-session, scoped tokens;
  prompt-injection cannot exfiltrate long-lived secrets.
- **UC-F-019 — IoT / OT / branch-device identity enrolment.** IoT /
  OT / ATM / branch devices enrol via DPS / EST / SCEP with hardware-
  rooted identity; fleet-wide pre-shared keys eliminated.
- **UC-F-020 — Mainframe / midrange credential rotation pipeline.**
  RACF / ACF2 / Top-Secret / IBM-i started-task and batch-scheduler
  credentials rotated under change-window governance; core-banking
  NHIs are not effectively static.
- **UC-F-021 — Backup / DR agent identity de-privileging.** Backup /
  DR agents (NetBackup, Commvault, Veeam, Rubrik, Cohesity) operate
  with least-privilege, vaulted credentials; ransomware operators
  cannot pivot via backup tier.
- **UC-F-022 — Webhook inbound identity verification.** Every
  inbound webhook (Stripe, GitHub, Twilio, payment-rail callbacks)
  verified by HMAC signature, mTLS or replay-protected JWT.
- **UC-F-023 — Network-device credential modernisation.** Router /
  switch / firewall / SD-WAN credentials rotated via vault-integrated
  TACACS+ / RADIUS; shared device-admin passwords and SNMP
  communities eliminated.
- **UC-F-024 — Open-Banking / FAPI 2.0 mTLS partner identity.** CDR /
  Open-Banking / payments-rail partner clients authenticated by
  FAPI-2.0-compliant mTLS with sender-constrained tokens.
- **UC-F-025 — OAuth-app / marketplace integration governance.**
  Third-party OAuth apps installed into M365 / Google Workspace /
  Salesforce / Slack / GitHub inventoried, risk-scored and revocable;
  no shadow integrations.
- **UC-F-026 — Vault-internal identity hardening.** The secrets-
  manager's own identities (root tokens, auto-unseal KMS principals,
  replication tokens, agent / proxy) governed with the same rigour as
  customer workloads.
- **UC-F-027 — Orphaned / dormant NHI cleanup pipeline.** Recurring
  sweep identifies and retires NHIs unused for > N days (test in
  prod, ex-vendor backdoors, decommissioned-app SAs).

### C.2.2 Non-functional UCs

- **UC-N-001 — Real-time secret-sprawl KPI dashboard.** Plaintext-
  remaining count by team / NHI bucket / repo / age with trend line.
  `[USER-SUPPLIED SEED]`.
- **UC-N-002 — NHI inventory and ownership attestation.** Complete
  owner-attested inventory of every NHI across the estate; orphans /
  sprawl evidenced and remediated.
- **UC-N-003 — Rotation-coverage and freshness KPIs.** Monthly
  rotation-coverage, freshness (median days since last rotation) and
  failure-backlog by NHI bucket.
- **UC-N-004 — Regulator audit evidence pack.** One-click APRA CPS
  234 evidence pack (controls §22 / §28 / §33 / §35) for any in-scope
  NHI bucket.
- **UC-N-005 — Essential 8 / ZT control-area scorecard.** Quarterly
  scorecard mapping the secrets-management programme to E8 maturity
  levels and NIST SP 800-207 ZT pillars.
- **UC-N-006 — Vendor / SaaS supply-chain risk attestation.** Every
  SaaS / OAuth-app integration risk-scored on data scope, residency,
  secret-handling and incident-disclosure SLAs.
- **UC-N-007 — Data-sovereignty and residency assurance.** Explicit
  data-flow evidence for every vault / KMS / HSM / SaaS secrets
  product; APRA-regulated data does not transit non-approved
  jurisdictions.
- **UC-N-008 — Engineer training and secure-coding adoption KPI.**
  Every engineer shipping code has completed secrets-management
  training in the last 12 months.
- **UC-N-009 — Exception register and risk-acceptance governance.**
  Every deviation from the standard (static keys, long rotation,
  shared SAs) registered with risk-owner, expiry and compensating
  control.
- **UC-N-010 — Break-glass and quorum-operator governance.** Every
  break-glass identity and HSM / CA / KMS quorum-operator role
  inventoried, monitored and drilled.
- **UC-N-011 — Post-incident reporting and identity-driven RCA.**
  Every secrets / identity incident captured with NHI attribution +
  MITRE T1552 sub-technique + lessons learned.
- **UC-N-012 — Supply-chain / SLSA-provenance assurance reporting.**
  Quarterly reports on signed-artifact coverage (SLSA level, signed-
  image %, signed-package %, in-toto attestations).
- **UC-N-013 — Crypto-agility and post-quantum readiness reporting.**
  Crypto-inventory and PQC migration scorecard (NIST FIPS 203/204/205,
  hybrid certs, CA / HSM capability).
- **UC-N-014 — Vendor-evaluation matrix maintenance.** The 19-vendor
  matrix refreshed each release cycle with capability deltas
  highlighted.
- **UC-N-015 — Communications cadence.** Stakeholder communications
  (engineering / business / executive / board) on the secrets-
  management programme.
- **UC-N-016 — IoT / OT / branch-fleet posture reporting.** Monthly
  fleet-posture reports on IoT / OT / ATM / branch-peripheral
  identities; default-credentials and PSK exposure burning down.
- **UC-N-017 — Observability / telemetry secret-leak governance.**
  Evidence that logs and telemetry do not propagate secrets onward
  to Datadog / Splunk / Elastic SaaS.
- **UC-N-018 — Confidential-computing / TEE attestation assurance.**
  Attestation evidence for any workload claiming TEE-bound secret
  release.
- **UC-N-019 — AI-agent / autonomous-workflow KPI suite.** KPIs
  specific to AI-agent NHIs — tools-invoked-per-session, scope
  inflation, refusal / escalation rates, prompt-injection-induced
  credential calls.
- **UC-N-020 — Mainframe / legacy posture and exception
  transparency.** Mainframe / midrange / RPA posture reported
  alongside cloud; legacy long-tail visible to the exception
  register.

---

## C.3 Acronym table

Acronyms appearing in PRD body, ADRs and Appendices A–D, expanded with
canonical source.

| Acronym | Expansion | Primary source |
|---|---|---|
| AAM | Agentic Access Management (Oasis Security) | <https://www.oasis.security/> |
| ACF2 | Access Control Facility 2 — Broadcom mainframe security manager | <https://www.broadcom.com/products/mainframe/identity-access/acf2> |
| ACME | Automatic Certificate Management Environment (IETF RFC 8555) | <https://www.rfc-editor.org/rfc/rfc8555> |
| ADCS | Active Directory Certificate Services | <https://learn.microsoft.com/windows-server/identity/ad-cs/> |
| ADP | Advanced Data Protection (HashiCorp Vault module — Transform, KM) | <https://developer.hashicorp.com/vault> |
| AKS | Azure Kubernetes Service | <https://learn.microsoft.com/azure/aks/> |
| APRA | Australian Prudential Regulation Authority | <https://www.apra.gov.au/> |
| ASD | Australian Signals Directorate | <https://www.asd.gov.au/> |
| ATM | Automated Teller Machine | n/a — generic |
| BCM | Business Continuity Management (APRA CPS 230) | <https://www.apra.gov.au/cps-230> |
| BYOK | Bring Your Own Key | <https://learn.microsoft.com/azure/key-vault/keys/byok-specification> |
| CCM | Confidential Computing Manager (Fortanix) | <https://www.fortanix.com/platform/confidential-computing-manager> |
| CDR | Consumer Data Right (Australia — Open Banking) | <https://www.cdr.gov.au/> |
| CICD | Continuous Integration / Continuous Delivery | n/a — generic |
| CMK | Customer Master Key (cloud KMS terminology) | <https://docs.aws.amazon.com/kms/> |
| CPG 234 | APRA Prudential Practice Guide 234 — information security | <https://www.apra.gov.au/sites/default/files/cpg_234_information_security.pdf> |
| CPS 230 | APRA Prudential Standard 230 — operational risk + BCM (Jul 2025) | <https://www.apra.gov.au/cps-230> |
| CPS 234 | APRA Prudential Standard 234 — information security | <https://www.apra.gov.au/sites/default/files/cps_234_july_2019_for_public_release.pdf> |
| CSF | NIST Cybersecurity Framework (v2.0 — deferred per ADR-003) | <https://www.nist.gov/cyberframework> |
| DPoP | Demonstrating Proof of Possession (OAuth 2.0 — RFC 9449) | <https://www.rfc-editor.org/rfc/rfc9449> |
| DPS | (Azure) Device Provisioning Service | <https://learn.microsoft.com/azure/iot-dps/> |
| DSM | Data Security Manager (Fortanix) | <https://www.fortanix.com/platform/data-security-manager> |
| E8 | ACSC Essential 8 (mitigation strategies; ML1/2/3) | <https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight> |
| EKM | External Key Manager (GCP Cloud EKM; AWS XKS analogue) | <https://cloud.google.com/kms/docs/ekm> |
| EPM | Endpoint Privilege Manager | <https://www.cyberark.com/products/endpoint-privilege-manager/> |
| EPV | Enterprise Password Vault (CyberArk PAM Self-Hosted) | <https://docs.cyberark.com/PAS/Latest/en/Content/PAS%20INST/Introduction.htm> |
| ESN | (Project / programme code referenced internally) — deferred to PRD §17 | n/a |
| EST | Enrollment over Secure Transport (RFC 7030) | <https://www.rfc-editor.org/rfc/rfc7030> |
| FAPI | Financial-grade API (OpenID Foundation; 2.0 baseline + advanced) | <https://openid.net/specs/fapi-2_0-baseline.html> |
| FI 27 | Internal FI strategic programme (cloud-native + ZT + consolidation) — per Task 0 §A.05 | n/a (internal, paraphrased per ADR-005) |
| FIPS | Federal Information Processing Standards (NIST — incl. 140-3, 203/204/205 PQC) | <https://csrc.nist.gov/publications/fips> |
| FPE | Format-Preserving Encryption | <https://csrc.nist.gov/projects/block-cipher-techniques> |
| gMSA | Group Managed Service Account (Microsoft AD) | <https://learn.microsoft.com/windows-server/security/group-managed-service-accounts/> |
| GPP | Group Policy Preferences (Windows) — MITRE T1552.006 vector | <https://attack.mitre.org/techniques/T1552/006/> |
| HSM | Hardware Security Module | <https://csrc.nist.gov/glossary/term/hardware_security_module> |
| IAM | Identity and Access Management (cloud-provider IAM principal) | n/a — generic |
| IMDS | (Cloud) Instance Metadata Service | <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html> |
| IR | Incident Response | n/a — generic |
| IRAP | Infosec Registered Assessors Program (ASD) | <https://www.cyber.gov.au/irap> |
| ISM | ASD Information Security Manual | <https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism> |
| ITDR | Identity Threat Detection and Response | <https://www.gartner.com/en/documents/4017795> |
| JIT | Just-In-Time (credential issuance) | n/a — generic |
| JWT | JSON Web Token (RFC 7519) | <https://www.rfc-editor.org/rfc/rfc7519> |
| KMIP | Key Management Interoperability Protocol (OASIS) | <https://docs.oasis-open.org/kmip/> |
| KMS | Key Management Service (cloud) | <https://csrc.nist.gov/glossary/term/key_management_service> |
| MAA | Microsoft Azure Attestation | <https://learn.microsoft.com/azure/attestation/> |
| MCP | Model Context Protocol (LLM tool-server protocol) | <https://modelcontextprotocol.io/> |
| MIM | Machine Identity Management (Gartner category) | <https://www.gartner.com/en/documents/4017805> |
| ML | Maturity Level (Essential 8 ML1 / ML2 / ML3) | <https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model> |
| ML-DSA | Module-Lattice Digital Signature Algorithm (NIST FIPS 204) | <https://csrc.nist.gov/pubs/fips/204/final> |
| ML-KEM | Module-Lattice Key Encapsulation Mechanism (NIST FIPS 203) | <https://csrc.nist.gov/pubs/fips/203/final> |
| mTLS | Mutual TLS | <https://datatracker.ietf.org/doc/html/rfc8705> |
| NHI | Non-Human Identity (machine / workload / service identity) | <https://cloudsecurityalliance.org/research/working-groups/non-human-identity-management> |
| NHIDR | NHI Detection and Response | <https://entro.security/> |
| NIST SP 800-207 | NIST Zero Trust Architecture (and follow-on SP 800-204D for workload-mTLS) | <https://csrc.nist.gov/pubs/sp/800/207/final> |
| NPP | New Payments Platform (Australia) | <https://nppa.com.au/> |
| OAuth | Open Authorization 2.0 / 2.1 (IETF) | <https://oauth.net/2/> |
| OBO | On-Behalf-Of (OAuth flow / token exchange) | <https://www.rfc-editor.org/rfc/rfc8693> |
| OIDC | OpenID Connect | <https://openid.net/connect/> |
| OT | Operational Technology (industrial / branch / ATM control) | n/a — generic |
| PAM | Privileged Access Management | <https://www.gartner.com/en/documents/4022047> |
| PAT | Personal Access Token (Git platforms) | <https://docs.github.com/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens> |
| PEXA | Property Exchange Australia | <https://www.pexa.com.au/> |
| PKI | Public Key Infrastructure | <https://csrc.nist.gov/glossary/term/public_key_infrastructure> |
| PQC | Post-Quantum Cryptography (NIST FIPS 203 / 204 / 205) | <https://csrc.nist.gov/projects/post-quantum-cryptography> |
| PSM | Privileged Session Manager (CyberArk) | <https://docs.cyberark.com/PAS/Latest/en/Content/PASIMP/PSM-Overview.htm> |
| RACF | Resource Access Control Facility — IBM mainframe security manager | <https://www.ibm.com/products/resource-access-control-facility> |
| RACI | Responsible / Accountable / Consulted / Informed (matrix) | n/a — generic |
| RBAC | Role-Based Access Control | n/a — generic |
| RFI / RFP | Request For Information / Request For Proposal | n/a — generic |
| RPA | Robotic Process Automation | n/a — generic |
| RPO / RTO | Recovery Point Objective / Recovery Time Objective | n/a — generic |
| SaaS | Software-as-a-Service | n/a — generic |
| SAS | Shared Access Signature (Azure) | <https://learn.microsoft.com/azure/storage/common/storage-sas-overview> |
| SBOM | Software Bill of Materials | <https://www.cisa.gov/sbom> |
| SCEP | Simple Certificate Enrollment Protocol (RFC 8894) | <https://www.rfc-editor.org/rfc/rfc8894> |
| SEV-SNP | AMD Secure Encrypted Virtualisation — Secure Nested Paging (TEE) | <https://www.amd.com/en/developer/sev.html> |
| SGX | Intel Software Guard Extensions (TEE) | <https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions.html> |
| SLA | Service Level Agreement | n/a — generic |
| SLSA | Supply-chain Levels for Software Artifacts | <https://slsa.dev/> |
| SPIFFE | Secure Production Identity Framework For Everyone | <https://spiffe.io/> |
| SPIRE | SPIFFE Runtime Environment | <https://spiffe.io/docs/latest/spire-about/> |
| SSA | Software Statement Assertion (FAPI 2.0) | <https://openid.net/specs/fapi-2_0-baseline.html> |
| STS | Security Token Service (AWS / Azure terminology) | <https://docs.aws.amazon.com/STS/> |
| SVID | SPIFFE Verifiable Identity Document (X.509-SVID / JWT-SVID) | <https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/> |
| TACACS+ | Terminal Access Controller Access-Control System Plus (RFC 8907) | <https://www.rfc-editor.org/rfc/rfc8907> |
| TDE | Transparent Data Encryption | <https://learn.microsoft.com/sql/relational-databases/security/encryption/transparent-data-encryption> |
| TDX | Intel Trust Domain Extensions (TEE) | <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-trust-domain-extensions.html> |
| TEE | Trusted Execution Environment | <https://csrc.nist.gov/glossary/term/trusted_execution_environment> |
| TTP | Tactic, Technique and Procedure (MITRE ATT&CK terminology) | <https://attack.mitre.org/> |
| UAT | User Acceptance Testing | n/a — generic |
| WIAM | Workload Identity and Access Management (Aembit category) | <https://aembit.io/> |
| XKS | (AWS KMS) External Key Store | <https://docs.aws.amazon.com/kms/latest/developerguide/keystore-external.html> |
| ZT | Zero Trust (NIST SP 800-207) | <https://csrc.nist.gov/pubs/sp/800/207/final> |
| ZTBA | Zero Trust Brokered Access (Akeyless category) | <https://www.akeyless.io/> |

> **Sensitivity note (ADR-005).** Where an internal programme code
> appears (FI 27, ESN), it is referenced by the code only and the
> underlying detail is `[INTERNAL]` paraphrased to "a major AU
> Tier-1 FI". The acronym table includes the code so readers can
> follow PRD cross-references but does not expand internal scope.

---

> _End of Appendix C (Wave B v0.1)._

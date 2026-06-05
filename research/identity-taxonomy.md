# Machine Identity (NHI) Taxonomy — XYZ Secrets-Management PRD

**Sensitivity:** [PUBLIC] — independent of XYZ-specific evidence.
**Author:** Identity Taxonomist sub-agent (Opus 4.7), 2026-05-21.
**Version:** v0.1.

---

## 1. Scope and methodology

This taxonomy enumerates Non-Human Identity (NHI) types that any
secrets-management programme — and the 12-vendor evaluation matrix —
must address. The list is biased toward **breadth** so the PRD can
challenge product owners' "the familiar five" mental model. We anchor
to four canonical references: the Cloud Security Alliance NHI Working
Group taxonomy [csa-nhi-taxonomy-2024]; Gartner's Machine Identity
Management (MIM) market guide framing [gartner-mim-2023]; the SPIFFE /
SPIRE workload-identity specification [spiffe-spec-2023]; and the
Sigstore / cosign workload-signing model [sigstore-arch-2023]. NIST
SP 800-63-4 [nist-sp-800-63-4-2024], SP 800-57 [nist-sp-800-57-2020]
and SP 800-204D [nist-sp-800-204d-2024] supply lifecycle, key-management
and service-mesh framing. Each row is tagged `[COMMON]` (most product
owners recognise it) or `[UNCOMMON]` (the long tail that is routinely
overlooked yet materially expands blast radius). Every claim links to
a primary URL or carries `[INDUSTRY-CONSENSUS]` / `[SPECULATION]`.

## 2. Identity classification axes

We classify each NHI along five orthogonal axes:

1. **Lifecycle** — `EPHEMERAL` (<1h), `SHORT-LIVED` (≤24h),
   `LONG-LIVED` (>24h–90d), `STATIC` (rotation-on-incident only).
2. **Trust anchor** — self-attested, third-party IdP (OIDC/SAML),
   hardware-rooted (TPM/HSM/TEE), or shared-secret.
3. **Authentication shape** — X.509 certificate, asymmetric keypair,
   bearer token (JWT/OAuth), API key / shared secret, Kerberos ticket.
4. **Governance maturity (industry typical)** — `LOW` / `MEDIUM` /
   `HIGH` based on whether ownership, rotation and revocation are
   programmatic across the enterprise. Per CSA NHI WG, most enterprises
   sit `LOW`–`MEDIUM` outside Tier-1 hyperscale shops
   [csa-nhi-state-2024].
5. **NHI vs human-shared** — pure NHI, or an identity humans and
   machines both authenticate as (service accounts in AD, shared
   "automation" users). Human-shared identities are the most common
   audit finding [verizon-dbir-2024].

These axes feed CSV columns and PRD §7 "what good looks like" tables.

## 3. COMMON identities (the familiar majority)

### NHI-001 — Cloud IAM principal (role / service account) `[COMMON]`
- **What it is:** A workload-bound principal in AWS IAM, Azure AD
  (Entra) managed identity, or GCP service account, used by compute
  resources to call cloud APIs.
- **Where it appears:** EC2/EKS, Lambda, Azure VMs / Functions / AKS,
  GCE / GKE / Cloud Run.
- **Typical secrets / credentials:** STS tokens, managed-identity
  tokens, GCP metadata-server tokens, service-account JSON keys
  (legacy).
- **Lifecycle:** SHORT-LIVED (STS / metadata tokens) or LONG-LIVED
  (JSON keys, IAM access keys).
- **Governance maturity:** MEDIUM.
- **Citations:** [aws-iam-roles-2024], [azure-managed-identity-2024],
  [gcp-sa-2024].

### NHI-002 — Kubernetes ServiceAccount `[COMMON]`
- **What it is:** Pod-bound identity issued by the K8s API server,
  projected as a short-lived JWT via the TokenRequest API.
- **Where it appears:** EKS, AKS, GKE, OpenShift, Rancher, bare-metal
  K8s.
- **Typical secrets / credentials:** Projected service-account tokens
  (audience-bound JWTs), legacy long-lived SA tokens (deprecated).
- **Lifecycle:** SHORT-LIVED (default 1h, configurable).
- **Governance maturity:** MEDIUM.
- **Citations:** [k8s-sa-tokens-2024], [k8s-tokenrequest-2024].

### NHI-003 — CI/CD pipeline identity `[COMMON]`
- **What it is:** GitHub Actions, GitLab CI, Azure DevOps, Jenkins, or
  CircleCI job identity. Increasingly OIDC-federated to cloud IAM.
- **Where it appears:** Source-to-cloud build pipelines, IaC apply
  jobs, container-build pipelines.
- **Typical secrets / credentials:** OIDC ID tokens, repository / org
  secrets, deploy keys, PATs.
- **Lifecycle:** EPHEMERAL (per-job OIDC) or LONG-LIVED (PATs, deploy
  keys).
- **Governance maturity:** LOW–MEDIUM (PATs sprawl).
- **Citations:** [github-oidc-2024], [gitlab-oidc-2024].

### NHI-004 — Container / image-pull credential `[COMMON]`
- **What it is:** Registry credential used by orchestrators and build
  tools to pull container images.
- **Where it appears:** ECR/ACR/GAR/Harbor/Artifactory; `imagePullSecret`
  in K8s.
- **Typical secrets / credentials:** OAuth2 tokens, docker-config
  JSON, robot accounts.
- **Lifecycle:** SHORT-LIVED to LONG-LIVED.
- **Governance maturity:** MEDIUM.
- **Citations:** [docker-registry-token-2024], [harbor-robot-2024].

### NHI-005 — Database service account `[COMMON]`
- **What it is:** Application-to-database principal (RDBMS, NoSQL,
  warehouse) for reads/writes.
- **Where it appears:** PostgreSQL, MySQL, Oracle, MSSQL, MongoDB,
  Snowflake, BigQuery, Redshift, Cassandra.
- **Typical secrets / credentials:** Username/password, client
  certificates, IAM-DB tokens (RDS IAM, Cloud SQL IAM).
- **Lifecycle:** LONG-LIVED to STATIC (common rotation failure mode).
- **Governance maturity:** LOW–MEDIUM.
- **Citations:** [aws-rds-iam-auth-2024], [snowflake-key-pair-2024].

### NHI-006 — Application TLS server / mTLS workload identity `[COMMON]`
- **What it is:** X.509 identity for a web/API workload (server TLS)
  or mTLS workload-to-workload identity (e.g., SPIFFE/SPIRE).
- **Where it appears:** Ingress, API gateways, service mesh (Istio,
  Linkerd, Consul), gRPC services.
- **Typical secrets / credentials:** X.509 certificates + private
  keys, SPIFFE SVIDs (X.509-SVID, JWT-SVID).
- **Lifecycle:** SHORT-LIVED (SPIFFE typically 1h) to LONG-LIVED
  (90-day public CA certs).
- **Governance maturity:** MEDIUM.
- **Citations:** [spiffe-spec-2023], [istio-mtls-2024].

### NHI-007 — Third-party SaaS API key / OAuth client `[COMMON]`
- **What it is:** OAuth client credential or static API key used to
  call an external SaaS (Salesforce, Workday, ServiceNow, Slack,
  Datadog, etc.).
- **Where it appears:** Integration platforms (Mulesoft, Workato,
  Boomi), iPaaS, in-app integrations.
- **Typical secrets / credentials:** OAuth client_id+secret, refresh
  tokens, static API keys, webhook signing secrets.
- **Lifecycle:** LONG-LIVED to STATIC.
- **Governance maturity:** LOW.
- **Citations:** [oauth2-rfc6749-2012], [astrix-nhi-report-2024].

### NHI-008 — Git platform credential (PAT, SSH key, deploy key) `[COMMON]`
- **What it is:** Source-control identity used by humans, bots, and
  pipelines to read/write code and trigger workflows.
- **Where it appears:** GitHub, GitLab, Bitbucket, Azure Repos.
- **Typical secrets / credentials:** Personal Access Tokens (PATs),
  fine-grained tokens, SSH keys, deploy keys, GitHub App
  installation tokens.
- **Lifecycle:** LONG-LIVED (PATs/SSH) to SHORT-LIVED (App tokens).
- **Governance maturity:** LOW (PAT sprawl is endemic per GitGuardian
  state-of-secrets report).
- **Citations:** [gitguardian-sots-2024], [github-fine-grained-2023].

### NHI-009 — Configuration-management / IaC agent identity `[COMMON]`
- **What it is:** Ansible Automation Platform, Puppet, Chef,
  Terraform Cloud / Enterprise, Pulumi agents.
- **Where it appears:** Build farms, control planes, ephemeral
  runners.
- **Typical secrets / credentials:** Tower/AAP credentials, Vault
  AppRoles, Terraform Cloud team tokens, dynamic cloud creds.
- **Lifecycle:** SHORT-LIVED to LONG-LIVED.
- **Governance maturity:** MEDIUM.
- **Citations:** [hashicorp-tfc-2024], [ansible-aap-2024].

### NHI-010 — Monitoring / observability agent `[COMMON]`
- **What it is:** Datadog, Splunk forwarders, Dynatrace OneAgent,
  Prometheus exporters, Elastic Beats, New Relic agents.
- **Where it appears:** Every host and container; SaaS endpoints.
- **Typical secrets / credentials:** API keys, ingest tokens, mTLS
  certs.
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW (often baked into golden images).
- **Citations:** [datadog-agent-keys-2024],
  [splunk-hec-token-2024].

### NHI-011 — Message broker / event-bus client `[COMMON]`
- **What it is:** Producer/consumer client for Kafka, RabbitMQ,
  Pulsar, SQS/SNS, Service Bus, Pub/Sub, Event Grid.
- **Where it appears:** Event-driven microservices, ingestion
  pipelines.
- **Typical secrets / credentials:** SASL/SCRAM creds, mTLS certs,
  IAM signed requests, shared-access signatures (SAS).
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW–MEDIUM.
- **Citations:** [kafka-security-2024], [azure-sb-sas-2024].

### NHI-012 — Active Directory / LDAP service account `[COMMON]`
- **What it is:** Domain service accounts (`svc_`-prefixed) used by
  on-prem and hybrid workloads.
- **Where it appears:** Windows file/print, SQL Server, SharePoint,
  Exchange hybrid, legacy Java apps via Kerberos / LDAPS.
- **Typical secrets / credentials:** Passwords (often never rotated),
  Kerberos keys, gMSA / sMSA, msDS-KeyCredentialLink.
- **Lifecycle:** STATIC (or LONG-LIVED via gMSA).
- **Governance maturity:** LOW.
- **Citations:** [ms-gmsa-2024], [ms-spn-2024].

### NHI-013 — Reverse-proxy / API-gateway upstream identity `[COMMON]`
- **What it is:** Identity an API gateway (Apigee, Kong, AWS API GW,
  Azure APIM, F5, NGINX+) presents to upstream services.
- **Where it appears:** North-south traffic boundary.
- **Typical secrets / credentials:** mTLS client certs, signed JWTs,
  HMAC keys, AWS SigV4 IAM creds.
- **Lifecycle:** SHORT-LIVED to LONG-LIVED.
- **Governance maturity:** MEDIUM.
- **Citations:** [apigee-mtls-2024], [aws-apigw-iam-2024].

### NHI-014 — RPA bot identity `[COMMON]`
- **What it is:** UiPath, Blue Prism, Automation Anywhere robot
  identity — frequently authenticated as a "real" AD user.
- **Where it appears:** Back-office automation (banking, insurance),
  attended and unattended bots.
- **Typical secrets / credentials:** AD user passwords vaulted in
  Orchestrator, MFA bypass tokens, browser session cookies.
- **Lifecycle:** STATIC (passwords rotated on schedule, not on use).
- **Governance maturity:** LOW.
- **Citations:** [uipath-creds-2024], [blueprism-creds-2024].

## 4. NOT-SO-COMMON identities (the overlooked long tail)

### NHI-015 — Code-signing identity (Sigstore / Authenticode / Apple) `[UNCOMMON]`
- **What it is:** Identity that signs binaries, container images,
  packages, or SBOM attestations. Often ephemeral (Sigstore Fulcio)
  or hardware-backed (Authenticode HSM, Apple Notary).
- **Where it appears:** Build pipelines, release engineering, app
  stores, kernel modules, container registries.
- **Typical secrets / credentials:** Fulcio short-lived certs, EV /
  OV code-signing certs in HSM, Apple Developer ID keys, GPG keys
  for package repos.
- **Lifecycle:** EPHEMERAL (Sigstore: ~10 min) to LONG-LIVED
  (Authenticode).
- **Governance maturity:** LOW–MEDIUM.
- **Citations:** [sigstore-arch-2023], [ms-authenticode-2024],
  [apple-notary-2024].

### NHI-016 — Build provenance / SLSA attestation identity `[UNCOMMON]`
- **What it is:** Identity that signs in-toto / SLSA provenance
  statements proving how an artifact was built.
- **Where it appears:** GitHub Actions reusable workflows, GitLab
  SLSA, Buildkite, Tekton Chains.
- **Typical secrets / credentials:** Sigstore keyless OIDC creds,
  TUF root keys, in-toto layout keys.
- **Lifecycle:** EPHEMERAL.
- **Governance maturity:** LOW.
- **Citations:** [slsa-spec-2024], [in-toto-spec-2024].

### NHI-017 — Service mesh control-plane identity `[UNCOMMON]`
- **What it is:** Identity the mesh control plane (Istiod, Linkerd
  identity, Consul Connect CA) uses to mint workload SVIDs.
- **Where it appears:** Every meshed K8s cluster.
- **Typical secrets / credentials:** Intermediate-CA private keys,
  bootstrap tokens, root-CA trust bundles.
- **Lifecycle:** LONG-LIVED (rotated quarterly at best).
- **Governance maturity:** LOW (often unknown to the secrets team).
- **Citations:** [istio-ca-2024], [consul-connect-ca-2024].

### NHI-018 — Confidential-computing attestation identity `[UNCOMMON]`
- **What it is:** Identity rooted in a TEE (Intel SGX/TDX, AMD SEV-SNP,
  AWS Nitro Enclaves, Azure Confidential VMs, GCP Confidential Space)
  that attests measurements before secret release.
- **Where it appears:** Regulated workloads (key-management,
  privacy-preserving analytics, ML model protection).
- **Typical secrets / credentials:** Attestation reports / quotes,
  ephemeral RSA keys bound to measurement, MAA / Nitro attestation
  documents.
- **Lifecycle:** EPHEMERAL.
- **Governance maturity:** LOW.
- **Citations:** [nitro-enclaves-attestation-2024],
  [azure-maa-2024], [confidential-space-2024].

### NHI-019 — AI agent / autonomous workflow identity `[UNCOMMON]`
- **What it is:** LLM-driven agent (LangChain, AutoGen, MS Copilot
  Studio, Agentforce, custom agentic frameworks) calling tools, APIs,
  and human-facing systems on behalf of a user or business process.
- **Where it appears:** Customer-service automation, internal
  copilots, RAG pipelines, agentic coding tools.
- **Typical secrets / credentials:** OAuth on-behalf-of tokens,
  static tool API keys, retrieval-store creds, model-provider keys,
  vector-DB tokens. Increasingly the most over-scoped NHI class.
- **Lifecycle:** SHORT-LIVED (token) to LONG-LIVED (tool keys).
- **Governance maturity:** LOW.
- **Citations:** [owasp-llm-top10-2024], [csa-ai-agents-2024],
  [astrix-nhi-report-2024].

### NHI-020 — Model artifact / registry identity `[UNCOMMON]`
- **What it is:** Identity that pushes/pulls trained models or
  weights from a model registry (MLflow, SageMaker Model Registry,
  Hugging Face, Vertex Model Garden, Azure ML).
- **Where it appears:** ML platforms, model-promotion pipelines.
- **Typical secrets / credentials:** Registry tokens, S3 / GCS / Blob
  credentials, signed model artifacts (model-cards-as-attestations).
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW.
- **Citations:** [hf-tokens-2024], [sagemaker-registry-2024].

### NHI-021 — IoT / OT device identity `[UNCOMMON]`
- **What it is:** Per-device identity for sensors, gateways, ATMs,
  POS terminals, branch-printer fleets, building-management systems,
  EV chargers. Often hardware-rooted (TPM, secure element).
- **Where it appears:** AWS IoT Core, Azure IoT Hub, GCP IoT
  (deprecated), branch / ATM networks, smart buildings.
- **Typical secrets / credentials:** Per-device X.509, DPS-issued
  certs, TPM-attested keys, symmetric pre-shared keys (legacy).
- **Lifecycle:** LONG-LIVED (often device lifetime).
- **Governance maturity:** LOW.
- **Citations:** [aws-iot-x509-2024], [azure-iot-dps-2024].

### NHI-022 — Mainframe / midrange service identity `[UNCOMMON]`
- **What it is:** RACF, ACF2, Top Secret userIDs used by started
  tasks (STCs), CICS region IDs, IMS dependent-region IDs, batch
  scheduler IDs (Control-M, OPCA); also AS/400 (IBM i) profiles.
- **Where it appears:** Core banking, payments switching, batch
  windows.
- **Typical secrets / credentials:** RACF passphrases, MFA tokens
  (IBM MFA), digital certs in RACF keyrings, ICSF master keys.
- **Lifecycle:** STATIC (rotation requires change windows).
- **Governance maturity:** LOW–MEDIUM (mature audit, weak rotation).
- **Citations:** [ibm-racf-2024], [ibm-icsf-2024].

### NHI-023 — Database encryption key-custodian principal (TDE/CMK) `[UNCOMMON]`
- **What it is:** The non-human **KMS/HSM custodian principal** that
  controls TDE/CMK master keys for SQL Server, Oracle TDE, PostgreSQL
  pgcrypto, AlwaysEncrypted, MongoDB CSFLE.
- **NPE conformance `[CREDENTIAL-NOT-IDENTITY]`:** the master *key
  itself is a managed secret, not an identity* (NIST NPE / OWASP). This
  row models the controlling principal, not the key — re-worded
  2026-06-03 per the regulator audit.
- **Where it appears:** Every regulated database.
- **Typical secrets / credentials:** KMS CMK ARN + KMS key policy,
  HSM partition credential, Always Encrypted CMK in Azure KV.
- **Lifecycle:** LONG-LIVED (key rotation per NIST SP 800-57).
- **Governance maturity:** MEDIUM.
- **Citations:** [nist-sp-800-57-2020], [aws-kms-tde-2024].

### NHI-024 — HSM/KMS operator (HUMAN-privileged — out of NHI scope) `[UNCOMMON]`
- **What it is:** Privileged **human** operators administering the
  HSM (CloudHSM, Thales Luna, nCipher nShield, Entrust, Utimaco) or
  the KMS control plane, usually quorum-protected (M-of-N).
- **NPE conformance `[HUMAN-IDENTITY]`:** reclassified **human** per
  NIST NPE ("not a human actor"); PED keys / smartcards are held by
  people. The non-human KMS auto-unseal principal is **NHI-035**.
  Retained for FK traceability; governed via UC-N-010.
- **Where it appears:** PCI cryptographic boundary, root-of-trust
  ceremonies, post-quantum migration prep.
- **Typical secrets / credentials:** PED keys, smartcards, quorum
  shares (Shamir), CloudHSM CO/CU/AU principals.
- **Lifecycle:** LONG-LIVED to STATIC.
- **Governance maturity:** MEDIUM–HIGH where mandated; LOW elsewhere.
- **Citations:** [thales-luna-roles-2024],
  [aws-cloudhsm-users-2024].

### NHI-025 — Private-CA operator roles (HUMAN — out of NHI scope) `[UNCOMMON]`
- **What it is:** Privileged **human** PKI roles in private CA
  (Microsoft ADCS, EJBCA, Venafi TPP/TLSPC, Keyfactor Command, AWS
  Private CA, GCP CAS) — RA, CA admin, auditor, enrolment agent.
- **NPE conformance `[HUMAN-IDENTITY]`:** reclassified **human** per
  NIST NPE; the non-human **issuing-CA signing identity** is the true
  NHI (mesh CA = **NHI-017**). Retained for FK traceability; governed
  via UC-N-010.
- **Where it appears:** Internal PKI, ACME endpoints, EST/SCEP for
  IoT, mTLS issuance.
- **Typical secrets / credentials:** Smartcard-bound admin certs,
  enrolment-agent certs, CA private keys in HSM, ACME EAB keys.
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** MEDIUM.
- **Citations:** [venafi-tpp-2024], [keyfactor-command-2024].

### NHI-026 — Backup / DR agent identity `[UNCOMMON]`
- **What it is:** NetBackup, Commvault, Veeam, Rubrik, Cohesity,
  Druva agent identities with cross-system read access — a prime
  ransomware target.
- **Where it appears:** Every regulated estate; air-gapped vaults.
- **Typical secrets / credentials:** Privileged AD service accounts,
  hypervisor admin creds, immutable-storage tokens (object-lock).
- **Lifecycle:** STATIC.
- **Governance maturity:** LOW (per recent ransomware post-mortems).
- **Citations:** [cisa-ransomware-2024], [veeam-perms-2024].

### NHI-027 — Backend-for-frontend / on-behalf-of token holder `[UNCOMMON]`
- **What it is:** Service identities that exchange user tokens for
  downstream-API tokens (OAuth 2.0 token exchange, OBO flow, JWT
  bearer grant).
- **Where it appears:** BFF tier, microservice graphs that propagate
  user identity (e.g., banking customer 360).
- **Typical secrets / credentials:** Confidential-client secrets,
  signed JWT assertions (private_key_jwt), DPoP keys.
- **Lifecycle:** SHORT-LIVED (tokens) backed by LONG-LIVED keys.
- **Governance maturity:** LOW–MEDIUM.
- **Citations:** [rfc8693-token-exchange-2020],
  [fapi2-baseline-2024].

### NHI-028 — Federated B2B / Open Banking client identity `[UNCOMMON]`
- **What it is:** mTLS / FAPI 2.0 client identities used by partner
  banks, fintechs and CDR data recipients (Australian Consumer Data
  Right).
- **Where it appears:** Open Banking, payments rails (PEXA, NPP),
  Swift / Swift Alliance, ASX trading interfaces.
- **Typical secrets / credentials:** mTLS client certs (FAPI 2.0
  requires sender-constrained tokens), software-statement assertions
  (SSAs), DPoP keys.
- **Lifecycle:** LONG-LIVED (cert) / SHORT-LIVED (token).
- **Governance maturity:** MEDIUM (regulator-driven).
- **Citations:** [acccdr-2024], [fapi2-baseline-2024].

### NHI-029 — Shared functional service account (human-used NHI) `[UNCOMMON]`
- **What it is:** A non-human service account whose **risk is
  concurrent use by multiple humans AND scripts** — the OWASP
  **NHI10:2025 "Human Use of NHI"** anti-pattern; common in legacy ops
  and outsourced run teams.
- **NPE conformance `[HUMAN-USE-ANTIPATTERN]`:** the account is an NHI;
  the human use is the governance defect, not a second identity class.
- **Where it appears:** Unix `oracle`, `sapadm`, `weblogic`; Windows
  `svc_batch`; shared Tableau / Power BI service users.
- **Typical secrets / credentials:** Long passwords, SSH keys in
  shared filesystems, RDP saved creds.
- **Lifecycle:** STATIC.
- **Governance maturity:** LOW.
- **Citations:** [verizon-dbir-2024], [cis-controls-v8-2021].

### NHI-030 — Browser / SaaS extension and OAuth-app identity `[UNCOMMON]`
- **What it is:** Third-party app installed into Google Workspace,
  M365, Salesforce, Slack, GitHub Apps — operating with delegated
  scopes against tenant data.
- **Where it appears:** Anywhere users can self-install OAuth apps.
- **Typical secrets / credentials:** OAuth refresh tokens (long-lived),
  app-installation tokens, webhook secrets, marketplace API keys.
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW (the "shadow integration" problem).
- **Citations:** [astrix-nhi-report-2024], [salesforce-connected-apps-2024].

### NHI-031 — Webhook / inbound integration identity `[UNCOMMON]`
- **What it is:** Inbound caller identity asserted via HMAC-signed
  webhooks, mTLS, or replay-protected JWTs (Stripe, GitHub, Twilio,
  payment gateways).
- **Where it appears:** Event-driven integrations, fraud feeds,
  payment notifications.
- **Typical secrets / credentials:** HMAC signing secrets, webhook
  endpoint secrets, JWKs.
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW.
- **Citations:** [stripe-webhook-sigs-2024],
  [github-webhook-sigs-2024].

### NHI-032 — Network / infrastructure device identity `[UNCOMMON]`
- **What it is:** Router, switch, firewall, load-balancer, SD-WAN
  edge identity used by NetOps automation (Ansible, Terraform,
  vendor controllers) and TACACS+/RADIUS-authenticated principals.
- **Where it appears:** WAN backbone, branch routers, DC fabric,
  cloud transit gateways, F5 / NetScaler / Palo Alto Panorama.
- **Typical secrets / credentials:** SSH keys, TACACS+ shared
  secrets, SNMPv3 creds, vendor cloud-controller tokens (Meraki,
  Panorama, Aruba Central).
- **Lifecycle:** STATIC.
- **Governance maturity:** LOW.
- **Citations:** [tacacs-rfc8907-2020], [cisa-network-defaults-2024].

### NHI-033 — Print / spooler / branch-peripheral identity `[UNCOMMON]`
- **What it is:** Network printer, MFP, cheque scanner, ATM
  peripheral, kiosk identities — historically authenticated via
  default credentials.
- **Where it appears:** Branch networks, retail floors, ATM
  enclosures.
- **Typical secrets / credentials:** SNMPv3 creds, 802.1X EAP-TLS
  certs, default admin creds (very common gap).
- **Lifecycle:** STATIC.
- **Governance maturity:** LOW.
- **Citations:** [cisa-default-creds-2024], [nist-sp-800-213-2021].

### NHI-034 — Post-quantum / hybrid-PKI crypto-agility attribute `[UNCOMMON]`
- **What it is:** **Not a distinct identity** — a **cross-cutting
  crypto-migration attribute** of existing PKI identities (NHI-006,
  NHI-017, NHI-025) during post-quantum (NIST PQC: ML-KEM, ML-DSA,
  SLH-DSA) and hybrid-cert rollouts: dual-signed certificates,
  PQC-capable CAs and HSMs. On every Tier-1 bank's 2026–2028 roadmap.
- **NPE conformance `[CROSS-CUTTING-ATTRIBUTE]`:** dual-signed certs are
  *credentials, not actors*; tracked as a lifecycle attribute via
  UC-N-013 rather than a standalone NHI.
- **Where it appears:** Internal PKI roadmaps, regulator briefings
  (APRA, ASD, NIST), payment-rail working groups.
- **Typical secrets / credentials:** Hybrid X.509 (classical + PQC),
  ML-DSA private keys, composite signatures.
- **Lifecycle:** LONG-LIVED.
- **Governance maturity:** LOW (early-adopter only).
- **Citations:** [nist-pqc-fips-203-204-205-2024],
  [asd-pqc-guidance-2024].

### NHI-035 — Vault-internal / secrets-broker identity `[UNCOMMON]`
- **What it is:** The vault's own service identities — auto-unseal
  KMS principals, replication tokens, performance / DR replication
  identities, agent / proxy identities (Vault Agent, CyberArk Conjur
  follower, Akeyless gateway). The vault itself is an NHI.
- **Where it appears:** Inside every secrets-management deployment.
- **Typical secrets / credentials:** Root tokens, recovery keys
  (Shamir), Sentinel policy admin tokens, auto-unseal KMS keys.
- **Lifecycle:** LONG-LIVED / STATIC.
- **Governance maturity:** MEDIUM (mature vaults) to LOW (sprawl).
- **Citations:** [hashicorp-vault-auto-unseal-2024],
  [cyberark-conjur-followers-2024].

### NHI-036 — Ephemeral workload via SPIFFE / Aembit / Clutch `[UNCOMMON]`
- **What it is:** "Zero-trust workload identity" issued just-in-time
  to a workload after attestation (kernel, K8s, AWS metadata, etc.),
  replacing static secrets. Aembit / Clutch / Akeyless ZTBA brokers
  exemplify the pattern.
- **Where it appears:** Modern microservice estates, cross-cloud
  brokering, agentic-AI tool calls.
- **Typical secrets / credentials:** Short-lived JWTs, X.509-SVIDs,
  signed-attestation-bound tokens.
- **Lifecycle:** EPHEMERAL.
- **Governance maturity:** LOW (early adoption).
- **Citations:** [spiffe-spec-2023], [aembit-arch-2024].

### NHI-037 — Forgotten / orphaned legacy identity `[UNCOMMON]`
- **What it is:** Decommissioned-app service accounts still active,
  expired-team credentials, "test" accounts in production, ex-vendor
  back-doors. The class most-often abused in breaches per Verizon
  DBIR.
- **Where it appears:** Everywhere; surfaced only by attestation /
  ITDR sweeps.
- **Typical secrets / credentials:** Anything — but rarely rotated.
- **Lifecycle:** STATIC.
- **Governance maturity:** LOW.
- **Citations:** [verizon-dbir-2024], [csa-nhi-state-2024].

## 5. Cross-cutting concerns

**Ephemerality is not free.** Replacing a long-lived secret with a
1-hour token reduces blast radius but multiplies issuance traffic;
the trust anchor (KMS, SPIRE, IdP) becomes a Tier-0 dependency whose
own NHIs (NHI-035) must be hardened
[spiffe-spec-2023][nist-sp-800-204d-2024].

**Federation moves blame, not risk.** OIDC-federated CI/CD removes
PATs but concentrates trust in the IdP signing key (an NHI in itself)
and in cloud trust-policy hygiene; mis-scoped `sub`/`aud` conditions
remain a primary attack vector [github-oidc-2024].

**Blast radius scales with privilege × persistence × reachability.**
A static, highly-privileged backup or RPA identity (NHI-014, NHI-026)
trumps an ephemeral pod token in real-world risk
[cisa-ransomware-2024][verizon-dbir-2024].

**Vault sprawl is the predictable failure mode.** Most regulated
estates run 3–7 vault systems (cloud-native + HashiCorp + CyberArk +
legacy) plus hidden caches in CI variables, K8s Secrets, observability
configs, mainframe RACF keyrings. The taxonomy above intentionally
surfaces these caches as identity-classes.

**Secrets in observability dashboards.** Datadog, Splunk and Elastic
agents (NHI-010) routinely ingest logs containing secrets;
agent-credentials themselves are LOW-governance. Treat as a control
in PRD §11 [datadog-agent-keys-2024].

**Post-quantum readiness.** NIST FIPS 203/204/205 (ML-KEM, ML-DSA,
SLH-DSA) were finalised in 2024; ASD has issued PQC migration
guidance; APRA-regulated entities must plan crypto-agility for
NHI-023 / NHI-025 / NHI-034 by 2030 [nist-pqc-fips-203-204-205-2024]
[asd-pqc-guidance-2024].

**AU sovereignty.** Vault, KMS and HSM control-plane identities
processing APRA-regulated data must respect CPS 230 / CPS 234 data
residency and BCM requirements; offshore SaaS vault choices (e.g.,
Doppler, Infisical SaaS, 1Password) need explicit data-flow analysis
[apra-cps-230-2023][apra-cps-234-2019].

## 6. Open questions for v1.0 deep-dive

- Is **AI agent identity (NHI-019)** a distinct PRD section or a
  cross-cutting concern that re-uses NHI-007 / NHI-027 patterns?
- Do we require **Sigstore / SLSA (NHI-015 / NHI-016)** as in-scope
  for v0.1 or defer to v1.0 supply-chain track?
- How do we treat **mainframe (NHI-022)** — first-class column in
  the dual matrix, or appendix?
- ~~Where do **HSM operator (NHI-024)** and **CA operator (NHI-025)**
  identities live~~ — **Resolved 2026-06-03 (regulator audit):** both
  are **human** identities per NIST NPE → flagged `HUMAN-IDENTITY`, out
  of strict NHI scope; the non-human counterparts are NHI-035 (KMS) and
  NHI-017 (mesh CA). See
  [`matrix/REGULATOR-AUDIT-2026-06-03.md`](../matrix/REGULATOR-AUDIT-2026-06-03.md).
- Should **forgotten / orphaned (NHI-037)** be a row, or a
  cross-cutting maturity dimension?
- Do **vault-internal identities (NHI-035)** get evaluated against
  the same matrix as the products under evaluation?
- ~~**PQC (NHI-034)** — explicit roadmap item in v0.1 or v1.0?~~ —
  **Resolved 2026-06-03:** not a distinct identity; reclassified as a
  `CROSS-CUTTING-ATTRIBUTE` of PKI identities, tracked via UC-N-013.
- Treatment of **Open Banking / FAPI 2.0 (NHI-028)** identities given
  ACCC CDR sectoral expansion to non-bank lenders in 2026.
- ~~Confirm classification of **service-account-as-human (NHI-029)**~~ —
  **Resolved 2026-06-03:** it is an NHI; the human use is the OWASP
  NHI10:2025 anti-pattern, flagged `HUMAN-USE-ANTIPATTERN`.

## 7. Citations

See `meta/citations.bib`. BibTeX keys used above are appended to that
file in this commit.

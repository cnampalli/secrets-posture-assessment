# Vendor Profile — AWS Secrets Manager

**Tier:** cloud-native
**Primary docs:** https://docs.aws.amazon.com/secretsmanager/
**Profile written:** 2026-05-22
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

AWS Secrets Manager is an AWS-managed SaaS service for storing, rotating, and retrieving secrets (database credentials, API keys, OAuth tokens, TLS certificates) across AWS workloads. Owned by Amazon Web Services (Amazon.com, Inc.), it is a fully managed, multi-tenant, regional control-plane service with no self-hosted deployment option. The primary differentiator is native, first-class integration with every major AWS service — IAM, KMS, RDS, Aurora, Redshift, DocumentDB, ECS, EKS, Lambda, Bedrock, SageMaker, and 50+ others — combined with managed rotation that requires no Lambda function for supported AWS databases. AU presence: fully GA in ap-southeast-2 (Sydney); ap-southeast-4 (Melbourne) is an AWS region but Secrets Manager availability must be confirmed per the AWS Region table. Cross-region secret replication to Melbourne is supported where the region is enabled. IRAP PROTECTED-assessed (verified November 2025). [PUBLIC]

---

## 2. Architecture (≤ 250 words)

**Storage backend:** AWS-managed, regionally distributed, serverless store. Secrets are stored as versioned JSON blobs (up to 64 KB). No customer-controlled storage backend.

**Auth methods:** Exclusively AWS IAM — identity-based policies (IAM roles, users, groups) and resource-based policies on secrets. Supports ABAC via IAM condition keys (`secretsmanager:ResourceTag/*`). Cross-account access via resource-based policies. VPC endpoint (Interface type, PrivateLink) available for private connectivity from VPCs without internet egress.

**Encryption:** Envelope encryption with AWS KMS. Every secret value is encrypted with a 256-bit AES data key; the data key is itself encrypted by a KMS key (AWS-managed `aws/secretsmanager` or customer-managed CMK). KMS External Key Store (XKS) supported — allows CMKs whose key material lives in an on-premises or collocated HSM (e.g., Thales CipherTrust, Entrust nShield) accessible via XKS Proxy. AWS CloudHSM can back KMS CMKs via a CloudHSM cluster-backed custom key store. Secret metadata (name, tags, rotation config) is NOT encrypted.

**Secrets engines:** Single engine: opaque key-value / JSON blob store. No dynamic credential generation native to the service (rotation is Lambda-mediated or managed by source AWS services). Dynamic DB credentials require Lambda rotation functions or managed rotation (RDS/Aurora/Redshift/DocumentDB natively supported without Lambda).

**Replication / DR:** One primary + N replicas across any enabled AWS regions. Replicas are read-only; rotation on primary propagates automatically. Cross-region replica uses a per-region KMS key.

**Compliance:** IRAP PROTECTED (AU, last assessed November 2025), FedRAMP High (US-East/West, GovCloud), SOC 1/2/3, PCI DSS Level 1, ISO/IEC 27001/27017/27018, HIPAA, OSPAR (SG). No FedRAMP equivalent AU PROTECTED+ tier declared.

---

## 3. NHI coverage map (≤ 600 words)

| NHI-ID | Coverage | Maturity | Evidence |
|---|---|---|---|
| NHI-001 Cloud IAM principal | NATIVE | 4 | IAM roles, instance profiles, STS tokens natively consumed; IAM identity-based + resource-based policies. [aws-sm-auth-2024] |
| NHI-002 Kubernetes ServiceAccount | NATIVE | 4 | EKS IRSA projects SA tokens to assume IAM roles; secrets-store-csi-driver-provider-aws mounts secrets; External Secrets Operator (ESO) syncs. [aws-sm-eks-2024] |
| NHI-003 CI/CD pipeline identity | NATIVE | 4 | GitHub Actions OIDC → IAM role assumption + `aws-actions/aws-secretsmanager-get-secrets@v2`; GitLab CI OIDC supported. [aws-sm-github-2024] |
| NHI-004 Container image-pull credential | ADD-ON | 2 | ECR tokens stored/rotated in Secrets Manager via Lambda; no native ECR imagePullSecret sync. [aws-sm-ecr-2024] |
| NHI-005 Database service account | NATIVE | 4 | Managed rotation (no Lambda) for RDS, Aurora, Redshift, DocumentDB master creds; Lambda rotation for other DBs. [aws-sm-rotation-2024] |
| NHI-006 App TLS / mTLS workload identity | ADD-ON | 2 | AWS Private CA (ACM PCA) is a separate product; ECS Service Connect managed rotation for TLS certs via Secrets Manager. No native SPIFFE/SPIRE issuance. [aws-ecs-sc-tls-2024] |
| NHI-007 Third-party SaaS API key | NATIVE | 3 | Generic opaque storage and Lambda-based rotation for any API key type. [aws-sm-intro-2024] |
| NHI-008 Git platform credential | NATIVE | 3 | Generic opaque storage; no native git-platform rotation Lambda templates (custom Lambda required). [aws-sm-intro-2024] |
| NHI-009 IaC / config-management agent | NATIVE | 3 | Terraform AWS provider reads secrets at apply-time; Ansible lookup plugin; SSM Parameter Store also usable for IaC vars. [aws-sm-intro-2024] |
| NHI-010 Monitoring / observability agent | NATIVE | 3 | Generic opaque storage and rotation; no native Datadog/Splunk rotation templates (custom Lambda). [aws-sm-intro-2024] |
| NHI-011 Message broker / event-bus client | NATIVE | 3 | Amazon MSK (Kafka) SASL/SCRAM creds stored and rotated via Secrets Manager integration. [aws-sm-integrations-2024] |
| NHI-012 AD / LDAP service account | ADD-ON | 2 | No native AD connector; Lambda rotation can call AD APIs. AWS Directory Service integration exists but does not auto-rotate AD passwords. [INDUSTRY-CONSENSUS] |
| NHI-013 API gateway upstream identity | NATIVE | 3 | AWS API Gateway IAM SigV4 creds and certificates managed through IAM + Secrets Manager; JWT authoriser secrets stored natively. [aws-sm-intro-2024] |
| NHI-014 RPA bot identity | ADD-ON | 1 | No native RPA connector; opaque storage only; custom Lambda rotation required. [INDUSTRY-CONSENSUS] |
| NHI-015 Code-signing identity | GAP | 0 | AWS Signer is a separate service; Secrets Manager does not manage Sigstore/Authenticode identities. [INDUSTRY-CONSENSUS] |
| NHI-016 Build provenance / SLSA attestation | GAP | 0 | No SLSA attestation management; separate CodeBuild/OIDC patterns needed. [INDUSTRY-CONSENSUS] |
| NHI-017 Service mesh control-plane identity | ADD-ON | 1 | Mesh CA certs can be stored; no native Istio/Linkerd CA rotation. [INDUSTRY-CONSENSUS] |
| NHI-018 Confidential-computing attestation | NATIVE | 3 | AWS Nitro Enclaves attestation document validates before secret release via IAM condition `kms:RecipientAttestation`. [nitro-enclaves-attestation-2024] |
| NHI-019 AI agent / autonomous workflow | ADD-ON | 2 | Amazon Bedrock and SageMaker integrations listed; agents consume secrets via IAM execution roles, but no agent-specific scoping or per-session brokering. [aws-sm-integrations-2024] |
| NHI-020 Model artifact / registry identity | ADD-ON | 2 | SageMaker AI integration listed; model registry tokens stored; no dynamic model-registry credential issuance. [aws-sm-integrations-2024] |
| NHI-021 IoT / OT device identity | ADD-ON | 2 | AWS IoT SiteWise integration listed; per-device certs via AWS IoT Core (separate service); Secrets Manager stores device credentials. [aws-sm-integrations-2024] |
| NHI-022 Mainframe / midrange service identity | GAP | 0 | No RACF/ACF2/IBM i integration; no mainframe connector. [INDUSTRY-CONSENSUS] |
| NHI-023 Database encryption / TDE master key | NATIVE | 3 | KMS CMK stores TDE master keys; Secrets Manager stores custodian identity credentials; KMS XKS enables BYOK from on-prem HSM. [aws-sm-encryption-2024] |
| NHI-024 HSM / KMS operator / break-glass identity | NATIVE | 3 | CloudHSM CO/CU/AU identities and quorum-protected KMS key policies; Secrets Manager stores HSM operator credentials. [aws-cloudhsm-users-2024] |
| NHI-025 CA operator identity | ADD-ON | 2 | AWS Private CA (separate product) manages CA identities; Secrets Manager can store CA admin credentials. [INDUSTRY-CONSENSUS] |
| NHI-026 Backup / DR agent identity | NATIVE | 3 | AWS Backup service-linked role credentials; Secrets Manager stores backup admin creds; cross-region replication for DR. [aws-sm-replication-2024] |
| NHI-027 Backend-for-frontend / OBO token | ADD-ON | 2 | Confidential client secrets stored; no native OBO token exchange broker; custom Lambda required. [INDUSTRY-CONSENSUS] |
| NHI-028 Federated B2B / Open Banking client | GAP | 0 | No native FAPI 2.0 / CDR mTLS client cert lifecycle management; AWS Private CA is separate; no Open Banking-specific integration. [INDUSTRY-CONSENSUS] |
| NHI-029 Service-account-as-human (shared functional ID) | ADD-ON | 2 | Generic credential storage and rotation; no IGA-style attestation or human/machine disambiguation. [INDUSTRY-CONSENSUS] |
| NHI-030 Browser / SaaS extension / OAuth-app | GAP | 0 | No SaaS OAuth-app inventory or shadow-integration discovery capability. [INDUSTRY-CONSENSUS] |
| NHI-031 Webhook / inbound integration identity | NATIVE | 2 | HMAC signing secrets and webhook tokens stored natively; no native replay-protection enforcement. [aws-sm-intro-2024] |
| NHI-032 Network / infrastructure device identity | ADD-ON | 1 | Generic credential storage; no native TACACS+/RADIUS integration or network-device rotation templates. [INDUSTRY-CONSENSUS] |
| NHI-033 Print / spooler / branch peripheral | GAP | 0 | No IoT peripheral cert management; AWS IoT Core is the appropriate separate service. [INDUSTRY-CONSENSUS] |
| NHI-034 Quantum-resistant / hybrid-PKI rotation identity | ADD-ON | 1 | KMS supports post-quantum key exchange (ML-KEM hybrid) in preview (2024 announcement); Secrets Manager inherits KMS PQC roadmap but no hybrid-cert management. [INDUSTRY-CONSENSUS] |
| NHI-035 Vault-internal / secrets-broker identity | NATIVE | 3 | IAM service-linked role for Secrets Manager; auto-unseal equivalent is KMS-backed; no Shamir root-token recovery (AWS-managed service). Cross-region replication token managed by AWS. [aws-sm-auth-2024] |
| NHI-036 Ephemeral workload via SPIFFE / Aembit | GAP | 0 | No native SPIFFE SVID issuance; SPIRE integration requires partner tooling (external-secrets.io). [INDUSTRY-CONSENSUS] |
| NHI-037 Forgotten / orphaned legacy identity | ADD-ON | 2 | AWS Config rules detect unused secrets; Security Hub CSPM finds rotation-overdue secrets; IAM Access Analyzer flags cross-account exposure. No automated dormancy-based retirement pipeline. [aws-sm-compliance-2024] |

**NHI split:** NATIVE=20, ADD-ON=10, PARTNER=0, GAP=7, N/A=0

---

## 4. Use-case scoring (≤ 800 words)

| UC-ID | Coverage | Maturity | Evidence |
|---|---|---|---|
| UC-F-001 Prevent plaintext secrets in source repos | ADD-ON | 2 | No native pre-commit or push-protection; GitHub Actions OIDC + Secrets Manager integration eliminates long-lived keys in CI variables. [aws-sm-github-2024] |
| UC-F-002 Detect/remediate secrets already in history | GAP | 0 | No native repo-scanning capability; AWS does not offer secret-scanning equivalent to GitGuardian. [INDUSTRY-CONSENSUS] |
| UC-F-003 JIT short-lived cloud credentials via OIDC | NATIVE | 4 | GitHub Actions and GitLab OIDC → IAM role → Secrets Manager is documented natively; STS short-lived tokens eliminate long-lived keys. [aws-sm-github-2024] |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | GAP | 0 | No native SPIFFE/SPIRE; EKS IRSA is analogous but JWT-scoped, not SVID-based. [INDUSTRY-CONSENSUS] |
| UC-F-005 Dynamic database credentials with leases | NATIVE | 4 | Managed rotation (RDS/Aurora/Redshift/DocumentDB) + Lambda rotation for others; alternating-user strategy documented. [aws-sm-rotation-2024] |
| UC-F-006 Automated rotation of long-lived static secrets | NATIVE | 4 | Cron/rate rotation schedules, managed rotation without Lambda, Lambda rotation templates for generic secrets. [aws-sm-rotation-2024] |
| UC-F-007 Immediate revocation on identity compromise | NATIVE | 3 | IAM deny policies propagate in seconds; secret deletion/disable immediate; CloudTrail captures all API calls. No SOAR native playbook — integrates via EventBridge. [aws-sm-monitoring-2024] |
| UC-F-008 K8s secret consumption without on-disk plaintext | NATIVE | 4 | Secrets Store CSI Driver (AWS provider) mounts secrets as tmpfs volumes; IRSA authenticates pods; etcd encryption separately enforced. [aws-sm-eks-2024] |
| UC-F-009 Container image-pull credentials per workload | ADD-ON | 2 | ECR short-lived tokens via IAM roles for EKS nodes/pods; Secrets Manager stores ECR credentials for non-AWS registries. [aws-sm-ecr-2024] |
| UC-F-010 IaC / config-mgmt secrets injected at apply-time | NATIVE | 3 | Terraform AWS provider (`aws_secretsmanager_secret_version` data source); Ansible AWS collection; no native state-file scanner. [aws-sm-intro-2024] |
| UC-F-011 Observability-agent credentials rotated | NATIVE | 3 | Generic rotation via Lambda for Datadog/Splunk/Dynatrace API keys; no out-of-box rotation template for observability vendors. [aws-sm-rotation-2024] |
| UC-F-012 Message-broker client identity hardening | NATIVE | 3 | Amazon MSK + Secrets Manager SASL/SCRAM integration natively documented. [aws-sm-integrations-2024] |
| UC-F-013 gMSA / Kerberos modernisation for AD service accounts | GAP | 0 | No AD connector or gMSA rotation; AWS Directory Service does not expose gMSA through Secrets Manager. [INDUSTRY-CONSENSUS] |
| UC-F-014 API-gateway upstream identity standardised | NATIVE | 3 | API Gateway IAM SigV4, JWT authoriser secrets, and mutual TLS cert ARNs stored in Secrets Manager. [aws-sm-intro-2024] |
| UC-F-015 RPA bot credentials vaulted and session-bound | ADD-ON | 1 | Generic opaque storage only; no UiPath/Blue Prism/Automation Anywhere connector. [INDUSTRY-CONSENSUS] |
| UC-F-016 Keyless code- and artifact-signing in CI | GAP | 0 | AWS Signer is separate; no Sigstore/Fulcio integration in Secrets Manager. [INDUSTRY-CONSENSUS] |
| UC-F-017 TEE attestation gates secret release | NATIVE | 3 | Nitro Enclaves attestation condition in KMS key policy gates secret decryption; policy-enforced measurement binding. [nitro-enclaves-attestation-2024] |
| UC-F-018 AI-agent / LLM tool-credential brokering | ADD-ON | 2 | Bedrock/SageMaker agents access secrets via execution role IAM; no per-session scoped token issuance or prompt-injection audit trail. [aws-sm-integrations-2024] |
| UC-F-019 IoT / OT / branch-device identity enrolment | ADD-ON | 2 | AWS IoT Core handles DPS/EST/SCEP (separate service); IoT SiteWise integration with Secrets Manager listed. [aws-sm-integrations-2024] |
| UC-F-020 Mainframe / midrange credential rotation pipeline | GAP | 0 | No mainframe connector; RACF/IBM i not addressable from Secrets Manager. [INDUSTRY-CONSENSUS] |
| UC-F-021 Backup / DR agent identity de-privileging | NATIVE | 3 | AWS Backup service-linked role; Secrets Manager stores backup credentials; cross-region replication for DR resilience. [aws-sm-replication-2024] |
| UC-F-022 Webhook inbound identity verification | NATIVE | 2 | HMAC signing secrets stored; rotation via Lambda; no replay-protection enforcement built in. [aws-sm-intro-2024] |
| UC-F-023 Network-device credential modernisation | GAP | 0 | No TACACS+/RADIUS integration or network-device rotation templates; custom Lambda required. [INDUSTRY-CONSENSUS] |
| UC-F-024 Open-Banking / FAPI 2.0 mTLS partner identity | GAP | 0 | No FAPI 2.0 / CDR mTLS cert lifecycle; AWS Private CA is separate and requires additional integration work. [INDUSTRY-CONSENSUS] |
| UC-F-025 OAuth-app / marketplace integration governance | GAP | 0 | No OAuth-app inventory or shadow-integration discovery; not a feature of Secrets Manager. [INDUSTRY-CONSENSUS] |
| UC-F-026 Vault-internal identity hardening | NATIVE | 3 | KMS-backed service; no root-token risk (AWS-managed); IAM SCPs restrict admin operations; CloudTrail logs all control-plane actions. [aws-sm-encryption-2024] |
| UC-F-027 Orphaned / dormant NHI cleanup pipeline | ADD-ON | 2 | AWS Config managed rules (`secretsmanager-secret-unused`, `secretsmanager-rotation-enabled-check`); Security Hub surfaces overdue secrets; no automated retirement pipeline. [aws-sm-compliance-2024] |
| UC-N-001 Real-time secret-sprawl KPI dashboard | ADD-ON | 2 | Security Hub + Config aggregated dashboard; no native secret-sprawl KPI covering non-AWS repos. [aws-sm-compliance-2024] |
| UC-N-002 NHI inventory and ownership attestation | NATIVE | 3 | AWS Resource Explorer + Config inventory; tags for ownership; no automated owner re-attestation workflow. [aws-sm-compliance-2024] |
| UC-N-003 Rotation-coverage and freshness KPIs | NATIVE | 3 | Config rule `secretsmanager-rotation-enabled-check` + CloudWatch metrics; Security Hub aggregates. [aws-sm-monitoring-2024] |
| UC-N-004 Regulator audit evidence pack | NATIVE | 3 | CloudTrail immutable logs; AWS Artifact provides IRAP/SOC/PCI audit reports; Config compliance timeline. [aws-sm-compliance-2024] |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 2 | Security Hub CSPM maps to CIS benchmarks; no out-of-box Essential 8 scorecard; manual mapping required. [aws-sm-compliance-2024] |
| UC-N-006 Vendor / SaaS supply-chain risk attestation | ADD-ON | 2 | AWS Artifact provides vendor attestations; no native SaaS integration risk-scoring within Secrets Manager. [aws-sm-compliance-2024] |
| UC-N-007 Data-sovereignty and residency assurance | NATIVE | 4 | ap-southeast-2 (Sydney) confirmed; VPC endpoints enforce data stays in region; KMS key policy `kms:ViaService` locks to region endpoint; replication explicit and customer-controlled. [aws-sm-replication-2024] |
| UC-N-008 Engineer training and secure-coding adoption KPI | GAP | 0 | Not a Secrets Manager function; AWS offers training via AWS Skill Builder separately. [INDUSTRY-CONSENSUS] |
| UC-N-009 Exception register and risk-acceptance governance | ADD-ON | 1 | No native exception register; Config non-compliance findings can feed GRC tools via EventBridge. [INDUSTRY-CONSENSUS] |
| UC-N-010 Break-glass and quorum-operator governance | NATIVE | 3 | CloudHSM quorum authentication; KMS key policy M-of-N grants; CloudTrail captures all break-glass API calls. [aws-cloudhsm-users-2024] |
| UC-N-011 Post-incident reporting and identity-driven RCA | NATIVE | 3 | CloudTrail + GuardDuty + Security Hub provide identity-attributed incident timeline; EventBridge SOAR integration. [aws-sm-monitoring-2024] |
| UC-N-012 Supply-chain / SLSA-provenance assurance reporting | GAP | 0 | No SLSA provenance management; AWS Signer and CodeArtifact are separate services. [INDUSTRY-CONSENSUS] |
| UC-N-013 Crypto-agility and PQC readiness reporting | ADD-ON | 2 | KMS key inventory via Config; PQC hybrid key exchange in KMS preview (2024); no crypto-agility dashboard. [INDUSTRY-CONSENSUS] |
| UC-N-014 Vendor-evaluation matrix maintenance | N/A | 0 | Not applicable — this is a procurement/governance process, not a product feature. |
| UC-N-015 Communications / stakeholder cadence | N/A | 0 | Not applicable — organisational process. |
| UC-N-016 IoT / OT / branch-fleet posture reporting | ADD-ON | 2 | AWS IoT Device Defender provides fleet posture; Secrets Manager stores device credentials; separate service required for reporting. [aws-sm-integrations-2024] |
| UC-N-017 Observability/telemetry secret-leak governance | ADD-ON | 2 | CloudWatch Logs metric filters can detect secret patterns; no native log-scrubbing enforcement. [aws-sm-monitoring-2024] |
| UC-N-018 Confidential-computing / TEE attestation assurance | NATIVE | 3 | Nitro Enclaves attestation logs in CloudTrail; KMS policy enforces attestation condition; policy review supported. [nitro-enclaves-attestation-2024] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | GAP | 0 | No AI-agent-specific KPI suite; Bedrock CloudTrail logs cover invocation but not per-tool credential issuance. [INDUSTRY-CONSENSUS] |
| UC-N-020 Mainframe / legacy posture and exception transparency | GAP | 0 | No mainframe integration; legacy posture for non-AWS identities not addressable. [INDUSTRY-CONSENSUS] |

**UC split:** NATIVE=19, ADD-ON=16, PARTNER=0, GAP=10, N/A=2

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **Unmatched AWS-native depth.** For pure-AWS workloads, Secrets Manager is industry-leading (maturity 4) across the most critical NHIs: cloud IAM principals (NHI-001), Kubernetes service accounts via EKS IRSA (NHI-002), CI/CD OIDC pipelines (NHI-003), and database credentials with managed rotation (NHI-005). The GitHub Actions `aws-actions/aws-secretsmanager-get-secrets@v2` action and GitLab OIDC integration are fully documented native paths, eliminating long-lived CI pipeline secrets. Managed rotation for RDS/Aurora/Redshift/DocumentDB requires no Lambda code — this is the most operationally mature rotation offering in the evaluated set for AWS databases.

2. **KMS + CloudHSM + XKS encryption depth.** Envelope encryption with AES-256 data keys is mandatory (no plaintext storage). Customer-managed CMKs, CloudHSM-backed KMS custom key stores, and KMS External Key Store (XKS) for BYOK from on-premises HSMs give a genuine path to hardware-rooted encryption. The `kms:ViaService` condition locks decryption to Secrets Manager context, preventing key misuse.

3. **AU sovereignty + IRAP PROTECTED assurance.** Sydney (ap-southeast-2) is fully available; cross-region replication to any enabled region is customer-controlled. IRAP PROTECTED assessed and listed in scope as of November 2025 — the strongest available compliance mark for Australian government and APRA-regulated workloads. CloudTrail + Security Hub + Config provide immutable audit trails suitable for APRA CPS 234 evidence packs.

### Top 3 gaps

1. **Single-cloud lock-in.** Secrets Manager provides no meaningful capability for Azure, GCP, or on-premises non-AWS workloads. Multi-cloud secrets federation requires a separate tool (HashiCorp Vault, CyberArk, etc.).

2. **No SPIFFE / SVID / workload-attestation native path.** UC-F-004 and NHI-036 are structural GAPs. EKS IRSA is a close analogue but is not SPIFFE-compliant.

3. **Long-tail NHI gaps.** Mainframe (NHI-022), AD/gMSA (NHI-012 beyond basic storage), Open Banking FAPI 2.0 (NHI-028), RPA orchestrators (NHI-014), and SLSA/code-signing (NHI-015/016) are all GAP or ADD-ON at low maturity — requiring partner tooling or custom Lambda.

---

## 6. AU-specific notes (≤ 150 words)

**Sydney (ap-southeast-2):** Fully GA. All Secrets Manager features including managed rotation, cross-region replication, VPC endpoints, and KMS CMKs are available. Confirmed in AWS Region table.

**Melbourne (ap-southeast-4):** AWS region launched February 2023. Secrets Manager availability should be verified in the AWS Region Services table before assuming feature parity; as of this profile, Melbourne is an enabled region for replication targets.

**IRAP PROTECTED:** AWS Secrets Manager listed in scope as of 6 November 2025 (verified at aws.amazon.com/compliance/services-in-scope/IRAP/). The 2025 H1 IRAP report is available via AWS Artifact. No PROTECTED+ tier exists in IRAP framework — PROTECTED is the ceiling.

**APRA CPS 234 / CPS 230:** CloudTrail + Config + Security Hub provide the control-evidence artefacts required by CPS 234 §28, §33, §35. Data-residency is enforced via regional endpoints and VPC endpoint policies. Cross-border replication is explicit and customer-initiated.

**Essential 8:** No out-of-box E8 maturity scorecard; manual mapping from Security Hub CIS controls to E8 required.

---

## 7. Citations

BibTeX keys appended to `meta/citations.bib` under `## AWS Secrets Manager (Agent 03 wave 2)`:

- `aws-sm-intro-2024`
- `aws-sm-rotation-2024`
- `aws-sm-auth-2024`
- `aws-sm-encryption-2024`
- `aws-sm-replication-2024`
- `aws-sm-monitoring-2024`
- `aws-sm-compliance-2024`
- `aws-sm-pricing-2024`
- `aws-sm-github-2024`
- `aws-sm-eks-2024`
- `aws-sm-ecr-2024`
- `aws-sm-integrations-2024`
- `aws-irap-scope-2025`
- `nitro-enclaves-attestation-2024`
- `aws-cloudhsm-users-2024`

---

## 8. Open questions for v1.0

1. **Melbourne (ap-southeast-4) Secrets Manager GA status** — AWS does not explicitly list per-region service availability for every service in documentation; confirm via AWS Region Services table or account team before recommending as DR replica target.

2. **IRAP PROTECTED scope depth** — The IRAP assessment covers the service, but which specific features (cross-region replication, XKS, CloudHSM custom key store) are within the assessed boundary? APRA-regulated entities should request the AWS IRAP consumer guide from AWS Artifact.

3. **KMS XKS latency and reliability** — Docs warn that XKS cryptographic operations "might take longer and be less reliable and durable." What are the SLA implications for APRA-regulated workloads requiring HSM BYOK?

4. **AI agent per-session credential scoping** — Bedrock Agents use IAM execution roles for Secrets Manager access. Is there a documented pattern for per-session, per-tool scoped secret issuance that would satisfy UC-F-018 without custom Lambda?

5. **Multi-cloud posture** — For XYZ's hybrid/multi-cloud workloads touching Azure or GCP, what is the recommended integration pattern (e.g., AWS Secrets Manager + External Secrets Operator on AKS/GKE)?

6. **Open Banking / CDR B2B** — AWS provides no native FAPI 2.0 mTLS client cert lifecycle tooling. Is AWS Private CA + ACM sufficient with manual Secret Manager integration, or does CDR mandate a dedicated PKI product?

7. **Managed rotation for non-AWS databases** — MongoDB Atlas, Snowflake, Oracle, and MSSQL require custom Lambda rotation functions. What is the maintenance burden for these Lambda functions at enterprise scale?

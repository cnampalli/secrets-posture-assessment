# Google Cloud Secret Manager

**Sensitivity:** [PUBLIC]
**Vendor slug:** `gcp-secret-manager`
**Tier:** cloud-native
**Research date:** 2026-05-22
**Author:** Vendor Researcher sub-agent (Sonnet 4.6), XYZ Secrets-Management PRD M2 Wave 2

---

## 1. Product overview

Google Cloud Secret Manager is a fully managed secrets-storage service on Google Cloud Platform. It stores arbitrary blobs (API keys, passwords, certificates, TLS private keys, connection strings) as versioned secrets, with access controlled via Cloud IAM and payload encrypted at rest using Google-managed or customer-managed keys. Secret Manager is a regional and global service available in 30+ regions including both Australian regions (`australia-southeast1` Sydney, `australia-southeast2` Melbourne). It is closely paired with Cloud KMS, Cloud HSM, and Cloud EKM for key management, and with Cloud IAM for identity-based access.

**Core capabilities:**
- Versioned secrets with enabled/disabled/destroyed states
- Automatic (multi-region) or user-managed (specific regions) replication policies
- CMEK via Cloud KMS (software, HSM-backed, or externally-managed keys)
- IAM-based access control at project and per-secret resource level
- Cloud Audit Logs integration (ADMIN_WRITE, ADMIN_READ, DATA_READ, DATA_WRITE)
- Rotation notifications via Pub/Sub topics (cron-style schedule; $0.05/notification after 3 free)
- Integrations with GKE, Cloud Run, App Engine, Compute Engine, Cloud Functions, GKE Workload Identity

---

## 2. Australian regional availability and data residency

| Region | Regional Secret Manager | Parameter Manager |
|---|---|---|
| `australia-southeast1` (Sydney) | **Yes** | Yes |
| `australia-southeast2` (Melbourne) | **Yes** | Yes |

User-managed replication allows pinning secrets to one or both AU regions exclusively, satisfying APRA CPS 230 / CPS 234 data residency requirements. Automatic replication stores data across multiple Google-managed locations globally; it is **not** suitable where strict AU data residency is mandated. For regulated use cases (PROTECTED, APRA-regulated), user-managed replication to `australia-southeast1` + `australia-southeast2` is the recommended pattern. [gcp-sm-locations-2025]

Cloud KMS CMEK keys can be provisioned in either AU region; Cloud EKM connections can be configured to point to on-premises or partner-hosted HSMs within Australia. [gcp-sm-cmek-2025]

---

## 3. IRAP PROTECTED status

An independent third-party IRAP assessor evaluated Google Cloud and Google Workspace against OFFICIAL and PROTECTED ISM controls, finding both "strongly aligned with PROTECTED level control requirements." The assessment covers cyber security roles, incident detection and management, physical and personnel security, system hardening, networking, and cryptography. [gcp-irap-2025]

The ASD's CCSL was deprecated in July 2020. The current framework requires cloud service providers to undergo IRAP assessments, with agencies responsible for their own risk-managed authorisation. Google makes assessment reports available via the Compliance Reports Manager (available to GCP customers). The GCP platform assessment scope covers the core platform including IAM, Cloud KMS, Cloud Logging, and related services. **Specific inclusion of Secret Manager and Cloud HSM should be verified against the current IRAP assessment report available in the GCP Compliance Reports Manager.**

Key IRAP control areas addressed by GCP platform:
- Cryptography: Cloud KMS + Cloud HSM (FIPS 140-2 L3) + Cloud EKM
- Access control: Cloud IAM with fine-grained resource-level policies
- Audit: Cloud Audit Logs (mandatory admin activity; configurable data access)
- Incident management: Security Command Center + Cloud Logging

**Note for XYZ:** Given that XYZ Bank processes data at OFFICIAL: Sensitive (likely not PROTECTED), GCP's IRAP alignment is likely sufficient. Agencies processing PROTECTED must validate the current assessment scope against Secret Manager and Cloud KMS/HSM. [gcp-irap-2025]

---

## 4. Identity integration (NHI mapping)

### 4.1 Cloud IAM Service Accounts (NHI-001) — NATIVE

GCP Service Accounts are the primary identity primitive for workloads accessing Secret Manager. The `roles/secretmanager.secretAccessor` role grants `secretmanager.versions.access` and can be bound at the project level (access all secrets) or per-secret resource (least privilege). Workloads running on GCE, Cloud Run, Cloud Functions, GKE receive Application Default Credentials (ADC) automatically from the metadata server — no long-lived key files required. [gcp-sm-access-2025]

### 4.2 GKE Workload Identity (NHI-002) — NATIVE

GKE Workload Identity Federation allows Kubernetes ServiceAccounts to be bound to IAM service accounts without exporting JSON key files. The GKE metadata server intercepts ADC requests, exchanges the Kubernetes JWT for a federated access token via Security Token Service (STS), and returns short-lived credentials. Pods can then call `secretmanager.googleapis.com` directly. The Secrets Store CSI Driver with the GCP provider enables mounting secrets as files or environment variables. [gcp-gke-wi-2025]

### 4.3 CI/CD Pipeline Identity via Workload Identity Federation (NHI-003) — NATIVE

Workload Identity Federation (WIF) supports any OIDC or SAML 2.0 identity provider, including GitHub Actions, GitLab CI, Terraform Cloud, CircleCI, and Jenkins. Pipelines exchange short-lived OIDC tokens for GCP access tokens without storing long-lived service account JSON keys. WIF attribute mappings allow fine-grained conditions (e.g., only a specific GitHub repo/branch). [gcp-wif-2025]

### 4.4 Encryption / KMS / HSM (NHI-023, NHI-024) — NATIVE

- **Google-managed encryption:** AES-256 at rest by default, no configuration required.
- **CMEK via Cloud KMS (software):** Customer creates Cloud KMS key; Secret Manager encrypts payload with it. Key rotation managed by Cloud KMS policy.
- **CMEK via Cloud HSM:** Keys backed by FIPS 140-2 Level 3 certified HSMs; Google manages HSM cluster (no patching/clustering required). Cloud HSM is available in major regions.
- **Cloud EKM (bring-your-own external keys):** Key material never leaves the external HSM. Supported partners include Fortanix (documented as Cloud EKM partner — relevant to XYZ's Fortanix DSM migration story), Futurex, and Thales. Partner-managed EKM includes sovereign partner configurations. [gcp-hsm-2025, gcp-ekm-2025]

### 4.5 Rotation (UC-F-006 alignment)

Secret Manager provides **rotation notifications** via Pub/Sub, not built-in managed rotation. Configuration:
- Attach a Pub/Sub topic to a secret
- Set `rotation_period` (minimum 1 hour) and `next_rotation_time`
- Secret Manager publishes a message to the topic on schedule; a Cloud Function or workflow performs the actual rotation (new version create, update dependent systems, destroy old version)
- Retry: automatic retry up to 7 days; in-flight rotations block concurrent schedules

**Key difference vs AWS Secrets Manager:** AWS SM provides managed rotation with pre-built Lambda templates for RDS, Redshift, DocumentDB, and custom targets. GCP SM requires customer-authored rotation logic. Maturity rating: ADD-ON (event-driven but not turnkey). [gcp-sm-rotation-2025]

---

## 5. Audit and observability (UC-N rows)

**Cloud Audit Logs:**
- `ADMIN_WRITE`: CreateSecret, UpdateSecret, DeleteSecret, AddSecretVersion, DestroySecretVersion, SetIamPolicy — generated by default
- `ADMIN_READ`: GetSecret, ListSecrets, ListSecretVersions, GetIamPolicy — generated by default
- `DATA_READ`: AccessSecretVersion — **must be explicitly enabled** in audit log configuration
- `DATA_WRITE`: no DATA_WRITE methods in current API
- Logs available in Cloud Logging; exportable to BigQuery, Cloud Storage, Pub/Sub for SIEM integration

**Security Command Center:** Detects threats (privilege escalation, data exfiltration, malicious code execution) and misconfigurations. No native "secret sprawl" or orphaned-NHI detection dashboard. SIEM integration required for UC-N-001 (KPI dashboard) and UC-N-011 (post-incident RCA). [gcp-scc-2025]

---

## 6. Certificate Authority Service (NHI-006, NHI-025)

Google Certificate Authority Service (CAS) is a separate product providing hosted private CA capabilities backed by Cloud HSM. It supports ACME and REST-based certificate issuance. **CAS is not integrated with Secret Manager directly** — issued certificates and private keys are managed separately. For XYZ's mTLS and TLS lifecycle (NHI-006, UC-F-007), CAS + Cloud HSM provides the CA layer; Secret Manager can store static TLS assets but does not manage cert lifecycle. [gcp-cas-2025]

---

## 7. AI agents and Vertex AI (NHI-019)

Vertex AI service agents are IAM service accounts automatically created and managed by Google Cloud per project. They can be granted `secretmanager.secretAccessor` to access secrets at runtime. No dedicated AI-agent vault abstraction exists; IAM SA is the identity primitive. Vertex AI custom code service agents can be granted per-secret IAM bindings for least-privilege access. [gcp-vertex-2025]

---

## 8. Gaps and limitations

| Gap | Detail | XYZ Impact |
|---|---|---|
| Managed rotation | No built-in rotation logic; Pub/Sub notification requires custom Cloud Function. AWS SM has managed templates. | Rotation UC-F-006: ADD-ON (not NATIVE) |
| Dynamic database credentials | No native dynamic secrets engine (cf. HashiCorp Vault). Cloud SQL IAM auth + Secret Manager is best practice but requires custom orchestration. | NHI-005: ADD-ON |
| Mainframe / RPA | No native integration for IBM RACF/ACF2, UiPath, Blue Prism. REST API callable via middleware but no documented pattern. | NHI-022, NHI-014: GAP |
| FAPI 2.0 / Open Banking CDR | No built-in mTLS client cert lifecycle or CDR register integration. Apigee may address API gateway layer but CAS + Secret Manager would require custom wiring. | NHI-028, UC-F-024: GAP |
| IoT / OT device enrolment | No native IoT certificate provisioning (cf. AWS IoT Core). GCP IoT Core was deprecated. | NHI-021: GAP |
| Secret sprawl dashboard | No native KPI dashboard for secret coverage, orphaned NHIs, or rotation freshness. Requires custom Looker Studio / BigQuery + Cloud Logging. | UC-N-001, UC-N-003: ADD-ON |
| Orphaned NHI detection | No built-in unused-secret scanning or last-access alerting. Cloud Asset Inventory + Cloud Logging query required. | NHI-037, UC-F-027: ADD-ON |
| Webhook identity | No built-in inbound webhook signature verification service. | NHI-031: GAP |
| Post-quantum / hybrid PKI | No native PQC key types in Cloud KMS/HSM as of 2025/2026. | NHI-034: GAP |

---

## 9. Pricing (summary)

- Active secret versions: free up to 6/month per account; $0.06/version/month beyond
- Access operations: free first 10,000/month; $0.03/10,000 beyond
- Rotation notifications: free first 3/month; **$0.05 per notification** beyond
- Management operations: free

---

## 10. Citations

[gcp-sm-overview-2025] https://cloud.google.com/secret-manager/docs/overview
[gcp-sm-access-2025] https://cloud.google.com/secret-manager/docs/access-control
[gcp-sm-cmek-2025] https://cloud.google.com/secret-manager/docs/cmek
[gcp-sm-locations-2025] https://cloud.google.com/secret-manager/docs/locations
[gcp-sm-audit-2025] https://cloud.google.com/secret-manager/docs/audit-logging
[gcp-sm-integrations-2025] https://cloud.google.com/secret-manager/docs/using-other-products
[gcp-sm-rotation-2025] https://cloud.google.com/secret-manager/docs/secret-rotation
[gcp-sm-best-practices-2025] https://cloud.google.com/secret-manager/docs/best-practices
[gcp-sm-pricing-2025] https://cloud.google.com/secret-manager/pricing
[gcp-wif-2025] https://cloud.google.com/iam/docs/workload-identity-federation
[gcp-gke-wi-2025] https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity
[gcp-hsm-2025] https://cloud.google.com/kms/docs/hsm
[gcp-ekm-2025] https://cloud.google.com/kms/docs/ekm
[gcp-iam-sa-2025] https://cloud.google.com/iam/docs/service-account-overview
[gcp-irap-2025] https://cloud.google.com/security/compliance/irap
[gcp-cas-2025] https://cloud.google.com/certificate-authority-service/docs/ca-service-overview
[gcp-scc-2025] https://cloud.google.com/security/products/security-command-center
[gcp-vertex-2025] https://cloud.google.com/vertex-ai/docs/general/access-control

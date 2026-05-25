# Checkpoint: GCP Secret Manager Vendor Research — 001

**Vendor:** Google Cloud Secret Manager (gcp-secret-manager)
**Date:** 2026-05-22
**Agent:** Vendor Researcher (Sonnet 4.6)
**Status:** Pre-write guard — all research complete, writing deliverables

---

## Research Sources Indexed

| Source Label | URL | Status |
|---|---|---|
| gcp-sm-overview | https://cloud.google.com/secret-manager/docs/overview | OK |
| gcp-sm-access-control | https://cloud.google.com/secret-manager/docs/access-control | OK |
| gcp-sm-cmek | https://cloud.google.com/secret-manager/docs/cmek | OK |
| gcp-sm-locations | https://cloud.google.com/secret-manager/docs/locations | OK |
| gcp-sm-audit | https://cloud.google.com/secret-manager/docs/audit-logging | OK |
| gcp-sm-integrations | https://cloud.google.com/secret-manager/docs/using-other-products | OK |
| gcp-sm-rotation4 | https://cloud.google.com/secret-manager/docs/secret-rotation | OK |
| gcp-sm-best-practices | https://cloud.google.com/secret-manager/docs/best-practices | OK |
| gcp-sm-pricing | https://cloud.google.com/secret-manager/pricing | OK |
| gcp-sm-versions | https://cloud.google.com/secret-manager/docs/access-secret-version | OK |
| gcp-sm-versions2 | https://cloud.google.com/secret-manager/docs/add-secret-version | OK |
| gcp-sm-manage | https://cloud.google.com/secret-manager/docs/managing-secrets | OK |
| gcp-wif | https://cloud.google.com/iam/docs/workload-identity-federation | OK |
| gcp-gke-wi | https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity | OK |
| gcp-hsm | https://cloud.google.com/kms/docs/hsm | OK |
| gcp-cloud-ekm | https://cloud.google.com/kms/docs/ekm | OK |
| gcp-iam-sa | https://cloud.google.com/iam/docs/service-account-overview | OK |
| gcp-irap | https://cloud.google.com/security/compliance/irap | OK |
| gcp-compliance-au | https://cloud.google.com/security/compliance/offerings/#/regions=Australia | OK |
| gcp-regions | https://cloud.google.com/docs/geography-and-regions | OK |
| gcp-cas | https://cloud.google.com/certificate-authority-service/docs/ca-service-overview | OK |
| gcp-scc | https://cloud.google.com/security/products/security-command-center | OK |
| gcp-vertex-access | https://cloud.google.com/vertex-ai/docs/general/access-control | OK |

---

## Key Findings Summary

### AU Regions
- `australia-southeast1` (Sydney) — Regional Secret Manager: YES; Parameter Manager: YES
- `australia-southeast2` (Melbourne) — Regional Secret Manager: YES; Parameter Manager: YES
- User-managed replication can pin secrets to AU regions only (data residency enforcement)

### IRAP Status
- GCP IRAP: independent third-party assessor evaluated Google Cloud and Google Workspace against OFFICIAL and PROTECTED ISM controls; found "strongly aligned with PROTECTED level control requirements"
- Scope includes guidelines for cyber security roles, incident management, physical/personnel security, system hardening, networking, cryptography
- CCSL deprecated July 2020; current model: CSP self-assessment + customer risk-managed approach
- Secret Manager and Cloud KMS/HSM are within GCP platform scope; specific service-level IRAP scoping must be confirmed via Compliance Reports Manager

### Rotation
- Rotation schedules via Pub/Sub topic + `rotation_period` (min 1 hour) + `next_rotation_time`
- Rotation sends notification to Pub/Sub; customer-owned Cloud Functions/workflows perform actual rotation (no managed rotation built-in)
- Pricing: $0.05/rotation notification after 3 free/month
- Compare: AWS SM has managed rotation (Lambda-based, built-in templates for RDS etc.); GCP SM is notification-only — **GAP** for automated rotation maturity

### Encryption / KMS / HSM / EKM
- All secrets encrypted at rest with Google-managed keys by default (AES-256)
- CMEK via Cloud KMS: both automatic and user-managed replication policies support CMEK
- Cloud HSM: FIPS 140-2 Level 3 certified HSMs; Cloud KMS front-end; available in major regions including AU
- Cloud EKM: bring-your-own key material that never leaves external HSM; supports Fortanix (documented XYZ migration path), Futurex, Thales
- EKM partner-managed: sovereign partner creates/manages keys; data residency enforced per region

### IAM / Identity
- Service Accounts (NHI-001): primary identity primitive; `roles/secretmanager.secretAccessor` grants `secretmanager.versions.access`
- GKE Workload Identity Federation (NHI-002): Kubernetes ServiceAccount federated to IAM SA via GKE metadata server + Security Token Service; no key files needed
- Workload Identity Federation (NHI-003): OIDC/SAML/AWS federation; supports GitHub Actions, GitLab, Terraform Cloud, etc. without long-lived keys
- `roles/secretmanager.secretAccessor`, `secretmanager.secretVersionManager`, `secretmanager.admin` — fine-grained IAM at project/secret level

### Audit
- Cloud Audit Logs: ADMIN_WRITE (creates/updates), ADMIN_READ (gets), DATA_READ (AccessSecretVersion), DATA_WRITE
- DATA_ACCESS audit logs must be explicitly enabled (not on by default)
- Security Command Center: threat detection, misconfigurations, but no native "secret sprawl" detection dashboard

### CA Service (PKI)
- Certificate Authority Service (CAS): hosted private CA; ACME/EST support; backed by Cloud HSM
- Not integrated with Secret Manager directly (separate product); certs stored separately
- Relevant for NHI-006, NHI-025

### Mainframe / RPA / IoT
- No native integration; Secret Manager REST API could be called from custom middleware
- GAP for NHI-022 (mainframe), NHI-014 (RPA bots), NHI-032 (network devices)

### Vertex AI / AI Agents
- Vertex AI resources use Vertex AI service agents (IAM service accounts) by default
- Service accounts can be granted `secretmanager.secretAccessor` to access secrets at runtime
- No dedicated "AI agent vault" abstraction; IAM SA is the identity primitive

### Multi-cloud / Anthos
- Workload Identity Federation works for any OIDC IDP (cross-cloud, on-prem)
- GKE Enterprise (formerly Anthos) extends GKE patterns to multi-cloud/on-prem clusters

---

## Planned Coverage Summary (pre-write)

**NHI Coverage:**
- NATIVE (high confidence): NHI-001, NHI-002, NHI-003, NHI-005, NHI-006, NHI-007, NHI-008, NHI-009, NHI-010, NHI-011, NHI-013, NHI-017, NHI-018, NHI-019, NHI-023, NHI-024, NHI-025, NHI-035
- ADD-ON/PARTNER: NHI-004, NHI-012, NHI-015, NHI-016, NHI-020, NHI-026, NHI-027, NHI-028, NHI-029, NHI-030, NHI-031, NHI-034, NHI-036
- GAP: NHI-014, NHI-021, NHI-022, NHI-032, NHI-033, NHI-037

**Open Questions:**
1. Which specific GCP services are named in the IRAP assessment report (downloadable via Compliance Reports Manager)?
2. Cloud HSM availability in `australia-southeast1` / `australia-southeast2` — confirm region-level HSM support
3. Does `australia-southeast2` (Melbourne) support Cloud HSM keys or only Cloud KMS software keys?
4. Dynamic database credentials (NHI-005): GCP has no native equivalent to Vault dynamic secrets; Cloud SQL IAM auth + Secret Manager is the pattern — maturity?
5. Fortanix DSM as Cloud EKM partner — documented; is there an XYZ-specific deployment guide?
6. FAPI 2.0 / CDR support: GAP unless via Apigee; confirm Apigee scope

---

HANDOFF_NEEDED: no — writing deliverables now

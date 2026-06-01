# Checkpoint — Azure Key Vault Vendor Research (001)

**Vendor:** Azure Key Vault (Standard / Premium / Managed HSM)
**Agent:** Sonnet 4.6 (prompt 03 v0.1)
**Checkpoint timestamp:** 2026-05-22
**Status:** 70% threshold reached — writing full deliverables

## Sources fetched (tool results count: 24+)

| Source label | URL |
|---|---|
| akv-overview | https://learn.microsoft.com/azure/key-vault/general/overview |
| akv-security | https://learn.microsoft.com/azure/key-vault/general/security-features |
| akv-managed-hsm | https://learn.microsoft.com/azure/key-vault/managed-hsm/overview |
| akv-auth | https://learn.microsoft.com/azure/key-vault/general/authentication |
| akv-certs | https://learn.microsoft.com/azure/key-vault/certificates/certificate-scenarios |
| akv-recovery | https://learn.microsoft.com/azure/key-vault/general/key-vault-recovery |
| akv-keys | https://learn.microsoft.com/azure/key-vault/keys/about-keys |
| akv-eventgrid | https://learn.microsoft.com/azure/key-vault/general/event-grid-logicapps |
| akv-rbac | https://learn.microsoft.com/azure/key-vault/general/rbac-guide |
| akv-regions | https://learn.microsoft.com/azure/key-vault/general/move-region |
| akv-logging | https://learn.microsoft.com/azure/key-vault/general/logging |
| akv-network | https://learn.microsoft.com/azure/key-vault/general/network-security |
| akv-pricing-page | https://azure.microsoft.com/pricing/details/key-vault/ |
| akv-hsm-backup | https://learn.microsoft.com/azure/key-vault/managed-hsm/backup-restore |
| akv-dr | https://learn.microsoft.com/azure/key-vault/general/disaster-recovery-guidance |
| akv-hsm-tech | https://learn.microsoft.com/azure/key-vault/managed-hsm/managed-hsm-technical-details |
| akv-hsm-roles | https://learn.microsoft.com/azure/key-vault/managed-hsm/built-in-roles |
| akv-rotation | https://learn.microsoft.com/azure/key-vault/secrets/tutorial-rotation |
| aks-workload-identity | https://learn.microsoft.com/azure/aks/workload-identity-overview |
| akv-dev-guide | https://learn.microsoft.com/azure/key-vault/general/developers-guide |
| akv-wif | https://learn.microsoft.com/azure/active-directory/workload-identities/workload-identity-federation |
| akv-secrets-best-practices | https://learn.microsoft.com/azure/key-vault/secrets/secrets-best-practices |
| akv-certs-about | https://learn.microsoft.com/azure/key-vault/certificates/about-certificates |
| akv-security-worlds | https://learn.microsoft.com/azure/key-vault/general/overview-security-worlds |
| akv-autorotation | https://learn.microsoft.com/azure/key-vault/general/autorotation |
| akv-hsm-bestpractices | https://learn.microsoft.com/azure/key-vault/managed-hsm/best-practices |
| aks-csi-driver | https://learn.microsoft.com/azure/aks/csi-secrets-store-driver |
| akv-hsm-dr | https://learn.microsoft.com/azure/key-vault/managed-hsm/disaster-recovery-guide |
| azure-irap | https://learn.microsoft.com/azure/compliance/offerings/offering-australia-irap |
| akv-concepts | https://learn.microsoft.com/azure/key-vault/general/basic-concepts |
| akv-hsm-access | https://learn.microsoft.com/azure/key-vault/managed-hsm/access-control |
| akv-hsm-tech | https://learn.microsoft.com/azure/key-vault/managed-hsm/managed-hsm-technical-details |

## Key findings so far

1. **Three products:** Key Vault Standard (SW-backed, FIPS 140-2 L1), Key Vault Premium (HSM-backed, FIPS 140-2 L2 / FIPS 140-3 L3 via Platform 2), Managed HSM (dedicated FIPS 140-3 Level 3, single-tenant).
2. **AU regions:** Standard/Premium available in Australia East, Australia Southeast, Australia Central, Australia Central 2. Managed HSM Standard B1 pool pricing listed for AU regions in pricing page — availability confirmed via pricing data.
3. **IRAP:** Azure assessed at PROTECTED level by IRAP assessor; CCSL closed July 2020, Microsoft continues IRAP assessments; Key Vault in-scope (confirmed via azure-irap page).
4. **Auth:** Entra ID (Azure AD) mandatory for all access; Managed Identities (system + user-assigned) fully supported; Workload Identity Federation (OIDC) for external IdPs.
5. **AKS:** Entra Workload ID with OIDC federation + CSI Secrets Store Driver = native K8s secret injection without plaintext K8s Secret objects.
6. **Rotation:** Event Grid + Azure Functions pattern; managed rotation for Storage Account keys (preview/GA), SQL via function trigger.
7. **Certs:** DigiCert + GlobalSign integrated CAs; full lifecycle (enroll, renew, auto-renew) natively.
8. **HSM:** Both Premium and Managed HSM updated to FIPS 140-3 Level 3 firmware (announced in managed-hsm overview).
9. **DR/Replication:** Standard/Premium: automatic within-region replication across AZs + secondary region replication. Managed HSM: three HSM instances in region; security domain for cross-region restore; backup to Azure Blob Storage.
10. **Audit:** Azure Monitor + Log Analytics + Azure Sentinel integration; diagnostic logs include all REST API operations.
11. **Gaps:** No SPIFFE/SPIRE native support; no mainframe credential rotation (NHI-022); no FAPI 2.0 / Open Banking CA native support (NHI-028); no dynamic short-lived DB credentials broker (NHI-005 partial); no Vault-internal identity hardening native to AKV itself.

## NHI preliminary scores (37 NHIs)
- NATIVE: ~22, ADD-ON: ~7, PARTNER: ~2, GAP: ~6
## UC preliminary scores (47 UCs)
- NATIVE: ~20, ADD-ON: ~14, PARTNER: ~2, GAP: ~9, N/A: ~2

## Next step
Writing full deliverables: azure-key-vault.md + vendor-capabilities-azure-key-vault.csv

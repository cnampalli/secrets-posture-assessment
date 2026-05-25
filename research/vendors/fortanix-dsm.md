# Vendor Profile — Fortanix DSM

**Tier:** data-security
**Primary docs:** https://support.fortanix.com / https://www.fortanix.com/platform/data-security-manager
**Profile written:** 2026-05-23
**Profiled by:** Sonnet 4.6 (prompt 03 v0.1)

---

## 1. Vendor snapshot (≤ 150 words)

Fortanix (founded 2016, Santa Clara CA; ~$122 M raised to Series C) is
the company that commercialised Intel SGX-backed confidential computing
and built a unified **HSM-as-a-service + KMS + tokenization + secrets
management** platform called **Data Security Manager (DSM)**. DSM is the
crypto root that sits *below* vault platforms — a major AU Tier-1 FI
recently migrated its Vault Enterprise HSM seal from Thales SafeNet Luna
to Fortanix DSM (see ADR-004, 2026-05-22; `[USER-SUPPLIED]`). Fortanix is
a named GA partner in AWS KMS XKS
(Nov 2022), Azure Key Vault BYOK, and GCP Cloud EKM. Deployment options:
SaaS on Equinix (15 DCs globally including **AU/APAC region**), on-prem
FX2200/FX3400 appliances, or self-hosted virtual. Compliance: SOC 2,
ISO 27001, PCI DSS, FIPS 140-2 Level 3 (FX2200 GA; FX3400 FIPS 140-3
pending). No confirmed IRAP assessment as of May 2026. [fortanix-dsm-hsm-saas-2025]

---

## 2. Architecture (≤ 250 words)

**Core platform.** Fortanix DSM unifies five capabilities in one control
plane: HSM services, key management (KMS), secrets management, data
tokenization, and Confidential Computing Manager (CCM). All cryptographic
operations are performed inside FIPS 140-2 Level 3 certified HSMs (FX2200
Series); the forthcoming FX3400 appliance targets FIPS 140-3 Level 3.
[fortanix-dsm-hsm-saas-2025][fortanix-dsm-deployment-options-2025]

**Interfaces.** REST API, PKCS#11, KMIP, JCE, and CNG are all
production-GA, enabling integration with virtually any vault platform
(HashiCorp Vault Enterprise via PKCS#11 auto-unseal + seal-wrap;
CyberArk EPV via PKCS#11; Veeam v12.1 via KMIP; EJBCA/Keyfactor via
KMIP). [fortanix-vault-enterprise-2024][fortanix-cyberark-integration-2024]

**Cloud Data Control (CDC).** Fortanix CDC federates key management across
AWS KMS (XKS + BYOK + BYOKMS), Azure Key Vault (Managed HSM BYOK),
and GCP Cloud EKM from a single console. Virtual "linked" or "copied"
keys replicate to multiple CSP regions, supporting multi-cloud BYOK
orchestration. [fortanix-aws-xks-2022][fortanix-gcp-ekm-2024][fortanix-byok-2024]

**Confidential Computing.** CCM provides hardware attestation across Intel
SGX, Intel TDX, AMD SEV-SNP, AWS Nitro Enclaves, and NVIDIA GPU TEEs.
Secure Key Release (SKR) in DSM gates key delivery on a verified CCM
attestation certificate — described as operational in December 2025.
[fortanix-ccm-skr-2025]

**Tokenization.** Vaultless FF1 + FF3-1 Format-Preserving Encryption
(NIST-certified) with no central token vault required; encryption keys
stored in FIPS 140-2 Level 3 HSMs. [fortanix-tokenization-fpe-2025][fortanix-fpe-faq-2025]

**HA / DR.** SaaS: 3 physically isolated DCs per region on Equinix Fabric;
99.95% availability SLA. On-prem: clustered FX2200 appliances.

**Compliance declared:** SOC 2, ISO 27001, PCI DSS, FIPS 140-2 Level 3.
APRA CPS 234 alignment blog published [fortanix-cps234-blog-2024]. IRAP
and FedRAMP: **not confirmed** in public documentation as of May 2026.

---

## 3. NHI coverage map (≤ 600 words)

Fortanix DSM is a **crypto-root and KMS layer**, not a secrets vault. It
does not directly broker application secrets (no Vault-equivalent dynamic
secrets engine, no AppRole/K8s auth). Coverage is therefore:
- **Strong** on NHIs whose trust anchor IS the HSM or KMS (NHI-013, NHI-017,
  NHI-018, NHI-023, NHI-024, NHI-034, NHI-035).
- **Weak** on NHIs that are vault-brokered application credentials
  (NHI-001..012, NHI-014, NHI-019..022, NHI-026..033, NHI-036, NHI-037).

| NHI | Coverage | Maturity | Evidence |
|-----|----------|----------|---------|
| NHI-001 Cloud IAM principal | GAP | 0 | Not addressed; vault platforms handle this layer. |
| NHI-002 K8s ServiceAccount | GAP | 0 | No K8s auth or CSI driver. |
| NHI-003 CI/CD pipeline identity | GAP | 0 | Not in scope. |
| NHI-004 Container image-pull | GAP | 0 | Not in scope. |
| NHI-005 Database service account | GAP | 0 | No dynamic DB secrets engine. |
| NHI-006 TLS/mTLS workload identity | ADD-ON | 2 | DSM stores TLS private keys + certs; integrates with EJBCA/Keyfactor for issuance. [fortanix-cyberark-integration-2024] |
| NHI-007 Third-party SaaS API key | ADD-ON | 2 | DSM secrets manager stores arbitrary blobs including API keys. [fortanix-dsm-hsm-saas-2025] |
| NHI-008 Git platform credential | ADD-ON | 1 | Stored as opaque secrets; no native Git integration. |
| NHI-009 Config-mgmt / IaC agent | ADD-ON | 1 | Vault/Ansible retrieve keys from DSM via PKCS#11/KMIP; indirect. |
| NHI-010 Monitoring agent | GAP | 0 | No monitoring-agent credential management. |
| NHI-011 Message broker client | GAP | 0 | No Kafka/MQ integration documented. |
| NHI-012 AD/LDAP service account | GAP | 0 | Not in scope. |
| NHI-013 API-gateway upstream identity | PARTNER | 2 | DSM manages mTLS cert keys for API gateways via PKCS#11/KMIP. [fortanix-vault-enterprise-2024] |
| NHI-014 RPA bot identity | GAP | 0 | Not in scope. |
| NHI-015 Code-signing identity | ADD-ON | 2 | HSM-backed code-signing keys (Authenticode, EV certs) via PKCS#11. [fortanix-dsm-hsm-saas-2025] |
| NHI-016 Build provenance / SLSA | GAP | 1 | No Sigstore/SLSA integration documented; keys could be stored. |
| NHI-017 Service mesh control-plane | ADD-ON | 2 | Intermediate CA keys for Istio/Consul can be stored in DSM via PKCS#11. [fortanix-vault-enterprise-2024] |
| NHI-018 Confidential-computing attestation | NATIVE | 4 | CCM + DSM Secure Key Release gates key delivery on SGX/TDX/SEV-SNP/Nitro attestation. Industry-leading. [fortanix-ccm-skr-2025] |
| NHI-019 AI agent / autonomous workflow | ADD-ON | 1 | DSM can store tool credentials; no native agent attestation broker. |
| NHI-020 Model artifact / registry identity | GAP | 0 | Not in scope. |
| NHI-021 IoT / OT device identity | ADD-ON | 1 | PKI/cert management for devices via EJBCA integration; no EST/SCEP native. |
| NHI-022 Mainframe service identity | GAP | 0 | No z/OS / RACF integration documented. |
| NHI-023 DB encryption TDE master key | NATIVE | 3 | BYOK/BYOKMS for TDE CMKs (AWS RDS, SQL Server AlwaysEncrypted, Azure CMK) via KMS CDC. [fortanix-aws-xks-2022][fortanix-byok-2024] |
| NHI-024 HSM/KMS operator break-glass | NATIVE | 4 | Fortanix DSM IS the HSM; quorum-admin M-of-N roles, FX appliance PED/smartcard. [fortanix-dsm-hsm-saas-2025] |
| NHI-025 CA operator identity | ADD-ON | 2 | CA private keys stored in DSM; EJBCA + Keyfactor KMIP integration documented. [fortanix-cyberark-integration-2024] |
| NHI-026 Backup / DR agent identity | GAP | 0 | Veeam v12.1 KMIP integration for backup encryption keys only, not credential brokering. |
| NHI-027 BFF / OBO token holder | GAP | 0 | Not in scope. |
| NHI-028 Federated B2B / Open Banking | ADD-ON | 1 | mTLS cert keys for FAPI 2.0 partners managed in DSM via PKCS#11/KMIP. |
| NHI-029 Service-account-as-human | GAP | 0 | Not in scope. |
| NHI-030 Browser/SaaS OAuth-app | GAP | 0 | Not in scope. |
| NHI-031 Webhook / inbound integration | GAP | 0 | Not in scope. |
| NHI-032 Network / infra device | GAP | 0 | No TACACS+/RADIUS/SNMP credential management. |
| NHI-033 Print / branch peripheral | GAP | 0 | Not in scope. |
| NHI-034 PQC / hybrid-PKI rotation | NATIVE | 3 | PQC Central (June 2025): ML-KEM + ML-DSA + LMS/XMSS key generation and inventory; crypto-agility dashboard. [fortanix-pqc-central-2025] |
| NHI-035 Vault-internal / secrets-broker | NATIVE | 4 | Fortanix DSM is the auto-unseal HSM for Vault Enterprise; the crypto root-of-trust for the vault platform itself. [fortanix-vault-enterprise-2024] |
| NHI-036 Ephemeral workload SPIFFE | GAP | 0 | No SPIFFE/SPIRE integration; CCM does attestation but not SVID issuance. |
| NHI-037 Orphaned / dormant identity | GAP | 0 | No orphan-detection or ITDR capabilities. |

**NHI summary:** NATIVE=5, ADD-ON=11, PARTNER=1, GAP=20, N/A=0.

---

## 4. Use-case scoring (≤ 800 words)

Fortanix DSM excels at crypto-root, BYOK, TEE attestation and PQC UCs.
It does not address secrets-sprawl detection, vault-brokered dynamic
credentials, or identity-governance UCs directly.

### Functional UCs

| UC | Coverage | Maturity | Evidence |
|----|----------|----------|---------|
| UC-F-001 Prevent plaintext secrets in repos | GAP | 0 | Not in scope; no scanning capability. |
| UC-F-002 Detect secrets in history | GAP | 0 | Not in scope. |
| UC-F-003 JIT short-lived cloud creds (OIDC) | GAP | 0 | DSM manages keys, not OIDC federation. |
| UC-F-004 Workload-attested ephemeral identity (SPIFFE) | GAP | 1 | CCM provides attestation but not SVID issuance; partial overlap. |
| UC-F-005 Dynamic database credentials | GAP | 0 | No dynamic DB secrets engine. |
| UC-F-006 Automated rotation of long-lived secrets | ADD-ON | 2 | DSM key-rotation policies for KMS keys; vault platforms rotate application secrets using DSM-managed keys. [fortanix-byok-2024] |
| UC-F-007 Immediate revocation on compromise | ADD-ON | 2 | DSM key deactivation/deletion revokes KMS-derived keys cloud-wide; vault-layer revocation requires vault. [fortanix-aws-xks-2022] |
| UC-F-008 K8s secret consumption without on-disk plaintext | GAP | 0 | No CSI driver or K8s agent. |
| UC-F-009 Container image-pull creds per workload | GAP | 0 | Not in scope. |
| UC-F-010 IaC/config-mgmt secrets at apply-time | ADD-ON | 1 | Vault+Fortanix combo; DSM as HSM backend only. |
| UC-F-011 Observability-agent credential rotation | GAP | 0 | Not in scope. |
| UC-F-012 Message-broker client identity hardening | GAP | 0 | Not in scope. |
| UC-F-013 gMSA/Kerberos modernisation for AD SAs | GAP | 0 | Not in scope. |
| UC-F-014 API-gateway upstream identity standardised | ADD-ON | 2 | DSM stores mTLS private keys for API gateway certs via PKCS#11. [fortanix-vault-enterprise-2024] |
| UC-F-015 RPA bot credentials vaulted | GAP | 0 | Not in scope. |
| UC-F-016 Keyless code- and artifact-signing in CI | ADD-ON | 2 | HSM-backed code-signing keys (Authenticode, EV) via PKCS#11; not keyless but HSM-rooted. [fortanix-dsm-hsm-saas-2025] |
| UC-F-017 TEE attestation gates secret release | NATIVE | 4 | CCM + DSM SKR: attestation-gated key release for SGX/TDX/SEV-SNP/Nitro/NVIDIA — operational Dec 2025. [fortanix-ccm-skr-2025] |
| UC-F-018 AI-agent / LLM tool-credential brokering | ADD-ON | 1 | DSM Armet AI platform stores AI tool keys; CCM attests AI workloads; no native broker/per-session scoping. [fortanix-ccm-skr-2025] |
| UC-F-019 IoT/OT/branch device identity enrolment | ADD-ON | 1 | PKI cert storage via EJBCA/Keyfactor integration; no native EST/SCEP/DPS. |
| UC-F-020 Mainframe/midrange credential rotation | GAP | 0 | No z/OS integration. |
| UC-F-021 Backup/DR agent identity de-privileging | ADD-ON | 1 | Veeam v12.1 KMIP: backup encryption keys in DSM; not credential brokering. [fortanix-cyberark-integration-2024] |
| UC-F-022 Webhook inbound identity verification | GAP | 0 | Not in scope. |
| UC-F-023 Network-device credential modernisation | GAP | 0 | Not in scope. |
| UC-F-024 Open Banking / FAPI 2.0 mTLS partner identity | ADD-ON | 2 | mTLS client cert private keys managed in DSM FIPS HSM; BYOK for partner key custody. [fortanix-byok-2024] |
| UC-F-025 OAuth-app / marketplace integration governance | GAP | 0 | Not in scope. |
| UC-F-026 Vault-internal identity hardening | NATIVE | 4 | Fortanix DSM is the auto-unseal HSM and seal-wrap provider for Vault Enterprise; M-of-N quorum admin; root-of-trust hardening. [fortanix-vault-enterprise-2024] |
| UC-F-027 Orphaned / dormant NHI cleanup | GAP | 0 | No orphan detection. |

### Non-functional UCs

| UC | Coverage | Maturity | Evidence |
|----|----------|----------|---------|
| UC-N-001 Real-time secret-sprawl KPI dashboard | GAP | 0 | Not in scope; no scanning/discovery layer. |
| UC-N-002 NHI inventory and ownership attestation | GAP | 0 | DSM Key Insight has crypto inventory; not NHI-breadth inventory. |
| UC-N-003 Rotation-coverage and freshness KPIs | ADD-ON | 2 | DSM Key Insight provides key rotation status and crypto inventory KPIs. [fortanix-pqc-central-2025] |
| UC-N-004 Regulator audit evidence pack | ADD-ON | 2 | DSM audit logs + key lifecycle reports; CPS 234 blog confirms alignment intent. [fortanix-cps234-blog-2024] |
| UC-N-005 Essential 8 / ZT control-area scorecard | ADD-ON | 1 | Partial — DSM covers crypto controls; no E8/ZT scorecard output. |
| UC-N-006 Vendor/SaaS supply-chain risk attestation | GAP | 0 | Not in scope. |
| UC-N-007 Data-sovereignty and residency assurance | ADD-ON | 2 | BYOK/BYOKMS with on-prem FX appliances or AU Equinix SaaS region; explicit data-residency control. [fortanix-dsm-deployment-options-2025] |
| UC-N-008 Engineer training and secure-coding adoption | GAP | 0 | Not in scope. |
| UC-N-009 Exception register and risk-acceptance governance | GAP | 0 | Not in scope. |
| UC-N-010 Break-glass and quorum-operator governance | NATIVE | 4 | Fortanix DSM quorum administration; HSM operator roles; M-of-N; full audit trail. [fortanix-dsm-hsm-saas-2025] |
| UC-N-011 Post-incident reporting and identity-driven RCA | ADD-ON | 1 | DSM audit logs are forensic-grade; no NHI-attribution or ATT&CK tagging. |
| UC-N-012 Supply-chain / SLSA-provenance assurance | ADD-ON | 1 | HSM-backed signing keys support SLSA; no SLSA reporting layer. |
| UC-N-013 Crypto-agility and PQC readiness reporting | NATIVE | 3 | PQC Central (Key Insight): discovery, risk scoring, transition tracking, ML-KEM + ML-DSA support, crypto-agility dashboard. [fortanix-pqc-central-2025] |
| UC-N-014 Vendor-evaluation matrix maintenance | GAP | 0 | Not in scope. |
| UC-N-015 Communications and stakeholder cadence | GAP | 0 | Not in scope. |
| UC-N-016 IoT/OT/branch-fleet posture reporting | GAP | 0 | Not in scope. |
| UC-N-017 Observability/telemetry secret-leak governance | GAP | 0 | Not in scope. |
| UC-N-018 Confidential-computing / TEE attestation assurance | NATIVE | 4 | CCM attestation logs (SGX/TDX/SEV-SNP/Nitro); key release audit per TEE attestation event. [fortanix-ccm-skr-2025] |
| UC-N-019 AI-agent / autonomous-workflow KPI suite | ADD-ON | 1 | Armet AI platform provides workload key-use logging; no NHI-scope KPI suite. |
| UC-N-020 Mainframe / legacy posture and exception transparency | GAP | 0 | Not in scope. |

**UC summary:** NATIVE=6, ADD-ON=17, PARTNER=0, GAP=24, N/A=0.

---

## 5. Strengths and gaps (≤ 300 words)

### Top 3 strengths

1. **HSM / KMS root-of-trust for vault platforms (NHI-035, UC-F-026, UC-N-010).** Fortanix DSM is the cryptographic foundation XYZ uses for Vault Enterprise auto-unseal and seal-wrap. It is the load-bearing HSM layer: PKCS#11, KMIP, REST interfaces; FIPS 140-2 Level 3 certified hardware; M-of-N quorum operator governance. No other vendor in this matrix directly replaces this role. [fortanix-vault-enterprise-2024]

2. **Cross-cloud BYOK / EKM for TDE master keys and data-at-rest governance (NHI-023, NHI-024, UC-F-006, UC-N-007).** Fortanix is a named GA partner for AWS XKS, Azure Key Vault BYOK, and GCP Cloud EKM. This gives XYZ cryptographic custody of TDE CMKs across all three hyperscalers from a single, FIPS-compliant control plane — covering the sovereignty and APRA CPS 234 data-residency angle directly. [fortanix-aws-xks-2022][fortanix-gcp-ekm-2024][fortanix-byok-2024]

3. **TEE attestation-gated key release + PQC readiness (NHI-018, NHI-034, UC-F-017, UC-N-013, UC-N-018).** CCM + DSM Secure Key Release is industry-leading: composite attestation across SGX/TDX/SEV-SNP/Nitro before key delivery into enclave memory. PQC Central (June 2025) adds ML-KEM + ML-DSA inventory, risk scoring, and transition tracking — the only vendor in this evaluation with a dedicated PQC dashboard. [fortanix-ccm-skr-2025][fortanix-pqc-central-2025]

### Top 3 gaps

1. **No secrets-vault capability (NHI-001..012, UC-F-001..003, UC-F-005, UC-F-008).** Fortanix does not broker dynamic DB credentials, K8s secrets, or CI/CD OIDC tokens. It must be paired with Vault Enterprise or another vault platform for application-layer secrets management.

2. **IRAP and FedRAMP not confirmed.** No IRAP assessment found in public documentation as of May 2026. This is a material gap for XYZ and other APRA-regulated entities needing Australian Government–certified cloud services.

3. **Weak application-identity NHIs (NHI-019, NHI-036, NHI-003).** Fortanix has no SPIFFE/SPIRE workload identity, no AI-agent credential broker, and no CI/CD OIDC integration. The CCM attests TEE workloads but does not issue SVIDs or broker per-session tokens.

---

## 6. AU-specific notes (≤ 150 words)

**Region:** "Australia" is listed as an available region on the Fortanix HSM platform page [fortanix-hsm-platform-2025]. SaaS runs on Equinix infrastructure; Equinix operates SY3 and SY4 in Sydney, making AU-resident DSM SaaS plausible but the specific Equinix site is not confirmed in public docs.

**APRA CPS 234:** Fortanix published a CPS 234 alignment blog [fortanix-cps234-blog-2024], noting DSM supports "security role clarity, asset classification, control implementation" requirements. Direct CPS 234 control mapping not publicly available.

**IRAP:** No IRAP (Information Security Registered Assessors Program) assessment confirmed. Material risk for XYZ using DSM SaaS for data classified above PROTECTED.

**FIPS 140-3 transition:** NIST moves all FIPS 140-2 certs to Historical status 21 September 2026. FX3400 (FIPS 140-3 Level 3 pending) must reach certification before this date for ongoing federal/regulated use.

**Data residency:** On-prem FX2200/FX3400 appliances offer complete AU data sovereignty with no dependency on Fortanix SaaS control plane. [fortanix-dsm-deployment-options-2025]

---

## 7. Citations

See `meta/citations.bib` — BibTeX keys appended under `## Fortanix DSM (Agent 03 wave 4)`.

Keys introduced: fortanix-dsm-hsm-saas-2025, fortanix-dsm-deployment-options-2025,
fortanix-vault-enterprise-2024, fortanix-aws-xks-2022, fortanix-gcp-ekm-2024,
fortanix-byok-2024, fortanix-tokenization-fpe-2025, fortanix-fpe-faq-2025,
fortanix-pqc-central-2025, fortanix-ccm-skr-2025, fortanix-cyberark-integration-2024,
fortanix-cps234-blog-2024, fortanix-hsm-platform-2025, fortanix-hashicorp-partner-2024.

---

## 8. Open questions for v1.0

1. **IRAP status** — Has Fortanix DSM SaaS (AU Equinix region) been assessed under IRAP? At what classification level? Critical for APRA-regulated production use.
2. **Specific AU Equinix site** — Is the AU SaaS cluster on SY3/SY4 or another facility? Confirmed data-residency guarantee (no cross-border replication)?
3. **FIPS 140-3 timeline** — When does FX3400 receive FIPS 140-3 Level 3 certificate? Before Sep 2026 NIST deadline?
4. **XYZ Vault auto-unseal configuration** — Is XYZ's production Vault cluster currently using Fortanix DSM SaaS (AU region) or on-prem FX appliance? Which Vault Enterprise version and seal method?
5. **PQC Central GA completeness** — Are ML-KEM / ML-DSA *key operations* (keygen, encap/decap, sign/verify) supported inside the FIPS HSM, or is PQC Central only a discovery/inventory tool for existing keys?
6. **Tokenization integration depth** — Does Fortanix vaultless FPE require a DSM-side SDK/agent in the application, or is it purely API-driven? How does this compare to Vault Transform's transit-engine model?
7. **SLH-DSA (FIPS 205)** — PQC Central press release lists ML-KEM + ML-DSA; is SLH-DSA supported, or on roadmap?
8. **Delinea/CyberArk PAM integration** — Is Fortanix DSM integrated with Delinea Secret Server or CyberArk Privilege Cloud (not just EPV legacy) for PAM use cases?

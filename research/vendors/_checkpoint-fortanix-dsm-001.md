# Checkpoint — fortanix-dsm-001

**Agent:** Vendor Researcher (Sonnet 4.6, prompt 03 v0.1)
**Vendor:** Fortanix DSM
**Date:** 2026-05-23
**Status:** PRE-WRITE GUARD — all research complete; writing final outputs now.

## Completed work

- Read canonical prompt 03, README invariants, identity-taxonomy.md (37 NHIs), use-cases.md (27 UC-F + 20 UC-N).
- Executed 10 WebSearch queries; 8 WebFetch calls to primary Fortanix sources.
- Key sources confirmed:
  - HSM as a service: FIPS 140-2 L3 FX2200 appliance; FIPS 140-3 FX3400 pending; SaaS on Equinix 15 DCs; **AU/APAC region listed** on HSM platform page.
  - Cross-cloud: AWS XKS (GA Nov 2022), Azure Key Vault BYOK (GA), GCP EKM (GA) — all documented at support.fortanix.com.
  - Vault Enterprise: PKCS#11 auto-unseal + seal-wrap confirmed (support.fortanix.com/docs/using-fortanix-data-security-manager-with-hashicorp-vault-enterprise); HashiCorp partner page confirmed.
  - Tokenization: vaultless FF1 (NIST-certified) + FF3-1 FPE; PCI DSS 4.0 alignment; fortanix.com/platform/data-security-manager/data-tokenization.
  - PQC: PQC Central announced June 2025; ML-KEM (CRYSTALS-Kyber) + ML-DSA (CRYSTALS-Dilithium) supported; LMS/XMSS also listed; no explicit FIPS 140-3 timeline.
  - Confidential Computing: CCM supports SGX/TDX/SEV-SNP/Nitro/NVIDIA GPU; Secure Key Release blog Dec 2025 confirms attestation-gated key release as operational.
  - CyberArk EPV integration via PKCS#11 confirmed; Veeam v12.1 KMIP integration confirmed; KMIP/REST/JCE/CNG/PKCS#11 interfaces all GA.
  - Compliance: SOC 2, ISO 27001, PCI DSS, FIPS listed on fortanix.com/solutions/compliance; **IRAP not confirmed**; FedRAMP not confirmed; APRA CPS 234 blog published.
  - AU deployment: "Australia" listed as region on HSM platform page (fortanix.com/platform/data-security-manager/hardware-security-module); SaaS on Equinix (Sydney SY3/SY4 possible); no explicit IRAP assessment found.

## Remaining work

- Write fortanix-dsm.md (vendor profile).
- Write vendor-capabilities-fortanix-dsm.csv (84 rows: 37 NHI + 47 UC).
- Append BibTeX block to meta/citations.bib.
- Append log row to meta/agents.md (LAST operation).

## NHI scoring plan

- NHI-001..008: GAP (0–1) — Fortanix is not a secrets vault; it complements vault platforms.
- NHI-013 (API gateway upstream certs): PARTNER/2 — key management for mTLS certs.
- NHI-015 (code-signing): ADD-ON/2 — HSM-backed code-signing keys.
- NHI-016 (SLSA provenance): GAP/1 — no direct SLSA integration found.
- NHI-017 (service mesh CA): ADD-ON/2 — PKCS#11/KMIP for Istio/Consul CA keys.
- NHI-018 (confidential computing): NATIVE/4 — CCM + DSM SKR is industry-leading.
- NHI-023 (DB TDE master keys): NATIVE/3 — KMS for TDE CMK via BYOK/BYOKMS.
- NHI-024 (HSM/KMS operator): NATIVE/4 — Fortanix IS the HSM; M-of-N quorum admin.
- NHI-025 (CA operator): ADD-ON/2 — EJBCA + Keyfactor integration documented.
- NHI-034 (PQC): NATIVE/3 — ML-KEM + ML-DSA in PQC Central (June 2025 GA).
- NHI-035 (vault-internal): NATIVE/4 — Vault auto-unseal HSM; the crypto root itself.

## Citations gathered

fortanix-dsm-hsm-saas-2025, fortanix-dsm-deployment-options-2025, fortanix-vault-enterprise-2024, fortanix-aws-xks-2022, fortanix-gcp-ekm-2024, fortanix-byok-2024, fortanix-tokenization-fpe-2025, fortanix-fpe-faq-2025, fortanix-pqc-central-2025, fortanix-ccm-skr-2025, fortanix-cyberark-integration-2024, fortanix-cps234-blog-2024, fortanix-hsm-platform-2025, hashicorp-fortanix-partner-2024

## Continuation instructions

If handoff needed: re-read this checkpoint, then write the three output files. No additional research required.

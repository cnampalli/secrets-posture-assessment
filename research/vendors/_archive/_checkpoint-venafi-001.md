# Checkpoint — Venafi (CyberArk Machine Identity Security) Vendor Researcher — 001

**Agent:** Vendor Researcher (Sonnet 4.6)
**Vendor slug:** venafi
**Prompt:** prompts/03-vendor-researcher-template.md
**Timestamp:** 2026-05-22
**Status:** PRE-WRITE GUARD — research complete, writing outputs now.

---

## Completed work

- Read canonical prompt, identity-taxonomy, use-cases, README invariants.
- Fetched and indexed:
  - https://www.cyberark.com/products/machine-identity-security/
  - https://www.cyberark.com/product-name-updates/
  - https://www.cyberark.com/products/certificate-manager/
  - https://www.cyberark.com/products/workload-identity-manager/
  - https://www.cyberark.com/products/code-sign-manager/
  - https://www.cyberark.com/products/ssh-manager-for-machines/
  - https://www.cyberark.com/products/zero-touch-pki/
  - https://www.cyberark.com/trust/compliance/
  - https://www.cyberark.com/what-is/machine-identity-security/
  - https://docs.venafi.cloud/whatsnew/
  - https://docs.venafi.cloud/firefly/overview/
  - https://docs.venafi.cloud/firefly/get-started/
  - https://docs.venafi.com/ (self-hosted docs root)
  - https://docs.venafi.cloud/vaas/about-vaas/

## Key findings

### Product Rebranding (2024–2026)
- Venafi acquired by CyberArk, October 2024. All products rebranded:
  - Venafi TLS Protect → CyberArk Certificate Manager, Self-Hosted
  - Venafi TLS Protect Cloud → CyberArk Certificate Manager, SaaS
  - Venafi TLS Protect for Kubernetes → CyberArk Certificate Manager for Kubernetes
  - Venafi SSH Protect → CyberArk SSH Manager for Machines
  - Venafi CodeSign Protect → CyberArk Code Sign Manager
  - Venafi Zero Touch PKI → CyberArk Zero Touch PKI
  - Venafi Firefly → CyberArk Workload Identity Manager

### Certificate Manager (formerly TLS Protect)
- Discovery: internet + IP scan modes; identifies every cert, owner, expiry
- CA integrations: DigiCert, Sectigo, GlobalSign, Entrust, Let's Encrypt (public); MS AD CS, EJBCA, AWS Private CA (private) [INDUSTRY-CONSENSUS + product page evidence]
- ACME, EST, SCEP, REST interfaces (Zero Touch PKI)
- Machine integrations: F5, Akamai CDN, A10 Thunder ADC, Radware Alteon, IIS, Apache, Nginx (from what's new 2025/2026)
- cert-manager (Kubernetes) integration via VSatellite
- SaaS + self-hosted deployment options
- 47-day TLS cert lifespan automation emphasis (post-2025 browser policy)

### Workload Identity Manager (formerly Firefly)
- SPIFFE/SPIRE-compatible; issues X.509-SVIDs and JWT-SVIDs
- Kubernetes-native; lightweight cert issuer
- HSM integration for signing key protection (GA June 2024)
- Policy-governed issuance; integrates with Certificate Manager SaaS for governance

### Code Sign Manager (formerly CodeSign Protect)
- HSM-backed key custody; signing-as-a-service
- Works with existing developer tools and pipelines (Jenkins, GitHub Actions, Azure DevOps)
- SaaS + self-hosted deployment options
- Authenticode, Java JAR, and other signing formats

### SSH Manager for Machines (formerly SSH Protect)
- Full SSH key inventory, discovery, trusted-relationship mapping
- Rotation and remediation workflows
- Audit logging with user/time/key correlation
- Self-hosted deployment (on-prem)

### Zero Touch PKI
- Cloud-managed PKI; globally available; multi-datacentre redundancy
- Supports SCEP, MDM, ACME, EST, REST
- Windows auto-enrollment and modern use cases

### Compliance
- SOC 2 Type 2: YES (confirmed)
- ISO 27001: YES (confirmed)
- CSA STAR: YES (Trusted Cloud Provider trustmark)
- FedRAMP: NOT found in public docs [GAP for AU government]
- IRAP: NOT found in public docs [GAP for AU government]
- Zero Touch PKI: North America and Europe data-centre redundancy confirmed; AU region NOT explicitly stated

### AU-specific
- Certificate Manager Self-Hosted: can be deployed on AU-hosted infrastructure → customer controls data residency
- Certificate Manager SaaS: US/EU datacentres confirmed; AU region not confirmed in public docs [SPECULATION — needs SE confirmation]
- No explicit IRAP assessment found in public docs

### Conjur-Venafi integration
- PAM (CyberArk EPV) can store and rotate private keys for certificate workflows [ADD-ON via platform integration]
- No deep native Conjur secrets-vault ↔ Certificate Manager integration documented publicly
- Both now under CyberArk Identity Security Platform umbrella — roadmap integration plausible

## NHI score summary (pre-write)
- NATIVE (4): NHI-006, NHI-015, NHI-016, NHI-021, NHI-025, NHI-032, NHI-036, NHI-034 (cert/SSH/codesign/workload/PKI lanes)
- ADD-ON (2-3): NHI-002, NHI-003, NHI-013, NHI-017, NHI-024, NHI-026
- GAP (0-1): NHI-001, NHI-004, NHI-005, NHI-007, NHI-008, NHI-009, NHI-010, NHI-011, NHI-012, NHI-014, NHI-018, NHI-019, NHI-020, NHI-022, NHI-023, NHI-027, NHI-028, NHI-029, NHI-030, NHI-031, NHI-033, NHI-035, NHI-037

## Citations gathered
- venafi-product-rebranding-2025
- cyberark-cert-mgr-2025
- cyberark-wim-2025
- cyberark-code-sign-mgr-2025
- cyberark-ssh-mgr-2025
- cyberark-zero-touch-pki-2025
- cyberark-mis-overview-2025
- cyberark-compliance-2025
- cyberark-mis-what-is-2025
- venafi-cloud-docs-2026
- venafi-cloud-whatsnew-2026
- venafi-wim-hsm-2024
- venafi-firefly-overview-2025

## Remaining work
- Write research/vendors/venafi.md
- Write matrix/vendor-capabilities-venafi.csv
- Append citations to meta/citations.bib
- Append log row to meta/agents.md

## Continuation instructions
Successor: read this file, then write the four output files. No additional research needed.

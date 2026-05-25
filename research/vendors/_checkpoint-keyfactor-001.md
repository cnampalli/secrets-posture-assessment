# Checkpoint — Keyfactor Vendor Researcher — 001

**Agent:** Vendor Researcher (Sonnet 4.6)
**Vendor:** Keyfactor (keyfactor)
**Prompt:** prompts/03-vendor-researcher-template.md
**Date:** 2026-05-22
**Status:** PRE-WRITE GUARD — all research complete, about to write final outputs

---

## Completed work

- Read canonical prompt (03-vendor-researcher-template.md) — full schema understood.
- Read identity-taxonomy.md — 37 NHIs (NHI-001..NHI-037).
- Read use-cases.md — 27 UC-F + 20 UC-N = 47 UCs.
- Fetched and indexed Keyfactor public documentation:
  - keyfactor-command-product (keyfactor.com/products/command/)
  - keyfactor-ejbca-product (keyfactor.com/products/ejbca-enterprise/)
  - keyfactor-signserver-product (keyfactor.com/products/signserver-enterprise/)
  - keyfactor-platform (keyfactor.com/platform/)
  - keyfactor-finserv (keyfactor.com/solutions/financial-services/)
  - keyfactor-integrations (keyfactor.com/integrations/)
  - ejbca-docs-intro (docs.keyfactor.com/ejbca/latest/ejbca-introduction)
  - keyfactor-docs-home (docs.keyfactor.com)
  - ejbca-docs-toc (docs.keyfactor.com/ejbca/latest/)
  - signserver-docs-toc + signserver-docs-ops
  - ejbca-guides (composite certs, PQC lab)
  - keyfactor-customers, keyfactor-about
  - keyfactor-pqc2 (PQC endpoint blog)
  - keyfactor-crypto-agility, keyfactor-pki-automation

## Key findings

### Keyfactor Command
- Certificate lifecycle orchestration platform (discovery, rotation, revocation, automation).
- Deployment: on-prem, SaaS Lite (Azure Marketplace), Kubernetes (Helm Charts), cloud/hybrid.
- No dedicated AWS region or AU-specific data residency stated publicly.
- Integrations: Ansible, Akamai, Kubernetes (cert-manager), ACME, REST API.
- Compliance audit logs, RBAC, key vault/HSM integrations.

### EJBCA Enterprise
- Full PKI platform (root + issuing + sub-CAs).
- Protocols: ACME, EST, CMP, SCEP, Microsoft Autoenrollment, SOAP, REST.
- PQC READY: composite certificates (ML-DSA + RSA/ECDSA/EdDSA), PQC Lab Test Drive.
- SaaS: available on AWS and Azure.
- Powers IoT identity (SCEP/EST/CMP for device enrollment).
- SPIFFE: not explicitly named in docs; EJBCA issues X.509 SVIDs; no SPIRE integration page found.

### SignServer Enterprise
- Server-side signing: code, PDF documents, XML, firmware.
- HSM integration: on-prem HSM, cloud HSM, built-in hardware appliance.
- CI/CD integration via API.
- Detailed audit logs.

### Bouncy Castle
- Keyfactor acquired Bouncy Castle (BC FIPS Java + .NET) — open-source crypto library.
- Early PQC adopter via BC: ML-DSA, ML-KEM, SLH-DSA algorithms.
- Powers EJBCA and SignServer crypto layers.

### PQC
- EJBCA: composite certificate issuance (hybrid classical + ML-DSA).
- Keyfactor PQC Lab Test Drive available.
- "State of Quantum Readiness" report published.
- Crypto-agility blog.

### Compliance
- Financial services page mentions compliance readiness; SOC 2 resources page exists.
- No explicit IRAP mention found publicly.
- No FedRAMP authorization found in public pages.
- Customers: M&T Bank, EQ Bank, RSA Security, ServiceNow.

### HSM
- Command: integrations to "popular HSMs and key vaults."
- SignServer: on-prem or cloud HSM, or built-in hardware appliance.
- EJBCA: supports HSM-backed CA keys (standard for PKI).
- Specific named HSM vendors (Thales Luna, nCipher, Entrust, Fortanix) mentioned in taxonomy but not confirmed in fetched pages — [INDUSTRY-CONSENSUS] / requires SE confirmation.

### SPIFFE / Workload Identity
- No dedicated SPIFFE/SPIRE integration page found; EJBCA can issue X.509 SVIDs [INDUSTRY-CONSENSUS]; no native SPIRE server/agent.

## Remaining work

- Write vendors/keyfactor.md  [NEXT]
- Write matrix/vendor-capabilities-keyfactor.csv [NEXT]
- Append citations to meta/citations.bib [NEXT]
- Append log row to meta/agents.md [LAST]

## Citations gathered

- keyfactor-command-2024: https://www.keyfactor.com/products/command/
- keyfactor-ejbca-2024: https://www.keyfactor.com/products/ejbca-enterprise/
- keyfactor-signserver-2024: https://www.keyfactor.com/products/signserver-enterprise/
- keyfactor-platform-2024: https://www.keyfactor.com/platform/
- ejbca-docs-intro-2024: https://docs.keyfactor.com/ejbca/latest/ejbca-introduction
- ejbca-pqc-guide-2024: https://docs.keyfactor.com/ejbca/latest/issue-composite-certificates
- keyfactor-finserv-2024: https://www.keyfactor.com/solutions/financial-services/
- keyfactor-integrations-2024: https://www.keyfactor.com/integrations/
- signserver-docs-2024: https://docs.keyfactor.com/signserver/latest/signserver-operations
- keyfactor-crypto-agility-2024: https://www.keyfactor.com/blog/crypto-agility/

## Continuation instructions

If handoff required: re-read this checkpoint, then write the three output files in order. All research is complete.

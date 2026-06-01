# Checkpoint — Infisical Vendor Researcher (Sonnet 4.6)

**Checkpoint ID:** _checkpoint-infisical-001.md
**Date:** 2026-05-22
**Status:** Pre-write guard (Invariant #8 — written before full output to ensure recovery path)

## Completed work

- Read canonical prompt (03-vendor-researcher-template.md)
- Read identity-taxonomy.md (37 NHIs), use-cases.md (27 UC-F + 20 UC-N), prompts/README.md
- Fetched and indexed 28 Infisical documentation URLs across:
  - Getting started / intro, self-hosting, pricing
  - Auth methods: Universal Auth, Kubernetes, AWS, Azure, GCP, OIDC, JWT
  - Secret rotation, dynamic secrets (PostgreSQL, Oracle, AWS IAM)
  - KMS overview, HSM integration (Thales Luna, Fortanix, AWS CloudHSM)
  - PKI / CA overview, PQC algorithms page
  - SSH (404 — docs page exists but not at expected path; confirmed via GitHub)
  - Secret scanning CLI, audit logs, Kubernetes operator / Helm
  - SSO, access controls, security architecture, GitHub repo

## Key findings

### Licensing
- Core repo: MIT expat licence (github.com/Infisical/infisical)
- Enterprise features in `/ee` directory require commercial licence
- Three tiers: Free, Pro ($18/identity/month), Enterprise (custom)

### Deployment
- Cloud (US/EU regions — no confirmed AU SaaS region)
- Self-hosted: Docker Compose, Kubernetes/Helm, bare-metal Linux
- Architecture: PostgreSQL + Redis backend

### Auth methods (all confirmed native)
- Universal Auth (client ID/secret), AWS Auth, Azure Auth, GCP Auth, Kubernetes Auth, OIDC Auth, JWT Auth
- LDAP: Enterprise tier only (listed in pricing)
- SSO: SAML/OIDC via Enterprise; requires email-domain verification

### Secret rotation (v2)
- PostgreSQL, MySQL, AWS IAM confirmed via docs
- Rotation interval (days) with auto-rotation toggle

### Dynamic secrets (confirmed)
- AWS ElastiCache, AWS IAM, AWS MemoryDB, PostgreSQL, Oracle
- Navigation menu also shows more templates (Kubernetes, Redis, Cassandra, MongoDB)

### KMS
- Internal KMS: AES-256-GCM, per-org/per-project keys
- External KMS: AWS KMS, GCP KMS, Azure KMS via settings
- HSM: Thales Luna, Fortanix, AWS CloudHSM via PKCS#11 — Enterprise self-hosted only

### PKI
- Internal CA (private CA hierarchy), External CA (ACME, Let's Encrypt, DigiCert, Microsoft ADCS)
- Enrollment: API, ACME, EST
- Certificate lifecycle, CRL, policies/profiles
- Code signing, certificate discovery, certificate syncs (AWS ACM, Azure)

### SSH
- Confirmed in GitHub README: "Signed SSH Certificates" with link to /docs/documentation/platform/ssh
- Docs page 404 — may be recent feature or path changed

### PQC
- Dedicated page at /docs/documentation/platform/pki/reference/pqc-algorithms
- Confirmed in PKI section — post-quantum algorithms reference exists

### Secret scanning
- CLI-based, 140+ secret types, pre-commit hook install, git history scanning

### MCP / AI
- GitHub README and pricing show "AI Security Advisor" (Enterprise)
- MCP server URL 404 — may be undocumented/recent

### Compliance
- SOC 2 reports available at Enterprise tier
- Self-hosting enables HIPAA, FIPS 140-3 alignment
- No confirmed ISO 27001 primary source found

### AU sovereignty
- No AU-specific SaaS region confirmed
- Self-hosting provides full data sovereignty
- APRA CPS 230/234 alignment possible via self-hosted only

## Remaining work
- Write infisical.md vendor profile
- Write vendor-capabilities-infisical.csv (84 rows: 37 NHI + 47 UC)
- Append BibTeX to meta/citations.bib
- Append row to meta/agents.md (LAST write)

## Citations gathered
- infisical-github-2024 (github.com/Infisical/infisical)
- infisical-intro-2024 (infisical.com/docs/.../introduction)
- infisical-pricing-2024 (infisical.com/pricing)
- infisical-security-2024 (infisical.com/security)
- infisical-selfhost-2024 (infisical.com/docs/self-hosting/overview)
- infisical-universal-auth-2024
- infisical-k8s-auth-2024
- infisical-aws-auth-2024
- infisical-oidc-auth-2024
- infisical-rotation-2024
- infisical-dynamic-secrets-2024
- infisical-kms-2024
- infisical-kms-hsm-2024
- infisical-pki-2024
- infisical-scanning-2024
- infisical-pqc-2024
- infisical-k8s-operator-2024
- infisical-audit-2024

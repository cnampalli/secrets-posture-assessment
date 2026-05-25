# Checkpoint — Akeyless Vendor Researcher — 001

**Date:** 2026-05-22
**Agent:** Vendor Researcher (Sonnet 4.6) — prompt 03 v0.1
**Status:** RESEARCH COMPLETE — writing output files

## Completed work

- Read canonical prompt (03-vendor-researcher-template.md)
- Read identity-taxonomy.md (NHI-001 through NHI-037)
- Read use-cases.md (UC-F-001 through UC-F-027 + UC-N-001 through UC-N-020)
- Read prompts/README.md (invariants)
- Fetched and indexed 18 Akeyless documentation pages via ctx_fetch_and_index
- Searched all indexed content across 14 topic queries
- Web searched: pricing, compliance, AU presence

## Key findings (not yet flushed to final outputs)

### DFC Architecture
- DFC = Distributed Fragments Cryptography — proprietary Akeyless patent
- Key material split into multiple independent fragments; complete key NEVER reconstructed on any single server
- Operations performed via cryptographic derivation across independent fragments
- Customer Fragment optional: if deployed via Gateway, customer holds one fragment to which Akeyless has NO access → operational zero-knowledge
- Without Customer Fragment: Akeyless holds all fragments → partial zero-knowledge (marketing claim partially accurate)

### FIPS
- FIPS 140-3 validated, Certificate #5227 (NIST CMVP) — NOT Level 3 hardware; software module
- Trust center also references FIPS 140-2 (legacy references in marketing copy; cert page shows 140-3)

### Compliance
- SOC 2 Type II ✓, ISO 27001 ✓, ISO 27701 ✓, PCI DSS ✓, HIPAA ✓, DORA ✓
- IRAP: NOT mentioned anywhere in public docs → GAP for AU government/regulated use
- FedRAMP: NOT mentioned → GAP

### SaaS Regions
- US SaaS: console.akeyless.io
- EU SaaS: console.eu.akeyless.io
- No AP / Australia SaaS region documented publicly
- Gateway can be self-hosted anywhere (including AU-hosted customer environment) → Customer controls data residency via Gateway + Customer Fragment

### Auth Methods (full list)
API Key, AWS IAM, Azure AD, Certificates, Email, GCP IAM, Kerberos, Kubernetes (dedicated SA), LDAP, OAuth 2.0/JWT, OCI IAM, OIDC (Auth0, Azure AD, GitHub, GitLab, Google, Okta), SAML (Azure AD, Okta, Ping Identity), Universal Identity

### Dynamic Secrets (producers)
AWS, Azure AD, Chef Infra, Database (MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis, Redshift, Snowflake, Cassandra, HanaDB), Docker Hub, EKS, GCP, GitHub, GitLab, GKE, Google Workspace, K8s generic, LDAP, OpenAI, Ping, RabbitMQ, RDP, Snowflake

### Rotated Secrets
Database, LDAP, AWS, Azure, GCP, Docker Hub, Windows, SSH, OpenAI, Splunk, Custom

### AI/Agentic features (2026)
- Agentic Runtime Authority (early access) — policy-based access control for AI agents; input/output rules; traceable sessions
- Prompt Injection Protection for AI Agents — secretless runtime access patterns
- AI Security overview page
- Identity & Secrets Intelligence (early access) — NHI discovery/analytics surface
- MCP Server integration (Claude Desktop, Cursor, GitHub Copilot, JetBrains)

### SPIRE
- 4 SPIRE plugins: Key Manager, Secret Manager, Upstream Authority, Upstream Authority SM
- Full SPIFFE/SPIRE integration as Upstream Authority / Key Manager backend

### PKI/Certificates
- Certificate Lifecycle Management, ACME Server, Certificate Discovery, Certificate Provisioning, Renewal, Revocation List
- SSH certificates, PKI certificate issuer
- Code signing (Java JAR, APK)
- Public CA integration, Venafi target

### PQC
- Hybrid PQC TLS: X25519MLKEM768 between clients and SaaS/Gateway (TLS 1.3)
- No PQC for key-storage (ML-KEM/ML-DSA for secrets at rest not yet documented)

### Audit / SIEM
- Gateway Log Forwarding to: Amazon S3, Azure Log Analytics, Datadog, Elasticsearch, Google Chronicle, Logstash, Logz.io, Splunk, SumoLogic, stdout

### NHI Inventory
- Resource Discovery: imports domain + local users as Rotated Secrets, servers as SSH/Windows targets
- Identity & Secrets Intelligence (early access): NHI analytics dashboard — stale credentials, ownership, anomaly

### Pricing
- Consumption-based / transaction-quota model; overage invoiced annually
- AWS Marketplace available (monthly recurring)
- No public per-secret or per-API-call rate card

### AU/Australian notes
- No dedicated AU/AP SaaS region documented
- Gateway can be AU-hosted → addresses APRA data residency IF Gateway + Customer Fragment deployed in AU
- No IRAP assessment listed
- No named AU financial services customers in public docs

## Remaining work
- Write vendors/akeyless.md (IN PROGRESS)
- Write matrix/vendor-capabilities-akeyless.csv (IN PROGRESS)
- Append meta/citations.bib
- Append meta/agents.md

## Citations gathered
- akeyless-dfc-overview-2024: https://docs.akeyless.io/docs/dfc-overview.md
- akeyless-dfc-deepdive-2024: https://docs.akeyless.io/docs/dfc-deep-dive.md
- akeyless-zero-knowledge-2024: https://docs.akeyless.io/docs/zero-knowledge.md
- akeyless-fips-2024: https://docs.akeyless.io/docs/fips.md
- akeyless-components-2024: https://docs.akeyless.io/docs/components.md
- akeyless-gw-overview-2024: https://docs.akeyless.io/docs/gateway-overview.md
- akeyless-gw-zk-2024: https://docs.akeyless.io/docs/gateway-zero-knowledge.md
- akeyless-spire-2024: https://docs.akeyless.io/docs/spire-plugins.md
- akeyless-agentic-2024: https://docs.akeyless.io/docs/agentic-runtime-authority.md
- akeyless-ai-security-2024: https://docs.akeyless.io/docs/ai-security.md
- akeyless-prompt-injection-2024: https://docs.akeyless.io/docs/prompt-injection-protection-for-ai-agents.md
- akeyless-discovery-2024: https://docs.akeyless.io/docs/resource-discovery.md
- akeyless-pqc-2024: https://docs.akeyless.io/docs/gateway-pqc-support-reference.md
- akeyless-trust-center-2024: https://www.akeyless.io/trust-center/
- akeyless-log-fwd-2024: https://docs.akeyless.io/docs/gateway-log-forwarding.md
- akeyless-auth-overview-2024: https://docs.akeyless.io/docs/auth-overview.md
- akeyless-isi-2024: https://docs.akeyless.io/docs/identity-and-secrets-intelligence.md
- akeyless-saas-us-2024: https://docs.akeyless.io/docs/akeyless-saas-core-services-us.md
- akeyless-saas-eu-2024: https://docs.akeyless.io/docs/akeyless-saas-core-services-eu.md

## Continuation instructions
If this session is truncated, successor should:
1. Read this checkpoint
2. Read vendors/akeyless.md (may be partially written)
3. Read matrix/vendor-capabilities-akeyless.csv (may be partially written)
4. Continue from where partial writing stopped
5. Append remaining citations to meta/citations.bib
6. Append log row to meta/agents.md

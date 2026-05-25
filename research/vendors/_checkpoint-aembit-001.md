# Checkpoint — Aembit Vendor Research (aembit-001)

**Agent:** Vendor Researcher (Sonnet 4.6, prompt 03 v0.1)
**Date:** 2026-05-23
**Status:** PRE-WRITE — all research complete, writing output files now.

## Completed work

- Read canonical prompt (03-vendor-researcher-template.md)
- Read identity-taxonomy.md (37 NHIs)
- Read use-cases.md (27 UC-F + 20 UC-N = 47 UCs)
- Read prompts/README.md (invariants)
- Read meta/agents.md (context on prior runs)
- Executed 18 web research calls (WebSearch + WebFetch) on Aembit

## Key findings

### Company
- Founded 2021, HQ Silver Spring MD; ~45 employees
- $25M Series A (Sep 2024), ~$45M total raised; Acrew Capital lead; Ballistic, Ten Eleven, Okta Ventures, CrowdStrike Falcon Fund
- Tier: nhi-discovery (workload-IAM / access-management sub-niche)
- Tagline: "Attest. Authenticate. Accelerate."

### Architecture
- Hybrid: Aembit Cloud (control plane) + Aembit Edge (deployable agent / auth proxy)
- Edge deployable on K8s (Helm), AWS ECS Fargate, Lambda, VMs
- Terraform provider available; no self-hosted control plane option found

### Trust Providers (attestation methods)
1. AWS Metadata Service
2. AWS Role
3. Azure Instance Metadata Service / Azure Entra WIF
4. Azure Metadata Service
5. GCP Identity Token / GCP WIF
6. GitHub Actions OIDC
7. GitLab Job OIDC
8. Kubernetes Service Account (EKS, AKS, GKE, self-hosted)
9. Kerberos (Windows/AD on-prem)
10. OIDC ID Token (generic)
11. SAMLv2
12. Terraform Cloud Identity Token
13. Certificate Signed Attestation
- SPIFFE SVIDs supported as credential OUTPUT (JWT-SVID, X.509-SVID); no native SPIRE integration found (Aembit layers above/beside SPIRE)

### Credential Providers (target systems)
- API Key, Username/Password
- JSON Web Token (JWT)
- OAuth 2.0 Client Credentials, OAuth 2.0 Authorization Code
- AWS STS, AWS Secrets Manager, AWS IAM Role Federation
- Azure Entra WIF, Azure Key Vault
- GCP WIF
- HashiCorp Vault (integration)
- SPIFFE JWT-SVID, X.509-SVID
- OIDC ID Token
- GitLab account (managed), Aembit Access Token
- MCP User-Based Access Token

### Named target systems in cookbook/docs
- Snowflake, PostgreSQL, MySQL, Redis, HTTP/HTTPS APIs
- Atlassian, GitLab, Slack, Google Workspace, PagerDuty (SaaS via OAuth)

### Conditional Access
- Geo IP access conditions (NATIVE)
- Time-based access conditions (NATIVE)
- CrowdStrike Falcon posture integration (NATIVE, in Enterprise tier)
- Wiz security findings integration (NATIVE, Enterprise tier)

### AI Agent / Agentic Identity
- Blended Identity: cryptographic agent identity + human binding (GA April 2026, RSA Conf)
- MCP Identity Gateway: OAuth 2.1 Authorization Server + token exchange without exposing creds to agent runtime
- Pricing: Starter free / AI Teams $20/agent/month / Enterprise custom
- Customer: $300B investment firm deploying Claude agents via Aembit

### Compliance
- SOC 2 Type II: Feb 2024 initial; Feb 2025 recertification (Sensiba LLP auditor)
- ISO 27001:2022: March 2025 (Sensiba LLP, ANAB-accredited)
- FedRAMP: NOT FOUND
- IRAP: NOT FOUND
- AU data residency: NOT FOUND — SaaS control plane only; no AU region documented

### SPIFFE relationship
- Aembit integrates with existing SPIRE deployments (layers above, does not replace)
- Issues SPIFFE JWT-SVID and X.509-SVID as credential types
- Addresses gaps SPIRE leaves (SaaS, legacy apps, on-prem, AI agents)

### Vault/secrets relationship
- Aembit can use HashiCorp Vault and AWS Secrets Manager as credential providers (source)
- Also AWS Secrets Manager and Azure Key Vault as sources
- Aembit is a broker layer above vault — does NOT store secrets at rest
- "Secretless" model: no stored credentials in Aembit; JIT issuance only

### Customer references
- Snowflake CISO Brad Jones quote (Series A press release)
- Snowflake case study: 85% credential workload reduction, 5-10 hrs/day saved
- $300B investment firm (unnamed) for AI agent deployment

### AU-specific
- No AU data residency region
- No IRAP assessment
- No Essential 8 or APRA CPS 234 mapping found publicly
- No AU customer references found
- Material blocker for APRA-regulated production adoption

## Remaining work
- Write research/vendors/aembit.md
- Write matrix/vendor-capabilities-aembit.csv (84 rows: 37 NHI + 47 UC)
- Append to meta/citations.bib
- Append to meta/agents.md (LAST)

## Citations gathered
- aembit-arch-2024: https://docs.aembit.io
- aembit-trust-providers-2024: https://docs.aembit.io/user-guide/access-policies/trust-providers/kubernetes-service-account-trust-provider
- aembit-credential-providers-2024: https://docs.aembit.io/user-guide/access-policies/credential-providers/oauth-authorization-code
- aembit-agentic-ai-ga-2026: https://aembit.io/blog/aembit-iam-for-agentic-ai-is-now-generally-available/
- aembit-agentic-ai-launch-2025: https://aembit.io/press-release/aembit-introduces-identity-and-access-management-for-agentic-ai/
- aembit-soc2-2024: https://aembit.io/press-release/aembit-achieves-soc-2-type-ii-compliance-for-data-security/
- aembit-soc2-recert-2025: https://aembit.io/blog/aembit-earns-soc-2-type-ii-recertification-for-ongoing-security-and-compliance/
- aembit-iso27001-2025: https://aembit.io/blog/aembit-achieves-iso-27001-certification/
- aembit-series-a-2024: https://aembit.io/press-release/aembit-raises-25-million-in-series-a-funding-for-non-human-identity-and-access-management/
- aembit-snowflake-case-study-2024: https://aembit.io/case-study/snowflake-uses-aembit-to-secure-workload-access/
- aembit-conditional-access-2024: https://aembit.io/blog/introducing-workload-conditional-access-in-aembit/
- aembit-crowdstrike-2024: https://aembit.io/press-release/aembit-and-crowdstrike-enhance-non-human-workload-security/
- aembit-wiz-2024: https://docs.aembit.io/user-guide/access-policies/access-conditions/integrations/wiz/
- aembit-spiffe-2025: https://aembit.io/blog/everyone-wants-spiffe-almost-no-one-can-afford-to-build-it-right/
- aembit-ms-environments-2025: https://aembit.io/blog/introducing-comprehensive-workload-identity-and-access-management-across-microsoft-environments/
- aembit-nhi-2024: https://aembit.io/aembit-non-human-identity-and-access-management/
- aembit-wiam-guide-2024: https://aembit.io/blog/the-what-where-and-why-of-workload-identity-and-access-management/

## Continuation instructions
If handoff needed: read this checkpoint + identity-taxonomy.md + use-cases.md then continue writing output files.

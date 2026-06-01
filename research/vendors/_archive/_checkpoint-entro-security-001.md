# Checkpoint — Entro Security Vendor Profile
**Agent:** Vendor Researcher (Sonnet 4.6, prompt 03 v0.1)
**Checkpoint:** 001 (pre-write guard — within 4,000-word Sonnet budget)
**Date:** 2026-05-23

## Completed work
- Read canonical prompt, identity-taxonomy.md, use-cases.md, README.md
- Fetched entro.security homepage, platform-non-human-identities, platform-secrets, platform-ai-agents, integrations, financial-services, discovery page, Wiz integration blog, Dell Technologies Capital Series A post, NHIMG profile, GlobeNewswire Nov 2024 announcement
- Searched: NHI platform/lineage, funding, compliance/IRAP/AU, vault integrations, NHIDR/posture/rotation, M&A, founding team
- Total tool results consumed: ~22

## Key findings
- **Company:** Entro Security Ltd, founded 2022, Tel Aviv (Israel), HQ listed as Boston. CEO Itzik Alvas (ex-Microsoft Defender for Cloud), CTO Adam Cheriki (ex-Javelin Networks/Symantec)
- **Funding:** $6M seed + $18M Series A (June 2024, led by Dell Technologies Capital). Total $24M. M&A offer reportedly received April 2025 — unconfirmed acquirer.
- **Deployment:** SaaS only (app.entro.security). No self-hosted or private-cloud option documented publicly.
- **Discovery sources (confirmed):** 50+ integrations — Vaults: 1Password, Akeyless, AWS SM, Azure KV, BeyondTrust, CyberArk Conjur, Delinea, GCP SM, HashiCorp Vault, K8s Secrets, LastPass; CI/CD: Azure DevOps, CircleCI, Drone CI, GitHub Actions, Jenkins, Octopus Deploy, TeamCity, Travis CI; Repos: Bitbucket, GitHub, GitLab (incl. on-prem); Cloud: AWS, Azure, GCP, OCI; IdP: AD, Azure AD, Okta, SAML; SaaS: Confluence, Jira, Slack, Teams, Google Workspace, Salesforce, ServiceNow, Snowflake, Workday, etc.; SIEM: Datadog, Elastic, Sentinel, QRadar, Splunk, Wiz
- **Secret types:** 1,200+ types detected via ContextIQ™ AI model
- **NHI lineage / secret context:** Core differentiator — maps creation→storage→consumption paths; traces who created token, where stored, who/what uses it
- **NHIDR™:** Behavioral anomaly detection engine; baselines NHI activity; detects re-activated stale identities, multi-device token use; automated remediation triggers
- **Posture management:** Continuous assessment; right-sizes permissions, removes idle/orphaned NHIs; compliance posture against SOC2, HIPAA, PCI, ISO27001
- **Rotation:** Policy enforcement, active rotation of at-risk secrets, vaulting enforcement — but Entro does NOT store secrets; it triggers/orchestrates rotation into existing vaults
- **AI agent coverage:** Dedicated platform pillar — discovers shadow agents, maps agent→NHI→resource chains, NHIDR monitoring of agentic credential use; integrates OpenAI, Claude, MCP servers
- **Compliance:** ISO 27001 certified, SOC 2 Type II. No IRAP, no AU data residency, no FedRAMP mentioned anywhere.
- **AU sovereignty:** No AU region, no IRAP. SaaS-only with no documented AU data residency option — material APRA gap.
- **Customers (named publicly):** Elastic, SolarWinds, Nasuni, Booking.com, Regatta (outdoor brand). No Tier-1 AU FI references found.
- **Wiz integration:** First NHI/secrets platform in Wiz Integration Network (WIN); correlates NHI permissions with DSPM data classification (PCI/PHI/PII)

## Remaining work
- Write vendor profile markdown
- Write CSV rows (37 NHI + 47 UC = 84 rows)
- Append BibTeX to citations.bib
- Append log row to agents.md (LAST write)

## Citations gathered
- entro-security-homepage-2025
- entro-security-integrations-2025
- entro-security-nhi-platform-2025
- entro-security-secrets-platform-2025
- entro-security-ai-agents-2025
- entro-security-financial-svcs-2025
- entro-security-wiz-integration-2025
- entro-security-series-a-2024
- entro-security-dtc-series-a-2024
- entro-security-nov-2024-announcement
- entro-security-nhidr-h1-2025

## Continuation instructions
- Read this checkpoint before proceeding
- Output paths: research/vendors/entro-security.md, matrix/vendor-capabilities-entro-security.csv
- Append BibTeX under ## Entro Security (Agent 03 wave 4) in meta/citations.bib
- Append log row to meta/agents.md AS LAST WRITE

# Checkpoint — Astrix Security Vendor Researcher
**Agent:** Vendor Researcher (Sonnet 4.6), prompt 03 v0.1
**Checkpoint ID:** 001
**Created:** 2026-05-23
**Status:** PRE-WRITE — all research complete; writing outputs now

## Completed work
- Read canonical prompt, identity-taxonomy.md, use-cases.md, README.md
- Read meta/citations.bib (header + first 80 lines) and meta/agents.md
- Fetched: astrix.security (homepage), /product/, /product/discover-non-human-identities/, /product/ai-agent-discovery/, /use-cases/lifecycle-management/, /use-cases/third-party-risk/, /use-cases/secret-management/, /security-programs/iam-itdr/, /why-astrix/, /learn/blog/a-new-chapter-astrix-security-is-joining-cisco/, /learn/customer-stories/rsac-2025-how-workday-implemented-nhi-security/
- WebSearch: NHI platform features, compliance/IRAP, funding/customers, integrations, Cisco acquisition
- Tool results consumed: ~18 (within Sonnet 4,000-word checkpoint heuristic; writing now)

## Key findings
- Founded 2021 (Tel Aviv / NY); SaaS-only; agentless API-based
- Cisco acquisition announced 2026-05-04 (~$250–350M); pending close
- SOC 2 Type 2 (Big Four audit); NO ISO 27001 or IRAP found
- $85M total VC (Series B $45M Dec 2024; investors: CRV, Menlo, Workday Ventures, BVP)
- Fortune Cyber 60 2026; Gartner Hype Cycle for Digital Identity 2025 (Workload Identity Mgmt)
- Discovery: agentless, API-based; 20+ integrations (AWS, Azure, GCP, GitHub, Slack, Salesforce, Okta, Databricks, Snowflake, K8s, ServiceNow, etc.)
- NHI types covered: OAuth apps, API keys, service accounts, IAM roles, secrets, webhooks, PATs, managed identities, AI agents, MCP servers
- Anomaly detection: ML behavioral analytics on access patterns + API traffic (Agentic Detection & Response / ADR™)
- Lifecycle: provisioning, rotation/revocation, decommissioning, attestation workflows, ITSM/SIEM/GRC integration
- Secrets: discovers unvaulted secrets; aggregates across vaults; automated rotation enforcement (vault names not explicitly disclosed)
- OAuth/SaaS risk: strong — continuous third-party app inventory, vendor reputation scoring, stale token revocation
- AU: NO explicit AU region / data-residency / IRAP claims found; SaaS-only = data residency risk for APRA
- Customers: Workday, NetApp, Priceline, Figma, HubSpot, Boomi, Mercury, Pagaya — tech/SaaS dominant; NO Tier-1 FI or AU bank cited
- AI agent: differentiated capability — ACP, Agent Policies, four-method discovery, MCP server governance

## Remaining work
- Write research/vendors/astrix-security.md
- Write matrix/vendor-capabilities-astrix-security.csv (84 rows: 37 NHI + 47 UC)
- Append BibTeX to meta/citations.bib
- Append log row to meta/agents.md (LAST write)

## Citations gathered
- astrix-nhi-platform-2026: https://astrix.security/product/
- astrix-nhi-discover-2026: https://astrix.security/product/discover-non-human-identities/
- astrix-ai-agent-discovery-2026: https://astrix.security/product/ai-agent-discovery/
- astrix-lifecycle-2026: https://astrix.security/use-cases/lifecycle-management/
- astrix-third-party-risk-2026: https://astrix.security/use-cases/third-party-risk/
- astrix-secret-management-2026: https://astrix.security/use-cases/secret-management/
- astrix-iam-itdr-2026: https://astrix.security/security-programs/iam-itdr/
- astrix-why-2026: https://astrix.security/why-astrix/
- astrix-cisco-2026: https://astrix.security/learn/blog/a-new-chapter-astrix-security-is-joining-cisco/
- astrix-workday-2026: https://astrix.security/learn/customer-stories/rsac-2025-how-workday-implemented-nhi-security/
- astrix-state-nhi-2024: https://astrix.security/learn/whitepapers/the-state-of-non-human-identity-security/
- astrix-soc2-2022: https://www.prnewswire.com/news-releases/astrix-security-achieves-soc-2-type-2-certification-five-months-after-emerging-from-stealth-301595305.html
- astrix-series-b-2024: https://astrix.security/learn/news/astrix-raises-45m-series-b-to-redefine-identity-security-for-the-ai-era/
- astrix-helpnet-2026: https://www.helpnetsecurity.com/2026/03/23/astrix-security-ai-agent-security-platform-expansion/
- cisco-astrix-securityweek-2026: https://www.securityweek.com/cisco-moves-to-acquire-astrix-security-to-tackle-non-human-identity-risks/

## Continuation instructions
All research complete. Successor should read this checkpoint and proceed directly to writing outputs. No further web fetching needed.

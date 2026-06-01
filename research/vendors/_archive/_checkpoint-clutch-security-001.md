# Checkpoint — Clutch Security Vendor Researcher
**Agent:** Sonnet 4.6 (prompt 03 v0.1)
**Checkpoint:** 001 (pre-write guard)
**Date:** 2026-05-23
**Status:** Research complete; writing final outputs.

## Completed work
- Read canonical prompt, taxonomy (37 NHI), use-cases (27 UC-F + 20 UC-N), README invariants.
- Fetched clutch.security homepage, platform page, integrations page, principles page.
- Fetched Series A blog post, AWS Marketplace listing.
- Fetched MCP Server blog post, Agentic AI Governance page, Shadow AI Discovery page.
- Ran 6 web searches covering funding, AU/IRAP, Identity Lineage integrations, customer refs, rotation philosophy.

## Key findings
- **Deployment:** Agentless SaaS; Zero-Knowledge Architecture (data stays in customer network); AWS Marketplace listed ($50k/year Starter Pack).
- **Funding:** $28.5M total — $8.5M Seed (July 2024, Lightspeed+Merlin), $20M Series A (Jan 2025, SignalFire lead + Lightspeed + Merlin + Cyber Club London).
- **Founders:** CEO Ofir Har-Chen; Israeli-founded (Sygnia/Hunters background).
- **Differentiator:** Identity Lineage® Graph — maps every NHI to origin, owner, storage, consumers, resources. "Universal NHI" platform.
- **Discovery sources:** Cloud (AWS/Azure/GCP), SaaS 100+ apps, vaults (HashiCorp, CyberArk, Delinea, 1Password, AWS SM), code repos (GitHub/GitLab/Bitbucket), CI/CD (Jenkins/CircleCI/Azure DevOps), Kubernetes, endpoints, AI platforms.
- **Rotation philosophy:** Anti-rotation — advocates ephemeral credentials + ZT over rotation cycles. Orchestration of rotation is NOT the product focus; visibility + ZT is.
- **AI agent:** Shadow AI / MCP server discovery (Aug 2025); Agentic AI Governance page; agent guardrails; detects Claude/Copilot/Cursor MCP usage. GA feature.
- **Secret scanning:** Contextual secret scanning with blast-radius context; vault augmentation.
- **Risk scoring:** Blast-radius driven; prioritises by access scope and damage potential.
- **SOC 2 + ISO 27001:** Confirmed (homepage + Cybersecurity Excellence Awards).
- **AU/APAC:** No AU data residency region found; no IRAP; no APRA CPS 234 mapping — material gap.
- **Customers:** NTT Data (75k+ employees), Fluidra, OpenWeb, Cedar. Banking/FS sector claimed but no named Tier-1 bank reference.
- **Universal NHI MCP Server:** Announced Aug 21 2025 — natural language NHI queries, autonomous remediation.

## Remaining work
- Write vendors/clutch-security.md (all 8 sections).
- Write matrix/vendor-capabilities-clutch-security.csv (84 rows: 37 NHI + 47 UC).
- Append BibTeX to meta/citations.bib.
- Append log row to meta/agents.md (LAST operation).

## Citations gathered
- clutch-homepage-2025: https://www.clutch.security/
- clutch-platform-2025: https://www.clutch.security/platform
- clutch-principles-2025: https://www.clutch.security/principles
- clutch-series-a-2025: https://www.clutch.security/blog/clutch-security-20M-series-a
- clutch-mcp-server-2025: https://www.clutch.security/blog/introducing-the-first-universal-nhi-mcp-server-intelligent-identity-lineage-tm-at-your-fingertips
- clutch-shadow-ai-2025: https://www.clutch.security/use-cases/shadow-ai-discovery
- clutch-agentic-ai-2025: https://www.clutch.security/platform/agentic-ai-governance
- clutch-aws-marketplace-2025: https://aws.amazon.com/marketplace/pp/prodview-6xqgcbyf7vj7m
- signalfire-clutch-2025: https://www.signalfire.com/blog/signalfire-leads-clutch-security-series-a
- clutch-integrations-2025: https://www.clutch.security/integrations

## Sensitive tags
[PUBLIC] — all sources are public vendor documentation or news.

## Continuation instructions
If a successor agent is needed, re-read:
- prompts/03-vendor-researcher-template.md
- This checkpoint file
Output paths:
- research/vendors/clutch-security.md
- matrix/vendor-capabilities-clutch-security.csv
- meta/citations.bib (append under "## Clutch Security (Agent 03 wave 4)")
- meta/agents.md (append log row LAST)

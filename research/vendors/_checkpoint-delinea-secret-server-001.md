# Checkpoint — Delinea Secret Server Vendor Researcher (Agent 03 Wave 1)

**Checkpoint ID:** 001  
**Written:** 2026-05-22  
**Agent:** Sonnet 4.6 — Vendor Researcher (prompt 03 v0.1)  
**Status:** PRE-WRITE — completing all outputs in this turn

## Completed work

- Read canonical prompt `prompts/03-vendor-researcher-template.md`
- Read `research/identity-taxonomy.md` (37 NHIs: NHI-001 to NHI-037)
- Read `research/use-cases.md` (47 UCs: UC-F-001 to UC-F-027 + UC-N-001 to UC-N-020)
- Read `prompts/README.md` (8 invariants confirmed)
- Fetched Delinea docs: start.htm, authentication, discovery, security-hardening, api-scripting, features, product page, home, admin, privilege-manager
- Tool results consumed: ~14 fetch calls + search rounds

## Key findings (not yet flushed)

### Architecture
- Self-hosted: Windows Server + MS SQL Server backend; AES-256 CBC at rest, TLS 1.2+ in transit
- Cloud: SaaS edition (previously Thycotic.com, rebranded Secret Server Cloud)
- Distributed Engine (DE) architecture — lightweight proxy agents deployed on-prem to relay requests; supports multi-site federated deployments
- HA: multiple web nodes behind load balancer + multiple DEs per site
- HSM: integration documented but specific vendor list not confirmed from public docs (Safenet/Thales referenced in community)
- Auth: Windows Auth, SAML, LDAP/AD, MFA supported
- REST API + SOAP/Web Services API; token-based auth

### Discovery
- AD discovery: Windows local admin, Windows domain accounts, scheduled tasks, app pools, services
- Linux/Unix non-daemon accounts
- AWS, GCP discovery (IAM accounts)
- ESX/ESXi discovery
- Extensible via custom PowerShell

### Rotation (Remote Password Changing - RPC)
- Extensive built-in password changers for AD, Windows local, SQL, Oracle, MySQL, Unix, network devices
- Heartbeat capability to detect password drift
- Custom password changers via PowerShell

### Kubernetes / DevOps
- REST API integration; no native K8s controller documented publicly
- DevOps Secrets Vault (DSV) is a separate lighter product for DevOps workflows
- CI/CD via REST API + scripts

### Certificates
- Certificate management feature in later versions but limited scope vs. Venafi/Keyfactor
- Not a full CLM (Certificate Lifecycle Management) product

### HSM
- Supports HSM for master encryption key; Thales/SafeNet mentioned in community docs
- Not as extensively documented publicly as Vault/CyberArk

### Cloud IAM / Dynamic Creds
- Can manage AWS/Azure/GCP service account passwords (static rotation)
- No native dynamic ephemeral cloud credential generation (unlike Vault)

### Delinea Platform / StrongDM
- Delinea acquiring StrongDM for JIT runtime authorization — extends platform coverage
- Privilege Manager = endpoint privilege management (separate product, EPM)
- DSV = DevOps Secrets Vault (lighter developer-facing vault)

### Australian footprint
- Delinea is used in AU financial services (community evidence); no dedicated AU data center confirmed in public docs
- Secret Server Cloud regions: US, EU — AU region not confirmed publicly

### Mainframe / Legacy
- No documented RACF/Top Secret/ACF2 support in Secret Server
- Network device (Cisco, Juniper, F5) supported via RPC

## Remaining work
- Write vendor profile markdown
- Write 84-row CSV
- Append BibTeX citations
- Append agents.md row

## Citations gathered

| Key | URL |
|-----|-----|
| delinea-ss-docs-2025 | https://docs.delinea.com/online-help/secret-server/start.htm |
| delinea-ss-discovery-2025 | https://docs.delinea.com/online-help/secret-server/discovery/index.htm |
| delinea-ss-auth-2025 | https://docs.delinea.com/online-help/secret-server/authentication/index.htm |
| delinea-ss-security-2025 | https://docs.delinea.com/online-help/secret-server/security-hardening/index.htm |
| delinea-ss-api-2025 | https://docs.delinea.com/online-help/secret-server/api-scripting/index.htm |
| delinea-ss-features-2025 | https://delinea.com/products/secret-server/features |
| delinea-ss-product-2025 | https://delinea.com/products/secret-server |
| delinea-pm-product-2025 | https://delinea.com/products/privilege-manager |
| delinea-home-2025 | https://delinea.com/ |
| delinea-ss-admin-2025 | https://docs.delinea.com/online-help/secret-server/admin/index.htm |

## Continuation instructions

If a successor is needed:
- Re-read this checkpoint file first
- Output paths:
  - `research/vendors/delinea-secret-server.md`
  - `matrix/vendor-capabilities-delinea-secret-server.csv`
  - Append to `meta/citations.bib` under `## Delinea Secret Server (Agent 03 wave 1)`
  - Append one row to `meta/agents.md`
- All NHI and UC IDs confirmed: NHI-001 to NHI-037, UC-F-001 to UC-F-027, UC-N-001 to UC-N-020

<!-- CHECKPOINT-001 pre-write; all outputs being written in same turn -->

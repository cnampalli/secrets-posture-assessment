# Appendix B — Vendor profiles index

**Status:** v0.1 (Wave B — 2026-05-23).
**Parent document:** [`PRD-FI-v0.1.md`](../PRD-FI-v0.1.md) §11 + §19.
**Scope:** one paragraph per vendor across the 19-vendor shortlist
([ADR-004](../adrs/ADR-004-vendor-shortlist.md)) with tier, canonical
URL, capability headline, top-3 strengths and top-3 gaps, and links to
the full profile under [`research/vendors/`](../../research/vendors/)
and the per-vendor capability CSV under
[`matrix/`](../../matrix/). Headlines are drawn from each profile's
§1 snapshot and §5 strengths-and-gaps. Sensitivity tagging per
[ADR-005](../adrs/ADR-005-anz-evidence-policy.md): XYZ lived-experience
signals are paraphrased and attributed to "a major AU Tier-1 FI".

---

## B.1 Core tier (vault-class)

> **Layer 1 — Secrets management.** `NATIVE` here = *brokers / stores /
> rotates secrets* for the identity. (Stack model: [ADR-007](../adrs/ADR-007-reading-model-and-confidence.md).)

### HashiCorp Vault Enterprise — core
- **URL:** <https://developer.hashicorp.com/vault>
- **Capability headline:** broadest NATIVE NHI coverage in the matrix
  (26/37) + broadest UC-F NATIVE (17/27); plugin-modular auth and
  secrets engines; FIPS 140-3 builds; HSM PKCS#11 unseal. The lived
  reality at a major AU Tier-1 FI is **system of record, not day-to-day
  operational vault** (cloud-native vault drift since 2020).
- **Top strengths:** (1) API maturity + plugin breadth — AppRole, K8s,
  AWS IAM and dynamic-DB engines are reference-grade; (2) PKI +
  SPIFFE-SVID issuance + Consul Connect; (3) Performance / DR
  Replication + PKCS#11 unseal + Leidos-attested FIPS 140-3 v1.19.4+.
- **Top gaps:** (1) no secret-scanning / sprawl detection (UC-F-001,
  UC-F-002, UC-N-001); (2) Azure auth method under-adopted; (3)
  licensing complexity at scale — non-prod and prod separately
  licensed, model has changed 2–3 times in six years.
- **Profile:** [hashicorp-vault-enterprise.md](../../research/vendors/hashicorp-vault-enterprise.md).
- **Capabilities CSV:** [vendor-capabilities-hashicorp-vault-enterprise.csv](../../matrix/vendor-capabilities-hashicorp-vault-enterprise.csv).

### CyberArk Conjur — core
- **URL:** <https://www.conjur.org/> + <https://www.cyberark.com/products/secrets-manager/>
- **Capability headline:** strongest **cloud-native authenticator
  breadth** in the core tier (AWS IAM, Azure, GCP, K8s, OIDC/JWT, LDAP)
  with PAM-ecosystem integration via Secrets Hub / Vault Synchronizer
  to native cloud vaults. CyberArk holds IRAP Protected for its
  Identity Security platform.
- **Top strengths:** (1) GA authenticator breadth incl. authn-k8s
  (sidecar + init-container); (2) hybrid PAM↔Conjur sync (EPV ↔
  Conjur ↔ cloud-native vaults) — decisive for a major AU Tier-1 FI
  legacy estate; (3) horizontal Follower scale with selective replication
  (Conjur Cloud India region 2025).
- **Top gaps:** (1) no native PKI / cert-lifecycle engine (separate
  Venafi/CyberArk MIS product); (2) no secrets-sprawl detection or
  discovery; (3) thin out-of-box audit / KPI dashboarding.
- **Profile:** [cyberark-conjur.md](../../research/vendors/cyberark-conjur.md).
- **Capabilities CSV:** [vendor-capabilities-cyberark-conjur.csv](../../matrix/vendor-capabilities-cyberark-conjur.csv).

### CyberArk PAM — core
- **URL:** <https://www.cyberark.com/products/privileged-access-manager/>
- **Capability headline:** Tier-1 PAM incumbent — industry-leading AD
  service-account governance via CPM; **the entrenched legacy lane** at
  the FI for `svc_` rotation after a prior Vault attempt was rolled
  back. National Australia Bank is a documented customer; Privilege
  Cloud runs in AWS Sydney (IRAP pending).
- **Top strengths:** (1) AD service-account rotation depth (250+
  platform plug-ins; dependency mapping across Windows services / IIS
  app pools / scheduled tasks); (2) PSM session isolation + tamper-
  resistant audit (CPS 234 / PCI-DSS aligned); (3) breadth of legacy /
  hybrid platform coverage (Unix, mainframe z/OS, AS/400, network
  devices, RPA).
- **Top gaps:** (1) no cloud-native ephemeral / OIDC JIT / SPIFFE /
  dynamic DB; (2) no K8s auth or CSI driver; (3) no developer-tooling
  (secret scanning, SLSA, OAuth-app governance).
- **Profile:** [cyberark-pam.md](../../research/vendors/cyberark-pam.md).
- **Capabilities CSV:** [vendor-capabilities-cyberark-pam.csv](../../matrix/vendor-capabilities-cyberark-pam.csv).

### Delinea Secret Server — core
- **URL:** <https://delinea.com/products/secret-server>
- **Capability headline:** mid-market PAM positioned between Vault and
  CyberArk; strongest **ease-of-use + time-to-value** in the core tier;
  Windows + MS SQL self-hosted or SaaS (US/EU only). Adjacent products
  DevOps Secrets Vault (DSV), Privilege Manager and acquired StrongDM
  extend the platform.
- **Top strengths:** (1) AD / Windows service-account discovery +
  gMSA + heartbeat-driven dependency mapping; (2) low-friction UX
  (150+ secret templates, GUI discovery wizard); (3) static long-lived
  secret rotation incl. NATIVE network-device coverage (Cisco / F5 /
  Juniper).
- **Top gaps:** (1) no dynamic / ephemeral creds (no Vault-equivalent
  engine); (2) no K8s CSI / OIDC federation / Terraform provider; (3)
  no mainframe / FAPI 2.0 / PQC roadmap.
- **Profile:** [delinea-secret-server.md](../../research/vendors/delinea-secret-server.md).
- **Capabilities CSV:** [vendor-capabilities-delinea-secret-server.csv](../../matrix/vendor-capabilities-delinea-secret-server.csv).

---

## B.2 Cloud-native tier

> **Layer 1 — Secrets management.** `NATIVE` here = *brokers / stores /
> rotates secrets* for the identity.

### AWS Secrets Manager — cloud-native
- **URL:** <https://aws.amazon.com/secrets-manager/>
- **Capability headline:** **unmatched AWS-native depth** (IRSA, OIDC
  GitHub Actions, managed RDS/Aurora/Redshift/DocumentDB rotation
  without Lambda); IRAP PROTECTED, ap-southeast-2 Sydney GA. Top tier
  for AU sovereignty assurance.
- **Top strengths:** (1) AWS-native first-class integration across
  IAM / EKS-IRSA / OIDC CI/CD / managed DB rotation; (2) KMS + CloudHSM
  + XKS envelope encryption with `kms:ViaService` lockdown; (3) IRAP
  PROTECTED (Nov 2025); CloudTrail + Security Hub for CPS 234 evidence.
- **Top gaps:** (1) single-cloud lock-in (no Azure/GCP/on-prem reach);
  (2) no SPIFFE / SVID / workload-attestation; (3) long-tail NHI gaps
  (mainframe, AD/gMSA beyond storage, FAPI 2.0, RPA, SLSA / signing).
- **Profile:** [aws-secrets-manager.md](../../research/vendors/aws-secrets-manager.md).
- **Capabilities CSV:** [vendor-capabilities-aws-secrets-manager.csv](../../matrix/vendor-capabilities-aws-secrets-manager.csv).

### Azure Key Vault — cloud-native
- **URL:** <https://learn.microsoft.com/azure/key-vault/>
- **Capability headline:** deepest Azure-native integration + FIPS
  140-3 Level 3 at both Premium and Managed HSM tiers; Entra Workload
  ID + OIDC Federation as the strongest cloud-native K8s pattern; AU
  East + Southeast + Central regions all GA; IRAP PROTECTED.
- **Top strengths:** (1) Azure-native breadth (Managed Identity, RBAC,
  Event Grid, APIM, AKS CSI, SQL TDE CMK); (2) FIPS 140-3 L3 across
  Premium + Managed HSM (Shamir M-of-N domain, Intel SGX TEE-backed
  ops); (3) Entra Workload ID OIDC federation for AKS — best cloud
  K8s secrets pattern.
- **Top gaps:** (1) no dynamic credential brokering (Vault-style DB
  leases); (2) no SPIFFE / SPIRE native; (3) no mainframe / no FAPI
  2.0 / CDR partner-CA management.
- **Profile:** [azure-key-vault.md](../../research/vendors/azure-key-vault.md).
- **Capabilities CSV:** [vendor-capabilities-azure-key-vault.csv](../../matrix/vendor-capabilities-azure-key-vault.csv).

### GCP Secret Manager — cloud-native
- **URL:** <https://cloud.google.com/secret-manager>
- **Capability headline:** versioned secrets + CMEK via Cloud KMS /
  HSM / EKM; both AU regions (Sydney + Melbourne) GA; assessed under
  IRAP. Strongest **multi-region replication policy controls** of the
  hyperscale vaults.
- **Top strengths:** (1) GCP-native IAM + GKE Workload Identity +
  Workload Identity Federation for OIDC CI/CD; (2) Cloud KMS / HSM /
  EKM coverage including externally-managed key paths; (3) AU regions
  Sydney + Melbourne + IRAP-assessed.
- **Top gaps:** (1) GCP-only reach; (2) no Vault-style dynamic DB
  engines or SPIFFE-native SVID issuance; (3) thin mainframe / RPA /
  IoT coverage — partner toolchain required.
- **Profile:** [gcp-secret-manager.md](../../research/vendors/gcp-secret-manager.md).
- **Capabilities CSV:** [vendor-capabilities-gcp-secret-manager.csv](../../matrix/vendor-capabilities-gcp-secret-manager.csv).

### AKEYLESS — cloud-native
- **URL:** <https://www.akeyless.io/>
- **Capability headline:** SaaS-first **Distributed Fragments
  Cryptography (DFC)** zero-knowledge architecture; Vault-proxy
  compatibility layer for migration. **21 NATIVE NHIs** —
  hyperscaler-competitive — but **no AU SaaS region**; AU customers
  must self-host the Gateway. No publicly named AU FI customers.
- **Top strengths:** (1) DFC — keys never reconstructed on any single
  server, including Akeyless infra (FIPS 140-3 cert #5227); (2)
  broadest SaaS-native multi-cloud dynamic-secrets coverage; (3) AI-
  agent / MCP / Agentic Runtime Authority shipping ahead of most
  competitors.
- **Top gaps:** (1) no AU/AP SaaS region; no IRAP; (2) no mainframe
  integration (NHI-022); (3) NHI inventory / orphan discovery in
  early access only.
- **Profile:** [akeyless.md](../../research/vendors/akeyless.md).
- **Capabilities CSV:** [vendor-capabilities-akeyless.csv](../../matrix/vendor-capabilities-akeyless.csv).

---

## B.3 Emerging tier

> **Layer 1 — Secrets management.** `NATIVE` here = *brokers / stores /
> rotates secrets* for the identity.

### Doppler — emerging
- **URL:** <https://www.doppler.com/>
- **Capability headline:** developer-first SaaS (GCP us-central1 only);
  CLI-first environment-variable model + 30+ sync integrations + early
  MCP server. **AU residency disqualifies for APRA-regulated
  production.** No publicly named AU FI customers.
- **Top strengths:** (1) developer-experience and 30+ multi-environment
  sync integrations; (2) early MCP-server AI-agent brokering
  (NHI-019 / UC-F-018); (3) OIDC workload identity for CI/CD and K8s.
- **Top gaps:** (1) AU sovereignty — no AU region, no self-host, no
  IRAP (disqualifying); (2) no PKI / SPIFFE / code-signing / CA; (3)
  no on-prem / legacy / mainframe coverage.
- **Profile:** [doppler.md](../../research/vendors/doppler.md).
- **Capabilities CSV:** [vendor-capabilities-doppler.csv](../../matrix/vendor-capabilities-doppler.csv).

### Infisical — emerging
- **URL:** <https://infisical.com/>
- **Capability headline:** open-source-first (MIT core) — secrets +
  dynamic + PKI + SSH CA + KMS + HSM in a single platform; broadest
  built-in scope of any emerging vendor. **Self-host is the AU-
  sovereign path** (Cloud is US/EU only).
- **Top strengths:** (1) broadest built-in scope from a single
  codebase (secrets, PKI, KMS, SSH CA, HSM); (2) MIT-licensed core +
  Helm self-host with external Postgres/Redis — APRA CPS 230-friendly;
  (3) PQC roadmap in the PKI CA ahead of peers.
- **Top gaps:** (1) no AU SaaS region; (2) weak enterprise governance
  (no orphan/dormancy cleanup, exception register, SLSA attestation);
  (3) no mainframe; SPIFFE only via SPIRE pairing.
- **Profile:** [infisical.md](../../research/vendors/infisical.md).
- **Capabilities CSV:** [vendor-capabilities-infisical.csv](../../matrix/vendor-capabilities-infisical.csv).

### 1Password Secrets Automation — emerging
- **URL:** <https://1password.com/developers/secrets-automation>
- **Capability headline:** developer-secrets product layered onto the
  consumer 1Password vault; Service Accounts + Connect Server + CLI /
  Operator / Injector; 2026 MCP-server launch. **AU residency only via
  self-hosted Connect Server**; no IRAP; not recommended as primary.
- **Top strengths:** (1) developer-experience for static-secret
  injection (`op://` references, `op run`, Terraform provider, SDKs);
  (2) K8s Operator + Secrets Injector (mutating webhook); (3) emerging
  MCP / agent hooks for NHI-019.
- **Top gaps:** (1) no dynamic-secrets engine (CPS 234 §28a blocker);
  (2) no PKI / cert lifecycle / CA; (3) no AU SaaS region, no IRAP,
  no ISO 27001 certificate, no CPS 230/234 data-flow evidence.
- **Profile:** [1password-secrets-automation.md](../../research/vendors/1password-secrets-automation.md).
- **Capabilities CSV:** [vendor-capabilities-1password-secrets-automation.csv](../../matrix/vendor-capabilities-1password-secrets-automation.csv).

---

## B.4 PKI / MIM tier

> **Layer 1 — Secrets management, distinct cert/key-lifecycle sub-lane.**
> These govern certificates and keys, not application secrets. High GAP
> counts against the secrets-broker rubric are *expected* — judge them on
> PKI/MIM rows, not vault rows.

### Venafi (CyberArk Machine Identity Security) — pki-mim
- **URL:** <https://www.cyberark.com/products/machine-identity-security/>
- **Capability headline:** market-defining certificate-lifecycle
  platform — acquired by CyberArk Oct 2024 and rebranded under
  Machine Identity Security; Certificate Manager + SSH Manager + Code
  Sign Manager + Workload Identity Manager (formerly Firefly,
  SPIFFE-compatible) + Zero Touch PKI; covers 47-day cert-lifespan
  automation.
- **Top strengths:** (1) certificate lifecycle at FI scale — 12+ CAs,
  200+ machine integrations; (2) HSM-backed code-signing as a
  service with native CI/CD integration; (3) SPIFFE-compatible
  workload-identity issuance via Firefly / Workload Identity Manager.
- **Top gaps:** (1) not a general secrets vault — NHI-001..005 / 007 /
  008 / 012 explicitly out of scope; (2) AU SaaS sovereignty / IRAP
  unconfirmed; (3) no AI / TEE / mainframe lanes (NHI-018, NHI-019,
  NHI-020, NHI-022, NHI-035).
- **Profile:** [venafi.md](../../research/vendors/venafi.md).
- **Capabilities CSV:** No per-vendor CSV; rows present in
  [`matrix/vendor-capabilities.csv`](../../matrix/vendor-capabilities.csv).

### Keyfactor — pki-mim
- **URL:** <https://www.keyfactor.com/>
- **Capability headline:** **owns the full PKI stack** — Keyfactor
  Command (lifecycle) + EJBCA Enterprise (CA) + SignServer Enterprise
  (signing) + Bouncy Castle (FIPS-certified crypto library). **PQC
  leader** — composite ML-DSA + classical hybrid certs GA today.
- **Top strengths:** (1) full PKI stack ownership in one vendor;
  industry-leading IoT (SCEP / EST / CMP); (2) PQC leadership —
  EJBCA composite cert issuance GA; (3) certificate lifecycle at
  scale (discovery, ACME orchestration, policy-driven auto-renew).
- **Top gaps:** (1) not a general secrets vault (NHI-001..008 are
  GAP); (2) no SPIFFE / SPIRE native — EJBCA-as-CA only; (3) AU data
  residency / IRAP unclear (EJBCA SaaS on AWS / Azure, no AU
  confirmation).
- **Profile:** [keyfactor.md](../../research/vendors/keyfactor.md).
- **Capabilities CSV:** [vendor-capabilities-keyfactor.csv](../../matrix/vendor-capabilities-keyfactor.csv).

---

## B.5 NHI-discovery tier

> **Layer 2 — NHI discovery / governance (above the vault).** `NATIVE`
> here = *discovers / inventories / governs* the identity — **not**
> brokers its secrets. These are complementary to the vault tier, not
> competitors. Do not compare a discovery `NATIVE` against a vault
> `NATIVE`. (Stack model: [ADR-007](../adrs/ADR-007-reading-model-and-confidence.md).)
>
> **Tier-wide constraint (per PRD §11 F-V-5):** all five vendors below
> are SaaS-only with **no AU region across the tier** and **no IRAP
> assessment**. They are positioned in PRD §16 R1 as an
> **observability / inventory control-plane above existing vaults**,
> not as primary platforms for APRA-regulated production.

### Astrix Security — nhi-discovery
- **URL:** <https://astrix.security/>
- **Capability headline:** SaaS-only NHI security platform — OAuth
  app and AI-agent posture, four-method agentless discovery across
  20+ SaaS connectors. **Cisco intent-to-acquire announced 2026-05-04
  (deal pending close)** — to integrate into Cisco Identity
  Intelligence / Secure Access / Duo / Splunk.
- **Top strengths:** (1) NHI discovery breadth across SaaS/cloud (the
  Workday third-party prevention case study); (2) Agent Control Plane
  + policies for NHI-019 (OpenAI / Bedrock / Vertex / Agentforce /
  MCP); (3) continuous third-party / OAuth supply-chain risk scoring.
- **Top gaps:** (1) no secrets brokering / dynamic-credential issuance
  (must partner with Vault / AWS SM / Conjur); (2) no AU residency,
  no IRAP; (3) no PKI / mTLS / mainframe / IoT coverage.
- **Profile:** [astrix-security.md](../../research/vendors/astrix-security.md).
- **Capabilities CSV:** [vendor-capabilities-astrix-security.csv](../../matrix/vendor-capabilities-astrix-security.csv).

### Entro Security — nhi-discovery
- **URL:** <https://entro.security/>
- **Capability headline:** secret-lineage and NHI context — ContextIQ™
  traces every secret from creation through storage to runtime across
  1,200+ secret types / 50+ integrations. NHIDR™ adds behavioural
  anomaly detection. M&A offer reported Apr 2025 (acquirer
  unconfirmed).
- **Top strengths:** (1) secret-lineage / ContextIQ depth — "who
  created, where stored, what uses" is market-differentiated; (2)
  broadest NHI discovery in this tier (16 NATIVE NHIs); SaaS OAuth +
  cloud IAM + AI agents; (3) AI-agent governance (dedicated agentic
  AI pillar + NHIDR™).
- **Top gaps:** (1) no credential issuance / dynamic generation —
  discovery + governance only; (2) no AU residency; SaaS-only; no
  IRAP; (3) no PKI / mainframe / IoT / network-device coverage
  (NHI-006, 015–018, 021–025, 032–034 GAP).
- **Profile:** [entro-security.md](../../research/vendors/entro-security.md).
- **Capabilities CSV:** [vendor-capabilities-entro-security.csv](../../matrix/vendor-capabilities-entro-security.csv).

### Oasis Security — nhi-discovery
- **URL:** <https://www.oasis.security/>
- **Capability headline:** full NHI lifecycle + dedicated **Agentic
  Access Management (AAM™)** layer for AI agents (GA Nov 2025); $120M
  Series B (Mar 2026, Craft Ventures lead). NHI Scout (ITDR, Jan
  2025) with AuthPrint™ behavioural fingerprinting.
- **Top strengths:** (1) AAM™ for AI-agent NHI-019 — per-session
  ephemeral identity + intent-based policy + full audit chain
  (industry-leading Maturity 4); (2) NHI discovery + ownership
  attribution (cloud IAM, AD agent + agentless, SaaS, git, vaults,
  data platforms); (3) NHI Scout ITDR — high-fidelity threat
  detection + public NHI Threat Center.
- **Top gaps:** (1) AU sovereignty / IRAP — material blocker for
  APRA-regulated deployments; (2) no vault-class secrets brokering /
  SVID / DB-lease issuance — orchestrates against existing vaults;
  (3) infrastructure perimeter NHIs (mainframe, network, IoT, mesh,
  TEE, code-signing) are GAP.
- **Profile:** [oasis-security.md](../../research/vendors/oasis-security.md).
- **Capabilities CSV:** [vendor-capabilities-oasis-security.csv](../../matrix/vendor-capabilities-oasis-security.csv).

### Aembit — nhi-discovery
- **URL:** <https://aembit.io/>
- **Capability headline:** **Workload Identity and Access Management
  (WIAM)** broker — Aembit Edge attests workloads via 13 trust-provider
  types and injects short-lived JIT credentials. **Blended Identity +
  MCP Identity Gateway GA at RSA Apr 2026.** SOC 2 Type II + ISO
  27001:2022; no IRAP; SaaS-only control plane.
- **Top strengths:** (1) industry-leading workload attestation + JIT
  brokering (NHI-036, UC-F-003/004/005) — Snowflake case study cites
  85% credential-workload reduction; (2) AI-agent identity — Blended
  Identity (agent + human binding) + MCP Identity Gateway with OAuth
  2.1 token exchange (no agent-side secret exposure); (3) conditional
  access with real-time CrowdStrike Falcon + Wiz posture signals.
- **Top gaps:** (1) no secrets discovery / scanning / inventory —
  must pair with Oasis / Entro / Astrix; (2) AU sovereignty / IRAP
  blocker — SaaS-only control plane; (3) narrow long-tail (mainframe,
  IoT/OT, backup agents, network devices, RPA, message brokers all
  GAP).
- **Profile:** [aembit.md](../../research/vendors/aembit.md).
- **Capabilities CSV:** [vendor-capabilities-aembit.csv](../../matrix/vendor-capabilities-aembit.csv).

### Clutch Security — nhi-discovery
- **URL:** <https://www.clutch.security/>
- **Capability headline:** "Universal Non-Human Identity Security
  Platform" built on the **Identity Lineage® Graph**; agentless SaaS
  with zero-knowledge architecture. **Shadow AI / MCP discovery GA
  Aug 2025** + Universal NHI MCP Server.
- **Top strengths:** (1) Identity Lineage® Graph — contextual NHI
  inventory mapping origin / owner / storage / consumers / resources
  across 100+ platforms; (2) shadow MCP discovery + Agentic AI
  Governance — first-mover on NHI-019 unsanctioned-server discovery;
  (3) Zero Trust NHI philosophy — ephemeral credentials + behaviour
  analytics + blast-radius risk scoring.
- **Top gaps:** (1) AU sovereignty / IRAP — material blocker; (2)
  secrets brokering / rotation deliberately out of scope — partner
  with Vault / CyberArk / AWS SM; (3) legacy / infrastructure
  long-tail out of scope (mainframe, network, IoT/OT, PKI/HSM,
  brokers, code-signing).
- **Profile:** [clutch-security.md](../../research/vendors/clutch-security.md).
- **Capabilities CSV:** [vendor-capabilities-clutch-security.csv](../../matrix/vendor-capabilities-clutch-security.csv).

---

## B.6 Layer-0 crypto-substrate dependency (NOT a ranked vendor)

> **This is a dependency, not part of the 18-vendor ranking** (per
> [ADR-007](../adrs/ADR-007-reading-model-and-confidence.md)). The vault
> must be unsealed / key-rooted by an HSM substrate beneath it; you *pair*
> one with the vault, you don't *shortlist* it against the vault. Fortanix
> is **not a secrets manager** — scoring it on the secrets rubric would GAP
> ~21/37 NHIs by design. The profile below is retained as **reference for
> XYZ's Thales SafeNet → Fortanix substrate decision** (Task 0 §D);
> evaluate it as crypto infrastructure (FIPS 140-3, IRAP, PQC, vault
> integration), not against vaults. PRD cross-ref: §9.x.

### Fortanix DSM — data-security
- **URL:** <https://www.fortanix.com/platform/data-security-manager>
- **Capability headline:** the **crypto root below the vault tier** —
  unified HSM-as-a-service + KMS + tokenisation + secrets management.
  A major AU Tier-1 FI recently migrated its Vault unseal from Thales
  SafeNet Luna to Fortanix DSM (paraphrased per ADR-005). FIPS 140-2
  L3 hardware. **PQC Central (Jun 2025)** is the only dedicated PQC
  dashboard in the matrix. IRAP unconfirmed (PRD §17 O9).
- **Top strengths:** (1) HSM / KMS root-of-trust for vault platforms
  (NHI-035, UC-F-026, UC-N-010) — PKCS#11 / KMIP / REST, FIPS 140-2
  L3, M-of-N quorum; (2) cross-cloud BYOK / EKM (AWS XKS, Azure KV
  BYOK, GCP Cloud EKM) — single FIPS-compliant control plane; (3)
  TEE attestation-gated key release (CCM SKR across SGX/TDX/SEV-
  SNP/Nitro) + PQC Central inventory and migration tracking.
- **Top gaps:** (1) no secrets-vault capability — must pair with
  Vault Enterprise or other vault platform; (2) IRAP and FedRAMP not
  confirmed; (3) weak application-identity NHIs (no SPIFFE / SPIRE,
  no AI-agent broker, no CI/CD OIDC).
- **Profile:** [fortanix-dsm.md](../../research/vendors/fortanix-dsm.md).
- **Capabilities CSV:** [vendor-capabilities-fortanix-dsm.csv](../../matrix/vendor-capabilities-fortanix-dsm.csv).

---

## B.7 Reading guide

Three orthogonal lookups are supported:

- **By UC × NHI cell** — start from the interactive report
  [`matrix/matrix-viewer.html`](../../matrix/matrix-viewer.html)
  (dashboard + decision cards + a browse-all table over the 18 ranked
  vendors / 1,512 rows) or the aggregate CSV
  [`matrix/vendor-capabilities.csv`](../../matrix/vendor-capabilities.csv)
  (1,596 rows including the Fortanix substrate reference).
- **By vendor narrative + citations** — open the linked
  `research/vendors/<slug>.md` profile.
- **By regulatory control** — see
  [Appendix A](./A-compliance-traceability.md) +
  [`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv)
  (145 control rows joining UC ↔ NHI ↔ framework).

PRD §11 (vendor findings) is the narrative front door for §B.1–§B.6
above; PRD §10 (XYZ current-state) is the dual view for the FI lived-
experience overlay. PRD §16 recommendations cite vendors by slug; this
appendix is the resolution layer for those citations.

---

> _End of Appendix B (Wave B v0.1)._

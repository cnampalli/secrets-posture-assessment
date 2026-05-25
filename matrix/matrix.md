# Vendor Capability Matrix — Cross-Vendor Summary

> **19 vendors × 37 NHIs × 47 UCs = 1,596 capability rows** assembled from
> per-vendor sub-agent profiles, joined into [`vendor-capabilities.csv`](./vendor-capabilities.csv).
> For row-level filterable view see [`matrix-viewer.html`](./matrix-viewer.html).
> For per-vendor narrative see [`../research/vendors/`](../research/vendors/).

**Scoring rubric (per ADR-006):**

- **Coverage:** `NATIVE` / `ADD-ON` / `PARTNER` / `GAP` / `N/A`.
- **Maturity:** 0 (none) → 4 (industry-leading).

---

## 0. The three-layer stack — read this first

These are **not one competitive set**. The **18 ranked vendors** occupy
**two comparison layers**; beneath them sits a **Layer-0 crypto-substrate
dependency** that is *not ranked* (you pair one with the vault, you don't
shortlist it against the vault). **Rank within a layer; compose across
layers.** (Rationale: [ADR-007](../PRD/adrs/ADR-007-reading-model-and-confidence.md).)

| Layer | Position | `NATIVE` means | Vendors |
|---|---|---|---|
| **L2 — Discovery / governance** | above the vault | *discovers / inventories / governs* this identity | Astrix, Entro, Oasis, Aembit, Clutch (5) |
| **L1 — Secrets management** (this PRD) | the vault tier | *brokers / stores / rotates secrets for* this identity | Vault, Conjur, CyberArk PAM, Delinea, AWS, Azure, GCP, AKEYLESS, Doppler, Infisical, 1Password; PKI/MIM lane: Venafi, Keyfactor (13) |
| **L0 — Crypto substrate** *(dependency, not ranked)* | below the vault | *provides the HSM / key-root / BYOK* the vault needs | e.g. Fortanix DSM, Thales — see §1.x |

A discovery tool's `NATIVE` (it *finds* the identity) is not comparable to
a vault's `NATIVE` (it *brokers secrets* for it). The §1 tables below are
grouped by layer — do **not** read them as a single league table. The
Layer-0 substrate is a separate infrastructure decision (§1.x), excluded
from the 18-vendor ranking per ADR-007.

---

## 1. NHI coverage by layer (37 NHIs)

### Layer 1 — Secrets management (the apples-to-apples comparison)

Ranked by `NATIVE` count *within the secrets-management layer*:

| Rank | Vendor | Tier | NATIVE | ADD-ON | PARTNER | GAP | N/A |
|---|---|---|---|---|---|---|---|
| 1 | **HashiCorp Vault Enterprise** | core | **26** | 6 | 1 | 4 | 0 |
| 2 | AKEYLESS | cloud-native | 21 | 11 | 0 | 5 | 0 |
| 3 | Azure Key Vault | cloud-native | 18 | 14 | 1 | 4 | 0 |
| 4 | GCP Secret Manager | cloud-native | 17 | 12 | 0 | 8 | 0 |
| 5 | AWS Secrets Manager | cloud-native | 16 | 14 | 0 | 7 | 0 |
| 6 | Delinea Secret Server | core | 14 | 14 | 1 | 8 | 0 |
| 7 | CyberArk Conjur | core | 13 | 13 | 3 | 8 | 0 |
| 7 | Infisical | emerging | 13 | 19 | 0 | 5 | 0 |
| 9 | CyberArk PAM | core | 10 | 10 | 3 | 14 | 0 |
| 10 | Doppler | emerging | 9 | 10 | 0 | 18 | 0 |
| 11 | 1Password Secrets Auto | emerging | 7 | 14 | 0 | 16 | 0 |

**PKI / MIM sub-lane** (distinct discipline — certificate & key lifecycle,
*not* secrets brokering; high GAP vs the secrets-broker rubric is expected):

| Vendor | Tier | NATIVE | ADD-ON | PARTNER | GAP | N/A |
|---|---|---|---|---|---|---|
| Keyfactor | pki-mim | 9 | 12 | 0 | 16 | 0 |
| Venafi (CyberArk) | pki-mim | 8 | 9 | 0 | 20 | 0 |

### §1.x Layer-0 crypto-substrate dependency (NOT ranked)

The vault must be unsealed and key-rooted by an HSM / key-management
substrate beneath it. This is a **dependency, not a vendor choice in this
comparison** — so it is **excluded from the 18-vendor ranking** (ADR-007).
Scoring an HSM on a secrets rubric is a category error: it would GAP ~21/37
NHIs by design because it never brokers application secrets.

XYZ's substrate decision is the **Thales SafeNet Luna → Fortanix DSM** HSM
migration (Task 0 §D). Evaluate it as **crypto infrastructure** on its own
criteria — FIPS 140-3 level, IRAP / AU region, PQC roadmap, vault
integration (PKCS#11 auto-unseal, BYOK/EKM) — not against vaults. Its full
profile is retained for reference in
[`../research/vendors/fortanix-dsm.md`](../research/vendors/fortanix-dsm.md)
and [Appendix B §B.6](../PRD/appendices/B-vendor-profiles-index.md); the
per-vendor CSV still carries its 84 cells as substrate reference.

### Layer 2 — NHI discovery / governance (ranked within tier)

`NATIVE` here = *discovers / governs* the identity, **not** brokers its
secrets. These tools sit **above** the vault as a control-plane:

| Rank | Vendor | NATIVE | ADD-ON | PARTNER | GAP | N/A |
|---|---|---|---|---|---|---|
| 1 | Entro Security | 16 | 8 | 1 | 12 | 0 |
| 2 | Astrix Security | 13 | 9 | 0 | 15 | 0 |
| 2 | Clutch Security | 13 | 7 | 0 | 17 | 0 |
| 4 | Oasis Security | 11 | 10 | 3 | 13 | 0 |
| 5 | Aembit | 10 | 6 | 0 | 21 | 0 |

> SaaS-only, **no AU region / IRAP across the tier** (§4) — material for
> APRA-regulated production. Positioned in PRD §16 as inventory /
> observability above existing vaults, not as primary secrets platforms.

---

## 2. Vendor capability headline — UC coverage (27 functional + 20 non-functional = 47 UCs)

| Vendor | UC-F: NATIVE / ADD-ON / GAP | UC-N: NATIVE / ADD-ON / GAP |
|---|---|---|
| HashiCorp Vault Enterprise | **17** / 6 / 3 | 4 / 8 / 5 |
| Delinea Secret Server | 12 / 8 / 5 | **8** / 6 / 4 |
| Azure Key Vault | 12 / 10 / 4 | 5 / 9 / 2 |
| AKEYLESS | 14 / 9 / 4 | 5 / 8 / 5 |
| AWS Secrets Manager | 13 / 6 / 8 | 7 / 7 / 4 |
| GCP Secret Manager | 12 / 10 / 5 | 6 / 9 / 5 |
| CyberArk Conjur | 10 / 10 / 6 | 2 / 9 / 7 |
| CyberArk PAM | 9 / 8 / 7 | 7 / 4 / 5 |
| Infisical | 10 / 14 / 3 | 2 / 11 / 5 |
| Astrix Security | 7 / 8 / 11 | 7 / 4 / 9 |
| Aembit | 7 / 5 / 15 | 1 / 5 / 14 |
| Oasis Security | 6 / 7 / 12 | 6 / 6 / 8 |
| Entro Security | 6 / 11 / 10 | 6 / 5 / 9 |
| Clutch Security | 6 / 8 / 13 | 5 / 7 / 7 |
| Venafi (CyberArk) | 8 / 3 / 16 | 4 / 9 / 7 |
| Keyfactor | 7 / 7 / 13 | 5 / 7 / 8 |
| Doppler | 7 / 8 / 12 | 0 / 9 / 11 |
| 1Password Secrets Auto | 4 / 13 / 10 | 1 / 11 / 8 |

> *(Fortanix DSM excluded from this ranking — Layer-0 substrate dependency, §1.x.)*

> **Headline:** Vault Enterprise has the broadest functional-UC NATIVE coverage
> (17/27). Delinea leads on non-functional UCs (8/20). CyberArk PAM is uniquely
> strong on UC-N privileged-access governance lanes but weaker on functional /
> developer-facing UCs (consistent with its category: privileged-access platform
> rather than secrets-management platform).

---

## 3. Tier-by-tier read

| Layer | Tier | Vendors | Strongest at | Weakest at |
|---|---|---|---|---|
| **L1** | **core** (vault-class) | Vault Ent, Conjur, PAM, Delinea | Broad NHI coverage; dynamic creds; HSM integration | AI agent identity; supply-chain signing; NHI inventory |
| **L1** | **cloud-native** | AWS SM, Azure KV, GCP SM, AKEYLESS | Native cloud-IAM integration; HSM-backed encryption | Multi-cloud reach; mainframe; SPIFFE; FAPI 2.0 |
| **L1** | **emerging** | Doppler, Infisical, 1Password Secrets Auto | Developer DX; modern APIs | AU residency (no IRAP); enterprise governance |
| **L1** | **pki-mim** (distinct cert/key lane) | Venafi, Keyfactor | Cert lifecycle; code-signing; PQC (Keyfactor leading) | Generic secrets-vault use cases — *different discipline* |
| **L2** | **nhi-discovery** (above the vault) | Astrix, Entro, Oasis, Aembit, Clutch | NHI inventory; posture; AI agent identity (Oasis + Clutch); workload attestation (Aembit) | Secrets brokering / rotation (*by design — not their job*); AU residency (no IRAP across tier) |
| **L0** *(dependency, not ranked — §1.x)* | **data-security** (below the vault) | Fortanix DSM (XYZ substrate) | Crypto root (HSM, TEE, BYOK/EKM, PQC); key-roots the vault | Not a secrets vault — evaluate as infrastructure, not against vaults |

---

## 4. AU residency / IRAP status snapshot

| Vendor | AU region | IRAP PROTECTED |
|---|---|---|
| HashiCorp Vault Enterprise | self-hosted (anywhere) | Customer responsibility |
| Azure Key Vault | AU East + Southeast + Central | ✓ PROTECTED |
| AWS Secrets Manager | Sydney (ap-southeast-2) | ✓ PROTECTED |
| GCP Secret Manager | Sydney + Melbourne | ✓ Assessed |
| AKEYLESS | Gateway self-host (no SaaS AU) | ✗ |
| CyberArk Conjur | Conjur Cloud (US/EU only at present); on-prem any region | Pending |
| CyberArk PAM | Privilege Cloud — AWS Sydney | Pending |
| Delinea Secret Server | self-hosted; Cloud US/EU only | Pending |
| Doppler | SaaS GCP us-central1 only | ✗ |
| Infisical | self-hosted | Customer responsibility |
| 1Password Secrets Auto | SaaS Connect Server self-host | ✗ |
| Venafi (CyberArk) | TLS Protect Datacenter (on-prem); Cloud regions limited | Unconfirmed |
| Keyfactor | Self-host + SaaS (regions limited) | Unconfirmed |
| Astrix / Entro / Oasis / Aembit / Clutch | SaaS-only — no AU region across tier | ✗ across tier |
| Fortanix DSM | DSM SaaS (limited regions) + on-prem appliance + AU Equinix HSM | Unconfirmed |

> **APRA + CPS 230 sovereignty implication:** all SaaS-only vendors without AU
> regions (5 NHI-discovery + Doppler + 1Password) require explicit data-residency
> contractual commitments or are unsuitable as primary platforms for APRA-regulated
> production workloads. Self-host (Vault, Infisical, on-prem PAM / Delinea) and AU-
> region cloud-native vaults (Azure KV, AWS SM, GCP SM) materially reduce this risk.

---

## 5. AI agent identity (NHI-019) — emerging leadership

A category that didn't exist in the 2019 XYZ red-team and has rapidly emerged
2024-2026. Cross-vendor:

- **Oasis Security** — AAM™ GA Nov 2025 (Maturity 4 — industry-leading).
- **Aembit** — Blended Identity + MCP Gateway GA Apr 2026 (Maturity 4).
- **Clutch Security** — shadow MCP discovery GA Aug 2025 (Maturity 3).
- **Astrix** — OAuth-app risk applied to AI agents (Maturity 2-3).
- **Infisical** — MCP server (preview).
- **Doppler** — MCP server (experimental).
- **HashiCorp Vault, AWS SM, Azure KV, GCP SM** — partial via standard auth methods + cloud-native managed identities for AI services.

> **PRD §16 finding:** the NHI discovery tier currently leads on AI-agent identity
> governance. FI 27 demystification work on ZT workload identity (§J of Task 0)
> should incorporate AI-agent identity as a first-class deliverable.

---

## 6. Where to drill down

- Per-cell view (filterable + sortable): [`matrix-viewer.html`](./matrix-viewer.html).
- Per-vendor profile (narrative + citations): [`../research/vendors/<slug>.md`](../research/vendors/).
- Per-UC vs framework back-map: [`regulatory-trace.csv`](./regulatory-trace.csv) (E8 + CISA ZTMM v2.0 primary; CPS 234 + CPS 230 + CPG 234 + ISM back-map; MITRE ATT&CK adversary lens — 145 control rows).
- Adversary post-mortems mapping: [`../research/adversary/breach-postmortems.md`](../research/adversary/breach-postmortems.md).
- XYZ current-state vs framework: [`anz-current-state.csv`](./anz-current-state.csv) + [`../research/anz-current-state-evidence.md`](../research/anz-current-state-evidence.md).

---

## 7. Per-vendor profile index

| Vendor | Tier | Profile path |
|---|---|---|
| HashiCorp Vault Enterprise | core | [vendors/hashicorp-vault-enterprise.md](../research/vendors/hashicorp-vault-enterprise.md) |
| CyberArk Conjur | core | [vendors/cyberark-conjur.md](../research/vendors/cyberark-conjur.md) |
| CyberArk PAM | core | [vendors/cyberark-pam.md](../research/vendors/cyberark-pam.md) |
| Delinea Secret Server | core | [vendors/delinea-secret-server.md](../research/vendors/delinea-secret-server.md) |
| AWS Secrets Manager | cloud-native | [vendors/aws-secrets-manager.md](../research/vendors/aws-secrets-manager.md) |
| Azure Key Vault | cloud-native | [vendors/azure-key-vault.md](../research/vendors/azure-key-vault.md) |
| GCP Secret Manager | cloud-native | [vendors/gcp-secret-manager.md](../research/vendors/gcp-secret-manager.md) |
| AKEYLESS | cloud-native | [vendors/akeyless.md](../research/vendors/akeyless.md) |
| Doppler | emerging | [vendors/doppler.md](../research/vendors/doppler.md) |
| Infisical | emerging | [vendors/infisical.md](../research/vendors/infisical.md) |
| 1Password Secrets Auto | emerging | [vendors/1password-secrets-automation.md](../research/vendors/1password-secrets-automation.md) |
| Venafi | pki-mim | [vendors/venafi.md](../research/vendors/venafi.md) |
| Keyfactor | pki-mim | [vendors/keyfactor.md](../research/vendors/keyfactor.md) |
| Astrix Security | nhi-discovery | [vendors/astrix-security.md](../research/vendors/astrix-security.md) |
| Entro Security | nhi-discovery | [vendors/entro-security.md](../research/vendors/entro-security.md) |
| Oasis Security | nhi-discovery | [vendors/oasis-security.md](../research/vendors/oasis-security.md) |
| Aembit | nhi-discovery | [vendors/aembit.md](../research/vendors/aembit.md) |
| Clutch Security | nhi-discovery | [vendors/clutch-security.md](../research/vendors/clutch-security.md) |
| Fortanix DSM | data-security | [vendors/fortanix-dsm.md](../research/vendors/fortanix-dsm.md) |

# Task 0 Questionnaire — Your Prior Context

> **Format:** Each question has an **ID** (`Q-X.NN`) you can quote in
> `responses.md`. Most questions have a short multi-select; the free-form
> box is where the real value lives.
>
> **Sensitivity tags** (per ADR-005, see `task0/README.md`):
> `[PUBLIC]` / `[INTERNAL]` / `[SENSITIVE]` / `[NOT-FOR-DISTRIBUTION]`.
>
> **Don't try to be exhaustive.** Anything left blank becomes a PRD §18
> Open Question for the stakeholder. That's a deliberate design — you don't
> need to remember everything.

---

## Section A — Project context & stakeholders

### Q-A.01 — Stakeholder inside XYZ (or wherever the report lands)

Who is the **primary stakeholder** the report is being written for?

- [ ] CISO
- [ ] Head of Identity & Access Management
- [ ] Head of Platform Security / Cloud Security
- [ ] Head of DevSecOps / Engineering Productivity
- [ ] Internal Audit (3LoD)
- [ ] Procurement / Vendor Risk
- [ ] CTO / Chief Architect
- [ ] Other: _________

Free-form (name omitted unless `[PUBLIC]`): the role, team, what they own.

### Q-A.02 — Secondary readers

Who else will read or sign off?
(Tick any.) [ ] CIO  [ ] Board sub-committee  [ ] APRA-facing risk function
[ ] External auditor  [ ] Vendor SE (for RFP)  [ ] Other engineering leaders
[ ] None / unknown

### Q-A.03 — Distribution surface

Where does this PRD ultimately go?

- [ ] Internal to XYZ only
- [ ] XYZ + named external vendor SEs (for RFP)
- [ ] XYZ + APRA / external regulator
- [ ] XYZ + external auditor (e.g., Big-4)
- [ ] Industry forum (anonymised)
- [ ] Don't know yet

### Q-A.04 — Decision the report supports

- [ ] **Re-validate** XYZ's existing secrets-management choice (Vault Ent)
- [ ] **Identify gaps** in the current deployment for remediation
- [ ] **Build a buyer's framework** for future selection (re-platform, expansion)
- [ ] **Audit defence** — show that current state is defensible vs APRA / ISM / CSF
- [ ] **Strategy input** — feed FI 27 (see §J below)
- [ ] Other / combination: _________

### Q-A.05 — FI 27 strategy preview (optional)

Anything you can share right now (even one paragraph) about what **FI 27**
is, what it expects from secrets-management, and what the report should not
contradict?

> _Your text here_ — or "Will share after v0.1 review."

---

## Section B — XYZ organisational context (real where public)

### Q-B.01 — Public anchors we can cite

Anything **public** I should anchor the XYZ narrative on?

- [ ] XYZ's published "Cloud Centre of Excellence" or platform-engineering posts
- [ ] HashiCorp case study referencing XYZ
- [ ] Conference talks (KubeCon AU, AWS re:Invent, HashiConf, RSA APAC, etc.)
- [ ] Public APRA notices or regulatory commentary
- [ ] Other: _________

Drop URLs in the free-form area.

### Q-B.02 — Scale orientation (no real numbers needed)

Coarse-grained scale (order of magnitude):

- [ ] Tens to hundreds of dev teams
- [ ] Hundreds to low-thousands of dev teams
- [ ] Workload count: ~10³ / ~10⁴ / ~10⁵ / ~10⁶ machines & containers (pick)
- [ ] Multi-cloud (AWS / Azure / GCP) — tick the ones in use
- [ ] On-prem + mainframe coexists (Y/N)
- [ ] Significant Kubernetes footprint (Y/N)
- [ ] Significant CI/CD footprint (tooling? Jenkins / GitLab / GitHub Actions / Azure DevOps / Bamboo / Other)

### Q-B.03 — Regulatory pressure observed

Which controls were the most-cited in conversations during your engagement?

- [ ] APRA CPS 234
- [ ] APRA CPS 230 (operational risk)
- [ ] ASD Essential 8 maturity
- [ ] ASD ISM (specific control families — note which if you remember)
- [ ] NIST CSF (1.x or 2.0)
- [ ] PCI-DSS (cardholder data scope)
- [ ] SOX (financial reporting scope)
- [ ] APRA CPG 235 (data risk)
- [ ] AU Privacy Act / OAIC reporting
- [ ] Other: _________

Free-form: which auditor concerns repeatedly surfaced about secrets handling?

---

## Section C — XYZ identity inventory observed (NHI scope)

For each row: tick **Present**, **Suspected**, or **Absent / unknown**, then
optionally note the rough population and where it was stored / governed.

| Identity type | Present | Suspected | Absent/unknown | Population (rough) | Where governed |
|---|---|---|---|---|---|
| AD service accounts | ☐ | ☐ | ☐ | | |
| Domain-joined service accounts (gMSA) | ☐ | ☐ | ☐ | | |
| Local service accounts on Windows | ☐ | ☐ | ☐ | | |
| UNIX/Linux service accounts | ☐ | ☐ | ☐ | | |
| Database service accounts (Oracle, MSSQL, Postgres, etc.) | ☐ | ☐ | ☐ | | |
| Application-to-application API keys | ☐ | ☐ | ☐ | | |
| OAuth client credentials (machine-to-machine) | ☐ | ☐ | ☐ | | |
| SSH host keys | ☐ | ☐ | ☐ | | |
| SSH user keys for jump hosts / bastions | ☐ | ☐ | ☐ | | |
| TLS server certificates | ☐ | ☐ | ☐ | | |
| TLS client / mTLS certificates | ☐ | ☐ | ☐ | | |
| Code-signing certificates | ☐ | ☐ | ☐ | | |
| Internal CA roots / sub-CAs | ☐ | ☐ | ☐ | | |
| Cloud IAM roles (AWS / Azure / GCP) | ☐ | ☐ | ☐ | | |
| Cloud IAM service accounts | ☐ | ☐ | ☐ | | |
| Workload Identity Federation (OIDC) | ☐ | ☐ | ☐ | | |
| Kubernetes ServiceAccounts | ☐ | ☐ | ☐ | | |
| SPIFFE / SPIRE workload identities | ☐ | ☐ | ☐ | | |
| Container registry pull tokens | ☐ | ☐ | ☐ | | |
| CI/CD runner tokens (Jenkins agents, GitHub Actions runners, etc.) | ☐ | ☐ | ☐ | | |
| GitOps controller tokens (ArgoCD, Flux) | ☐ | ☐ | ☐ | | |
| IaC bot tokens (Terraform Cloud, Atlantis, Pulumi) | ☐ | ☐ | ☐ | | |
| Build-time secret-scanning tool tokens | ☐ | ☐ | ☐ | | |
| Webhook / event-bus secrets | ☐ | ☐ | ☐ | | |
| Sigstore / supply-chain signing keys | ☐ | ☐ | ☐ | | |
| Cosign / Notary keys | ☐ | ☐ | ☐ | | |
| HSM-backed keys (Thales, Entrust, Atos, AWS CloudHSM, etc.) | ☐ | ☐ | ☐ | | |
| KMIP-managed keys | ☐ | ☐ | ☐ | | |
| Database TDE keys | ☐ | ☐ | ☐ | | |
| Mainframe service IDs (RACF / Top Secret / ACF2) | ☐ | ☐ | ☐ | | |
| Mainframe APPC / DB2 IDs | ☐ | ☐ | ☐ | | |
| Legacy COBOL/JCL embedded creds | ☐ | ☐ | ☐ | | |
| RPA bot identities (UiPath / Blue Prism / Automation Anywhere) | ☐ | ☐ | ☐ | | |
| AI / ML model serving tokens | ☐ | ☐ | ☐ | | |
| AI agent identities (LLM agents calling tools / MCP servers) | ☐ | ☐ | ☐ | | |
| IoT / OT device identities | ☐ | ☐ | ☐ | | |
| OT SCADA / DCS identities | ☐ | ☐ | ☐ | | |
| B2B partner API tokens (SWIFT, Open Banking AU, NPP, etc.) | ☐ | ☐ | ☐ | | |
| Open Banking AU consent / accreditation tokens | ☐ | ☐ | ☐ | | |
| Federated B2B SAML IdP credentials | ☐ | ☐ | ☐ | | |
| Browser-extension / UI agent tokens | ☐ | ☐ | ☐ | | |
| Encryption-at-rest application keys | ☐ | ☐ | ☐ | | |
| Print / scan / fax device service accounts | ☐ | ☐ | ☐ | | |
| Network device admin creds (routers, switches, firewalls) | ☐ | ☐ | ☐ | | |
| SD-WAN / firewall API tokens | ☐ | ☐ | ☐ | | |
| Backup tool service accounts (NetBackup, Commvault, etc.) | ☐ | ☐ | ☐ | | |
| Monitoring/observability tool API tokens (Datadog, Splunk, Dynatrace, etc.) | ☐ | ☐ | ☐ | | |
| SIEM / SOAR connector tokens | ☐ | ☐ | ☐ | | |
| ITSM tool tokens (ServiceNow, Jira) | ☐ | ☐ | ☐ | | |
| Vault Enterprise root tokens (emergency-break-glass) | ☐ | ☐ | ☐ | | |

> **Open the floor:** anything you observed that the table above is missing?
> This is the "not-so-common machine identities most product owners don't
> think about" bucket the report needs to highlight.

---

## Section D — XYZ secrets-management stack (current state)

### Q-D.01 — Primary platform(s)

- [ ] HashiCorp Vault Enterprise
- [ ] HashiCorp Vault OSS
- [ ] CyberArk PAM / Conjur
- [ ] Delinea Secret Server
- [ ] AWS Secrets Manager (alongside Vault?)
- [ ] Azure Key Vault
- [ ] GCP Secret Manager
- [ ] Cloud KMS (AWS KMS / Azure Key Vault HSM / GCP KMS)
- [ ] Internal home-grown vault / config store
- [ ] Other: _________

### Q-D.02 — Coverage by NHI type

Of the identity types ticked in §C, which ones are **actually stored /
brokered through** the platform(s) above?

- [ ] Almost all → uniform coverage
- [ ] Workload + cloud IAM only
- [ ] DB + service-account creds only
- [ ] Patchwork (some teams use the platform, others don't)
- [ ] Don't know — likely shadow vaults exist

Free-form notes:

### Q-D.03 — Auth methods enabled

- [ ] AppRole
- [ ] Kubernetes auth method
- [ ] AWS IAM auth
- [ ] Azure AD / Entra auth
- [ ] GCP IAM auth
- [ ] LDAP / AD
- [ ] OIDC / JWT
- [ ] TLS cert auth
- [ ] Tokens (static)
- [ ] PKI / SPIRE / SPIFFE
- [ ] Other: _________

### Q-D.04 — HSM / Seal posture

- [ ] HSM-sealed (which vendor — Thales / Entrust / AWS CloudHSM / Other)
- [ ] Cloud-KMS auto-unseal
- [ ] Shamir keys (manual)
- [ ] Don't know

### Q-D.05 — DR / multi-region posture

- [ ] Performance Replication (Vault Enterprise)
- [ ] Disaster Recovery Replication
- [ ] Active-active across regions
- [ ] Active-passive
- [ ] Single-region only
- [ ] Don't know

### Q-D.06 — Secret rotation

For which secret types is rotation **automated**? Tick all that apply.

- [ ] Database creds (dynamic secrets)
- [ ] Cloud IAM creds (dynamic / STS)
- [ ] PKI certs (short-lived)
- [ ] SSH OTPs / SSH CA signing
- [ ] Static KV secrets
- [ ] None / mostly manual
- [ ] Mixed

---

## Section E — Control gaps observed at XYZ

For each row pick **Met / Partial / Gap / Unknown** and add one line of
evidence if you have it.

| Capability | Met | Partial | Gap | Unknown | Evidence (1 line) |
|---|---|---|---|---|---|
| No plain-text secrets in source code | ☐ | ☐ | ☐ | ☐ | |
| No plain-text secrets in CI/CD logs | ☐ | ☐ | ☐ | ☐ | |
| Secret-scanning enforced pre-merge | ☐ | ☐ | ☐ | ☐ | |
| Just-in-time DB credentials | ☐ | ☐ | ☐ | ☐ | |
| Just-in-time cloud IAM | ☐ | ☐ | ☐ | ☐ | |
| Mutual TLS between services | ☐ | ☐ | ☐ | ☐ | |
| Cert lifecycle automated (issuance / rotation / revocation) | ☐ | ☐ | ☐ | ☐ | |
| SSH access via SSH-CA / OTPs (no static keys) | ☐ | ☐ | ☐ | ☐ | |
| Centralised audit log of every secret access | ☐ | ☐ | ☐ | ☐ | |
| Tamper-resistant audit log (WORM / SIEM-shipped) | ☐ | ☐ | ☐ | ☐ | |
| Break-glass account governance | ☐ | ☐ | ☐ | ☐ | |
| Quorum / dual-control on critical operations | ☐ | ☐ | ☐ | ☐ | |
| HSM-backed root keys | ☐ | ☐ | ☐ | ☐ | |
| Geographic data residency enforced (AU sovereignty) | ☐ | ☐ | ☐ | ☐ | |
| Crypto-agility (post-quantum readiness, algorithm migration) | ☐ | ☐ | ☐ | ☐ | |
| Vault inventory of where secrets live (vaultless detection) | ☐ | ☐ | ☐ | ☐ | |
| Secret usage analytics (which workload uses which secret) | ☐ | ☐ | ☐ | ☐ | |
| Mean-time-to-rotate for an exposed secret | ☐ | ☐ | ☐ | ☐ | |
| Inventory of orphaned / unused secrets | ☐ | ☐ | ☐ | ☐ | |
| Mainframe coverage by secrets platform | ☐ | ☐ | ☐ | ☐ | |
| RPA bot coverage by secrets platform | ☐ | ☐ | ☐ | ☐ | |
| AI agent / LLM tool-call secret governance | ☐ | ☐ | ☐ | ☐ | |
| Partner / B2B token rotation | ☐ | ☐ | ☐ | ☐ | |
| IoT / OT device identity governance | ☐ | ☐ | ☐ | ☐ | |
| Detection of secrets in observability tools (Splunk/Datadog dashboards) | ☐ | ☐ | ☐ | ☐ | |

---

## Section F — Red team findings (2019) and follow-ups

### Q-F.01 — Scope of the 2019 red-team

What was in / out of scope?

> _Your text here_

### Q-F.02 — Top findings related to secrets / NHI

Free-form, ideally 3–5 bullets. Anonymise as needed.

> -
> -
> -
> -
> -

### Q-F.03 — Which findings drove the Vault Enterprise selection?

> _Your text here_

### Q-F.04 — Findings that you believe are still open today

> _Your text here_

### Q-F.05 — Adversary TTPs observed or modelled

Cross-reference where possible to MITRE ATT&CK T1552 sub-techniques
(see `research/adversary/mitre-attack-t1552-family.md` once generated):

- [ ] T1552.001 — Credentials in Files
- [ ] T1552.002 — Credentials in Registry
- [ ] T1552.003 — Bash History
- [ ] T1552.004 — Private Keys
- [ ] T1552.005 — Cloud Instance Metadata
- [ ] T1552.006 — Group Policy Preferences
- [ ] T1552.007 — Container API
- [ ] T1552.008 — Chat Messages
- [ ] T1528 — Steal Application Access Token
- [ ] T1606.002 — Web Cookies / Web Session Cookie
- [ ] T1078.004 — Cloud Accounts (legitimate creds reused)
- [ ] Other: _________

---

## Section G — Vendor deployment experience (free-form per vendor)

Multi-vendor — fill only the ones you've actually deployed or evaluated.

### Q-G.01 — HashiCorp Vault Enterprise

- Where deployed: _________
- Years of operation: _________
- Modes used (KV v2 / DB engine / PKI / Transit / Transform / KMIP / GCP-AKM / Azure-AKM / AWS-AKM / Plugins): _________
- Things that worked well:
- Things that **didn't** work well:
- Hardest NHI to onboard:
- Gaps relative to the universal framework (your view):

### Q-G.02 — CyberArk Conjur (and/or CyberArk PAM if relevant)

- Where deployed:
- Modes used (Open Source / Enterprise / Conjur Cloud / DAP):
- Worked well:
- Didn't work well:
- Hardest NHI to onboard:
- Gaps:

### Q-G.03 — Delinea Secret Server (and/or Delinea PAM / Server Suite)

- Where deployed:
- Worked well:
- Didn't work well:
- Hardest NHI to onboard:
- Gaps:

### Q-G.04 — Any cloud-native vault (AWS SM / Azure KV / GCP SM)

- Where deployed:
- Worked well:
- Didn't work well:
- Gaps:

### Q-G.05 — Any "emerging" vault (AKEYLESS / Doppler / Infisical / 1Password Secrets Auto / others)

- Anything to share:

### Q-G.06 — Any PKI / machine-identity platform (Venafi / Keyfactor / others)

- Anything to share:

---

## Section H — Incidents (real or near-miss)

### Q-H.01 — Documented secrets-related incidents at XYZ

- [ ] Public (notified to OAIC / APRA)
- [ ] Internal-only (anonymised in PRD)
- [ ] None / unknown

### Q-H.02 — Near-misses worth narrating (anonymised)

> _Your text here_

### Q-H.03 — Industry incidents you want me to specifically address

(I'll already cover Okta / Cloudflare / CircleCI / Internet Archive /
Sourcegraph / LastPass / xz-utils backdoor by default. Add anything else.)

> _Your text here_

---

## Section I — Prior decisions worth remembering

### Q-I.01 — Decisions XYZ has already made that I should respect

E.g., "Stay on Vault Enterprise; don't propose replacement", or "All new
workloads must be on cloud-native vaults", or "On-prem PKI is decom'd by
end of FY27".

> _Your text here_

### Q-I.02 — Decisions in flight that this report should inform

> _Your text here_

### Q-I.03 — Procurement constraints

Any vendor on the 12-vendor list that XYZ has **formally ruled out** (and
should therefore be dropped or footnoted only)?

> _Your text here_

---

## Section J — FI 27 strategy

### Q-J.01 — What FI 27 expects from secrets-management

> _Your text here_

### Q-J.02 — Where FI 27 conflicts with anything in this PRD (your view)

> _Your text here_

---

## Section K — Anything else

Open mic. Anything you want in the PRD that the structure above didn't ask
about?

> _Your text here_

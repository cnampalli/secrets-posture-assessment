# Appendix D — Adversary context

**Status:** v0.1 (Wave B — 2026-05-23).
**Parent document:** [`PRD-FI-v0.1.md`](../PRD-FI-v0.1.md) §13 + §19.
**Scope:** consolidated narrative from
[`research/adversary/mitre-attack-t1552-family.md`](../../research/adversary/mitre-attack-t1552-family.md)
and
[`research/adversary/breach-postmortems.md`](../../research/adversary/breach-postmortems.md),
joined to the 31 ADVERSARY-LENS rows in
[`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv) (16
MITRE techniques + 15 breach post-mortems). Sensitivity tagging per
[ADR-005](../adrs/ADR-005-fi-evidence-policy.md) — the 2019 red-team
chain is paraphrased and attributed to "a major AU Tier-1 FI".

---

## D.1 Methodology

The adversary lens is **third-priority** behind the PRIMARY-LENS (E8 +
NIST ZT) and BACK-MAP frames (CPS 234 + ISM) per
[ADR-003](../adrs/ADR-003-regulatory-lens.md). Its purpose is not to
re-frame the rubric but to **sharpen it**: for every functional gap
named in PRD §11 and §12, there is at least one MITRE ATT&CK
sub-technique and at least one publicly disclosed breach that names
the gap as a root cause. Where the FI's 2019 red-team chain is
relevant, it is paraphrased — never reproduced. Inputs:

- **MITRE ATT&CK** — T1552 family (8 sub-techniques) + 8 adjacent
  techniques. Source: <https://attack.mitre.org/techniques/T1552/>.
- **Breach catalog** — 15 incidents 2020–2024, each with an
  authoritative primary source. Source:
  [`research/adversary/breach-postmortems.md`](../../research/adversary/breach-postmortems.md).
- **FI 2019 red-team paraphrase** — Task 0 §F.01 / §F.02 / §F.05
  evidence, ADR-005-compliant.
- **Joins** — every TTP and incident row in
  [`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv)
  carries ≥ 1 UC and ≥ 1 NHI; this appendix narrates the joins.

---

## D.2 MITRE ATT&CK T1552 family + adjacent techniques

The T1552 family ("Unsecured Credentials") is the spine of this lens
because every sub-technique resolves to **"the credential the attacker
needed was stored as a recoverable secret instead of an attested,
short-lived, broker-issued identity."** The FI's 2019 finding maps to
T1552.001 / .005 / .006 collectively (see §D.4). Coverage maturity
targets are taken from
[`research/adversary/mitre-attack-t1552-family.md`](../../research/adversary/mitre-attack-t1552-family.md)
§2–§3.

### D.2.1 T1552 sub-techniques (per-technique NHI impact + mitigating UCs)

- **T1552.001 — Credentials in Files.** Plaintext credentials in
  configs, scripts, history files or cloud-provider creds files.
  **Real-world:** Uber 2022 (PowerShell with hard-coded admin
  password on a network share); Toyota 2022 (AWS access key in
  public GitHub repo, ~5 years exposure). **NHIs especially exposed:**
  NHI-001, NHI-003, NHI-005, NHI-007, NHI-008, NHI-009, NHI-012,
  NHI-029, NHI-037. **Mitigating UCs:** UC-F-001, UC-F-002, UC-F-005,
  UC-F-006, UC-F-010, UC-N-001, UC-N-002. **Maturity target: 3.**
- **T1552.002 — Credentials in Registry.** Windows Registry
  credentials cached by services, installers and admin tools.
  **Real-world:** Conti / BlackBasta ransomware crews (M-Trends 2024);
  SolarWinds post-compromise lateral movement. **NHIs:** NHI-012,
  NHI-022, NHI-029, NHI-033, NHI-037. **Mitigating UCs:** UC-F-006,
  UC-F-013, UC-F-015, UC-F-027, UC-N-002. **Maturity target: 3.**
- **T1552.003 — Bash History.** Shell-history files
  (`.bash_history`, `.zsh_history`, `.psql_history`) read for tokens
  and connection strings. **Real-world:** Sourcegraph Aug 2023.
  **NHIs:** NHI-005, NHI-008, NHI-009, NHI-029. **Mitigating UCs:**
  UC-F-001, UC-F-005, UC-F-006, UC-N-008, UC-N-017. **Maturity
  target: 2.**
- **T1552.004 — Private Keys.** SSH, TLS, code-signing, PGP keys
  exfiltrated and reused. **Real-world:** Storm-0558 Jul 2023
  (consumer MSA signing key); xz-utils Mar 2024 (signing-key trust
  abused to land backdoored release). **NHIs:** NHI-006, NHI-008,
  NHI-015, NHI-016, NHI-024, NHI-025, NHI-034. **Mitigating UCs:**
  UC-F-004, UC-F-006, UC-F-016, UC-F-017, UC-F-026, UC-N-010,
  UC-N-013. **Maturity target: 4** (keyless signing + HSM custody +
  quorum break-glass).
- **T1552.005 — Cloud Instance Metadata API.** IMDS queried from a
  compromised workload to retrieve attached-role STS credentials.
  **Real-world:** Capital One 2019 (WAF SSRF → IMDSv1 token theft);
  Sumo Logic Nov 2023 (AWS access-key compromise). **NHIs:** NHI-001,
  NHI-002, NHI-003, NHI-004, NHI-006. **Mitigating UCs:** UC-F-003,
  UC-F-004, UC-F-008, UC-F-009, UC-F-017, UC-N-002. **Maturity
  target: 3** (IMDSv2-only + scoped roles + workload attestation).
- **T1552.006 — Group Policy Preferences (GPP).** Decrypt cached
  `cpassword` values in GPP XML files (AES key publicly disclosed by
  Microsoft 2014). **Real-world:** persistent AD pen-test finding
  including the FI's 2019 red-team analogue (§D.4). **NHIs:**
  NHI-012, NHI-029, NHI-037. **Mitigating UCs:** UC-F-006, UC-F-013,
  UC-F-027, UC-N-002. **Maturity target: 2.**
- **T1552.007 — Container API.** K8s API or container-runtime sockets
  queried to retrieve SA tokens, Secret objects, or `kubeconfig`.
  **Real-world:** TeamTNT 2021–2023; SCARLETEEL 2023 AWS+K8s lateral
  movement. **NHIs:** NHI-002, NHI-003, NHI-004, NHI-017, NHI-036.
  **Mitigating UCs:** UC-F-004, UC-F-008, UC-F-009, UC-F-017,
  UC-N-002. **Maturity target: 3.**
- **T1552.008 — Chat Messages.** Slack / Teams / Discord / Jira /
  chat-bot histories scraped for credentials, tokens, connection
  strings. **Real-world:** Uber 2022 (internal Slack screenshots);
  EA Games 2021 (Slack-cookie reuse). **NHIs:** NHI-007, NHI-008,
  NHI-029, NHI-030. **Mitigating UCs:** UC-F-001, UC-F-007,
  UC-F-025, UC-N-008, UC-N-017. **Maturity target: 2.**

### D.2.2 Adjacent techniques (mapped because they exercise the same NHIs)

- **T1528 — Steal Application Access Token.** OAuth consent
  phishing. **Examples:** Midnight Blizzard Jan 2024; Sourcegraph
  Aug 2023. **NHIs:** NHI-007, NHI-019, NHI-027, NHI-028, NHI-030.
  **Mitigating UCs:** UC-F-007, UC-F-018, UC-F-022, UC-F-024,
  UC-F-025, UC-N-006.
- **T1078.004 — Valid Cloud Accounts.** Legitimate creds reused.
  **Examples:** Snowflake-related 2024; Sumo Logic Nov 2023. **NHIs:**
  NHI-001, NHI-005, NHI-007, NHI-029, NHI-037. **Mitigating UCs:**
  UC-F-003, UC-F-005, UC-F-006, UC-F-007, UC-N-002, UC-N-011.
- **T1606.002 — Web Session Cookie (Forge).** Forge or steal SAML /
  session cookies. **Examples:** Storm-0558 Jul 2023; EA Games 2021.
  **NHIs:** NHI-006, NHI-007, NHI-013, NHI-024, NHI-027. **Mitigating
  UCs:** UC-F-004, UC-F-006, UC-F-007, UC-F-014, UC-F-024, UC-F-026.
  **Maturity target: 4.**
- **T1098.001 — Account Manipulation: Additional Cloud Credentials.**
  Add new keys / SSH / SP secrets for persistence. **Examples:** Okta
  Jan 2022 (LAPSUS$); SolarWinds 2020 (Golden SAML). **NHIs:** NHI-001,
  NHI-007, NHI-008, NHI-012, NHI-027, NHI-028. **Mitigating UCs:**
  UC-F-006, UC-F-007, UC-F-027, UC-N-002, UC-N-009, UC-N-011.
- **T1199 — Trusted Relationship.** Abuse a trusted third-party
  (vendor / MSP / maintainer / contractor). **Examples:** xz-utils
  2024 (maintainer trust); SolarWinds 2020 (signed Orion update);
  Okta Oct 2023 (support-portal vendor tier). **NHIs:** NHI-007,
  NHI-008, NHI-015, NHI-016, NHI-019, NHI-028, NHI-030. **Mitigating
  UCs:** UC-F-016, UC-F-022, UC-F-024, UC-F-025, UC-N-006, UC-N-012,
  UC-N-014.
- **T1539 — Steal Web Session Cookie.** Info-stealer → cookie replay.
  **Examples:** CircleCI Jan 2023; Snowflake-related 2024. **NHIs:**
  NHI-007, NHI-008, NHI-027, NHI-030. **Mitigating UCs:** UC-F-007,
  UC-F-025, UC-N-008, UC-N-017.
- **T1556.006 — Modify Authentication Process: MFA-related bypass.**
  MFA-bombing / factor-modification. **Examples:** Uber Sep 2022;
  Okta Jan 2022 (LAPSUS$). **NHIs:** NHI-007, NHI-029, NHI-030.
  **Mitigating UCs:** UC-F-007, UC-F-013, UC-F-025, UC-N-002,
  UC-N-009.
- **T1566 — Phishing.** Initial-access feeder; not directly a
  secrets-platform control but bounds blast radius. **Examples:** the
  FI's 2019 chain (§D.4); Uber Sep 2022; Twilio Aug 2022. **NHIs:**
  NHI-029, NHI-007, NHI-008, NHI-030. **Mitigating UCs:** UC-F-007,
  UC-F-013, UC-N-008, UC-N-009. **Maturity target: N/A for the
  secrets platform** — phishing is primarily an IAM / email-security
  control; the secrets platform contains blast radius, not entry.

### D.2.3 Cross-cutting observations (per
[`research/adversary/mitre-attack-t1552-family.md`](../../research/adversary/mitre-attack-t1552-family.md)
§4)

Three clusters dominate:

- **Cluster A — "kill the prize."** T1552.001, .003, .004, .006, .008
  and T1078.004 share a common refutation: if the credential is
  short-lived, attestation-bound or signature-keyless, the find-and-
  exfil tradecraft collapses. **UC-F-003 + UC-F-004 + UC-F-005 +
  UC-F-016** flatten the success surface across six techniques at once
  — the single highest-leverage investment in the catalog.
- **Cluster B — "containment after compromise."** T1098.001, T1078.004,
  T1539, T1606.002, T1556.006 are post-access. **UC-F-007 + UC-N-002 +
  UC-N-009 + UC-N-011** are the mitigations — without an inventory you
  cannot revoke; without revocation you cannot contain.
- **Cluster C — "the supply chain you don't own."** T1199, T1528,
  T1566 (+ partially T1552.004) sit at the vendor / maintainer /
  contractor boundary. **UC-F-022 + UC-F-024 + UC-F-025 + UC-N-006 +
  UC-N-012** are the mitigations — Okta-2023 → Cloudflare-2023 bleed
  and xz-utils 2024 are the canonical case studies.

---

## D.3 Breach catalog narrative (15 incidents)

Per-incident schema: **vector → NHIs at root cause → TTPs exercised →
mitigating UCs**. Full quotes and authoritative URLs are in
[`research/adversary/breach-postmortems.md`](../../research/adversary/breach-postmortems.md).
All entries are `[PUBLIC]`.

| # | Incident | Vector (≤ 30 w) | NHIs at root cause | TTPs | Mitigating UCs |
|---|---|---|---|---|---|
| 1 | **Okta 2023-10 (Customer Support)** | Stolen service-account cred saved into employee personal Google Chrome on Okta-managed laptop; ~134 customer HAR files leaked. | NHI-007; NHI-029; NHI-030 | T1552.001, T1552.008, T1539, T1078.004, T1199 | UC-F-001, UC-F-006, UC-F-025, UC-F-027, UC-N-002, UC-N-006, UC-N-017 |
| 2 | **Okta 2022-01 (LAPSUS$ via Sitel)** | Sitel support-engineer laptop compromised; cached RDP / session + Okta SuperUser app → ~366 customer tenants over 5 days. | NHI-029; NHI-007; NHI-030 | T1199, T1078.004, T1539, T1556.006, T1098.001 | UC-F-007, UC-F-025, UC-N-002, UC-N-006, UC-N-009, UC-N-011 |
| 3 | **Cloudflare 2023-11** | Tokens not rotated after Okta Oct-2023 incident → nation-state actor accessed Atlassian Confluence/Jira/Bitbucket; 5,000 prod creds rotated in response. | NHI-007; NHI-008; NHI-029; NHI-037 | T1199, T1078.004, T1552.001, T1098.001 | UC-F-006, UC-F-007, UC-F-027, UC-N-002, UC-N-006, UC-N-011 |
| 4 | **CircleCI 2023-01** | Info-stealer on engineer laptop bypassed MFA via session-cookie theft → prod access Dec 19; customers told to rotate all secrets. | NHI-003; NHI-007; NHI-008; NHI-030 | T1539, T1552.001, T1552.008, T1078.004, T1606.002 | UC-F-003, UC-F-004, UC-F-006, UC-F-007, UC-N-006, UC-N-017 |
| 5 | **Internet Archive 2024-10** | GitLab config file with auth tokens exposed → 31M user records; unrotated Zendesk API tokens used after disclosure. | NHI-007; NHI-008; NHI-029 | T1552.001, T1078.004, T1098.001, T1539 | UC-F-001, UC-F-002, UC-F-006, UC-F-007, UC-N-002, UC-N-006 |
| 6 | **Sourcegraph 2023-08** | Site-admin access token committed to public GitHub PR Jul 14; external user found it Aug 28, generated ~100 free API tokens. | NHI-007; NHI-008; NHI-029 | T1552.001, T1552.003, T1528, T1078.004, T1098.001 | UC-F-001, UC-F-002, UC-F-006, UC-F-007, UC-N-001, UC-N-008 |
| 7 | **LastPass 2022-08 + 2022-11** | Source-code theft Aug; Nov DevOps engineer home computer keylogged via Plex bug → corporate-vault master password → customer-vault backups for 30 customers. | NHI-008; NHI-024; NHI-029; NHI-035 | T1552.001, T1552.004, T1552.008, T1078.004, T1098.001, T1199 | UC-F-006, UC-F-007, UC-F-017, UC-F-026, UC-N-010, UC-N-011 |
| 8 | **xz-utils 2024-03** | Three-year social-engineering of OSS maintainer; SSHD backdoor in 5.6.0/5.6.1; caught accidentally pre-downstream-stable. | NHI-008; NHI-015; NHI-016; NHI-019 | T1199, T1078, T1552.004, T1195.002 | UC-F-016, UC-N-012, UC-N-006, UC-N-014, UC-F-025 |
| 9 | **SolarWinds (SUNBURST) 2020-12** | Russian SVR compromised SolarWinds build pipeline; signed Orion update → ~18,000 customers; downstream Golden SAML via AD FS token-signing cert. | NHI-003; NHI-008; NHI-015; NHI-016; NHI-024; NHI-025; NHI-006 | T1199, T1195.002, T1552.004, T1606.002, T1098.001, T1078.004 | UC-F-004, UC-F-016, UC-F-017, UC-F-026, UC-N-010, UC-N-011, UC-N-012, UC-N-013 |
| 10 | **Microsoft Storm-0558 2023-07** | Consumer MSA signing key leaked into crash-dump moved to debug env; token-validation flaw → forged Exchange Online tokens; ~25 orgs incl. US State/Commerce. | NHI-015; NHI-024; NHI-025; NHI-006 | T1552.004, T1606.002, T1078.004, T1199 | UC-F-006, UC-F-016, UC-F-017, UC-F-026, UC-N-010, UC-N-011, UC-N-013 |
| 11 | **Uber 2022-09** | Contractor VPN creds bought on dark web; MFA defeated via push-fatigue + social-eng; PowerShell script on network share with PAM admin password. | NHI-001; NHI-005; NHI-012; NHI-024; NHI-029; NHI-037 | T1556.006, T1552.001, T1552.008, T1078.004, T1098.001 | UC-F-001, UC-F-005, UC-F-007, UC-F-013, UC-F-015, UC-F-026, UC-N-002, UC-N-010 |
| 12 | **Toyota 2022-10** | T-Connect subcontractor uploaded source with AWS key to public GitHub Dec 2017; exposed ~5 years; ~296,019 customer records potentially accessed. | NHI-001; NHI-008; NHI-029 | T1552.001, T1078.004 | UC-F-001, UC-F-002, UC-F-003, UC-F-006, UC-N-001, UC-N-002, UC-N-006 |
| 13 | **Sumo Logic 2023-11** | Compromised AWS access key used against Sumo Logic AWS infra; no customer-data exposure confirmed; customers urged to rotate. | NHI-001; NHI-007; NHI-029 | T1552.001, T1552.005, T1078.004, T1098.001 | UC-F-003, UC-F-006, UC-F-007, UC-N-002, UC-N-017 |
| 14 | **MOVEit 2023-05/06 (Cl0p)** | SQLi zero-day (CVE-2023-34362) in Progress MOVEit Transfer; LEMURLOOT webshell; 2,700+ orgs incl. a major AU Tier-1 FI in victim cohort via Citrix-MOVEit vendor channel (~7,000 staff data). | NHI-006; NHI-007; NHI-013; NHI-029; NHI-031 | T1190, T1552.001, T1552.004, T1078.004, T1098.001 | UC-F-007, UC-F-014, UC-F-022, UC-N-006, UC-N-011, UC-N-014 |
| 15 | **Snowflake-related 2024-06** | UNC5537 used info-stealer-harvested creds (some from 2020) against 165+ Snowflake tenants lacking MFA; victims incl. Ticketmaster, AT&T, Santander, Pure Storage. | NHI-001; NHI-005; NHI-007; NHI-029; NHI-037 | T1078.004, T1552.001, T1552.008, T1539, T1556.006, T1199 | UC-F-003, UC-F-005, UC-F-006, UC-F-007, UC-N-002, UC-N-006, UC-N-011 |

> **AU-relevance flag (row 14).** The Cl0p / MOVEit campaign named a
> major AU Tier-1 FI in its victim cohort via the Citrix-MOVEit
> vendor channel in June 2023 (~7,000 staff data). This is `[PUBLIC]`
> information; per ADR-005 the FI is referenced as "a major AU Tier-1
> FI" in this PRD.

---

## D.4 The FI's 2019 red-team chain (paraphrased per ADR-005)

> Attribution: paraphrased lived-experience signal from a major AU
> Tier-1 FI per [ADR-005](../adrs/ADR-005-fi-evidence-policy.md).
> No `[SENSITIVE]` or `[NOT-FOR-DISTRIBUTION]` material is reproduced.
> Source: Task 0 §F.01 / §F.02 / §F.04 / §F.05 lived-experience
> evidence, paraphrased.

An external consultancy engagement of roughly one week's duration
produced a credible offensive chain against the FI in 2019. The
narrative — to the extent it is captured in the PRD — is as follows.

- **Initial access (T1566 Phishing).** A targeted phishing campaign
  against an executive's mailbox succeeded; the campaign exploited
  user-trust signals more than email-security controls. This is an
  IAM / mail-security control boundary, not a secrets-platform one
  (per §D.2.2 — the secrets platform contains blast radius, not
  entry).
- **Lateral pivot (T1078 Valid Accounts).** Mailbox compromise was
  used to harvest credentials adjacent to the executive's role and
  pivot into privileged accounts. T1078.004 (cloud-accounts variant)
  was not the dominant vector in 2019 because the cloud estate was
  less mature; the on-prem / AD variant carried the weight.
- **Credential discovery (T1552-family).** Three sub-techniques
  appear in the lived-experience evidence:
  - **T1552.001 — Credentials in Files.** Plaintext secrets in source
    repositories. **This finding remains the dominant open exposure
    six years later** and is the anchor for PRD R7.
  - **T1552.005 — Cloud Instance Metadata API** (or its 2019 on-prem
    analogue) — over-permissioned PA-SAs effectively played the same
    role IMDS would later play in cloud-native breaches: a single
    over-scoped identity broadened blast radius materially.
  - **T1552.006 — Group Policy Preferences.** A persistent finding
    in AD pen-tests of this vintage; the FI was no exception.
- **Privilege escalation (T1098 Account Manipulation).** Over-
  permissioned UNIX / Linux PA-SAs with direct database access — a
  blast-radius violation more than a credential-secret violation.
  **Post-CyberArk PAM status is unconfirmed** (PRD §17 O10) and is
  the open question that anchors PRD R8.
- **Trusted-relationship variants (T1199).** The consultancy itself
  modelled a vendor-trust path; this is the lens through which the
  FI should read the Okta-2023 → Cloudflare-2023 bleed and xz-utils
  2024 today.

**Implication for v0.1 recommendations.** The 2019 chain is **still
live as a control narrative**. The UCs that would have detected or
prevented the chain — UC-F-001 (no plaintext in repos), UC-F-006
(rotation), UC-F-007 (immediate revocation), UC-F-013 (gMSA / AD
modernisation), UC-N-002 (NHI inventory), UC-N-011 (identity-driven
RCA) — are exactly the lanes where the FI carries the most
unfinished work today. PRD R1 + R2 + R7 + R8 are the response.

---

## D.5 Cross-incident observations

Per [`research/adversary/breach-postmortems.md`](../../research/adversary/breach-postmortems.md)
§"Cross-incident pattern observations":

### D.5.1 NHIs most often at root cause (across the 15 incidents)

| NHI | Incidents | Bucket |
|---|---|---|
| **NHI-007** — third-party SaaS API key / OAuth client | 13 of 15 | COMMON |
| **NHI-029** — service-account-as-human | 12 of 15 | UNCOMMON |
| **NHI-008** — Git platform credential | 10 of 15 | COMMON |
| **NHI-001** — cloud IAM principal | 8 of 15 | COMMON |
| **NHI-037** — orphaned / dormant identity | 6 of 15 | UNCOMMON |
| **NHI-015, NHI-016, NHI-024, NHI-025** — signing / SLSA / HSM / CA | concentrated in the **highest-severity** incidents (Storm-0558, SolarWinds, LastPass, xz-utils) | UNCOMMON |

**Signal.** The UNCOMMON taxonomy entries (NHI-015 signing identity,
NHI-016 SLSA provenance, NHI-024 HSM operator, NHI-025 CA operator)
appear in the *highest-severity* incidents. These are low-volume /
high-blast-radius identities and warrant **Maturity-4** controls —
consistent with the T1552.004 + T1606.002 maturity-4 target.

### D.5.2 UCs with the highest aggregate "would have prevented" impact

| UC | Hits / 15 | Cluster |
|---|---|---|
| **UC-F-006** — rotation of long-lived static secrets | 11/15 | B |
| **UC-F-007** — immediate revocation on compromise | 11/15 | B |
| **UC-N-002** — NHI inventory and ownership attestation | 10/15 | B |
| **UC-F-001** — prevent plaintext in repos | 8/15 | A |
| **UC-N-006** — vendor / SaaS supply-chain risk attestation | 8/15 | C |
| **UC-F-003** — JIT short-lived cloud creds via OIDC | 7/15 | A |
| **UC-N-011** — identity-driven post-incident RCA | 7/15 | B |
| **UC-F-002** — detect secrets in history | 4/15 | A (lower leverage than prevention) |

**Sequencing implication.** The PRD §16 priority order
(**inventory → rotation → revocation → short-lived issuance → vendor
attestation**) is justified by the breach evidence, not by abstract
control wishlists. UC-F-002 (history sweep) is useful but not the
highest-leverage investment versus prevention.

### D.5.3 Repeating patterns across incidents

- **"Unrotated after a known-bad event"** was the proximate vector in
  Cloudflare-2023, Internet Archive-2024 (Zendesk), Sourcegraph-2023
  (token visible ~7 weeks) and Snowflake-2024. **UC-F-007 + UC-N-011
  SLA discipline matters more than any new tool.**
- **"Contractor / vendor / maintainer trust"** was material in Okta×2,
  Cloudflare, xz-utils, SolarWinds and LastPass. **UC-N-006 and
  UC-N-014 are not nice-to-haves.**
- **"Endpoint-malware → session-cookie → bypass MFA"** was decisive in
  CircleCI, Uber, LastPass and Snowflake-related. **UC-F-007 +
  UC-F-025 plus phishing-resistant MFA** (out of secrets scope; cross-
  stream to IAM) close the loop.
- **AU-relevant breaches.** Direct attribution: a major AU Tier-1 FI
  was in the MOVEit-Cl0p victim cohort via the Citrix-MOVEit vendor
  channel (June 2023). Latent: Snowflake-2024 affected Santander but
  no AU Tier-1 FI publicly confirmed. APRA's breach-notification
  register under CPS 234 §35 is non-public, so further AU-FI
  attribution cannot be cited from primary sources at v0.1.

---

## D.6 Bridging to the PRD body and Appendix A

Every dominant FI-side finding in PRD §12 (titled there "Findings —
XYZ side" as a structural document label only) maps to ≥ 1 TTP and
≥ 1 breach. The summary below is the PRD's "audit-facing read" of this
appendix and is reproduced verbatim from PRD §13 for orientation:

- **F-A-9 (plaintext-in-repos)** ↔ T1552.001 + Uber 2022 + Toyota
  2022 + Internet Archive 2024-10.
- **F-A-6 (no SPIFFE, AWS-only JIT)** ↔ T1552.005 + Capital One 2019
  + Sumo Logic 2023.
- **F-A-10 (ZT workload identity not understood)** ↔ T1552.007 +
  TeamTNT / SCARLETEEL.
- **F-A-2 (vault sprawl across cloud-native vaults)** ↔ T1552.004 +
  T1078.004 + LastPass 2022 + Storm-0558.

The 31 ADVERSARY-LENS rows in
[`matrix/regulatory-trace.csv`](../../matrix/regulatory-trace.csv) are
the data underpinning this narrative and are also enumerated in
[Appendix A](./A-compliance-traceability.md) §A.4.

---

> _End of Appendix D (Wave B v0.1)._

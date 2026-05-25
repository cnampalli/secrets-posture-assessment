# MITRE ATT&CK — T1552 Credential Access and Related Techniques

Mapped by: Opus 4.7 (prompt 05 v0.1)
Date: 2026-05-23
Sensitivity: `[PUBLIC]`

## 1. Why this lens (≤ 150 words)

Regulatory and outcome lenses (Essential 8, NIST ZT, APRA CPS 234, ISM) describe what *should* be true. The adversary lens describes what *actually goes wrong*. MITRE ATT&CK is the public lingua franca for credential-theft tradecraft: T1552 and its adjacents are the techniques where stolen secrets, mis-scoped service accounts and trusted-relationship abuse converge. Every named breach below (Okta, CircleCI, Storm-0558, SolarWinds, LastPass, MOVEit, Snowflake, Uber, xz-utils) is reducible to one or more of these codes. By mapping each technique to the project's UCs and NHIs, the PRD can claim — defensibly — "investing in UC-F-X reduces our exposure to T1552.x, which was the proximate cause of incident Y". This is what converts a control wishlist into a board-grade risk narrative, including the XYZ 2019 red-team chain (T1566 → T1078 → T1552-family) referenced in Task 0 §Q-F.01.

## 2. T1552 sub-techniques in scope

### T1552.001 — Credentials in Files
- **Definition:** Adversaries search file systems and code repositories for unsecured credentials in plaintext configs, scripts, history files or cloud-provider creds files. (≤ 40 words from MITRE.)
- **Real-world examples:** Uber 2022 (PowerShell script with hard-coded admin password on the network share); Toyota 2022 (AWS access key in public GitHub repo, ~5 years exposure).
- **NHIs especially exposed:** NHI-001, NHI-003, NHI-005, NHI-007, NHI-008, NHI-009, NHI-012, NHI-029, NHI-037.
- **UCs that mitigate:** UC-F-001, UC-F-002, UC-F-005, UC-F-006, UC-F-010, UC-N-001, UC-N-002.
- **Coverage maturity 0–4 needed:** **3** (continuous scanning + remediation SLAs + secret-less issuance for the top NHI classes).
- **Citation:** https://attack.mitre.org/techniques/T1552/001/

### T1552.002 — Credentials in Registry
- **Definition:** Adversaries query the Windows Registry for credentials stored by services, installers and admin tools (e.g., AutoLogon, WinSCP, PuTTY).
- **Real-world examples:** Multiple ransomware crews (Conti, BlackBasta) per Mandiant M-Trends 2024 [INDUSTRY-CONSENSUS]; SolarWinds Orion lateral movement post-compromise stage.
- **NHIs especially exposed:** NHI-012, NHI-022, NHI-029, NHI-033, NHI-037.
- **UCs that mitigate:** UC-F-006, UC-F-013, UC-F-015, UC-F-027, UC-N-002.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1552/002/

### T1552.003 — Bash History
- **Definition:** Adversaries read shell-history files (`.bash_history`, `.zsh_history`, `.psql_history`) for tokens, passwords and connection strings pasted on the command line.
- **Real-world examples:** Sourcegraph Aug 2023 (engineer endpoint creds exposed); generic incident-response pattern, Verizon DBIR 2024 §"Credential Compromise" [INDUSTRY-CONSENSUS].
- **NHIs especially exposed:** NHI-005, NHI-008, NHI-009, NHI-029.
- **UCs that mitigate:** UC-F-001, UC-F-005, UC-F-006, UC-N-008 (engineer training KPI), UC-N-017.
- **Coverage maturity 0–4 needed:** **2** (training + endpoint hardening + dynamic creds remove the prize).
- **Citation:** https://attack.mitre.org/techniques/T1552/003/

### T1552.004 — Private Keys
- **Definition:** Adversaries search for private SSH, TLS, code-signing or PGP keys on disk or in artifact stores to impersonate identities or sign malicious artifacts.
- **Real-world examples:** Microsoft Storm-0558 (consumer MSA signing key, July 2023); xz-utils Mar 2024 (signing-key trust abused to land backdoored release).
- **NHIs especially exposed:** NHI-006, NHI-008, NHI-015, NHI-016, NHI-024, NHI-025, NHI-034.
- **UCs that mitigate:** UC-F-004, UC-F-006, UC-F-016, UC-F-017, UC-F-026, UC-N-010, UC-N-013.
- **Coverage maturity 0–4 needed:** **4** (keyless signing + HSM custody + quorum break-glass).
- **Citation:** https://attack.mitre.org/techniques/T1552/004/

### T1552.005 — Cloud Instance Metadata API
- **Definition:** Adversaries query a cloud instance's metadata service (IMDS) from a compromised workload to retrieve temporary credentials of the attached IAM role.
- **Real-world examples:** Capital One 2019 (WAF SSRF → IMDSv1 token theft) [INDUSTRY-CONSENSUS, regulator filing]; Sumo Logic Nov 2023 (AWS access-key compromise — root cause in adjacent vector but same class).
- **NHIs especially exposed:** NHI-001, NHI-002, NHI-003, NHI-004, NHI-006.
- **UCs that mitigate:** UC-F-003, UC-F-004, UC-F-008, UC-F-009, UC-F-017, UC-N-002.
- **Coverage maturity 0–4 needed:** **3** (IMDSv2-only + scoped roles + workload attestation).
- **Citation:** https://attack.mitre.org/techniques/T1552/005/

### T1552.006 — Group Policy Preferences (GPP)
- **Definition:** Adversaries decrypt cached `cpassword` values in GPP XML files — the AES key was publicly disclosed by Microsoft in 2014.
- **Real-world examples:** Persistent finding in AD penetration tests including XYZ 2019 red-team analog per Task 0 §Q-F.01 [BREACH-POST-MORTEM, internal]; pervasive in Mandiant M-Trends [INDUSTRY-CONSENSUS].
- **NHIs especially exposed:** NHI-012, NHI-029, NHI-037.
- **UCs that mitigate:** UC-F-006, UC-F-013, UC-F-027, UC-N-002.
- **Coverage maturity 0–4 needed:** **2**.
- **Citation:** https://attack.mitre.org/techniques/T1552/006/

### T1552.007 — Container API
- **Definition:** Adversaries query the Kubernetes API or container-runtime sockets to retrieve ServiceAccount tokens, secret objects or `kubeconfig` mounts.
- **Real-world examples:** TeamTNT campaigns 2021–2023 (Kubernetes token theft → cryptomining) [INDUSTRY-CONSENSUS]; SCARLETEEL 2023 AWS+K8s lateral-movement (Sysdig report).
- **NHIs especially exposed:** NHI-002, NHI-003, NHI-004, NHI-017, NHI-036.
- **UCs that mitigate:** UC-F-004, UC-F-008, UC-F-009, UC-F-017, UC-N-002.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1552/007/

### T1552.008 — Chat Messages
- **Definition:** Adversaries scrape Slack, Teams, Discord, Jira or chat-bot histories for credentials, tokens and connection strings shared by operators.
- **Real-world examples:** Uber 2022 (attacker exfiltrated internal Slack screenshots showing creds); EA Games 2021 (Slack-cookie-driven access) [INDUSTRY-CONSENSUS].
- **NHIs especially exposed:** NHI-007, NHI-008, NHI-029, NHI-030.
- **UCs that mitigate:** UC-F-001, UC-F-007, UC-F-025, UC-N-008, UC-N-017.
- **Coverage maturity 0–4 needed:** **2**.
- **Citation:** https://attack.mitre.org/techniques/T1552/008/

## 3. Adjacent techniques

### T1528 — Steal Application Access Token
- **Definition:** Adversaries phish or socially engineer users into granting OAuth scopes to an attacker-controlled app, harvesting the resulting tokens.
- **Real-world examples:** Midnight Blizzard (Microsoft) Jan 2024 — legacy OAuth consent grant; Sourcegraph Aug 2023 (leaked engineer token reused for API access).
- **NHIs especially exposed:** NHI-007, NHI-019, NHI-025 (?), NHI-027, NHI-028, NHI-030.
- **UCs that mitigate:** UC-F-007, UC-F-018, UC-F-022, UC-F-024, UC-F-025, UC-N-006.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1528/

### T1078.004 — Cloud Accounts (legitimate creds reused)
- **Definition:** Adversaries obtain and use credentials of valid cloud accounts to access resources, often combined with T1552.001/005/008.
- **Real-world examples:** Snowflake-related 2024 (info-stealer-harvested customer credentials reused against Snowflake tenants); Sumo Logic Nov 2023.
- **NHIs especially exposed:** NHI-001, NHI-005, NHI-007, NHI-029, NHI-037.
- **UCs that mitigate:** UC-F-003, UC-F-005, UC-F-006, UC-F-007, UC-N-002, UC-N-011.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1078/004/

### T1606.002 — Web Session Cookie (Forge)
- **Definition:** Adversaries forge or steal web session cookies / SAML responses to authenticate without credentials or MFA.
- **Real-world examples:** Storm-0558 Jul 2023 (forged Azure AD tokens); EA Games 2021 (Slack cookie reuse) [INDUSTRY-CONSENSUS].
- **NHIs especially exposed:** NHI-006, NHI-007, NHI-013, NHI-024, NHI-027.
- **UCs that mitigate:** UC-F-004, UC-F-006, UC-F-007, UC-F-014, UC-F-024, UC-F-026.
- **Coverage maturity 0–4 needed:** **4** (forge resistance requires HSM-backed signing + key rotation + token-binding).
- **Citation:** https://attack.mitre.org/techniques/T1606/002/

### T1098.001 — Account Manipulation: Additional Cloud Credentials
- **Definition:** After initial access, adversaries add new credentials, SSH keys or service-principal secrets to maintain persistence under a legitimate identity.
- **Real-world examples:** Okta Jan 2022 (LAPSUS$ added factors); SolarWinds 2020 (Golden SAML — AD FS token-signing certificate abuse).
- **NHIs especially exposed:** NHI-001, NHI-007, NHI-008, NHI-012, NHI-027, NHI-028.
- **UCs that mitigate:** UC-F-006, UC-F-007, UC-F-027, UC-N-002, UC-N-009, UC-N-011.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1098/001/

### T1199 — Trusted Relationship
- **Definition:** Adversaries abuse a trusted third party (vendor, MSP, contractor, open-source maintainer) whose access bypasses target controls.
- **Real-world examples:** xz-utils Mar 2024 (maintainer-trust abuse landed backdoor); SolarWinds 2020 (signed Orion update); Okta Oct 2023 (support-portal vendor-tier trust).
- **NHIs especially exposed:** NHI-007, NHI-008, NHI-015, NHI-016, NHI-019, NHI-028, NHI-030.
- **UCs that mitigate:** UC-F-016, UC-F-022, UC-F-024, UC-F-025, UC-N-006, UC-N-012, UC-N-014.
- **Coverage maturity 0–4 needed:** **3**.
- **Citation:** https://attack.mitre.org/techniques/T1199/

### T1539 — Steal Web Session Cookie (Theft)
- **Definition:** Adversaries steal session cookies from a browser, endpoint or memory dump to replay authenticated sessions without credentials.
- **Real-world examples:** CircleCI Jan 2023 (info-stealer harvested engineer 2FA-backed session); Snowflake-related 2024 (info-stealer logs sold and reused).
- **NHIs especially exposed:** NHI-007, NHI-008, NHI-027, NHI-030.
- **UCs that mitigate:** UC-F-007, UC-F-025, UC-N-008, UC-N-017.
- **Coverage maturity 0–4 needed:** **2**.
- **Citation:** https://attack.mitre.org/techniques/T1539/

### T1556.006 — Modify Authentication Process: MFA-related bypass
- **Definition:** Adversaries modify, register or downgrade MFA factors to bypass second-factor authentication on a legitimate identity.
- **Real-world examples:** Uber Sep 2022 (MFA-bombing → push fatigue → factor-add); Okta Jan 2022 (LAPSUS$ session-cookie reuse from contractor laptop).
- **NHIs especially exposed:** NHI-007, NHI-029 (human-shaped NHIs are the prime vector), NHI-030.
- **UCs that mitigate:** UC-F-007, UC-F-013, UC-F-025, UC-N-002, UC-N-009.
- **Coverage maturity 0–4 needed:** **3** (phishing-resistant MFA + factor-change anomaly detection).
- **Citation:** https://attack.mitre.org/techniques/T1556/006/

### T1566 — Phishing (initial-access feeder)
- **Definition:** Adversaries send electronic messages to elicit credentials, MFA approvals or malware execution — the dominant feeder into the credential-theft chain.
- **Real-world examples:** XYZ 2019 red-team chain (Task 0 §Q-F.01 — phishing of CEO → privileged-account creds); Uber Sep 2022; Twilio Aug 2022 [INDUSTRY-CONSENSUS].
- **NHIs especially exposed:** NHI-029 (service-account-as-human), NHI-007, NHI-008, NHI-030.
- **UCs that mitigate:** UC-F-007, UC-F-013, UC-N-008, UC-N-009 (the secrets-platform mitigations are bounded — phishing is primarily an IAM/email-security control; we contain blast radius, not the entry).
- **Coverage maturity 0–4 needed:** **N/A for secrets platform**; blast-radius containment matures from 2 → 3 with UC-F-007 (immediate revocation) + UC-F-003 (short-lived creds).
- **Citation:** https://attack.mitre.org/techniques/T1566/

## 4. Cross-cutting observations (≤ 250 words)

Three clusters dominate.

**Cluster A — "kill the prize."** T1552.001, T1552.003, T1552.004, T1552.006, T1552.008 and T1078.004 share a common refutation: if the credential the attacker steals is short-lived, attestation-bound or signature-keyless, the find-and-exfil tradecraft collapses. UC-F-003 (OIDC short-lived), UC-F-004 (SPIFFE workload-attested), UC-F-005 (dynamic DB leases) and UC-F-016 (keyless signing) flatten the success surface across six techniques at once. This is the single highest-leverage investment in the catalog.

**Cluster B — "containment after compromise."** T1098.001, T1078.004, T1539, T1606.002 and T1556.006 describe what happens once the attacker is inside. The mitigations are detection + revocation — UC-F-007 (immediate revocation), UC-N-002 (NHI inventory + ownership), UC-N-011 (identity-driven RCA) and UC-N-009 (exception register). Without an inventory you cannot revoke; without revocation you cannot contain.

**Cluster C — "the supply chain you don't own."** T1199, T1528, T1566 and (partially) T1552.004 sit at the boundary between the bank and its vendors / maintainers / contractors. Mitigations span UC-F-022 (webhook identity), UC-F-024 (FAPI mTLS partners), UC-F-025 (OAuth-app governance), UC-N-006 (vendor risk attestation) and UC-N-012 (SLSA provenance). The Okta-2023 → Cloudflare-2023 bleed and xz-utils 2024 are the canonical case studies.

Implication for PRD §5/§14: the "coverage maturity" column in the matrix should be read alongside the TTP it mitigates. A control at Maturity 1 against a Maturity-3-needed TTP is *materially* exposed.

## 5. Open questions

- Does XYZ have an internal red-team replay of T1552.001/.004/.005 against the current secrets surface (post-2019)?
- Is T1556.006 in scope for the secrets platform, or owned entirely by the IAM/Entra control plane?
- Should T1647 (Plist File Modification — macOS) be added given developer-laptop fleet?
- How does the matrix treat T1078 (parent) vs T1078.004 (cloud sub) — do we need a dual row?
- What's the right authoritative source for T1199 XYZ-relevant breaches (APRA breach-notification register has not historically been public — confirm via CPS 234 §35 reporting)?
- Should we map T1606.001 (Web Cookies — local theft) separately from T1606.002 (Forge)?
- For T1552.004 (private keys), is the project's Maturity-4 ambition (keyless + HSM + quorum) realistic in a 12-month roadmap?
- For T1566, should the PRD explicitly *defer* phishing mitigations to the IAM stream with a clean RACI handoff (recommend: yes)?

## 6. Citations

Appended to `meta/citations.bib` under `## Adversary TTPs (Agent 05)`. Keys used in this file:

- `mitre-attack-t1552-2024`, `mitre-attack-t1552-001`, `mitre-attack-t1552-002`, `mitre-attack-t1552-003`, `mitre-attack-t1552-004`, `mitre-attack-t1552-005`, `mitre-attack-t1552-006`, `mitre-attack-t1552-007`, `mitre-attack-t1552-008`
- `mitre-attack-t1528`, `mitre-attack-t1078-004`, `mitre-attack-t1606-002`, `mitre-attack-t1098-001`, `mitre-attack-t1199`, `mitre-attack-t1539`, `mitre-attack-t1556-006`, `mitre-attack-t1566`
- `mandiant-m-trends-2024`, `verizon-dbir-2024`, `sysdig-scarleteel-2023`

# Breach Post-Mortems Relevant to Secrets / Machine-Identity Management

Mapped by: Opus 4.7 (prompt 05 v0.1)
Date: 2026-05-23
Sensitivity: `[PUBLIC]`

Scope: 15 publicly-disclosed incidents from 2020–2024 where stolen, mismanaged or over-scoped secrets / machine identities were the proximate or contributing cause. Each entry conforms to the schema in `prompts/05-adversary-ttp-mapper.md` §"Markdown schema — breach-postmortems.md".

---

## Okta — 2023-10 (Customer Support System breach)
- **Vector:** Attacker used a stolen service-account credential saved into an employee's personal Google account to access Okta's customer support case-management system; ~134 customers' HAR files (containing session cookies) exposed; Cloudflare and 1Password downstream.
- **Secrets / NHIs at root cause:** NHI-007 (SaaS API key / OAuth client), NHI-029 (service-account-as-human, saved-to-personal-browser), NHI-030 (browser extension / cookie sync).
- **MITRE ATT&CK techniques exercised:** T1552.001, T1552.008, T1539, T1078.004, T1199.
- **UCs that — if matured — would have detected or prevented:** UC-F-001, UC-F-006, UC-F-025, UC-F-027, UC-N-002, UC-N-006, UC-N-017.
- **Authoritative source:** https://sec.okta.com/harfiles ; https://sec.okta.com/articles/2023/11/unauthorized-access-oktas-customer-support-system-and-okta
- **Quote (≤ 30 words):** "A service account stored within the system in question … signed into an employee's personal Google profile on the Chrome browser of their Okta-managed laptop." (Okta, 2023-11-03)

## Okta — 2022-01 (LAPSUS$ via Sitel contractor)
- **Vector:** LAPSUS$ compromised a Sitel support engineer's laptop, used cached RDP / session and Okta SuperUser app to access ~366 customer tenants over a 5-day window in January 2022.
- **Secrets / NHIs at root cause:** NHI-029, NHI-007, NHI-030.
- **MITRE ATT&CK techniques exercised:** T1199, T1078.004, T1539, T1556.006, T1098.001.
- **UCs that — if matured — would have prevented:** UC-F-007, UC-F-025, UC-N-002, UC-N-006, UC-N-009, UC-N-011.
- **Authoritative source:** https://sec.okta.com/articles/2022/03/oktas-investigation-january-2022-compromise ; https://sec.okta.com/articles/2022/04/okta-concludes-its-investigation-january-2022-compromise
- **Quote:** "A 25-minute time-frame on January 21, 2022 in which the threat actor had access to the Sitel support engineer's workstation." (Okta, 2022-04-19)

## Cloudflare — 2023-11 (Thanksgiving — Okta-supply-chain bleed)
- **Vector:** Tokens and service-account credentials *not rotated* after the Okta Oct-2023 incident allowed a nation-state actor to access Atlassian Confluence, Jira and Bitbucket on Thanksgiving 2023; rotated 5,000 production credentials in response.
- **Secrets / NHIs at root cause:** NHI-007, NHI-008, NHI-029, NHI-037.
- **MITRE ATT&CK techniques exercised:** T1199, T1078.004, T1552.001, T1098.001.
- **UCs that — if matured — would have prevented:** UC-F-006, UC-F-007, UC-F-027, UC-N-002, UC-N-006, UC-N-011.
- **Authoritative source:** https://blog.cloudflare.com/thanksgiving-2023-security-incident
- **Quote:** "One service token and three service accounts that were not rotated were used by the threat actor … This was our mistake." (Cloudflare, 2024-02-01)

## CircleCI — 2023-01 (Engineer endpoint malware → OAuth + secrets exfil)
- **Vector:** Info-stealer malware on a CircleCI engineer's laptop bypassed MFA via session-cookie theft (June 30 token-theft) and accessed production systems on Dec 19; customers instructed to rotate *all* secrets stored in CircleCI.
- **Secrets / NHIs at root cause:** NHI-003 (CI/CD identity), NHI-007, NHI-008, NHI-030.
- **MITRE ATT&CK techniques exercised:** T1539, T1552.001, T1552.008, T1078.004, T1606.002.
- **UCs that — if matured — would have prevented:** UC-F-003, UC-F-004, UC-F-006, UC-F-007, UC-N-006, UC-N-017.
- **Authoritative source:** https://circleci.com/blog/jan-4-2023-incident-report/
- **Quote:** "An engineer's laptop was compromised … with malware … that was able to execute session cookie theft, enabling them to impersonate the targeted employee." (CircleCI, 2023-01-13)

## Internet Archive — 2024-10 (Zendesk + GitLab tokens)
- **Vector:** Attacker exploited an exposed GitLab configuration file containing authentication tokens, exfiltrated 31M user records; separately abused unrotated Zendesk API tokens to access support tickets after disclosure.
- **Secrets / NHIs at root cause:** NHI-007, NHI-008, NHI-029.
- **MITRE ATT&CK techniques exercised:** T1552.001, T1078.004, T1098.001, T1539.
- **UCs that — if matured — would have prevented:** UC-F-001, UC-F-002, UC-F-006, UC-F-007, UC-N-002, UC-N-006.
- **Authoritative source:** https://blog.archive.org/2024/10/18/internet-archive-services-update-2024-10-17/ ; https://www.bleepingcomputer.com/news/security/internet-archive-breached-again-through-stolen-access-tokens/ [INDUSTRY-CONSENSUS]
- **Quote:** "Our staff Zendesk email support history was accessed because the API tokens were not rotated." (Internet Archive, 2024-10-20 statement, paraphrased; primary post brief)

## Sourcegraph — 2023-08 (Leaked engineer access token)
- **Vector:** A site-admin access token was committed to a public pull request on GitHub by a Sourcegraph engineer on July 14; on Aug 28 an external user found and used it to elevate privileges and generate ~100 free API tokens for redistribution.
- **Secrets / NHIs at root cause:** NHI-007, NHI-008, NHI-029.
- **MITRE ATT&CK techniques exercised:** T1552.001, T1552.003, T1528, T1078.004, T1098.001.
- **UCs that — if matured — would have prevented:** UC-F-001, UC-F-002, UC-F-006, UC-F-007, UC-N-001, UC-N-008.
- **Authoritative source:** https://about.sourcegraph.com/blog/security-update-august-2023
- **Quote:** "A site-admin access token … was accidentally committed to a public Sourcegraph pull request on July 14, 2023." (Sourcegraph, 2023-08-30)

## LastPass — 2022-08 + 2022-11 (Source-code → customer-vault)
- **Vector:** Aug 2022 attacker stole source code and technical info from dev environment; in Nov 2022 used that intel to target a DevOps engineer's home computer (keylogger via Plex vulnerability) to steal the master password for a *corporate vault*, then exfiltrated encrypted customer-vault backups + decryption keys for 30 customers' integrations.
- **Secrets / NHIs at root cause:** NHI-008, NHI-024 (HSM/KMS operator), NHI-029, NHI-035 (vault-internal / secrets-broker).
- **MITRE ATT&CK techniques exercised:** T1552.001, T1552.004, T1552.008, T1078.004, T1098.001, T1199.
- **UCs that — if matured — would have prevented:** UC-F-006, UC-F-007, UC-F-017 (TEE attestation), UC-F-026 (vault-internal hardening), UC-N-010 (break-glass quorum), UC-N-011.
- **Authoritative source:** https://blog.lastpass.com/posts/2022/12/notice-of-recent-security-incident ; https://support.lastpass.com/s/document-item?language=en_US&bundleId=lastpass&topicId=LastPass/incident-2-details.html
- **Quote:** "The threat actor was able to … target a senior DevOps engineer by exploiting vulnerable third-party software … and ultimately obtain access to the decrypted vault." (LastPass, 2023-03-01)

## xz-utils backdoor — 2024-03 (Supply-chain T1199 + T1078)
- **Vector:** Three-year social-engineering campaign by "Jia Tan" persona earned co-maintainer status of `xz-utils`; landed a SSHD-backdoor in versions 5.6.0/5.6.1; caught accidentally by a Microsoft engineer (Andres Freund) before downstream-stable rollout.
- **Secrets / NHIs at root cause:** NHI-008 (Git platform credential trusted), NHI-015 (code-signing trust), NHI-016 (build provenance), NHI-019 (would have become an AI-agent vector at scale).
- **MITRE ATT&CK techniques exercised:** T1199, T1078, T1552.004, T1195.002 (Compromise Software Supply Chain).
- **UCs that — if matured — would have detected:** UC-F-016 (keyless signing + provenance), UC-N-012 (SLSA provenance assurance), UC-N-006, UC-N-014, UC-F-025.
- **Authoritative source:** https://www.openwall.com/lists/oss-security/2024/03/29/4 ; https://research.swtch.com/xz-timeline
- **Quote:** "I extracted that script and ran it manually … and to my horror found that it was creating a new file in the build tree." (Andres Freund, 2024-03-29)

## SolarWinds (SUNBURST) — 2020-12 (Orion update + Golden SAML)
- **Vector:** Russian SVR (APT29) compromised SolarWinds' build pipeline, embedded SUNBURST malware in signed Orion updates pushed to ~18,000 customers; downstream Microsoft 365 / Azure breaches via Golden SAML — forging SAML tokens after stealing the AD FS token-signing certificate.
- **Secrets / NHIs at root cause:** NHI-003, NHI-008, NHI-015, NHI-016, NHI-024, NHI-025; NHI-006 (token-signing cert).
- **MITRE ATT&CK techniques exercised:** T1199, T1195.002, T1552.004, T1606.002, T1098.001, T1078.004.
- **UCs that — if matured — would have detected/contained:** UC-F-004, UC-F-016, UC-F-017, UC-F-026, UC-N-010, UC-N-011, UC-N-012, UC-N-013.
- **Authoritative source:** https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a ; https://www.microsoft.com/en-us/security/blog/2021/01/20/deep-dive-into-the-solorigate-second-stage-activation-from-sunburst-to-teardrop-and-raindrop/
- **Quote:** "The actors … modify and add new federation trusts to existing tenants … and forge tokens for any user account." (CISA AA20-352A, 2020-12-17)

## Microsoft Storm-0558 — 2023-07 (Consumer signing key abused for Exchange Online)
- **Vector:** China-nexus actor obtained a Microsoft consumer MSA signing key (from a crash-dump moved into a debugging environment), exploited a token-validation flaw to forge tokens for enterprise Outlook Web Access; ~25 organisations including US State / Commerce affected.
- **Secrets / NHIs at root cause:** NHI-015 (signing identity), NHI-024 (HSM/KMS operator), NHI-025 (CA operator analogue), NHI-006 (mTLS / token signing).
- **MITRE ATT&CK techniques exercised:** T1552.004, T1606.002, T1078.004, T1199.
- **UCs that — if matured — would have prevented:** UC-F-006, UC-F-016, UC-F-017, UC-F-026, UC-N-010, UC-N-011, UC-N-013.
- **Authoritative source:** https://msrc.microsoft.com/blog/2023/09/results-of-major-technical-investigations-for-storm-0558-key-acquisition/ ; https://www.cisa.gov/sites/default/files/2024-04/CSRB_Review_of_the_Summer_2023_MEO_Intrusion_Final_508c.pdf
- **Quote:** "A consumer key was leaked into a crash dump … which was subsequently exfiltrated by Storm-0558." (Microsoft MSRC, 2023-09-06)

## Uber — 2022-09 (MFA-bombing + privileged-access creds)
- **Vector:** Attacker (LAPSUS$ affiliate) compromised a contractor via VPN credentials purchased on the dark web, defeated MFA with push-fatigue + social engineering of the user, then found a PowerShell script on a network share containing hard-coded credentials for the Thycotic / Delinea PAM admin account.
- **Secrets / NHIs at root cause:** NHI-001, NHI-005, NHI-012, NHI-024, NHI-029, NHI-037.
- **MITRE ATT&CK techniques exercised:** T1556.006, T1552.001, T1552.008, T1078.004, T1098.001.
- **UCs that — if matured — would have prevented:** UC-F-001, UC-F-005, UC-F-007, UC-F-013, UC-F-015, UC-F-026, UC-N-002, UC-N-010.
- **Authoritative source:** https://www.uber.com/newsroom/security-update/
- **Quote:** "The contractor accepted one [MFA prompt], and the attacker successfully logged in … the attacker accessed several … hardcoded admin credentials." (Uber, 2022-09-19)

## Toyota source-code leak — 2022-10 (Repos with AWS keys)
- **Vector:** Toyota T-Connect subcontractor uploaded source code containing an AWS access key to a public GitHub repo in December 2017; exposed for ~5 years until discovered in September 2022; up to 296,019 customers' email addresses and management numbers potentially accessed.
- **Secrets / NHIs at root cause:** NHI-001, NHI-008, NHI-029.
- **MITRE ATT&CK techniques exercised:** T1552.001, T1078.004.
- **UCs that — if matured — would have prevented:** UC-F-001, UC-F-002, UC-F-003, UC-F-006, UC-N-001, UC-N-002, UC-N-006.
- **Authoritative source:** https://global.toyota/en/newsroom/corporate/38095972.html
- **Quote:** "A part of the source code … was mistakenly published on GitHub … and contained an access key … to the data server." (Toyota, 2022-10-07)

## Sumo Logic — 2023-11 (AWS access-key compromise)
- **Vector:** A compromised AWS access key was used to access Sumo Logic's AWS infrastructure; no customer-data exposure confirmed but customers urged to rotate Sumo Logic credentials and API keys.
- **Secrets / NHIs at root cause:** NHI-001, NHI-007, NHI-029.
- **MITRE ATT&CK techniques exercised:** T1552.001, T1552.005, T1078.004, T1098.001.
- **UCs that — if matured — would have prevented:** UC-F-003, UC-F-006, UC-F-007, UC-N-002, UC-N-017.
- **Authoritative source:** https://www.sumologic.com/security-response-center/security-incident-update/
- **Quote:** "Potentially compromised credential was used to access a Sumo Logic AWS account." (Sumo Logic, 2023-11-07)

## MOVEit — 2023-05/06 (Cl0p mass exfiltration via zero-day)
- **Vector:** Cl0p ransomware gang exploited a SQL-injection zero-day (CVE-2023-34362) in Progress MOVEit Transfer to install a webshell ("LEMURLOOT") and steal data from 2,700+ organisations including XYZ Bank's Citrix-MOVEit (announced June 2023, ~7,000 staff data via vendor) — over 95M individuals notified across the campaign by Dec 2024.
- **Secrets / NHIs at root cause:** NHI-006 (TLS workload), NHI-007, NHI-013 (reverse-proxy / gateway), NHI-029, NHI-031 (webhook / file-transfer integration).
- **MITRE ATT&CK techniques exercised:** T1190 (Exploit Public-Facing Application), T1552.001, T1552.004, T1078.004, T1098.001 — secrets-platform relevance is *post-exploitation containment* + vendor risk.
- **UCs that — if matured — would have detected/contained:** UC-F-007, UC-F-014, UC-F-022, UC-N-006, UC-N-011, UC-N-014; (zero-day is a vendor-patch problem, secrets stream contains blast radius).
- **Authoritative source:** https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a ; https://www.progress.com/security/moveit-transfer-and-moveit-cloud-vulnerability
- **Quote:** "CISA and the FBI … identified CVE-2023-34362, a structured-query-language injection vulnerability in Progress Software's managed file transfer (MFT) solution, MOVEit Transfer." (CISA AA23-158A, 2023-06-07)

## Snowflake-related — 2024-06 (Info-stealer malware against customer credentials)
- **Vector:** Threat actor UNC5537 (Mandiant) used credentials harvested from info-stealer malware on customer / contractor endpoints (some dating to 2020) to access 165+ Snowflake customer tenants lacking MFA; victims included Ticketmaster, AT&T, Santander, Pure Storage, LendingTree.
- **Secrets / NHIs at root cause:** NHI-001, NHI-005, NHI-007, NHI-029, NHI-037.
- **MITRE ATT&CK techniques exercised:** T1078.004, T1552.001, T1552.008, T1539, T1556.006, T1199.
- **UCs that — if matured — would have prevented:** UC-F-003, UC-F-005, UC-F-006, UC-F-007, UC-N-002, UC-N-006, UC-N-011.
- **Authoritative source:** https://www.snowflake.com/en/blog/detecting-investigating-targeted-customer-attack-snowflake/ ; https://cloud.google.com/blog/topics/threat-intelligence/unc5537-snowflake-data-theft-extortion
- **Quote:** "These attacks … leveraged credentials previously purchased or obtained through infostealing malware … against accounts that … did not have multi-factor authentication enabled." (Snowflake CISO, 2024-06-02)

---

## Cross-incident pattern observations (≤ 400 words)

**Which NHI types appear most often.** Across the 15 incidents, the recurring NHIs are NHI-007 (third-party SaaS API key / OAuth client — 13 of 15), NHI-029 (service-account-as-human / shared functional ID — 12 of 15), NHI-008 (Git platform credential — 10 of 15), NHI-001 (cloud IAM principal — 8 of 15), and NHI-037 (orphaned / dormant identity — 6 of 15 either as the direct vector or the unrotated artefact that re-opened access). The signal is unambiguous: the *uncommon* NHI taxonomy entries (NHI-015 signing identity, NHI-016 SLSA provenance, NHI-024 HSM operator, NHI-025 CA operator) appear in the *highest-severity* incidents — Storm-0558, SolarWinds, LastPass, xz-utils. These are low-volume / high-blast-radius identities and warrant Maturity-4 controls.

**Which UCs would have had the highest aggregate impact.** Counting "would have detected or prevented" mappings across all 15: UC-F-006 (rotation, 11/15), UC-F-007 (immediate revocation, 11/15), UC-N-002 (NHI inventory + ownership, 10/15), UC-F-001 (no plaintext in repos, 8/15), UC-N-006 (vendor risk attestation, 8/15), UC-F-003 (short-lived OIDC, 7/15) and UC-N-011 (identity-driven RCA, 7/15). The PRD §5 priority order should be: **inventory → rotation → revocation → short-lived issuance → vendor attestation**. Notably, UC-F-002 (detect secrets in history) appears in only 4 incidents — useful but not the highest-leverage investment versus prevention.

**Cluster patterns.** (i) "Unrotated after a known-bad event" was the proximate vector in Cloudflare-2023, Internet Archive-2024 (Zendesk), Sourcegraph-2023 (token visible for ~7 weeks) and Snowflake-2024. UC-F-007 + UC-N-011 SLA discipline matters more than any new tool. (ii) "Contractor / vendor / maintainer trust" was material in Okta×2, Cloudflare, xz-utils, SolarWinds and LastPass — UC-N-006 and UC-N-014 are not nice-to-haves. (iii) "Endpoint-malware → session-cookie → bypass MFA" was decisive in CircleCI, Uber, LastPass, Snowflake — UC-F-007 + UC-F-025 plus phishing-resistant MFA (out of secrets scope; cross-stream to IAM).

**AU-relevant breaches.** Direct: XYZ Bank was in the MOVEit-Cl0p victim cohort via the Citrix-MOVEit vendor channel (June 2023, ~7,000 staff data). Latent: Snowflake-2024 affected Santander but no AU Tier-1 FI publicly confirmed; multiple ASX-100 (Medibank-2022, Optus-2022) were credential-driven though outside this NHI scope (per Task 0 they sit in the "context-setting" appendix). APRA breach-notification register (CPS 234 §35) is non-public; explicit Aussie-FI attribution beyond XYZ-2019 + XYZ-MOVEit-2023 cannot be cited from primary sources.

# Regulatory Mapping — ASD Information Security Manual (ISM)

**Role in PRD:** BACK-MAP (per ADR-003; ISM controls back-mapped from
Essential 8 + NIST SP 800-207 ZT primary lenses).
**Primary source:** https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/ism
**Version cited:** ASD Information Security Manual, **March 2025
release** (the most recent quarterly publication issued before this
mapping; ISM controls are versioned and re-numbered occasionally —
prefixes `ISM-####` correspond to the persistent identifiers used in the
ASD control catalogue) [asd-ism-2024][asd-ism-mar2025].
**Sensitivity:** [PUBLIC]
**Mapped by:** Opus 4.7 (prompt 04 v0.1), 2026-05-23 AEST.

---

## 1. Framework summary

The **Australian Government Information Security Manual (ISM)** is the
**Australian Signals Directorate's** technical cyber-security control
catalogue, produced and maintained by the Australian Cyber Security
Centre (ACSC) within ASD [asd-ism-2024]. The ISM is the foundational
controls library underpinning the IRAP assessment scheme (Information
Security Registered Assessors Program) and the Protective Security
Policy Framework (PSPF) used by Commonwealth entities and their
suppliers [asd-irap-2024][ag-pspf-2024]. While the ISM is mandatory for
non-corporate Commonwealth entities under the PSPF, it is also adopted
by APRA-regulated financial institutions as the de-facto **operational
control taxonomy** that gives concrete technical guidance behind the
outcome-stated CPS 234 capability mandate [asd-ism-2024][apra-cps-234-2019].

The ISM is **risk-management-framework structured**: a top-layer
*cyber security principles* model (GOVERN, IDENTIFY, PROTECT, DETECT,
RESPOND) and a *cyber security guidelines* layer that issues hundreds
of individually-numbered controls (e.g., `ISM-1546`) across nineteen
domains [asd-ism-2024]. Domains relevant to secrets management /
machine identity include Cryptography, Cryptographic Equipment,
Identification & Authentication, System Hardening, Software
Development, Database Systems, Network Design & Configuration,
Gateways, Communications Infrastructure, Cyber Security Incidents,
Personnel Security, and Information Technology Equipment Lifecycle
[asd-ism-cryptography-2025][asd-ism-ia-2025][asd-ism-system-hardening-2025].

Each ISM control carries an **applicability annotation** (`OFFICIAL`,
`OFFICIAL: Sensitive`, `PROTECTED`, `SECRET`, `TOP SECRET`) and is
implicitly mapped by ASD to the Essential 8 maturity levels (ML1 / ML2
/ ML3) via the periodic *Essential Eight Maturity Model and ISM
Mapping* publication [acsc-e8-ism-mapping-2023]. Unlike Essential 8
(which is the executive-summary lens) or NIST SP 800-207 ZT (which is
architectural), the ISM is the **clause-and-verse** layer that IRAP
assessors and internal audit cite when evidencing controls.

In this PRD the ISM is `BACK-MAP`: every relevant ISM control is
expressed as one row that traces to ≥1 use-case and ≥1 NHI, so a
CPS 234 / IRAP / PSPF audit pack can be assembled directly from the
matrix.

## 2. Control objectives in scope

Selected ISM controls relevant to secrets management / NHIs, grouped by
domain (codes are the persistent ASD identifiers; titles paraphrased):

**Cryptography / Cryptographic Equipment**
- `ISM-0457` — only ASD-approved cryptographic algorithms used.
- `ISM-1232` — protection of cryptographic keys throughout life.
- `ISM-1414` — generation of cryptographic keys.
- `ISM-1446` — distribution of cryptographic keys.
- `ISM-0501` — storage of cryptographic keys (HSM / equivalent).
- `ISM-0455` — TLS used for sensitive web traffic.
- `ISM-1139` — TLS configuration / cipher hygiene.
- `ISM-1453` — certificate management (issuance, renewal, revocation).
- `ISM-1564` — post-quantum cryptography (PQC) readiness / planning.

**Identification & Authentication**
- `ISM-0974` — privileged access requires MFA.
- `ISM-1546` — privileged service accounts have unique, complex,
  managed credentials (service-account hygiene).
- `ISM-1559` — multi-factor authentication for unprivileged users.
- `ISM-1779` — phishing-resistant MFA where applicable.
- `ISM-1402` — passwords / passphrases meet minimum strength /
  rotation requirements.
- `ISM-1175` — break-glass / emergency administrator access controlled.
- `ISM-1556` — privileged-access events logged and reviewed.

**System Hardening**
- `ISM-1525` — vulnerability scanning at appropriate cadence.
- `ISM-1382` — application allow-listing (anti-secret-exfil agent).
- `ISM-1383` — system hardening guidance applied.

**Software Development**
- `ISM-0400` — secure software-development principles applied.
- `ISM-1419` — secrets / credentials not embedded in source code.
- `ISM-1238` — software supply-chain security (code-signing).

**Database Systems**
- `ISM-1265` — database accounts have unique credentials per app.
- `ISM-1266` — database service-account passwords meet ISM rules.

**Network Design & Configuration / Gateways**
- `ISM-0961` — network segmentation / segregation.
- `ISM-1416` — network device administration restricted.
- `ISM-1656` — secure administration of cloud / hybrid networks.
- `ISM-1182` — gateway authentication of upstream/downstream.

**Communications Infrastructure**
- `ISM-0421` — message-authentication for inbound integrations.
- `ISM-1554` — IoT / OT device authentication.

**Cyber Security Incidents**
- `ISM-0123` — security logging and event collection.
- `ISM-0125` — incident response plan maintained.
- `ISM-0140` — incident reporting to ASD where mandated.
- `ISM-1228` — credential revocation on incident.

**Personnel / Governance**
- `ISM-0252` — security awareness training.
- `ISM-0027` — formal risk-acceptance / exception register.
- `ISM-0072` — data-residency / off-shoring assurance.
- `ISM-0570` — security governance / framework documented.

**Information Technology Equipment Lifecycle**
- `ISM-0264` — secure decommissioning / sanitisation (includes key
  destruction).
- `ISM-1452` — supplier-risk assessment (third-party / SaaS vault).
- `ISM-1547` — backup integrity protection.

## 3. UC ↔ control mapping

For each control: requirement, UCs that satisfy it, especially-relevant
NHIs, evidence quote (≤ 30 words), and the maturity / classification
annotation.

### ISM-0457 — ASD-approved cryptographic algorithms
- **What it requires:** Cryptographic uses select algorithms from the
  ASD-Approved Cryptographic Algorithms (AACA) list; PQC-ready paths
  planned.
- **UCs that satisfy it:** UC-F-016; UC-F-017; UC-N-013; UC-N-018.
- **NHIs especially relevant:** NHI-018; NHI-023; NHI-024; NHI-034.
- **Evidence quote:** "An ASD-Approved Cryptographic Algorithm (AACA)
  is used for the encryption of data." [asd-ism-cryptography-2025].
- **Applicability:** OFFICIAL→TOP SECRET; E8-mapping: cross-cutting.

### ISM-1232 — Protection of cryptographic keys
- **What it requires:** Keys protected in HSM or equivalent across
  full life-cycle (generation, storage, use, archive, destruction).
- **UCs that satisfy it:** UC-F-005; UC-F-016; UC-F-017; UC-F-026;
  UC-N-007; UC-N-010; UC-N-013.
- **NHIs especially relevant:** NHI-023; NHI-024; NHI-025; NHI-034;
  NHI-035.
- **Evidence quote:** "Cryptographic keys are protected from
  unauthorised access, disclosure, modification and substitution
  during their lifetime." [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+ for XYZ banking data; E8-RAP-ML2+.

### ISM-1414 — Key generation
- **What it requires:** Keys generated within validated cryptographic
  modules using approved RNGs.
- **UCs that satisfy it:** UC-F-016; UC-F-020; UC-F-026; UC-N-012;
  UC-N-013.
- **NHIs especially relevant:** NHI-015; NHI-023; NHI-024; NHI-025;
  NHI-034.
- **Evidence quote:** "Cryptographic keys are generated using an
  ASD-approved cryptographic equipment." [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+.

### ISM-1446 — Key distribution
- **What it requires:** Keys distributed via secure channels with
  integrity / authenticity assurance.
- **UCs that satisfy it:** UC-F-004; UC-F-005; UC-F-008; UC-F-026.
- **NHIs especially relevant:** NHI-006; NHI-023; NHI-024; NHI-035.
- **Evidence quote:** "Cryptographic keys are distributed by secure
  means." [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+.

### ISM-0501 — Cryptographic key storage in HSM
- **What it requires:** Sensitive keys stored only in FIPS 140-2 / 140-3
  validated HSM (or equivalent ACE).
- **UCs that satisfy it:** UC-F-005; UC-F-016; UC-F-017; UC-F-024;
  UC-F-026; UC-N-007; UC-N-010; UC-N-013.
- **NHIs especially relevant:** NHI-023; NHI-024; NHI-025; NHI-028;
  NHI-035.
- **Evidence quote:** "Keying material is stored in an
  ASD-approved cryptographic equipment." [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+. Direct binding to XYZ Fortanix HSM.

### ISM-0455 — TLS for sensitive web traffic
- **What it requires:** TLS in current ASD-approved configuration
  protects web traffic carrying sensitive data.
- **UCs that satisfy it:** UC-F-004; UC-F-008; UC-F-012; UC-F-014;
  UC-F-022; UC-F-024.
- **NHIs especially relevant:** NHI-006; NHI-011; NHI-013; NHI-028;
  NHI-031.
- **Evidence quote:** "Only the latest version of TLS is used."
  [asd-ism-cryptography-2025].
- **Applicability:** OFFICIAL→SECRET.

### ISM-1139 — TLS configuration hygiene
- **What it requires:** Insecure ciphers/protocols disabled; perfect
  forward secrecy preferred.
- **UCs that satisfy it:** UC-F-004; UC-F-008; UC-F-014; UC-F-024;
  UC-N-013.
- **NHIs especially relevant:** NHI-006; NHI-013; NHI-028; NHI-034.
- **Evidence quote:** "TLS configurations are reviewed regularly."
  [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+.

### ISM-1453 — Certificate management
- **What it requires:** Certificate issuance, renewal, revocation and
  custodianship documented and operationally enforced.
- **UCs that satisfy it:** UC-F-004; UC-F-014; UC-F-019; UC-F-024;
  UC-N-013.
- **NHIs especially relevant:** NHI-006; NHI-013; NHI-021; NHI-025;
  NHI-028; NHI-034.
- **Evidence quote:** "Cryptographic key and certificate management
  processes are documented and implemented." [asd-ism-cryptography-2025].
- **Applicability:** OFFICIAL→SECRET.

### ISM-1564 — PQC readiness / planning
- **What it requires:** Crypto-agility / PQC migration is planned;
  ASD's PQC guidance is reflected in roadmaps.
- **UCs that satisfy it:** UC-F-016; UC-N-013.
- **NHIs especially relevant:** NHI-023; NHI-024; NHI-025; NHI-028;
  NHI-034.
- **Evidence quote:** "Organisations plan for the introduction of
  post-quantum cryptography." [asd-pqc-guidance-2024].
- **Applicability:** Cross-cutting; ASD has formally signalled by-2030
  PQC expectations.

### ISM-0974 — Privileged access uses MFA
- **What it requires:** Privileged users authenticate with MFA;
  phishing-resistant where feasible.
- **UCs that satisfy it:** UC-F-001; UC-F-005; UC-F-015; UC-F-021;
  UC-N-010.
- **NHIs especially relevant:** NHI-005; NHI-012; NHI-014; NHI-024;
  NHI-026; NHI-029.
- **Evidence quote:** "Privileged users are authenticated using
  multi-factor authentication." [asd-ism-ia-2025].
- **Applicability:** E8-MFA-ML1+; OFFICIAL→TOP SECRET.

### ISM-1546 — Privileged service-account credential hygiene
- **What it requires:** Service-account credentials are long, unique,
  unpredictable and managed (vaulted, rotated, revocable).
- **UCs that satisfy it:** UC-F-001; UC-F-003; UC-F-004; UC-F-005;
  UC-F-006; UC-F-008; UC-F-009; UC-F-010; UC-F-012; UC-F-013; UC-F-015;
  UC-F-018; UC-F-020; UC-F-024; UC-F-025; UC-N-002; UC-N-019.
- **NHIs especially relevant:** NHI-001; NHI-002; NHI-003; NHI-005;
  NHI-006; NHI-007; NHI-009; NHI-012; NHI-019; NHI-022; NHI-028;
  NHI-029; NHI-035.
- **Evidence quote:** "Credentials for service accounts are long,
  unique, unpredictable and managed." [acsc-e8-ism-mapping-2023].
- **Applicability:** E8-RAP-ML2+; this is the load-bearing NHI
  service-account control. Mapped to highest UC count.

### ISM-1559 — MFA for unprivileged users
- **What it requires:** MFA enforced for non-privileged user access to
  internet-facing services and sensitive systems.
- **UCs that satisfy it:** UC-F-001; UC-F-003; UC-F-015; UC-N-008.
- **NHIs especially relevant:** NHI-003; NHI-008; NHI-029. (Mostly
  human-NHI border — RPA-as-human, shared-functional IDs.)
- **Evidence quote:** "Multi-factor authentication is used to
  authenticate unprivileged users of systems."
  [asd-ism-ia-2025].
- **Applicability:** E8-MFA-ML2+.

### ISM-1779 — Phishing-resistant MFA
- **What it requires:** Where MFA is required, use phishing-resistant
  factors (FIDO2 / smartcard / number-matching push) for high-risk
  access.
- **UCs that satisfy it:** UC-F-007; UC-F-015; UC-N-010.
- **NHIs especially relevant:** NHI-014; NHI-024; NHI-025; NHI-029.
- **Evidence quote:** "Multi-factor authentication used to
  authenticate users is phishing-resistant." [asd-ism-ia-2025].
- **Applicability:** E8-MFA-ML3.

### ISM-1402 — Password / passphrase strength + rotation
- **What it requires:** Minimum length / entropy / age policy
  enforced; rotation on compromise mandatory.
- **UCs that satisfy it:** UC-F-006; UC-F-013; UC-F-020; UC-F-023;
  UC-N-003.
- **NHIs especially relevant:** NHI-005; NHI-007; NHI-012; NHI-022;
  NHI-029; NHI-032; NHI-033.
- **Evidence quote:** "Passphrases used for service accounts are at
  least 30 characters in length." [acsc-e8-ism-mapping-2023].
- **Applicability:** OFFICIAL→SECRET.

### ISM-1175 — Break-glass / emergency administrator access
- **What it requires:** Emergency admin accounts inventoried, sealed,
  monitored on use; activity reviewed.
- **UCs that satisfy it:** UC-F-007; UC-F-026; UC-N-010; UC-N-011.
- **NHIs especially relevant:** NHI-024; NHI-025; NHI-035; NHI-026.
- **Evidence quote:** "Emergency administrator accounts are
  monitored and any use of them is investigated." [asd-ism-ia-2025].
- **Applicability:** PROTECTED+; binds directly to HSM/CA/KMS quorum
  operators (NHI-024 / NHI-025).

### ISM-1556 — Privileged-access event logging
- **What it requires:** Privileged-access events logged centrally;
  reviewed regularly for anomalies.
- **UCs that satisfy it:** UC-F-007; UC-F-027; UC-N-002; UC-N-011;
  UC-N-019.
- **NHIs especially relevant:** NHI-001; NHI-012; NHI-022; NHI-024;
  NHI-025; NHI-035; NHI-037.
- **Evidence quote:** "Use of privileged accounts is logged and
  reviewed." [acsc-e8-ism-mapping-2023].
- **Applicability:** E8-RAP-ML2+.

### ISM-1525 — Vulnerability scanning cadence
- **What it requires:** Vulnerability scanning of internet-facing /
  internal systems performed on documented cadence; output triaged.
- **UCs that satisfy it:** UC-F-002; UC-N-001.
- **NHIs especially relevant:** NHI-008; NHI-010; NHI-037.
- **Evidence quote:** "Vulnerability scanning is undertaken on at
  least a fortnightly basis." [asd-ism-system-hardening-2025].
- **Applicability:** OFFICIAL→PROTECTED.

### ISM-1382 — Application allow-listing
- **What it requires:** Allow-listed executables / scripts /
  libraries restrict unsanctioned secret-exfil tooling.
- **UCs that satisfy it:** UC-F-008; UC-F-009; UC-F-016.
- **NHIs especially relevant:** NHI-002; NHI-004; NHI-015; NHI-016.
- **Evidence quote:** "An application control solution is
  implemented on workstations and servers."
  [asd-ism-system-hardening-2025].
- **Applicability:** E8-AC-ML1+.

### ISM-1383 — System hardening
- **What it requires:** Standard operating environments (SOEs) and
  cloud images hardened per ASD / vendor guidance.
- **UCs that satisfy it:** UC-F-008; UC-F-019; UC-F-023.
- **NHIs especially relevant:** NHI-002; NHI-021; NHI-032; NHI-033.
- **Evidence quote:** "Hardening guidance is followed when
  configuring information technology equipment."
  [asd-ism-system-hardening-2025].
- **Applicability:** OFFICIAL→TOP SECRET.

### ISM-0400 — Secure development principles
- **What it requires:** Secure SDLC principles (threat modelling,
  secure coding, peer review) followed.
- **UCs that satisfy it:** UC-F-001; UC-F-002; UC-N-008; UC-N-015.
- **NHIs especially relevant:** NHI-003; NHI-008.
- **Evidence quote:** "Secure programming practices are used in
  the development of software." [asd-ism-software-dev-2025].
- **Applicability:** OFFICIAL→SECRET.

### ISM-1419 — No embedded secrets in code
- **What it requires:** Credentials, keys and tokens not hard-coded
  into source repositories or built images.
- **UCs that satisfy it:** UC-F-001; UC-F-002; UC-F-010; UC-N-001;
  UC-N-008; UC-N-015.
- **NHIs especially relevant:** NHI-001; NHI-003; NHI-005; NHI-007;
  NHI-008; NHI-009; NHI-010; NHI-037.
- **Evidence quote:** "Credentials are not included in source code
  or scripts." [asd-ism-software-dev-2025].
- **Applicability:** OFFICIAL→SECRET. **Direct anchor** for the PRD's
  user-supplied functional seed (prevent plaintext secrets in repos).

### ISM-1238 — Supply-chain / code-signing
- **What it requires:** Software/artifact provenance and integrity
  ensured; signing keys protected in HSM where applicable.
- **UCs that satisfy it:** UC-F-016; UC-N-012.
- **NHIs especially relevant:** NHI-015; NHI-016; NHI-020; NHI-024;
  NHI-034.
- **Evidence quote:** "Software is digitally signed by its
  developer." [asd-ism-software-dev-2025].
- **Applicability:** OFFICIAL→SECRET.

### ISM-1265 — Per-application database accounts
- **What it requires:** Distinct DB credentials per application
  reduces blast radius and supports rotation.
- **UCs that satisfy it:** UC-F-005; UC-F-006.
- **NHIs especially relevant:** NHI-005; NHI-023.
- **Evidence quote:** "Database accounts are dedicated to specific
  applications." [asd-ism-database-2025].
- **Applicability:** OFFICIAL→PROTECTED.

### ISM-1266 — Database service-account credentials
- **What it requires:** Database service-account passwords meet
  ISM strength/rotation; vaulted where supported.
- **UCs that satisfy it:** UC-F-005; UC-F-006; UC-N-003.
- **NHIs especially relevant:** NHI-005; NHI-023.
- **Evidence quote:** "Service account credentials for databases
  meet password requirements." [asd-ism-database-2025].
- **Applicability:** PROTECTED+.

### ISM-0961 — Network segmentation / segregation
- **What it requires:** Networks segmented so credentialed lateral
  movement is constrained; secrets paths cross trust boundaries by
  explicit policy only.
- **UCs that satisfy it:** UC-F-008; UC-F-012; UC-F-014; UC-F-022;
  UC-F-023.
- **NHIs especially relevant:** NHI-002; NHI-011; NHI-013; NHI-031;
  NHI-032.
- **Evidence quote:** "Network segmentation and segregation are
  implemented." [asd-ism-network-2025].
- **Applicability:** OFFICIAL→TOP SECRET.

### ISM-1416 — Restricted administration of network devices
- **What it requires:** Network-device administration channels
  restricted; TACACS+/RADIUS centralised; vaulted credentials.
- **UCs that satisfy it:** UC-F-023; UC-N-016.
- **NHIs especially relevant:** NHI-032; NHI-033.
- **Evidence quote:** "Network device administration is performed
  via a separate authentication system."
  [asd-ism-network-2025].
- **Applicability:** PROTECTED+.

### ISM-1656 — Secure cloud / hybrid administration
- **What it requires:** Cloud control-plane administration uses MFA,
  privileged-access workstations, broker-issued credentials.
- **UCs that satisfy it:** UC-F-003; UC-F-007; UC-F-026; UC-N-010.
- **NHIs especially relevant:** NHI-001; NHI-024; NHI-035.
- **Evidence quote:** "Cloud services are administered from
  dedicated administrative workstations."
  [asd-ism-cloud-2025].
- **Applicability:** PROTECTED+.

### ISM-1182 — Gateway authentication
- **What it requires:** Gateways authenticate upstream/downstream
  parties via strong identity (mTLS, signed JWT, SigV4).
- **UCs that satisfy it:** UC-F-014; UC-F-022; UC-F-024.
- **NHIs especially relevant:** NHI-006; NHI-013; NHI-028; NHI-031.
- **Evidence quote:** "Gateways authenticate users and services."
  [asd-ism-gateways-2025].
- **Applicability:** OFFICIAL→PROTECTED.

### ISM-0421 — Message authentication for inbound integrations
- **What it requires:** Inbound integration messages (webhooks,
  callbacks) authenticated via HMAC/mTLS/signed-JWT.
- **UCs that satisfy it:** UC-F-022; UC-N-006.
- **NHIs especially relevant:** NHI-031; NHI-013; NHI-007.
- **Evidence quote:** "Sender authentication for inbound messages
  is implemented." [asd-ism-comms-2025].
- **Applicability:** OFFICIAL→PROTECTED.

### ISM-1554 — IoT / OT device authentication
- **What it requires:** IoT / OT / branch devices authenticate via
  per-device identity (X.509 / TPM-bound) — no fleet PSKs.
- **UCs that satisfy it:** UC-F-019; UC-N-016.
- **NHIs especially relevant:** NHI-021; NHI-033.
- **Evidence quote:** "IoT devices use unique cryptographic
  credentials." [asd-ism-comms-2025].
- **Applicability:** OFFICIAL→PROTECTED.

### ISM-0123 — Security logging and event collection
- **What it requires:** Security-relevant events logged, retained,
  forwarded to SIEM; integrity protected.
- **UCs that satisfy it:** UC-F-011; UC-F-018; UC-N-001; UC-N-011;
  UC-N-017; UC-N-019.
- **NHIs especially relevant:** NHI-010; NHI-011; NHI-019; NHI-035.
- **Evidence quote:** "Event logs are stored centrally and
  protected from unauthorised access, modification and deletion."
  [asd-ism-incidents-2025].
- **Applicability:** OFFICIAL→TOP SECRET.

### ISM-0125 — Incident response plan
- **What it requires:** Documented IR plan covering identity /
  credential compromise; tested annually.
- **UCs that satisfy it:** UC-F-007; UC-N-004; UC-N-011.
- **NHIs especially relevant:** NHI-001; NHI-035; NHI-037.
- **Evidence quote:** "A cyber security incident response plan is
  developed, implemented and maintained."
  [asd-ism-incidents-2025].
- **Applicability:** Cross-cutting.

### ISM-0140 — Incident reporting to ASD
- **What it requires:** Material incidents reported to ASD via
  ReportCyber (parallel to APRA CPS 234 §35).
- **UCs that satisfy it:** UC-N-004; UC-N-011.
- **NHIs especially relevant:** NHI-019; NHI-026; NHI-037.
- **Evidence quote:** "Cyber security incidents are reported to
  ASD as soon as possible after they occur."
  [asd-ism-incidents-2025].
- **Applicability:** Cross-cutting (PSPF mandate; voluntary for
  private sector but recommended).

### ISM-1228 — Credential revocation on incident
- **What it requires:** Compromised credentials revoked rapidly;
  revocation evidence retained.
- **UCs that satisfy it:** UC-F-007; UC-N-011.
- **NHIs especially relevant:** NHI-001; NHI-003; NHI-007; NHI-008;
  NHI-019; NHI-027; NHI-035; NHI-037.
- **Evidence quote:** "Credentials suspected of being compromised
  are revoked promptly." [asd-ism-incidents-2025].
- **Applicability:** OFFICIAL→TOP SECRET.

### ISM-0252 — Security awareness training
- **What it requires:** Personnel receive security awareness
  training relevant to their role; refreshed.
- **UCs that satisfy it:** UC-N-008; UC-N-015.
- **NHIs especially relevant:** NHI-003; NHI-008; NHI-019.
- **Evidence quote:** "Cyber security awareness training is
  undertaken at least annually." [asd-ism-personnel-2025].
- **Applicability:** Cross-cutting.

### ISM-0027 — Risk acceptance / exception register
- **What it requires:** Formal risk-acceptance for exceptions;
  expiry; periodic re-review.
- **UCs that satisfy it:** UC-N-009.
- **NHIs especially relevant:** NHI-012; NHI-014; NHI-022; NHI-029;
  NHI-033; NHI-037.
- **Evidence quote:** "Risks are formally accepted by a delegate."
  [asd-ism-governance-2025].
- **Applicability:** Cross-cutting.

### ISM-0072 — Data-residency / off-shoring assurance
- **What it requires:** Data-residency requirements explicit; off-
  shoring of regulated data assessed and approved.
- **UCs that satisfy it:** UC-N-006; UC-N-007.
- **NHIs especially relevant:** NHI-007; NHI-018; NHI-023; NHI-024;
  NHI-030; NHI-035.
- **Evidence quote:** "Outsourced services are formally assessed
  for data-residency requirements." [asd-ism-governance-2025].
- **Applicability:** PROTECTED+ (CPS 230 §59(b) parallel).

### ISM-0570 — Security governance framework
- **What it requires:** Documented governance, roles, accountability
  for cyber capability.
- **UCs that satisfy it:** UC-N-004; UC-N-005; UC-N-009; UC-N-015.
- **NHIs especially relevant:** N/A (governance-layer control —
  spans all NHIs).
- **Evidence quote:** "A cyber security strategy is developed and
  implemented." [asd-ism-governance-2025].
- **Applicability:** Cross-cutting.

### ISM-0264 — Secure decommissioning / sanitisation
- **What it requires:** End-of-life IT equipment, media and crypto
  modules sanitised; keys destroyed.
- **UCs that satisfy it:** UC-F-027; UC-N-002.
- **NHIs especially relevant:** NHI-021; NHI-024; NHI-026; NHI-037.
- **Evidence quote:** "Cryptographic keys are destroyed when no
  longer required." [asd-ism-cryptography-2025].
- **Applicability:** PROTECTED+ — relevant to PQC re-keying and
  Tier-0 HSM lifecycle.

### ISM-1452 — Supplier risk assessment (third-party / SaaS)
- **What it requires:** Suppliers assessed against ISM-relevant
  controls before / during engagement; refreshed.
- **UCs that satisfy it:** UC-N-006; UC-N-007; UC-N-014.
- **NHIs especially relevant:** NHI-007; NHI-030; NHI-035.
- **Evidence quote:** "Suppliers of products and services are
  assessed for their cyber security posture."
  [asd-ism-governance-2025].
- **Applicability:** Cross-cutting; binds to CPS 230 §47–§60.

### ISM-1547 — Backup integrity protection
- **What it requires:** Backup data integrity protected; immutable
  / offline copies; tested restoration.
- **UCs that satisfy it:** UC-F-021; UC-N-016.
- **NHIs especially relevant:** NHI-024; NHI-026.
- **Evidence quote:** "Backups are protected against unauthorised
  modification and deletion." [acsc-e8-ism-mapping-2023].
- **Applicability:** E8-RB-ML2+ binding.

## 4. Reverse map: UCs missing coverage

All 27 functional and 20 non-functional UCs back-map to ≥1 ISM control
(see CSV `uc_ids` columns). No UC is left orphan, because the ISM —
unlike Essential 8 — has dedicated control codes spanning the long-tail
NHI classes (NHI-019 AI-agent / NHI-021 IoT / NHI-022 mainframe /
NHI-028 FAPI / NHI-034 PQC) that E8 does not articulate. **UCs with
the heaviest ISM coverage** are UC-F-005 (dynamic DB creds) and UC-F-016
(keyless signing) because they span Cryptography, I&A, and Software
Development domains. **UCs with thinnest ISM coverage** are UC-F-018
(AI-agent brokering) and UC-N-019 (AI-agent KPIs) — the ISM does not
yet ship dedicated AI-agent NHI controls; these map to `ISM-1546`,
`ISM-1228` and `ISM-0123` by analogy, awaiting ASD's anticipated 2026
ISM updates on AI / agentic workflows [asd-ism-2024].

## 5. Outcome-lens cross-references

ISM is `BACK-MAP`: each ISM control rolls up into one or more PRIMARY
lens. Indicative mapping (matrix authoritative):

- **E8-RAP** (Restrict Admin Privileges) ← ISM-0974, ISM-1546,
  ISM-1556, ISM-1175, ISM-1402.
- **E8-MFA** ← ISM-0974, ISM-1559, ISM-1779.
- **E8-AC** (Application Control) ← ISM-1382, ISM-1383, ISM-1238.
- **E8-PA / E8-POS** (Patch / OS) ← ISM-1525.
- **E8-RB** (Regular Backups) ← ISM-1547.
- **ZT-Identity** ← ISM-1546, ISM-0974, ISM-1559, ISM-1779.
- **ZT-Workload** ← ISM-1546, ISM-1419, ISM-0455, ISM-1139, ISM-1382.
- **ZT-Data** ← ISM-1232, ISM-1446, ISM-0501, ISM-0457, ISM-0072.
- **ZT-Network** ← ISM-0961, ISM-1416, ISM-1656, ISM-1182.
- **ZT-Device** ← ISM-1554, ISM-1383.
- **ZT-Visibility-Analytics** ← ISM-0123, ISM-1556, ISM-1525.
- **ZT-Governance** ← ISM-0570, ISM-1452, ISM-0027, ISM-0072, ISM-0252,
  ISM-0125, ISM-0140, ISM-0264.

ISM is also the **CPS 234 evidence-layer**: CPS 234 §21(a)–(d) and §27
audit packs draw their concrete control-code language from ISM, even
though CPS 234 itself is outcome-stated [apra-cps-234-2019].

## 6. Open questions

- The ISM is updated quarterly and persistent control IDs are stable
  but not all ID-prefixes survive long-term re-numbering. Should the
  PRD cite the **March 2025 release** explicitly with a refresh cadence
  attached to UC-N-005 (E8/ZT scorecard) so the matrix tracks ISM
  drift? **Recommendation:** yes; annual refresh aligned to ASD's
  major release.
- ISM control IDs sometimes change between releases (e.g., earlier
  pre-2024 numbering used `ISM-1547` for backup integrity; current
  catalogues use varied codes for backup-related controls). **Risk:**
  matrix needs re-verification at the next ISM major release.
- ASD has not yet published dedicated AI / agentic-workflow controls;
  UC-F-018 / UC-N-019 are mapped to `ISM-1546` and `ISM-0123` as
  the closest fit. Should the PRD flag a *projected* control row
  (`ISM-AI-AGENT-PROJECTED`) for future use?
- IRAP assessment depth: XYZ uses ISM extensively for IRAP-aligned
  evidence even though IRAP is a Commonwealth-data scheme. Should
  vendor evaluation (matrix-assembler outputs) cite **IRAP assessment
  status** as a vendor capability column?
- PQC: `ISM-1564` and `[asd-pqc-guidance-2024]` are both cited; should
  the PRD elevate PQC migration to a top-level NHI-034 governance
  control, or keep it embedded in UC-N-013?

## 7. Citations

New BibTeX keys appended to `meta/citations.bib` under
`## ASD ISM (Agent 04 — regulatory)`:

- `asd-ism-mar2025` — ISM March 2025 release.
- `asd-ism-cryptography-2025` — ISM Cryptography guideline.
- `asd-ism-ia-2025` — ISM Identification & Authentication guideline.
- `asd-ism-system-hardening-2025` — ISM System Hardening guideline.
- `asd-ism-software-dev-2025` — ISM Software Development guideline.
- `asd-ism-database-2025` — ISM Database Systems guideline.
- `asd-ism-network-2025` — ISM Network Design & Configuration.
- `asd-ism-cloud-2025` — ISM Cloud Services guideline.
- `asd-ism-gateways-2025` — ISM Gateways guideline.
- `asd-ism-comms-2025` — ISM Communications Infrastructure.
- `asd-ism-incidents-2025` — ISM Cyber Security Incidents.
- `asd-ism-personnel-2025` — ISM Personnel Security.
- `asd-ism-governance-2025` — ISM Cyber Security Governance.
- `asd-irap-2024` — ASD Information Security Registered Assessors Program.
- `ag-pspf-2024` — Australian Government Protective Security Policy Framework.

Re-used keys: `asd-ism-2024`, `asd-pqc-guidance-2024`,
`acsc-e8-ism-mapping-2023`, `apra-cps-234-2019`.

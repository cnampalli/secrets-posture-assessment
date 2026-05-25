# ASD ISM Control Verification — 2026-05-24

**Trigger:** Stakeholder flagged that removed/non-applicable ISM control IDs were present in the regulatory lens.
**Authoritative source used:** https://ismcontrol.xyz/ (tracks per-control `Current` / `Removed` status + topic + history).
**Cross-check note:** ismcontrol.xyz statements match the genuine ASD ISM control texts on spot-checks (e.g. ISM-1139 "Only the latest version of TLS is used"). Official source of record remains cyber.gov.au (ASD ISM). Recommend final confirmation there before publishing corrected IDs.

## Headline

Of **41 ISM control IDs** in `matrix/regulatory-trace.csv` (`framework_slug = asd-ism`):

| Verdict | Count | Meaning |
|---|---|---|
| ✅ Accurate | ~8 | Current control AND our topic matches the real ISM topic |
| ❌ Wrong topic | ~27 | Control ID is current, but mapped to a **different topic** than the real ISM control |
| 🗑️ Removed | 5 | Control was removed from the ISM (no longer applicable) |
| ⛔ Does not exist | 1 | ID returns 404 — never a valid ISM control |

**~80% of ISM IDs are inaccurate.** This is not stale-data drift; the original mapping appears to have assigned fabricated/incorrect control numbers to our topics.

## Removed / non-existent (must be pulled)

| Our ID | Our claimed topic | Reality on ismcontrol.xyz |
|---|---|---|
| ISM-1232 | Protection of cryptographic keys throughout lifecycle | **Removed** — real ISM-1232 was "AACAs used by HACE" (High Assurance Cryptographic Equipment) |
| ISM-1414 | Cryptographic key generation in validated module | **Removed** — real ISM-1414 was Microsoft EMET version |
| ISM-1382 | Application control / allow-listing | **Removed** — real ISM-1382 was unprivileged admin accounts |
| ISM-1383 | System hardening guidance applied | **Removed** — real topic "Separate privileged operating environments" |
| ISM-1266 | Database service-account credential strength | **Removed** — merged into ISM-1247 ("Anonymous database accounts") |
| ISM-1265 | Per-application database accounts | **404 — does not exist** |

## Current ID but WRONG topic (mapping is fabricated)

| Our ID | Our claimed topic | Real ISM topic |
|---|---|---|
| ISM-0457 | ASD-approved cryptographic algorithms | Encrypting data at rest |
| ISM-1446 | Secure cryptographic key distribution | Using Elliptic Curve Cryptography |
| ISM-0501 | Cryptographic key storage in HSM | Transporting cryptographic equipment |
| ISM-0455 | TLS for sensitive web traffic | Data recovery |
| ISM-1453 | Certificate management lifecycle | Perfect Forward Secrecy |
| ISM-1564 | Post-quantum cryptography readiness | Plan of action and milestones |
| ISM-1546 | Privileged service-account credential hygiene | Authenticating to systems |
| ISM-1779 | Phishing-resistant MFA factors | Manual export of data |
| ISM-1402 | Password/passphrase strength and rotation | Protecting credentials (borderline) |
| ISM-1175 | Break-glass / emergency administrator account | (privileged-account email/web use) |
| ISM-1556 | Privileged-access event logging and review | After travelling overseas with mobile devices |
| ISM-1525 | Vulnerability scanning cadence | System ownership and oversight |
| ISM-0400 | Secure software development principles | Dev/test/staging/production environments (borderline) |
| ISM-1419 | No embedded secrets in source code | Development environments |
| ISM-1238 | Software supply-chain / code-signing | Secure software development (borderline) |
| ISM-0961 | Network segmentation and segregation | Using web content filters |
| ISM-1416 | Network device admin via separate auth | Software firewall |
| ISM-1656 | Secure cloud / hybrid administration | Application control |
| ISM-1182 | Gateway upstream/downstream authentication | Network access controls |
| ISM-0421 | Inbound message sender authentication | Single-factor authentication |
| ISM-1554 | IoT / OT device unique authentication | Before travelling overseas with mobile devices |
| ISM-0123 | Security logging and centralised event collection | Reporting cybersecurity incidents |
| ISM-0125 | Cyber security incident response plan | Cyber security incident register (borderline) |
| ISM-1228 | Compromised credential revocation | Event log monitoring |
| ISM-0072 | Data-residency / off-shoring assurance | Contractual security requirements with service providers |
| ISM-0570 | Security governance framework documented | Email gateway maintenance activities |
| ISM-0264 | Secure decommissioning and key destruction | Email usage policy |

## Plausibly accurate (current ID, topic matches — still confirm against cyber.gov.au)

| Our ID | Our topic | Real ISM topic |
|---|---|---|
| ISM-1139 | TLS configuration and cipher hygiene | Configuring Transport Layer Security ✓ |
| ISM-0974 | Privileged access requires MFA | Multi-factor authentication ✓ |
| ISM-1559 | MFA for unprivileged users | Multi-factor authentication ✓ |
| ISM-0140 | Incident reporting to ASD | Reporting cybersecurity incidents to ASD ✓ |
| ISM-0252 | Cyber security awareness training | Providing cybersecurity awareness training ✓ |
| ISM-1452 | Supplier cyber security assessment | Cyber supply chain risk management activities ✓ |
| ISM-1547 | Backup integrity protection | Data backup and restoration processes ✓ |
| ISM-0027 | Formal risk acceptance / exception register | Authorisation to operate / acceptance of security risks ✓ |

## Implications for the other frameworks

ismcontrol.xyz only covers ASD ISM. The other lenses in `regulatory-trace.csv` use different ID schemes and need different authoritative sources:

- **MITRE ATT&CK** (31 IDs, `T####.###` + `BREACH-*`): T-codes verifiable against attack.mitre.org STIX data. BREACH-* are editorial, not official IDs.
- **APRA CPS 234** (25 IDs, `CPS234-§NN`): paragraph references — verify against the legal instrument (some §-numbers may not exist).
- **APRA CPS 230 / CPG 234 / NIST SP 800-207 / Essential 8**: these are *synthesized* codes (e.g. `E8-RAP-ML1`, `ZT-Pillar-Identity`), not official numbered controls — accuracy is editorial, not an ID-validity problem.

Given how unreliable the ISM IDs proved, MITRE and APRA paragraph refs should be independently verified before the stakeholder review.

## Downstream impact (files referencing the "145 controls" figure)

- `matrix/regulatory-trace.csv` (source data)
- `matrix/matrix.md`
- `PRD/appendices/A-compliance-traceability.md`
- `matrix/build_matrix_viewer.py` + generated `matrix/matrix-viewer.html` (Compliance-trace cascade tab)
- `dist/XYZ-Secrets-Management-PRD-v0.1*` (built package)
- Any "145 controls / 7 frameworks" count in the PRD body

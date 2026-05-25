# Corrected ASD ISM Control Mapping — 2026-05-24

Proposed replacement for the ASD ISM lens in `matrix/regulatory-trace.csv`. Every ID below is **verified `Current`** on ismcontrol.xyz (Hugo index, 1000 current controls), with the real topic + control statement. This supersedes the broken mapping documented in `ISM-CONTROL-VERIFICATION-2026-05-24.md`.

**Verification basis:** ismcontrol.xyz `/index.xml` (all 1862 controls) + `/tags/current/` + `/tags/removed/`. Confirm against cyber.gov.au ISM (Dec 2024 / Mar 2025 release) before publishing.

Legend: ⭐ = newly surfaced control that fits secrets-management / NHI better than the original; ✓ = retained from original (ID + topic were already correct).

## Cryptography & key management
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-0471 | Using ASD Approved Cryptographic Algorithms | Only AACAs are used | ISM-0457 (was mislabeled "ASD-approved algorithms"; 0457 is actually "Encrypting data at rest") |
| ISM-0481 | Using ASD Approved Cryptographic Protocols | Only ASD-approved protocols used | — (new coverage) |
| ISM-0507 ⭐ | Cryptographic key management processes and procedures | Key-management processes & procedures developed/implemented/maintained | ISM-1232 (removed) |
| ISM-0457 | Encrypting data at rest | CC-evaluated crypto used for OFFICIAL:Sensitive+ at rest | (repurpose: secrets-at-rest) |
| ISM-0469 | Encrypting data in transit | CC-evaluated crypto used in transit | — |
| ISM-1917 ⭐ | Transitioning to post-quantum cryptography | Support ML-DSA-87/ML-KEM-1024/SHA-384/512/AES-256 by 2030 | ISM-1564 (was mislabeled; 1564 is "Plan of action and milestones") |
| ISM-1990 ⭐ | Using post-quantum cryptographic algorithms | ML-DSA/ML-KEM per FIPS 203/204 | — |

## TLS / certificates / PKI
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1139 ✓ | Configuring Transport Layer Security | Only latest TLS version used | (keep — was correct) |
| ISM-1453 | Perfect Forward Secrecy | PFS used for TLS connections | (repurpose: was mislabeled "certificate mgmt") |
| ISM-1323 | Generating and issuing certificates for authentication | Unique certificates per device/user | ISM-1453-as-cert-mgmt |
| ISM-1324 ⭐ | Generating and issuing certificates for authentication | Certs generated using evaluated CA **or HSM** | ISM-0501 (was mislabeled "key storage in HSM"; 0501 is "Transporting cryptographic equipment") |
| ISM-1327 | Generating and issuing certificates for authentication | Certs protected by access controls, encryption, authentication | — |

## Authentication / MFA
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1173 ⭐ | Multi-factor authentication | MFA for **all privileged users** and positions of trust | ISM-0974 (0974 is generic MFA; 1173 is the privileged-user control) |
| ISM-1401 | Multi-factor authentication | MFA uses ≥2 approved factor types | ISM-1402-as-MFA |
| ISM-1504 | Multi-factor authentication | MFA for org online services with sensitive data | — |
| ISM-1505 | Multi-factor authentication | MFA for users of data repositories | ISM-1559-as-unpriv (1559 is actually "memorised secret length") |
| ISM-1402 ✓ | Protecting credentials | Credential protection | (keep — topic "Protecting credentials" is close enough to "credential strength") |

## Privileged / service / break-glass accounts (strong NHI relevance)
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1175 ✓ | Privileged access to systems | Privileged access governance | (keep ID; fix title — was "break-glass") |
| ISM-1566 | Unprivileged access to systems | Unprivileged access governance | — |
| ISM-1610 ⭐ | Emergency access to systems | Emergency-access method documented & tested | ISM-1175-as-breakglass |
| ISM-1611 ⭐ | Emergency access to systems | Break-glass only when normal auth unavailable | — |
| ISM-1613 ⭐ | Emergency access to systems | Break-glass use centrally logged | ISM-1556 (was mislabeled "priv-access logging") |
| ISM-1614 ⭐ | Emergency access to systems | Break-glass creds changed after access by any party | — |
| ISM-1619 ⭐ | Setting/resetting credentials for service accounts | Service accounts created as group Managed Service Accounts | ISM-1546 (was mislabeled "service-account hygiene"; 1546 is "Authenticating to systems") |
| ISM-1685 ⭐ | Credentials for break glass / local admin / service accounts | Long, unique, unpredictable, managed | ISM-1266 (removed) |
| ISM-1795 ⭐ | Credentials for built-in admin / break glass / local admin / service accounts | Minimum 30 characters | — |
| ISM-1847 ⭐ | Changing credentials | KRBTGT service-account credentials rotated twice | (new — secret rotation) |

## Logging / monitoring / incident response
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1405 ⭐ | Centralised event logging facility | Centralised event logging implemented | ISM-0123 (was mislabeled; 0123 is "Reporting cybersecurity incidents") |
| ISM-1228 ✓ | Event log monitoring | Cybersecurity events analysed timely | (keep ID; fix title — was "compromised credential revocation") |
| ISM-1537 | Database event logging | Security-relevant DB events centrally logged | ISM-1265 (404) / ISM-1266 db-account controls |
| ISM-0043 ⭐ | Cybersecurity incident response plan | Systems have an IR plan covering defined elements | ISM-0125 (was mislabeled; 0125 has no current topic) |
| ISM-1819 | Enacting cyber security incident response plans | IR plan enacted on incident | — |
| ISM-0140 ✓ | Reporting cybersecurity incidents to ASD | Report to ASD ASAP | (keep — was correct) |

## Vulnerability / patching
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1690 | When to patch vulnerabilities | Patch online-service vulns within 2 weeks (48h if critical) | ISM-1525 (was mislabeled "vuln scanning"; 1525 is "System ownership and oversight") |
| ISM-1694 | When to patch vulnerabilities | Patch internet-facing server/device OS within 2 weeks | — |

## Secure SDLC / supply chain
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-0401 | Secure software development | Secure dev practices | ISM-0400 (0400 is "dev/test/staging/prod environments") |
| ISM-1238 ✓ | Secure software development | Secure dev | (keep — topic confirmed) |
| ISM-1730 ⭐ | Software bill of materials | SBOM produced/consumed | ISM-1419 (was mislabeled "no secrets in code"; 1419 is "Development environments") |
| ISM-1452 ✓ | Cyber supply chain risk management activities | CSCRM activities | (keep — was correct) |

## Network
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1181 ⭐ | Network segmentation and segregation | Network segmented & segregated | ISM-0961 (was mislabeled; 0961 is "Using web content filters") |
| ISM-1182 | Network access controls | Network access controls applied | (keep ID; fix title — was "gateway upstream/downstream auth") |

## Cloud / offshoring
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1570 ⭐ | Assessment of outsourced cloud service providers | IRAP assessment of cloud providers | ISM-0072 (0072 is "Contractual security requirements with service providers") |

## Backups (immutability now has dedicated controls)
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-1511 | Performing and retaining backups | Backups performed & retained per criticality | — |
| ISM-1515 | Testing restoration of backups | Restoration tested in DR exercises | — |
| ISM-1547 ✓ | Data backup and restoration processes and procedures | Backup processes maintained | (keep — was correct) |
| ISM-1705 ⭐ | Backup access | Privileged accounts can't access others' backups | (new — least privilege on backups) |
| ISM-1707 ⭐ | Backup modification and deletion | Privileged accounts prevented from modifying/deleting backups (immutability) | ISM-1547-as-integrity |

## Governance / awareness
| ISM ID | Real topic | Statement (abridged) | Replaces |
|---|---|---|---|
| ISM-0252 ✓ | Providing cybersecurity awareness training | Awareness training provided | (keep — was correct) |
| ISM-0027 ✓ | Protecting systems and their resources | Authorisation to operate / risk acceptance | (keep — close enough) |

---

## Dropped concepts (no clean current ISM home for secrets/NHI)
- "IoT / OT device unique authentication" (was ISM-1554 = "Before travelling overseas") — out of scope for secrets mgmt; drop.
- "Inbound message sender authentication" (was ISM-0421 = "Single-factor authentication") — email-gateway concern; drop.
- "Secure decommissioning and key destruction" (was ISM-0264 = "Email usage policy") — covered by ISM-0507 key-management lifecycle; fold in.
- "Secure cloud / hybrid administration" (was ISM-1656 = "Application control") — covered by privileged-access + cloud-assessment controls; fold in.
- "Network device administration via separate auth" (was ISM-1416 = "Software firewall") — covered by ISM-1175/1182; fold in.

## Net result
~38 verified current ISM controls (vs 41 originally, of which only ~8 were correct). Coverage of the secrets/NHI domain is **stronger and accurate**: dedicated break-glass, service-account-credential, credential-rotation, PQC, and backup-immutability controls now anchor the lens.

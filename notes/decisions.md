# Working notes — running decision log

Working notes accumulated during the build. Each major call is later
promoted into an ADR under `PRD/adrs/` at milestone close.

---

## 2026-05-20 — M1 kickoff (Wed AEST)

- **Workspace structure** confirmed per the approved plan (`meta/workflow.md`).
- **Legacy `GEMINI.md`** in the directory is unrelated AI-research-papers
  boilerplate. **Left in place but explicitly superseded by `README.md`.**
  (Consider deleting in a later session if the user confirms.)
- **iCloud / Drive sync** — assumed configured at the macOS level for
  `Desktop/Projects/DE/`. **Not verified by Claude.** Surface this as an
  open item in the M1 review for the user to confirm.
- **No git initialised** in the project directory. Per the plan: propose at
  M1 review whether to `git init` (recommended for version control on
  artifacts).
- **Stakeholder identity inside XYZ** — not yet specified. Folded into
  Task 0 questionnaire §A4.
- **FI 27 strategy** — user will brief later. Reserved subsection placeholder
  in PRD §17.

## Pending → promote to ADR at M1 close

- ADR-001 (format choice) — Enterprise + ADRs + Dual Matrix
- ADR-002 (identity taxonomy source) — CSA NHI WG + Gartner MIM + SPIFFE deltas
- ADR-003 (regulatory lens) — outcomes-first (E8 + ZT), back-map to CPS 234/ISM/CSF
- ADR-004 (vendor shortlist) — **updated 2026-05-22**: now **13 vendors + an NHI-discovery tier (5 vendors)** = 18 total candidates. See M2 scope below.
- ADR-005 (XYZ evidence policy) — real-where-public / anonymised-where-internal
- ADR-006 (scoring rubric) — Native / Add-on / Partner / Gap / N/A × Maturity 0-4

## 2026-05-22 — Vendor scope expanded (post-Task-0)

Driven by `task0/responses.md` findings:

1. **CyberArk PAM added as a 13th vendor row** (distinct from CyberArk
   Conjur). Rationale: PAM is the entrenched governance platform for AD
   service accounts at XYZ after the Vault rollback (§Q-I.03). The PRD
   must score PAM directly, not infer from Conjur.

2. **New "NHI discovery / governance" tier introduced** (5 vendors —
   Astrix Security, Entro Security, Oasis Security, Aembit, Clutch
   Security). Rationale: §C.00 headline finding — XYZ has no inventory
   layer above its vaults. PRD §16 needs a defensible recommendation,
   which requires explicit capability scoring of this emerging category.

3. **Dispatch sequence:**
   - **Wave 1 (FIRING NOW):** Vault Enterprise, CyberArk Conjur,
     CyberArk PAM, Delinea Secret Server — the 4 with strongest
     user-direct-experience grounding for cross-check.
   - **Wave 2 (next):** Cloud-native — AWS SM, Azure KV, GCP SM,
     AKEYLESS.
   - **Wave 3:** Doppler, Infisical, 1Password Secrets Automation,
     Venafi (incl. PKI/MIM lane), Keyfactor.
   - **Wave 4 (NHI discovery tier — added 2026-05-22):** Astrix, Entro,
     Oasis, Aembit, Clutch.

4. **CSV write strategy update:** each vendor agent writes to
   `matrix/vendor-capabilities-<slug>.csv` (per-vendor file), not the
   single shared `matrix/vendor-capabilities.csv`. Avoids parallel-write
   races. **Matrix Assembler (prompt 06)** at M3 concatenates per-vendor
   CSVs into the canonical `matrix/vendor-capabilities.csv`. Update to
   prompt 06 may be required at M3 to reflect this.

## 2026-05-22 (post-Wave-2) — Two scope adjustments

1. **AKEYLESS framing tightened.** Despite 21 NATIVE NHIs (competitive
   with the hyperscalers), **AKEYLESS has no AU SaaS region**; tier-1
   AU FIs must self-host the customer-Gateway component. No publicly
   named AU FI customers. This is a **material v0.1 concern** for XYZ
   per APRA CPS 234 + CPS 230 data-residency expectations.
   - PRD §11 Akeyless row: lead with capability strength + this
     residency caveat.
   - PRD §16 recommendations: AKEYLESS is **not a like-for-like
     replacement for Vault Enterprise** at XYZ until / unless a
     customer-controlled AU deployment can be operationalised.

2. **Fortanix DSM added as 19th vendor.** Promoted from v1.0 to v0.1.
   Two converging reasons:
   - **XYZ migrated from Thales SafeNet Luna → Fortanix** per Task 0
     §Q-D.04. Fortanix DSM is load-bearing in XYZ's current crypto
     posture.
   - **GCP Cloud EKM names Fortanix as a documented partner** —
     directly relevant if XYZ extends Fortanix as the BYOK control
     plane across hyperscalers.
   - Dispatched as part of Wave 4 (5 NHI-discovery vendors + Fortanix).
   - Vendor slug: `fortanix-dsm`.
   - Vendor tier: `data-security` (a new tier for HSM / DSM /
     tokenisation platforms).

   ADR-004 updated below to reflect the 19-vendor scope.

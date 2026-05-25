# Workflow (mirror of approved plan)

**Source of truth:**
`/Users/cnampalli/.claude/plans/wondrous-meandering-yao.md`

This file is a project-local mirror so reviewers can read the plan inside
this directory without leaving it. If the canonical plan and this file
diverge, the canonical plan wins — but in practice any change to the plan
will be reflected here by the same commit.

---

## TL;DR

Build a PRD whose **product is a Report** on secrets-management positioning
across **all machine identities**, for **XYZ Bank** as primary deployer, by
**Mon 2026-05-25** (v0.1) with deeper iteration the week after.

Three milestone gates:

1. **M1 — Outline + scaffolding** ✓ done 2026-05-21 (Thu).
2. **M2 — Matrices populated** ✓ done 2026-05-23 (Sat) — PASS-with-comments → fixes applied.
3. **M3 — PRD v0.1 ready** ✓ done 2026-05-23 (Sat, one day ahead).

PRD package: ~20,500 words across body + 6 ADRs + 4 appendices.

PRD format: **Enterprise + ADRs + DUAL MATRIX + compliance trace appendix**.
Primary lens: **Essential 8 maturity + NIST SP 800-207 Zero Trust**;
APRA CPS 234, ASD ISM, NIST CSF 2.0 back-mapped.

Research depth: **Maximal** — vendor docs + analyst + community + primary
regulatory text + breach post-mortems + adversary TTPs (MITRE ATT&CK T1552).

Vendor set (**19, expanded from original 12 — see ADR-004**):

- **Core (4):** HashiCorp Vault Enterprise, CyberArk Conjur, CyberArk PAM (separated post-Task-0), Delinea Secret Server.
- **Cloud-native (4):** AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, AKEYLESS.
- **Emerging (3):** Doppler, Infisical, 1Password Secrets Automation.
- **PKI/MIM (2):** Venafi (now CyberArk-owned), Keyfactor.
- **NHI discovery (5):** Astrix Security, Entro Security, Oasis Security, Aembit, Clutch Security.
- **Data security (1):** Fortanix DSM (promoted from v1.0 given XYZ HSM migration).

Identity scope: **Comprehensive NHI taxonomy** — workload, cloud IAM,
crypto identities, DevOps & runtime, RPA, AI agents, IoT/OT, mainframe,
B2B/partner, legacy.

Sensitivity policy: **real where publicly known, anonymised where
internal/sensitive** (per ADR-005).

---

## Sub-agent dispatch

| # | Role | Subagent type | Model | Concurrency |
|---|---|---|---|---|
| 00 | Task 0 questionnaire | main thread | Opus 4.7 | — |
| 01 | Identity Taxonomist | general-purpose | Opus 4.7 | serial |
| 02 | Use Case Catalog Builder | general-purpose | Opus 4.7 | serial |
| 03 | Vendor Researcher ×12 | general-purpose (WebSearch+WebFetch) | Sonnet 4.6 | 4-at-a-time waves |
| 04 | Regulatory Mapper ×5 | general-purpose (WebSearch) | Opus 4.7 | 5-way parallel |
| 05 | Adversary TTP Mapper | general-purpose (WebSearch) | Opus 4.7 | serial |
| 06 | Matrix Assembler | main thread | Opus 4.7 | — |
| 07 | XYZ Current-State Synthesizer | main thread | Opus 4.7 | — |
| 08 | PRD Writer | main thread | Opus 4.7 | — |
| 09 | PRD Reviewer (independent) | adapted reviewer | Opus 4.7 | per milestone |

Full prompts live in `../prompts/`. Every invocation gets one row in
`agents.md`.

---

## Durable operational rules (added 2026-05-20 mid-session by user)

### 70% checkpoint-and-handoff rule

**Every agent — sub-agent AND this main thread — must checkpoint and hand
off when its context window crosses ~70 % utilisation.** Saved to memory
as `feedback-70-percent-checkpoint-rule`. Full text in
`prompts/README.md` Invariant #8.

Practically:
- Sub-agents estimate via heuristics (output word count, tool call count,
  loop count) and write `_checkpoint-<NNN>.md` then signal
  `HANDOFF_NEEDED: <path>`.
- Main thread writes `meta/_main-checkpoint-<NNN>.md` and stops.
- Successor agent reads checkpoint, references same prompt file, continues.

### Session + weekly budget management

**Preserve daily and weekly budget across the multi-day project cadence.**
Saved to memory as `feedback-session-budget-management`. Specifically:

- v0.1 review is Mon 2026-05-25; work spans Wed 2026-05-20 → Sun 2026-05-24.
- Don't burn the daily session in one push; don't sprint past 50–60 %
  weekly utilisation early in the week.
- Cheap durable artifacts (memory, rules, checkpoints) before expensive
  ones (sub-agent dispatch, deep web fetching).
- End each session with `meta/_main-checkpoint-<NNN>.md` describing where
  we stopped and what tomorrow picks up.

### Session-start telemetry (2026-05-20 17:xx AEST)

User reported at mid-session pause:
- Current session: 7 % used, resets in ~4h15m.
- Weekly cloud context: 23 % used.
- Direction: "make sure that we should be able to work tomorrow as well…
  If not, save it until further instructions by me."

Implication: today, finish foundational artifacts (memory rules,
prompts 00–05, handoff checkpoint). Defer research sub-agent dispatch and
deeper artifacts (prompts 06–09, PRD skeleton, vendor research) to
tomorrow with a fresh session budget.

---

## Deferred from v0.1

- Industry-agnostic v2 (deferred until v1 stakeholder review).
- RFP/RFI derivation from PRD.
- Vendor TCO cost-modelling.
- XYZ remediation roadmap sequencing (only "what" is in v0.1).
- FI 27 strategy alignment detail (awaiting user briefing).
- Git initialisation (proposed at M1 user review; not yet assumed).
